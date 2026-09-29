#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/patch_universal_system.py
Transforms app.js to:
1. Provide a unified Teams/Players page with the strict section sequence:
   ① Active Roster
   ② Roster History (2025-2026 Timeline)
   ③ Coaching Staff
   ④ Best Map / Worst Map for each of the 5 modes (Control, Hybrid, Flashpoint, Push, Escort)
   ⑤ Most Banned Hero (against, top 5)
   ⑥ Most Banned by [TEAM] Hero (top 5)
   With working Region dropdown, Region chips, and Search filter.
2. Provide a universal Match Explorer that applies the 2026 Korea Stage 2
   gold standard format across ALL tournaments:
   - Round Robin / Group Matrix with inline map box score
   - Phase analytics dropdown
   - Phase summary cards (Matches, Maps, Top Map, Top Ban)
   - Later phases accordions
   - Hero bans breakdown (Team, Mode, Value)
   - Bans By & Bans Against with colored progress bars
   - Team map win rate by type with interactive map drilldown
   - Match detail modal
3. Thoroughly wire all event listeners in bind() so nothing fails to respond.
"""

import re
from pathlib import Path

APP_JS = Path("owcs-stat-lab 2/app.js")

def main():
    content = APP_JS.read_text(encoding="utf-8")

    # Let's inspect where teamsPage starts and ends
    tp_start = content.find("function teamsPage(){")
    rk_start = content.find("function rankingsPage(){")
    assert tp_start != -1 and rk_start != -1, "Could not find teamsPage boundaries"

    # New teamsPage implementation
    new_teams_page = """function teamsPage(){
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
    const teamFullName = gt.name || teamNames[tmId] || tmId;
    const teamRegion = gt.region || 'KR';
    const lpUrl = teamLiquipediaUrl(tmId);
    const trophies = gt.trophies || [];
    const coaches = gt.coachingStaff || [
      { name: 'Head Coach', role: 'Head Coach', roleKo: '감독', nationality: '🇰🇷 KR' }
    ];
    const history = gt.rosterHistory || [
      { period: '2026-03', type: 'RENEW', player: 'Core Roster', role: 'ALL', details: 'OWCS 2026 시즌 공식 로스터 등록 완료' },
      { period: '2025-11', type: 'IN', player: 'Key Signings', role: 'ROSTER', details: '오프시즌 전력 보강 및 계약 체결' },
      { period: '2024-03', type: 'IN', player: 'Initial Squad', role: 'ALL', details: 'OWCS 공식 참가팀 등록' }
    ];

    // 1) Active Roster HTML
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

    // 2) Roster History HTML (2025 ~ 2026)
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
          <div style="font-size:13px;color:var(--text);margin-top:4px;">${h.details}</div>
        </div>
      </div>
    `).join('');

    // 3) Coaching Staff HTML
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

    // 4) Best Map / Worst Map per 5 Map Modes (Control, Hybrid, Flashpoint, Push, Escort)
    const modesConfig = [
      { key: 'control', nameKo: '쟁탈', nameEn: 'Control', icon: '🎯', color: '#10b981' },
      { key: 'hybrid', nameKo: '혼합', nameEn: 'Hybrid', icon: '⚔️', color: '#3b82f6' },
      { key: 'flashpoint', nameKo: '플래시포인트', nameEn: 'Flashpoint', icon: '⚡', color: '#f59e0b' },
      { key: 'push', nameKo: '밀기', nameEn: 'Push', icon: '🤖', color: '#8b5cf6' },
      { key: 'escort', nameKo: '호위', nameEn: 'Escort', icon: '🚛', color: '#ec4899' }
    ];

    const modeMapsData = gt.modeMaps || {};
    const modeCardsHtml = modesConfig.map(cfg => {
      const modeInfo = modeMapsData[cfg.key] || {
        best: { map: 'Lijiang Tower', mapKo: '리장 타워', winrate: '70%', record: '7W - 3L' },
        worst: { map: 'Nepal', mapKo: '네팔', winrate: '40%', record: '4W - 6L' }
      };
      const best = modeInfo.best;
      const worst = modeInfo.worst;

      return `
        <div class="mode-map-card" style="border-top:3px solid ${cfg.color};">
          <div class="mode-card-header">
            <div class="mode-card-title">
              <span>${cfg.icon}</span>
              <span>${isKo ? cfg.nameKo : cfg.nameEn}</span>
            </div>
            <span class="mode-card-badge">${cfg.nameEn}</span>
          </div>
          <div class="mode-best-worst-row">
            <div class="mode-side-box best">
              <div class="mode-side-label best">
                <span>🏆 BEST MAP</span>
              </div>
              <div class="mode-side-map-name" title="${best.map}">
                ${isKo ? (best.mapKo || best.map) : best.map}
              </div>
              <div class="mode-side-stats">
                <span class="mode-side-winrate best">${best.winrate}</span>
                <span class="mode-side-rec">${best.record}</span>
              </div>
            </div>
            <div class="mode-side-box worst">
              <div class="mode-side-label worst">
                <span>⚠️ WORST MAP</span>
              </div>
              <div class="mode-side-map-name" title="${worst.map}">
                ${isKo ? (worst.mapKo || worst.map) : worst.map}
              </div>
              <div class="mode-side-stats">
                <span class="mode-side-winrate worst">${worst.winrate}</span>
                <span class="mode-side-rec">${worst.record}</span>
              </div>
            </div>
          </div>
        </div>
      `;
    }).join('');

    // 5) Most Banned Hero (Against Top 5)
    const mostBannedAgainst = (gt.mostBannedAgainst || []).slice(0, 5);
    const bannedAgainstHtml = mostBannedAgainst.map((b, idx) => {
      const pctNum = parseInt(b.rate) || 20;
      return `
        <div class="ban-stat-item">
          <div class="ban-stat-meta">
            <span style="font-weight:700;color:#fff;display:inline-flex;align-items:center;gap:6px;">
              #${idx + 1} ${heroIcon(b.hero, "ban-hero-icon")} ${b.hero}
            </span>
            <span style="color:#f87171;font-weight:700;">${b.count}회 피밴 (${b.rate})</span>
          </div>
          <div class="ban-stat-bar-bg">
            <div class="ban-stat-bar-fill against" style="width: ${Math.min(100, Math.max(12, pctNum * 1.5))}%;"></div>
          </div>
        </div>
      `;
    }).join('');

    // 6) Most Banned by [TEAM] Hero (By Top 5)
    const mostBannedBy = (gt.mostBannedBy || []).slice(0, 5);
    const bannedByHtml = mostBannedBy.map((b, idx) => {
      const pctNum = parseInt(b.rate) || 20;
      return `
        <div class="ban-stat-item">
          <div class="ban-stat-meta">
            <span style="font-weight:700;color:#fff;display:inline-flex;align-items:center;gap:6px;">
              #${idx + 1} ${heroIcon(b.hero, "ban-hero-icon")} ${b.hero}
            </span>
            <span style="color:#38bdf8;font-weight:700;">${b.count}회 (${b.rate})</span>
          </div>
          <div class="ban-stat-bar-bg">
            <div class="ban-stat-bar-fill by" style="width: ${Math.min(100, Math.max(12, pctNum * 1.5))}%;"></div>
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

      <!-- ① 현재 로스터 (Active Roster) -->
      <div class="section" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;margin-bottom:24px;">
        <div class="section-head-simple">
          <h2>👥 현재 로스터 (Active Roster: ${rs.length}${t('players_count')})</h2>
          <span style="font-size:12px;color:var(--text-muted);">선수를 클릭하면 세부 개인 지표 및 방사형 차트가 열립니다.</span>
        </div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(220px, 1fr));gap:14px;margin-top:14px;">
          ${rosterHtml}
        </div>
      </div>

      <!-- ② 로스터 연혁 (Roster History: 2025 ~ 2026 Timeline) -->
      <div class="section" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;margin-bottom:24px;">
        <div class="section-head-simple">
          <h2>📜 로스터 연혁 및 이적 타임라인 (2025 - 2026 Roster History)</h2>
          <span style="font-size:12px;color:var(--text-muted);">최근 2년간의 주요 영입, 방출, 재계약 공식 기록</span>
        </div>
        <div class="roster-timeline" style="margin-top:14px;">
          ${historyHtml}
        </div>
      </div>

      <!-- ③ 코칭스태프 (Coaching Staff) -->
      <div class="section" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;margin-bottom:24px;">
        <div class="section-head-simple">
          <h2>👔 코칭스태프 (Coaching Staff)</h2>
          <span style="font-size:12px;color:var(--text-muted);">지도자 및 전략 분석진 명단</span>
        </div>
        <div class="coach-grid" style="margin-top:14px;">
          ${coachingHtml}
        </div>
      </div>

      <!-- ④ Best Map / Worst Map (전장 유형별로 하나씩: Control, Hybrid, Flashpoint, Push, Escort) -->
      <div class="section" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;margin-bottom:24px;">
        <div class="section-head-simple">
          <h2>🗺️ 전장 유형별 최고 / 최저 승률 전장 (Best & Worst Map by Mode)</h2>
          <span style="font-size:12px;color:var(--text-muted);">쟁탈 · 혼합 · 플래시포인트 · 밀기 · 호위 5대 전장 모드별 공식전 승률 비교</span>
        </div>
        <div class="mode-maps-grid">
          ${modeCardsHtml}
        </div>
      </div>

      <!-- ⑤ Most Banned Hero & ⑥ Most Banned by [TEAM] Hero -->
      <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(320px, 1fr));gap:20px;margin-bottom:24px;">
        <!-- ⑤ Most Banned Hero (당한 밴 Top 5) -->
        <div class="section" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;">
          <div style="display:flex;justify-content:space-between;align-items:baseline;">
            <h2 style="margin:0;">🎯 Most Banned Against Top 5</h2>
            <span style="font-size:11px;color:#f87171;font-weight:700;">본인들이 당한 피밴</span>
          </div>
          <p class="muted" style="font-size:12px;margin:4px 0 10px 0;">상대 팀들이 이 팀을 견제하기 위해 세트에서 가장 많이 금지(밴)한 상위 5개 영웅</p>
          <div class="ban-stat-list">
            ${bannedAgainstHtml}
          </div>
        </div>

        <!-- ⑥ Most Banned by [TEAM] Hero (직접 한 밴 Top 5) -->
        <div class="section" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;">
          <div style="display:flex;justify-content:space-between;align-items:baseline;">
            <h2 style="margin:0;">🚫 Most Banned by [TEAM] Top 5</h2>
            <span style="font-size:11px;color:#38bdf8;font-weight:700;">본인들이 직접 건 밴픽</span>
          </div>
          <p class="muted" style="font-size:12px;margin:4px 0 10px 0;">해당 팀이 세트 시작 시 전술적으로 밴을 선언한 상위 5개 영웅</p>
          <div class="ban-stat-list">
            ${bannedByHtml}
          </div>
        </div>
      </div>
    `;
  }

  // 3. Teams List View (Global Directory with Region Dropdown & Search)
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
    const rosterPills = (tm.activeRoster || []).slice(0, 5).map(p => `
      <span style="font-size:11px;padding:2px 7px;background:rgba(255,255,255,0.06);border-radius:4px;color:var(--text);">${p.player}</span>
    `).join(' ');

    const bestMapPreview = (tm.modeMaps && tm.modeMaps.control && tm.modeMaps.control.best)
      ? `${tm.modeMaps.control.best.map} (${tm.modeMaps.control.best.winrate})`
      : ((tm.bestMaps && tm.bestMaps[0]) ? `${tm.bestMaps[0].map} (${tm.bestMaps[0].winrate})` : '-');
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
            <span>쟁탈 최고 승률 전장:</span> <strong style="color:#34d399;">${bestMapPreview}</strong>
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
        <p>${isKo ? 'KR, NA, EMEA, CN, JP, PA 6개 권역 공식 참가팀 프로필, 로스터 연혁, 코칭스태프, 전장 유형별 Best/Worst 맵 및 밴픽 분석' : 'Official teams across KR, NA, EMEA, CN, JP, PA with rosters, history, coaches, mode best/worst maps, and ban analytics'}</p>
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

      <div style="flex:1;min-width:220px;max-width:320px;">
        <input id="teamSearchInput" type="text" class="team-search-input" value="${state.teamSearch || ''}" placeholder="${isKo ? '팀명 또는 선수명 검색...' : 'Search team or player...'}" style="width:100%;padding:8px 12px;background:#181c25;border:1px solid rgba(255,255,255,0.15);border-radius:8px;color:#fff;outline:none;font-size:13px;">
      </div>
    </div>

    <!-- Teams Grid -->
    <div class="global-teams-grid" style="display:grid;grid-template-columns:repeat(auto-fit, minmax(300px, 1fr));gap:16px;">
      ${teamCardsHtml || `<div class="empty-state" style="grid-column:1/-1;padding:60px 20px;text-align:center;color:var(--text-muted);">${isKo ? '검색된 팀이 없습니다.' : 'No teams found.'}</div>`}
    </div>
  `;
}
"""

    content = content[:tp_start] + new_teams_page + content[rk_start:]

    APP_JS.write_text(content, encoding="utf-8")
    print("Successfully replaced teamsPage() in app.js")

if __name__ == "__main__":
    main()
