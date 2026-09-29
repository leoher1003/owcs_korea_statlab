#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
patch_app_js.py
Injects:
1. Match detail modal helper & openMatchDetailModal()
2. stage1PreviewPage() & stage1MatchesPage()
3. Router updates for kr-s1 in render()
4. Event binding for Stage 1 tabs & match card modal clicks
5. Interactive click hints for Stage 2 matches
"""

import os

APP_JS = "owcs-stat-lab 2/app.js"
MODAL_JS = "scratch/match_modal_logic.js"
PAGES_JS = "scratch/stage1_pages.js"

with open(APP_JS, "r", encoding="utf-8") as f:
    app_text = f.read()

with open(MODAL_JS, "r", encoding="utf-8") as f:
    modal_code = f.read()

with open(PAGES_JS, "r", encoding="utf-8") as f:
    pages_code = f.read()

# 1. Insert modal logic & Stage 1 pages right before "function stage2PreviewPage(){"
marker = "function stage2PreviewPage(){"
if marker in app_text and "function openMatchDetailModal(" not in app_text:
    combined_code = "\n\n" + modal_code + "\n\n" + pages_code + "\n\n" + marker
    app_text = app_text.replace(marker, combined_code, 1)
    print("Injected modal logic & Stage 1 pages before stage2PreviewPage().")
else:
    print("Modal logic already injected or marker not found.")

# 2. Update render() for kr-s1 routing
render_kr_s1_old = "  }else if(state.tourney === 'kr-s1'){\n    app.innerHTML = stageUpcomingPlaceholderPage('kr-s1');\n  }else{"
render_kr_s1_new = """  }else if(state.tourney === 'kr-s1'){
    if(state.page === 'matches'){
      app.innerHTML = stage1MatchesPage();
    }else{
      app.innerHTML = stage1PreviewPage();
    }
  }else{"""

if render_kr_s1_old in app_text:
    app_text = app_text.replace(render_kr_s1_old, render_kr_s1_new, 1)
    print("Updated render() for kr-s1 routing.")
else:
    print("render() kr-s1 marker not found or already replaced.")

# 3. Add data-match-key and hint to s2-match-row in stage2PreviewPage()
s2_row_old = '<div class="s3-match-row s2-match-row ${homeWon || awayWon ? \'completed\' : \'\'} ${isDimmed ? \'dimmed\' : \'\'}">'
s2_row_new = '<div class="s3-match-row s2-match-row ${homeWon || awayWon ? \'completed\' : \'\'} ${isDimmed ? \'dimmed\' : \'\'}" data-match-key="${m.key}" data-tourney="kr-s2" title="${isKo ? \'클릭하여 세부 스코어 및 밴픽 보기\' : \'Click to view detail scores and bans\'}">'

if s2_row_old in app_text:
    app_text = app_text.replace(s2_row_old, s2_row_new)
    print("Updated s2-match-row with data-match-key and tooltip.")

s2_meta_old = """            <div class="s3-match-meta">
              <span class="s3-match-num">${m.phase}</span>
              <span class="s2-result-tag">FINAL</span>
            </div>"""
s2_meta_new = """            <div class="s3-match-meta">
              <span class="s3-match-num">${m.phase}</span>
              <span class="s2-result-tag">FINAL</span>
              <span class="s2-match-hint">🔍 ${isKo ? '세부 정보' : 'Details'}</span>
            </div>"""

if s2_meta_old in app_text:
    app_text = app_text.replace(s2_meta_old, s2_meta_new)
    print("Added s2-match-hint to stage2PreviewPage().")

# 4. In bind(), attach Stage 1 tab handlers and bindMatchModalEvents()
bind_marker = "  // Language Switch\n  const langBtns=document.querySelectorAll('.lang-btn');"
bind_injection = """  // Stage 1 Sub-Tab switching
  document.querySelectorAll('[data-s1-tab]').forEach(btn => {
    btn.onclick = () => {
      state.s1Tab = btn.dataset.s1Tab;
      render();
    };
  });

  // Stage 1 Week filter
  document.querySelectorAll('[data-s1-week]').forEach(btn => {
    btn.onclick = () => {
      state.s1Week = btn.dataset.s1Week;
      render();
    };
  });

  // Stage 1 Team filter
  document.querySelectorAll('[data-s1-team]').forEach(btn => {
    btn.onclick = () => {
      state.s1TeamFilter = btn.dataset.s1Team;
      render();
    };
  });

  // Bind Match Detail Modal Clicks
  bindMatchModalEvents();

  // Language Switch
  const langBtns=document.querySelectorAll('.lang-btn');"""

if bind_marker in app_text:
    app_text = app_text.replace(bind_marker, bind_injection, 1)
    print("Added Stage 1 event bindings and bindMatchModalEvents() to bind().")

with open(APP_JS, "w", encoding="utf-8") as f:
    f.write(app_text)

print(f"Successfully patched {APP_JS}.")
