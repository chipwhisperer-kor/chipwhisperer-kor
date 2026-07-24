# AI_ROSTER — 바인딩 · 쓰기 소유

`role_id` = 안정 식별자. **서비스명 = 교체 가능한 바인딩.**

## 활성 역할

| 순서 | role_id | 서비스 | 직함 | 관여 |
|------|---------|--------|------|------|
| 1 | `curator` | Codex | 학술정보·연구자산 큐레이터 | 상시 |
| 2 | `analyst` | Grok | 연구문헌 심층분석가 | 상시 |
| 3 | `producer` | Agy | Marp 프레젠테이션 프로듀서 | 상시 |
| — | `director` | Claude | 연구 프로젝트 총괄 디렉터 | **호출 시** (`roles/director/ROLE.md` 호출 시점) |

```text
                    director  ── 규격 정의 · 단계 승인/반려 · 충돌 최종 결정
                       ┆ (호출 시에만)
curator ──→ analyst ──→ producer ──→ 사용자
```

`director`는 파이프라인 **외부**다. 순서에 끼지 않으며, 호출되지 않은 동안 세 역할은 정상 진행한다.

## 단독 쓰기

| role_id | 단독 쓰기 | 비고 |
|---------|-----------|------|
| `curator` | `Papers/**`, `roles/curator/**`, `To_Do_Curator.md` | 자산 카탈로그 `Papers/ASSET_CATALOG.md` 포함. **신규 `paper_id` 발급**(D43) — analyst는 발급된 ID로 `META.md` 작성 |
| `analyst` | `.Intermediate_Artifacts/papers/**`, `roles/analyst/**`, `To_Do_Analyst.md` | Intermediate **전체** 아님 |
| `producer` | `Presentation_Marp/**`, `roles/producer/**`, `To_Do_Producer.md`, `style_enhancer.py` | |
| `director` | `roles/director/**`, `To_Do_Director.md`, `CROSS_CHECK.md`, `SYNC.md`, **공통 정책 문서** | 공통 = `PROMPT`·`README`·`AI_ROSTER`·`ARTIFACT_CONTRACTS`·`BOOTSTRAP_PROMPT`·`AGENTS`·`DECISIONS` (D42로 curator에서 이관). `SYNC.md`는 **작업 루트 선언**·절대경로 유일 허용처 (D49) |

접점 파일 `To_Do_<Role>.md`는 **공유가 아니다.** 사용자만 `## 사용자 답변 칸`에 쓰고, 타 역할은 쓰지 않는다 (`PROMPT` §8.1).

## 공유 (행·섹션 규칙)

| 경로 | 규칙 |
|------|------|
| `.Intermediate_Artifacts/HANDOFF.md` | 송·수신 상태 전이 (`ARTIFACT_CONTRACTS`) |
| `MILESTONES` · `ROADMAP` | 자기 책임 행만. M-항목 `done` 전환은 **director 승인 근거** 필요 (PROMPT §8.2) |

## 바인딩 변경

1. 사용자 지시 → 본 표 수정  
2. `roles/*/ROLE.md`의 “현재 서비스” 한 줄 동기  
3. `DECISIONS`에 D-기록 · 해당 `To_Do_<Role>.md` 상태 한 줄  
4. 열린 HANDOFF의 from/to 유효성 확인  

축소/확장: **활성 역할** 표에서 역할 제거·추가 + `roles/<role_id>/` 패키지 + `To_Do_<Role>.md` 접점 파일.

## 세션 역할 확정

1. 본 표에서 **현재 서비스명 ↔ active role_id**
2. 표에 없는 AI(신규·교체)는 사용자 지시로 **표에 먼저 추가**한 뒤 그 role_id로 행동
3. 불명이면 **어떤 파일도 쓰지 않고 대화로 확인 후 대기**  
   — 접점 파일은 모두 역할 소유이므로, 역할 미확정 AI는 쓸 수 있는 파일이 없다

사용자 작업 지시는 role_id의 **업무**를 정하지만 임시로 다른 역할을 겸임하게 만들지 않는다.
