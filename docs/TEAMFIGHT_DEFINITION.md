# Teamfight Definition (한타 정의)

Status: definition finalized by the project author, 2026-10-09. Not yet published.
Scope: OWCS Korea 2026 Stage 3, Weeks 1–2.

This is the author's annotation standard for the manually recorded `TEAMFIGHT INFO` sheet.
It is written in the author's own terms. An English summary goes into `docs/METHODOLOGY.md` when the teamfight section is published.

## 1. 정의

- 한타란 두 팀이 거점/화물/로봇의 주도권을 가져오기 위해 벌이는 싸움이다.
- 교전은 한 군데에서만 일어나지 않고 2~3군데에서 동시에 일어날 수 있다.
- 꼭 5 vs 5 구도가 아니어도 된다. 4 vs 5, 3 vs 5도 한타로 간주한다.
- 정면이 아닌 사이드 싸움의 승/패는 따로 기록하지 않는다. 사이드 싸움의 결과는 결국 본대 한타의 승패에 반영된다.

## 2. 시작

- 게임 시작 직후의 첫 교전도 한타로 센다.
- 그다음 한타는 한쪽이 자리를 잡고 있고 다른 한쪽이 reengage하는 시점에 시작한다.
- reengage 과정(spawn → point)에서 일방적인 킬이 일어나 다시 reengage를 시작한다면, 그 과정은 한타로 보지 않는다.

## 3. 같은 한타 / 새 한타

다음 경우는 하나의 한타(sequence)로 본다.

- 한타가 길어져서, 초반에 이탈했던 인원이 재합류해 싸움을 이어가는 경우
- 거점 주변에서 이탈 인원의 재합류를 기다렸다가 바로 다시 들어가는 경우
- 초반에 상대의 자원(스킬, 궁극기 등)을 뺀 뒤 뒤로 빠져 재정비하고 다시 치고 나가는 과정에서 거점이 잠시 넘어가는 경우. 이는 한타의 패배가 아니라 한타의 과정으로 본다.
- 마지막 순간에 비비는 한타 같은 특수한 경우. 이때는 spawn 근처에서 reengage를 하지 않으므로 하나로 잡는다.

다음 경우는 새 한타로 본다.

- spawn 근처에서 재정비한 뒤 다시 들어가는 경우
- 여기서 "spawn 근처"란 상대와 교전이 일어나지 않는 위치를 말한다.

## 4. 종료와 승자

- 한타는 어느 한쪽이 거점/화물/로봇의 주도권을 유지하거나 되찾아오면 끝난다.
- 승자는 최종적으로 주도권을 쥔 쪽이다.
- 무승부는 없다.
- 한타 도중 되돌릴 수 없는 결과가 나오면(예: 라운드 종료, 경유지 도달, 거점 점령 완료), 이득을 본 쪽이 승자다.
- 중립 상태에서 시작한 한타는 처음 주도권을 쥔 쪽이 승자다.

## 5. 기록

- 조합은 교전이 시작되는 시점의 조합을 기록한다.
- 기록은 한 명의 기록자가 VOD를 보고 수동으로 판정한 결과이다.

- 맵 기록 완료 여부는 `TEAMFIGHT INFO` 시트 맨 오른쪽의 `Map Complete` 열에 표시한다.

## 6. 집계 기준

- 팀별 한타 승률: 최소 표본 없음. 항상 한타 수(n)를 함께 표시한다.
- 조합별 한타 승률: 10 teamfights 이상인 조합만 순위에 포함한다.

## 7. Open Items

- Maps recorded before this definition was finalized (9 maps in Week 1): the author re-checks them personally.
