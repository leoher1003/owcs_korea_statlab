// Stage 1 Dataset Adapter & Analytics matching Stage 2 Match Explorer Standard

function getStage1Dataset() {
  const raw = (window.OWCS_STAGE1_PREVIEW && window.OWCS_STAGE1_PREVIEW.matches) || [];
  const s1TeamNames = (window.OWCS_STAGE1_PREVIEW && window.OWCS_STAGE1_PREVIEW.teamNames) || {
    CR: "Crazy Raccoon", FLC: "Team Falcons", T1: "T1", ZETA: "ZETA DIVISION",
    ERA: "New Era", OSG: "ONSIDE GAMING", ZAN: "ZAN Esports", CB: "Cheeseburger", PF: "Poker Face"
  };

  const matchInfo = [];
  const matchesAdapted = raw.map(m => {
    const key = m.matchId;
    const a = m.team1;
    const b = m.team2;
    const aw = m.score1;
    const bw = m.score2;
    const phase = m.phase === '2nd RR' ? '2nd RR' : (m.phase === 'Playoffs' ? 'Playoffs' : (m.phase === 'LCQ' ? 'LCQ' : 'Round Robin'));
    const week = m.week || (m.phase === 'Playoffs' ? 6 : 5);
    const day = m.day || 1;

    const setsAdapted = (m.sets || []).map(s => {
      const modeNorm = s.mode ? (s.mode.charAt(0).toUpperCase() + s.mode.slice(1).toLowerCase()) : '';
      const row = {
        WEEK: week,
        DAY: day,
        MATCH: m.matchNumber || 1,
        'Set #': s.setNumber,
        DATE: m.date,
        PHASE: phase,
        'TEAM 1': a,
        'TEAM 2': b,
        MAP: s.map,
        'MAP TYPE': modeNorm,
        WINNER: s.winner,
        'TEAM 1 BAN': s.team1Ban,
        'TEAM 2 BAN': s.team2Ban,
        MATCH_ID: m.matchId,
        DETAIL_SCORE: s.detailScore || `${s.score1} : ${s.score2}`,
        'TEAM 1 SCORE': s.score1,
        'TEAM 2 SCORE': s.score2
      };
      matchInfo.push(row);
      return row;
    });

    return {
      key,
      a,
      b,
      aw,
      bw,
      phase,
      week,
      day,
      winner: m.winner,
      mvp: m.mvp,
      date: m.date,
      casters: m.casters,
      vod: m.vod,
      maps: setsAdapted
    };
  });

  return { matches: matchesAdapted, matchInfo, teamNames: s1TeamNames };
}

function s1PhaseRows(phase) {
  const ds = getStage1Dataset();
  return ds.matchInfo.filter(r => phase === 'All' || r.PHASE === phase);
}

function s1PhaseSummary(phase) {
  const isKo = state.lang === 'ko';
  const rows = s1PhaseRows(phase);
  const ds = getStage1Dataset();
  const ms = ds.matches.filter(m => phase === 'All' || m.phase === phase);
  const mapsCount = rows.length;

  const mc = {};
  rows.forEach(r => { mc[r.MAP] = (mc[r.MAP] || 0) + 1; });
  const mostMap = Object.entries(mc).sort((a, b) => b[1] - a[1])[0];

  const bc = {};
  rows.forEach(r => {
    [r['TEAM 1 BAN'], r['TEAM 2 BAN']].filter(Boolean).forEach(h => {
      bc[h] = (bc[h] || 0) + 1;
    });
  });
  const mostBan = Object.entries(bc).sort((a, b) => b[1] - a[1])[0];

  return `
    <div class="phase-summary">
      <div><b>${ms.length}</b><span>${t('phase_matches')}</span></div>
      <div><b>${mapsCount}</b><span>${t('phase_maps')}</span></div>
      <div><b>${mostMap ? mapDisplayName(mostMap[0]) : '—'}</b><span>${t('most_played_map')}</span></div>
      <div><b>${mostBan ? mostBan[0] : '—'}</b><span>${t('most_banned_hero')}</span></div>
    </div>
  `;
}

function s1RoundRobinMatrix() {
  const ds = getStage1Dataset();
  const rr = ds.matches.filter(m => m.phase === 'Round Robin');
  const teams = ['ZETA', 'CR', 'FLC', 'OSG', 'T1', 'ZAN', 'PF', 'CB', 'ERA'];

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
              <div class="rr-cell ${rw > rl ? 'win' : 'loss'}" data-match="${m.key}" data-tourney="kr-s1" title="클릭하여 세부 정보 보기">
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

function s1PhaseMatchList(phase) {
  const isKo = state.lang === 'ko';
  const ds = getStage1Dataset();
  const ms = ds.matches.filter(m => m.phase === phase);
  const open = state.s1OpenPhase === phase;
  const countText = isKo ? `총 ${ms.length} 경기` : `${ms.length} matches`;
  const phaseTitle = isKo ? (phase === '2nd RR' ? '2차 라운드 로빈 (시드 결정전)' : phase === 'Playoffs' ? '플레이오프' : phase === 'LCQ' ? 'LCQ' : phase) : phase;

  return `
    <div class="phase-accordion">
      <button class="phase-toggle" data-s1-phase-toggle="${phase}">
        <span>${phaseTitle}</span>
        <span>${countText} · ${open ? '−' : '+'}</span>
      </button>
      ${open ? `
        <div class="phase-matches">
          ${ms.map(m => `
            <div class="match-list-item">
              <button class="match-main" data-match="${m.key}" data-tourney="kr-s1">
                <span>
                  <b>${m.a} vs ${m.b}</b>
                  <small>${m.date ? m.date.split(' - ')[0] : ''} ${m.mvp ? '· ⭐ ' + m.mvp : ''}</small>
                </span>
                <strong style="color:${m.aw > m.bw ? '#38bdf8' : '#fff'};">${m.aw} : ${m.bw}</strong>
              </button>
              ${state.openMatch === m.key ? matchMapBox(m) : ''}
            </div>
          `).join('')}
        </div>
      ` : ''}
    </div>
  `;
}

function s1BanBreakdownControls(phase) {
  const mode = state.s1BanBreakMode || 'Overall';
  const rows = s1PhaseRows(phase);
  const vals = mode === 'Map Type'
    ? [...new Set(rows.map(r => r['MAP TYPE']).filter(Boolean))].sort()
    : mode === 'Map'
      ? [...new Set(rows.map(r => r.MAP).filter(Boolean))].sort()
      : [];

  return `
    <div class="ban-break-controls">
      <div class="control">
        <label>Ban Breakdown</label>
        <select id="s1BanBreakMode">
          ${['Overall', 'Map Type', 'Map'].map(x => `<option ${x === mode ? 'selected' : ''}>${x}</option>`).join('')}
        </select>
      </div>
      ${mode === 'Overall' ? '' : `
        <div class="control">
          <label>${mode}</label>
          <select id="s1BanBreakValue">
            <option value="All">All</option>
            ${vals.map(x => `<option value="${x}" ${x === state.s1BanBreakValue ? 'selected' : ''}>${mode === 'Map Type' ? mapTypeName(x) : mapDisplayName(x)}</option>`).join('')}
          </select>
        </div>
      `}
    </div>
  `;
}

function s1BanCounts(phase, team, mode, breakMode = 'Overall', breakValue = 'All') {
  let rows = s1PhaseRows(phase);
  if (breakMode === 'Map Type' && breakValue !== 'All') rows = rows.filter(r => r['MAP TYPE'] === breakValue);
  if (breakMode === 'Map' && breakValue !== 'All') rows = rows.filter(r => r.MAP === breakValue);

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
  return Object.entries(c).sort((a, b) => b[1] - a[1]).slice(0, 12);
}

function s1MapTypeStats(phase) {
  const isKo = state.lang === 'ko';
  const rows = s1PhaseRows(phase);
  const ds = getStage1Dataset();
  const teams = ['ZETA', 'CR', 'FLC', 'OSG', 'T1', 'ZAN', 'PF', 'CB', 'ERA'];
  const types = ['Control', 'Hybrid', 'Flashpoint', 'Push', 'Escort'].filter(t => rows.some(r => r['MAP TYPE'] === t));

  return `
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>${isKo ? '팀' : 'Team'}</th>
            ${types.map(tHead => `<th>${mapTypeName(tHead)}</th>`).join('')}
          </tr>
        </thead>
        <tbody>
          ${teams.map(team => `
            <tr>
              <td><strong>${ds.teamNames[team] || team}</strong></td>
              ${types.map(type => {
                const x = rows.filter(r => r['MAP TYPE'] === type && (r['TEAM 1'] === team || r['TEAM 2'] === team));
                const w = x.filter(r => r.WINNER === team).length;
                const isDrillActive = state.s1MapDrill === `${team}|${type}`;
                return `
                  <td>
                    ${x.length ? `
                      <button class="maptype-drill ${isDrillActive ? 'active-drill' : ''}" data-s1-mapdrill="${team}|${type}">
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
    ${state.s1MapDrill ? s1SpecificMapStats(phase, ...state.s1MapDrill.split('|')) : ''}
  `;
}

function s1SpecificMapStats(phase, team, type) {
  const ds = getStage1Dataset();
  const rows = s1PhaseRows(phase).filter(r => r['MAP TYPE'] === type && (r['TEAM 1'] === team || r['TEAM 2'] === team));
  const maps = {};

  rows.forEach(r => {
    let x = maps[r.MAP] ??= { w: 0, l: 0, games: [] };
    const isWin = r.WINNER === team;
    if (isWin) x.w++; else x.l++;
    const opp = r['TEAM 1'] === team ? r['TEAM 2'] : r['TEAM 1'];
    x.games.push({ opp, isWin, week: r.WEEK, day: r.DAY, match: r.MATCH, phase: r.PHASE, matchId: r.MATCH_ID });
  });

  const mapEntries = Object.entries(maps).sort((a, b) => (b[1].w + b[1].l) - (a[1].w + a[1].l));
  if (!mapEntries.length) return '';

  const currentMap = state.s1SelectedMapDetail && maps[state.s1SelectedMapDetail] ? state.s1SelectedMapDetail : mapEntries[0][0];
  const currentData = maps[currentMap];
  const winGames = currentData?.games.filter(g => g.isWin) || [];
  const lossGames = currentData?.games.filter(g => !g.isWin) || [];
  const currentImg = getMapImage(currentMap);

  return `
    <div class="specific-maps">
      <div class="specific-maps-header">
        <h3><b>${ds.teamNames[team] || team}</b> · ${mapTypeName(type)} (${t('map_win_rate_type')})</h3>
        <p class="muted">${t('map_detail_hint')}</p>
      </div>

      <div class="map-chip-list">
        ${mapEntries.map(([m, x]) => `
          <button class="map-chip ${m === currentMap ? 'active' : ''}" data-s1-mapdetail="${m}">
            <img src="${getMapImage(m)}" alt="${m}" class="map-chip-photo" loading="lazy" />
            <div class="map-chip-info">
              <span class="map-name">${mapDisplayName(m)}</span>
              <span class="map-rec">${x.w}승 ${x.l}패 (${Math.round(x.w / (x.w + x.l) * 100)}%)</span>
            </div>
          </button>
        `).join('')}
      </div>

      <div class="selected-map-banner" style="background-image: linear-gradient(90deg, rgba(17, 21, 29, 0.95) 0%, rgba(17, 21, 29, 0.75) 55%, rgba(17, 21, 29, 0.45) 100%), url('${currentImg}');">
        <div class="selected-map-banner-content">
          <h4 class="selected-map-name">${mapDisplayName(currentMap)}</h4>
          <span class="selected-map-stat">
            ${ds.teamNames[team] || team} 세트 전적: <b>${currentData.w}승 ${currentData.l}패</b> (승률 <b>${Math.round(currentData.w / (currentData.w + currentData.l) * 100)}%</b>)
          </span>
        </div>
      </div>

      <div class="map-history-container">
        <div class="map-history-col win-col">
          <div class="history-title win">${t('map_wins_vs')} (${winGames.length})</div>
          ${winGames.length ? `
            <div class="history-list">
              ${winGames.map(g => {
                const phaseStr = state.lang === 'ko' ? (g.phase === 'Round Robin' ? '정규시즌' : g.phase === '2nd RR' ? '2차 라운드 로빈' : g.phase === 'Playoffs' ? '플레이오프' : g.phase) : g.phase;
                return `
                  <div class="history-item win" data-match-id="${g.matchId}" data-tourney="kr-s1" style="cursor:pointer;" title="클릭하여 세부 정보 보기">
                    <div class="hist-team"><strong>vs ${ds.teamNames[g.opp] || g.opp}</strong></div>
                    <div class="hist-meta">Week ${g.week} (${phaseStr})</div>
                  </div>
                `;
              }).join('')}
            </div>
          ` : `<div class="history-empty">${t('no_wins_map')}</div>`}
        </div>

        <div class="map-history-col loss-col">
          <div class="history-title loss">${t('map_losses_vs')} (${lossGames.length})</div>
          ${lossGames.length ? `
            <div class="history-list">
              ${lossGames.map(g => {
                const phaseStr = state.lang === 'ko' ? (g.phase === 'Round Robin' ? '정규시즌' : g.phase === '2nd RR' ? '2차 라운드 로빈' : g.phase === 'Playoffs' ? '플레이오프' : g.phase) : g.phase;
                return `
                  <div class="history-item loss" data-match-id="${g.matchId}" data-tourney="kr-s1" style="cursor:pointer;" title="클릭하여 세부 정보 보기">
                    <div class="hist-team"><strong>vs ${ds.teamNames[g.opp] || g.opp}</strong></div>
                    <div class="hist-meta">Week ${g.week} (${phaseStr})</div>
                  </div>
                `;
              }).join('')}
            </div>
          ` : `<div class="history-empty">${t('no_losses_map')}</div>`}
        </div>
      </div>
    </div>
  `;
}

// Stage 1 Match Explorer Page - 100% Matching Stage 2 Standard
function stage1MatchesPage() {
  const isKo = state.lang === 'ko';
  const phase = state.s1MatchPhase || 'All';
  const s1Phases = ['All', 'Round Robin', '2nd RR', 'LCQ', 'Playoffs'];
  const ds = getStage1Dataset();
  const banTeam = state.s1BanTeam || 'All';

  return `
    <div class="page-title">
      <div>
        <h1>${isKo ? 'OWCS Korea 2026 Stage 1 경기 탐색기' : 'OWCS Korea 2026 Stage 1 Match Explorer'}</h1>
        <p>${isKo ? '정규 시즌 풀 라운드 로빈 매트릭스, 포스트시즌 경기 결과, 영웅 밴 통계 및 전장 모드별 팀 승률 분석' : 'Regular season matrix, postseason matches, ban statistics, and map win rate analytics'}</p>
      </div>
    </div>

    <!-- 1. Round Robin Matrix -->
    <div class="section round-robin-section">
      <h2>${t('rr_title')}</h2>
      <p class="muted">${t('rr_note')}</p>
      ${s1RoundRobinMatrix()}
      ${state.openMatch ? matchMapBox(ds.matches.find(m => m.key === state.openMatch)) : ''}
    </div>

    <!-- 2. Phase Analytics Controls & Summary -->
    <div class="controls match-analytics-controls">
      <div class="control">
        <label>${t('analytics_phase')}</label>
        <select id="s1MatchPhase">
          ${s1Phases.map(x => `<option value="${x}" ${x === phase ? 'selected' : ''}>${x === '2nd RR' && isKo ? '2차 라운드 로빈 (시드 결정전)' : x === 'Playoffs' && isKo ? '플레이오프' : x}</option>`).join('')}
        </select>
      </div>
    </div>
    ${s1PhaseSummary(phase)}

    <!-- 3. Later Phases (2nd RR, LCQ, Playoffs) -->
    <div class="section">
      <h2>${t('later_phases')}</h2>
      ${['2nd RR', 'LCQ', 'Playoffs'].map(s1PhaseMatchList).join('')}
    </div>

    <!-- 4. Hero Bans Breakdown Panel -->
    <div class="ban-breakdown-panel">
      <h2>${t('hero_bans')}</h2>
      <div class="ban-break-controls">
        <div class="control">
          <label>Team</label>
          <select id="s1BanTeam">
            <option value="All">All</option>
            ${Object.keys(ds.teamNames).map(x => `<option value="${x}" ${x === banTeam ? 'selected' : ''}>${ds.teamNames[x] || x}</option>`).join('')}
          </select>
        </div>
      </div>
      ${s1BanBreakdownControls(phase)}
    </div>

    <div class="section analytics-grid">
      <div class="card">
        <h2>${t('bans_by')} (${banTeam})</h2>
        ${banList(s1BanCounts(phase, banTeam, 'by', state.s1BanBreakMode, state.s1BanBreakValue))}
      </div>
      <div class="card">
        <h2>${t('bans_against')} (${banTeam})</h2>
        ${banList(s1BanCounts(phase, banTeam, 'against', state.s1BanBreakMode, state.s1BanBreakValue))}
      </div>
    </div>

    <!-- 5. Map Win Rates by Type & Specific Maps -->
    <div class="section">
      <h2>${t('map_win_rate_type')}</h2>
      <p class="muted">${t('drill_note')}</p>
      ${s1MapTypeStats(phase)}
    </div>
  `;
}
