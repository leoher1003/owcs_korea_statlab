// Helper to get game mode icons & names
function getModeIcon(mode) {
  if (!mode) return '🎮';
  const m = mode.toLowerCase();
  if (m.includes('control')) return '🎯';
  if (m.includes('hybrid')) return '⚔️';
  if (m.includes('flashpoint')) return '⚡';
  if (m.includes('push')) return '🤖';
  if (m.includes('escort')) return '🚛';
  return '🎮';
}

function getModeName(mode, isKo) {
  if (!mode) return '';
  const m = mode.toLowerCase();
  if (m.includes('control')) return isKo ? '쟁탈' : 'Control';
  if (m.includes('hybrid')) return isKo ? '혼합' : 'Hybrid';
  if (m.includes('flashpoint')) return isKo ? '플포' : 'Flashpoint';
  if (m.includes('push')) return isKo ? '밀기' : 'Push';
  if (m.includes('escort')) return isKo ? '호위' : 'Escort';
  return mode;
}

// Find Match object across Stage 1 or Stage 2
function findMatchObject(keyOrId, tourney) {
  if (tourney === 'kr-s1') {
    const s1List = (window.OWCS_STAGE1_PREVIEW && window.OWCS_STAGE1_PREVIEW.matches) || [];
    return s1List.find(m => m.matchId === keyOrId || `${m.phase}_${m.matchNumber}` === keyOrId);
  }
  
  // kr-s2: check window.OWCS_STAGE2_MATCHES
  const s2Lq = window.OWCS_STAGE2_MATCHES || [];
  let found = s2Lq.find(m => m.matchId === keyOrId);
  if (found) return found;

  // match key from groupMatches: e.g. "1-1-1-Round Robin"
  const mParts = String(keyOrId).split('-');
  if (mParts.length >= 4) {
    const week = parseInt(mParts[0]);
    const day = parseInt(mParts[1]);
    const matchNum = parseInt(mParts[2]);
    const phase = mParts[3];
    found = s2Lq.find(m => m.phase === phase && m.week === week && m.matchNumber === matchNum);
    if (found) return found;
  }

  // fallback to local matches array
  const localM = (typeof matches !== 'undefined' ? matches : []).find(m => m.key === keyOrId);
  if (localM) {
    return {
      phase: localM.phase,
      week: localM.week,
      team1: localM.a,
      team2: localM.b,
      score1: localM.aw,
      score2: localM.bw,
      winner: localM.winner,
      mvp: '',
      date: '',
      casters: [],
      sets: (localM.maps || []).map((x, idx) => ({
        setNumber: idx + 1,
        map: x.MAP,
        mode: x['MAP TYPE'],
        detailScore: x.DETAIL_SCORE || (x['TEAM 1 SCORE'] ? `${x['TEAM 1 SCORE']} : ${x['TEAM 2 SCORE']}` : ''),
        winner: x.WINNER,
        team1Ban: x['TEAM 1 BAN'] || '',
        team2Ban: x['TEAM 2 BAN'] || '',
        banStart: x['INITIAL BAN RIGHT'] === 'TEAM 1' ? '1' : (x['INITIAL BAN RIGHT'] === 'TEAM 2' ? '2' : '')
      }))
    };
  }
  return null;
}

// Open Match Detail Modal
function openMatchDetailModal(keyOrId, tourney) {
  const match = findMatchObject(keyOrId, tourney);
  if (!match) return;

  const isKo = state.lang === 'ko';
  const tourName = tourney === 'kr-s1' 
    ? (isKo ? 'OWCS 코리아 2026 Stage 1' : 'OWCS Korea 2026 Stage 1')
    : (isKo ? 'OWCS 코리아 2026 Stage 2' : 'OWCS Korea 2026 Stage 2');

  const t1 = match.team1 || match.a;
  const t2 = match.team2 || match.b;
  const s1 = match.score1 !== undefined ? match.score1 : match.aw;
  const s2 = match.score2 !== undefined ? match.score2 : match.bw;
  const winner = match.winner;
  const isT1Win = winner === t1;
  const isT2Win = winner === t2;
  const mvp = match.mvp || '';
  const dateStr = match.date || '';
  const castersStr = match.casters && match.casters.length ? match.casters.join(', ') : '';
  const vodUrl = match.vod || '';
  const phaseStr = match.phase === 'Round Robin' 
    ? (isKo ? `정규 시즌 ${match.week ? match.week + '주차' : ''}` : `Regular Season ${match.week ? 'Week ' + match.week : ''}`)
    : (match.phase === '2nd RR' ? (isKo ? '2차 라운드 로빈 (시드 결정전)' : 'Playoffs Seeding Decider') : match.phase);

  // Compute H2H within tournament
  const allTourneyMatches = tourney === 'kr-s1'
    ? ((window.OWCS_STAGE1_PREVIEW && window.OWCS_STAGE1_PREVIEW.matches) || [])
    : (window.OWCS_STAGE2_MATCHES || []);

  const h2hMatches = allTourneyMatches.filter(m => {
    const mt1 = m.team1 || m.a;
    const mt2 = m.team2 || m.b;
    return (mt1 === t1 && mt2 === t2) || (mt1 === t2 && mt2 === t1);
  });

  let t1H2hWins = 0, t2H2hWins = 0;
  h2hMatches.forEach(m => {
    if (m.winner === t1) t1H2hWins++;
    else if (m.winner === t2) t2H2hWins++;
  });

  const t1Name = teamNames[t1] || (window.OWCS_STAGE1_PREVIEW?.teamNames?.[t1]) || t1;
  const t2Name = teamNames[t2] || (window.OWCS_STAGE1_PREVIEW?.teamNames?.[t2]) || t2;

  // Build sets rows
  const sets = match.sets || [];
  const setsRowsHtml = sets.map(s => {
    const setWin = s.winner;
    const modeIcon = getModeIcon(s.mode);
    const modeName = getModeName(s.mode, isKo);
    const scoreText = s.detailScore || (s.score1 ? `${s.score1} : ${s.score2}` : '-');

    return `
      <tr class="match-modal-set-row">
        <td style="width:55px;text-align:center;">
          <span class="set-num-badge">Set ${s.setNumber}</span>
        </td>
        <td>
          <div class="set-map-cell">
            <span class="set-mode-icon">${modeIcon}</span>
            <div>
              <div class="set-map-name">${mapDisplayName(s.map)}</div>
              <span class="set-mode-tag">${modeName}</span>
            </div>
          </div>
        </td>
        <td style="text-align:center;">
          <span class="set-score-pill">${scoreText}</span>
        </td>
        <td style="text-align:center;">
          <span class="set-winner-tag">${setWin ? setWin + (isKo ? ' 승' : ' Win') : '-'}</span>
        </td>
        <td>
          <div class="set-bans-wrap">
            <span class="ban-chip team1" title="${t1} Ban">🚫 ${t1}: <b>${s.team1Ban || '-'}</b></span>
            <span class="ban-chip team2" title="${t2} Ban">🚫 ${t2}: <b>${s.team2Ban || '-'}</b></span>
          </div>
        </td>
      </tr>
    `;
  }).join('');

  // Remove existing modal if any
  const existing = document.getElementById('matchDetailModalBackdrop');
  if (existing) existing.remove();

  const modalHtml = `
    <div class="match-modal-backdrop" id="matchDetailModalBackdrop">
      <div class="match-modal-card" id="matchDetailModalCard" role="dialog" aria-modal="true">
        <!-- Header -->
        <div class="match-modal-header">
          <div class="match-modal-meta-left">
            <span class="match-modal-stage-badge">${tourName} · ${phaseStr}</span>
            ${dateStr ? `<span class="match-modal-date">📅 ${dateStr}</span>` : ''}
            ${castersStr ? `<span class="match-modal-date">🎙️ ${castersStr}</span>` : ''}
          </div>
          <button class="match-modal-close-btn" id="btnMatchModalClose" title="${isKo ? '닫기' : 'Close'}">✕</button>
        </div>

        <!-- Hero Match Banner -->
        <div class="match-modal-hero-banner">
          <div class="match-modal-teams-row">
            <div class="match-modal-team home">
              <div class="match-modal-team-text">
                <span class="team-abbr" style="color:${isT1Win ? '#38bdf8' : '#fff'};">${t1}</span>
                <span class="team-name">${t1Name}</span>
              </div>
              ${teamLogo(t1, 'match-modal-team-logo')}
            </div>

            <div class="match-modal-score-wrap">
              <div class="match-modal-score-box">
                <span class="score-digit ${isT1Win ? 'winner-score' : ''}">${s1}</span>
                <span class="score-colon">:</span>
                <span class="score-digit ${isT2Win ? 'winner-score' : ''}">${s2}</span>
              </div>
            </div>

            <div class="match-modal-team away">
              ${teamLogo(t2, 'match-modal-team-logo')}
              <div class="match-modal-team-text">
                <span class="team-abbr" style="color:${isT2Win ? '#38bdf8' : '#fff'};">${t2}</span>
                <span class="team-name">${t2Name}</span>
              </div>
            </div>
          </div>

          <div class="match-modal-badges-row">
            ${mvp ? `<div class="match-modal-mvp-badge">⭐ Match MVP (POTM): <b>${mvp}</b></div>` : ''}
            ${vodUrl ? `<a href="${vodUrl}" target="_blank" rel="noopener noreferrer" class="match-modal-vod-btn">▶ ${isKo ? 'VOD 다시보기' : 'Watch VOD'}</a>` : ''}
          </div>
        </div>

        <!-- Content Body -->
        <div class="match-modal-content">
          <!-- H2H Summary -->
          <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07); border-radius:12px; padding:12px 18px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px;">
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="font-size:16px;">⚔️</span>
              <strong style="font-size:13px; color:#e2e8f0;">${isKo ? '대회 내 상대전적 (Head-to-Head)' : 'Tournament Head-to-Head'}</strong>
            </div>
            <div style="font-size:13px; font-weight:700; color:#38bdf8;">
              ${t1} ${t1H2hWins}W - ${t2H2hWins}W ${t2}
              <span style="font-size:11px; color:#94a3b8; font-weight:500; margin-left:6px;">(${h2hMatches.length}${isKo ? '경기 치름' : ' matches played'})</span>
            </div>
          </div>

          <!-- Set Scores & Bans Table -->
          <div>
            <div class="match-modal-section-title">
              <span>🎯</span>
              <span>${isKo ? '세트별 세부 스코어 및 밴픽' : 'Set-by-Set Scoreboard & Hero Bans'}</span>
            </div>
            <div style="overflow-x:auto;">
              <table class="match-modal-sets-table">
                <thead>
                  <tr style="font-size:11.5px; color:#94a3b8; text-transform:uppercase; letter-spacing:0.04em;">
                    <th style="padding:4px 14px; text-align:center;">Set</th>
                    <th style="padding:4px 14px; text-align:left;">Map / Mode</th>
                    <th style="padding:4px 14px; text-align:center;">Score</th>
                    <th style="padding:4px 14px; text-align:center;">Winner</th>
                    <th style="padding:4px 14px; text-align:left;">Hero Bans</th>
                  </tr>
                </thead>
                <tbody>
                  ${setsRowsHtml}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', modalHtml);

  // Close handlers
  const backdrop = document.getElementById('matchDetailModalBackdrop');
  const closeBtn = document.getElementById('btnMatchModalClose');
  const closeModal = () => {
    if (backdrop) backdrop.remove();
    document.removeEventListener('keydown', handleEsc);
  };
  const handleEsc = (e) => {
    if (e.key === 'Escape') closeModal();
  };

  if (closeBtn) closeBtn.onclick = closeModal;
  if (backdrop) {
    backdrop.onclick = (e) => {
      if (e.target === backdrop) closeModal();
    };
  }
  document.addEventListener('keydown', handleEsc);
}

// Bind clicks on match rows
function bindMatchModalEvents() {
  document.querySelectorAll('.s2-match-row, .s1-match-row').forEach(row => {
    row.onclick = () => {
      const matchId = row.dataset.matchId || row.dataset.matchKey;
      const tourney = row.dataset.tourney || (state.tourney || 'kr-s2');
      if (matchId) {
        openMatchDetailModal(matchId, tourney);
      }
    };
  });
}
