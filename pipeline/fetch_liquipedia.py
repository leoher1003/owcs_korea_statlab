"""Fetch match results from Liquipedia into the workbook's MATCH INFO / POTM shape.

Usage:
    python3 pipeline/fetch_liquipedia.py                        # Stage 3 Korea -> tmp/liquipedia/*.csv
    python3 pipeline/fetch_liquipedia.py --compare site/data/data_s3.js
    python3 pipeline/fetch_liquipedia.py --week 2                # only Week 2 rows
    python3 pipeline/fetch_liquipedia.py --yesterday             # daily job -> tmp/liquipedia/<date>/
    python3 pipeline/fetch_liquipedia.py --page Overwatch_Champions_Series/2026/Asia/Stage_3/Korea --out tmp/liquipedia

Reads the wikitext of the tournament page (and the subpages it transcludes) through the
Liquipedia MediaWiki API
and parses every {{Match}} template. Field names follow Liquipedia's Overwatch match2 input
(Module:MatchGroup/Input/Custom): opponent1/2, date, mvp, mapN={{Map|map=|score1=|score2=|winner=|t1b1=|t2b1=}}.

Writes three CSVs (UTF-8 with BOM, so Excel opens Korean text correctly):
    match_info.csv  one row per played map, MATCH INFO columns (TIME comes from player rows, so it is not here)
    potm.csv        one row per series with an MVP, POTM sheet columns
    series.csv      one row per series: set score, winner, POTM (for checking at a glance)

Team codes, player names and roster positions come from the --roster site data file (teamInfo).
--compare diffs the fetched rows against an existing site data file and exits 1 on any difference.

Liquipedia API terms (https://liquipedia.net/api-terms-of-use): identifying User-Agent, gzip,
at most one request every 2 seconds, and cache results. Responses are cached in --cache for
--max-age seconds; a normal run makes 2 requests.
"""
import argparse
import csv
import datetime as dt
import gzip
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

API = "https://liquipedia.net/overwatch/api.php"
USER_AGENT = "OWCSKoreaStatLab/1.0 (https://github.com/leoher1003/owcs_korea_statlab)"
DEFAULT_PAGE = "Overwatch_Champions_Series/2026/Asia/Stage_3/Korea"
KST = ZoneInfo("Asia/Seoul")  # match dates on Liquipedia are Korean dates, whatever the local timezone
REQUEST_GAP = 2.1  # seconds between API calls (Liquipedia limit: 1 request / 2 s)

MATCH_INFO_COLS = ["WEEK", "DAY", "MATCH", "Set #", "DATE", "PHASE", "TEAM 1", "TEAM 2", "MAP", "MAP TYPE",
                   "WINNER", "TEAM 1 BAN", "TEAM 2 BAN", "MATCH_ID", "TEAM 1 SCORE", "TEAM 2 SCORE"]
POTM_COLS = ["Date", "Match", "POTM", "Position"]
SERIES_COLS = ["WEEK", "DAY", "MATCH", "DATE", "PHASE", "TEAM 1", "TEAM 2", "TEAM 1 SETS", "TEAM 2 SETS",
               "WINNER", "POTM", "LIQUIPEDIA PAGE"]

MAP_TYPES = {
    "Antarctic Peninsula": "Control", "Busan": "Control", "Ilios": "Control", "Lijiang Tower": "Control",
    "Nepal": "Control", "Oasis": "Control", "Samoa": "Control",
    "Blizzard World": "Hybrid", "Eichenwalde": "Hybrid", "Hollywood": "Hybrid", "King's Row": "Hybrid",
    "Midtown": "Hybrid", "Neon Junction": "Hybrid", "Numbani": "Hybrid", "Paraiso": "Hybrid",
    "Circuit Royal": "Escort", "Dorado": "Escort", "Havana": "Escort", "Junkertown": "Escort",
    "Rialto": "Escort", "Route 66": "Escort", "Shambali Monastery": "Escort", "Watchpoint: Gibraltar": "Escort",
    "Colosseo": "Push", "Esperanca": "Push", "New Queen Street": "Push", "Runasapi": "Push",
    "Aatlis": "Flashpoint", "New Junk City": "Flashpoint", "Suravasa": "Flashpoint",
}

# Heroes that may appear as bans; Liquipedia accepts aliases, so match loosely (see norm()).
HEROES = [
    "D.Va", "Doomfist", "Domina", "D.Mon", "Hazard", "Junker Queen", "Mauga", "Orisa", "Ramattra", "Reinhardt",
    "Roadhog", "Sigma", "Winston", "Wrecking Ball", "Zarya",
    "Anran", "Ashe", "Bastion", "Cassidy", "Echo", "Emre", "Freja", "Genji", "Hanzo", "Junkrat", "Mei",
    "Pharah", "Reaper", "Shion", "Sojourn", "Soldier: 76", "Sombra", "Symmetra", "Torbjörn", "Tracer",
    "Vendetta", "Venture", "Widowmaker",
    "Ana", "Baptiste", "Brigitte", "Illari", "Jetpack Cat", "Juno", "Kiriko", "Lifeweaver", "Lucio",
    "Mercy", "Moira", "Wuyang", "Zenyatta",
    "Doctrine", "Mizuki", "Sierra",
]
HERO_ALIASES = {"dva": "D.Va", "hammond": "Wrecking Ball", "ball": "Wrecking Ball", "soldier": "Soldier: 76",
                "soldier76": "Soldier: 76", "torb": "Torbjörn", "rammatra": "Ramattra", "mccree": "Cassidy",
                "brig": "Brigitte", "bap": "Baptiste", "zen": "Zenyatta", "widow": "Widowmaker",
                "jq": "Junker Queen", "lw": "Lifeweaver", "doom": "Doomfist", "rein": "Reinhardt"}

# Liquipedia team names that differ from the TEAM INFO sheet
TEAM_ALIASES = {"ZANSIDE Gaming": "ROZE"}

MONTHS = {m: i for i, m in enumerate(["january", "february", "march", "april", "may", "june", "july", "august",
                                      "september", "october", "november", "december"], 1)}


def norm(s):
    """Lowercase, strip accents and everything but letters/digits: 'Esperança' -> 'esperanca'."""
    s = str(s).translate(str.maketrans({"ø": "o", "Ø": "O", "æ": "ae", "Æ": "AE", "ß": "ss"}))
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", s.lower())


MAP_BY_NORM = {norm(m): m for m in MAP_TYPES}
HERO_BY_NORM = {**{norm(h): h for h in HEROES}, **HERO_ALIASES}


# --------------------------------------------------------------------------- API + cache

class Liquipedia:
    def __init__(self, cache_dir, max_age):
        self.cache_dir, self.max_age, self.last = cache_dir, max_age, 0.0
        os.makedirs(cache_dir, exist_ok=True)

    def get(self, **params):
        params = {"format": "json", "formatversion": "2", **params}
        query = urllib.parse.urlencode(sorted(params.items()))
        path = os.path.join(self.cache_dir, hashlib.sha1(query.encode()).hexdigest()[:16] + ".json")
        if os.path.exists(path) and time.time() - os.path.getmtime(path) < self.max_age:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        wait = self.last + REQUEST_GAP - time.time()
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(f"{API}?{query}", headers={"User-Agent": USER_AGENT,
                                                               "Accept-Encoding": "gzip"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip":
                body = gzip.decompress(body)
        self.last = time.time()
        data = json.loads(body)
        if "error" in data:
            sys.exit(f"Liquipedia API error: {data['error']}")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        return data

    def wikitext(self, titles):
        data = self.get(action="query", prop="revisions", rvprop="content", rvslots="main",
                        titles="|".join(titles))
        pages = {p["title"]: p for p in data["query"]["pages"]}
        return {t: pages[t]["revisions"][0]["slots"]["main"]["content"]
                for t in titles if t in pages and not pages[t].get("missing")}

    def tournament_wikitext(self, page):
        """Wikitext of the page plus the pages it transcludes, e.g. {{#section:Page/Regular Season|...}}."""
        page = page.replace("_", " ")
        main = self.wikitext([page]).get(page)
        if main is None:
            sys.exit(f"Liquipedia page not found: {page}")
        subs = []
        # {{:Page}}, {{/Sub}} and labeled-section transclusion: {{#section:Page|name}}, #section-h, #lst, #lsth
        pattern = r"\{\{\s*(#(?:section|section-h|lst|lsth)\s*:\s*)?([:/]?[^|{}#]+?)\s*[|}]"
        for m in re.finditer(pattern, strip_comments(main)):
            t = m.group(2).strip()
            if t.startswith("/"):
                t = page + t
            elif t.startswith(":"):
                t = t[1:].strip()
            elif not m.group(1):
                continue  # an ordinary template such as {{Abbr/KST}}
            t = t.replace("_", " ")
            if t not in subs and t != page:
                subs.append(t)
        texts = self.wikitext(subs) if subs else {}
        return [(page, main)] + [(t, texts[t]) for t in subs if t in texts]


# --------------------------------------------------------------------------- wikitext parsing

def balanced(text, start):
    """Index just past the '}}' closing the template that opens at text[start] ('{{')."""
    depth, i = 0, start
    while i < len(text) - 1:
        pair = text[i:i + 2]
        if pair == "{{":
            depth, i = depth + 1, i + 2
        elif pair == "}}":
            depth, i = depth - 1, i + 2
            if depth == 0:
                return i
        else:
            i += 1
    raise ValueError(f"unbalanced template at offset {start}")


def split_params(body):
    """Split a template body on top-level '|' (ignoring pipes inside {{ }} and [[ ]])."""
    parts, depth, cur, i = [], 0, [], 0
    while i < len(body):
        pair = body[i:i + 2]
        if pair in ("{{", "[["):
            depth += 1
            cur.append(pair)
            i += 2
        elif pair in ("}}", "]]"):
            depth -= 1
            cur.append(pair)
            i += 2
        elif body[i] == "|" and depth == 0:
            parts.append("".join(cur))
            cur, i = [], i + 1
        else:
            cur.append(body[i])
            i += 1
    parts.append("".join(cur))
    return parts


def strip_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def template(text):
    """'{{Name|a|k=v}}' -> (name, {1: 'a', 'k': 'v'})."""
    text = text.strip()
    if not (text.startswith("{{") and text.endswith("}}")):
        return None, {}
    parts = split_params(text[2:-2])
    params, pos = {}, 1
    for p in parts[1:]:
        k, eq, v = p.partition("=")
        if eq and "{{" not in k:
            params[k.strip().lower()] = v.strip()
        else:
            params[pos] = p.strip()
            pos += 1
    return parts[0].strip(), params


def find_templates(text, name):
    """All top-level-or-nested occurrences of {{name ...}} (exact name, case-insensitive), in order."""
    out = []
    for m in re.finditer(r"\{\{\s*" + re.escape(name) + r"\s*(?=[|}])", text, flags=re.I):
        out.append((m.start(), text[m.start():balanced(text, m.start())]))
    return out


PHASE_RULES = [  # (pattern in the section heading or Matchlist/Bracket title, PHASE value), first match wins
    (r"last chance|\blcq\b", "LCQ"),
    (r"\b2nd\b|second", "2nd RR"),
    (r"playoff|final|bracket", "Playoffs"),
]


def phases(text):
    """[(offset, phase)] for every section heading and Matchlist/Bracket, read with PHASE_RULES.

    Bracket templates default to Playoffs and everything else to Round Robin.
    """
    marks = []
    for m in re.finditer(r"^(=+)\s*(.*?)\s*\1\s*$", text, flags=re.M):
        marks.append((m.start(), m.group(2), None))
    for m in re.finditer(r"\{\{\s*(Matchlist|Bracket)\b", text, flags=re.I):
        _, params = template(text[m.start():balanced(text, m.start())])
        marks.append((m.start(), params.get("title", ""), "Playoffs" if m.group(1).lower() == "bracket" else None))
    out, heading = [], "Round Robin"
    for off, label, default in sorted(marks, key=lambda x: x[0]):
        phase = next((v for pat, v in PHASE_RULES if re.search(pat, label, flags=re.I)), None)
        if default is None and phase is None and label:
            phase = "Round Robin" if re.search(r"week|round robin|regular|group", label, flags=re.I) else None
        if default is None and phase:  # a heading or Matchlist title sets the phase for what follows
            heading = phase
        out.append((off, phase or default or heading))
    return out


def parse_date(raw):
    """'October 2, 2026 - 17:00 {{Abbr/KST}}' -> (date, 'HH:MM' or '')."""
    raw = re.sub(r"\{\{.*?\}\}", "", raw or "").strip()
    m = re.match(r"([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})(?:\s*-\s*(\d{1,2}:\d{2}))?", raw)
    if m and m.group(1).lower() in MONTHS:
        return dt.date(int(m.group(3)), MONTHS[m.group(1).lower()], int(m.group(2))), m.group(4) or ""
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})(?:[ T](\d{1,2}:\d{2}))?", raw)
    if m:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))), m.group(4) or ""
    return None, ""


def opponent_name(raw):
    name, params = template(raw)
    if not name:
        return raw.strip()
    return (params.get(1) or params.get("template") or params.get("name") or "").strip()


def parse_matches(pages):
    """Every {{Match}} with both teams named, in page order.

    `finished` is true once a team has won a majority of `bestof` maps (bestof carries over from the
    previous match, as on Liquipedia); unfinished ones are left out of the CSVs.
    """
    matches, seen, bestof = [], set(), 5
    for title, text in pages:
        text = strip_comments(text)
        marks = phases(text)
        for offset, raw in find_templates(text, "Match"):
            _, p = template(raw)
            if p.get("bestof", "").isdigit():
                bestof = int(p["bestof"])
            team1, team2 = opponent_name(p.get("opponent1", "")), opponent_name(p.get("opponent2", ""))
            if not (team1 and team2):
                continue  # placeholder for a match whose teams are not known yet
            phase = next((ph for off, ph in reversed(marks) if off < offset), "Round Robin")
            date, clock = parse_date(p.get("date"))
            maps = []
            for i in range(1, 10):
                mraw = p.get(f"map{i}")
                if not mraw:
                    break
                _, mp = template(mraw)
                if not mp.get("map") or mp.get("map", "").lower() in ("tbd", "tba"):
                    break
                s1, s2 = mp.get("score1", ""), mp.get("score2", "")
                if not (s1 or s2 or mp.get("winner")):
                    break  # not played yet
                maps.append({"map": mp["map"], "score1": s1, "score2": s2, "winner": mp.get("winner", ""),
                             "t1b1": mp.get("t1b1", ""), "t2b1": mp.get("t2b1", "")})
            key = (date, team1, team2)
            if key in seen:  # the same page can be transcluded more than once
                continue
            seen.add(key)
            wins = [sum(map_winner(m) == side for m in maps) for side in (1, 2)]
            mvp = [x.split("|")[0].strip() for x in (p.get("mvp") or "").split(",") if x.strip()]
            matches.append({"page": title, "phase": phase, "date": date, "time": clock,
                            "team1": team1, "team2": team2, "maps": maps, "mvp": mvp,
                            "finished": max(wins) > bestof // 2})
    return matches


# --------------------------------------------------------------------------- mapping to the workbook

def load_site_data(path):
    with open(path, encoding="utf-8") as f:
        s = f.read()
    return json.loads(s[s.index("=") + 1:].rstrip().rstrip(";"))


class Roster:
    """Team codes and player positions from a site data file's teamInfo."""

    def __init__(self, data, team_aliases):
        self.team, self.players, self.notes = {}, {}, []
        for r in data.get("teamInfo", []):
            if r.get("Team Name"):
                code = r["Shortened"]
                self.team[norm(r["Team Name"])] = self.team[norm(code)] = code
            elif r.get("Player Name"):
                base = re.sub(r" \((TANK|DPS|SPT)\)$", "", r["Player Name"])
                self.players.setdefault(norm(base), (base, set()))[1].add(r["Player Position"])
        for alias, code in team_aliases.items():
            self.team[norm(alias)] = code

    def team_code(self, name, problems):
        code = self.team.get(norm(name))
        if not code:
            problems.append(f"unknown team '{name}' (add it with --team-alias '{name}=CODE')")
            return name.upper()
        return code

    def player(self, name, problems):
        hit = self.players.get(norm(name))
        if not hit:
            problems.append(f"POTM '{name}' is not on any roster; position left blank")
            return name.upper(), ""
        base, positions = hit
        if len(positions) > 1:
            self.notes.append(f"POTM {base} played {sorted(positions)}; fill Position by hand")
            return base, ""
        return base, next(iter(positions))


def map_name(raw, problems):
    name = MAP_BY_NORM.get(norm(raw))
    if not name:
        problems.append(f"unknown map '{raw}' (add it to MAP_TYPES)")
        return raw, ""
    return name, MAP_TYPES[name]


def hero_name(raw, problems):
    if not raw:
        return ""
    name = HERO_BY_NORM.get(norm(raw))
    if not name:
        problems.append(f"unknown hero ban '{raw}' (add it to HEROES or HERO_ALIASES)")
        return raw
    return name


def score_text(raw):
    """'141.97m' -> '141.97', '2' -> '2' (same text as the site's TEAM n SCORE)."""
    v = raw.strip().rstrip("m").strip()
    try:
        f = float(v)
    except ValueError:
        return v
    return str(int(f)) if f.is_integer() else f"{f:.2f}"


def map_winner(m):
    if m["winner"] in ("1", "2"):
        return int(m["winner"])
    try:
        a, b = float(score_text(m["score1"])), float(score_text(m["score2"]))
    except ValueError:
        return 0
    return 1 if a > b else 2 if b > a else 0


def build_rows(matches, roster):
    problems = []
    matches = sorted(matches, key=lambda m: (m["date"] or dt.date.max, m["time"]))  # stable: keeps page order
    if any(m["date"] is None for m in matches):
        problems.append("some matches have no parseable date; they are numbered last")
    first = next((m["date"] for m in matches if m["date"]), None)
    # week = 7-day block from the first match day; day = n-th match date in that week; match = n-th series that day
    week_days, day_count = {}, {}
    info, potm, series = [], [], []
    for m in matches:
        d = m["date"]
        week = (d - first).days // 7 + 1 if d else 0
        days = week_days.setdefault(week, [])
        if d not in days:
            days.append(d)
        day = days.index(d) + 1
        day_count[(week, day)] = day_count.get((week, day), 0) + 1
        no = day_count[(week, day)]
        t1, t2 = roster.team_code(m["team1"], problems), roster.team_code(m["team2"], problems)
        date_s = d.isoformat() if d else ""
        prefix = d.strftime("%y%m%d") if d else "000000"
        sets = [0, 0]
        for i, mp in enumerate(m["maps"], 1):
            name, mtype = map_name(mp["map"], problems)
            w = map_winner(mp)
            if not w:
                problems.append(f"{date_s} {t1} vs {t2} map {i} ({name}): no winner")
            else:
                sets[w - 1] += 1
            info.append({"WEEK": week, "DAY": day, "MATCH": no, "Set #": i, "DATE": date_s, "PHASE": m["phase"],
                         "TEAM 1": t1, "TEAM 2": t2, "MAP": name, "MAP TYPE": mtype,
                         "WINNER": {1: t1, 2: t2}.get(w, ""),
                         "TEAM 1 BAN": hero_name(mp["t1b1"], problems),
                         "TEAM 2 BAN": hero_name(mp["t2b1"], problems),
                         "MATCH_ID": f"{prefix}_{t1}_{t2}_S{i}",
                         "TEAM 1 SCORE": score_text(mp["score1"]), "TEAM 2 SCORE": score_text(mp["score2"])})
        mvps = [roster.player(x, problems) for x in m["mvp"]]
        for name, pos in mvps:
            potm.append({"Date": date_s, "Match": f"{t1}_{t2}", "POTM": name, "Position": pos})
        series.append({"WEEK": week, "DAY": day, "MATCH": no, "DATE": date_s, "PHASE": m["phase"],
                       "TEAM 1": t1, "TEAM 2": t2, "TEAM 1 SETS": sets[0], "TEAM 2 SETS": sets[1],
                       "WINNER": t1 if sets[0] > sets[1] else t2 if sets[1] > sets[0] else "",
                       "POTM": ", ".join(n for n, _ in mvps), "LIQUIPEDIA PAGE": m["page"]})
    return info, potm, series, problems


# --------------------------------------------------------------------------- output

def write_csv(path, cols, rows):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def compare(info, potm, data, weeks=None, date=None):
    """Differences between fetched rows and a site data file (limited to `weeks` / `date` when given)."""
    diffs = []
    site_info = [r for r in data.get("matchInfo", [])
                 if (not weeks or r["WEEK"] in weeks) and (not date or r["DATE"] == date.isoformat())]
    have = {r["MATCH_ID"]: r for r in site_info}
    keys = [c for c in MATCH_INFO_COLS if c != "MATCH_ID"]
    for r in info:
        old = have.pop(r["MATCH_ID"], None)
        if old is None:
            diffs.append(f"new on Liquipedia: {r['MATCH_ID']} ({r['MAP']})")
            continue
        for k in keys:
            if str(old.get(k, "")) != str(r[k]):
                diffs.append(f"{r['MATCH_ID']} {k}: site {old.get(k)!r} vs Liquipedia {r[k]!r}")
    diffs += [f"only in site data: {mid}" for mid in have]
    dates = {r["DATE"] for r in site_info}
    old_potm = {(p["Date"], p["Match"]): re.sub(r" \((TANK|DPS|SPT)\)$", "", p["POTM"])
                for p in data.get("potm", []) if not (weeks or date) or p["Date"] in dates}
    for p in potm:
        old = old_potm.pop((p["Date"], p["Match"]), None)
        if old is None:
            diffs.append(f"new POTM on Liquipedia: {p['Date']} {p['Match']} {p['POTM']}")
        elif norm(old) != norm(p["POTM"]):
            diffs.append(f"POTM {p['Date']} {p['Match']}: site {old!r} vs Liquipedia {p['POTM']!r}")
    diffs += [f"POTM only in site data: {d} {m}" for d, m in old_potm]
    return diffs


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--page", default=DEFAULT_PAGE, help="Liquipedia page title (transcluded subpages are included)")
    ap.add_argument("--roster", default="site/data/data_s3.js", help="site data file with teamInfo")
    ap.add_argument("--out", help="output folder for the CSVs (default tmp/liquipedia, or tmp/liquipedia/<date>)")
    ap.add_argument("--cache", default="tmp/liquipedia/cache", help="API response cache folder")
    ap.add_argument("--max-age", type=int, default=600, help="seconds a cached response stays fresh")
    ap.add_argument("--team-alias", action="append", default=[], metavar="NAME=CODE",
                    help="extra Liquipedia team name -> team code mapping")
    ap.add_argument("--wikitext", nargs="+", metavar="FILE",
                    help="parse saved wikitext files instead of calling the API (offline)")
    ap.add_argument("--week", type=int, action="append", help="only write these weeks (repeatable)")
    ap.add_argument("--date", type=dt.date.fromisoformat, help="only write matches played on this date (YYYY-MM-DD)")
    ap.add_argument("--yesterday", action="store_true", help="--date of yesterday in Korea (for the daily job)")
    ap.add_argument("--compare", metavar="SITE_DATA_JS", help="diff against an existing site data file")
    args = ap.parse_args(argv)
    if args.yesterday:
        args.date = dt.datetime.now(KST).date() - dt.timedelta(days=1)
    if args.out is None:
        args.out = f"tmp/liquipedia/{args.date}" if args.date else "tmp/liquipedia"

    if args.wikitext:
        pages = []
        for path in args.wikitext:
            with open(path, encoding="utf-8") as f:
                pages.append((os.path.basename(path), f.read()))
    else:
        pages = Liquipedia(args.cache, args.max_age).tournament_wikitext(args.page)

    aliases = {**TEAM_ALIASES, **dict(a.split("=", 1) for a in args.team_alias)}
    roster = Roster(load_site_data(args.roster), aliases)
    matches = parse_matches(pages)
    played = [m for m in matches if m["finished"]]
    info, potm, series, problems = build_rows(played, roster)
    unfinished = [m for m in matches if not m["finished"] and m["maps"]]
    if args.date:  # the daily job: everything scheduled that day must be over
        unfinished = [m for m in matches if not m["finished"] and m["date"] == args.date]
    # numbering is computed on the whole stage first, so filtered rows keep their real WEEK/DAY/MATCH
    if args.week:
        info = [r for r in info if r["WEEK"] in args.week]
        series = [r for r in series if r["WEEK"] in args.week]
    if args.date:
        info = [r for r in info if r["DATE"] == args.date.isoformat()]
        series = [r for r in series if r["DATE"] == args.date.isoformat()]
    if args.week or args.date:
        keep = {(s["DATE"], f"{s['TEAM 1']}_{s['TEAM 2']}") for s in series}
        potm = [p for p in potm if (p["Date"], p["Match"]) in keep]

    os.makedirs(args.out, exist_ok=True)
    write_csv(os.path.join(args.out, "match_info.csv"), MATCH_INFO_COLS, info)
    write_csv(os.path.join(args.out, "potm.csv"), POTM_COLS, potm)
    write_csv(os.path.join(args.out, "series.csv"), SERIES_COLS, series)
    print(f"{len(pages)} page(s), {len(series)} series, {len(info)} maps, {len(potm)} POTM -> {args.out}/")
    for s in series:
        print(f"  W{s['WEEK']} D{s['DAY']} M{s['MATCH']} {s['DATE']} {s['TEAM 1']} {s['TEAM 1 SETS']}:"
              f"{s['TEAM 2 SETS']} {s['TEAM 2']}  POTM {s['POTM'] or '-'}")

    notes = [n for n in dict.fromkeys(roster.notes) if any(f"POTM {p['POTM']} " in n for p in potm)]
    if notes:
        print("NOTES:\n  " + "\n  ".join(notes))
    failed = bool(problems)
    if unfinished:
        print("NOT FINISHED ON LIQUIPEDIA YET (left out):\n  " + "\n  ".join(
            f"{m['date']} {m['team1']} vs {m['team2']} ({len(m['maps'])} map(s) entered)" for m in unfinished))
        failed = failed or bool(args.date)
    if args.date and not series and not unfinished:
        print(f"no matches on {args.date} on Liquipedia")
    if problems:
        print("PROBLEMS:\n  " + "\n  ".join(dict.fromkeys(problems)))
    if args.compare:
        diffs = compare(info, potm, load_site_data(args.compare), args.week, args.date)
        print(f"COMPARE with {args.compare}: " + ("no differences" if not diffs else f"{len(diffs)} difference(s)"))
        for d in diffs:
            print("  " + d)
        failed = failed or bool(diffs)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
