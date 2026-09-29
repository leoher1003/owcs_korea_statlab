#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teams_list_temporal.py
Temporal working copy for OWCS Team Rosters (Active & Inactive)
Parsed and structured from Liquipedia API.

Data Architecture:
- ACTIVE Teams: Current Active Roster (PLAYERS) and Staff/Coaches (STAFF)
- INACTIVE Teams: Disbandment Roster (PLAYERS), Staff at Disbandment (STAFF), and Special Notes (NOTE: M&A, seed transfer, hiatus, etc.)
"""

TEAMS_ROSTER = {
    # =========================================================================
    # OWCS KOREA (KR) ACTIVE
    # =========================================================================
    "Crazy Raccoon": {
        "STAFF": {
            "Moon": "Head Coach",
            "Kong": "Assistant Coach",
            "Izayaki": "Assistant Coach",
            "Twinkl": "General Manager",
            "Pavane": "Assistant General Manager"
        },
        "PLAYERS": {
            "Junbin": "TANK",
            "MAX": "TANK",
            "HeeSang": "DPS",
            "LIP": "DPS",
            "Stalk3r": "DPS",
            "CH0R0NG": "SPT",
            "vigilante": "SPT"
        }
    },
    "Team Falcons": {
        "STAFF": {
            "NineK": "Head Coach",
            "Junkbuck": "Coach",
            "SP9RK1E": "Coach",
            "Levi": "Team Manager"
        },
        "PLAYERS": {
            "HanBin": "TANK",
            "SOMEONE": "TANK",
            "Checkmate": "DPS",
            "SP1NT": "DPS",
            "MER1T": "DPS",
            "ChiYo": "SPT",
            "Fielder": "SPT"
        }
    },
    "ZETA DIVISION": {
        "STAFF": {
            "Crusty": "Head Coach",
            "Twilight": "Coach"
        },
        "PLAYERS": {
            "Bernar": "TANK",
            "Mealgaru": "TANK",
            "Proper": "DPS",
            "knife": "DPS",
            "Viol2t": "SPT",
            "shu": "SPT"
        }
    },
    "T1": {
        "STAFF": {
            "RUSH": "Head Coach",
            "Fleta": "Playing Coach",
            "GgulTaek": "Coach"
        },
        "PLAYERS": {
            "DONGHAK": "TANK",
            "Jasm1ne": "TANK",
            "ZEST": "DPS",
            "Proud": "DPS",
            "Bliss": "SPT",
            "skewed": "SPT"
        }
    },
    "Røde ZANSIDE GAMING": {
        "STAFF": {
            "KariV": "Head Coach",
            "Ir1s": "Coach",
            "Mircalla": "Coach"
        },
        "PLAYERS": {
            "HEISER": "TANK",
            "HEESUNG": "TANK",
            "Taejong": "DPS",
            "Kilo": "DPS",
            "Becky": "DPS",
            "OPENER": "SPT",
            "IRONY": "SPT"
        }
    },
    "O2 Blast": {
        "STAFF": {
            "O2Boss": "Head Coach",
            "Chilhwa": "Coach",
            "Myunb0ng": "Coach",
            "Cane": "Coach"
        },
        "PLAYERS": {
            "FATE": "TANK",
            "Homerunball": "TANK",
            "WuTian": "DPS",
            "Perr": "DPS",
            "A1IEN": "DPS",
            "Faith": "SPT",
            "Gamjung": "SPT"
        }
    },
    "Poker Face": {
        "STAFF": {
            "SEON": "Head Coach",
            "Mandu": "Coach"
        },
        "PLAYERS": {
            "SoLA": "TANK",
            "SWOO": "TANK",
            "F1nally": "DPS",
            "SORI": "DPS",
            "Dumbbell": "SPT",
            "Caffeine": "SPT",
            "SOAE": "SPT"
        }
    },
    "Cheeseburger": {
        "STAFF": {
            "KRILLIN": "Coach"
        },
        "PLAYERS": {
            "Belosrea": "TANK",
            "K4NE": "DPS",
            "Profit": "DPS",
            "AZENT": "DPS",
            "TENTEN": "SPT",
            "Trest": "SPT"
        }
    },
    "Seiji Esports": {
        "STAFF": {
            "Da1Da1Smooth": "Coach",
            "SanGuiNar": "Coach"
        },
        "PLAYERS": {
            "SENTIER": "TANK",
            "DOX": "TANK",
            "D4RT": "DPS",
            "M1NUT2": "DPS",
            "OFF": "SPT",
            "Lavender": "SPT"
        }
    },

    # =========================================================================
    # OWCS KOREA (KR) INACTIVE
    # =========================================================================
    "WAC": {
        "STAFF": {
            "MOON": "Head Coach",
            "Kong": "Coach",
            "Pavane": "Coach"
        },
        "PLAYERS": {
            "Junbin": "TANK",
            "MAX": "TANK",
            "HeeSang": "DPS",
            "LIP": "DPS",
            "CH0R0NG": "SPT",
            "shu": "SPT"
        },
        "NOTE": "Whole roster acquired by Crazy Raccoon prior to OWCS Asia Stage 1."
    },
    "From The Gamer": {
        "STAFF": {
            "Neko": "Coach"
        },
        "PLAYERS": {
            "Bernar": "TANK",
            "AlphaYi": "DPS",
            "Flora": "DPS",
            "Viol2t": "SPT",
            "FiNN": "SPT"
        },
        "NOTE": "Whole roster acquired by ZETA DIVISION prior to OWCS Stage 2."
    },
    "YETI": {
        "STAFF": {
            "Fate": "Head Coach",
            "Fleta": "Coach"
        },
        "PLAYERS": {
            "DONGHAK": "TANK",
            "Viper": "DPS",
            "knife": "DPS",
            "Bliss": "SPT",
            "IRONY": "SPT"
        },
        "NOTE": "Whole roster acquired by FNATIC prior to OWCS Korea Stage 2."
    },
    "RunAway": {
        "STAFF": {
            "Chara": "Coach"
        },
        "PLAYERS": {
            "MAG": "TANK",
            "ZEST": "DPS",
            "Prophet": "DPS",
            "LeeJaeGon": "SPT",
            "vigilante": "SPT"
        },
        "NOTE": "Disbanded after 2024 OWCS Korea Stage 1."
    },
    "Vesta Esports Crew": {
        "STAFF": {
            "YUL": "Coach",
            "Dumbbell": "Analyst"
        },
        "PLAYERS": {
            "Leonopteryx": "TANK",
            "BreadTurtle": "DPS",
            "Setsuna": "DPS",
            "Liz": "SPT",
            "Kiibo": "SPT",
            "NHZ": "SPT"
        },
        "NOTE": "Formed via merger of Invincible and Born Flame in late 2023. Competed across OWCS Korea (2024 Stage 1~2, 2025 Stage 1~2) and OWCS Japan (2025 Stage 3). Officially disbanded on October 4, 2025."
    },
    "Sin Prisa Gaming": {
        "STAFF": {
            "SKY": "Head Coach",
            "Wonsoomin": "Coach",
            "Candle": "Manager",
            "Mobugi": "General Manager"
        },
        "PLAYERS": {
            "Mealgaru": "TANK",
            "Toyou": "TANK",
            "Ade": "DPS",
            "Argon": "DPS",
            "Hyunjae": "SPT",
            "LeeSooMin": "SPT"
        },
        "NOTE": "Announced the hiatus of their Overwatch division on April 16, 2024 after OWCS Korea Stage 1."
    },
    "FNATIC": {
        "STAFF": {
            "Fleta": "Head Coach",
            "nuGget": "Manager"
        },
        "PLAYERS": {
            "DONGHAK": "TANK",
            "Checkmate": "DPS",
            "knife": "DPS",
            "LeeJaeGon": "SPT",
            "Izayaki": "SPT"
        },
        "NOTE": "Acquired YETI roster ahead of 2024 OWCS Korea Stage 2 and EWC 2024. Exited Overwatch on September 17, 2024 following 2024 Stage 2."
    },
    "HaeJeokDan": {
        "STAFF": {
            "GgulTaek": "Coach"
        },
        "PLAYERS": {
            "Mag": "TANK",
            "ZEST": "DPS",
            "Viper": "DPS",
            "MN3": "DPS",
            "OPENER": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS Korea Stage 2 and won Aurora Cup Challenge 2024. Disbanded on January 16, 2025, with core roster (ZEST, Viper, OPENER, GgulTaek) acquired by T1 for the 2025 season."
    },
    "Old Ocean": {
        "STAFF": {
            "Yang1": "Head Coach",
            "Hunter": "Coach",
            "DOX": "Coach"
        },
        "PLAYERS": {
            "HEISER": "TANK",
            "Gur3um": "TANK",
            "A1IEN": "DPS",
            "Becky": "DPS",
            "D4RT": "DPS",
            "ryujehong": "SPT",
            "KIVIS": "SPT"
        },
        "NOTE": "Formed by veteran Korean players for 2024 Stage 2; re-qualified for 2025 Stage 2 and Stage 3. Officially disbanded on October 5, 2025 following 2025 Stage 3 LCQ."
    },
    "New Era": {
        "STAFF": {
            "Rumba": "Manager"
        },
        "PLAYERS": {
            "SoLA": "TANK",
            "D0D0": "DPS",
            "perr": "DPS",
            "Secret": "SPT",
            "MCD": "SPT",
            "Yate": "SPT"
        },
        "NOTE": "Competed in 2025 Stage 1 and 2026 Stage 1. Officially disbanded on April 27, 2026 following 2026 Stage 1."
    },
    "WAY": {
        "STAFF": {
            "GgulTaek": "Coach"
        },
        "PLAYERS": {
            "Mealgaru": "TANK",
            "PEPPI": "TANK",
            "Ade": "DPS",
            "WhoRu": "DPS",
            "LeeSooMin": "SPT",
            "MAKA": "SPT"
        },
        "NOTE": "Whole roster acquired by All Gamers Global during 2025 OWCS Korea Stage 2."
    },
    "All Gamers Global": {
        "STAFF": {
            "Daemin": "Coach",
            "Dongsu": "Coach",
            "Algos05": "Manager",
            "Cointree": "Assistant Manager"
        },
        "PLAYERS": {
            "Mealgaru": "TANK",
            "Jasm1ne": "TANK",
            "Ade": "DPS",
            "SeonJun": "DPS",
            "LeeSooMin": "SPT",
            "MAKA": "SPT"
        },
        "NOTE": "Acquired WAY roster to compete in 2025 Stage 2 and Midseason Championship (EWC). Disbanded on August 11, 2025, with core roster reforming as WAE."
    },
    "ONSIDE GAMING": {
        "STAFF": {
            "F4zE": "Head Coach",
            "Ado": "Coach",
            "Doo": "Coach",
            "Mixtape": "Manager"
        },
        "PLAYERS": {
            "Attack": "TANK",
            "Kilo": "DPS",
            "SP1NT": "DPS",
            "Haksal": "DPS",
            "OPENER": "SPT",
            "IRONY": "SPT"
        },
        "NOTE": "Competed across 2025 Stage 2~3 and 2026 Stage 1. Merged with ZAN Esports on May 20, 2026 to form Røde ZANSIDE GAMING."
    },
    "WAE": {
        "STAFF": {
            "Daemin": "Coach",
            "Dongsu": "Coach"
        },
        "PLAYERS": {
            "Mealgaru": "TANK",
            "Ade": "DPS",
            "SeonJun": "DPS",
            "Taejong": "DPS",
            "LeeSooMin": "SPT",
            "MAKA": "SPT"
        },
        "NOTE": "Former WAY/All Gamers Global roster reformed as WAE for 2025 Stage 3; won G-Star Cup 2025 Elite. Disbanded on January 24, 2026 as core roster transferred to Weibo Gaming and Dallas Fuel."
    },
    "Mir Gaming": {
        "STAFF": {
            "le0na": "Coach",
            "Rumba": "Manager"
        },
        "PLAYERS": {
            "RULER": "TANK",
            "Flos": "DPS",
            "AZENT": "DPS",
            "K4ne": "DPS",
            "MCD": "SPT",
            "Univ2r": "SPT"
        },
        "NOTE": "Acquired New Era roster on August 21, 2025 to compete in 2025 OWCS Korea Stage 3. Disbanded on October 29, 2025 following Stage 3."
    },
    "Røde ONSIDE GAMING": {
        "STAFF": {
            "F4ze": "Head Coach",
            "Ado": "Coach",
            "Haksal": "Coach"
        },
        "PLAYERS": {
            "Attack": "TANK",
            "Kilo": "DPS",
            "SP1NT": "DPS",
            "OPENER": "SPT",
            "IRONY": "SPT"
        },
        "NOTE": "Merged with ZAN Esports to form Røde ZANSIDE GAMING prior to 2026 OWCS Korea Stage 2."
    },
    "ZAN Esports": {
        "STAFF": {
            "KariV": "Head Coach",
            "Mircalla": "Coach",
            "Ir1s": "Coach",
            "sihu": "Manager"
        },
        "PLAYERS": {
            "HEISER": "TANK",
            "A1IEN": "DPS",
            "Probe": "DPS",
            "Becky": "DPS",
            "Yangjun": "SPT",
            "KIVIS": "SPT",
            "Havira": "SPT"
        },
        "NOTE": "Merged with Røde ONSIDE GAMING prior to 2026 OWCS Korea Stage 2."
    },
    "Super Bad": {
        "STAFF": {
            "SeltaRet": "Coach",
            "Yui": "Coach"
        },
        "PLAYERS": {
            "SENTIER": "TANK",
            "Homerunball": "TANK",
            "SORI": "DPS",
            "AZENT": "DPS",
            "Dumbbell": "SPT",
            "Univ2r": "SPT",
            "Soae": "SPT"
        },
        "NOTE": "Qualified 4th in 2026 OWCS Korea Stage 2 Open Qualifier and awarded seed after ZAN Esports relinquished their slot. Disbanded after Stage 2."
    },

    # =========================================================================
    # OWCS JAPAN (JP) ACTIVE
    # =========================================================================
    "VARREL": {
        "STAFF": {
            "Pain": "Coach",
            "Dae1": "Coach"
        },
        "PLAYERS": {
            "KSG": "TANK",
            "Nico": "DPS",
            "Qki": "DPS",
            "TOPDRAGON": "DPS",
            "Qloud": "SPT",
            "Sley": "SPT"
        }
    },
    "ENTER FORCE.36": {
        "STAFF": {
            "Tydolla": "Coach"
        },
        "PLAYERS": {
            "Fearless": "TANK",
            "Edison": "DPS",
            "NewJ": "DPS",
            "Soulsay": "DPS",
            "Ydot": "SPT",
            "Gaisen": "SPT"
        }
    },
    "MURASH GAMING": {
        "STAFF": {
            "YaHo": "Coach"
        },
        "PLAYERS": {
            "PEPPI": "TANK",
            "Viper": "DPS",
            "ky0n": "DPS",
            "epic": "SPT",
            "orca": "SPT"
        }
    },
    "99DIVINE": {
        "STAFF": {
            "Hyunjae": "Coach"
        },
        "PLAYERS": {
            "Ichi": "TANK",
            "MN3": "DPS",
            "ALTHOUGH": "DPS",
            "Sakume": "SPT",
            "Umi": "SPT",
            "Supreme": "SPT"
        }
    },
    "Please Not Hero Ban": {
        "STAFF": {},
        "PLAYERS": {
            "UYOU": "TANK",
            "RLG5656": "DPS",
            "Suraimu1": "DPS",
            "Neivis": "SPT",
            "Secret": "SPT",
            "Langley": "SPT"
        }
    },
    "Uwinks": {
        "STAFF": {
            "Opera": "Coach"
        },
        "PLAYERS": {
            "xzahyo": "TANK",
            "yumilalan": "TANK",
            "Yot1y": "DPS",
            "Develop": "DPS",
            "Undersea": "DPS",
            "EuclidEUC": "SPT",
            "UGH": "SPT",
            "APDO": "SPT"
        }
    },
    "Lazuli": {
        "STAFF": {
            "Ares": "Coach",
            "Mazzless": "Coach",
            "Baksa": "Coach"
        },
        "PLAYERS": {
            "FARMER": "TANK",
            "Probe": "DPS",
            "dra": "DPS",
            "zenith": "DPS",
            "sans": "SPT",
            "Amateru": "SPT"
        }
    },
    "REVATI": {
        "STAFF": {
            "Menhera": "Coach",
            "Nyammulba": "Coach",
            "LUD": "Manager",
            "KISHI": "Manager"
        },
        "PLAYERS": {
            "Vosa1q": "TANK",
            "BreadTurtle": "DPS",
            "Anarchy": "DPS",
            "Elysia": "SPT",
            "Azue1recker": "SPT"
        }
    },

    # =========================================================================
    # OWCS JAPAN (JP) INACTIVE
    # =========================================================================
    "SixBlow": {
        "STAFF": {
            "MyNa": "Manager"
        },
        "PLAYERS": {
            "Max": "TANK",
            "pressure": "TANK",
            "Doux": "DPS",
            "Rrmy": "DPS",
            "TQQ": "DPS",
            "APL01": "SPT",
            "MyNa": "SPT",
            "Sakume": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS Japan Stage 1, placing 7th-8th before disbanding."
    },
    "Arise Project": {
        "STAFF": {
            "Kutoto": "Head Coach",
            "HaRoom": "Coach",
            "Baksa": "Coach",
            "toriso": "Manager",
            "Takoyaki": "Manager"
        },
        "PLAYERS": {
            "Vosa1q": "TANK",
            "Dororo": "DPS",
            "Tomosa": "DPS",
            "TOMITAKEexe": "DPS",
            "kani": "SPT",
            "Fiesta": "SPT",
            "Astar": "SPT"
        },
        "NOTE": "Competed in 2024 Stage 1 and 2025 Stages 2~3 before disbanding following 2025 Stage 3."
    },
    "Namekuji Brothers": {
        "STAFF": {
            "Chen": "Coach"
        },
        "PLAYERS": {
            "Nsesl": "TANK",
            "Piece": "DPS",
            "NewJ": "DPS",
            "Bambie": "DPS",
            "Jisoo": "SPT",
            "Keiou": "SPT",
            "Menhera": "SPT",
            "EuclidEUC": "SPT"
        },
        "NOTE": "Finished 3rd in 2024 Stage 1 and 4th in Stage 2. Officially disbanded on January 3, 2025."
    },
    "Pandia": {
        "STAFF": {
            "YUL": "Coach"
        },
        "PLAYERS": {
            "chang": "TANK",
            "DOX": "TANK",
            "ZeSin": "DPS",
            "sanyo": "DPS",
            "Neivis": "SPT",
            "Mimoza": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS Japan Stage 1. Disbanded on April 2, 2024."
    },
    "INSOMNIA": {
        "STAFF": {
            "Spear": "Head Coach",
            "Menhera": "Assistant Coach",
            "GENESIS": "Manager"
        },
        "PLAYERS": {
            "elia": "TANK",
            "Hofac": "DPS",
            "Undersea": "DPS",
            "NHZ": "SPT",
            "eYeKu": "SPT",
            "Hesty": "SPT"
        },
        "NOTE": "Competed in 2024 Stage 1~2 and 2025 Stage 1. Withdrew prior to 2025 Stage 2 due to roster issues and officially disbanded."
    },
    "Hayabusa Gaming": {
        "STAFF": {
            "Godo": "Coach",
            "Angey": "Coach"
        },
        "PLAYERS": {
            "SoLA": "TANK",
            "SigSa": "DPS",
            "Momiji893": "DPS",
            "Keiou": "SPT",
            "FREGRE": "SPT",
            "Secret": "SPT"
        },
        "NOTE": "Long-running Japanese contender across 2024 Stage 1 and 2025 Stages 1~3 before disbanding."
    },
    "Nyam Gaming": {
        "STAFF": {
            "SeltaRet": "Coach",
            "soo": "Coach",
            "GBS": "Manager"
        },
        "PLAYERS": {
            "Roxy": "TANK",
            "APDO": "DPS",
            "Daisy": "DPS",
            "Undersea": "DPS",
            "orca": "SPT",
            "Mint": "SPT"
        },
        "NOTE": "Competed from 2024 Stage 1 through 2026 Stage 1 before disbanding."
    },
    "REVATI X NTMR": {
        "STAFF": {
            "Fickle": "Head Coach",
            "Byeolha": "Assistant Coach",
            "JeonMinHyouk": "Assistant Coach",
            "Fromis": "Assistant Coach",
            "Millfy": "Manager"
        },
        "PLAYERS": {
            "Fearful": "TANK",
            "solace": "DPS",
            "harutoon": "DPS",
            "Hofac": "DPS",
            "Hesty": "SPT",
            "epic": "SPT",
            "NHZ": "SPT"
        },
        "NOTE": "Joint partnership between REVATI and North American org NTMR for 2024 OWCS Japan Stage 2. Reverted back to REVATI post-tournament."
    },
    "MFC X Supreme": {
        "STAFF": {
            "HoChiLee": "Head Coach",
            "KymerOW": "Manager"
        },
        "PLAYERS": {
            "Romani": "TANK",
            "AOKIGAHARA": "DPS",
            "ta1yo": "DPS",
            "Kilaa": "DPS",
            "Frogger": "SPT",
            "Supreme": "SPT"
        },
        "NOTE": "Competed as a joint roster between MFC and Supreme in 2024 OWCS Japan Stage 2."
    },
    "Telomere": {
        "STAFF": {
            "YUL": "Coach"
        },
        "PLAYERS": {
            "Leonopteryx": "TANK",
            "Vosa1q": "TANK",
            "BreadTurtle": "DPS",
            "Pav2l": "DPS",
            "Kiibo": "SPT",
            "Elysia": "SPT",
            "HINIS4Ku": "SPT"
        },
        "NOTE": "Competed in 2024 Stage 2, 2025 Stage 3, and 2026 Stage 1 before disbanding."
    },
    "VortexWolf": {
        "STAFF": {
            "Undine": "Coach"
        },
        "PLAYERS": {
            "Kalios": "TANK",
            "Edison": "DPS",
            "Rrmy": "DPS",
            "AOKIGAHARA": "DPS",
            "kiru01": "SPT",
            "Sakume": "SPT"
        },
        "NOTE": "Placed 4th in 2025 OWCS Japan Stage 1 playoffs before core roster transferred to REJECT."
    },
    "JKOT": {
        "STAFF": {
            "Godo": "Coach",
            "Angey": "Coach",
            "taein": "Manager"
        },
        "PLAYERS": {
            "Leedy": "TANK",
            "ky0n": "DPS",
            "dra": "DPS",
            "Keiou": "SPT",
            "FREGRE": "SPT",
            "Secret": "SPT"
        },
        "NOTE": "Competed in 2025 OWCS Japan Stage 1 and Stage 2 before disbanding."
    },
    "Inferno": {
        "STAFF": {
            "YUL": "Head Coach",
            "SOL": "Coach"
        },
        "PLAYERS": {
            "SWOO": "TANK",
            "Hry": "DPS",
            "BreadTurtle": "DPS",
            "Prologue": "SPT",
            "Kiibo": "SPT",
            "HINIS4Ku": "SPT"
        },
        "NOTE": "Finished runners-up in 2025 OWCS Japan Stage 2 before disbanding ahead of Stage 3."
    },
    "Aplomb Tiger": {
        "STAFF": {
            "Mint": "Coach",
            "Da1Da1Sm00th": "Coach"
        },
        "PLAYERS": {
            "DOX": "TANK",
            "yumilalan": "TANK",
            "Daisy": "DPS",
            "FodCarry": "DPS",
            "Gaisen": "SPT",
            "mazz": "SPT"
        },
        "NOTE": "Competed in 2025 OWCS Japan Stage 1 and Stage 2 before disbanding."
    },
    "Under Cat": {
        "STAFF": {},
        "PLAYERS": {
            "ARLLY": "TANK",
            "ike": "TANK",
            "TOMITAKEexe": "DPS",
            "POSS": "SPT",
            "Qutyan": "SPT",
            "Noricutea": "SPT",
            "Sonic100": "SPT"
        },
        "NOTE": "Competed in 2025 OWCS Japan Stage 1 before disbanding."
    },
    "LostNever Gaming": {
        "STAFF": {
            "CALD": "Coach",
            "Akirou": "Assistant Coach",
            "Aki": "Manager"
        },
        "PLAYERS": {
            "XLIM": "TANK",
            "Wolf": "DPS",
            "ZEROLKH": "DPS",
            "LtNest": "SPT",
            "Number": "SPT",
            "Chii": "SPT",
            "azue1recker": "SPT"
        },
        "NOTE": "Competed in 2025 OWCS Japan Stage 1 and Stage 3 before disbanding."
    },
    "REJECT": {
        "STAFF": {
            "Undine": "Coach"
        },
        "PLAYERS": {
            "Kalios": "TANK",
            "Edison": "DPS",
            "Undersea": "DPS",
            "Epic": "SPT",
            "Gaisen": "SPT",
            "Ydot": "SPT"
        },
        "NOTE": "Won back-to-back championships in 2025 OWCS Japan Stage 2 and Stage 3. Disbanded Overwatch division following the 2025 season."
    },
    "ZG": {
        "STAFF": {
            "Optimus015": "Coach"
        },
        "PLAYERS": {
            "Xzahyo": "TANK",
            "Water": "DPS",
            "Hop3r": "DPS",
            "GFONAFASK": "DPS",
            "SUZUME": "SPT",
            "BaLLisTa": "SPT",
            "pokotaros": "SPT"
        },
        "NOTE": "Competed in 2025 OWCS Japan Stage 2 before disbanding."
    },
    "Toxic Hamster": {
        "STAFF": {
            "Menh2ra": "Coach",
            "Troy": "Coach",
            "GENESIS": "Manager"
        },
        "PLAYERS": {
            "E1THER": "TANK",
            "Yot1y": "DPS",
            "SORI": "DPS",
            "Kyouchan": "DPS",
            "Amane": "SPT",
            "WGYM": "SPT",
            "eYeKu": "SPT"
        },
        "NOTE": "Competed in 2025 OWCS Japan Stage 3 before disbanding."
    },
    "Lost Never Gaming": {
        "STAFF": {
            "CALD": "Coach",
            "Akirou": "Assistant Coach",
            "Aki": "Manager"
        },
        "PLAYERS": {
            "XLIM": "TANK",
            "Wolf": "DPS",
            "ZEROLKH": "DPS",
            "LtNest": "SPT",
            "Number": "SPT",
            "Chii": "SPT",
            "azue1recker": "SPT"
        },
        "NOTE": "Alias/Duplicate entry for LostNever Gaming; competed in 2025 OWCS Japan Stage 1 and Stage 3."
    },
    "Tokyo Ta1yo's": {
        "STAFF": {
            "KIM": "Coach",
            "Mandu": "Coach",
            "Rexi": "Coach"
        },
        "PLAYERS": {
            "PEPPI": "TANK",
            "Ta1yo": "DPS",
            "ANS": "DPS",
            "Rrmy": "DPS",
            "epic": "SPT",
            "Mihawk": "SPT"
        },
        "NOTE": "Project team founded by ta1yo; finished 2nd in 2026 OWCS Japan Stage 1 before disbanding."
    },

    # =========================================================================
    # OWCS PACIFIC (PA) ACTIVE
    # =========================================================================
    "CantHear": {
        "STAFF": {},
        "PLAYERS": {
            "Yoshinori2k": "TANK",
            "oPuTo": "DPS",
            "Petrichor": "DPS",
            "Kairen": "SPT",
            "PaLee": "SPT",
            "mush2oom": "SPT"
        }
    },
    "Retirement Home": {
        "STAFF": {
            "Scorch": "Coach",
            "Mirgaon": "Coach"
        },
        "PLAYERS": {
            "Yunko": "TANK",
            "Winter": "DPS",
            "SAVEHOPE": "DPS",
            "Ace": "SPT",
            "Abbs": "SPT",
            "Jae": "SPT",
            "lumi": "FLEX"
        }
    },
    "SeijiKing": {
        "STAFF": {},
        "PLAYERS": {
            "Jamorant": "TANK",
            "Kamo": "DPS",
            "HyVision": "DPS",
            "Sp1nel": "SPT",
            "beeple": "SPT",
            "Tavi": "SPT"
        }
    },
    "junjilopzfx0764": {
        "STAFF": {
            "Scorch": "Coach"
        },
        "PLAYERS": {
            "Nanda": "TANK",
            "Bnji": "TANK",
            "TKL": "DPS",
            "QIN": "DPS",
            "Bertlog": "SPT",
            "Huntin": "SPT"
        }
    },

    # =========================================================================
    # OWCS PACIFIC (PA) INACTIVE
    # =========================================================================
    "RTFM": {
        "STAFF": {
            "LnlD": "Coach",
            "JPG": "Manager"
        },
        "PLAYERS": {
            "RULER": "TANK",
            "XIAOLIAN": "DPS",
            "Kurumi": "DPS",
            "MaoLi": "SPT",
            "Ayako": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS Pacific Stage 1, placing 4th before disbanding on March 28, 2024."
    },
    "DAF": {
        "STAFF": {
            "mush2oom": "Coach",
            "rXis": "Manager"
        },
        "PLAYERS": {
            "CLEAR": "TANK",
            "Dank": "TANK",
            "Ace": "DPS",
            "HyVision": "DPS",
            "PaLee": "SPT",
            "TxQ4": "SPT",
            "Lumi": "SPT"
        },
        "NOTE": "Runners-up in 2024 Stage 1. Roster acquired by Bleed Esports in June 2024; reformed in early 2026 before roster acquired by Team Secret on March 25, 2026."
    },
    "Teenage Rising": {
        "STAFF": {},
        "PLAYERS": {
            "KrizV": "TANK",
            "PunMAVERICK": "DPS",
            "Cartiace": "DPS",
            "Phewsofast": "DPS",
            "AnandaS": "SPT",
            "Savier": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS Pacific Stage 1 (7th-8th) and Stage 2 (5th-6th) before disbanding."
    },
    "Fade": {
        "STAFF": {},
        "PLAYERS": {
            "Kairen": "TANK",
            "HYE": "DPS",
            "Exia": "DPS",
            "MSCG": "DPS",
            "Maybe": "SPT",
            "ShakeIt": "SPT"
        },
        "NOTE": "Competed as Fade Altair in 2024 OWCS Pacific Stage 1 and Stage 2 before disbanding."
    },
    "Honeypot": {
        "STAFF": {
            "Joker": "Coach"
        },
        "PLAYERS": {
            "Adam": "TANK",
            "Nyang": "DPS",
            "sgy": "DPS",
            "Lightt": "SPT",
            "Overshake": "SPT"
        },
        "NOTE": "Champions of 2024 OWCS Pacific Stage 1. Disbanded on July 16, 2024, transferring seed/slot to 99DIVINE."
    },
    "Personate Gang": {
        "STAFF": {},
        "PLAYERS": {
            "NDF": "TANK",
            "Ong10": "DPS",
            "KanNY": "DPS",
            "Personate": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS Pacific Stage 1 Open Qualifiers before disbanding."
    },
    "Far East Society": {
        "STAFF": {
            "blueice": "Coach"
        },
        "PLAYERS": {
            "Yunko": "TANK",
            "XP7": "DPS",
            "Tomato": "DPS",
            "Osir1s": "SPT",
            "HAZII": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS Pacific Stage 1 (placed 5th-6th) before disbanding."
    },
    "321 Diving": {
        "STAFF": {
            "Joel": "Coach"
        },
        "PLAYERS": {
            "SeungAn": "TANK",
            "CHONLEE": "DPS",
            "j003": "DPS",
            "PetalS": "DPS",
            "Proxiezs": "DPS",
            "EzClap": "SPT",
            "SPOOK": "SPT"
        },
        "NOTE": "Placed 3rd in 2024 OWCS Pacific Stage 1. Rebranded to Full House on July 29, 2024."
    },
    "Bleed Esports": {
        "STAFF": {
            "rXis": "Head Coach",
            "mush2oom": "Coach"
        },
        "PLAYERS": {
            "SeungAn": "TANK",
            "Ace": "DPS",
            "HVS": "DPS",
            "MAKA": "SPT",
            "PaLee": "SPT",
            "lumi": "SPT"
        },
        "NOTE": "Acquired DAF core in June 2024 and won 2024 OWCS Pacific Stage 2. Disbanded on October 2, 2024."
    },
    "Full House": {
        "STAFF": {
            "Joel": "Coach",
            "Spook": "Manager"
        },
        "PLAYERS": {
            "Yunko": "TANK",
            "Yoshinori2k": "DPS",
            "Arc": "DPS",
            "Joo": "SPT",
            "Univ2r": "SPT",
            "Overshake": "SPT"
        },
        "NOTE": "Formerly 321 Diving (rebranded 2024-07-29). Placed 3rd in 2024 Stage 2 and 3rd-4th in 2025 Stage 2. Disbanded on August 21, 2025."
    },
    "Goon Squad": {
        "STAFF": {},
        "PLAYERS": {
            "TiniValkyrie": "TANK",
            "Yunko": "TANK",
            "QiXMico": "DPS",
            "Hiren": "DPS",
            "Snuwy": "SPT",
            "Revolver": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS Pacific Stage 2, placing 7th-8th before disbanding."
    },
    "Cat": {
        "STAFF": {
            "Mixtape": "Coach",
            "BUTEUK": "Manager"
        },
        "PLAYERS": {
            "Magician": "TANK",
            "Kurumi": "DPS",
            "AV7": "DPS",
            "Proxiezs": "DPS",
            "Dash": "SPT",
            "Rus": "SPT"
        },
        "NOTE": "Active from July 31, 2024 to September 5, 2024. Competed in 2024 OWCS Pacific Stage 2 before disbanding."
    },
    "USIA Esports": {
        "STAFF": {
            "Siphs": "Coach"
        },
        "PLAYERS": {
            "Bearfoo": "TANK",
            "Chako": "DPS",
            "sunset": "DPS",
            "Charm": "DPS",
            "Temper": "DPS",
            "Otakaw": "DPS",
            "b4yadere": "SPT",
            "Juuzou": "SPT"
        },
        "NOTE": "Finished 5th-6th in 2024 OWCS Pacific Stage 2; continued competing in regional qualifiers through 2026."
    },
    "MFC": {
        "STAFF": {},
        "PLAYERS": {
            "Ackyyy": "TANK",
            "Nyang": "DPS",
            "Lightt": "SPT"
        },
        "NOTE": "Formerly Miku Fan Club. Finished runners-up in 2025 OWCS Pacific Stage 1. Disbanded on May 20, 2025, transferring slot to The Gatos Guapos."
    },
    "MENG GONG 2": {
        "STAFF": {},
        "PLAYERS": {
            "Proxy": "TANK",
            "Jamorant": "TANK",
            "Kurumi": "DPS",
            "Mikouw": "DPS",
            "Hop3r": "DPS",
            "CQB": "SPT",
            "Aria": "SPT",
            "Cruncher": "SPT"
        },
        "NOTE": "Placed 3rd-4th in 2025 OWCS Pacific Stage 1 and 7th in Stage 2. Disbanded on March 22, 2026."
    },
    "Antic X Odium": {
        "STAFF": {},
        "PLAYERS": {
            "Lumi": "TANK",
            "revzi": "DPS",
            "Havanah": "DPS",
            "Seqtar": "SPT",
            "Jae": "SPT"
        },
        "NOTE": "Merger of Antic and Odium. Competed in 2025 OWCS Pacific Stage 1 before disbanding."
    },
    "MONSTARGEAR GAMING": {
        "STAFF": {},
        "PLAYERS": {
            "prot3ct": "TANK",
            "speed75": "DPS",
            "Mememachine": "SPT",
            "Dumbbell": "SPT"
        },
        "NOTE": "Competed in 2025 OWCS Pacific Stage 1. Roster released in May 2025 and rebranded as Cold Metal on May 22, 2025."
    },
    "Trap12": {
        "STAFF": {},
        "PLAYERS": {
            "Jamorant": "TANK",
            "Tavi": "TANK",
            "Regr3T": "DPS",
            "Pugz": "SPT",
            "OFF": "SPT",
            "beeple": "SPT",
            "Huntin": "SPT"
        },
        "NOTE": "Competed in 2025 Stage 1 and finished 4th in 2026 OWCS Pacific Stage 2."
    },
    "The Gatos Guapos": {
        "STAFF": {},
        "PLAYERS": {
            "Punk": "TANK",
            "Renaco": "TANK",
            "Colourhex": "DPS",
            "HOYA": "DPS",
            "MCD": "SPT",
            "Ackyyy": "SPT",
            "lumi": "FLEX"
        },
        "NOTE": "Acquired MFC's slot in May 2025 and won 2025 Pacific Stage 2. Roster core acquired by SHENGSHI Esports in 2026."
    },
    "mud dog": {
        "STAFF": {
            "Joel": "Coach",
            "Nozumo": "Manager"
        },
        "PLAYERS": {
            "lumi": "TANK",
            "OLAM": "DPS",
            "kame": "DPS",
            "Jae": "SPT",
            "Seqtar": "SPT"
        },
        "NOTE": "Australian team. Competed in 2025 OWCS Pacific Stage 2 before disbanding."
    },
    "Cold Metal": {
        "STAFF": {
            "IDExpensive": "Manager"
        },
        "PLAYERS": {
            "prot3ct": "TANK",
            "speed75": "DPS",
            "Joo": "DPS",
            "Mememachine": "SPT",
            "Dumbbell": "SPT"
        },
        "NOTE": "Rebranded from MONSTARGEAR GAMING on May 22, 2025. Competed across 2025 Stages 2~3 before slot acquired by UNDEFINED in 2026."
    },
    "FURY": {
        "STAFF": {},
        "PLAYERS": {
            "Scorch": "TANK",
            "sar": "DPS",
            "hamster": "DPS",
            "Hope": "DPS",
            "Exrai": "SPT",
            "Akraken": "SPT"
        },
        "NOTE": "Finished 3rd-4th in 2025 Stages 2 & 3 and 5th in 2026 Stage 1. Roster spot acquired by Dynasty in May 2026."
    },
    "I LOVE YOU": {
        "STAFF": {
            "ALright": "Head Coach"
        },
        "PLAYERS": {
            "Pobi": "TANK",
            "JONGWOO": "DPS",
            "Mikouw": "DPS",
            "Huntin": "SPT"
        },
        "NOTE": "Competed in 2025 OWCS Pacific Stages 2~3 (placing 5th-6th). Officially disbanded on October 3, 2025."
    },
    "Nosebleed Esports": {
        "STAFF": {
            "rXis": "Manager",
            "SPOOK": "Manager"
        },
        "PLAYERS": {
            "CLEAR": "TANK",
            "Gilly": "TANK",
            "HyVision": "DPS",
            "Bun": "DPS",
            "Kame": "SPT",
            "PaLee": "SPT",
            "MSCG": "SPT"
        },
        "NOTE": "Champions of 2025 OWCS Pacific Stage 3. Disbanded on February 24, 2026, transferring slot and core to DAF (later Team Secret)."
    },
    "Stronghold": {
        "STAFF": {},
        "PLAYERS": {
            "lumi": "TANK",
            "Poszum": "DPS",
            "kame": "DPS",
            "Netra": "SPT",
            "Jae": "SPT"
        },
        "NOTE": "New Zealand team. Placed 7th in 2025 OWCS Pacific Stage 3 and 4th in 2026 Stage 1 Open Qualifiers."
    },
    "INVADERS": {
        "STAFF": {
            "Optimus015": "Coach",
            "DZX23S": "Manager"
        },
        "PLAYERS": {
            "Jamorant": "TANK",
            "F1nally": "DPS",
            "Kurumi": "DPS",
            "TARO": "SPT",
            "Snuwy": "SPT"
        },
        "NOTE": "Placed 3rd-4th in 2025 OWCS Pacific Stage 3. Roster slot acquired by MMY in 2026."
    },
    "NewGens": {
        "STAFF": {},
        "PLAYERS": {
            "Prot3ct": "TANK",
            "Seatonnes": "TANK",
            "JXI": "DPS",
            "M00N": "SPT"
        },
        "NOTE": "Competed in 2025 OWCS Pacific Stage 3 before disbanding on October 25, 2025."
    },
    "Team Secret": {
        "STAFF": {
            "mush2oom": "Coach",
            "rXis": "Manager"
        },
        "PLAYERS": {
            "cuFFa": "TANK",
            "sgy": "DPS",
            "Yoshinori2k": "DPS",
            "Akame": "DPS",
            "PaLee": "SPT"
        },
        "NOTE": "Acquired DAF roster in March 2026. Finished runners-up in 2026 Stage 1 and won 2026 Pacific Stage 2 championship."
    },
    "MMY": {
        "STAFF": {},
        "PLAYERS": {
            "Kairen": "TANK",
            "sunset": "DPS",
            "Flos": "DPS",
            "MSCG": "SPT"
        },
        "NOTE": "Acquired INVADERS' Pacific slot. Competed in 2026 OWCS Pacific Stage 1, placing 6th."
    },
    "Rankers": {
        "STAFF": {
            "Detai1": "Coach"
        },
        "PLAYERS": {
            "FEEL1NG": "TANK",
            "Despair": "TANK",
            "Zephyr": "DPS",
            "brysonbtw": "DPS",
            "Amamiyaren": "SPT",
            "FEI": "SPT"
        },
        "NOTE": "Placed 3rd in 2026 OWCS Pacific Stage 1. Roster core acquired by Najdorf Esports in May 2026."
    },
    "Quasar Esports": {
        "STAFF": {},
        "PLAYERS": {
            "Jamorant": "TANK",
            "Lumi": "TANK",
            "TKL": "DPS",
            "Yoko": "DPS",
            "Beeple": "SPT",
            "Huntin": "SPT"
        },
        "NOTE": "Competed in 2026 OWCS Pacific Stage 1, finishing in 4th place."
    },
    "MENG GONG 3": {
        "STAFF": {
            "EmolGa": "Coach"
        },
        "PLAYERS": {
            "Pobi": "TANK",
            "Bearfoo": "TANK",
            "Kurumi": "DPS",
            "Despair": "DPS",
            "Aria": "DPS",
            "ManGoJai": "SPT"
        },
        "NOTE": "Competed in 2026 OWCS Pacific Stage 2 Regular Season."
    },
    "ELMT": {
        "STAFF": {
            "KIM": "Coach"
        },
        "PLAYERS": {
            "AlbertDryWall": "TANK",
            "fed": "DPS",
            "tkl": "DPS",
            "QIN": "DPS",
            "bnji": "SPT",
            "Bertlog": "SPT",
            "Hamster": "SPT"
        },
        "NOTE": "Finished 5th in 2026 OWCS Pacific Stage 2. Roster core continued under junjilopzfx0764 after August 2026."
    },
    "Najdorf": {
        "STAFF": {
            "Detai1": "Coach"
        },
        "PLAYERS": {
            "Akie": "TANK",
            "brysonbtw": "DPS",
            "Zephyr": "DPS",
            "FEI": "SPT",
            "Amamiyaren": "SPT"
        },
        "NOTE": "Acquired Rankers' roster core in May 2026. Finished 3rd in 2026 OWCS Pacific Stage 2."
    },

    # =========================================================================
    # OWCS CHINA (CN) ACTIVE
    # =========================================================================
    "SHENGSHI": {
        "STAFF": {
            "Troyda": "Coach",
            "Fuhu": "Coach",
            "NoX": "Manager",
            "Renaco": "Manager"
        },
        "PLAYERS": {
            "Gur3um": "TANK",
            "Punk": "TANK",
            "Colourhex": "DPS",
            "HOYA": "DPS",
            "sai": "SPT",
            "MCD": "SPT"
        }
    },
    "JD Gaming": {
        "STAFF": {
            "soo": "Coach"
        },
        "PLAYERS": {
            "Roxy": "TANK",
            "Kaneki": "DPS",
            "Prophet": "DPS",
            "Farway1987": "SPT",
            "HaoYoqian": "SPT"
        }
    },
    "All Gamers": {
        "STAFF": {
            "GA9A": "Coach",
            "Dreamer": "Assistant Coach",
            "YoungJin": "Manager"
        },
        "PLAYERS": {
            "Mag": "TANK",
            "GA9A": "TANK",
            "Ezhan": "DPS",
            "Alphari": "DPS",
            "Lengsa": "SPT",
            "Recall": "SPT"
        }
    },
    "Solus Victorem": {
        "STAFF": {},
        "PLAYERS": {
            "prot3ct": "TANK",
            "Apr1ta": "DPS",
            "BABAYAGA": "DPS",
            "Unkn0w": "SPT"
        }
    },
    "Weibo Gaming": {
        "STAFF": {
            "Daemin": "Coach",
            "YangXiaoLong": "Coach"
        },
        "PLAYERS": {
            "Guxue": "TANK",
            "Sunzo": "TANK",
            "Leave": "DPS",
            "shy": "DPS",
            "LeeSooMin": "SPT",
            "MAKA": "SPT"
        }
    },
    "OU Gaming": {
        "STAFF": {
            "Lori": "Coach",
            "Linabell": "Assistant Coach",
            "Ahty": "Analyst",
            "Jiangdong": "Manager"
        },
        "PLAYERS": {
            "Decade": "TANK",
            "Odium": "TANK",
            "Pride": "DPS",
            "Victoria": "DPS",
            "Insane": "DPS",
            "Damo": "SPT",
            "Ir1s": "SPT"
        }
    },
    "HUNENG": {
        "STAFF": {
            "Gyomin": "Coach"
        },
        "PLAYERS": {
            "DuFan": "TANK",
            "SeungAn": "TANK",
            "GhostShadow": "DPS",
            "A1WAYS": "SPT",
            "Amamiyaren": "SPT"
        }
    },
    "Black Flag": {
        "STAFF": {},
        "PLAYERS": {
            "suna": "TANK",
            "agayabab": "TANK",
            "Ripples": "DPS",
            "Rockclimb": "DPS",
            "Sa1nt": "SPT",
            "Moon1ightT": "SPT",
            "Hypnos": "SPT"
        }
    },

    # =========================================================================
    # OWCS CHINA (CN) INACTIVE
    # =========================================================================
    "Once Again": {
        "STAFF": {
            "Daemin": "Coach",
            "Dongsu": "Coach"
        },
        "PLAYERS": {
            "Guxue": "TANK",
            "Leave": "DPS",
            "shy": "DPS",
            "Lengsa": "SPT",
            "Mmonk": "SPT"
        },
        "NOTE": "Formed by former Hangzhou Spark/Team China core. Placed 2nd at 2024 OWCS Dallas Major and 3rd at EWC 2024. Roster acquired by Weibo Gaming on April 30, 2025."
    },
    "ROC Esports": {
        "STAFF": {
            "KariV": "Coach",
            "FITS": "Coach",
            "Linabell": "Coach",
            "Cointree": "Assistant Coach",
            "YoungJin": "Manager",
            "Lotsha": "Manager"
        },
        "PLAYERS": {
            "Belosrea": "TANK",
            "Flora": "DPS",
            "JinMu": "DPS",
            "Lilko": "DPS",
            "Lengsa": "SPT",
            "Molly": "SPT"
        },
        "NOTE": "Competed across EMEA (2024) and moved to China (2025). Disbanded on 2025-10-11 after 2025 OWCS CN Stage 3."
    },
    "Blade": {
        "STAFF": {
            "currentRR": "Coach"
        },
        "PLAYERS": {
            "Wen": "TANK",
            "Fari": "DPS",
            "Pride": "DPS",
            "NuoRan": "SPT",
            "Remedy": "SPT"
        },
        "NOTE": "Competed in 2025 OWCS China Stage 1, placing 5th-6th before disbanding."
    },
    "Super Levi": {
        "STAFF": {},
        "PLAYERS": {
            "Keios": "TANK",
            "Jimmy": "DPS",
            "Jeremy": "DPS",
            "Amamiyaren": "SPT",
            "Tamper": "SPT"
        },
        "NOTE": "Competed in 2025 OWCS China Stage 1 (placed 7th-8th) before disbanding."
    },
    "Little Sheep": {
        "STAFF": {},
        "PLAYERS": {
            "Wh4le": "TANK",
            "Remefer": "DPS",
            "Kim": "DPS",
            "Kusari": "SPT",
            "Hypnos": "SPT",
            "DMS": "SPT"
        },
        "NOTE": "Competed in 2025 OWCS China Stage 1 (placed 4th) and Stage 2 before disbanding."
    },
    "Team CC": {
        "STAFF": {
            "LnlD": "Coach"
        },
        "PLAYERS": {
            "Guxue": "TANK",
            "LiGe": "TANK",
            "Kaneki": "DPS",
            "Mmonk": "SPT",
            "Mew": "SPT"
        },
        "NOTE": "Former Shanghai Dragons academy team. Finished runners-up in 2025 OWCS China Stage 1 and Stage 3. Disbanded on February 1, 2026."
    },
    "Team XX": {
        "STAFF": {
            "KingDebu": "Coach",
            "Genius91": "Manager"
        },
        "PLAYERS": {
            "Genius91": "TANK",
            "Decade": "TANK",
            "Pity": "DPS",
            "Lilko": "DPS",
            "ProYung": "SPT"
        },
        "NOTE": "Formed in August 2024. Placed 5th-6th in 2025 OWCS China Stage 1 before disbanding."
    },
    "Team Equal": {
        "STAFF": {},
        "PLAYERS": {
            "M0CHA": "TANK",
            "EmolGa": "DPS",
            "Flicker": "DPS",
            "TCC": "DPS",
            "Twe12e": "SPT",
            "Ketto": "SPT",
            "Lavender": "SPT"
        },
        "NOTE": "Competed in 2025 OWCS China Stage 1 (placed 7th-8th) under Team Equal before rebranding to Solus Victorem."
    },
    "Homie E": {
        "STAFF": {
            "LnlD": "Coach",
            "MightyLord": "Manager"
        },
        "PLAYERS": {
            "Wen": "TANK",
            "faaaariii": "DPS",
            "pOv": "DPS",
            "Remedy": "SPT",
            "Mashiro": "SPT"
        },
        "NOTE": "Formerly Home E. Placed 7th-8th in 2026 OWCS China Stage 1 before disbanding."
    },
    "ZONES": {
        "STAFF": {
            "Ask": "Manager"
        },
        "PLAYERS": {
            "Wen": "TANK",
            "Lilko": "TANK",
            "SeaWave": "DPS",
            "tengyuan": "DPS",
            "Aiden": "SPT",
            "Unkn0w": "SPT"
        },
        "NOTE": "Competed across 2025 OWCS China Stages 1~2."
    },
    "Milk Tea": {
        "STAFF": {},
        "PLAYERS": {
            "R3K": "TANK",
            "Wen": "TANK",
            "Insane": "DPS",
            "Recall": "SPT"
        },
        "NOTE": "Formed on April 27, 2025. Finished 3rd in 2025 OWCS China Stage 3. Disbanded on April 29, 2026."
    },
    "YNB Esports": {
        "STAFF": {},
        "PLAYERS": {
            "Odium": "TANK",
            "Wen": "TANK",
            "Alphari": "DPS",
            "Sara": "SPT",
            "BLX": "SPT"
        },
        "NOTE": "Placed 4th in 2025 OWCS China Stage 3. Officially disbanded on February 13, 2026."
    },
    "boom": {
        "STAFF": {},
        "PLAYERS": {
            "feiyang": "TANK",
            "Pride": "DPS",
            "Molly": "SPT",
            "DMS": "SPT"
        },
        "NOTE": "Smash Boom. Won Baihe Championship 2026 and qualified for 2026 OWCS China Stage 2 before disbanding."
    },
    "MDY": {
        "STAFF": {},
        "PLAYERS": {
            "Eaglet": "TANK",
            "Bigdevi1": "DPS",
            "Keios": "DPS",
            "verde": "SPT"
        },
        "NOTE": "Formerly CNOW的希望 (Mei Dui Yao). Competed in 2025 OWCS China Stage 3 and 2026 OWCS China Stage 1 Open Qualifiers before disbanding."
    },
    "DEG": {
        "STAFF": {
            "Kano": "Coach"
        },
        "PLAYERS": {
            "wh4le": "TANK",
            "Lateyoung": "TANK",
            "Wangming": "DPS",
            "JAYA": "DPS",
            "skyshow": "DPS",
            "sara": "SPT",
            "Coldj": "SPT"
        },
        "NOTE": "Streamer team. Competed in 2026 OWCS China Stage 1 before disbanding."
    },
    "Naive Piggy": {
        "STAFF": {},
        "PLAYERS": {
            "LateYoung": "TANK",
            "Wh4le": "DPS",
            "JAYA": "DPS",
            "Coldj": "SPT",
            "Sara": "SPT"
        },
        "NOTE": "Competed in 2026 OWCS China Stage 1 (placed 5th). Formed by veteran CNOW players after winning the 2025 Tianzhen Cup."
    },
    "4AM": {
        "STAFF": {},
        "PLAYERS": {
            "Odium": "TANK",
            "Lilko": "DPS",
            "Setsuna": "DPS",
            "Sa1nt": "SPT",
            "Hypnos": "SPT"
        },
        "NOTE": "Four Angry Men. Competed in 2026 OWCS China Stage 2 (placing 6th) before disbanding."
    },
    "ReturnZ": {
        "STAFF": {
            "Optimus015": "Coach"
        },
        "PLAYERS": {
            "suna": "TANK",
            "Decade": "TANK",
            "Kouzi": "DPS",
            "asphy": "DPS",
            "honeycombo": "SPT"
        },
        "NOTE": "Competed in 2026 OWCS China Stage 2."
    },
    "Kitsune Kage": {
        "STAFF": {
            "Kakitsubata": "Coach"
        },
        "PLAYERS": {
            "Ringleader": "TANK",
            "logan": "DPS",
            "dosoldier": "DPS",
            "LazYYanG": "DPS",
            "ripples": "DPS",
            "Soyo": "SPT",
            "Kakitsubata": "SPT"
        },
        "NOTE": "Formerly Team KK (rebranded on May 29, 2026). Competed in 2026 OWCS China Stage 2."
    },

    # =========================================================================
    # OWCS NORTH AMERICA (NA) ACTIVE
    # =========================================================================
    # =========================================================================
    # OWCS NORTH AMERICA (NA) ACTIVE
    # =========================================================================
    "Spacestation Gaming": {
        "STAFF": {
            "ChrisTFer": "Head Coach",
            "Artemis": "Manager"
        },
        "PLAYERS": {
            "Hawk": "TANK",
            "RhynO": "TANK",
            "Sugarfree": "DPS",
            "Lethal": "DPS",
            "scissors": "DPS",
            "Admiral": "SPT"
        }
    },
    "Dallas Fuel": {
        "STAFF": {
            "Wheats": "Head Coach",
            "Yong": "Coach"
        },
        "PLAYERS": {
            "Kellan": "TANK",
            "SeonJun": "DPS",
            "Kronik": "DPS",
            "Cjay": "SPT",
            "Lukemino": "SPT"
        }
    },
    "disguised": {
        "STAFF": {
            "ByZenith": "Head Coach",
            "Capitology": "Coach",
            "McGravy": "Coach",
            "Zei": "Coach"
        },
        "PLAYERS": {
            "Tred": "TANK",
            "PGE": "DPS",
            "Rokit": "DPS",
            "KiWii": "SPT",
            "Scyle": "SPT"
        }
    },
    "Team Liquid": {
        "STAFF": {
            "Casores": "Head Coach",
            "Danny": "Coach",
            "F4zE": "Coach"
        },
        "PLAYERS": {
            "Attack": "TANK",
            "TR33": "DPS",
            "zeruhh": "DPS",
            "Vega": "SPT",
            "KIVIS": "SPT"
        }
    },
    "NTMR": {
        "STAFF": {
            "Urzo": "Manager"
        },
        "PLAYERS": {
            "Painkiller": "TANK",
            "iCy": "TANK",
            "JUTSU": "DPS",
            "peace": "DPS",
            "Wybie": "SPT",
            "Virtual": "SPT",
            "Rep": "SPT"
        },
        "NOTE": "Won FACEIT League Season 9 - NA Master and OWCS 2026 NA Stage 2 Promotion/Relegation to secure OWCS NA Stage 3 spot."
    },

    # =========================================================================
    # OWCS NORTH AMERICA (NA) INACTIVE
    # =========================================================================
    "Toronto Defiant": {
        "STAFF": {
            "Casores": "Head Coach",
            "Danny": "Analyst",
            "Lovell": "General Manager"
        },
        "PLAYERS": {
            "SOMEONE": "TANK",
            "MER1T": "DPS",
            "Sugarfree": "DPS",
            "Rupal": "SPT",
            "Vega": "SPT"
        },
        "NOTE": "Won all 4 NA stages in 2024 (competed as Toronto Ultra at 2024 EWC). Officially disbanded on 2024-12-11 following 2024 OWCS World Finals Stockholm."
    },
    "LFO": {
        "STAFF": {
            "SNR": "Head Coach",
            "Algos05": "Assistant Coach"
        },
        "PLAYERS": {
            "MirroR": "TANK",
            "Seeker": "DPS",
            "TOPDRAGON": "DPS",
            "zeruhh": "DPS",
            "Lyar": "SPT",
            "MCD": "SPT",
            "McGravy": "SPT"
        },
        "NOTE": "Originally formed as WD40 (rebranded to LFO on 2024-03-07). Placed 5th-6th in 2024 OWCS NA Stage 1 before disbanding."
    },
    "Timeless": {
        "STAFF": {
            "ThatAFKNoob": "Manager"
        },
        "PLAYERS": {
            "cuFFa": "TANK",
            "Doomed": "DPS",
            "squid": "DPS",
            "Lukemino": "SPT",
            "Vision": "SPT"
        },
        "NOTE": "Placed 2nd in 2024 OWCS NA Stage 1 before roster was acquired by TSM. Later acquired Anomaly for Stage 3 before ceasing operations in late 2024."
    },
    "Beluga's Platoon": {
        "STAFF": {
            "Trysome": "Head Coach"
        },
        "PLAYERS": {
            "sawhill": "TANK",
            "Snozlar": "DPS",
            "Tristan": "DPS",
            "Shaq": "SPT",
            "Bun": "SPT",
            "Halo": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS NA Stage 1 Group Stage (Group D). Disbanded post-tournament."
    },
    "Students of the Game": {
        "STAFF": {
            "Wheats": "Coach"
        },
        "PLAYERS": {
            "Infekted": "TANK",
            "MirroR": "TANK",
            "PGE": "DPS",
            "scissors": "DPS",
            "cal": "SPT",
            "Rakattack": "SPT"
        },
        "NOTE": "Formed on 2024-03-04. Qualified for 2024 OWCS Dallas Major as an unsigned team. Acquired by NRG Esports on 2024-05-31 to compete as NRG Shock."
    },
    "M80": {
        "STAFF": {
            "Faust": "Head Coach"
        },
        "PLAYERS": {
            "Coluge": "TANK",
            "Spectra": "DPS",
            "TR33": "DPS",
            "UltraViolet": "SPT",
            "Lyar": "SPT"
        },
        "NOTE": "Competed at 2024 Dallas Major (top 6) and Esports World Cup 2024. Disbanded in August 2024 after key players transferred to NRG Shock."
    },
    "Luminosity Gaming": {
        "STAFF": {},
        "PLAYERS": {
            "Danteh": "TANK",
            "False": "TANK",
            "k1ng": "DPS",
            "Vision": "DPS",
            "Lukemino": "SPT",
            "squid": "SPT",
            "Joobi": "SPT"
        },
        "NOTE": "Collegiate partnership with Maryville University formed on 2024-03-06. Placed 4th in 2024 OWCS NA Stage 1. Disbanded on 2024-07-15."
    },
    "Daybreak": {
        "STAFF": {
            "Maeve": "Coach"
        },
        "PLAYERS": {
            "Hutch": "TANK",
            "JUTSU": "DPS",
            "Faded": "DPS",
            "Putter": "DPS",
            "Abyss": "SPT",
            "NightKnight": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS NA Stage 1 Group Stage (Group A) and Stage 2 Qualifiers before disbanding."
    },
    "Shikigami": {
        "STAFF": {
            "Fleta": "Coach",
            "April": "Manager"
        },
        "PLAYERS": {
            "Dantwist": "TANK",
            "SeonJun": "DPS",
            "Taejong": "DPS",
            "Aspect": "DPS",
            "Graveyard": "SPT",
            "Noctis": "SPT"
        },
        "NOTE": "Competed across OWCS 2024 NA Stages 1-4 (placed 7th-8th in Stage 4). Officially disbanded on 2026-04-12."
    },
    "BangBangPow Galaxy": {
        "STAFF": {},
        "PLAYERS": {
            "Krawi": "TANK",
            "NOS": "DPS",
            "pink": "DPS",
            "Paintbrush": "SPT",
            "FishCake": "SPT",
            "Haven": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS NA Stage 1 Group Stage (Group C). Disbanded post-tournament."
    },
    "Nah I'd Win": {
        "STAFF": {},
        "PLAYERS": {},
        "NOTE": "Unsigned amateur roster that qualified through Swiss Stage to compete in 2024 OWCS NA Stage 1 Group Stage (Group C, finished 0-2). Disbanded post-tournament."
    },
    "Pirates in Pyjamas": {
        "STAFF": {},
        "PLAYERS": {
            "Hing3d": "TANK",
            "Divinity": "DPS",
            "Taejong": "DPS",
            "Aniyun": "SPT",
            "MagicM8Ball": "SPT"
        },
        "NOTE": "Placed top 6 in 2024 OWCS NA Stage 1. Disbanded on 2024-08-09 prior to Stage 3 due to roster departures."
    },
    "Dreamland": {
        "STAFF": {
            "chime": "Manager"
        },
        "PLAYERS": {
            "RhynO": "TANK",
            "chime": "DPS",
            "Manually": "DPS",
            "Divinity": "SPT",
            "Shikigami": "SPT"
        },
        "NOTE": "Formed on 2024-03-01. Acquired by FLUFFY AIMERS on 2024-05-22, returned to Dreamland in late 2024, won FACEIT League S5 Master, disbanded on 2026-06-19."
    },
    "Timeless Obsidian": {
        "STAFF": {
            "Tokki": "Coach"
        },
        "PLAYERS": {
            "Tred": "TANK",
            "Dynasty": "DPS",
            "Dove": "DPS",
            "Sloth": "SPT",
            "Hcpeful": "SPT"
        },
        "NOTE": "Academy/secondary team for Timeless. Competed in 2024 OWCS NA Stage 1 Group Stage (Group C) before disbanding."
    },
    "Citrus Nation": {
        "STAFF": {},
        "PLAYERS": {
            "Zeb": "TANK",
            "TAP": "DPS",
            "Lethal": "DPS",
            "durpee": "SPT",
            "Lep": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS NA Stage 1 & 2. Acquired by NTMR in June 2024 to compete as Citrus Nightmare. Disbanded on 2025-01-17."
    },
    "Final Gambit": {
        "STAFF": {},
        "PLAYERS": {
            "Eve": "DPS",
            "Passenger": "SPT",
            "muhiki": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS NA Stage 1 Group Stage (Group A) and FACEIT League S1 NA Expert. Disbanded post-tournament."
    },
    "Vice": {
        "STAFF": {
            "Domlyy": "Head Coach",
            "Maeve": "Coach",
            "STRIKE": "Assistant Coach"
        },
        "PLAYERS": {
            "Axure": "TANK",
            "JUTSU": "DPS",
            "Rymazing": "DPS",
            "Hing3d": "SPT",
            "Salmon": "SPT"
        },
        "NOTE": "Formed on 2024-04-05. Acquired entirely by YFP Gaming on 2024-09-20."
    },
    "FMCL": {
        "STAFF": {
            "LnID": "Coach"
        },
        "PLAYERS": {
            "Infekted": "TANK",
            "Seeker": "DPS",
            "TR33": "DPS",
            "Admiral": "SPT",
            "Lep": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS NA Stage 2. Roster acquired by Timeless on 2024-06-14 for FACEIT League Season 1 Master Playoffs."
    },
    "DhillDucks": {
        "STAFF": {
            "zhulander": "Coach"
        },
        "PLAYERS": {
            "Krawi": "TANK",
            "Karmez": "DPS",
            "Reyzr": "DPS",
            "FrothyFilly7": "SPT",
            "Redex": "SPT"
        },
        "NOTE": "Competed in 2024–2025 OWCS NA stages and FACEIT League. Also hosted community tournaments including DhillVitational."
    },
    "Visored": {
        "STAFF": {
            "Ocie": "Coach",
            "ThatAFKNoob": "Manager"
        },
        "PLAYERS": {
            "Lava": "TANK",
            "Amadien": "DPS",
            "Lampent": "DPS",
            "karmez": "DPS",
            "TwoFish": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS NA Stage 2 Group Stage. Rebranded to Good Boys before disbanding on 2024-12-09."
    },
    "Nightmare Rotation": {
        "STAFF": {
            "Hogz": "Coach",
            "Aeroplayne": "Manager"
        },
        "PLAYERS": {
            "dust": "TANK",
            "Bizz": "DPS",
            "azruf": "DPS",
            "GoldFish": "SPT",
            "reverse": "SPT",
            "debit": "SPT"
        },
        "NOTE": "Original team formed in late 2023. Competed in 2024 OWCS NA Stage 2. Rebranded to NTMR on 2024-06-21."
    },
    "UNC INC": {
        "STAFF": {
            "ThatAFKNoob": "Manager"
        },
        "PLAYERS": {
            "Painkiller": "TANK",
            "peace": "DPS",
            "Ryan": "DPS",
            "Haven": "DPS",
            "Hanbei": "SPT",
            "Paintbrush": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS NA Stage 2. Officially rebranded to Team Z on 2024-07-16."
    },
    "Who Is Goldfish": {
        "STAFF": {},
        "PLAYERS": {
            "dust": "TANK",
            "azruf": "DPS",
            "Bizz": "DPS",
            "Tristan": "DPS",
            "reverse": "SPT",
            "Shaq": "SPT",
            "Yimitra": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS NA Stage 2 Swiss/Qualifiers. Predecessor/sister roster associated with Nightmare Rotation."
    },
    "NRG Shock": {
        "STAFF": {
            "Wheats": "Coach",
            "yeHHH": "General Manager",
            "clicky": "Manager"
        },
        "PLAYERS": {
            "Kellan": "TANK",
            "Attack": "TANK",
            "TR33": "DPS",
            "PGE": "DPS",
            "UltraViolet": "SPT",
            "Rakattack": "SPT"
        },
        "NOTE": "Formed on 2024-05-31 via acquisition of Students of the Game. Placed 4th at 2024 OWCS World Finals Stockholm. Disbanded on 2024-12-18."
    },
    "Citrus Nightmare": {
        "STAFF": {},
        "PLAYERS": {
            "Zeb": "TANK",
            "TAP": "DPS",
            "Lethal": "DPS",
            "durpee": "SPT",
            "Lep": "SPT"
        },
        "NOTE": "Formed in June 2024 as a joint project when NTMR acquired Citrus Nation for FACEIT League Season 1 Masters. Reverted back to Citrus Nation post-tournament."
    },
    "TSM": {
        "STAFF": {
            "Cap": "Head Coach",
            "Faustus": "Assistant Coach",
            "Tensa": "Assistant Coach"
        },
        "PLAYERS": {
            "iCy": "TANK",
            "Raikker": "TANK",
            "Rokit": "DPS",
            "k1ng": "DPS",
            "Lep": "SPT",
            "Renko": "SPT"
        },
        "NOTE": "Re-entered Overwatch on 2024-05-01 by signing Timeless roster. Placed 2nd in FACEIT League Season 2 NA Master. Disbanded on 2024-10-16."
    },
    "Avidity": {
        "STAFF": {},
        "PLAYERS": {
            "pela": "TANK",
            "azruf": "DPS",
            "scuffed": "SPT",
            "Hanbei": "SPT"
        },
        "NOTE": "Competed in 2024–2025 OWCS NA circuit and Calling All Heroes. Partnered with Rad Esports as Rad x Avidity for 2024 Stage 4."
    },
    "Timeless Ethereal": {
        "STAFF": {},
        "PLAYERS": {
            "Haven": "TANK",
            "wsps": "DPS",
            "Melophobia": "DPS",
            "Sloth": "SPT",
            "Karasu": "SPT"
        },
        "NOTE": "Formed on 2022-11-18. Competitive roster for Calling All Heroes and OWCS NA qualifiers. Disbanded on 2025-05-07."
    },
    "Arizona State": {
        "STAFF": {
            "h2dr0gen": "Head Coach",
            "Maji": "Manager"
        },
        "PLAYERS": {
            "PROJEK": "TANK",
            "Anhoo": "DPS",
            "Jman": "DPS",
            "Scylla": "SPT",
            "Anghell1c": "SPT"
        },
        "NOTE": "Collegiate varsity esports program for Arizona State University. Won 2024 Western Cactus League and competed in 2024 OWCS NA Stage 3 / 2025 Stage 1 Open Qualifier."
    },
    "FLUFFY AIMERS": {
        "STAFF": {},
        "PLAYERS": {
            "RhynO": "TANK",
            "Ryan": "DPS",
            "Manually": "DPS",
            "Divinity": "SPT",
            "Shikigami": "SPT"
        },
        "NOTE": "Competed in OWCS 2024 NA Stage 3 & Stage 4 as 'Fluffy Dreamland' (upset NRG Shock in Stage 4). Ceased all operations on 2024-12-11."
    },
    "Fries In The Bag": {
        "STAFF": {
            "zhulander": "Coach"
        },
        "PLAYERS": {
            "dust": "TANK",
            "Bizz": "DPS",
            "NOS": "DPS",
            "Shaq": "SPT",
            "Aniyun": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS NA Stage 3. Disbanded post-tournament."
    },
    "Team Z": {
        "STAFF": {
            "ThatAFKNoob": "Manager"
        },
        "PLAYERS": {
            "Painkiller": "TANK",
            "peace": "DPS",
            "Talisman": "DPS",
            "Excal": "DPS",
            "Hanbei": "SPT",
            "lenn": "SPT"
        },
        "NOTE": "Formerly UNC INC (rebranded on 2024-07-16). Competed in FACEIT League and 2024–2025 NA qualifiers before disbanding in late 2025."
    },
    "Tanuki Esports": {
        "STAFF": {
            "Izzy": "Manager"
        },
        "PLAYERS": {
            "Passenger": "TANK",
            "Narwhal": "DPS",
            "azruf": "DPS",
            "TwoFish": "SPT"
        },
        "NOTE": "Competed in 2024–2025 NA qualifiers and FACEIT League."
    },
    "Absolution": {
        "STAFF": {
            "jVenom": "Coach"
        },
        "PLAYERS": {
            "MonkeyHappy": "TANK",
            "Soulsay": "DPS",
            "KiWii": "SPT",
            "cinnabar": "SPT"
        },
        "NOTE": "Competed in OWCS 2024 NA Stage 4 and FACEIT League."
    },
    "O3 Splash": {
        "STAFF": {},
        "PLAYERS": {
            "Pummy": "TANK",
            "JUTSU": "DPS",
            "K41": "DPS",
            "Aeko": "SPT"
        },
        "NOTE": "Competed in Contenders and 2024–2025 NA qualifiers / FACEIT League."
    },
    "Tanuki Tapire": {
        "STAFF": {
            "Izzy": "Manager"
        },
        "PLAYERS": {
            "Passenger": "TANK",
            "Narwhal": "DPS",
            "azruf": "DPS",
            "TwoFish": "SPT"
        },
        "NOTE": "Academy/secondary roster for Tanuki Esports in 2024. Merged into main Tanuki Esports roster in January 2025."
    },
    "EXN Zenith": {
        "STAFF": {},
        "PLAYERS": {
            "Passenger": "TANK",
            "Narwhal": "DPS",
            "Meman": "DPS",
            "Cyber": "SPT",
            "Thunder": "SPT"
        },
        "NOTE": "Division/roster of Extinction (EXN) that competed in 2024 OWCS NA qualifiers and FACEIT events."
    },
    "Rammatra Punch": {
        "STAFF": {},
        "PLAYERS": {
            "IqMighty": "TANK",
            "Floomfie": "DPS",
            "Salmon": "SPT"
        },
        "NOTE": "Competed in OWCS 2024 NA Stage 4 Group Stage (Group C) and FACEIT League S3 NA Master."
    },
    "Rad X Avidity": {
        "STAFF": {},
        "PLAYERS": {
            "pela": "TANK",
            "azruf": "DPS",
            "scuffed": "SPT"
        },
        "NOTE": "Joint partnership between Rad Esports and Avidity for OWCS 2024 NA Stage 4. Disbanded on 2025-01-15."
    },
    "Blast Off Buds": {
        "STAFF": {},
        "PLAYERS": {
            "Lava": "TANK",
            "dust": "TANK",
            "Emmeryn": "DPS",
            "Eve": "DPS",
            "v1ctory": "SPT",
            "FrothyFilly7": "SPT"
        },
        "NOTE": "Competed in OWCS 2024 NA Stage 4 (placed 9th-12th). Disbanded post-tournament."
    },
    "YFP Gaming": {
        "STAFF": {
            "Domlyy": "Head Coach",
            "STRIKE": "Coach"
        },
        "PLAYERS": {
            "Axure": "TANK",
            "JUTSU": "DPS",
            "Rymazing": "DPS",
            "Hing3d": "SPT",
            "Salmon": "SPT"
        },
        "NOTE": "Competed in 2024 NA Stage 1, disbanded, returned on 2024-09-20 by acquiring the Vice roster for OWCS NA Stage 4."
    },
    "Rad Esports": {
        "STAFF": {},
        "PLAYERS": {
            "pela": "TANK",
            "azruf": "DPS",
            "scuffed": "SPT"
        },
        "NOTE": "Independent NA organization that competed in OWCS and FACEIT League before disbanding in May 2025."
    },
    "Amplify": {
        "STAFF": {
            "Envidia": "Manager"
        },
        "PLAYERS": {
            "GAP": "TANK",
            "Santana": "TANK",
            "Kabe": "DPS",
            "KriGD": "DPS",
            "Crumb": "SPT",
            "Ewan": "SPT"
        },
        "NOTE": "Competed in OWCS 2024–2026 NA circuits and FACEIT League."
    },
    "Extinction": {
        "STAFF": {},
        "PLAYERS": {
            "Painkiller": "TANK",
            "Passenger": "TANK",
            "Narwhal": "DPS",
            "Karmez": "DPS",
            "Cyber": "SPT",
            "Thunder": "SPT"
        },
        "NOTE": "North American esports organization founded in August 2024. Placed 2nd in FACEIT League Season 9 - NA Master (Grand Finals vs NTMR)."
    },
    "Sakura Esports": {
        "STAFF": {},
        "PLAYERS": {
            "Zeb": "TANK",
            "xomba": "DPS",
            "xten": "SPT"
        },
        "NOTE": "Re-entered Overwatch on 2024-05-10. Placed 4th in 2025 OWCS NA Stage 3 (upset NTMR). Disbanded on 2026-02-28, with core players moving to LuneX Gaming."
    },
    "Supernova": {
        "STAFF": {},
        "PLAYERS": {
            "Alex": "TANK",
            "Juice": "TANK",
            "Ryan": "DPS",
            "JUTSU": "DPS",
            "Karmez": "SPT"
        },
        "NOTE": "Active from 2025-01-16 to 2025-09-10. Competed in 2025 OWCS NA Stage 1 & Stage 2 (and Promotion/Relegation)."
    },
    "LuneX Gaming": {
        "STAFF": {},
        "PLAYERS": {
            "Zeb": "TANK",
            "xomba": "DPS",
            "NenWhy": "DPS",
            "xten": "SPT",
            "zzz": "SPT"
        },
        "NOTE": "Competed in 2026 OWCS NA stages (featuring ex-Sakura Esports core)."
    },
    "The Kafe": {
        "STAFF": {},
        "PLAYERS": {
            "Gorilla": "TANK",
            "Ryan": "DPS",
            "pdk": "DPS",
            "sniper": "DPS",
            "Astronexz": "SPT",
            "Grapes": "SPT",
            "scuffed": "SPT"
        },
        "NOTE": "Competed in 2026 OWCS NA Stage 2 (6th place) and Stage 2 Promotion/Relegation. Disbanded on 2026-09-07."
    },

    # =========================================================================
    # OWCS EMEA ACTIVE
    # =========================================================================
    "Twisted Minds": {
        "STAFF": {},
        "PLAYERS": {
            "TVNT": "TANK",
            "KSAA": "TANK",
            "Quartz": "DPS",
            "Youbi": "DPS",
            "JaeWoo": "DPS",
            "FunnyAstro": "SPT",
            "Simple": "SPT"
        },
        "NOTE": "Longstanding powerhouse in EMEA and Saudi eLeagues. Won OWCS 2024 EMEA Stage 1 & Stage 3, and 2025 OWCS EMEA Stage 1. Currently active with captain Youbi."
    },
    "Virtus.pro": {
        "STAFF": {
            "SMASH": "Head Coach",
            "Nozumo": "Manager"
        },
        "PLAYERS": {
            "eisgnom": "TANK",
            "kevster": "DPS",
            "Seicoe": "DPS",
            "Landon": "SPT",
            "FiXa": "SPT"
        },
        "NOTE": "Entered Overwatch on 2024-06-11 by acquiring the Ataraxia roster. Won 2025 OWCS EMEA Stage 2 and competed at 2024 EWC and 2024 World Finals."
    },
    "1234": {
        "STAFF": {
            "Backbone": "Coach"
        },
        "PLAYERS": {
            "GoldenPants": "TANK",
            "amdp": "SPT",
            "Kai": "DPS",
            "WMaimone": "DPS",
            "Khenail": "SPT",
            "crispy": "SPT"
        },
        "NOTE": "Formed following the release of the Anyone's Legend roster. Placed 5th in OWCS 2026 EMEA Stage 2 and secured Stage 3 spot through Stage 2 Promotion/Relegation."
    },
    "Team Peps": {
        "STAFF": {
            "René": "Head Coach",
            "SoOn": "Coach",
            "Féfé": "General Manager",
            "Søeny": "Manager"
        },
        "PLAYERS": {
            "Willys07": "TANK",
            "KroxZ": "TANK",
            "Rav": "DPS",
            "xzodyal": "DPS",
            "FDGod": "SPT",
            "Xeriongdh": "SPT"
        },
        "NOTE": "Prominent French organization. Competed as Gaimin Gladiators in mid-2024 before returning to Team Peps. OWCS EMEA Partner team for 2026."
    },
    "Geekay Esports": {
        "STAFF": {
            "Undine": "Head Coach",
            "AOY": "Manager"
        },
        "PLAYERS": {
            "ZIYAD": "TANK",
            "AlphaYi": "DPS",
            "LBBD7": "DPS",
            "FiNN": "SPT",
            "Kellex": "SPT",
            "Haku": "SPT"
        },
        "NOTE": "Competed in NA throughout 2025 before returning to the EMEA region in early 2026 with a newly rebuilt roster."
    },

    # =========================================================================
    # OWCS EMEA INACTIVE
    # =========================================================================
    "ENCE": {
        "STAFF": {
            "Algos05": "Coach"
        },
        "PLAYERS": {
            "Vestola": "TANK",
            "Chase": "TANK",
            "Kai": "DPS",
            "kevster": "DPS",
            "WMaimone": "DPS",
            "SKAI": "SPT",
            "Kellex": "SPT"
        },
        "NOTE": "Formed by acquiring BuboSprayCheck roster. Won 2024 OWCS EMEA Stage 2, placed 4th at 2024 World Finals Stockholm. Officially disbanded on 2025-01-09."
    },
    "Ex Oblivione": {
        "STAFF": {
            "Cas": "Head Coach",
            "PeaNuTz": "Coach",
            "Kendar": "Manager"
        },
        "PLAYERS": {
            "Theomatic": "TANK",
            "eisgnom": "TANK",
            "Avo": "DPS",
            "TOPDRAGON": "DPS",
            "Alpha": "SPT",
            "D0nghun": "SPT",
            "Bonkey": "SPT"
        },
        "NOTE": "Placed 4th in 2024 OWCS EMEA Stage 4 (featuring Korean imports TOPDRAGON and D0nghun) before ceasing operations in January 2025."
    },
    "Sheer Cold": {
        "STAFF": {
            "Sully": "Coach",
            "Thor": "Manager"
        },
        "PLAYERS": {
            "choose": "TANK",
            "Románi": "TANK",
            "olpx": "DPS",
            "M3WS": "DPS",
            "Kilaa": "DPS",
            "gcb": "SPT",
            "Natlocks": "SPT",
            "Soax": "SPT"
        },
        "NOTE": "Historic European organization founded in 2020. Competed in 2024 OWCS EMEA Stages 1 & 2 before officially disbanding on 2024-09-08."
    },
    "Quick Esports": {
        "STAFF": {
            "littleblits": "Manager"
        },
        "PLAYERS": {
            "TwolzZ": "TANK",
            "phi": "DPS",
            "Dannedd": "DPS",
            "Grathen": "DPS",
            "Shax": "DPS",
            "yoham": "SPT",
            "Strebor": "SPT"
        },
        "NOTE": "Placed 5th-6th in 2024 OWCS EMEA Stage 1. Rebranded to Vanir Quick on 2025-11-07."
    },
    "nu.age": {
        "STAFF": {
            "Spongey": "Coach",
            "W1lliam": "Manager",
            "Mat71": "Manager"
        },
        "PLAYERS": {
            "KroxZ": "TANK",
            "ImScared22": "TANK",
            "SharP": "DPS",
            "Nielou": "DPS",
            "Natsuki": "SPT",
            "Buddie": "SPT",
            "GOGO": "SPT"
        },
        "NOTE": "French organization active from 2023-11-10 to 2024-09-13. Competed in 2024 OWCS EMEA Stage 1 (9th-12th) and Overwatch All For One before disbanding."
    },
    "LeftRightGnight": {
        "STAFF": {
            "Saadist": "General Manager"
        },
        "PLAYERS": {
            "cuFFa": "TANK",
            "Saadist": "TANK",
            "Lethal": "DPS",
            "Scyle": "DPS",
            "Vision": "DPS",
            "Galaa": "SPT",
            "Admiral": "SPT",
            "Lukemino": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS EMEA Stage 1 (9th-12th) fielding a hybrid collegiate/pro lineup before officially disbanding on 2024-04-07."
    },
    "AWW YEAH": {
        "STAFF": {
            "Minimi": "Coach",
            "Jaydasch": "Manager"
        },
        "PLAYERS": {
            "chazm": "TANK",
            "Minimi": "TANK",
            "Necros": "DPS",
            "h9mpe": "DPS",
            "Isack": "SPT",
            "Love": "SPT"
        },
        "NOTE": "Successor to Avoided, notorious for Wrecking Ball and Genji one-trick compositions. Competed in 2024 OWCS EMEA Stage 1 (Group C)."
    },
    "A One Man Army": {
        "STAFF": {
            "PeaNuTz": "Coach"
        },
        "PLAYERS": {
            "Theomatic": "TANK",
            "TOPDRAGON": "DPS",
            "Avo": "DPS",
            "D0nghun": "SPT",
            "Alpha": "SPT"
        },
        "NOTE": "Acquired Korean imports TOPDRAGON and D0nghun for FACEIT League Season 2 - EMEA Master, upsetting Gaimin Gladiators. Disbanded on 2024-10-24."
    },
    "Celtas": {
        "STAFF": {
            "Pathfinder": "Manager"
        },
        "PLAYERS": {
            "Tama": "TANK",
            "Pastor": "DPS",
            "Zydra": "DPS",
            "Podonova": "SPT"
        },
        "NOTE": "Partnered with Supershy during 2024 OWCS EMEA competition. Officially disbanded on 2024-12-29."
    },
    "Bingus": {
        "STAFF": {},
        "PLAYERS": {
            "Helmerdrake": "TANK",
            "Lutu": "DPS",
            "SterbeGern": "DPS",
            "Jack": "SPT",
            "Waynon": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS EMEA Stage 1 (Group C) before disbanding."
    },
    "EF Flexodiax": {
        "STAFF": {},
        "PLAYERS": {
            "Lunar": "TANK",
            "Sonne": "TANK",
            "Kurama": "DPS",
            "Tricky": "DPS",
            "Reisu": "SPT",
            "RodFD": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS EMEA Stage 1 before rebranding to Everfrost Esports in April 2024."
    },
    "A-Square Tengu": {
        "STAFF": {},
        "PLAYERS": {
            "ImScared22": "TANK",
            "Kabetaijin": "DPS",
            "Nielou": "DPS",
            "KZR": "SPT",
            "Neliozu": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS EMEA Stage 1 and finished 2nd at Gamers Assembly 2024 before merging into A-Square 0907."
    },
    "Peace and Love": {
        "STAFF": {},
        "PLAYERS": {
            "eisgnom": "TANK",
            "kaiBa": "DPS",
            "Loren": "DPS",
            "PSYCH0": "DPS",
            "Abheek": "SPT",
            "Bya": "SPT",
            "Ailiseu": "SPT"
        },
        "NOTE": "Placed 4th in 2024 OWCS EMEA Stage 2. Roster was signed by R8 Esports on 2024-04-29 and later formed the core of Ex Oblivione."
    },
    "Ataraxia": {
        "STAFF": {
            "Laggy": "Manager",
            "Ness": "Manager"
        },
        "PLAYERS": {
            "Raajaro": "TANK",
            "sHockWave": "DPS",
            "Clowd": "DPS",
            "Sauna": "DPS",
            "Khenail": "SPT",
            "Galaa": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS EMEA Stage 2. Roster was acquired by Virtus.pro on 2024-06-11 ahead of the Esports World Cup 2024."
    },
    "Deimpero": {
        "STAFF": {
            "GOGO": "Coach"
        },
        "PLAYERS": {
            "Willys07": "TANK",
            "Shyraa": "TANK",
            "china": "DPS",
            "Meliø": "DPS",
            "GOGO": "SPT",
            "reviewz": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS EMEA Stage 2 (7th-8th). Disbanded on 2024-08-01, with core briefly transitioning to Shadow Wizard Crew."
    },
    "Supershy": {
        "STAFF": {
            "Loyn": "Coach",
            "Sully": "Manager"
        },
        "PLAYERS": {
            "TwolzZ": "TANK",
            "Scraine": "DPS",
            "Zorrow": "DPS",
            "KZR": "SPT"
        },
        "NOTE": "Active from 2023-09-01 to 2025-11-28. Competed in European tournaments and partnered with Celtas and Harmony."
    },
    "Metaboiz": {
        "STAFF": {
            "KuroQ": "Coach",
            "Woods": "Coach",
            "Sully": "Manager",
            "Algos05": "Manager"
        },
        "PLAYERS": {
            "PoroPlays": "TANK",
            "Philion": "DPS",
            "icav": "DPS",
            "FakeJake": "DPS",
            "teksol": "SPT",
            "flipper": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS EMEA Stages 1 through 4 (Group B in Stage 4) with a core Polish lineup. Officially disbanded in January 2025."
    },
    "Rocstars": {
        "STAFF": {
            "Pathfinder": "Manager"
        },
        "PLAYERS": {
            "TVNT": "TANK",
            "roho": "DPS",
            "Scyle": "DPS",
            "AOY": "SPT",
            "Olli": "SPT"
        },
        "NOTE": "Formed by the Saudi core of ROC Esports (along with Scyle and Olli) to compete in 2024 OWCS EMEA Stage 2 (9th-12th) when ROC Esports did not enter as an organization."
    },
    "SCHMUNGUS": {
        "STAFF": {},
        "PLAYERS": {
            "Bogur": "TANK",
            "Zerggy": "DPS",
            "qrxu": "DPS",
            "mL7": "SPT",
            "Eskay": "SPT"
        },
        "NOTE": "Content creator stack featuring Bogur, ML7, and Eskay. Competed in 2024 OWCS EMEA Stage 2 Group Stage."
    },
    "Gaimin Gladiators": {
        "STAFF": {
            "René": "Head Coach",
            "SoOn": "Coach",
            "Féfé": "General Manager"
        },
        "PLAYERS": {
            "Tred": "TANK",
            "Naga": "DPS",
            "xzodyal": "DPS",
            "FDGod": "SPT",
            "yoham": "SPT"
        },
        "NOTE": "Signed the Team Peps roster in June 2024 to compete at Esports World Cup 2024 and OWCS 2024 EMEA Stage 3 before disbanding on 2024-09-07, returning to Team Peps."
    },
    "Wasp X Ohhhh No": {
        "STAFF": {},
        "PLAYERS": {
            "Ostrix": "TANK",
            "Gurkmeister": "TANK",
            "Qrxu": "DPS",
            "tekuno": "DPS",
            "KDM": "SPT",
            "ilppi13": "SPT"
        },
        "NOTE": "Formed on 2024-08-09 as a partnership between Element Wasp and unsigned team OHHHH NO. Competed in 2024 OWCS EMEA Stages 3 & 4 before disbanding on 2025-09-04."
    },
    "Hypnos": {
        "STAFF": {
            "Schef": "Coach",
            "Ashh": "Manager"
        },
        "PLAYERS": {
            "Skytorr": "TANK",
            "CaptainPrash": "TANK",
            "delusion": "DPS",
            "kio": "DPS",
            "sxj": "SPT",
            "MCD": "SPT"
        },
        "NOTE": "Placed 5th-6th in 2024 OWCS EMEA Stage 3 with a lineup featuring veteran Korean support MCD and Skytorr."
    },
    "Vendetta": {
        "STAFF": {
            "jun": "Manager"
        },
        "PLAYERS": {
            "Hybrid": "TANK",
            "Cookie084": "DPS",
            "Jakub": "DPS",
            "china": "DPS",
            "crispy": "SPT",
            "Lv1Crook": "SPT"
        },
        "NOTE": "Formed on 2024-08-08 to compete in 2024 OWCS EMEA Stage 3 (qualifying through Swiss) and Stage 4. Active until disbanding in early 2025."
    },
    "SrPeakCheck": {
        "STAFF": {},
        "PLAYERS": {
            "LhCloudy": "TANK",
            "Sauna": "DPS",
            "Qrxu": "DPS",
            "ghost91": "DPS",
            "mL7": "SPT",
            "AkkuFastLeer": "SPT"
        },
        "NOTE": "Legendary Finnish stack originally formed in 2021 whose core joined ENCE via BuboSprayCheck. Returned on 2024-08-08 featuring LhCloudy, Sauna, and ML7 for OWCS Stage 3 & 4."
    },
    "Al Qadsiah": {
        "STAFF": {},
        "PLAYERS": {
            "Vestola": "TANK",
            "Taejong": "DPS",
            "Ade": "DPS",
            "zox": "DPS",
            "KORZ": "SPT",
            "SirMajed": "SPT",
            "Galaa": "SPT"
        },
        "NOTE": "Esports division of Saudi club Al Qadsiah FC. Won 2026 Saudi eLeague Championship and competed in 2026 OWCS EMEA Stage 2 before officially disbanding on 2026-08-29."
    },
    "Ohana Aloha": {
        "STAFF": {},
        "PLAYERS": {
            "Majin": "TANK",
            "roho": "DPS",
            "Escanor": "DPS",
            "alba": "SPT",
            "Chaba": "SPT"
        },
        "NOTE": "Competed in 2024 OWCS EMEA Stage 3 (Swiss & Group Stage) featuring Saudi players roho and Escanor."
    },
    "Piece of Cake": {
        "STAFF": {
            "BenBest": "Coach"
        },
        "PLAYERS": {
            "Tred": "TANK",
            "Naga": "DPS",
            "xzodyal": "DPS",
            "crispy": "SPT",
            "Scyle": "SPT"
        },
        "NOTE": "Formed after Gaimin Gladiators disbanded, featuring ex-GG core with BenBest as coach. Placed 1st in Swiss and 5th-6th in 2024 OWCS EMEA Stage 4."
    },
    "Team G4mbit": {
        "STAFF": {
            "Weza": "Manager"
        },
        "PLAYERS": {
            "PoroPlays": "TANK",
            "PommiTimo": "DPS",
            "Szymondki": "DPS",
            "Verit": "DPS",
            "ilppi13": "SPT"
        },
        "NOTE": "Polish team that competed in 2024 OWCS EMEA Stage 4 Swiss/qualifiers and FACEIT League EMEA Master."
    },
    "Negative Mental": {
        "STAFF": {},
        "PLAYERS": {
            "Mesopos": "TANK",
            "olpx": "DPS",
            "d7mi": "DPS",
            "RKM": "DPS",
            "Zero": "SPT"
        },
        "NOTE": "Saudi Arabian stack that competed in 2024 OWCS EMEA Stage 4 (Group D) and the ESL Saudi Challenge."
    },
    "Gen.G Esports": {
        "STAFF": {},
        "PLAYERS": {
            "Tred": "TANK",
            "Backbone": "DPS",
            "xzodyal": "DPS",
            "Strebor": "DPS",
            "crispy": "SPT",
            "FunnyAstro": "SPT",
            "Khenail": "SPT"
        },
        "NOTE": "Returned to Overwatch in 2025 as an OWCS EMEA Partner team. Placed 4th in 2025 OWCS EMEA Stage 3 playoffs before officially disbanding on 2025-12-03."
    },
    "The Ultimates": {
        "STAFF": {
            "antares": "Head Coach",
            "Sukaira": "Manager",
            "Kekbondi": "Manager"
        },
        "PLAYERS": {
            "Skytorr": "TANK",
            "Kekbondi": "TANK",
            "Evil": "DPS",
            "SNOWDR0P": "DPS",
            "ZERO": "DPS",
            "yoham": "SPT",
            "Strebor": "SPT",
            "Jonte": "SPT"
        },
        "NOTE": "Prominent Saudi organization. Finished 3rd in 2025 OWCS EMEA Stage 1 and 4th in Stage 2 before roster issues led to removal from Stage 3 in August 2025."
    },
    "Team Vision": {
        "STAFF": {
            "jun": "Manager"
        },
        "PLAYERS": {
            "Tama": "TANK",
            "ChoiSehwan": "DPS",
            "Prophet": "DPS",
            "Viol2t": "SPT",
            "Khenail": "SPT",
            "One": "SPT"
        },
        "NOTE": "Saudi Arabian organization that won 2025 OWCS EMEA Stage 2 Promotion/Relegation and placed 5th-6th in Stage 3 fielding Viol2t, ChoiSehwan, Prophet, and Tama."
    },
    "DVSG": {
        "STAFF": {
            "PnR": "Head Coach",
            "ilppi13": "Assistant Coach",
            "antares": "Manager"
        },
        "PLAYERS": {
            "Willys07": "TANK",
            "Dip": "DPS",
            "Zydra": "DPS",
            "Natsuki": "SPT",
            "yoham": "SPT"
        },
        "NOTE": "Competed as 1DIPVS100GORILLAS (DVSG) in 2025 OWCS EMEA Stage 2 (7th) and Stage 2 Promotion/Relegation (3rd) before disbanding in August 2025."
    },
    "Frost Tails eSport": {
        "STAFF": {
            "YounaCha": "Manager"
        },
        "PLAYERS": {
            "JesperSwag": "TANK",
            "Sined": "DPS",
            "Pak": "DPS",
            "Verit": "DPS"
        },
        "NOTE": "French team founded in 2022 that won Overwatch All For One 2025 Playoffs and competed in OWCS EMEA qualifiers and FACEIT League."
    },
    "Goud Guys ANM": {
        "STAFF": {},
        "PLAYERS": {
            "KroxZ": "TANK",
            "EgS": "DPS",
            "Johnowich": "DPS"
        },
        "NOTE": "French squad that competed in 2025 OWCS EMEA Stage 3 (7th place) before its core was acquired by Goud Guys in early 2026."
    },
    "Anyone's Legent": {
        "STAFF": {
            "YaHo": "Head Coach"
        },
        "PLAYERS": {
            "amdp": "TANK",
            "Kai": "DPS",
            "WMaimone": "DPS",
            "Backbone": "DPS",
            "Khenail": "SPT",
            "crispy": "SPT"
        },
        "NOTE": "Chinese organization Anyone's Legend that entered OWCS EMEA in 2026. Placed 5th in 2026 OWCS EMEA Stage 1 before releasing roster on 2026-04-16 (later becoming 1234)."
    },
    "Telacy": {
        "STAFF": {
            "JuJu": "Coach",
            "Clutch": "Manager"
        },
        "PLAYERS": {
            "Mesopos": "TANK",
            "icav": "DPS",
            "sxj": "SPT",
            "teksol": "SPT",
            "Clutch": "SPT"
        },
        "NOTE": "Austrian esports organization with main roster competing in OWCS EMEA and FACEIT League divisions alongside sister team Telacy Crimson."
    },

    # =========================================================================
    # GLOBAL LAN & LCQ INVITATIONALS
    # =========================================================================
    "Toronto Ultra": {
        "STAFF": {
            "Casores": "Head Coach",
            "Danny": "Analyst",
            "Lovell": "General Manager"
        },
        "PLAYERS": {
            "SOMEONE": "TANK",
            "MER1T": "DPS",
            "Sugarfree": "DPS",
            "Rupal": "SPT",
            "Vega": "SPT"
        },
        "NOTE": "Temporary rebrand of Toronto Defiant (OverActive Media) to compete in the Esports World Cup 2024 (where they finished 2nd) before reverting back to Toronto Defiant."
    },
    "LGD.OA": {
        "STAFF": {
            "RUSH": "Head Coach"
        },
        "PLAYERS": {
            "Guxue": "TANK",
            "Leave": "DPS",
            "Shy": "DPS",
            "Lengsa": "SPT",
            "Mmonk": "SPT"
        },
        "NOTE": "Formed on 2024-06-13 as a partnership between LGD Gaming and Once Again for the Esports World Cup 2024 China invitation slot (placed 9th-12th)."
    },
    "MKERS": {
        "STAFF": {},
        "PLAYERS": {
            "punk": "TANK",
            "Colourhex": "DPS",
            "TOPDRAGON": "DPS",
            "Neuu": "DPS",
            "OPENER": "SPT",
            "Ackyyy": "SPT"
        },
        "NOTE": "Italian organization that signed Australian team The Great Showmen to represent Oceania at the Esports World Cup 2024 before disbanding on 2024-08-01."
    },
    "Sign Esports": {
        "STAFF": {
            "Wheats": "Head Coach",
            "Empress": "Assistant Coach",
            "ThatAFKNoob": "General Manager"
        },
        "PLAYERS": {
            "RhynO": "TANK",
            "Rokit": "DPS",
            "Painkiller": "DPS",
            "Lep": "SPT",
            "Lukemino": "SPT"
        },
        "NOTE": "Saudi organization that partnered with NTMR to loan their entire roster for the OWCS 2025 Midseason Championship in Riyadh (placed 9th-12th)."
    },
    "ZoKorp Esports": {
        "STAFF": {
            "Zohaib Khawaja": "Manager"
        },
        "PLAYERS": {
            "StillKIWI": "TANK",
            "Abbs": "DPS",
            "Poke": "DPS",
            "Kani": "SPT",
            "ShawnOFF": "SPT"
        },
        "NOTE": "South American qualifier representative at the OWCS 2025 Midseason Championship (13th-16th). Disbanded in November 2025 following organizational controversy."
    },
    "9z Team": {
        "STAFF": {},
        "PLAYERS": {
            "CLEAR": "TANK",
            "Lightt": "DPS",
            "Wed": "DPS",
            "B3rt": "SPT",
            "tizi": "SPT"
        },
        "NOTE": "Argentinian organization that represented South America at the OWCS 2026 Midseason Championship (13th-16th)."
    },
    "Aura": {
        "STAFF": {},
        "PLAYERS": {
            "Symbol": "DPS",
            "ØØØ": "DPS",
            "Lkyj": "SPT"
        },
        "NOTE": "Competed in the OWCS 2025 Midseason Championship - Last Chance Qualifier in Riyadh (9th-12th place)."
    },
    "Bright FUture": {
        "STAFF": {},
        "PLAYERS": {
            "PEPPI": "TANK",
            "roho": "DPS",
            "zox": "DPS",
            "alba": "SPT",
            "Chaba": "SPT"
        },
        "NOTE": "Saudi Arabian organization that placed 3rd-4th in the OWCS 2025 Midseason Championship - Last Chance Qualifier."
    },
    "FlexaBull": {
        "STAFF": {},
        "PLAYERS": {
            "SIXSIXSIXSIX": "DPS",
            "SLY": "DPS"
        },
        "NOTE": "Saudi Arabian squad featuring Ahmed 'SIXSIXSIXSIX' Alhaidari and Abdallah 'SLY' Khaled El-ghamdi that competed in the OWCS 2025 Midseason Championship - Last Chance Qualifier (9th-12th place)."
    },
    "Force": {
        "STAFF": {
            "Tydolla": "Coach"
        },
        "PLAYERS": {
            "Fearless": "TANK",
            "Edison": "DPS",
            "NewJ": "DPS",
            "Soulsay": "DPS",
            "Ydot": "SPT",
            "Gaisen": "SPT"
        },
        "NOTE": "Entry/Alias for ENTER FORCE.36 at the OWCS 2025 Midseason Championship - Last Chance Qualifier (5th-8th place, defeating Zenith 3-0 before falling to Team Falcons and ZETA DIVISION)."
    },
    "LOLARIOUS": {
        "STAFF": {},
        "PLAYERS": {
            "nawaf": "TANK",
            "Koala!": "DPS",
            "cloud": "DPS"
        },
        "NOTE": "Competed in the OWCS 2025 Midseason Championship - Last Chance Qualifier in Riyadh (9th-12th place)."
    },
    "TFW": {
        "STAFF": {
            "Merc": "Coach",
            "CamoMilla": "Manager"
        },
        "PLAYERS": {
            "NevsH200": "TANK",
            "SLEEK": "DPS"
        },
        "NOTE": "European squad that competed in FACEIT League Season 6 EMEA Master and OWCS 2025 Midseason Championship - Last Chance Qualifier (5th-8th)."
    },
    "Zenith": {
        "STAFF": {},
        "PLAYERS": {
            "H2BY-": "TANK",
            "Astel": "DPS",
            "MJED": "DPS",
            "Tobi": "SPT",
            "9jzm": "SPT"
        },
        "NOTE": "Competed in the OWCS 2025 Midseason Championship - Last Chance Qualifier (9th-12th place) in Riyadh."
    },
    "ZoneX": {
        "STAFF": {},
        "PLAYERS": {
            "Rashed": "TANK",
            "Quixz": "DPS",
            "diobrando": "DPS"
        },
        "NOTE": "Competed in the OWCS 2025 Midseason Championship - Last Chance Qualifier in Riyadh."
    },
    "Shock": {
        "STAFF": {},
        "PLAYERS": {},
        "NOTE": "Saudi Arabian team (distinct from NA's NRG Shock) that competed in the OWCS 2025 Midseason Championship - Last Chance Qualifier in Riyadh."
    }
}

# Alias
TEAMS = TEAMS_ROSTER
