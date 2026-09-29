// scripts/verify_app_runtime.js
// Mock browser environment for JavaScriptCore
var window = {
  location: { search: '', hash: '' },
  localStorage: {
    getItem: function() { return null; },
    setItem: function() {},
    removeItem: function() {}
  },
  addEventListener: function() {},
  removeEventListener: function() {},
  scrollTo: function() {},
  OWCS_DATA: null,
  OWCS_STAGE1_PREVIEW: null,
  OWCS_STAGE2_PREVIEW: null,
  OWCS_ASIA_S1_PREVIEW: null,
  OWCS_BOOTCAMP_PREVIEW: null,
  OWCS_CLASH_PREVIEW: null,
  OWCS_MIDSEASON_PREVIEW: null,
  OWCS_OWWC_PREVIEW: null,
  GLOBAL_TEAMS_DATA: null
};
var global = window;
var localStorage = window.localStorage;
var location = window.location;
var document = {
  addEventListener: function() {},
  removeEventListener: function() {},
  getElementById: function(id) {
    return {
      id: id,
      innerHTML: '',
      innerText: '',
      style: {},
      classList: {
        add: function() {},
        remove: function() {},
        toggle: function() {},
        contains: function() { return false; }
      },
      addEventListener: function() {},
      querySelectorAll: function() { return []; },
      querySelector: function() { return null; },
      value: ''
    };
  },
  querySelector: function() { return null; },
  querySelectorAll: function() { return []; },
  createElement: function(tag) {
    return {
      tagName: tag.toUpperCase(),
      innerHTML: '',
      style: {},
      classList: { add: function() {}, remove: function() {} },
      appendChild: function() {},
      setAttribute: function() {},
      addEventListener: function() {}
    };
  },
  body: {
    classList: { add: function() {}, remove: function() {} },
    appendChild: function() {}
  }
};

print("[1/5] Loading data files...");
load("owcs-stat-lab 2/data/data.js");
load("owcs-stat-lab 2/data/stage1_preview.js");
load("owcs-stat-lab 2/data/stage2_preview.js");
load("owcs-stat-lab 2/data/asia_s1_preview.js");
load("owcs-stat-lab 2/data/bootcamp_preview.js");
load("owcs-stat-lab 2/data/clash_preview.js");
load("owcs-stat-lab 2/data/midseason_preview.js");
load("owcs-stat-lab 2/data/owwc_preview.js");
load("owcs-stat-lab 2/data/global_teams_data.js");

print("[2/5] Loading app.js...");
load("owcs-stat-lab 2/app.js");

print("[3/5] Testing all 7 tournaments Match Explorer components...");
var tournaments = ['kr-s2', 'kr-s1', 'asia-s1', 'bootcamp-s1', 'clash-2026', 'midseason-2026', 'owwc-2026'];

for (var i = 0; i < tournaments.length; i++) {
  var tid = tournaments[i];
  state.tourney = tid;
  var ds = getActiveTourneyData();
  if (!ds || !ds.matches || ds.matches.length === 0) {
    throw new Error("Dataset for " + tid + " is missing or empty!");
  }
  
  var html = matchesPage();
  if (!html || html.length < 500) {
    throw new Error("matchesPage for " + tid + " returned too short HTML!");
  }
  
  var rr = roundRobinMatrix(ds);
  var phaseMatches = phaseMatchList('all', ds);
  var bans = banCounts('All', 'All', 'by', 'Overall', 'All', ds);
  var mapStats = mapTypeStats(ds);
  var specMapStats = specificMapStats(ds, 'Control');
  
  // Test match detail lookup
  var firstMatch = ds.matches[0];
  var testId = firstMatch.matchId || firstMatch.key || firstMatch.id;
  var mObj = findMatchObject(testId, tid);
  // Test exact match lookup
  if (!mObj) {
    throw new Error("findMatchObject failed for " + tid + " matchId: " + testId);
  }
  
  // Test prefix variation if matchId starts with word
  if (testId.indexOf('-') !== -1 && testId.indexOf('Round') === -1) {
    var altId = testId.replace(/^[a-z0-9]+-/, '');
    var mObjAlt = findMatchObject(altId, tid);
    if (!mObjAlt) {
      throw new Error("findMatchObject alt failed for " + tid + " id: " + altId);
    }
  }
  
  print("  -> Tournament OK: " + tid + " (" + ds.matches.length + " matches, " + Object.keys(bans).length + " bans recorded)");
}

print("[4/5] Testing Teams Page & 6-step ordering...");
var teamsHtml = teamsPage();
if (!teamsHtml || teamsHtml.length < 1000) {
  throw new Error("teamsPage returned empty HTML!");
}

// 1. Current OWCS Team (CR)
state.team = 'CR';
var crHtml = teamsPage();
if (!crHtml || crHtml.length < 1000) {
  throw new Error("teamsPage with state.team=CR returned empty HTML!");
}

var c_sec0 = crHtml.indexOf("주요 우승 및 입상 기록 (Key Achievements)");
var c_sec1 = crHtml.indexOf("현재 로스터 (Active Roster)");
var c_sec2 = crHtml.indexOf("로스터 연혁 및 이적 타임라인");
var c_sec3 = crHtml.indexOf("코칭스태프 (Coaching Staff)");
var c_sec4 = crHtml.indexOf("전장 유형별 최고 / 최저 승률 전장");
var c_sec5 = crHtml.indexOf("Most Banned Against Top 5");
var c_sec6 = crHtml.indexOf("Most Banned by [TEAM] Top 5");

if (c_sec0 === -1 || c_sec1 === -1 || c_sec2 === -1 || c_sec3 === -1 || c_sec4 === -1 || c_sec5 === -1 || c_sec6 === -1) {
  throw new Error("Current Team section missing: " + [c_sec0, c_sec1, c_sec2, c_sec3, c_sec4, c_sec5, c_sec6].join(", "));
}

if (!(c_sec0 < c_sec1 && c_sec1 < c_sec2 && c_sec2 < c_sec3 && c_sec3 < c_sec4 && c_sec4 < c_sec5 && c_sec5 < c_sec6)) {
  throw new Error("Current Team ordering violation! Must be: Achievements < Active Roster < Transfers < Coaches < Mode Maps < Bans");
}
print("  -> Current Team (CR) strict 6-section order verified: Achievements -> Active Roster -> Transfers -> Coaches -> Mode Maps -> Bans!");

// 2. Past OWCS Team (FTG or WAC)
state.team = 'FTG';
var ftgHtml = teamsPage();
if (!ftgHtml || ftgHtml.length < 1000) {
  throw new Error("teamsPage with state.team=FTG returned empty HTML!");
}

var p_sec1 = ftgHtml.indexOf("마지막 공식 로스터 (Final Roster)");
var p_sec2 = ftgHtml.indexOf("구단 인수/합병 및 이적 연혁");
var p_sec3 = ftgHtml.indexOf("코칭스태프 (Coaching Staff)");
var p_sec4 = ftgHtml.indexOf("전장 유형별 최고 / 최저 승률 전장");
var p_sec5 = ftgHtml.indexOf("Most Banned Against Top 5");
var p_sec6 = ftgHtml.indexOf("Most Banned by [TEAM] Top 5");

if (p_sec1 === -1 || p_sec2 === -1 || p_sec3 === -1 || p_sec4 === -1 || p_sec5 === -1 || p_sec6 === -1) {
  throw new Error("Past Team section missing: " + [p_sec1, p_sec2, p_sec3, p_sec4, p_sec5, p_sec6].join(", "));
}

if (!(p_sec1 < p_sec2 && p_sec2 < p_sec3 && p_sec3 < p_sec4 && p_sec4 < p_sec5 && p_sec5 < p_sec6)) {
  throw new Error("Past Team ordering violation! Must be: Final Roster < Transfers < Coaches < Mode Maps < Bans");
}
print("  -> Past Team (FTG) strict ordering verified: Final Roster -> Transfers -> Coaches -> Mode Maps -> Bans!");

// Check for 5 mode cards
var modes = ['쟁탈', '혼합', '플래시포인트', '밀기', '호위', 'Control', 'Hybrid', 'Flashpoint', 'Push', 'Escort'];
for (var m = 0; m < modes.length; m++) {
  if (crHtml.indexOf(modes[m]) === -1 || ftgHtml.indexOf(modes[m]) === -1) {
    throw new Error("Missing game mode token: " + modes[m]);
  }
}
print("  -> All 5 Game Modes (Control, Hybrid, Flashpoint, Push, Escort) Best/Worst cards present!");

print("[5/6] Testing North America (NA) Region Current and Past Teams...");

// 1. NA Current Teams list test
state.team = null;
state.teamRegionFilter = 'NA';
state.teamStatus = 'CURRENT';
var naCurrentListHtml = teamsPage();

var expectedNaCurrent = ['SSG', 'TL', 'DF', 'M80', 'DSG'];
for (var i = 0; i < expectedNaCurrent.length; i++) {
  var nid = expectedNaCurrent[i];
  if (naCurrentListHtml.indexOf(nid) === -1) {
    throw new Error("NA Current team list missing: " + nid);
  }
}
print("  -> NA Current Teams list successfully verified (SSG, TL, DF, M80, DSG)!");

// 2. NA Past Teams list test
state.teamStatus = 'PAST';
var naPastListHtml = teamsPage();

var expectedNaPast = ['TD', 'NTMR', 'LG', 'CN', 'SOTG'];
for (var i = 0; i < expectedNaPast.length; i++) {
  var pid = expectedNaPast[i];
  if (naPastListHtml.indexOf(pid) === -1) {
    throw new Error("NA Past team list missing: " + pid);
  }
}
print("  -> NA Past Teams list successfully verified (TD, NTMR, LG, CN, SOTG)!");

// 3. NA Current Team Detail: SSG (Spacestation Gaming) 6-step ordering
state.team = 'SSG';
var ssgHtml = teamsPage();
var ssg_s0 = ssgHtml.indexOf("주요 우승 및 입상 기록 (Key Achievements)");
var ssg_s1 = ssgHtml.indexOf("현재 로스터 (Active Roster)");
var ssg_s2 = ssgHtml.indexOf("로스터 연혁 및 이적 타임라인");
var ssg_s3 = ssgHtml.indexOf("코칭스태프 (Coaching Staff)");
var ssg_s4 = ssgHtml.indexOf("전장 유형별 최고 / 최저 승률 전장");
var ssg_s5 = ssgHtml.indexOf("Most Banned Against Top 5");
var ssg_s6 = ssgHtml.indexOf("Most Banned by [TEAM] Top 5");

if (ssg_s0 === -1 || ssg_s1 === -1 || ssg_s2 === -1 || ssg_s3 === -1 || ssg_s4 === -1 || ssg_s5 === -1 || ssg_s6 === -1) {
  throw new Error("SSG detail sections missing: " + [ssg_s0, ssg_s1, ssg_s2, ssg_s3, ssg_s4, ssg_s5, ssg_s6].join(", "));
}
if (!(ssg_s0 < ssg_s1 && ssg_s1 < ssg_s2 && ssg_s2 < ssg_s3 && ssg_s3 < ssg_s4 && ssg_s4 < ssg_s5 && ssg_s5 < ssg_s6)) {
  throw new Error("SSG strict 6-step ordering violated!");
}
if (ssgHtml.indexOf("Sugarfree") === -1 || ssgHtml.indexOf("Hawk") === -1) {
  throw new Error("SSG active roster players missing!");
}
print("  -> NA Current Team (SSG) strict 6-section order & players verified!");

// 4. NA Past Team Detail: TD (Toronto Defiant) 5-step ordering
state.team = 'TD';
var tdHtml = teamsPage();
var td_s1 = tdHtml.indexOf("마지막 공식 로스터 (Final Roster)");
var td_s2 = tdHtml.indexOf("구단 인수/합병 및 이적 연혁");
var td_s3 = tdHtml.indexOf("코칭스태프 (Coaching Staff)");
var td_s4 = tdHtml.indexOf("전장 유형별 최고 / 최저 승률 전장");
var td_s5 = tdHtml.indexOf("Most Banned Against Top 5");
var td_s6 = tdHtml.indexOf("Most Banned by [TEAM] Top 5");

if (td_s1 === -1 || td_s2 === -1 || td_s3 === -1 || td_s4 === -1 || td_s5 === -1 || td_s6 === -1) {
  throw new Error("TD detail sections missing: " + [td_s1, td_s2, td_s3, td_s4, td_s5, td_s6].join(", "));
}
if (!(td_s1 < td_s2 && td_s2 < td_s3 && td_s3 < td_s4 && td_s4 < td_s5 && td_s5 < td_s6)) {
  throw new Error("TD strict 5-step ordering violated!");
}
if (tdHtml.indexOf("SOMEONE") === -1 || tdHtml.indexOf("MER1T") === -1) {
  throw new Error("TD final roster players missing!");
}
print("  -> NA Past Team (TD) strict 5-section order & final roster verified!");

// 5. NA Past Team Detail: NTMR (Nightmare) 5-step ordering
state.team = 'NTMR';
var ntmrHtml = teamsPage();
var ntmr_s1 = ntmrHtml.indexOf("마지막 공식 로스터 (Final Roster)");
var ntmr_s2 = ntmrHtml.indexOf("구단 인수/합병 및 이적 연혁");
var ntmr_s3 = ntmrHtml.indexOf("코칭스태프 (Coaching Staff)");
var ntmr_s4 = ntmrHtml.indexOf("전장 유형별 최고 / 최저 승률 전장");
var ntmr_s5 = ntmrHtml.indexOf("Most Banned Against Top 5");
var ntmr_s6 = ntmrHtml.indexOf("Most Banned by [TEAM] Top 5");

if (ntmr_s1 === -1 || ntmr_s2 === -1 || ntmr_s3 === -1 || ntmr_s4 === -1 || ntmr_s5 === -1 || ntmr_s6 === -1) {
  throw new Error("NTMR detail sections missing: " + [ntmr_s1, ntmr_s2, ntmr_s3, ntmr_s4, ntmr_s5, ntmr_s6].join(", "));
}
if (!(ntmr_s1 < ntmr_s2 && ntmr_s2 < ntmr_s3 && ntmr_s3 < ntmr_s4 && ntmr_s4 < ntmr_s5 && ntmr_s5 < ntmr_s6)) {
  throw new Error("NTMR strict 5-step ordering violated!");
}
if (ntmrHtml.indexOf("Seicoe") === -1 || ntmrHtml.indexOf("scissors") === -1) {
  throw new Error("NTMR final roster players missing!");
}
print("  -> NA Past Team (NTMR) strict 5-section order & final roster verified!");

print("[6/6] Scanning for forbidden fictional hero names in rendered output...");
var forbiddenHeroes = ['Jetpack Cat', 'Vendetta', 'Mizuki', 'Shion', 'Domina'];
for (var f = 0; f < forbiddenHeroes.length; f++) {
  var hero = forbiddenHeroes[f];
  if (crHtml.indexOf(hero) !== -1 || ftgHtml.indexOf(hero) !== -1 || ssgHtml.indexOf(hero) !== -1 || tdHtml.indexOf(hero) !== -1) {
    throw new Error("Forbidden fictional hero found in output: " + hero);
  }
}
print("  -> Zero fictional hero names found in output!");

print("\n=== ALL TESTS PASSED SUCCESSFULLY! ===");

