// Stage 1 Overview Page - Exactly Matching Stage 2 Layout & Design
function stage1PreviewPage(){
  const s1 = window.OWCS_STAGE1_PREVIEW || {};
  const tour = s1.tournament || {};
  const isKo = state.lang === 'ko';
  const curTab = state.s1Tab || 'schedule';
  const curWeek = state.s1Week || 'all';
  const curTeam = state.s1TeamFilter || 'ALL';
  const curMapType = state.s1MapTypeFilter || 'ALL';
  const tourName = isKo ? (tour.nameKo || tour.name) : tour.name;

  // Sub-tabs
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

  // 1. Regular Season Standings Data (36 Matches Round Robin)
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

  const standingsRowsHtml = s1Standings.map(s => {
    const isTop4 = s.rank <= 4;
    const isLcq = s.rank >= 5 && s.rank <= 8;
    const tierClass = isTop4 ? 'tier-rr2' : (isLcq ? 'tier-lcq' : 'tier-elim');

    return `
      <tr class="s2-standing-row ${tierClass}" data-s1-team="${s.team}" title="${s.name} (${s.team})">
        <td class="col-rank" style="text-align:center;">
          <span class="rank-num ${s.statusClass}">${s.rank}</span>
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
          <b class="s2-diff-tag ${s.diff.startsWith('+') ? 'pos' : 'neg'}">${s.diff}</b>
        </td>
        <td class="col-status" style="text-align:center;">
          <span class="s2-outcome-badge ${s.statusClass}">${s.status}</span>
        </td>
      </tr>
    `;
  }).join('');

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
        <div class="s2-standings-legend">
          <span class="s2-legend-item green">
            <span class="s2-legend-dot green"></span>
            <b>1~4위:</b> Advanced to 2nd RR
          </span>
          <span class="s2-legend-item yellow">
            <span class="s2-legend-dot yellow"></span>
            <b>5~8위:</b> Advanced to LCQ
          </span>
          <span class="s2-legend-item red">
            <span class="s2-legend-dot red"></span>
            <b>9위:</b> Eliminated
          </span>
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

  // 2. Schedule Data & Rendering (Identical to Stage 2 Grouping Structure)
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

  // Group filtered matches exactly like Stage 2 (Week block -> Days grid -> Day card)
  const matchGroups = [];
  filteredMatches.forEach(m => {
    let groupKey = m.phase === 'Round Robin' ? `Week ${m.week}` : m.phase;
    let groupTitleKo = m.phase === 'Round Robin' ? `정규 시즌 ${m.week}주차` : (m.phase === '2nd RR' ? '2차 라운드 로빈 (시드 결정전)' : (m.phase === 'Playoffs' ? '플레이오프' : m.phase));
    let groupTitleEn = m.phase === 'Round Robin' ? `Regular Season Week ${m.week}` : (m.phase === '2nd RR' ? '2nd Round Robin' : (m.phase === 'Playoffs' ? 'Playoffs' : m.phase));

    let grp = matchGroups.find(g => g.key === groupKey);
    if (!grp) {
      grp = { key: groupKey, titleKo: groupTitleKo, titleEn: groupTitleEn, days: [] };
      matchGroups.push(grp);
    }

    let dayKey = `Day ${m.day || 1}`;
    let dayObj = grp.days.find(d => d.key === dayKey);
    if (!dayObj) {
      dayObj = { key: dayKey, dayNum: m.day || 1, matches: [] };
      grp.days.push(dayObj);
    }
    dayObj.matches.push(m);
  });

  const scheduleHtml = matchGroups.length ? matchGroups.map(grp => {
    const grpTitle = isKo ? grp.titleKo : grp.titleEn;
    const daysHtml = grp.days.map(d => {
      const matchesCardsHtml = d.matches.map(m => {
        const homeWon = m.winner === m.team1;
        const awayWon = m.winner === m.team2;
        const homeName = teamNamesLookup[m.team1] || m.team1;
        const awayName = teamNamesLookup[m.team2] || m.team2;
        const isMatchTarget = curTeam === 'ALL' || m.team1 === curTeam || m.team2 === curTeam;
        const isDimmed = !isMatchTarget;
        const phaseLabel = m.phase === 'Round Robin' ? `W${m.week} M${m.matchNumber || ''}` : m.phase;

        return `
          <div class="s3-match-row s2-match-row s1-match-row ${homeWon || awayWon ? 'completed' : ''} ${isDimmed ? 'dimmed' : ''}" data-match-id="${m.matchId}" data-tourney="kr-s1" title="${isKo ? '클릭하여 세부 스코어 및 밴픽 보기' : 'Click to view detail scores and bans'}">
            <div class="s3-match-meta">
              <span class="s3-match-num">${phaseLabel}</span>
              <span class="s2-result-tag">FINAL</span>
              <span class="s1-match-hint">🔍 ${isKo ? '세부 정보' : 'Details'}</span>
            </div>

            <div class="s2-match-body">
              <div class="s2-match-team home ${homeWon ? 'winner-team' : ''}" title="${homeName}">
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

              <div class="s2-match-team away ${awayWon ? 'winner-team' : ''}" title="${awayName}">
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

      return `
        <div class="s3-day-card">
          <div class="s3-day-head">
            <div class="s3-day-title-wrap">
              <span class="s3-day-badge">${d.key}</span>
            </div>
            <span class="s3-day-time">${d.matches.length}${isKo ? '경기' : ' Matches'}</span>
          </div>
          <div class="s3-matches-container">
            ${matchesCardsHtml}
          </div>
        </div>
      `;
    }).join('');

    return `
      <div class="s3-week-block">
        <div class="s3-week-header">
          <div style="display:flex;align-items:center;gap:12px;">
            <span class="s3-week-indicator"></span>
            <h3 class="s3-week-title">${grpTitle}</h3>
          </div>
          <span class="s3-week-matchcount">${grp.days.reduce((acc, cur) => acc + cur.matches.length, 0)}${isKo ? '경기' : ' Matches'}</span>
        </div>
        <div class="s3-days-grid">
          ${daysHtml}
        </div>
      </div>
    `;
  }).join('') : `<div class="empty-state" style="padding:40px 20px;text-align:center;color:var(--text-muted);">${isKo ? '해당 조건의 경기 결과가 없습니다.' : 'No matches found.'}</div>`;

  // 3. Map Pool Data & Rendering (Identical to Stage 2 Map Pool Structure)
  const rawPool = s1.mapPool || {};
  const mapTypeOrder = ['Control', 'Hybrid', 'Flashpoint', 'Push', 'Escort'];

  const mapFilterOptions = [
    { key: 'ALL', ko: '전체 전장 모드', en: 'All Game Modes' },
    { key: 'Control', ko: '🎯 쟁탈 (Control)', en: '🎯 Control' },
    { key: 'Hybrid', ko: '⚔️ 혼합 (Hybrid)', en: '⚔️ Hybrid' },
    { key: 'Flashpoint', ko: '⚡ 플래시포인트', en: '⚡ Flashpoint' },
    { key: 'Push', ko: '🤖 밀기 (Push)', en: '🤖 Push' },
    { key: 'Escort', ko: '🚛 호위 (Escort)', en: '🚛 Escort' }
  ];

  const mapFilterChipsHtml = mapFilterOptions.map(opt => {
    let count = 0;
    if (opt.key === 'ALL') {
      count = Object.values(rawPool).reduce((acc, p) => acc + (p.maps ? p.maps.length : 0), 0);
    } else if (rawPool[opt.key]) {
      count = rawPool[opt.key].maps ? rawPool[opt.key].maps.length : 0;
    }
    const isAct = curMapType === opt.key;
    return `
      <button class="chip s3-filter-chip ${isAct ? 'active' : ''}" data-s1-maptype="${opt.key}">
        <span>${isKo ? opt.ko : opt.en}</span>
        <span class="s3-chip-count">${count}</span>
      </button>
    `;
  }).join('');

  const typesToRender = curMapType === 'ALL'
    ? mapTypeOrder.filter(k => rawPool[k])
    : [curMapType].filter(k => rawPool[k]);

  const mapPoolBlocksHtml = typesToRender.map(typeKey => {
    const pool = rawPool[typeKey];
    if (!pool) return '';

    const mapsCardsHtml = (pool.maps || []).map(m => {
      const mapImg = getMapImage(m.nameEn || m.nameKo);
      return `
        <div class="s3-map-card ${pool.type.toLowerCase()}">
          <div class="s3-map-card-img-wrap">
            <img src="${mapImg}" alt="${m.nameKo}" class="s3-map-card-img" loading="lazy" />
            <div class="s3-map-card-overlay"></div>
            <span class="s3-map-mode-badge" style="background:${pool.color}dd; color:#fff; border:1px solid ${pool.color};">
              ${pool.icon} ${isKo ? pool.nameKo : pool.nameEn}
            </span>
          </div>
          <div class="s3-map-card-body">
            <h4 class="s3-map-name">${isKo ? m.nameKo : m.nameEn} <span class="s3-map-en">(${isKo ? m.nameEn : m.nameKo})</span></h4>
          </div>
        </div>
      `;
    }).join('');

    return `
      <div class="s3-map-type-group" style="--mode-col:${pool.color};">
        <div class="s3-map-type-header">
          <div style="display:flex;align-items:center;gap:10px;">
            <span class="s3-map-type-dot" style="background:${pool.color};box-shadow:0 0 10px ${pool.color};"></span>
            <h3 class="s3-map-type-title" style="color:${pool.color};">${pool.icon} ${isKo ? pool.nameKo : pool.nameEn}</h3>
            <span class="s3-map-count-badge">${(pool.maps || []).length}${isKo ? '개 전장' : ' Maps'}</span>
          </div>
        </div>
        <div class="s3-maps-grid">
          ${mapsCardsHtml}
        </div>
      </div>
    `;
  }).join('');

  const mapPoolSectionHtml = `
    <div class="s3-mappool-section" id="s1-mappool">
      <div class="page-title" style="margin-bottom:14px;">
        <div>
          <h2>${isKo ? '공식 전장 맵 풀 (Stage 1 Map Pool)' : 'Stage 1 Official Map Pool'}</h2>
          <p class="muted" style="margin:4px 0 0;">${isKo ? '2026 시즌 개막전 정규 시즌 및 플레이오프 공식 채택 전장 모드' : 'Official competitive map pool for Stage 1 Regular Season & Postseason'}</p>
        </div>
      </div>

      <div class="s3-map-filters-bar">
        ${mapFilterChipsHtml}
      </div>

      <div class="s3-mappool-container">
        ${mapPoolBlocksHtml}
      </div>
    </div>
  `;

  // 4. Teams Data & Rendering (Identical to Stage 2 Team Cards)
  const teamsHtml = (s1.teams || []).map(tm => {
    const isZeta = tm.short === 'ZETA';
    const rankBadge = tm.seed ? `
      <span class="stage3-seed-badge" style="${isZeta ? 'background:linear-gradient(135deg, rgba(251,191,36,0.18) 0%, rgba(217,119,6,0.28) 100%);color:#fbbf24;border:1px solid rgba(251,191,36,0.5);font-weight:800;' : ''}">
        ${isZeta ? '🏆 ' : ''}${isKo ? tm.seedKo : tm.seed}
      </span>
    ` : '';

    const rosterItems = (tm.roster || []).map(p => `
      <div class="stage3-roster-item">
        <span style="display:inline-flex;align-items:center;">
          <b style="color:var(--text);">${p.name}</b>
        </span>
        <span class="stage3-role-tag ${(p.role || '').toLowerCase()}">${p.role}</span>
      </div>
    `).join('');

    return `
      <div class="stage3-team-card">
        <div class="stage3-team-head">
          <div style="display:flex;align-items:center;gap:10px;">
            ${teamLogo(tm.short, 'team-logo')}
            <div>
              <strong style="font-size:15px;display:block;">${tm.name}</strong>
              <span class="muted" style="font-size:12px;">${tm.short}</span>
            </div>
          </div>
          ${rankBadge}
        </div>
        <div class="stage3-roster-list">
          ${rosterItems}
        </div>
      </div>
    `;
  }).join('');

  const showSchedule = curTab === 'schedule' || curTab === 'all';
  const showStandings = curTab === 'standings' || curTab === 'schedule' || curTab === 'all';
  const showMapPool = curTab === 'mappool' || curTab === 'all';
  const showTeams = curTab === 'teams' || curTab === 'all';

  return `
    <div class="stage3-hero">
      <div class="stage3-hero-top">
        <div class="stage3-brand-row">
          <img src="assets/owcs_korea_dark.png" alt="OWCS Korea" class="stage3-official-logo" />
          <span class="stage3-tier-badge">
            <span class="stage3-tier-icon">💎</span>
            <b>${isKo ? 'A-TIER 대회' : 'A-TIER'}</b>
          </span>
          <span class="stage3-dday-badge" style="background:linear-gradient(135deg, #10b981 0%, #059669 100%);color:#fff;box-shadow:0 2px 10px rgba(16,185,129,0.35);">
            ✓ ${isKo ? '대회 종료 (우승: ZETA DIVISION)' : 'Completed (Champion: ZETA)'}
          </span>
        </div>
        <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
          <button class="chip" id="btnGoStage2Direct">⚡ ${isKo ? 'Stage 2 통계 랩 가기' : 'Go to Stage 2 Stats'}</button>
          <button class="chip" id="btnGoStage3Direct">🚀 ${isKo ? 'Stage 3 프리뷰' : 'Stage 3 Preview'}</button>
        </div>
      </div>
      <h1 class="stage3-title">${tourName}</h1>
      <div class="stage3-meta-pills" style="margin-top:12px;">
        <span class="stage3-pill tier">💎 <b>${isKo ? 'A-TIER 대회' : 'A-TIER Tournament'}</b></span>
        <span class="stage3-pill prize">💰 <b>${isKo ? '총 상금 $38,500' : 'Total Prize $38,500'}</b></span>
        <span class="stage3-pill" style="background:rgba(251,191,36,0.15);color:#fbbf24;border:1px solid rgba(251,191,36,0.35);">
          🏆 <b>${isKo ? '우승: ZETA DIVISION' : 'Champion: ZETA DIVISION'}</b>
        </span>
      </div>
    </div>

    <!-- Stage 1 Navigation Sub-tabs -->
    <div class="s3-main-nav-bar">
      ${s1NavTabsHtml}
    </div>

    ${showStandings ? standingsSectionHtml : ''}

    ${showSchedule ? `
      <!-- Schedule Section -->
      <div class="s3-schedule-section">
        <div class="s3-schedule-topbar">
          <div>
            <div style="display:flex;align-items:center;gap:8px;">
              <span class="s3-schedule-live-dot" style="background:#10b981;box-shadow:0 0 10px #10b981;"></span>
              <h2 class="s3-schedule-heading">${isKo ? 'Stage 1 전체 경기 일정 & 최종 결과' : 'Stage 1 Match Schedule & Final Results'}</h2>
            </div>
            <p class="muted" style="margin:4px 0 0;font-size:13px;">
              ${isKo ? '정규 시즌 36경기 풀 라운드 로빈 및 2차 RR · LCQ · 플레이오프 전 경기 최종 스코어 (클릭 시 세부 점수 및 밴픽 모달)' : 'Full Round Robin (36 matches), 2nd Round Robin, LCQ and Playoffs official scores'}
            </p>
          </div>
          <div class="s3-broadcast-box">
            <span class="s3-broadcast-label">🔴 ${isKo ? '공식 중계 다시보기' : 'Official Streams'}</span>
            <div class="s3-broadcast-links">
              <a href="https://www.sooplive.com/station/owesports" target="_blank" rel="noopener noreferrer" class="s3-stream-badge soop" title="${isKo ? 'SOOP 한국어 공식 중계 바로가기' : 'Watch on SOOP'}">
                <span class="s3-stream-dot"></span>
                <b>SOOP</b>
                <span class="s3-stream-tag">KR</span>
                <span class="s3-ext-arrow">↗</span>
              </a>
              <a href="https://www.twitch.tv/ow_esports/" target="_blank" rel="noopener noreferrer" class="s3-stream-badge twitch" title="${isKo ? 'Twitch 글로벌 공식 중계 바로가기' : 'Watch on Twitch'}">
                <span class="s3-stream-dot twitch-dot"></span>
                <b>Twitch</b>
                <span class="s3-stream-tag">Global</span>
                <span class="s3-ext-arrow">↗</span>
              </a>
            </div>
          </div>
        </div>

        <div class="s3-schedule-controls">
          <div class="s3-week-tabs">
            ${weekTabsHtml}
          </div>
          <div class="s3-team-filters">
            <span class="s3-filter-label">${isKo ? '팀별 경기 필터:' : 'Filter by Team:'}</span>
            <div class="s3-team-chips-wrap">
              ${teamFilterChipsHtml}
            </div>
          </div>
        </div>

        <div class="s3-weeks-container">
          ${scheduleHtml}
        </div>
      </div>
    ` : ''}

    ${showMapPool ? mapPoolSectionHtml : ''}

    ${showTeams ? `
      <div class="section" style="margin-bottom:24px;">
        <div class="page-title" style="margin-bottom:12px;">
          <div>
            <h2>${isKo ? 'Stage 1 참가 9개 팀 공식 로스터' : 'Official 9-team Stage 1 Rosters'}</h2>
            <p class="muted" style="margin:4px 0 0;">${isKo ? '2026 시즌 개막전 정규 시즌 참가 구단 공식 명단' : 'Official verified rosters for Stage 1'} (ZETA DIVISION 🏆 우승)</p>
          </div>
        </div>
        <div class="stage3-teams-grid">
          ${teamsHtml}
        </div>
      </div>
    ` : ''}

    <div class="stage3-notice-card" style="border-left-color:#38bdf8;">
      <span class="stage3-notice-icon">📢</span>
      <div>
        <strong style="color:#38bdf8;display:block;margin-bottom:2px;">${isKo ? 'Stage 1 경기 기록 안내' : 'Stage 1 Match Records Notice'}</strong>
        <span>${isKo ? '각 경기 카드를 클릭하시면 세트별 세부 점수(쟁탈 라운드, 밀기 실제 미터, 화물 도달 점수 등), 양 팀 밴 영웅 및 매치 MVP(POTM) 상세 내역을 확인하실 수 있습니다.' : 'Click on any match card to open the detailed match modal with set scores, hero bans, and MVP awards.'}</span>
      </div>
    </div>
  `;
}
