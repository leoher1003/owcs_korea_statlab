const D=window.OWCS_DATA;
const L=window.OWCS_LIQUIPEDIA||{players:{},teams:{}};
const state={
  tourney:localStorage.getItem('owcs_stat_lab_tourney')||'kr-s2',
  page:localStorage.getItem('owcs_stat_lab_page')||'overview',
  team:null,
  player:null,
  profileTab:'percentile',
  rankRole:'MAIN DPS',
  rankMode:'per10',
  rankMetric:'Damage / 10',
  rankSortDir:'desc',
  plotRole:'MAIN DPS',
  plotX:'Damage / 10',
  plotY:'Elim / 10',
  plotPhase:'All',
  plotHighlight:'All',
  h2hRole:'MAIN DPS',
  h2hA:'PROPER',
  h2hB:'LIP',
  matchPhase:'All',
  banTeam:'All',
  banBreakMode:'Overall',
  banBreakValue:'All',
  openMatch:null,
  openPhase:null,
  openMap:null,
  mapDrill:null,
  selectedMapDetail:null,
  lang:localStorage.getItem('owcs_stat_lab_lang')||'ko',
  s3Week:'all',
  s3TeamFilter:'ALL',
  s3Tab:'schedule',
  s3MapTypeFilter:'ALL',
  s2Tab:'schedule',
  s2Week:'all',
  s2TeamFilter:'ALL',
  s2MapPhase:'regular',
  s2MapTypeFilter:'ALL',
  s1Tab:'schedule',
  s1Week:'all',
  s1TeamFilter:'ALL',
  s1MapTypeFilter:'ALL',
  s1MatchPhase:'All',
  s1BanTeam:'All',
  s1BanBreakMode:'Overall',
  s1BanBreakValue:'All',
  s1OpenPhase:null,
  s1MapDrill:null,
  s1SelectedMapDetail:null
};

const MAP_TYPE_NAMES = {
  ko: {
    Control: '쟁탈',
    Hybrid: '혼합',
    Flashpoint: '플래시포인트',
    Push: '밀기',
    Escort: '호위'
  },
  en: {
    Control: 'Control',
    Hybrid: 'Hybrid',
    Flashpoint: 'Flashpoint',
    Push: 'Push',
    Escort: 'Escort'
  }
};

function mapTypeName(t){
  return MAP_TYPE_NAMES[state.lang]?.[t] || MAP_TYPE_NAMES['ko']?.[t] || t;
}

const MAP_IMAGES = {
  'aatlis': 'assets/maps/aatlis.jpg',
  '아틀리스': 'assets/maps/aatlis.jpg',
  'antarctic peninsula': 'assets/maps/antarctic_peninsula.jpg',
  '남극 반도': 'assets/maps/antarctic_peninsula.jpg',
  'blizzard world': 'assets/maps/blizzard_world.jpg',
  '블리자드 월드': 'assets/maps/blizzard_world.jpg',
  'busan': 'assets/maps/busan.jpg',
  '부산': 'assets/maps/busan.jpg',
  'circuit royal': 'assets/maps/circuit_royal.jpg',
  '서킷 로얄': 'assets/maps/circuit_royal.jpg',
  'colosseo': 'assets/maps/colosseo.jpg',
  '콜로세오': 'assets/maps/colosseo.jpg',
  'dorado': 'assets/maps/dorado.jpg',
  '도라도': 'assets/maps/dorado.jpg',
  'eichenwalde': 'assets/maps/eichenwalde.jpg',
  '아이헨발데': 'assets/maps/eichenwalde.jpg',
  'esperança': 'assets/maps/esperanca.jpg',
  'esperanca': 'assets/maps/esperanca.jpg',
  '이스페란사': 'assets/maps/esperanca.jpg',
  'havana': 'assets/maps/havana.jpg',
  '하바나': 'assets/maps/havana.jpg',
  'hollywood': 'assets/maps/hollywood.jpg',
  '할리우드': 'assets/maps/hollywood.jpg',
  'ilios': 'assets/maps/ilios.jpg',
  '일리오스': 'assets/maps/ilios.jpg',
  'junkertown': 'assets/maps/junkertown.jpg',
  '쓰레기촌': 'assets/maps/junkertown.jpg',
  "king's row": 'assets/maps/king_s_row.jpg',
  'kings row': 'assets/maps/king_s_row.jpg',
  '왕의 길': 'assets/maps/king_s_row.jpg',
  'lijiang tower': 'assets/maps/lijiang_tower.jpg',
  '리장 타워': 'assets/maps/lijiang_tower.jpg',
  'midtown': 'assets/maps/midtown.jpg',
  '미드타운': 'assets/maps/midtown.jpg',
  'neon junction': 'assets/maps/neon_junction.jpg',
  'neonjunction': 'assets/maps/neon_junction.jpg',
  '네온 교차로': 'assets/maps/neon_junction.jpg',
  'nepal': 'assets/maps/nepal.jpg',
  '네팔': 'assets/maps/nepal.jpg',
  'new junk city': 'assets/maps/new_junk_city.jpg',
  'newjunkcity': 'assets/maps/new_junk_city.jpg',
  '뉴 정크 시티': 'assets/maps/new_junk_city.jpg',
  'new queen street': 'assets/maps/new_queen_street.jpg',
  'newqueenstreet': 'assets/maps/new_queen_street.jpg',
  '뉴 퀸 스트리트': 'assets/maps/new_queen_street.jpg',
  'numbani': 'assets/maps/numbani.jpg',
  '눔바니': 'assets/maps/numbani.jpg',
  'oasis': 'assets/maps/oasis.jpg',
  '오아시스': 'assets/maps/oasis.jpg',
  'paraíso': 'assets/maps/paraiso.jpg',
  'paraiso': 'assets/maps/paraiso.jpg',
  '파라이수': 'assets/maps/paraiso.jpg',
  'rialto': 'assets/maps/rialto.jpg',
  '리알토': 'assets/maps/rialto.jpg',
  'route 66': 'assets/maps/route_66.jpg',
  'route66': 'assets/maps/route_66.jpg',
  '66번 국도': 'assets/maps/route_66.jpg',
  'runasapi': 'assets/maps/runasapi.jpg',
  '루나사피': 'assets/maps/runasapi.jpg',
  'samoa': 'assets/maps/samoa.jpg',
  '사모아': 'assets/maps/samoa.jpg',
  'shambali monastery': 'assets/maps/shambali_monastery.jpg',
  'shambalimonastery': 'assets/maps/shambali_monastery.jpg',
  '샴발리 수도원': 'assets/maps/shambali_monastery.jpg',
  'suravasa': 'assets/maps/suravasa.jpg',
  '수라바사': 'assets/maps/suravasa.jpg',
  'watchpoint: gibraltar': 'assets/maps/watchpoint_gibraltar.jpg',
  'watchpoint gibraltar': 'assets/maps/watchpoint_gibraltar.jpg',
  '감시기지: 지브롤터': 'assets/maps/watchpoint_gibraltar.jpg'
};

function getMapImage(mapName){
  if(!mapName) return 'assets/maps/busan.jpg';
  const clean = String(mapName).trim().toLowerCase().replace(/['"`]/g, '');
  return MAP_IMAGES[clean] || MAP_IMAGES[String(mapName).trim().toLowerCase()] || 'assets/maps/busan.jpg';
}

const MAP_NAMES_KO = {
  // Control (쟁탈)
  'antarctic peninsula': '남극 반도',
  'antartic peninsula': '남극 반도',
  'busan': '부산',
  'ilios': '일리오스',
  'lijiang tower': '리장 타워',
  'nepal': '네팔',
  'oasis': '오아시스',
  'samoa': '사모아',

  // Hybrid (혼합)
  'blizzard world': '블리자드 월드',
  'eichenwalde': '아이헨발데',
  'hollywood': '할리우드',
  "king's row": '왕의 길',
  'kings row': '왕의 길',
  'midtown': '미드타운',
  'neon junction': '네온 교차로',
  'neonjunction': '네온 교차로',
  'numbani': '눔바니',
  'paraiso': '파라이수',
  'paraíso': '파라이수',

  // Escort (호위)
  'circuit royal': '서킷 로얄',
  'dorado': '도라도',
  'havana': '하바나',
  'junkertown': '쓰레기촌',
  'rialto': '리알토',
  'route 66': '66번 국도',
  'route66': '66번 국도',
  'shambali monastery': '샴발리 수도원',
  'shambalimonastery': '샴발리 수도원',
  'watchpoint: gibraltar': '감시기지: 지브롤터',
  'watchpoint gibraltar': '감시기지: 지브롤터',

  // Push (밀기)
  'colosseo': '콜로세오',
  'esperanca': '이스페란사',
  'esperança': '이스페란사',
  'new queen street': '뉴 퀸 스트리트',
  'newqueenstreet': '뉴 퀸 스트리트',
  'runasapi': '루나사피',

  // Flashpoint (플래시포인트)
  'aatlis': '아틀리스',
  'new junk city': '뉴 정크 시티',
  'newjunkcity': '뉴 정크 시티',
  'suravasa': '수라바사'
};

function mapDisplayName(mapName){
  if(!mapName) return '';
  const key = String(mapName).trim().toLowerCase();
  if(state.lang === 'ko'){
    return MAP_NAMES_KO[key] || MAP_NAMES_KO[key.replace(/['"`]/g, '')] || mapName;
  }
  return mapName;
}

const I18N = {
  ko: {
    nav_overview: '대회 개요',
    nav_teams: '기본 정보',
    nav_rankings: '선수 랭킹',
    nav_plotting: '그래프',
    nav_h2h: '선수 맞대결',
    nav_matches: '경기 탐색기',

    tourney_kr_s1: 'OWCS Korea 2026 Stage 1',
    tourney_kr_s2: 'OWCS Korea 2026 Stage 2',
    tourney_kr_s3: 'OWCS Korea 2026 Stage 3',
    tourney_asia_s1: 'OWCS Asia 2026 Stage 1',
    tourney_bootcamp: 'OWCS 2026 Pre-Season Bootcamp',
    tourney_clash: 'OWCS 2026 Champions Clash',
    tourney_midseason: 'OWCS 2026 Midseason Championship',
    tourney_owwc: 'Overwatch World Cup 2026',
    status_active: '진행 중',
    status_soon: '준비 중',
    toast_soon: '해당 대회 데이터는 차기 업데이트에서 지원될 예정입니다!',

    stage3_tab_title: 'Stage 3 프리뷰',
    stage3_subtitle: '2026년 10월 2일 개막! 신규 로스터 및 참가팀 현황',
    stage3_dday_badge: 'Starts Oct 02',
    stage3_news_title: '주요 로스터 변동 & 오프시즌 이슈',
    stage3_teams_title: 'Stage 3 본선 진출 8개 팀 로스터',
    stage3_format_title: '대회 포맷 안내',
    stage3_badge_new: 'NEW',
    stage3_notice_text: '정규 리그 개막(10/2) 후 경기 결과 및 박스스코어 데이터가 실시간으로 집계 및 업데이트됩니다.',
    stage3_switch_back_btn: '← Stage 2 분석 통계 보기',

    stage2_tab_title: 'Stage 2 프리뷰',
    stage2_subtitle: '오프시즌 이적, 공식 맵 풀 및 전체 경기 일정·결과',
    stage2_status_completed: '대회 종료 (결과 확정)',
    stage2_switch_to_stats: '📊 Stage 2 상세 통계 랩 보기',
    stage2_switch_to_s3: '🚀 Stage 3 프리뷰 보기',
    stage2_schedule_heading: 'Stage 2 전체 경기 일정 & 최종 결과',
    stage2_schedule_sub: '총 36경기 정규시즌 라운드 로빈 및 2차 RR · LCQ · 플레이오프 최종 결과',
    stage2_mappool_title: 'Stage 2 공식 전장 맵 풀',
    stage2_mappool_reg: '정규 시즌 맵 풀',
    stage2_mappool_post: 'LCQ / 2차 RR / 플레이오프 맵 풀',
    stage2_transfers_title: 'Stage 1 ➔ Stage 2 선수단 변동 (IN / OUT)',
    stage2_transfers_sub: 'Stage 2 개막 전 공식 영입(IN) 및 계약 종료/이적(OUT) 현황',
    stage2_teams_title: 'Stage 2 본선 진출 8개 팀 로스터',

    teams_title: '기본 정보',
    teams_subtitle: '정규시즌 성적 및 순위와 팀별 로스터 및 선수 정보입니다.',
    lbl_tiebreak_order: '타이브레이커 규칙:',
    tiebreak_note: '공식 순위 산정 기준: 매치 승패 → 상대전적 세트 득실 → 상대전적 맵 득실 → 전체 맵 득실차.',
    maps: '세트',
    diff: '득실',
    series: '매치',
    all_teams_back: '← 전체 팀 목록',
    team_back: '← 팀으로',
    championships: '우승 경력 (Championships)',
    total_wins: '회 우승',
    lan_champion: 'OWCS International LAN Champion',
    tournament_titles: 'Tournament Titles',
    no_trophies: '기록된 공식 대회 우승 경력이 없습니다.',
    roster: '선수 로스터',
    players_count: '명',
    link_lp: 'Liquipedia 바로가기 ↗',
    export_card: '카드 저장 (PNG)',
    player_id: 'Player ID',
    position: 'Position',
    team: 'Team',
    potm_title: 'Player of the Match (POTM)',
    potm_total_awards: '총 수상',
    potm_times: '회',
    potm_empty: '기록된 Stage 2 POTM 수상 내역이 없습니다.',

    rank_title: '선수 랭킹',
    rank_sub_per10: '',
    rank_sub_acc: '스테이지 전체 누적 기록 순위입니다.',
    role_all: '전체 포지션',
    mode_per10: '10분당 기록 (Per 10)',
    mode_acc: '누적 기록 (Total)',
    min_playtime_note: '최소 출전 기준: <b>30분</b>. 표본 크기를 확인할 수 있도록 출전 시간이 함께 표기됩니다.',
    col_rank: '순위',
    col_player: '선수',
    col_team: '팀',
    col_role: '포지션',
    col_playtime: '출전 시간',

    plot_title: '그래프',
    plot_subtitle: '페이즈별 10분당 지표 산점도 비교 · 해당 페이즈 내 30분 이상 출전 기준.',
    lbl_position: '포지션',
    lbl_x_metric: '가로 축 지표',
    lbl_y_metric: '세로 축 지표',
    lbl_phase: '단계',
    lbl_highlight: '선수 하이라이트',
    eligible_players: '기준 충족 선수',
    median: '중앙값',

    h2h_title: '선수 맞대결 비교',
    h2h_subtitle: '동일 포지션 두 선수의 10분당 지표 및 포지션 내 백분위수를 직접 비교합니다.',
    h2h_export: 'H2H 카드 저장 (PNG)',
    h2h_radar_title: 'Head-to-Head Radar Profile',
    sample_warning: '표본 부족 · 30분 미만 출전',
    h2h_footnote: '그라데이션은 파란색(하위 백분위)에서 빨간색(상위 백분위)으로 표시됩니다. 백분위는 30분 이상 출전한 동일 포지션 선수를 대상으로 산출됩니다. Death / 10은 역산되어 백분위가 높을수록 생존력이 우수함을 나타냅니다. 맵 승률은 해당 선수가 출전한 세트의 팀 승률입니다.',
    map_record: '세트 전적',
    map_win_rate: '세트 승률',

    match_title: '경기 탐색기',
    match_subtitle: '대회 경기 결과, 세트별 전적, 영웅 밴 현황 및 맵별 박스스코어를 확인합니다.',
    rr_title: '정규 라운드 로빈',
    rr_note: '대진표 셀을 클릭하면 세트별 상세 결과 및 5v5 박스스코어가 열립니다.',
    analytics_phase: '분석 페이즈',
    later_phases: '후속 페이즈',
    hero_bans: '영웅 밴 통계',
    bans_by: '가 시행한 밴',
    bans_against: '를 상대로 나온 밴',
    map_win_rate_type: '팀별 맵 모드 승률',
    drill_note: '기록을 클릭하면 세부 맵별 전적과 승리 매치 상세를 확인합니다.',
    map_wins_vs: '이긴 경기',
    map_losses_vs: '진 경기',
    no_wins_map: '이긴 경기가 없습니다.',
    no_losses_map: '진 경기가 없습니다.',
    map_detail_hint: '세부 맵을 클릭하면 이긴 경기와 진 경기 목록을 확인할 수 있습니다.',
    match_win: '승리',
    match_loss: '패배',
    phase_matches: '경기 수',
    phase_maps: '총 세트',
    most_played_map: '최다 진행 맵',
    most_banned_hero: '최다 밴 영웅',

    footer_text: '데이터 출처: OWCS Korea 2026 Stage 2 공식 중계 기록 워크북 · 비공식 팬 분석 프로젝트. Blizzard Entertainment와 제휴되거나 보증되지 않았습니다.'
  },
  en: {
    nav_overview: 'Overview',
    nav_teams: 'Teams & Players',
    nav_rankings: 'Player Rankings',
    nav_plotting: 'Plotting',
    nav_h2h: 'Head-to-Head',
    nav_matches: 'Match Explorer',

    tourney_kr_s1: 'OWCS 코리아 2026 스테이지 1',
    tourney_kr_s2: 'OWCS 코리아 2026 스테이지 2',
    tourney_kr_s3: 'OWCS 코리아 2026 스테이지 3',
    tourney_asia_s1: 'OWCS 아시아 2026 스테이지 1',
    tourney_bootcamp: 'OWCS 2026 프리시즌 부트캠프',
    tourney_clash: 'OWCS 2026 챔피언스 클래시',
    tourney_midseason: 'OWCS 2026 미드시즌 챔피언십',
    tourney_owwc: '오버워치 월드컵 2026',
    status_active: 'Active',
    status_soon: 'Coming Soon',
    toast_soon: 'This tournament will be supported in upcoming updates!',

    stage3_tab_title: 'Stage 3 Preview',
    stage3_subtitle: 'Starts October 2, 2026! Roster changes & team lineups',
    stage3_dday_badge: 'Starts Oct 02',
    stage3_news_title: 'Key Roster Changes & Offseason News',
    stage3_teams_title: 'Stage 3 Qualified Teams & Rosters',
    stage3_format_title: 'Tournament Format',
    stage3_badge_new: 'NEW',
    stage3_notice_text: 'Match statistics and boxscores will be updated live once the regular season begins on Oct 2.',
    stage3_switch_back_btn: '← View Stage 2 Statistics',

    stage2_tab_title: 'Stage 2 Preview',
    stage2_subtitle: 'Offseason Transfers, Official Map Pools & Full Match Results',
    stage2_status_completed: 'Completed',
    stage2_switch_to_stats: '📊 View Stage 2 Stats Lab',
    stage2_switch_to_s3: '🚀 View Stage 3 Preview',
    stage2_schedule_heading: 'Stage 2 Match Schedule & Final Results',
    stage2_schedule_sub: '36 Regular Season Matches, 2nd Round Robin, LCQ & Playoffs',
    stage2_mappool_title: 'Stage 2 Official Map Pool',
    stage2_mappool_reg: 'Regular Season Map Pool',
    stage2_mappool_post: 'LCQ & Playoffs Map Pool',
    stage2_transfers_title: 'Stage 1 ➔ Stage 2 Roster Transfers (IN / OUT)',
    stage2_transfers_sub: 'Official signings (IN) and transfers/departures (OUT) ahead of Stage 2',
    stage2_teams_title: 'Stage 2 Qualified 8 Teams & Rosters',

    teams_title: 'Teams & Players',
    teams_subtitle: 'Round Robin standings, rosters and player profiles.',
    lbl_tiebreak_order: 'Official tiebreak order:',
    tiebreak_note: 'Official tiebreak order: Series W-L → H2H Series Differential → H2H Map Differential → Overall Map Differential.',
    maps: 'Maps',
    diff: 'Diff',
    series: 'series',
    all_teams_back: '← All Teams',
    team_back: '← Teams',
    championships: 'Championships',
    total_wins: 'Titles',
    lan_champion: 'OWCS International LAN Champion',
    tournament_titles: 'Tournament Titles',
    no_trophies: 'No official tournament titles recorded.',
    roster: 'Roster',
    players_count: 'players',
    link_lp: 'Link to Liquipedia ↗',
    export_card: 'Export Card (PNG)',
    player_id: 'Player ID',
    position: 'Position',
    team: 'Team',
    potm_title: 'Player of the Match (POTM)',
    potm_total_awards: 'Total Awards',
    potm_times: 'time(s)',
    potm_empty: 'No Stage 2 POTM awards recorded.',

    rank_title: 'Player Rankings',
    rank_sub_per10: '',
    rank_sub_acc: 'Accumulated production across the stage.',
    role_all: 'All Roles',
    mode_per10: 'Per 10',
    mode_acc: 'Accumulated',
    min_playtime_note: 'Minimum eligibility: <b>30 minutes</b>. Playtime is shown alongside rate stats to make sample size visible.',
    col_rank: 'Rank',
    col_player: 'Player',
    col_team: 'Team',
    col_role: 'Role',
    col_playtime: 'Playtime',

    plot_title: 'Plotting',
    plot_subtitle: 'Phase-specific Per 10 comparison · minimum 30 minutes within selected phase.',
    lbl_position: 'Position',
    lbl_x_metric: 'X Metric',
    lbl_y_metric: 'Y Metric',
    lbl_phase: 'Phase',
    lbl_highlight: 'Highlight Player',
    eligible_players: 'Eligible players',
    median: 'Median',

    h2h_title: 'Head-to-Head',
    h2h_subtitle: 'Compare two players from the same position using Per 10 values and same-position percentiles.',
    h2h_export: 'Export H2H (PNG)',
    h2h_radar_title: 'Head-to-Head Radar Profile',
    sample_warning: 'Limited sample · under 30 min',
    h2h_footnote: 'Gradient runs from blue (lower percentile) to red (higher percentile). Percentiles are calculated among same-position players with at least 30 minutes played. Death / 10 is inverted, so a higher percentile indicates fewer deaths. Map win rate is team map wins divided by maps in which the player recorded playtime.',
    map_record: 'map record',
    map_win_rate: 'map win rate',

    match_title: 'Match Explorer',
    match_subtitle: 'Competition results, map performance, hero bans and map-level player box scores.',
    rr_title: 'Round Robin',
    rr_note: 'Click a matchup cell to open match details and 5v5 map box scores below.',
    analytics_phase: 'Analytics Phase',
    later_phases: 'Later Phases',
    hero_bans: 'Hero Ban Statistics',
    bans_by: 'Bans by',
    bans_against: 'Bans against',
    map_win_rate_type: 'Team Win Rate by Map Type',
    drill_note: 'Click a record to drill down into individual maps.',
    map_wins_vs: 'Won Matches',
    map_losses_vs: 'Lost Matches',
    no_wins_map: 'No won matches.',
    no_losses_map: 'No lost matches.',
    map_detail_hint: 'Click a map above to see won and lost matches.',
    match_win: 'WIN',
    match_loss: 'LOSS',
    phase_matches: 'Matches',
    phase_maps: 'Maps',
    most_played_map: 'Most Played Map',
    most_banned_hero: 'Most Banned Hero',

    footer_text: 'Data: OWCS Korea 2026 Stage 2 workbook · Unofficial fan analytics project. Not affiliated with or endorsed by Blizzard Entertainment.'
  }
};

function t(key){
  const lang=state.lang||'ko';
  return I18N[lang]?.[key] || I18N.en?.[key] || key;
}

let toastTimeout=null;
function showToast(msg){
  const toast=document.getElementById('toast');
  if(!toast)return;
  toast.textContent=msg;
  toast.classList.add('show');
  if(toastTimeout)clearTimeout(toastTimeout);
  toastTimeout=setTimeout(()=>{toast.classList.remove('show')},2800);
}

function updateStaticHeaderTexts(){
  const curTitle=document.getElementById('tourneyCurrentTitle');
  if(curTitle){
    const titleMap = {
      'kr-s1': t('tourney_kr_s1'),
      'kr-s2': t('tourney_kr_s2'),
      'kr-s3': t('tourney_kr_s3'),
      'asia-s1': t('tourney_asia_s1'),
      'bootcamp-s1': t('tourney_bootcamp'),
      'clash-2026': t('tourney_clash'),
      'midseason-2026': t('tourney_midseason'),
      'owwc-2026': t('tourney_owwc')
    };
    curTitle.textContent = titleMap[state.tourney] || t('tourney_kr_s2');
  }
  const bLive=document.getElementById('badgeLive');
  if(bLive)bLive.textContent=t('status_active');
  const bEwc=document.getElementById('badgeEwcSoon');
  if(bEwc)bEwc.textContent=t('status_soon');
  const bOwwc=document.getElementById('badgeOwwcSoon');
  if(bOwwc)bOwwc.textContent=t('status_soon');
  const footer=document.getElementById('footerText');
  if(footer)footer.textContent=t('footer_text');

  document.querySelectorAll('.tourney-option').forEach(opt=>{
    opt.classList.toggle('active', opt.dataset.tourney === state.tourney);
  });
}

const TEAM_LOGOS={
  SB:'assets/teams/sb.png',
  CR:'assets/teams/cr.png',
  T1:'assets/teams/t1.png',
  PF:'assets/teams/pf.png',
  O2:'assets/teams/o2.png',
  '02':'assets/teams/o2.png',
  CB:'assets/teams/cb.png',
  FLC:'assets/teams/flc.png',
  ROZE:'assets/teams/roze.png',
  ZETA:'assets/teams/zeta.png',
  SEJ:'assets/teams/sej.png',
  RT:'assets/teams/sej.png'
};

function teamLogo(team,cls='team-logo'){
  const src=TEAM_LOGOS[team];
  if(src)return`<img class="${cls}" src="${src}?v=white" alt="${team} logo">`;
  return`<div class="${cls} team-logo-placeholder" style="display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;background:rgba(255,255,255,0.08);border-radius:6px;color:var(--text);border:1px solid rgba(255,255,255,0.12);width:28px;height:28px;flex-shrink:0;">${team}</div>`;
}

function heroAssetKey(hero){return String(hero||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[.:]/g,'').replace(/\s+/g,'-').replace(/[^a-z0-9-]/g,'')}
function heroIcon(hero,cls='hero-icon'){if(!hero)return'';const k=heroAssetKey(hero);return`<img class="${cls}" src="https://raw.githubusercontent.com/drippinghere/overwatch-hero-icons/main/2d/${k}.png" alt="${hero}" loading="lazy" onerror="this.style.display='none'">`}
const fmt=n=>n==null?'—':typeof n==='number'?n.toLocaleString(undefined,{maximumFractionDigits:2}):n;
const roleName=r=>r==='SPT'?'SUPPORT':r==='MAIN SPT'?'MAIN SUPPORT':r==='FLEX SPT'?'FLEX SUPPORT':r;
const teamNames={}; const rosters={}; let cur=null;
D.teamInfo.forEach(r=>{if(r['Team Name']&&r['Team Name']!=='#VALUE!'){cur=r.Shortened;teamNames[cur]=r['Team Name'];rosters[cur]=[]} if(r['Player Name']&&cur)rosters[cur].push({player:r['Player Name'],position:r.Detailed||r['Player Position']});});
const totals=Object.fromEntries(D.totalStats.map(r=>[r.PLAYER,r]));
const per10=Object.fromEntries(D.per10Stats.map(r=>[r.Player,r]));
const players=[...new Set(D.totalStats.map(r=>r.PLAYER))].filter(Boolean);
const phases=['All',...new Set(D.matchInfo.map(r=>r.PHASE).filter(Boolean))];
const potmByPlayer={}; D.potm.forEach(r=>{(potmByPlayer[r.POTM]??=[]).push(r)});
function groupMatches(rows=D.matchInfo){const m=new Map();rows.forEach(r=>{const key=`${r.WEEK}-${r.DAY}-${r.MATCH}-${r.PHASE}`;(m.get(key)??m.set(key,[]).get(key)).push(r)});return [...m.entries()].map(([key,maps])=>{const a=maps[0]['TEAM 1'],b=maps[0]['TEAM 2'];let aw=0,bw=0;maps.forEach(x=>{if(x.WINNER===a)aw++;else if(x.WINNER===b)bw++});return{key,a,b,aw,bw,phase:maps[0].PHASE,week:maps[0].WEEK,day:maps[0].DAY,maps,winner:aw>bw?a:b}})}
const matches=groupMatches();
function teamStandings(){
 const rr=matches.filter(m=>m.phase==='Round Robin');
 const s={};
 Object.keys(teamNames).forEach(t=>s[t]={team:t,mw:0,ml:0,mapw:0,mapl:0});
 rr.forEach(m=>{s[m.a]??={team:m.a,mw:0,ml:0,mapw:0,mapl:0};s[m.b]??={team:m.b,mw:0,ml:0,mapw:0,mapl:0};s[m.a].mapw+=m.aw;s[m.a].mapl+=m.bw;s[m.b].mapw+=m.bw;s[m.b].mapl+=m.aw;if(m.winner===m.a){s[m.a].mw++;s[m.b].ml++}else{s[m.b].mw++;s[m.a].ml++}});
 const h2h=(a,b)=>{const h=rr.filter(m=>(m.a===a.team&&m.b===b.team)||(m.a===b.team&&m.b===a.team));let as=0,bs=0,am=0,bm=0;h.forEach(m=>{if(m.winner===a.team)as++;else if(m.winner===b.team)bs++;am+=m.a===a.team?m.aw:m.bw;bm+=m.a===b.team?m.aw:m.bw});return{series:as-bs,maps:am-bm}};
 return Object.values(s).sort((a,b)=>{let d=b.mw-a.mw;if(d)return d;let h=h2h(a,b);if(h.series)return-h.series;if(h.maps)return-h.maps;d=(b.mapw-b.mapl)-(a.mapw-a.mapl);if(d)return d;return a.team.localeCompare(b.team)}).map((x,i)=>({...x,rank:i+1}));
}
const standings=teamStandings(), standingMap=Object.fromEntries(standings.map(x=>[x.team,x]));
function teamMapTypeRecord(team){const rows=D.matchInfo.filter(r=>r.PHASE==='Round Robin'&&(r['TEAM 1']===team||r['TEAM 2']===team));const types=[...new Set(rows.map(r=>r['MAP TYPE']).filter(Boolean))];return types.map(type=>{const x=rows.filter(r=>r['MAP TYPE']===type),w=x.filter(r=>r.WINNER===team).length;return{type,w,l:x.length-w,rate:x.length?Math.round(w/x.length*100):null}})}
function teamPotm(team){return Object.entries(potmByPlayer).map(([player,awards])=>({player,count:awards.filter(a=>totals[player]?.TEAM===team).length})).filter(x=>x.count>0).sort((a,b)=>b.count-a.count||a.player.localeCompare(b.player))}

let currentRadarChart = null;
let currentH2HChart = null;
let currentHallOfFameChart = null;
let currentPrizeChart = null;

function radarAxisLabel(metric){
  if(metric==='Elim / 10') return '처치 (Elim)';
  if(metric==='Damage / 10') return '딜량 (Damage)';
  if(metric==='Death / 10') return '생존율 (Survival)';
  if(metric==='Assists / 10') return '도움 (Assists)';
  if(metric==='Mitigated / 10') return '경감 (Mitigated)';
  if(metric==='Heal / 10') return '치유 (Heal)';
  return metric.replace(' / 10','');
}

function renderPlayerRadar(containerId, playerName){
  const p=per10[playerName];
  if(!p||p.Playtime_Min<30||typeof echarts==='undefined')return;
  const chartDom=document.getElementById(containerId);
  if(!chartDom)return;
  if(currentRadarChart){currentRadarChart.dispose()}
  const myChart=echarts.init(chartDom,'dark',{renderer:'canvas'});
  currentRadarChart=myChart;
  const metrics=roleMetrics(p.Position);
  const indicator=metrics.map(m=>({
    name: radarAxisLabel(m),
    max: 100
  }));
  const values=metrics.map(m=>percentile(playerName,m)||0);
  const option={
    backgroundColor:'transparent',
    tooltip:{
      trigger:'item',
      backgroundColor:'#151922',
      borderColor:'#2e3646',
      borderWidth:1,
      padding:[10,14],
      textStyle:{color:'#f8fafc',fontSize:12},
      formatter:function(){
        let res=`<b style="color:#fff;font-size:13px">${playerName} (${p.Team}) · ${roleName(p.Position)}</b><br/><div style="margin-top:6px;line-height:1.7">`;
        metrics.forEach((m,idx)=>{
          const val=Number.isFinite(+p[m])?fmt(+p[m]):'—';
          res+=`<span style="color:#94a3b8">${radarAxisLabel(m)}:</span> <b style="color:#ff9e42">${values[idx]}th %</b> <small style="color:#cbd5e1">(${val}/10m)</small><br/>`;
        });
        res+=`</div>`;
        return res;
      }
    },
    radar:{
      indicator:indicator,
      shape:'polygon',
      splitNumber:4,
      axisName:{color:'#cbd5e1',fontSize:11.5,fontWeight:'700'},
      splitLine:{lineStyle:{color:'rgba(255,255,255,0.1)'}},
      splitArea:{show:true,areaStyle:{color:['rgba(255,255,255,0.015)','rgba(255,255,255,0.035)']}},
      axisLine:{lineStyle:{color:'rgba(255,255,255,0.12)'}}
    },
    series:[{
      name:playerName,
      type:'radar',
      data:[{
        value:values,
        name:`${playerName} Percentile`,
        symbol:'circle',
        symbolSize:7,
        itemStyle:{color:'#ff6b2c'},
        areaStyle:{color:'rgba(255,107,44,0.3)'},
        lineStyle:{width:2.5,color:'#ff6b2c'}
      }]
    }]
  };
  myChart.setOption(option);
}

function renderH2HRadar(containerId,playerA,playerB){
  const A=per10[playerA],B=per10[playerB];
  if(!A||!B||typeof echarts==='undefined')return;
  const chartDom=document.getElementById(containerId);
  if(!chartDom)return;
  if(currentH2HChart){currentH2HChart.dispose()}
  const myChart=echarts.init(chartDom,'dark',{renderer:'canvas'});
  currentH2HChart=myChart;
  const metrics=roleMetrics(state.h2hRole);
  const indicator=metrics.map(m=>({
    name: radarAxisLabel(m),
    max: 100
  }));
  const valuesA=metrics.map(m=>percentile(playerA,m)||0);
  const valuesB=metrics.map(m=>percentile(playerB,m)||0);
  const seriesData=[];
  if(A.Playtime_Min>=30){
    seriesData.push({
      value:valuesA,
      name:`${A.Player} (${A.Team})`,
      symbol:'circle',
      symbolSize:6,
      itemStyle:{color:'#ff6b2c'},
      areaStyle:{color:'rgba(255,107,44,0.22)'},
      lineStyle:{width:2,color:'#ff6b2c'}
    });
  }
  if(B.Playtime_Min>=30){
    seriesData.push({
      value:valuesB,
      name:`${B.Player} (${B.Team})`,
      symbol:'circle',
      symbolSize:6,
      itemStyle:{color:'#38bdf8'},
      areaStyle:{color:'rgba(56,189,248,0.22)'},
      lineStyle:{width:2,color:'#38bdf8'}
    });
  }
  const option={
    backgroundColor:'transparent',
    tooltip:{trigger:'item',backgroundColor:'#1b1f28',borderColor:'#2a303b',textStyle:{color:'#f4f6f8',fontSize:12}},
    legend:{data:seriesData.map(s=>s.name),textStyle:{color:'#cbd5e1',fontSize:12},bottom:0},
    radar:{
      indicator:indicator,
      shape:'polygon',
      splitNumber:4,
      axisName:{color:'#cbd5e1',fontSize:11.5,fontWeight:'700'},
      splitLine:{lineStyle:{color:'rgba(255,255,255,0.1)'}},
      splitArea:{show:true,areaStyle:{color:['rgba(255,255,255,0.015)','rgba(255,255,255,0.035)']}},
      axisLine:{lineStyle:{color:'rgba(255,255,255,0.12)'}}
    },
    series:[{name:'Comparison',type:'radar',data:seriesData}]
  };
  myChart.setOption(option);
}

function downloadCard(elementId,filename='owcs-stat-card.png'){
  const target=document.getElementById(elementId);
  if(!target||typeof html2canvas==='undefined')return;
  target.classList.add('is-exporting');
  html2canvas(target,{
    backgroundColor:'#0c0e12',
    scale:2,
    useCORS:true,
    logging:false
  }).then(canvas=>{
    target.classList.remove('is-exporting');
    const link=document.createElement('a');
    link.download=filename;
    link.href=canvas.toDataURL('image/png');
    link.click();
  }).catch(err=>{
    target.classList.remove('is-exporting');
    console.error('Image export failed:',err);
  });
}

function getTourneyDataset(tourneyKey) {
  if (tourneyKey === 'kr-s1') return window.OWCS_STAGE1_PREVIEW;
  if (tourneyKey === 'kr-s2') return window.OWCS_STAGE2_PREVIEW;
  if (tourneyKey === 'kr-s3') return window.OWCS_STAGE3_PREVIEW;
  if (tourneyKey === 'asia-s1') return window.OWCS_ASIA_S1_PREVIEW;
  if (tourneyKey === 'bootcamp-s1') return window.OWCS_BOOTCAMP_PREVIEW;
  if (tourneyKey === 'clash-2026') return window.OWCS_CLASH_PREVIEW;
  if (tourneyKey === 'midseason-2026') return window.OWCS_MIDSEASON_PREVIEW;
  if (tourneyKey === 'owwc-2026') return window.OWCS_OWWC_PREVIEW;
  return null;
}

function getNavItems(){
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
}

function nav(){
  document.getElementById('nav').innerHTML=getNavItems().map(([k,l])=>`
    <button class="navbtn ${state.page===k?'active':''}" data-page="${k}">${l}</button>
  `).join('');
  document.querySelectorAll('[data-page]').forEach(b=>b.onclick=()=>{
    const p=b.dataset.page;
    state.page=p;
    localStorage.setItem('owcs_stat_lab_page', p);
    if(p!=='teams'){
      state.team=null;
      state.player=null;
    }
    render();
  });
}

function percentile(player,metric){
  const p=per10[player];
  if(!p||p.Playtime_Min<30)return null;
  const pool=D.per10Stats.filter(x=>x.Position===p.Position&&x.Playtime_Min>=30&&Number.isFinite(+x[metric]));
  if(!pool.length)return null;
  let v=+p[metric];
  let better=pool.filter(x=>metric==='Death / 10'?+x[metric]>=v:+x[metric]<=v).length;
  return Math.round((better-1)/Math.max(1,pool.length-1)*100);
}

function roleMetrics(role){
  if(role==='TANK') return ['Elim / 10','Damage / 10','Death / 10','Assists / 10','Mitigated / 10'];
  if(role==='SPT'||role==='MAIN SPT'||role==='FLEX SPT') return ['Elim / 10','Damage / 10','Death / 10','Assists / 10','Heal / 10'];
  return ['Elim / 10','Damage / 10','Death / 10','Assists / 10'];
}

const METRIC_META = {
  'Elim / 10': { icon: '⚔️', nameKo: '10분당 처치 (Elim)', desc: '10분당 결정타 및 처치 관여 횟수' },
  'Damage / 10': { icon: '💥', nameKo: '10분당 피해량 (Damage)', desc: '10분당 적에게 입힌 총 피해량' },
  'Death / 10': { icon: '🛡️', nameKo: '10분당 생존율 (Survival)', desc: '적은 데스수 = 높은 생존율 백분위 (역산 산출)' },
  'Assists / 10': { icon: '🤝', nameKo: '10분당 어시스트 (Assists)', desc: '10분당 아군 연계 및 보조 킬 기여' },
  'Mitigated / 10': { icon: '🛡️', nameKo: '10분당 피해 경감 (Mitigated)', desc: '탱커 방벽 및 보호 스킬로 흡수한 피해량' },
  'Heal / 10': { icon: '💚', nameKo: '10분당 치유량 (Heal)', desc: '힐러의 10분당 누적 아군 회복량' }
};

function teamLiquipediaUrl(team) {
  const lt = L.teams?.[team];
  if (lt && lt.liquipediaUrl) return lt.liquipediaUrl;
  const slugs = {
    CR: 'Crazy_Raccoon',
    FLC: 'Team_Falcons',
    ZETA: 'ZETA_DIVISION',
    PF: 'Poker_Face',
    T1: 'T1',
    FNC: 'Fnatic',
    GEN: 'Genesis_(Korean_team)',
    HJD: 'HaeJeokDan',
    OO: 'Old_Ocean',
    NT: 'Night_Talon',
    CB: 'Cheeseburger',
    ROZE: 'Røde_Zanside_Gaming',
    SB: 'SuperBad',
    O2: 'O2_Blast',
    VEC: 'VEC'
  };
  const slug = slugs[team] || (teamNames[team] || team).replace(/\s+/g, '_');
  return `https://liquipedia.net/overwatch/${slug}`;
}

function playerLiquipediaUrl(name) {
  const lp = L.players?.[name];
  if (lp && lp.liquipediaUrl) return lp.liquipediaUrl;
  return `https://liquipedia.net/overwatch/${encodeURIComponent(name)}`;
}

function playerProfile(name){
  const tInfo=totals[name];
  if(!tInfo)return`<div class="note">Player data unavailable.</div>`;
  const awards=potmByPlayer[name]||[];
  const teamCode=tInfo.TEAM;
  const teamFullName=teamNames[teamCode]||teamCode;
  const lpUrl=playerLiquipediaUrl(name);

  // Per 10 & Percentile Calculations
  const p = per10[name];
  const playtime = p ? +p.Playtime_Min : 0;
  const isQualified = p && playtime >= 30;
  const pos = p ? p.Position : (tInfo.POSITION || 'DPS');
  const metrics = roleMetrics(pos);
  const pool = D.per10Stats.filter(x => x.Position === pos && x.Playtime_Min >= 30);
  const poolCount = pool.length;

  const stats = metrics.map(m => {
    const rawVal = (p && Number.isFinite(+p[m])) ? +p[m] : null;
    if (!isQualified || rawVal === null || !poolCount) {
      return {
        metric: m,
        rawVal: rawVal,
        pct: null,
        rank: null,
        poolCount: poolCount
      };
    }
    const pct = percentile(name, m);
    let rank = 1;
    if (m === 'Death / 10') {
      rank = pool.filter(x => +x[m] < rawVal).length + 1;
    } else {
      rank = pool.filter(x => +x[m] > rawVal).length + 1;
    }
    return {
      metric: m,
      rawVal: rawVal,
      pct: pct,
      rank: rank,
      poolCount: poolCount
    };
  });

  return`<div class="profile-header-actions">
    <a href="${lpUrl}" target="_blank" rel="noopener noreferrer" class="btn-lp-external">
      <span class="lp-external-icon">📖</span> ${t('link_lp')}
    </a>
    <button class="btn-export" id="btnExportProfile">
      <span class="btn-export-icon">📸</span> ${t('export_card')}
    </button>
  </div>
  <div id="player-profile-export" class="export-target card player-simple-profile-card">
    <div class="player-simple-header">
      <div class="player-simple-logo-wrap">
        ${teamLogo(teamCode,'profile-team-logo-lg')}
      </div>
      <div class="player-simple-meta">
        <div class="player-meta-badges">
          <span class="profile-team-tag">${teamFullName}</span>
          <span class="role-pill">${roleName(pos)}</span>
          ${!isQualified ? '<span class="pill-nq-top-badge">⚠️ NOT QUALIFIED</span>' : ''}
        </div>
        <h1 class="player-simple-name">${name}</h1>
      </div>
    </div>

    <!-- Basic Info Grid -->
    <!-- Basic Info Grid -->
    <div class="player-info-grid">
      <div class="player-info-item">
        <span class="player-info-label">${t('player_id')}</span>
        <b class="player-info-val">${name}</b>
      </div>
      <div class="player-info-item">
        <span class="player-info-label">${t('position')}</span>
        <b class="player-info-val">${roleName(pos)}</b>
      </div>
      <div class="player-info-item">
        <span class="player-info-label">${t('team')}</span>
        <b class="player-info-val">${teamFullName} (${teamCode})</b>
      </div>
      <div class="player-info-item">
        <span class="player-info-label">출전 시간 (Playtime)</span>
        <b class="player-info-val ${!isQualified ? 'val-not-qualified' : ''}">
          ${playtime > 0 ? playtime.toFixed(1) + '분' : '0.0분'}
          ${!isQualified ? '<span class="pill-nq-badge">NOT QUALIFIED (&lt;30m)</span>' : ''}
        </b>
      </div>
    </div>

    <!-- NOT QUALIFIED Alert Banner (if under 30 minutes) -->
    ${!isQualified ? `
      <div class="not-qualified-banner">
        <div class="nq-badge-box">
          <span class="nq-alert-icon">⚠️</span>
          <span class="nq-badge-text">NOT QUALIFIED</span>
        </div>
        <div class="nq-message-box">
          <div class="nq-message-title">최소 출전 시간(30분) 미달 선수</div>
          <div class="nq-message-desc">
            현재 정규 시즌 출전 시간은 <b>${playtime > 0 ? playtime.toFixed(1) + '분' : '0.0분'}</b>입니다. 신뢰도 높은 백분위 통계 산출 기준(최소 30분)에 미달하여 공식 백분위 랭킹(Percentile Ranking) 대상에서 제외되었습니다. 아래 지표는 참고용으로만 표시됩니다.
          </div>
        </div>
      </div>
    ` : ''}

    <!-- Per 10 Percentile Ranking Section -->
    <div class="player-percentile-section ${!isQualified ? 'is-not-qualified' : ''}">
      <div class="pct-section-topbar">
        <div class="pct-title-group">
          <h3 class="pct-title">
            <span class="pct-title-icon">📊</span> Per 10 백분위 랭킹 (Percentile Ranking)
          </h3>
          <span class="pct-sub-tag">
            ${isQualified 
              ? `동일 포지션 (${roleName(pos)}) ${poolCount}명 기준 · 최소 30분 이상 출전자 풀` 
              : `최소 출전 기준 30분 미달 (${playtime > 0 ? playtime.toFixed(1) : '0'}분 출전 · 백분위 미산출)`}
          </span>
        </div>
        <div class="pct-playtime-tag ${!isQualified ? 'is-nq' : ''}">
          ⏱️ 출전 시간: <b>${playtime > 0 ? playtime.toFixed(1) + '분' : '-'}</b>
          ${!isQualified ? '<span class="nq-tag-pill">NOT QUALIFIED</span>' : ''}
        </div>
      </div>

      <div class="pct-content-grid">
        <!-- Left: Radar Chart Box -->
        <div class="pct-radar-card">
          <div class="pct-radar-head">
            <span class="radar-card-title">📈 포지션 지표 레이더</span>
            ${isQualified ? '<span class="radar-live-badge">Percentile</span>' : '<span class="radar-nq-badge">NQ</span>'}
          </div>
          ${isQualified ? `
            <div id="profile-radar-canvas" class="pct-radar-canvas"></div>
            <div class="pct-radar-footnote">
              * 레이더 차트의 각 꼭짓점은 30분 이상 출전한 동일 포지션 선수 대비 백분위(0~100%)를 나타냅니다.
            </div>
          ` : `
            <div class="pct-radar-empty">
              <div class="nq-radar-empty-icon">📊</div>
              <div class="nq-radar-empty-title">레이더 차트 비활성화</div>
              <div class="nq-radar-empty-desc">출전 시간 30분 이상 달성 시<br/>포지션 백분위 다이어그램이 활성화됩니다.</div>
              <div class="nq-radar-empty-time">현재 출전: <b>${playtime > 0 ? playtime.toFixed(1) : 0}분</b> / 30분</div>
            </div>
          `}
        </div>

        <!-- Right: Percentile Metrics List -->
        <div class="pct-metrics-card">
          <div class="pct-metrics-head">
            <span class="metrics-card-title">포지션 세부 지표 & 랭킹</span>
            ${isQualified ? `
              <span class="metrics-legend">
                <span class="legend-dot dot-gold"></span> 상위 20%
                <span class="legend-dot dot-cyan"></span> 상위 50%
                <span class="legend-dot dot-slate"></span> 50% 이하
              </span>
            ` : `
              <span class="metrics-legend" style="color:#f87171">
                ⚠️ 공식 백분위 산출 제외
              </span>
            `}
          </div>

          <div class="pct-metrics-list">
            ${stats.map(s => {
              const meta = METRIC_META[s.metric] || { icon: '📊', nameKo: s.metric, desc: '' };
              const isTopTier = s.pct !== null && s.pct >= 80;
              const isMidTier = s.pct !== null && s.pct >= 50 && s.pct < 80;
              const tierClass = isTopTier ? 'tier-gold' : isMidTier ? 'tier-cyan' : 'tier-slate';
              
              return `
                <div class="pct-metric-row ${tierClass} ${!isQualified ? 'row-not-qualified' : ''}">
                  <div class="pct-metric-info">
                    <div class="pct-metric-name-wrap">
                      <span class="pct-metric-icon">${meta.icon}</span>
                      <span class="pct-metric-name">${meta.nameKo}</span>
                      ${meta.desc ? `<span class="pct-metric-tooltip" title="${meta.desc}">ℹ️</span>` : ''}
                    </div>
                    <div class="pct-metric-values">
                      <span class="pct-raw-val">${s.rawVal !== null ? fmt(s.rawVal) : '—'}<small>/10m</small></span>
                      ${isQualified && s.rank !== null ? `
                        <span class="pct-rank-badge ${s.rank === 1 ? 'rank-first' : ''}">
                          ${s.rank === 1 ? '👑 #1' : `#${s.rank}`} <span class="rank-total">/ ${s.poolCount}</span>
                        </span>
                      ` : ''}
                      ${isQualified && s.pct !== null ? `
                        <span class="pct-percentile-badge ${tierClass}">
                          ${s.pct}th %
                        </span>
                      ` : `
                        <span class="pct-percentile-badge nq-badge-mini">
                          NOT QUALIFIED
                        </span>
                      `}
                    </div>
                  </div>

                  <!-- Bar Track -->
                  <div class="pct-bar-track">
                    ${isQualified && s.pct !== null ? `
                      <div class="pct-bar-fill ${tierClass}" style="width: ${Math.max(6, s.pct)}%"></div>
                    ` : `
                      <div class="pct-bar-fill is-nq" style="width: 15%"></div>
                    `}
                  </div>
                </div>
              `;
            }).join('')}
          </div>

          ${isQualified ? `
            <div class="pct-footer-note">
              💡 <b>지표 안내:</b> 생존율(Survival)은 데스 수(Death / 10)의 역산으로, 적게 죽을수록 더 높은 백분위와 1위에 가까운 랭킹을 부여받습니다.
            </div>
          ` : `
            <div class="pct-footer-note nq-note">
              ⚠️ <b>안내:</b> 출전 시간 30분 미만 선수의 수치는 표본 부족으로 공식 백분위 및 순위가 산정되지 않으며 참고용 기록만 표시됩니다.
            </div>
          `}
        </div>
      </div>
    </div>
    <div class="player-potm-section">
      <div class="potm-section-head">
        <div class="potm-section-title">
          <span class="potm-star-icon">⭐</span> ${t('potm_title')}
        </div>
        <span class="badge-potm-count">${t('potm_total_awards')} <b>${awards.length}</b>${t('potm_times')}</span>
      </div>
      ${awards.length?`
        <div class="player-potm-list">
          ${awards.map(a=>`
            <div class="player-potm-item">
              <span class="potm-date">🗓️ ${a.Date}</span>
              <span class="potm-match">⚔️ ${a.Match}</span>
              ${a.Hero?`<span class="potm-hero">👤 ${a.Hero}</span>`:''}
            </div>
          `).join('')}
        </div>
      `:`<div class="potm-empty-msg">${t('potm_empty')}</div>`}
    </div>
    <div class="export-watermark">OWCS Korea 2026 Stage 2 · Stat Lab</div>
  </div>`;
}

function statTable(rows){return`<div class="table-wrap"><table><tbody>${rows.map(([a,b])=>`<tr><td>${a}</td><td>${fmt(b)}</td></tr>`).join('')}</tbody></table></div>`}

function teamsPage() {
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

// ==============================================================================
// OWCS TOURNAMENTS & HISTORICAL ARCHIVE
// ==============================================================================

function findGlobalTeamId(teamName) {
  if (!teamName) return null;
  const clean = teamName.trim();
  const directMap = {
    'Crazy Raccoon': 'CR',
    'CR': 'CR',
    'Team Falcons': 'FLC',
    'FLC': 'FLC',
    'Falcons': 'FLC',
    'T1': 'T1',
    'ZETA DIVISION': 'ZETA',
    'ZETA': 'ZETA',
    'Røde Zanside Gaming': 'ROZE',
    'Røde ZANSIDE GAMING': 'ROZE',
    'ROZE': 'ROZE',
    'Cheeseburger': 'CB',
    'CB': 'CB',
    'O2 Blast': 'O2',
    'O2': 'O2',
    'Poker Face': 'PF',
    'PF': 'PF',
    'Super Bad': 'SB',
    'SuperBad': 'SB',
    'SB': 'SB',
    'Spacestation Gaming': 'SSG',
    'SSG': 'SSG',
    'Team Liquid': 'TL',
    'TL': 'TL',
    'Dallas Fuel': 'DF',
    'DF': 'DF',
    'M80': 'M80',
    'Disguised': 'DSG',
    'disguised': 'DSG',
    'DSG': 'DSG',
    'Toronto Defiant': 'TD',
    'Toronto Ultra': 'TD',
    'TD': 'TD',
    'NTMR': 'NTMR',
    'Luminosity Gaming': 'LG',
    'LG': 'LG',
    'Citrus Nation': 'CN',
    'Students of the Game': 'SOTG',
    'SOTG': 'SOTG',
    'From The Gamer': 'FTG',
    'FTG': 'FTG',
    'We Are Chicks': 'WAC',
    'WAC': 'WAC',
    'New Era': 'ERA',
    'ERA': 'ERA',
    'ZAN Esports': 'ZAN',
    'ZAN': 'ZAN',
    'ONSIDE GAMING': 'OSG',
    'Røde ONSIDE GAMING': 'OSG',
    'OSG': 'OSG',
    'ENCE': 'ENCE',
    'FNATIC': 'FNC',
    'Fnatic': 'FNC',
    'FNC': 'FNC',
    'VARREL': 'VAR',
    'VAR': 'VAR',
    'ALBUS Esports': 'ALB',
    'Space Gaming': 'SPG'
  };
  if (directMap[clean]) return directMap[clean];
  const allTeams = window.OWCS_GLOBAL_TEAMS?.teams || {};
  for (const [id, t] of Object.entries(allTeams)) {
    if ((t.name && t.name.toLowerCase() === clean.toLowerCase()) || 
        (t.nameKo && t.nameKo.toLowerCase() === clean.toLowerCase())) {
      return id;
    }
  }
  return null;
}

function tournamentsPage() {
  const isKo = state.lang === 'ko';
  state.tourneyYear = state.tourneyYear || 'ALL';
  state.tourneyCat = state.tourneyCat || 'ALL';
  state.tourneySearch = state.tourneySearch || '';
  state.tourneyView = state.tourneyView || 'grid';

  const db = window.OWCS_TOURNAMENT_DATABASE || { tournaments: [], summary: {} };
  const allTourneys = db.tournaments || [];
  const summary = db.summary || {};

  // Filter tournaments
  const filtered = allTourneys.filter(t => {
    // Year filter
    if (state.tourneyYear !== 'ALL' && t.year.toString() !== state.tourneyYear.toString()) {
      return false;
    }
    // Category filter
    if (state.tourneyCat !== 'ALL') {
      if (state.tourneyCat === 'LAN' && t.category !== 'LAN') return false;
      if (state.tourneyCat !== 'LAN' && t.category !== state.tourneyCat) return false;
    }
    // Search query filter
    if (state.tourneySearch) {
      const q = state.tourneySearch.toLowerCase();
      const inTitle = (t.name || '').toLowerCase().includes(q) || (t.nameKo || '').toLowerCase().includes(q);
      const inLoc = (t.location || '').toLowerCase().includes(q) || (t.venue || '').toLowerCase().includes(q);
      const inChamp = (t.champion || '').toLowerCase().includes(q) || (t.runnerUp || '').toLowerCase().includes(q);
      const inTeams = (t.teams || []).some(tm => tm.toLowerCase().includes(q));
      if (!inTitle && !inLoc && !inChamp && !inTeams) return false;
    }
    return true;
  });

  // Calculate filtered stats
  const totalPrizeFiltered = filtered.reduce((acc, cur) => acc + (cur.prizeNum || 0), 0);

  // Year buttons
  const years = ['ALL', '2024', '2025', '2026'];
  const yearTabsHtml = years.map(y => {
    const active = state.tourneyYear === y ? 'active' : '';
    const label = y === 'ALL' ? (isKo ? '전체 시즌' : 'All Years') : `${y} ${isKo ? '시즌' : 'Season'}`;
    return `<button class="tourney-year-btn ${active}" data-year="${y}">${label}</button>`;
  }).join('');

  // Category chips
  const categories = summary.categories || [
    { code: 'ALL', nameKo: '전체 대회', nameEn: 'All Tournaments', icon: '🌐' },
    { code: 'LAN', nameKo: '글로벌 LAN 메이저', nameEn: 'Global LAN', icon: '🌍' },
    { code: 'KR', nameKo: '한국 (Korea)', nameEn: 'Korea', icon: '🇰🇷' },
    { code: 'NA', nameKo: '북미 (NA)', nameEn: 'North America', icon: '🇺🇸' },
    { code: 'EMEA', nameKo: '유럽·중동 (EMEA)', nameEn: 'EMEA', icon: '🇪🇺' },
    { code: 'CN', nameKo: '중국 (China)', nameEn: 'China', icon: '🇨🇳' },
    { code: 'JP', nameKo: '일본 (Japan)', nameEn: 'Japan', icon: '🇯🇵' },
    { code: 'PA', nameKo: '태평양 (Pacific)', nameEn: 'Pacific', icon: '🌏' },
    { code: 'ASIA', nameKo: '아시아 본선', nameEn: 'Asia Main', icon: '🌏' }
  ];

  const catChipsHtml = categories.map(c => {
    const active = state.tourneyCat === c.code ? 'active' : '';
    const count = c.code === 'ALL' 
      ? allTourneys.length 
      : allTourneys.filter(x => x.category === c.code).length;
    const label = isKo ? c.nameKo : c.nameEn;
    const prizeBadge = c.prizeFormatted ? `<span style="font-size:10.5px;color:#4ade80;font-weight:700;background:rgba(34,197,94,0.12);padding:1px 6px;border-radius:4px;border:1px solid rgba(34,197,94,0.25);margin-left:2px;">${c.prizeFormatted}</span>` : '';
    return `
      <button class="tourney-cat-chip ${active}" data-cat="${c.code}">
        <span>${c.icon}</span>
        <span>${label}</span>
        <span style="opacity:0.6;font-size:11px;">(${count})</span>
        ${prizeBadge}
      </button>
    `;
  }).join('');

  // Cards or Timeline
  let contentHtml = '';
  if (filtered.length === 0) {
    contentHtml = `
      <div style="text-align:center;padding:60px 20px;background:var(--panel);border:1px dashed var(--line);border-radius:12px;color:var(--text-muted);">
        <div style="font-size:36px;margin-bottom:12px;">🔍</div>
        <div style="font-size:16px;color:#fff;font-weight:700;">${isKo ? '검색된 대회가 없습니다' : 'No tournaments found'}</div>
        <div style="font-size:13px;margin-top:6px;">${isKo ? '필터 조건을 변경하거나 다른 검색어를 입력해 보세요.' : 'Try changing your filter criteria or search query.'}</div>
      </div>
    `;
  } else if (state.tourneyView === 'timeline') {
    // Timeline View
    const timelineItemsHtml = filtered.map(t => {
      const isLAN = t.isLAN;
      const champId = findGlobalTeamId(t.champion);
      const runnerId = findGlobalTeamId(t.runnerUp);
      
      const teamsChips = (t.teams || []).map(tm => {
        const tid = findGlobalTeamId(tm);
        const isChamp = tm === t.champion;
        return `<span class="tourney-team-chip ${isChamp ? 'champion-chip' : ''}" data-team-jump="${tid || ''}" data-team-name="${tm}">${isChamp ? '🏆 ' : ''}${tm}</span>`;
      }).join('');

      return `
        <div class="timeline-item ${isLAN ? 'lan-event' : ''}">
          <div class="timeline-dot"></div>
          <div class="tourney-card ${isLAN ? 'lan-card' : ''}" style="margin:0;">
            <div class="tourney-card-top">
              <div class="tourney-badges">
                <span class="badge-tourney-region">${t.regionIcon} ${t.category}</span>
                <span class="badge-tourney-tier ${t.tier === 'Major' ? 'badge-tier-major' : t.tier === 'World Finals' ? 'badge-tier-finals' : 'badge-tier-regional'}">${t.tier}</span>
                <span class="badge-tourney-region">${t.year}</span>
              </div>
              <div class="tourney-card-prize ${t.prizeNum === 0 ? 'tbd' : ''}">${t.prize}</div>
            </div>
            
            <div>
              <h3 class="tourney-card-title">${isKo ? (t.nameKo || t.name) : t.name}</h3>
              <div class="tourney-card-meta">
                <div class="tourney-card-meta-item">📅 ${t.startDate} ~ ${t.endDate}</div>
                <div class="tourney-card-meta-item">📍 ${t.venue || t.location}</div>
              </div>
            </div>

            <div class="tourney-podium-box">
              <div class="podium-slot">
                <span class="podium-slot-title gold">🥇 ${isKo ? '우승 (Champion)' : '1st Place'}</span>
                <span class="podium-slot-team" data-team-jump="${champId || ''}" data-team-name="${t.champion}" title="${champId ? '팀 상세 페이지로 이동' : ''}">${t.champion}</span>
              </div>
              <div class="podium-slot">
                <span class="podium-slot-title silver">🥈 ${isKo ? '준우승 (Runner-Up)' : '2nd Place'}</span>
                <span class="podium-slot-team" data-team-jump="${runnerId || ''}" data-team-name="${t.runnerUp}" title="${runnerId ? '팀 상세 페이지로 이동' : ''}">${t.runnerUp}</span>
              </div>
            </div>

            <div class="tourney-teams-wrap">
              <div class="tourney-teams-head">
                <span>👥 ${isKo ? '참가 팀' : 'Participating Teams'} (${t.teams ? t.teams.length : t.teamCount})</span>
              </div>
              <div class="tourney-teams-chips">
                ${teamsChips}
              </div>
            </div>
          </div>
        </div>
      `;
    }).join('');

    contentHtml = `<div class="tourney-timeline-wrap">${timelineItemsHtml}</div>`;
  } else {
    // Grid Cards View
    const cardsHtml = filtered.map(t => {
      const isLAN = t.isLAN;
      const champId = findGlobalTeamId(t.champion);
      const runnerId = findGlobalTeamId(t.runnerUp);

      const teamsChips = (t.teams || []).map(tm => {
        const tid = findGlobalTeamId(tm);
        const isChamp = tm === t.champion;
        return `<span class="tourney-team-chip ${isChamp ? 'champion-chip' : ''}" data-team-jump="${tid || ''}" data-team-name="${tm}" title="${tid ? '팀 프로필 보기' : ''}">${isChamp ? '🏆 ' : ''}${tm}</span>`;
      }).join('');

      return `
        <div class="tourney-card ${isLAN ? 'lan-card' : ''}">
          <div>
            <div class="tourney-card-top">
              <div class="tourney-badges">
                <span class="badge-tourney-region">${t.regionIcon} ${t.category}</span>
                <span class="badge-tourney-tier ${t.tier === 'Major' ? 'badge-tier-major' : t.tier === 'World Finals' ? 'badge-tier-finals' : 'badge-tier-regional'}">${t.tier}</span>
                <span class="badge-tourney-region">${t.year}</span>
              </div>
              <div class="tourney-card-prize ${t.prizeNum === 0 ? 'tbd' : ''}">${t.prize}</div>
            </div>

            <h3 class="tourney-card-title">${isKo ? (t.nameKo || t.name) : t.name}</h3>
            <div class="tourney-card-meta">
              <div class="tourney-card-meta-item">📅 ${t.startDate} ~ ${t.endDate}</div>
              <div class="tourney-card-meta-item" title="${t.venue || t.location}">📍 ${t.venue || t.location}</div>
            </div>
          </div>

          <div class="tourney-podium-box">
            <div class="podium-slot">
              <span class="podium-slot-title gold">🥇 ${isKo ? '우승 (Champion)' : '1st Place'}</span>
              <span class="podium-slot-team" data-team-jump="${champId || ''}" data-team-name="${t.champion}" title="${champId ? '팀 상세 페이지로 이동' : ''}">${t.champion}</span>
            </div>
            <div class="podium-slot">
              <span class="podium-slot-title silver">🥈 ${isKo ? '준우승 (Runner-Up)' : '2nd Place'}</span>
              <span class="podium-slot-team" data-team-jump="${runnerId || ''}" data-team-name="${t.runnerUp}" title="${runnerId ? '팀 상세 페이지로 이동' : ''}">${t.runnerUp}</span>
            </div>
          </div>

          <div class="tourney-teams-wrap">
            <div class="tourney-teams-head">
              <span>👥 ${isKo ? '참가 팀' : 'Participating Teams'} (${t.teams ? t.teams.length : t.teamCount})</span>
            </div>
            <div class="tourney-teams-chips">
              ${teamsChips}
            </div>
          </div>
        </div>
      `;
    }).join('');

    contentHtml = `<div class="tourney-cards-grid">${cardsHtml}</div>`;
  }

  // Derive dynamic Hero KPIs from summary
  const topChamp = (summary.topChampions && summary.topChampions[0]) || { team: 'Crazy Raccoon', titles: 9 };
  const topPodium = (summary.topPodiums || []).find(p => p.team === topChamp.team);
  const champWins = topChamp.titles || 0;
  const champFinals = topPodium ? topPodium.finals : champWins;
  const champRunner = Math.max(0, champFinals - champWins);
  const lanCount = allTourneys.filter(t => t.category === 'LAN').length;
  const regionalCount = allTourneys.length - lanCount;

  return `
    <div class="tourney-hero">
      <div class="tourney-hero-title">
        <span style="font-size:32px;">🏆</span>
        <h1>${isKo ? 'OWCS 공식 대회 역사 & 토너먼트 아카이브' : 'OWCS Official Tournaments & Historical Archive'}</h1>
      </div>
      <p class="tourney-hero-desc">
        ${isKo 
          ? '2024~2026 역대 OWCS 전 권역(한국, 북미, EMEA, 중국, 일본, 태평양, 아시아) 및 글로벌 LAN 메이저 토너먼트의 공식 일정, 총상금, 참가팀, 챔피언 통합 데이터베이스입니다.'
          : 'Official tournament records, schedules, prize pools, venues, champions, and participating team rosters across all OWCS regions (KR, NA, EMEA, CN, JP, PA, ASIA) and Global LAN Majors (2024-2026).'
        }
      </p>

      <div class="tourney-kpis">
        <div class="tourney-kpi-card">
          <span class="tourney-kpi-label">🏟️ ${isKo ? '총 개최 대회' : 'Total Tournaments'}</span>
          <span class="tourney-kpi-val">${summary.totalTournaments || allTourneys.length} <span style="font-size:15px;color:var(--text-muted);font-weight:600;">Events</span></span>
          <span class="tourney-kpi-sub">🌍 LAN ${lanCount}개 · 권역 ${regionalCount}개</span>
        </div>
        <div class="tourney-kpi-card">
          <span class="tourney-kpi-label">💰 ${isKo ? '누적 총상금' : 'Cumulative Prize Pool'}</span>
          <span class="tourney-kpi-val" style="color:#4ade80;">${summary.totalPrizeUsdFormatted || '$7,884,116'}</span>
          <span class="tourney-kpi-sub">${isKo ? '한화 약 105억 원 (Asia Main: $155,000)' : 'Approx. 10.5 Billion KRW (Asia Main: $155,000)'}</span>
        </div>
        <div class="tourney-kpi-card">
          <span class="tourney-kpi-label">👑 ${isKo ? '역대 최다 우승' : 'All-time Top Champion'}</span>
          <span class="tourney-kpi-val" style="color:#fbbf24;">${topChamp.team}</span>
          <span class="tourney-kpi-sub">${champWins}${isKo ? '회 우승' : ' Titles'} · ${champRunner}${isKo ? '회 준우승' : ' Runner-up'}</span>
        </div>
        <div class="tourney-kpi-card">
          <span class="tourney-kpi-label">🗓️ ${isKo ? '공식 서킷 시즌' : 'Active Circuit'}</span>
          <span class="tourney-kpi-val">2024 ~ 2026</span>
          <span class="tourney-kpi-sub">${isKo ? '3개년 공식 서킷' : '3-Year Official Circuit'}</span>
        </div>
      </div>
    </div>

    <!-- Visual Analytics: ECharts Row -->
    <div class="tourney-charts-grid">
      <div class="tourney-chart-panel">
        <div class="tourney-chart-head">
          <h3>🏆 ${isKo ? 'OWCS 명예의 전당: 최다 우승 & 결승 진출 Top 10' : 'OWCS Hall of Fame: Titles & Finalists Top 10'}</h3>
          <span style="font-size:11px;color:var(--text-muted);">${isKo ? '1위(우승) & 2위(준우승) 누적' : '1st & 2nd Place Records'}</span>
        </div>
        <div id="tourneyHallOfFameChart" style="width:100%;height:320px;"></div>
      </div>

      <div class="tourney-chart-panel">
        <div class="tourney-chart-head">
          <h3>📊 ${isKo ? '권역별 총상금 규모 및 대회 분포' : 'Prize Pool & Tournaments Distribution'}</h3>
          <span style="font-size:11px;color:var(--text-muted);">${isKo ? '누적 상금 비중 (%)' : 'Cumulative Share (%)'}</span>
        </div>
        <div id="tourneyPrizeDistributionChart" style="width:100%;height:320px;"></div>
      </div>
    </div>

    <!-- Filter Toolbar -->
    <div class="tourney-filter-bar">
      <div class="tourney-filter-row-top">
        <div class="tourney-year-tabs">
          ${yearTabsHtml}
        </div>

        <div class="tourney-search-wrap">
          <span class="tourney-search-icon">🔍</span>
          <input type="text" id="tourneySearchInput" class="tourney-search-input" placeholder="${isKo ? '대회명, 개최지, 챔피언, 참가팀 검색...' : 'Search tournament, venue, champion, team...'}" value="${state.tourneySearch}" />
        </div>

        <div class="tourney-view-toggle">
          <button class="tourney-view-btn ${state.tourneyView === 'grid' ? 'active' : ''}" data-view="grid">🗂️ ${isKo ? '카드 뷰' : 'Grid'}</button>
          <button class="tourney-view-btn ${state.tourneyView === 'timeline' ? 'active' : ''}" data-view="timeline">⏱️ ${isKo ? '타임라인' : 'Timeline'}</button>
        </div>
      </div>

      <div class="tourney-cat-chips">
        ${catChipsHtml}
      </div>
    </div>

    <!-- Results Status Line -->
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;font-size:13px;color:var(--text-muted);">
      <span>
        총 <b style="color:#fff;">${filtered.length}</b>개 대회가 표시되었습니다 
        ${totalPrizeFiltered > 0 ? `(표시 상금 합계: <b style="color:#4ade80;">$${totalPrizeFiltered.toLocaleString()}</b>)` : ''}
      </span>
      <span style="font-size:12px;">※ 팀명을 클릭하면 해당 팀의 상세 프로필 및 전장/밴 통계로 바로 이동합니다.</span>
    </div>

    <!-- Main Tournaments Listing -->
    ${contentHtml}
  `;
}

function bindTournamentsPage() {
  // 1. Year Buttons
  document.querySelectorAll('.tourney-year-btn').forEach(btn => {
    btn.onclick = () => {
      state.tourneyYear = btn.dataset.year;
      render();
    };
  });

  // 2. Category Chips
  document.querySelectorAll('.tourney-cat-chip').forEach(chip => {
    chip.onclick = () => {
      state.tourneyCat = chip.dataset.cat;
      render();
    };
  });

  // 3. View Mode Toggle
  document.querySelectorAll('.tourney-view-btn').forEach(btn => {
    btn.onclick = () => {
      state.tourneyView = btn.dataset.view;
      render();
    };
  });

  // 4. Real-time Search Input
  const searchInput = document.getElementById('tourneySearchInput');
  if (searchInput) {
    searchInput.oninput = (e) => {
      state.tourneySearch = e.target.value;
      clearTimeout(window._tourneySearchTimer);
      window._tourneySearchTimer = setTimeout(() => {
        render();
        const inp = document.getElementById('tourneySearchInput');
        if (inp) {
          inp.focus();
          inp.setSelectionRange(inp.value.length, inp.value.length);
        }
      }, 250);
    };
  }

  // 5. Team Jump Clicks
  document.querySelectorAll('[data-team-jump]').forEach(el => {
    el.onclick = (e) => {
      e.stopPropagation();
      const tid = el.dataset.teamJump;
      const tname = el.dataset.teamName;
      if (tid) {
        state.page = 'teams';
        state.team = tid;
        state.player = null;
        localStorage.setItem('owcs_stat_lab_page', 'teams');
        render();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } else if (tname) {
        showToast(`${tname} - ${state.lang === 'ko' ? '팀 상세 페이지가 곧 추가됩니다.' : 'Team profile coming soon.'}`);
      }
    };
  });

  // 6. Initialize ECharts Visualizations with layout breathing room
  setTimeout(() => {
    initTourneyCharts();
  }, 60);
}

function initTourneyCharts() {
  if (typeof echarts === 'undefined') return;

  const db = window.OWCS_TOURNAMENT_DATABASE;
  if (!db) return;

  const isKo = state.lang === 'ko';

  // --- Chart 1: Hall of Fame (Top 10 Teams Dual Stacked Horizontal Bar) ---
  const hofDom = document.getElementById('tourneyHallOfFameChart');
  if (hofDom) {
    if (currentHallOfFameChart) {
      currentHallOfFameChart.dispose();
    }
    const myHofChart = echarts.init(hofDom, 'dark', { renderer: 'canvas' });
    currentHallOfFameChart = myHofChart;

    const summary = db.summary || {};
    const topChamps = summary.topChampions || [];
    const podiumMap = {};
    (summary.topPodiums || []).forEach(p => { podiumMap[p.team] = p.finals; });
    const champMap = {};
    topChamps.forEach(c => { champMap[c.team] = c.titles; });
    
    const candidateTeams = [...new Set([...topChamps.map(x => x.team), ...(summary.topPodiums || []).map(x => x.team)])];
    const top10 = candidateTeams.map(t => ({
      name: t,
      c: champMap[t] || 0,
      r: Math.max(0, (podiumMap[t] || 0) - (champMap[t] || 0))
    })).sort((a,b) => (b.c - a.c) || ((b.c+b.r) - (a.c+a.r))).slice(0, 10).reverse();

    const optionHof = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: '#11141a',
        borderColor: '#2a303b',
        textStyle: { color: '#f4f6f8', fontSize: 12 },
        formatter: (params) => {
          const team = params[0].name;
          const gold = params[0].value;
          const silver = params[1].value;
          return `
            <div style="font-weight:800;margin-bottom:4px;color:#fff;">${team}</div>
            <div style="color:#fbbf24;">🥇 ${isKo ? '우승 (1위)' : '1st Place'}: <b>${gold}회</b></div>
            <div style="color:#cbd5e1;">🥈 ${isKo ? '준우승 (2위)' : '2nd Place'}: <b>${silver}회</b></div>
            <div style="color:var(--text-muted);margin-top:3px;border-top:1px dashed #333;padding-top:3px;">
              총 결승 진출: <b>${gold + silver}회</b>
            </div>
          `;
        }
      },
      legend: {
        data: [isKo ? '🥇 우승 (1위)' : '1st Place', isKo ? '🥈 준우승 (2위)' : '2nd Place'],
        bottom: 0,
        textStyle: { color: '#9ba5b3', fontSize: 11 }
      },
      grid: {
        left: '28%',
        right: '8%',
        top: '6%',
        bottom: '14%'
      },
      xAxis: {
        type: 'value',
        splitLine: { lineStyle: { color: '#1e2430', type: 'dashed' } },
        axisLabel: { color: '#9ba5b3', fontSize: 11 }
      },
      yAxis: {
        type: 'category',
        data: top10.map(t => t.name),
        axisLine: { lineStyle: { color: '#2a303b' } },
        axisLabel: { color: '#f4f6f8', fontSize: 11, fontWeight: 700 }
      },
      series: [
        {
          name: isKo ? '🥇 우승 (1위)' : '1st Place',
          type: 'bar',
          stack: 'total',
          data: top10.map(t => t.c),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#d97706' },
              { offset: 1, color: '#fbbf24' }
            ])
          }
        },
        {
          name: isKo ? '🥈 준우승 (2위)' : '2nd Place',
          type: 'bar',
          stack: 'total',
          data: top10.map(t => t.r),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#475569' },
              { offset: 1, color: '#94a3b8' }
            ]),
            borderRadius: [0, 6, 6, 0]
          }
        }
      ]
    };
    myHofChart.setOption(optionHof);
  }

  // --- Chart 2: Prize Money Distribution (Doughnut Chart) ---
  const prizeDom = document.getElementById('tourneyPrizeDistributionChart');
  if (prizeDom) {
    if (currentPrizeChart) {
      currentPrizeChart.dispose();
    }
    const myPrizeChart = echarts.init(prizeDom, 'dark', { renderer: 'canvas' });
    currentPrizeChart = myPrizeChart;

    const catMap = {
      'LAN': { name: isKo ? '글로벌 LAN 메이저' : 'Global LAN Events', color: '#ef4444', val: 0 },
      'NA': { name: isKo ? '북미 (NA)' : 'North America', color: '#3b82f6', val: 0 },
      'EMEA': { name: isKo ? '유럽·중동 (EMEA)' : 'EMEA', color: '#a855f7', val: 0 },
      'CN': { name: isKo ? '중국 (China)' : 'China', color: '#eab308', val: 0 },
      'KR': { name: isKo ? '한국 (Korea)' : 'Korea', color: '#38bdf8', val: 0 },
      'JP': { name: isKo ? '일본 (Japan)' : 'Japan', color: '#ec4899', val: 0 },
      'ASIA': { name: isKo ? '아시아 본선 ($155K)' : 'Asia Main ($155K)', color: '#f97316', val: 0 },
      'PA': { name: isKo ? '태평양 (Pacific)' : 'Pacific', color: '#10b981', val: 0 }
    };
    (db.tournaments || []).forEach(t => {
      const cat = t.isLAN ? 'LAN' : t.category;
      if (catMap[cat]) {
        catMap[cat].val += (t.prizeNum || 0);
      }
    });
    const prizeData = Object.values(catMap).map(c => ({
      name: c.name,
      value: c.val,
      itemStyle: { color: c.color }
    })).sort((a,b) => b.value - a.value);

    const optionPrize = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'item',
        backgroundColor: '#11141a',
        borderColor: '#2a303b',
        textStyle: { color: '#f4f6f8', fontSize: 12 },
        formatter: (params) => {
          const val = params.value;
          const pct = params.percent;
          return `
            <div style="font-weight:800;color:#fff;margin-bottom:4px;">${params.name}</div>
            <div style="color:#4ade80;">총 상금: <b>$${val.toLocaleString()} USD</b></div>
            <div style="color:var(--text-muted);font-size:11px;">전체 상금의 <b>${pct}%</b> 차지</div>
          `;
        }
      },
      legend: {
        type: 'scroll',
        orient: 'vertical',
        right: '2%',
        top: 'middle',
        textStyle: { color: '#9ba5b3', fontSize: 11 },
        pageTextStyle: { color: '#9ba5b3' }
      },
      series: [
        {
          name: isKo ? '상금 규모' : 'Prize Pool',
          type: 'pie',
          radius: ['42%', '72%'],
          center: ['34%', '50%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 6,
            borderColor: '#151820',
            borderWidth: 2
          },
          label: {
            show: false,
            position: 'center'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 13,
              fontWeight: 'bold',
              color: '#fff',
              formatter: '{b}\n{d}%'
            }
          },
          labelLine: { show: false },
          data: prizeData
        }
      ]
    };
    myPrizeChart.setOption(optionPrize);
  }
}

function rankingsPage(){
 const mode=state.rankMode==='acc'?'acc':'per10', role=state.rankRole;
 const cols=rankingColumns(role,mode);
 if(!cols.some(([k])=>k===state.rankMetric)){
   state.rankMetric=mode==='per10'?'Damage / 10':'TOTAL DAMAGE';
 }
 let rows=(mode==='per10'?D.per10Stats:D.totalStats).filter(r=>(r.Position||r.POSITION)===role);
 if(mode==='per10')rows=rows.filter(r=>r.Playtime_Min>=30);
 const metric=state.rankMetric, deathMetric=metric==='Death / 10'||metric==='TOTAL DEATHS';
 const defaultDir=deathMetric?'asc':'desc';
 const dir=state.rankSortDir||defaultDir;

 rows.sort((a,b)=>{
   const av=metric==='Playtime'? (mode==='per10'?+a.Playtime_Min:+a['TOTAL PLAYTIME']/60):+a[metric];
   const bv=metric==='Playtime'? (mode==='per10'?+b.Playtime_Min:+b['TOTAL PLAYTIME']/60):+b[metric];
   return dir==='asc'?av-bv:bv-av;
 });
 const sortMark=k=>state.rankMetric===k?(dir==='asc'?' ↑':' ↓'):'';
 return`<div class="page-title"><div><h1>${t('rank_title')}</h1>${mode==='per10'?'':`<p>${t('rank_sub_acc')}</p>`}</div></div>
 <div class="ranking-toolbar">
   <div class="ranking-role-tabs">${['TANK','MAIN DPS','FLEX DPS','MAIN SPT','FLEX SPT'].map(r=>`<button class="rank-role-tab ${r===role?'active':''}" data-rank-role="${r}">${roleName(r)}</button>`).join('')}</div>
   <div class="ranking-mode-toggle"><button class="${mode==='per10'?'active':''}" data-rank-mode="per10">${t('mode_per10')}</button><button class="${mode==='acc'?'active':''}" data-rank-mode="acc">${t('mode_acc')}</button></div>
 </div>
  ${mode==='per10'?`<div class="ranking-note"><span style="font-size:14px;flex-shrink:0">⚠️</span><span>${t('min_playtime_note')}</span></div>`:''}
 <div class="table-wrap rankings-table"><table><thead><tr>
   <th>${t('col_rank')}</th><th>${t('col_player')}</th><th>${t('col_team')}</th>
   <th class="sortable" data-rank-sort="Playtime">${t('col_playtime')}${sortMark('Playtime')}</th>
   ${cols.map(([k,l])=>`<th class="sortable ${state.rankMetric===k?'sorted':''}" data-rank-sort="${k}">${l}${sortMark(k)}</th>`).join('')}
 </tr></thead><tbody>${rows.map((r,i)=>{const pl=r.Player||r.PLAYER;const play=mode==='per10'?r.Playtime_Min:(r['TOTAL PLAYTIME']/60);return`<tr><td class="rank">${i+1}</td><td class="player-link" data-player="${pl}">${pl}</td><td>${r.Team||r.TEAM}</td><td>${fmt(play)} min</td>${cols.map(([k])=>`<td><strong>${fmt(r[k])}</strong></td>`).join('')}</tr>`}).join('')}</tbody></table></div>`;
}

function aggregatePhase(role,phase){const rows=D.rawStats.filter(r=>r.Position===role && (phase==='All'||D.matchInfo.find(m=>m.MATCH_ID===r.MATCH_ID)?.PHASE===phase));const g={};rows.forEach(r=>{let x=g[r.Player]??={Player:r.Player,Team:r.Team,Position:r.Position,sec:0,Elim:0,Death:0,Assists:0,Damage:0,Heal:0,Mitigated:0};x.sec+=+r['Playtime(Seconds)']||0;['Elim','Death','Assists','Damage','Heal','Mitigated'].forEach(k=>x[k]+=+r[k]||0)});return Object.values(g).map(x=>{let f=600/Math.max(1,x.sec);return{...x,Playtime_Min:x.sec/60,'Elim / 10':x.Elim*f,'Death / 10':x.Death*f,'Assists / 10':x.Assists*f,'Damage / 10':x.Damage*f,'Heal / 10':x.Heal*f,'Mitigated / 10':x.Mitigated*f}})}

function shortMetricName(m){return m.replace('Damage / 10','Damage').replace('Elim / 10','Elim').replace('Death / 10','Death').replace('Assists / 10','Assists').replace('Heal / 10','Heal').replace('Mitigated / 10','Mitigated')}
function median(vals){const a=[...vals].sort((x,y)=>x-y),n=a.length;if(!n)return null;return n%2?a[(n-1)/2]:(a[n/2-1]+a[n/2])/2}
function scatter(rows,xm,ym,highlight='All'){
 rows=rows.filter(r=>r.Playtime_Min>=30&&Number.isFinite(r[xm])&&Number.isFinite(r[ym]));
 if(!rows.length)return'<div class="note">No eligible players for this selection.</div>';
 const W=980,H=560,pad=68,xs=rows.map(r=>r[xm]),ys=rows.map(r=>r[ym]);
 const xmin=Math.min(...xs)*.95,xmax=Math.max(...xs)*1.05,ymin=Math.min(...ys)*.95,ymax=Math.max(...ys)*1.05;
 const X=v=>pad+(v-xmin)/(xmax-xmin||1)*(W-2*pad),Y=v=>H-pad-(v-ymin)/(ymax-ymin||1)*(H-2*pad);
 const xmed=median(xs),ymed=median(ys);
 let ticks='';
 for(let i=0;i<=5;i++){
   let xv=xmin+(xmax-xmin)*i/5,yv=ymin+(ymax-ymin)*i/5;
   ticks+=`<text class="tick" x="${X(xv)}" y="${H-pad+18}" text-anchor="middle">${fmt(xv)}</text><text class="tick" x="${pad-8}" y="${Y(yv)+3}" text-anchor="end">${fmt(yv)}</text>`;
 }
 const pts=rows.map(r=>{
   const hi=highlight!=='All'&&r.Player===highlight;
   const faded=highlight!=='All'&&!hi;
   return `<g class="plot-point-group ${hi?'highlighted':''} ${faded?'faded':''}">
      <circle class="point ${hi?'point-highlight':''}" data-plot-player="${r.Player}" cx="${X(r[xm])}" cy="${Y(r[ym])}" r="${hi?8:5}">
        <title>${r.Player} (${r.Team})
${xm}: ${fmt(r[xm])}
${ym}: ${fmt(r[ym])}
Playtime: ${fmt(r.Playtime_Min)} min</title>
      </circle>
      <text class="point-label ${hi?'label-highlight':''}" x="${X(r[xm])+8}" y="${Y(r[ym])-7}">${r.Player}</text>
   </g>`;
 }).join('');
 return`<div class="plot-summary"><span>${t('eligible_players')}: <b>${rows.length}</b></span><span>${t('median')} ${xm}: <b>${fmt(xmed)}</b></span><span>${t('median')} ${ym}: <b>${fmt(ymed)}</b></span></div>
 <div class="plot-wrap"><svg viewBox="0 0 ${W} ${H}">
   <line x1="${pad}" y1="${H-pad}" x2="${W-pad}" y2="${H-pad}" stroke="#46505c"/>
   <line x1="${pad}" y1="${pad}" x2="${pad}" y2="${H-pad}" stroke="#46505c"/>
   <line class="median-line" x1="${X(xmed)}" y1="${pad}" x2="${X(xmed)}" y2="${H-pad}"/>
   <line class="median-line" x1="${pad}" y1="${Y(ymed)}" x2="${W-pad}" y2="${Y(ymed)}"/>
   <text class="median-label" x="${Math.min(W-pad-8,X(xmed)+6)}" y="${pad+14}">Median ${shortMetricName(xm)}</text>
   <text class="median-label" x="${pad+6}" y="${Math.max(pad+30,Y(ymed)-7)}">Median ${shortMetricName(ym)}</text>
   ${ticks}${pts}
   <text class="axis-label" x="${W/2}" y="${H-10}" text-anchor="middle">${xm}</text>
   <text class="axis-label" transform="translate(15 ${H/2}) rotate(-90)" text-anchor="middle">${ym}</text>
 </svg>
 <div id="plotTooltip" class="plot-tooltip" hidden></div></div>`;
}

function plottingPage(){
 const metrics=['Elim / 10','Death / 10','Assists / 10','Damage / 10','Heal / 10','Mitigated / 10'];
 const rows=aggregatePhase(state.plotRole,state.plotPhase);
 const eligible=rows.filter(r=>r.Playtime_Min>=30&&Number.isFinite(r[state.plotX])&&Number.isFinite(r[state.plotY]));
 const names=eligible.map(r=>r.Player).sort();
 if(state.plotHighlight!=='All'&&!names.includes(state.plotHighlight))state.plotHighlight='All';
 return`<div class="page-title"><div><h1>${t('plot_title')}</h1><p>${t('plot_subtitle')}</p></div></div>
 <div class="controls">
   <div class="control"><label>${t('lbl_position')}</label><select id="plotRole">${['TANK','MAIN DPS','FLEX DPS','MAIN SPT','FLEX SPT'].map(x=>`<option ${x===state.plotRole?'selected':''}>${x}</option>`).join('')}</select></div>
   <div class="control"><label>${t('lbl_x_metric')}</label><select id="plotX">${metrics.map(x=>`<option ${x===state.plotX?'selected':''}>${x}</option>`).join('')}</select></div>
   <div class="control"><label>${t('lbl_y_metric')}</label><select id="plotY">${metrics.map(x=>`<option ${x===state.plotY?'selected':''}>${x}</option>`).join('')}</select></div>
   <div class="control"><label>${t('lbl_phase')}</label><select id="plotPhase">${phases.map(x=>`<option ${x===state.plotPhase?'selected':''}>${x}</option>`).join('')}</select></div>
   <div class="control"><label>${t('lbl_highlight')}</label><select id="plotHighlight"><option>All</option>${names.map(x=>`<option ${x===state.plotHighlight?'selected':''}>${x}</option>`).join('')}</select></div>
 </div>
 ${scatter(rows,state.plotX,state.plotY,state.plotHighlight)}`;
}

function playerMapRecord(name){
 const rows=D.rawStats.filter(r=>r.Player===name), seen=new Map();
 rows.forEach(r=>{const key=`${r.MATCH_ID}-${r.Map||r.MAP||''}`;if(!seen.has(key))seen.set(key,r)});
 let w=0,l=0;
 seen.forEach(r=>{const mi=D.matchInfo.find(x=>x.MATCH_ID===r.MATCH_ID&&x.MAP===(r.Map||r.MAP));if(mi){if(mi.WINNER===r.Team)w++;else l++}});
 return{played:seen.size,w,l,rate:(w+l)?Math.round(w/(w+l)*1000)/10:null}
}

function pctSlider(q){return q==null?`<div class="pct-slider unavailable"><span>N/A</span></div>`:`<div class="pct-slider"><i style="left:${q}%"></i><span style="left:${q}%">${q}</span></div>`}

function h2hPage(){
  const roles=['TANK','MAIN DPS','FLEX DPS','MAIN SPT','FLEX SPT'];
  const opts=players.filter(p=>per10[p]?.Position===state.h2hRole).sort();
  if(!opts.includes(state.h2hA))state.h2hA=opts[0]||null;
  if(!opts.includes(state.h2hB)||state.h2hB===state.h2hA)state.h2hB=opts.find(x=>x!==state.h2hA)||opts[0]||null;
  const A=per10[state.h2hA],B=per10[state.h2hB];
  const metrics=roleMetrics(state.h2hRole);
  const sampleA=A?.Playtime_Min>=30,sampleB=B?.Playtime_Min>=30;
  const ra=A?playerMapRecord(A.Player):null,rb=B?playerMapRecord(B.Player):null;
  return`<div class="page-title"><div><h1>${t('h2h_title')}</h1><p>${t('h2h_subtitle')}</p></div></div>
  <div class="profile-header-actions"><button class="btn-export" id="btnExportH2H"><span class="btn-export-icon">📸</span> ${t('h2h_export')}</button></div>
  <div class="controls"><div class="control"><label>${t('lbl_position')}</label><select id="h2hRole">${roles.map(x=>`<option ${x===state.h2hRole?'selected':''}>${x}</option>`).join('')}</select></div><div class="control"><label>Player A</label><select id="h2hA">${opts.map(x=>`<option ${x===state.h2hA?'selected':''}>${x}</option>`).join('')}</select></div><div class="control"><label>Player B</label><select id="h2hB">${opts.map(x=>`<option ${x===state.h2hB?'selected':''}>${x}</option>`).join('')}</select></div></div>
  <div id="h2h-export-target" class="export-target">
  ${!A||!B?'<div class="note">Not enough player data for this position.</div>':`<div class="h2h"><div class="h2h-player"><div class="muted">${A.Team} · ${roleName(A.Position)}</div><h2>${A.Player}</h2><div class="h2h-meta"><span><b>${fmt(A.Playtime_Min)}</b> min</span><span><b>${ra.played}</b> maps</span><span><b>${ra.w}-${ra.l}</b> ${t('map_record')}</span><span><b>${ra.rate==null?'—':ra.rate+'%'}</b> ${t('map_win_rate')}</span></div>${sampleA?'':`<div class="sample-warning">${t('sample_warning')}</div>`}</div><div class="vs">VS</div><div class="h2h-player"><div class="muted">${B.Team} · ${roleName(B.Position)}</div><h2>${B.Player}</h2><div class="h2h-meta"><span><b>${fmt(B.Playtime_Min)}</b> min</span><span><b>${rb.played}</b> maps</span><span><b>${rb.w}-${rb.l}</b> ${t('map_record')}</span><span><b>${rb.rate==null?'—':rb.rate+'%'}</b> ${t('map_win_rate')}</span></div>${sampleB?'':`<div class="sample-warning">${t('sample_warning')}</div>`}</div></div>
  <div class="radar-chart-container">
    <div class="radar-chart-header">
      <div class="radar-chart-title">${t('h2h_radar_title')}</div>
      <div class="muted" style="font-size:12px"><span style="color:#ff6b2c;font-weight:700">■ ${A.Player}</span> vs <span style="color:#68a8ff;font-weight:700">■ ${B.Player}</span></div>
    </div>
    <div id="h2h-radar-canvas" class="h2h-radar-canvas"></div>
  </div>
  <div class="card compare">${metrics.map(m=>{const pa=percentile(A.Player,m),pb=percentile(B.Player,m);return`<div class="compare-row slider-row"><div class="slider-side left"><strong>${fmt(A[m])}</strong>${pctSlider(pa)}</div><div class="compare-metric"><span>${m}</span><small>Per 10</small></div><div class="slider-side right"><strong>${fmt(B[m])}</strong>${pctSlider(pb)}</div></div>`}).join('')}</div>
  <p class="muted h2h-footnote">${t('h2h_footnote')}</p>`}
  <div class="export-watermark">OWCS Korea 2026 Stage 2 · Stat Lab</div>
  </div>`;
}

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

function phaseRows(phase='All', tData) {
  const td = tData || getActiveTourneyData();
  if (!td || !td.mapRows) return [];
  const pNorm = String(phase || 'All').toLowerCase();
  return td.mapRows.filter(r => pNorm === 'all' || String(r.PHASE || '').toLowerCase() === pNorm);
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

function banCounts(phase='All', team='All', mode='by', breakMode='Overall', breakValue='All', tData) {
  const td = tData || getActiveTourneyData();
  const rows = banFilterRows(phase, breakMode, breakValue, td);
  const arr = [];
  rows.forEach(r => {
    if (mode === 'by' || !mode) {
      if (team === 'All' || !team || r['TEAM 1'] === team) arr.push(r['TEAM 1 BAN']);
      if (team === 'All' || !team || r['TEAM 2'] === team) arr.push(r['TEAM 2 BAN']);
    } else if (team !== 'All' && team) {
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

function stage3PreviewPage(){
  const s3 = window.OWCS_STAGE3_PREVIEW || {};
  const tour = s3.tournament || {};
  const isKo = state.lang === 'ko';
  const tourName = isKo ? tour.nameKo : tour.name;
  const tourDesc = isKo ? tour.format?.ko : tour.format?.en;

  const transfers = s3.transfers || { in: [], out: [] };
  const inList = transfers.in || [];
  const outList = transfers.out || [];
  const newTeam = s3.newTeam || {};

  const scheduleData = s3.schedule || [];
  const teamLookup = s3.teamLookup || {};

  // Schedule filtering state
  const curWeek = state.s3Week || 'all';
  const curTeam = state.s3TeamFilter || 'ALL';

  const allTeams = ['ALL', 'CR', 'FLC', 'T1', 'ZETA', 'PF', 'CB', 'ROZE', 'O2', 'SEJ'];

  const teamFilterChipsHtml = allTeams.map(tm => {
    const isAct = curTeam === tm;
    const label = tm === 'ALL' ? (isKo ? '전체 팀' : 'All Teams') : tm;
    return `<button class="chip s3-filter-chip ${isAct ? 'active' : ''}" data-s3-team="${tm}">
      ${tm !== 'ALL' ? teamLogo(tm, 's3-chip-logo') : ''}
      <span>${label}</span>
    </button>`;
  }).join('');

  const weekTabs = [
    { id: 'all', ko: '전체 일정 (4주 36경기)', en: 'All Matches (4 Weeks)' },
    { id: '1', ko: '1주차 (10.02 - 10.04)', en: 'Week 1 (10.02 - 10.04)' },
    { id: '2', ko: '2주차 (10.09 - 10.11)', en: 'Week 2 (10.09 - 10.11)' },
    { id: '3', ko: '3주차 (10.16 - 10.18)', en: 'Week 3 (10.16 - 10.18)' },
    { id: '4', ko: '4주차 (10.23 - 10.25)', en: 'Week 4 (10.23 - 10.25)' }
  ];

  const weekTabsHtml = weekTabs.map(w => `
    <button class="tabbtn s3-week-tab ${curWeek === w.id ? 'active' : ''}" data-s3-week="${w.id}">
      ${isKo ? w.ko : w.en}
    </button>
  `).join('');

  const weeksToDisplay = curWeek === 'all' 
    ? scheduleData 
    : scheduleData.filter(w => String(w.week) === String(curWeek));

  const scheduleHtml = weeksToDisplay.map(w => {
    const weekTitle = isKo ? w.titleKo : w.titleEn;
    
    const daysHtml = w.days.map(d => {
      const dayDate = isKo ? d.dateKo : d.dateEn;
      
      const matchesHtml = d.matches.map(m => {
        const homeTeam = teamLookup[m.home] || { name: m.home, short: m.home };
        const awayTeam = teamLookup[m.away] || { name: m.away, short: m.away };
        
        const isMatchTarget = curTeam === 'ALL' || m.home === curTeam || m.away === curTeam;
        const isDimmed = !isMatchTarget;
        const isHighlighted = curTeam !== 'ALL' && isMatchTarget;

        return `
          <div class="s3-match-row ${m.isBigMatch ? 'big-match' : ''} ${isDimmed ? 'dimmed' : ''} ${isHighlighted ? 'highlighted' : ''}">
            <div class="s3-match-meta">
              <span class="s3-match-num">M${m.matchNum}</span>
              ${m.isBigMatch ? '<span class="s3-big-badge" title="빅매치">🔥 BIG MATCH</span>' : ''}
            </div>
            
            <div class="s3-match-body">
              <div class="s3-match-team home" title="${homeTeam.name}">
                <div class="s3-team-text">
                  <strong class="s3-team-abbr">${m.home}</strong>
                  <span class="s3-team-fullname">${homeTeam.name}</span>
                </div>
                ${teamLogo(m.home, 's3-match-logo')}
              </div>

              <div class="s3-match-vs">
                <span>VS</span>
              </div>

              <div class="s3-match-team away" title="${awayTeam.name}">
                ${teamLogo(m.away, 's3-match-logo')}
                <div class="s3-team-text">
                  <strong class="s3-team-abbr">${m.away}</strong>
                  <span class="s3-team-fullname">${awayTeam.name}</span>
                </div>
              </div>
            </div>
          </div>
        `;
      }).join('');

      return `
        <div class="s3-day-card">
          <div class="s3-day-head">
            <div class="s3-day-title-wrap">
              <span class="s3-day-badge">DAY ${d.day}</span>
              <span class="s3-day-date">${dayDate}</span>
            </div>
            <span class="s3-day-time">⏰ ${d.time} KST</span>
          </div>
          <div class="s3-matches-container">
            ${matchesHtml}
          </div>
        </div>
      `;
    }).join('');

    return `
      <div class="s3-week-block">
        <div class="s3-week-header">
          <div style="display:flex;align-items:center;gap:12px;">
            <span class="s3-week-indicator"></span>
            <h3 class="s3-week-title">${weekTitle}</h3>
            <span class="s3-week-dates">${w.dateRange}</span>
          </div>
          <span class="s3-week-matchcount">${isKo ? '9경기 진행' : '9 Matches'}</span>
        </div>
        <div class="s3-days-grid">
          ${daysHtml}
        </div>
      </div>
    `;
  }).join('');

  const mapPoolData = s3.mapPool || {};
  const curTab = state.s3Tab || 'schedule';
  const curMapFilter = state.s3MapTypeFilter || 'ALL';

  const s3Tabs = [
    { id: 'schedule', icon: '📅', ko: '경기 일정', en: 'Schedule' },
    { id: 'mappool', icon: '🗺️', ko: '공식 맵 풀', en: 'Map Pool' },
    { id: 'transfers', icon: '🔄', ko: '선수단 변동', en: 'Transfers' },
    { id: 'teams', icon: '👥', ko: '참가팀 로스터', en: 'Teams' },
    { id: 'all', icon: '📑', ko: '전체 보기', en: 'View All' }
  ];

  const s3NavTabsHtml = s3Tabs.map(t => `
    <button class="tabbtn s3-nav-tab ${curTab === t.id ? 'active' : ''}" data-s3-tab="${t.id}">
      <span>${t.icon}</span>
      <b>${isKo ? t.ko : t.en}</b>
    </button>
  `).join('');

  // Map Pool Rendering
  const mapTypes = ['ALL', 'Control', 'Hybrid', 'Escort', 'Push', 'Flashpoint'];
  const mapFilterChipsHtml = mapTypes.map(mType => {
    const isAct = curMapFilter === mType;
    let label = mType;
    if (mType === 'ALL') label = isKo ? '전체 전장 (14개)' : 'All Maps (14)';
    else if (mapPoolData[mType]) {
      const info = mapPoolData[mType];
      label = `${info.icon} ${isKo ? info.nameKo : info.nameEn} (${info.maps.length})`;
    }
    return `<button class="chip s3-map-chip ${isAct ? 'active' : ''}" data-s3-maptype="${mType}">
      <span>${label}</span>
    </button>`;
  }).join('');

  const typesToRender = curMapFilter === 'ALL'
    ? Object.keys(mapPoolData)
    : [curMapFilter].filter(k => mapPoolData[k]);

  const mapPoolBlocksHtml = typesToRender.map(typeKey => {
    const pool = mapPoolData[typeKey];
    if (!pool) return '';

    const mapsCardsHtml = pool.maps.map(m => {
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
            <span class="s3-map-count-badge">${pool.maps.length}${isKo ? '개 전장' : ' Maps'}</span>
          </div>
        </div>
        <div class="s3-maps-grid">
          ${mapsCardsHtml}
        </div>
      </div>
    `;
  }).join('');

  const mapPoolSectionHtml = `
    <div class="s3-mappool-section" id="s3-mappool">
      <div class="page-title" style="margin-bottom:14px;">
        <div>
          <h2>${isKo ? '공식 전장 맵 풀 (Stage 3 Map Pool)' : 'Stage 3 Official Map Pool'}</h2>
          <p class="muted" style="margin:4px 0 0;">${isKo ? 'OWCS Korea 2026 Stage 3 공식 채택 5개 전장 모드 · 총 14개 전장' : 'Official 14 competitive maps across 5 game modes'}</p>
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

  const inTeamsHtml = inList.map(item => `
    <div class="transfer-team-card">
      <div class="transfer-team-head">
        ${teamLogo(item.short, 'transfer-team-logo')}
        <span>${item.team} (${item.short})</span>
      </div>
      <div class="transfer-pills-wrap">
        ${item.items.map(p => `<span class="transfer-pill in">+ ${p.name}</span>`).join('')}
      </div>
    </div>
  `).join('');

  const outTeamsHtml = outList.map(item => `
    <div class="transfer-team-card">
      <div class="transfer-team-head">
        ${teamLogo(item.short, 'transfer-team-logo')}
        <span>${item.team} (${item.short})</span>
      </div>
      <div class="transfer-pills-wrap">
        ${item.items.map(p => `<span class="transfer-pill out">− ${p.name}</span>`).join('')}
      </div>
    </div>
  `).join('');

  const newTeamHtml = newTeam.name ? `
    <div class="new-team-spotlight">
      <div class="spotlight-head">
        <div class="spotlight-title-wrap">
          <span class="spotlight-badge">NEW TEAM</span>
          <h3 class="spotlight-title">${newTeam.name} <span class="muted" style="font-size:14px;font-weight:400">(${newTeam.short})</span></h3>
        </div>
      </div>
      <div class="spotlight-roster-grid">
        <div class="spotlight-role-card">
          <span class="spotlight-role-title tank">TANK</span>
          <div class="spotlight-players-list">
            ${(newTeam.roster||[]).filter(p=>p.role==='TANK').map(p=>`<span class="spotlight-player-pill">${p.name}</span>`).join('')}
          </div>
        </div>
        <div class="spotlight-role-card">
          <span class="spotlight-role-title dps">DPS</span>
          <div class="spotlight-players-list">
            ${(newTeam.roster||[]).filter(p=>p.role==='DPS').map(p=>`<span class="spotlight-player-pill">${p.name}</span>`).join('')}
          </div>
        </div>
        <div class="spotlight-role-card">
          <span class="spotlight-role-title spt">SUPPORT</span>
          <div class="spotlight-players-list">
            ${(newTeam.roster||[]).filter(p=>p.role==='SPT').map(p=>`<span class="spotlight-player-pill">${p.name}</span>`).join('')}
          </div>
        </div>
      </div>
    </div>
  ` : '';

  const teamsHtml = (s3.teams || []).map(tm => {
    const isZeta = tm.short === 'ZETA';
    const seedBadge = isZeta ? `
      <span class="stage3-seed-badge" style="background:linear-gradient(135deg, rgba(251,191,36,0.18) 0%, rgba(217,119,6,0.28) 100%);color:#fbbf24;border:1px solid rgba(251,191,36,0.5);font-weight:800;">
        🏆 ${isKo ? '디펜딩 챔피언' : 'Defending Champion'}
      </span>
    ` : '';
    const rosterItems = (tm.roster || []).map(p => `
      <div class="stage3-roster-item">
        <span style="display:inline-flex;align-items:center;">
          <b style="color:var(--text);">${p.name}</b>
          ${p.isNew ? `<span class="stage3-new-tag">NEW</span>` : ''}
        </span>
        <span class="stage3-role-tag ${p.role.toLowerCase()}">${p.role}</span>
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
          ${seedBadge}
        </div>
        <div class="stage3-roster-list">
          ${rosterItems}
        </div>
      </div>
    `;
  }).join('');

  const showSchedule = curTab === 'schedule' || curTab === 'all';
  const showMapPool = curTab === 'mappool' || curTab === 'all';
  const showTransfers = curTab === 'transfers' || curTab === 'all';
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
          <span class="stage3-dday-badge">
            <span class="opt-status-dot upcoming" style="background:#111;"></span>
            ${t('stage3_dday_badge')}
          </span>
        </div>
        <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
          <span class="stage3-dates">2026.10.02 ~ 2026.11.08</span>
          <button class="chip" id="btnGoStage2">${t('stage3_switch_back_btn')}</button>
        </div>
      </div>
      <h1 class="stage3-title">${tourName}</h1>
      <div class="stage3-meta-pills" style="margin-top:12px;">
        <span class="stage3-pill tier">💎 <b>${isKo ? 'A-TIER 대회' : 'A-TIER Tournament'}</b></span>
        <span class="stage3-pill prize">💰 <b>${isKo ? '총 상금 $38,500' : 'Total Prize $38,500'}</b></span>
      </div>
    </div>

    <!-- Stage 3 Navigation Sub-tabs -->
    <div class="s3-main-nav-bar">
      ${s3NavTabsHtml}
    </div>

    ${showSchedule ? `
      <!-- Regular Season Match Schedule Section -->
      <div class="s3-schedule-section">
        <div class="s3-schedule-topbar">
          <div>
            <div style="display:flex;align-items:center;gap:8px;">
              <span class="s3-schedule-live-dot"></span>
              <h2 class="s3-schedule-heading">${isKo ? '정규 시즌 경기 일정 (Match Schedule)' : 'Regular Season Match Schedule'}</h2>
            </div>
            <p class="muted" style="margin:4px 0 0;font-size:13px;">
              ${isKo ? '10.02(금) ~ 10.25(일) · 총 4주간 36경기 풀 라운드 로빈 · 금 17:00 / 토·일 15:00 KST' : 'Oct 02 - Oct 25 · 4 Weeks 36 Matches Full Round Robin · Fri 17:00 / Sat·Sun 15:00 KST'}
            </p>
          </div>
          <div class="s3-broadcast-box">
            <span class="s3-broadcast-label">🔴 ${isKo ? '공식 생중계' : 'Official Streams'}</span>
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
            <span class="s3-filter-label">${isKo ? '팀별 일정 필터:' : 'Filter by Team:'}</span>
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

    ${showTransfers ? `
      <div class="roster-changes-section">
        <div class="page-title" style="margin-bottom:12px;">
          <div>
            <h2>${isKo ? '오프시즌 선수단 변동 (IN / OUT)' : 'Offseason Transfers (IN / OUT)'}</h2>
            <p class="muted" style="margin:4px 0 0;">${isKo ? 'Stage 3 개막 전 공식 영입(IN) 및 계약 종료(OUT) 현황' : 'Official signings (IN) and departures (OUT) ahead of Stage 3'}</p>
          </div>
        </div>
        <div class="in-out-transfer-board">
          <div class="transfer-column in-col">
            <div class="transfer-column-head in">
              <span class="transfer-dot in"></span>
              <h3>IN (${isKo ? '영입' : 'Signings'})</h3>
            </div>
            <div class="transfer-team-list">
              ${inTeamsHtml}
            </div>
          </div>
          <div class="transfer-column out-col">
            <div class="transfer-column-head out">
              <span class="transfer-dot out"></span>
              <h3>OUT (${isKo ? '계약 종료 / 이적' : 'Departures & Releases'})</h3>
            </div>
            <div class="transfer-team-list">
              ${outTeamsHtml}
            </div>
          </div>
        </div>
        ${newTeamHtml}
      </div>
    ` : ''}

    ${showTeams ? `
      <div class="section" style="margin-bottom:24px;">
        <div class="page-title" style="margin-bottom:12px;">
          <div>
            <h2>${t('stage3_teams_title')}</h2>
            <p class="muted" style="margin:4px 0 0;">${isKo ? 'Stage 3 참가 9개 구단 확정 로스터' : 'Official 9-team Stage 3 rosters'}</p>
          </div>
        </div>
        <div class="stage3-teams-grid">
          ${teamsHtml}
        </div>
      </div>
    ` : ''}

    <div class="stage3-notice-card">
      <span class="stage3-notice-icon">📢</span>
      <div>
        <strong style="color:#ffc107;display:block;margin-bottom:2px;">${isKo ? '스테이지 3 데이터 수집 안내' : 'Stage 3 Data Collection Notice'}</strong>
        <span>${t('stage3_notice_text')}</span>
      </div>
    </div>
  `;
}



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

// Find Match object across all tournaments
function findMatchObject(keyOrId, tourney) {
  const currentOrSpecifiedTourney = tourney || (typeof state !== 'undefined' ? state.tourney : 'kr-s2');
  const targetDs = getTourneyDataset(currentOrSpecifiedTourney);
  if (targetDs && targetDs.matches) {
    const normKey = String(keyOrId).toLowerCase().replace(/[^a-z0-9]/g, '');
    let found = targetDs.matches.find(m => {
      if (!m) return false;
      if (m.matchId === keyOrId || m.key === keyOrId) return true;
      const nmId = String(m.matchId || '').toLowerCase().replace(/[^a-z0-9]/g, '');
      const nmKey = String(m.key || '').toLowerCase().replace(/[^a-z0-9]/g, '');
      return nmId === normKey || nmKey === normKey || (normKey.length >= 3 && (nmId.endsWith(normKey) || normKey.endsWith(nmId)));
    });
    if (found) return found;
  }

  // Universal lookup across all new datasets
  const allDatasets = [
    window.OWCS_STAGE1_PREVIEW,
    window.OWCS_ASIA_S1_PREVIEW,
    window.OWCS_BOOTCAMP_PREVIEW,
    window.OWCS_CLASH_PREVIEW,
    window.OWCS_MIDSEASON_PREVIEW,
    window.OWCS_OWWC_PREVIEW,
    window.OWCS_STAGE2_PREVIEW
  ];
  const normKeyAll = String(keyOrId).toLowerCase().replace(/[^a-z0-9]/g, '');
  for (const ds of allDatasets) {
    if (!ds || !ds.matches) continue;
    let found = ds.matches.find(m => {
      if (!m) return false;
      if (m.matchId === keyOrId || m.key === keyOrId) return true;
      const nmId = String(m.matchId || '').toLowerCase().replace(/[^a-z0-9]/g, '');
      const nmKey = String(m.key || '').toLowerCase().replace(/[^a-z0-9]/g, '');
      return nmId === normKeyAll || nmKey === normKeyAll || (normKeyAll.length >= 3 && (nmId.endsWith(normKeyAll) || normKeyAll.endsWith(nmId)));
    });
    if (found) return found;
  }
  const isS1 = tourney === 'kr-s1' || String(keyOrId).startsWith('S1_') || String(keyOrId).startsWith('kr26-s1');
  if (isS1) {
    const s1List = (window.OWCS_STAGE1_PREVIEW && window.OWCS_STAGE1_PREVIEW.matches) || [];
    let found = s1List.find(m => m.matchId === keyOrId || `${m.phase}_${m.matchNumber}` === keyOrId || m.matchId === String(keyOrId).replace(/^kr26-s1-/, ''));
    if (found) return found;

    if (typeof getStage1Dataset === 'function') {
      const ds1 = getStage1Dataset();
      const mAdapted = ds1.matches.find(m => m.key === keyOrId || m.matchId === keyOrId);
      if (mAdapted) {
        return {
          matchId: mAdapted.key,
          phase: mAdapted.phase,
          week: mAdapted.week,
          day: mAdapted.day,
          team1: mAdapted.a,
          team2: mAdapted.b,
          score1: mAdapted.aw,
          score2: mAdapted.bw,
          winner: mAdapted.winner,
          mvp: mAdapted.mvp || '',
          date: mAdapted.date || '',
          casters: mAdapted.casters || [],
          vod: mAdapted.vod || '',
          sets: (mAdapted.maps || []).map((x, idx) => ({
            setNumber: idx + 1,
            map: x.MAP,
            mode: x['MAP TYPE'],
            detailScore: x.DETAIL_SCORE || (x['TEAM 1 SCORE'] ? `${x['TEAM 1 SCORE']} : ${x['TEAM 2 SCORE']}` : ''),
            winner: x.WINNER,
            team1Ban: x['TEAM 1 BAN'] || '',
            team2Ban: x['TEAM 2 BAN'] || ''
          }))
        };
      }
    }
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
      mvp: localM.mvp || '',
      date: localM.date || '',
      casters: localM.casters || [],
      vod: localM.vod || '',
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
  const activeTourKey = tourney || state.tourney;
  const tourDataset = getTourneyDataset(activeTourKey);
  const tourName = tourDataset?.tournament 
    ? (isKo ? (tourDataset.tournament.nameKo || tourDataset.tournament.name) : tourDataset.tournament.name)
    : (activeTourKey === 'kr-s1' 
        ? (isKo ? 'OWCS 코리아 2026 Stage 1' : 'OWCS Korea 2026 Stage 1')
        : (isKo ? 'OWCS 코리아 2026 Stage 2' : 'OWCS Korea 2026 Stage 2'));

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
  const allTourneyMatches = (tourDataset && tourDataset.matches) 
    ? tourDataset.matches 
    : (activeTourKey === 'kr-s1' 
        ? ((window.OWCS_STAGE1_PREVIEW && window.OWCS_STAGE1_PREVIEW.matches) || [])
        : (window.OWCS_STAGE2_MATCHES || []));

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

  const t1Name = tourDataset?.teamNames?.[t1] || teamNames[t1] || (window.OWCS_STAGE1_PREVIEW?.teamNames?.[t1]) || t1;
  const t2Name = tourDataset?.teamNames?.[t2] || teamNames[t2] || (window.OWCS_STAGE1_PREVIEW?.teamNames?.[t2]) || t2;

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

// Bind clicks on match rows and cells to open Match Detail Modal
function bindMatchModalEvents() {
  const matchSelector = '.s2-match-row, .s1-match-row, .rr-cell[data-match], .match-main[data-match], .history-item[data-match-id]';
  document.querySelectorAll(matchSelector).forEach(el => {
    el.onclick = (e) => {
      // Don't hijack if user clicked an explicit link or stream button
      if (e.target.tagName === 'A' || e.target.closest('a')) return;
      e.stopPropagation();
      const matchId = el.dataset.matchId || el.dataset.matchKey || el.dataset.match;
      const tourney = el.dataset.tourney || (state.tourney || 'kr-s2');
      if (matchId) {
        openMatchDetailModal(matchId, tourney);
      }
    };
  });
}


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
  const showStandings = curTab === 'standings' || curTab === 'all';
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
              <div class="rr-cell ${rw > rl ? 'win' : 'loss'}" data-match-id="${m.key}" data-match="${m.key}" data-tourney="kr-s1" title="${row} vs ${col} (${rw}:${rl}) - 클릭하여 세부 스코어 및 밴픽 보기" style="cursor:pointer;">
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
              <button class="match-main" data-match-id="${m.key}" data-match="${m.key}" data-tourney="kr-s1" title="클릭하여 세부 스코어 및 밴픽 보기">
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


function stage2PreviewPage(){
  const s2 = window.OWCS_STAGE2_PREVIEW || {};
  const tour = s2.tournament || {};
  const isKo = state.lang === 'ko';
  const curTab = state.s2Tab || 'schedule';
  const curWeek = state.s2Week || 'all';
  const curTeam = state.s2TeamFilter || 'ALL';
  const curMapPhase = state.s2MapPhase || 'regular';
  const curMapType = state.s2MapTypeFilter || 'ALL';

  const tourName = isKo ? (tour.nameKo || tour.name) : tour.name;

  // Sub-tabs
  const s2NavTabs = [
    { id: 'schedule', icon: '📅', ko: '경기 일정', en: 'Schedule' },
    { id: 'standings', icon: '🏆', ko: '정규 순위표', en: 'Standings' },
    { id: 'mappool', icon: '🗺️', ko: '공식 맵 풀', en: 'Map Pool' },
    { id: 'transfers', icon: '🔄', ko: '선수단 변동', en: 'Transfers' },
    { id: 'teams', icon: '👥', ko: '참가팀 로스터', en: 'Teams' },
    { id: 'all', icon: '📑', ko: '전체 보기', en: 'View All' }
  ];
  const s2NavTabsHtml = s2NavTabs.map(t => `
    <button class="tabbtn s3-nav-tab ${curTab === t.id ? 'active' : ''}" data-s2-tab="${t.id}">
      <span>${t.icon}</span>
      <b>${isKo ? t.ko : t.en}</b>
    </button>
  `).join('');

  // 0. Regular Season Standings Data & Rendering
  const standingsRowsHtml = standings.map(s => {
    const isTop4 = s.rank <= 4;
    const isLcq = s.rank >= 5 && s.rank <= 8;
    const isElim = s.rank === 9;
    
    const tierClass = isTop4 ? 'tier-rr2' : (isLcq ? 'tier-lcq' : 'tier-elim');
    const statusClass = isTop4 ? 'status-green' : (isLcq ? 'status-yellow' : 'status-red');
    const statusText = isTop4 ? 'Advanced to 2nd RR' : (isLcq ? 'Advanced to LCQ' : 'Eliminated');

    const diff = s.mapw - s.mapl;
    const diffText = diff > 0 ? `+${diff}` : String(diff);
    const diffClass = diff > 0 ? 'pos' : (diff < 0 ? 'neg' : 'zero');
    const winRate = Math.round((s.mw / (s.mw + s.ml || 1)) * 100);
    const tmName = teamNames[s.team] || s.team;

    return `
      <tr class="s2-standing-row ${tierClass}" data-s2-team="${s.team}" title="${tmName} (${s.team})">
        <td class="col-rank" style="text-align:center;">
          <span class="rank-num ${statusClass}">${s.rank}</span>
        </td>
        <td class="col-team">
          <div class="team-cell">
            ${teamLogo(s.team, 's2-standing-team-logo')}
            <div class="team-names">
              <strong class="team-abbr">${s.team}</strong>
              <span class="team-full">${tmName}</span>
            </div>
          </div>
        </td>
        <td class="col-series" style="text-align:center;">
          <b style="color:#fff;">${s.mw}W - ${s.ml}L</b>
        </td>
        <td class="col-winrate" style="text-align:center;">
          <span class="s2-winrate-tag">${winRate}%</span>
        </td>
        <td class="col-maps" style="text-align:center;">
          <span>${s.mapw}W - ${s.mapl}L</span>
        </td>
        <td class="col-diff" style="text-align:center;">
          <b class="s2-diff-tag ${diffClass}">${diffText}</b>
        </td>
        <td class="col-status" style="text-align:center;">
          <span class="s2-outcome-badge ${statusClass}">${statusText}</span>
        </td>
      </tr>
    `;
  }).join('');

  const standingsSectionHtml = `
    <div class="s2-standings-card" id="s2-standings">
      <div class="s2-standings-header">
        <div style="display:flex;align-items:center;gap:12px;">
          <span class="s2-standings-icon">🏆</span>
          <div>
            <h3 class="s2-standings-title" style="margin:0;font-size:16.5px;font-weight:800;color:#fff;">
              ${isKo ? 'Stage 2 정규 시즌 최종 순위표' : 'Stage 2 Regular Season Final Standings'}
            </h3>
            <p class="s2-standings-sub muted" style="margin:3px 0 0;font-size:12px;">
              ${isKo ? '총 36경기 풀 라운드 로빈 결과 · 승자승(H2H) 동률 규정 적용' : '36 Regular Season Matches · Head-to-Head Tiebreakers Applied'}
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

  // 1. Schedule Data & Rendering
  const allS2Matches = matches || [];
  const s2TeamsList = ['ALL', 'CR', 'FLC', 'ZETA', 'T1', 'ROZE', 'CB', 'O2', 'PF'];
  
  const teamFilterChipsHtml = s2TeamsList.map(tm => {
    const isAct = curTeam === tm;
    const label = tm === 'ALL' ? (isKo ? '전체 팀' : 'All Teams') : (teamNames[tm] || tm);
    return `<button class="chip s3-filter-chip ${isAct ? 'active' : ''}" data-s2-team="${tm}">
      ${tm !== 'ALL' ? teamLogo(tm, 's3-chip-logo') : ''}
      <span>${label}</span>
    </button>`;
  }).join('');

  const weekTabs = [
    { id: 'all', ko: '전체 경기 (' + allS2Matches.length + '경기)', en: 'All Matches (' + allS2Matches.length + ')' },
    { id: '1', ko: '정규 1주차', en: 'Regular Week 1' },
    { id: '2', ko: '정규 2주차', en: 'Regular Week 2' },
    { id: '3', ko: '정규 3주차', en: 'Regular Week 3' },
    { id: '4', ko: '정규 4주차', en: 'Regular Week 4' },
    { id: '2nd RR', ko: '2차 라운드 로빈', en: '2nd Round Robin' },
    { id: 'LCQ', ko: 'LCQ', en: 'LCQ' },
    { id: 'Playoffs', ko: '플레이오프', en: 'Playoffs' }
  ];

  const weekTabsHtml = weekTabs.map(w => `
    <button class="tabbtn s3-week-tab ${curWeek === w.id ? 'active' : ''}" data-s2-week="${w.id}">
      ${isKo ? w.ko : w.en}
    </button>
  `).join('');

  // Filter matches
  const filteredMatches = allS2Matches.filter(m => {
    const matchWeek = (curWeek === 'all') 
      ? true 
      : (curWeek === '1' || curWeek === '2' || curWeek === '3' || curWeek === '4')
        ? (m.phase === 'Round Robin' && String(m.week) === curWeek)
        : (m.phase === curWeek);
    const matchTeam = (curTeam === 'ALL') || (m.a === curTeam || m.b === curTeam);
    return matchWeek && matchTeam;
  });

  // Group filtered matches
  const matchGroups = [];
  filteredMatches.forEach(m => {
    let groupKey = m.phase === 'Round Robin' ? `Week ${m.week}` : m.phase;
    let groupTitleKo = m.phase === 'Round Robin' ? `정규 시즌 ${m.week}주차` : (m.phase === '2nd RR' ? '2차 라운드 로빈' : (m.phase === 'Playoffs' ? '플레이오프' : m.phase));
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
        const homeWon = m.winner === m.a;
        const awayWon = m.winner === m.b;
        const homeName = teamNames[m.a] || m.a;
        const awayName = teamNames[m.b] || m.b;
        const isMatchTarget = curTeam === 'ALL' || m.a === curTeam || m.b === curTeam;
        const isDimmed = !isMatchTarget;

        return `
          <div class="s3-match-row s2-match-row ${homeWon || awayWon ? 'completed' : ''} ${isDimmed ? 'dimmed' : ''}" data-match-key="${m.key}" data-tourney="kr-s2" title="${isKo ? '클릭하여 세부 스코어 및 밴픽 보기' : 'Click to view detail scores and bans'}">
            <div class="s3-match-meta">
              <span class="s3-match-num">${m.phase}</span>
              <span class="s2-result-tag">FINAL</span>
              <span class="s2-match-hint">🔍 ${isKo ? '세부 정보' : 'Details'}</span>
            </div>
            
            <div class="s2-match-body">
              <div class="s2-match-team home ${homeWon ? 'winner-team' : ''}" title="${homeName}">
                <div class="s3-team-text">
                  <strong class="s3-team-abbr">${m.a}</strong>
                  <span class="s3-team-fullname">${homeName}</span>
                </div>
                ${teamLogo(m.a, 's3-match-logo')}
              </div>

              <div class="s2-match-score-badge">
                <span class="s2-score ${homeWon ? 'win' : ''}">${m.aw}</span>
                <span class="s2-score-divider">:</span>
                <span class="s2-score ${awayWon ? 'win' : ''}">${m.bw}</span>
              </div>

              <div class="s2-match-team away ${awayWon ? 'winner-team' : ''}" title="${awayName}">
                ${teamLogo(m.b, 's3-match-logo')}
                <div class="s3-team-text">
                  <strong class="s3-team-abbr">${m.b}</strong>
                  <span class="s3-team-fullname">${awayName}</span>
                </div>
              </div>
            </div>

            ${(m.maps && m.maps.length) ? `
              <div class="s2-match-maps-footer">
                ${m.maps.map((x, idx) => `
                  <span class="s2-map-set-tag ${x.WINNER === m.winner ? 'winner' : ''}">
                    <b>S${idx + 1}</b> ${mapDisplayName(x.MAP)} <small>(${x.WINNER})</small>
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

  // 2. Map Pool Data & Rendering
  const rawPool = (s2.mapPool && s2.mapPool[curMapPhase]) || (s2.mapPool && s2.mapPool.regular) || {};
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
      <button class="chip s3-filter-chip ${isAct ? 'active' : ''}" data-s2-maptype="${opt.key}">
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
    <div class="s3-mappool-section" id="s2-mappool">
      <div class="page-title" style="margin-bottom:14px;">
        <div>
          <h2>${isKo ? '공식 전장 맵 풀 (Stage 2 Map Pool)' : 'Stage 2 Official Map Pool'}</h2>
          <p class="muted" style="margin:4px 0 0;">${isKo ? '정규 시즌 및 LCQ · 플레이오프 공식 채택 5개 전장 모드' : 'Official competitive map pool for Regular Season & Postseason'}</p>
        </div>
      </div>

      <!-- Phase Selector: Regular vs Postseason -->
      <div class="s2-mapphase-switch" style="display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap;">
        <button class="chip s2-mapphase-btn ${curMapPhase === 'regular' ? 'active' : ''}" data-s2-mapphase="regular">
          🎯 <b>${isKo ? '정규 시즌 맵 풀' : 'Regular Season Map Pool'}</b>
        </button>
        <button class="chip s2-mapphase-btn ${curMapPhase === 'postseason' ? 'active' : ''}" data-s2-mapphase="postseason">
          ⚔️ <b>${isKo ? 'LCQ / 2차 RR / 플레이오프 맵 풀' : 'LCQ & Playoffs Map Pool'}</b>
        </button>
      </div>

      <div class="s3-map-filters-bar">
        ${mapFilterChipsHtml}
      </div>

      <div class="s3-mappool-container">
        ${mapPoolBlocksHtml}
      </div>
    </div>
  `;

  // 3. Transfers Data & Rendering
  const transfers = s2.transfers || { in: [], out: [] };
  const inList = transfers.in || [];
  const outList = transfers.out || [];

  const inTeamsHtml = inList.map(item => `
    <div class="transfer-team-card">
      <div class="transfer-team-head">
        ${teamLogo(item.short, 'transfer-team-logo')}
        <span>${item.team} (${item.short})</span>
      </div>
      <div class="transfer-pills-wrap">
        ${item.items.map(p => `
          <span class="transfer-pill in">
            + <b>${p.name}</b>
            ${p.from ? `<small style="opacity:0.75;margin-left:4px;">(from ${p.from})</small>` : ''}
          </span>
        `).join('')}
      </div>
    </div>
  `).join('');

  const outTeamsHtml = outList.map(item => `
    <div class="transfer-team-card">
      <div class="transfer-team-head">
        ${teamLogo(item.short, 'transfer-team-logo')}
        <span>${item.team} (${item.short})</span>
      </div>
      <div class="transfer-pills-wrap">
        ${item.items.map(p => `
          <span class="transfer-pill out">
            − <b>${p.name}</b>
            ${p.to ? `<small style="opacity:0.75;margin-left:4px;">(to ${p.to})</small>` : ''}
          </span>
        `).join('')}
      </div>
    </div>
  `).join('');

  // 4. Teams Data & Rendering
  const teamsHtml = (s2.teams || []).map(tm => {
    const isZeta = tm.short === 'ZETA';
    const rankBadge = tm.stage1Rank ? `
      <span class="stage3-seed-badge" style="${isZeta ? 'background:linear-gradient(135deg, rgba(251,191,36,0.18) 0%, rgba(217,119,6,0.28) 100%);color:#fbbf24;border:1px solid rgba(251,191,36,0.5);font-weight:800;' : ''}">
        ${isZeta ? '🏆 ' : ''}${tm.stage1Rank}
      </span>
    ` : '';
    const rosterItems = (tm.roster || []).map(p => `
      <div class="stage3-roster-item">
        <span style="display:inline-flex;align-items:center;">
          <b style="color:var(--text);">${p.name}</b>
          ${p.isNew ? `<span class="stage3-new-tag">NEW</span>` : ''}
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
  const showStandings = curTab === 'standings' || curTab === 'all';
  const showMapPool = curTab === 'mappool' || curTab === 'all';
  const showTransfers = curTab === 'transfers' || curTab === 'all';
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
            ✓ ${isKo ? '대회 종료 (결과 확정)' : 'Completed'}
          </span>
        </div>
        <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
          <button class="chip" id="btnGoStage1FromS2">🏆 ${isKo ? 'Stage 1 둘러보기' : 'Stage 1 Results'}</button>
          <button class="chip" id="btnGoStage2Stats">📊 ${isKo ? 'Stage 2 상세 통계 랩' : 'View Stage 2 Stats Lab'}</button>
          <button class="chip" id="btnGoStage3">🚀 ${isKo ? 'Stage 3 프리뷰' : 'Stage 3 Preview'}</button>
        </div>
      </div>
      <h1 class="stage3-title">${tourName}</h1>
      <div class="stage3-meta-pills" style="margin-top:12px;">
        <span class="stage3-pill tier">💎 <b>${isKo ? 'A-TIER 대회' : 'A-TIER Tournament'}</b></span>
        <span class="stage3-pill prize">💰 <b>${isKo ? '총 상금 $38,500' : 'Total Prize $38,500'}</b></span>
      </div>
    </div>

    <!-- Stage 2 Navigation Sub-tabs -->
    <div class="s3-main-nav-bar">
      ${s2NavTabsHtml}
    </div>

    ${showStandings ? standingsSectionHtml : ''}

    ${showSchedule ? `
      <!-- Schedule Section -->
      <div class="s3-schedule-section">
        <div class="s3-schedule-topbar">
          <div>
            <div style="display:flex;align-items:center;gap:8px;">
              <span class="s3-schedule-live-dot" style="background:#10b981;box-shadow:0 0 10px #10b981;"></span>
              <h2 class="s3-schedule-heading">${isKo ? 'Stage 2 전체 경기 일정 & 최종 결과' : 'Stage 2 Match Schedule & Final Results'}</h2>
            </div>
            <p class="muted" style="margin:4px 0 0;font-size:13px;">
              ${isKo ? '정규 시즌 36경기 풀 라운드 로빈 및 2차 RR · LCQ · 플레이오프 전 경기 최종 스코어' : 'Full Round Robin (36 matches), 2nd Round Robin, LCQ and Playoffs official scores'}
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

    ${showTransfers ? `
      <div class="roster-changes-section">
        <div class="page-title" style="margin-bottom:12px;">
          <div>
            <h2>${isKo ? 'Stage 1 ➔ Stage 2 선수단 변동 (IN / OUT)' : 'Stage 1 ➔ Stage 2 Transfers (IN / OUT)'}</h2>
            <p class="muted" style="margin:4px 0 0;">${isKo ? 'Stage 2 개막 전 공식 영입(IN) 및 계약 종료/이적(OUT) 현황' : 'Official signings (IN) and transfers/departures (OUT) ahead of Stage 2'}</p>
          </div>
        </div>
        <div class="in-out-transfer-board">
          <div class="transfer-column in-col">
            <div class="transfer-column-head in">
              <span class="transfer-dot in"></span>
              <h3>IN (${isKo ? '영입' : 'Signings'})</h3>
            </div>
            <div class="transfer-team-list">
              ${inTeamsHtml}
            </div>
          </div>
          <div class="transfer-column out-col">
            <div class="transfer-column-head out">
              <span class="transfer-dot out"></span>
              <h3>OUT (${isKo ? '계약 종료 / 이적' : 'Departures & Releases'})</h3>
            </div>
            <div class="transfer-team-list">
              ${outTeamsHtml}
            </div>
          </div>
        </div>
      </div>
    ` : ''}

    ${showTeams ? `
      <div class="section" style="margin-bottom:24px;">
        <div class="page-title" style="margin-bottom:12px;">
          <div>
            <h2>${t('stage2_teams_title')}</h2>
            <p class="muted" style="margin:4px 0 0;">${isKo ? 'Stage 2 본선 진출 8개 팀 확정 로스터' : 'Official 8-team Stage 2 rosters'}</p>
          </div>
        </div>
        <div class="stage3-teams-grid">
          ${teamsHtml}
        </div>
      </div>
    ` : ''}

    <div class="stage3-notice-card" style="border-left-color:#10b981;">
      <span class="stage3-notice-icon">📊</span>
      <div>
        <strong style="color:#10b981;display:block;margin-bottom:2px;">${isKo ? 'Stage 2 공식 통계 랩 안내' : 'Stage 2 Stats Lab Notice'}</strong>
        <span>${isKo ? 'Stage 2의 모든 선수/팀 지표, 상관관계 산점도 및 영웅 밴 분석은 상단 메뉴의 각 탭(기본 정보, 선수 랭킹, 경기 탐색기 등)에서 확인하실 수 있습니다.' : 'All Stage 2 player/team metrics, correlation plots, and hero ban analyses can be explored in the top navigation tabs.'}</span>
      </div>
    </div>
  `;
}

function stageUpcomingPlaceholderPage(tourneyKey){
  const isKo = state.lang === 'ko';
  const isS3 = tourneyKey === 'kr-s3';
  const tourName = isS3 
    ? (isKo ? 'OWCS 코리아 2026 스테이지 3' : 'OWCS Korea 2026 Stage 3')
    : (isKo ? 'OWCS 코리아 2026 스테이지 1' : 'OWCS Korea 2026 Stage 1');
  const dateInfo = isS3 ? '2026.10.02 Starts' : '2026 Spring';
  const desc = isS3
    ? (isKo 
      ? 'OWCS Korea 2026 Stage 3는 10월 2일 개막합니다. 정규 시즌 개막 후 실시간 박스스코어 및 선수/팀 통계 지표가 집계됩니다.<br>현재 공식 맵 풀, 이적 현황 및 참가팀 로스터는 <strong>대회 개요</strong> 탭에서 확인하실 수 있습니다.'
      : 'OWCS Korea 2026 Stage 3 begins on October 2. Match box scores and statistics will be updated live once matches begin.<br>You can check the official map pool, transfers, and rosters in the <strong>Overview</strong> tab.')
    : (isKo
      ? '해당 대회의 상세 통계 데이터는 차기 업데이트에서 지원될 예정입니다.'
      : 'Detailed stats for this stage will be supported in upcoming updates.');

  return `
    <div class="stage3-hero s2-hero" style="margin-bottom:24px;">
      <div class="stage3-hero-top">
        <div class="stage3-brand-row">
          <img src="assets/owcs_korea_dark.png" alt="OWCS Korea" class="stage3-official-logo" />
          <span class="stage3-tier-badge">
            <span class="stage3-tier-icon">💎</span>
            <b>${isKo ? 'A-TIER 대회' : 'A-TIER'}</b>
          </span>
          <span class="stage3-dday-badge" style="${isS3 ? '' : 'background:#64748b;color:#fff;'}">
            ${isS3 ? 'Starts Oct 02' : 'Completed'}
          </span>
        </div>
        <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
          <button class="chip" id="btnGoOverviewFromPlc">📋 ${isKo ? '대회 개요 보기' : 'View Overview'}</button>
          <button class="chip" id="btnGoS2StatsFromPlc">📊 ${isKo ? 'Stage 2 통계 랩 가기' : 'View Stage 2 Stats'}</button>
        </div>
      </div>
      <h1 class="stage3-title">${tourName}</h1>
      <p class="muted" style="margin:4px 0 0;font-size:14px;">${dateInfo}</p>
    </div>

    <div class="empty-state-box" style="padding:60px 24px; text-align:center; max-width:680px; margin:30px auto; background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.08); border-radius:16px;">
      <span style="font-size:44px; display:block; margin-bottom:14px;">📊</span>
      <h2 style="font-size:20px; margin-bottom:8px;">${isKo ? '통계 데이터 수집 준비 중' : 'Statistics In Preparation'}</h2>
      <p class="muted" style="line-height:1.6; font-size:14px; margin-bottom:24px;">
        ${desc}
      </p>
      <div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap;">
        <button class="chip" id="btnGoOverviewDirect" style="background:#38bdf8; color:#0f172a; font-weight:700;">
          📋 ${isKo ? '대회 개요(프리뷰) 확인하기' : 'View Tournament Overview'}
        </button>
        <button class="chip" id="btnGoS2StatsDirect">
          📊 ${isKo ? 'Stage 2 통계 랩 둘러보기' : 'Explore Stage 2 Stats Lab'}
        </button>
      </div>
    </div>
  `;
}

function render(){
  nav();
  updateStaticHeaderTexts();
  const app = document.getElementById('app');

  const tourneyHeaderBtn = document.getElementById('tournamentsBtn');
  if (tourneyHeaderBtn) {
    tourneyHeaderBtn.classList.toggle('active', state.page === 'tournaments');
  }
  const globalTeamsHeaderBtn = document.getElementById('globalTeamsBtn');
  if (globalTeamsHeaderBtn) {
    globalTeamsHeaderBtn.classList.toggle('active', state.page === 'teams');
  }

  if (state.page === 'tournaments') {
    app.innerHTML = tournamentsPage();
    bindTournamentsPage();
    return;
  }

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
}

function bind(){
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

  // Team Page Status (Current vs Past) & Region Filter & Search Controls
  document.querySelectorAll('[data-team-status]').forEach(btn => {
    btn.onclick = () => {
      state.teamStatus = btn.dataset.teamStatus;
      render();
    };
  });
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


// ==========================================
// Setup Global Header Controls
// ==========================================
function setupHeaderControls(){
  // Tournament Dropdown Toggle
  const tourneyBtn=document.getElementById('tourneyBtn');
  const tourneySelector=document.getElementById('tourneySelector');
  if(tourneyBtn && tourneySelector){
    tourneyBtn.onclick=(e)=>{
      e.stopPropagation();
      tourneySelector.classList.toggle('open');
    };
    document.addEventListener('click',(e)=>{
      if(!tourneySelector.contains(e.target)){
        tourneySelector.classList.remove('open');
      }
    });
  }

  const globalTeamsBtn = document.getElementById('globalTeamsBtn');
  if (globalTeamsBtn) {
    globalTeamsBtn.onclick = () => {
      state.page = 'teams';
      state.team = null;
      state.player = null;
      localStorage.setItem('owcs_stat_lab_page', 'teams');
      render();
    };
  }

  const tournamentsBtn = document.getElementById('tournamentsBtn');
  if (tournamentsBtn) {
    tournamentsBtn.onclick = () => {
      state.page = 'tournaments';
      state.team = null;
      state.player = null;
      localStorage.setItem('owcs_stat_lab_page', 'tournaments');
      render();
    };
  }

  document.querySelectorAll('.tourney-option').forEach(opt=>{
    opt.onclick=()=>{
      if(opt.classList.contains('disabled')){
        showToast(t('toast_soon'));
        if(tourneySelector)tourneySelector.classList.remove('open');
        return;
      }
      const tKey=opt.dataset.tourney;
      state.tourney = tKey;
      state.page = 'overview';
      state.team = null;
      state.player = null;
      state.openMatch = null;
      state.openPhase = null;
      state.s1OpenPhase = null;
      state.tTab = 'schedule';
      state.tPhase = 'All';
      state.tSearch = '';
      localStorage.setItem('owcs_stat_lab_tourney', tKey);
      localStorage.setItem('owcs_stat_lab_page', 'overview');
      if(tourneySelector)tourneySelector.classList.remove('open');
      render();
    };
  });

  // Language Switch
  const langBtns=document.querySelectorAll('.lang-btn');
  langBtns.forEach(btn=>{
    btn.classList.toggle('active', btn.dataset.lang === state.lang);
    btn.onclick=()=>{
      const nextLang=btn.dataset.lang;
      if(state.lang!==nextLang){
        state.lang=nextLang;
        localStorage.setItem('owcs_stat_lab_lang',nextLang);
        langBtns.forEach(b=>b.classList.toggle('active',b.dataset.lang===nextLang));
        render();
      }
    };
  });
}

window.addEventListener('resize',()=>{
  if(currentRadarChart)currentRadarChart.resize();
  if(currentH2HChart)currentH2HChart.resize();
  if(currentHallOfFameChart)currentHallOfFameChart.resize();
  if(currentPrizeChart)currentPrizeChart.resize();
});



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


setupHeaderControls();
render();
