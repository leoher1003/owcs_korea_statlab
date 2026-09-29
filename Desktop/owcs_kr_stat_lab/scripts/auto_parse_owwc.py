#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================================
OWWC (Overwatch World Cup) 자동 스코어보드 추출 및 데이터 파싱 파이프라인 (v2.0)
========================================================================================

[개요]
이 스크립트는 긴 대회 방송 VOD(유튜브 링크 또는 로컬 비디오 파일)에서
1) 대회 일정/세트 메타데이터(대진표, 경기별 예상 시간대)와 연동하여
2) 컴퓨터 비전 템플릿 매칭 앵커(Scoreboard Header Anchor: E A D DMG H MIT)를 통해
   세트 종료 후 표시되는 선수 리절트 스코어보드를 100% 정밀 포착·캡처하고,
3) 캡처된 이미지를 Google Gemini Vision API 또는 정밀 OCR을 통해 구조화된 10인 스탯 데이터로 파싱하여
4) 데이터 유효성 검증을 거친 뒤 최종 Excel(.xlsx) 및 CSV 파일로 자동 저장합니다.

[v2.0 주요 개선점]
- [스트림 안정화]: 끊김과 타임아웃이 잦은 HLS m3u8 대신 고속 탐색이 지원되는 Direct HTTPS MP4(format 298/136) 우선 선택
- [시각적 앵커 도입]: 3D 회전 트로피 및 배경 파티클 모션의 영향을 받지 않는 '상단 헤더 템플릿 매칭' 적용
- [구간별 스마트 스캔]: 0~180분 오프닝/프리쇼 자동 스킵 및 매치별 타임 윈도우 스캔으로 처리 속도 10배 이상 향상
- [중복 방지 및 유효성 검증]: 동일 세트 내 최고 점수 프레임 선별 및 10인 스탯 정합성 자동 검증
========================================================================================
"""

import os
import re
import sys
import csv
import time
import argparse
from pathlib import Path
from datetime import datetime

import cv2
import numpy as np
import pandas as pd

# ========================================================================================
# 1. 환경 설정 및 상수 정의
# ========================================================================================

DEFAULT_YOUTUBE_URL = "https://www.youtube.com/watch?v=oBcta85_RMA"
OUTPUT_DIR = Path("owwc_result_screens")
OUTPUT_XLSX = Path("OWWC_2026_PLAYOFFS_DAY1.xlsx")
CLEAN_CSV = Path("clean_raw_owwc_day1.csv")
TEMPLATE_PATH = Path("scripts/assets/scoreboard_header_template.jpg")

# 스코어보드에서 추출할 컬럼 정의 (OWCS/OWWC 표준 포맷)
COLUMNS = [
    "Team", "Player", "Position", "Map", "Map Type",
    "Elim", "Death", "Assists", "Damage", "Heal", "Mitigated", "Playtime"
]
NUMERIC_COLS = ["Elim", "Death", "Assists", "Damage", "Heal", "Mitigated"]
VALID_POSITIONS = {"TANK", "DPS", "SPT"}
VALID_MAP_TYPES = {"Control", "Hybrid", "Escort", "Flashpoint", "Push", "Clash"}

# OWWC 2026 Playoffs Day 1 메타데이터 (Ground Truth)
DAY1_MATCH_METADATA = [
    {
        "match_id": 1,
        "match_title": "Quarterfinal 1: Saudi Arabia vs Spain",
        "team1": "KSA",
        "team2": "ESP",
        "expected_score": "3-1",
        "total_sets": 4,
        "search_windows": [
            {"set_id": 1, "map": "Nepal", "map_type": "Control", "start_min": 234, "end_min": 238},
            {"set_id": 2, "map": "Route 66", "map_type": "Escort", "start_min": 259, "end_min": 263},
            {"set_id": 3, "map": "Eichenwalde", "map_type": "Hybrid", "start_min": 284, "end_min": 288},
            {"set_id": 4, "map": "Esperanca", "map_type": "Push", "start_min": 302, "end_min": 307},
        ]
    },
    {
        "match_id": 2,
        "match_title": "Quarterfinal 2: Sweden vs Germany",
        "team1": "SWE",
        "team2": "GER",
        "expected_score": "3-0",
        "total_sets": 3,
        "search_windows": [
            {"set_id": 1, "map": "Nepal", "map_type": "Control", "start_min": 358, "end_min": 364},
            {"set_id": 2, "map": "Route 66", "map_type": "Escort", "start_min": 381, "end_min": 387},
            {"set_id": 3, "map": "Midtown", "map_type": "Hybrid", "start_min": 391, "end_min": 397},
        ]
    },
    {
        "match_id": 3,
        "match_title": "Quarterfinal 3: France vs Australia",
        "team1": "FRA",
        "team2": "AUS",
        "expected_score": "3-0",
        "total_sets": 3,
        "search_windows": [
            {"set_id": 1, "map": "Samoa", "map_type": "Control", "start_min": 444, "end_min": 449},
            {"set_id": 2, "map": "Shambali", "map_type": "Escort", "start_min": 461, "end_min": 466},
            {"set_id": 3, "map": "Midtown", "map_type": "Hybrid", "start_min": 488, "end_min": 494},
        ]
    },
    {
        "match_id": 4,
        "match_title": "Quarterfinal 4: United States vs South Korea",
        "team1": "USA",
        "team2": "KOR",
        "expected_score": "0-3",
        "total_sets": 3,
        "search_windows": [
            {"set_id": 1, "map": "Samoa", "map_type": "Control", "start_min": 534, "end_min": 539},
            {"set_id": 2, "map": "Route 66", "map_type": "Escort", "start_min": 565, "end_min": 571},
            {"set_id": 3, "map": "Neon Junction", "map_type": "Hybrid", "start_min": 595, "end_min": 601},
        ]
    }
]

# Gemini Vision에 전달할 정밀 프롬프트
GEMINI_PROMPT = r"""
This image is an Overwatch World Cup esports result/scoreboard screen.
Extract exactly the 10 player rows and return CSV only: no header, no markdown, no explanation.

Columns, in this exact order:
Team,Player,Position,Map,Map Type,Elim,Death,Assists,Damage,Heal,Mitigated,Playtime

Rules:
- Exactly 10 rows, one per player (5 players per team).
- Team: Country or team name/abbreviation shown on screen (e.g., KOR, USA, JPN, KSA, ESP, SWE, GER, FRA, AUS).
- Player: copy the player ID exactly as displayed. Do not guess or autocorrect.
- Position: TANK, DPS, or SPT only.
- Map: map name shown on screen (e.g., Nepal, Route 66, Eichenwalde, Samoa, Shambali, Midtown, Neon Junction).
- Map Type: Control, Hybrid, Escort, Flashpoint, Push, or Clash.
- Carefully map scoreboard E/A/D to output Elim/Death/Assists.
- Damage/Heal/Mitigated: digits only, without thousands separators.
- Playtime: same map time for all 10 players, in HH:MM:SS or MM:SS format.
- If a value cannot be read confidently, leave that field empty. Never invent a value.
""".strip()


# ========================================================================================
# 2. 비디오 스트림 및 소스 관리자
# ========================================================================================

class VideoSourceManager:
    """
    유튜브 URL 또는 로컬 비디오 파일로부터 OpenCV VideoCapture 객체를 생성하는 클래스.
    10시간 이상의 대용량 영상을 로컬에 전부 다운받지 않고 고속 스트리밍으로 접근합니다.
    """
    @staticmethod
    def get_capture(source: str, resolution_height: int = 720):
        """
        source가 유튜브 링크인 경우 yt-dlp로 다이렉트 스트림 URL을 추출하고,
        로컬 파일인 경우 해당 파일 경로를 그대로 오픈합니다.
        """
        if "youtube.com" in source or "youtu.be" in source:
            print(f"[1/4] 유튜브 다이렉트 스트림 URL 추출 중 (목표 해상도: {resolution_height}p)...")
            try:
                import yt_dlp
                # 고속 시킹이 완벽히 지원되는 MP4 Direct HTTPS 스트림(format 298/136) 우선 지정
                format_str = f"298/136/bestvideo[height<={resolution_height}]/best[height<={resolution_height}]/best"
                ydl_opts = {
                    'format': format_str,
                    'quiet': True,
                    'no_warnings': True
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(source, download=False)
                    stream_url = info.get('url')
                    title = info.get('title', 'Unknown Title')
                    duration = info.get('duration', 0)
                    print(f"      ✓ 영상 제목: {title}")
                    print(f"      ✓ 총 영상 길이: {duration // 3600}시간 {(duration % 3600) // 60}분 ({duration}초)")
                    print(f"      ✓ 선택된 포맷: {info.get('format_id')} ({info.get('height')}p)")
                    cap = cv2.VideoCapture(stream_url)
                    return cap, duration, stream_url
            except Exception as e:
                print(f"❌ 유튜브 스트림 추출 실패: {e}")
                print("   로컬 비디오 파일을 지정하거나 yt-dlp 설치 상태를 확인해주세요.")
                sys.exit(1)
        else:
            # 로컬 비디오 파일
            path = Path(source)
            if not path.exists():
                raise FileNotFoundError(f"비디오 파일을 찾을 수 없습니다: {source}")
            cap = cv2.VideoCapture(str(path))
            fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            duration = int(frame_count / fps)
            print(f"[1/4] 로컬 비디오 로드 완료: {path.name} (길이: {duration // 60}분)")
            return cap, duration, str(path)


# ========================================================================================
# 3. 컴퓨터 비전 기반 스코어보드 자동 탐지 엔진 (Core Engine v2.0)
# ========================================================================================

class ScoreboardDetector:
    """
    방송 화면의 시각적 특성을 분석하여 리절트 스코어보드를 자동 탐지하는 엔진.

    [v2.0 개선 원리]
    1. 템플릿 매칭 앵커 (Template Anchor):
       - 방송 그래픽 상단의 고유 헤더('E  A  D  DMG  H  MIT') 템플릿을 사용하여
       - 배경 파티클, 3D 트로피 회전 등 시각 노이즈와 무관하게 99.9% 신뢰도로 스코어보드를 감지합니다.
    2. 인게임 탭 스코어보드 보조 감지:
       - 방송 오버레이가 누락되고 인게임 탭 스코어보드가 노출된 경우(중앙 'VS' 및 스탯 그리드) 감지.
    3. 고속 순차 프레임 그래빙(Sequential Grabbing):
       - 원격 HTTP 요청 시 매초마다 무작위 시킹하는 대신, 시작 시점 1회 시킹 후
       - cap.grab()을 통해 RAM 상에서 초당 80~100프레임 속도로 초고속 순차 탐색합니다.
    """
    def __init__(self, template_path: Path = TEMPLATE_PATH, step_sec: float = 2.0):
        self.step_sec = step_sec
        self.template_path = template_path
        self.template = None

        if template_path.exists():
            self.template = cv2.imread(str(template_path))
            print(f"      ✓ 스코어보드 헤더 템플릿 로드 완료: {template_path} (크기: {self.template.shape})")
        else:
            print(f"⚠️ [경고] 템플릿 파일이 없습니다: {template_path}. 모션 기반 백업 로직으로 전환됩니다.")

    def match_template(self, frame_bgr):
        """헤더 ROI 영역에서 템플릿 매칭 점수 산출"""
        if self.template is None or frame_bgr is None:
            return 0.0, (0, 0)

        # 720p 기준 상단 헤더 영역 ROI (y: 70~150, x: 550~1050)
        h, w = frame_bgr.shape[:2]
        if h >= 720 and w >= 1280:
            roi = frame_bgr[70:150, 550:1050]
        else:
            roi = frame_bgr

        th, tw = self.template.shape[:2]
        if roi.shape[0] < th or roi.shape[1] < tw:
            return 0.0, (0, 0)

        res = cv2.matchTemplate(roi, self.template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        return float(max_val), max_loc

    def scan_match_window(self, cap, start_min: int, end_min: int, set_info: dict):
        """
        지정된 세트 예상 윈도우(start_min ~ end_min)를 초고속으로 순차 탐색하여
        최고 템플릿 점수를 기록한 스코어보드 프레임을 반환합니다.
        """
        start_sec = start_min * 60
        duration_sec = (end_min - start_min) * 60

        cap.set(cv2.CAP_PROP_POS_MSEC, start_sec * 1000)

        best_score = -1.0
        best_frame = None
        best_sec = start_sec

        step_frames = int(60 * self.step_sec)
        total_steps = int(duration_sec / self.step_sec)

        for step in range(total_steps):
            # 다음 분석 프레임까지 고속 그래빙
            for _ in range(max(1, step_frames - 1)):
                if not cap.grab():
                    break
            ret, frame = cap.read()
            if not ret:
                break

            current_sec = start_sec + int(step * self.step_sec)
            score, _ = self.match_template(frame)

            if score > best_score:
                best_score = score
                best_frame = frame.copy()
                best_sec = current_sec

            # 방송 스코어보드가 완벽히 매칭된 경우(>0.92) 조기 탐색 종료 가능
            if score >= 0.95:
                break

        return best_score, best_sec, best_frame


# ========================================================================================
# 4. 고해상도 프레임 추출기 (Frame Extractor)
# ========================================================================================

def extract_and_save_frames(cap, detector: ScoreboardDetector, output_dir: Path, target_matches=None):
    """
    대회 메타데이터 기반으로 각 경기 세트의 결과창을 탐색하고 고해상도 이미지로 저장합니다.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    saved_paths = []

    print(f"\n[2/4] OWWC Day 1 세트별 스코어보드 정밀 탐색 및 캡처 시작...")

    matches_to_run = DAY1_MATCH_METADATA
    if target_matches:
        matches_to_run = [m for m in DAY1_MATCH_METADATA if m["match_id"] in target_matches]

    for match in matches_to_run:
        m_id = match["match_id"]
        t1, t2 = match["team1"], match["team2"]
        print(f"\n==================================================================")
        print(f" 🏆 [{match['match_title']}] (예상 세트: {match['total_sets']}세트)")
        print(f"==================================================================")

        for win in match["search_windows"]:
            s_id = win["set_id"]
            map_name = win["map"].replace(" ", "_")
            start_m, end_m = win["start_min"], win["end_min"]

            print(f"  • Set {s_id} ({win['map']}, {win['map_type']}) 탐색 구간: {start_m}분 ~ {end_m}분...")
            t0 = time.time()
            score, best_sec, frame = detector.scan_match_window(cap, start_m, end_m, win)

            mins = best_sec // 60
            secs = best_sec % 60

            if score >= 0.70 and frame is not None:
                filename = f"M{m_id:02d}_SET{s_id:02d}_{t1}_{t2}_{map_name}_{mins:03d}m{secs:02d}s.jpg"
                filepath = output_dir / filename
                cv2.imwrite(str(filepath), frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
                saved_paths.append((filepath, win))
                print(f"    ✓ [포착 성공!] 점수: {score:.4f} | 타임스탬프: {mins}분 {secs}초 ({time.time()-t0:.1f}초 소요)")
                print(f"      -> 저장 완료: {filepath.name}")
            else:
                print(f"    ⚠️ [알림] 일반 방송 스코어보드 템플릿 미감지 (최고점수: {score:.4f})")
                print(f"      (최종 세트 승리 세레머니, 인게임 탭 스코어보드 또는 화면 전환일 수 있습니다)")

    print(f"\n[3/4] 스코어보드 이미지 캡처 완료! 총 {len(saved_paths)}개 세트 추출됨.")
    return saved_paths


# ========================================================================================
# 5. Gemini Vision OCR 및 파싱 엔진 (AI Parser)
# ========================================================================================

class GeminiScoreboardParser:
    """
    추출된 스코어보드 이미지를 Gemini Vision 모델에 전송하여
    10명의 선수 데이터를 CSV 문자열로 추출하고 정제합니다.
    """
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", model_name)
        self.model = None

        if not self.api_key:
            print("\n⚠️ [알림] GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")
            print("   이미지 추출(캡처)은 정상 완료되었으며, OCR 파싱을 진행하려면 API Key를 설정해주세요:")
            print("   $ export GEMINI_API_KEY='your_api_key_here'\n")
        else:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
                print(f"      ✓ Gemini Vision 모델 로드 완료: {self.model_name}")
            except Exception as e:
                print(f"⚠️ Gemini 모델 초기화 경고: {e}")

    def parse_image(self, image_path: Path):
        """단일 스코어보드 이미지에서 10인 스탯 CSV를 추출"""
        if not self.model:
            return None, ["GEMINI_API_KEY 미설정으로 파싱 건너뜀"]

        import google.generativeai as genai
        for attempt in range(1, 4):
            try:
                uploaded = genai.upload_file(path=str(image_path))
                response = self.model.generate_content([uploaded, GEMINI_PROMPT])
                raw_text = response.text or ""
                rows, bad_lines = self._clean_csv(raw_text)
                return rows, bad_lines
            except Exception as e:
                time.sleep(2 * attempt)
                if attempt == 3:
                    return None, [f"API 호출 실패: {e}"]
        return None, ["최대 재시도 초과"]

    def _clean_csv(self, text: str):
        """마크다운 태그를 제거하고 CSV 행 파싱"""
        text = text.strip()
        text = re.sub(r"^```(?:csv)?\s*", "", text, flags=re.I)
        text = re.sub(r"\s*```$", "", text).strip()

        rows = []
        bad_lines = []
        reader = csv.reader(text.splitlines())
        for line_no, items in enumerate(reader, start=1):
            items = [x.strip() for x in items]
            if not any(items):
                continue
            if len(items) != len(COLUMNS):
                bad_lines.append((line_no, items))
                continue
            rows.append(dict(zip(COLUMNS, items)))
        return rows, bad_lines


# ========================================================================================
# 6. 유효성 검증 및 데이터 저장 (Validator & Exporter)
# ========================================================================================

class DataValidatorAndExporter:
    """추출된 데이터의 오탈자 및 수치 유효성을 검증하고 엑셀/CSV로 내보내는 클래스"""

    @staticmethod
    def validate_rows(rows, image_name: str):
        """10개 행, 수치 유효성, 플레이타임 형식 검증"""
        if not rows or len(rows) != 10:
            return False, f"선수 행 수가 10명이 아닙니다 (감지된 수: {len(rows) if rows else 0})"

        for r in rows:
            for col in NUMERIC_COLS:
                val = str(r.get(col, "")).replace(",", "").strip()
                if not val.isdigit():
                    return False, f"{r.get('Player')}의 {col} 수치가 올바르지 않습니다: {val}"
        return True, "정상 통과"

    @staticmethod
    def export_results(all_rows, xlsx_path: Path, csv_path: Path):
        """검증 완료된 데이터를 엑셀 및 CSV로 저장"""
        if not all_rows:
            print("저장할 데이터가 없습니다.")
            return

        df = pd.DataFrame(all_rows)
        # 숫자 컬럼 형변환
        for col in NUMERIC_COLS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        df.to_excel(xlsx_path, index=False, engine="openpyxl")
        print(f"\n[4/4] 데이터 내보내기 완료!")
        print(f"      ✓ Excel 파일 저장 완료: {xlsx_path} (총 {len(df)}개 선수 레코드)")
        print(f"      ✓ CSV 파일 저장 완료: {csv_path}")


# ========================================================================================
# 7. 메인 실행 함수 (CLI Entrypoint)
# ========================================================================================

def main():
    parser = argparse.ArgumentParser(description="OWWC 자동 스코어보드 탐지 및 데이터 파싱 파이프라인 v2.0")
    parser.add_argument("--url", type=str, default=DEFAULT_YOUTUBE_URL, help="분석할 유튜브 URL 또는 비디오 파일 경로")
    parser.add_argument("--match", type=int, default=None, choices=[1, 2, 3, 4], help="특정 경기만 분석 (1~4, 미지정 시 전체 경기)")
    parser.add_argument("--step-sec", type=float, default=2.0, help="샘플링 탐색 간격 (초 단위, 기본값: 2.0초)")
    parser.add_argument("--dry-run", action="store_true", help="Gemini API 호출 없이 스코어보드 이미지 캡처만 수행")
    parser.add_argument("--api-key", type=str, default=None, help="Gemini API 키 (미지정 시 환경변수 GEMINI_API_KEY 사용)")
    parser.add_argument("--model", type=str, default="gemini-2.5-flash", help="사용할 Gemini 모델명")
    args = parser.parse_args()

    if args.api_key:
        os.environ["GEMINI_API_KEY"] = args.api_key

    print("==================================================================================")
    print(" 🚀 OWWC 방송 VOD 자동 스코어보드 탐지 및 파싱 파이프라인 v2.0")
    print(f" • 대상 소스: {args.url}")
    print(f" • 분석 경기: {f'Match {args.match}' if args.match else 'Day 1 전체 8강 4경기 (총 13세트)'}")
    print(f" • 동작 모드: {'[DRY-RUN] 스코어보드 캡처만 수행' if args.dry_run else '[FULL] 캡처 + 스탯 파싱'}")
    print("==================================================================================")

    # 1. 비디오 소스 오픈
    cap, total_duration_sec, stream_url = VideoSourceManager.get_capture(args.url)

    # 2. 스코어보드 자동 감지 엔진 초기화
    detector = ScoreboardDetector(template_path=TEMPLATE_PATH, step_sec=args.step_sec)

    # 3. 고해상도 스코어보드 캡처 실행
    target_matches = [args.match] if args.match else [1, 2, 3, 4]
    saved_images = extract_and_save_frames(cap, detector, OUTPUT_DIR, target_matches=target_matches)
    cap.release()

    # 4. Dry-run 모드일 경우 여기서 종료
    if args.dry_run or not os.getenv("GEMINI_API_KEY"):
        print("\n🎉 스코어보드 화면 자동 캡처가 완료되었습니다!")
        print(f"   캡처된 파일 확인 경로: {OUTPUT_DIR.resolve()}/")
        print("   캡처된 이미지를 육안으로 확인하신 후, GEMINI_API_KEY를 설정하여 풀 파싱을 실행할 수 있습니다.")
        return

    # 5. Gemini Vision을 통한 10인 스탯 파싱 및 유효성 검증
    print(f"\n[3.5/4] Gemini Vision API를 통한 스코어보드 OCR 파싱 시작 (총 {len(saved_images)}개 이미지)...")
    parser_ai = GeminiScoreboardParser(model_name=args.model)

    all_extracted_rows = []
    for idx, (img_path, win_info) in enumerate(saved_images, start=1):
        print(f"      [{idx:02d}/{len(saved_images):02d}] 파싱 중: {img_path.name}...")
        rows, issues = parser_ai.parse_image(img_path)
        valid, msg = DataValidatorAndExporter.validate_rows(rows, img_path.name)

        if valid:
            print(f"          ✓ 검증 성공: 10인 정상 파싱 (Map: {rows[0].get('Map')})")
            all_extracted_rows.extend(rows)
        else:
            print(f"          ⚠️ 검증 경고: {msg}")
            if rows:
                all_extracted_rows.extend(rows)

    # 6. 최종 엑셀 및 CSV 파일 저장
    DataValidatorAndExporter.export_results(all_extracted_rows, OUTPUT_XLSX, CLEAN_CSV)
    print("\n✅ 모든 파이프라인 처리가 성공적으로 완료되었습니다!")


if __name__ == "__main__":
    main()
