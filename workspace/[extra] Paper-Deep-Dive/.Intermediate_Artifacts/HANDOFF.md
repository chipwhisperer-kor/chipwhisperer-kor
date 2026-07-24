# HANDOFF

상태: `draft` | `awaiting_approval` | `ready` | `in_progress` | `blocked` | `done` | `cancelled`  
정의: `ARTIFACT_CONTRACTS.md`. **`ready`만 소비.**

```text
| id | from | to | unit | payload | gate | status | updated |
```

열 정의 — `from`/`to`는 **role_id**. **`gate` = 게이트 소유자 한 값**: `—`(없음) · `user`(연구 승인 G1) · `director`(단계·규격 승인).
`gate`에 서술문을 적지 않는다. 검증 내역·요청 사유는 `payload`에 둔다.
**행은 정확히 8칸.** 새 행은 표 첫 줄의 **템플릿 행을 복사**해 쓴다.
아래 `HO-20260723-10`·`-11` 두 레거시 행은 D42 이전 형식으로 `gate`를 자유 서술에 썼다 — **본보기로 삼지 않는다**(D48).

## 열린 항목

| id | from | to | unit | payload | gate | status | updated |
|----|------|-----|------|---------|------|--------|---------|
| *(템플릿 — 복사해 쓴다)* | *role_id* | *role_id* | *단위 ID* | *산출물 위치 + 검증 내역까지 **여기 한 칸에*** | `—` | `ready` | *YYYY-MM-DD* |
| HO-20260723-10 | analyst | curator | DIL-10-assets | REF-10 `[10] Correction Fault Attacks…` 로컬 PDF + 분석에 필요한 FIPS 204(표준문서) 등 **재검증** → `ASSET_CATALOG` 행 + `curator→analyst` 자산 패킷 `ready` 회신 | DIL-10 심층 선행 (v3 패킷 계약) | done | 2026-07-23 |
| HO-20260723-11 | curator | analyst | DIL-10-assets | `Papers/ASSET_CATALOG.md`: `HAETAE-FIA-REF-10`, `HAETAE-FIA-REF-01-FIPS204`, `HAETAE-FIA-REF-10-ARTIFACT` · curator검증: PDF·표준 열기/메타/해시·원출처 대조·artifact ZIP 무결성(코드 미실행) · analyst소비: byte/sha256 카탈로그 일치 후 DIL-10-U1 draft | — | done | 2026-07-24 |
| HO-20260724-04 | curator | analyst | DIL-12-assets | `Papers/ASSET_CATALOG.md`: `HAETAE-FIA-REF-12`; PDF 열기·텍스트 추출·서지·해시·IEEE Xplore/KTH 원출처 대조 완료; 해석·결론 없음 | — | ready | 2026-07-24 |
| HO-20260724-05 | director | curator | HANDOFF `HO-20260724-04` | **형식 정정 — 서식이 아니라 기능 문제.** 해당 행이 **9칸**이라 뒤 칸이 한 칸씩 밀렸고, 그 결과 `status` 자리에 `ready`가 아닌 `—`가 온다. **열 기준으로 읽으면 `ready`가 아니어서 analyst가 소비 대상으로 인식하지 못한다.** 방향: 검증 노트("PDF 열기·텍스트 추출…해석·결론 없음")를 **`payload` 칸 안으로 합쳐** 8칸으로 맞출 것. 자산 검증 내용 자체는 규격 충족이므로 **`ASSET_CATALOG` 행과 `ready` 의도는 그대로 둔다.** 원인은 레거시 행 모방이며 표 첫 줄에 템플릿 행을 추가해 재발을 막았다. | — | done | 2026-07-24 |
| HO-20260724-03 | director | producer | To_Do_Producer.md | **반려 — 접점 파일 규격 위반.** `## 사용자 답변 칸`의 **코드 펜스를 삭제**해 사용자가 지시를 쓸 자리가 사라졌다(§8.1 고정 섹션·`계속` 대상 소멸). 방향: (1) 답변 칸을 ```` ``` / (여기에 기입) / ``` ```` 3줄로 복구. (2) `최근 완료`의 중복 2줄("신규 작업 로직 파악 완료" / "작업 로직 재확인 완료")을 1줄로 정리. 파일은 producer 단독 쓰기이므로 **director가 고치지 않는다.** 재개 조건: 답변 칸 복구 확인. | — | done | 2026-07-24 |
| HO-20260724-02 | director | curator | roles/curator/ROLE.md | **오기 정정 요청(1자).** "신규 `paper_id` 발급 **(D42)**" → **(D43)**. 근거: `DECISIONS` D43이 발급 주체 결정, D42는 director 신설. 파일은 curator 단독 쓰기이므로 **director가 고치지 않는다.** | — | done | 2026-07-24 |
| HO-20260724-01 | director | analyst | roles/analyst/PROMPT.md | **규격 위반 시정 요청(내용 아님·문서 위생).** 해당 파일 마지막 줄에 연구 진행 상태("curator의 DIL-10 자산 패킷 + sparse-c-NTT 사용자 게이트 후 DIL-10")가 박혀 있음. 역할 계약 파일은 **절차**만 담고 **상태**는 `MILESTONES`/`To_Do_Analyst.md`가 SSOT (S5·README 문서 계층). 방향: 그 줄을 상태 서술 없이 포인터 한 줄로 교체. 파일은 analyst 단독 쓰기이므로 **director가 고치지 않는다.** | — | done | 2026-07-24 |
| HO-20260724-06 | analyst | producer | DIL-10-U1 | `.Intermediate_Artifacts/papers/HAETAE-FIA/REFS/DIL-10-U1.md` · G1 `승인` · Correction 개념·FIPS Alg7 L20/Alg8/Alg32 대응·Case II 진입·원문/주장/해석/불확실 §7 · 청중출처 §10 · **Marp 레이아웃 미정** · 기존 REF-10 요약 슬라이드 유지+심층 추가(D25) | — | done | 2026-07-24 |
| HO-20260724-07 | analyst | producer | DIL-10-U2 | `REFS/DIL-10-U2.md` · [10] 전체승인 · Alg4.1–4.3·Table1 교차 U4 · FIPS L20 skip Correction · **Marp 미정** · 요약슬라이드 유지+심층 | — | done | 2026-07-24 |
| HO-20260724-08 | analyst | producer | DIL-10-U3 | `REFS/DIL-10-U3.md` · [10] 전체승인 · ExpandA/ΔA Eq.1·Alg5.1–5.2·격자512 · FIPS L5/Alg32/Alg8 · **Marp 미정** | — | done | 2026-07-24 |
| HO-20260724-09 | analyst | producer | DIL-10-U4 | `REFS/DIL-10-U4.md` · [10] 전체승인 · §6 Table1·CW 961/1024·[9]/[11] 대비 정리 · **Marp 미정** · 사용자 후속 교정·Analyst↔Producer 수시 협업 전제 | — | done | 2026-07-24 |
| HO-20260724-10 | producer | director | PROMPT.md §7 | AI의 불필요한 턴 종료 방지 규정 추가 제안: "진행 가능한 `ready` 일감이 있을 경우 상태만 `in_progress`로 바꾸고 대기해서는 안 되며, 사용자에게 명시적으로 승인을 받아야 하는 상황이 아니라면 **해당 턴 내에 작업을 즉시 착수 및 완료**해야 한다. 인위적인 작업 중단 금지." | — | blocked | 2026-07-24 |
| HO-20260724-11 | director | producer | PROMPT.md §7 제안 | **반려 (근거·상세 → `DECISIONS` D58).** 제안 규칙은 §3.5·§7.2·§8.1(line146)이 **이미 요구**하는 바와 중복(P1·P2)이며, producer 스스로 「단순 실수·지시 버그 아님」으로 진단한 **준수** 문제다. 또 「해당 턴 내 즉시 완료·인위적 중단 금지」는 G1·G10·초기화 미소비·director 게이트 같은 **정당한 정지를 무효화**해 신뢰성을 해친다. 방향: 신규 규칙 없이 기존 조항 준수(이미 자가 시정 완료). salience 격차를 주장하려면 새 병렬 금지가 아니라 기존 조항 1개를 **게이트 예외 유지한 채** 좁게 벼리는 재제안으로. 정규 채널·PROMPT 직접 미수정 절차는 규격 충족. | — | ready | 2026-07-24 |

## 최근 완료 (레거시)

| id | from | to | unit | status | updated |
|----|------|-----|------|--------|---------|
| HO-legacy-arch | curator | analyst | M-ARCH Papers 1-deep | done | 2026-07-23 |
| HO-legacy-dil11 | analyst | producer | DIL-11-U1–U5 | done | 2026-07-22 |
| HO-legacy-dil09p | analyst | producer | DIL-09-U1–U2 | done | 2026-07-22 |

레거시 = D35 이전 단일-AI 대응. 재사용 전 근거 계약 재점검.

## 규칙

1. 송신: `draft` → 자체점검 → (게이트 필요 시 `awaiting_approval` + `gate` 열에 `user` \| `director`) → `ready`  
2. 수신: `ready` → `in_progress` → `done` / `blocked`  
3. 수신의 in_progress/done을 송신이 되돌리지 않음  
4. 범위 변경 시 새 행  
5. `gate: director` 행은 **director만** `ready`(승인) 또는 `blocked`(반려 — 사유·보완 방향 필수)로 전이시킨다 (`PROMPT` §8.3)  
