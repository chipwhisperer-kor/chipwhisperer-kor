# MILESTONES — 상태 보드

최종 갱신: 2026-07-23 (`Papers/` 아카이브 전량 반영)  
사용자 접점: **`To_Do.md` only** — 상세 핸드오프는 To_Do 본문

범례: `pending` | `in_progress` | `done` | `blocked` | `deferred`

---

## 전역

| ID | 항목 | 상태 | 비고 |
|----|------|------|------|
| M0 | 작업 계약·결정 고정 | **done** | PROMPT, To_Do 단일 접점 D13; **D25**; **D34** Papers 아카이브 |
| M-ARCH | `Papers/` 1-deep PDF 아카이브 | **done** | HAETAE 24/24 · PCM 35/35 · 표준문서 1 · 매니페스트 대조 OK |

---

## Paper: HAETAE-FIA

| ID | 항목 | 상태 | 비고 |
|----|------|------|------|
| H-M1 | 서지·목차 확정 | **done** | |
| H-M2 | 문단 인덱싱 | **done** | 73단위 confirmed |
| H-M3 | 본문 심층 읽기 | **blocked** (P-014+) | **D25:** Dilithium deep-dive 완료 전 보류 |
| H-M4 | 그림·표 이관 | pending | |
| H-M5 | 레퍼런스 1-deep | **in_progress** | PDF **전량 있음**; 요약 [9–12] done; 심층 [11] done, [9] partial, [10][12] pending |
| H-M6 | Marp 통합·정합 | **in_progress** | D24+D30+D32; 제3자 중간 점검본 |
| H-M7 | 교차 검증 | pending | |
| H-M8 | 논문 단위 완료 | pending | |

### Dilithium FI Deep-Dive (D25)

| 단위 | 상태 |
|------|------|
| DIL-11-U1 NTT + Alg 41 전문 | **done** |
| DIL-11-U2 Attack-1 | **done** |
| DIL-11-U3 Attack-2 | **done** |
| DIL-11-U4 Verify-Bypass | **done** |
| DIL-11-U5 [11] 정리 | **done** |
| DIL-09-U1 ExpandMask skip | **done** (slides) |
| DIL-09-U2 MLWE→RLWE | **done** (slides; 중간 점검 중) |
| DIL-09 정리 / DIL-10 / DIL-12 | pending |

### H-M3 진행

| ID | 상태 |
|----|------|
| P-001 … P-013 | **approved** |
| P-014 | **deferred** (D25) |
| P-015 … P-073 | pending |
| REF-09…12 요약 | **approved** + Marp |
| REF-01…08, 13…24 PDF | **있음** (요약 미착수) |
| REF-11 심층 | **U1–U5 done** |
| REF-09 심층 | **U1–U2 slides; 중간 점검** |
| REF-10·12 심층 | pending |

---

## Paper: PCM-DFA

| ID | 상태 | 비고 |
|----|------|------|
| 자료 아카이브 | **ready** | 대상 PDF + 1-deep 35편 + REF-INDEX |
| 본문 파이프라인 (M1–M8) | **deferred** | D9: HAETAE-FIA 완료 후 |

---

## 활성 포인터

- **Active:** HAETAE-FIA / 동료 피드백 팩트체크 완료 (sparse $c$ vs NTT) → 슬라이드 보강 여부 또는 **[10]**  
- **Blocked on:** `To_Do.md` 사용자 회신  
- **PDF 요청:** 불필요 (1-deep 누락 없음)  
