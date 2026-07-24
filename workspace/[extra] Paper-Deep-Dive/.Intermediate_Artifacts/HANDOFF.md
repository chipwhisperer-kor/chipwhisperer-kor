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
| HO-20260723-11 | curator | analyst | DIL-10-assets | `Papers/ASSET_CATALOG.md`: `HAETAE-FIA-REF-10`, `HAETAE-FIA-REF-01-FIPS204`, `HAETAE-FIA-REF-10-ARTIFACT` | PDF·표준 열기/메타/해시·원출처 대조, artifact ZIP 무결성 완료; 코드는 미실행 | ready | 2026-07-23 |
| HO-20260724-04 | curator | analyst | DIL-12-assets | `Papers/ASSET_CATALOG.md`: `HAETAE-FIA-REF-12` | PDF 열기·텍스트 추출·서지·해시·IEEE Xplore/KTH 원출처 대조 완료; 해석·결론 없음 | — | ready | 2026-07-24 |
| HO-20260724-05 | director | curator | HANDOFF `HO-20260724-04` | **형식 정정 — 서식이 아니라 기능 문제.** 해당 행이 **9칸**이라 뒤 칸이 한 칸씩 밀렸고, 그 결과 `status` 자리에 `ready`가 아닌 `—`가 온다. **열 기준으로 읽으면 `ready`가 아니어서 analyst가 소비 대상으로 인식하지 못한다.** 방향: 검증 노트("PDF 열기·텍스트 추출…해석·결론 없음")를 **`payload` 칸 안으로 합쳐** 8칸으로 맞출 것. 자산 검증 내용 자체는 규격 충족이므로 **`ASSET_CATALOG` 행과 `ready` 의도는 그대로 둔다.** 원인은 레거시 행 모방이며 표 첫 줄에 템플릿 행을 추가해 재발을 막았다. | — | ready | 2026-07-24 |
| HO-20260724-03 | director | producer | To_Do_Producer.md | **반려 — 접점 파일 규격 위반.** `## 사용자 답변 칸`의 **코드 펜스를 삭제**해 사용자가 지시를 쓸 자리가 사라졌다(§8.1 고정 섹션·`계속` 대상 소멸). 방향: (1) 답변 칸을 ```` ``` / (여기에 기입) / ``` ```` 3줄로 복구. (2) `최근 완료`의 중복 2줄("신규 작업 로직 파악 완료" / "작업 로직 재확인 완료")을 1줄로 정리. 파일은 producer 단독 쓰기이므로 **director가 고치지 않는다.** 재개 조건: 답변 칸 복구 확인. | — | done | 2026-07-24 |
| HO-20260724-02 | director | curator | roles/curator/ROLE.md | **오기 정정 요청(1자).** "신규 `paper_id` 발급 **(D42)**" → **(D43)**. 근거: `DECISIONS` D43이 발급 주체 결정, D42는 director 신설. 파일은 curator 단독 쓰기이므로 **director가 고치지 않는다.** | — | done | 2026-07-24 |
| HO-20260724-01 | director | analyst | roles/analyst/PROMPT.md | **규격 위반 시정 요청(내용 아님·문서 위생).** 해당 파일 마지막 줄에 연구 진행 상태("curator의 DIL-10 자산 패킷 + sparse-c-NTT 사용자 게이트 후 DIL-10")가 박혀 있음. 역할 계약 파일은 **절차**만 담고 **상태**는 `MILESTONES`/`To_Do_Analyst.md`가 SSOT (S5·README 문서 계층). 방향: 그 줄을 상태 서술 없이 포인터 한 줄로 교체. 파일은 analyst 단독 쓰기이므로 **director가 고치지 않는다.** | — | done | 2026-07-24 |

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
