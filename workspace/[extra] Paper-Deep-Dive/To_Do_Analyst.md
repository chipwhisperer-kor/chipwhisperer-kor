# To_Do_Analyst — 사용자 ↔ `analyst` 접점

`analyst` **단독 쓰기** · 사용자는 **답변 칸**.
채팅 키워드: **`계속`** = 이 파일 답변 칸 · **`초기화`** = 기억 폐기 후 폴더만 재부트스트랩 (`BOOTSTRAP_PROMPT.md`). 규칙은 `PROMPT.md` §8 · §3.5.

---

## 지금 상태

| | |
|--|--|
| 역할 | `analyst` = Grok (`AI_ROSTER.md`) |
| 작업 루트 | S7 대조 **OK** — `.Intermediate_Artifacts/SYNC.md` 선언과 일치 |
| 재부트스트랩 | **2026-07-24 `초기화` 완료** — 폴더만으로 재구성 · 연구 미착수 |
| 진행 | DIL-10 **미착수** — sparse-c-NTT 사용자 게이트 대기 |
| 병목 | 아래 「지금 할 일」1건 (파이프라인 연구 차단) |

### 자기 대상 handoff (`to: analyst`)

| id | 열 기준 status | 소비? | 비고 |
|----|----------------|-------|------|
| `HO-20260723-11` | `ready` | **게이트 후** | DIL-10 자산 3건. 레거시 `gate` 서술 형식(D44)이나 status=`ready` |
| `HO-20260724-04` | **`—` (9칸 밀림)** | **불가** | 의도 status는 끝에서 두 번째 칸 `ready`로 보이나, 8칸 규격상 status 자리=`—`. `HO-20260724-05` → curator 정정 대기 |
| `HO-20260724-01` | `done` | — | PROMPT 위생 완료 |

### 연구 위치 (`MILESTONES` · 본 파일)

| 단위 | 상태 |
|------|------|
| DIL-11 U1–U5 | done (레거시) |
| DIL-09 U1–U2 | done partial (레거시) |
| DIL-10 자산 | 패킷 ready (`HO-…-11`) |
| sparse-c-NTT 1줄 | **awaiting_approval** |
| DIL-10 분석 | blocked (위 게이트) |
| DIL-12 | pending (자산 handoff 형식 정정 후 · 순서는 DIL-10 다음) |
| 본문 P-014+ | blocked/deferred (D25 deep-dive 선행) |
| PCM-DFA | deferred (D9) |

순서: Dilithium deep-dive **[11]→[9]→[10]→[12]** (D25).

---

## 지금 할 일 (사용자) — 1건

### ☐ sparse-c-NTT 한 줄 반영 검토

**배경:** *Sign_internal* 에서 *NTT* 호출 (FIPS 204 Alg 7). 전용 슬라이드 삭제 후, NTT 호출 표 하단 **한 줄**만 유지 중.

**유지 문장(안):**
> L16 *SampleInBall* 로 $c$ 가 sparse 이어도, FIPS 204는 L17에서 $\mathrm{NTT}(c)$ 를 생략하지 않는다.

| 답변 칸 | 의미 |
|---------|------|
| **`승인`** / **`작업 계속`** | 한 줄 OK → `HO-20260723-11` 소비 · DIL-10 심층 1단위 |
| **`수정: …`** | 문장·위치 수정 |
| **`삭제`** | 해당 한 줄 제거 후 DIL-10 착수 |

---

## 다음에 올 일 (응답 불필요)

1. NTT 승인 → DIL-10 심층 1단위 → 사용자 승인 → producer handoff
2. DIL-12: `HO-…-04` 8칸 정정 확인 후 · DIL-10 다음
3. deep-dive 종료 → director 단계 판정 · 본문 P-014 경로

---

## 최근 완료

- **`초기화` 재부트스트랩** — S7 OK · role 확정 · handoff/MILESTONES 재구성 · 연구 미착수
- `HO-20260724-01` done — `roles/analyst/PROMPT.md` SSOT 포인터만
- DIL-11 U1–U5 · DIL-09 U1–U2 (레거시) · M0 done

---

## 사용자 답변 칸

```

```
