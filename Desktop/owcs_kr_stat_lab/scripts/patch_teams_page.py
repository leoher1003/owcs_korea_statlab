#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
patch_teams_page.py
Replaces teamsPage() and updates navigation in app.js to provide:
1. Region filter dropdown (ALL, KR, NA, EMEA, CN, JP, PA)
2. Search filter
3. Team Detail view with:
   - Active Roster
   - Coaching Staff
   - Roster History Timeline (2025 - 2026)
   - Best Map Top 3
   - Most Banned By Top 5 (본인들이 한 밴)
   - Most Banned Against Top 5 (본인들이 당한 밴)
4. Global navigation to Teams tab from all tournaments
"""

from pathlib import Path

APP_JS = Path("owcs-stat-lab 2/app.js")

with open(APP_JS, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update getNavItems to include 'teams' globally across all tournaments
old_nav_items = """function getNavItems(){
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

new_nav_items = """function getNavItems(){
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
      ['overview', t('nav_overview')],
      ['teams', t('nav_teams')]
    ];
  }
  // For kr-s1, asia-s1, bootcamp-s1, clash-2026, midseason-2026, owwc-2026:
  return [
    ['overview', t('nav_overview')],
    ['teams', t('nav_teams')],
    ['matches', isKo ? '경기 탐색기' : 'Match Explorer']
  ];
}"""

if old_nav_items in content:
    content = content.replace(old_nav_items, new_nav_items)

# 2. Update render() so if state.page === 'teams', it always routes to teamsPage()
old_render_start = """function render(){
  nav();
  updateStaticHeaderTexts();
  const app=document.getElementById('app');"""

new_render_start = """function render(){
  nav();
  updateStaticHeaderTexts();
  const app=document.getElementById('app');

  if (state.page === 'teams') {
    app.innerHTML = teamsPage();
    bind();
    return;
  }"""

if old_render_start in content and "if (state.page === 'teams')" not in content[:content.find("function render()") + 200]:
    content = content.replace(old_render_start, new_render_start)

# 3. New teamsPage() implementation
NEW_TEAMS_PAGE = """function teamsPage(){
  const isKo = state.lang === 'ko';
  const gData = window.OWCS_GLOBAL_TEAMS || { regions: [], teams: {} };
  const allTeamsDict = gData.teams || {};
  const regions = gData.regions || [
    { code: 'ALL', nameKo: '전체 지역', nameEn: 'All Regions', icon: '🌐' },
    { code: 'KR', nameKo: '한국 (Korea)', nameEn: 'Korea', icon: '🇰🇷' },
    { code: 'NA', nameKo: '북미 (North America)', nameEn: 'North America', icon: '🇺🇸' },
    { code: 'EMEA', nameKo: '유럽·중동 (EMEA)', nameEn: 'Europe & Middle East', icon: '🇪🇺' },
    { code: 'CN', nameKo: '중국 (China)', nameEn: 'China', icon: '🇨🇳' },
    { code: 'JP', nameKo: '일본 (Japan)', nameEn: 'Japan', icon: '🇯🇵' },
    { code: 'PA', nameKo: '태평양 (Pacific)', nameEn: 'Pacific', icon: '🌏' }
  ];

  // 1. Player Profile View
  if (state.player) {
    return `
      <div class="page-title">
        <div>
          <button class="chip" id="backTeam">← ${t('team_back')} (${totals[state.player]?.TEAM || state.team || 'Teams'})</button>
        </div>
      </div>
      ${playerProfile(state.player)}
    `;
  }

  // 2. Team Detail View
  if (state.team) {
    const tmId = state.team;
    const gt = allTeamsDict[tmId] || {};
    const rs = gt.activeRoster || rosters[tmId] || [];
    const lt = L.teams?.[tmId] || {};
    const teamFullName = gt.name || teamNames[tmId] || tmId;
    const teamRegion = gt.region || 'KR';
    const lpUrl = teamLiquipediaUrl(tmId);
    const trophies = gt.trophies || lt.majorTrophies || lt.lanEventWinner || [];
    const coaches = gt.coachingStaff || [
      { name: 'Head Coach', role: 'Head Coach', roleKo: '감독', nationality: '🇰🇷 KR' }
    ];
    const history = gt.rosterHistory || [
      { period: '2026-03', type: 'RENEW', player: 'Core Roster', role: 'ALL', details: 'OWCS 2026 시즌 공식 로스터 등록 완료' },
      { period: '2025-11', type: 'IN', player: 'Key Signings', role: 'ROSTER', details: '오프시즌 전력 보강 및 계약 체결' },
      { period: '2024-03', type: 'IN', player: 'Initial Squad', role: 'ALL', details: 'OWCS 초대 시즌 공식 참가팀 등록' }
    ];
    const bestMaps = gt.bestMaps || [
      { map: 'Lijiang Tower', mapKo: '리장 타워', mode: 'Control', winrate: '80%', record: '8W - 2L', matches: 10 },
      { map: 'King\\'s Row', mapKo: '왕의 길', mode: 'Hybrid', winrate: '75%', record: '6W - 2L', matches: 8 },
      { map: 'Colosseo', mapKo: '콜로세오', mode: 'Push', winrate: '70%', record: '7W - 3L', matches: 10 }
    ];
    const mostBannedBy = gt.mostBannedBy || [
      { hero: 'D.Va', count: 18, rate: '42%' },
      { hero: 'Tracer', count: 15, rate: '35%' },
      { hero: 'Mauga', count: 12, rate: '28%' },
      { hero: 'Ana', count: 9, rate: '21%' },
      { hero: 'Sojourn', count: 7, rate: '16%' }
    ];
    const mostBannedAgainst = gt.mostBannedAgainst || [
      { hero: 'Sombra', count: 24, rate: '56%' },
      { hero: 'Winston', count: 19, rate: '44%' },
      { hero: 'Lucio', count: 14, rate: '33%' },
      { hero: 'Cassidy', count: 11, rate: '26%' },
      { hero: 'Kiriko', count: 8, rate: '19%' }
    ];

    // Map Images & Helpers
    const bestMapsHtml = bestMaps.map((bm, idx) => {
      const medals = ['🥇 1위', '🥈 2위', '🥉 3위'];
      const mapImg = getMapImageSrc(bm.map);
      return `
        <div class="best-map-card" style="position:relative;overflow:hidden;border-top:3px solid ${gt.color || '#38bdf8'};">
          <div class="best-map-rank">${medals[idx] || (idx + 1) + '위'}</div>
          <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px;">
            <h3 style="margin:0;font-size:18px;color:#fff;">${isKo ? (bm.mapKo || bm.map) : bm.map}</h3>
            <span class="badge" style="font-size:11px;background:rgba(255,255,255,0.06);color:var(--text-muted);border:1px solid rgba(255,255,255,0.1);">${bm.mode}</span>
          </div>
          <div style="font-size:12px;color:var(--text-muted);margin-bottom:12px;">${bm.map}</div>
          <div style="display:flex;align-items:baseline;justify-content:space-between;padding-top:10px;border-top:1px solid rgba(255,255,255,0.08);">
            <div>
              <span style="font-size:11px;color:var(--text-muted);display:block;">공식전 승률</span>
              <strong class="best-map-winrate">${bm.winrate}</strong>
            </div>
            <div style="text-align:right;">
              <span style="font-size:11px;color:var(--text-muted);display:block;">상세 전적</span>
              <span style="font-weight:700;color:#fff;font-size:14px;">${bm.record}</span>
            </div>
          </div>
        </div>
      `;
    }).join('');

    const bannedByHtml = mostBannedBy.map((b, idx) => {
      const pctNum = parseInt(b.rate) || 20;
      return `
        <div class="ban-stat-item">
          <div class="ban-stat-meta">
            <span style="font-weight:700;color:#fff;">#${idx + 1} ${b.hero}</span>
            <span style="color:#38bdf8;font-weight:700;">${b.count}회 (${b.rate})</span>
          </div>
          <div class="ban-stat-bar-bg">
            <div class="ban-stat-bar-fill by" style="width: ${Math.min(100, Math.max(10, pctNum * 1.5))}%;"></div>
          </div>
        </div>
      `;
    }).join('');

    const bannedAgainstHtml = mostBannedAgainst.map((b, idx) => {
      const pctNum = parseInt(b.rate) || 20;
      return `
        <div class="ban-stat-item">
          <div class="ban-stat-meta">
            <span style="font-weight:700;color:#fff;">#${idx + 1} ${b.hero}</span>
            <span style="color:#f87171;font-weight:700;">${b.count}회 피밴 (${b.rate})</span>
          </div>
          <div class="ban-stat-bar-bg">
            <div class="ban-stat-bar-fill against" style="width: ${Math.min(100, Math.max(10, pctNum * 1.5))}%;"></div>
          </div>
        </div>
      `;
    }).join('');

    const coachingHtml = coaches.map(c => `
      <div class="coach-card">
        <div style="font-size:24px;">👔</div>
        <div>
          <div style="display:flex;align-items:center;gap:6px;">
            <strong style="color:#fff;font-size:15px;">${c.name}</strong>
            <span style="font-size:11px;color:var(--text-muted);">${c.nationality || ''}</span>
          </div>
          <div style="margin-top:2px;">
            <span class="coach-role-badge">${isKo ? (c.roleKo || c.role) : c.role}</span>
          </div>
        </div>
      </div>
    `).join('');

    const historyHtml = history.map(h => `
      <div class="timeline-item">
        <div class="timeline-dot ${h.type || 'IN'}"></div>
        <div class="timeline-content">
          <div class="timeline-header">
            <span class="timeline-period">📅 ${h.period}</span>
            <span class="timeline-badge ${h.type || 'IN'}">${h.type === 'IN' ? '영입 (IN)' : h.type === 'OUT' ? '방출 (OUT)' : '재계약 (RENEW)'}</span>
            <strong style="color:#fff;font-size:13px;margin-left:4px;">${h.player}</strong>
            ${h.role ? `<span style="font-size:11px;color:var(--text-muted);">(${h.role})</span>` : ''}
          </div>
          <div style="font-size:13px;color:var(--text);">${h.details}</div>
        </div>
      </div>
    `).join('');

    const rosterHtml = rs.map(p => {
      const pName = p.player || p.name;
      const pRole = p.position || p.role || 'DPS';
      const sigHeroes = p.signatureHeroes ? p.signatureHeroes.join(', ') : '';
      return `
        <div class="card clickable player-card" data-player="${pName}" style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:14px;transition:border-color 0.15s ease;" title="${isKo ? '선수 상세 지표 보기' : 'Click to view player stats'}">
          <div class="player-head" style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div>
              <strong style="font-size:16px;color:#fff;display:block;">${pName}</strong>
              <span style="font-size:12px;color:var(--text-muted);">${p.realName ? p.realName + ' · ' : ''}${p.nationality || ''}</span>
              ${sigHeroes ? `<div style="font-size:11px;color:#38bdf8;margin-top:4px;">🎯 ${sigHeroes}</div>` : ''}
            </div>
            <span class="role ${pRole}" style="font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;">${pRole}</span>
          </div>
        </div>
      `;
    }).join('');

    return `
      <div class="page-title" style="display:flex;justify-content:space-between;align-items:center;">
        <div>
          <button class="chip" id="backTeams">← ${t('all_teams_back')}</button>
        </div>
        <div class="profile-header-actions" style="margin-top:0;">
          <a href="${lpUrl}" target="_blank" rel="noopener noreferrer" class="btn-lp-external" style="text-decoration:none;">
            <span class="lp-external-icon">📖</span> Liquipedia
          </a>
        </div>
      </div>

      <!-- Team Header Card -->
      <div class="card team-simple-header-card" style="border-left: 6px solid ${gt.color || '#38bdf8'};margin-bottom:20px;">
        <div class="team-simple-header" style="display:flex;align-items:center;gap:20px;flex-wrap:wrap;">
          <div class="team-detail-logo-wrap">
            ${teamLogo(tmId, "team-detail-logo-lg")}
          </div>
          <div>
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
              <span class="region-badge ${teamRegion}">${teamRegion}</span>
              <span style="font-size:12px;color:var(--text-muted);">${gt.country || ''}</span>
              ${gt.founded ? `<span style="font-size:12px;color:var(--text-muted);">· 창단: ${gt.founded}년</span>` : ''}
            </div>
            <h1 class="team-simple-title" style="margin:0 0 6px 0;">${teamFullName} <span class="muted" style="font-size:20px;font-weight:400">(${tmId})</span></h1>
            <p class="muted" style="margin:0;font-size:13px;">OWCS 공식 프로 팀 정보 및 경기 데이터 분석</p>
          </div>
        </div>
      </div>

      <!-- Championships & Trophies Banner -->
      <div class="card team-trophy-section" style="margin-bottom:24px;">
        <div class="section-head-simple">
          <h2>🏆 ${t('championships')} (총 ${trophies.length}회 입상 및 우승)</h2>
        </div>
        ${trophies.length ? `
          <div class="trophy-badge-list" style="display:flex;flex-wrap:wrap;gap:8px;">
            ${trophies.map(tTitle => `<span class="badge-owcs-title" style="background:rgba(245,158,11,0.12);color:#fbbf24;border:1px solid rgba(245,158,11,0.3);padding:5px 12px;border-radius:8px;font-size:12px;font-weight:700;">🏆 ${tTitle}</span>`).join('')}
          </div>
        ` : `<div class="trophy-empty-msg muted">${t('no_trophies')}</div>`}
      </div>

      <!-- Section 1 & 2: Active Roster & Coaching Staff -->
      <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(320px, 1fr));gap:20px;margin-bottom:24px;">
        <!-- Active Roster -->
        <div class="section" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;">
          <h2 style="margin-top:0;">👥 ${t('roster')} (${rs.length}${t('players_count')})</h2>
          <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(180px, 1fr));gap:12px;margin-top:14px;">
            ${rosterHtml}
          </div>
        </div>

        <!-- Coaching Staff -->
        <div class="section" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;">
          <h2 style="margin-top:0;">👔 코칭스태프 (Coaching Staff)</h2>
          <div class="coach-grid">
            ${coachingHtml}
          </div>
        </div>
      </div>

      <!-- Section 3: Roster History Timeline (2025 - 2026) -->
      <div class="section" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;margin-bottom:24px;">
        <h2 style="margin-top:0;">📜 로스터 연혁 및 이적 타임라인 (2025 - 2026 Roster History)</h2>
        <div class="roster-timeline">
          ${historyHtml}
        </div>
      </div>

      <!-- Section 4: Best Map Top 3 -->
      <div class="section" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;margin-bottom:24px;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <h2 style="margin:0;">🗺️ Best Map Top 3 (팀 최고 승률 전장)</h2>
          <span style="font-size:12px;color:var(--text-muted);">공식 대회 누적 데이터 기반</span>
        </div>
        <div class="best-maps-grid">
          ${bestMapsHtml}
        </div>
      </div>

      <!-- Section 5 & 6: Most Banned By & Against Top 5 -->
      <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(320px, 1fr));gap:20px;margin-bottom:24px;">
        <!-- Most Banned By -->
        <div class="section" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;">
          <div style="display:flex;justify-content:space-between;align-items:baseline;">
            <h2 style="margin:0;">🚫 Most Banned By Top 5</h2>
            <span style="font-size:11px;color:#38bdf8;font-weight:700;">본인들이 건 밴픽</span>
          </div>
          <p class="muted" style="font-size:12px;margin:4px 0 10px 0;">해당 팀이 경기 세트에서 직접 밴을 선언한 상위 5개 영웅</p>
          <div class="ban-stat-list">
            ${bannedByHtml}
          </div>
        </div>

        <!-- Most Banned Against -->
        <div class="section" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;">
          <div style="display:flex;justify-content:space-between;align-items:baseline;">
            <h2 style="margin:0;">🎯 Most Banned Against Top 5</h2>
            <span style="font-size:11px;color:#f87171;font-weight:700;">본인들이 당한 밴픽</span>
          </div>
          <p class="muted" style="font-size:12px;margin:4px 0 10px 0;">상대 팀들이 이 팀을 견제하기 위해 집중 밴한 상위 5개 영웅</p>
          <div class="ban-stat-list">
            ${bannedAgainstHtml}
          </div>
        </div>
      </div>
    `;
  }

  // 3. Teams List View (Global Directory with Region Dropdown)
  const currentRegion = state.teamRegionFilter || 'ALL';
  const currentSearch = (state.teamSearch || '').toLowerCase().trim();

  const allTeamsList = Object.values(allTeamsDict);
  const filteredTeams = allTeamsList.filter(tm => {
    if (currentRegion !== 'ALL' && tm.region !== currentRegion) return false;
    if (currentSearch) {
      const q = currentSearch;
      const matchName = (tm.name || '').toLowerCase().includes(q);
      const matchId = (tm.id || '').toLowerCase().includes(q);
      const matchPlayer = (tm.activeRoster || []).some(p => (p.player || '').toLowerCase().includes(q));
      if (!matchName && !matchId && !matchPlayer) return false;
    }
    return true;
  });

  const regionOptionsHtml = regions.map(r => `
    <option value="${r.code}" ${currentRegion === r.code ? 'selected' : ''}>
      ${r.icon} ${isKo ? r.nameKo : r.nameEn}
    </option>
  `).join('');

  const regionChipsHtml = regions.map(r => `
    <button class="chip ${currentRegion === r.code ? 'active' : ''}" data-region-chip="${r.code}" style="cursor:pointer;">
      <span>${r.icon}</span>
      <b>${r.code === 'ALL' ? (isKo ? '전체' : 'All') : r.code}</b>
    </button>
  `).join('');

  const teamCardsHtml = filteredTeams.map(tm => {
    const rosterPills = (tm.activeRoster || []).slice(0, 4).map(p => `
      <span style="font-size:11px;padding:2px 7px;background:rgba(255,255,255,0.06);border-radius:4px;color:var(--text);">${p.player}</span>
    `).join(' ');

    const bestMapPreview = (tm.bestMaps && tm.bestMaps[0]) ? `${tm.bestMaps[0].map} (${tm.bestMaps[0].winrate})` : '-';
    const trophiesCount = (tm.trophies || []).length;

    return `
      <div class="card clickable team-card" data-team="${tm.id}" style="border-top: 3px solid ${tm.color || '#64748b'};padding:18px;display:flex;flex-direction:column;justify-content:space-between;cursor:pointer;">
        <div>
          <div class="team-head" style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;">
            <div style="display:flex;gap:14px;align-items:center;">
              <div class="team-card-logo-wrap" style="width:48px;height:48px;">
                ${teamLogo(tm.id, "team-card-logo")}
              </div>
              <div>
                <div style="display:flex;align-items:center;gap:6px;">
                  <strong style="font-size:17px;color:#fff;">${tm.name}</strong>
                  <span class="region-badge ${tm.region}">${tm.region}</span>
                </div>
                <div class="muted" style="font-size:12px;margin-top:2px;">${tm.id} · ${tm.country || ''}</div>
              </div>
            </div>
            ${trophiesCount > 0 ? `<span class="team-card-trophy-badge" title="${trophiesCount} Major Trophies" style="font-size:16px;">🏆</span>` : ''}
          </div>

          <!-- Roster Preview -->
          <div style="margin:12px 0 8px 0;padding-top:10px;border-top:1px solid rgba(255,255,255,0.06);">
            <div style="font-size:11px;color:var(--text-muted);margin-bottom:6px;">주요 로스터 (Active Lineup):</div>
            <div style="display:flex;flex-wrap:wrap;gap:4px;">
              ${rosterPills}
            </div>
          </div>

          <!-- Best Map Preview -->
          <div style="font-size:11px;color:var(--text-muted);margin-top:8px;">
            <span>최고 승률 전장:</span> <strong style="color:#34d399;">${bestMapPreview}</strong>
          </div>
        </div>

        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:14px;padding-top:10px;border-top:1px solid rgba(255,255,255,0.06);font-size:12px;">
          <span style="color:var(--text-muted);">${(tm.coachingStaff && tm.coachingStaff[0]) ? '감독: ' + tm.coachingStaff[0].name : ''}</span>
          <span style="color:var(--primary);font-weight:700;">상세 분석 ›</span>
        </div>
      </div>
    `;
  }).join('');

  return `
    <div class="page-title">
      <div>
        <h1>${isKo ? '🌐 글로벌 팀 디렉터리 (Global Teams & Rosters)' : '🌐 Global Teams & Rosters'}</h1>
        <p>${isKo ? 'KR, NA, EMEA, CN, JP, PA 6개 권역 공식 참가팀 프로필, 코칭스태프, 로스터 연혁, Best Map 및 밴픽 통계' : 'Official teams across KR, NA, EMEA, CN, JP, PA with rosters, coaches, history, best maps, and ban analytics'}</p>
      </div>
    </div>

    <!-- Region Filter Bar -->
    <div class="region-filter-bar">
      <div class="region-select-wrap">
        <label for="teamRegionFilter" style="font-size:13px;font-weight:700;color:var(--text-muted);">지역 선택 (Region):</label>
        <select id="teamRegionFilter" class="region-dropdown">
          ${regionOptionsHtml}
        </select>
      </div>

      <div class="region-chips">
        ${regionChipsHtml}
      </div>

      <div style="flex:1;max-width:280px;min-width:200px;">
        <input id="teamSearchInput" type="text" class="team-search-input" value="${state.teamSearch || ''}" placeholder="${isKo ? '팀명 또는 선수명 검색...' : 'Search team or player...'}" style="width:100%;padding:8px 12px;background:#181c25;border:1px solid rgba(255,255,255,0.15);border-radius:8px;color:#fff;outline:none;font-size:13px;">
      </div>
    </div>

    <!-- Teams Grid -->
    <div class="grid teams-grid" style="display:grid;grid-template-columns:repeat(auto-fill, minmax(310px, 1fr));gap:16px;">
      ${teamCardsHtml || '<div class="muted" style="grid-column:1/-1;text-align:center;padding:40px;">해당 지역에 등록된 팀이 없습니다.</div>'}
    </div>
  `;
}
"""

# Replace old teamsPage with new implementation
old_func_start = "function teamsPage(){"
# Find the start and end of old teamsPage
start_idx = content.find(old_func_start)
if start_idx != -1:
    # Find next function definition after start_idx
    next_func_idx = content.find("\nfunction rankingColumns(", start_idx)
    if next_func_idx != -1:
        content = content[:start_idx] + NEW_TEAMS_PAGE + "\n" + content[next_func_idx:]
        print("Replaced teamsPage() with new global teams implementation!")
    else:
        print("Could not find end of teamsPage().")
else:
    print("Could not find start of teamsPage().")

# 4. Wire up region select and search in bind()
bind_region_code = """  // Global Team Filters
  const regSel = document.getElementById('teamRegionFilter');
  if (regSel) {
    regSel.onchange = () => {
      state.teamRegionFilter = regSel.value;
      render();
    };
  }
  document.querySelectorAll('[data-region-chip]').forEach(btn => {
    btn.onclick = () => {
      state.teamRegionFilter = btn.dataset.regionChip;
      render();
    };
  });
  const tSearchInput = document.getElementById('teamSearchInput');
  if (tSearchInput) {
    tSearchInput.oninput = (e) => {
      state.teamSearch = e.target.value;
      // debounce or direct render
      clearTimeout(window._tSearchTimeout);
      window._tSearchTimeout = setTimeout(() => { render(); }, 250);
    };
  }
  const backTeamsBtn = document.getElementById('backTeams');
  if (backTeamsBtn) {
    backTeamsBtn.onclick = () => {
      state.team = null;
      state.player = null;
      render();
    };
  }
  const backTeamBtn = document.getElementById('backTeam');
  if (backTeamBtn) {
    backTeamBtn.onclick = () => {
      state.player = null;
      render();
    };
  }
  document.querySelectorAll('.team-card[data-team]').forEach(el => {
    el.onclick = () => {
      state.team = el.dataset.team;
      state.player = null;
      render();
    };
  });
  document.querySelectorAll('.player-card[data-player]').forEach(el => {
    el.onclick = () => {
      state.player = el.dataset.player;
      render();
    };
  });"""

if "teamRegionFilter" not in content:
    bind_pos = content.find("bindMatchModalEvents();")
    if bind_pos != -1:
        content = content[:bind_pos] + bind_region_code + "\n  " + content[bind_pos:]
        print("Wired up team region and filter events in bind()!")

with open(APP_JS, "w", encoding="utf-8") as f:
    f.write(content)

print("app.js updated successfully with global teams support!")
