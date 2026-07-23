# ROADMAP — 학술 논문 심층 이해·Marp 발표자료

최종 갱신: 2026-07-23  
근거 프롬프트: `Paper-Deep-Dive/PROMPT.md`  
설계 원본: `.Prompt_Engineering/학술 논문의 심층적 이해 및 분석을 위한 AI 프롬프트 설계.md`

---

## 1. 목표

대상 논문 **전문**을 문단 단위로 심층 이해·분석하고, 템플릿 기반 **한글 Marp** 발표자료로 이관한다.  
요약 목적이 아니며, 레퍼런스는 **1-deep 요약**만 허용한다.

## 2. 논문 처리 순서

```text
[1] HAETAE-FIA  양자 내성 암호 HAETAE에 대한 오류 주입 공격 및 대응 기법
        │
        ├─ M0 계약 고정
        ├─ M1 서지·목차
        ├─ M2 문단 인덱스
        ├─ M3 본문 문단 루프 (P-001 … 각 1회 승인)
        ├─ M4 그림·표
        ├─ M5 레퍼런스 1-deep (PDF 없으면 요청)
        ├─ M6 Marp 통합
        ├─ M7 교차 검증
        └─ M8 논문 완료 승인
        │
        ▼
[2] PCM-DFA  Public Coefficient Matters A Practical Differential Fault Attack on ML-DSA and HAETAE
           (동일 파이프라인, HAETAE-FIA 완료 후; **PDF 아카이브 ready** 2026-07-23)
```

## 3. 마일스톤 의존 그래프

```text
M0 ──► M1 ──► M2 ──► M3 ◄──► M4
                      │
                      ▼
                     M5
                      │
              M3+M4+M5 완료
                      │
                      ▼
                     M6 ──► M7 ──► M8
```

| 관계 | 설명 |
|------|------|
| M3 ⇄ M4 | 본문 중 Fig 참조 시 이미지 이관 병행 가능 |
| M5 | 본문에서 인용 맥락 누적 후, 절 단위 안정 또는 사용자 지시 시 요약 |
| M6 | 본문·그림·레퍼런스 슬라이드 정합 |
| M7 | 다 AI 교차 검증 / 재실행 점검 |

## 4. 산출물 위치

| 종류 | 경로 |
|------|------|
| 실행 프롬프트 | `Paper-Deep-Dive/PROMPT.md` |
| 상태 보드 | `.Intermediate_Artifacts/MILESTONES.md` |
| 결정 로그 | `.Intermediate_Artifacts/DECISIONS.md` |
| 교차 검증 | `.Intermediate_Artifacts/CROSS_CHECK.md` |
| 논문 내부 베이스 | `.Intermediate_Artifacts/papers/<paper_id>/` |
| 발표자료 | `Presentation_Marp/<논문폴더>/presentation.md` |

## 5. 진행 원칙 (로드맵 불변식)

1. **한 문단 게이트**: 승인 없이 다음 문단 금지  
2. **PDF only**: 웹에서 레퍼런스 수집 금지, 부재 시 요청  
3. **전문 보존**: 슬라이드 분할은 허용, 내용 삭제는 금지  
4. **대면 최소 잡설**: 사용자에게는 현재 문단 해석만  
5. **지속 갱신**: 매 승인마다 `MILESTONES.md`·해당 `PROGRESS.md` 갱신  
6. **Canonical 동기화**: 정식 경로는 `/home/user/fia_cm_haetae/Collabo_HB` — 매 쓰기 후 메인 반영 (`SYNC.md`)  
7. **사용자 단일 접점**: `To_Do.md`만 — 판단 1건/턴(최대 2). Intermediate는 AI 내부  

## 6. HAETAE-FIA 본문 골격 (H-M1 confirmed)

- 표지·요약·ABSTRACT·Keywords  
- I. 서론  
- II. 관련 연구 및 배경 지식  
- III. HAETAE 서명 알고리즘 오류 주입 공격  
- IV. 실험 설계 및 구현  
- V. 대응 방안  
- VI. 결론  
- References → 1-deep  

## 7. 다음 액션 (로드맵 헤드)

**완료:** M0, H-M1, H-M2, Canonical, To_Do 단일 접점, **M-ARCH Papers 1-deep PDF 전량**.  
**현재:** Dilithium deep-dive [9] 중간 점검 → **[10]** 심층 또는 피드백 반영. P-014는 D25 완료 후.  
**PDF:** 1-deep 요청 불필요 (HAETAE 24/24, PCM 35/35).
