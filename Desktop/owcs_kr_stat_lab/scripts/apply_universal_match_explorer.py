#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/apply_universal_match_explorer.py
Applies the Universal Match Explorer engine to app.js, so that ALL tournaments
(kr-s2, kr-s1, asia-s1, bootcamp-s1, clash-2026, midseason-2026, owwc-2026)
use the exact 2026 Korea Stage 2 format:
- Primary Phase Matrix (Round Robin or Groups) with inline map box score
- Phase analytics dropdown (#matchPhase)
- Phase summary metrics cards (Matches, Maps, Top Map, Top Ban)
- Later phases accordions ([data-phase-toggle])
- Hero bans breakdown panel (#banTeam, #banBreakMode, #banBreakValue)
- Bans By [TEAM] & Bans Against [TEAM] with progress bars
- Team Map Win Rate by Type table ([data-mapdrill]) with specific map drilldowns ([data-mapdetail])
- Rich Match Detail Modal with set scores, maps, winners, bans, and MVP
"""

import re
from pathlib import Path

APP_JS = Path("owcs-stat-lab 2/app.js")

UNIVERSAL_EXPLORER_CODE = """
// =========================================================================
// Universal Tournament Match Explorer Engine (Stage 2 Gold Standard Format)
// =========================================================================

function getActiveTourneyData(tourneyKey) {
  const tk = tourneyKey || state.tourney || 'kr-s2';
  const isKo = state.lang === 'ko';

  if (tk === 'kr-s2') {
    const tNames = { ...teamNames };
    const mRows = D.matchInfo.map(r => ({
      ...r,
      'TEAM 1 BAN': r['TEAM 1 BAN'] || '',
      'TEAM 2 BAN': r['TEAM 2 BAN'] || ''
    }));
    const grouped = groupMatches(mRows);
    const phasesList = ['All', ...new Set(mRows.map(r => r.PHASE).filter(Boolean))];
    const teamsList = Object.keys(tNames).length ? Object.keys(tNames) : [...new Set(grouped.flatMap(m => [m.a, m.b]))].sort();

    return {
      tourneyKey: 'kr-s2',
      title: isKo ? 'OWCS 코리아 2026 Stage 2' : 'OWCS Korea 2026 Stage 2',
      matches: grouped,
      mapRows: mRows,
      teamNames: tNames,
      teams: teamsList,
      phases: phasesList,
      primaryPhase: 'Round Robin',
      laterPhases: ['2nd RR', 'LCQ', 'Playoffs'].filter(p => grouped.some(m => m.phase === p))
    };
  }

  const rawDs = getTourneyDataset(tk) || {};
  const tour = rawDs.tournament || {};
  const title = isKo ? (tour.nameKo || tour.name) : tour.name;
  const rawMatches = rawDs.matches || [];
  const tNames = rawDs.teamNames || {};

  const mapRows = [];
  const adaptedMatches = rawMatches.map((m, mIdx) => {
    const key = m.matchId || m.key || `${tk}_m${mIdx+1}`;
    const a = m.team1 || m.a;
    const b = m.team2 || m.b;
    const aw = m.score1 !== undefined ? m.score1 : m.aw;
    const bw = m.score2 !== undefined ? m.score2 : m.bw;
    const phase = m.phase || 'Round Robin';
    const week = m.week || 1;
    const day = m.day || 1;
    const winner = m.winner || (aw > bw ? a : b);

    const setsAdapted = (m.sets || []).map((s, sIdx) => {
      const modeNorm = s.mode ? (s.mode.charAt(0).toUpperCase() + s.mode.slice(1).toLowerCase()) : 'Control';
      const t1b = s.team1Ban || (s.bans && s.bans.t1b1) || '';
      const t2b = s.team2Ban || (s.bans && s.bans.t2b1) || '';
      const row = {
        WEEK: week,
        DAY: day,
        MATCH: m.matchNumber || mIdx + 1,
        'Set #': s.setNumber || sIdx + 1,
        DATE: m.date || '',
        PHASE: phase,
        'TEAM 1': a,
        'TEAM 2': b,
        MAP: s.map,
        'MAP TYPE': modeNorm,
        WINNER: s.winner,
        'TEAM 1 BAN': t1b,
        'TEAM 2 BAN': t2b,
        MATCH_ID: key,
        DETAIL_SCORE: s.detailScore || `${s.score1 || 0} : ${s.score2 || 0}`,
        'TEAM 1 SCORE': s.score1,
        'TEAM 2 SCORE': s.score2
      };
      mapRows.push(row);
      return row;
    });

    return {
      key,
      matchId: key,
      a,
      b,
      team1: a,
      team2: b,
      aw,
      bw,
      score1: aw,
      score2: bw,
      phase,
      week,
      day,
      winner,
      mvp: m.mvp || '',
      date: m.date || '',
      casters: m.casters || [],
      vod: m.vod || '',
      maps: setsAdapted,
      sets: m.sets || setsAdapted
    };
  });

  const phasesList = ['All', ...new Set(adaptedMatches.map(m => m.phase).filter(Boolean))];
  const teamsList = Object.keys(tNames).length ? Object.keys(tNames) : [...new Set(adaptedMatches.flatMap(m => [m.a, m.b]))].sort();

  let primaryPhase = adaptedMatches.some(m => m.phase === 'Round Robin') ? 'Round Robin'
    : (adaptedMatches.some(m => m.phase === 'Group Stage') ? 'Group Stage'
    : (adaptedMatches.some(m => m.phase === 'Round of 12') ? 'Round of 12'
    : (adaptedMatches.some(m => m.phase === 'Quarterfinals') ? 'Quarterfinals' : (phasesList[1] || 'Playoffs'))));

  const laterPhases = phasesList.filter(p => p !== 'All' && p !== primaryPhase);

  return {
    tourneyKey: tk,
    title,
    matches: adaptedMatches,
    mapRows,
    teamNames: tNames,
    teams: teamsList,
    phases: phasesList,
    primaryPhase,
    laterPhases
  };
}

function phaseRows(phase, tData) {
  const td = tData || getActiveTourneyData();
  return td.mapRows.filter(r => phase === 'All' || r.PHASE === phase);
}

function phaseSummary(phase, tData) {
  const td = tData || getActiveTourneyData();
  const rows = phaseRows(phase, td);
  const ms = td.matches.filter(m => phase === 'All' || m.phase === phase);
  const maps = rows.length;

  const mc = {};
  rows.forEach(r => { if(r.MAP) mc[r.MAP] = (mc[r.MAP] || 0) + 1; });
  const mostMap = Object.entries(mc).sort((a,b)=>b[1]-a[1])[0];

  const bc = {};
  rows.forEach(r => {
    [r['TEAM 1 BAN'], r['TEAM 2 BAN']].filter(Boolean).forEach(h => {
      bc[h] = (bc[h] || 0) + 1;
    });
  });
  const mostBan = Object.entries(bc).sort((a,b)=>b[1]-a[1])[0];

  return `
    <div class="phase-summary">
      <div><b>${ms.length}</b><span>${t('phase_matches')}</span></div>
      <div><b>${maps}</b><span>${t('phase_maps')}</span></div>
      <div><b>${mostMap ? mapDisplayName(mostMap[0]) : '—'}</b><span>${t('most_played_map')}</span></div>
      <div><b>${mostBan ? mostBan[0] : '—'}</b><span>${t('most_banned_hero')}</span></div>
    </div>
  `;
}

function matchTooltip(m) {
  if (!m) return '';
  return `<div class="matrix-tip"><strong>${m.a} ${m.aw}–${m.bw} ${m.b}</strong><span>${m.phase} ${m.week ? '· Week ' + m.week : ''}</span>${(m.maps || []).map(x=>`<span>${mapDisplayName(x.MAP)} · ${x.WINNER}</span>`).join('')}</div>`;
}

function roundRobinMatrix(tData) {
  const td = tData || getActiveTourneyData();
  const primaryP = td.primaryPhase;
  const rr = td.matches.filter(m => m.phase === primaryP);
  const teams = [...new Set(rr.flatMap(m => [m.a, m.b]))].sort();

  if (teams.length < 3) {
    // If not a matrix tournament, render opening round cards
    return `
      <div class="bracket-matches-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px;margin-top:10px;">
        ${rr.map(m => `
          <div class="match-list-item card" style="cursor:pointer;" data-match="${m.key}" data-match-id="${m.key}" data-tourney="${td.tourneyKey}">
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <div style="display:flex;align-items:center;gap:8px;">
                ${teamLogo(m.a, 's3-chip-logo')} <b>${m.a}</b> <small style="color:var(--text-muted);">vs</small> <b>${m.b}</b> ${teamLogo(m.b, 's3-chip-logo')}
              </div>
              <strong style="color:#38bdf8;">${m.aw} : ${m.bw}</strong>
            </div>
          </div>
        `).join('')}
      </div>
    `;
  }

  return `
    <div class="rr-wrap">
      <div class="rr-matrix" style="grid-template-columns:80px repeat(${teams.length},minmax(54px,1fr))">
        <div></div>
        ${teams.map(tHead => `<div class="rr-head">${tHead}</div>`).join('')}
        ${teams.map(row => `
          <div class="rr-head row">${row}</div>
          ${teams.map(col => {
            if (row === col) return '<div class="rr-cell diagonal">—</div>';
            const m = rr.find(x => (x.a === row && x.b === col) || (x.a === col && x.b === row));
            if (!m) return '<div class="rr-cell empty">—</div>';
            const rw = m.a === row ? m.aw : m.bw;
            const rl = m.a === row ? m.bw : m.aw;
            return `
              <div class="rr-cell ${rw > rl ? 'win' : 'loss'}" data-match-id="${m.key}" data-match="${m.key}" data-tourney="${td.tourneyKey}" style="cursor:pointer;" title="${row} vs ${col} (${rw}:${rl}) - 클릭하여 세부 스코어 및 밴픽 보기">
                <b>${rw}–${rl}</b>
                ${matchTooltip(m)}
              </div>
            `;
          }).join('')}
        `).join('')}
      </div>
    </div>
  `;
}

function getMapPlaytime(x){
  if (!x) return null;
  if (x.TIME != null && !isNaN(x.TIME) && Number(x.TIME) > 0){
    const sec = Math.round(Number(x.TIME) * 86400);
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${m}:${String(s).padStart(2, '0')}`;
  }
  const mid = x.MATCH_ID;
  const mapName = x.MAP || x.Map;
  if(mid && mapName && typeof D !== 'undefined' && D.rawStats){
    const raw = D.rawStats.find(r => r.MATCH_ID === mid && ((r.Map || r.MAP) === mapName));
    if(raw){
      if(raw.Playtime && typeof raw.Playtime === 'string'){
        const parts = raw.Playtime.trim().split(':');
        if(parts.length === 3){
          const h = parseInt(parts[0], 10);
          const m = parseInt(parts[1], 10) + (h * 60);
          const s = parseInt(parts[2], 10);
          return `${m}:${String(s).padStart(2, '0')}`;
        } else if(parts.length === 2){
          return raw.Playtime.trim();
        }
      }
      if(raw['Playtime(Seconds)'] != null && !isNaN(raw['Playtime(Seconds)'])){
        const sec = Math.round(Number(raw['Playtime(Seconds)']));
        const m = Math.floor(sec / 60);
        const s = sec % 60;
        return `${m}:${String(s).padStart(2, '0')}`;
      }
    }
  }
  return null;
}

function playerBoxScore(matchId, map){
  if(typeof D === 'undefined' || !D.rawStats) return '<div class="note">No player box score available.</div>';
  const rows = D.rawStats.filter(r => r.MATCH_ID === matchId && ((r.Map || r.MAP) === map));
  if(!rows.length) return '<div class="note">No player box score available.</div>';
  return `<div class="boxscore"><table><thead><tr><th>Player</th><th>Team</th><th>E</th><th>D</th><th>A</th><th>Damage</th><th>Heal</th><th>Mitigated</th></tr></thead><tbody>${rows.map(r=>`<tr><td><strong>${r.Player}</strong></td><td>${r.Team}</td><td>${fmt(r.Elim)}</td><td>${fmt(r.Death)}</td><td>${fmt(r.Assists)}</td><td>${fmt(r.Damage)}</td><td>${fmt(r.Heal)}</td><td>${fmt(r.Mitigated)}</td></tr>`).join('')}</tbody></table></div>`;
}

function matchMapBox(m, tData) {
  if (!m || !m.maps) return '';
  const td = tData || getActiveTourneyData();
  const tk = td.tourneyKey || state.tourney;

  return `
    <div class="match-detail">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,0.08);">
        <div>
          <strong style="font-size:16px;color:#fff;">${m.a} vs ${m.b}</strong>
          <span style="font-size:12px;color:var(--text-muted);margin-left:8px;">(${m.phase} ${m.week ? '· Week ' + m.week : ''})</span>
          ${m.mvp ? `<span style="font-size:11px;font-weight:700;color:#fbbf24;margin-left:10px;">⭐ MVP: ${m.mvp}</span>` : ''}
        </div>
        <div style="font-size:18px;font-weight:900;color:#38bdf8;">
          ${m.aw} : ${m.bw}
        </div>
      </div>

      ${m.maps.map(x => {
        const mapTypeStr = mapTypeName(x['MAP TYPE']);
        const timeStr = getMapPlaytime(x);
        const scoreStr = x.DETAIL_SCORE ? ` · ${x.DETAIL_SCORE}` : (x['TEAM 1 SCORE'] != null && x['TEAM 2 SCORE'] != null ? ` · ${x['TEAM 1 SCORE']}:${x['TEAM 2 SCORE']}` : '');
        const subText = timeStr ? `${mapTypeStr} · ${timeStr}${scoreStr}` : `${mapTypeStr}${scoreStr}`;
        const mapImg = getMapImage(x.MAP);
        const isBoxScoreOpen = state.openMap === `${m.key}|${x.MATCH_ID}|${x.MAP}`;

        return `
          <div class="map-block">
            <button class="map-toggle" data-mapkey="${m.key}|${x.MATCH_ID}|${x.MAP}">
              <div class="map-toggle-left">
                <img src="${mapImg}" alt="${x.MAP}" class="map-toggle-thumb" loading="lazy" />
                <span><b>${mapDisplayName(x.MAP)}</b><small>${subText}</small></span>
              </div>
              <strong class="map-winner-tag">WINNER: ${x.WINNER}</strong>
            </button>
            ${isBoxScoreOpen ? playerBoxScore(x.MATCH_ID, x.MAP) : ''}
            <div class="map-bans">
              <span>${x['TEAM 1']}: ${heroIcon(x['TEAM 1 BAN'], 'map-ban-icon')}${x['TEAM 1 BAN'] || '—'}</span>
              <span>${x['TEAM 2']}: ${heroIcon(x['TEAM 2 BAN'], 'map-ban-icon')}${x['TEAM 2 BAN'] || '—'}</span>
            </div>
          </div>
        `;
      }).join('')}

      <div style="margin-top:12px; display:flex; justify-content:flex-end;">
        <button class="btn btn-sm" style="cursor:pointer;" onclick="openMatchDetailModal('${m.key}', '${tk}')">
          🔍 ${state.lang === 'ko' ? '매치 전체 세부 기록 모달 보기' : 'View Full Match Detail Modal'}
        </button>
      </div>
    </div>
  `;
}

function phaseMatchList(phase, tData) {
  const td = tData || getActiveTourneyData();
  const ms = td.matches.filter(m => m.phase === phase);
  const open = state.openPhase === phase;
  const isKo = state.lang === 'ko';
  const countText = isKo ? `총 ${ms.length} 경기` : `${ms.length} matches`;
  const phaseTitle = isKo ? (phase==='2nd RR'?'2차 라운드 로빈 (시드 결정전)':phase==='Playoffs'?'플레이오프':phase==='LCQ'?'LCQ':phase==='Group Stage'?'조별 풀리그':phase) : phase;

  return `
    <div class="phase-accordion">
      <button class="phase-toggle" data-phase-toggle="${phase}">
        <span>${phaseTitle}</span>
        <span>${countText} · ${open ? '−' : '+'}</span>
      </button>
      ${open ? `
        <div class="phase-matches">
          ${ms.map(m => `
            <div class="match-list-item">
              <button class="match-main" data-match-id="${m.key}" data-match="${m.key}" data-tourney="${td.tourneyKey}" title="클릭하여 세부 스코어 및 밴픽 보기">
                <span>
                  <b>${m.a} vs ${m.b}</b>
                  <small>${m.date ? m.date.split(' - ')[0] : (m.week ? 'Week ' + m.week : '')} ${m.mvp ? '· ⭐ ' + m.mvp : ''}</small>
                </span>
                <strong style="color:${m.aw > m.bw ? '#38bdf8' : '#fff'};">${m.aw} : ${m.bw}</strong>
              </button>
              ${state.openMatch === m.key ? matchMapBox(m, td) : ''}
            </div>
          `).join('')}
        </div>
      ` : ''}
    </div>
  `;
}

function banFilterRows(phase, breakMode='Overall', breakValue='All', tData) {
  const td = tData || getActiveTourneyData();
  let rows = phaseRows(phase, td);
  if (breakMode === 'Map Type' && breakValue !== 'All') rows = rows.filter(r => r['MAP TYPE'] === breakValue);
  if (breakMode === 'Map' && breakValue !== 'All') rows = rows.filter(r => r.MAP === breakValue);
  return rows;
}

function banCounts(phase, team, mode, breakMode='Overall', breakValue='All', tData) {
  const td = tData || getActiveTourneyData();
  const rows = banFilterRows(phase, breakMode, breakValue, td);
  const arr = [];
  rows.forEach(r => {
    if (mode === 'by') {
      if (team === 'All' || r['TEAM 1'] === team) arr.push(r['TEAM 1 BAN']);
      if (team === 'All' || r['TEAM 2'] === team) arr.push(r['TEAM 2 BAN']);
    } else if (team !== 'All') {
      if (r['TEAM 1'] === team) arr.push(r['TEAM 2 BAN']);
      if (r['TEAM 2'] === team) arr.push(r['TEAM 1 BAN']);
    }
  });
  const c = {};
  arr.filter(Boolean).forEach(h => { c[h] = (c[h] || 0) + 1; });
  return Object.entries(c).sort((a,b)=>b[1]-a[1]).slice(0, 12);
}

function banBreakdownControls(phase, tData) {
  const td = tData || getActiveTourneyData();
  const mode = state.banBreakMode || 'Overall';
  const rows = phaseRows(phase, td);
  const vals = mode === 'Map Type'
    ? [...new Set(rows.map(r => r['MAP TYPE']).filter(Boolean))].sort()
    : mode === 'Map'
      ? [...new Set(rows.map(r => r.MAP).filter(Boolean))].sort()
      : [];

  return `
    <div class="ban-break-controls">
      <div class="control">
        <label>Ban Breakdown</label>
        <select id="banBreakMode">
          ${['Overall', 'Map Type', 'Map'].map(x => `<option ${x === mode ? 'selected' : ''}>${x}</option>`).join('')}
        </select>
      </div>
      ${mode === 'Overall' ? '' : `
        <div class="control">
          <label>${mode}</label>
          <select id="banBreakValue">
            <option value="All">All</option>
            ${vals.map(x => `<option value="${x}" ${x === state.banBreakValue ? 'selected' : ''}>${mode === 'Map Type' ? mapTypeName(x) : mapDisplayName(x)}</option>`).join('')}
          </select>
        </div>
      `}
    </div>
  `;
}

function banList(arr) {
  const max = arr[0]?.[1] || 1;
  return arr.length ? `
    <div class="ban-list">
      ${arr.map(([h, n]) => `
        <div class="ban-item">
          <span class="ban-hero">
            ${heroIcon(h, "ban-hero-icon")}
            <span>${h}</span>
          </span>
          <div class="mini-bar">
            <span style="width:${Math.min(100, Math.max(10, n / max * 100))}%;"></span>
          </div>
          <b>${n}</b>
        </div>
      `).join('')}
    </div>
  ` : '<div class="note">Select a team to view bans against that team.</div>';
}

function mapTypeStats(phase, tData) {
  const td = tData || getActiveTourneyData();
  const rows = phaseRows(phase, td);
  const teams = td.teams;
  const types = ['Control', 'Hybrid', 'Flashpoint', 'Push', 'Escort'].filter(t => rows.some(r => r['MAP TYPE'] === t));

  return `
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>${state.lang === 'ko' ? '팀' : 'Team'}</th>
            ${types.map(tHead => `<th>${mapTypeName(tHead)}</th>`).join('')}
          </tr>
        </thead>
        <tbody>
          ${teams.map(team => `
            <tr>
              <td><strong>${td.teamNames[team] || team}</strong></td>
              ${types.map(type => {
                const x = rows.filter(r => r['MAP TYPE'] === type && (r['TEAM 1'] === team || r['TEAM 2'] === team));
                const w = x.filter(r => r.WINNER === team).length;
                const isDrillActive = state.mapDrill === `${team}|${type}`;
                return `
                  <td>
                    ${x.length ? `
                      <button class="maptype-drill ${isDrillActive ? 'active-drill' : ''}" data-mapdrill="${team}|${type}">
                        ${w}-${x.length - w} · ${Math.round(w / x.length * 100)}%
                      </button>
                    ` : '—'}
                  </td>
                `;
              }).join('')}
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>
    ${state.mapDrill ? specificMapStats(phase, ...state.mapDrill.split('|'), td) : ''}
  `;
}

function specificMapStats(phase, team, type, tData) {
  const td = tData || getActiveTourneyData();
  const rows = phaseRows(phase, td).filter(r => r['MAP TYPE'] === type && (r['TEAM 1'] === team || r['TEAM 2'] === team));
  const maps = {};

  rows.forEach(r => {
    let x = maps[r.MAP] ??= { w: 0, l: 0, games: [] };
    const isWin = r.WINNER === team;
    if (isWin) x.w++; else x.l++;
    const opp = r['TEAM 1'] === team ? r['TEAM 2'] : r['TEAM 1'];
    x.games.push({ opp, isWin, week: r.WEEK, day: r.DAY, match: r.MATCH, phase: r.PHASE });
  });

  const mapEntries = Object.entries(maps).sort((a,b) => (b[1].w + b[1].l) - (a[1].w + a[1].l));
  if (!mapEntries.length) return '';

  const currentMap = state.selectedMapDetail && maps[state.selectedMapDetail] ? state.selectedMapDetail : mapEntries[0][0];
  const currentData = maps[currentMap];
  const winGames = currentData?.games.filter(g => g.isWin) || [];
  const lossGames = currentData?.games.filter(g => !g.isWin) || [];
  const currentImg = getMapImage(currentMap);

  return `
    <div class="specific-maps">
      <div class="specific-maps-header">
        <h3><b>${td.teamNames[team] || team}</b> · ${mapTypeName(type)} (${t('map_win_rate_type')})</h3>
        <p class="muted">${t('map_detail_hint')}</p>
      </div>

      <div class="map-chip-list">
        ${mapEntries.map(([m, x]) => `
          <button class="map-chip ${m === currentMap ? 'active' : ''}" data-mapdetail="${m}">
            <img src="${getMapImage(m)}" alt="${m}" class="map-chip-photo" loading="lazy" />
            <div class="map-chip-info">
              <span class="map-name">${mapDisplayName(m)}</span>
              <span class="map-rec">${x.w}승 ${x.l}패 (${Math.round(x.w / (x.w + x.l) * 100)}%)</span>
            </div>
          </button>
        `).join('')}
      </div>

      <div class="specific-map-detail card">
        <div class="specific-map-hero">
          <img src="${currentImg}" alt="${currentMap}" class="specific-map-hero-bg" loading="lazy" />
          <div class="specific-map-hero-scrim"></div>
          <div class="specific-map-hero-content">
            <span class="specific-map-mode-pill">${mapTypeName(type)}</span>
            <h4 class="specific-map-title">${mapDisplayName(currentMap)}</h4>
            <div class="specific-map-stat-row">
              <span class="specific-map-record">${currentData.w}승 ${currentData.l}패</span>
              <span class="specific-map-rate">승률 ${Math.round(currentData.w / (currentData.w + currentData.l) * 100)}%</span>
            </div>
          </div>
        </div>

        <div class="specific-map-columns">
          <div class="specific-map-col win">
            <div class="specific-col-title">
              <span class="result-badge win">${t('match_win')}</span>
              <span>${t('map_wins_vs')} (${winGames.length})</span>
            </div>
            ${winGames.length ? `
              <ul class="specific-game-list">
                ${winGames.map(g => `
                  <li class="specific-game-item">
                    <span class="game-opp">vs <b>${td.teamNames[g.opp] || g.opp}</b></span>
                    <span class="game-meta">${g.phase} ${g.week ? 'W' + g.week : ''}</span>
                  </li>
                `).join('')}
              </ul>
            ` : `<p class="muted specific-empty">${t('no_wins_map')}</p>`}
          </div>

          <div class="specific-map-col loss">
            <div class="specific-col-title">
              <span class="result-badge loss">${t('match_loss')}</span>
              <span>${t('map_losses_vs')} (${lossGames.length})</span>
            </div>
            ${lossGames.length ? `
              <ul class="specific-game-list">
                ${lossGames.map(g => `
                  <li class="specific-game-item">
                    <span class="game-opp">vs <b>${td.teamNames[g.opp] || g.opp}</b></span>
                    <span class="game-meta">${g.phase} ${g.week ? 'W' + g.week : ''}</span>
                  </li>
                `).join('')}
              </ul>
            ` : `<p class="muted specific-empty">${t('no_losses_map')}</p>`}
          </div>
        </div>
      </div>
    </div>
  `;
}

function matchesPage() {
  const td = getActiveTourneyData();
  const phase = state.matchPhase || 'All';
  const openMatchObj = td.matches.find(m => m.key === state.openMatch);
  const banTeam = state.banTeam || 'All';

  return `
    <div class="page-title">
      <div>
        <h1>${td.title} ${t('match_title')}</h1>
        <p>${t('match_subtitle')}</p>
      </div>
    </div>

    <!-- 1. Primary Round Robin / Group Matrix -->
    <div class="section round-robin-section">
      <h2>${t('rr_title')} (${td.primaryPhase})</h2>
      <p class="muted">${t('rr_note')}</p>
      ${roundRobinMatrix(td)}
      ${state.openMatch && openMatchObj ? matchMapBox(openMatchObj, td) : ''}
    </div>

    <!-- 2. Phase Analytics Controls & Summary -->
    <div class="controls match-analytics-controls">
      <div class="control">
        <label>${t('analytics_phase')}</label>
        <select id="matchPhase">
          ${td.phases.map(x => `<option ${x === phase ? 'selected' : ''}>${x}</option>`).join('')}
        </select>
      </div>
    </div>
    ${phaseSummary(phase, td)}

    <!-- 3. Later Phases Accordions -->
    ${td.laterPhases.length ? `
      <div class="section">
        <h2>${t('later_phases')}</h2>
        ${td.laterPhases.map(p => phaseMatchList(p, td)).join('')}
      </div>
    ` : ''}

    <!-- 4. Hero Bans Breakdown Panel -->
    <div class="ban-breakdown-panel">
      <h2>${t('hero_bans')}</h2>
      <div class="ban-break-controls">
        <div class="control">
          <label>Team</label>
          <select id="banTeam">
            <option>All</option>
            ${td.teams.map(x => `<option ${x === banTeam ? 'selected' : ''}>${td.teamNames[x] || x}</option>`).join('')}
          </select>
        </div>
      </div>
      ${banBreakdownControls(phase, td)}
    </div>

    <!-- 5. Bans By & Bans Against Cards -->
    <div class="section analytics-grid">
      <div class="card">
        <h2>${t('bans_by')} (${banTeam})</h2>
        ${banList(banCounts(phase, banTeam, 'by', state.banBreakMode, state.banBreakValue, td))}
      </div>
      <div class="card">
        <h2>${t('bans_against')} (${banTeam})</h2>
        ${banList(banCounts(phase, banTeam, 'against', state.banBreakMode, state.banBreakValue, td))}
      </div>
    </div>

    <!-- 6. Map Win Rate by Type Table -->
    <div class="section">
      <h2>${t('map_win_rate_type')}</h2>
      <p class="muted">${t('drill_note')}</p>
      ${mapTypeStats(phase, td)}
    </div>
  `;
}
"""

def main():
    content = APP_JS.read_text(encoding="utf-8")

    # Find where phaseRows starts and matchesPage ends
    pr_idx = content.find("function phaseRows(phase){")
    mp_end = content.find("function stage3PreviewPage(){")
    assert pr_idx != -1 and mp_end != -1, f"Could not find match engine bounds: pr={pr_idx}, mp_end={mp_end}"

    content = content[:pr_idx] + UNIVERSAL_EXPLORER_CODE.strip() + "\n\n" + content[mp_end:]

    # Also make sure render() routes state.page === 'matches' to matchesPage()
    # Replace router logic
    render_start = content.find("function render(){")
    bind_start = content.find("function bind(){")
    assert render_start != -1 and bind_start != -1, "Could not find render/bind bounds"

    new_render = """function render(){
  nav();
  updateStaticHeaderTexts();
  const app = document.getElementById('app');

  if (state.page === 'teams') {
    app.innerHTML = teamsPage();
    bind();
    return;
  }

  if (state.tourney === 'kr-s3') {
    if (state.page === 'overview' || state.page === 'stage3') {
      app.innerHTML = stage3PreviewPage();
    } else {
      app.innerHTML = stageUpcomingPlaceholderPage('kr-s3');
    }
  } else if (state.page === 'matches') {
    app.innerHTML = matchesPage();
  } else if (state.tourney === 'kr-s1') {
    app.innerHTML = stage1PreviewPage();
  } else if (state.tourney === 'kr-s2') {
    if (state.page === 'overview' || state.page === 'stage2') {
      app.innerHTML = stage2PreviewPage();
    } else if (state.page === 'rankings') {
      app.innerHTML = rankingsPage();
    } else if (state.page === 'plotting') {
      app.innerHTML = plottingPage();
    } else if (state.page === 'h2h') {
      app.innerHTML = h2hPage();
    } else {
      app.innerHTML = stage2PreviewPage();
    }
  } else {
    // asia-s1, bootcamp-s1, clash-2026, midseason-2026, owwc-2026
    app.innerHTML = genericTournamentPreviewPage(state.tourney);
  }
  bind();
}"""

    content = content[:render_start] + new_render + "\n\n" + content[bind_start:]

    # Now let's check bind() to make sure all event listeners are present and clean
    bind_end = content.find("// ==========================================\n// Setup Global Header Controls")
    assert bind_end != -1, "Could not find bind_end"

    new_bind = """function bind(){
  const btnS2 = document.getElementById('btnGoStage2') || document.getElementById('btnGoStage2Direct');
  if(btnS2) btnS2.onclick = () => {
    state.tourney = 'kr-s2';
    state.page = 'overview';
    localStorage.setItem('owcs_stat_lab_tourney', 'kr-s2');
    localStorage.setItem('owcs_stat_lab_page', 'overview');
    render();
  };
  const btnGoS1FromS2 = document.getElementById('btnGoStage1FromS2') || document.getElementById('btnGoStage1Direct');
  if(btnGoS1FromS2) btnGoS1FromS2.onclick = () => {
    state.tourney = 'kr-s1';
    state.page = 'overview';
    localStorage.setItem('owcs_stat_lab_tourney', 'kr-s1');
    localStorage.setItem('owcs_stat_lab_page', 'overview');
    render();
  };
  const btnGoS2Stats = document.getElementById('btnGoStage2Stats') || document.getElementById('btnGoS2StatsDirect');
  if(btnGoS2Stats) btnGoS2Stats.onclick = () => {
    state.tourney = 'kr-s2';
    state.page = 'matches';
    localStorage.setItem('owcs_stat_lab_tourney', 'kr-s2');
    localStorage.setItem('owcs_stat_lab_page', 'matches');
    render();
  };
  const btnGoS3 = document.getElementById('btnGoStage3') || document.getElementById('btnGoStage3Direct');
  if(btnGoS3) btnGoS3.onclick = () => {
    state.tourney = 'kr-s3';
    state.page = 'overview';
    localStorage.setItem('owcs_stat_lab_tourney', 'kr-s3');
    localStorage.setItem('owcs_stat_lab_page', 'overview');
    render();
  };
  const btnPlcOverview = document.getElementById('btnGoOverviewFromPlc') || document.getElementById('btnGoOverviewDirect');
  if(btnPlcOverview) btnPlcOverview.onclick = () => {
    state.page = 'overview';
    localStorage.setItem('owcs_stat_lab_page','overview');
    render();
  };

  // Team Page Region Filter & Search Controls
  const trf = document.getElementById('teamRegionFilter');
  if (trf) trf.onchange = () => {
    state.teamRegionFilter = trf.value;
    render();
  };
  document.querySelectorAll('[data-region-chip]').forEach(chip => {
    chip.onclick = () => {
      state.teamRegionFilter = chip.dataset.regionChip;
      render();
    };
  });
  const tSearchInput = document.getElementById('teamSearchInput');
  if (tSearchInput) {
    tSearchInput.oninput = (e) => {
      state.teamSearch = e.target.value;
      const q = (e.target.value || '').toLowerCase().trim();
      document.querySelectorAll('.team-card').forEach(card => {
        const text = card.textContent.toLowerCase();
        card.style.display = (!q || text.includes(q)) ? '' : 'none';
      });
    };
  }

  // Team & Player Profile Navigations
  document.querySelectorAll('.team-card').forEach(x => x.onclick = () => {
    state.team = x.dataset.team;
    state.player = null;
    render();
  });
  document.querySelectorAll('[data-player]').forEach(x => x.onclick = () => {
    state.page = 'teams';
    state.player = x.dataset.player;
    state.team = totals[state.player]?.TEAM || state.team;
    render();
  });
  let b = document.getElementById('backTeams');
  if (b) b.onclick = () => { state.team = null; state.player = null; render(); };
  b = document.getElementById('backTeam');
  if (b) b.onclick = () => { state.player = null; render(); };
  document.querySelectorAll('[data-ptab]').forEach(x => x.onclick = () => { state.profileTab = x.dataset.ptab; render(); });

  // Stage 2 & 1 Overview Sub-tabs
  document.querySelectorAll('[data-s2-tab]').forEach(x => x.onclick = () => {
    state.s2Tab = x.dataset.s2Tab;
    render();
  });
  document.querySelectorAll('[data-s2-week]').forEach(x => x.onclick = () => {
    state.s2Week = x.dataset.s2Week;
    render();
  });
  document.querySelectorAll('[data-s2-team]').forEach(x => x.onclick = () => {
    state.s2TeamFilter = x.dataset.s2Team;
    render();
  });
  document.querySelectorAll('[data-s2-mapphase]').forEach(x => x.onclick = () => {
    state.s2MapPhase = x.dataset.s2Mapphase;
    render();
  });
  document.querySelectorAll('[data-s2-maptype]').forEach(x => x.onclick = () => {
    state.s2MapTypeFilter = x.dataset.s2Maptype;
    render();
  });

  document.querySelectorAll('[data-s1-tab]').forEach(x => x.onclick = () => {
    state.s1Tab = x.dataset.s1Tab;
    render();
  });
  document.querySelectorAll('[data-s1-week]').forEach(x => x.onclick = () => {
    state.s1Week = x.dataset.s1Week;
    render();
  });
  document.querySelectorAll('[data-s1-team]').forEach(x => x.onclick = () => {
    state.s1TeamFilter = x.dataset.s1Team;
    render();
  });
  document.querySelectorAll('[data-s1-maptype]').forEach(x => x.onclick = () => {
    state.s1MapTypeFilter = x.dataset.s1Maptype;
    render();
  });

  document.querySelectorAll('[data-s3-tab]').forEach(x => x.onclick = () => {
    state.s3Tab = x.dataset.s3Tab;
    render();
  });
  document.querySelectorAll('[data-s3-maptype]').forEach(x => x.onclick = () => {
    state.s3MapTypeFilter = x.dataset.s3Maptype;
    render();
  });
  document.querySelectorAll('[data-s3-week]').forEach(x => x.onclick = () => {
    state.s3Week = x.dataset.s3Week;
    render();
  });
  document.querySelectorAll('[data-s3-team]').forEach(x => x.onclick = () => {
    state.s3TeamFilter = x.dataset.s3Team;
    render();
  });

  // Generic Tourney Tabs
  document.querySelectorAll('[data-t-tab]').forEach(x => x.onclick = () => {
    state.tTab = x.dataset.tTab;
    render();
  });
  document.querySelectorAll('[data-t-team]').forEach(x => x.onclick = () => {
    state.tTeam = x.dataset.tTeam;
    render();
  });

  // Rankings & Plotting Controls
  document.querySelectorAll('[data-rank-role]').forEach(x => x.onclick = () => {
    state.rankRole = x.dataset.rankRole;
    state.rankMetric = state.rankMode === 'per10' ? 'Damage / 10' : 'TOTAL DAMAGE';
    state.rankSortDir = 'desc';
    render();
  });
  document.querySelectorAll('[data-rank-mode]').forEach(x => x.onclick = () => {
    state.rankMode = x.dataset.rankMode;
    state.rankMetric = state.rankMode === 'per10' ? 'Damage / 10' : 'TOTAL DAMAGE';
    state.rankSortDir = 'desc';
    render();
  });
  document.querySelectorAll('[data-rank-sort]').forEach(x => x.onclick = () => {
    const k = x.dataset.rankSort;
    if (state.rankMetric === k) {
      state.rankSortDir = state.rankSortDir === 'asc' ? 'desc' : 'asc';
    } else {
      state.rankMetric = k;
      state.rankSortDir = (k === 'Death / 10' || k === 'TOTAL DEATHS') ? 'asc' : 'desc';
    }
    render();
  });

  ['rankRole','rankMode','rankMetric','plotRole','plotX','plotY','plotPhase','plotHighlight','h2hRole','h2hA','h2hB','matchPhase','banTeam','banBreakValue'].forEach(id => {
    let e = document.getElementById(id);
    if(e) e.onchange = () => { state[id] = e.value; render(); };
  });

  let bbm = document.getElementById('banBreakMode');
  if (bbm) bbm.onchange = () => {
    state.banBreakMode = bbm.value;
    state.banBreakValue = 'All';
    render();
  };

  // Plot tooltips
  document.querySelectorAll('[data-plot-player]').forEach(c => {
    c.addEventListener('mousemove', e => {
      const tip = document.getElementById('plotTooltip');
      if (!tip) return;
      const p = c.dataset.plotPlayer;
      const row = aggregatePhase(state.plotRole, state.plotPhase).find(r => r.Player === p);
      if (!row) return;
      tip.hidden = false;
      tip.innerHTML = `<strong>${row.Player}</strong><span>${row.Team} · ${roleName(row.Position)}</span><span>${state.plotX}: <b>${fmt(row[state.plotX])}</b></span><span>${state.plotY}: <b>${fmt(row[state.plotY])}</b></span><span>Playtime: <b>${fmt(row.Playtime_Min)} min</b></span>`;
      const box = c.closest('.plot-wrap').getBoundingClientRect();
      tip.style.left = (e.clientX - box.left + 14) + 'px';
      tip.style.top = (e.clientY - box.top + 14) + 'px';
    });
    c.addEventListener('mouseleave', () => {
      const tip = document.getElementById('plotTooltip');
      if (tip) tip.hidden = true;
    });
  });

  // Match Explorer Interactive Controls
  document.querySelectorAll('[data-match]').forEach(x => {
    x.onclick = (e) => {
      state.openMatch = state.openMatch === x.dataset.match ? null : x.dataset.match;
      render();
    };
  });
  document.querySelectorAll('[data-phase-toggle]').forEach(x => {
    x.onclick = () => {
      state.openPhase = state.openPhase === x.dataset.phaseToggle ? null : x.dataset.phaseToggle;
      render();
    };
  });
  document.querySelectorAll('[data-mapkey]').forEach(x => {
    x.onclick = () => {
      state.openMap = state.openMap === x.dataset.mapkey ? null : x.dataset.mapkey;
      render();
    };
  });
  document.querySelectorAll('[data-mapdrill]').forEach(x => {
    x.onclick = () => {
      state.mapDrill = state.mapDrill === x.dataset.mapdrill ? null : x.dataset.mapdrill;
      state.selectedMapDetail = null;
      render();
    };
  });
  document.querySelectorAll('[data-mapdetail]').forEach(x => {
    x.onclick = () => {
      state.selectedMapDetail = x.dataset.mapdetail;
      render();
    };
  });

  // Radar charts & exports
  if (document.getElementById('profile-radar-canvas') && state.player) {
    renderPlayerRadar('profile-radar-canvas', state.player);
  }
  if (document.getElementById('h2h-radar-canvas') && state.h2hA && state.h2hB) {
    renderH2HRadar('h2h-radar-canvas', state.h2hA, state.h2hB);
  }
  const expP = document.getElementById('btnExportProfile');
  if (expP) expP.onclick = () => { downloadCard('player-profile-export', `${state.player}_owcs_stats.png`); };
  const expH = document.getElementById('btnExportH2H');
  if (expH) expH.onclick = () => { downloadCard('h2h-export-target', `${state.h2hA}_vs_${state.h2hB}_owcs.png`); };

  // Re-bind modal clicks on schedule rows and cards
  bindMatchModalEvents();
}
"""

    content = content[:content.find("function bind(){")] + new_bind + "\n\n" + content[bind_end:]

    APP_JS.write_text(content, encoding="utf-8")
    print("Successfully integrated Universal Tournament Match Explorer into app.js")

if __name__ == "__main__":
    main()
