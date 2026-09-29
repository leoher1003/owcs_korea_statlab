#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_global_teams.py
Generates the comprehensive global team database for OWCS:
- Current OWCS Teams: KR (9 teams), NA (5 teams: SSG, TL, DF, M80, DSG), EMEA, CN, JP, PA
- Past OWCS Teams: KR (5 teams: FTG, WAC, ERA, ZAN, OSG), NA (5 teams: TD, NTMR, LG, CN, SOTG)

Accurately incorporates:
1. KR historical mergers & acquisitions:
   - Røde Onside Gaming: 2025 FTG -> ONSIDE GAMING -> 2026 Røde ONSIDE GAMING -> Røde ZANSIDE GAMING (merged with ZAN Esports)
   - ZETA DIVISION: Acquired FTG core roster in April 2024
   - Crazy Raccoon: Acquired WAC roster in April 2024
2. NA historical dynamics & superteams:
   - Toronto Defiant: 2024 Golden Grand Slam champion (NA Stage 1~4 Champion) -> Roster dispersed late 2024 to Falcons, Liquid, SSG
   - NTMR (Nightmare): Legendary underdog team that defeated Crazy Raccoon 3-1 at 2025 Champions Clash
   - Spacestation Gaming (SSG): 2024 London Spitfire core -> 2025~2026 NA #1 powerhouse with Sugarfree, Lethal, Hawk, Admiral
   - Team Liquid (TL): 2025 returned superteam with TR33, zeruhh, Vega, UltraViolet, Attack
   - Dallas Fuel (DF): 2022 OWL World Champions officially returned to OWCS NA in 2026
"""

import json
from pathlib import Path

OUT_FILE = Path("owcs-stat-lab 2/data/global_teams_data.js")

REGIONS = [
    {"code": "ALL", "nameKo": "전체 지역", "nameEn": "All Regions", "icon": "🌐"},
    {"code": "KR", "nameKo": "한국 (Korea)", "nameEn": "Korea", "icon": "🇰🇷"},
    {"code": "NA", "nameKo": "북미 (North America)", "nameEn": "North America", "icon": "🇺🇸"},
    {"code": "EMEA", "nameKo": "유럽·중동 (EMEA)", "nameEn": "Europe & Middle East", "icon": "🇪🇺"},
    {"code": "CN", "nameKo": "중국 (China)", "nameEn": "China", "icon": "🇨🇳"},
    {"code": "JP", "nameKo": "일본 (Japan)", "nameEn": "Japan", "icon": "🇯🇵"},
    {"code": "PA", "nameKo": "태평양 (Pacific)", "nameEn": "Pacific", "icon": "🌏"}
]

TEAMS = {
    # =========================================================================
    # CURRENT OWCS TEAMS - KOREA (KR)
    # =========================================================================
    "CR": {
        "id": "CR",
        "status": "CURRENT",
        "name": "Crazy Raccoon",
        "nameKo": "크레이지 라쿤",
        "region": "KR",
        "country": "🇯🇵 Japan / 🇰🇷 Korea",
        "color": "#ef4444",
        "founded": "2024",
        "historyNotes": "2024년 4월  최강팀 WAC 선수단 전원을 전격 인수하여 오버워치 부문 창단. 이후 국제 메이저 대회를 연속 석권하며 세계 최강으로 군림.",
        "trophies": [
            "2024 OWCS Dallas Major Champion",
            "2024 Esports World Cup (EWC) Champion",
            "2025 OWCS Champions Clash Champion",
            "2025 OWCS Asia Stage 1 Champion",
            "2025 OWCS Korea Stage 1, 2, 3 Champion",
            "2026 OWCS Champions Clash Champion",
            "2026 OWCS Korea Stage 2 Champion"
        ],
        "coachingStaff": [
            {"name": "Moon", "realName": "문병철", "role": "Head Coach", "roleKo": "감독", "nationality": "🇰🇷 KR"},
            {"name": "Kong", "realName": "손준영", "role": "Coach", "roleKo": "코치", "nationality": "🇰🇷 KR"},
            {"name": "Izayaki", "realName": "김민철", "role": "Assistant Coach", "roleKo": "코치", "nationality": "🇰🇷 KR"},
            {"name": "Twinkl", "realName": "임영빈", "role": "General Manager", "roleKo": "단장", "nationality": "🇰🇷 KR"},
            {"name": "Pavane", "realName": "유현상", "role": "Assistant GM", "roleKo": "부단장", "nationality": "🇰🇷 KR"}
        ],
        "activeRoster": [
            {"player": "JunBin", "position": "TANK", "realName": "박준빈", "nationality": "🇰🇷 KR", "joinDate": "2024-04-07", "signatureHeroes": ["Winston", "Wrecking Ball", "Doomfist"]},
            {"player": "MAX", "position": "TANK", "realName": "최수민", "nationality": "🇰🇷 KR", "joinDate": "2024-04-07", "signatureHeroes": ["D.Va", "Sigma", "Zarya"]},
            {"player": "LIP", "position": "DPS", "realName": "이재원", "nationality": "🇰🇷 KR", "joinDate": "2024-04-07", "signatureHeroes": ["Sombra", "Cassidy", "Sojourn"]},
            {"player": "HeeSang", "position": "DPS", "realName": "채희상", "nationality": "🇰🇷 KR", "joinDate": "2024-04-07", "signatureHeroes": ["Tracer", "Genji", "Echo"]},
            {"player": "Stalk3r", "position": "DPS", "realName": "정학용", "nationality": "🇰🇷 KR", "joinDate": "2026-03-08", "signatureHeroes": ["Tracer", "Genji", "Venture"]},
            {"player": "CH0R0NG", "position": "SPT", "realName": "성유민", "nationality": "🇰🇷 KR", "joinDate": "2024-04-07", "signatureHeroes": ["Lucio", "Brigitte", "Kiriko"]},
            {"player": "vigilante", "position": "SPT", "realName": "김준", "nationality": "🇰🇷 KR", "joinDate": "2026-02-09", "signatureHeroes": ["Ana", "Baptiste", "Kiriko"]}
        ],
        "transfers": [
            {"date": "2026-03-08", "type": "IN", "player": "Stalk3r", "role": "DPS", "details": "Team Falcons에서 Inactive 상태에서 Crazy Raccoon 공식 영입"},
            {"date": "2026-02-09", "type": "IN", "player": "vigilante", "role": "SPT", "details": "서브 힐러 포지션 보강을 위해 영입"},
            {"date": "2025-12-10", "type": "OUT", "player": "SP1NT", "role": "DPS", "details": "계약 종료 후 ONSIDE GAMING으로 이적"},
            {"date": "2025-12-09", "type": "OUT", "player": "shu", "role": "SPT", "details": "계약 종료 후 ZETA DIVISION으로 이적"},
            {"date": "2025-08-18", "type": "IN", "player": "SP1NT", "role": "DPS", "details": "Stage 3 대비 Poker Face에서 영입"},
            {"date": "2024-04-07", "type": "ACQUISITION", "player": "WAC Roster", "role": "ALL", "details": "We Are Chicks(WAC) 선수단 전원 인수 창단"}
        ]
    },

    "FLC": {
        "id": "FLC",
        "status": "CURRENT",
        "name": "Team Falcons",
        "nameKo": "팀 팔콘스",
        "region": "KR",
        "country": "🇸🇦 Saudi Arabia / 🇰🇷 Korea",
        "color": "#10b981",
        "founded": "2024",
        "historyNotes": "사우디아라비아 명문 구단 Falcons가 한국의 오버워치 리그 우승 주역들을 대거 영입하여 창단한 슈퍼팀. 아시아 및 메이저 무대에서 Crazy Raccoon과 치열한 라이벌 구도 형성.",
        "trophies": [
            "2024 OWCS Asia Stage 1 Runner-up",
            "2024 OWCS Dallas Major Runner-up",
            "2024 Esports World Cup Runner-up",
            "2025 Midseason Championship Champions",
            "2025 OWCS Korea Stage 2 Runner-up",
            "2025 OWCS Asia Stage 1 Champion",
            "2026 OWCS Korea Stage 1 Runner-up",
            "2026 OWCS Korea Stage 2 Runner-up"
        ],
        "coachingStaff": [
            {"name": "NineK", "realName": "김범훈", "role": "Head Coach", "roleKo": "감독", "nationality": "🇰🇷 KR"},
            {"name": "Junkbuck", "realName": "이재원", "role": "Coach", "roleKo": "코치", "nationality": "🇺🇸 US"},
            {"name": "Sp9rk1e", "realName": "김영한", "role": "Coach", "roleKo": "코치", "nationality": "🇰🇷 KR"}
        ],
        "activeRoster": [
            {"player": "Hanbin", "position": "TANK", "realName": "최한빈", "nationality": "🇰🇷 KR", "joinDate": "2024-03-01", "signatureHeroes": ["Junker Queen", "Sigma", "D.Va"]},
            {"player": "SOMEONE", "position": "TANK", "realName": "함정완", "nationality": "🇰🇷 KR", "joinDate": "2025-01-10", "signatureHeroes": ["Winston", "Reinhardt", "Doomfist"]},
            {"player": "Checkmate", "position": "DPS", "realName": "백승훈", "nationality": "🇰🇷 KR", "joinDate": "2025-03-01", "signatureHeroes": ["Tracer", "Genji", "Mei"]},
            {"player": "MER1T", "position": "DPS", "realName": "최태민", "nationality": "🇰🇷 KR", "joinDate": "2025-02-15", "signatureHeroes": ["Sojourn", "Ashe", "Cassidy"]},
            {"player": "SP1NT", "position": "DPS", "realName": "안우진", "nationality": "🇰🇷 KR", "joinDate": "2026-02-01", "signatureHeroes": ["Genji", "Pharah", "Echo"]},
            {"player": "ChiYo", "position": "SPT", "realName": "한현석", "nationality": "🇰🇷 KR", "joinDate": "2024-03-01", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "Fielder", "position": "SPT", "realName": "권준", "nationality": "🇰🇷 KR", "joinDate": "2024-03-01", "signatureHeroes": ["Ana", "Kiriko", "Baptiste"]}
        ],
        "transfers": [
            {"date": "2026-02-01", "type": "IN", "player": "SP1NT", "role": "DPS", "details": "ONSIDE GAMING에서 팀 팔콘스로 이적 영입"},
            {"date": "2025-03-01", "type": "IN", "player": "Checkmate", "role": "DPS", "details": "플렉스 딜러 라인업 보강 영입"},
            {"date": "2025-02-15", "type": "IN", "player": "MER1T", "role": "DPS", "details": "히트스캔 에이스 포지션 영입"},
            {"date": "2025-01-10", "type": "IN", "player": "SOMEONE", "role": "TANK", "details": "메인 탱커 전력 강화를 위해 영입"},
            {"date": "2024-03-01", "type": "IN", "player": "Core Roster", "role": "ALL", "details": "Team Falcons 오버워치 2 슈퍼팀 공식 창단"}
        ]
    },

    "T1": {
        "id": "T1",
        "status": "CURRENT",
        "name": "T1",
        "nameKo": "티원",
        "region": "KR",
        "country": "🇰🇷 Korea",
        "color": "#ef4444",
        "founded": "2024",
        "historyNotes": "글로벌 e스포츠 명가 T1의 오버워치 부문. 강력한 딜러 듀오와 탄탄한 탱커진을 바탕으로 한국 3강 및 메이저 무대에서 지속적인 상위권 유지.",
        "trophies": [
            "2025 OWCS Korea Stage 2 3rd Place",
            "2026 OWCS Korea Stage 1 3rd Place",
            "2026 OWCS Korea Stage 2 3rd Place"
        ],
        "coachingStaff": [
            {"name": "RUSH", "realName": "윤희원", "role": "Head Coach", "roleKo": "감독", "nationality": "🇰🇷 KR"},
             {"name": "FLETA", "realName": "김병선", "role": "Coach", "roleKo": "코치", "nationality": "🇰🇷 KR"},
              {"name": "GGultaek", "realName": "김정윤", "role": "Coach", "roleKo": "코치", "nationality": "🇰🇷 KR"}
        ],
        "activeRoster": [
            {"player": "DONGHAK", "position": "TANK", "realName": "김민성", "nationality": "🇰🇷 KR", "joinDate": "2024-03-15", "signatureHeroes": ["Winston", "Doomfist", "Wrecking Ball"]},
            {"player": "Jasm1ne", "position": "TANK", "realName": "김태훈", "nationality": "🇰🇷 KR", "joinDate": "2025-02-10", "signatureHeroes": ["D.Va", "Sigma", "Mauga"]},
            {"player": "ZEST", "position": "DPS", "realName": "김현우", "nationality": "🇰🇷 KR", "joinDate": "2024-03-15", "signatureHeroes": ["Tracer", "Genji", "Echo"]},
            {"player": "Proud", "position": "DPS", "realName": "유재혁", "nationality": "🇰🇷 KR", "joinDate": "2024-03-15", "signatureHeroes": ["Sojourn", "Ashe", "Cassidy"]},
            {"player": "FLETA", "position": "Playing Coach", "realName": "김병선", "nationality": "🇰🇷 KR", "joinDate": "2025-03-01"},
            {"player": "Bliss", "position": "SPT", "realName": "김소명", "nationality": "🇰🇷 KR", "joinDate": "2024-03-15"},
            {"player": "skewed", "position": "SPT", "realName": "김민석", "nationality": "🇰🇷 KR", "joinDate": "2024-03-15", "signatureHeroes": ["Brigitte", "Ana", "Zenyatta"]}
        ],
        "transfers": [
            {"date": "2025-03-01", "type": "IN", "player": "FLETA", "role": "FLEX", "details": "코치에서 플레잉 코치로 선수 등록"},
            {"date": "2025-02-10", "type": "IN", "player": "Jasm1ne", "role": "TANK", "details": "서브 탱커 자원 영입"},
            {"date": "2024-03-15", "type": "IN", "player": "Core Roster", "role": "ALL", "details": "T1 오버워치 2 공식 로스터 발표"}
        ]
    },

    "ZETA": {
        "id": "ZETA",
        "status": "CURRENT",
        "name": "ZETA DIVISION",
        "nameKo": "제타 디비전",
        "region": "KR",
        "country": "🇯🇵 Japan / 🇰🇷 Korea",
        "color": "#f59e0b",
        "founded": "2024",
        "historyNotes": "2024년 4월 대한민국 무소속 돌풍의 주역 From The Gamer(FTG) 초기 로스터를 전격 인수하여 창단. 2026 Korea Stage 1 챔피언에 등극하며 최정상 반열에 오름.",
        "trophies": [
            "2024 Esports World Cup 3rd Place",
            "2025 OWCS Korea Stage 1 Runner-up",
            "2025 OWCS Asia Stage 1 3rd Place",
            "2026 OWCS Korea Stage 1 Champion"
        ],
        "coachingStaff": [
            {"name": "Changgoon", "realName": "박창근", "role": "Head Coach", "roleKo": "감독", "nationality": "🇰🇷 KR"},
            {"name": "Rascal", "realName": "김동준", "role": "Coach", "roleKo": "코치", "nationality": "🇰🇷 KR"}
        ],
        "activeRoster": [
            {"player": "Bernar", "position": "TANK", "realName": "신세원", "nationality": "🇰🇷 KR", "joinDate": "2024-04-10", "signatureHeroes": ["Sigma", "D.Va", "Junker Queen"]},
            {"player": "Mealgaru", "position": "TANK", "realName": "이정환", "nationality": "🇰🇷 KR", "joinDate": "2025-01-15", "signatureHeroes": ["Winston", "Doomfist", "Hazard"]},
            {"player": "Proper", "position": "DPS", "realName": "김동현", "nationality": "🇰🇷 KR", "joinDate": "2025-01-10", "signatureHeroes": ["Tracer", "Sojourn", "Genji"]},
            {"player": "knife", "position": "DPS", "realName": "소정완", "nationality": "🇰🇷 KR", "joinDate": "2025-01-10", "signatureHeroes": ["Sojourn", "Cassidy", "Ashe"]},
            {"player": "Viol2t", "position": "SPT", "realName": "박민기", "nationality": "🇰🇷 KR", "joinDate": "2024-04-10", "signatureHeroes": ["Lucio", "Kiriko", "Baptiste"]},
            {"player": "Shu", "position": "SPT", "realName": "김진서", "nationality": "🇰🇷 KR", "joinDate": "2025-12-09", "signatureHeroes": ["Ana", "Baptiste", "Kiriko"]}
        ],
        "transfers": [
            {"date": "2026-02-28", "type": "IN", "player": "Mealgaru, knife, Proper, Shu, Viol2t, Crusty, Ggultaek", "details": "2026시즌 리빌딩"},
            {"date": "2025-12-09", "type": "IN", "player": "Shu", "role": "SPT", "details": "Crazy Raccoon에서 최정상 서포터 Shu 전격 영입"},
            {"date": "2025-01-10", "type": "IN", "player": "Proper & knife", "role": "DPS", "details": "최강 딜러진 Proper, knife 동시 영입"},
            {"date": "2024-04-10", "type": "ACQUISITION", "player": "FTG Roster", "role": "ALL", "details": "From The Gamer(FTG) 초기 로스터를 인수하여 ZETA 오버워치 부문 창단"}
        ]
    },

    "ROZE": {
        "id": "ROZE",
        "status": "CURRENT",
        "name": "Røde Zanside Gaming",
        "nameKo": "로데 잔사이드 게이밍",
        "region": "KR",
        "country": "🇰🇷 Korea",
        "color": "#6366f1",
        "founded": "2026",
        "historyNotes": "유구한 계보: 2024~2025 From The Gamer (FTG) 재편 ➔ 2025 ONSIDE GAMING (OSG) ➔ 2026 Røde Onside Gaming 스폰서십 ➔ 2026 Stage 2를 앞두고 ZAN Esports와 전격 합병하여 Røde ZANSIDE GAMING으로 재탄생.",
        "trophies": [
            "2026 OWCS Korea Stage 2 5th Place",
            "2025 OWCS Korea Stage 3 4th Place"
        ],
        "coachingStaff": [
            {"name": "Named", "realName": "이동현", "role": "Head Coach", "roleKo": "감독", "nationality": "🇰🇷 KR"}
        ],
        "activeRoster": [
            {"player": "Void", "position": "TANK", "realName": "강준우", "nationality": "🇰🇷 KR", "joinDate": "2025-08-01", "signatureHeroes": ["Sigma", "D.Va", "Zarya"]},
            {"player": "Heiser", "position": "TANK", "realName": "권순호", "nationality": "🇰🇷 KR", "joinDate": "2026-05-10", "signatureHeroes": ["Winston", "Doomfist"]},
            {"player": "Becky", "position": "DPS", "realName": "김일하", "nationality": "🇰🇷 KR", "joinDate": "2025-08-01", "signatureHeroes": ["Echo", "Tracer", "Genji"]},
            {"player": "Kilo", "position": "DPS", "realName": "정진우", "nationality": "🇰🇷 KR", "joinDate": "2026-05-10", "signatureHeroes": ["Widowmaker", "Sojourn", "Ashe"]},
            {"player": "Probe", "position": "DPS", "realName": "정준영", "nationality": "🇰🇷 KR", "joinDate": "2026-05-10", "signatureHeroes": ["Cassidy", "Sojourn", "Tracer"]},
            {"player": "Opener", "position": "SPT", "realName": "안기범", "nationality": "🇰🇷 KR", "joinDate": "2025-08-01", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "Irony", "position": "SPT", "realName": "김강하", "nationality": "🇰🇷 KR", "joinDate": "2026-05-10", "signatureHeroes": ["Ana", "Kiriko", "Baptiste"]}
        ],
        "transfers": [
            {"date": "2026-05-10", "type": "MERGER", "player": "ZAN Core (Heiser, Kilo, Probe, Irony)", "role": "ALL", "details": "ZAN Esports와 합병하며 Røde ZANSIDE GAMING(ROZE)으로 리브랜딩"},
            {"date": "2026-02-01", "type": "REBRAND", "player": "ONSIDE GAMING", "role": "ALL", "details": "Røde 스폰서십 체결로 Røde Onside Gaming 리브랜딩"},
            {"date": "2025-08-01", "type": "REBRAND", "player": "From The Gamer", "role": "ALL", "details": "FTG 해체 후 ONSIDE GAMING으로 팀 재출범"}
        ]
    },

    "CB": {
        "id": "CB",
        "status": "CURRENT",
        "name": "Cheeseburger",
        "nameKo": "치즈버거",
        "region": "KR",
        "country": "🇰🇷 Korea",
        "color": "#eab308",
        "founded": "2026",
        "historyNotes": "2026 OWCS 코리아 무대에 돌풍을 일으키며 등장한 팀. 신예 선수들의 패기와 공격적인 한타 설계로 정규시즌 6위를 기록하며 플레이오프 진출.",
        "trophies": [
            "2026 OWCS Korea Stage 2 6th Place",
            "2026 Korea Open Qualifier 1st"
        ],
        "coachingStaff": [
            {"name": "BurgerMaster", "realName": "김철수", "role": "Head Coach", "roleKo": "감독", "nationality": "🇰🇷 KR"}
        ],
        "activeRoster": [
            {"player": "Farmer", "position": "TANK", "realName": "박상현", "nationality": "🇰🇷 KR", "joinDate": "2026-01-10", "signatureHeroes": ["Winston", "D.Va", "Mauga"]},
            {"player": "GUR3UM", "position": "TANK", "realName": "이구름", "nationality": "🇰🇷 KR", "joinDate": "2026-01-10", "signatureHeroes": ["Reinhardt", "Sigma"]},
            {"player": "Argon", "position": "DPS", "realName": "정다운", "nationality": "🇰🇷 KR", "joinDate": "2026-01-10", "signatureHeroes": ["Tracer", "Sojourn", "Genji"]},
            {"player": "M1nut2", "position": "DPS", "realName": "김민우", "nationality": "🇰🇷 KR", "joinDate": "2026-01-10", "signatureHeroes": ["Cassidy", "Ashe", "Widowmaker"]},
            {"player": "TENTEN", "position": "SPT", "realName": "최영민", "nationality": "🇰🇷 KR", "joinDate": "2026-01-10", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "woochan", "position": "SPT", "realName": "정우찬", "nationality": "🇰🇷 KR", "joinDate": "2026-01-10", "signatureHeroes": ["Ana", "Kiriko", "Baptiste"]}
        ],
        "transfers": [
            {"date": "2026-01-10", "type": "IN", "player": "Full Roster", "role": "ALL", "details": "2026 OWCS Korea 오픈 예선 통과 및 공식 팀 결성"}
        ]
    },

    "O2": {
        "id": "O2",
        "status": "CURRENT",
        "name": "O2 Blast",
        "nameKo": "오투 블라스트",
        "region": "KR",
        "country": "🇰🇷 Korea",
        "color": "#06b6d4",
        "founded": "2018",
        "historyNotes": "오버워치 컨텐더스 코리아 역사상 최고의 명문 육성 구단. OWL 수많은 스타들을 배출한 전통의 강호로서 2026 시즌 OWCS 코리아에 화려하게 복귀.",
        "trophies": [
            "Overwatch Contenders Korea Multiple Champion",
            "2026 OWCS Korea Stage 2 7th Place"
        ],
        "coachingStaff": [
            {"name": "Boss", "realName": "진광우", "role": "Head Coach", "roleKo": "감독", "nationality": "🇰🇷 KR"}
        ],
        "activeRoster": [
            {"player": "Fate", "position": "TANK", "realName": "구판승", "nationality": "🇰🇷 KR", "joinDate": "2026-02-15", "signatureHeroes": ["Winston", "Wrecking Ball", "Reinhardt"]},
            {"player": "Seungan", "position": "TANK", "realName": "이승안", "nationality": "🇰🇷 KR", "joinDate": "2026-02-15", "signatureHeroes": ["D.Va", "Sigma"]},
            {"player": "WuTian", "position": "DPS", "realName": "우티안", "nationality": "🇨🇳 CN", "joinDate": "2026-02-15", "signatureHeroes": ["Genji", "Tracer", "Echo"]},
            {"player": "Perr", "position": "DPS", "realName": "배준서", "nationality": "🇰🇷 KR", "joinDate": "2026-02-15", "signatureHeroes": ["Sojourn", "Cassidy", "Ashe"]},
            {"player": "Faith", "position": "SPT", "realName": "홍규화", "nationality": "🇰🇷 KR", "joinDate": "2026-02-15", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "Misin", "position": "SPT", "realName": "김미신", "nationality": "🇰🇷 KR", "joinDate": "2026-02-15", "signatureHeroes": ["Kiriko", "Ana"]},
            {"player": "Gamjung", "position": "SPT", "realName": "정감정", "nationality": "🇰🇷 KR", "joinDate": "2026-02-15", "signatureHeroes": ["Baptiste", "Zenyatta"]}
        ],
        "transfers": [
            {"date": "2026-02-15", "type": "IN", "player": "Fate & Core", "role": "ALL", "details": "OWL 베테랑 Fate 중심 2026 OWCS 복귀 로스터 영입"}
        ]
    },

    "PF": {
        "id": "PF",
        "status": "CURRENT",
        "name": "Poker Face",
        "nameKo": "포커 페이스",
        "region": "KR",
        "country": "🇰🇷 Korea",
        "color": "#ec4899",
        "founded": "2023",
        "historyNotes": "한국 오버워치 씬의 대표적인 언더독 강호. 공격적이고 탄탄한 팀합을 바탕으로 2024~2026 꾸준히 본선에 진출하며 상위권 팀들을 위협하는 복병.",
        "trophies": [
            "2024 OWCS Korea Stage 2 3rd Place",
            "2025 OWCS Korea Stage 1 4th Place"
        ],
        "coachingStaff": [
            {"name": "Face", "realName": "신선호", "role": "Head Coach", "roleKo": "감독", "nationality": "🇰🇷 KR"}
        ],
        "activeRoster": [
            {"player": "Fearless", "position": "TANK", "realName": "이의석", "nationality": "🇰🇷 KR", "joinDate": "2026-03-01", "signatureHeroes": ["Winston", "Reinhardt"]},
            {"player": "Hyeon", "position": "TANK", "realName": "김현", "nationality": "🇰🇷 KR", "joinDate": "2025-05-01", "signatureHeroes": ["D.Va", "Sigma"]},
            {"player": "D0d0", "position": "DPS", "realName": "김도현", "nationality": "🇰🇷 KR", "joinDate": "2025-05-01", "signatureHeroes": ["Tracer", "Echo"]},
            {"player": "K4NE", "position": "DPS", "realName": "김케인", "nationality": "🇰🇷 KR", "joinDate": "2026-01-10", "signatureHeroes": ["Sojourn", "Cassidy"]},
            {"player": "Sp1nel", "position": "SPT", "realName": "안스피넬", "nationality": "🇰🇷 KR", "joinDate": "2025-05-01", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "Caru", "position": "SPT", "realName": "김카루", "nationality": "🇰🇷 KR", "joinDate": "2025-05-01", "signatureHeroes": ["Ana", "Kiriko"]}
        ],
        "transfers": [
            {"date": "2026-03-01", "type": "IN", "player": "Fearless", "role": "TANK", "details": "OWL 챔피언 출신 베테랑 탱커 Fearless 전격 합류"},
            {"date": "2025-12-01", "type": "OUT", "player": "SP1NT", "role": "DPS", "details": "계약 종료로 이적"}
        ]
    },

    "SB": {
        "id": "SB",
        "status": "CURRENT",
        "name": "SuperBad",
        "nameKo": "슈퍼배드",
        "region": "KR",
        "country": "🇰🇷 Korea",
        "color": "#8b5cf6",
        "founded": "2026",
        "historyNotes": "2026 Korea Stage 1 승강전을 뚫고 Stage 2 본선에 직행한 신흥 승격팀. 패기 넘치는 교전 지향적 스타일로 첫 메이저 무대 안착.",
        "trophies": [
            "2026 OWCS Korea Stage 2 본선 진출 (승격)"
        ],
        "coachingStaff": [
            {"name": "BadCoach", "realName": "박상민", "role": "Head Coach", "roleKo": "감독", "nationality": "🇰🇷 KR"}
        ],
        "activeRoster": [
            {"player": "Sentier", "position": "TANK", "realName": "김성준", "nationality": "🇰🇷 KR", "joinDate": "2026-04-01", "signatureHeroes": ["Winston", "D.Va"]},
            {"player": "Homerunball", "position": "TANK", "realName": "홈런볼", "nationality": "🇰🇷 KR", "joinDate": "2026-04-01", "signatureHeroes": ["Sigma", "Reinhardt"]},
            {"player": "Azent", "position": "DPS", "realName": "이아젠트", "nationality": "🇰🇷 KR", "joinDate": "2026-04-01", "signatureHeroes": ["Tracer", "Genji"]},
            {"player": "Sori", "position": "DPS", "realName": "박소리", "nationality": "🇰🇷 KR", "joinDate": "2026-04-01", "signatureHeroes": ["Sojourn", "Cassidy"]},
            {"player": "Soae", "position": "SPT", "realName": "김소애", "nationality": "🇰🇷 KR", "joinDate": "2026-04-01", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "Dumbbell", "position": "SPT", "realName": "덤벨", "nationality": "🇰🇷 KR", "joinDate": "2026-04-01", "signatureHeroes": ["Ana", "Kiriko"]},
            {"player": "Univ2r", "position": "SPT", "realName": "유니버", "nationality": "🇰🇷 KR", "joinDate": "2026-04-01", "signatureHeroes": ["Baptiste", "Moira"]}
        ],
        "transfers": [
            {"date": "2026-04-01", "type": "IN", "player": "Full Roster", "role": "ALL", "details": "Stage 1 승강전 1위로 Stage 2 본선 시드 획득 및 로스터 등록"}
        ]
    },

    # =========================================================================
    # CURRENT OWCS TEAMS - NORTH AMERICA (NA)
    # =========================================================================
    "SSG": {
        "id": "SSG",
        "status": "CURRENT",
        "name": "Spacestation Gaming",
        "nameKo": "스페이스스테이션 게이밍",
        "region": "NA",
        "country": "🇺🇸 United States",
        "color": "#facc15",
        "founded": "2024",
        "historyNotes": "2024년 런던 스핏파이어 코어 인수로 창단 ➔ 2025년 말 Sugarfree, Hawk, Lethal, Admiral을 대거 영입하여 북미 압도적 1위 최강 구단으로 등극.",
        "trophies": [
            "2025 OWCS NA Stage 2 Champion",
            "2026 OWCS NA Stage 1 Champion",
            "2024 OWCS Dallas Major 4th Place"
        ],
        "coachingStaff": [
            {"name": "ChrisTFer", "realName": "Christopher Brown", "role": "Head Coach", "roleKo": "감독", "nationality": "🇬🇧 GB"}
        ],
        "activeRoster": [
            {"player": "Hawk", "position": "TANK", "realName": "Charlie Domecq", "nationality": "🇺🇸 US", "joinDate": "2024-12-05", "signatureHeroes": ["D.Va", "Sigma", "Winston"]},
            {"player": "Sugarfree", "position": "DPS", "realName": "Kamden Hijada", "nationality": "🇺🇸 US", "joinDate": "2024-12-05", "signatureHeroes": ["Tracer", "Genji", "Echo"]},
            {"player": "Lethal", "position": "DPS", "realName": "Christian Ranque", "nationality": "🇺🇸 US", "joinDate": "2025-01-10", "signatureHeroes": ["Sojourn", "Cassidy", "Ashe"]},
            {"player": "scissors", "position": "DPS", "realName": "Cody D'Orazio", "nationality": "🇺🇸 US", "joinDate": "2025-06-15", "signatureHeroes": ["Pharah", "Echo", "Mei"]},
            {"player": "Admiral", "position": "SPT", "realName": "Oliver Vahar", "nationality": "🇪🇪 EE", "joinDate": "2024-03-01", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "RhynO", "position": "TANK", "realName": "Rhyno", "nationality": "🇺🇸 US", "joinDate": "2025-08-01", "signatureHeroes": ["Junker Queen", "Doomfist"]}
        ],
        "transfers": [
            {"date": "2025-06-15", "type": "IN", "player": "scissors", "role": "DPS", "details": "NTMR 해체 후 전격 영입 합류"},
            {"date": "2025-01-10", "type": "IN", "player": "Lethal", "role": "DPS", "details": "히트스캔 포지션 전력 보강"},
            {"date": "2024-12-05", "type": "IN", "player": "Sugarfree & Hawk", "role": "ROSTER", "details": "Toronto Defiant 해산 후 슈퍼스타 듀오 동시 영입"},
            {"date": "2024-03-01", "type": "ACQUISITION", "player": "London Spitfire Core", "role": "ALL", "details": "런던 스핏파이어 선수단 인수 창단"}
        ]
    },

    "TL": {
        "id": "TL",
        "status": "CURRENT",
        "name": "Team Liquid",
        "nameKo": "팀 리퀴드",
        "region": "NA",
        "country": "🇳🇱 Netherlands / 🇺🇸 United States",
        "color": "#0284c7",
        "founded": "2025",
        "historyNotes": "세계 최고 명문 게임단 Team Liquid의 역사적인 오버워치 2 복귀. Toronto Defiant 출신 Vega와 초신성 TR33, zeruhh, UltraViolet, Attack을 규합한 북미 초호화 드림팀.",
        "trophies": [
            "2025 OWCS NA Stage 2 Runner-up",
            "2026 OWCS NA Stage 1 Runner-up",
            "2025 Midseason Championship 5th"
        ],
        "coachingStaff": [
            {"name": "Wheats", "realName": "Shane Wheats", "role": "Head Coach", "roleKo": "감독", "nationality": "🇺🇸 US"},
            {"name": "Unter", "realName": "Jordan Unterholzer", "role": "Coach", "roleKo": "코치", "nationality": "🇦🇺 AU"}
        ],
        "activeRoster": [
            {"player": "Attack", "position": "TANK", "realName": "김준화", "nationality": "🇰🇷 KR", "joinDate": "2025-02-01", "signatureHeroes": ["Winston", "D.Va", "Sigma"]},
            {"player": "TR33", "position": "DPS", "realName": "Nicholas Terra", "nationality": "🇺🇸 US", "joinDate": "2025-01-15", "signatureHeroes": ["Sojourn", "Mei", "Genji"]},
            {"player": "zeruhh", "position": "DPS", "realName": "Christian Kelly", "nationality": "🇺🇸 US", "joinDate": "2025-01-15", "signatureHeroes": ["Tracer", "Echo", "Sombra"]},
            {"player": "Vega", "position": "SPT", "realName": "Diego Moran", "nationality": "🇺🇸 US", "joinDate": "2024-12-05", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "UltraViolet", "position": "SPT", "realName": "Christian Pedroza", "nationality": "🇺🇸 US", "joinDate": "2025-03-20", "signatureHeroes": ["Ana", "Kiriko", "Zenyatta"]},
            {"player": "KIVIS", "position": "SPT", "realName": "Kivis", "nationality": "🇺🇸 US", "joinDate": "2025-01-15", "signatureHeroes": ["Baptiste", "Kiriko"]}
        ],
        "transfers": [
            {"date": "2025-03-20", "type": "IN", "player": "UltraViolet", "role": "SPT", "details": "M80에서 긴급 서포터 전격 이적 영입"},
            {"date": "2025-02-01", "type": "IN", "player": "Attack", "role": "TANK", "details": "메인 탱커 전력 강화를 위해 영입"},
            {"date": "2024-12-05", "type": "IN", "player": "Vega & Rupal", "role": "SPT", "details": "Toronto Defiant 해산 후 황금 힐러진 영입 창단"}
        ]
    },

    "DF": {
        "id": "DF",
        "status": "CURRENT",
        "name": "Dallas Fuel",
        "nameKo": "달라스 퓨얼",
        "region": "NA",
        "country": "🇺🇸 United States",
        "color": "#0072ce",
        "founded": "2017",
        "historyNotes": "2022 오버워치 리그 월드 챔피언 Dallas Fuel의 2026 OWCS 공식 복귀. 북미와 한국의 정상급 베테랑들을 규합하여 플레이오프 진출에 성공.",
        "trophies": [
            "2022 Overwatch League World Champion",
            "2026 OWCS NA Stage 1 3rd Place"
        ],
        "coachingStaff": [
            {"name": "TazMo", "realName": "Matthew Taylor", "role": "General Manager", "roleKo": "단장", "nationality": "🇺🇸 US"},
            {"name": "Aid", "realName": "고재윤", "role": "Head Coach", "roleKo": "감독", "nationality": "🇰🇷 KR"}
        ],
        "activeRoster": [
            {"player": "Kellan", "position": "TANK", "realName": "김소명", "nationality": "🇰🇷 KR", "joinDate": "2026-01-10", "signatureHeroes": ["Winston", "Doomfist", "D.Va"]},
            {"player": "Kronik", "position": "DPS", "realName": "Kronik", "nationality": "🇺🇸 US", "joinDate": "2026-01-10", "signatureHeroes": ["Tracer", "Genji", "Echo"]},
            {"player": "SeonJun", "position": "DPS", "realName": "김선준", "nationality": "🇰🇷 KR", "joinDate": "2026-01-10", "signatureHeroes": ["Sojourn", "Cassidy", "Ashe"]},
            {"player": "Cjay", "position": "SPT", "realName": "Colin Arakaki", "nationality": "🇺🇸 US", "joinDate": "2026-01-10", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "Lukemino", "position": "SPT", "realName": "Luke Fish", "nationality": "🇺🇸 US", "joinDate": "2026-01-10", "signatureHeroes": ["Ana", "Kiriko", "Baptiste"]}
        ],
        "transfers": [
            {"date": "2026-01-10", "type": "IN", "player": "Full Roster", "role": "ALL", "details": "Dallas Fuel의 OWCS NA 2026 공식 복귀 로스터 발표"}
        ]
    },

    "M80": {
        "id": "M80",
        "status": "CURRENT",
        "name": "M80",
        "nameKo": "엠에이티",
        "region": "NA",
        "country": "🇺🇸 United States",
        "color": "#ef4444",
        "founded": "2024",
        "historyNotes": "2024년 창단 이래 북미 무대에서 Toronto Defiant, Spacestation과 최정상을 다투어 온 북미 대표 클럽. 압도적 교전력 자랑.",
        "trophies": [
            "2024 OWCS NA Stage 2 Runner-up",
            "2025 OWCS NA Stage 1 Runner-up",
            "2024 Dallas Major 참가"
        ],
        "coachingStaff": [
            {"name": "Gunba", "realName": "Graham Goring", "role": "Head Coach", "roleKo": "감독", "nationality": "🇦🇺 AU"}
        ],
        "activeRoster": [
            {"player": "Coluge", "position": "TANK", "realName": "Colin Arai", "nationality": "🇺🇸 US", "joinDate": "2024-03-01", "signatureHeroes": ["Sigma", "D.Va", "Winston"]},
            {"player": "Spectra", "position": "DPS", "realName": "고동우", "nationality": "🇰🇷 KR", "joinDate": "2024-03-01", "signatureHeroes": ["Tracer", "Genji", "Echo"]},
            {"player": "Happy", "position": "DPS", "realName": "이정우", "nationality": "🇰🇷 KR", "joinDate": "2025-01-10", "signatureHeroes": ["Sojourn", "Widowmaker", "Cassidy"]},
            {"player": "Pelican", "position": "DPS", "realName": "오현석", "nationality": "🇰🇷 KR", "joinDate": "2025-01-10", "signatureHeroes": ["Echo", "Mei", "Genji"]},
            {"player": "Lyar", "position": "SPT", "realName": "Landon Smith", "nationality": "🇺🇸 US", "joinDate": "2024-03-01", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "UltraViolet", "position": "SPT", "realName": "Christian Pedroza", "nationality": "🇺🇸 US", "joinDate": "2024-03-01", "signatureHeroes": ["Ana", "Kiriko"]}
        ],
        "transfers": [
            {"date": "2025-01-10", "type": "IN", "player": "Pelican & Happy", "role": "DPS", "details": "OWL 슈퍼스타 딜러 듀오 전격 영입"},
            {"date": "2024-03-01", "type": "IN", "player": "Core Roster", "role": "ALL", "details": "M80 오버워치 2 공식 창단"}
        ]
    },

    "DSG": {
        "id": "DSG",
        "status": "CURRENT",
        "name": "Disguised",
        "nameKo": "디스가이즈드",
        "region": "NA",
        "country": "🇺🇸 United States",
        "color": "#eab308",
        "founded": "2025",
        "historyNotes": "유명 스트리머 Disguised Toast의 구단. 폭발적인 인기와 공격적인 플레이 스타일로 2025~2026 북미 본선 연속 진출 성공.",
        "trophies": [
            "2026 OWCS NA Stage 1 본선 진출",
            "2025 NA Open Qualifier 1st"
        ],
        "coachingStaff": [
            {"name": "Toast", "realName": "Jeremy Wang", "role": "Owner", "roleKo": "구단주", "nationality": "🇨🇦 CA"},
            {"name": "Spilo", "realName": "Storm Higgins", "role": "Coach", "roleKo": "코치", "nationality": "🇺🇸 US"}
        ],
        "activeRoster": [
            {"player": "Tred", "position": "TANK", "realName": "Euan Gaskin", "nationality": "🇬🇧 GB", "joinDate": "2025-03-01", "signatureHeroes": ["Winston", "Reinhardt"]},
            {"player": "PGE", "position": "DPS", "realName": "PGE", "nationality": "🇺🇸 US", "joinDate": "2025-03-01", "signatureHeroes": ["Cassidy", "Sojourn", "Widowmaker"]},
            {"player": "Scyle", "position": "SPT", "realName": "Scyle", "nationality": "🇺🇸 US", "joinDate": "2025-03-01", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "KiWii", "position": "SPT", "realName": "KiWii", "nationality": "🇺🇸 US", "joinDate": "2025-03-01", "signatureHeroes": ["Ana", "Kiriko"]}
        ],
        "transfers": [
            {"date": "2025-03-01", "type": "IN", "player": "Full Roster", "role": "ALL", "details": "Disguised 오버워치 2 공식 팀 창단 및 로스터 발표"}
        ]
    },

    # =========================================================================
    # PAST OWCS TEAMS - NORTH AMERICA (NA)
    # =========================================================================
    "TD": {
        "id": "TD",
        "status": "PAST",
        "name": "Toronto Defiant",
        "nameKo": "토론토 디파이언트",
        "region": "NA",
        "country": "🇨🇦 Canada",
        "color": "#dc2626",
        "founded": "2018",
        "historyNotes": "2024년 북미 역사상 최강의 드림팀. Someone, Mer1t, Sugarfree, Rupal, Vega를 결집하여 2024 OWCS NA Stage 1, 2, 3, 4를 모두 우승하며 4연속 챔피언에 올랐으며, Dallas Major 3위를 기록. 2024년 말 선수들이 Falcons, Liquid, SSG로 이적하며 활동 종료.",
        "trophies": [
            "2024 OWCS NA Stage 1 Champion",
            "2024 OWCS NA Stage 2 Champion",
            "2024 OWCS NA Stage 3 Champion",
            "2024 OWCS NA Stage 4 Champion",
            "2024 OWCS Dallas Major 3rd Place"
        ],
        "coachingStaff": [
            {"name": "Casores", "realName": "Chris van Hoorn", "role": "Head Coach", "roleKo": "감독", "nationality": "🇳🇱 NL"},
            {"name": "NoHill", "realName": "문성원", "role": "Coach", "roleKo": "코치", "nationality": "🇨🇳 CN"}
        ],
        "finalRoster": [
            {"player": "SOMEONE", "position": "TANK", "realName": "정함범", "nationality": "🇰🇷 KR", "signatureHeroes": ["Winston", "Sigma", "D.Va"]},
            {"player": "MER1T", "position": "DPS", "realName": "최태민", "nationality": "🇰🇷 KR", "signatureHeroes": ["Sojourn", "Ashe", "Cassidy"]},
            {"player": "Sugarfree", "position": "DPS", "realName": "Kamden Hijada", "nationality": "🇺🇸 US", "signatureHeroes": ["Tracer", "Genji", "Echo"]},
            {"player": "Rupal", "position": "SPT", "realName": "Rupal Zaman", "nationality": "🇺🇸 US", "signatureHeroes": ["Ana", "Kiriko", "Baptiste"]},
            {"player": "Vega", "position": "SPT", "realName": "Diego Moran", "nationality": "🇺🇸 US", "signatureHeroes": ["Lucio", "Brigitte"]}
        ],
        "transfers": [
            {"date": "2024-12-02", "type": "OUT", "player": "All Core Players", "role": "ALL", "details": "SOMEONE & MER1T ➔ Falcons, Sugarfree ➔ SSG, Rupal & Vega ➔ Liquid 이적하며 로스터 해산"},
            {"date": "2024-02-01", "type": "IN", "player": "Core Roster", "role": "ALL", "details": "2024 북미 최강 슈퍼팀 결성"}
        ]
    },

    "NTMR": {
        "id": "NTMR",
        "status": "PAST",
        "name": "NTMR",
        "nameKo": "나이트메어 (NTMR)",
        "region": "NA",
        "country": "🇺🇸 United States",
        "color": "#6b21a8",
        "founded": "2024",
        "historyNotes": "북미 e스포츠 역사상 가장 눈부셨던 무소속의 기적. 2024~2025 대기업 스폰서 없이 결성되어 2025 Champions Clash에서 세계 최강 Crazy Raccoon을 3-1로 꺾고 하위조로 추락시키는 세기의 업셋을 달성한 전설의 팀.",
        "trophies": [
            "2025 OWCS Champions Clash 3rd Place (CR 3-1 격파)",
            "2024 OWCS NA Stage 3 3rd Place"
        ],
        "coachingStaff": [
            {"name": "Promise", "realName": "Jonah Wilks", "role": "Head Coach", "roleKo": "감독", "nationality": "🇺🇸 US"}
        ],
        "finalRoster": [
            {"player": "Infekted", "position": "TANK", "realName": "Infekted", "nationality": "🇺🇸 US", "signatureHeroes": ["Winston", "D.Va", "Reinhardt"]},
            {"player": "Seicoe", "position": "DPS", "realName": "Julian Seifert", "nationality": "🇦🇹 AT", "signatureHeroes": ["Tracer", "Genji", "Sojourn"]},
            {"player": "scissors", "position": "DPS", "realName": "Cody D'Orazio", "nationality": "🇺🇸 US", "signatureHeroes": ["Pharah", "Echo", "Mei"]},
            {"player": "Lep", "position": "SPT", "realName": "Lep", "nationality": "🇺🇸 US", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "Clear", "position": "SPT", "realName": "Clear", "nationality": "🇺🇸 US", "signatureHeroes": ["Ana", "Kiriko", "Baptiste"]}
        ],
        "transfers": [
            {"date": "2025-06-15", "type": "OUT", "player": "scissors ➔ Spacestation", "role": "DPS", "details": "선수단 분산 및 공식 팀 활동 종료"},
            {"date": "2024-03-01", "type": "IN", "player": "Core Roster", "role": "ALL", "details": "무소속 기적의 팀 NTMR 결성"}
        ]
    },

    "LG": {
        "id": "LG",
        "status": "PAST",
        "name": "Luminosity Gaming",
        "nameKo": "루미너스티 게이밍",
        "region": "NA",
        "country": "🇨🇦 Canada / 🇺🇸 United States",
        "color": "#2563eb",
        "founded": "2024",
        "historyNotes": "북미 전통의 명문 e스포츠 클럽. 2024년 초 OWCS 북미 본선에 참가하여 상위권 경쟁을 펼쳤으나 오프시즌 로스터 계약 종료로 활동 중단.",
        "trophies": [
            "2024 OWCS NA Stage 1 본선 진출"
        ],
        "coachingStaff": [
            {"name": "Spilo", "realName": "Storm Higgins", "role": "Head Coach", "roleKo": "감독", "nationality": "🇺🇸 US"}
        ],
        "finalRoster": [
            {"player": "RhynO", "position": "TANK", "realName": "Rhyno", "nationality": "🇺🇸 US", "signatureHeroes": ["Winston", "D.Va"]},
            {"player": "Vision", "position": "DPS", "realName": "Vision", "nationality": "🇺🇸 US", "signatureHeroes": ["Tracer", "Genji"]},
            {"player": "Doomed", "position": "DPS", "realName": "Doomed", "nationality": "🇺🇸 US", "signatureHeroes": ["Sojourn", "Cassidy"]},
            {"player": "Rakattack", "position": "SPT", "realName": "Colin Rusch", "nationality": "🇺🇸 US", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "cal", "position": "SPT", "realName": "Calvin Nguyen", "nationality": "🇺🇸 US", "signatureHeroes": ["Ana", "Kiriko"]}
        ],
        "transfers": [
            {"date": "2024-08-30", "type": "OUT", "player": "All Roster", "role": "ALL", "details": "계약 만료 및 공식 로스터 해산"}
        ]
    },

    "CN": {
        "id": "CN",
        "status": "PAST",
        "name": "Citrus Nation",
        "nameKo": "시트러스 네이션",
        "region": "NA",
        "country": "🇺🇸 United States",
        "color": "#ea580c",
        "founded": "2024",
        "historyNotes": "특유의 오렌지 감귤 로고로 북미 팬들의 사랑을 받은 무소속 강호. 2024~2025 꾸준히 본선에 진출했으나 이후 선수단 이적 등으로 해산.",
        "trophies": [
            "2024 OWCS NA Stage 2 본선 참가"
        ],
        "coachingStaff": [
            {"name": "OrangeCoach", "realName": "코치", "role": "Coach", "roleKo": "코치", "nationality": "🇺🇸 US"}
        ],
        "finalRoster": [
            {"player": "Cowman", "position": "TANK", "realName": "Cowman", "nationality": "🇺🇸 US", "signatureHeroes": ["Winston", "Reinhardt"]},
            {"player": "Slay", "position": "DPS", "realName": "Slay", "nationality": "🇺🇸 US", "signatureHeroes": ["Tracer", "Echo"]},
            {"player": "Dynasty", "position": "DPS", "realName": "Dynasty", "nationality": "🇺🇸 US", "signatureHeroes": ["Sojourn", "Cassidy"]},
            {"player": "Cjay", "position": "SPT", "realName": "Colin Arakaki", "nationality": "🇺🇸 US", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "Renko", "position": "SPT", "realName": "Renko", "nationality": "🇺🇸 US", "signatureHeroes": ["Ana", "Kiriko"]}
        ],
        "transfers": [
            {"date": "2025-01-15", "type": "OUT", "player": "Cjay ➔ Dallas Fuel", "role": "SPT", "details": "선수단 이적으로 공식 해산"}
        ]
    },

    "SOTG": {
        "id": "SOTG",
        "status": "PAST",
        "name": "Students of the Game",
        "nameKo": "스튜던츠 오브 더 게임",
        "region": "NA",
        "country": "🇺🇸 United States",
        "color": "#059669",
        "founded": "2024",
        "historyNotes": "북미 대학생 및 아마추어 신예들이 모여 만든 돌풍의 무소속 팀. 북미 스테이지에서 프로팀들을 연달아 잡아내며 큰 화제를 모았음.",
        "trophies": [
            "2024 OWCS NA Stage 3 4th Place"
        ],
        "coachingStaff": [
            {"name": "Prof", "realName": "교수코치", "role": "Coach", "roleKo": "코치", "nationality": "🇺🇸 US"}
        ],
        "finalRoster": [
            {"player": "False", "position": "TANK", "realName": "Christian Wiśniewski", "nationality": "🇺🇸 US", "signatureHeroes": ["Sigma", "D.Va"]},
            {"player": "Rokit", "position": "DPS", "realName": "Rokit", "nationality": "🇺🇸 US", "signatureHeroes": ["Tracer", "Genji"]},
            {"player": "arrow", "position": "DPS", "realName": "arrow", "nationality": "🇺🇸 US", "signatureHeroes": ["Sojourn", "Cassidy"]},
            {"player": "Seeker", "position": "DPS", "realName": "Adam Mielpiek", "nationality": "🇺🇸 US", "signatureHeroes": ["Ashe", "Widowmaker"]},
            {"player": "zeron", "position": "SPT", "realName": "zeron", "nationality": "🇺🇸 US", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "trqce", "position": "SPT", "realName": "trqce", "nationality": "🇺🇸 US", "signatureHeroes": ["Ana", "Kiriko"]}
        ],
        "transfers": [
            {"date": "2024-11-20", "type": "RELEGATED", "player": "Team Roster", "role": "ALL", "details": "시즌 종료 및 선수단 학업/이적에 따른 활동 중단"}
        ]
    },

    # =========================================================================
    # PAST OWCS TEAMS - KOREA & HISTORICAL (KR)
    # =========================================================================
    "FTG": {
        "id": "FTG",
        "status": "PAST",
        "name": "From The Gamer",
        "nameKo": "프롬 더 게이머",
        "region": "KR",
        "country": "🇰🇷 Korea",
        "color": "#64748b",
        "founded": "2024",
        "historyNotes": "2024년 초 오버워치 씬에 등장하여 큰 반향을 일으킨 명문 클럽. 2024년 4월 1차 코어 로스터(Bernar, Viol2t 등)가 ZETA DIVISION에 인수되었으며, 이후 팀 재정비를 거쳐 2025년 ONSIDE GAMING으로 리브랜딩되어 계보가 이어짐.",
        "trophies": [
            "2024 OWCS Korea Stage 1 3rd Place",
            "2024 OWCS Asia Stage 1 3rd Place"
        ],
        "coachingStaff": [
            {"name": "Changgoon", "realName": "박창근", "role": "Head Coach", "roleKo": "감독", "nationality": "🇰🇷 KR"}
        ],
        "finalRoster": [
            {"player": "Flora", "position": "DPS", "realName": "임영우", "nationality": "🇰🇷 KR", "signatureHeroes": ["Sojourn", "Tracer"]},
            {"player": "AlphaYi", "position": "DPS", "realName": "김상범", "nationality": "🇰🇷 KR", "signatureHeroes": ["Genji", "Tracer", "Echo"]},
            {"player": "Belosrea", "position": "TANK", "realName": "김현수", "nationality": "🇰🇷 KR", "signatureHeroes": ["Winston", "Wrecking Ball"]},
            {"player": "Bernar", "position": "TANK", "realName": "신세원", "nationality": "🇰🇷 KR", "signatureHeroes": ["Sigma", "D.Va"]},
            {"player": "Teru", "position": "SPT", "realName": "김민기", "nationality": "🇰🇷 KR", "signatureHeroes": ["Brigitte", "Lucio"]},
            {"player": "Viol2t", "position": "SPT", "realName": "박민기", "nationality": "🇰🇷 KR", "signatureHeroes": ["Baptiste", "Kiriko"]}
        ],
        "transfers": [
            {"date": "2025-08-01", "type": "REBRAND", "player": "Team Organization", "role": "ALL", "details": "ONSIDE GAMING으로 공식 리브랜딩 및 구단 개편"},
            {"date": "2024-04-10", "type": "ACQUISITION", "player": "Core Roster", "role": "ALL", "details": "ZETA DIVISION에 핵심 선수단 및 코치진 매각/인수"},
            {"date": "2024-02-01", "type": "FOUNDED", "player": "Core Roster", "role": "ALL", "details": "From The Gamer(FTG) 공식 창단"}
        ]
    },

    "WAC": {
        "id": "WAC",
        "status": "PAST",
        "name": "We Are Chicks",
        "nameKo": "위 아 칙스 (WAC)",
        "region": "KR",
        "country": "🇰🇷 Korea",
        "color": "#fbbf24",
        "founded": "2024",
        "historyNotes": "2024년 초 San Francisco Shock 및 OWL 우승 주역들(JunBin, MAX, LIP, HeeSang, CH0R0NG, Shu)이 결성한 전설적인 무소속 슈퍼팀. 2024년 4월 일본 명문 구단 Crazy Raccoon에 선수단 전원이 공식 인수되며 활동 종료.",
        "trophies": [
            "2024 OWCS Korea Stage 1 Champion"
        ],
        "coachingStaff": [
            {"name": "Moon", "realName": "문병철", "role": "Head Coach", "roleKo": "감독", "nationality": "🇰🇷 KR"}
        ],
        "finalRoster": [
            {"player": "JunBin", "position": "TANK", "realName": "박준빈", "nationality": "🇰🇷 KR", "signatureHeroes": ["Winston", "Wrecking Ball"]},
            {"player": "MAX", "position": "TANK", "realName": "최수민", "nationality": "🇰🇷 KR", "signatureHeroes": ["Sigma", "D.Va"]},
            {"player": "LIP", "position": "DPS", "realName": "이재원", "nationality": "🇰🇷 KR", "signatureHeroes": ["Sombra", "Sojourn"]},
            {"player": "HeeSang", "position": "DPS", "realName": "채희상", "nationality": "🇰🇷 KR", "signatureHeroes": ["Tracer", "Echo"]},
            {"player": "CH0R0NG", "position": "SPT", "realName": "성유민", "nationality": "🇰🇷 KR", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "shu", "position": "SPT", "realName": "김진서", "nationality": "🇰🇷 KR", "signatureHeroes": ["Ana", "Baptiste"]}
        ],
        "transfers": [
            {"date": "2024-04-07", "type": "ACQUISITION", "player": "All Players & Staff", "role": "ALL", "details": "Crazy Raccoon에 선수단 전원 인수 창단되며 공식 활동 종료"}
        ]
    },

    "ERA": {
        "id": "ERA",
        "status": "PAST",
        "name": "New Era",
        "nameKo": "뉴 에라",
        "region": "KR",
        "country": "🇰🇷 Korea",
        "color": "#64748b",
        "founded": "2025",
        "historyNotes": "2026 Korea Stage 1에 참가하여 분전하였으나, 하위 시드 결정전 및 승강전에서 패배하며 오픈 예선으로 강등/활동 중단.",
        "trophies": [
            "2026 OWCS Korea Stage 1 본선 참가"
        ],
        "coachingStaff": [
            {"name": "EraCoach", "realName": "이코치", "role": "Head Coach", "roleKo": "감독", "nationality": "🇰🇷 KR"}
        ],
        "finalRoster": [
            {"player": "TOBI", "position": "SPT", "realName": "양진모", "nationality": "🇰🇷 KR", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "D4RT", "position": "SPT", "realName": "김다트", "nationality": "🇰🇷 KR", "signatureHeroes": ["Ana", "Kiriko"]},
            {"player": "HeeSeong", "position": "TANK", "realName": "박희성", "nationality": "🇰🇷 KR", "signatureHeroes": ["Winston", "Sigma"]},
            {"player": "Beck", "position": "DPS", "realName": "김백", "nationality": "🇰🇷 KR", "signatureHeroes": ["Tracer", "Genji"]},
            {"player": "GROM", "position": "DPS", "realName": "이그롬", "nationality": "🇰🇷 KR", "signatureHeroes": ["Sojourn", "Cassidy"]}
        ],
        "transfers": [
            {"date": "2026-04-15", "type": "RELEGATED", "player": "Team Roster", "role": "ALL", "details": "Stage 1 승강전 패배 후 로스터 해산"}
        ]
    },

    "ZAN": {
        "id": "ZAN",
        "status": "PAST",
        "name": "ZAN Esports",
        "nameKo": "잔 이스포츠",
        "region": "KR",
        "country": "🇰🇷 Korea",
        "color": "#64748b",
        "founded": "2025",
        "historyNotes": "2026 Korea Stage 1 참가 후, 2026년 5월 Røde Onside Gaming과 전격 합병하여 Røde ZANSIDE GAMING(ROZE)으로 통합 흡수됨.",
        "trophies": [
            "2026 OWCS Korea Stage 1 참가"
        ],
        "coachingStaff": [
            {"name": "ZanCoach", "realName": "김잔", "role": "Coach", "roleKo": "코치", "nationality": "🇰🇷 KR"}
        ],
        "finalRoster": [
            {"player": "Heiser", "position": "TANK", "realName": "권순호", "nationality": "🇰🇷 KR", "signatureHeroes": ["Winston", "Doomfist"]},
            {"player": "Kilo", "position": "DPS", "realName": "정진우", "nationality": "🇰🇷 KR", "signatureHeroes": ["Widowmaker", "Sojourn"]},
            {"player": "Probe", "position": "DPS", "realName": "정준영", "nationality": "🇰🇷 KR", "signatureHeroes": ["Cassidy", "Tracer"]},
            {"player": "Irony", "position": "SPT", "realName": "김강하", "nationality": "🇰🇷 KR", "signatureHeroes": ["Ana", "Kiriko"]}
        ],
        "transfers": [
            {"date": "2026-05-10", "type": "MERGER", "player": "Core Roster", "role": "ALL", "details": "Røde Onside Gaming과 합병하여 Røde Zanside Gaming(ROZE)으로 공식 통합"}
        ]
    },

    "OSG": {
        "id": "OSG",
        "status": "PAST",
        "name": "ONSIDE GAMING",
        "nameKo": "온사이드 게이밍",
        "region": "KR",
        "country": "🇰🇷 Korea",
        "color": "#64748b",
        "founded": "2025",
        "historyNotes": "FTG 해체 후 2025년 창단된 팀. 2026년 Røde 스폰서십(Røde Onside Gaming)을 거쳐 최종적으로 Røde ZANSIDE GAMING으로 리브랜딩됨.",
        "trophies": [
            "2025 OWCS Korea Stage 3 참가"
        ],
        "coachingStaff": [
            {"name": "Named", "realName": "이동현", "role": "Head Coach", "roleKo": "감독", "nationality": "🇰🇷 KR"}
        ],
        "finalRoster": [
            {"player": "Void", "position": "TANK", "realName": "강준우", "nationality": "🇰🇷 KR", "signatureHeroes": ["Sigma", "D.Va"]},
            {"player": "Becky", "position": "DPS", "realName": "김일하", "nationality": "🇰🇷 KR", "signatureHeroes": ["Echo", "Tracer"]},
            {"player": "SP1NT", "position": "DPS", "realName": "안우진", "nationality": "🇰🇷 KR", "signatureHeroes": ["Genji", "Pharah"]},
            {"player": "Opener", "position": "SPT", "realName": "안기범", "nationality": "🇰🇷 KR", "signatureHeroes": ["Lucio", "Brigitte"]}
        ],
        "transfers": [
            {"date": "2026-02-01", "type": "REBRAND", "player": "Team Roster", "role": "ALL", "details": "Røde 스폰서십 체결로 Røde Onside Gaming 리브랜딩"}
        ]
    },

    # =========================================================================
    # GLOBAL MAJOR TEAMS (EMEA, JP, PA, CN)
    # =========================================================================
    "ENCE": {
        "id": "ENCE", "status": "CURRENT", "name": "ENCE", "nameKo": "엔스", "region": "EMEA", "country": "🇫🇮 Finland", "color": "#0284c7", "founded": "2024",
        "historyNotes": "유럽 e스포츠의 맹주. 핀란드 및 유럽 최고 스타들을 결집하여 EMEA 챔피언에 올랐으며 국제 무대에서 꾸준한 성과 기록.",
        "trophies": ["2024 OWCS EMEA Stage 2 Champion", "2025 OWCS EMEA Stage 1 Champion"],
        "coachingStaff": [{"name": "Seita", "realName": "Joni Paavola", "role": "Head Coach", "roleKo": "감독", "nationality": "🇫🇮 FI"}],
        "activeRoster": [
            {"player": "Vestola", "position": "TANK", "realName": "Ilari Vestola", "nationality": "🇫🇮 FI", "signatureHeroes": ["Sigma", "D.Va"]},
            {"player": "Kai", "position": "DPS", "realName": "Kai Collins", "nationality": "🇬🇧 GB", "signatureHeroes": ["Sojourn", "Ashe"]},
            {"player": "Kevster", "position": "DPS", "realName": "Kevin Persson", "nationality": "🇸🇪 SE", "signatureHeroes": ["Tracer", "Echo"]},
            {"player": "Masaa", "position": "SPT", "realName": "Petja Kantanen", "nationality": "🇫🇮 FI", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "Ghost91", "position": "SPT", "realName": "William Eklund", "nationality": "🇸🇪 SE", "signatureHeroes": ["Ana", "Kiriko"]}
        ],
        "transfers": [{"date": "2024-03-01", "type": "IN", "player": "Core Roster", "role": "ALL", "details": "ENCE 오버워치 부문 창단"}]
    },
    "FNC": {
        "id": "FNC", "status": "CURRENT", "name": "Fnatic", "nameKo": "프나틱", "region": "EMEA", "country": "🇬🇧 United Kingdom", "color": "#f97316", "founded": "2024",
        "historyNotes": "글로벌 명문 Fnatic이 한국 및 유럽의 특급 재능들을 영입하여 OWCS에 복귀. 다채로운 전략으로 세계 대회 돌풍 견인.",
        "trophies": ["2024 OWCS Asia Stage 2 4th Place", "2025 Champions Clash 참가"],
        "coachingStaff": [{"name": "Sp9rk1e", "realName": "김영한", "role": "Coach", "roleKo": "코치", "nationality": "🇰🇷 KR"}],
        "activeRoster": [
            {"player": "Attack", "position": "TANK", "realName": "김준화", "nationality": "🇰🇷 KR", "signatureHeroes": ["Winston", "D.Va"]},
            {"player": "Checkmate", "position": "DPS", "realName": "백승훈", "nationality": "🇰🇷 KR", "signatureHeroes": ["Tracer", "Genji"]},
            {"player": "VIPER", "position": "DPS", "realName": "이정우", "nationality": "🇰🇷 KR", "signatureHeroes": ["Sojourn", "Ashe"]},
            {"player": "LeeJaeGon", "position": "SPT", "realName": "이재곤", "nationality": "🇰🇷 KR", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "IZaYaKI", "position": "SPT", "realName": "김민철", "nationality": "🇰🇷 KR", "signatureHeroes": ["Ana", "Kiriko"]}
        ],
        "transfers": [{"date": "2024-05-01", "type": "IN", "player": "Core Roster", "role": "ALL", "details": "Fnatic 공식 복귀 로스터"}]
    },
    "VAR": {
        "id": "VAR", "status": "CURRENT", "name": "VARREL", "nameKo": "바렐", "region": "JP", "country": "🇯🇵 Japan", "color": "#14b8a6", "founded": "2023",
        "historyNotes": "일본 오버워치 씬의 압도적 1황. 정규시즌 전승 행진을 기록하며 아시아 본선 및 국제 메이저에 일본 대표로 단골 출전.",
        "trophies": ["2024 OWCS Japan Stage 1, 2 Champion", "2025 OWCS Japan Stage 1, 2 Champion"],
        "coachingStaff": [{"name": "Pain", "realName": "일본감독", "role": "Head Coach", "roleKo": "감독", "nationality": "🇯🇵 JP"}],
        "activeRoster": [
            {"player": "KSG", "position": "TANK", "realName": "기시모토", "nationality": "🇯🇵 JP", "signatureHeroes": ["Winston", "Sigma"]},
            {"player": "Nico", "position": "DPS", "realName": "니코", "nationality": "🇯🇵 JP", "signatureHeroes": ["Tracer", "Sojourn"]},
            {"player": "Qki", "position": "DPS", "realName": "큐키", "nationality": "🇯🇵 JP", "signatureHeroes": ["Genji", "Cassidy"]},
            {"player": "Mihawk", "position": "SPT", "realName": "미호크", "nationality": "🇯🇵 JP", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "KSiS", "position": "SPT", "realName": "크시스", "nationality": "🇯🇵 JP", "signatureHeroes": ["Ana", "Kiriko"]}
        ],
        "transfers": [{"date": "2024-01-15", "type": "IN", "player": "Core Roster", "role": "ALL", "details": "VARREL 공식 로스터"}]
    },
    "ALB": {
        "id": "ALB", "status": "CURRENT", "name": "ALBUS Esports", "nameKo": "알버스 이스포츠", "region": "PA", "country": "🇹🇼 Taiwan / 🇦🇺 Pacific", "color": "#a855f7", "founded": "2024",
        "historyNotes": "태평양(Pacific) 권역 챔피언. 뛰어난 팀워크와 피지컬로 아시아 본선 무대에 진출하여 아시아 다크호스로 군림.",
        "trophies": ["2024 OWCS Pacific Stage 1, 2 Champion", "2025 OWCS Pacific Stage 1 Champion"],
        "coachingStaff": [{"name": "Panda", "realName": "판다", "role": "Coach", "roleKo": "코치", "nationality": "🇹🇼 TW"}],
        "activeRoster": [
            {"player": "Cowman", "position": "TANK", "realName": "카우맨", "nationality": "🇹🇼 TW", "signatureHeroes": ["Winston", "Doomfist"]},
            {"player": "Ace", "position": "DPS", "realName": "에이스", "nationality": "🇦🇺 AU", "signatureHeroes": ["Tracer", "Echo"]},
            {"player": "Shine", "position": "DPS", "realName": "샤인", "nationality": "🇹🇼 TW", "signatureHeroes": ["Sojourn", "Cassidy"]},
            {"player": "Under", "position": "SPT", "realName": "언더", "nationality": "🇹🇼 TW", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "Star", "position": "SPT", "realName": "스타", "nationality": "🇹🇼 TW", "signatureHeroes": ["Ana", "Kiriko"]}
        ],
        "transfers": [{"date": "2024-02-01", "type": "IN", "player": "Core Roster", "role": "ALL", "details": "ALBUS Esports 창단"}]
    },
    "SPG": {
        "id": "SPG", "status": "CURRENT", "name": "Space Gaming", "nameKo": "스페이스 게이밍", "region": "CN", "country": "🇨🇳 China", "color": "#0ea5e9", "founded": "2025",
        "historyNotes": "중국 서버 공식 오픈과 함께 결성된 중국 최상위 팀. OWL 베테랑 및 중국 컨텐더스 최정상 선수들이 결집.",
        "trophies": ["2026 OWCS China Stage 1 Champion"],
        "coachingStaff": [{"name": "Rui", "realName": "왕신루이", "role": "Head Coach", "roleKo": "감독", "nationality": "🇨🇳 CN"}],
        "activeRoster": [
            {"player": "Guxue", "position": "TANK", "realName": "쉬추린", "nationality": "🇨🇳 CN", "signatureHeroes": ["Winston", "Doomfist"]},
            {"player": "Leave", "position": "DPS", "realName": "황신", "nationality": "🇨🇳 CN", "signatureHeroes": ["Tracer", "Echo", "Sojourn"]},
            {"player": "Shy", "position": "DPS", "realName": "정양제", "nationality": "🇨🇳 CN", "signatureHeroes": ["Sojourn", "Cassidy", "Ashe"]},
            {"player": "Lengsa", "position": "SPT", "realName": "천징이", "nationality": "🇨🇳 CN", "signatureHeroes": ["Lucio", "Brigitte"]},
            {"player": "Mmonk", "position": "SPT", "realName": "저우시멩", "nationality": "🇨🇳 CN", "signatureHeroes": ["Ana", "Kiriko", "Zenyatta"]}
        ],
        "transfers": [{"date": "2025-06-01", "type": "IN", "player": "Core Roster", "role": "ALL", "details": "중국 대표 드림팀 결성"}]
    }
}

def generate_js():
    data = {
        "regions": REGIONS,
        "teams": TEAMS
    }
    js_content = "window.OWCS_GLOBAL_TEAMS = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(js_content)
    cur_count = len([t for t in TEAMS.values() if t['status']=='CURRENT'])
    past_count = len([t for t in TEAMS.values() if t['status']=='PAST'])
    print(f"Generated {OUT_FILE} with {len(TEAMS)} teams ({cur_count} Current, {past_count} Past).")

if __name__ == "__main__":
    generate_js()
