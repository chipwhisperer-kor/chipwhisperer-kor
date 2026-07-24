# MILESTONES

갱신: 2026-07-24 · D42 director 신설
범례: pending | in_progress | awaiting_approval | done | blocked | deferred

**M-항목 `done` 전환은 `director` 승인 handoff를 근거로 한다** (`PROMPT` §8.2·§8.3). 각 역할은 자기 책임 행만 갱신한다.
어휘 주의 — 여기 범례는 **마일스톤 상태**다. handoff 상태(`draft`/`ready`/…)는 `ARTIFACT_CONTRACTS` §1, 분석 단위 상태(`pending`/`approved`/…)는 `PARAGRAPH_INDEX.md`. 셋은 별개 어휘다.

## 전역

| ID | 항목 | 상태 | 책임 |
|----|------|------|------|
| M0 | 공통 계약·역할·인계 | **done** | 사용자 부트스트랩 완료 |
| M-ARCH | 1-deep PDF 아카이브 | done | curator |
| M-TRACE | 추적·패킷 계약 v3 | done | 정책 |

## HAETAE-FIA

| ID | 상태 | 책임 | 비고 |
|----|------|------|------|
| H-M1 목차 | done | analyst | |
| H-M2 인덱스 | done | analyst | 73단위 |
| H-M3 본문 | blocked | analyst | P-014+, D25 |
| H-M4 그림 | pending | producer | |
| H-M5 REF | in_progress | 순차 | [11] done, [9] partial, [10][12] 대기 |
| H-M6 Marp | in_progress | producer | 레거시분 |
| H-M7 교차검증 | pending | 역할별 근거 → **director 판정** | `CROSS_CHECK.md` |
| H-M8 최종 | pending | 사용자 | director 단계 승인 후 |

### Dilithium deep-dive

| 단위 | 상태 |
|------|------|
| DIL-11 U1–U5 | done (레거시) |
| DIL-09 U1–U2 | done partial (레거시) |
| DIL-10 자산 패킷 | done → `HO-20260723-11` ready |
| sparse-c-NTT 1줄 | **awaiting_approval** (`To_Do_Analyst.md` 1건) |
| DIL-10 분석 | blocked (NTT 사용자 게이트) |
| DIL-12 | pending |

### 본문

P-001–013 approved · P-014 deferred · P-015–073 pending

## PCM-DFA

아카이브 done · 본문 deferred (D9)

## 포인터

- 사용자: sparse-c-NTT 한 줄
- curator: DIL-10 자산 완료
- analyst: `HO-20260723-11` ready; 사용자 게이트 후 DIL-10
- producer: 대기
- director: 미호출 (다음 관여 = D25 deep-dive 종료 또는 H-M5 완료 시 단계 판정)
