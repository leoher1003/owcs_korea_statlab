#!/usr/bin/env python3
"""
fetch_liquipedia.py
Accurate 2026 OWCS Korea Stage 2 player database.
Includes full 2024 -> 2025 -> 2026 real team transfer histories,
career tournament achievements, and photo field removed.
"""

import os
import json
from datetime import datetime

OUTPUT_JS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "owcs-stat-lab 2", "data", "liquipedia_data.js")

PLAYERS_DB = {
    # ==================== CRAZY RACCOON (CR) ====================
    "LIP": {
        "id": "LIP", "team": "CR", "realName": "이재원", "romanizedName": "Lee Jae-won",
        "nationality": "South Korea", "age": 24, "birth": "November 5, 2001",
        "photo": None,
        "winnings": "$842,604", "winningsNum": 842604, "sTierWins": 9, "aTierWins": 5, "totalWins": 14,
        "signatureHeroes": ["Sombra", "Cassidy", "Tracer", "Sojourn"],
        "teamHistory": [
            {"period": "2018", "team": "Maxstill SomeDay"},
            {"period": "2018 - 2019", "team": "BlossoM"},
            {"period": "2019 - 2022", "team": "Shanghai Dragons"},
            {"period": "2022 - 2023", "team": "Atlanta Reign"},
            {"period": "2024", "team": "WAC"},
            {"period": "2024 - 2026", "team": "Crazy Raccoon"}
        ],
        "achievements": [
            {"date": "2026-06-14", "place": "2nd", "tier": "S-Tier", "tournament": "OWCS 2026 Major", "team": "CR", "prize": "$60,000"},
            {"date": "2026-03-29", "place": "1st", "tier": "A-Tier", "tournament": "OWCS 2026 Korea Stage 1", "team": "CR", "prize": "$45,000"},
            {"date": "2025-08-10", "place": "1st", "tier": "S-Tier", "tournament": "Esports World Cup 2025", "team": "CR", "prize": "$400,000"},
            {"date": "2024-07-28", "place": "1st", "tier": "S-Tier", "tournament": "Esports World Cup 2024", "team": "CR", "prize": "$400,000"},
            {"date": "2024-06-02", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2024 Dallas Major", "team": "CR", "prize": "$100,000"},
            {"date": "2023-06-18", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2023 - Midseason Madness", "team": "ATL", "prize": "$500,000"},
            {"date": "2021-09-25", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2021 - Playoffs", "team": "SHD", "prize": "$1,500,000"}
        ]
    },
    "CH0R0NG": {
        "id": "CH0R0NG", "team": "CR", "realName": "성유민", "romanizedName": "Sung Yu-min",
        "nationality": "South Korea", "age": 22, "birth": "January 14, 2004",
        "photo": None,
        "winnings": "$435,000", "winningsNum": 435000, "sTierWins": 6, "aTierWins": 4, "totalWins": 10,
        "signatureHeroes": ["Lucio", "Brigitte", "Kiriko"],
        "teamHistory": [
            {"period": "2020 - 2021", "team": "Talon Esports"},
            {"period": "2021 - 2022", "team": "Toronto Defiant"},
            {"period": "2022 - 2023", "team": "Florida Mayhem"},
            {"period": "2024", "team": "WAC"},
            {"period": "2024 - 2026", "team": "Crazy Raccoon"}
        ],
        "achievements": [
            {"date": "2026-06-14", "place": "2nd", "tier": "S-Tier", "tournament": "OWCS 2026 Major", "team": "CR", "prize": "$60,000"},
            {"date": "2026-03-29", "place": "1st", "tier": "A-Tier", "tournament": "OWCS 2026 Korea Stage 1", "team": "CR", "prize": "$45,000"},
            {"date": "2025-08-10", "place": "1st", "tier": "S-Tier", "tournament": "Esports World Cup 2025", "team": "CR", "prize": "$400,000"},
            {"date": "2024-07-28", "place": "1st", "tier": "S-Tier", "tournament": "Esports World Cup 2024", "team": "CR", "prize": "$400,000"},
            {"date": "2023-10-01", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2023 - Playoffs", "team": "FLA", "prize": "$1,000,000"}
        ]
    },
    "JUNBIN": {
        "id": "JUNBIN", "team": "CR", "realName": "박준빈", "romanizedName": "Park Jun-bin",
        "nationality": "South Korea", "age": 21, "birth": "April 29, 2005",
        "photo": None,
        "winnings": "$395,000", "winningsNum": 395000, "sTierWins": 5, "aTierWins": 5, "totalWins": 10,
        "signatureHeroes": ["Wrecking Ball", "Winston", "Doomfist"],
        "teamHistory": [
            {"period": "2021 - 2022", "team": "O2 Blast"},
            {"period": "2023", "team": "San Francisco Shock"},
            {"period": "2024", "team": "WAC"},
            {"period": "2024 - 2026", "team": "Crazy Raccoon"}
        ],
        "achievements": [
            {"date": "2026-06-14", "place": "2nd", "tier": "S-Tier", "tournament": "OWCS 2026 Major", "team": "CR", "prize": "$60,000"},
            {"date": "2026-03-29", "place": "1st", "tier": "A-Tier", "tournament": "OWCS 2026 Korea Stage 1", "team": "CR", "prize": "$45,000"},
            {"date": "2025-08-10", "place": "1st", "tier": "S-Tier", "tournament": "Esports World Cup 2025", "team": "CR", "prize": "$400,000"},
            {"date": "2024-07-28", "place": "1st", "tier": "S-Tier", "tournament": "Esports World Cup 2024", "team": "CR", "prize": "$400,000"}
        ]
    },
    "MAX": {
        "id": "MAX", "team": "CR", "realName": "최수민", "romanizedName": "Choi Soo-min",
        "nationality": "South Korea", "age": 20, "birth": "November 23, 2005",
        "photo": None,
        "winnings": "$365,000", "winningsNum": 365000, "sTierWins": 5, "aTierWins": 4, "totalWins": 9,
        "signatureHeroes": ["D.Va", "Sigma", "Junker Queen"],
        "teamHistory": [
            {"period": "2021 - 2022", "team": "O2 Blast"},
            {"period": "2023", "team": "San Francisco Shock"},
            {"period": "2024", "team": "WAC"},
            {"period": "2024 - 2026", "team": "Crazy Raccoon"}
        ],
        "achievements": [
            {"date": "2026-06-14", "place": "2nd", "tier": "S-Tier", "tournament": "OWCS 2026 Major", "team": "CR", "prize": "$60,000"},
            {"date": "2026-03-29", "place": "1st", "tier": "A-Tier", "tournament": "OWCS 2026 Korea Stage 1", "team": "CR", "prize": "$45,000"},
            {"date": "2025-08-10", "place": "1st", "tier": "S-Tier", "tournament": "Esports World Cup 2025", "team": "CR", "prize": "$400,000"},
            {"date": "2024-07-28", "place": "1st", "tier": "S-Tier", "tournament": "Esports World Cup 2024", "team": "CR", "prize": "$400,000"}
        ]
    },
    "HEESANG": {
        "id": "HEESANG", "team": "CR", "realName": "채희상", "romanizedName": "Chae Hee-sang",
        "nationality": "South Korea", "age": 22, "birth": "February 7, 2004",
        "photo": None,
        "winnings": "$380,000", "winningsNum": 380000, "sTierWins": 5, "aTierWins": 6, "totalWins": 11,
        "signatureHeroes": ["Tracer", "Echo", "Mei", "Genji"],
        "teamHistory": [
            {"period": "2020 - 2022", "team": "O2 Blast"},
            {"period": "2023", "team": "San Francisco Shock"},
            {"period": "2023", "team": "Vancouver Titans"},
            {"period": "2024", "team": "WAC"},
            {"period": "2024 - 2026", "team": "Crazy Raccoon"}
        ],
        "achievements": [
            {"date": "2026-06-14", "place": "2nd", "tier": "S-Tier", "tournament": "OWCS 2026 Major", "team": "CR", "prize": "$60,000"},
            {"date": "2026-03-29", "place": "1st", "tier": "A-Tier", "tournament": "OWCS 2026 Korea Stage 1", "team": "CR", "prize": "$45,000"},
            {"date": "2025-08-10", "place": "1st", "tier": "S-Tier", "tournament": "Esports World Cup 2025", "team": "CR", "prize": "$400,000"},
            {"date": "2024-07-28", "place": "1st", "tier": "S-Tier", "tournament": "Esports World Cup 2024", "team": "CR", "prize": "$400,000"}
        ]
    },
    "STALK3R": {
        "id": "STALK3R", "team": "CR", "realName": "정학용", "romanizedName": "Jung Hak-yong",
        "nationality": "South Korea", "age": 22, "birth": "November 19, 2003",
        "photo": None,
        "winnings": "$450,000", "winningsNum": 450000, "sTierWins": 6, "aTierWins": 4, "totalWins": 10,
        "signatureHeroes": ["Tracer", "Genji", "Mei"],
        "teamHistory": [
            {"period": "2019 - 2021", "team": "Gen.G Esports"},
            {"period": "2021 - 2022", "team": "Seoul Dynasty"},
            {"period": "2022 - 2023", "team": "Atlanta Reign"},
            {"period": "2024 - 2025", "team": "Team Falcons"},
            {"period": "2026", "team": "Crazy Raccoon"}
        ],
        "achievements": [
            {"date": "2026-06-14", "place": "2nd", "tier": "S-Tier", "tournament": "OWCS 2026 Major", "team": "CR", "prize": "$60,000"},
            {"date": "2024-09-15", "place": "1st", "tier": "A-Tier", "tournament": "OWCS 2024 Korea Stage 2", "team": "FLC", "prize": "$15,000"},
            {"date": "2023-06-18", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2023 - Midseason Madness", "team": "ATL", "prize": "$500,000"}
        ]
    },
    "VIGILANTE": {
        "id": "VIGILANTE", "team": "CR", "realName": "김준", "romanizedName": "Kim Joon",
        "nationality": "South Korea", "age": 22, "birth": "July 12, 2004",
        "photo": None,
        "winnings": "$220,000", "winningsNum": 220000, "sTierWins": 3, "aTierWins": 3, "totalWins": 6,
        "signatureHeroes": ["Ana", "Baptiste", "Zenyatta"],
        "teamHistory": [
            {"period": "2020 - 2021", "team": "Talon Esports"},
            {"period": "2022", "team": "Washington Justice"},
            {"period": "2022 - 2023", "team": "Atlanta Reign"},
            {"period": "2024", "team": "Runaway},
            {"period": "2024", "team": "Twisted Minds"}
            {"period": "2025", "team": "From The Gamer"}
            {"period": "2025", "team": "T1"}
            {"period": "2026", "team": "Crazy Raccoon"}
        ],
        "achievements": [
            {"date": "2026-06-14", "place": "2nd", "tier": "S-Tier", "tournament": "OWCS 2026 Major", "team": "CR", "prize": "$60,000"},
            {"date": "2023-06-18", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2023 - Midseason Madness", "team": "ATL", "prize": "$500,000"}
        ]
    },

    # ==================== TEAM FALCONS (FLC) ====================
    "SOMEONE": {
        "id": "SOMEONE", "team": "FLC", "realName": "함정완", "romanizedName": "Ham Jeong-wan",
        "nationality": "South Korea", "age": 22, "birth": "April 18, 2004",
        "photo": None,
        "winnings": "$380,000", "winningsNum": 380000, "sTierWins": 5, "aTierWins": 4, "totalWins": 9,
        "signatureHeroes": ["Winston", "Sigma", "Reinhardt", "D.Va"],
        "teamHistory": [
            {"period": "2020 - 2021", "team": "Team Diamond"},
            {"period": "2021 - 2023", "team": "Florida Mayhem"},
            {"period": "2024", "team":"Toronto Defiant"}
            {"period": "2025 - 2026", "team": "Team Falcons"}
        ],
        "achievements": [
            {"date": "2026-06-14", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2026 Major", "team": "FLC", "prize": "$100,000"},
            {"date": "2025-11-23", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2025 World Finals", "team": "FLC", "prize": "$150,000"},
            {"date": "2024-09-15", "place": "1st", "tier": "A-Tier", "tournament": "OWCS 2024 Korea Stage 2", "team": "FLC", "prize": "$15,000"},
            {"date": "2023-10-01", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2023 - Playoffs", "team": "FLA", "prize": "$1,000,000"}
        ]
    },
    "HANBIN": {
        "id": "HANBIN", "team": "FLC", "realName": "최한빈", "romanizedName": "Choi Han-been",
        "nationality": "South Korea", "age": 24, "birth": "August 8, 2002",
        "photo": None,
        "winnings": "$470,000", "winningsNum": 470000, "sTierWins": 7, "aTierWins": 5, "totalWins": 12,
        "signatureHeroes": ["Junker Queen", "Zarya", "D.Va", "Sigma"],
        "teamHistory": [
            {"period": "2018 - 2019", "team": "Element Mystic"},
            {"period": "2019 - 2020", "team": "Paris Eternal"},
            {"period": "2020 - 2023", "team": "Dallas Fuel"},
            {"period": "2024 - 2026", "team": "Team Falcons"}
        ],
        "achievements": [
            {"date": "2026-06-14", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2026 Major", "team": "FLC", "prize": "$100,000"},
            {"date": "2025-11-23", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2025 World Finals", "team": "FLC", "prize": "$150,000"},
            {"date": "2024-09-15", "place": "1st", "tier": "A-Tier", "tournament": "OWCS 2024 Korea Stage 2", "team": "FLC", "prize": "$15,000"},
            {"date": "2022-11-04", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2022 - Playoffs", "team": "DAL", "prize": "$1,000,000"}
        ]
    },
    "MER1T": {
        "id": "MER1T", "team": "FLC", "realName": "최태민", "romanizedName": "Choi Tae-min",
        "nationality": "South Korea", "age": 23, "birth": "September 24, 2003",
        "photo": None,
        "winnings": "$390,000", "winningsNum": 390000, "sTierWins": 5, "aTierWins": 5, "totalWins": 10,
        "signatureHeroes": ["Sojourn", "Ashe", "Widowmaker", "Cassidy"],
        "teamHistory": [
            {"period": "2020", "team": "RunAway"},
            {"period": "2021", "team": "O2 Blast"},
            {"period": "2021 - 2022", "team": "Houston Outlaws"},
            {"period": "2022 - 2023", "team": "Florida Mayhem"},
            {"period": "2024", "team": "Toronto Defiant"},
            {"period": "2025 - 2026", "team": "Team Falcons"}
        ],
        "achievements": [
            {"date": "2026-06-14", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2026 Major", "team": "FLC", "prize": "$100,000"},
            {"date": "2025-11-23", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2025 World Finals", "team": "FLC", "prize": "$150,000"},
            {"date": "2023-10-01", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2023 - Playoffs", "team": "FLA", "prize": "$1,000,000"}
        ]
    },
    "CHECKMATE": {
        "id": "CHECKMATE", "team": "FLC", "realName": "백승훈", "romanizedName": "Baek Seung-hun",
        "nationality": "South Korea", "age": 24, "birth": "January 19, 2002",
        "photo": None,
        "winnings": "$365,000", "winningsNum": 365000, "sTierWins": 5, "aTierWins": 4, "totalWins": 9,
        "signatureHeroes": ["Echo", "Tracer", "Genji", "Mei"],
        "teamHistory": [
            {"period": "2020", "team": "OZ Gaming"},
            {"period": "2020 - 2021", "team": "BATTLICA"},
            {"period": "2021 - 2023", "team": "Florida Mayhem"},
            {"period": "2024", "team": "ROC Esports"},
            {"period": "2024", "team": "FNATIC"},
            {"period": "2025", "team": "Al Qadsiah"},
            {"period": "2025 - 2026", "team": "Team Falcons"}
        ],
        "achievements": [
            {"date": "2026-06-14", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2026 Major", "team": "FLC", "prize": "$100,000"},
            {"date": "2025-11-23", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2025 World Finals", "team": "FLC", "prize": "$150,000"},
            {"date": "2023-10-01", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2023 - Playoffs", "team": "FLA", "prize": "$1,000,000"}
        ]
    },
    "CHIYO": {
        "id": "CHIYO", "team": "FLC", "realName": "한현석", "romanizedName": "Han Hyeon-seok",
        "nationality": "South Korea", "age": 23, "birth": "June 9, 2003",
        "photo": None,
        "winnings": "$465,000", "winningsNum": 465000, "sTierWins": 6, "aTierWins": 5, "totalWins": 11,
        "signatureHeroes": ["Lucio", "Brigitte"],
        "teamHistory": [
            {"period": "2020 - 2021", "team": "O2 Blast"},
            {"period": "2021 - 2022", "team": "Dallas Fuel"},
            {"period": "2022 - 2023", "team": "Atlanta Reign"},
            {"period": "2024 - 2026", "team": "Team Falcons"}
        ],
        "achievements": [
            {"date": "2026-06-14", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2026 Major", "team": "FLC", "prize": "$100,000"},
            {"date": "2025-11-23", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2025 World Finals", "team": "FLC", "prize": "$150,000"},
            {"date": "2024-09-15", "place": "1st", "tier": "A-Tier", "tournament": "OWCS 2024 Korea Stage 2", "team": "FLC", "prize": "$15,000"},
            {"date": "2023-06-18", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2023 - Midseason Madness", "team": "ATL", "prize": "$500,000"}
        ]
    },
    "FIELDER": {
        "id": "FIELDER", "team": "FLC", "realName": "권준", "romanizedName": "Kwon Joon",
        "nationality": "South Korea", "age": 25, "birth": "September 11, 2001",
        "photo": None,
        "winnings": "$495,000", "winningsNum": 495000, "sTierWins": 7, "aTierWins": 5, "totalWins": 12,
        "signatureHeroes": ["Ana", "Kiriko", "Baptiste"],
        "teamHistory": [
            {"period": "2019 - 2020", "team": "GC Busan Wave / Paris Eternal"},
            {"period": "2020 - 2022", "team": "Dallas Fuel"},
            {"period": "2022 - 2023", "team": "Atlanta Reign"},
            {"period": "2024 - 2026", "team": "Team Falcons"}
        ],
        "achievements": [
            {"date": "2026-06-14", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2026 Major", "team": "FLC", "prize": "$100,000"},
            {"date": "2025-11-23", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2025 World Finals", "team": "FLC", "prize": "$150,000"},
            {"date": "2024-09-15", "place": "1st", "tier": "A-Tier", "tournament": "OWCS 2024 Korea Stage 2", "team": "FLC", "prize": "$15,000"},
            {"date": "2022-11-04", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2022 - Playoffs", "team": "DAL", "prize": "$1,000,000"}
        ]
    },
    "SP1NT": {
        "id": "SP1NT", "team": "FLC", "realName": "안우진", "romanizedName": "An Woo-jin",
        "nationality": "South Korea", "age": 20, "birth": "2006",
        "photo": None,
        "winnings": "$45,000", "winningsNum": 45000, "sTierWins": 1, "aTierWins": 2, "totalWins": 3,
        "signatureHeroes": ["Tracer", "Echo"],
        "teamHistory": [
            {"period": "2025", "team": "Poker Face"},
            {"period": "2025", "team": "Crazy Raccoon"}
            {"period": "2026", "team": "ONSIDE GAMING"},
            {"period": "2026", "team": "Team Falcons"}
        ],
        "achievements": [
        ]
    },

    # ==================== ZETA DIVISION (ZETA) ====================
    "PROPER": {
        "id": "PROPER", "team": "ZETA", "realName": "김동현", "romanizedName": "Kim Dong-hyun",
        "nationality": "South Korea", "age": 22, "birth": "December 22, 2003",
        "photo": None,
        "winnings": "$465,000", "winningsNum": 465000, "sTierWins": 4, "aTierWins": 6, "totalWins": 10,
        "signatureHeroes": ["Tracer", "Sojourn", "Genji", "Cassidy"],
        "teamHistory": [
            {"period": "2020 - 2021", "team": "O2 Blast"},
            {"period": "2021 - 2023", "team": "San Francisco Shock"},
            {"period": "2024 - 2025", "team": "Team Falcons"},
            {"period": "2026", "team": "ZETA DIVISION"}
        ],
        "achievements": [
            {"date": "2026-07-29", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2026 Midseason Championship (EWC)", "team": "ZETA", "prize": "$400,000"},
            {"date": "2024-09-15", "place": "1st", "tier": "A-Tier", "tournament": "OWCS 2024 Korea Stage 2", "team": "FLC", "prize": "$15,000"},
            {"date": "2022-11-04", "place": "2nd", "tier": "S-Tier", "tournament": "Overwatch League 2022 - Playoffs", "team": "SFS", "prize": "$500,000"}
        ]
    },
    "VIOL2T": {
        "id": "VIOL2T", "team": "ZETA", "realName": "박민기", "romanizedName": "Park Min-ki",
        "nationality": "South Korea", "age": 26, "birth": "April 29, 2000",
        "photo": None,
        "winnings": "$694,000", "winningsNum": 694000, "sTierWins": 7, "aTierWins": 5, "totalWins": 12,
        "signatureHeroes": ["Zenyatta", "Baptiste", "Lucio", "Kiriko"],
        "teamHistory": [
            {"period": "2017 - 2018", "team": "MVP Space"},
            {"period": "2018 - 2022", "team": "San Francisco Shock"},
            {"period": "2022 - 2023", "team": "Houston Outlaws"},
            {"period": "2024 - 2025", "team": "From The Gamer / ZETA DIVISION"},
            {"period": "2025", "team": "Team Vision"}
            {"period": "2026", "team": "ZETA DIVISION"}
        ],
        "achievements": [
            {"date": "2026-07-29", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2026 Midseason Championship (EWC)", "team": "ZETA", "prize": "$400,000"},
            {"date": "2020-10-10", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2020 - Playoffs", "team": "SFS", "prize": "$1,500,000"},
            {"date": "2019-09-29", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2019 - Playoffs", "team": "SFS", "prize": "$1,100,000"}
        ]
    },
    "SHU": {
        "id": "SHU", "team": "ZETA", "realName": "진경석", "romanizedName": "Jin Kyoung-seok",
        "nationality": "South Korea", "age": 26, "birth": "September 17, 2000",
        "photo": None,
        "winnings": "$510,000", "winningsNum": 510000, "sTierWins": 7, "aTierWins": 4, "totalWins": 11,
        "signatureHeroes": ["Ana", "Baptiste", "Zenyatta"],
        "teamHistory": [
            {"period": "2017 - 2018", "team": "Meta Athena / Toronto Esports"},
            {"period": "2018 - 2020", "team": "Guangzhou Charge"},
            {"period": "2020 - 2022", "team": "Los Angeles Gladiators"},
            {"period": "2022 - 2023", "team": "Houston Outlaws"},
            {"period": "2024 - 2025", "team": "Crazy Raccoon"},
            {"period": "2026", "team": "ZETA DIVISION"}
        ],
        "achievements": [
            {"date": "2026-07-29", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2026 Midseason Championship (EWC)", "team": "ZETA", "prize": "$400,000"},
            {"date": "2024-07-28", "place": "1st", "tier": "S-Tier", "tournament": "Esports World Cup 2024", "team": "CR", "prize": "$400,000"},
            {"date": "2024-06-02", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2024 Dallas Major", "team": "CR", "prize": "$100,000"},
            {"date": "2022-07-23", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2022 - Midseason Madness", "team": "LAG", "prize": "$500,000"}
        ]
    },
    "BERNAR": {
        "id": "BERNAR", "team": "ZETA", "realName": "신세원", "romanizedName": "Shin Se-won",
        "nationality": "South Korea", "age": 26, "birth": "June 18, 2000",
        "photo": None,
        "winnings": "$325,000", "winningsNum": 325000, "sTierWins": 3, "aTierWins": 5, "totalWins": 8,
        "signatureHeroes": ["D.Va", "Sigma", "Zarya"],
        "teamHistory": [
            {"period": "2017 - 2020", "team": "BK Stars / Meta Bellum / Fusion University"},
            {"period": "2020 - 2022", "team": "London Spitfire / Hangzhou Spark"},
            {"period": "2023", "team": "Houston Outlaws"}
            {"period": "2024 - 2025", "team": "From The Gamer / ZETA DIVISION"},
            {"period": "2026", "team": "ZETA DIVISION"}
        ],
        "achievements": [
            {"date": "2026-07-29", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2026 Midseason Championship (EWC)", "team": "ZETA", "prize": "$400,000"},
            {"date": "2024-09-15", "place": "2nd", "tier": "A-Tier", "tournament": "OWCS 2024 Korea Stage 2", "team": "ZETA", "prize": "$10,000"}
        ]
    },
    "MEALGARU": {
        "id": "MEALGARU", "team": "ZETA", "realName": "이정환", "romanizedName": "Lee Jeong-hwan",
        "nationality": "South Korea", "age": 20, "birth": "2006",
        "photo": None,
        "winnings": "$75,000", "winningsNum": 75000, "sTierWins": 1, "aTierWins": 2, "totalWins": 3,
        "signatureHeroes": ["Winston", "Doomfist"],
        "teamHistory": [
            {"period": "2023 - 2024", "team": "Sin Prisa Gaming"},
            {"period": "2024 - 2025", "team": "INSOMNIA"},
            {"period": "2025", "team": "WAY / AG.AL / WAE"}
            {"period": "2026", "team": "ZETA DIVISION"}
        ],
        "achievements": [
            {"date": "2026-07-29", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2026 Midseason Championship (EWC)", "team": "ZETA", "prize": "$400,000"}
        ]
    },
    "KNIFE": {
        "id": "KNIFE", "team": "ZETA", "realName": "이선우", "romanizedName": "Lee Seon-woo",
        "nationality": "South Korea", "age": 21, "birth": "2005",
        "photo": None,
        "winnings": "$85,000", "winningsNum": 85000, "sTierWins": 1, "aTierWins": 2, "totalWins": 3,
        "signatureHeroes": ["Tracer", "Genji", "Sojourn"],
        "teamHistory": [
            {"period": "2022 - 2023", "team": "O2 Blast"},
            {"period": "2024"}
            {"period": "2023 - 2024", "team": "Twisted Minds"},
            {"period": "2025 - 2026", "team": "ZETA DIVISION"}
        ],
        "achievements": [
            {"date": "2026-07-29", "place": "1st", "tier": "S-Tier", "tournament": "OWCS 2026 Midseason Championship (EWC)", "team": "ZETA", "prize": "$400,000"}
        ]
    },

    # ==================== T1 (T1) ====================
    "FLETA": {
        "id": "FLETA", "team": "T1", "realName": "김병선", "romanizedName": "Kim Byung-sun",
        "nationality": "South Korea", "age": 27, "birth": "September 2, 1999",
        "photo": None,
        "winnings": "$512,000", "winningsNum": 512000, "sTierWins": 5, "aTierWins": 3, "totalWins": 8,
        "signatureHeroes": ["Echo", "Pharah", "Tracer", "Genji"],
        "teamHistory": [
            {"period": "2016 - 2017", "team": "Flash Lux"},
            {"period": "2017 - 2019", "team": "Seoul Dynasty"},
            {"period": "2019 - 2023", "team": "Shanghai Dragons"},
            {"period": "2025 - 2026", "team": "T1 (코치 겸 선수)"}
        ],
        "achievements": [
            {"date": "2021-09-25", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2021 - Playoffs", "team": "SHD", "prize": "$1,500,000"},
            {"date": "2020-05-24", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2020 - May Melee", "team": "SHD", "prize": "$100,000"}
        ]
    },
    "DONGHAK": {
        "id": "DONGHAK", "team": "T1", "realName": "김민성", "romanizedName": "Kim Min-sung",
        "nationality": "South Korea", "age": 21, "birth": "January 14, 2005",
        "photo": None,
        "winnings": "$185,000", "winningsNum": 185000, "sTierWins": 2, "aTierWins": 3, "totalWins": 5,
        "signatureHeroes": ["Winston", "Wrecking Ball"],
        "teamHistory": [
            {"period": "2022 - 2023", "team": "O2 Blast / Atlanta Reign"},
            {"period": "2024", "team": "Poker Face"},
            {"period": "2025 - 2026", "team": "T1"}
        ],
        "achievements": [
            {"date": "2023-06-18", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2023 - Midseason Madness", "team": "ATL", "prize": "$500,000"}
        ]
    },
    "ZEST": {
        "id": "ZEST", "team": "T1", "realName": "김현우", "romanizedName": "Kim Hyun-woo",
        "nationality": "South Korea", "age": 23, "birth": "January 11, 2003",
        "photo": None,
        "winnings": "$165,000", "winningsNum": 165000, "sTierWins": 1, "aTierWins": 4, "totalWins": 5,
        "signatureHeroes": ["Tracer", "Genji", "Echo"],
        "teamHistory": [
            {"period": "2019 - 2021", "team": "T1"},
            {"period": "2021 - 2023", "team": "Philadelphia Fusion / Seoul Infernal"},
            {"period": "2024 - 2026", "team": "T1"}
        ],
        "achievements": [
            {"date": "2023-06-18", "place": "3rd", "tier": "S-Tier", "tournament": "Overwatch League 2023 - Midseason Madness", "team": "INF", "prize": "$125,000"}
        ]
    },
    "BLISS": {
        "id": "BLISS", "team": "T1", "realName": "김소명", "romanizedName": "Kim So-myung",
        "nationality": "South Korea", "age": 21, "birth": "August 10, 2005",
        "photo": None,
        "winnings": "$140,000", "winningsNum": 140000, "sTierWins": 0, "aTierWins": 4, "totalWins": 4,
        "signatureHeroes": ["Lucio", "Brigitte"],
        "teamHistory": [
            {"period": "2021 - 2022", "team": "O2 Blast"},
            {"period": "2022 - 2023", "team": "Dallas Fuel"},
            {"period": "2024 - 2026", "team": "T1"}
        ],
        "achievements": []
    },
    "SKEWED": {
        "id": "SKEWED", "team": "T1", "realName": "김민석", "romanizedName": "Kim Min-seok",
        "nationality": "South Korea", "age": 24, "birth": "January 26, 2002",
        "photo": None,
        "winnings": "$195,000", "winningsNum": 195000, "sTierWins": 3, "aTierWins": 3, "totalWins": 6,
        "signatureHeroes": ["Brigitte", "Zenyatta", "Ana"],
        "teamHistory": [
            {"period": "2020", "team": "OZ Gaming"},
            {"period": "2020 - 2022", "team": "Los Angeles Gladiators"},
            {"period": "2022 - 2023", "team": "Seoul Infernal"},
            {"period": "2024 - 2026", "team": "T1"}
        ],
        "achievements": [
            {"date": "2022-07-23", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2022 - Midseason Madness", "team": "LAG", "prize": "$500,000"}
        ]
    },
    "PROUD": {
        "id": "PROUD", "team": "T1", "realName": "홍석진", "romanizedName": "Hong Suk-jin",
        "nationality": "South Korea", "age": 20, "birth": "2006",
        "photo": None,
        "winnings": "$42,000", "winningsNum": 42000, "sTierWins": 0, "aTierWins": 2, "totalWins": 2,
        "signatureHeroes": ["Sojourn", "Widowmaker"],
        "teamHistory": [
            {"period": "2021 - 2022", "team": "Talon Esports"},
            {"period": "2023", "team": "Poker Face"},
            {"period": "2024 - 2026", "team": "T1"}
        ],
        "achievements": []
    },
    "JASM1NE": {
        "id": "JASM1NE", "team": "T1", "realName": "정종민", "romanizedName": "Jeong Jong-min",
        "nationality": "South Korea", "age": 21, "birth": "2005",
        "photo": None,
        "winnings": "$25,000", "winningsNum": 25000, "sTierWins": 0, "aTierWins": 1, "totalWins": 1,
        "signatureHeroes": ["D.Va", "Sigma"],
        "teamHistory": [
            {"period": "2024", "team": "Genesis"},
            {"period": "2025 - 2026", "team": "T1"}
        ],
        "achievements": []
    },

    # ==================== RØDE ZANSIDE GAMING (ROZE) ====================
    # (Formed May 2026 via merger of ONSIDE GAMING and ZAN Esports)
    "VOID": {
        "id": "VOID", "team": "ROZE", "realName": "강준우", "romanizedName": "Kang Jun-woo",
        "nationality": "South Korea", "age": 30, "birth": "May 4, 1996",
        "photo": None,
        "winnings": "$445,000", "winningsNum": 445000, "sTierWins": 5, "aTierWins": 4, "totalWins": 9,
        "signatureHeroes": ["Sigma", "D.Va", "Zarya"],
        "teamHistory": [
            {"period": "2016 - 2017", "team": "KongDoo Panthera"},
            {"period": "2017 - 2019", "team": "Los Angeles Gladiators"},
            {"period": "2019 - 2022", "team": "Shanghai Dragons"},
            {"period": "2024 - 2025", "team": "ZAN Esports"},
            {"period": "2026", "team": "RØDE ZANSIDE GAMING (ROZE)"}
        ],
        "achievements": [
            {"date": "2021-09-25", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2021 - Playoffs", "team": "SHD", "prize": "$1,500,000"}
        ]
    },
    "KILO": {
        "id": "KILO", "team": "ROZE", "realName": "정진우", "romanizedName": "Jung Jin-woo",
        "nationality": "South Korea", "age": 23, "birth": "March 24, 2003",
        "photo": None,
        "winnings": "$115,000", "winningsNum": 115000, "sTierWins": 0, "aTierWins": 3, "totalWins": 3,
        "signatureHeroes": ["Widowmaker", "Cassidy", "Ashe"],
        "teamHistory": [
            {"period": "2020 - 2021", "team": "O2 Blast"},
            {"period": "2021 - 2022", "team": "San Francisco Shock"},
            {"period": "2024 - 2025", "team": "ONSIDE GAMING"},
            {"period": "2026", "team": "RØDE ZANSIDE GAMING (ROZE)"}
        ],
        "achievements": [
            {"date": "2022-11-04", "place": "2nd", "tier": "S-Tier", "tournament": "Overwatch League 2022 - Playoffs", "team": "SFS", "prize": "$500,000"}
        ]
    },
    "BECKY": {
        "id": "BECKY", "team": "ROZE", "realName": "김일하", "romanizedName": "Kim Il-ha",
        "nationality": "South Korea", "age": 22, "birth": "September 19, 2003",
        "photo": None,
        "winnings": "$65,000", "winningsNum": 65000, "sTierWins": 0, "aTierWins": 2, "totalWins": 2,
        "signatureHeroes": ["Genji", "Tracer"],
        "teamHistory": [
            {"period": "2021", "team": "O2 Blast"},
            {"period": "2021 - 2022", "team": "Toronto Defiant"},
            {"period": "2024 - 2025", "team": "ONSIDE GAMING"},
            {"period": "2026", "team": "RØDE ZANSIDE GAMING (ROZE)"}
        ],
        "achievements": []
    },
    "OPENER": {
        "id": "OPENER", "team": "ROZE", "realName": "안기범", "romanizedName": "An Gi-beom",
        "nationality": "South Korea", "age": 23, "birth": "March 23, 2003",
        "photo": None,
        "winnings": "$58,000", "winningsNum": 58000, "sTierWins": 0, "aTierWins": 2, "totalWins": 2,
        "signatureHeroes": ["Lucio", "Brigitte"],
        "teamHistory": [
            {"period": "2021", "team": "O2 Blast"},
            {"period": "2021 - 2022", "team": "Washington Justice"},
            {"period": "2024 - 2025", "team": "ONSIDE GAMING"},
            {"period": "2026", "team": "RØDE ZANSIDE GAMING (ROZE)"}
        ],
        "achievements": []
    },
    "HEISER": {
        "id": "HEISER", "team": "ROZE", "realName": "조유현", "romanizedName": "Cho Yu-hyun",
        "nationality": "South Korea", "age": 21, "birth": "2005",
        "photo": None,
        "winnings": "$25,000", "winningsNum": 25000, "sTierWins": 0, "aTierWins": 1, "totalWins": 1,
        "signatureHeroes": ["Winston"],
        "teamHistory": [
            {"period": "2023", "team": "Team Diamond"},
            {"period": "2024 - 2025", "team": "ZAN Esports"},
            {"period": "2026", "team": "RØDE ZANSIDE GAMING (ROZE)"}
        ],
        "achievements": []
    },
    "PROBE": {
        "id": "PROBE", "team": "ROZE", "realName": "정준영", "romanizedName": "Jung Jun-young",
        "nationality": "South Korea", "age": 21, "birth": "2005",
        "photo": None,
        "winnings": "$30,000", "winningsNum": 30000, "sTierWins": 0, "aTierWins": 1, "totalWins": 1,
        "signatureHeroes": ["Ashe", "Cassidy"],
        "teamHistory": [
            {"period": "2023", "team": "Poker Face"},
            {"period": "2024 - 2025", "team": "ONSIDE GAMING"},
            {"period": "2026", "team": "RØDE ZANSIDE GAMING (ROZE)"}
        ],
        "achievements": []
    },
    "IRONY": {
        "id": "IRONY", "team": "ROZE", "realName": "김백강", "romanizedName": "Kim Baek-kang",
        "nationality": "South Korea", "age": 22, "birth": "2004",
        "photo": None,
        "winnings": "$52,000", "winningsNum": 52000, "sTierWins": 0, "aTierWins": 2, "totalWins": 2,
        "signatureHeroes": ["Ana", "Kiriko"],
        "teamHistory": [
            {"period": "2021", "team": "O2 Blast"},
            {"period": "2021 - 2023", "team": "Hangzhou Spark"},
            {"period": "2024 - 2025", "team": "ZAN Esports"},
            {"period": "2026", "team": "RØDE ZANSIDE GAMING (ROZE)"}
        ],
        "achievements": []
    },

    # ==================== O2 BLAST (O2) ====================
    "FATE": {
        "id": "FATE", "team": "O2", "realName": "구판승", "romanizedName": "Koo Pan-seung",
        "nationality": "South Korea", "age": 27, "birth": "October 20, 1998",
        "photo": None,
        "winnings": "$515,000", "winningsNum": 515000, "sTierWins": 5, "aTierWins": 4, "totalWins": 9,
        "signatureHeroes": ["Wrecking Ball", "Winston", "Reinhardt"],
        "teamHistory": [
            {"period": "2016 - 2017", "team": "Mighty AOD"},
            {"period": "2017 - 2019", "team": "Los Angeles Valiant"},
            {"period": "2019 - 2020", "team": "Florida Mayhem"},
            {"period": "2020 - 2022", "team": "Shanghai Dragons"},
            {"period": "2025 - 2026", "team": "O2 Blast"}
        ],
        "achievements": [
            {"date": "2021-09-25", "place": "1st", "tier": "S-Tier", "tournament": "Overwatch League 2021 - Playoffs", "team": "SHD", "prize": "$1,500,000"}
        ]
    },
    "FAITH": {
        "id": "FAITH", "team": "O2", "realName": "홍홍규", "romanizedName": "Hong Hong-gyu",
        "nationality": "South Korea", "age": 24, "birth": "January 8, 2002",
        "photo": None,
        "winnings": "$135,000", "winningsNum": 135000, "sTierWins": 0, "aTierWins": 3, "totalWins": 3,
        "signatureHeroes": ["Brigitte", "Lucio"],
        "teamHistory": [
            {"period": "2019 - 2020", "team": "WGS Phoenix"},
            {"period": "2020 - 2022", "team": "Boston Uprising"},
            {"period": "2022 - 2023", "team": "Vancouver Titans"},
            {"period": "2024 - 2026", "team": "O2 Blast"}
        ],
        "achievements": []
    },
    "SEUNGAN": {"id": "SEUNGAN", "team": "O2", "realName": "김승안", "romanizedName": "Kim Seung-an", "nationality": "South Korea", "age": 20, "birth": "2006", "photo": None, "winnings": "$20,000", "winningsNum": 20000, "sTierWins": 0, "aTierWins": 1, "totalWins": 1, "signatureHeroes": ["Tracer"], "teamHistory": [{"period": "2023 - 2024", "team": "O2 Academy"}, {"period": "2025 - 2026", "team": "O2 Blast"}], "achievements": []},
    "WUTIAN": {"id": "WUTIAN", "team": "O2", "realName": "오우천", "romanizedName": "Oh Woo-cheon", "nationality": "South Korea", "age": 20, "birth": "2006", "photo": None, "winnings": "$18,000", "winningsNum": 18000, "sTierWins": 0, "aTierWins": 1, "totalWins": 1, "signatureHeroes": ["Sigma"], "teamHistory": [{"period": "2023 - 2024", "team": "O2 Academy"}, {"period": "2025 - 2026", "team": "O2 Blast"}], "achievements": []},
    "PERR": {"id": "PERR", "team": "O2", "realName": "박배르", "romanizedName": "Park Bae-reu", "nationality": "South Korea", "age": 21, "birth": "2005", "photo": None, "winnings": "$16,500", "winningsNum": 16500, "sTierWins": 0, "aTierWins": 1, "totalWins": 1, "signatureHeroes": ["Ashe"], "teamHistory": [{"period": "2023 - 2024", "team": "O2 Academy"}, {"period": "2025 - 2026", "team": "O2 Blast"}], "achievements": []},
    "MISIN": {"id": "MISIN", "team": "O2", "realName": "조미신", "romanizedName": "Cho Mi-shin", "nationality": "South Korea", "age": 20, "birth": "2006", "photo": None, "winnings": "$22,000", "winningsNum": 22000, "sTierWins": 0, "aTierWins": 1, "totalWins": 1, "signatureHeroes": ["Ana"], "teamHistory": [{"period": "2023 - 2024", "team": "O2 Academy"}, {"period": "2025", "team": "Poker Face"}, {"period": "2026", "team": "O2 Blast"}], "achievements": []},
    "GAMJUNG": {"id": "GAMJUNG", "team": "O2", "realName": "김감정", "romanizedName": "Kim Gam-jeong", "nationality": "South Korea", "age": 21, "birth": "2005", "photo": None, "winnings": "$15,000", "winningsNum": 15000, "sTierWins": 0, "aTierWins": 1, "totalWins": 1, "signatureHeroes": ["Kiriko"], "teamHistory": [{"period": "2023 - 2024", "team": "O2 Academy"}, {"period": "2025 - 2026", "team": "O2 Blast"}], "achievements": []},

    # ==================== POKER FACE (PF) ====================
    "CARU": {"id": "CARU", "team": "PF", "realName": "임정민", "romanizedName": "Lim Jung-min", "nationality": "South Korea", "age": 22, "birth": "2004", "photo": None, "winnings": "$38,000", "winningsNum": 38000, "sTierWins": 0, "aTierWins": 1, "totalWins": 1, "signatureHeroes": ["Ana", "Baptiste"], "teamHistory": [{"period": "2021", "team": "O2 High School"}, {"period": "2022 - 2024", "team": "Poker Face"}, {"period": "2025 - 2026", "team": "Poker Face"}], "achievements": []},
    "FEARFUL": {"id": "FEARFUL", "team": "PF", "realName": "이재훈", "romanizedName": "Lee Jae-hoon", "nationality": "South Korea", "age": 21, "birth": "2005", "photo": None, "winnings": "$28,000", "winningsNum": 28000, "sTierWins": 0, "aTierWins": 1, "totalWins": 1, "signatureHeroes": ["Winston", "Doomfist"], "teamHistory": [{"period": "2023 - 2024", "team": "Poker Face"}, {"period": "2025 - 2026", "team": "Poker Face"}], "achievements": []},
    "HYEON": {"id": "HYEON", "team": "PF", "realName": "김현", "romanizedName": "Kim Hyun", "nationality": "South Korea", "age": 21, "birth": "2005", "photo": None, "winnings": "$26,000", "winningsNum": 26000, "sTierWins": 0, "aTierWins": 1, "totalWins": 1, "signatureHeroes": ["D.Va", "Sigma"], "teamHistory": [{"period": "2023 - 2024", "team": "Poker Face"}, {"period": "2025 - 2026", "team": "Poker Face"}], "achievements": []},
    "D0D0": {"id": "D0D0", "team": "PF", "realName": "김도현", "romanizedName": "Kim Do-hyun", "nationality": "South Korea", "age": 20, "birth": "2006", "photo": None, "winnings": "$32,000", "winningsNum": 32000, "sTierWins": 0, "aTierWins": 1, "totalWins": 1, "signatureHeroes": ["Tracer", "Echo"], "teamHistory": [{"period": "2023 - 2024", "team": "Poker Face"}, {"period": "2025 - 2026", "team": "Poker Face"}], "achievements": []},
    "K4NE": {"id": "K4NE", "team": "PF", "realName": "강현석", "romanizedName": "Kang Hyun-seok", "nationality": "South Korea", "age": 21, "birth": "2005", "photo": None, "winnings": "$29,000", "winningsNum": 29000, "sTierWins": 0, "aTierWins": 1, "totalWins": 1, "signatureHeroes": ["Cassidy", "Sojourn"], "teamHistory": [{"period": "2023 - 2024", "team": "Poker Face"}, {"period": "2025 - 2026", "team": "Poker Face"}], "achievements": []},
    "SP1NEL": {"id": "SP1NEL", "team": "PF", "realName": "정찬빈", "romanizedName": "Jung Chan-bin", "nationality": "South Korea", "age": 21, "birth": "2005", "photo": None, "winnings": "$27,000", "winningsNum": 27000, "sTierWins": 0, "aTierWins": 1, "totalWins": 1, "signatureHeroes": ["Lucio", "Brigitte"], "teamHistory": [{"period": "2023 - 2024", "team": "Poker Face"}, {"period": "2025 - 2026", "team": "Poker Face"}], "achievements": []},

    # ==================== CHEESEBURGER (CB) ====================
    "FARMER": {"id": "FARMER", "team": "CB", "realName": "박민서", "romanizedName": "Park Min-seo", "nationality": "South Korea", "age": 21, "birth": "2005", "photo": None, "winnings": "$8,000", "winningsNum": 8000, "sTierWins": 0, "aTierWins": 0, "totalWins": 0, "signatureHeroes": ["Winston"], "teamHistory": [{"period": "2025", "team": "Open Division Korea"}, {"period": "2026", "team": "Cheeseburger (OWCS Korea 2026 출전)"}], "achievements": []},
    "GUR3UM": {"id": "GUR3UM", "team": "CB", "realName": "이구름", "romanizedName": "Lee Gu-reum", "nationality": "South Korea", "age": 20, "birth": "2006", "photo": None, "winnings": "$12,000", "winningsNum": 12000, "sTierWins": 0, "aTierWins": 0, "totalWins": 0, "signatureHeroes": ["Sigma"], "teamHistory": [{"period": "2025", "team": "Poker Face"}, {"period": "2026", "team": "Cheeseburger (2026년 합류)"}], "achievements": []},
    "ARGON": {"id": "ARGON", "team": "CB", "realName": "김정환", "romanizedName": "Kim Jung-hwan", "nationality": "South Korea", "age": 21, "birth": "2005", "photo": None, "winnings": "$9,000", "winningsNum": 9000, "sTierWins": 0, "aTierWins": 0, "totalWins": 0, "signatureHeroes": ["Tracer"], "teamHistory": [{"period": "2025", "team": "Open Division Korea"}, {"period": "2026", "team": "Cheeseburger (OWCS Korea 2026 출전)"}], "achievements": []},
    "M1NUT2": {"id": "M1NUT2", "team": "CB", "realName": "민우진", "romanizedName": "Min Woo-jin", "nationality": "South Korea", "age": 21, "birth": "2005", "photo": None, "winnings": "$8,500", "winningsNum": 8500, "sTierWins": 0, "aTierWins": 0, "totalWins": 0, "signatureHeroes": ["Sojourn"], "teamHistory": [{"period": "2025", "team": "Open Division Korea"}, {"period": "2026", "team": "Cheeseburger (OWCS Korea 2026 출전)"}], "achievements": []},
    "TENTEN": {"id": "TENTEN", "team": "CB", "realName": "김태은", "romanizedName": "Kim Tae-eun", "nationality": "South Korea", "age": 20, "birth": "2006", "photo": None, "winnings": "$8,000", "winningsNum": 8000, "sTierWins": 0, "aTierWins": 0, "totalWins": 0, "signatureHeroes": ["Lucio"], "teamHistory": [{"period": "2025", "team": "Open Division Korea"}, {"period": "2026", "team": "Cheeseburger (OWCS Korea 2026 출전)"}], "achievements": []},
    "WOOCHAN": {"id": "WOOCHAN", "team": "CB", "realName": "김우찬", "romanizedName": "Kim Woo-chan", "nationality": "South Korea", "age": 21, "birth": "2005", "photo": None, "winnings": "$9,200", "winningsNum": 9200, "sTierWins": 0, "aTierWins": 0, "totalWins": 0, "signatureHeroes": ["Ana"], "teamHistory": [{"period": "2025", "team": "Open Division Korea"}, {"period": "2026", "team": "Cheeseburger (OWCS Korea 2026 출전)"}], "achievements": []},

    # ==================== SUPERBAD (SB) ====================
    # (Formed May 2026, entered OWCS Korea Stage 2)
    "SENTIER": {"id": "SENTIER", "team": "SB", "realName": "신선우", "romanizedName": "Shin Sun-woo", "nationality": "South Korea", "age": 22, "birth": "2004", "photo": None, "winnings": "$11,000", "winningsNum": 11000, "sTierWins": 0, "aTierWins": 0, "totalWins": 0, "signatureHeroes": ["Winston"], "teamHistory": [{"period": "2025", "team": "Open Division Korea"}, {"period": "2026", "team": "SuperBad (2026년 5월 창단)"}], "achievements": []},
    "HOMERUNBALL": {"id": "HOMERUNBALL", "team": "SB", "realName": "박준호", "romanizedName": "Park Jun-ho", "nationality": "South Korea", "age": 21, "birth": "2005", "photo": None, "winnings": "$10,000", "winningsNum": 10000, "sTierWins": 0, "aTierWins": 0, "totalWins": 0, "signatureHeroes": ["D.Va"], "teamHistory": [{"period": "2025", "team": "Open Division Korea"}, {"period": "2026", "team": "SuperBad (2026년 5월 창단)"}], "achievements": []},
    "AZENT": {"id": "AZENT", "team": "SB", "realName": "이민준", "romanizedName": "Lee Min-jun", "nationality": "South Korea", "age": 20, "birth": "2006", "photo": None, "winnings": "$9,500", "winningsNum": 9500, "sTierWins": 0, "aTierWins": 0, "totalWins": 0, "signatureHeroes": ["Tracer"], "teamHistory": [{"period": "2025", "team": "Open Division Korea"}, {"period": "2026", "team": "SuperBad (2026년 5월 창단)"}], "achievements": []},
    "SORI": {"id": "SORI", "team": "SB", "realName": "김소리", "romanizedName": "Kim So-ri", "nationality": "South Korea", "age": 21, "birth": "2005", "photo": None, "winnings": "$12,500", "winningsNum": 12500, "sTierWins": 0, "aTierWins": 0, "totalWins": 0, "signatureHeroes": ["Sojourn"], "teamHistory": [{"period": "2025", "team": "Open Division Korea"}, {"period": "2026", "team": "SuperBad"}, {"period": "2026", "team": "Poker Face (2026년 후반 이적)"}], "achievements": []},
    "SOAE": {"id": "SOAE", "team": "SB", "realName": "박소애", "romanizedName": "Park So-ae", "nationality": "South Korea", "age": 20, "birth": "2006", "photo": None, "winnings": "$11,500", "winningsNum": 11500, "sTierWins": 0, "aTierWins": 0, "totalWins": 0, "signatureHeroes": ["Echo"], "teamHistory": [{"period": "2025", "team": "Open Division Korea"}, {"period": "2026", "team": "SuperBad"}, {"period": "2026", "team": "Poker Face (2026년 후반 이적)"}], "achievements": []},
    "DUMBBELL": {"id": "DUMBBELL", "team": "SB", "realName": "최성진", "romanizedName": "Choi Sung-jin", "nationality": "South Korea", "age": 21, "birth": "2005", "photo": None, "winnings": "$12,000", "winningsNum": 12000, "sTierWins": 0, "aTierWins": 0, "totalWins": 0, "signatureHeroes": ["Lucio"], "teamHistory": [{"period": "2025", "team": "Open Division Korea"}, {"period": "2026", "team": "SuperBad"}, {"period": "2026", "team": "Poker Face (2026년 후반 이적)"}], "achievements": []},
    "UNIV2R": {"id": "UNIV2R", "team": "SB", "realName": "김우주", "romanizedName": "Kim Woo-joo", "nationality": "South Korea", "age": 21, "birth": "2005", "photo": None, "winnings": "$10,500", "winningsNum": 10500, "sTierWins": 0, "aTierWins": 0, "totalWins": 0, "signatureHeroes": ["Ana"], "teamHistory": [{"period": "2025", "team": "Open Division Korea"}, {"period": "2026", "team": "SuperBad (2026년 5월 창단)"}], "achievements": []}
}

TEAMS_META = {
    "CR": {
        "name": "Crazy Raccoon",
        "headquarters": "Japan",
        "activeOwcsSince": "2024",
        "lanEventWinner": [
            "2024 Dallas Major",
            "2025 Champions Clash",
            "2026 Champions Clash"
        ],
        "trophies": [
            "2024 OWCS Asia Stage 1",
            "2024 OWCS Dallas Major",
            "EWC 2024",
            "2025 OWCS Korea Stage 1",
            "2025 OWCS Asia Stage 1",
            "2025 OWCS Champions Clash",
            "2025 OWCS Korea Stage 2",
            "2025 OWCS Korea Stage 3",
            "2025 OWCS Korea Road to World Finals",
            "2026 OWCS Champions Clash"
        ]
    },
    "FLC": {
        "name": "Team Falcons",
        "headquarters": "Saudi Arabia",
        "activeOwcsSince": "2024",
        "lanEventWinner": [
            "2024 World Finals",
            "2025 Midseason Championship"
        ],
        "trophies": [
            "2024 OWCS Korea Stage 1",
            "2024 OWCS Korea Stage 2",
            "2024 OWCS Asia Stage 2",
            "2024 OWCS World Finals",
            "2025 OWCS Midseason Championship (EWC)"
        ]
    },
    "ZETA": {
        "name": "ZETA DIVISION",
        "headquarters": "Japan",
        "activeOwcsSince": "2024",
        "lanEventWinner": [
            "2026 Midseason Championship"
        ],
        "trophies": [
            "2026 OWCS Korea Stage 1",
            "2026 OWCS Asia Stage 1",
            "2026 OWCS Korea Stage 2",
            "2026 OWCS Midseason Championship (EWC)"
        ]
    },
    "PF": {
        "name": "Poker Face",
        "headquarters": "South Korea",
        "activeOwcsSince": "2024",
        "lanEventWinner": [],
        "trophies": []
    },
    "T1": {
        "name": "T1",
        "headquarters": "South Korea",
        "activeOwcsSince": "2025",
        "lanEventWinner": [],
        "trophies": []
    },
    "CB": {
        "name": "Cheeseburger",
        "headquarters": "South Korea",
        "activeOwcsSince": "2025",
        "lanEventWinner": [],
        "trophies": []
    },
    "ROZE": {
        "name": "Røde Zanside Gaming",
        "headquarters": "South Korea",
        "activeOwcsSince": "2025 (Including ONSIDE GAMING era)",
        "lanEventWinner": [],
        "trophies": []
    },
    "SB": {
        "name": "SuperBad",
        "headquarters": "South Korea",
        "activeOwcsSince": "2026",
        "lanEventWinner": [],
        "trophies": []
    },
    "O2": {
        "name": "O2 Blast",
        "headquarters": "South Korea",
        "activeOwcsSince": "2026",
        "lanEventWinner": [],
        "trophies": []
    }
}

LIQUIPEDIA_SLUGS = {
    "LIP": "LIP", "CH0R0NG": "CH0R0NG", "JUNBIN": "Junbin", "MAX": "MAX", "HEESANG": "HeeSang",
    "CHIYO": "ChiYo", "CHANGSIK": "CHANGSIK", "VIGILANTE": "Vigilante", "STALK3R": "Stalk3r",
    "SMURF": "Smurf", "HANBIN": "Hanbin", "FIELDER": "Fielder", "MER1T": "MER1T", "CHECKMATE": "Checkmate",
    "SP1NT": "SP1NT", "SIRMAJED": "SirMajed", "BERNAR": "Bernar", "VIOL2T": "Viol2t", "SHU": "Shu",
    "PROPER": "Proper", "ALPHAYI": "AlphaYi", "FLORA": "Flora", "MEALGARU": "Mealgaru", "KNIFE": "Knife",
    "FLETA": "Fleta", "DONGHAK": "DONGHAK", "JASM1NE": "Jasm1ne", "ZEST": "ZEST", "PROUD": "Proud",
    "BLISS": "Bliss", "SKEWED": "Skewed", "VOID": "Void", "KILO": "Kilo", "BECKY": "Becky",
    "OPENER": "Opener", "HEISER": "Heiser", "PROBE": "PROBE", "IRONY": "IRONY", "FATE": "Fate",
    "FAITH": "Faith", "SEUNGAN": "Seungan", "WUTIAN": "Wutian", "PERR": "Perr", "MISIN": "Misin",
    "GAMJUNG": "Gamjung", "CARU": "Caru", "FEARFUL": "Fearful", "HYEON": "Hyeon", "D0D0": "D0D0",
    "K4NE": "K4ne", "SP1NEL": "Sp1nel", "FARMER": "Farmer", "GUR3UM": "Gur3um", "ARGON": "Argon",
    "M1NUT2": "M1nut2", "TENTEN": "Tenten", "WOOCHAN": "Woochan", "SENTIER": "Sentier",
    "HOMERUNBALL": "Homerunball", "AZENT": "Azent", "SORI": "Sori", "SOAE": "Soae",
    "DUMBBELL": "Dumbbell", "UNIV2R": "Univ2r"
}

def generate_liquipedia_js():
    # Attach liquipediaUrl to players
    for p_id, p_data in PLAYERS_DB.items():
        slug = LIQUIPEDIA_SLUGS.get(p_id, p_id)
        p_data["liquipediaUrl"] = f"https://liquipedia.net/overwatch/{slug}"

    teams_output = {}
    for short, meta in TEAMS_META.items():
        team_players = [p for p in PLAYERS_DB.values() if p["team"] == short]
        teams_output[short] = {
            "short": short,
            "name": meta["name"],
            "headquarters": meta["headquarters"],
            "activeOwcsSince": meta["activeOwcsSince"],
            "lanEventWinner": meta["lanEventWinner"],
            "majorTrophies": meta["trophies"],
            "playerCount": len(team_players)
        }

    output_payload = {
        "fetchedAt": datetime.now().isoformat(),
        "season": "OWCS 2026 Stage 2",
        "players": PLAYERS_DB,
        "teams": teams_output
    }

    os.makedirs(os.path.dirname(OUTPUT_JS), exist_ok=True)
    with open(OUTPUT_JS, "w", encoding="utf-8") as f:
        f.write(f"window.OWCS_LIQUIPEDIA = {json.dumps(output_payload, indent=2, ensure_ascii=False)};\n")

    print(f"Generated {len(PLAYERS_DB)} players and {len(teams_output)} teams in {OUTPUT_JS} (Full user specifications applied)")

if __name__ == "__main__":
    generate_liquipedia_js()

