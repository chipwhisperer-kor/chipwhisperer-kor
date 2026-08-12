# PROMPT.md — 사이클 계약

이 문서 하나만 읽고도 한 사이클을 끝까지 돌릴 수 있어야 한다.
행동 규칙은 `AGENTS.md`, 배경과 설계는 `README.md` 에 있다.

---

## 0. 시작 전 확인

```bash
docker exec -it chipwhisperer-kor bash
cd "/workspace/[extra] Physical-AI-SCA"
python3 -m physai.collectors.emulation --selftest --n 10
```

`selftest_ok: true` 가 아니면 **아무것도 수집하지 않는다.** 확인 항목은 넷이다.

| 게이트 | 실패하면 |
|---|---|
| 골든 AES 일치 | 에뮬레이션 환경이 잘못됐다. 하네스 빌드부터 다시 본다 |
| 마스크 회수 (masked) | 시드 주입 경로가 끊겼다. `vir_IN[32:36]` 규약을 확인한다 |
| **명령어 수 고정** | `sample_map` 이 성립하지 않는다. 누설 검정을 진행할 수 없다 (TA 는 유효) |
| Trace 1개당 소요 시간 | 목표 트레이스 수를 다시 정한다 |

---

## 1. 사이클

```
① 설계    exp/<id>.yaml 작성          ← AI 가 하는 일
② 수집    collect  (계획 보고서 자동 생성 → 수집)
③ 분석    analyze  (TA → SPA → DPA → soundness → cpa)
④ 해석    results.json 읽기            ← AI 가 하는 일
⑤ 보고    report   (분석 보고서 + 증거 번들)
⑥ 검증    verify   (해시·스키마·툴체인)
```

**②와 ③, ⑤, ⑥ 은 도구가 결정적으로 수행한다.** AI 가 하는 일은 ①과 ④뿐이다.

---

## 2. ① 실험 설계 — spec 작성

`contracts/experiment_spec.schema.json` 이 계약이고, `spec.load()` 가 위반을 전부 모아
알려 준다. 기존 spec 을 복사해 시작하되 아래는 **매번 다시 생각한다.**

### 반드시 채워야 하는 것

| 필드 | 주의 |
|---|---|
| `scope.not_claimed` | **비울 수 없다.** 이 실험에서 실제로 못 하는 것을 다시 센다 |
| `criteria.sensitive_leakage_time.rationale` | 이 경계가 합/부를 직접 바꾼다. Annex H.2(a)와 다르게 정했다면 그 이유를 적는다 |
| `criteria.vendor_info` | 3항목(`shall [07.04]`). 벤더 = 시험자이므로 스스로 적는다 |
| `criteria.preprocessing.average_n` | Level 3 은 10을 요구한다. 1이면 미준수이며 대조표에 그대로 나온다 |
| `rationale` | 왜 이 실험을 하는가. 계획 보고서 첫머리에 실린다 |

### 적지 않는 것

**필요 트레이스 수 N 을 spec 에 적지 않는다.** `spec.required_n()` 이 Formula (1) 로 계산한다.
트레이스 수는 판단이 아니라 α·β·d 의 **결과**이고, 따로 적으면 파라미터와 어긋난다.

### subset 구성 — 분석이 요구하는 role

| 분석 | 필요한 role |
|---|---|
| `ta` | `timing` × 2 (랜덤 키+고정 평문 / 고정 키+랜덤 평문) |
| `spa` | `simple-analysis` — `same-data`, **`different-data-fixed`(키가 다름)**, `different-data-random` |
| `dpa` | `leakage-detection-fixed` + `leakage-detection-random` |
| `soundness` | `profiling` |
| `cpa` | `attack` |

`spa` 가 보는 것은 **키가 다른 쌍**이다. 평문이 다르면 트레이스도 다른 것은 모든 구현에서
당연하므로 근거가 될 수 없다(§8.3.1 이 지목한 표적은 key derivation 이다).

**`spa` 는 `pass` 도 `fail` 도 내지 않는다.** A.2.2 가 요구하는 육안 검사는 사람의 몫이고,
잡음 바닥이 0 인 결정적 채널에서는 키가 다르면 트레이스가 거의 항상 달라서 그것만으로
fail 을 내면 판별력이 없다. 결과는 언제나 `inconclusive` 이며 `statistical_verdict` 가
무엇이 관측되었는지 말한다 — `key-dependent-structure-observed` / `no-difference-beyond-noise`
/ `requirements-unmet`. 판정은 그림과 이 값을 보고 사람이 한다.

---

## 3. ② 수집

```bash
python3 -m physai.collect --spec exp/<id>.yaml
```

수집 **전에** `runs/<id>/01_experiment_plan.md` 가 먼저 생긴다. 이것이 사후 정당화를
막는 구조적 장치다. 수집이 끝나면 스키마 검증이 자동으로 돌고, 위반이 있으면 종료 코드가
0이 아니다.

실물 수집기(`cw_power`·`cw_debugtrace`)는 **실행되지 않는다** — 명확한 안내와 함께
`NotImplementedError` 를 낸다. 실장비가 준비되면 각 파일 머리말의 순서를 따른다.

---

## 4. ③ 분석

```bash
python3 -m physai.analyze --spec exp/<id>.yaml
```

TA → SPA → DPA 순서로 수행한다. **앞이 fail 이어도 뒤를 계속 수행한다** — §8.1 이 셋을
모두 평가하라고 `shall` 로 요구하기 때문이다(순서는 should). 유일한 예외는 TA 내부의
2단계로, §7.3.4 가 1단계 실패 시 2단계로 가지 않는다고 명시한다.

`--n-soundness` 와 `--n-perm` 으로 soundness 의 비용을 조절할 수 있다.
`--n-perm` 은 귀무분포용 라벨 순열 횟수이며, 적으면 임계가 덜 보수적이 된다.

---

## 5. ④ 결과 해석 — AI 가 하는 일

`runs/<id>/results.json` 을 읽는다. **`grades` 필드를 먼저 본다.**

| 등급 | 항목 | 다루는 법 |
|---|---|---|
| `mandatory` | ta · spa · dpa | 판정 근거 |
| `judgement` | soundness | 판정 근거 |
| `reference_only` | snr | **합/부를 주장하지 않는다** |
| `positive_control` | cpa | 배관 검증. **판정 근거가 아니다** |

### 해석할 때 지킬 것

1. **`inconclusive` 를 `pass` 로 옮기지 않는다.** 트레이스 수 부족이나 육안 미결은 "안전" 이 아니다.
2. **`spa` 의 `inconclusive` 를 "안전" 으로 옮기지 않는다.** 그것은 이 도구가 판정할 수
   없다는 뜻이다. `statistical_verdict` 를 그대로 인용한다.
3. **경계 밖 검출을 fail 로 세지 않는다.** Annex H 에 따라 별도 목록으로 보고한다.
   단 감추지도 않는다 — 경계 설정이 옳았는지 다음 사람이 다시 볼 수 있어야 한다.
4. **결함 후보는 주소와 함께** 옮긴다. `arm-none-eabi-addr2line -e emul_harness/build/<IUT>.elf <주소>`
   로 소스 행을 찾을 수 있다(하네스는 `-gdwarf-2` 로 빌드한다).
5. **masked 에서 검출이 없었다면** `exp/001`(비마스킹 대조군)의 결과를 함께 인용한다.
   대조군 없는 "검출 없음" 은 의미가 없다.
6. **에뮬 TA 의 `cycle_accurate: false` 를 옮긴다.** 명령어 수가 같아도 constant-time 이
   증명된 것은 아니다.

---

## 6. ⑤ 보고 · ⑥ 검증

```bash
python3 -m physai.report --run <id>
python3 -m physai.verify --run <id>
```

`report` 는 분석 보고서와 증거 번들을 만든다. 그림도 여기서 나온다 — 특히
`spa_traces.svg` 는 **육안 검사의 근거 자료**이므로 반드시 증거에 포함된다.

`verify` 는 해시를 다시 계산해 대조하고, 데이터셋이 여전히 스키마를 지키는지, 툴체인이
같은지 확인한다. **툴체인 불일치는 경고이지 실패가 아니다** — 다른 버전에서 재현되는지는
실제로 다시 돌려 봐야 알 수 있고, 그것은 이 도구가 판단할 일이 아니다.

---

## 7. 사용자에게 보고할 때

세 문서의 경로와 함께 다음을 **반드시** 전한다.

- 종합 판정과 그것이 `pass`/`fail`/`inconclusive` 중 무엇인지
- **보지 않은 고리** — 이번에 어떤 채널을 쓰지 않았는지
- 요건 대조표의 `미준수`·`미기록` 개수
- 결함 후보가 있다면 **개수와 대표 주소**

"검증 완료" 라고 쓰지 않는다. 이 환경이 낼 수 있는 것은 **사전 진단 결과**이지 적합성
판정이 아니다.

---

## 8. 막혔을 때

| 증상 | 원인·조치 |
|---|---|
| `spec 계약 위반` | 메시지에 위반이 전부 나온다. 하나씩이 아니라 한 번에 고친다 |
| `analyses 에 'x' 가 있는데 role … subset 이 없다` | §2 의 role 표를 본다 |
| `관측 구간 명령어 수가 달라졌다` | 제어흐름이 데이터 의존이다. 타이밍 소견이며, 누설 검정은 진행 불가 |
| `데이터셋이 스키마를 어긴다` | 수집기가 필드를 빠뜨렸다. 지어내 채우지 말고 수집기를 고친다 |
| `manifest.json 이 없다` | `report` 를 먼저 돌린다 |
| 해시 불일치 | 파일이 바뀌었다. 무엇이 언제 바뀌었는지 확인하기 전에는 결과를 신뢰하지 않는다 |
