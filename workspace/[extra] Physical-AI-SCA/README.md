# Physical-AI-SCA — ISO L3/L4 부채널 사전진단과 CW Lab 파일럿

이 프로젝트는 실험 계획, 에뮬레이션/ChipWhisperer 수집, 통계 분석, 증거 검증과 보고를
하나의 재현 가능한 흐름으로 묶는다. ISO/IEC 17825:2024의 방법론을 준용하지만
ISO/IEC 19790 모듈 경계, 승인 기관과 독립 시험소가 없으므로 **적합성 평가가 아니라
pre-assessment**다.

## 처음 실행하는 사람

ChipWhisperer Docker의 code-server에서
`demo/0.1.Demo_without_TraceWhisperer.ipynb`를 열고 **Run All**을 누른다. 기본 study는
`demo/study.yaml`이며 다음 네 실험을 순서대로 수행한다.

| 채널 | 비마스킹 양성 대조 | 마스킹 IUT |
|---|---|---|
| Unicorn 명령어 HW/HD | tiny-AES-c | masked-aes-c |
| CW308T-STM32F3 전력 | tiny-AES-c | masked-aes-c |

기본값은 `iso-17825-l3 + cw-lab-pilot`이다. 실물 단계에는 연결된 ChipWhisperer Husky와
CW308T-STM32F3가 필요하다. Grok CLI는 컨테이너가 아니라 **호스트**에 설치하고 로그인한다.
Run All은 사전 자문과 출판 감사 셀에서 요청 파일을 쓴 뒤 기다린다. 각 셀은 호스트의
`chipwhisperer-kor` 저장소 루트에서 실행할 정확한 Python 한 줄을 출력한다. 표시된 one-shot
스크립트는 현재 요청 하나를 검증하고 Grok headless를 포그라운드에서 한 번 호출한 뒤 응답
JSON을 쓰고 즉시 종료한다. 감시기·데몬·백그라운드 Grok은 없다. 정상 Run All은 같은 한 줄을
사전 자문과 출판 감사에 각각 한 번 요구하고, 파이프라인 실패 진단이 발생하면 한 번 더 요구한다.

## 프로파일과 캠페인 단계

보안 레벨과 캠페인 단계는 서로 다른 축이다.

| 값 | 의미 |
|---|---|
| `iso-17825-l3` | Annex A.2 수량·효과크기·시간·전처리 |
| `iso-17825-l4` | Annex A.3 수량과 L4 필터·정적/동적 정렬 |
| `smoke` | 계약·코드·배관의 최소 확인 |
| `cw-lab-pilot` | 본시험 전에 같은 절차를 저표본으로 예행 |
| `full` | 프로파일의 수집량과 Formula (1)을 목표로 수행 |

CW Lab은 “노이즈 없는 제3의 레벨”이나 간이 판정이 아니다. ChipWhisperer 전용 보드의
통제된 환경에서 시간이 긴 L3/L4 본시험 전에 수행하는 파일럿이다. 절차, 증거, 한계와 결론
규율은 본시험과 같지만 통계 검정력은 별도로 `underpowered`라고 기록한다.

프로파일 수치의 정본은 `physai/profiles.py` 하나다. 원시 YAML에는 보안 수준, effect size,
α·β, 시간 제한, 반복 수와 subset 수량을 복제하지 않는다.

| 기준 | L3 | L4 |
|---|---:|---:|
| 효과크기 d | 0.04 | 0.01 |
| 수집 시간 상한 | 6 h | 24 h |
| TA 원시 실행/블록 | 1,000 | 10,000 |
| SPA 최소 트레이스 | 11 | 21 |
| CSP bit당 SPA 샘플 | 100 | 1,000 |
| 같은 입력 원본 실행/파생 평균 | 10회/1장 | 10회/1장 |

공통 통계 정책은 α=1e-5, β=0.05, Bonferroni 보정과 보정 전 |t| 하한 4.5다. Formula (1)의
N은 이 값에서 계산하며 별도 설정으로 적지 않는다.

CW Lab 기본 물리 실험은 TA 32+32, SPA 4+4+4, TVLA 64+64, DPA/CPA 128로 논리
트레이스 332개를 만들고 각각 10회 실행해 원시 캡처 3,320개를 보존한다.

## v2 계약

`contracts/experiment_spec.schema.json`은 실험별 사실을, `contracts/study.schema.json`은
여러 실험의 순서·대조 관계·출판 정책을 검증한다. v1은 묵시적으로 읽지 않는다. 어떤
프로파일과 단계였는지 추정하면 과거 결과의 의미가 바뀌기 때문이다.

study가 소유하는 값:

- `assessment_profile`, `campaign_stage`, `algorithm`
- 실행할 experiment와 양성 대조/비교 관계
- Grok 자문·출판 감사 정책

experiment가 소유하는 값:

- IUT와 countermeasure
- 수집기·실제 장비 설정·관측 구간
- subset의 입력 방식과 분석 입력 매핑
- 민감 경계·벤더 정보·`scope.not_claimed`

판정 기준을 바꾸면 새 study와 experiment ID를 만든다. 기존 Dataset을 덮어쓰거나 새 기준으로
재해석하지 않는다. 수집 전에 `resolved_spec.json`과 `01_experiment_plan.{md,html}`을 써서
계약을 동결한다.

실물 수집 계약은 장치에 실제로 플래시하는 Intel HEX의 SHA-256을 사용한다. 기본 firmware
make는 같은 기계어에도 ELF의 링크·디버그 바이트를 바꾸므로 ELF 전체 해시를 계약에 쓰면
Run All마다 거짓 신규 계약이 생긴다. HDF5 `firmware_sha256`은 Schema 1.3의 provenance
정의대로 해당 실행에서 생성된 ELF 원본 해시를 별도로 기록한다.

한 experiment ID에 `capture_manifest.json`이 봉인된 뒤에는 resolved spec과 원본 SHA가
일치할 때만 그 원본을 읽기 전용으로 재사용하며 빌드·플래시·장비 연결을 다시 하지 않는다.
IUT 소스·컴파일 설정·펌웨어 이미지를 바꿀 때는 새 experiment ID를 만든다. 같은 ID를
새 구현에 재사용하면 과거 증거가 다른 구현의 결과처럼 읽히므로 허용하지 않는다.

## 분석의 의미

ISO 필수 순서는 TA → SPA → DPA다. 앞 시험이 fail이어도 뒤 시험은 계속 수행한다. 단,
TA 내부에서 CSP 의존성 1단계가 fail이면 표준 절차에 따라 평문 의존성 2단계로 가지 않는다.

| 분석 | 역할 | 집단/모델 |
|---|---|---|
| TA | ISO 필수 판정 | 실행시간 평균과 분산의 CSP·평문 의존성 |
| SPA | ISO 필수, 사람 검토 필요 | key schedule 구조와 잡음 바닥, 최종 `pending` |
| TVLA | 독립 누설 평가 | fixed-vs-random Welch t-test |
| DPA | ISO 필수 판정 | 사전 지정 민감값으로 동일 수집 집합을 분할한 Welch t-test |
| CPA | 참고/양성 대조 | 공격자 관점 AES HW(S-box) 상관, ISO 판정에 미포함 |
| soundness | 에뮬레이션 연구자 관점 | 실제 기계어 HW/HD와 알려진 민감값의 종속성 |

과거 코드의 `dpa.py`는 fixed-vs-random을 비교했으므로 실제로는 TVLA였다. v2에서는 이를
`tvla.py`로 분리했다. AES DPA 기본 표적은 수집 전에 고정한 첫 라운드
`SBOX(plaintext[0] xor key[0])`의 bit 0이다.

각 시험은 하나의 단어에 서로 다른 의미를 섞지 않는다.

- `procedure_status`: 자동 절차가 complete/incomplete/error인가
- `statistical_power`: sufficient/underpowered/not-applicable인가
- `early_finding`: detected/not-detected-at-N/not-applicable인가
- `preassessment_verdict`: pass/fail/inconclusive/not-applicable인가
- `human_review.spa`: 자동화하지 않으므로 항상 pending

TA 또는 DPA 누설이 관측되면 저표본이어도 fail이다. 누설 미검출은 요구 수량과 양성 대조가
모두 충족되어야 pass가 될 수 있다. TVLA 검출은 중요한 독립 소견이지만 ISO 종합 판정을
직접 바꾸지 않는다. SPA의 사람 검토가 구조화 입력으로 돌아오지 않으므로 자동 종합 결과는
다른 필수시험의 fail이 없는 한 inconclusive다.

## 원본 수집 HDF5와 파생 분석 HDF5

Schema 1.3은 수집과 분석의 책임을 분리한다.

| 구분 | 저장 단위 | 변경 정책 | 소비자 |
|---|---|---|---|
| `raw-acquisition` | Execution 1회 = 1행 | 완료 후 불변 | TA의 실행별 `exec_time`, 파생 생성기 |
| `derived-analysis` | 같은 입력 10회 = float64 평균 1행 | 계약이 바뀌면 새로 생성 | SPA·TVLA·DPA·CPA·soundness |

원본의 같은 key/plaintext/ciphertext 실행은 `repeat_group_id`로 묶고 `repeat_index=0..9`로
구분한다. `trace`, `exec_time`, masked IUT의 `mask`를 매 실행 별도로 보존하며 수집기에는
평균값이 없다. 10회 전체가 성공한 뒤에만 10행을 함께 추가하므로 부분 묶음은 정상 원본이
될 수 없다.

파생 파일은 원본 SHA-256, 전처리 설정과 파이프라인 판번호에서 정한 content-addressed
경로에 생성한다. 이 계약과 저장된 파생 SHA-256이 모두 같을 때만 캐시를 재사용한다. 평균은
원본 `sample_scale`로 정규화한 float64라 분수 정보를 보존한다. 원본은 처음 한 번 수집하고,
같은 봉인 원본을 분석할 때 다시 수집하지 않는다.

## Level 4 전처리

L3는 정규화 후 직접 평균한다. L4는 원본 HDF5를 수정하지 않고 각 Execution을 먼저
전처리한 뒤 평균하며 다음 고정 순서를 적용한다.

1. 실제 target clock의 0.5–1.5배, 4차 Butterworth SOS zero-phase band-pass
2. 기준 파형과 normalized cross-correlation 전역 정렬(최대 2 target cycles)
3. 8개 등간격 anchor normalized cross-correlation 국소 정렬(최대 1 cycle)
4. anchor shift 선형 보간과 공통 유효 구간 crop
5. 정렬된 동일 입력 10회 평균

기준은 `spa_same` 첫 논리 레코드의 첫 반복이다. anchor 상관 최솟값 0.8, 교정 PSD의 대역
내 peak prominence 6 dB를 요구한다. Nyquist·prominence·이동·상관 기준을 어기면 중단하고
inconclusive 근거로 남긴다. 결과를 본 뒤 대역이나 정렬값을 자동 조정하지 않는다.

원본/파생 SHA-256, 필터 응답, PSD, 이동량, 상관계수, mapping 해시와 전후 파형은 파생
HDF5 옆의 `.provenance.json`, run의 NPZ와 보고서 그림에 남는다.

## Grok headless와 출판

프로젝트는 전역 Grok 설정을 수정하거나 인증정보를 컨테이너에 공유하지 않는다. 노트북은
프로파일에서 해석된 수량·통계·전처리는 `runs/<study>_preflight.json`에 결정적으로 기록한다.
노트북은 이 파일과 원본 명세를 `runs/grok_request.json`에 프로젝트 상대경로·크기·SHA-256으로
기록하고 현재 셀에서 응답을 기다린다. 사용자가 호스트에서 표시된 Python 한 줄을 실행할 때만 Grok이 시작되며 완료 후 즉시
종료한다. 모델·추론 강도·task 문장·출력 스키마·다음 제한의 정본은 모두
`physai/grok_once.py` 하나다.

```text
--single --no-memory --no-subagents --disable-web-search --no-plan
--tools Shell(cat:*) --permission-mode dontAsk
```

자문은 `grok-4.6/high`, 필수 출판 감사는 `grok-4.6/xhigh`다. 자문은 계획 검토·실패 설명·
결과 설명만 하며 파일 수정, 판정 변경과 명령 재실행 권한이 없다. 데모 Run All에서는 사전
자문 실패나 Grok 부재가 수집을 막고, 출판 감사 실패·부재는 publication 완료를 막는다.

감사 JSON은 모든 입력의 프로젝트 상대경로·바이트·SHA-256을 기록한다. 통합 보고서 생성 시 현재
파일과 다시 비교해 stale 감사를 거부한다. Grok이 쓴 finding에는 파일/필드 근거와 한계를
함께 요구하며 수치·판정·해시의 정본은 항상 결정적 JSON이다.

## 보고서와 CLI

각 run은 다음 산출물을 만든다.

- `01_experiment_plan.{md,html}` — 수집 전 계약과 계획
- `02_analysis_report.{md,html}` — 수치, 판정 축, SPA/TVLA/DPA/CPA와 전처리 증거
- `03_evidence_manifest.{md,html}` + `manifest.json` — 재현 명령과 파일 해시
- `results.json` — 기계 판독 정본

통합 보고서는 `demo/0.1.Demo_without_TraceWhisperer_Report.{md,html}`이다. HTML은 외부 CDN
없이 CSS와 그림을 내장하고 화면·인쇄에 모두 맞춘다.

```bash
cd '/workspace/[extra] Physical-AI-SCA'

# study의 experiment 하나를 명시적으로 수행
python3 -m physai.collect --study demo/study.yaml --experiment demo_l3lab_emul_tinyaes
python3 -m physai.analyze --study demo/study.yaml --experiment demo_l3lab_emul_tinyaes
python3 -m physai.report --run demo_l3lab_emul_tinyaes --study demo/study.yaml
python3 -m physai.verify --run demo_l3lab_emul_tinyaes --study demo/study.yaml

# 통합 요약
python3 -m physai.demo --study demo/study.yaml

# 아래 명령은 요청을 쓴 뒤 기다리면서 호스트에서 실행할 Python 한 줄을 표시한다.
python3 -m physai.demo --study demo/study.yaml --grok
python3 -m physai.demo --study demo/study.yaml --report
```

## 새 알고리즘 추가

`physai/algorithms` 계약에 다음을 구현하고 registry에 등록한다.

1. 고유 ID와 key/input/output byte 폭
2. 입력을 바꾸지 않는 골든 연산
3. 이름이 고정된 DPA target 목록과 `(plaintext,key) → 0/1 label` 분할
4. 지원한다면 CPA 예측 행렬과 soundness 가능 여부

그 뒤 experiment의 `algorithm`, subset 폭을 사용하는 수집기와 펌웨어 통신을 함께 구현한다.
현재 에뮬레이션 하네스와 ChipWhisperer SimpleSerial 수집기는 AES 16바이트 구현이다. 폭만
명세에서 바꿔 놓고 동작한다고 주장하지 않는다. 골든 연산, 분할 균형, 알려진 누설 합성
데이터와 양성 대조를 먼저 테스트한다.

## 새 수집 도구 추가

오실로스코프 드라이버는 이번 구현에 포함하지 않는다. 새 수집기는 공용 HDF5 Schema 1.3을
통과하는 파일을 생성해야 하며 최소한 다음을 실제 값으로 기록한다.

- 채널 종류, probe와 trigger 의미
- target clock, sample rate, resolution, gain과 실제 파형 길이
- 대역폭 값의 출처와 nominal/calibrated 구분
- 동일 입력의 Execution별 원파형·실행시간, `repeat_group_id`와 `repeat_index`
- key/plaintext/ciphertext의 행 정렬과 골든 결과
- 수집 시간, 툴체인, seed, 자연 발생 복구 이력

원본 수집기는 평균을 저장하지 않는다. 분석기가 동일한 Schema 1.3 파생 계약으로 float64
평균을 만든다. 모르는 대역폭·션트·교정값은 추정하지 말고 미기록으로 둔다.

## 해석 한계

- 에뮬레이션은 물리 글리치·커플링·파이프라인 효과를 포함하지 않는다.
- Unicorn 실행시간은 명령어 수이며 Cortex-M4 cycle-accurate 시간이 아니다.
- EM 채널과 독립 시험소 판정은 제공하지 않는다.
- CPA 실패/성공은 ISO 판정이 아니라 배관과 공격 참고다.
- 고차 DPA는 현재 범위 밖이다. TA의 분산 검정은 별개로 수행한다.
- `미기록`, `미준수`, `검정력 부족`, `검출 없음`을 서로 바꾸어 쓰지 않는다.

표준 출처는 ISO/IEC 17825:2024, Second edition, 2024-01이며 커밋 문서는 조항 번호와
요구 취지만 자체 문장으로 설명한다.
