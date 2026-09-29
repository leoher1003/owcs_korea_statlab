#!/usr/bin/env python3
# -*- coding: utf-8 -*-

APP_JS = "owcs-stat-lab 2/app.js"
CODE_JS = "scratch/stage1_explorer_code.js"

with open(APP_JS, "r", encoding="utf-8") as f:
    app_text = f.read()

with open(CODE_JS, "r", encoding="utf-8") as f:
    explorer_code = f.read()

start_marker = "// Stage 1 Matches Page (Match Explorer)\nfunction stage1MatchesPage() {"
end_marker = "\n\nfunction stage2PreviewPage(){"

start_idx = app_text.find(start_marker)
end_idx = app_text.find(end_marker)

if start_idx != -1 and end_idx != -1:
    app_text = app_text[:start_idx] + explorer_code + app_text[end_idx:]
    print("Successfully replaced stage1MatchesPage with complete Stage 2 analytics components!")
else:
    print(f"Error finding markers: start={start_idx}, end={end_idx}")

# Add event listeners for Stage 1 match explorer controls in bind()
s1_bind_events = """
  // Stage 1 Match Explorer Controls
  const s1PhaseSelect = document.getElementById('s1MatchPhase');
  if(s1PhaseSelect) s1PhaseSelect.onchange = () => {
    state.s1MatchPhase = s1PhaseSelect.value;
    render();
  };

  const s1BanTeamSelect = document.getElementById('s1BanTeam');
  if(s1BanTeamSelect) s1BanTeamSelect.onchange = () => {
    state.s1BanTeam = s1BanTeamSelect.value;
    render();
  };

  const s1BanBreakMode = document.getElementById('s1BanBreakMode');
  if(s1BanBreakMode) s1BanBreakMode.onchange = () => {
    state.s1BanBreakMode = s1BanBreakMode.value;
    state.s1BanBreakValue = 'All';
    render();
  };

  const s1BanBreakValue = document.getElementById('s1BanBreakValue');
  if(s1BanBreakValue) s1BanBreakValue.onchange = () => {
    state.s1BanBreakValue = s1BanBreakValue.value;
    render();
  };

  document.querySelectorAll('[data-s1-phase-toggle]').forEach(btn => {
    btn.onclick = () => {
      const p = btn.dataset.s1PhaseToggle;
      state.s1OpenPhase = state.s1OpenPhase === p ? null : p;
      render();
    };
  });

  document.querySelectorAll('[data-s1-mapdrill]').forEach(btn => {
    btn.onclick = () => {
      const val = btn.dataset.s1Mapdrill;
      state.s1MapDrill = state.s1MapDrill === val ? null : val;
      state.s1SelectedMapDetail = null;
      render();
    };
  });

  document.querySelectorAll('[data-s1-mapdetail]').forEach(btn => {
    btn.onclick = () => {
      state.s1SelectedMapDetail = btn.dataset.s1Mapdetail;
      render();
    };
  });

  // Stage 1 Matrix & Accordion Match modal click
  document.querySelectorAll('.rr-cell[data-tourney="kr-s1"], .match-main[data-tourney="kr-s1"]').forEach(el => {
    el.onclick = (e) => {
      const matchKey = el.dataset.match;
      if(matchKey) {
        openMatchDetailModal(matchKey, 'kr-s1');
      }
    };
  });
"""

bind_target = "  // Bind Match Detail Modal Clicks\n  bindMatchModalEvents();"
if bind_target in app_text and "s1MatchPhase" not in app_text:
    app_text = app_text.replace(bind_target, bind_target + s1_bind_events)
    print("Added Stage 1 explorer control handlers to bind()!")

with open(APP_JS, "w", encoding="utf-8") as f:
    f.write(app_text)

print("Patching complete.")
