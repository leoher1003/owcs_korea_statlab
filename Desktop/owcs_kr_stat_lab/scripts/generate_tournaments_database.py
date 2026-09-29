#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_tournaments_database.py
Compiles the comprehensive OWCS Tournament & Schedule database:
- Global LAN Events (Dallas Major, EWC, World Finals, Champions Clash, Midseason, LCQ, Bootcamp)
- Regional Stages across Korea (KR), Japan (JP), Pacific (PA), China (CN), North America (NA), EMEA
- Asia Tournaments, Wildcards & Road to World Finals
Outputs: owcs-stat-lab 2/data/tournaments_data.js
"""

import json
from pathlib import Path

OUT_FILE = Path("owcs-stat-lab 2/data/tournaments_data.js")

# Comprehensive teams list updated by user
TEAMS_KR = {
    "2024_STAGE_1": ["WAC", "Team Falcons", "From The Gamer", "YETI", "RunAway", "Poker Face", "Vesta Esports Crew", "Sin Prisa Gaming"],
    "2024_STAGE_2": ["Crazy Raccoon", "Team Falcons", "ZETA DIVISION", "FNATIC", "Poker Face", "HaeJeokDan", "Vesta Esports Crew", "Old Ocean"],
    "2025_STAGE_1": ["Crazy Raccoon", "Team Falcons", "ZETA DIVISION", "T1", "Poker Face", "New Era", "Vesta Esports Crew", "WAY", "From The Gamer"],
    "2025_STAGE_2": ["Crazy Raccoon", "Team Falcons", "ZETA DIVISION", "T1", "All Gamers Global", "ONSIDE GAMING", "Poker Face", "Old Ocean", "Vesta Esports Crew"],
    "2025_STAGE_3": ["Crazy Raccoon", "Team Falcons", "ZETA DIVISION", "T1", "WAE", "ONSIDE GAMING", "Old Ocean", "Poker Face", "Mir Gaming", "Cheeseburger"],
    "2026_STAGE_1": ["Crazy Raccoon", "Team Falcons", "ZETA DIVISION", "T1", "Røde ONSIDE GAMING", "ZAN Esports", "New Era", "Cheeseburger", "Poker Face"],
    "2026_STAGE_2": ["Crazy Raccoon", "Team Falcons", "ZETA DIVISION", "T1", "Røde ZANSIDE GAMING", "O2 Blast", "Cheeseburger", "Poker Face", "Super Bad"],
    "2026_STAGE_3": ["Crazy Raccoon", "Team Falcons", "ZETA DIVISION", "T1", "Røde ZANSIDE GAMING", "O2 Blast", "Cheeseburger", "Poker Face", "Seiji Esports"]
}

TEAMS_JP = {
    "2024_STAGE_1": ["SixBlow", "Arise Project", "Namekuji Brothers", "VARREL", "Pandia", "REVATI", "INSOMNIA", "Hayabusa Gaming", "Nyam Gaming"],
    "2024_STAGE_2": ["VARREL", "INSOMNIA", "Nyam Gaming", "Namekuji Brothers", "REVATI X NTMR", "Lazuli", "MFC X Supreme", "Telomere"],
    "2025_STAGE_1": ["Lazuli", "Nyam Gaming", "VARREL", "VortexWolf", "Please Not Hero Ban", "JKOT", "Inferno", "Hayabusa Gaming", "Aplomb Tiger", "Under Cat", "INSOMNIA", "LostNever Gaming"],
    "2025_STAGE_2": ["VARREL", "REJECT", "Inferno", "Aplomb Tiger", "Please Not Hero Ban", "Lazuli", "REVATI", "Arise Project", "JKOT", "ZG", "Hayabusa Gaming", "Nyam Gaming"],
    "2025_STAGE_3": ["VARREL", "REJECT", "Please Not Hero Ban", "Telomere", "Vesta Esports Crew", "Hayabusa Gaming", "Lazuli", "99DIVINE", "Toxic Hamster", "Nyam Gaming", "Arise Project", "Lost Never Gaming"],
    "2026_STAGE_1": ["VARREL", "Tokyo Ta1yo's", "Please Not Hero Ban", "99DIVINE", "Telomere", "Lazuli", "ENTER FORCE.36", "Nyam Gaming"],
    "2026_STAGE_2": ["VARREL", "ENTER FORCE.36", "99DIVINE", "MURASH GAMING", "REVATI", "Please Not Hero Ban", "Lazuli", "Uwinks"],
    "2026_STAGE_3": ["VARREL", "ENTER FORCE.36", "99DIVINE", "MURASH GAMING", "REVATI", "Please Not Hero Ban", "Lazuli", "Uwinks"]
}

TEAMS_PA = {
    "2024_STAGE_1": ["RTFM", "DAF", "Teenage Rising", "Fade", "Honeypot", "Personate Gang", "Far East Society", "321 Diving"],
    "2024_STAGE_2": ["99DIVINE", "Bleed Esports", "Teenage Rising", "Fade", "Full House", "Goon Squad", "Cat", "USIA Esports"],
    "2025_STAGE_1": ["99DIVINE", "MFC", "MENG GONG 2", "Full House", "Antic X Odium", "MONSTARGEAR GAMING", "Trap12", "Fade"],
    "2025_STAGE_2": ["99DIVINE", "The Gatos Guapos", "Full House", "MENG GONG 2", "mud dog", "Cold Metal", "FURY", "I LOVE YOU"],
    "2025_STAGE_3": ["The Gatos Guapos", "Nosebleed Esports", "FURY", "Stronghold", "I LOVE YOU", "Cold Metal", "INVADERS", "NewGens"],
    "2026_STAGE_1": ["Team Secret", "The Gatos Guapos", "FURY", "MMY", "Rankers", "Quasar Esports"],
    "2026_STAGE_2": ["SHENGSHI", "Team Secret", "MENG GONG 3", "ELMT", "Najdorf", "Trap12"],
    "2026_STAGE_3": ["CantHear", "Retirement Home", "SeijiKing", "junjilopzfx0764", "TBD", "TBD"]
}

TEAMS_CN = {
    "2025_STAGE_1": ["Once Again", "ROC Esports", "Blade", "Super Levi", "Little Sheep", "Team CC", "Team XX", "Team Equal"],
    "2025_STAGE_2": ["Weibo Gaming", "ROC Esports", "Team CC", "Little Sheep", "Team XX", "Homie E", "ZONES", "Milk Tea"],
    "2025_STAGE_3": ["Weibo Gaming", "ROC Esports", "Team CC", "Milk Tea", "YNB Esports", "boom", "ZONES", "MDY"],
    "2026_STAGE_1": ["Weibo Gaming", "JD Gaming", "All Gamers", "Milk Tea", "Homie E", "DEG", "Solus Victorem", "Naive Piggy"],
    "2026_STAGE_2": ["Weibo Gaming", "JD Gaming", "All Gamers", "Solus Victorem", "HUNENG", "4AM", "ReturnZ", "Kitsune Kage"],
    "2026_STAGE_3": ["Weibo Gaming", "JD Gaming", "All Gamers", "Solus Victorem", "HUNENG", "OU Gaming", "Black Flag", "SHENGSHI"]
}

TEAMS_NA = {
    "2024_STAGE_1": ["Toronto Defiant", "LFO", "Timeless", "Beluga's Platoon", "Students of the Game", "M80", "Luminosity Gaming", "Daybreak", "Shikigami", "BangBangPow Galaxy", "Nah I'd Win", "Pirates in Pyjamas", "Dreamland", "Timeless Obsidian", "Citrus Nation", "Final Gambit"],
    "2024_STAGE_2": ["Toronto Defiant", "M80", "Timeless", "Vice", "FMCL", "Luminosity Gaming", "Pirates in Pyjamas", "DhillDucks", "Visored", "Citrus Nation", "Shikigami", "Nightmare Rotation", "Students of the Game", "UNC INC", "Daybreak", "Who Is Goldfish"],
    "2024_STAGE_3": ["Toronto Defiant", "NRG Shock", "Citrus Nightmare", "NTMR", "Timeless", "Shikigami", "TSM", "Avidity", "Timeless Ethereal", "Arizona State", "FLUFFY AIMERS", "Fries In The Bag", "Team Z", "Vice", "Tanuki Esports", "Absolution"],
    "2024_STAGE_4": ["Toronto Defiant", "NTMR", "NRG Shock", "Citrus Nation", "O3 Splash", "TSM", "FLUFFY AIMERS", "Shikigami", "Tanuki Tapire", "EXN Zenith", "Rammatra Punch", "Absolution", "Team Z", "Rad X Avidity", "Blast Off Buds", "YFP Gaming"],
    "2025_STAGE_1": ["Spacestation Gaming", "Team Liquid", "Timeless", "Avidity", "Rad Esports", "NTMR", "Shikigami", "Amplify"],
    "2025_STAGE_2": ["Geekay Esports", "Spacestation Gaming", "Team Liquid", "NTMR", "Extinction", "Sakura Esports", "Supernova", "DhillDucks"],
    "2025_STAGE_3": ["Geekay Esports", "Spacestation Gaming", "Team Liquid", "NTMR", "Extinction", "Sakura Esports", "Team Z", "DhillDucks"],
    "2026_STAGE_1": ["Dallas Fuel", "disguised", "Spacestation Gaming", "Team Liquid", "LuneX Gaming", "Extinction"],
    "2026_STAGE_2": ["Dallas Fuel", "disguised", "Spacestation Gaming", "Team Liquid", "LuneX Gaming", "The Kafe"],
    "2026_STAGE_3": ["Dallas Fuel", "disguised", "Spacestation Gaming", "Team Liquid", "NTMR", "TBD"]
}

TEAMS_EMEA = {
    "2024_STAGE_1": ["Twisted Minds", "ENCE", "ROC Esports", "Spacestation Gaming", "Ex Oblivione", "Sheer Cold", "Quick Esports", "Team Peps", "nu.age", "LeftRightGnight", "AWW YEAH", "A One Man Army", "Celtas", "Bingus", "EF Flexodiax", "A-Square Tengu"],
    "2024_STAGE_2": ["Spacestation Gaming", "ENCE", "Twisted Minds", "Peace and Love", "Ataraxia", "Deimpero", "Team Peps", "Ex Oblivione", "Supershy", "A One Man Army", "EF Flexodiax", "Metaboiz", "AWW YEAH", "Rocstars", "Sheer Cold", "SCHMUNGUS"],
    "2024_STAGE_3": ["Spacestation Gaming", "ENCE", "Gaimin Gladiators", "Ex Oblivione", "Virtus.pro", "Twisted Minds", "Wasp X Ohhhh No", "Hypnos", "Vendetta", "AWW YEAH", "A One Man Army", "Supershy", "SrPeakCheck", "Al Qadsiah", "Metaboiz", "Ohana Aloha"],
    "2024_STAGE_4": ["ENCE", "Virtus.pro", "Spacestation Gaming", "Twisted Minds", "Piece of Cake", "SrPeakCheck", "Team Peps", "Quick Esports", "Wasp X Ohhhh No", "A One Man Army", "Ex Oblivione", "Team G4mbit", "Negative Mental", "Hypnos", "Metaboiz", "Vendetta"],
    "2025_STAGE_1": ["Gen.G Esports", "Twisted Minds", "Virtus.pro", "The Ultimates", "Sakura Esports", "Team Peps", "Al Qadsiah", "Team Vision"],
    "2025_STAGE_2": ["Virtus.pro", "Al Qadsiah", "The Ultimates", "Twisted Minds", "Gen.G Esports", "Team Peps", "DVSG", "Frost Tails eSport"],
    "2025_STAGE_3": ["Al Qadsiah", "Twisted Minds", "Virtus.pro", "Gen.G Esports", "Team Peps", "Team Vision", "Goud Guys ANM", "Quick Esports"],
    "2026_STAGE_1": ["Team Peps", "Twisted Minds", "Al Qadsiah", "Virtus.pro", "Geekay Esports", "Anyone's Legent"],
    "2026_STAGE_2": ["Twisted Minds", "Al Qadsiah", "Virtus.pro", "Geekay Esports", "1234", "Telacy"],
    "2026_STAGE_3": ["Twisted Minds", "Virtus.pro", "Geekay Esports", "1234", "Team Peps", "TBD"]
}

TEAMS_ASIA = {
    "2024_STAGE_1": {
        "KR#1": "Team Falcons", "KR#2": "Crazy Raccoon", "KR#3": "From The Gamer",
        "JP#1": "VARREL", "JP#2": "INSOMNIA",
        "PA#1": "Honeypot", "PA#2": "DAF", "WILDCARD": "YETI"
    },
    "2024_STAGE_1_WILDCARD": {
        "KR#4": "YETI",
        "JP#3": "SixBlow",
        "PA#3": "321 Diving"
    },
    "2024_STAGE_2": {
        "KR#1": "Team Falcons", "KR#2": "ZETA DIVISION", "KR#3": "Crazy Raccoon",
        "JP#1": "Lazuli", "JP#2": "Nyam Gaming",
        "PA#1": "Bleed Esports", "PA#2": "99DIVINE", "WILDCARD": "Poker Face"
    },
    "2024_STAGE_2_WILDCARD": {
        "KR#4": "Poker Face",
        "JP#3": "VARREL",
        "PA#3": "USIA Esports"
    },
    "2025_STAGE_1": {
        "KR#1": "Crazy Raccoon", "KR#2": "ZETA DIVISION", "KR#3": "WAY", "KR#4": "Team Falcons",
        "JP#1": "VARREL", "JP#2": "VortexWolf",
        "PA#1": "99DIVINE", "PA#2": "MFC"
    },
    "2025_KR_ROAD_TO_WORLD_FINALS": {
        "KR#1": "Crazy Raccoon", "KR#2": "T1", "KR#3": "WAE",
        "KR#4": "ZETA DIVISION", "KR#5": "Team Falcons", "KR#6": "ONSIDE GAMING"
    },
    "2025_JPvsPA_ROAD_TO_WORLD_FINALS": {
        "JP#1": "VARREL", "JP#2": "REJECT",
        "PA#1": "Nosebleed Esports", "PA#2": "The Gatos Guapos"
    },
    "2026_STAGE_1": {
        "KR#1": "ZETA DIVISION", "KR#2": "Team Falcons", "KR#3": "Crazy Raccoon", "KR#4": "T1",
        "JP#1": "VARREL", "JP#2": "ENTER FORCE.36", "JP#3": "Please Not Hero Ban",
        "PA#1": "The Gatos Guapos"
    }
}

LAN_EVENT_TEAMS = {
    "2024 Dallas Major": ["Team Falcons", "Crazy Raccoon", "M80", "Toronto Defiant", "NRG Shock", "ENCE", "Twisted Minds", "Spacestation Gaming"],
    "2024 EWC": [
        "Team Falcons", "Crazy Raccoon", "ZETA DIVISION", "FNATIC", "Toronto Ultra", "M80", "NTMR", "Virtus.pro", "Twisted Minds",
        "Gaimin Gladiators", "ENCE", "Bleed Esports", "LGD.OA", "MKERS", "ROC Esports", "Spacestation Gaming"
    ],
    "2024 World Finals Stockholm": ["Team Falcons", "Crazy Raccoon", "Toronto Defiant", "NRG Shock", "NTMR", "ENCE", "Twisted Minds", "Spacestation Gaming"],
    "2025 Champions Clash Hangzhou": ["NTMR", "Spacestation Gaming", "Virtus.pro", "Al Qadsiah", "Once Again", "Team CC", "Team Falcons", "Crazy Raccoon"],
    "2025 Midseason Championship (EWC)": [
        "Crazy Raccoon", "Team Falcons", "All Gamers Global", "T1", "Twisted Minds", "Al Qadsiah", "Virtus.pro", "Weibo Gaming", "Team CC",
        "ROC Esports", "Team Liquid", "Sign Esports", "Geekay Esports", "VARREL", "The Gatos Guapos", "ZoKorp Esports"
    ],
    "2025 Midseason Championship (EWC) LCQ": [
        "Team Falcons", "ZETA DIVISION", "Cold Metal", "Team Vision", "Aura", "Bright FUture", "INVADERS",
        "FlexaBull", "Force", "LOLARIOUS", "TFW", "Zenith", "ZoneX", "Shock"
    ],
    "2025 World Finals Stockholm": ["Team Falcons", "Crazy Raccoon", "T1", "Twisted Minds", "Al Qadsiah", "Team Peps", "Team Liquid", "Spacestation Gaming",
                          "Geekay Esports", "Weibo Gaming", "Team CC", "VARREL"],
    "2026 Pre-Season Bootcamp": ["Team Falcons", "Crazy Raccoon", "T1", "Twisted Minds", "Team Peps", "Virtus.pro", "Dallas Fuel", "Team Liquid",
                                  "disguised", "Weibo Gaming", "All Gamers", "VARREL"],
    "2026 Champions Clash Tokyo": ["ZETA DIVISION", "Crazy Raccoon", "Twisted Minds", "Virtus.pro", "Weibo Gaming", "All Gamers", "Team Liquid",
                              "Dallas Fuel"],
    "2026 Midseason Championship (EWC)": [
        "ZETA DIVISION", "Crazy Raccoon", "T1", "Team Falcons", "Twisted Minds", "Virtus.pro", "Geekay Esports", "Team Liquid", "Dallas Fuel",
        "Spacestation Gaming", "VARREL", "Team Secret", "Weibo Gaming", "JD Gaming", "All Gamers", "9z Team"
    ],
    "2026 World Finals Guangzhou": []
}

# Updated competition list and metadata
KR_DATES = {
    "2024_STAGE_1": {"START_DATE":"2024-03-01","END_DATE":"2024-04-07","TEAMS":"8","PRIZE":"$45,000","VENUE":"WDG eSports Studio","LOCATION":"Seoul, South Korea (WDG eSports Studio)","1st":"Team Falcons","2nd":"WAC"},
    "2024_STAGE_2": {"START_DATE":"2024-08-09","END_DATE":"2024-09-15","TEAMS":"8","PRIZE":"$48,000","VENUE":"WDG eSports Studio","LOCATION":"Seoul, South Korea (WDG eSports Studio)","1st":"Team Falcons","2nd":"ZETA DIVISION"},
    "2025_STAGE_1": {"START_DATE":"2025-02-14","END_DATE":"2025-03-23","TEAMS":"9","PRIZE":"$51,500","VENUE":"WDG eSports Studio Hongdae","LOCATION":"Seoul, South Korea (WDG eSports Studio Hongdae)","1st":"Crazy Raccoon","2nd":"Team Falcons"},
    "2025_STAGE_2": {"START_DATE":"2025-05-09","END_DATE":"2025-06-22","TEAMS":"9","PRIZE":"$51,500","VENUE":"WDG eSports Studio Hongdae","LOCATION":"Seoul, South Korea (WDG eSports Studio Hongdae)","1st":"Crazy Raccoon","2nd":"T1"},
    "2025_STAGE_3": {"START_DATE":"2025-08-29","END_DATE":"2025-10-12","TEAMS":"9","PRIZE":"$51,500","VENUE":"WDG eSports Studio Hongdae","LOCATION":"Seoul, South Korea (WDG eSports Studio Hongdae)","1st":"Crazy Raccoon","2nd":"T1"},
    "2026_STAGE_1": {"START_DATE":"2026-03-20","END_DATE":"2026-05-03","TEAMS":"9","PRIZE":"$38,500","VENUE":"WDG eSports Studio Hongdae","LOCATION":"Seoul, South Korea (WDG eSports Studio Hongdae)","1st":"ZETA DIVISION","2nd":"Team Falcons"},
    "2026_STAGE_2": {"START_DATE":"2026-06-05","END_DATE":"2026-07-12","TEAMS":"9","PRIZE":"$38,500","VENUE":"WDG eSports Studio Hongdae","LOCATION":"Seoul, South Korea (WDG eSports Studio Hongdae)","1st":"ZETA DIVISION","2nd":"Crazy Raccoon"},
    "2026_STAGE_3": {"START_DATE":"2026-10-02","END_DATE":"2026-11-08","TEAMS":"9","PRIZE":"TBD","VENUE":"WDG eSports Studio Hongdae","LOCATION":"Seoul, South Korea (WDG eSports Studio Hongdae)","1st":"TBD","2nd":"TBD"}
}

JP_DATES = {
    "2024_STAGE_1": {"START_DATE":"2024-02-26","END_DATE":"2024-04-03","TEAMS":"9","PRIZE":"$27,500","LOCATION":"Japan (Online)","1st":"VARREL","2nd":"INSOMNIA"},
    "2024_STAGE_2": {"START_DATE":"2024-08-12","END_DATE":"2024-09-15","TEAMS":"8","PRIZE":"$24,500","LOCATION":"Japan (Online)","1st":"Lazuli","2nd":"Nyam Gaming"},
    "2025_STAGE_1": {"START_DATE":"2025-01-27","END_DATE":"2025-03-02","TEAMS":"12","PRIZE":"$20,000","LOCATION":"Japan (Online)","1st":"VARREL","2nd":"VortexWolf"},
    "2025_STAGE_2": {"START_DATE":"2025-05-12","END_DATE":"2025-06-22","TEAMS":"12","PRIZE":"$33,500","LOCATION":"Japan (Online)","1st":"VARREL","2nd":"REJECT"},
    "2025_STAGE_3": {"START_DATE":"2025-08-25","END_DATE":"2025-10-04","TEAMS":"12","PRIZE":"$33,500","LOCATION":"Japan (Online)","1st":"VARREL","2nd":"REJECT"},
    "2026_STAGE_1": {"START_DATE":"2026-03-16","END_DATE":"2026-04-14","TEAMS":"8","PRIZE":"$18,500","LOCATION":"Japan (Online)","1st":"VARREL","2nd":"ENTER FORCE.36"},
    "2026_STAGE_2": {"START_DATE":"2026-06-01","END_DATE":"2026-06-30","TEAMS":"8","PRIZE":"$18,500","LOCATION":"Japan (Online)","1st":"VARREL","2nd":"MURASH GAMING"},
    "2026_STAGE_3": {"START_DATE":"2026-09-21","END_DATE":"2026-10-20","TEAMS":"8","PRIZE":"TBD","LOCATION":"Japan (Online)","1st":"TBD","2nd":"TBD"}
}

PA_DATES = {
    "2024_STAGE_1": {"START_DATE":"2024-02-29","END_DATE":"2024-03-28","TEAMS":"8","PRIZE":"$17,500","LOCATION":"Pacific (Online)","1st":"Honeypot","2nd":"DAF"},
    "2024_STAGE_2": {"START_DATE":"2024-08-08","END_DATE":"2024-09-05","TEAMS":"8","PRIZE":"$20,500","LOCATION":"Pacific (Online)","1st":"Bleed Esports","2nd":"99DIVINE"},
    "2025_STAGE_1": {"START_DATE":"2025-01-30","END_DATE":"2025-03-04","TEAMS":"8","PRIZE":"$15,000","LOCATION":"Pacific (Online)","1st":"99DIVINE","2nd":"MFC"},
    "2025_STAGE_2": {"START_DATE":"2025-05-15","END_DATE":"2025-06-19","TEAMS":"8","PRIZE":"$15,000","LOCATION":"Pacific (Online)","1st":"The Gatos Guapos","2nd":"99DIVINE"},
    "2025_STAGE_3": {"START_DATE":"2025-08-28","END_DATE":"2025-10-02","TEAMS":"8","PRIZE":"$15,000","LOCATION":"Pacific (Online)","1st":"Nosebleed Esports","2nd":"The Gatos Guapos"},
    "2026_STAGE_1": {"START_DATE":"2026-03-26","END_DATE":"2026-04-30","TEAMS":"6","PRIZE":"$7,000","LOCATION":"Pacific (Online)","1st":"The Gatos Guapos","2nd":"Team Secret"},
    "2026_STAGE_2": {"START_DATE":"2026-06-04","END_DATE":"2026-07-09","TEAMS":"6","PRIZE":"$7,000","LOCATION":"Pacific (Online)","1st":"Team Secret","2nd":"SHENGSHI Esports"},
    "2026_STAGE_3": {"START_DATE":"2026-10-26","END_DATE":"2026-11-03","TEAMS":"6","PRIZE":"TBD","LOCATION":"Pacific (Online)","1st":"TBD","2nd":"TBD"}
}

CN_DATES = {
    "2025_STAGE_1": {"START_DATE":"2025-03-27","END_DATE":"2025-04-06","TEAMS":"8","PRIZE":"$96,133","LOCATION":"China (Online / Lan)","1st":"Once Again","2nd":"Team CC"},
    "2025_STAGE_2": {"START_DATE":"2025-05-24","END_DATE":"2025-06-29","TEAMS":"8","PRIZE":"$97,595","LOCATION":"China (Online / Lan)","1st":"Weibo Gaming","2nd":"Team CC"},
    "2025_STAGE_3": {"START_DATE":"2025-09-06","END_DATE":"2025-10-12","TEAMS":"8","PRIZE":"$98,387","LOCATION":"China (Online / Lan)","1st":"Weibo Gaming","2nd":"Team CC"},
    "2026_STAGE_1": {"START_DATE":"2026-03-21","END_DATE":"2026-04-26","TEAMS":"8","PRIZE":"$102,395","LOCATION":"China (Online / Lan)","1st":"Weibo Gaming","2nd":"All Gamers"},
    "2026_STAGE_2": {"START_DATE":"2026-06-06","END_DATE":"2026-07-05","TEAMS":"8","PRIZE":"$103,106","LOCATION":"China (Online / Lan)","1st":"Weibo Gaming","2nd":"JD Gaming"},
    "2026_STAGE_3": {"START_DATE":"2026-10-03","END_DATE":"2026-11-08","TEAMS":"8","PRIZE":"TBD","LOCATION":"China (Online / Lan)","1st":"TBD","2nd":"TBD"}
}

NA_DATES = {
    "2024_STAGE_1": {"START_DATE":"2024-03-01","END_DATE":"2024-03-24","TEAMS":"16","PRIZE":"$75,000","LOCATION":"North America (Online)","1st":"Toronto Defiant","2nd":"Timeless"},
    "2024_STAGE_2": {"START_DATE":"2024-04-05","END_DATE":"2024-04-28","TEAMS":"16","PRIZE":"$75,000","LOCATION":"North America (Online)","1st":"Toronto Defiant","2nd":"M80"},
    "2024_STAGE_3": {"START_DATE":"2024-08-09","END_DATE":"2024-09-01","TEAMS":"16","PRIZE":"$75,000","LOCATION":"North America (Online)","1st":"Toronto Defiant","2nd":"NRG Shock"},
    "2024_STAGE_4": {"START_DATE":"2024-09-20","END_DATE":"2024-10-13","TEAMS":"16","PRIZE":"$75,000","LOCATION":"North America (Online)","1st":"Toronto Defiant","2nd":"NTMR"},
    "2025_STAGE_1": {"START_DATE":"2025-01-31","END_DATE":"2025-03-09","TEAMS":"8","PRIZE":"$100,000","LOCATION":"North America (Online)","1st":"NTMR","2nd":"Spacestation Gaming"},
    "2025_STAGE_2": {"START_DATE":"2025-05-10","END_DATE":"2025-06-29","TEAMS":"8","PRIZE":"$100,000","LOCATION":"North America (Online)","1st":"Geekay Esports","2nd":"Team Liquid"},
    "2025_STAGE_3": {"START_DATE":"2025-09-06","END_DATE":"2025-10-26","TEAMS":"8","PRIZE":"$100,000","LOCATION":"North America (Online)","1st":"Team Liquid","2nd":"Spacestation Gaming"},
    "2026_STAGE_1": {"START_DATE":"2026-03-21","END_DATE":"2026-04-12","TEAMS":"6","PRIZE":"$75,000","LOCATION":"North America (Online)","1st":"Dallas Fuel","2nd":"Spacestation Gaming"},
    "2026_STAGE_2": {"START_DATE":"2026-06-13","END_DATE":"2026-07-05","TEAMS":"6","PRIZE":"$75,000","LOCATION":"North America (Online)","1st":"Dallas Fuel","2nd":"Spacestation Gaming"},
    "2026_STAGE_3": {"START_DATE":"2026-10-10","END_DATE":"2026-11-01","TEAMS":"6","PRIZE":"$75,000","LOCATION":"North America (Online)","1st":"TBD","2nd":"TBD"}
}

EMEA_DATES = {
    "2024_STAGE_1": {"START_DATE":"2024-03-01","END_DATE":"2024-03-24","TEAMS":"16","PRIZE":"$75,000","LOCATION":"EMEA (Online)","1st":"Twisted Minds","2nd":"ENCE"},
    "2024_STAGE_2": {"START_DATE":"2024-04-05","END_DATE":"2024-04-28","TEAMS":"16","PRIZE":"$75,000","LOCATION":"EMEA (Online)","1st":"Spacestation Gaming","2nd":"ENCE"},
    "2024_STAGE_3": {"START_DATE":"2024-08-09","END_DATE":"2024-09-01","TEAMS":"16","PRIZE":"$75,000","LOCATION":"EMEA (Online)","1st":"ENCE","2nd":"Virtus.pro"},
    "2024_STAGE_4": {"START_DATE":"2024-09-20","END_DATE":"2024-10-13","TEAMS":"16","PRIZE":"$75,000","LOCATION":"EMEA (Online)","1st":"Spacestation Gaming","2nd":"ENCE"},
    "2025_STAGE_1": {"START_DATE":"2025-01-31","END_DATE":"2025-03-09","TEAMS":"8","PRIZE":"$100,000","LOCATION":"EMEA (Online)","1st":"Virtus.pro","2nd":"Al Qadsiah"},
    "2025_STAGE_2": {"START_DATE":"2025-05-10","END_DATE":"2025-06-29","TEAMS":"8","PRIZE":"$100,000","LOCATION":"EMEA (Online)","1st":"Al Qadsiah","2nd":"Twisted Minds"},
    "2025_STAGE_3": {"START_DATE":"2025-09-06","END_DATE":"2025-10-26","TEAMS":"8","PRIZE":"$100,000","LOCATION":"EMEA (Online)","1st":"Twisted Minds","2nd":"Al Qadsiah"},
    "2026_STAGE_1": {"START_DATE":"2026-03-21","END_DATE":"2026-04-12","TEAMS":"6","PRIZE":"$75,000","LOCATION":"EMEA (Online)","1st":"Twisted Minds","2nd":"Virtus.pro"},
    "2026_STAGE_2": {"START_DATE":"2026-06-13","END_DATE":"2026-07-05","TEAMS":"6","PRIZE":"$75,000","LOCATION":"EMEA (Online)","1st":"Virtus.pro","2nd":"Geekay Esports"},
    "2026_STAGE_3": {"START_DATE":"2026-10-10","END_DATE":"2026-11-01","TEAMS":"6","PRIZE":"$75,000","LOCATION":"EMEA (Online)","1st":"TBD","2nd":"TBD"}
}

ASIA_DATES = {
    "2024_STAGE_1_WILDCARD": {"START_DATE":"2024-04-08","END_DATE":"2024-04-14","TEAMS":"3","PRIZE":"QUALIFIER","VENUE":"Online","LOCATION":"Asia (Online)","1st":"YETI","2nd":"SixBlow"},
    "2024_STAGE_1": {"START_DATE":"2024-04-25","END_DATE":"2024-04-28","TEAMS":"8","PRIZE":"$60,000","VENUE":"WDG eSports Studio","LOCATION":"Seoul, South Korea (WDG eSports Studio)","1st":"Crazy Raccoon","2nd":"Team Falcons"},
    "2024_STAGE_2_WILDCARD": {"START_DATE":"2024-09-13","END_DATE":"2024-09-15","TEAMS":"3","PRIZE":"QUALIFIER","VENUE":"Online","LOCATION":"Asia (Online)","1st":"Poker Face","2nd":"VARREL"},
    "2024_STAGE_2": {"START_DATE":"2024-09-27","END_DATE":"2024-10-05","TEAMS":"8","PRIZE":"$60,000","VENUE":"WDG eSports Studio","LOCATION":"Seoul, South Korea (WDG eSports Studio)","1st":"Team Falcons","2nd":"Crazy Raccoon"},
    "2025_STAGE_1": {"START_DATE":"2025-03-06","END_DATE":"2025-03-16","TEAMS":"8","PRIZE":"$35,000","VENUE":"WDG eSports Studio Hongdae","LOCATION":"Seoul, South Korea (WDG eSports Studio Hongdae)","1st":"Team Falcons","2nd":"Crazy Raccoon"},
    "2025_STAGE_3_KR": {"START_DATE":"2025-10-24","END_DATE":"2025-10-26","TEAMS":"6","PRIZE":"QUALIFIER","VENUE":"WDG eSports Studio Hongdae","LOCATION":"Seoul, South Korea (WDG eSports Studio Hongdae)","1st":"Crazy Raccoon","2nd":"Team Falcons"},
    "2025_STAGE_3_JPvsPA": {"START_DATE":"2025-10-24","END_DATE":"2025-10-25","TEAMS":"4","PRIZE":"QUALIFIER","VENUE":"Online / Lan","LOCATION":"Tokyo, Japan (Online / Lan)","1st":"VARREL","2nd":"Nosebleed Esports"},
    "2026_STAGE_1": {"START_DATE":"2026-05-05","END_DATE":"2026-05-10","TEAMS":"8","PRIZE":"QUALIFIER","VENUE":"WDG eSports Studio Hongdae","LOCATION":"Seoul, South Korea (WDG eSports Studio Hongdae)","1st":"ZETA DIVISION","2nd":"Crazy Raccoon"}
}

LAN_EVENT_DATES = {
    "2024 DALLAS": {
        "START_DATE": "2024-05-31",
        "END_DATE": "2024-06-02",
        "VENUE": "Kay Bailey Hutchison Convention Center (Dreamhack Dallas)",
        "LOCATION": "Dallas, United States 🇺🇸",
        "TEAMS": "8",
        "PRIZE": "$250,000",
        "1st": "Crazy Raccoon",
        "2nd": "Team Falcons",
        "match_key": "2024 Dallas Major"
    },
    "2024 EWC": {
        "START_DATE": "2024-07-24",
        "END_DATE": "2024-07-28",
        "VENUE": "Boulevard Riyadh City, Qiddiya Arena",
        "LOCATION": "Riyadh, Saudi Arabia 🇸🇦",
        "TEAMS": "16",
        "PRIZE": "$1,050,000",
        "1st": "Crazy Raccoon",
        "2nd": "Toronto Ultra",
        "match_key": "2024 EWC"
    },
    "2024 World Finals Stockholm": {
        "START_DATE": "2024-11-22",
        "END_DATE": "2024-11-24",
        "VENUE": "Stockholmsmässan (Dreamhack Stockholm)",
        "LOCATION": "Stockholm, Sweden 🇸🇪",
        "TEAMS": "8",
        "PRIZE": "$500,000",
        "1st": "Team Falcons",
        "2nd": "Crazy Raccoon",
        "match_key": "2024 World Finals Stockholm"
    },
    "2025 Champions Clash Hangzhou": {
        "START_DATE": "2025-04-18",
        "END_DATE": "2025-04-20",
        "VENUE": "Hangzhou Esports Center",
        "LOCATION": "Hangzhou, China 🇨🇳",
        "TEAMS": "8",
        "PRIZE": "$260,000",
        "1st": "Crazy Raccoon",
        "2nd": "Team Falcons",
        "match_key": "2025 Champions Clash Hangzhou"
    },
    "2025 Midseason Championship (EWC) LCQ": {
        "START_DATE": "2025-07-17",
        "END_DATE": "2025-07-19",
        "VENUE": "Boulevard Riyadh City, stc Esports Arena",
        "LOCATION": "Riyadh, Saudi Arabia 🇸🇦",
        "TEAMS": "14",
        "PRIZE": "$89,000",
        "1st": "Team Falcons",
        "2nd": "ZETA DIVISION",
        "match_key": "2025 Midseason Championship (EWC) LCQ"
    },
    "2025 Midseason Championship (EWC)": {
        "START_DATE": "2025-07-31",
        "END_DATE": "2025-08-03",
        "VENUE": "Boulevard Riyadh City, stc Esports Arena",
        "LOCATION": "Riyadh, Saudi Arabia 🇸🇦",
        "TEAMS": "16",
        "PRIZE": "$1,060,000",
        "1st": "Team Falcons",
        "2nd": "Al Qadsiah",
        "match_key": "2025 Midseason Championship (EWC)"
    },
    "2025 World Finals Stockholm": {
        "START_DATE": "2025-11-26",
        "END_DATE": "2025-11-30",
        "VENUE": "ESL / Dreamhack Studios (Day 1,2) | Stockholmsmässan (Day 3-5)",
        "LOCATION": "Stockholm, Sweden 🇸🇪",
        "TEAMS": "12",
        "PRIZE": "$500,000",
        "1st": "Twisted Minds",
        "2nd": "Al Qadsiah",
        "match_key": "2025 World Finals Stockholm"
    },
    "2026 Pre-Season Bootcamp": {
        "START_DATE": "2026-02-13",
        "END_DATE": "2026-02-15",
        "VENUE": "WDG Studio Hongdae",
        "LOCATION": "Seoul, South Korea 🇰🇷",
        "TEAMS": "12",
        "PRIZE": "$25,000",
        "1st": "Twisted Minds",
        "2nd": "Crazy Raccoon",
        "match_key": "2026 Pre-Season Bootcamp"
    },
    "2026 Champions Clash Tokyo": {
        "START_DATE": "2026-05-22",
        "END_DATE": "2026-05-24",
        "VENUE": "Arena Tachikawa Tachihi",
        "LOCATION": "Tokyo, Japan 🇯🇵",
        "TEAMS": "8",
        "PRIZE": "$250,000",
        "1st": "Crazy Raccoon",
        "2nd": "Twisted Minds",
        "match_key": "2026 Champions Clash Tokyo"
    },
    "2026 Midseason Championship (EWC)": {
        "START_DATE": "2026-07-29",
        "END_DATE": "2026-08-02",
        "VENUE": "Paris Expo Porte de Versailles, stc Arena",
        "LOCATION": "Paris, France 🇫🇷",
        "TEAMS": "16",
        "PRIZE": "$1,000,000",
        "1st": "ZETA DIVISION",
        "2nd": "Twisted Minds",
        "match_key": "2026 Midseason Championship (EWC)"
    },
    "2026 World Finals Guangzhou": {
        "START_DATE": "2026-12-02",
        "END_DATE": "2026-12-06",
        "VENUE": "Guangzhou Gymnasium",
        "LOCATION": "Guangzhou, China 🇨🇳",
        "TEAMS": "TBD",
        "PRIZE": "TBD",
        "1st": "TBD",
        "2nd": "TBD",
        "match_key": "2026 World Finals Guangzhou"
    }
}

def parse_prize_num(prize_str):
    if not prize_str or "TBD" in str(prize_str).upper() or "QUALIFIER" in str(prize_str).upper():
        return 0
    clean = str(prize_str).replace("$", "").replace(",", "").strip()
    try:
        return int(clean)
    except:
        return 0

def format_prize_str(prize_str):
    if not prize_str or "TBD" in str(prize_str).upper():
        return "TBD"
    if "QUALIFIER" in str(prize_str).upper():
        return "Qualifier (Seeds Only)"
    num = parse_prize_num(prize_str)
    if num > 0:
        return f"${num:,}"
    return str(prize_str)

def build_tournament_dataset():
    tournaments = []

    # 1. Global LAN Events
    for key, meta in LAN_EVENT_DATES.items():
        m_key = meta.get("match_key") or key
        teams = LAN_EVENT_TEAMS.get(m_key, [])
        if not teams:
            # Fallback direct lookup
            teams = LAN_EVENT_TEAMS.get(key, [])

        year = int(meta["START_DATE"][:4])
        tier = "World Finals" if "World Finals" in key else "Major" if ("Major" in key or "EWC" in key or "Champions Clash" in key or "Midseason" in key) else "Invitational" if "Bootcamp" in key else "Qualifier"
        
        t_id = "lan-" + key.lower().replace(" ", "-").replace("(", "").replace(")", "").replace(".", "")
        tournaments.append({
            "id": t_id,
            "name": f"OWCS {key}",
            "nameKo": f"OWCS {key}",
            "category": "LAN",
            "region": "GLOBAL",
            "regionIcon": "🌍",
            "year": year,
            "tier": tier,
            "startDate": meta["START_DATE"],
            "endDate": meta["END_DATE"],
            "venue": meta.get("VENUE", "Offline Arena"),
            "location": meta.get("LOCATION", "Global"),
            "prize": format_prize_str(meta.get("PRIZE")),
            "prizeNum": parse_prize_num(meta.get("PRIZE")),
            "champion": meta.get("1st", "TBD"),
            "runnerUp": meta.get("2nd", "TBD"),
            "teamCount": len(teams) if teams else (int(meta["TEAMS"]) if meta["TEAMS"].isdigit() else 0),
            "teams": teams,
            "isLAN": True
        })

    # 2. Regional Stages
    regional_configs = [
        ("KR", "OWCS Korea", "OWCS 코리아", "🇰🇷", TEAMS_KR, KR_DATES, "SEOUL, SOUTH KOREA"),
        ("JP", "OWCS Japan", "OWCS 재팬", "🇯🇵", TEAMS_JP, JP_DATES, "Tokyo, Japan"),
        ("PA", "OWCS Pacific", "OWCS 퍼시픽", "🌏", TEAMS_PA, PA_DATES, "Pacific"),
        ("CN", "OWCS China", "OWCS 차이나", "🇨🇳", TEAMS_CN, CN_DATES, "China"),
        ("NA", "OWCS North America", "OWCS 북미", "🇺🇸", TEAMS_NA, NA_DATES, "North America"),
        ("EMEA", "OWCS EMEA", "OWCS 유럽·중동", "🇪🇺", TEAMS_EMEA, EMEA_DATES, "Europe & Middle East"),
    ]

    for reg_code, reg_name_en, reg_name_ko, reg_icon, teams_dict, dates_dict, default_loc in regional_configs:
        for stage_key, date_meta in dates_dict.items():
            teams = teams_dict.get(stage_key, [])
            parts = stage_key.split("_")
            year = int(parts[0])
            stage_num = parts[2] if len(parts) >= 3 else "1"
            display_title = f"{reg_name_en} {year} Stage {stage_num}"
            display_title_ko = f"{reg_name_ko} {year} 스테이지 {stage_num}"
            t_id = f"{reg_code.lower()}-{year}-s{stage_num}"
            
            tournaments.append({
                "id": t_id,
                "name": display_title,
                "nameKo": display_title_ko,
                "category": reg_code,
                "region": reg_code,
                "regionIcon": reg_icon,
                "year": year,
                "tier": "Regional Stage",
                "startDate": date_meta["START_DATE"],
                "endDate": date_meta["END_DATE"],
                "venue": date_meta.get("VENUE") or ("WDG eSports Studio" if year == 2024 else "WDG eSports Studio Hongdae" if reg_code == "KR" else default_loc),
                "location": date_meta.get("LOCATION", default_loc),
                "prize": format_prize_str(date_meta.get("PRIZE")),
                "prizeNum": parse_prize_num(date_meta.get("PRIZE")),
                "champion": date_meta.get("1st", "TBD"),
                "runnerUp": date_meta.get("2nd", "TBD"),
                "teamCount": len(teams) if teams else (int(date_meta["TEAMS"]) if date_meta["TEAMS"].isdigit() else 0),
                "teams": teams,
                "isLAN": False
            })

    # 3. Asia Tournaments & Wildcards
    for stage_key, date_meta in ASIA_DATES.items():
        parts = stage_key.split("_")
        year = int(parts[0])
        teams_data = TEAMS_ASIA.get(stage_key, {})
        if isinstance(teams_data, dict):
            teams_list = [f"{v} ({k})" for k, v in teams_data.items()]
            clean_teams = list(teams_data.values())
        else:
            teams_list = teams_data
            clean_teams = teams_data

        sub_name = stage_key.replace(f"{year}_", "").replace("_", " ")
        t_id = f"asia-{year}-{sub_name.lower().replace(' ', '-')}"
        tier = "Major Qualifier" if ("WILDCARD" in stage_key or "ROAD" in stage_key) else "Regional Championship"
        
        tournaments.append({
            "id": t_id,
            "name": f"OWCS Asia {year} {sub_name}",
            "nameKo": f"OWCS 아시아 {year} {sub_name}",
            "category": "ASIA",
            "region": "ASIA",
            "regionIcon": "🌏",
            "year": year,
            "tier": tier,
            "startDate": date_meta["START_DATE"],
            "endDate": date_meta["END_DATE"],
            "venue": date_meta.get("VENUE") or ("WDG eSports Studio" if year == 2024 else "WDG eSports Studio Hongdae"),
            "location": date_meta.get("LOCATION", "Asia"),
            "prize": format_prize_str(date_meta.get("PRIZE")),
            "prizeNum": parse_prize_num(date_meta.get("PRIZE")),
            "champion": date_meta.get("1st", "TBD"),
            "runnerUp": date_meta.get("2nd", "TBD"),
            "teamCount": len(clean_teams) if clean_teams else (int(date_meta["TEAMS"]) if date_meta["TEAMS"].isdigit() else 0),
            "teams": clean_teams,
            "seedTeams": teams_list if isinstance(teams_data, dict) else [],
            "isLAN": "WDG" in date_meta.get("LOCATION", "")
        })

    # Sort all tournaments chronologically by startDate
    tournaments.sort(key=lambda x: x["startDate"])

    # Compute global summary metrics
    total_tournaments = len(tournaments)
    total_prize_usd = sum(t["prizeNum"] for t in tournaments)
    
    # Leaderboard: Champions and Runner-ups
    champ_counts = {}
    podium_counts = {}
    for t in tournaments:
        c = t["champion"]
        r = t["runnerUp"]
        if c and c != "TBD" and c != "TBA":
            champ_counts[c] = champ_counts.get(c, 0) + 1
            podium_counts[c] = podium_counts.get(c, 0) + 1
        if r and r != "TBD" and r != "TBA":
            podium_counts[r] = podium_counts.get(r, 0) + 1

    sorted_champs = sorted(champ_counts.items(), key=lambda x: x[1], reverse=True)
    sorted_podium = sorted(podium_counts.items(), key=lambda x: x[1], reverse=True)

    category_prizes = {}
    for t in tournaments:
        cat = t["category"]
        category_prizes[cat] = category_prizes.get(cat, 0) + t["prizeNum"]

    summary = {
        "totalTournaments": total_tournaments,
        "totalPrizeUsd": total_prize_usd,
        "totalPrizeUsdFormatted": f"${total_prize_usd:,}",
        "years": sorted(list(set(t["year"] for t in tournaments))),
        "categories": [
            {"code": "ALL", "nameKo": "전체 대회", "nameEn": "All Tournaments", "icon": "🌐", "prizeUsd": total_prize_usd, "prizeFormatted": f"${total_prize_usd:,}"},
            {"code": "LAN", "nameKo": "글로벌 LAN 메이저", "nameEn": "Global LAN Events", "icon": "🌍", "prizeUsd": category_prizes.get("LAN", 0), "prizeFormatted": f"${category_prizes.get('LAN', 0):,}"},
            {"code": "KR", "nameKo": "한국 (Korea)", "nameEn": "Korea", "icon": "🇰🇷", "prizeUsd": category_prizes.get("KR", 0), "prizeFormatted": f"${category_prizes.get('KR', 0):,}"},
            {"code": "NA", "nameKo": "북미 (North America)", "nameEn": "North America", "icon": "🇺🇸", "prizeUsd": category_prizes.get("NA", 0), "prizeFormatted": f"${category_prizes.get('NA', 0):,}"},
            {"code": "EMEA", "nameKo": "유럽·중동 (EMEA)", "nameEn": "Europe & Middle East", "icon": "🇪🇺", "prizeUsd": category_prizes.get("EMEA", 0), "prizeFormatted": f"${category_prizes.get('EMEA', 0):,}"},
            {"code": "CN", "nameKo": "중국 (China)", "nameEn": "China", "icon": "🇨🇳", "prizeUsd": category_prizes.get("CN", 0), "prizeFormatted": f"${category_prizes.get('CN', 0):,}"},
            {"code": "JP", "nameKo": "일본 (Japan)", "nameEn": "Japan", "icon": "🇯🇵", "prizeUsd": category_prizes.get("JP", 0), "prizeFormatted": f"${category_prizes.get('JP', 0):,}"},
            {"code": "ASIA", "nameKo": "아시아 본선", "nameEn": "Asia Main", "icon": "🌏", "prizeUsd": category_prizes.get("ASIA", 0), "prizeFormatted": f"${category_prizes.get('ASIA', 0):,}"},
            {"code": "PA", "nameKo": "태평양 (Pacific)", "nameEn": "Pacific", "icon": "🌏", "prizeUsd": category_prizes.get("PA", 0), "prizeFormatted": f"${category_prizes.get('PA', 0):,}"}
        ],
        "topChampions": [{"team": team, "titles": count} for team, count in sorted_champs[:12]],
        "topPodiums": [{"team": team, "finals": count} for team, count in sorted_podium[:12]],
    }

    return {
        "summary": summary,
        "tournaments": tournaments
    }

def main():
    data = build_tournament_dataset()
    js_content = "window.OWCS_TOURNAMENT_DATABASE = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"✅ Generated {OUT_FILE} with {len(data['tournaments'])} tournaments.")
    print(f"   Total Cumulative Prize Pool: {data['summary']['totalPrizeUsdFormatted']}")
    print(f"   Top Champions: {data['summary']['topChampions'][:5]}")

if __name__ == "__main__":
    main()
