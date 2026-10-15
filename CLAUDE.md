# Project: [OWCS STAT LAB]

## Overview
Overwatch Champions Series (OWCS)의 스탯 랩 으로, open API가 없는 상황에서 중계 화면에 나오는 인게임 결과창의 정보를 수집하고, 분석하며 시각화 하는 웹사이트.

## Tech Stack
- Language: TypeScript (v5.x)
- Framework: Next.js 14 (App Router) / React
- Styling: Tailwind CSS (또는 Vanilla CSS / CSS Modules)
- Database: Supabase / PostgreSQL (또는 Prisma ORM / Local JSON)
- State & Data: TanStack Query (React Query) / Zustand

## Project Structure
src/ ├── app/ # Next.js App Router (페이지 및 라우트) │ ├── (routes)/ │ │ ├── matches/ # 매치별 결과 및 세트별 상세 스탯 페이지 │ │ ├── players/ # 선수 목록 및 개인 프로필/스탯 페이지 │ │ ├── teams/ # 팀 목록 및 팀 전적 페이지 │ │ ├── heroes/ # 영웅별 픽률, 승률 및 통계 페이지 │ │ ├── leaderboard/ # 포지션/지표별 리더보드 및 랭킹 │ │ └── admin/ # 인게임 결과창 업로드 및 데이터 검수/입력 페이지 │ ├── api/ # API 엔드포인트 (OCR 파싱, 스탯 CRUD 등) │ ├── layout.tsx # 공통 레이아웃 (네비게이션 바, 푸터) │ └── page.tsx # 메인 대시보드 (최근 경기, 주요 지표 요약) │ ├── components/ # UI 컴포넌트 │ ├── common/ # 공통 컴포넌트 (버튼, 모달, 테이블, 뱃지 등) │ ├── layout/ # 헤더, 사이드바, 네비게이션 │ ├── stats/ # 스탯 표, 선수 비교 카드, 포지션별 지표 뷰 │ ├── charts/ # 영웅 픽률/딜량/힐량 시각화 차트 │ └── admin/ # 중계 캡처 이미지 업로더, OCR 결과 확인/수정 폼 │ ├── lib/ # 외부 라이브러리 및 설정 │ ├── supabase/ # Supabase / DB 클라이언트 및 쿼리 함수 │ └── ocr/ # 중계 화면 텍스트 인식(OCR) 및 템플릿 매칭 로직 │ ├── types/ # TypeScript 타입 정의 │ ├── player.ts # 선수, 팀, 역할군(포지션) 타입 │ ├── match.ts # 매치, 세트, 맵 정보 타입 │ ├── stats.ts # 영웅별 세부 스탯 (처치, 데스, 딜량, 힐량 등) │ └── ocr.ts # 결과창 파싱 데이터 및 검수 상태 타입 │ ├── hooks/ # 커스텀 훅 │ ├── useStatsFilter.ts # 시즌/패치/포지션별 필터링 훅 │ └── usePlayerData.ts # 선수 스탯 쿼리 및 캐싱 훅 │ ├── utils/ # 순수 유틸리티 함수 │ ├── calculator.ts # 통계 지표 계산 공식 (10분당 스탯, K/D, 레이팅 등) │ ├── parser.ts # 인게임 결과창 텍스트/데이터 정규화 파서 │ └── formatters.ts # 시간, 숫자 콤마, K/D 소수점 포맷터 │ └── constants/ # 상수 데이터 ├── heroes.ts # 오버워치 영웅 목록 및 역할군 매핑 ├── maps.ts # 쟁탈/혼합/호위 등 모드별 전장 목록 └── seasons.ts # OWCS 시즌 및 대회 단계(Stage/Group) 정보
## Code Style Rules
- [ ] 커밋 메시지는 Conventional Commits 규칙 준수 (`feat:`, `fix:`, `refactor:`, `docs:` 등)
- [ ] TypeScript strict 모드 준수 (`any` 타입 지양, 명시적 인터페이스/타입 선언)
- [ ] 모든 복잡한 통계 계산/변환 유틸 함수에 JSDoc 주석 및 설명 추가
- [ ] `console.log` 대신 전역 logger 또는 디버그 유틸 사용
- [ ] 컴포넌트는 단일 책임 원칙(SRP)을 따르고, 비즈니스 로직은 hooks/utils로 분리
- [ ] 핵심 통계 계산 로직 및 유틸리티에 대한 단위 테스트 필수 작성

## Commands
- `npm run dev` - 개발 서버 실행 (로컬 환경: http://localhost:3000)
- `npm run build` - 프로덕션 빌드 생성
- `npm run start` - 프로덕션 빌드 서버 실행
- `npm run lint` - ESLint 코드 스타일 및 린트 검사
- `npm run test` - 단위 테스트(Vitest/Jest) 실행

## Important Notes
- **패치 버전별 데이터 분리**: 오버워치 밸런스 패치에 따라 스탯 가치가 달라지므로 시즌 및 패치 버전별 필터링 무결성을 유지해야 합니다.
- **선수/팀 메타데이터 동기화**: 선수 닉네임 변경 및 이적/로스터 변동 이력을 추적할 수 있도록 고유 ID 기반으로 데이터를 매핑합니다.
- **API Rate Limit 및 캐싱**: 경기 데이터 수집 및 외부 API 호출 시 요청 제한(Rate Limit)을 고려해 적절한 캐싱 전략(SWR/Next.js Data Cache)을 적용합니다.
- **환경 변수 보안**: Supabase/DB 연결 문자열 및 비공개 API Key는 반드시 `.env.local`로 관리하며 Git에 커밋하지 않습니다.
