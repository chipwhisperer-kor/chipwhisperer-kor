# Paper-Deep-Dive

논문·관련 자산을 **수집·검증**하고, 근거가 추적되는 **심층 분석**을 거쳐 **한글 Marp** 발표자료로 만든다.  
3-AI 파이프라인 + 총괄 디렉터(서비스 바인딩은 교체 가능).

## 역할

| 순서 | role_id | 현재 서비스 | 직함 | 단독 쓰기 |
|------|---------|-------------|------|-----------|
| 1 | `curator` | Codex | 학술정보·연구자산 큐레이터 | `Papers/**`, `roles/curator/**`, `To_Do_Curator.md` |
| 2 | `analyst` | Grok | 연구문헌 심층분석가 | `.Intermediate_Artifacts/papers/**`, `roles/analyst/**`, `To_Do_Analyst.md` |
| 3 | `producer` | Agy | Marp 프레젠테이션 프로듀서 | `Presentation_Marp/**`, `roles/producer/**`, `To_Do_Producer.md`, `style_enhancer.py` |
| — | `director` | Claude | 연구 프로젝트 총괄 디렉터 | `roles/director/**`, `To_Do_Director.md`, `CROSS_CHECK.md`, 공통 정책 문서 |

```text
                 director  ── 규격 정의 · 단계 승인/반려 · 충돌 최종 결정
                    ┆ (호출 시에만 · 파이프라인 외부)
curator ──────→ analyst ──────→ producer ──────→ 사용자
수집·검증·정리    분석·해석      구조화·시각화·Marp
```

`director`는 **상시가 아니다.** 마일스톤 종료·규격 개정·상위 계층 변경·역할 충돌 때만 관여하고, 그 외에는 세 역할이 정상 진행한다. 산출물 내용은 직접 만들거나 고치지 않으며, 반려 시 **방향만** 제시한다. 호출 시점 → `roles/director/ROLE.md`.

역할 전문은 `BOOTSTRAP_PROMPT.md` / `roles/<role_id>/ROLE.md`에만 둔다. 여기·PROMPT에 장문 복붙하지 않는다.

## 두 명제 — 프로젝트 전체를 관통한다

**자기완결성 (Self-contained)** — 이 폴더만 넘겨받은 제3의 AI가 외부 정보 없이 이어받을 수 있어야 한다.
경로는 루트 기준 상대경로만 쓴다. 대화는 양방향으로 휘발되므로, 사용자 지시도 **AI의 보고도** 그 턴에 폴더 안 문서로 남긴다 — 사용자가 `To_Do_*.md`만 열어도 무슨 일이 있었고 무엇을 해야 하는지 알 수 있어야 한다.

**단순성 (Simplicity is the ultimate sophistication)** — 규칙을 늘려 문제를 덮지 않고 구조를 바꿔 문제가 생기지 않게 한다. 한 사실은 한 곳에, 기존 것을 먼저 쓰고, 안 쓰는 것은 지운다.

규칙 전문 → `PROMPT.md` **§0** (자기완결성 S1–S6 · 단순성 P1–P5).

## 문서 계층 (SSOT · 중복 금지)

폴더 안 모든 파일은 아래 셋 중 하나로 분류된다. **분류 없는 파일을 만들지 않는다** (S5).

### 운영 — 읽고 따른다

| 관심사 | 단일 기준 문서 | AI가 읽을 때 |
|--------|----------------|--------------|
| **작업 루트 선언** | `.Intermediate_Artifacts/SYNC.md` | **매 세션 제일 먼저** — 내가 올바른 사본에 있는지 대조 (S7) |
| 진입·지도 | **이 파일** | 최초 세션·구조 변경 시 |
| 에이전트 진입점 | `AGENTS.md` · `CLAUDE.md` | 해당 하네스가 자동 로드 (내용은 이 표의 축약) |
| 동일 시작 문구 | `BOOTSTRAP_PROMPT.md` | 최초 세션 |
| 자기완결성·공통 실행 계약 | `PROMPT.md` | 매 세션 |
| 바인딩·쓰기 소유 | `AI_ROSTER.md` | 매 세션 |
| 패킷·handoff 상태 | `ARTIFACT_CONTRACTS.md` | handoff 생성·소비 전 |
| 역할 행동 | `roles/<role_id>/ROLE.md` + `PROMPT.md` | 자기 역할만 |
| 사용자 지시 | `To_Do_<Role>.md` | 매 턴 (**자기 파일** 답변 칸) |
| 인계 큐 | `.Intermediate_Artifacts/HANDOFF.md` | 매 턴 |
| 연구 결정 로그 | `.Intermediate_Artifacts/DECISIONS.md` | 충돌 시 (번호 큰 쪽 우선) |
| 진행 상태 | `.Intermediate_Artifacts/MILESTONES.md` · `ROADMAP.md` | 필요 시 |
| 최종 교차검증·품질 판정 | `.Intermediate_Artifacts/CROSS_CHECK.md` | M7 (director 판정) |
| 자산 메타 규격·기록 | `Papers/ASSET_CATALOG_SCHEMA.md` · `ASSET_CATALOG.md` | curator 자산 작업 시 |
| Marp 문법·스타일 기준 | `Presentation_Marp/0. Template/presentation.md` | producer 슬라이드 작성 전 |

### 역사 — 읽지 않는다 (참고 이력, 현행 규칙 아님)

| 파일 | 비고 |
|------|------|
| `.Intermediate_Artifacts/COMMS/*` | 단일-AI 시절 내부 로그. **매 턴 갱신 의무 없음** (D41) |
| `.Intermediate_Artifacts/ARCHITECTURE_AUDIT_2026-07-23.md` | 당시 검수 기록 |
| `.Intermediate_Artifacts/ROSTER_STATE.md` | 폐기 포인터 — 소유는 `AI_ROSTER.md` |
| `Papers/reference-download-manifest.csv` | 레거시 파일 장부. 보존만, 소급 기입 안 함 |

### 산출물 — 역할 소유

`Papers/**` (curator) · `.Intermediate_Artifacts/papers/**` (analyst) · `Presentation_Marp/**` · `style_enhancer.py` (producer)

**충돌 시 우선순위** → `PROMPT.md` §6.

## 디렉터리

```text
Paper-Deep-Dive/                    # ← 프로젝트 루트. 모든 경로는 여기 기준 상대경로
├── README.md · BOOTSTRAP_PROMPT.md · PROMPT.md          # director 소유
├── AI_ROSTER.md · ARTIFACT_CONTRACTS.md · AGENTS.md · CLAUDE.md
├── To_Do_Curator.md · To_Do_Analyst.md · To_Do_Producer.md · To_Do_Director.md
├── roles/{curator,analyst,producer,director}/
├── Papers/                         # curator
├── .Intermediate_Artifacts/
│   ├── SYNC.md                     # ★ 운영 · director 단독 — 작업 루트 선언(S7). 매 세션 제일 먼저
│   ├── papers/                     # analyst 단독
│   ├── HANDOFF.md · MILESTONES.md · ROADMAP.md          # 공유(행 규칙)
│   ├── DECISIONS.md · CROSS_CHECK.md                    # director 단독
│   └── COMMS/ · ROSTER_STATE.md · ARCHITECTURE_AUDIT_*.md            # 역사
├── Presentation_Marp/              # producer
└── style_enhancer.py               # producer 보조 (루트에서 실행, 제자리 덮어쓰기)
```

`.Intermediate_Artifacts/` **전체**가 analyst 소유가 아니다. `papers/`만 analyst 단독.

동일한 요청을 여러 AI가 받아도 단독 쓰기 소유는 유지된다. 공통 정책 문서는 **director**가 소유하고, 나머지 역할은 자기 역할 문서만 고치거나 `to: director` handoff로 개정을 제안한다.

## 사용자

볼 파일은 **역할별 접점 4개** — `To_Do_Curator.md` · `To_Do_Analyst.md` · `To_Do_Producer.md` · `To_Do_Director.md`.
각 파일은 그 역할만 쓰므로 AI끼리 서로의 지시를 덮어쓸 수 없다. 사용자는 각 파일의 `## 사용자 답변 칸`에만 적는다.
`To_Do_Director.md`는 상시 역할이 아니어서 대부분 비어 있는 것이 정상이다.
완성된 발표자료는 `Presentation_Marp/<논문>/presentation.md`.
