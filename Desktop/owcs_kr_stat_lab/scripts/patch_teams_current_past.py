#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
patch_teams_current_past.py
Patches app.js to support:
1. Current OWCS Teams vs Past OWCS Teams toggle filter
2. Strict ordering for Current OWCS Teams:
   1. Key Achievements -> 2. Active Roster -> 3. Transfers -> 4. Coaching Staff -> 5. Best/Worst Map By Mode -> 6. Most Banned / Banned By
3. Strict ordering for Past OWCS Teams:
   1. Final Roster -> 2. Transfers -> 3. Coaching Staff -> 4. Best/Worst Map By Mode -> 5. Most Banned / Banned By
4. Header "Teams & Players" button integration
"""

import re
from pathlib import Path

APP_JS = Path("owcs-stat-lab 2/app.js")

def patch_app():
    code = APP_JS.read_text(encoding="utf-8")

    # 1. Ensure state has teamStatus default
    if "teamStatus:" not in code:
        code = code.replace("teamRegionFilter: 'ALL',", "teamRegionFilter: 'ALL',\n  teamStatus: 'CURRENT',")

    # 2. Extract and replace teamsPage function
    # Find start and end of function teamsPage()
    t_start = code.find("function teamsPage(){")
    if t_start == -1:
        t_start = code.find("function teamsPage() {")
    if t_start == -1:
        print("Error: function teamsPage() not found")
        return

    t_end = code.find("function rankingsPage(){", t_start)
    if t_end == -1:
        t_end = code.find("function rankingsPage()", t_start)

    old_teams_page = code[t_start:t_end]

    new_teams_page = """function teamsPage() {
  const isKo = state.lang === 'ko';
  state.teamStatus = state.teamStatus || 'CURRENT';

  // 1. Player Profile View
  if (state.player) {
    return renderPlayerProfile(state.player);
  }

  // Load global teams directory
  const globalTeamsObj = window.OWCS_GLOBAL_TEAMS || {};
  const allTeamsDict = globalTeamsObj.teams || {};
  const regions = globalTeamsObj.regions || [
    { code: 'ALL', nameKo: '전체 지역', nameEn: 'All Regions', icon: '🌐' },
    { code: 'KR', nameKo: '한국 (Korea)', nameEn: 'Korea', icon: '🇰🇷' },
    { code: 'NA', nameKo: '북미 (North America)', nameEn: 'North America', icon: '🇺🇸' },
    { code: 'EMEA', nameKo: '유럽·중동 (EMEA)', nameEn: 'Europe & Middle East', icon: '🇪🇺' },
    { code: 'CN', nameKo: '중국 (China)', nameEn: 'China', icon: '🇨🇳' },
    { code: 'JP', nameKo: '일본 (Japan)', nameEn: 'Japan', icon: '🇯🇵' },
    { code: 'PA', nameKo: '태평양 (Pacific)', nameEn: 'Pacific', icon: '🌏' }
  ];

  // 2. Team Detail Profile View
  if (state.team) {
    const tmId = state.team;
    const gt = allTeamsDict[tmId] || {};
    const isPast = (gt.status === 'PAST');
    const teamFullName = gt.name || tmId;
    const teamRegion = gt.region || 'KR';
    const rs = isPast ? (gt.finalRoster || gt.activeRoster || []) : (gt.activeRoster || []);
    const lpUrl = teamLiquipediaUrl(tmId);
    const trophies = gt.trophies || [];
    const coaches = gt.coachingStaff || [
      { name: 'Head Coach', role: 'Head Coach', roleKo: '감독', nationality: '🇰🇷 KR' }
    ];
    const history = gt.transfers || gt.rosterHistory || [
      { date: '2026-03', type: 'IN', player: 'Core Roster', role: 'ALL', details: 'OWCS 2026 시즌 공식 로스터' }
    ];

    // Roster Cards HTML (Active or Final)
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
              ${p.joinDate ? `<div style="font-size:11px;color:var(--text-muted);margin-top:2px;">입단: ${p.joinDate}</div>` : ''}
              ${sigHeroes ? `<div style="font-size:11px;color:#38bdf8;margin-top:4px;">🎯 ${sigHeroes}</div>` : ''}
            </div>
            <span class="role ${pRole}" style="font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;">${pRole}</span>
          </div>
        </div>
      `;
    }).join('');

    // Transfers / History HTML
    const historyHtml = history.map(h => {
      const dt = h.date || h.period || '2025';
      const badgeCls = h.type === 'IN' ? 'IN' : h.type === 'OUT' ? 'OUT' : 'RENEW';
      const badgeText = h.type === 'IN' ? '영입 (IN)' : h.type === 'OUT' ? '방출 (OUT)' : h.type === 'ACQUISITION' ? '구단 인수' : h.type === 'MERGER' ? '구단 합병' : '리브랜딩';
      return `
        <div class="timeline-item">
          <div class="timeline-dot ${badgeCls}"></div>
          <div class="timeline-content">
            <div class="timeline-header">
              <span class="timeline-period">📅 ${dt}</span>
              <span class="timeline-badge ${badgeCls}">${badgeText}</span>
              <strong style="color:#fff;font-size:13px;margin-left:4px;">${h.player || ''}</strong>
              ${h.role ? `<span style="font-size:11px;color:var(--text-muted);">(${h.role})</span>` : ''}
            </div>
            <div style="font-size:13px;color:var(--text);margin-top:4px;">${h.details}</div>
          </div>
        </div>
      `;
    }).join('');

    // Coaching Staff HTML
    const coachingHtml = coaches.map(c => `
      <div class="coach-card">
        <div style="font-size:24px;">👔</div>
        <div>
          <strong style="color:#fff;font-size:14px;display:block;">${c.name} ${c.realName ? `<span class="muted" style="font-size:12px;font-weight:400;">(${c.realName})</span>` : ''}</strong>
          <span style="font-size:12px;color:var(--text-muted);">${c.roleKo || c.role || '코치'} · ${c.nationality || '🇰🇷 KR'}</span>
        </div>
      </div>
    `).join('');

    // 5 Mode Best/Worst Map Cards HTML
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

    // Most Banned Against Top 5
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

    // Most Banned by [TEAM] Top 5
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

    // Shared Header
    const teamHeaderCard = `
      <div class="page-title" style="display:flex;justify-content:space-between;align-items:center;">
        <div>
          <button class="chip" id="backTeams">← ${isKo ? '팀 디렉터리 목록으로 돌아가기' : 'Back to Teams List'}</button>
        </div>
        <div class="profile-header-actions" style="margin-top:0;">
          <a href="${lpUrl}" target="_blank" rel="noopener noreferrer" class="btn-lp-external" style="text-decoration:none;">
            <span class="lp-external-icon">📖</span> Liquipedia
          </a>
        </div>
      </div>

      <div class="card team-simple-header-card" style="border-left: 6px solid ${gt.color || '#38bdf8'};margin-bottom:20px;">
        <div class="team-simple-header" style="display:flex;align-items:center;gap:20px;flex-wrap:wrap;">
          <div class="team-detail-logo-wrap">
            ${teamLogo(tmId, "team-detail-logo-lg")}
          </div>
          <div>
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
              <span class="region-badge ${teamRegion}">${teamRegion}</span>
              <span class="badge-status ${isPast ? 'badge-past' : 'badge-current'}" style="${isPast ? 'background:rgba(100,116,139,0.2);color:#94a3b8;border:1px solid rgba(100,116,139,0.3);' : 'background:rgba(34,197,94,0.15);color:#4ade80;border:1px solid rgba(34,197,94,0.3);'}padding:3px 8px;border-radius:6px;font-size:11px;font-weight:700;">
                ${isPast ? '⚪ Past OWCS Team (역대/합병팀)' : '🟢 Current OWCS Team (현재 활성팀)'}
              </span>
              <span style="font-size:12px;color:var(--text-muted);">${gt.country || ''}</span>
              ${gt.founded ? `<span style="font-size:12px;color:var(--text-muted);">· 창단: ${gt.founded}년</span>` : ''}
            </div>
            <h1 class="team-simple-title" style="margin:0 0 6px 0;">${teamFullName} <span class="muted" style="font-size:20px;font-weight:400">(${tmId})</span></h1>
            <p class="muted" style="margin:0;font-size:13px;">${gt.historyNotes || 'OWCS 공식 프로 팀 정보 및 경기 데이터 분석'}</p>
          </div>
        </div>
      </div>
    `;

    // Section Components
    const achievementsSection = `
      <!-- Key Achievements -->
      <div class="card team-trophy-section" style="margin-bottom:24px;">
        <div class="section-head-simple">
          <h2>🏆 ${isKo ? '주요 우승 및 입상 기록 (Key Achievements)' : 'Key Achievements'} (${trophies.length} Titles)</h2>
        </div>
        ${trophies.length ? `
          <div class="trophy-badge-list" style="display:flex;flex-wrap:wrap;gap:8px;">
            ${trophies.map(tTitle => `<span class="badge-owcs-title" style="background:rgba(245,158,11,0.12);color:#fbbf24;border:1px solid rgba(245,158,11,0.3);padding:5px 12px;border-radius:8px;font-size:12px;font-weight:700;">🏆 ${tTitle}</span>`).join('')}
          </div>
        ` : `<div class="trophy-empty-msg muted">${isKo ? '공식 우승 기록 없음' : 'No major titles recorded'}</div>`}
      </div>
    `;

    const rosterSection = `
      <!-- ${isPast ? 'Final Roster' : 'Active Roster'} -->
      <div class="section" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;margin-bottom:24px;">
        <div class="section-head-simple">
          <h2>👥 ${isPast ? '마지막 공식 로스터 (Final Roster)' : '현재 로스터 (Active Roster)'} (${rs.length} Players)</h2>
          <span style="font-size:12px;color:var(--text-muted);">${isKo ? '선수를 클릭하면 세부 개인 지표 및 방사형 차트가 열립니다.' : 'Click player to inspect detailed profile'}</span>
        </div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(220px, 1fr));gap:14px;margin-top:14px;">
          ${rosterHtml}
        </div>
      </div>
    `;

    const transfersSection = `
      <!-- Transfers / History -->
      <div class="section" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;margin-bottom:24px;">
        <div class="section-head-simple">
          <h2>📜 ${isPast ? '구단 인수/합병 및 이적 연혁 (Transfers & Historical Timeline)' : '로스터 연혁 및 이적 타임라인 (Transfers & History)'}</h2>
          <span style="font-size:12px;color:var(--text-muted);">${isKo ? '공식 영입, 방출, 인수, 합병 및 재계약 기록' : 'Official transfers, acquisitions, mergers, and renewals'}</span>
        </div>
        <div class="roster-timeline" style="margin-top:14px;">
          ${historyHtml}
        </div>
      </div>
    `;

    const coachingSection = `
      <!-- Coaching Staff -->
      <div class="section" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;margin-bottom:24px;">
        <div class="section-head-simple">
          <h2>👔 코칭스태프 (Coaching Staff)</h2>
          <span style="font-size:12px;color:var(--text-muted);">${isKo ? '지도자 및 전략 분석진 명단' : 'Staff and Strategic Analysts'}</span>
        </div>
        <div class="coach-grid" style="margin-top:14px;">
          ${coachingHtml}
        </div>
      </div>
    `;

    const bestWorstSection = `
      <!-- Best/Worst Map By Mode -->
      <div class="section" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;margin-bottom:24px;">
        <div class="section-head-simple">
          <h2>🗺️ 전장 유형별 최고 / 최저 승률 전장 (Best & Worst Map by Mode)</h2>
          <span style="font-size:12px;color:var(--text-muted);">쟁탈 · 혼합 · 플래시포인트 · 밀기 · 호위 5대 전장 모드별 공식전 승률 비교</span>
        </div>
        <div class="mode-maps-grid">
          ${modeCardsHtml}
        </div>
      </div>
    `;

    const bansSection = `
      <!-- Most Banned / Banned by Heroes -->
      <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(320px, 1fr));gap:20px;margin-bottom:24px;">
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

    // Render strictly ordered by user requirement:
    if (!isPast) {
      // Current OWCS Teams: Key Achievements -> Active Roster -> Transfers -> Coaching Staff -> Best/Worst Map By Mode -> Most Banned/Banned by Heroes
      return `
        ${teamHeaderCard}
        ${achievementsSection}
        ${rosterSection}
        ${transfersSection}
        ${coachingSection}
        ${bestWorstSection}
        ${bansSection}
      `;
    } else {
      // Past OWCS Teams: Final Roster -> Transfers -> Coaching Staff -> Best/Worst Map By Mode -> Most Banned/Banned by Heroes
      return `
        ${teamHeaderCard}
        ${rosterSection}
        ${transfersSection}
        ${coachingSection}
        ${bestWorstSection}
        ${bansSection}
      `;
    }
  }

  // 3. Teams List View with Current vs Past Toggle
  const currentStatus = state.teamStatus || 'CURRENT';
  const currentRegion = state.teamRegionFilter || 'ALL';
  const currentSearch = (state.teamSearch || '').toLowerCase().trim();

  const allTeamsList = Object.values(allTeamsDict);
  const filteredTeams = allTeamsList.filter(tm => {
    // Status filter (CURRENT vs PAST)
    if (tm.status && tm.status !== currentStatus) return false;
    if (!tm.status && currentStatus === 'PAST') return false;

    // Region filter
    if (currentRegion !== 'ALL' && tm.region !== currentRegion) return false;

    // Search query
    if (currentSearch) {
      const q = currentSearch;
      const matchName = (tm.name || '').toLowerCase().includes(q);
      const matchId = (tm.id || '').toLowerCase().includes(q);
      const rosterList = (tm.activeRoster || tm.finalRoster || []);
      const matchPlayer = rosterList.some(p => (p.player || '').toLowerCase().includes(q));
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
    const isPast = (tm.status === 'PAST');
    const rosterList = isPast ? (tm.finalRoster || tm.activeRoster || []) : (tm.activeRoster || []);
    const rosterPills = rosterList.slice(0, 5).map(p => `
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
                  ${isPast ? '<span style="font-size:10px;padding:1px 5px;background:rgba(100,116,139,0.2);color:#94a3b8;border:1px solid rgba(100,116,139,0.4);border-radius:4px;">PAST</span>' : ''}
                </div>
                <div class="muted" style="font-size:12px;margin-top:2px;">${tm.id} · ${tm.country || ''}</div>
              </div>
            </div>
            ${trophiesCount > 0 ? `<span class="team-card-trophy-badge" title="${trophiesCount} Major Trophies" style="font-size:16px;">🏆</span>` : ''}
          </div>

          <div style="margin:12px 0 8px 0;padding-top:10px;border-top:1px solid rgba(255,255,255,0.06);">
            <div style="font-size:11px;color:var(--text-muted);margin-bottom:6px;">${isPast ? '마지막 로스터 (Final Lineup):' : '주요 로스터 (Active Lineup):'}</div>
            <div style="display:flex;flex-wrap:wrap;gap:4px;">
              ${rosterPills}
            </div>
          </div>

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

    <!-- Current vs Past Team Switcher -->
    <div style="display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap;">
      <button class="chip team-status-toggle ${currentStatus === 'CURRENT' ? 'active' : ''}" data-team-status="CURRENT" style="cursor:pointer;padding:8px 18px;font-size:13px;border-radius:8px;">
        <span>🟢</span> <b>Current OWCS Teams (현재 활성 참가팀)</b>
      </button>
      <button class="chip team-status-toggle ${currentStatus === 'PAST' ? 'active' : ''}" data-team-status="PAST" style="cursor:pointer;padding:8px 18px;font-size:13px;border-radius:8px;">
        <span>⚪</span> <b>Past OWCS Teams (역대/합병/해체팀)</b>
      </button>
    </div>

    <!-- Filter Toolbar -->
    <div class="card toolbar team-toolbar" style="margin-bottom:24px;padding:16px;">
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
          ${regionChipsHtml}
        </div>
        <div style="display:flex;gap:12px;align-items:center;">
          <select id="teamRegionFilter" class="select-input" style="padding:8px 12px;background:var(--bg-card);border:1px solid rgba(255,255,255,0.1);color:#fff;border-radius:8px;font-size:13px;">
            ${regionOptionsHtml}
          </select>
          <input type="text" id="teamSearchInput" placeholder="${isKo ? '팀명, 선수명, ID 검색...' : 'Search team or player...'}" value="${state.teamSearch || ''}" style="padding:8px 14px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);border-radius:8px;color:#fff;font-size:13px;min-width:200px;" />
        </div>
      </div>
    </div>

    <div style="margin-bottom:14px;font-size:13px;color:var(--text-muted);display:flex;justify-content:space-between;align-items:center;">
      <span>총 <b>${filteredTeams.length}</b>개 팀이 검색되었습니다.</span>
      <span style="font-size:11px;">※ 팀 카드를 클릭하면 상세 프로필, 로스터 연혁, 5개 모드별 Best/Worst 전장 비교가 열립니다.</span>
    </div>

    <div class="team-grid" style="display:grid;grid-template-columns:repeat(auto-fill, minmax(320px, 1fr));gap:18px;">
      ${teamCardsHtml}
    </div>
  `;
}
"""

    code = code[:t_start] + new_teams_page + code[t_end:]

    # 3. Add event binding for data-team-status
    if "data-team-status" not in code:
        bind_target = "document.querySelectorAll('[data-region-chip]').forEach(btn => {"
        bind_replacement = """document.querySelectorAll('[data-team-status]').forEach(btn => {
    btn.onclick = () => {
      state.teamStatus = btn.dataset.teamStatus;
      render();
    };
  });
  document.querySelectorAll('[data-region-chip]').forEach(btn => {"""
        code = code.replace(bind_target, bind_replacement)

    APP_JS.write_text(code, encoding="utf-8")
    print("Successfully patched app.js with Current vs Past team functionality!")

if __name__ == "__main__":
    patch_app()
