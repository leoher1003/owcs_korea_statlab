#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_stage2_data.py
Updates OWCS_STAT_LAB_26_KR_STAGE2_RECALCULATED.xlsx and data.js with:
- Title Case hero names for TEAM 1 BAN and TEAM 2 BAN
- Detail scores (TEAM 1 SCORE, TEAM 2 SCORE, DETAIL_SCORE) from Liquipedia stage2_matches.json
- Preserves all formulas and existing statistical integrity
"""

import json
import re
import openpyxl

HERO_CANONICAL_MAP = {
    "d.va": "D.Va",
    "dva": "D.Va",
    "lucio": "Lucio",
    "lúcio": "Lucio",
    "wrecking ball": "Wrecking Ball",
    "junker queen": "Junker Queen",
    "soldier: 76": "Soldier: 76",
    "soldier 76": "Soldier: 76",
    "jetpack cat": "Jetpack Cat",
    "torbjorn": "Torbjörn",
    "torbjörn": "Torbjörn",
}

def format_hero_name(raw):
    if not raw:
        return ""
    clean = str(raw).strip()
    low = clean.lower()
    if low in HERO_CANONICAL_MAP:
        return HERO_CANONICAL_MAP[low]
    return " ".join(w.capitalize() for w in clean.split())

def update_stage2_excel():
    xlsx_path = "OWCS_STAT_LAB_26_KR_STAGE2_RECALCULATED.xlsx"
    json_path = "owcs-stat-lab 2/data/stage2_matches.json"
    
    with open(json_path, "r", encoding="utf-8") as f:
        lq_matches = json.load(f)
        
    # Build map lookup: (team1, team2, map_name) -> set detail
    lq_map_lookup = {}
    for m in lq_matches:
        t1, t2 = m["team1"], m["team2"]
        for s in m["sets"]:
            key = (t1, t2, s["map"].strip().lower())
            key_rev = (t2, t1, s["map"].strip().lower())
            lq_map_lookup[key] = (s, False) # not reversed
            lq_map_lookup[key_rev] = (s, True) # reversed
            
    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb["MATCH INFO"]
    
    # Check headers
    headers = [cell.value for cell in ws[1]]
    col_t1_ban = headers.index("TEAM 1 BAN") + 1
    col_t2_ban = headers.index("TEAM 2 BAN") + 1
    
    # Add new columns if not present
    if "TEAM 1 SCORE" not in headers:
        headers.extend(["TEAM 1 SCORE", "TEAM 2 SCORE", "INITIAL BAN RIGHT", "INITIAL BAN"])
        for c_idx, h_name in enumerate(["TEAM 1 SCORE", "TEAM 2 SCORE", "INITIAL BAN RIGHT", "INITIAL BAN"], start=len(headers)-3):
            ws.cell(row=1, column=c_idx, value=h_name)
            
    col_t1_score = headers.index("TEAM 1 SCORE") + 1
    col_t2_score = headers.index("TEAM 2 SCORE") + 1
    col_ban_right = headers.index("INITIAL BAN RIGHT") + 1
    col_init_ban = headers.index("INITIAL BAN") + 1
    
    updated_rows = 0
    matched_scores = 0
    
    for row in range(2, ws.max_row + 1):
        t1 = ws.cell(row=row, column=7).value # TEAM 1
        t2 = ws.cell(row=row, column=8).value # TEAM 2
        map_val = ws.cell(row=row, column=9).value # MAP
        
        # 1. Title Case Bans
        b1 = ws.cell(row=row, column=col_t1_ban).value
        b2 = ws.cell(row=row, column=col_t2_ban).value
        if b1:
            ws.cell(row=row, column=col_t1_ban, value=format_hero_name(b1))
        if b2:
            ws.cell(row=row, column=col_t2_ban, value=format_hero_name(b2))
            
        # 2. Match with Liquipedia data
        if t1 and t2 and map_val:
            lookup_key = (str(t1).strip(), str(t2).strip(), str(map_val).strip().lower())
            if lookup_key in lq_map_lookup:
                s_info, is_rev = lq_map_lookup[lookup_key]
                matched_scores += 1
                
                sc1 = s_info["score1"]
                sc2 = s_info["score2"]
                if is_rev:
                    sc1, sc2 = sc2, sc1
                    
                try:
                    sc1_val = float(sc1) if "." in str(sc1) else int(sc1)
                except:
                    sc1_val = sc1
                try:
                    sc2_val = float(sc2) if "." in str(sc2) else int(sc2)
                except:
                    sc2_val = sc2
                    
                ws.cell(row=row, column=col_t1_score, value=sc1_val)
                ws.cell(row=row, column=col_t2_score, value=sc2_val)
                
                b_start = s_info.get("banStart", "")
                if b_start:
                    if (b_start == "1" and not is_rev) or (b_start == "2" and is_rev):
                        ws.cell(row=row, column=col_ban_right, value="TEAM 1")
                        ws.cell(row=row, column=col_init_ban, value=format_hero_name(s_info["team1Ban"] if not is_rev else s_info["team2Ban"]))
                    else:
                        ws.cell(row=row, column=col_ban_right, value="TEAM 2")
                        ws.cell(row=row, column=col_init_ban, value=format_hero_name(s_info["team2Ban"] if not is_rev else s_info["team1Ban"]))
                        
        updated_rows += 1
        
    wb.save(xlsx_path)
    print(f"Stage 2 Excel updated: {updated_rows} rows processed, {matched_scores} map scores matched.")

def update_stage2_data_js():
    js_path = "owcs-stat-lab 2/data/data.js"
    json_path = "owcs-stat-lab 2/data/stage2_matches.json"
    
    with open(json_path, "r", encoding="utf-8") as f:
        lq_matches = json.load(f)
        
    lq_map_lookup = {}
    for m in lq_matches:
        t1, t2 = m["team1"], m["team2"]
        for s in m["sets"]:
            key = (t1, t2, s["map"].strip().lower())
            key_rev = (t2, t1, s["map"].strip().lower())
            lq_map_lookup[key] = (s, False)
            lq_map_lookup[key_rev] = (s, True)
            
    with open(js_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    prefix = "window.OWCS_DATA = "
    json_str = content[len(prefix):].strip()
    if json_str.endswith(";"):
        json_str = json_str[:-1]
        
    data = json.loads(json_str)
    
    matched_count = 0
    for r in data.get("matchInfo", []):
        t1 = r.get("TEAM 1")
        t2 = r.get("TEAM 2")
        mp = r.get("MAP")
        
        # Title case bans
        if r.get("TEAM 1 BAN"):
            r["TEAM 1 BAN"] = format_hero_name(r["TEAM 1 BAN"])
        if r.get("TEAM 2 BAN"):
            r["TEAM 2 BAN"] = format_hero_name(r["TEAM 2 BAN"])
            
        if t1 and t2 and mp:
            key = (str(t1).strip(), str(t2).strip(), str(mp).strip().lower())
            if key in lq_map_lookup:
                s_info, is_rev = lq_map_lookup[key]
                sc1 = s_info["score1"]
                sc2 = s_info["score2"]
                if is_rev:
                    sc1, sc2 = sc2, sc1
                r["TEAM 1 SCORE"] = sc1
                r["TEAM 2 SCORE"] = sc2
                r["DETAIL_SCORE"] = f"{sc1} : {sc2}"
                matched_count += 1
                
    new_content = prefix + json.dumps(data, ensure_ascii=False) + ";\n"
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Stage 2 data.js updated: {matched_count} map scores injected, bans title cased.")

if __name__ == "__main__":
    update_stage2_excel()
    update_stage2_data_js()
