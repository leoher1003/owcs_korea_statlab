#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_stage2_preview_js.py
Generates owcs-stat-lab 2/data/stage2_preview.js with complete Stage 2 data from stage2_matches.json.
"""

import os
import json

def generate_stage2_preview():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "owcs-stat-lab 2", "data", "stage2_matches.json")
    out_path = os.path.join(base_dir, "owcs-stat-lab 2", "data", "stage2_preview.js")
    
    with open(json_path, "r", encoding="utf-8") as f:
        matches = json.load(f)
        
    teams_roster = [
        {
            "name": "Crazy Raccoon", "short": "CR", "color": "#e11d48",
            "seed": "Champion", "seedKo": "우승",
            "roster": [
                {"name": "JunBin", "role": "TANK"},
                {"name": "MAX", "role": "TANK"},
                {"name": "LIP", "role": "DPS"},
                {"name": "HeeSang", "role": "DPS"},
                {"name": "Stalk3r", "role": "DPS"},
                {"name": "CH0R0NG", "role": "SPT"},
                {"name": "vigilante", "role": "SPT"}
            ]
        },
        {
            "name": "Team Falcons", "short": "FLC", "color": "#10b981",
            "seed": "Runner-up", "seedKo": "준우승",
            "roster": [
                {"name": "SOMEONE", "role": "TANK"},
                {"name": "Hanbin", "role": "TANK"},
                {"name": "SP1NT", "role": "DPS"},
                {"name": "Checkmate", "role": "DPS"},
                {"name": "MER1T", "role": "DPS"},
                {"name": "ChiYo", "role": "SPT"},
                {"name": "Fielder", "role": "SPT"}
            ]
        },
        {
            "name": "T1", "short": "T1", "color": "#ef4444",
            "seed": "3rd Place", "seedKo": "3위",
            "roster": [
                {"name": "DONGHAK", "role": "TANK"},
                {"name": "Jasm1ne", "role": "TANK"},
                {"name": "ZEST", "role": "DPS"},
                {"name": "Proud", "role": "DPS"},
                {"name": "FLETA", "role": "SPT"},
                {"name": "Bliss", "role": "SPT"},
                {"name": "skewed", "role": "SPT"}
            ]
        },
        {
            "name": "ZETA DIVISION", "short": "ZETA", "color": "#f59e0b",
            "seed": "4th Place", "seedKo": "4위",
            "roster": [
                {"name": "Bernar", "role": "TANK"},
                {"name": "Mealgaru", "role": "TANK"},
                {"name": "Proper", "role": "DPS"},
                {"name": "knife", "role": "DPS"},
                {"name": "Viol2t", "role": "SPT"},
                {"name": "Shu", "role": "SPT"}
            ]
        },
        {
            "name": "Røde Zanside Gaming", "short": "ROZE", "color": "#6366f1",
            "seed": "5th Place", "seedKo": "5위",
            "roster": [
                {"name": "Void", "role": "TANK"},
                {"name": "Heiser", "role": "TANK"},
                {"name": "Becky", "role": "DPS"},
                {"name": "Kilo", "role": "DPS"},
                {"name": "Probe", "role": "DPS"},
                {"name": "Opener", "role": "SPT"},
                {"name": "Irony", "role": "SPT"}
            ]
        },
        {
            "name": "Cheeseburger", "short": "CB", "color": "#eab308",
            "seed": "6th Place", "seedKo": "6위",
            "roster": [
                {"name": "Farmer", "role": "TANK"},
                {"name": "GUR3UM", "role": "TANK"},
                {"name": "Argon", "role": "DPS"},
                {"name": "M1nut2", "role": "DPS"},
                {"name": "TENTEN", "role": "SPT"},
                {"name": "woochan", "role": "SPT"}
            ]
        },
        {
            "name": "O2 Blast", "short": "O2", "color": "#06b6d4",
            "seed": "7th Place", "seedKo": "7위",
            "roster": [
                {"name": "Fate", "role": "TANK"},
                {"name": "Seungan", "role": "TANK"},
                {"name": "WuTian", "role": "DPS"},
                {"name": "Perr", "role": "DPS"},
                {"name": "Faith", "role": "SPT"},
                {"name": "Misin", "role": "SPT"},
                {"name": "Gamjung", "role": "SPT"}
            ]
        },
        {
            "name": "Poker Face", "short": "PF", "color": "#ec4899",
            "seed": "8th Place", "seedKo": "8위",
            "roster": [
                {"name": "Fearless", "role": "TANK"},
                {"name": "Hyeon", "role": "TANK"},
                {"name": "D0d0", "role": "DPS"},
                {"name": "K4NE", "role": "DPS"},
                {"name": "Sp1nel", "role": "SPT"},
                {"name": "Caru", "role": "SPT"}
            ]
        },
        {
            "name": "SuperBad", "short": "SB", "color": "#8b5cf6",
            "seed": "9th Place", "seedKo": "9위",
            "roster": [
                {"name": "Sentier", "role": "TANK"},
                {"name": "Homerunball", "role": "TANK"},
                {"name": "Azent", "role": "DPS"},
                {"name": "Sori", "role": "DPS"},
                {"name": "Soae", "role": "SPT"},
                {"name": "Dumbbell", "role": "SPT"},
                {"name": "Univ2r", "role": "SPT"}
            ]
        }
    ]

    map_pool = {
        "regular": {
            "Control": {
                "type": "Control", "nameKo": "쟁탈", "nameEn": "Control", "color": "#10b981", "icon": "🎯",
                "maps": [
                    {"nameKo": "남극 반도", "nameEn": "Antarctic Peninsula"},
                    {"nameKo": "일리오스", "nameEn": "Ilios"},
                    {"nameKo": "오아시스", "nameEn": "Oasis"}
                ]
            },
            "Hybrid": {
                "type": "Hybrid", "nameKo": "혼합", "nameEn": "Hybrid", "color": "#f59e0b", "icon": "⚔️",
                "maps": [
                    {"nameKo": "할리우드", "nameEn": "Hollywood"},
                    {"nameKo": "왕의 길", "nameEn": "King's Row"},
                    {"nameKo": "눔바니", "nameEn": "Numbani"}
                ]
            },
            "Flashpoint": {
                "type": "Flashpoint", "nameKo": "플래시포인트", "nameEn": "Flashpoint", "color": "#ec4899", "icon": "⚡",
                "maps": [
                    {"nameKo": "수라바사", "nameEn": "Suravasa"},
                    {"nameKo": "뉴 정크 시티", "nameEn": "New Junk City"}
                ]
            },
            "Push": {
                "type": "Push", "nameKo": "밀기", "nameEn": "Push", "color": "#8b5cf6", "icon": "🤖",
                "maps": [
                    {"nameKo": "루나사피", "nameEn": "Runasapi"},
                    {"nameKo": "뉴 퀸 스트리트", "nameEn": "New Queen Street"}
                ]
            },
            "Escort": {
                "type": "Escort", "nameKo": "호위", "nameEn": "Escort", "color": "#3b82f6", "icon": "🚛",
                "maps": [
                    {"nameKo": "서킷 로얄", "nameEn": "Circuit Royal"},
                    {"nameKo": "도라도", "nameEn": "Dorado"},
                    {"nameKo": "리알토", "nameEn": "Rialto"}
                ]
            }
        }
    }

    # Format matches to ensure standard keys
    clean_matches = []
    for m in matches:
        clean_m = dict(m)
        clean_m["matchId"] = m.get("matchId") or f"kr26-s2-{m.get('team1')}-{m.get('team2')}"
        clean_matches.append(clean_m)

    data_obj = {
        "tournament": {
            "name": "OWCS Korea 2026 Stage 2",
            "nameKo": "OWCS 코리아 2026 스테이지 2",
            "startDate": "2026-06-05",
            "endDate": "2026-07-19",
            "status": "Completed",
            "statusKo": "대회 종료 (결과 확정)",
            "venue": "WDG Esports Studio (Seoul)",
            "tier": "A-TIER",
            "tierKo": "A-TIER 대회",
            "tierEn": "A-TIER Tournament",
            "prizePool": "$38,500",
            "prizePoolKo": "총 상금 $38,500",
            "prizePoolEn": "Total Prize $38,500"
        },
        "teams": teams_roster,
        "mapPool": map_pool,
        "matches": clean_matches
    }

    js_content = "window.OWCS_STAGE2_PREVIEW = " + json.dumps(data_obj, ensure_ascii=False, indent=2) + ";\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"Generated {out_path} with {len(clean_matches)} matches.")

if __name__ == "__main__":
    generate_stage2_preview()
