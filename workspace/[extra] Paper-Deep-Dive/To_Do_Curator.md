# To_Do_Curator — 사용자 ↔ `curator` 접점

`curator` **단독 쓰기** · 사용자는 **답변 칸**. 채팅 **`계속`** = 이 파일의 답변 칸. 규칙은 `PROMPT.md` §8.

---

## 지금 상태

| # | 재부트스트랩 결과 |
|---|-------------------|
| 0. 작업 루트 대조 결과 | `OK` — 현재 디렉터리와 `.Intermediate_Artifacts/SYNC.md` 선언이 일치 |
| 1. role_id / 서비스 | `curator` / Codex |
| 2. 단독 쓰기 경로 | `Papers/**`, `roles/curator/**`, `To_Do_Curator.md` |
| 3. 소비 가능한 `ready` handoff | 없음 |
| 4. 차단 요인·질문 | 없음 |
| 5. 연구 작업 | 대상 논문 Markdown 파생본 2편 수동 구조 교정 완료 · 모두 `verified` |

### 완료 — 검증된 Markdown 파생본 2편

- 변환 규격·검수 SSOT: `Papers/PDF_TO_MARKDOWN.md`
- 재현 도구: `Papers/tools/pdf_to_markdown.py` (`deterministic-bbox-v1`, 생성형 AI·OCR 미사용)

#### `HAETAE-FIA-TARGET-MD`

- 원본 14쪽; 파생본 53,346 bytes, SHA-256 `aa774afbe58dbf3b393ba215db1cb4c26d9c3728cd4135672ee17b3dceb9ceff`
- 수식 (1)–(8), Fig. 2·3 알고리즘, Table 1–6 구조 전사; 시각 링크 19개·매니페스트 자산 20개
- 페이지 14/14, 누락 링크 0, 매니페스트 불일치 0, `CONVERSION-ISSUE` 0, private-use 글리프 0

#### `PCM-DFA-TARGET-MD`

- 원본 10쪽, 1,619,979 bytes, SHA-256 `7b9dfdeab09968173c0769f8fd66f12c33aa24a2cffb701802e3296f283fcbb4`
- 파생본 58,525 bytes, SHA-256 `c129062d3d42ecc0d0ad2669d8134618beb61701793103ce12be63eddf4e7219`
- 자동 보존 검사: bbox word 9,208/9,208, numeric token 875/875, source block 190/190
- 수동 교정: 수식 (1)–(2), Algorithm 1–9, Table I–III 구조 전사; Fig. 1–3·알고리즘·표·저자 사진 5개의 시각 링크/매니페스트 자산 20개
- 페이지 10/10, 누락 링크 0, 매니페스트 SHA-256 불일치 0, `CONVERSION-ISSUE` 0, private-use 글리프 0

두 파생본과 source PDF는 `Papers/ASSET_CATALOG.md`에 `verified`로 등록했다. 최종 인용 기준은 계속 source PDF 페이지다.

### 향후 활용 메모 위치

리서치 갭 후보 발굴 논의는 `Papers/PDF_TO_MARKDOWN.md` §7 **「향후 활용 메모 — 비활성」**에 보존했다. `verified` Markdown은 발견 계층, source PDF는 판정 계층으로 사용하고, 실제 분석은 `analyst` 책임이라는 경계를 함께 기록했다.

이 항목은 ROADMAP·마일스톤·활성 업무가 아니며 별도 사용자 지시와 역할 인계 전에는 착수하지 않는다.

---

## 지금 할 일 (사용자) — 0건

없음.

---

## 다음에 올 일 (응답 불필요)

1. 추가 지시가 있을 때 다른 논문의 Markdown 변환 범위·비용 산정
2. 정식 analyst 입력으로 채택할 때 director에 공통 인계 계약 개정 요청
3. 향후 리서치 갭 후보 발굴을 활성화할 때 verified Markdown 묶음과 source PDF를 함께 인계

---

## 최근 완료

- 사용자 요청 처리 — PCM-DFA 대상 논문 10쪽의 수식 (1)–(2)·알고리즘 1–9·표 I–III·그림/사진 20개를 source PDF와 수동 대조 교정하고 `PCM-DFA-TARGET-MD`를 `verified`로 등록
- 사용자 `B 승인` 처리 — HAETAE 대상 논문 14쪽의 수식·알고리즘·표·그림을 source PDF와 수동 대조 교정하고 `HAETAE-FIA-TARGET-MD`를 `verified`로 갱신; 리서치 갭 후보 발굴 논의는 `Papers/PDF_TO_MARKDOWN.md` §7의 비활성 메모로 보존
- B 활용성 자문 완료 — `verified` Markdown은 리서치 갭 후보의 발견 계층, PDF는 후보의 판정 계층이며 여러 논문 교차검증이 필요하다고 답변; 분석은 analyst 책임, 추가 변환 미착수
- 사용자 승인 처리 — 변환 규격·결정론적 도구 작성, 대상 논문 1편 Markdown 파일럿 생성, 자동 검사·14쪽 curator 대조·카탈로그 등록 완료; 21개 명시적 예외로 `partial` 판정, 전체 확대 미착수
- PDF+Markdown 병존 자문 완료 — 저장소 PDF 62개·사용 가능 비생성형 도구·대표 2단 PDF 추출 실패 양상을 점검하고, 원본 고정·보수적 변환·자동 검사·페이지별 검수의 조건부 파일럿 권고; 변환 미착수
- `HO-20260724-05` 소비 완료 — `HO-20260724-04`의 검증 설명을 payload에 합쳐 정확히 8칸으로 복구하고 analyst 대상 `ready` 상태 보존
- `초기화` — 폴더만으로 작업 루트·역할·소유권·접점·handoff 상태 재구성, 상태표를 0–5 응답 양식에 맞게 정정; 연구 작업·handoff 소비 미착수
- `초기화` 재수행 — 폴더만으로 작업 루트·역할·소유권·접점·handoff 상태 재구성, 연구 작업·handoff 소비 미착수
- DIL-12 논문 PDF 재검증·`HAETAE-FIA-REF-12` 카탈로그 등록 → `HO-20260724-04` ready
- 작업 로직 변경(D40–D44) 재확인 — 역할별 접점, 자기완결성, director 소유·게이트, `ready` 소비 규칙 및 현재 대기 상태 파악
- `HO-20260724-02`의 D42→D43 오기 정정 완료
- 현재 사용자 요청에 따라 기존 `AGENTS.md` 존재 여부 확인 · 파일 변경 없이 보존
- DIL-10 자산 3건 검증·`ASSET_CATALOG` 등록 → `HO-20260723-11` ready
- 부트스트랩 완료 (D39) · M0 done

---

## 사용자 답변 칸

```
```
