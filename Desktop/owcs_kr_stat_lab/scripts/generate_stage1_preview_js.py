#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_stage1_preview_js.py
Generates owcs-stat-lab 2/data/stage1_preview.js with complete Stage 1 data:
tournament meta, map pool, rosters, standings, and 51 match objects with sets.
"""

import os
import json

def generate_js():
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "owcs-stat-lab 2", "data", "stage1_matches.json")
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "owcs-stat-lab 2", "data", "stage1_preview.js")
    
    with open(json_path, "r", encoding="utf-8") as f:
        matches = json.load(f)
        
    teams_roster = [
        {
            "name": "ZETA DIVISION", "short": "ZETA", "color": "#f59e0b",
            "seed": "Champion", "seedKo": "우승",
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
            "name": "Team Falcons", "short": "FLC", "color": "#10b981",
            "seed": "Runner-up", "seedKo": "준우승",
            "roster": [
                {"name": "Hanbin", "role": "TANK"},
                {"name": "SOMEONE", "role": "TANK"},
                {"name": "Checkmate", "role": "DPS"},
                {"name": "MER1T", "role": "DPS"},
                {"name": "ChiYo", "role": "SPT"},
                {"name": "Fielder", "role": "SPT"}
            ]
        },
        {
            "name": "Crazy Raccoon", "short": "CR", "color": "#e11d48",
            "seed": "3rd Place", "seedKo": "3위",
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
            "name": "T1", "short": "T1", "color": "#ef4444",
            "seed": "4th Place", "seedKo": "4위",
            "roster": [
                {"name": "DONGHAK", "role": "TANK"},
                {"name": "jasm1ne", "role": "TANK"},
                {"name": "Proud", "role": "DPS"},
                {"name": "ZEST", "role": "DPS"},
                {"name": "skewed", "role": "SPT"},
                {"name": "Bliss", "role": "SPT"}
            ]
        },
        {
            "name": "ONSIDE GAMING", "short": "OSG", "color": "#38bdf8",
            "seed": "5-6th", "seedKo": "5~6위",
            "roster": [
                {"name": "Attack", "role": "TANK"},
                {"name": "SP1NT", "role": "DPS"},
                {"name": "Kilo", "role": "DPS"},
                {"name": "Haksal", "role": "DPS"},
                {"name": "OPENER", "role": "SPT"},
                {"name": "IRONY", "role": "SPT"}
            ]
        },
        {
            "name": "ZAN Esports", "short": "ZAN", "color": "#64748b",
            "seed": "5-6th", "seedKo": "5~6위",
            "roster": [
                {"name": "HEISER", "role": "TANK"},
                {"name": "A1IEN", "role": "DPS"},
                {"name": "Probe", "role": "DPS"},
                {"name": "Becky", "role": "DPS"},
                {"name": "Havira", "role": "SPT"},
                {"name": "YangIun", "role": "SPT"},
                {"name": "KIVIS", "role": "SPT"}
            ]
        },
        {
            "name": "Poker Face", "short": "PF", "color": "#a855f7",
            "seed": "7th", "seedKo": "7위",
            "roster": [
                {"name": "Fearful", "role": "TANK"},
                {"name": "Gur3um", "role": "TANK"},
                {"name": "M1nut2", "role": "DPS"},
                {"name": "D4RT", "role": "DPS"},
                {"name": "TenTen", "role": "SPT"},
                {"name": "CARU", "role": "SPT"},
                {"name": "Sp1nel", "role": "SPT"}
            ]
        },
        {
            "name": "Cheeseburger", "short": "CB", "color": "#f97316",
            "seed": "8th", "seedKo": "8위",
            "roster": [
                {"name": "FARMER", "role": "TANK"},
                {"name": "SeungAn", "role": "TANK"},
                {"name": "Argon", "role": "DPS"},
                {"name": "Zesin", "role": "DPS"},
                {"name": "Jamelgong", "role": "DPS"},
                {"name": "WoochaN", "role": "SPT"},
                {"name": "Faith", "role": "SPT"}
            ]
        },
        {
            "name": "New Era", "short": "ERA", "color": "#94a3b8",
            "seed": "9th", "seedKo": "9위",
            "roster": [
                {"name": "SoLA", "role": "TANK"},
                {"name": "Yate", "role": "TANK"},
                {"name": "D0DO", "role": "DPS"},
                {"name": "Perr", "role": "DPS"},
                {"name": "Secret", "role": "SPT"},
                {"name": "MCD", "role": "SPT"}
            ]
        }
    ]
    
    stage1_obj = {
        "tournament": {
            "name": "OWCS Korea 2026 Stage 1",
            "nameKo": "OWCS 코리아 2026 스테이지 1",
            "startDate": "2026-03-20",
            "endDate": "2026-05-03",
            "status": "Completed",
            "statusKo": "대회 종료 (결과 확정)",
            "venue": "WDG Esports Studio (Seoul)",
            "tier": "A-TIER",
            "tierKo": "A-TIER 대회",
            "tierEn": "A-TIER Tournament",
            "prizePool": "$38,500",
            "prizePoolKo": "총 상금 $38,500",
            "prizePoolEn": "Total Prize $38,500",
            "champion": "ZETA DIVISION"
        },
        "mapPool": {
            "Control": {
                "type": "Control", "nameKo": "쟁탈", "nameEn": "Control", "color": "#10b981", "icon": "🎯",
                "maps": [
                    {"nameKo": "부산", "nameEn": "Busan"},
                    {"nameKo": "리장 타워", "nameEn": "Lijiang Tower"},
                    {"nameKo": "네팔", "nameEn": "Nepal"},
                    {"nameKo": "사모아", "nameEn": "Samoa"}
                ]
            },
            "Hybrid": {
                "type": "Hybrid", "nameKo": "혼합", "nameEn": "Hybrid", "color": "#f59e0b", "icon": "⚔️",
                "maps": [
                    {"nameKo": "블리자드 월드", "nameEn": "Blizzard World"},
                    {"nameKo": "아이헨발데", "nameEn": "Eichenwalde"},
                    {"nameKo": "왕의 길", "nameEn": "King's Row"},
                    {"nameKo": "눔바니", "nameEn": "Numbani"}
                ]
            },
            "Flashpoint": {
                "type": "Flashpoint", "nameKo": "플래시포인트", "nameEn": "Flashpoint", "color": "#06b6d4", "icon": "⚡",
                "maps": [
                    {"nameKo": "뉴 정크 시티", "nameEn": "New Junk City"},
                    {"nameKo": "수라바사", "nameEn": "Suravasa"}
                ]
            },
            "Push": {
                "type": "Push", "nameKo": "밀기", "nameEn": "Push", "color": "#a855f7", "icon": "🤖",
                "maps": [
                    {"nameKo": "콜로세오", "nameEn": "Colosseo"},
                    {"nameKo": "이스페란사", "nameEn": "Esperança"},
                    {"nameKo": "루나사피", "nameEn": "Runasapi"}
                ]
            },
            "Escort": {
                "type": "Escort", "nameKo": "호위", "nameEn": "Escort", "color": "#3b82f6", "icon": "🚛",
                "maps": [
                    {"nameKo": "서킷 로얄", "nameEn": "Circuit Royal"},
                    {"nameKo": "도라도", "nameEn": "Dorado"},
                    {"nameKo": "하바나", "nameEn": "Havana"},
                    {"nameKo": "66번 국도", "nameEn": "Route 66"}
                ]
            }
        },
        "teams": teams_roster,
        "teamNames": {
            "ZETA": "ZETA DIVISION",
            "FLC": "Team Falcons",
            "CR": "Crazy Raccoon",
            "T1": "T1",
            "OSG": "ONSIDE GAMING",
            "ZAN": "ZAN Esports",
            "PF": "Poker Face",
            "CB": "Cheeseburger",
            "ERA": "New Era"
        },
        "matches": matches
    }
    
    js_content = "window.OWCS_STAGE1_PREVIEW = " + json.dumps(stage1_obj, ensure_ascii=False, indent=2) + ";\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"Generated {out_path} with {len(matches)} matches.")

if __name__ == "__main__":
    generate_js()
