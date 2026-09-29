window.OWCS_STAGE3_PREVIEW = {
  tournament: {
    name: "OWCS Korea 2026 Stage 3",
    nameKo: "OWCS 코리아 2026 스테이지 3",
    startDate: "2026-10-02",
    endDate: "2026-11-08",
    status: "Starts Oct 02",
    statusKo: "Starts Oct 02",
    venue: "WDG Esports Studio (Seoul)",
    tier: "A-TIER",
    tierKo: "A-TIER 대회",
    tierEn: "A-TIER Tournament",
    prizePool: "$38,500",
    prizePoolKo: "총 상금 $38,500",
    prizePoolEn: "Total Prize $38,500"
  },
  broadcasts: [
    {
      platform: "SOOP",
      nameKo: "SOOP (한국어 공식 중계)",
      nameEn: "SOOP (KR Official)",
      url: "https://www.sooplive.com/station/owesports",
      color: "#38bdf8",
      tag: "KR"
    },
    {
      platform: "Twitch",
      nameKo: "Twitch (글로벌 공식 중계)",
      nameEn: "Twitch (Global Official)",
      url: "https://www.twitch.tv/ow_esports/",
      color: "#a855f7",
      tag: "Global"
    }
  ],
  mapPool: {
    Control: {
      type: "Control",
      nameKo: "쟁탈",
      nameEn: "Control",
      color: "#10b981",
      icon: "🎯",
      maps: [
        { nameKo: "부산", nameEn: "Busan" },
        { nameKo: "네팔", nameEn: "Nepal" },
        { nameKo: "사모아", nameEn: "Samoa" }
      ]
    },
    Hybrid: {
      type: "Hybrid",
      nameKo: "혼합",
      nameEn: "Hybrid",
      color: "#f59e0b",
      icon: "⚔️",
      maps: [
        { nameKo: "아이헨발데", nameEn: "Eichenwalde" },
        { nameKo: "파라이수", nameEn: "Paraíso" },
        { nameKo: "네온 교차로", nameEn: "Neon Junction" }
      ]
    },
    Escort: {
      type: "Escort",
      nameKo: "호위",
      nameEn: "Escort",
      color: "#3b82f6",
      icon: "🚛",
      maps: [
        { nameKo: "쓰레기촌", nameEn: "Junkertown" },
        { nameKo: "66번 국도", nameEn: "Route 66" },
        { nameKo: "샴발리 수도원", nameEn: "Shambali Monastery" }
      ]
    },
    Push: {
      type: "Push",
      nameKo: "밀기",
      nameEn: "Push",
      color: "#a855f7",
      icon: "🤖",
      maps: [
        { nameKo: "콜로세오", nameEn: "Colosseo" },
        { nameKo: "이스페란사", nameEn: "Esperança" }
      ]
    },
    Flashpoint: {
      type: "Flashpoint",
      nameKo: "플래시포인트",
      nameEn: "Flashpoint",
      color: "#06b6d4",
      icon: "⚡",
      maps: [
        { nameKo: "아틀리스", nameEn: "Aatlis" },
        { nameKo: "뉴 정크 시티", nameEn: "New Junk City" },
        { nameKo: "수라바사", nameEn: "Suravasa" }
      ]
    }
  },
  transfers: {
    in: [
      { team: "T1", short: "T1", items: [{ name: "Ggultaek" }] },
      { team: "Røde Zanside Gaming", short: "ROZE", items: [{ name: "HEESUNG" }, { name: "Taejong" }] },
      { team: "O2 Blast", short: "O2", items: [{ name: "Homerunball" }, { name: "A1IEN" }] },
      { team: "Cheeseburger", short: "CB", items: [{ name: "Belosrea" }, { name: "Profit" }, { name: "AZENT" }, { name: "Trest" }, { name: "K4ne" }] },
      { team: "Poker Face", short: "PF", items: [{ name: "F1nally" }, { name: "SORI" }, { name: "SoLA" }, { name: "SWOO" }, { name: "Caffeine" }, { name: "Dumbbell" }, { name: "SOAE" }] }
    ],
    out: [
      { team: "Røde Zanside Gaming", short: "ROZE", items: [{ name: "Probe" }, { name: "SeungAn" }] },
      { team: "Cheeseburger", short: "CB", items: [{ name: "Farmer" }, { name: "WoochaN" }, { name: "Gur3um" }, { name: "Argon" }] },
      { team: "Poker Face", short: "PF", items: [{ name: "Fearful" }, { name: "HYEON" }, { name: "K4ne" }, { name: "D0D0" }, { name: "Sp1nel" }, { name: "CARU" }] }
    ]
  },
  newTeam: {
    name: "Seiji Esports",
    short: "SEJ",
    roster: [
      { name: "DOX", role: "TANK", isNew: true },
      { name: "SENTIER", role: "TANK", isNew: true },
      { name: "D4RT", role: "DPS", isNew: true },
      { name: "M1NUT2", role: "DPS", isNew: true },
      { name: "OFF", role: "SPT", isNew: true },
      { name: "LAVENDER", role: "SPT", isNew: true }
    ]
  },
  teams: [
    {
      name: "Crazy Raccoon",
      short: "CR",
      roster: [
        { name: "JUNBIN", role: "TANK" },
        { name: "MAX", role: "TANK" },
        { name: "HEESANG", role: "DPS" },
        { name: "LIP", role: "DPS" },
        { name: "STALK3R", role: "DPS" },
        { name: "CH0R0NG", role: "SPT" },
        { name: "VIGILANTE", role: "SPT" }
      ]
    },
    {
      name: "Team Falcons",
      short: "FLC",
      roster: [
        { name: "SOMEONE", role: "TANK" },
        { name: "HANBIN", role: "TANK" },
        { name: "CHECKMATE", role: "DPS" },
        { name: "SP1NT", role: "DPS" },
        { name: "MER1T", role: "DPS" },
        { name: "CHIYO", role: "SPT" },
        { name: "FIELDER", role: "SPT" }
      ]
    },
    {
      name: "T1",
      short: "T1",
      roster: [
        { name: "DONGHAK", role: "TANK" },
        { name: "JASM1NE", role: "TANK" },
        { name: "ZEST", role: "DPS" },
        { name: "PROUD", role: "DPS" },
        { name: "BLISS", role: "SPT" },
        { name: "SKEWED", role: "SPT" },
        { name: "FLETA", role: "SPT" }
      ]
    },
    {
      name: "ZETA DIVISION",
      short: "ZETA",
      seed: "Defending Champion",
      seedKo: "디펜딩 챔피언",
      roster: [
        { name: "BERNAR", role: "TANK" },
        { name: "MEALGARU", role: "TANK" },
        { name: "PROPER", role: "DPS" },
        { name: "KNIFE", role: "DPS" },
        { name: "VIOL2T", role: "SPT" },
        { name: "SHU", role: "SPT" }
      ]
    },
    {
      name: "Poker Face",
      short: "PF",
      roster: [
        { name: "F1NALLY", role: "TANK", isNew: true },
        { name: "SORI", role: "DPS", isNew: true },
        { name: "SOLA", role: "DPS", isNew: true },
        { name: "SWOO", role: "SPT", isNew: true },
        { name: "CAFFEINE", role: "SPT", isNew: true },
        { name: "DUMBBELL", role: "SPT", isNew: true },
        { name: "SOAE", role: "SPT", isNew: true }
      ]
    },
    {
      name: "Cheeseburger",
      short: "CB",
      roster: [
        { name: "BELOSREA", role: "TANK", isNew: true },
        { name: "TREST", role: "DPS", isNew: true },
        { name: "K4NE", role: "DPS", isNew: true },
        { name: "PROFIT", role: "DPS", isNew: true },
        { name: "TENTEN", role: "SPT" },
        { name: "AZENT", role: "SPT", isNew: true }
      ]
    },
    {
      name: "Røde Zanside Gaming",
      short: "ROZE",
      roster: [
        { name: "HEISER", role: "TANK" },
        { name: "HEESUNG", role: "TANK", isNew: true },
        { name: "BECKY", role: "DPS" },
        { name: "KILO", role: "DPS" },
        { name: "TAEJONG", role: "DPS", isNew: true },
        { name: "OPENER", role: "SPT" },
        { name: "IRONY", role: "SPT" }
      ]
    },
    {
      name: "Seiji Esports",
      short: "SEJ",
      altShort: "RT",
      roster: [
        { name: "DOX", role: "TANK", isNew: true },
        { name: "SENTIER", role: "TANK", isNew: true },
        { name: "D4RT", role: "DPS", isNew: true },
        { name: "M1NUT2", role: "DPS", isNew: true },
        { name: "OFF", role: "SPT", isNew: true },
        { name: "LAVENDER", role: "SPT", isNew: true }
      ]
    },
    {
      name: "O2 Blast",
      short: "O2",
      roster: [
        { name: "FATE", role: "TANK" },
        { name: "HOMERUNBALL", role: "TANK", isNew: true },
        { name: "WUTIAN", role: "DPS" },
        { name: "PERR", role: "DPS" },
        { name: "A1IEN", role: "DPS", isNew: true },
        { name: "FAITH", role: "SPT" },
        { name: "GAMJUNG", role: "SPT" }
      ]
    }
  ],
  teamLookup: {
    CR: { name: "Crazy Raccoon", short: "CR", color: "#e11d48" },
    FLC: { name: "Team Falcons", short: "FLC", color: "#10b981" },
    T1: { name: "T1", short: "T1", color: "#ef4444" },
    ZETA: { name: "ZETA DIVISION", short: "ZETA", color: "#f59e0b" },
    PF: { name: "Poker Face", short: "PF", color: "#a855f7" },
    CB: { name: "Cheeseburger", short: "CB", color: "#f97316" },
    ROZE: { name: "Røde Zanside Gaming", short: "ROZE", color: "#64748b" },
    O2: { name: "O2 Blast", short: "O2", color: "#38bdf8" },
    SEJ: { name: "Seiji Esports", short: "SEJ", altName: "RT", color: "#38bdf8" },
    RT: { name: "Seiji Esports", short: "SEJ", altName: "RT", color: "#38bdf8" }
  },
  schedule: [
    {
      week: 1,
      titleKo: "1주차 (Week 1)",
      titleEn: "Week 1",
      dateRange: "10.02 - 10.04",
      days: [
        {
          day: 1,
          dateKo: "10.02 (금)",
          dateEn: "Oct 02 (Fri)",
          time: "17:00",
          matches: [
            { matchNum: 1, home: "CB", away: "PF" },
            { matchNum: 2, home: "FLC", away: "ZETA", isBigMatch: true },
            { matchNum: 3, home: "SEJ", away: "T1" }
          ]
        },
        {
          day: 2,
          dateKo: "10.03 (토)",
          dateEn: "Oct 03 (Sat)",
          time: "15:00",
          matches: [
            { matchNum: 4, home: "CB", away: "ROZE" },
            { matchNum: 5, home: "T1", away: "ZETA", isBigMatch: true },
            { matchNum: 6, home: "CR", away: "O2" }
          ]
        },
        {
          day: 3,
          dateKo: "10.04 (일)",
          dateEn: "Oct 04 (Sun)",
          time: "15:00",
          matches: [
            { matchNum: 7, home: "O2", away: "SEJ" },
            { matchNum: 8, home: "CR", away: "ROZE" },
            { matchNum: 9, home: "FLC", away: "PF" }
          ]
        }
      ]
    },
    {
      week: 2,
      titleKo: "2주차 (Week 2)",
      titleEn: "Week 2",
      dateRange: "10.09 - 10.11",
      days: [
        {
          day: 1,
          dateKo: "10.09 (금)",
          dateEn: "Oct 09 (Fri)",
          time: "17:00",
          matches: [
            { matchNum: 10, home: "FLC", away: "O2" },
            { matchNum: 11, home: "PF", away: "T1" },
            { matchNum: 12, home: "SEJ", away: "ZETA" }
          ]
        },
        {
          day: 2,
          dateKo: "10.10 (토)",
          dateEn: "Oct 10 (Sat)",
          time: "15:00",
          matches: [
            { matchNum: 13, home: "SEJ", away: "ROZE" },
            { matchNum: 14, home: "CR", away: "T1", isBigMatch: true },
            { matchNum: 15, home: "CB", away: "FLC" }
          ]
        },
        {
          day: 3,
          dateKo: "10.11 (일)",
          dateEn: "Oct 11 (Sun)",
          time: "15:00",
          matches: [
            { matchNum: 16, home: "O2", away: "ROZE" },
            { matchNum: 17, home: "CB", away: "CR" },
            { matchNum: 18, home: "PF", away: "ZETA" }
          ]
        }
      ]
    },
    {
      week: 3,
      titleKo: "3주차 (Week 3)",
      titleEn: "Week 3",
      dateRange: "10.16 - 10.18",
      days: [
        {
          day: 1,
          dateKo: "10.16 (금)",
          dateEn: "Oct 16 (Fri)",
          time: "17:00",
          matches: [
            { matchNum: 19, home: "FLC", away: "SEJ" },
            { matchNum: 20, home: "CB", away: "T1" },
            { matchNum: 21, home: "O2", away: "ZETA" }
          ]
        },
        {
          day: 2,
          dateKo: "10.17 (토)",
          dateEn: "Oct 17 (Sat)",
          time: "15:00",
          matches: [
            { matchNum: 22, home: "O2", away: "PF" },
            { matchNum: 23, home: "CR", away: "FLC", isBigMatch: true },
            { matchNum: 24, home: "T1", away: "ROZE" }
          ]
        },
        {
          day: 3,
          dateKo: "10.18 (일)",
          dateEn: "Oct 18 (Sun)",
          time: "15:00",
          matches: [
            { matchNum: 25, home: "CB", away: "SEJ" },
            { matchNum: 26, home: "CR", away: "PF" },
            { matchNum: 27, home: "ROZE", away: "ZETA" }
          ]
        }
      ]
    },
    {
      week: 4,
      titleKo: "4주차 (Week 4)",
      titleEn: "Week 4",
      dateRange: "10.23 - 10.25",
      days: [
        {
          day: 1,
          dateKo: "10.23 (금)",
          dateEn: "Oct 23 (Fri)",
          time: "17:00",
          matches: [
            { matchNum: 28, home: "CB", away: "O2" },
            { matchNum: 29, home: "FLC", away: "ROZE" },
            { matchNum: 30, home: "CR", away: "SEJ" }
          ]
        },
        {
          day: 2,
          dateKo: "10.24 (토)",
          dateEn: "Oct 24 (Sat)",
          time: "15:00",
          matches: [
            { matchNum: 31, home: "CB", away: "ZETA" },
            { matchNum: 32, home: "FLC", away: "T1", isBigMatch: true },
            { matchNum: 33, home: "PF", away: "SEJ" }
          ]
        },
        {
          day: 3,
          dateKo: "10.25 (일)",
          dateEn: "Oct 25 (Sun)",
          time: "15:00",
          matches: [
            { matchNum: 34, home: "PF", away: "ROZE" },
            { matchNum: 35, home: "O2", away: "T1" },
            { matchNum: 36, home: "ZETA", away: "CR", isBigMatch: true }
          ]
        }
      ]
    }
  ]
};
