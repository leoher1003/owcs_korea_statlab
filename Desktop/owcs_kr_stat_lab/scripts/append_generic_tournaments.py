#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
append_generic_tournaments.py
Appends genericTournamentPreviewPage and genericTournamentMatchesPage to app.js,
and ensures bind() wires up all tournament tab, filter, and modal events.
"""

from pathlib import Path

APP_JS = Path("owcs-stat-lab 2/app.js")

GENERIC_CODE = """
// ==============================================================================
// GENERIC TOURNAMENT PREVIEW & MATCH EXPLORER
// Supports: asia-s1, bootcamp-s1, clash-2026, midseason-2026, owwc-2026
// ==============================================================================

function getMapImageSrc(mapName) {
  if (!mapName) return '';
  const clean = mapName.toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '');
  return `assets/maps/${clean}.jpg`;
}

function genericTournamentPreviewPage(tourneyKey) {
  const ds = getTourneyDataset(tourneyKey) || {};
  const tour = ds.tournament || {};
  const isKo = state.lang === 'ko';
  const curTab = state.tTab || 'schedule';
  const curPhase = state.tPhase || 'All';
  const curSearch = (state.tSearch || '').toLowerCase().trim();
  const curTeam = state.tTeam || 'ALL';
  const tourName = isKo ? (tour.nameKo || tour.name) : tour.name;

  const navTabs = [
    { id: 'schedule', icon: '📅', ko: '경기 일정', en: 'Schedule' },
    { id: 'standings', icon: '🏆', ko: '순위표', en: 'Standings' },
    { id: 'mappool', icon: '🗺️', ko: '공식 맵 풀', en: 'Map Pool' },
    { id: 'teams', icon: '👥', ko: '참가팀 로스터', en: 'Teams' },
    { id: 'all', icon: '📑', ko: '전체 보기', en: 'View All' }
  ];

  const navTabsHtml = navTabs.map(t => `
    <button class="tabbtn s3-nav-tab ${curTab === t.id ? 'active' : ''}" data-tourney-tab="${t.id}">
      <span>${t.icon}</span>
      <b>${isKo ? t.ko : t.en}</b>
    </button>
  `).join('');

  // 1. Dynamic Standings Calculation
  const matches = ds.matches || [];
  const teams = ds.teams || [];
  const teamStats = {};

  teams.forEach(t => {
    teamStats[t.short] = {
      team: t.short,
      name: t.name,
      seed: isKo ? (t.seedKo || t.seed) : t.seed,
      color: t.color || '#64748b',
      mw: 0,
      ml: 0,
      mapw: 0,
      mapl: 0
    };
  });

  matches.forEach(m => {
    const t1 = m.team1;
    const t2 = m.team2;
    if (!teamStats[t1]) teamStats[t1] = { team: t1, name: ds.teamNames?.[t1] || t1, seed: '-', color: '#64748b', mw: 0, ml: 0, mapw: 0, mapl: 0 };
    if (!teamStats[t2]) teamStats[t2] = { team: t2, name: ds.teamNames?.[t2] || t2, seed: '-', color: '#64748b', mw: 0, ml: 0, mapw: 0, mapl: 0 };

    const s1 = Number(m.score1) || 0;
    const s2 = Number(m.score2) || 0;
    teamStats[t1].mapw += s1;
    teamStats[t1].mapl += s2;
    teamStats[t2].mapw += s2;
    teamStats[t2].mapl += s1;

    if (m.winner === t1) {
      teamStats[t1].mw += 1;
      teamStats[t2].ml += 1;
    } else if (m.winner === t2) {
      teamStats[t2].mw += 1;
      teamStats[t1].ml += 1;
    }
  });

  const standingsList = Object.values(teamStats).map(s => {
    const totalM = s.mw + s.ml;
    const winrate = totalM > 0 ? Math.round((s.mw / totalM) * 100) : 0;
    const diff = s.mapw - s.mapl;
    return {
      ...s,
      diff: diff > 0 ? `+${diff}` : `${diff}`,
      rawDiff: diff,
      winrate: `${winrate}%`,
      rawWinrate: winrate
    };
  }).sort((a, b) => {
    if (b.mw !== a.mw) return b.mw - a.mw;
    if (b.rawDiff !== a.rawDiff) return b.rawDiff - a.rawDiff;
    return b.mapw - a.mapw;
  });

  const standingsRowsHtml = standingsList.map((s, idx) => {
    const rank = idx + 1;
    const isTop1 = rank === 1;
    const isTop2 = rank === 2;
    const rankClass = isTop1 ? 'status-green' : (isTop2 ? 'status-yellow' : 'status-gray');

    return `
      <tr class="s2-standing-row tier-rr2" data-tourney-team="${s.team}">
        <td class="col-rank" style="text-align:center;">
          <span class="rank-num ${rankClass}">${rank}</span>
        </td>
        <td class="col-team">
          <div class="team-cell">
            ${teamLogo(s.team, 's2-standing-team-logo')}
            <div class="team-names">
              <strong class="team-abbr">${s.team}</strong>
              <span class="team-full">${s.name}</span>
            </div>
          </div>
        </td>
        <td class="col-series" style="text-align:center;">
          <b style="color:#fff;">${s.mw}W - ${s.ml}L</b>
        </td>
        <td class="col-winrate" style="text-align:center;">
          <span class="s2-winrate-tag">${s.winrate}</span>
        </td>
        <td class="col-maps" style="text-align:center;">
          <span>${s.mapw}W - ${s.mapl}L</span>
        </td>
        <td class="col-diff" style="text-align:center;">
          <span class="s2-diff-tag ${s.rawDiff >= 0 ? 'pos' : 'neg'}">${s.diff}</span>
        </td>
        <td class="col-status" style="text-align:center;">
          <span class="s2-qual-badge tier-rr2" style="background:${s.color}22;color:${s.color};border:1px solid ${s.color}44;">
            ${s.seed || (isTop1 ? 'Champion' : isTop2 ? 'Runner-up' : 'Participant')}
          </span>
        </td>
      </tr>
    `;
  }).join('');

  // 2. Schedule Filters & Match Rows
  const allPhases = ['All', ...new Set(matches.map(m => m.phase).filter(Boolean))];
  const phasePillsHtml = allPhases.map(p => `
    <button class="chip ${curPhase === p ? 'active' : ''}" data-tourney-phase="${p}">
      ${p === 'All' ? (isKo ? '전체 경기' : 'All Matches') : p}
    </button>
  `).join('');

  const filteredMatches = matches.filter(m => {
    if (curPhase !== 'All' && m.phase !== curPhase) return false;
    if (curTeam !== 'ALL' && m.team1 !== curTeam && m.team2 !== curTeam) return false;
    if (curSearch) {
      const q = curSearch;
      const t1 = (m.team1 || '').toLowerCase();
      const t2 = (m.team2 || '').toLowerCase();
      const mvp = (m.mvp || '').toLowerCase();
      const mapMatch = (m.sets || []).some(s => (s.map || '').toLowerCase().includes(q) || (s.mapKo || '').toLowerCase().includes(q));
      if (!t1.includes(q) && !t2.includes(q) && !mvp.includes(q) && !mapMatch) return false;
    }
    return true;
  });

  const matchRowsHtml = filteredMatches.map(m => {
    const isT1Win = m.winner === m.team1;
    const isT2Win = m.winner === m.team2;
    const t1Name = ds.teamNames?.[m.team1] || m.team1;
    const t2Name = ds.teamNames?.[m.team2] || m.team2;
    const mvpHtml = m.mvp ? `<span class="s2-badge-mvp" style="background:rgba(245,158,11,0.15);color:#fbbf24;border:1px solid rgba(245,158,11,0.3);padding:2px 7px;border-radius:12px;font-size:11px;font-weight:700;">⭐ MVP: ${m.mvp}</span>` : '';
    const vodHtml = m.vod ? `<a class="btn-ghost" href="${m.vod}" target="_blank" rel="noopener" onclick="event.stopPropagation();" style="padding:3px 9px;font-size:11px;text-decoration:none;border-radius:6px;border:1px solid rgba(255,255,255,0.15);color:var(--text);">🎬 VOD</a>` : '';

    return `
      <div class="s3-match-row s2-match-row s1-match-row tourney-match-row completed" data-match-id="${m.matchId}" data-tourney="${tourneyKey}" title="${isKo ? '클릭하여 세부 스코어 및 밴픽 보기' : 'Click to view detail scores and bans'}" style="cursor:pointer;">
        <div class="s3-match-meta">
          <span class="s3-match-date">📅 ${m.date} ${m.time || ''}</span>
          <span class="s3-match-status-badge live" style="background:rgba(59,130,246,0.15);color:#60a5fa;border:1px solid rgba(59,130,246,0.3);">${m.phaseKo || m.phase}</span>
          ${mvpHtml}
        </div>
        <div class="s3-match-teams">
          <div class="s3-match-team home ${isT1Win ? 'winner' : ''}">
            ${teamLogo(m.team1, 's3-team-logo')}
            <span class="s3-team-name">${m.team1}</span>
            <span class="s2-team-subname" style="font-size:11px;color:var(--text-muted);margin-left:4px;">${t1Name}</span>
          </div>
          <div class="s3-match-score s2-match-score">
            <span class="s2-score-num ${isT1Win ? 'win-score' : ''}">${m.score1}</span>
            <span class="s2-score-sep">:</span>
            <span class="s2-score-num ${isT2Win ? 'win-score' : ''}">${m.score2}</span>
          </div>
          <div class="s3-match-team away ${isT2Win ? 'winner' : ''}">
            <span class="s2-team-subname" style="font-size:11px;color:var(--text-muted);margin-right:4px;">${t2Name}</span>
            <span class="s3-team-name">${m.team2}</span>
            ${teamLogo(m.team2, 's3-team-logo')}
          </div>
        </div>
        <div class="s3-match-footer" style="display:flex;align-items:center;justify-content:space-between;margin-top:8px;padding-top:6px;border-top:1px solid rgba(255,255,255,0.06);font-size:12px;color:var(--text-muted);">
          <span>${m.casters && m.casters.length ? '🎙️ ' + m.casters.join(', ') : '🎙️ Official Broadcast'}</span>
          <div style="display:flex;align-items:center;gap:8px;">
            ${vodHtml}
            <span style="color:var(--primary);font-weight:700;">${isKo ? '세부 정보 ›' : 'Details ›'}</span>
          </div>
        </div>
      </div>
    `;
  }).join('');

  // 3. Map Pool Cards
  const mapPool = ds.mapPool || {};
  const mapPoolCardsHtml = Object.keys(mapPool).map(mtype => {
    const p = mapPool[mtype];
    const maps = p.maps || [];
    return `
      <div class="s3-map-type-card">
        <div class="s3-map-type-header" style="border-left: 4px solid ${p.color};">
          <div class="s3-map-type-icon">${p.icon}</div>
          <div>
            <h3>${isKo ? p.nameKo : p.nameEn}</h3>
            <span class="s3-map-type-en">${p.nameEn} (${maps.length} Maps)</span>
          </div>
        </div>
        <div class="s3-map-grid">
          ${maps.map(m => `
            <div class="s3-map-item" style="position:relative;overflow:hidden;border-radius:8px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);padding:10px;">
              <div class="s3-map-name" style="font-weight:700;font-size:14px;color:#fff;">${isKo ? m.nameKo : m.nameEn}</div>
              <div class="s3-map-name-en" style="font-size:11px;color:var(--text-muted);">${m.nameEn}</div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }).join('');

  // 4. Teams Cards
  const teamCardsHtml = teams.map(tm => {
    const roster = tm.roster || [];
    return `
      <div class="s3-team-card" style="border-top: 3px solid ${tm.color || '#64748b'};">
        <div class="s3-team-header">
          ${teamLogo(tm.short, 's3-team-card-logo')}
          <div>
            <h4>${tm.name}</h4>
            <span class="s3-team-seed" style="background:${tm.color || '#64748b'}22;color:${tm.color || '#64748b'};border:1px solid ${tm.color || '#64748b'}44;">
              ${isKo ? (tm.seedKo || tm.seed) : tm.seed}
            </span>
          </div>
        </div>
        <div class="s3-roster-list">
          ${roster.map(r => `
            <div class="s3-roster-item">
              <span class="s3-role-badge ${r.role}">${r.role}</span>
              <span class="s3-player-name">${r.name}</span>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }).join('');

  // Sections
  const scheduleSection = `
    <div class="section s3-section" id="tourneyScheduleSec">
      <div class="section-header">
        <div>
          <h2>${isKo ? '📅 대회 경기 일정 및 결과' : '📅 Match Schedule & Results'}</h2>
          <p class="muted">${isKo ? '총 ' + matches.length + '경기 세부 스코어, 밴픽, MVP 및 VOD 리플레이 (경기를 클릭하면 상세 정보가 표시됩니다)' : 'Total ' + matches.length + ' matches with set scores, bans, and VODs (Click match to open detail modal)'}</p>
        </div>
      </div>
      <div class="chips" style="margin-bottom:14px;display:flex;flex-wrap:wrap;gap:8px;">
        ${phasePillsHtml}
      </div>
      <div class="s3-matches-list">
        ${matchRowsHtml || '<div class="muted" style="text-align:center;padding:30px;">조건에 일치하는 경기가 없습니다.</div>'}
      </div>
    </div>
  `;

  const standingsSection = `
    <div class="section s3-section" id="tourneyStandingsSec">
      <div class="section-header">
        <div>
          <h2>${isKo ? '🏆 공식 토너먼트 순위표' : '🏆 Official Tournament Standings'}</h2>
          <p class="muted">${isKo ? '경기 결과 기반 실시간 승패, 득실차, 승률 통계' : 'Standings calculated dynamically from match results'}</p>
        </div>
      </div>
      <div class="table-wrap s2-standings-table-wrap">
        <table class="table s2-standings-table">
          <thead>
            <tr>
              <th style="width:48px;text-align:center;">#</th>
              <th>${isKo ? '팀' : 'Team'}</th>
              <th style="text-align:center;">${isKo ? '매치 성적' : 'Series'}</th>
              <th style="text-align:center;">${isKo ? '승률' : 'Win%'}</th>
              <th style="text-align:center;">${isKo ? '세트 스코어' : 'Maps'}</th>
              <th style="text-align:center;">${isKo ? '세트 득실' : 'Diff'}</th>
              <th style="text-align:center;">${isKo ? '시드 / 최종 순위' : 'Status'}</th>
            </tr>
          </thead>
          <tbody>
            ${standingsRowsHtml}
          </tbody>
        </table>
      </div>
    </div>
  `;

  const mapPoolSection = `
    <div class="section s3-section" id="tourneyMapPoolSec">
      <div class="section-header">
        <div>
          <h2>${isKo ? '🗺️ 공식 대회 전장 풀' : '🗺️ Official Map Pool'}</h2>
          <p class="muted">${isKo ? '쟁탈, 혼합, 플래시포인트, 밀기, 호위 전장 풀' : 'Official map pool across all competitive game modes'}</p>
        </div>
      </div>
      <div class="s3-map-pool-grid">
        ${mapPoolCardsHtml}
      </div>
    </div>
  `;

  const teamsSection = `
    <div class="section s3-section" id="tourneyTeamsSec">
      <div class="section-header">
        <div>
          <h2>${isKo ? '👥 참가팀 및 공식 로스터' : '👥 Teams & Rosters'}</h2>
          <p class="muted">${isKo ? '총 ' + teams.length + '개 참가팀의 포지션별 선수 라인업' : 'Total ' + teams.length + ' teams with player position rosters'}</p>
        </div>
      </div>
      <div class="s3-teams-grid">
        ${teamCardsHtml}
      </div>
    </div>
  `;

  let activeContentHtml = '';
  if (curTab === 'standings') activeContentHtml = standingsSection;
  else if (curTab === 'mappool') activeContentHtml = mapPoolSection;
  else if (curTab === 'teams') activeContentHtml = teamsSection;
  else if (curTab === 'all') activeContentHtml = scheduleSection + standingsSection + mapPoolSection + teamsSection;
  else activeContentHtml = scheduleSection;

  return `
    <div class="page-title stage3-hero-banner" style="background:linear-gradient(135deg, rgba(255,255,255,0.06), rgba(0,0,0,0.6));border:1px solid rgba(255,255,255,0.12);border-radius:14px;padding:24px;margin-bottom:20px;">
      <div class="stage3-hero-content">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
          <span class="badge live" style="background:#f59e0b22;color:#f59e0b;border:1px solid #f59e0b44;padding:4px 10px;border-radius:20px;font-size:12px;font-weight:800;">${tour.tier || 'S-TIER'}</span>
          <span class="s3-dday-badge" style="background:rgba(16,185,129,0.15);color:#34d399;border:1px solid rgba(16,185,129,0.3);padding:4px 10px;border-radius:20px;font-size:12px;font-weight:700;">${isKo ? '결과 확정' : 'Completed'}</span>
          <span style="font-size:12px;color:var(--text-muted);">📅 ${tour.startDate} ~ ${tour.endDate}</span>
        </div>
        <h1 style="font-size:28px;font-weight:900;color:#fff;margin:0 0 6px 0;">${tourName}</h1>
        <p style="color:var(--text-muted);font-size:14px;margin:0 0 16px 0;">
          ${tour.venue ? '📍 ' + tour.venue + ' · ' : ''}${tour.prizePool ? '💰 총 상금 ' + tour.prizePool : ''}
        </p>
        <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
          <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);padding:8px 16px;border-radius:10px;display:flex;align-items:center;gap:8px;">
            <span>🏆 우승 (Champion):</span>
            ${teamLogo(tour.champion, 'team-logo-small')}
            <strong style="color:#fbbf24;">${tour.champion}</strong>
          </div>
          ${tour.runnerUp ? `
          <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);padding:8px 16px;border-radius:10px;display:flex;align-items:center;gap:8px;">
            <span>🥈 준우승:</span>
            ${teamLogo(tour.runnerUp, 'team-logo-small')}
            <strong style="color:#e2e8f0;">${tour.runnerUp}</strong>
          </div>` : ''}
        </div>
      </div>
    </div>

    <!-- Sub-navigation Tabs -->
    <div class="s3-nav-tabs" style="margin-bottom:20px;display:flex;gap:8px;overflow-x:auto;">
      ${navTabsHtml}
    </div>

    ${activeContentHtml}
  `;
}

function genericTournamentMatchesPage(tourneyKey) {
  const ds = getTourneyDataset(tourneyKey) || {};
  const tour = ds.tournament || {};
  const isKo = state.lang === 'ko';
  const matches = ds.matches || [];
  const curPhase = state.tPhase || 'All';
  const curBanTeam = state.tBanTeam || 'All';

  // Metrics
  const totalMatches = matches.length;
  let totalSets = 0;
  const mapCounts = {};
  const banCounts = {};

  matches.forEach(m => {
    (m.sets || []).forEach(s => {
      totalSets++;
      if (s.map) mapCounts[s.map] = (mapCounts[s.map] || 0) + 1;
      if (s.bans) {
        if (s.bans.t1b1) banCounts[s.bans.t1b1] = (banCounts[s.bans.t1b1] || 0) + 1;
        if (s.bans.t2b1) banCounts[s.bans.t2b1] = (banCounts[s.bans.t2b1] || 0) + 1;
      }
    });
  });

  const mostPlayedMap = Object.entries(mapCounts).sort((a,b)=>b[1]-a[1])[0] || ['-', 0];
  const mostBannedHero = Object.entries(banCounts).sort((a,b)=>b[1]-a[1])[0] || ['-', 0];

  const allPhases = ['All', ...new Set(matches.map(m => m.phase).filter(Boolean))];
  const phasePillsHtml = allPhases.map(p => `
    <button class="chip ${curPhase === p ? 'active' : ''}" data-tourney-phase="${p}">
      ${p === 'All' ? (isKo ? '전체 경기' : 'All Matches') : p}
    </button>
  `).join('');

  const filteredMatches = matches.filter(m => curPhase === 'All' || m.phase === curPhase);

  const matchCardsHtml = filteredMatches.map(m => {
    const isT1Win = m.winner === m.team1;
    const isT2Win = m.winner === m.team2;
    const sets = m.sets || [];

    const setPills = sets.map(s => {
      const isSetT1Win = s.winner === m.team1 || s.winner === '1';
      const isSetT2Win = s.winner === m.team2 || s.winner === '2';
      return `
        <span class="set-pill" style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);padding:2px 8px;border-radius:6px;font-size:11px;">
          ${isKo ? (s.mapKo || s.map) : s.map} 
          <b style="color:${isSetT1Win ? '#34d399' : isSetT2Win ? '#f87171' : '#fff'};">${s.score1 || 0}:${s.score2 || 0}</b>
        </span>
      `;
    }).join(' ');

    return `
      <div class="match-card" data-match-id="${m.matchId}" data-tourney="${tourneyKey}" style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:16px;margin-bottom:12px;cursor:pointer;" title="${isKo ? '클릭하여 세부 스코어 및 밴픽 보기' : 'Click to view details'}">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
          <span style="font-size:12px;color:var(--text-muted);">📅 ${m.date} · ${m.phaseKo || m.phase}</span>
          ${m.mvp ? `<span style="font-size:11px;font-weight:700;color:#fbbf24;">⭐ MVP: ${m.mvp}</span>` : ''}
        </div>
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
          <div style="display:flex;align-items:center;gap:8px;flex:1;">
            ${teamLogo(m.team1, 'team-logo')}
            <strong style="font-size:16px;color:${isT1Win ? '#34d399' : '#fff'};">${m.team1}</strong>
          </div>
          <div style="font-size:20px;font-weight:900;padding:4px 14px;background:rgba(0,0,0,0.4);border-radius:8px;border:1px solid rgba(255,255,255,0.1);">
            <span style="color:${isT1Win ? '#34d399' : '#fff'};">${m.score1}</span>
            <span style="color:var(--text-muted);margin:0 4px;">:</span>
            <span style="color:${isT2Win ? '#34d399' : '#fff'};">${m.score2}</span>
          </div>
          <div style="display:flex;align-items:center;gap:8px;flex:1;justify-content:flex-end;">
            <strong style="font-size:16px;color:${isT2Win ? '#34d399' : '#fff'};">${m.team2}</strong>
            ${teamLogo(m.team2, 'team-logo')}
          </div>
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:6px;align-items:center;padding-top:8px;border-top:1px solid rgba(255,255,255,0.06);">
          <span style="font-size:11px;color:var(--text-muted);">세트 결과:</span>
          ${setPills || '<span style="font-size:11px;color:var(--text-muted);">기록 없음</span>'}
        </div>
      </div>
    `;
  }).join('');

  // Map Stats Table
  const mapStatsTableHtml = Object.entries(mapCounts).sort((a,b)=>b[1]-a[1]).map(([map, count]) => {
    return `
      <tr>
        <td><strong>${map}</strong></td>
        <td style="text-align:center;">${count}</td>
        <td style="text-align:center;">${Math.round((count / Math.max(1, totalSets)) * 100)}%</td>
      </tr>
    `;
  }).join('');

  // Ban stats table
  const banStatsTableHtml = Object.entries(banCounts).sort((a,b)=>b[1]-a[1]).map(([hero, count]) => {
    return `
      <tr>
        <td><strong>${hero}</strong></td>
        <td style="text-align:center;">${count}</td>
        <td style="text-align:center;">${Math.round((count / Math.max(1, totalSets)) * 100)}%</td>
      </tr>
    `;
  }).join('');

  return `
    <div class="page-title">
      <div>
        <h1>${isKo ? (tour.nameKo || tour.name) + ' 경기 탐색기' : tour.name + ' Match Explorer'}</h1>
        <p>${isKo ? '경기 결과, 세트별 상세 스코어, 밴픽 통계 및 전장 분석' : 'Match results, set details, hero bans, and map analytics'}</p>
      </div>
    </div>

    <!-- Summary Metrics -->
    <div class="metrics-grid" style="display:grid;grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));gap:14px;margin-bottom:20px;">
      <div class="metric-card" style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:16px;">
        <span class="metric-label" style="font-size:12px;color:var(--text-muted);">총 경기 수 (Matches)</span>
        <h2 style="font-size:26px;color:#fff;margin:4px 0 0 0;">${totalMatches}</h2>
      </div>
      <div class="metric-card" style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:16px;">
        <span class="metric-label" style="font-size:12px;color:var(--text-muted);">총 진행 세트 (Maps)</span>
        <h2 style="font-size:26px;color:#38bdf8;margin:4px 0 0 0;">${totalSets}</h2>
      </div>
      <div class="metric-card" style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:16px;">
        <span class="metric-label" style="font-size:12px;color:var(--text-muted);">최다 플레이 맵 (Top Map)</span>
        <h2 style="font-size:20px;color:#34d399;margin:4px 0 0 0;">${mostPlayedMap[0]} (${mostPlayedMap[1]}회)</h2>
      </div>
      <div class="metric-card" style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:16px;">
        <span class="metric-label" style="font-size:12px;color:var(--text-muted);">최다 밴 영웅 (Top Ban)</span>
        <h2 style="font-size:20px;color:#f87171;margin:4px 0 0 0;">${mostBannedHero[0]} (${mostBannedHero[1]}회)</h2>
      </div>
    </div>

    <!-- Phase Filter -->
    <div class="chips" style="margin-bottom:16px;display:flex;flex-wrap:wrap;gap:8px;">
      ${phasePillsHtml}
    </div>

    <!-- Match List Cards -->
    <div class="section" style="margin-bottom:24px;">
      <h2 style="margin-bottom:12px;">${isKo ? '대회 경기 목록 (클릭 시 세부 밴픽/스코어)' : 'Matches (Click for set details & bans)'}</h2>
      <div>
        ${matchCardsHtml}
      </div>
    </div>

    <!-- Map & Ban Stats Breakdown -->
    <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(320px, 1fr));gap:20px;margin-bottom:24px;">
      <div class="section" style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:18px;">
        <h3 style="margin-bottom:12px;">🗺️ 전장별 진행 통계 (Map Frequency)</h3>
        <table class="table" style="width:100%;">
          <thead>
            <tr>
              <th>Map</th>
              <th style="text-align:center;">Played</th>
              <th style="text-align:center;">Pick %</th>
            </tr>
          </thead>
          <tbody>
            ${mapStatsTableHtml}
          </tbody>
        </table>
      </div>

      <div class="section" style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:18px;">
        <h3 style="margin-bottom:12px;">🚫 영웅 밴 통계 (Hero Bans)</h3>
        <table class="table" style="width:100%;">
          <thead>
            <tr>
              <th>Hero</th>
              <th style="text-align:center;">Banned</th>
              <th style="text-align:center;">Ban %</th>
            </tr>
          </thead>
          <tbody>
            ${banStatsTableHtml}
          </tbody>
        </table>
      </div>
    </div>
  `;
}
"""

with open(APP_JS, "r", encoding="utf-8") as f:
    code = f.read()

# Append generic code before the final setup Header Controls & render
if "function genericTournamentPreviewPage" not in code:
    insertion_point = code.rfind("setupHeaderControls();")
    if insertion_point != -1:
        new_code = code[:insertion_point] + "\n" + GENERIC_CODE + "\n\n" + code[insertion_point:]
    else:
        new_code = code + "\n" + GENERIC_CODE
    
    # Also wire up generic subtabs in bind()
    subtab_hook = """  document.querySelectorAll('[data-tourney-tab]').forEach(x => x.onclick = () => {
    state.tTab = x.dataset.tourneyTab;
    render();
  });
  document.querySelectorAll('[data-tourney-phase]').forEach(x => x.onclick = () => {
    state.tPhase = x.dataset.tourneyPhase;
    render();
  });
  document.querySelectorAll('.match-card[data-match-id]').forEach(el => {
    el.onclick = () => {
      const mId = el.dataset.matchId;
      const tKey = el.dataset.tourney || state.tourney;
      openMatchDetailModal(mId, tKey);
    };
  });
  document.querySelectorAll('.tourney-match-row[data-match-id]').forEach(el => {
    el.onclick = () => {
      const mId = el.dataset.matchId;
      const tKey = el.dataset.tourney || state.tourney;
      openMatchDetailModal(mId, tKey);
    };
  });"""
    
    if "data-tourney-tab" not in new_code:
        bind_pos = new_code.find("bindMatchModalEvents();")
        if bind_pos != -1:
            new_code = new_code[:bind_pos] + subtab_hook + "\n  " + new_code[bind_pos:]

    with open(APP_JS, "w", encoding="utf-8") as f:
        f.write(new_code)
    print("Generic tournament pages appended to app.js!")
else:
    print("Generic code already present.")
