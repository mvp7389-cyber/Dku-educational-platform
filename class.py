# ============================================================
#  DKU Educational Platform v4
#  흐름: 이름 입력 → 수준 선택 → 메뉴 1~5번 → FR 실행
#  수준(하위/중/상위권)에 따라 각 FR 콘텐츠가 달라짐
# ============================================================
import os
from collections import defaultdict


# ──────────────────────────────────────────────────────────────
# 취약 단원 누적 트래커 (FR-04용)
# ──────────────────────────────────────────────────────────────
class WeaknessTracker:
    def __init__(self):
        self._data: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    def record(self, student_name: str, unit: str):
        self._data[student_name][unit] += 1

    def get(self, student_name: str) -> dict[str, int]:
        return dict(self._data.get(student_name, {}))

    def has_data(self, student_name: str) -> bool:
        return bool(self._data.get(student_name))


# ──────────────────────────────────────────────────────────────
# FR-01 : 학사 일정 및 시간표 동기화
# ──────────────────────────────────────────────────────────────
class FR01_ScheduleService:
    # 수준별 시간표 구성이 다름
    SCHEDULE_BY_LEVEL = {
        "하위권": [
            {"날짜": "05/19(월)", "내용": "기초 수학 보충수업 (방과 후 4시)"},
            {"날짜": "05/21(수)", "내용": "국어 기본 독해 특강"},
            {"날짜": "05/23(금)", "내용": "1학년 전체 모의고사"},
        ],
        "중위권": [
            {"날짜": "05/19(월)", "내용": "중간고사 성적 발표"},
            {"날짜": "05/21(수)", "내용": "수학 심화 보충수업 (방과 후 5시)"},
            {"날짜": "05/23(금)", "내용": "1학년 전체 모의고사"},
        ],
        "상위권": [
            {"날짜": "05/20(화)", "내용": "수능 대비 자율학습 (야간 자습 필참)"},
            {"날짜": "05/22(목)", "내용": "킬러 문항 집중 세미나"},
            {"날짜": "05/23(금)", "내용": "1학년 전체 모의고사"},
        ],
    }
    TIMETABLE = {
        "월": ["수학", "국어", "영어", "과학", "역사"],
        "화": ["영어", "수학", "체육", "국어", "음악"],
        "수": ["과학", "수학", "국어", "미술", "영어"],
        "목": ["역사", "영어", "수학", "국어", "과학"],
        "금": ["국어", "체육", "영어", "수학", "자율"],
    }

    def run(self, level: str):
        print(f"\n📅 [FR-01] 학사 일정 및 시간표 동기화 ({level} 맞춤)")
        print("─" * 50)
        print("▶ 이번 주 주요 일정")
        for item in self.SCHEDULE_BY_LEVEL[level]:
            print(f"  {item['날짜']}  {item['내용']}")
        print("\n▶ 요일별 시간표 조회 (종료: q)")
        while True:
            day = input("  조회할 요일 (월~금): ").strip()
            if day == "q":
                break
            subjects = self.TIMETABLE.get(day)
            if subjects:
                print("  " + " → ".join(f"{i+1}교시 {s}" for i, s in enumerate(subjects)))
            else:
                print("  ❌ 월/화/수/목/금 중 하나를 입력해주세요.")
        print("  ✅ 시간표 조회 완료. 메뉴로 돌아갑니다.")


# ──────────────────────────────────────────────────────────────
# FR-02 : 문제 이미지 인식 및 해설 제공
# ──────────────────────────────────────────────────────────────
class FR02_ImageService:
    MOCK_BY_LEVEL = {
        "하위권": {
            "문제 유형": "이차방정식 기본 풀이",
            "핵심 개념": "근의 공식: x = (-b ± √(b²-4ac)) / 2a",
            "풀이 요약": "① 계수 식별 → ② 판별식 계산 → ③ 근 산출",
            "난이도": "기본",
            "추천 다음 단계": "인수분해 반복 훈련",
        },
        "중위권": {
            "문제 유형": "함수의 극한과 연속",
            "핵심 개념": "좌극한·우극한 일치 여부 → 연속 판별",
            "풀이 요약": "① 불연속 후보점 탐색 → ② 좌/우극한 계산 → ③ 함숫값 비교",
            "난이도": "중급",
            "추천 다음 단계": "연속함수 심화 문제 10선",
        },
        "상위권": {
            "문제 유형": "합성함수 미분 + 극값 추론",
            "핵심 개념": "chain rule: (f∘g)' = f'(g(x))·g'(x)",
            "풀이 요약": "① 합성 구조 파악 → ② chain rule 적용 → ③ 극값 조건 연립",
            "난이도": "준킬러",
            "추천 다음 단계": "2025 수능 미적분 29·30번 도전",
        },
    }
    UNIT_MAP = {"1": "방정식", "2": "함수", "3": "수열", "4": "확률", "5": "미분", "6": "기타"}

    def run(self, level: str, student_name: str, tracker: WeaknessTracker):
        print(f"\n🖼️  [FR-02] 문제 이미지 인식 및 해설 제공 ({level} 맞춤)")
        print("─" * 50)
        image_path = input("  분석할 문제 이미지 경로를 입력하세요: ").strip()
        if not os.path.exists(image_path):
            print("  ⚠️  파일 없음 — 데모 해설을 제공합니다.")

        result = self.MOCK_BY_LEVEL[level]
        print("\n  ✅ 이미지 분석 완료")
        for k, v in result.items():
            print(f"  {k}: {v}")

        # 취약 단원 질문 → FR-04 트래커에 기록
        print("\n  📝 이 문제에서 가장 어려웠던 단원은?")
        print("  " + "  ".join(f"[{k}] {v}" for k, v in self.UNIT_MAP.items()))
        while True:
            c = input("  번호 입력 (1~6): ").strip()
            if c in self.UNIT_MAP:
                unit = self.UNIT_MAP[c]
                tracker.record(student_name, unit)
                print(f"  ✅ '{unit}' — FR-04 리포트에 기록됐습니다.")
                break
            print("  ❌ 1~6 중 하나를 입력해주세요.")


# ──────────────────────────────────────────────────────────────
# FR-03 : 맞춤형 학습 로드맵 추천
# ──────────────────────────────────────────────────────────────
class FR03_RoadmapService:
    ROADMAP_DB = {
        "하위권": [
            "STEP 1 (2주) — 중학 수학 핵심 개념 복습 (방정식·함수 기초)",
            "STEP 2 (2주) — 수학II 기본 문제 반복 (오답 없을 때까지)",
            "STEP 3 (3주) — EBS 수능특강 기본편 1회독",
            "STEP 4 (1주) — 틀린 문제 유형 분류 및 재풀이",
        ],
        "중위권": [
            "STEP 1 (1주) — 수1·수2 취약 단원 집중 점검",
            "STEP 2 (2주) — 준킬러 유형 집중 공략 (4점 문제 50선)",
            "STEP 3 (2주) — 선택과목 실전 세트 반복",
            "STEP 4 (2주) — 시간 단축 훈련 + 실전 모의",
        ],
        "상위권": [
            "STEP 1 (1주) — 킬러 문항 오답 패턴 분석",
            "STEP 2 (2주) — 수능 기출 15개년 킬러 집중 재풀이",
            "STEP 3 (2주) — 변형 문제·시중 킬러 세트 풀이",
            "STEP 4 (1주) — 실전 모의 + 멘탈 관리 전략 수립",
        ],
    }

    def run(self, level: str, student_name: str, tracker: WeaknessTracker):
        print(f"\n🗺️  [FR-03] 맞춤형 학습 로드맵 추천 ({level} 맞춤) — {student_name} 학생")
        print("─" * 50)

        # 취약 단원 질문 → 트래커 기록
        unit_map = {"1": "수열", "2": "미분", "3": "정적분", "4": "삼각함수", "5": "확률", "6": "함수의 극한"}
        print("  📝 지금 가장 어렵게 느끼는 단원을 선택하세요.")
        print("  " + "  ".join(f"[{k}] {v}" for k, v in unit_map.items()))
        while True:
            c = input("  번호 입력 (1~6): ").strip()
            if c in unit_map:
                unit = unit_map[c]
                tracker.record(student_name, unit)
                print(f"  ✅ '{unit}' — FR-04 리포트에 기록됐습니다.")
                break
            print("  ❌ 1~6 중 하나를 입력해주세요.")

        roadmap = self.ROADMAP_DB[level]
        print(f"\n  📋 [{level}] 맞춤 학습 로드맵")
        for step in roadmap:
            print(f"    ✦ {step}")


# ──────────────────────────────────────────────────────────────
# FR-04 : 취약 단원 시각적 리포트 조회
# ──────────────────────────────────────────────────────────────
class FR04_ReportService:
    @staticmethod
    def _bar(score: int, width: int = 28) -> str:
        filled = int(score / 100 * width)
        return "[" + "█" * filled + "░" * (width - filled) + f"] {score:>3}%"

    def run(self, student_name: str, tracker: WeaknessTracker):
        print(f"\n📊 [FR-04] 취약 단원 시각적 리포트 — {student_name} 학생")
        print("─" * 58)
        data = tracker.get(student_name)

        if not data:
            print("  ⚠️  아직 기록된 데이터가 없습니다.")
            print("  💡 FR-02·03·05를 먼저 실행하면 취약 단원이 자동으로 누적됩니다.")
            return

        max_cnt = max(data.values())
        scores = {u: max(20, 75 - int((cnt / max_cnt) * 55)) for u, cnt in data.items()}
        sorted_units = sorted(scores.items(), key=lambda x: x[1])

        print(f"  {'단원':<16} {'정답률 추정':<36} {'선택 횟수'}")
        print(f"  {'─'*16} {'─'*36} {'─'*6}")
        for unit, score in sorted_units:
            cnt   = data[unit]
            bar   = self._bar(score)
            warn  = " ⚠️  집중 보완" if score < 50 else ""
            print(f"  {unit:<16} {bar}{warn}  x{cnt}회")

        weakest = sorted_units[0]
        print(f"\n  🔎 최우선 보완 단원 : '{weakest[0]}' (정답률 추정 {weakest[1]}%)")
        print(f"  📌 총 누적 기록 수  : {sum(data.values())}회")
        print("─" * 58)


# ──────────────────────────────────────────────────────────────
# FR-05 : 고난도 변형 문제 큐레이션
# ──────────────────────────────────────────────────────────────
class FR05_CurationService:
    CURATION_DB = {
        "1": {
            "name": "미분",
            "difficulty": "준킬러/킬러",
            "source": "2025 수능 미적분 30번",
            "title": "삼각함수·합성함수 미분법으로 극대점 추론",
            "stats": "오답률 88%",
            "ebsi": "https://www.ebsi.co.kr/ebs/xip/xipa/retrieveScrpPrbAnsw.ebs?prbId=24수능수학미적30",
            "blogs": [
                ("수학올인 블로그", "https://suhakallin.com/255"),
                ("LY4I 블로그",    "https://ly4i.com/post/csat-november-2024-math-part3/"),
            ],
        },
        "2": {
            "name": "정적분",
            "difficulty": "준킬러",
            "source": "2025 6월 모의 공통 14번",
            "title": "정적분으로 정의된 함수의 극대·극소",
            "stats": "오답률 71%",
            "ebsi": "https://www.ebsi.co.kr/ebs/xip/xipa/retrieveScrpPrbAnsw.ebs?prbId=2406수학공통14",
            "blogs": [
                ("수학올인 블로그 (6월 모의 15번 연계)", "https://suhakallin.com/216"),
                ("호랭이닷컴 문제·해설 모음",            "https://horaeng.com/279"),
            ],
        },
        "3": {
            "name": "수열",
            "difficulty": "킬러",
            "source": "2025 수능 공통 22번",
            "title": "귀납적 정의 수열에서 첫째항 추론",
            "stats": "오답률 84%",
            "ebsi": "https://www.ebsi.co.kr/ebs/xip/xipa/retrieveScrpPrbAnsw.ebs?prbId=24수능수학공통22",
            "blogs": [
                ("수학올인 블로그",  "https://suhakallin.com/256"),
                ("LYC-MATH 해설",   "https://lyc-math-hww.com/entry/2024%EB%85%84-%EC%8B%9C%ED%96%89-%EA%B3%A03-%EC%88%98%EB%8A%A5-%EC%88%98%ED%95%99-22%EB%B2%88-%ED%95%B4%EC%84%A4"),
                ("오르비 손풀이",   "https://orbi.kr/00069916044"),
            ],
        },
        "4": {
            "name": "함수의 극한",
            "difficulty": "준킬러",
            "source": "2025 9월 모의 공통 15번",
            "title": "연속성·미분가능성 조건을 통한 함수 추론",
            "stats": "오답률 69%",
            "ebsi": "https://www.ebsi.co.kr/ebs/xip/xipa/retrieveScrpPrbAnsw.ebs?prbId=2409수학공통15",
            "blogs": [
                ("수학올인 블로그 (9월 모의 15번)", "https://suhakallin.com/223"),
                ("수학올인 블로그 (9월 모의 21번)", "https://suhakallin.com/222"),
            ],
        },
        "5": {
            "name": "확률과 통계",
            "difficulty": "준킬러",
            "source": "2025 수능 확률과통계 29번",
            "title": "조건부확률·독립시행 결합 고난도 문항",
            "stats": "오답률 65%",
            "ebsi": "https://www.ebsi.co.kr/ebs/xip/xipa/retrieveScrpPrbAnsw.ebs?prbId=24수능수학확통29",
            "blogs": [
                ("오르비 수능 수학 총평 (확통 29번 분석)", "https://orbi.kr/00069916025"),
                ("오르비 수능 수학 손풀이",                "https://orbi.kr/00070034733"),
            ],
        },
        "6": {
            "name": "기하",
            "difficulty": "킬러",
            "source": "2025 6월 모의 기하 30번",
            "title": "평면벡터 내적 최댓값·최솟값 기하학적 추론",
            "stats": "오답률 78%",
            "ebsi": "https://www.ebsi.co.kr/ebs/xip/xipa/retrieveScrpPrbAnsw.ebs?prbId=2406수하기하30",
            "blogs": [
                ("수학올인 블로그 (6월 모의 미적 30번 연계)", "https://suhakallin.com/212"),
                ("나무위키 2025수능 의견 (기하 분석)",        "https://namu.wiki/w/2025%ED%95%99%EB%85%84%EB%8F%84%20%EB%8C%80%ED%95%99%EC%88%98%ED%95%99%EB%8A%A5%EB%A0%A5%EC%8B%9C%ED%97%98/%EC%9D%98%EA%B2%AC"),
            ],
        },
    }

    # 수준별 안내 메시지
    LEVEL_MSG = {
        "하위권": "⚠️  아직 기초가 우선입니다. 개념을 이해한 뒤 도전해보세요.",
        "중위권": "💪 준킬러 문항부터 차근차근 정복해봅시다!",
        "상위권": "🔥 킬러 문항을 저격합니다. 집중하세요!",
    }

    def run(self, level: str, student_name: str, tracker: WeaknessTracker):
        print(f"\n🎯 [FR-05] 고난도 변형 문제 큐레이션 ({level} 맞춤) — {student_name} 학생")
        print(f"  {self.LEVEL_MSG[level]}")
        print("─" * 58)
        print("  📝 취약하다고 느끼는 단원을 선택하세요.")
        print("  [1] 미분  [2] 정적분  [3] 수열  [4] 함수의 극한  [5] 확률과 통계  [6] 기하")
        print("─" * 58)

        while True:
            c = input("  번호 입력 (1~6): ").strip()
            if c in self.CURATION_DB:
                break
            print("  ❌ 1~6 중 하나를 입력해주세요.")

        sol = self.CURATION_DB[c]
        tracker.record(student_name, sol["name"])
        print(f"  ✅ '{sol['name']}' — FR-04 리포트에 기록됐습니다.")
        print(f"\n  [📊 분석 완료] '{sol['name']}' 단원 취약점 감지")
        print("  " + "=" * 62)
        print(f"  🎯 추천 유형 : {sol['difficulty']} 피드백 문항")
        print(f"  📌 문항 특징 : {sol['title']}")
        print(f"  📌 실제 출처 : {sol['source']} ({sol['stats']})")
        print(f"  🔗 EBSi 링크 : {sol['ebsi']}")
        print(f"\n  📚 풀이 참고 출처")
        for i, (name, url) in enumerate(sol["blogs"], 1):
            print(f"     [{i}] {name}")
            print(f"         {url}")
        print("  " + "=" * 62)


# ──────────────────────────────────────────────────────────────
# 메인 플랫폼
# ──────────────────────────────────────────────────────────────
class DKUEducationalPlatform:
    LEVELS = {"1": "하위권", "2": "중위권", "3": "상위권"}
    MENU   = {
        "1": "학사 일정 및 시간표 동기화      (FR-01)",
        "2": "문제 이미지 인식 및 해설 제공  (FR-02)",
        "3": "맞춤형 학습 로드맵 추천         (FR-03)",
        "4": "취약 단원 시각적 리포트 조회   (FR-04)",
        "5": "고난도 변형 문제 큐레이션       (FR-05)",
    }

    def __init__(self):
        self.tracker   = WeaknessTracker()
        self.fr01      = FR01_ScheduleService()
        self.fr02      = FR02_ImageService()
        self.fr03      = FR03_RoadmapService()
        self.fr04      = FR04_ReportService()
        self.fr05      = FR05_CurationService()

    @staticmethod
    def _ask(prompt: str, valid: list) -> str:
        while True:
            v = input(prompt).strip()
            if v in valid:
                return v
            print(f"  ❌ {valid} 중 하나를 입력해주세요.")

    def _print_menu(self, level: str):
        print(f"\n{'─'*52}")
        print(f"  📋 메뉴 [{level}]")
        print(f"{'─'*52}")
        for k, desc in self.MENU.items():
            print(f"  [{k}] {desc}")
        print(f"  [0] 종료")
        print(f"{'─'*52}")

    def run(self):
        print("\n" + "=" * 52)
        print("   🏫  DKU 고등학교 교육 플랫폼")
        print("=" * 52)

        # 이름 입력
        while True:
            name = input("👤 학생 이름을 입력하세요: ").strip()
            if name:
                break
            print("  ❌ 이름을 입력해주세요.")

        # 수준 선택
        print(f"\n  안녕하세요, {name} 학생!")
        print("  현재 본인의 학습 수준을 선택하세요:")
        for k, v in self.LEVELS.items():
            print(f"  [{k}] {v}")
        level_key = self._ask("  번호 입력 (1~3): ", ["1", "2", "3"])
        level     = self.LEVELS[level_key]
        print(f"\n  ✅ {level} 모드로 진입합니다.\n")

        # 메뉴 루프
        while True:
            self._print_menu(level)
            choice = self._ask("  번호를 선택하세요: ", ["0", "1", "2", "3", "4", "5"])

            if choice == "0":
                print(f"\n  👋 {name} 학생, 오늘도 수고했어요! 파이팅!\n")
                break
            elif choice == "1":
                self.fr01.run(level)
            elif choice == "2":
                self.fr02.run(level, name, self.tracker)
            elif choice == "3":
                self.fr03.run(level, name, self.tracker)
            elif choice == "4":
                self.fr04.run(name, self.tracker)
            elif choice == "5":
                self.fr05.run(level, name, self.tracker)


# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    platform = DKUEducationalPlatform()
    platform.run()