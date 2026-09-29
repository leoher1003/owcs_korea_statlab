#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
patch_app_tournaments.py
Updates app.js to support:
- OWCS Asia 2026 Stage 1 (asia-s1)
- OWCS 2026 Pre-Season Bootcamp (bootcamp-s1)
- OWCS 2026 Champions Clash (clash-2026)
- OWCS 2026 Midseason Championship (midseason-2026)
- Overwatch World Cup 2026 (owwc-2026)
With full Overview pages, Match Explorer pages, and Match Detail Modal integration.
"""

import re
from pathlib import Path

APP_JS = Path("owcs-stat-lab 2/app.js")

with open(APP_JS, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add translations
old_en_tourney = """    tourney_kr_s1: 'OWCS Korea 2026 Stage 1',

    tourney_kr_s2: 'OWCS Korea 2026 Stage 2',
    tourney_kr_s3: 'OWCS Korea 2026 Stage 3',
    tourney_ewc: 'Midseason Championship (EWC) 2026',
    tourney_owwc: 'Overwatch World Cup 2026',"""

new_en_tourney = """    tourney_kr_s1: 'OWCS Korea 2026 Stage 1',
    tourney_kr_s2: 'OWCS Korea 2026 Stage 2',
    tourney_kr_s3: 'OWCS Korea 2026 Stage 3',
    tourney_asia_s1: 'OWCS Asia 2026 Stage 1',
    tourney_bootcamp: 'OWCS 2026 Pre-Season Bootcamp',
    tourney_clash: 'OWCS 2026 Champions Clash',
    tourney_midseason: 'OWCS 2026 Midseason Championship',
    tourney_owwc: 'Overwatch World Cup 2026',"""

old_ko_tourney = """    tourney_kr_s1: 'OWCS Korea 2026 Stage 1',

    tourney_kr_s2: 'OWCS Korea 2026 Stage 2',
    tourney_kr_s3: 'OWCS Korea 2026 Stage 3',
    tourney_ewc: 'Midseason Championship (EWC) 2026',
    tourney_owwc: 'Overwatch World Cup 2026',"""

new_ko_tourney = """    tourney_kr_s1: 'OWCS 코리아 2026 스테이지 1',
    tourney_kr_s2: 'OWCS 코리아 2026 스테이지 2',
    tourney_kr_s3: 'OWCS 코리아 2026 스테이지 3',
    tourney_asia_s1: 'OWCS 아시아 2026 스테이지 1',
    tourney_bootcamp: 'OWCS 2026 프리시즌 부트캠프',
    tourney_clash: 'OWCS 2026 챔피언스 클래시',
    tourney_midseason: 'OWCS 2026 미드시즌 챔피언십',
    tourney_owwc: '오버워치 월드컵 2026',"""

if old_en_tourney in content:
    # First occurrence is in English section
    content = content.replace(old_en_tourney, new_en_tourney, 1)

# In Korean section
if old_ko_tourney in content:
    content = content.replace(old_ko_tourney, new_ko_tourney, 1)

# 2. Update updateStaticHeaderTexts
old_header_text = """  const curTitle=document.getElementById('tourneyCurrentTitle');
  if(curTitle){
    curTitle.textContent=state.tourney==='kr-s3'?t('tourney_kr_s3'):state.tourney==='kr-s1'?t('tourney_kr_s1'):t('tourney_kr_s2');
  }"""

new_header_text = """  const curTitle=document.getElementById('tourneyCurrentTitle');
  if(curTitle){
    const titleMap = {
      'kr-s1': t('tourney_kr_s1'),
      'kr-s2': t('tourney_kr_s2'),
      'kr-s3': t('tourney_kr_s3'),
      'asia-s1': t('tourney_asia_s1'),
      'bootcamp-s1': t('tourney_bootcamp'),
      'clash-2026': t('tourney_clash'),
      'midseason-2026': t('tourney_midseason'),
      'owwc-2026': t('tourney_owwc')
    };
    curTitle.textContent = titleMap[state.tourney] || t('tourney_kr_s2');
  }"""

content = content.replace(old_header_text, new_header_text)

# 3. Update getNavItems
old_nav_items = """function getNavItems(){
  const isKo = state.lang === 'ko';
  if (state.tourney === 'kr-s1') {
    return [
      ['overview', t('nav_overview')],
      ['matches', isKo ? '경기 탐색기' : 'Match Explorer']
    ];
  }
  if (state.tourney === 'kr-s3') {
    return [
      ['overview', t('nav_overview')]
    ];
  }
  return [
    ['overview', t('nav_overview')],
    ['teams', t('nav_teams')],
    ['rankings', t('nav_rankings')],
    ['plotting', t('nav_plotting')],
    ['h2h', t('nav_h2h')],
    ['matches', t('nav_matches')]
  ];
}"""

new_nav_items = """function getTourneyDataset(tourneyKey) {
  if (tourneyKey === 'kr-s1') return window.OWCS_STAGE1_PREVIEW;
  if (tourneyKey === 'kr-s2') return window.OWCS_STAGE2_PREVIEW;
  if (tourneyKey === 'kr-s3') return window.OWCS_STAGE3_PREVIEW;
  if (tourneyKey === 'asia-s1') return window.OWCS_ASIA_S1_PREVIEW;
  if (tourneyKey === 'bootcamp-s1') return window.OWCS_BOOTCAMP_PREVIEW;
  if (tourneyKey === 'clash-2026') return window.OWCS_CLASH_PREVIEW;
  if (tourneyKey === 'midseason-2026') return window.OWCS_MIDSEASON_PREVIEW;
  if (tourneyKey === 'owwc-2026') return window.OWCS_OWWC_PREVIEW;
  return null;
}

function getNavItems(){
  const isKo = state.lang === 'ko';
  if (state.tourney === 'kr-s2') {
    return [
      ['overview', t('nav_overview')],
      ['teams', t('nav_teams')],
      ['rankings', t('nav_rankings')],
      ['plotting', t('nav_plotting')],
      ['h2h', t('nav_h2h')],
      ['matches', t('nav_matches')]
    ];
  }
  if (state.tourney === 'kr-s3') {
    return [
      ['overview', t('nav_overview')]
    ];
  }
  // For kr-s1, asia-s1, bootcamp-s1, clash-2026, midseason-2026, owwc-2026:
  return [
    ['overview', t('nav_overview')],
    ['matches', isKo ? '경기 탐색기' : 'Match Explorer']
  ];
}"""

content = content.replace(old_nav_items, new_nav_items)

# 4. Enhance findMatchObject across all tournament datasets
old_find_match = """// Find Match object across Stage 1 or Stage 2
function findMatchObject(keyOrId, tourney) {"""

new_find_match = """// Find Match object across all tournaments
function findMatchObject(keyOrId, tourney) {
  const currentOrSpecifiedTourney = tourney || state.tourney;
  const targetDs = getTourneyDataset(currentOrSpecifiedTourney);
  if (targetDs && targetDs.matches) {
    let found = targetDs.matches.find(m => 
      m.matchId === keyOrId || 
      m.key === keyOrId || 
      String(m.matchId).toLowerCase() === String(keyOrId).toLowerCase() ||
      String(m.key).toLowerCase() === String(keyOrId).toLowerCase()
    );
    if (found) return found;
  }

  // Universal lookup across all new datasets
  const allDatasets = [
    window.OWCS_STAGE1_PREVIEW,
    window.OWCS_ASIA_S1_PREVIEW,
    window.OWCS_BOOTCAMP_PREVIEW,
    window.OWCS_CLASH_PREVIEW,
    window.OWCS_MIDSEASON_PREVIEW,
    window.OWCS_OWWC_PREVIEW
  ];
  for (const ds of allDatasets) {
    if (!ds || !ds.matches) continue;
    let found = ds.matches.find(m => 
      m.matchId === keyOrId || 
      m.key === keyOrId || 
      String(m.matchId).toLowerCase() === String(keyOrId).toLowerCase() ||
      String(m.key).toLowerCase() === String(keyOrId).toLowerCase()
    );
    if (found) return found;
  }"""

content = content.replace(old_find_match, new_find_match)

# 5. Enhance openMatchDetailModal tourName and teams
old_modal_header = """  const isKo = state.lang === 'ko';
  const tourName = tourney === 'kr-s1' 
    ? (isKo ? 'OWCS 코리아 2026 Stage 1' : 'OWCS Korea 2026 Stage 1')
    : (isKo ? 'OWCS 코리아 2026 Stage 2' : 'OWCS Korea 2026 Stage 2');"""

new_modal_header = """  const isKo = state.lang === 'ko';
  const activeTourKey = tourney || state.tourney;
  const tourDataset = getTourneyDataset(activeTourKey);
  const tourName = tourDataset?.tournament 
    ? (isKo ? (tourDataset.tournament.nameKo || tourDataset.tournament.name) : tourDataset.tournament.name)
    : (activeTourKey === 'kr-s1' 
        ? (isKo ? 'OWCS 코리아 2026 Stage 1' : 'OWCS Korea 2026 Stage 1')
        : (isKo ? 'OWCS 코리아 2026 Stage 2' : 'OWCS Korea 2026 Stage 2'));"""

content = content.replace(old_modal_header, new_modal_header)

old_h2h_lookup = """  // Compute H2H within tournament
  const allTourneyMatches = tourney === 'kr-s1'
    ? ((window.OWCS_STAGE1_PREVIEW && window.OWCS_STAGE1_PREVIEW.matches) || [])
    : (window.OWCS_STAGE2_MATCHES || []);"""

new_h2h_lookup = """  // Compute H2H within tournament
  const allTourneyMatches = (tourDataset && tourDataset.matches) 
    ? tourDataset.matches 
    : (activeTourKey === 'kr-s1' 
        ? ((window.OWCS_STAGE1_PREVIEW && window.OWCS_STAGE1_PREVIEW.matches) || [])
        : (window.OWCS_STAGE2_MATCHES || []));"""

content = content.replace(old_h2h_lookup, new_h2h_lookup)

old_team_names = """  const t1Name = teamNames[t1] || (window.OWCS_STAGE1_PREVIEW?.teamNames?.[t1]) || t1;
  const t2Name = teamNames[t2] || (window.OWCS_STAGE1_PREVIEW?.teamNames?.[t2]) || t2;"""

new_team_names = """  const t1Name = tourDataset?.teamNames?.[t1] || teamNames[t1] || (window.OWCS_STAGE1_PREVIEW?.teamNames?.[t1]) || t1;
  const t2Name = tourDataset?.teamNames?.[t2] || teamNames[t2] || (window.OWCS_STAGE1_PREVIEW?.teamNames?.[t2]) || t2;"""

content = content.replace(old_team_names, new_team_names)

# 6. Update render() to handle generic tournaments
old_render_block = """  if(state.tourney === 'kr-s3'){
    if(state.page === 'overview' || state.page === 'stage3'){
      app.innerHTML = stage3PreviewPage();
    }else{
      app.innerHTML = stageUpcomingPlaceholderPage('kr-s3');
    }
  }else if(state.tourney === 'kr-s1'){
    if(state.page === 'matches'){
      app.innerHTML = stage1MatchesPage();
    }else{
      app.innerHTML = stage1PreviewPage();
    }
  }else{
    // kr-s2
    if(state.page === 'overview' || state.page === 'stage2'){
      app.innerHTML = stage2PreviewPage();
    }else if(state.page === 'teams'){
      app.innerHTML = teamsPage();
    }else if(state.page === 'rankings'){
      app.innerHTML = rankingsPage();
    }else if(state.page === 'plotting'){
      app.innerHTML = plottingPage();
    }else if(state.page === 'h2h'){
      app.innerHTML = h2hPage();
    }else if(state.page === 'matches'){
      app.innerHTML = matchesPage();
    }else{
      app.innerHTML = stage2PreviewPage();
    }
  }"""

new_render_block = """  if(state.tourney === 'kr-s3'){
    if(state.page === 'overview' || state.page === 'stage3'){
      app.innerHTML = stage3PreviewPage();
    }else{
      app.innerHTML = stageUpcomingPlaceholderPage('kr-s3');
    }
  }else if(state.tourney === 'kr-s1'){
    if(state.page === 'matches'){
      app.innerHTML = stage1MatchesPage();
    }else{
      app.innerHTML = stage1PreviewPage();
    }
  }else if(state.tourney === 'kr-s2'){
    if(state.page === 'overview' || state.page === 'stage2'){
      app.innerHTML = stage2PreviewPage();
    }else if(state.page === 'teams'){
      app.innerHTML = teamsPage();
    }else if(state.page === 'rankings'){
      app.innerHTML = rankingsPage();
    }else if(state.page === 'plotting'){
      app.innerHTML = plottingPage();
    }else if(state.page === 'h2h'){
      app.innerHTML = h2hPage();
    }else if(state.page === 'matches'){
      app.innerHTML = matchesPage();
    }else{
      app.innerHTML = stage2PreviewPage();
    }
  }else{
    // asia-s1, bootcamp-s1, clash-2026, midseason-2026, owwc-2026
    if(state.page === 'matches'){
      app.innerHTML = genericTournamentMatchesPage(state.tourney);
    }else{
      app.innerHTML = genericTournamentPreviewPage(state.tourney);
    }
  }"""

content = content.replace(old_render_block, new_render_block)

# 7. Update tourney option click handler in bind()
old_tourney_click = """      if(tKey==='kr-s1'){
        state.tourney='kr-s1';
        state.page='overview';
        state.team=null;
        state.player=null;
        state.openMatch=null;
        state.openPhase=null;
        state.s1OpenPhase=null;
        localStorage.setItem('owcs_stat_lab_tourney','kr-s1');
        localStorage.setItem('owcs_stat_lab_page','overview');
      }else if(tKey==='kr-s3'){
        state.tourney='kr-s3';
        state.page='overview';
        localStorage.setItem('owcs_stat_lab_tourney','kr-s3');
        localStorage.setItem('owcs_stat_lab_page','overview');
      }else if(tKey==='kr-s2'){
        state.tourney='kr-s2';
        state.team=null;
        state.player=null;
        state.openMatch=null;
        state.openPhase=null;
        state.s1OpenPhase=null;
        localStorage.setItem('owcs_stat_lab_tourney','kr-s2');
      }"""

new_tourney_click = """      state.tourney = tKey;
      state.page = 'overview';
      state.team = null;
      state.player = null;
      state.openMatch = null;
      state.openPhase = null;
      state.s1OpenPhase = null;
      state.tTab = 'schedule';
      state.tPhase = 'All';
      state.tSearch = '';
      localStorage.setItem('owcs_stat_lab_tourney', tKey);
      localStorage.setItem('owcs_stat_lab_page', 'overview');"""

content = content.replace(old_tourney_click, new_tourney_click)

with open(APP_JS, "w", encoding="utf-8") as f:
    f.write(content)

print("Base app.js patched successfully.")
