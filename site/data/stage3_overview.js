// Stage 3 overview metadata in the same shape as OWCS_STAGE2_PREVIEW / OWCS_STAGE2_TRANSFER_EVENTS,
// derived from OWCS_STAGE3_PREVIEW (load stage3_preview.js first).
(function () {
  const p = window.OWCS_STAGE3_PREVIEW;
  if (!p) return;
  const lookup = p.teamLookup || {};
  const s2Teams = (window.OWCS_STAGE2_PREVIEW || {}).teams || [];

  window.OWCS_STAGE3_OVERVIEW = {
    tournament: { ...p.tournament, status: 'In Progress', statusKo: '진행 중' },
    teams: [...(p.teams || []), ...(p.newTeam && !(p.teams || []).some(t => t.short === p.newTeam.short) ? [p.newTeam] : [])]
      // keep each team's Stage 2 color so charts and cards stay consistent across stages
      .map(t => ({ ...t, color: (s2Teams.find(x => x.short === t.short) || lookup[t.short] || {}).color || '#64748b' })),
    mapPool: { regular: p.mapPool },
    // full round-robin schedule; the overview shows the ones without results as upcoming
    fixtures: (p.schedule || []).flatMap(w => w.days.flatMap(d => d.matches.map(m => ({
      week: w.week, day: d.day, a: m.home, b: m.away, dateKo: d.dateKo, dateEn: d.dateEn, time: d.time
    }))))
  };

  // plain name unless the item carries a role or remark to display
  const entry = i => (i.role || i.remarkKo) ? { name: i.name, role: i.role, remarkKo: i.remarkKo, remarkEn: i.remarkEn } : i.name;
  const events = [];
  [['IN', p.transfers?.in], ['OUT', p.transfers?.out]].forEach(([type, groups]) => {
    (groups || []).forEach(g => events.push({
      date: 'STAGE 3', team: g.team, short: g.short, type,
      players: g.items.filter(i => !i.staff).map(entry), staff: g.items.filter(i => i.staff).map(entry),
      noteEn: type === 'IN' ? `Joined ${g.team}` : `Left ${g.team}`,
      noteKo: type === 'IN' ? `${g.team} 합류` : `${g.team}를 떠남`
    }));
  });
  if (p.newTeam) events.push({
    date: 'STAGE 3', team: p.newTeam.name, short: p.newTeam.short, type: 'IN',
    players: p.newTeam.roster.map(r => ({ name: r.name, role: r.role })), staff: [],
    noteEn: 'Stage 3 roster', noteKo: 'Stage 3 참가 로스터'
  });
  window.OWCS_STAGE3_TRANSFER_EVENTS = events;
})();
