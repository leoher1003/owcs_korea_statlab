#!/usr/bin/env python3
# -*- coding: utf-8 -*-

APP_JS = "owcs-stat-lab 2/app.js"
NEW_PAGE_JS = "scratch/new_stage1_page.js"

with open(APP_JS, "r", encoding="utf-8") as f:
    app_text = f.read()

with open(NEW_PAGE_JS, "r", encoding="utf-8") as f:
    new_page_code = f.read()

start_marker = "// Stage 1 Overview Page\nfunction stage1PreviewPage() {"
end_marker = "\n\n// Stage 1 Matches Page (Match Explorer)"

start_idx = app_text.find(start_marker)
end_idx = app_text.find(end_marker)

if start_idx != -1 and end_idx != -1:
    app_text = app_text[:start_idx] + new_page_code + "\n" + app_text[end_idx:]
    print("Successfully replaced stage1PreviewPage with Stage 2 layout standard!")
else:
    print(f"Markers not found: start_idx={start_idx}, end_idx={end_idx}")

# Also check bind() to add stage 1 direct buttons and map filter
extra_bind_code = """
  // Stage 1 Map type filter
  document.querySelectorAll('[data-s1-maptype]').forEach(btn => {
    btn.onclick = () => {
      state.s1MapTypeFilter = btn.dataset.s1Maptype;
      render();
    };
  });

  // Stage 1 Direct navigation buttons
  const btnGoS2 = document.getElementById('btnGoStage2Direct');
  if(btnGoS2) btnGoS2.onclick = () => {
    state.tourney = 'kr-s2';
    state.page = 'overview';
    localStorage.setItem('owcs_stat_lab_tourney', 'kr-s2');
    localStorage.setItem('owcs_stat_lab_page', 'overview');
    render();
  };

  const btnGoS3 = document.getElementById('btnGoStage3Direct');
  if(btnGoS3) btnGoS3.onclick = () => {
    state.tourney = 'kr-s3';
    state.page = 'overview';
    localStorage.setItem('owcs_stat_lab_tourney', 'kr-s3');
    localStorage.setItem('owcs_stat_lab_page', 'overview');
    render();
  };
"""

target_bind_point = "  // Bind Match Detail Modal Clicks\n  bindMatchModalEvents();"
if target_bind_point in app_text and "btnGoStage2Direct" not in app_text:
    app_text = app_text.replace(target_bind_point, target_bind_point + extra_bind_code)
    print("Added Stage 1 map filter and direct navigation buttons to bind()!")

with open(APP_JS, "w", encoding="utf-8") as f:
    f.write(app_text)

print("Updated app.js successfully.")
