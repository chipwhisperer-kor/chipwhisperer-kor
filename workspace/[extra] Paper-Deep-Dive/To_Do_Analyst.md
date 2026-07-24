# To_Do_Analyst — 사용자 ↔ `analyst` 접점

`analyst` **단독 쓰기** · 사용자는 **답변 칸**. 채팅 **`계속`** = 이 파일의 답변 칸. 규칙은 `PROMPT.md` §8.

**작업 루트:** 사용자가 지정한 폴더(`README.md` 있는 곳). 다른 worktree/사본에 쓰지 않는다 — 사본 절대경로는 `.Intermediate_Artifacts/SYNC.md`만.

---

## 지금 상태

| | |
|--|--|
| 역할 | `analyst` = Grok (`AI_ROSTER.md`) |
| 진행 | **상황 파악 완료 (D40–D48)** · DIL-10 **미착수** — sparse-c-NTT 게이트 대기 |
| 파이프라인 병목 | 이 파일의 sparse-c-NTT 1건 (전체 연구 차단) |
| 처리한 handoff | `HO-20260724-01` → **done** (PROMPT 위생) |
| 소비 대기 | `HO-20260723-11` (DIL-10 자산) `ready` — **NTT 게이트 후** 소비 |
| 소비 보류 | `HO-20260724-04` (DIL-12) — **9칸 형식 오류** → curator가 `HO-20260724-05`로 정정 중. 칸 밀림으로 `ready`로 읽히지 않음. **수정 전에는 소비 안 함** |

### 변경된 작업 로직 요약 (D40–D48)

| # | 요지 |
|---|------|
| D40 | 접점 = 역할별 `To_Do_*.md` (단일 `To_Do.md` 폐지). 자기 파일만 쓰기 |
| D41 | 자기완결성 S1–S6 · 절대경로 Canonical 폐기 · 루트=README 폴더 |
| D42–43 | `director`(Claude) 신설 · 공통정책/`CROSS_CHECK` 소유 · `paper_id`=curator |
| D44 | `gate` = `—`\|`user`\|`director` 한 값 · 상태 어휘 3종 구분 |
| D45–46 | bare `계속` = 답변 칸 + 자기 `ready` 처리 · 빈 칸이어도 ready는 처리 |
| D47 | 보고 SSOT = 접점 파일(채팅만 = 미수행) · 단순성 P1–P5 |
| D48 | bare `계속` 자가수복 실증 · HANDOFF 8칸 템플릿 · `(여기에 기입)` 선택 |

역할: curator(Codex) → analyst(Grok) → producer(Agy) · director(Claude)는 호출 시만.

연구 순서(G9/D9/D25): HAETAE-FIA 완료 전 PCM-DFA 보류 · Dilithium deep-dive **[11]→[9]→[10]→[12]**.

| 단위 | 상태 |
|------|------|
| DIL-11 U1–U5 | done (레거시) |
| DIL-09 U1–U2 | done partial (레거시) |
| DIL-10 자산 | 패킷 ready (`HO-…-11`) |
| sparse-c-NTT 1줄 | **awaiting_approval** ← 지금 게이트 |
| DIL-10 분석 | blocked (위 게이트) |
| DIL-12 자산 | 카탈로그 등록됨 · handoff 형식 정정 대기 |
| 본문 P-014+ | blocked/deferred (D25 deep-dive 선행) |

---

## 지금 할 일 (사용자) — 1건

### ☐ sparse-c-NTT 한 줄 반영 검토

**배경:** *Sign_internal* 에서 *NTT* 호출 (FIPS 204 Alg 7). 전용 슬라이드 삭제 후, NTT 호출 표 슬라이드 하단 **한 줄**만 유지 중.

**유지 문장(안):**
> L16 *SampleInBall* 로 $c$ 가 sparse 이어도, FIPS 204는 L17에서 $\mathrm{NTT}(c)$ 를 생략하지 않는다.

| 답변 칸 | 의미 |
|---------|------|
| **`승인`** / **`작업 계속`** | 한 줄 OK → `HO-20260723-11` 소비 · DIL-10 심층 1단위 |
| **`수정: …`** | 문장·위치 수정 |
| **`삭제`** | 해당 한 줄도 제거 후 DIL-10 착수 |

---

## 다음에 올 일 (응답 불필요)

1. NTT 승인 후 DIL-10 심층 1단위 → 사용자 승인 → producer handoff
2. DIL-12: curator `HO-…-05` 정정 확인 후 자산 소비 · 분석 순서상 DIL-10 다음
3. deep-dive 종료 후 director 단계 판정 · 본문 P-014 재개 경로

---

## 최근 완료

- **상황 파악 완료** — D40–D48·역할·HANDOFF·마일스톤·자산 패킷 대조. **원인:** 이전 세션이 사용자 작업 루트가 아닌 worktree 사본을 봐 답변 칸·handoff를 놓침 → 이후 **지정 루트만** 사용
- `HO-20260724-01` **done** — `roles/analyst/PROMPT.md` 상태 서술 제거 → SSOT 포인터만
- DIL-11 U1–U5 · DIL-09 U1–U2 (레거시)
- 부트스트랩 완료 (D39) · M0 done

---

## 사용자 답변 칸

```

```
