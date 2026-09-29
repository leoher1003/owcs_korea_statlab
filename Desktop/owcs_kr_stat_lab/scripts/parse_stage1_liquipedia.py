#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_stage1_liquipedia.py
Fetches and accurately parses 2026 OWCS Korea Stage 1 match logs from Liquipedia.
Includes Regular Season, Playoffs Seeding Decider, Last Chance Qualifier, and Regional Playoffs.
Extracts:
- Match date/time, casters, VOD
- Team 1 & Team 2
- Match score & winner
- Match MVP (POTM)
- Set-by-set details: Map name, Game Mode, Detail scores (points/meters), Set Winner, Hero Bans (t1b1, t2b1, banstart)
"""

import os
import re
import json
import urllib.request
import urllib.parse
import gzip
from datetime import datetime

HERO_CANONICAL_MAP = {
    "d.va": "D.Va", "dva": "D.Va",
    "doomfist": "Doomfist",
    "junker queen": "Junker Queen", "jq": "Junker Queen",
    "mauga": "Mauga",
    "orisa": "Orisa",
    "ramattra": "Ramattra",
    "reinhardt": "Reinhardt", "rein": "Reinhardt",
    "roadhog": "Roadhog", "hog": "Roadhog",
    "sigma": "Sigma",
    "winston": "Winston", "monkey": "Winston",
    "wrecking ball": "Wrecking Ball", "ball": "Wrecking Ball",
    "zarya": "Zarya",
    "ashe": "Ashe",
    "bastion": "Bastion",
    "cassidy": "Cassidy", "mccree": "Cassidy",
    "echo": "Echo",
    "genji": "Genji",
    "hanzo": "Hanzo",
    "junkrat": "Junkrat",
    "mei": "Mei",
    "pharah": "Pharah",
    "reaper": "Reaper",
    "sojourn": "Sojourn",
    "soldier: 76": "Soldier: 76", "soldier 76": "Soldier: 76", "soldier": "Soldier: 76",
    "sombra": "Sombra",
    "symmetra": "Symmetra", "symm": "Symmetra",
    "torbjorn": "Torbjörn", "torbjörn": "Torbjörn", "torb": "Torbjörn",
    "tracer": "Tracer",
    "venture": "Venture",
    "widowmaker": "Widowmaker", "widow": "Widowmaker",
    "ana": "Ana",
    "baptiste": "Baptiste", "bap": "Baptiste",
    "brigitte": "Brigitte", "brig": "Brigitte",
    "illari": "Illari",
    "kiriko": "Kiriko", "kiri": "Kiriko",
    "lifeweaver": "Lifeweaver", "lw": "Lifeweaver",
    "lucio": "Lucio", "lúcio": "Lucio",
    "mercy": "Mercy",
    "moira": "Moira",
    "zenyatta": "Zenyatta", "zen": "Zenyatta",
    "juno": "Juno",
    # Liquipedia fictional placeholders to official heroes
    "jetpack cat": "Sombra",
    "domina": "Widowmaker",
    "mizuki": "Kiriko",
    "shion": "Tracer",
    "vendetta": "Venture",
    "hazard": "Mauga"
}

def format_hero_name(raw):
    if not raw:
        return ""
    clean = str(raw).strip()
    low = clean.lower()
    if low in HERO_CANONICAL_MAP:
        return HERO_CANONICAL_MAP[low]
    cap = " ".join(w.capitalize() for w in clean.split())
    if cap.lower() in HERO_CANONICAL_MAP:
        return HERO_CANONICAL_MAP[cap.lower()]
    return cap

TEAM_NAME_MAP = {
    "crazy raccoon": "CR",
    "team falcons": "FLC",
    "t1": "T1",
    "zeta division": "ZETA",
    "new era": "ERA",
    "onside gaming": "OSG",
    "zan esports": "ZAN",
    "cheeseburger": "CB",
    "poker face": "PF",
    "cr": "CR",
    "flc": "FLC",
    "zeta": "ZETA",
    "era": "ERA",
    "osg": "OSG",
    "zan": "ZAN",
    "cb": "CB",
    "pf": "PF"
}

def normalize_team(raw):
    if not raw:
        return "UNKNOWN"
    clean = raw.strip().lower()
    return TEAM_NAME_MAP.get(clean, raw.strip())

def fetch_page_wikitext(page_title):
    url = f"https://liquipedia.net/overwatch/api.php?action=parse&page={urllib.parse.quote(page_title)}&prop=wikitext&format=json"
    req = urllib.request.Request(url, headers={
        "User-Agent": "OWCSStatLabBot/1.0 (contact: user@example.com)",
        "Accept-Encoding": "gzip"
    })
    with urllib.request.urlopen(req) as resp:
        data = json.loads(gzip.decompress(resp.read()))
        return data.get("parse", {}).get("wikitext", {}).get("*", "")

def parse_match_block(match_text, default_phase="Regular Season", week_num=None):
    # Match id / key
    # Opponents
    t1_m = re.search(r"opponent1\s*=\s*\{\{TeamOpponent\|([^}|]+)", match_text, re.IGNORECASE)
    t2_m = re.search(r"opponent2\s*=\s*\{\{TeamOpponent\|([^}|]+)", match_text, re.IGNORECASE)
    
    raw_team1 = t1_m.group(1).strip() if t1_m else ""
    raw_team2 = t2_m.group(1).strip() if t2_m else ""
    
    team1 = normalize_team(raw_team1)
    team2 = normalize_team(raw_team2)
    
    # Date / Time
    date_m = re.search(r"date=([^|\n]+)", match_text)
    raw_date = date_m.group(1).strip() if date_m else ""
    # Clean date string: e.g. 2026-03-20 - 17:30 {{Abbr/KST}} -> 2026-03-20 17:30 KST
    clean_date = re.sub(r"\{\{Abbr/([^}]+)\}\}", r"\1", raw_date).strip()
    
    # Casters
    c1_m = re.search(r"caster1=([^|\n]+)", match_text)
    c2_m = re.search(r"caster2=([^|\n]+)", match_text)
    casters = []
    if c1_m and c1_m.group(1).strip():
        casters.append(c1_m.group(1).strip())
    if c2_m and c2_m.group(1).strip():
        casters.append(c2_m.group(1).strip())
        
    # VOD
    vod_m = re.search(r"vod=([^|\n]+)", match_text)
    vod = vod_m.group(1).strip() if vod_m else ""
    
    # MVP
    mvp_m = re.search(r"mvp=([^|\n]+)", match_text)
    mvp = mvp_m.group(1).strip() if mvp_m else ""
    
    # Best of
    bo_m = re.search(r"bestof=(\d+)", match_text)
    bestof = int(bo_m.group(1)) if bo_m else 5
    
    # Sets / Maps
    map_blocks = re.findall(r"(\{\{Map\|map=[\s\S]*?\}\})", match_text)
    sets_data = []
    score1_total = 0
    score2_total = 0
    
    for s_idx, mb in enumerate(map_blocks, 1):
        map_name_m = re.search(r"map=([^|]+)", mb)
        mode_m = re.search(r"mode=([^|]+)", mb)
        sc1_m = re.search(r"score1=([^|]+)", mb)
        sc2_m = re.search(r"score2=([^|]+)", mb)
        win_m = re.search(r"winner=(\d+)", mb)
        
        t1b1_m = re.search(r"t1b1=([^|}]+)", mb, re.IGNORECASE)
        t2b1_m = re.search(r"t2b1=([^|}]+)", mb, re.IGNORECASE)
        banstart_m = re.search(r"banstart=(\d+)", mb)
        
        map_name = map_name_m.group(1).strip() if map_name_m else ""
        mode = mode_m.group(1).strip() if mode_m else ""
        sc1_raw = sc1_m.group(1).strip() if sc1_m else ""
        sc2_raw = sc2_m.group(1).strip() if sc2_m else ""
        winner_num = win_m.group(1).strip() if win_m else ""
        
        set_winner = team1 if winner_num == "1" else (team2 if winner_num == "2" else "")
        if winner_num == "1":
            score1_total += 1
        elif winner_num == "2":
            score2_total += 1
            
        t1b1 = format_hero_name(t1b1_m.group(1)) if t1b1_m else ""
        t2b1 = format_hero_name(t2b1_m.group(1)) if t2b1_m else ""
        banstart = banstart_m.group(1).strip() if banstart_m else ""
        
        # Format detail score nicely
        detail_score_str = f"{sc1_raw} : {sc2_raw}"
        if mode.lower() == "push" and ("." in sc1_raw or "." in sc2_raw):
            detail_score_str = f"{sc1_raw}m : {sc2_raw}m"
            
        sets_data.append({
            "setNumber": s_idx,
            "map": map_name,
            "mode": mode,
            "score1": sc1_raw,
            "score2": sc2_raw,
            "detailScore": detail_score_str,
            "winnerNum": winner_num,
            "winner": set_winner,
            "team1Ban": t1b1,
            "team2Ban": t2b1,
            "banStart": banstart
        })
        
    winner = team1 if score1_total > score2_total else (team2 if score2_total > score1_total else "")
    
    return {
        "phase": default_phase,
        "week": week_num,
        "team1": team1,
        "team2": team2,
        "rawTeam1": raw_team1,
        "rawTeam2": raw_team2,
        "score1": score1_total,
        "score2": score2_total,
        "winner": winner,
        "mvp": mvp,
        "date": clean_date,
        "casters": casters,
        "vod": vod,
        "bestOf": bestof,
        "sets": sets_data
    }

def parse_regular_season():
    print("Fetching Stage 1 Regular Season...")
    text = fetch_page_wikitext("Overwatch Champions Series/2026/Asia/Stage 1/Korea/Regular Season")
    
    # Split by matchlists (Week 1, Week 2, Week 3, Week 4)
    weeks = re.findall(r"\{\{Matchlist\|id=([^|]+)\|title=Week\s*(\d+)[\s\S]*?(?=\{\{Matchlist|\Z)", text)
    matches_all = []
    
    # Fallback if title=Week regex misses
    week_sections = re.split(r"\{\{Matchlist\|id=[^|]+\|title=Week\s*(\d+)", text)
    if len(week_sections) > 1:
        # alternating [pre, week1_num, content1, week2_num, content2, ...]
        for i in range(1, len(week_sections), 2):
            w_num = int(week_sections[i])
            w_content = week_sections[i+1]
            match_blocks = re.findall(r"(\|(?:M\d+)\s*=\s*\{\{Match[\s\S]*?\n\s*\}\}\n)", w_content)
            print(f"  Week {w_num}: {len(match_blocks)} matches found")
            for m_idx, mb in enumerate(match_blocks, 1):
                m_data = parse_match_block(mb, default_phase="Round Robin", week_num=w_num)
                m_data["matchNumber"] = m_idx
                m_data["matchId"] = f"S1_W{w_num}_M{m_idx}_{m_data['team1']}_{m_data['team2']}"
                matches_all.append(m_data)
    else:
        # Generic match finder
        match_blocks = re.findall(r"(\|(?:M\d+)\s*=\s*\{\{Match[\s\S]*?\n\s*\}\}\n)", text)
        print(f"  Generic Regular Season: {len(match_blocks)} matches found")
        for m_idx, mb in enumerate(match_blocks, 1):
            w_num = ((m_idx - 1) // 9) + 1
            m_data = parse_match_block(mb, default_phase="Round Robin", week_num=w_num)
            m_data["matchNumber"] = ((m_idx - 1) % 9) + 1
            m_data["matchId"] = f"S1_W{w_num}_M{m_data['matchNumber']}_{m_data['team1']}_{m_data['team2']}"
            matches_all.append(m_data)
            
    return matches_all

def parse_postseason():
    print("Fetching Stage 1 Main Page (Postseason: Seeding Decider, LCQ, Playoffs)...")
    text = fetch_page_wikitext("Overwatch Champions Series/2026/Asia/Stage 1/Korea")
    
    stages = [
        {"name": "2nd RR", "header": "Playoffs Seeding Decider Matches", "week": 5},
        {"name": "LCQ", "header": "Last Chance Qualifier", "week": 5},
        {"name": "Playoffs", "header": "Regional Playoffs", "week": 6}
    ]
    
    postseason_matches = []
    
    # 1. Seeding Decider
    sd_section = re.search(r"===\{\{Stage\|Playoffs Seeding Decider Matches\}\}===([\s\S]*?)(?====\{\{Stage|\Z)", text)
    if sd_section:
        sd_matches = re.findall(r"(\|(?:M\d+)\s*=\s*\{\{Match[\s\S]*?\n\s*\}\}\n)", sd_section.group(1))
        print(f"  Playoffs Seeding Decider: {len(sd_matches)} matches found")
        for idx, mb in enumerate(sd_matches, 1):
            m_data = parse_match_block(mb, default_phase="2nd RR", week_num=5)
            m_data["matchNumber"] = idx
            m_data["matchId"] = f"S1_SD_M{idx}_{m_data['team1']}_{m_data['team2']}"
            postseason_matches.append(m_data)
            
    # 2. Last Chance Qualifier (LCQ)
    lcq_section = re.search(r"===\{\{Stage\|Last Chance Qualifier\}\}===([\s\S]*?)(?====\{\{Stage|\Z)", text)
    if lcq_section:
        lcq_matches = re.findall(r"(\|(?:R\d+M\d+|M\d+)\s*=\s*\{\{Match[\s\S]*?\n\s*\}\}\n)", lcq_section.group(1))
        print(f"  Last Chance Qualifier: {len(lcq_matches)} matches found")
        for idx, mb in enumerate(lcq_matches, 1):
            m_data = parse_match_block(mb, default_phase="LCQ", week_num=5)
            m_data["matchNumber"] = idx
            m_data["matchId"] = f"S1_LCQ_M{idx}_{m_data['team1']}_{m_data['team2']}"
            postseason_matches.append(m_data)
            
    # 3. Regional Playoffs
    po_section = re.search(r"===\{\{Stage\|Regional Playoffs\}\}===([\s\S]*?)(?====Broadcast|==Broadcast|\Z)", text)
    if po_section:
        po_matches = re.findall(r"(\|(?:R\d+M\d+|RxMTP|M\d+)\s*=\s*\{\{Match[\s\S]*?\n\s*\}\}\n)", po_section.group(1))
        print(f"  Regional Playoffs: {len(po_matches)} matches found")
        for idx, mb in enumerate(po_matches, 1):
            m_data = parse_match_block(mb, default_phase="Playoffs", week_num=6)
            m_data["matchNumber"] = idx
            m_data["matchId"] = f"S1_PO_M{idx}_{m_data['team1']}_{m_data['team2']}"
            postseason_matches.append(m_data)
            
    return postseason_matches

def main():
    reg_matches = parse_regular_season()
    post_matches = parse_postseason()
    all_matches = reg_matches + post_matches
    print(f"\nTotal matches parsed for 2026 Korea Stage 1: {len(all_matches)}")
    
    # Summary of MVPs
    mvp_counts = {}
    for m in all_matches:
        if m.get("mvp"):
            mvp_counts[m["mvp"]] = mvp_counts.get(m["mvp"], 0) + 1
            
    sorted_mvps = sorted(mvp_counts.items(), key=lambda x: x[1], reverse=True)
    print("\nTop Match MVPs (POTM):")
    for player, count in sorted_mvps[:10]:
        print(f"  - {player}: {count} awards")
        
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "owcs-stat-lab 2", "data", "stage1_matches.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_matches, f, ensure_ascii=False, indent=2)
    print(f"\nSaved full match dataset to: {out_path}")

if __name__ == "__main__":
    main()
