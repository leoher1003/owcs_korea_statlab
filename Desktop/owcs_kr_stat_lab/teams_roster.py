#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teams_roster.py
Master dictionary of all 231 OWCS teams (2024~2026).
Each team key is initialized to an empty dict schema template ready for roster & transfer data.
"""

TEAMS_ROSTER = {
    # =========================================================================
    # OWCS KOREA (KR) ACTIVE
    # =========================================================================
    "Crazy Raccoon": {
        "STAFF": {"Kong": "Assistant Coach",
                  "Izayaki":"Assistant Coach"},
        "PLAYERS": {"Junbin": "TANK",
                    "MAX": "TANK",
                    "HeeSang": "DPS", 
                    "LIP": "DPS", 
                    "Stalk3r": "DPS", 
                    "CH0R0NG": "SPT", 
                    "vigilante": "SPT"}
    },
    "Team Falcons": {
        "STAFF": {"NineK": "Head Coach", 
                  "Junkbuck": "Coach", 
                  "SP9RK1E": "Coach", 
                  "Levi": "Team Manager"},
        "PLAYERS": {"HanBin": "TANK", 
                    "SOMEONE": "TANK", 
                    "Checkmate":"DPS", 
                    "SP1NT":"DPS", 
                    "MER1T":"DPS", 
                    "ChiYo":"SPT", 
                    "Fielder":"SPT"}
    },
    "ZETA DIVISION": {
        "STAFF": {"Crusty":"Head Coach", 
                  "Twilight":"Coach"},
        "PLAYERS": {"Bernar":"TANK", 
                    "Mealgaru":"TANK", 
                    "Proper":"DPS", 
                    "knife":"DPS", 
                    "Viol2t":"SPT", 
                    "shu":"SPT"}
    },
    "T1": {
        "STAFF": {"RUSH": "Head Coach", 
                  "Fleta": "Playing Coach", 
                  "GgulTaek": "Coach"},
        "PLAYERS": {"DONGHAK": "TANK", 
                    "Jasm1ne": "TANK", 
                    "ZEST": "DPS",
                    "Proud": "DPS", 
                    "Bliss":"SPT", 
                    "skewed":"SPT"}
    },
    
    "Røde ZANSIDE GAMING": {
        "STAFF": {"KariV": "Head Coach", 
                  "Ir1s": "Coach", 
                  "Mircalla": "Coach"},
        "PLAYERS": {"HEISER":"TANK", 
                    "HEESUNG":"TANK", 
                    "Taejong":"DPS",
                    "Kilo":"DPS",
                    "Becky":"DPS",
                    "OPENER": "SPT", 
                    "IRONY": "SPT"}
    },
    "O2 Blast": {
        "STAFF": {"O2Boss":"Head Coach", 
                  "Chilhwa":"Coach", 
                  "Myunb0ng":"Coach", 
                  "Cane": "Coach"},
        "PLAYERS": { "FATE": "TANK", 
                     "Homerunball":"TANK", 
                     "WuTian":"DPS", 
                     "Perr":"DPS", 
                     "A1IEN":"DPS", 
                     "Faith":"SPT", 
                     "Gamjung":"SPT"}  
    },
    "Poker Face": {
        "STAFF": {"SEON":"Head Coach", 
                  "Mandu":"Coach"},
        "PLAYERS": {"SoLA":"TANK", 
                    "SWOO":"TANK", 
                    "F1nally":"DPS", 
                    "SORI":"DPS", 
                    "Dumbbell":"SPT", 
                    "Caffeine":"SPT", 
                    "SOAE":"SPT"}
    },
    "Cheeseburger": {
        "STAFF": {"KRILLIN":"Coach"},
        "PLAYERS": {"Belosrea":"TANK", 
                    "K4NE":"DPS", 
                    "Profit":"DPS", 
                    "AZENT":"DPS", 
                    "TENTEN":"SPT", 
                    "Trest":"SPT"}
    },
    "Seiji Esports": {
        "STAFF": {"Da1Da1Smooth":"Coach", 
                  "SanGuiNar":"Coach"},
        "PLAYERS": {"SENTIER":"TANK", 
                    "DOX":"TANK", 
                    "D4RT":"DPS", 
                    "M1NUT2":"DPS", 
                    "OFF":"SPT",
                    "Lavender":"SPT"}
    },
    # =========================================================================
    # OWCS KOREA (KR) INACTIVE
    # =========================================================================
    "WAC": {
        "STAFF": {"MOON":"Head Coach",
                 "Kong": "Coach",
                  "Pavane": "Coach",
                 },
        "PLAYERS": {
            "Junbin":"TANK",
            "MAX":"TANK",
            "HeeSang":"DPS",
            "LIP":"DPS",
            "CH0R0NG":"SPT",
            "shu":"SPT"
        },
        "NOTE": "Whole roster acquired by Crazy Raccoon." 
    },
    "From The Gamer": {
        "STAFF": {"Neko":"Coach"},
        "PLAYERS":{
            "Bernar":"TANK",
            "AlphaYi":"DPS",
            "Flora":"DPS",
            "Viol2t":"SPT",
            "FiNN":"SPT"
        },
        "NOTE": "Whole roster acquired by Crazy Raccoon
            
    },
    "YETI": {
        "STAFF": {"Fate": "Head Coach", "Fleta": "Coach"},
        "PLAYERS": {
            "DONGHAK":"TANK",
            "Viper":"DPS",
            "knife":"DPS",
            "Bliss":"SPT",
            "IRONY":"SPT"
        },
        "NOTE": "Whole roster acquired by FNATIC"
    },
    "RunAway": {
        "STAFF": {"Chara":"Coach"},
        "PLAYERS": {
            "MAG":"TANK",
            "ZEST":"DPS",
            "Prophet":"DPS",
            "LeeJaeGon":"SPT",
            "vigilante":"SPT"
        },
        "NOTE": "Disbanded after 2024 OWCS Korea Stage 1"
    },
    "Vesta Esports Crew": {
        
    },
    "Sin Prisa Gaming": {
        
    },
    "FNATIC": {
        
    },
    "HaeJeokDan": {
        
    },
    "Old Ocean": {
        
    },
    "New Era": {
        
    },
    "WAY": {
        "STAFF": {},
        "PLAYERS": {
            "Mealgaru":"TANK",
            "Jasm1ne":"TANK",
            "WhoRu":"DPS",
            "Ade":"DPS",
            "LeeSooMin":"SPT",
            "MAKA":"SPT
        },
        "NOTE": "Whole roster acquired by All Gamers Global during 2025 OWCS Korea Stage 2"
    },
    "All Gamers Global": {
        
    },
    "ONSIDE GAMING": {
        
    },
    "WAE": {
        
    },
    "Mir Gaming": {
        
    },
    "Røde ONSIDE GAMING": {
        "STAFF": {"F4ze": "Head Coach", "Ado":"Coach", "Haksal":"Coach"},
        "PLAYERS": {
            "Attack":"TANK",
            "Kilo":"DPS",
            "SP1NT":"DPS",
            "OPENER":"SPT",
            "IRONY":"SPT"
        },
        "NOTE": "Merged with ZAN Esports prior to 2026 OWCS Korea Stage 2
    },
    "ZAN Esports": {
        "STAFF": {"Ir1s":"Coach", "KariV":"Head Coach", "sihu":"Manager", "Mircalla":"Coach"},
        "PLAYERS":{
            "HEISER":"TANK",
            "Becky":"DPS",
            "Probe":"DPS",
            "A1IEN":"DPS",
            "Yangjun":"SPT",
            "KIVIS":"SPT",
            "Hyeonjun":"SPT"
        },
        "NOTE": "Merged with Røde Onside Gaming prior to 2026 OWCS Korea Stage 2
    },
    "Super Bad": {
        
    },

    # =========================================================================
    # OWCS JAPAN (JP) ACTIVE
    # =========================================================================
    "VARREL": {},
    "ENTER FORCE.36": {},
    "MURASH GAMING": {},
    "99DIVINE": {},
    "Please Not Hero Ban": {},
    "Uwinks": {},
    "Lazuli": {},
    "REVATI": {},
    # =========================================================================
    # OWCS JAPAN (JP) INACTIVE
    # =========================================================================
    "SixBlow": {},
    "Arise Project": {},
    "Namekuji Brothers": {},
    "Pandia": {},
    "INSOMNIA": {},
    "Hayabusa Gaming": {},
    "Nyam Gaming": {},
    "REVATI X NTMR": {},
    "MFC X Supreme": {},
    "Telomere": {},
    "VortexWolf": {},
    "JKOT": {},
    "Inferno": {},
    "Aplomb Tiger": {},
    "Under Cat": {},
    "LostNever Gaming": {},
    "REJECT": {},
    "ZG": {},
    "Toxic Hamster": {},
    "Lost Never Gaming": {},
    "Tokyo Ta1yo's": {},

    # =========================================================================
    # OWCS PACIFIC (PA) ACTIVE
    # =========================================================================
    "CantHear": {},
    "Retirement Home": {},
    "SeijiKing": {},
    "junjilopzfx0764": {},
    # =========================================================================
    # OWCS PACIFIC (PA) INACTIVE
    # =========================================================================
    "RTFM": {},
    "DAF": {},
    "Teenage Rising": {},
    "Fade": {},
    "Honeypot": {},
    "Personate Gang": {},
    "Far East Society": {},
    "321 Diving": {},
    "Bleed Esports": {},
    "Full House": {},
    "Goon Squad": {},
    "Cat": {},
    "USIA Esports": {},
    "MFC": {},
    "MENG GONG 2": {},
    "Antic X Odium": {},
    "MONSTARGEAR GAMING": {},
    "Trap12": {},
    "The Gatos Guapos": {},
    "mud dog": {},
    "Cold Metal": {},
    "FURY": {},
    "I LOVE YOU": {},
    "Nosebleed Esports": {},
    "Stronghold": {},
    "INVADERS": {},
    "NewGens": {},
    "Team Secret": {},
    "MMY": {},
    "Rankers": {},
    "Quasar Esports": {},
    "MENG GONG 3": {},
    "ELMT": {},
    "Najdorf": {},


    # =========================================================================
    # OWCS CHINA (CN) ACTIVE
    # =========================================================================
    "SHENGSHI": {},
    "JD Gaming": {},
    "All Gamers": {},   
    "Solus Victorem": {},
    "Weibo Gaming": {},
    "OU Gaming": {},
    "HUNENG": {},
    "Black Flag": {},


    # =========================================================================
    # OWCS CHINA (CN) INACTIVE
    # =========================================================================
    "Once Again": {},
    "ROC Esports": {},
    "Blade": {},
    "Super Levi": {},
    "Little Sheep": {},
    "Team CC": {},
    "Team XX": {},
    "Team Equal": {},
    "Homie E": {},
    "ZONES": {},
    "Milk Tea": {},
    "YNB Esports": {},
    "boom": {},
    "MDY": {},
    "DEG": {},
    "Naive Piggy": {},
    "4AM": {},
    "ReturnZ": {},
    "Kitsune Kage": {},

    # =========================================================================
    # OWCS NORTH AMERICA (NA) ACTIVE
    # =========================================================================
    "Spacestation Gaming": {},
    "Dallas Fuel": {},
    "disguised": {},
    "Team Liquid": {},
    "NTMR": {},
    # =========================================================================
    # OWCS NORTH AMERICA (NA) INACTIVE
    # =========================================================================
    "Toronto Defiant": {},
    "LFO": {},
    "Timeless": {},
    "Beluga's Platoon": {},
    "Students of the Game": {},
    "M80": {},
    "Luminosity Gaming": {},
    "Daybreak": {},
    "Shikigami": {},
    "BangBangPow Galaxy": {},
    "Nah I'd Win": {},
    "Pirates in Pyjamas": {},
    "Dreamland": {},
    "Timeless Obsidian": {},
    "Citrus Nation": {},
    "Final Gambit": {},
    "Vice": {},
    "FMCL": {},
    "DhillDucks": {},
    "Visored": {},
    "Nightmare Rotation": {},
    "UNC INC": {},
    "Who Is Goldfish": {},
    "NRG Shock": {},
    "Citrus Nightmare": {},
    "TSM": {},
    "Avidity": {},
    "Timeless Ethereal": {},
    "Arizona State": {},
    "FLUFFY AIMERS": {},
    "Fries In The Bag": {},
    "Team Z": {},
    "Tanuki Esports": {},
    "Absolution": {},
    "O3 Splash": {},
    "Tanuki Tapire": {},
    "EXN Zenith": {},
    "Rammatra Punch": {},
    "Rad X Avidity": {},
    "Blast Off Buds": {},
    "YFP Gaming": {},
    "Rad Esports": {},
    "Amplify": {},
    "Extinction": {},
    "Sakura Esports": {},
    "Supernova": {},
    "LuneX Gaming": {},
    "The Kafe": {},

    # =========================================================================
    # OWCS EMEA ACTIVE
    # =========================================================================
    "Twisted Minds": {},
    "Virtus.pro": {},
    "1234": {},
    "Team Peps": {},
    "Geekay Esports": {},

    # =========================================================================
    # OWCS EMEA INACTIVE
    # =========================================================================
    "ENCE": {},
    "Ex Oblivione": {},
    "Sheer Cold": {},
    "Quick Esports": {},
    "nu.age": {},
    "LeftRightGnight": {},
    "AWW YEAH": {},
    "A One Man Army": {},
    "Celtas": {},
    "Bingus": {},
    "EF Flexodiax": {},
    "A-Square Tengu": {},
    "Peace and Love": {},
    "Ataraxia": {},
    "Deimpero": {},
    "Supershy": {},
    "Metaboiz": {},
    "Rocstars": {},
    "SCHMUNGUS": {},
    "Gaimin Gladiators": {},
    "Wasp X Ohhhh No": {},
    "Hypnos": {},
    "Vendetta": {},
    "SrPeakCheck": {},
    "Al Qadsiah": {},
    "Ohana Aloha": {},
    "Piece of Cake": {},
    "Team G4mbit": {},
    "Negative Mental": {},
    "Gen.G Esports": {},
    "The Ultimates": {},
    "Team Vision": {},
    "DVSG": {},
    "Frost Tails eSport": {},
    "Goud Guys ANM": {},
    "Anyone's Legent": {},
    "Telacy": {},

    # =========================================================================
    # GLOBAL LAN & LCQ INVITATIONALS
    # =========================================================================
    "Toronto Ultra": {},
    "LGD.OA": {},
    "MKERS": {},
    "Sign Esports": {},
    "ZoKorp Esports": {},
    "9z Team": {},
    "Aura": {},
    "Bright FUture": {},
    "FlexaBull": {},
    "Force": {},
    "LOLARIOUS": {},
    "TFW": {},
    "Zenith": {},
    "ZoneX": {},
    "Shock": {},

}

# Alias
TEAMS = TEAMS_ROSTER
