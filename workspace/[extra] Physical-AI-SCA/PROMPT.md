# PROMPT.md — v2 실행 사이클 계약

이 문서는 자동화 에이전트가 한 study를 끝까지 수행할 때 지킬 순서와 실패 조건이다.
보안 판단 원칙은 `AGENTS.md`, 프로파일·분석·확장 설명은 `README.md`에 자기완결적으로 있다.

## 한 사이클

1. `demo/study.yaml`과 모든 experiment를 `spec.study_experiments()`로 검증한다.
2. 에뮬레이션 IUT를 빌드하고 selftest를 수행한다.
3. 노트북이 resolved 기준을 preflight JSON에 기록하고 Grok `pre-collection` 요청을 쓴 뒤
   기다리면서 호스트 저장소 루트에서 실행할
   정확한 Python 한 줄을 표시하면 사용자가 그 명령을 실행한다. one-shot 읽기 전용 자문이
   실패하면 수집 전에 중단한다.
4. 각 experiment를 study 순서대로 collect → analyze → report → verify한다.
5. SPA 그림과 `human_review.spa=pending`을 노트북에 표시한다.
6. 모든 결정적 증거가 완성된 뒤 같은 호스트 Python 한 줄로 Grok xhigh one-shot 출판 감사를
   수행한다.
7. 감사 입력 해시가 신선한 경우에만 통합 MD/HTML과 publication manifest를 생성한다.

```bash
cd '/workspace/[extra] Physical-AI-SCA'
python3 -m physai.collect --study demo/study.yaml --experiment <id>
python3 -m physai.analyze --study demo/study.yaml --experiment <id>
python3 -m physai.report --run <id> --study demo/study.yaml
python3 -m physai.verify --run <id> --study demo/study.yaml
# 다음 명령이 기다리면 호스트의 chipwhisperer-kor 루트에서 위 Python 한 줄을 실행한다.
python3 -m physai.demo --study demo/study.yaml --grok
python3 -m physai.demo --study demo/study.yaml --report
```

## 설계 계약

- 원시 experiment는 `schema_version: 2`여야 한다. v1을 추정 변환하지 않는다.
- 프로파일 수치와 subset 수량은 `physai/profiles.py`만 정의한다.
- `scope.not_claimed`, 민감 경계 rationale과 vendor_info를 비우지 않는다.
- TVLA 입력은 fixed/random subset, DPA 입력은 단일 attack subset과 알고리즘 민감 target,
  CPA 입력은 attack subset으로 각각 명시한다.
- 프로파일·단계·판정 기준을 바꾸면 새 study/experiment ID를 사용한다.
- 수집기는 같은 입력의 각 실행을 Schema 1.3 `raw-acquisition`에 별도 행으로 보존한다.
- 분석기는 원본을 수정하지 않고 계약 해시가 일치하는 `derived-analysis` float64 평균만 사용한다.
- TA는 원본의 실행별 `exec_time`, 파형 시험은 파생 `trace`를 사용한다.

## 분석과 판정

| 항목 | 지위 | 핵심 해석 |
|---|---|---|
| TA | ISO 필수 | 관측 누설은 저표본이어도 fail; 미검출 pass에는 수량 필요 |
| SPA | ISO 필수 | 자동 절차 완료와 별개로 사람 육안 검토는 항상 pending |
| TVLA | 독립 평가 | fixed-vs-random 소견이며 ISO 종합 판정에 합산하지 않음 |
| DPA | ISO 필수 | 사전 지정 민감값 0/1 집단; 관측 누설은 저표본이어도 fail |
| CPA | 양성 대조/참고 | 비마스킹 대조 실패 시 미검출 해석 차단; ISO 판정 아님 |
| soundness | 연구자 관점 | 에뮬레이션 구현 결함 후보; 물리 공격 성공 주장 아님 |

먼저 `procedure_status`, `statistical_power`, `early_finding`, `preassessment_verdict`,
`claim_scope`를 분리해 읽는다. `complete`를 pass로, `underpowered` 미검출을 안전으로,
TVLA 검출을 곧바로 ISO DPA 판정으로 바꾸지 않는다.

## 실패 처리

- 골든 암호문, 행 정렬, sample_map 또는 스키마 오류는 건너뛰지 않는다.
- L4 Nyquist·PSD prominence·정렬 이동·상관 기준 실패는 파라미터 자동 조정 없이 중단한다.
- 결정적 명령 실패 시 Grok failure 자문은 원인 설명만 하며 파일 수정이나 재실행을 하지 않는다.
- 호스트 one-shot Grok 사전 자문 실패/부재는 수집을, 출판 감사 실패/부재/stale은 publication을
  차단한다. 감시기·데몬·백그라운드 Grok은 사용하지 않는다.
- `미기록`, `미준수`, `검정력 부족`, `검출 없음`을 서로 바꾸지 않는다.

## 사용자에게 남길 것

- 개별·통합 Markdown/HTML 경로
- TA·SPA·TVLA·DPA와 CPA 양성 대조의 분리된 결과
- SPA 사람 검토 pending과 사용하지 않은 채널
- 통계 검정력과 CW Lab 파일럿이라는 claim scope
- Grok 출판 감사의 model/effort, 정확한 입력 해시와 stale 검증 상태

“적합성 검증 완료”라고 쓰지 않는다. 이 프로젝트의 산출물은 표준 방법론 준용 사전진단이다.
