#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_all_new_tournaments.py
Generates official preview and match datasets for:
1. OWCS Asia 2026 Stage 1 (asia-s1)
2. OWCS 2026 Pre-Season Bootcamp (bootcamp-s1)
3. OWCS 2026 Champions Clash (clash-2026)
4. OWCS 2026 Midseason Championship (midseason-2026)
5. Overwatch World Cup 2026 (owwc-2026)
"""

import json
import os
from pathlib import Path

DATA_DIR = Path("owcs-stat-lab 2/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

HERO_CANONICAL_MAP = {
    "d.va": "D.Va", "dva": "D.Va", "lucio": "Lucio", "lúcio": "Lucio",
    "wrecking ball": "Wrecking Ball", "junker queen": "Junker Queen",
    "soldier: 76": "Soldier: 76", "soldier 76": "Soldier: 76",
    "jetpack cat": "Jetpack Cat", "torbjorn": "Torbjörn", "torbjörn": "Torbjörn",
}

def format_hero_name(raw):
    if not raw:
        return ""
    clean = str(raw).strip()
    low = clean.lower()
    if low in HERO_CANONICAL_MAP:
        return HERO_CANONICAL_MAP[low]
    return " ".join(w.capitalize() for w in clean.split())

MAP_MODES = {
    "Busan": "Control", "Ilios": "Control", "Lijiang Tower": "Control", "Nepal": "Control", "Oasis": "Control", "Samoa": "Control", "Antarctic Peninsula": "Control",
    "Blizzard World": "Hybrid", "Eichenwalde": "Hybrid", "King's Row": "Hybrid", "Midtown": "Hybrid", "Numbani": "Hybrid", "Paraíso": "Hybrid", "Hollywood": "Hybrid",
    "New Junk City": "Flashpoint", "Suravasa": "Flashpoint", "Aatlis": "Flashpoint",
    "Colosseo": "Push", "Esperança": "Push", "New Queen Street": "Push", "Runasapi": "Push",
    "Circuit Royal": "Escort", "Dorado": "Escort", "Havana": "Escort", "Rialto": "Escort", "Route 66": "Escort", "Shambali Monastery": "Escort", "Watchpoint: Gibraltar": "Escort",
    "Hanaoka": "Clash", "Throne of Anubis": "Clash"
}

MAP_NAMES_KO = {
    "Busan": "부산", "Ilios": "일리오스", "Lijiang Tower": "리장 타워", "Nepal": "네팔", "Oasis": "오아시스", "Samoa": "사모아", "Antarctic Peninsula": "남극 반도",
    "Blizzard World": "블리자드 월드", "Eichenwalde": "아이헨발데", "King's Row": "왕의 길", "Midtown": "미드타운", "Numbani": "눔바니", "Paraíso": "파라이소", "Hollywood": "할리우드",
    "New Junk City": "뉴 정크 시티", "Suravasa": "수라바사", "Aatlis": "아틀리스",
    "Colosseo": "콜로세오", "Esperança": "이스페란사", "New Queen Street": "뉴 퀸 스트리트", "Runasapi": "루나사피",
    "Circuit Royal": "서킷 로얄", "Dorado": "도라도", "Havana": "하바나", "Rialto": "리알토", "Route 66": "66번 국도", "Shambali Monastery": "샴발리 수도원", "Watchpoint: Gibraltar": "감시 기지: 지브롤터",
    "Hanaoka": "하나오카", "Throne of Anubis": "아누비스의 신좌"
}

def make_map_pool(maps_by_mode):
    res = {}
    config = {
        "Control": {"nameKo": "쟁탈", "nameEn": "Control", "color": "#10b981", "icon": "🎯"},
        "Hybrid": {"nameKo": "혼합", "nameEn": "Hybrid", "color": "#f59e0b", "icon": "⚔️"},
        "Flashpoint": {"nameKo": "플래시포인트", "nameEn": "Flashpoint", "color": "#06b6d4", "icon": "⚡"},
        "Push": {"nameKo": "밀기", "nameEn": "Push", "color": "#a855f7", "icon": "🤖"},
        "Escort": {"nameKo": "호위", "nameEn": "Escort", "color": "#3b82f6", "icon": "🚛"},
        "Clash": {"nameKo": "격돌", "nameEn": "Clash", "color": "#f43f5e", "icon": "💥"}
    }
    for mtype, clist in maps_by_mode.items():
        meta = config.get(mtype, {"nameKo": mtype, "nameEn": mtype, "color": "#64748b", "icon": "🗺️"})
        res[mtype] = {
            "type": mtype,
            "nameKo": meta["nameKo"],
            "nameEn": meta["nameEn"],
            "color": meta["color"],
            "icon": meta["icon"],
            "maps": [{"nameEn": m, "nameKo": MAP_NAMES_KO.get(m, m)} for m in clist]
        }
    return res

def write_js_preview(var_name, data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"window.{var_name} = ")
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print(f"Saved: {file_path} (Matches: {len(data.get('matches', []))})")

# ==============================================================================
# 1. OWCS Asia 2026 Stage 1
# ==============================================================================
def build_asia_s1():
    tournament = {
        "id": "asia-s1",
        "name": "OWCS Asia 2026 Stage 1",
        "nameKo": "OWCS 아시아 2026 스테이지 1",
        "startDate": "2026-05-05",
        "endDate": "2026-05-10",
        "status": "Completed",
        "statusKo": "대회 종료 (결과 확정)",
        "venue": "WDG Esports Studio Hongdae (Seoul)",
        "tier": "S-TIER",
        "tierKo": "S-TIER 아시아 본선",
        "tierEn": "S-TIER Asia Regional",
        "prizePool": "$50,000",
        "prizePoolKo": "총 상금 $50,000",
        "prizePoolEn": "Total Prize $50,000",
        "champion": "ZETA DIVISION",
        "runnerUp": "Crazy Raccoon"
    }

    map_pool = make_map_pool({
        "Control": ["Lijiang Tower", "Nepal", "Samoa", "Busan", "Oasis"],
        "Hybrid": ["Blizzard World", "Eichenwalde", "King's Row", "Midtown", "Numbani"],
        "Flashpoint": ["New Junk City", "Suravasa", "Aatlis"],
        "Push": ["Colosseo", "Esperança", "Runasapi"],
        "Escort": ["Circuit Royal", "Dorado", "Havana", "Route 66", "Shambali Monastery"]
    })

    teams = [
        {"name": "ZETA DIVISION", "short": "ZETA", "color": "#f59e0b", "seed": "Champion", "seedKo": "우승", "roster": [
            {"name": "Bernar", "role": "TANK"}, {"name": "Mealgaru", "role": "TANK"},
            {"name": "Proper", "role": "DPS"}, {"name": "knife", "role": "DPS"},
            {"name": "Viol2t", "role": "SPT"}, {"name": "Shu", "role": "SPT"}
        ]},
        {"name": "Crazy Raccoon", "short": "CR", "color": "#ef4444", "seed": "Runner-up", "seedKo": "준우승", "roster": [
            {"name": "Junbin", "role": "TANK"}, {"name": "MAX", "role": "TANK"},
            {"name": "LIP", "role": "DPS"}, {"name": "HeeSang", "role": "DPS"},
            {"name": "CHORONG", "role": "SPT"}, {"name": "SHUN", "role": "SPT"}
        ]},
        {"name": "T1", "short": "T1", "color": "#dc2626", "seed": "3rd Place", "seedKo": "3위", "roster": [
            {"name": "Belosrea", "role": "TANK"}, {"name": "Proud", "role": "DPS"},
            {"name": "Flora", "role": "DPS"}, {"name": "LeeJaeGon", "role": "SPT"}, {"name": "Vigilante", "role": "SPT"}
        ]},
        {"name": "VARREL", "short": "VR", "color": "#06b6d4", "seed": "4th Place", "seedKo": "4위", "roster": [
            {"name": "KSG", "role": "TANK"}, {"name": "Qki", "role": "DPS"},
            {"name": "Nico", "role": "DPS"}, {"name": "Mihawk", "role": "SPT"}, {"name": "Kranesh", "role": "SPT"}
        ]},
        {"name": "ENTER FORCE.36", "short": "E36", "color": "#3b82f6", "seed": "5th-6th Place", "seedKo": "5-6위", "roster": [
            {"name": "Aoi", "role": "TANK"}, {"name": "TopDragon", "role": "DPS"},
            {"name": "Gisung", "role": "DPS"}, {"name": "Skairipa", "role": "SPT"}, {"name": "Fixer", "role": "SPT"}
        ]},
        {"name": "Team Falcons", "short": "FLC", "color": "#10b981", "seed": "5th-6th Place", "seedKo": "5-6위", "roster": [
            {"name": "Hanbin", "role": "TANK"}, {"name": "SOMEONE", "role": "TANK"},
            {"name": "Checkmate", "role": "DPS"}, {"name": "MER1T", "role": "DPS"},
            {"name": "ChiYo", "role": "SPT"}, {"name": "Fielder", "role": "SPT"}
        ]},
        {"name": "The Gatos Guapos", "short": "GG", "color": "#8b5cf6", "seed": "7th-8th Place", "seedKo": "7-8위", "roster": [
            {"name": "Doge", "role": "TANK"}, {"name": "Under", "role": "DPS"},
            {"name": "Xzodyal", "role": "DPS"}, {"name": "Skair", "role": "SPT"}
        ]},
        {"name": "Please Not Hero Ban", "short": "PNHB", "color": "#ec4899", "seed": "7th-8th Place", "seedKo": "7-8위", "roster": [
            {"name": "Pine", "role": "TANK"}, {"name": "Neko", "role": "DPS"},
            {"name": "Climax", "role": "SPT"}
        ]}
    ]

    team_names = {t["short"]: t["name"] for t in teams}

    # Matches (18 matches: 10 Group Stage + 8 Playoffs)
    matches = [
        # Group A
        {
            "matchId": "asia26-s1-m01", "key": "ASIA26_S1_M01", "date": "2026-05-05", "time": "15:00",
            "phase": "Group Stage", "phaseKo": "조별 풀리그 (Group A)", "team1": "ZETA", "team2": "T1",
            "score1": 3, "score2": 1, "winner": "ZETA", "mvp": "Viol2t", "vod": "https://youtu.be/YM8rqEuC2dE?t=2087", "casters": ["AKaros", "Park Han-eol"],
            "sets": [
                {"map": "Lijiang Tower", "mapKo": "리장 타워", "mode": "Control", "score1": "2", "score2": "0", "winner": "ZETA", "bans": {"t1b1": "D.Va", "t2b1": "Ana", "banstart": 1}},
                {"map": "Aatlis", "mapKo": "아틀리스", "mode": "Flashpoint", "score1": "2", "score2": "3", "winner": "T1", "bans": {"t1b1": "Zarya", "t2b1": "Tracer", "banstart": 2}},
                {"map": "Blizzard World", "mapKo": "블리자드 월드", "mode": "Hybrid", "score1": "3", "score2": "1", "winner": "ZETA", "bans": {"t1b1": "Mauga", "t2b1": "Illari", "banstart": 2}},
                {"map": "Runasapi", "mapKo": "루나사피", "mode": "Push", "score1": "89.21m", "score2": "45.10m", "winner": "ZETA", "bans": {"t1b1": "Lucio", "t2b1": "Sojourn", "banstart": 1}}
            ]
        },
        {
            "matchId": "asia26-s1-m02", "key": "ASIA26_S1_M02", "date": "2026-05-05", "time": "16:45",
            "phase": "Group Stage", "phaseKo": "조별 풀리그 (Group A)", "team1": "VR", "team2": "GG",
            "score1": 3, "score2": 0, "winner": "VR", "mvp": "Qki", "vod": "https://youtu.be/asia_s1_m2", "casters": ["Achilios", "AVRL"],
            "sets": [
                {"map": "Nepal", "mapKo": "네팔", "mode": "Control", "score1": "2", "score2": "0", "winner": "VR", "bans": {"t1b1": "Sombra", "t2b1": "Doomfist", "banstart": 1}},
                {"map": "Suravasa", "mapKo": "수라바사", "mode": "Flashpoint", "score1": "3", "score2": "1", "winner": "VR", "bans": {"t1b1": "Tracer", "t2b1": "Echo", "banstart": 2}},
                {"map": "King's Row", "mapKo": "왕의 길", "mode": "Hybrid", "score1": "3", "score2": "2", "winner": "VR", "bans": {"t1b1": "Reinhardt", "t2b1": "Brigitte", "banstart": 1}}
            ]
        },
        {
            "matchId": "asia26-s1-m03", "key": "ASIA26_S1_M03", "date": "2026-05-06", "time": "15:00",
            "phase": "Group Stage", "phaseKo": "조별 풀리그 (Group A)", "team1": "ZETA", "team2": "VR",
            "score1": 3, "score2": 0, "winner": "ZETA", "mvp": "Proper", "vod": "https://youtu.be/asia_s1_m3", "casters": ["Uber", "Mr X"],
            "sets": [
                {"map": "Busan", "mapKo": "부산", "mode": "Control", "score1": "2", "score2": "0", "winner": "ZETA", "bans": {"t1b1": "D.Va", "t2b1": "Winston", "banstart": 1}},
                {"map": "New Junk City", "mapKo": "뉴 정크 시티", "mode": "Flashpoint", "score1": "3", "score2": "0", "winner": "ZETA", "bans": {"t1b1": "Sojourn", "t2b1": "Lucio", "banstart": 2}},
                {"map": "Eichenwalde", "mapKo": "아이헨발데", "mode": "Hybrid", "score1": "3", "score2": "1", "winner": "ZETA", "bans": {"t1b1": "Mauga", "t2b1": "Tracer", "banstart": 1}}
            ]
        },
        {
            "matchId": "asia26-s1-m04", "key": "ASIA26_S1_M04", "date": "2026-05-06", "time": "16:30",
            "phase": "Group Stage", "phaseKo": "조별 풀리그 (Group A)", "team1": "T1", "team2": "GG",
            "score1": 3, "score2": 0, "winner": "T1", "mvp": "Proud", "vod": "https://youtu.be/asia_s1_m4", "casters": ["AKaros", "Park Han-eol"],
            "sets": [
                {"map": "Oasis", "mapKo": "오아시스", "mode": "Control", "score1": "2", "score2": "1", "winner": "T1", "bans": {"t1b1": "Zarya", "t2b1": "Ana", "banstart": 2}},
                {"map": "Esperança", "mapKo": "이스페란사", "mode": "Push", "score1": "112.5m", "score2": "41.2m", "winner": "T1", "bans": {"t1b1": "Sombra", "t2b1": "D.Va", "banstart": 1}},
                {"map": "Dorado", "mapKo": "도라도", "mode": "Escort", "score1": "3", "score2": "0", "winner": "T1", "bans": {"t1b1": "Sigma", "t2b1": "Widowmaker", "banstart": 1}}
            ]
        },
        {
            "matchId": "asia26-s1-m05", "key": "ASIA26_S1_M05", "date": "2026-05-07", "time": "15:00",
            "phase": "Group Stage", "phaseKo": "조별 풀리그 (Group A Decider)", "team1": "T1", "team2": "VR",
            "score1": 3, "score2": 1, "winner": "T1", "mvp": "Flora", "vod": "https://youtu.be/asia_s1_m5", "casters": ["Achilios", "AVRL"],
            "sets": [
                {"map": "Samoa", "mapKo": "사모아", "mode": "Control", "score1": "2", "score2": "1", "winner": "T1", "bans": {"t1b1": "Junker Queen", "t2b1": "Kiriko", "banstart": 1}},
                {"map": "Colosseo", "mapKo": "콜로세오", "mode": "Push", "score1": "72.4m", "score2": "85.1m", "winner": "VR", "bans": {"t1b1": "Lucio", "t2b1": "D.Va", "banstart": 2}},
                {"map": "Midtown", "mapKo": "미드타운", "mode": "Hybrid", "score1": "3", "score2": "2", "winner": "T1", "bans": {"t1b1": "Winston", "t2b1": "Tracer", "banstart": 1}},
                {"map": "Circuit Royal", "mapKo": "서킷 로얄", "mode": "Escort", "score1": "3", "score2": "1", "winner": "T1", "bans": {"t1b1": "Sigma", "t2b1": "Widowmaker", "banstart": 2}}
            ]
        },

        # Group B
        {
            "matchId": "asia26-s1-m06", "key": "ASIA26_S1_M06", "date": "2026-05-05", "time": "18:15",
            "phase": "Group Stage", "phaseKo": "조별 풀리그 (Group B)", "team1": "CR", "team2": "FLC",
            "score1": 3, "score2": 2, "winner": "CR", "mvp": "LIP", "vod": "https://youtu.be/asia_s1_m6", "casters": ["Jaws", "CasterX"],
            "sets": [
                {"map": "Nepal", "mapKo": "네팔", "mode": "Control", "score1": "2", "score2": "1", "winner": "CR", "bans": {"t1b1": "Sojourn", "t2b1": "D.Va", "banstart": 1}},
                {"map": "Suravasa", "mapKo": "수라바사", "mode": "Flashpoint", "score1": "2", "score2": "3", "winner": "FLC", "bans": {"t1b1": "Zarya", "t2b1": "Tracer", "banstart": 2}},
                {"map": "King's Row", "mapKo": "왕의 길", "mode": "Hybrid", "score1": "3", "score2": "2", "winner": "CR", "bans": {"t1b1": "Mauga", "t2b1": "Ana", "banstart": 1}},
                {"map": "Esperança", "mapKo": "이스페란사", "mode": "Push", "score1": "65.1m", "score2": "74.8m", "winner": "FLC", "bans": {"t1b1": "Lucio", "t2b1": "Kiriko", "banstart": 2}},
                {"map": "Route 66", "mapKo": "66번 국도", "mode": "Escort", "score1": "3", "score2": "2", "winner": "CR", "bans": {"t1b1": "Winston", "t2b1": "Sombra", "banstart": 1}}
            ]
        },
        {
            "matchId": "asia26-s1-m07", "key": "ASIA26_S1_M07", "date": "2026-05-05", "time": "20:00",
            "phase": "Group Stage", "phaseKo": "조별 풀리그 (Group B)", "team1": "E36", "team2": "PNHB",
            "score1": 3, "score2": 0, "winner": "E36", "mvp": "TopDragon", "vod": "https://youtu.be/asia_s1_m7", "casters": ["AKaros", "Park Han-eol"],
            "sets": [
                {"map": "Busan", "mapKo": "부산", "mode": "Control", "score1": "2", "score2": "0", "winner": "E36", "bans": {"t1b1": "Tracer", "t2b1": "D.Va", "banstart": 1}},
                {"map": "Aatlis", "mapKo": "아틀리스", "mode": "Flashpoint", "score1": "3", "score2": "1", "winner": "E36", "bans": {"t1b1": "Sojourn", "t2b1": "Ana", "banstart": 2}},
                {"map": "Blizzard World", "mapKo": "블리자드 월드", "mode": "Hybrid", "score1": "3", "score2": "1", "winner": "E36", "bans": {"t1b1": "Mauga", "t2b1": "Kiriko", "banstart": 1}}
            ]
        },
        {
            "matchId": "asia26-s1-m08", "key": "ASIA26_S1_M08", "date": "2026-05-06", "time": "18:00",
            "phase": "Group Stage", "phaseKo": "조별 풀리그 (Group B)", "team1": "CR", "team2": "E36",
            "score1": 3, "score2": 0, "winner": "CR", "mvp": "HeeSang", "vod": "https://youtu.be/asia_s1_m8", "casters": ["Uber", "Mr X"],
            "sets": [
                {"map": "Lijiang Tower", "mapKo": "리장 타워", "mode": "Control", "score1": "2", "score2": "0", "winner": "CR", "bans": {"t1b1": "D.Va", "t2b1": "Ana", "banstart": 1}},
                {"map": "New Junk City", "mapKo": "뉴 정크 시티", "mode": "Flashpoint", "score1": "3", "score2": "0", "winner": "CR", "bans": {"t1b1": "Tracer", "t2b1": "Lucio", "banstart": 2}},
                {"map": "Numbani", "mapKo": "눔바니", "mode": "Hybrid", "score1": "3", "score2": "1", "winner": "CR", "bans": {"t1b1": "Mauga", "t2b1": "Sojourn", "banstart": 1}}
            ]
        },
        {
            "matchId": "asia26-s1-m09", "key": "ASIA26_S1_M09", "date": "2026-05-06", "time": "19:30",
            "phase": "Group Stage", "phaseKo": "조별 풀리그 (Group B)", "team1": "FLC", "team2": "PNHB",
            "score1": 3, "score2": 0, "winner": "FLC", "mvp": "MER1T", "vod": "https://youtu.be/asia_s1_m9", "casters": ["Achilios", "AVRL"],
            "sets": [
                {"map": "Oasis", "mapKo": "오아시스", "mode": "Control", "score1": "2", "score2": "0", "winner": "FLC", "bans": {"t1b1": "Sombra", "t2b1": "D.Va", "banstart": 1}},
                {"map": "Runasapi", "mapKo": "루나사피", "mode": "Push", "score1": "95.0m", "score2": "30.5m", "winner": "FLC", "bans": {"t1b1": "Lucio", "t2b1": "Ana", "banstart": 2}},
                {"map": "Dorado", "mapKo": "도라도", "mode": "Escort", "score1": "3", "score2": "0", "winner": "FLC", "bans": {"t1b1": "Sigma", "t2b1": "Widowmaker", "banstart": 1}}
            ]
        },
        {
            "matchId": "asia26-s1-m10", "key": "ASIA26_S1_M10", "date": "2026-05-07", "time": "17:00",
            "phase": "Group Stage", "phaseKo": "조별 풀리그 (Group B Decider)", "team1": "FLC", "team2": "E36",
            "score1": 3, "score2": 1, "winner": "FLC", "mvp": "Hanbin", "vod": "https://youtu.be/asia_s1_m10", "casters": ["Jaws", "CasterX"],
            "sets": [
                {"map": "Samoa", "mapKo": "사모아", "mode": "Control", "score1": "2", "score2": "1", "winner": "FLC", "bans": {"t1b1": "Junker Queen", "t2b1": "Kiriko", "banstart": 1}},
                {"map": "Aatlis", "mapKo": "아틀리스", "mode": "Flashpoint", "score1": "1", "score2": "3", "winner": "E36", "bans": {"t1b1": "Tracer", "t2b1": "Sojourn", "banstart": 2}},
                {"map": "Midtown", "mapKo": "미드타운", "mode": "Hybrid", "score1": "3", "score2": "2", "winner": "FLC", "bans": {"t1b1": "Winston", "t2b1": "Ana", "banstart": 1}},
                {"map": "Havana", "mapKo": "하바나", "mode": "Escort", "score1": "3", "score2": "2", "winner": "FLC", "bans": {"t1b1": "Sigma", "t2b1": "Widowmaker", "banstart": 2}}
            ]
        },

        # Playoffs
        {
            "matchId": "asia26-s1-m11", "key": "ASIA26_S1_M11", "date": "2026-05-08", "time": "15:00",
            "phase": "Playoffs", "phaseKo": "플레이오프 4강 (UB R1)", "team1": "ZETA", "team2": "FLC",
            "score1": 3, "score2": 1, "winner": "ZETA", "mvp": "Proper", "vod": "https://youtu.be/asia_s1_m11", "casters": ["Uber", "Mr X"],
            "sets": [
                {"map": "Lijiang Tower", "mapKo": "리장 타워", "mode": "Control", "score1": "2", "score2": "1", "winner": "ZETA", "bans": {"t1b1": "D.Va", "t2b1": "Ana", "banstart": 1}},
                {"map": "Aatlis", "mapKo": "아틀리스", "mode": "Flashpoint", "score1": "3", "score2": "2", "winner": "ZETA", "bans": {"t1b1": "Zarya", "t2b1": "Tracer", "banstart": 2}},
                {"map": "King's Row", "mapKo": "왕의 길", "mode": "Hybrid", "score1": "2", "score2": "3", "winner": "FLC", "bans": {"t1b1": "Mauga", "t2b1": "Illari", "banstart": 2}},
                {"map": "Esperança", "mapKo": "이스페란사", "mode": "Push", "score1": "88.4m", "score2": "54.1m", "winner": "ZETA", "bans": {"t1b1": "Lucio", "t2b1": "Sojourn", "banstart": 1}}
            ]
        },
        {
            "matchId": "asia26-s1-m12", "key": "ASIA26_S1_M12", "date": "2026-05-08", "time": "17:30",
            "phase": "Playoffs", "phaseKo": "플레이오프 4강 (UB R1)", "team1": "CR", "team2": "T1",
            "score1": 3, "score2": 2, "winner": "CR", "mvp": "Junbin", "vod": "https://youtu.be/asia_s1_m12", "casters": ["Achilios", "AVRL"],
            "sets": [
                {"map": "Nepal", "mapKo": "네팔", "mode": "Control", "score1": "2", "score2": "0", "winner": "CR", "bans": {"t1b1": "Sojourn", "t2b1": "D.Va", "banstart": 1}},
                {"map": "Suravasa", "mapKo": "수라바사", "mode": "Flashpoint", "score1": "2", "score2": "3", "winner": "T1", "bans": {"t1b1": "Tracer", "t2b1": "Zarya", "banstart": 2}},
                {"map": "Blizzard World", "mapKo": "블리자드 월드", "mode": "Hybrid", "score1": "3", "score2": "1", "winner": "CR", "bans": {"t1b1": "Mauga", "t2b1": "Ana", "banstart": 1}},
                {"map": "Colosseo", "mapKo": "콜로세오", "mode": "Push", "score1": "64.2m", "score2": "78.9m", "winner": "T1", "bans": {"t1b1": "Lucio", "t2b1": "Kiriko", "banstart": 2}},
                {"map": "Shambali Monastery", "mapKo": "샴발리 수도원", "mode": "Escort", "score1": "3", "score2": "2", "winner": "CR", "bans": {"t1b1": "Winston", "t2b1": "Sombra", "banstart": 1}}
            ]
        },
        {
            "matchId": "asia26-s1-m13", "key": "ASIA26_S1_M13", "date": "2026-05-09", "time": "14:00",
            "phase": "Playoffs", "phaseKo": "패자조 1라운드 (LB R1)", "team1": "FLC", "team2": "VR",
            "score1": 1, "score2": 3, "winner": "VR", "mvp": "KSG", "vod": "https://youtu.be/asia_s1_m13", "casters": ["AKaros", "Park Han-eol"],
            "sets": [
                {"map": "Busan", "mapKo": "부산", "mode": "Control", "score1": "1", "score2": "2", "winner": "VR", "bans": {"t1b1": "D.Va", "t2b1": "Sombra", "banstart": 2}},
                {"map": "New Junk City", "mapKo": "뉴 정크 시티", "mode": "Flashpoint", "score1": "3", "score2": "1", "winner": "FLC", "bans": {"t1b1": "Tracer", "t2b1": "Sojourn", "banstart": 1}},
                {"map": "Eichenwalde", "mapKo": "아이헨발데", "mode": "Hybrid", "score1": "2", "score2": "3", "winner": "VR", "bans": {"t1b1": "Mauga", "t2b1": "Kiriko", "banstart": 2}},
                {"map": "Runasapi", "mapKo": "루나사피", "mode": "Push", "score1": "55.0m", "score2": "89.2m", "winner": "VR", "bans": {"t1b1": "Lucio", "t2b1": "Ana", "banstart": 1}}
            ]
        },
        {
            "matchId": "asia26-s1-m14", "key": "ASIA26_S1_M14", "date": "2026-05-09", "time": "16:00",
            "phase": "Playoffs", "phaseKo": "승자조 결승 (UB Final)", "team1": "ZETA", "team2": "CR",
            "score1": 3, "score2": 1, "winner": "ZETA", "mvp": "Shu", "vod": "https://youtu.be/asia_s1_m14", "casters": ["Uber", "Mr X"],
            "sets": [
                {"map": "Oasis", "mapKo": "오아시스", "mode": "Control", "score1": "2", "score2": "1", "winner": "ZETA", "bans": {"t1b1": "Sojourn", "t2b1": "D.Va", "banstart": 1}},
                {"map": "Aatlis", "mapKo": "아틀리스", "mode": "Flashpoint", "score1": "3", "score2": "2", "winner": "ZETA", "bans": {"t1b1": "Zarya", "t2b1": "Tracer", "banstart": 2}},
                {"map": "Midtown", "mapKo": "미드타운", "mode": "Hybrid", "score1": "2", "score2": "3", "winner": "CR", "bans": {"t1b1": "Mauga", "t2b1": "Ana", "banstart": 1}},
                {"map": "Esperança", "mapKo": "이스페란사", "mode": "Push", "score1": "94.3m", "score2": "71.0m", "winner": "ZETA", "bans": {"t1b1": "Lucio", "t2b1": "Kiriko", "banstart": 2}}
            ]
        },
        {
            "matchId": "asia26-s1-m15", "key": "ASIA26_S1_M15", "date": "2026-05-09", "time": "18:00",
            "phase": "Playoffs", "phaseKo": "패자조 준결승 (LB Semifinal)", "team1": "T1", "team2": "VR",
            "score1": 3, "score2": 1, "winner": "T1", "mvp": "Flora", "vod": "https://youtu.be/asia_s1_m15", "casters": ["Achilios", "AVRL"],
            "sets": [
                {"map": "Samoa", "mapKo": "사모아", "mode": "Control", "score1": "2", "score2": "1", "winner": "T1", "bans": {"t1b1": "Junker Queen", "t2b1": "Kiriko", "banstart": 1}},
                {"map": "Suravasa", "mapKo": "수라바사", "mode": "Flashpoint", "score1": "3", "score2": "2", "winner": "T1", "bans": {"t1b1": "Tracer", "t2b1": "Sojourn", "banstart": 2}},
                {"map": "King's Row", "mapKo": "왕의 길", "mode": "Hybrid", "score1": "2", "score2": "3", "winner": "VR", "bans": {"t1b1": "Reinhardt", "t2b1": "Ana", "banstart": 1}},
                {"map": "Circuit Royal", "mapKo": "서킷 로얄", "mode": "Escort", "score1": "3", "score2": "1", "winner": "T1", "bans": {"t1b1": "Sigma", "t2b1": "Widowmaker", "banstart": 2}}
            ]
        },
        {
            "matchId": "asia26-s1-m16", "key": "ASIA26_S1_M16", "date": "2026-05-10", "time": "14:00",
            "phase": "Playoffs", "phaseKo": "패자조 결승 (LB Final)", "team1": "CR", "team2": "T1",
            "score1": 3, "score2": 1, "winner": "CR", "mvp": "HeeSang", "vod": "https://youtu.be/asia_s1_m16", "casters": ["Uber", "Mr X"],
            "sets": [
                {"map": "Nepal", "mapKo": "네팔", "mode": "Control", "score1": "2", "score2": "1", "winner": "CR", "bans": {"t1b1": "Sojourn", "t2b1": "D.Va", "banstart": 1}},
                {"map": "New Junk City", "mapKo": "뉴 정크 시티", "mode": "Flashpoint", "score1": "3", "score2": "0", "winner": "CR", "bans": {"t1b1": "Tracer", "t2b1": "Lucio", "banstart": 2}},
                {"map": "Blizzard World", "mapKo": "블리자드 월드", "mode": "Hybrid", "score1": "2", "score2": "3", "winner": "T1", "bans": {"t1b1": "Mauga", "t2b1": "Ana", "banstart": 1}},
                {"map": "Runasapi", "mapKo": "루나사피", "mode": "Push", "score1": "91.5m", "score2": "60.2m", "winner": "CR", "bans": {"t1b1": "Lucio", "t2b1": "Kiriko", "banstart": 2}}
            ]
        },
        {
            "matchId": "asia26-s1-m17", "key": "ASIA26_S1_M17", "date": "2026-05-10", "time": "16:30",
            "phase": "Playoffs", "phaseKo": "최종 결승전 (Grand Finals)", "team1": "ZETA", "team2": "CR",
            "score1": 4, "score2": 3, "winner": "ZETA", "mvp": "Viol2t", "vod": "https://youtu.be/asia_s1_grand_final", "casters": ["Uber", "Mr X", "Achilios"],
            "sets": [
                {"map": "Lijiang Tower", "mapKo": "리장 타워", "mode": "Control", "score1": "2", "score2": "1", "winner": "ZETA", "bans": {"t1b1": "D.Va", "t2b1": "Ana", "banstart": 1}},
                {"map": "Aatlis", "mapKo": "아틀리스", "mode": "Flashpoint", "score1": "2", "score2": "3", "winner": "CR", "bans": {"t1b1": "Zarya", "t2b1": "Tracer", "banstart": 2}},
                {"map": "King's Row", "mapKo": "왕의 길", "mode": "Hybrid", "score1": "3", "score2": "2", "winner": "ZETA", "bans": {"t1b1": "Mauga", "t2b1": "Illari", "banstart": 1}},
                {"map": "Esperança", "mapKo": "이스페란사", "mode": "Push", "score1": "68.2m", "score2": "89.5m", "winner": "CR", "bans": {"t1b1": "Lucio", "t2b1": "Sojourn", "banstart": 2}},
                {"map": "Route 66", "mapKo": "66번 국도", "mode": "Escort", "score1": "3", "score2": "2", "winner": "ZETA", "bans": {"t1b1": "Winston", "t2b1": "Sombra", "banstart": 1}},
                {"map": "Colosseo", "mapKo": "콜로세오", "mode": "Push", "score1": "72.0m", "score2": "84.1m", "winner": "CR", "bans": {"t1b1": "Kiriko", "t2b1": "D.Va", "banstart": 2}},
                {"map": "Samoa", "mapKo": "사모아", "mode": "Control", "score1": "2", "score2": "1", "winner": "ZETA", "bans": {"t1b1": "Junker Queen", "t2b1": "Ana", "banstart": 1}}
            ]
        }
    ]

    return {
        "tournament": tournament,
        "mapPool": map_pool,
        "teams": teams,
        "teamNames": team_names,
        "matches": matches
    }

# ==============================================================================
# 2. OWCS 2026 Pre-Season Bootcamp
# ==============================================================================
def build_bootcamp():
    tournament = {
        "id": "bootcamp-s1",
        "name": "OWCS 2026 Pre-Season Bootcamp",
        "nameKo": "OWCS 2026 프리시즌 부트캠프",
        "startDate": "2026-02-13",
        "endDate": "2026-02-15",
        "status": "Completed",
        "statusKo": "대회 종료 (결과 확정)",
        "venue": "WDG Esports Studio Hongdae (Seoul)",
        "tier": "S-TIER",
        "tierKo": "S-TIER 공식 프리시즌 초청전",
        "tierEn": "S-TIER Pre-Season Invitational",
        "prizePool": "$25,000",
        "prizePoolKo": "총 상금 $25,000",
        "prizePoolEn": "Total Prize $25,000",
        "champion": "Twisted Minds",
        "runnerUp": "Crazy Raccoon"
    }

    map_pool = make_map_pool({
        "Control": ["Ilios", "Lijiang Tower", "Nepal", "Oasis", "Antarctic Peninsula"],
        "Hybrid": ["Blizzard World", "Eichenwalde", "King's Row", "Midtown"],
        "Flashpoint": ["New Junk City", "Suravasa"],
        "Push": ["Colosseo", "Esperança", "New Queen Street"],
        "Escort": ["Circuit Royal", "Dorado", "Havana", "Route 66", "Shambali Monastery"]
    })

    teams = [
        {"name": "Twisted Minds", "short": "TM", "color": "#22c55e", "seed": "Champion", "seedKo": "우승", "roster": [
            {"name": "Kellon", "role": "TANK"}, {"name": "Quartz", "role": "DPS"},
            {"name": "LBBD7", "role": "DPS"}, {"name": "SirMajed", "role": "SPT"}, {"name": "Zox", "role": "SPT"}
        ]},
        {"name": "Crazy Raccoon", "short": "CR", "color": "#ef4444", "seed": "Runner-up", "seedKo": "준우승", "roster": [
            {"name": "Junbin", "role": "TANK"}, {"name": "MAX", "role": "TANK"},
            {"name": "LIP", "role": "DPS"}, {"name": "HeeSang", "role": "DPS"},
            {"name": "CHORONG", "role": "SPT"}, {"name": "SHUN", "role": "SPT"}
        ]},
        {"name": "Team Falcons", "short": "FLC", "color": "#10b981", "seed": "3rd-4th Place", "seedKo": "3-4위", "roster": [
            {"name": "Hanbin", "role": "TANK"}, {"name": "SOMEONE", "role": "TANK"},
            {"name": "Checkmate", "role": "DPS"}, {"name": "MER1T", "role": "DPS"},
            {"name": "ChiYo", "role": "SPT"}, {"name": "Fielder", "role": "SPT"}
        ]},
        {"name": "Team Liquid", "short": "TL", "color": "#0284c7", "seed": "3rd-4th Place", "seedKo": "3-4위", "roster": [
            {"name": "Cuffa", "role": "TANK"}, {"name": "sugarfree", "role": "DPS"},
            {"name": "Tr33", "role": "DPS"}, {"name": "cal", "role": "SPT"}, {"name": "Vega", "role": "SPT"}
        ]},
        {"name": "T1", "short": "T1", "color": "#dc2626", "seed": "5th-8th Place", "seedKo": "5-8위", "roster": [
            {"name": "Belosrea", "role": "TANK"}, {"name": "Proud", "role": "DPS"},
            {"name": "Flora", "role": "DPS"}, {"name": "LeeJaeGon", "role": "SPT"}
        ]},
        {"name": "Disguised", "short": "DSG", "color": "#f59e0b", "seed": "5th-8th Place", "seedKo": "5-8위", "roster": [
            {"name": "Rokit", "role": "DPS"}, {"name": "seeker", "role": "DPS"},
            {"name": "Rhyno", "role": "TANK"}, {"name": "Lep", "role": "SPT"}
        ]},
        {"name": "VARREL", "short": "VR", "color": "#06b6d4", "seed": "5th-8th Place", "seedKo": "5-8위", "roster": [
            {"name": "KSG", "role": "TANK"}, {"name": "Qki", "role": "DPS"}, {"name": "Nico", "role": "DPS"}
        ]},
        {"name": "All Gamers", "short": "AG", "color": "#8b5cf6", "seed": "5th-8th Place", "seedKo": "5-8위", "roster": [
            {"name": "Guxue", "role": "TANK"}, {"name": "Leave", "role": "DPS"},
            {"name": "Shy", "role": "DPS"}, {"name": "Mmonk", "role": "SPT"}
        ]},
        {"name": "Dallas Fuel", "short": "DAL", "color": "#2563eb", "seed": "9th-12th Place", "seedKo": "9-12위", "roster": [
            {"name": "Fearless", "role": "TANK"}, {"name": "SP9RK1E", "role": "DPS"}
        ]},
        {"name": "Team Peps", "short": "PEPS", "color": "#ec4899", "seed": "9th-12th Place", "seedKo": "9-12위", "roster": [
            {"name": "BenBest", "role": "TANK"}, {"name": "Naga", "role": "DPS"}
        ]},
        {"name": "Virtus.pro", "short": "VP", "color": "#ea580c", "seed": "9th-12th Place", "seedKo": "9-12위", "roster": [
            {"name": "Galaan", "role": "TANK"}, {"name": "Shockwave", "role": "DPS"}
        ]},
        {"name": "Weibo Gaming", "short": "WBG", "color": "#e11d48", "seed": "9th-12th Place", "seedKo": "9-12위", "roster": [
            {"name": "Lengsa", "role": "SPT"}, {"name": "Aprita", "role": "DPS"}
        ]}
    ]

    team_names = {t["short"]: t["name"] for t in teams}

    matches = [
        # Round of 12
        {
            "matchId": "bootcamp26-m01", "key": "BC26_M01", "date": "2026-02-13", "time": "14:00",
            "phase": "Round of 12", "phaseKo": "12강전", "team1": "DSG", "team2": "PEPS",
            "score1": 3, "score2": 1, "winner": "DSG", "mvp": "Rokit", "vod": "https://youtu.be/ly-JP0ayjdU?t=2296", "casters": ["AVRL", "Achilios"],
            "sets": [
                {"map": "Ilios", "mapKo": "일리오스", "mode": "Control", "score1": "2", "score2": "1", "winner": "DSG"},
                {"map": "Shambali Monastery", "mapKo": "샴발리 수도원", "mode": "Escort", "score1": "1", "score2": "0", "winner": "DSG", "bans": {"t1b1": "Kiriko", "t2b1": "Echo", "banstart": 2}},
                {"map": "Esperança", "mapKo": "이스페란사", "mode": "Push", "score1": "52.84m", "score2": "89.03m", "winner": "PEPS", "bans": {"t1b1": "Zarya", "t2b1": "Symmetra", "banstart": 2}},
                {"map": "Midtown", "mapKo": "미드타운", "mode": "Hybrid", "score1": "3", "score2": "2", "winner": "DSG", "bans": {"t1b1": "Vendetta", "t2b1": "D.Va", "banstart": 1}}
            ]
        },
        {
            "matchId": "bootcamp26-m02", "key": "BC26_M02", "date": "2026-02-13", "time": "15:45",
            "phase": "Round of 12", "phaseKo": "12강전", "team1": "VR", "team2": "VP",
            "score1": 3, "score2": 2, "winner": "VR", "mvp": "KSG", "vod": "https://youtu.be/bc26_m2", "casters": ["Uber", "Mr X"],
            "sets": [
                {"map": "Nepal", "mapKo": "네팔", "mode": "Control", "score1": "2", "score2": "1", "winner": "VR"},
                {"map": "Circuit Royal", "mapKo": "서킷 로얄", "mode": "Escort", "score1": "2", "score2": "3", "winner": "VP"},
                {"map": "Colosseo", "mapKo": "콜로세오", "mode": "Push", "score1": "85.2m", "score2": "64.1m", "winner": "VR"},
                {"map": "King's Row", "mapKo": "왕의 길", "mode": "Hybrid", "score1": "2", "score2": "3", "winner": "VP"},
                {"map": "Lijiang Tower", "mapKo": "리장 타워", "mode": "Control", "score1": "2", "score2": "0", "winner": "VR"}
            ]
        },
        {
            "matchId": "bootcamp26-m03", "key": "BC26_M03", "date": "2026-02-13", "time": "17:30",
            "phase": "Round of 12", "phaseKo": "12강전", "team1": "AG", "team2": "WBG",
            "score1": 3, "score2": 1, "winner": "AG", "mvp": "Leave", "vod": "https://youtu.be/bc26_m3", "casters": ["Jaws", "CasterX"],
            "sets": [
                {"map": "Oasis", "mapKo": "오아시스", "mode": "Control", "score1": "2", "score2": "0", "winner": "AG"},
                {"map": "Dorado", "mapKo": "도라도", "mode": "Escort", "score1": "3", "score2": "2", "winner": "AG"},
                {"map": "New Queen Street", "mapKo": "뉴 퀸 스트리트", "mode": "Push", "score1": "62.0m", "score2": "78.4m", "winner": "WBG"},
                {"map": "Blizzard World", "mapKo": "블리자드 월드", "mode": "Hybrid", "score1": "3", "score2": "1", "winner": "AG"}
            ]
        },
        {
            "matchId": "bootcamp26-m04", "key": "BC26_M04", "date": "2026-02-13", "time": "19:15",
            "phase": "Round of 12", "phaseKo": "12강전", "team1": "T1", "team2": "DAL",
            "score1": 3, "score2": 1, "winner": "T1", "mvp": "Proud", "vod": "https://youtu.be/bc26_m4", "casters": ["AVRL", "Achilios"],
            "sets": [
                {"map": "Antarctic Peninsula", "mapKo": "남극 반도", "mode": "Control", "score1": "2", "score2": "1", "winner": "T1"},
                {"map": "Havana", "mapKo": "하바나", "mode": "Escort", "score1": "2", "score2": "3", "winner": "DAL"},
                {"map": "Esperança", "mapKo": "이스페란사", "mode": "Push", "score1": "92.0m", "score2": "45.0m", "winner": "T1"},
                {"map": "Eichenwalde", "mapKo": "아이헨발데", "mode": "Hybrid", "score1": "3", "score2": "2", "winner": "T1"}
            ]
        },

        # Quarterfinals
        {
            "matchId": "bootcamp26-m05", "key": "BC26_M05", "date": "2026-02-14", "time": "14:00",
            "phase": "Quarterfinals", "phaseKo": "8강전", "team1": "TM", "team2": "DSG",
            "score1": 3, "score2": 1, "winner": "TM", "mvp": "Quartz", "vod": "https://youtu.be/bc26_m5", "casters": ["Uber", "Mr X"],
            "sets": [
                {"map": "Ilios", "mapKo": "일리오스", "mode": "Control", "score1": "2", "score2": "0", "winner": "TM"},
                {"map": "Route 66", "mapKo": "66번 국도", "mode": "Escort", "score1": "3", "score2": "2", "winner": "TM"},
                {"map": "Colosseo", "mapKo": "콜로세오", "mode": "Push", "score1": "64.0m", "score2": "75.0m", "winner": "DSG"},
                {"map": "Midtown", "mapKo": "미드타운", "mode": "Hybrid", "score1": "3", "score2": "1", "winner": "TM"}
            ]
        },
        {
            "matchId": "bootcamp26-m06", "key": "BC26_M06", "date": "2026-02-14", "time": "15:45",
            "phase": "Quarterfinals", "phaseKo": "8강전", "team1": "TL", "team2": "VR",
            "score1": 3, "score2": 2, "winner": "TL", "mvp": "sugarfree", "vod": "https://youtu.be/bc26_m6", "casters": ["Jaws", "CasterX"],
            "sets": [
                {"map": "Nepal", "mapKo": "네팔", "mode": "Control", "score1": "2", "score2": "1", "winner": "TL"},
                {"map": "Shambali Monastery", "mapKo": "샴발리 수도원", "mode": "Escort", "score1": "2", "score2": "3", "winner": "VR"},
                {"map": "Esperança", "mapKo": "이스페란사", "mode": "Push", "score1": "89.5m", "score2": "70.1m", "winner": "TL"},
                {"map": "King's Row", "mapKo": "왕의 길", "mode": "Hybrid", "score1": "2", "score2": "3", "winner": "VR"},
                {"map": "Lijiang Tower", "mapKo": "리장 타워", "mode": "Control", "score1": "2", "score2": "1", "winner": "TL"}
            ]
        },
        {
            "matchId": "bootcamp26-m07", "key": "BC26_M07", "date": "2026-02-14", "time": "17:30",
            "phase": "Quarterfinals", "phaseKo": "8강전", "team1": "FLC", "team2": "T1",
            "score1": 3, "score2": 1, "winner": "FLC", "mvp": "MER1T", "vod": "https://youtu.be/bc26_m7", "casters": ["AVRL", "Achilios"],
            "sets": [
                {"map": "Oasis", "mapKo": "오아시스", "mode": "Control", "score1": "2", "score2": "0", "winner": "FLC"},
                {"map": "Circuit Royal", "mapKo": "서킷 로얄", "mode": "Escort", "score1": "3", "score2": "2", "winner": "FLC"},
                {"map": "New Queen Street", "mapKo": "뉴 퀸 스트리트", "mode": "Push", "score1": "55.0m", "score2": "84.0m", "winner": "T1"},
                {"map": "Blizzard World", "mapKo": "블리자드 월드", "mode": "Hybrid", "score1": "3", "score2": "1", "winner": "FLC"}
            ]
        },
        {
            "matchId": "bootcamp26-m08", "key": "BC26_M08", "date": "2026-02-14", "time": "19:15",
            "phase": "Quarterfinals", "phaseKo": "8강전", "team1": "CR", "team2": "AG",
            "score1": 3, "score2": 0, "winner": "CR", "mvp": "LIP", "vod": "https://youtu.be/bc26_m8", "casters": ["Uber", "Mr X"],
            "sets": [
                {"map": "Antarctic Peninsula", "mapKo": "남극 반도", "mode": "Control", "score1": "2", "score2": "0", "winner": "CR"},
                {"map": "Dorado", "mapKo": "도라도", "mode": "Escort", "score1": "3", "score2": "1", "winner": "CR"},
                {"map": "Esperança", "mapKo": "이스페란사", "mode": "Push", "score1": "95.2m", "score2": "40.1m", "winner": "CR"}
            ]
        },

        # Semifinals
        {
            "matchId": "bootcamp26-m09", "key": "BC26_M09", "date": "2026-02-15", "time": "14:00",
            "phase": "Semifinals", "phaseKo": "준결승전", "team1": "TM", "team2": "TL",
            "score1": 3, "score2": 1, "winner": "TM", "mvp": "SirMajed", "vod": "https://youtu.be/bc26_m9", "casters": ["Uber", "Mr X"],
            "sets": [
                {"map": "Lijiang Tower", "mapKo": "리장 타워", "mode": "Control", "score1": "2", "score2": "1", "winner": "TM"},
                {"map": "Havana", "mapKo": "하바나", "mode": "Escort", "score1": "3", "score2": "2", "winner": "TM"},
                {"map": "Colosseo", "mapKo": "콜로세오", "mode": "Push", "score1": "62.0m", "score2": "88.0m", "winner": "TL"},
                {"map": "Eichenwalde", "mapKo": "아이헨발데", "mode": "Hybrid", "score1": "3", "score2": "1", "winner": "TM"}
            ]
        },
        {
            "matchId": "bootcamp26-m10", "key": "BC26_M10", "date": "2026-02-15", "time": "16:00",
            "phase": "Semifinals", "phaseKo": "준결승전", "team1": "CR", "team2": "FLC",
            "score1": 3, "score2": 2, "winner": "CR", "mvp": "HeeSang", "vod": "https://youtu.be/bc26_m10", "casters": ["AVRL", "Achilios"],
            "sets": [
                {"map": "Nepal", "mapKo": "네팔", "mode": "Control", "score1": "2", "score2": "1", "winner": "CR"},
                {"map": "Route 66", "mapKo": "66번 국도", "mode": "Escort", "score1": "2", "score2": "3", "winner": "FLC"},
                {"map": "Esperança", "mapKo": "이스페란사", "mode": "Push", "score1": "91.2m", "score2": "72.4m", "winner": "CR"},
                {"map": "Midtown", "mapKo": "미드타운", "mode": "Hybrid", "score1": "2", "score2": "3", "winner": "FLC"},
                {"map": "Ilios", "mapKo": "일리오스", "mode": "Control", "score1": "2", "score2": "1", "winner": "CR"}
            ]
        },

        # Grand Finals
        {
            "matchId": "bootcamp26-m11", "key": "BC26_M11", "date": "2026-02-15", "time": "18:30",
            "phase": "Grand Finals", "phaseKo": "최종 결승전", "team1": "TM", "team2": "CR",
            "score1": 4, "score2": 1, "winner": "TM", "mvp": "Quartz", "vod": "https://youtu.be/bc26_grand_final", "casters": ["Uber", "Mr X", "AVRL"],
            "sets": [
                {"map": "Ilios", "mapKo": "일리오스", "mode": "Control", "score1": "2", "score2": "0", "winner": "TM"},
                {"map": "Shambali Monastery", "mapKo": "샴발리 수도원", "mode": "Escort", "score1": "3", "score2": "2", "winner": "TM"},
                {"map": "Colosseo", "mapKo": "콜로세오", "mode": "Push", "score1": "70.1m", "score2": "94.5m", "winner": "CR"},
                {"map": "King's Row", "mapKo": "왕의 길", "mode": "Hybrid", "score1": "3", "score2": "2", "winner": "TM"},
                {"map": "Lijiang Tower", "mapKo": "리장 타워", "mode": "Control", "score1": "2", "score2": "1", "winner": "TM"}
            ]
        }
    ]

    return {
        "tournament": tournament,
        "mapPool": map_pool,
        "teams": teams,
        "teamNames": team_names,
        "matches": matches
    }

# ==============================================================================
# 3. OWCS 2026 Champions Clash
# ==============================================================================
def build_clash():
    tournament = {
        "id": "clash-2026",
        "name": "OWCS 2026 Champions Clash",
        "nameKo": "OWCS 2026 챔피언스 클래시",
        "startDate": "2026-05-22",
        "endDate": "2026-05-24",
        "status": "Completed",
        "statusKo": "대회 종료 (결과 확정)",
        "venue": "Shinjuku Sumitomo Hall (Tokyo, Japan)",
        "tier": "S-TIER",
        "tierKo": "S-TIER 국제 메이저 대회",
        "tierEn": "S-TIER International Major",
        "prizePool": "$100,000",
        "prizePoolKo": "총 상금 $100,000",
        "prizePoolEn": "Total Prize $100,000",
        "champion": "Crazy Raccoon",
        "runnerUp": "Twisted Minds"
    }

    map_pool = make_map_pool({
        "Control": ["Oasis", "Lijiang Tower", "Nepal", "Samoa", "Busan"],
        "Hybrid": ["Blizzard World", "Eichenwalde", "King's Row", "Midtown", "Paraíso"],
        "Flashpoint": ["New Junk City", "Suravasa"],
        "Push": ["Colosseo", "Esperança", "Runasapi"],
        "Escort": ["Circuit Royal", "Dorado", "Havana", "Route 66", "Watchpoint: Gibraltar"]
    })

    teams = [
        {"name": "Crazy Raccoon", "short": "CR", "color": "#ef4444", "seed": "Champion", "seedKo": "우승", "roster": [
            {"name": "Junbin", "role": "TANK"}, {"name": "MAX", "role": "TANK"},
            {"name": "LIP", "role": "DPS"}, {"name": "HeeSang", "role": "DPS"},
            {"name": "CHORONG", "role": "SPT"}, {"name": "SHUN", "role": "SPT"}
        ]},
        {"name": "Twisted Minds", "short": "TM", "color": "#22c55e", "seed": "Runner-up", "seedKo": "준우승", "roster": [
            {"name": "Kellon", "role": "TANK"}, {"name": "Quartz", "role": "DPS"},
            {"name": "LBBD7", "role": "DPS"}, {"name": "SirMajed", "role": "SPT"}, {"name": "Zox", "role": "SPT"}
        ]},
        {"name": "ZETA DIVISION", "short": "ZETA", "color": "#f59e0b", "seed": "3rd Place", "seedKo": "3위", "roster": [
            {"name": "Bernar", "role": "TANK"}, {"name": "Mealgaru", "role": "TANK"},
            {"name": "Proper", "role": "DPS"}, {"name": "knife", "role": "DPS"},
            {"name": "Viol2t", "role": "SPT"}, {"name": "Shu", "role": "SPT"}
        ]},
        {"name": "Virtus.pro", "short": "VP", "color": "#ea580c", "seed": "4th Place", "seedKo": "4위", "roster": [
            {"name": "Galaan", "role": "TANK"}, {"name": "Shockwave", "role": "DPS"},
            {"name": "khenail", "role": "SPT"}
        ]},
        {"name": "Spacestation Gaming", "short": "SSG", "color": "#eab308", "seed": "5th-6th Place", "seedKo": "5-6위", "roster": [
            {"name": "Hadi", "role": "TANK"}, {"name": "SparkR", "role": "DPS"},
            {"name": "Seicoe", "role": "DPS"}, {"name": "FunnyAstro", "role": "SPT"}, {"name": "Landon", "role": "SPT"}
        ]},
        {"name": "Dallas Fuel", "short": "DAL", "color": "#2563eb", "seed": "5th-6th Place", "seedKo": "5-6위", "roster": [
            {"name": "Fearless", "role": "TANK"}, {"name": "SP9RK1E", "role": "DPS"}, {"name": "ChiYo", "role": "SPT"}
        ]},
        {"name": "All Gamers", "short": "AG", "color": "#8b5cf6", "seed": "7th-8th Place", "seedKo": "7-8위", "roster": [
            {"name": "Guxue", "role": "TANK"}, {"name": "Leave", "role": "DPS"}, {"name": "Shy", "role": "DPS"}
        ]},
        {"name": "Weibo Gaming", "short": "WBG", "color": "#e11d48", "seed": "7th-8th Place", "seedKo": "7-8위", "roster": [
            {"name": "Lengsa", "role": "SPT"}, {"name": "Aprita", "role": "DPS"}
        ]}
    ]

    team_names = {t["short"]: t["name"] for t in teams}

    matches = [
        # Upper Bracket R1
        {
            "matchId": "clash26-m01", "key": "CC26_M01", "date": "2026-05-22", "time": "13:00",
            "phase": "Playoffs", "phaseKo": "승자조 1라운드 (UB R1)", "team1": "TM", "team2": "AG",
            "score1": 2, "score2": 0, "winner": "TM", "mvp": "Quartz", "vod": "https://youtu.be/P2l1TN-QkOU", "casters": ["Jaws", "AVRL"],
            "sets": [
                {"map": "Oasis", "mapKo": "오아시스", "mode": "Control", "score1": "2", "score2": "1", "winner": "TM", "bans": {"t1b1": "Symmetra", "t2b1": "Lucio", "banstart": 1}},
                {"map": "New Junk City", "mapKo": "뉴 정크 시티", "mode": "Flashpoint", "score1": "3", "score2": "0", "winner": "TM", "bans": {"t1b1": "Lucio", "t2b1": "Sojourn", "banstart": 1}}
            ]
        },
        {
            "matchId": "clash26-m02", "key": "CC26_M02", "date": "2026-05-22", "time": "14:30",
            "phase": "Playoffs", "phaseKo": "승자조 1라운드 (UB R1)", "team1": "VP", "team2": "WBG",
            "score1": 2, "score2": 1, "winner": "VP", "mvp": "Shockwave", "vod": "https://youtu.be/qEeRX0FYIMg", "casters": ["Gott", "Caster2"],
            "sets": [
                {"map": "Nepal", "mapKo": "네팔", "mode": "Control", "score1": "2", "score2": "1", "winner": "VP"},
                {"map": "Suravasa", "mapKo": "수라바사", "mode": "Flashpoint", "score1": "1", "score2": "3", "winner": "WBG"},
                {"map": "King's Row", "mapKo": "왕의 길", "mode": "Hybrid", "score1": "3", "score2": "2", "winner": "VP"}
            ]
        },
        {
            "matchId": "clash26-m03", "key": "CC26_M03", "date": "2026-05-22", "time": "16:00",
            "phase": "Playoffs", "phaseKo": "승자조 1라운드 (UB R1)", "team1": "ZETA", "team2": "SSG",
            "score1": 2, "score2": 0, "winner": "ZETA", "mvp": "Proper", "vod": "https://youtu.be/cc26_m3", "casters": ["Uber", "Mr X"],
            "sets": [
                {"map": "Lijiang Tower", "mapKo": "리장 타워", "mode": "Control", "score1": "2", "score2": "0", "winner": "ZETA"},
                {"map": "New Junk City", "mapKo": "뉴 정크 시티", "mode": "Flashpoint", "score1": "3", "score2": "1", "winner": "ZETA"}
            ]
        },
        {
            "matchId": "clash26-m04", "key": "CC26_M04", "date": "2026-05-22", "time": "17:30",
            "phase": "Playoffs", "phaseKo": "승자조 1라운드 (UB R1)", "team1": "CR", "team2": "DAL",
            "score1": 2, "score2": 0, "winner": "CR", "mvp": "LIP", "vod": "https://youtu.be/cc26_m4", "casters": ["Achilios", "AVRL"],
            "sets": [
                {"map": "Busan", "mapKo": "부산", "mode": "Control", "score1": "2", "score2": "1", "winner": "CR"},
                {"map": "Suravasa", "mapKo": "수라바사", "mode": "Flashpoint", "score1": "3", "score2": "0", "winner": "CR"}
            ]
        },

        # Upper Bracket Semifinals
        {
            "matchId": "clash26-m05", "key": "CC26_M05", "date": "2026-05-23", "time": "13:00",
            "phase": "Playoffs", "phaseKo": "승자조 준결승 (UB Semifinal)", "team1": "ZETA", "team2": "VP",
            "score1": 3, "score2": 1, "winner": "ZETA", "mvp": "Viol2t", "vod": "https://youtu.be/cc26_m5", "casters": ["Uber", "Mr X"],
            "sets": [
                {"map": "Oasis", "mapKo": "오아시스", "mode": "Control", "score1": "2", "score2": "0", "winner": "ZETA"},
                {"map": "King's Row", "mapKo": "왕의 길", "mode": "Hybrid", "score1": "3", "score2": "2", "winner": "ZETA"},
                {"map": "Esperança", "mapKo": "이스페란사", "mode": "Push", "score1": "64.0m", "score2": "89.2m", "winner": "VP"},
                {"map": "Circuit Royal", "mapKo": "서킷 로얄", "mode": "Escort", "score1": "3", "score2": "1", "winner": "ZETA"}
            ]
        },
        {
            "matchId": "clash26-m06", "key": "CC26_M06", "date": "2026-05-23", "time": "15:00",
            "phase": "Playoffs", "phaseKo": "승자조 준결승 (UB Semifinal)", "team1": "CR", "team2": "TM",
            "score1": 3, "score2": 2, "winner": "CR", "mvp": "Junbin", "vod": "https://youtu.be/cc26_m6", "casters": ["Achilios", "AVRL"],
            "sets": [
                {"map": "Nepal", "mapKo": "네팔", "mode": "Control", "score1": "2", "score2": "1", "winner": "CR"},
                {"map": "Blizzard World", "mapKo": "블리자드 월드", "mode": "Hybrid", "score1": "2", "score2": "3", "winner": "TM"},
                {"map": "Runasapi", "mapKo": "루나사피", "mode": "Push", "score1": "92.0m", "score2": "74.0m", "winner": "CR"},
                {"map": "Route 66", "mapKo": "66번 국도", "mode": "Escort", "score1": "2", "score2": "3", "winner": "TM"},
                {"map": "Lijiang Tower", "mapKo": "리장 타워", "mode": "Control", "score1": "2", "score2": "1", "winner": "CR"}
            ]
        },

        # Upper Bracket Final
        {
            "matchId": "clash26-m07", "key": "CC26_M07", "date": "2026-05-23", "time": "17:30",
            "phase": "Playoffs", "phaseKo": "승자조 결승 (UB Final)", "team1": "CR", "team2": "ZETA",
            "score1": 3, "score2": 1, "winner": "CR", "mvp": "HeeSang", "vod": "https://youtu.be/cc26_m7", "casters": ["Uber", "Mr X"],
            "sets": [
                {"map": "Samoa", "mapKo": "사모아", "mode": "Control", "score1": "2", "score2": "1", "winner": "CR"},
                {"map": "Eichenwalde", "mapKo": "아이헨발데", "mode": "Hybrid", "score1": "3", "score2": "2", "winner": "CR"},
                {"map": "Colosseo", "mapKo": "콜로세오", "mode": "Push", "score1": "60.1m", "score2": "85.4m", "winner": "ZETA"},
                {"map": "Havana", "mapKo": "하바나", "mode": "Escort", "score1": "3", "score2": "1", "winner": "CR"}
            ]
        },

        # Lower Bracket Matches
        {
            "matchId": "clash26-m08", "key": "CC26_M08", "date": "2026-05-24", "time": "12:00",
            "phase": "Playoffs", "phaseKo": "패자조 준결승 (LB Semifinal)", "team1": "TM", "team2": "VP",
            "score1": 3, "score2": 1, "winner": "TM", "mvp": "Quartz", "vod": "https://youtu.be/cc26_m8", "casters": ["Jaws", "CasterX"],
            "sets": [
                {"map": "Oasis", "mapKo": "오아시스", "mode": "Control", "score1": "2", "score2": "1", "winner": "TM"},
                {"map": "King's Row", "mapKo": "왕의 길", "mode": "Hybrid", "score1": "3", "score2": "2", "winner": "TM"},
                {"map": "Esperança", "mapKo": "이스페란사", "mode": "Push", "score1": "55.0m", "score2": "89.0m", "winner": "VP"},
                {"map": "Dorado", "mapKo": "도라도", "mode": "Escort", "score1": "3", "score2": "1", "winner": "TM"}
            ]
        },
        {
            "matchId": "clash26-m09", "key": "CC26_M09", "date": "2026-05-24", "time": "14:00",
            "phase": "Playoffs", "phaseKo": "패자조 결승 (LB Final)", "team1": "TM", "team2": "ZETA",
            "score1": 3, "score2": 2, "winner": "TM", "mvp": "SirMajed", "vod": "https://youtu.be/cc26_m9", "casters": ["Achilios", "AVRL"],
            "sets": [
                {"map": "Nepal", "mapKo": "네팔", "mode": "Control", "score1": "2", "score2": "1", "winner": "TM"},
                {"map": "Blizzard World", "mapKo": "블리자드 월드", "mode": "Hybrid", "score1": "2", "score2": "3", "winner": "ZETA"},
                {"map": "Runasapi", "mapKo": "루나사피", "mode": "Push", "score1": "94.2m", "score2": "70.1m", "winner": "TM"},
                {"map": "Circuit Royal", "mapKo": "서킷 로얄", "mode": "Escort", "score1": "2", "score2": "3", "winner": "ZETA"},
                {"map": "Busan", "mapKo": "부산", "mode": "Control", "score1": "2", "score2": "1", "winner": "TM"}
            ]
        },

        # Grand Finals
        {
            "matchId": "clash26-m10", "key": "CC26_M10", "date": "2026-05-24", "time": "16:30",
            "phase": "Playoffs", "phaseKo": "최종 결승전 (Grand Finals)", "team1": "CR", "team2": "TM",
            "score1": 4, "score2": 3, "winner": "CR", "mvp": "LIP", "vod": "https://youtu.be/cc26_grand_final", "casters": ["Uber", "Mr X", "Achilios"],
            "sets": [
                {"map": "Lijiang Tower", "mapKo": "리장 타워", "mode": "Control", "score1": "2", "score2": "1", "winner": "CR"},
                {"map": "King's Row", "mapKo": "왕의 길", "mode": "Hybrid", "score1": "2", "score2": "3", "winner": "TM"},
                {"map": "Colosseo", "mapKo": "콜로세오", "mode": "Push", "score1": "91.4m", "score2": "68.2m", "winner": "CR"},
                {"map": "Route 66", "mapKo": "66번 국도", "mode": "Escort", "score1": "2", "score2": "3", "winner": "TM"},
                {"map": "Samoa", "mapKo": "사모아", "mode": "Control", "score1": "2", "score2": "0", "winner": "CR"},
                {"map": "Esperança", "mapKo": "이스페란사", "mode": "Push", "score1": "74.1m", "score2": "90.5m", "winner": "TM"},
                {"map": "Havana", "mapKo": "하바나", "mode": "Escort", "score1": "3", "score2": "2", "winner": "CR"}
            ]
        }
    ]

    return {
        "tournament": tournament,
        "mapPool": map_pool,
        "teams": teams,
        "teamNames": team_names,
        "matches": matches
    }

# ==============================================================================
# 4. OWCS 2026 Midseason Championship
# ==============================================================================
def build_midseason():
    tournament = {
        "id": "midseason-2026",
        "name": "OWCS 2026 Midseason Championship",
        "nameKo": "OWCS 2026 미드시즌 챔피언십",
        "startDate": "2026-07-29",
        "endDate": "2026-08-02",
        "status": "Completed",
        "statusKo": "대회 종료 (결과 확정)",
        "venue": "Paris Expo Porte de Versailles (Paris, France)",
        "tier": "S-TIER",
        "tierKo": "S-TIER 글로벌 메이저 챔피언십",
        "tierEn": "S-TIER Global Midseason Championship",
        "prizePool": "$1,000,000",
        "prizePoolKo": "총 상금 $1,000,000",
        "prizePoolEn": "Total Prize $1,000,000",
        "champion": "ZETA DIVISION",
        "runnerUp": "Twisted Minds"
    }

    map_pool = make_map_pool({
        "Control": ["Nepal", "Lijiang Tower", "Busan", "Oasis", "Antarctic Peninsula"],
        "Hybrid": ["Neon Junction", "Blizzard World", "King's Row", "Midtown"],
        "Flashpoint": ["New Junk City", "Suravasa", "Aatlis"],
        "Push": ["Colosseo", "Esperança", "Runasapi"],
        "Escort": ["Route 66", "Circuit Royal", "Dorado", "Havana"]
    })

    teams = [
        {"name": "ZETA DIVISION", "short": "ZETA", "color": "#f59e0b", "seed": "Champion", "seedKo": "우승", "roster": [
            {"name": "Bernar", "role": "TANK"}, {"name": "Mealgaru", "role": "TANK"},
            {"name": "Proper", "role": "DPS"}, {"name": "knife", "role": "DPS"},
            {"name": "Viol2t", "role": "SPT"}, {"name": "Shu", "role": "SPT"}
        ]},
        {"name": "Twisted Minds", "short": "TM", "color": "#22c55e", "seed": "Runner-up", "seedKo": "준우승", "roster": [
            {"name": "Kellon", "role": "TANK"}, {"name": "Quartz", "role": "DPS"},
            {"name": "LBBD7", "role": "DPS"}, {"name": "SirMajed", "role": "SPT"}, {"name": "Zox", "role": "SPT"}
        ]},
        {"name": "Crazy Raccoon", "short": "CR", "color": "#ef4444", "seed": "3rd-4th Place", "seedKo": "3-4위", "roster": [
            {"name": "Junbin", "role": "TANK"}, {"name": "MAX", "role": "TANK"},
            {"name": "LIP", "role": "DPS"}, {"name": "HeeSang", "role": "DPS"},
            {"name": "CHORONG", "role": "SPT"}, {"name": "SHUN", "role": "SPT"}
        ]},
        {"name": "Spacestation Gaming", "short": "SSG", "color": "#eab308", "seed": "3rd-4th Place", "seedKo": "3-4위", "roster": [
            {"name": "Hadi", "role": "TANK"}, {"name": "SparkR", "role": "DPS"},
            {"name": "Seicoe", "role": "DPS"}, {"name": "FunnyAstro", "role": "SPT"}, {"name": "Landon", "role": "SPT"}
        ]},
        {"name": "T1", "short": "T1", "color": "#dc2626", "seed": "5th-6th Place", "seedKo": "5-6위", "roster": [
            {"name": "Belosrea", "role": "TANK"}, {"name": "Proud", "role": "DPS"},
            {"name": "Flora", "role": "DPS"}, {"name": "LeeJaeGon", "role": "SPT"}
        ]},
        {"name": "Dallas Fuel", "short": "DAL", "color": "#2563eb", "seed": "5th-6th Place", "seedKo": "5-6위", "roster": [
            {"name": "Fearless", "role": "TANK"}, {"name": "SP9RK1E", "role": "DPS"}
        ]},
        {"name": "Geekay Esports", "short": "GK", "color": "#14b8a6", "seed": "7th-8th Place", "seedKo": "7-8위", "roster": [
            {"name": "KSAA", "role": "TANK"}, {"name": "Youbi", "role": "DPS"}
        ]},
        {"name": "Weibo Gaming", "short": "WBG", "color": "#e11d48", "seed": "7th-8th Place", "seedKo": "7-8위", "roster": [
            {"name": "Lengsa", "role": "SPT"}, {"name": "Aprita", "role": "DPS"}
        ]}
    ]

    team_names = {t["short"]: t["name"] for t in teams}

    matches = [
        # Group Stage
        {
            "matchId": "mid26-m01", "key": "MID26_M01", "date": "2026-07-29", "time": "15:00",
            "phase": "Group Stage", "phaseKo": "조별 풀리그 (Group A)", "team1": "TM", "team2": "GK",
            "score1": 3, "score2": 1, "winner": "TM", "mvp": "Quartz", "vod": "https://youtu.be/CgBpRPMrot0", "casters": ["Uber", "Mr X"],
            "sets": [
                {"map": "Nepal", "mapKo": "네팔", "mode": "Control", "score1": "2", "score2": "0", "winner": "TM", "bans": {"t1b1": "Sojourn", "t2b1": "Jetpack Cat", "banstart": 1}},
                {"map": "Neon Junction", "mapKo": "네온 정션", "mode": "Hybrid", "score1": "1", "score2": "0", "winner": "TM", "bans": {"t1b1": "Mizuki", "t2b1": "Mauga", "banstart": 2}},
                {"map": "New Junk City", "mapKo": "뉴 정크 시티", "mode": "Flashpoint", "score1": "1", "score2": "3", "winner": "GK", "bans": {"t1b1": "Vendetta", "t2b1": "Reinhardt", "banstart": 2}},
                {"map": "Route 66", "mapKo": "66번 국도", "mode": "Escort", "score1": "3", "score2": "1", "winner": "TM", "bans": {"t1b1": "Tracer", "t2b1": "Ana", "banstart": 1}}
            ]
        },
        {
            "matchId": "mid26-m02", "key": "MID26_M02", "date": "2026-07-29", "time": "17:00",
            "phase": "Group Stage", "phaseKo": "조별 풀리그 (Group A)", "team1": "CR", "team2": "WBG",
            "score1": 3, "score2": 0, "winner": "CR", "mvp": "LIP", "vod": "https://youtu.be/mid26_m2", "casters": ["Achilios", "AVRL"],
            "sets": [
                {"map": "Busan", "mapKo": "부산", "mode": "Control", "score1": "2", "score2": "0", "winner": "CR"},
                {"map": "Blizzard World", "mapKo": "블리자드 월드", "mode": "Hybrid", "score1": "3", "score2": "1", "winner": "CR"},
                {"map": "Colosseo", "mapKo": "콜로세오", "mode": "Push", "score1": "95.0m", "score2": "34.0m", "winner": "CR"}
            ]
        },
        {
            "matchId": "mid26-m03", "key": "MID26_M03", "date": "2026-07-30", "time": "15:00",
            "phase": "Group Stage", "phaseKo": "조별 풀리그 (Group B)", "team1": "ZETA", "team2": "DAL",
            "score1": 3, "score2": 0, "winner": "ZETA", "mvp": "Proper", "vod": "https://youtu.be/mid26_m3", "casters": ["Uber", "Mr X"],
            "sets": [
                {"map": "Lijiang Tower", "mapKo": "리장 타워", "mode": "Control", "score1": "2", "score2": "0", "winner": "ZETA"},
                {"map": "King's Row", "mapKo": "왕의 길", "mode": "Hybrid", "score1": "3", "score2": "2", "winner": "ZETA"},
                {"map": "Esperança", "mapKo": "이스페란사", "mode": "Push", "score1": "92.0m", "score2": "50.1m", "winner": "ZETA"}
            ]
        },
        {
            "matchId": "mid26-m04", "key": "MID26_M04", "date": "2026-07-30", "time": "17:00",
            "phase": "Group Stage", "phaseKo": "조별 풀리그 (Group B)", "team1": "SSG", "team2": "T1",
            "score1": 3, "score2": 2, "winner": "SSG", "mvp": "SparkR", "vod": "https://youtu.be/mid26_m4", "casters": ["Jaws", "CasterX"],
            "sets": [
                {"map": "Oasis", "mapKo": "오아시스", "mode": "Control", "score1": "2", "score2": "1", "winner": "SSG"},
                {"map": "Midtown", "mapKo": "미드타운", "mode": "Hybrid", "score1": "2", "score2": "3", "winner": "T1"},
                {"map": "Runasapi", "mapKo": "루나사피", "mode": "Push", "score1": "88.0m", "score2": "71.0m", "winner": "SSG"},
                {"map": "Circuit Royal", "mapKo": "서킷 로얄", "mode": "Escort", "score1": "2", "score2": "3", "winner": "T1"},
                {"map": "Nepal", "mapKo": "네팔", "mode": "Control", "score1": "2", "score2": "1", "winner": "SSG"}
            ]
        },

        # Playoffs
        {
            "matchId": "mid26-m05", "key": "MID26_M05", "date": "2026-08-01", "time": "15:00",
            "phase": "Playoffs", "phaseKo": "4강 준결승전 (Semifinal 1)", "team1": "TM", "team2": "SSG",
            "score1": 3, "score2": 1, "winner": "TM", "mvp": "LBBD7", "vod": "https://youtu.be/mid26_m5", "casters": ["Achilios", "AVRL"],
            "sets": [
                {"map": "Nepal", "mapKo": "네팔", "mode": "Control", "score1": "2", "score2": "0", "winner": "TM"},
                {"map": "Neon Junction", "mapKo": "네온 정션", "mode": "Hybrid", "score1": "2", "score2": "3", "winner": "SSG"},
                {"map": "Colosseo", "mapKo": "콜로세오", "mode": "Push", "score1": "89.0m", "score2": "60.0m", "winner": "TM"},
                {"map": "Route 66", "mapKo": "66번 국도", "mode": "Escort", "score1": "3", "score2": "1", "winner": "TM"}
            ]
        },
        {
            "matchId": "mid26-m06", "key": "MID26_M06", "date": "2026-08-01", "time": "17:30",
            "phase": "Playoffs", "phaseKo": "4강 준결승전 (Semifinal 2)", "team1": "ZETA", "team2": "CR",
            "score1": 3, "score2": 2, "winner": "ZETA", "mvp": "Viol2t", "vod": "https://youtu.be/mid26_m6", "casters": ["Uber", "Mr X"],
            "sets": [
                {"map": "Lijiang Tower", "mapKo": "리장 타워", "mode": "Control", "score1": "2", "score2": "1", "winner": "ZETA"},
                {"map": "King's Row", "mapKo": "왕의 길", "mode": "Hybrid", "score1": "2", "score2": "3", "winner": "CR"},
                {"map": "Esperança", "mapKo": "이스페란사", "mode": "Push", "score1": "94.0m", "score2": "75.0m", "winner": "ZETA"},
                {"map": "Circuit Royal", "mapKo": "서킷 로얄", "mode": "Escort", "score1": "2", "score2": "3", "winner": "CR"},
                {"map": "Busan", "mapKo": "부산", "mode": "Control", "score1": "2", "score2": "1", "winner": "ZETA"}
            ]
        },

        # Grand Finals
        {
            "matchId": "mid26-m07", "key": "MID26_M07", "date": "2026-08-02", "time": "16:00",
            "phase": "Playoffs", "phaseKo": "최종 결승전 (Grand Finals)", "team1": "ZETA", "team2": "TM",
            "score1": 4, "score2": 2, "winner": "ZETA", "mvp": "Proper", "vod": "https://youtu.be/mid26_grand_final", "casters": ["Uber", "Mr X", "Achilios"],
            "sets": [
                {"map": "Nepal", "mapKo": "네팔", "mode": "Control", "score1": "2", "score2": "0", "winner": "ZETA", "bans": {"t1b1": "Sojourn", "t2b1": "D.Va", "banstart": 1}},
                {"map": "Neon Junction", "mapKo": "네온 정션", "mode": "Hybrid", "score1": "3", "score2": "2", "winner": "ZETA", "bans": {"t1b1": "Mizuki", "t2b1": "Mauga", "banstart": 2}},
                {"map": "New Junk City", "mapKo": "뉴 정크 시티", "mode": "Flashpoint", "score1": "1", "score2": "3", "winner": "TM", "bans": {"t1b1": "Tracer", "t2b1": "Lucio", "banstart": 2}},
                {"map": "Colosseo", "mapKo": "콜로세오", "mode": "Push", "score1": "92.4m", "score2": "65.1m", "winner": "ZETA", "bans": {"t1b1": "Lucio", "t2b1": "Kiriko", "banstart": 1}},
                {"map": "Route 66", "mapKo": "66번 국도", "mode": "Escort", "score1": "2", "score2": "3", "winner": "TM", "bans": {"t1b1": "Winston", "t2b1": "Sombra", "banstart": 2}},
                {"map": "Blizzard World", "mapKo": "블리자드 월드", "mode": "Hybrid", "score1": "3", "score2": "1", "winner": "ZETA", "bans": {"t1b1": "Mauga", "t2b1": "Ana", "banstart": 1}}
            ]
        }
    ]

    return {
        "tournament": tournament,
        "mapPool": map_pool,
        "teams": teams,
        "teamNames": team_names,
        "matches": matches
    }

# ==============================================================================
# 5. Overwatch World Cup 2026
# ==============================================================================
def build_owwc():
    tournament = {
        "id": "owwc-2026",
        "name": "Overwatch World Cup 2026",
        "nameKo": "오버워치 월드컵 2026",
        "startDate": "2026-10-28",
        "endDate": "2026-11-03",
        "status": "Completed",
        "statusKo": "대회 종료 (결과 확정)",
        "venue": "Busan BEXCO (Group Stage) · Anaheim Convention Center (Playoffs)",
        "tier": "S-TIER",
        "tierKo": "S-TIER 국가 대항전 월드컵",
        "tierEn": "S-TIER National Team World Championship",
        "prizePool": "$365,000",
        "prizePoolKo": "총 상금 $365,000",
        "prizePoolEn": "Total Prize $365,000",
        "champion": "South Korea",
        "runnerUp": "Saudi Arabia"
    }

    map_pool = make_map_pool({
        "Control": ["Busan", "Nepal", "Samoa", "Lijiang Tower", "Ilios"],
        "Hybrid": ["Neon Junction", "Blizzard World", "Eichenwalde", "King's Row", "Midtown"],
        "Flashpoint": ["Aatlis", "New Junk City", "Suravasa"],
        "Push": ["Esperança", "Colosseo", "Runasapi"],
        "Escort": ["Route 66", "Circuit Royal", "Dorado", "Havana", "Shambali Monastery"]
    })

    teams = [
        {"name": "South Korea", "short": "KOR", "color": "#0284c7", "seed": "Champion", "seedKo": "우승", "roster": [
            {"name": "Hanbin", "role": "TANK"}, {"name": "Proper", "role": "DPS"},
            {"name": "LIP", "role": "DPS"}, {"name": "SP9RK1E", "role": "DPS"},
            {"name": "Viol2t", "role": "SPT"}, {"name": "ChiYo", "role": "SPT"}, {"name": "Fielder", "role": "SPT"}
        ]},
        {"name": "Saudi Arabia", "short": "KSA", "color": "#16a34a", "seed": "Runner-up", "seedKo": "준우승", "roster": [
            {"name": "Ziyad", "role": "TANK"}, {"name": "Quartz", "role": "DPS"},
            {"name": "LBBD7", "role": "DPS"}, {"name": "SirMajed", "role": "SPT"}, {"name": "Zox", "role": "SPT"}
        ]},
        {"name": "France", "short": "FRA", "color": "#2563eb", "seed": "3rd Place", "seedKo": "3위", "roster": [
            {"name": "BenBest", "role": "TANK"}, {"name": "Pak", "role": "DPS"},
            {"name": "Naga", "role": "DPS"}, {"name": "FDGod", "role": "SPT"}, {"name": "Kellex", "role": "SPT"}
        ]},
        {"name": "Sweden", "short": "SWE", "color": "#eab308", "seed": "4th Place", "seedKo": "4위", "roster": [
            {"name": "LullSiSH", "role": "TANK"}, {"name": "SparkR", "role": "DPS"},
            {"name": "Kevster", "role": "DPS"}, {"name": "FunnyAstro", "role": "SPT"}
        ]},
        {"name": "Spain", "short": "ESP", "color": "#dc2626", "seed": "5th-8th Place", "seedKo": "5-8위", "roster": [
            {"name": "Santy", "role": "TANK"}, {"name": "Bones", "role": "DPS"},
            {"name": "Xzodyal", "role": "DPS"}, {"name": "Galaa", "role": "SPT"}, {"name": "Khenail", "role": "SPT"}
        ]},
        {"name": "Germany", "short": "GER", "color": "#f97316", "seed": "5th-8th Place", "seedKo": "5-8위", "roster": [
            {"name": "Hadi", "role": "TANK"}, {"name": "Higan", "role": "DPS"},
            {"name": "Phi", "role": "DPS"}, {"name": "Landon", "role": "SPT"}
        ]},
        {"name": "Australia", "short": "AUS", "color": "#10b981", "seed": "5th-8th Place", "seedKo": "5-8위", "roster": [
            {"name": "Cuffa", "role": "TANK"}, {"name": "Punk", "role": "TANK"},
            {"name": "Naahmie", "role": "DPS"}, {"name": "Colourhex", "role": "DPS"}
        ]},
        {"name": "United States", "short": "USA", "color": "#3b82f6", "seed": "5th-8th Place", "seedKo": "5-8위", "roster": [
            {"name": "super", "role": "TANK"}, {"name": "sugarfree", "role": "DPS"},
            {"name": "hydron", "role": "DPS"}, {"name": "cal", "role": "SPT"}, {"name": "Lep", "role": "SPT"}
        ]},
        {"name": "China", "short": "CHN", "color": "#ef4444", "seed": "9th-12th Place", "seedKo": "9-12위", "roster": [
            {"name": "Guxue", "role": "TANK"}, {"name": "Leave", "role": "DPS"},
            {"name": "Shy", "role": "DPS"}, {"name": "Mmonk", "role": "SPT"}
        ]},
        {"name": "Great Britain", "short": "GBR", "color": "#6366f1", "seed": "9th-12th Place", "seedKo": "9-12위", "roster": [
            {"name": "Fusions", "role": "TANK"}, {"name": "Kai", "role": "DPS"}
        ]},
        {"name": "Japan", "short": "JPN", "color": "#ec4899", "seed": "9th-12th Place", "seedKo": "9-12위", "roster": [
            {"name": "KSG", "role": "TANK"}, {"name": "Qki", "role": "DPS"}, {"name": "Nico", "role": "DPS"}
        ]},
        {"name": "Thailand", "short": "THA", "color": "#8b5cf6", "seed": "9th-12th Place", "seedKo": "9-12위", "roster": [
            {"name": "Mickie", "role": "TANK"}, {"name": "oPuTo", "role": "DPS"}
        ]}
    ]

    team_names = {t["short"]: t["name"] for t in teams}

    matches = [
        # Quarterfinals
        {
            "matchId": "owwc26-m01", "key": "OWWC26_QF1", "date": "2026-11-01", "time": "14:00",
            "phase": "Quarterfinals", "phaseKo": "8강 1경기", "team1": "KSA", "team2": "ESP",
            "score1": 3, "score2": 1, "winner": "KSA", "mvp": "Quartz", "vod": "https://www.youtube.com/watch?v=oBcta85_RMA", "casters": ["Uber", "Mr X"],
            "sets": [
                {"map": "Nepal", "mapKo": "네팔", "mode": "Control", "score1": "2", "score2": "0", "winner": "KSA", "bans": {"t1b1": "Sojourn", "t2b1": "Tracer", "banstart": 1}},
                {"map": "Route 66", "mapKo": "66번 국도", "mode": "Escort", "score1": "2", "score2": "3", "winner": "ESP", "bans": {"t1b1": "Sigma", "t2b1": "Widowmaker", "banstart": 2}},
                {"map": "Eichenwalde", "mapKo": "아이헨발데", "mode": "Hybrid", "score1": "3", "score2": "1", "winner": "KSA", "bans": {"t1b1": "Mauga", "t2b1": "Ana", "banstart": 1}},
                {"map": "Esperança", "mapKo": "이스페란사", "mode": "Push", "score1": "94.0m", "score2": "52.0m", "winner": "KSA", "bans": {"t1b1": "Lucio", "t2b1": "Kiriko", "banstart": 2}}
            ]
        },
        {
            "matchId": "owwc26-m02", "key": "OWWC26_QF2", "date": "2026-11-01", "time": "16:00",
            "phase": "Quarterfinals", "phaseKo": "8강 2경기", "team1": "SWE", "team2": "GER",
            "score1": 3, "score2": 0, "winner": "SWE", "mvp": "SparkR", "vod": "https://www.youtube.com/watch?v=oBcta85_RMA", "casters": ["Achilios", "AVRL"],
            "sets": [
                {"map": "Nepal", "mapKo": "네팔", "mode": "Control", "score1": "2", "score2": "0", "winner": "SWE"},
                {"map": "Route 66", "mapKo": "66번 국도", "mode": "Escort", "score1": "3", "score2": "1", "winner": "SWE"},
                {"map": "Midtown", "mapKo": "미드타운", "mode": "Hybrid", "score1": "3", "score2": "1", "winner": "SWE"}
            ]
        },
        {
            "matchId": "owwc26-m03", "key": "OWWC26_QF3", "date": "2026-11-01", "time": "18:00",
            "phase": "Quarterfinals", "phaseKo": "8강 3경기", "team1": "FRA", "team2": "AUS",
            "score1": 3, "score2": 0, "winner": "FRA", "mvp": "Pak", "vod": "https://www.youtube.com/watch?v=oBcta85_RMA", "casters": ["Jaws", "CasterX"],
            "sets": [
                {"map": "Samoa", "mapKo": "사모아", "mode": "Control", "score1": "2", "score2": "0", "winner": "FRA"},
                {"map": "Shambali Monastery", "mapKo": "샴발리 수도원", "mode": "Escort", "score1": "3", "score2": "1", "winner": "FRA"},
                {"map": "Midtown", "mapKo": "미드타운", "mode": "Hybrid", "score1": "3", "score2": "2", "winner": "FRA"}
            ]
        },
        {
            "matchId": "owwc26-m04", "key": "OWWC26_QF4", "date": "2026-11-01", "time": "20:00",
            "phase": "Quarterfinals", "phaseKo": "8강 4경기", "team1": "USA", "team2": "KOR",
            "score1": 1, "score2": 3, "winner": "KOR", "mvp": "Proper", "vod": "https://www.youtube.com/watch?v=oBcta85_RMA", "casters": ["Uber", "Mr X"],
            "sets": [
                {"map": "Busan", "mapKo": "부산", "mode": "Control", "score1": "0", "score2": "2", "winner": "KOR", "bans": {"t1b1": "Ana", "t2b1": "Bastion", "banstart": 2}},
                {"map": "Neon Junction", "mapKo": "네온 정션", "mode": "Hybrid", "score1": "1", "score2": "2", "winner": "KOR", "bans": {"t1b1": "Mauga", "t2b1": "Mizuki", "banstart": 1}},
                {"map": "Aatlis", "mapKo": "아틀리스", "mode": "Flashpoint", "score1": "3", "score2": "2", "winner": "USA", "bans": {"t1b1": "Tracer", "t2b1": "Lucio", "banstart": 1}},
                {"map": "Route 66", "mapKo": "66번 국도", "mode": "Escort", "score1": "2", "score2": "3", "winner": "KOR", "bans": {"t1b1": "Winston", "t2b1": "Sombra", "banstart": 2}}
            ]
        },

        # Semifinals
        {
            "matchId": "owwc26-m05", "key": "OWWC26_SF1", "date": "2026-11-02", "time": "15:00",
            "phase": "Semifinals", "phaseKo": "4강 준결승 1경기", "team1": "KSA", "team2": "SWE",
            "score1": 3, "score2": 1, "winner": "KSA", "mvp": "LBBD7", "vod": "https://youtu.be/owwc26_sf1", "casters": ["Achilios", "AVRL"],
            "sets": [
                {"map": "Nepal", "mapKo": "네팔", "mode": "Control", "score1": "2", "score2": "0", "winner": "KSA"},
                {"map": "Blizzard World", "mapKo": "블리자드 월드", "mode": "Hybrid", "score1": "3", "score2": "2", "winner": "KSA"},
                {"map": "Colosseo", "mapKo": "콜로세오", "mode": "Push", "score1": "64.0m", "score2": "90.2m", "winner": "SWE"},
                {"map": "Circuit Royal", "mapKo": "서킷 로얄", "mode": "Escort", "score1": "3", "score2": "1", "winner": "KSA"}
            ]
        },
        {
            "matchId": "owwc26-m06", "key": "OWWC26_SF2", "date": "2026-11-02", "time": "17:30",
            "phase": "Semifinals", "phaseKo": "4강 준결승 2경기", "team1": "KOR", "team2": "FRA",
            "score1": 3, "score2": 0, "winner": "KOR", "mvp": "LIP", "vod": "https://youtu.be/owwc26_sf2", "casters": ["Uber", "Mr X"],
            "sets": [
                {"map": "Busan", "mapKo": "부산", "mode": "Control", "score1": "2", "score2": "0", "winner": "KOR"},
                {"map": "King's Row", "mapKo": "왕의 길", "mode": "Hybrid", "score1": "3", "score2": "1", "winner": "KOR"},
                {"map": "Esperança", "mapKo": "이스페란사", "mode": "Push", "score1": "95.4m", "score2": "42.0m", "winner": "KOR"}
            ]
        },

        # 3rd Place Match
        {
            "matchId": "owwc26-m07", "key": "OWWC26_3RD", "date": "2026-11-03", "time": "14:00",
            "phase": "3rd Place Match", "phaseKo": "3·4위전", "team1": "FRA", "team2": "SWE",
            "score1": 3, "score2": 2, "winner": "FRA", "mvp": "FDGod", "vod": "https://youtu.be/owwc26_3rd", "casters": ["Jaws", "CasterX"],
            "sets": [
                {"map": "Samoa", "mapKo": "사모아", "mode": "Control", "score1": "2", "score2": "1", "winner": "FRA"},
                {"map": "Midtown", "mapKo": "미드타운", "mode": "Hybrid", "score1": "2", "score2": "3", "winner": "SWE"},
                {"map": "Runasapi", "mapKo": "루나사피", "mode": "Push", "score1": "89.0m", "score2": "74.0m", "winner": "FRA"},
                {"map": "Route 66", "mapKo": "66번 국도", "mode": "Escort", "score1": "2", "score2": "3", "winner": "SWE"},
                {"map": "Ilios", "mapKo": "일리오스", "mode": "Control", "score1": "2", "score2": "1", "winner": "FRA"}
            ]
        },

        # Grand Finals
        {
            "matchId": "owwc26-m08", "key": "OWWC26_GF", "date": "2026-11-03", "time": "16:30",
            "phase": "Grand Finals", "phaseKo": "최종 결승전 (Grand Finals)", "team1": "KOR", "team2": "KSA",
            "score1": 4, "score2": 1, "winner": "KOR", "mvp": "Proper", "vod": "https://youtu.be/owwc26_grand_final", "casters": ["Uber", "Mr X", "Achilios"],
            "sets": [
                {"map": "Busan", "mapKo": "부산", "mode": "Control", "score1": "2", "score2": "0", "winner": "KOR", "bans": {"t1b1": "Sojourn", "t2b1": "Ana", "banstart": 1}},
                {"map": "Neon Junction", "mapKo": "네온 정션", "mode": "Hybrid", "score1": "3", "score2": "2", "winner": "KOR", "bans": {"t1b1": "Mauga", "t2b1": "Mizuki", "banstart": 2}},
                {"map": "Aatlis", "mapKo": "아틀리스", "mode": "Flashpoint", "score1": "2", "score2": "3", "winner": "KSA", "bans": {"t1b1": "Tracer", "t2b1": "Lucio", "banstart": 2}},
                {"map": "Esperança", "mapKo": "이스페란사", "mode": "Push", "score1": "96.5m", "score2": "60.4m", "winner": "KOR", "bans": {"t1b1": "Lucio", "t2b1": "Kiriko", "banstart": 1}},
                {"map": "Route 66", "mapKo": "66번 국도", "mode": "Escort", "score1": "3", "score2": "1", "winner": "KOR", "bans": {"t1b1": "Winston", "t2b1": "Sombra", "banstart": 1}}
            ]
        }
    ]

    return {
        "tournament": tournament,
        "mapPool": map_pool,
        "teams": teams,
        "teamNames": team_names,
        "matches": matches
    }

def main():
    print("Generating datasets for 5 new tournaments...")
    
    asia_s1 = build_asia_s1()
    write_js_preview("OWCS_ASIA_S1_PREVIEW", asia_s1, DATA_DIR / "asia_s1_preview.js")
    
    bootcamp = build_bootcamp()
    write_js_preview("OWCS_BOOTCAMP_PREVIEW", bootcamp, DATA_DIR / "bootcamp_preview.js")
    
    clash = build_clash()
    write_js_preview("OWCS_CLASH_PREVIEW", clash, DATA_DIR / "clash_preview.js")
    
    midseason = build_midseason()
    write_js_preview("OWCS_MIDSEASON_PREVIEW", midseason, DATA_DIR / "midseason_preview.js")
    
    owwc = build_owwc()
    write_js_preview("OWCS_OWWC_PREVIEW", owwc, DATA_DIR / "owwc_preview.js")

    print("All 5 tournament preview datasets generated successfully!")

if __name__ == "__main__":
    main()
