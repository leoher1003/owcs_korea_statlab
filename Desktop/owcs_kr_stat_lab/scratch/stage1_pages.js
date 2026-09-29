// Stage 1 Overview Page
function stage1PreviewPage() {
  const s1 = window.OWCS_STAGE1_PREVIEW || {};
  const tour = s1.tournament || {};
  const isKo = state.lang === 'ko';
  const curTab = state.s1Tab || 'schedule';
  const curWeek = state.s1Week || 'all';
  const curTeam = state.s1TeamFilter || 'ALL';
  const tourName = isKo ? (tour.nameKo || tour.name) : tour.name;

  const s1NavTabs = [
    { id: 'schedule', icon: '📅', ko: '경기 일정', en: 'Schedule' },
    { id: 'standings', icon: '🏆', ko: '정규 순위표', en: 'Standings' },
    { id: 'mappool', icon: '🗺️', ko: '공식 맵 풀', en: 'Map Pool' },
    { id: 'teams', icon: '👥', ko: '참가팀 로스터', en: 'Teams' },
    { id: 'all', icon: '📑', ko: '전체 보기', en: 'View All' }
  ];

  const s1NavTabsHtml = s1NavTabs.map(t => `
    <button class="tabbtn s3-nav-tab ${curTab === t.id ? 'active' : ''}" data-s1-tab="${t.id}">
      <span>${t.icon}</span>
      <b>${isKo ? t.ko : t.en}</b>
    </button>
  `).join('');

  // 1. Standings Data
  const s1Standings = [
    { rank: 1, team: 'ZETA', name: 'ZETA DIVISION', mw: 8, ml: 0, mapw: 24, mapl: 6, diff: '+18', winrate: '100%', status: 'Advanced to 2nd RR', statusClass: 'status-green' },
    { rank: 2, team: 'CR', name: 'Crazy Raccoon', mw: 6, ml: 2, mapw: 21, mapl: 9, diff: '+12', winrate: '75%', status: 'Advanced to 2nd RR', statusClass: 'status-green' },
    { rank: 3, team: 'FLC', name: 'Team Falcons', mw: 6, ml: 2, mapw: 20, mapl: 9, diff: '+11', winrate: '75%', status: 'Advanced to 2nd RR', statusClass: 'status-green' },
    { rank: 4, team: 'OSG', name: 'ONSIDE GAMING', mw: 5, ml: 3, mapw: 21, mapl: 13, diff: '+8', winrate: '63%', status: 'Advanced to 2nd RR', statusClass: 'status-green' },
    { rank: 5, team: 'T1', name: 'T1', mw: 5, ml: 3, mapw: 19, mapl: 11, diff: '+8', winrate: '63%', status: 'Advanced to LCQ', statusClass: 'status-yellow' },
    { rank: 6, team: 'ZAN', name: 'ZAN Esports', mw: 3, ml: 5, mapw: 12, mapl: 15, diff: '-3', winrate: '38%', status: 'Advanced to LCQ', statusClass: 'status-yellow' },
    { rank: 7, team: 'PF', name: 'Poker Face', mw: 2, ml: 6, mapw: 6, mapl: 18, diff: '-12', winrate: '25%', status: 'Advanced to LCQ', statusClass: 'status-yellow' },
    { rank: 8, team: 'CB', name: 'Cheeseburger', mw: 1, ml: 7, mapw: 3, mapl: 21, diff: '-18', winrate: '13%', status: 'Advanced to LCQ', statusClass: 'status-yellow' },
    { rank: 9, team: 'ERA', name: 'New Era', mw: 0, ml: 8, mapw: 0, mapl: 24, diff: '-24', winrate: '0%', status: 'Eliminated', statusClass: 'status-red' }
  ];

  const standingsRowsHtml = s1Standings.map(s => `
    <tr class="s2-standing-row ${s.rank <= 4 ? 'tier-rr2' : s.rank <= 8 ? 'tier-lcq' : 'tier-elim'}">
      <td style="text-align:center;"><span class="rank-num ${s.statusClass}">${s.rank}</span></td>
      <td>
        <div class="team-cell">
          ${teamLogo(s.team, 's2-standing-team-logo')}
          <div class="team-names">
            <strong class="team-abbr">${s.team}</strong>
            <span class="team-full">${s.name}</span>
          </div>
        </div>
      </td>
      <td style="text-align:center;"><b style="color:#fff;">${s.mw}W - ${s.ml}L</b></td>
      <td style="text-align:center;"><span class="s2-winrate-tag">${s.winrate}</span></td>
      <td style="text-align:center;"><span>${s.mapw}W - ${s.mapl}L</span></td>
      <td style="text-align:center;"><b class="s2-diff-tag ${s.diff.startsWith('+') ? 'pos' : 'neg'}">${s.diff}</b></td>
      <td style="text-align:center;"><span class="s2-outcome-badge ${s.statusClass}">${s.status}</span></td>
    </tr>
  `).join('');

  const standingsSectionHtml = `
    <div class="s2-standings-card" id="s1-standings">
      <div class="s2-standings-header">
        <div style="display:flex;align-items:center;gap:12px;">
          <span class="s2-standings-icon">🏆</span>
          <div>
            <h3 class="s2-standings-title" style="margin:0;font-size:16.5px;font-weight:800;color:#fff;">
              ${isKo ? 'Stage 1 정규 시즌 최종 순위표' : 'Stage 1 Regular Season Final Standings'}
            </h3>
            <p class="s2-standings-sub muted" style="margin:3px 0 0;font-size:12px;">
              ${isKo ? '총 36경기 풀 라운드 로빈 결과 · 1~4위 2차 RR / 5~8위 LCQ 진출' : '36 Regular Season Matches · Top 4 to 2nd RR, 5-8th to LCQ'}
            </p>
          </div>
        </div>
      </div>
      <div class="s2-standings-table-wrap">
        <table class="s2-standings-table">
          <thead>
            <tr>
              <th style="width:50px;text-align:center;">#</th>
              <th>${isKo ? '팀' : 'Team'}</th>
              <th style="text-align:center;width:110px;">${isKo ? '매치 성적' : 'Series (W-L)'}</th>
              <th style="text-align:center;width:80px;">${isKo ? '승률' : 'Win %'}</th>
              <th style="text-align:center;width:110px;">${isKo ? '세트 성적' : 'Maps (W-L)'}</th>
              <th style="text-align:center;width:80px;">${isKo ? '세트 득실' : 'Map Diff'}</th>
              <th style="text-align:center;width:200px;">${isKo ? '진출 / 결과' : 'Status / Outcome'}</th>
            </tr>
          </thead>
          <tbody>
            ${standingsRowsHtml}
          </tbody>
        </table>
      </div>
    </div>
  `;

  // 2. Schedule Data
  const allS1Matches = s1.matches || [];
  const s1TeamsList = ['ALL', 'ZETA', 'FLC', 'CR', 'T1', 'OSG', 'ZAN', 'PF', 'CB', 'ERA'];
  const teamNamesLookup = s1.teamNames || {};

  const teamFilterChipsHtml = s1TeamsList.map(tm => {
    const isAct = curTeam === tm;
    const label = tm === 'ALL' ? (isKo ? '전체 팀' : 'All Teams') : (teamNamesLookup[tm] || tm);
    return `<button class="chip s3-filter-chip ${isAct ? 'active' : ''}" data-s1-team="${tm}">
      ${tm !== 'ALL' ? teamLogo(tm, 's3-chip-logo') : ''}
      <span>${label}</span>
    </button>`;
  }).join('');

  const weekTabs = [
    { id: 'all', ko: `전체 경기 (${allS1Matches.length})`, en: `All Matches (${allS1Matches.length})` },
    { id: '1', ko: '정규 1주차', en: 'Regular Week 1' },
    { id: '2', ko: '정규 2주차', en: 'Regular Week 2' },
    { id: '3', ko: '정규 3주차', en: 'Regular Week 3' },
    { id: '4', ko: '정규 4주차', en: 'Regular Week 4' },
    { id: '2nd RR', ko: '2차 라운드 로빈', en: '2nd Round Robin' },
    { id: 'LCQ', ko: 'LCQ', en: 'LCQ' },
    { id: 'Playoffs', ko: '플레이오프', en: 'Playoffs' }
  ];

  const weekTabsHtml = weekTabs.map(w => `
    <button class="tabbtn s3-week-tab ${curWeek === w.id ? 'active' : ''}" data-s1-week="${w.id}">
      ${isKo ? w.ko : w.en}
    </button>
  `).join('');

  // Filter matches
  const filteredMatches = allS1Matches.filter(m => {
    const matchWeek = (curWeek === 'all')
      ? true
      : (curWeek === '1' || curWeek === '2' || curWeek === '3' || curWeek === '4')
        ? (m.phase === 'Round Robin' && String(m.week) === curWeek)
        : (m.phase === curWeek);
    const matchTeam = (curTeam === 'ALL') || (m.team1 === curTeam || m.team2 === curTeam);
    return matchWeek && matchTeam;
  });

  // Render match cards
  const matchCardsHtml = filteredMatches.map(m => {
    const homeWon = m.winner === m.team1;
    const awayWon = m.winner === m.team2;
    const homeName = teamNamesLookup[m.team1] || m.team1;
    const awayName = teamNamesLookup[m.team2] || m.team2;
    const phaseLabel = m.phase === 'Round Robin' ? `W${m.week} M${m.matchNumber || ''}` : m.phase;

    return `
      <div class="s1-match-row s3-match-row completed" data-match-id="${m.matchId}" data-tourney="kr-s1" title="${isKo ? '클릭하여 세부 스코어 및 밴픽 보기' : 'Click to view detail scores and bans'}">
        <div class="s3-match-meta">
          <span class="s3-match-num">${phaseLabel}</span>
          <span class="s2-result-tag">FINAL</span>
          <span class="s1-match-hint">🔍 ${isKo ? '세부 정보' : 'Details'}</span>
        </div>
        
        <div class="s2-match-body">
          <div class="s2-match-team home ${homeWon ? 'winner-team' : ''}">
            <div class="s3-team-text">
              <strong class="s3-team-abbr">${m.team1}</strong>
              <span class="s3-team-fullname">${homeName}</span>
            </div>
            ${teamLogo(m.team1, 's3-match-logo')}
          </div>

          <div class="s2-match-score-badge">
            <span class="s2-score ${homeWon ? 'win' : ''}">${m.score1}</span>
            <span class="s2-score-divider">:</span>
            <span class="s2-score ${awayWon ? 'win' : ''}">${m.score2}</span>
          </div>

          <div class="s2-match-team away ${awayWon ? 'winner-team' : ''}">
            ${teamLogo(m.team2, 's3-match-logo')}
            <div class="s3-team-text">
              <strong class="s3-team-abbr">${m.team2}</strong>
              <span class="s3-team-fullname">${awayName}</span>
            </div>
          </div>
        </div>

        ${m.mvp ? `
          <div style="padding: 6px 14px; background:rgba(245,158,11,0.08); border-top:1px solid rgba(255,255,255,0.04); font-size:11px; color:#fbbf24; font-weight:700; display:flex; align-items:center; gap:6px;">
            <span>⭐ POTM: <b>${m.mvp}</b></span>
          </div>
        ` : ''}

        ${(m.sets && m.sets.length) ? `
          <div class="s2-match-maps-footer">
            ${m.sets.map((x, idx) => `
              <span class="s2-map-set-tag ${x.winner === m.winner ? 'winner' : ''}">
                <b>S${idx + 1}</b> ${mapDisplayName(x.map)} <small>(${x.winner})</small>
              </span>
            `).join('')}
          </div>
        ` : ''}
      </div>
    `;
  }).join('');

  const scheduleSectionHtml = `
    <div class="s3-schedule-wrap" id="s1-schedule">
      <div class="s3-filters-bar">
        <div class="s3-filters-title">
          <span>🎯</span>
          <b>${isKo ? '주차별 / 단계별 선택' : 'Filter by Phase / Week'}</b>
        </div>
        <div class="s3-week-tabs-row">
          ${weekTabsHtml}
        </div>
        <div class="s3-team-chips-row">
          ${teamFilterChipsHtml}
        </div>
      </div>

      <div class="s3-matches-container" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(320px, 1fr)); gap:14px; margin-top:20px;">
        ${matchCardsHtml.length ? matchCardsHtml : `<div class="empty-state" style="padding:40px; text-align:center; color:var(--text-muted);">${isKo ? '해당 조건의 경기 결과가 없습니다.' : 'No matches found.'}</div>`}
      </div>
    </div>
  `;

  // 3. Map Pool Data
  const mapPool = s1.mapPool || {};
  const mapPoolHtml = Object.keys(mapPool).map(typeKey => {
    const mp = mapPool[typeKey];
    const mapsListHtml = mp.maps.map(m => `
      <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:10px 14px; display:flex; align-items:center; justify-content:space-between;">
        <strong style="color:#fff; font-size:13.5px;">${isKo ? m.nameKo : m.nameEn}</strong>
        <span style="font-size:11.5px; color:#94a3b8;">${m.nameEn}</span>
      </div>
    `).join('');

    return `
      <div style="background:rgba(18,22,31,0.6); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:18px;">
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
          <span style="font-size:18px;">${mp.icon}</span>
          <h4 style="margin:0; font-size:15px; color:#fff;">${isKo ? mp.nameKo : mp.nameEn}</h4>
          <span style="font-size:11px; padding:2px 6px; border-radius:4px; background:rgba(255,255,255,0.08); color:#94a3b8;">${mp.maps.length} Maps</span>
        </div>
        <div style="display:flex; flex-direction:column; gap:8px;">
          ${mapsListHtml}
        </div>
      </div>
    `;
  }).join('');

  // 4. Rosters
  const teamsList = s1.teams || [];
  const rostersHtml = teamsList.map(tm => {
    const rosterItemsHtml = (tm.roster || []).map(p => `
      <div style="display:flex; align-items:center; justify-content:space-between; padding:6px 10px; background:rgba(255,255,255,0.03); border-radius:6px; font-size:12.5px;">
        <span style="font-weight:700; color:#fff;">${p.name}</span>
        <span style="font-size:10.5px; font-weight:800; color:${p.role === 'TANK' ? '#38bdf8' : p.role === 'DPS' ? '#f43f5e' : '#10b981'};">${p.role}</span>
      </div>
    `).join('');

    return `
      <div style="background:rgba(18,22,31,0.6); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:18px;">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
          ${teamLogo(tm.short, 's3-chip-logo')}
          <div>
            <h4 style="margin:0; font-size:15px; color:#fff;">${tm.name} (${tm.short})</h4>
            <span style="font-size:11px; color:#fbbf24; font-weight:700;">${isKo ? tm.seedKo : tm.seed}</span>
          </div>
        </div>
        <div style="display:flex; flex-direction:column; gap:6px;">
          ${rosterItemsHtml}
        </div>
      </div>
    `;
  }).join('');

  return `
    <div class="s3-overview-page">
      <!-- Tournament Hero -->
      <div class="s3-hero-banner" style="background:linear-gradient(135deg, rgba(245,158,11,0.12), rgba(16,185,129,0.06)); border:1px solid rgba(245,158,11,0.25);">
        <div class="s3-hero-content">
          <div class="s3-hero-tag" style="background:rgba(245,158,11,0.2); color:#fbbf24; border:1px solid rgba(245,158,11,0.4);">
            🏆 ${isKo ? '우승: ZETA DIVISION' : 'Champion: ZETA DIVISION'}
          </div>
          <h1 class="s3-hero-title">${tourName}</h1>
          <p class="s3-hero-desc">
            ${isKo 
              ? '2026 시즌 개막전 · 총 9개 팀 출전 · 51경기 풀 데이터셋 (정규시즌, 2차 라운드로빈, LCQ, 플레이오프)' 
              : '2026 Season Kickoff · 9 Teams · 51 Full Matches (Regular Season, Seeding Decider, LCQ, Regional Playoffs)'}
          </p>
          <div class="s3-hero-meta-row">
            <span>📅 2026.03.20 - 05.03</span>
            <span>📍 ${tour.venue}</span>
            <span>💰 ${tour.prizePool}</span>
            <span>🎖️ ${tour.tier}</span>
          </div>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <div class="s3-main-nav-bar">
        ${s1NavTabsHtml}
      </div>

      <!-- Tab Content Area -->
      ${curTab === 'schedule' ? scheduleSectionHtml : ''}
      ${curTab === 'standings' ? standingsSectionHtml : ''}
      ${curTab === 'mappool' ? `<div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:16px;">${mapPoolHtml}</div>` : ''}
      ${curTab === 'teams' ? `<div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:16px;">${rostersHtml}</div>` : ''}
      ${curTab === 'all' ? `
        <div style="display:flex; flex-direction:column; gap:32px;">
          ${standingsSectionHtml}
          ${scheduleSectionHtml}
          <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:16px;">${mapPoolHtml}</div>
          <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:16px;">${rostersHtml}</div>
        </div>
      ` : ''}
    </div>
  `;
}

// Stage 1 Matches Page (Match Explorer)
function stage1MatchesPage() {
  const isKo = state.lang === 'ko';
  const s1 = window.OWCS_STAGE1_PREVIEW || {};
  const allMatches = s1.matches || [];
  const curWeek = state.s1Week || 'all';
  const curTeam = state.s1TeamFilter || 'ALL';
  const teamNamesLookup = s1.teamNames || {};

  const weekTabs = [
    { id: 'all', ko: `전체 경기 (${allMatches.length})`, en: `All Matches (${allMatches.length})` },
    { id: '1', ko: '정규 1주차', en: 'Regular Week 1' },
    { id: '2', ko: '정규 2주차', en: 'Regular Week 2' },
    { id: '3', ko: '정규 3주차', en: 'Regular Week 3' },
    { id: '4', ko: '정규 4주차', en: 'Regular Week 4' },
    { id: '2nd RR', ko: '2차 라운드 로빈', en: '2nd Round Robin' },
    { id: 'LCQ', ko: 'LCQ', en: 'LCQ' },
    { id: 'Playoffs', ko: '플레이오프', en: 'Playoffs' }
  ];

  const weekTabsHtml = weekTabs.map(w => `
    <button class="tabbtn s3-week-tab ${curWeek === w.id ? 'active' : ''}" data-s1-week="${w.id}">
      ${isKo ? w.ko : w.en}
    </button>
  `).join('');

  const teamsList = ['ALL', 'ZETA', 'FLC', 'CR', 'T1', 'OSG', 'ZAN', 'PF', 'CB', 'ERA'];
  const teamChipsHtml = teamsList.map(tm => `
    <button class="chip s3-filter-chip ${curTeam === tm ? 'active' : ''}" data-s1-team="${tm}">
      ${tm !== 'ALL' ? teamLogo(tm, 's3-chip-logo') : ''}
      <span>${tm === 'ALL' ? (isKo ? '전체 팀' : 'All Teams') : (teamNamesLookup[tm] || tm)}</span>
    </button>
  `).join('');

  const filtered = allMatches.filter(m => {
    const matchWeek = (curWeek === 'all')
      ? true
      : (curWeek === '1' || curWeek === '2' || curWeek === '3' || curWeek === '4')
        ? (m.phase === 'Round Robin' && String(m.week) === curWeek)
        : (m.phase === curWeek);
    const matchTeam = (curTeam === 'ALL') || (m.team1 === curTeam || m.team2 === curTeam);
    return matchWeek && matchTeam;
  });

  const cardsHtml = filtered.map(m => {
    const homeWon = m.winner === m.team1;
    const awayWon = m.winner === m.team2;
    const homeName = teamNamesLookup[m.team1] || m.team1;
    const awayName = teamNamesLookup[m.team2] || m.team2;
    const phaseLabel = m.phase === 'Round Robin' ? `Week ${m.week}` : m.phase;

    return `
      <div class="s1-match-row s3-match-row completed" data-match-id="${m.matchId}" data-tourney="kr-s1">
        <div class="s3-match-meta">
          <span class="s3-match-num">${phaseLabel}</span>
          <span class="s2-result-tag">FINAL</span>
          <span class="s1-match-hint">🔍 ${isKo ? '세부 정보' : 'Details'}</span>
        </div>

        <div class="s2-match-body">
          <div class="s2-match-team home ${homeWon ? 'winner-team' : ''}">
            <div class="s3-team-text">
              <strong class="s3-team-abbr">${m.team1}</strong>
              <span class="s3-team-fullname">${homeName}</span>
            </div>
            ${teamLogo(m.team1, 's3-match-logo')}
          </div>

          <div class="s2-match-score-badge">
            <span class="s2-score ${homeWon ? 'win' : ''}">${m.score1}</span>
            <span class="s2-score-divider">:</span>
            <span class="s2-score ${awayWon ? 'win' : ''}">${m.score2}</span>
          </div>

          <div class="s2-match-team away ${awayWon ? 'winner-team' : ''}">
            ${teamLogo(m.team2, 's3-match-logo')}
            <div class="s3-team-text">
              <strong class="s3-team-abbr">${m.team2}</strong>
              <span class="s3-team-fullname">${awayName}</span>
            </div>
          </div>
        </div>

        ${m.mvp ? `
          <div style="padding: 6px 14px; background:rgba(245,158,11,0.08); border-top:1px solid rgba(255,255,255,0.04); font-size:11px; color:#fbbf24; font-weight:700;">
            ⭐ POTM: <b>${m.mvp}</b>
          </div>
        ` : ''}

        ${(m.sets && m.sets.length) ? `
          <div class="s2-match-maps-footer">
            ${m.sets.map((x, idx) => `
              <span class="s2-map-set-tag ${x.winner === m.winner ? 'winner' : ''}">
                <b>S${idx + 1}</b> ${mapDisplayName(x.map)} <small>(${x.winner})</small>
              </span>
            `).join('')}
          </div>
        ` : ''}
      </div>
    `;
  }).join('');

  return `
    <div class="page-container" style="padding-top:20px;">
      <div style="margin-bottom:20px;">
        <h2 style="margin:0 0 6px; font-size:22px; font-weight:900; color:#fff;">
          ⚡ ${isKo ? 'Stage 1 경기 탐색기 (Match Explorer)' : 'Stage 1 Match Explorer'}
        </h2>
        <p style="margin:0; font-size:13px; color:#94a3b8;">
          ${isKo ? '정규시즌부터 시드결정전, LCQ, 플레이오프까지 51경기 전체 세부 기록과 밴픽, MVP를 확인하세요. 경기를 클릭하면 세트별 세부 점수와 밴픽 모달이 열립니다.' : 'Explore all 51 matches of Stage 1. Click any match card to view detailed set-by-set scores and hero bans.'}
        </p>
      </div>

      <div class="s3-filters-bar" style="margin-bottom:24px;">
        <div class="s3-week-tabs-row">
          ${weekTabsHtml}
        </div>
        <div class="s3-team-chips-row">
          ${teamChipsHtml}
        </div>
      </div>

      <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(320px, 1fr)); gap:16px;">
        ${cardsHtml.length ? cardsHtml : `<div class="empty-state" style="padding:40px; text-align:center; color:var(--text-muted);">${isKo ? '해당 조건의 경기 결과가 없습니다.' : 'No matches found.'}</div>`}
      </div>
    </div>
  `;
}
