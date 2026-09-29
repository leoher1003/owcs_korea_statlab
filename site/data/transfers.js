// OWCS Korea Stage 1 -> Stage 2 roster transition.
// User-maintained transfer log. Events are stored as a list so multiple moves on the same date are preserved.
window.OWCS_STAGE2_TRANSFER_EVENTS = [
  // SuperBad entered Stage 2 with this roster. No exact signing date is asserted here.
  {date:'STAGE 2',team:'SuperBad',short:'SB',type:'IN',players:['SENTIER','Homerunball','SORI','AZENT','Soae','Dumbbell','Univ2r'],staff:['SeltaRet'],noteEn:'Stage 2 roster',noteKo:'Stage 2 참가 로스터'},
  {date:'2026-03-29',team:'O2 Blast',short:'O2',type:'IN',players:['GyulBokBok','Gamjung','MINJUNE'],staff:[],noteEn:'Joined O2 Blast',noteKo:'O2 Blast 합류'},

  {date:'2026-04-24',team:'New Era',short:'NE',type:'OUT',players:['perr'],staff:[],noteEn:'Left New Era',noteKo:'New Era를 떠남'},
  {date:'2026-04-26',team:'Cheeseburger',short:'CB',type:'OUT',players:['Faith'],staff:[],noteEn:'Left Cheeseburger',noteKo:'Cheeseburger를 떠남'},
  {date:'2026-04-26',team:'Poker Face',short:'PF',type:'OUT',players:['Gur3um'],staff:[],noteEn:'Left Poker Face',noteKo:'Poker Face를 떠남'},
  {date:'2026-04-27',team:'Cheeseburger',short:'CB',type:'OUT',players:['ZeSin'],staff:[],noteEn:'Left Cheeseburger',noteKo:'Cheeseburger를 떠남'},
  {date:'2026-04-27',team:'Poker Face',short:'PF',type:'OUT',players:['TenTen'],staff:[],noteEn:'Left Poker Face',noteKo:'Poker Face를 떠남'},
  {date:'2026-04-27',team:'New Era',short:'NE',type:'OUT',players:['D0D0','Yate','SoLA','MCD','Secret'],staff:['Rumba'],noteEn:'Players and staff left New Era',noteKo:'선수 및 스태프가 New Era를 떠남'},

  {date:'2026-05-01',team:'Poker Face',short:'PF',type:'OUT',players:['M1NUT2','D0D0'],staff:[],noteEn:'Left Poker Face',noteKo:'Poker Face를 떠남'},
  {date:'2026-05-03',team:'ZAN Esports',short:'ZAN',type:'OUT',players:['Becky','HEISER'],staff:[],noteEn:'Left ZAN Esports',noteKo:'ZAN Esports를 떠남'},
  {date:'2026-05-04',team:'Cheeseburger',short:'CB',type:'OUT',players:['SeungAn'],staff:[],noteEn:'Left Cheeseburger',noteKo:'Cheeseburger를 떠남'},
  {date:'2026-05-04',team:'O2 Blast',short:'O2',type:'OUT',players:['Kalios','Myunb0ng','MINJUNE'],staff:[],noteEn:'Left O2 Blast',noteKo:'O2 Blast를 떠남'},
  {date:'2026-05-04',team:'O2 Blast',short:'O2',type:'IN',players:['perr','WuTian','Victoria','Faith','SeungAn'],staff:[],noteEn:'Joined O2 Blast',noteKo:'O2 Blast 합류'},
  {date:'2026-05-08',team:'Cheeseburger',short:'CB',type:'OUT',players:['Jamelgong'],staff:['Opera'],noteEn:'Player and staff left Cheeseburger',noteKo:'선수 및 스태프가 Cheeseburger를 떠남'},
  {date:'2026-05-08',team:'Cheeseburger',short:'CB',type:'IN',players:['M1NUT2','Gur3um','TenTen'],staff:['Da1Da1sm00th'],noteEn:'Joined Cheeseburger',noteKo:'Cheeseburger 합류'},
  {date:'2026-05-08',team:'Poker Face',short:'PF',type:'OUT',players:['Da1Da1sm00th'],staff:[],noteEn:'Left Poker Face',noteKo:'Poker Face를 떠남'},
  {date:'2026-05-09',team:'Poker Face',short:'PF',type:'IN',players:['HYEON','K4ne','D0D0'],staff:[],noteEn:'Joined Poker Face',noteKo:'Poker Face 합류'},
  {date:'2026-05-15',team:'Røde ONSIDE GAMING',short:'ROG',type:'OUT',players:['SP1NT'],staff:[],noteEn:'Left Røde ONSIDE GAMING',noteKo:'Røde ONSIDE GAMING을 떠남'},
  {date:'2026-05-15',team:'ZAN Esports',short:'ZAN',type:'OUT',players:['A1IEN','Yangjun','KIVIS'],staff:['Mircalla'],noteEn:'Players and staff left ZAN Esports',noteKo:'선수 및 스태프가 ZAN Esports를 떠남'},
  {date:'2026-05-20',team:'Røde ONSIDE GAMING',short:'ROG',type:'OUT',players:['Attack','IRONY','OPENER','Kilo'],staff:['Haksal','Ado','F4ze'],noteEn:'Players and staff left Røde ONSIDE GAMING',noteKo:'선수 및 스태프가 Røde ONSIDE GAMING을 떠남'},
  {date:'2026-05-20',team:'ZAN Esports',short:'ZAN',type:'OUT',players:['Probe'],staff:['Ir1s','KariV','sihu'],noteEn:'Player and staff left ZAN Esports',noteKo:'선수 및 스태프가 ZAN Esports를 떠남'},

  // Transfer v1 events retained alongside the expanded v2 log.
  {date:'2026-05-20',team:'Røde ZANSIDE GAMING',short:'ROZE',type:'IN',players:['Probe','Kilo','IRONY','OPENER','Void','Becky','HEISER'],staff:['Haksal','Ado','Ir1s','KariV','sihu'],noteEn:'Røde ONSIDE GAMING and ZAN Esports merged',noteKo:'Røde ONSIDE GAMING과 ZAN Esports의 합병으로 창단'},
  {date:'2026-05-25',team:'Poker Face',short:'PF',type:'IN',players:[],staff:['Nyammulba','Mandu','Rexi'],noteEn:'Signed coaching staff before Stage 2',noteKo:'Stage 2 시작 전 코칭 스태프 영입'},
  {date:'2026-05-26',team:'O2 Blast',short:'O2',type:'OUT',players:['Victoria'],staff:[],noteEn:'Left the team after the open qualifiers',noteKo:'오픈 퀄리파이어 이후 팀을 떠남'},
  {date:'2026-05-26',team:'O2 Blast',short:'O2',type:'IN',players:['Fate','Gamjung'],staff:[],noteEn:'Signed two players before Stage 2',noteKo:'Stage 2 시작 전 2명의 선수 영입'},
  {date:'2026-05-27',team:'Team Falcons',short:'FLC',type:'IN',players:['SP1NT'],staff:[],noteEn:'Signed from Røde ONSIDE GAMING',noteKo:'Røde ONSIDE GAMING에서 영입'},
  {date:'2026-05-30',team:'Cheeseburger',short:'CB',type:'IN',players:[],staff:['LeGo','Mircalla'],noteEn:'Signed two coaching staff after the open qualifiers',noteKo:'오픈 퀄리파이어 이후 코칭 스태프 2명 영입'}
];

window.OWCS_STAGE2_OPEN_QUALIFIER = {
  standings:{'1st-2nd':['Cheeseburger','O2 Blast'],'3rd':'Poker Face','4th':'SuperBad'},
  rosters:{
    'Cheeseburger':{staff:{Da1Da1sm00th:'Coach'},players:{FARMER:'TANK',Gur3um:'TANK',Argon:'DPS',M1NUT2:'DPS',TenTen:'SPT',WoochaN:'SPT'}},
    'O2 Blast':{staff:{O2Boss:'Head Coach',Chilhwa:'Coach',Myunb0ng:'Coach',Cane:'Coach'},players:{SeungAn:'TANK',WuTian:'DPS',perr:'DPS',Faith:'SPT',Victoria:'SPT',Gamjung:'SPT'}},
    'Poker Face':{staff:{Doha:'Coach'},players:{Fearful:'TANK',HYEON:'TANK',D0D0:'DPS',K4ne:'DPS',Sp1nel:'SPT',CARU:'SPT'}},
    'SuperBad':{staff:{SeltaRet:'Coach'},players:{SENTIER:'TANK',Homerunball:'TANK',SORI:'DPS',AZENT:'DPS',Soae:'DPS',Dumbbell:'SPT',Univ2r:'SPT'}}
  }
};
