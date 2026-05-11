# Dku-educational-platform
플랫폼을 구성하기 위해서 필요한 것들의 모임 입니다,

### 📊 시스템 유스케이스 다이어그램

```mermaid
usecaseDiagram
    actor "임수민(하위권)" as StudentC
    actor "이정훈(중위권)" as StudentB
    actor "안치용(상위권)" as StudentA

    package "고등학교 교육 플랫폼" {
        usecase "학사 일정 및 시간표 동기화 (FR-01)" as UC1
        usecase "문제 이미지 인식 및 해설 제공 (FR-02)" as UC2
        usecase "맞춤형 학습 로드맵 추천 (FR-03)" as UC3
        usecase "취약 단원 시각적 리포트 조회 (FR-04)" as UC4
        usecase "고난도 변형 문제 큐레이션 (FR-05)" as UC5
    }

    StudentC --> UC1
    StudentC --> UC2
    StudentB --> UC3
    StudentA --> UC5
```
