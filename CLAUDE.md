# CLAUDE.md

이 문서는 이 저장소에서 작업하는 Claude Code(claude.ai/code)의 프로젝트별 작업 기준이다.

## 이 저장소의 정체

ChipWhisperer 기반 부채널 분석(SCA)·오류주입(FA)을 가르치기 위한 **한국어 실습 저장소**다. 파이썬 패키지가 **아니다** — `setup.py`도, 테스트 스위트도, 린터도 없다. 산출물은 Jupyter 노트북, `make`로 빌드하는 타겟 펌웨어, 툴체인 전체를 담은 Docker 이미지, 그리고 각자 자기완결적인 `[extra]` 연구·문서 프로젝트들이다.

프로젝트가 작성한 활성 산문(README, 노트북 Markdown 셀, 코드 주석)은 **한국어 위주**로
쓴다. 용어 정의문과 코드 식별자·두문자어에는 `GLOSSARY.md`의 언어 규칙을 적용한다.
상위 프로젝트 원본과 외부 소스의 문구는 임의로 번역하지 않는다.

저장소 루트의 `AGENTS.md`는 모든 에이전트에게 구속력이 있으며 이 파일보다 우선한다. 3원칙 요약: (1) **단일 진실 공급원** — 기억이 아니라 실제 파일을 읽어 확인하고, 하나의 정의는 한 파일에만 둔다. (2) **단순함** — 요청된 문제만 풀고, 선제적 hook·wrapper·config flag를 만들지 않으며, 추상화는 실제 중복 3회 이후에, 불필요해진 코드는 주석 처리가 아니라 삭제한다. (3) **자기완결적 문서** — 배경 지식 없는 독자가 그 설명 하나로 이해할 수 있어야 하므로 *why*(제약, 버린 대안)를 쓰고, 코드와 문서를 같은 작업 안에서 함께 고친다. 사소하지 않은 변경 전에는 `AGENTS.md` 원문을 읽는다.

## 실행 모델 — 모든 것은 컨테이너 안에서 돈다

개발은 VMware **Ubuntu 게스트**에서 이뤄진다 (문서에서 "host"는 물리 PC가 아니라 이 게스트 = Docker 호스트를 가리킨다). `setup/docker-compose.yml`은 `workspace/`를 컨테이너의 `/workspace`에 bind-mount하고 `privileged` + `/dev/bus/usb` 매핑으로 ChipWhisperer 하드웨어에 접근한다. 노트북 실행과 펌웨어 빌드는 **컨테이너 안에서** 하는 것을 전제로 한다 — Python 3.12, `chipwhisperer`, `gcc-arm-none-eabi`, `gcc-avr`는 컨테이너에만 있고 호스트에는 보통 없다.

파이썬 버전은 3.12가 상한이다. chipwhisperer 6.0.0이 `numpy<=1.26.4`를 요구하는데 numpy 1.26.4에는 cp313 휠이 없다. 또한 chipwhisperer가 `capture/trace/TraceWhisperer.py`에서 `pkg_resources`를 import하고 이 모듈은 `import chipwhisperer`만으로 로드되므로, `setuptools<82` 핀(pkg_resources는 82.0.0에서 삭제됨)이 필수다. 두 제약 모두 `setup/cw-build/requirements.txt`에 이유와 함께 적혀 있다.

```bash
cd setup/
docker compose up -d --build        # cw-build/requirements.txt · extensions.txt 수정 시 재빌드 필수
docker compose ps / logs -f / restart / down
docker exec -it chipwhisperer-kor bash   # 컨테이너 셸, 작업 디렉터리 /workspace

# 호스트 최초 1회 설정 (udev + 그룹), 이후 재부팅:
sudo cp ./setup/50-newae.rules /etc/udev/rules.d/50-newae.rules && sudo udevadm control --reload-rules
sudo groupadd -fr chipwhisperer && sudo usermod -aG chipwhisperer,plugdev,docker $USER
```

같은 컨테이너에 두 가지 방식으로 붙는다: 브라우저 code-server(`http://localhost:8080`, `--auth none`) 또는 host VS Code의 *Dev Containers: Attach to Running Container*. 확장 목록은 `setup/cw-build/extensions.txt`(code-server용)와 `setup/cw-build/Dockerfile`의 `devcontainer.metadata` LABEL(원격 세션용) **두 곳에 따로** 있다 — 한쪽만 고치면 다른 쪽은 바뀌지 않는다.

**`scope`/`target`을 건드리는 모든 코드는 실장비가 있어야 하며 너는 검증할 수 없다.** 하드웨어 없이 돌아가는 것은 `[extra] PRE-SCA`(Unicorn 에뮬레이션)와 `[extra] Physical-AI-SCA`의 **에뮬레이션 경로**뿐이다(그 프로젝트의 실물 수집기 2종은 골격만 있고 실행된 적이 없다). 코드가 맞아 보인다는 이유로 동작한다고 말하지 말고, 실행하지 않았다는 사실을 명시한다.

## 펌웨어 빌드 (`workspace/base/` + 튜토리얼별 `simpleserial_main/`)

`workspace/base/`는 ChipWhisperer 원본 펌웨어 트리(`Makefile.inc`, `hal/`, `crypto/`, `simpleserial/`)이며, 상위 플랫폼 지원을 유지하기 위해 수정하지 않는다. 각 튜토리얼은 자기 `simpleserial_main/`(또는 `simpleserial-trace/`)에서 `TARGET`·`SRC`만 정하고 `FIRMWAREPATH = ../../base/.`로 `../../base/Makefile.inc`를 `include`한다. 빌드는 항상 그 프로젝트 디렉터리에서, 빌드 변수는 전부 명령줄로 넘긴다.

```bash
cd "workspace/1. SCA and FA/simpleserial_main"
make PLATFORM=CW308_STM32F3 CRYPTO_TARGET=NONE SS_VER=SS_VER_2_1 clean
make PLATFORM=CW308_STM32F3 CRYPTO_TARGET=NONE SS_VER=SS_VER_2_1
# → simpleserial-base-CW308_STM32F3.hex  (오브젝트는 objdir-$(PLATFORM)/ 아래)
```

플랫폼 이름은 `workspace/base/hal/Makefile.hal`의 `PLATFORM_LIST`에서 온다. 여기서 쓰는 둘은 `CW308_STM32F3`(CW308 UFO + STM32F303)와 `CWHUSKY`(CW312_SAM4S의 별칭)다. 출력 파일명이 `$(TARGET)-$(PLATFORM)` 형태라 다른 플랫폼의 낡은 바이너리를 실수로 프로그래밍하기 쉽다 — 노트북들이 빌드 전후로 모든 플랫폼·`SS_VER` 조합을 `clean`하는 이유다.

## 노트북 연결 구조

튜토리얼 노트북은 직접 하드웨어에 연결하지 않는다. 흐름은 다음과 같다.

`<튜토리얼>.ipynb`에서 `PLATFORM` 설정 → `%run '../base/My_Setup.ipynb'` → 그 안에서 `%%bash`로 펌웨어 빌드, `%run '../base/Setup_Generic.ipynb'`(순수 `cw.scope()` / `cw.target()`), `cw.program_target(...)` 수행 후 공용 헬퍼 정의.

`base/My_Setup.ipynb`가 정의하고 튜토리얼이 의존하는 헬퍼: `my_fsr_cmd(target, cmd, scmd, data, payload_only)`, `my_setting_num_samples(...)`(측정된 `trig_count`로부터 `scope.adc.samples`를 유도), `my_get_trace(target, scope)`, `cwUFO_reboot_flush()`. 공용 헬퍼는 노트북마다 복사하지 말고 여기에 추가한다(AGENTS.md 1-2). 예외는 `3. Release the Husky`로, 장비 **2대**(Lite = 프로그래밍·통신, Husky = 수동 관측)를 다루기 때문에 `My_Setup.ipynb` 대신 `My_script.ipynb`에서 자체 연결을 수행한다.

### 커스텀 SimpleSerial 2.1 프로토콜

`simpleserial_main/simpleserial-base.c`의 펌웨어는 기본 `'k'`/`'p'` SimpleSerial 명령을 **쓰지 않는다.** 아래 3개 명령을 등록하며, 노트북도 정확히 이 규약으로 통신한다.

| cmd | scmd | 의미 |
|-----|------|------|
| `0x81` | `'k'` / `'p'` / `'l'` | 키 / 평문 / 출력 길이 쓰기. 타겟이 저장한 값을 그대로 에코 |
| `0x82` | `'c'` | `trigger_high()`와 `trigger_low()` 사이에서 연산 수행(기본 `MY_OTP`), 응답 페이로드는 `0x82` |
| `0x83` | `'r'` | 결과 `global_len` 바이트 회수 |

C 펌웨어의 `MAX_DATA_LEN = 245`는 SimpleSerial 핸들러와 전역 버퍼의 **수용 한도**다.
튜토리얼 노트북은 같은 이름을 현재 전송할 payload 길이로 사용하며, 통신 점검에서는 245,
Dataset 수집에서는 16처럼 셀마다 다시 정한다. 둘은 같은 정의가 아니다. 노트북 값은 C의
수용 한도를 넘으면 안 되고, `0x81 'l'`로 보낸 1바이트 값이 실제 `global_len`이 된다.
동일한 식별자가 두 의미를 갖는 구조는 코드 리팩터링 전까지 유지되는 제약이므로 새 설명에서
두 값을 하나의 공유 상수처럼 서술하지 않는다.

## Trace(트레이스) 저장

**모든 Trace Dataset(데이터셋)은 저장소 루트의 `SCHEMA.md`를 따른다.** 용어는
`GLOSSARY.md`가 정본이다. 정본의 정의문은 영문을 유지하고, 파생 문서·주석·설명은 한국인
연구자를 독자로 삼아 한글 위주로 쓴다. 코드 식별자와 두문자어는 영문 원형을 유지한다.

핵심 구조는 HDF5 파일 하나가 Dataset 한 벌(Target 1개 × Channel 1개)이라는 것이다.
측정 조건은 **루트 HDF5 attrs**에, Record(레코드)별 Attributes(어트리뷰트)는
`/<subset>/` 아래의 HDF5 dataset(배열)에 둔다. 필수·선택 필드와 현재 판번호는
`SCHEMA.md`에서만 정의한다.

주의할 함정 두 가지: OPTIMIST의 **Attributes**(`trace` 등)는 HDF5에서 *배열*로, OPTIMIST의 **Metadata**는 HDF5 *attrs*로 저장되어 이름이 엇갈린다(`GLOSSARY.md` §6). 그리고 **모르는 메타데이터는 추정치로 채우지 않는다** — 비워 두고 검증기가 "부분 준수"로 보고하게 둔다(`SCHEMA.md` §5.3).

준수 여부는 **`workspace/lib/sca_schema.py`의 `validate_dataset(path=…)`**로 검사한다. 세 수집 경로(실물 전력·디버그 트레이스·에뮬레이션)가 같은 검증기를 통과해야 "준수"의 뜻이 하나로 유지되므로 저장소 공용 트리에 있다. `[extra] SCALib/scalib_common.py`는 이것을 **재노출**하므로 그 프로젝트 노트북 12개는 종전대로 `validate_dataset(target=…)`을 쓴다 — 승격하면서 노트북을 한 줄도 고치지 않기 위한 장치다.

검증기는 파일에 적힌 판번호의 규칙을 적용한다. 나중 규칙으로 기존 Dataset을 소급
판정하지 말고, 수집기는 실제로 기록하는 필드에 맞는 판번호를 써야 한다.

## 저장소 공용 트리 — `workspace/lib/`·`workspace/iut/`

한 서브프로젝트 안에만 두면 두 번째 소비자가 생기는 순간 사본이 생기는 것들을 올려 둔 곳이다(AGENTS.md 1-2).

| 위치 | 내용 | 쓰는 곳 |
|---|---|---|
| `workspace/lib/sca_schema.py` | 스키마 상수·검증기·경로 기반 로더 | 세 수집 경로 전부 |
| `workspace/lib/aes_ref.py` | `SBOX`·`HW`·`sbox_out`·`aes_ecb_encrypt`·**`intermediates()`** | 수집기의 골든 검증, 분석의 민감값 라벨 |
| `workspace/iut/{tiny-AES-c,masked-aes-c}/` | IUT(테스트 대상 구현) 암호 라이브러리 | SCALib 펌웨어 2종 + 에뮬 하네스 2종 |

**암호 라이브러리를 공용 트리에 둔 이유**: 실물 펌웨어와 에뮬레이션 하네스가 **같은 `aes.c`를 같은 플래그(`-Os`)로** 컴파일해야 "에뮬에서 찾은 결함이 실측 타겟에도 있다"고 말할 근거가 생긴다. 최적화 수준이 전이 누설을 만들기도 하고 없애기도 하므로 플래그가 다르면 다른 구현을 분석하는 셈이다. 경로를 옮기면 makefile 2개·수집 노트북 2개·SCALib README·`workspace/iut/README.md`를 함께 고치고 **`clean` 재빌드**한다(빌드 산출물에 소스 경로가 문자열로 박힌다).

`intermediates()`가 공용인 이유도 같다 — 에뮬과 실측이 서로 다른 값을 같은 이름으로 부르면 비교가 조용히 무너진다.

시각화는 matplotlib이 아니라 `output_notebook()`을 쓰는 Bokeh다. 트레이스 파일은 용량이 크므로 요청받지 않는 한 커밋에 넣지 않는다.

현재 checkout에는 `[extra] SCALib/traces/`의 생성 HDF5 파일이 없고 과거 노트북 실행 출력만
남아 있다. 따라서 두 파일의 현재 준수를 주장하지 않는다. 튜토리얼의
`workspace/traces/20260427_143337_SCA_DB.h5`는 스키마 제정 이전 수집분이라 기존 문서에서
부분 준수로 분류하지만, 이 환경에는 `h5py`가 없어 이번 점검에서 검증기를 다시 실행하지 못했다.

## `[extra]` 프로젝트 — 각자가 자기 규칙을 갖는다

`[extra]` 접두사가 붙은 디렉터리는 공식 튜토리얼 경로와 무관한 연구·부속 프로젝트다. 각각 자기완결적으로 작성되어 있으므로 손대기 전에 그 프로젝트의 README를 먼저 읽고, 경로는 **그 프로젝트 루트 기준 상대경로**로 유지한다(여러 프로젝트가 호스트 절대경로를 명시적으로 금지한다).

- **`[extra] Paper-Deep-Dive/`** — **자체 `CLAUDE.md`·`AGENTS.md`·`PROMPT.md`가 있고, 그 디렉터리 안에서는 이 파일보다 우선한다.** 역할별 단독 쓰기 소유가 엄격한 4역할 문서 파이프라인이며, Claude는 `director` 역할에 바인딩되어 `Papers/**`, `.Intermediate_Artifacts/papers/**`, `Presentation_Marp/**`에 쓰면 안 된다. 사본이 여러 개 존재하고 낡은 사본도 안에서 보면 구별되지 않으므로 `.Intermediate_Artifacts/SYNC.md`를 제일 먼저 확인한다.
- **`[extra] PRE-SCA/`** — ARM 펌웨어(tiny-AES)를 Unicorn/Capstone으로 에뮬레이션하는 pre-silicon SCA/FI 실험. 하드웨어가 필요 없다(`[extra] Physical-AI-SCA`의 에뮬 경로도 그렇다). 그 프로젝트가 이 트리의 **`elfParser.ElfParser`를 재사용**한다 — ELF 파싱 정의는 여기 한 곳이다. 다만 `logger.py`/`emul.py`는 쓰지 않는다. 전역 로거가 실행마다 CSV를 쓰고 에뮬레이션 훅이 명령어마다 입력 CSV를 다시 읽는 구조라, 오류주입 디버깅에는 맞지만 수천 Record 수집에는 I/O 비용이 지나치게 크기 때문이다. `[naive] PRE-SCA/`는 스크립트 버전으로 `python3 main.py`(또는 N회 반복 `./run_main.sh <N>`)로 실행하며, 설정은 전부 `config.py`에 있다. `config.py`의 snake_case 변수명은 `elfParser`·`emul`·`logger`가 이름으로 참조하므로 바꾸면 안 된다. 노트북 결과는 `nb_output/`에 쌓인다.
- **`[extra] SCALib/`** — SCALib 0.6.4의 기능을 **기능 하나당 노트북 하나**로 보이되, **Normal AES(`tiny-AES-c`) ∥ Masked AES(`masked-aes-c`) 이중 타겟**을 단계마다 나란히 비교하는 예제 모음(SNR·Quantizer·Ttest·MTtest·CPA·LDA·MultiLDA·RLDA·SASCA·KeyRank). **하드웨어가 필요한 노트북은 `0.0.Dataset_Collect_tiny-AES-c.ipynb`와 `0.1.Dataset_Collect_masked-aes-c.ipynb` 둘**이고, CW308+STM32F3에서 수집한 전력 Trace를 `traces/scalib_dataset_{tiny-AES-c,masked-aes-c}.h5`에 만든다. 분석 노트북 10개는 그 파일을 읽지만 GB 단위 생성물이라 커밋하지 않는다. 현재 checkout에는 HDF5 파일이 없고 수집 노트북의 과거 실행 출력만 남아 있다. Trace 길이는 수집 시 `scope.adc.trig_count`에서 정하며 AES 연산 전체(키 스케줄+10라운드)를 담도록 설계되어 있다.

  **암호 라이브러리는 이 서브프로젝트 밖에 있다** — `workspace/iut/{tiny-AES-c,masked-aes-c}/`. 펌웨어 makefile이 `../../iut/<lib>/aes.c`를 직접 컴파일한다. 세 수집 경로(실물 전력·디버그 트레이스·에뮬레이션)가 **같은 소스**를 봐야 결과를 나란히 놓을 수 있어서 저장소 공용 트리로 올렸다. 출처·패치 내역은 `workspace/iut/README.md`.

  경로·타겟 레지스트리·AES 상수·데이터셋 로더는 `scalib_common.py`(`TARGETS`, `load_group(target=…)`, `group_len`) 한 곳에만, 수집 공용 로직은 `dataset_collect_lib.py` 한 곳에만 있다. **분석 로직은 노트북이 직접 보여 준다** — 교육 목적이라 공용 모듈로 빼지 않는다.

  수집 중 캡처는 `Bench.capture()`(`dataset_collect_lib.py`)를 사용한다. 구현된 복구 순서는 단순 재시도 3회 → 재연결 2회 → **Husky 펌웨어 재기록 1회**이며, 재연결 뒤 측정 설정과 마스크 시드를 다시 적용한다. 펌웨어 재기록은 장치 상태를 덮어쓰는 부작용이 있으므로 `capture()`의 앞 단계가 모두 실패했을 때만 실행한다. 과거 Masked 수집의 저장된 노트북 출력에는 `reflash`, `reconnect`, `reconnect`가 기록되어 있지만, 현재 HDF5 파일이 없으므로 새 수집에서는 복구 이력과 설정 복원을 다시 확인해야 한다.

  이 서브프로젝트 고유의 세 가지 규칙:
  1. **관점 분리** — Masked h5에는 연구용 마스크 `mask (n,10)`이 들어 있다. **공격자 관점 셀은 절대 `mask`를 참조하지 않는다.** 쓰는 절은 "연구자" 로 제목을 분리한다.
  2. **비교는 암호화 구간에서만** — `masked-aes-c`는 `CipherMasked`만 보호하고 `KeyExpansion`은 벤더 원본 비마스킹인데, 펌웨어가 키 스케줄을 트리거 안에서 돌린다. 전 구간 비교는 이 공통 누설에 지배된다. 저장된 `2.0.Ttest.ipynb` 출력은 전 구간 최대 `|t|`가 Normal 114.31 / Masked 113.81임을 보여 준다. `1.0`은 Dataset에서 평문 의존 누설 시작점 `enc_start`를 산출해 `nb_output/poi_*.npz`에 저장하고 `2.0`–`6.0`은 그 이후만 보도록 작성되어 있다.
  3. **트레이스 수는 목표치가 아니라 실제 보유량** — `N_PROFILING` 같은 상수는 수집 목표다. 분석은 `group_len()`으로 실제 트레이스 수를 읽고, 타겟 간 비교는 양쪽을 같은 예산으로 맞춘다.

  저장된 수집 노트북 출력은 두 과거 실행이 profiling 목표 100,000 Record를 채웠고 검증기에서 위반을 보고하지 않았다고 기록한다. Masked 출력에는 `reflash`·`reconnect`·`reconnect` 복구 이력도 있다. 이는 현재 파일의 준수 증거가 아니므로 HDF5를 다시 만들면 검증기를 재실행한다. 마스크 RNG 패치는 벤더 원본 `rand() % 0xFF`가 제외하던 `0xFF`를 `rand() & 0xFF`로 포함하지만, `rand()`를 암호학적으로 안전한 RNG로 만들지는 않는다(`workspace/iut/masked-aes-c/aes.c`). 커스텀 프로토콜은 공통 `0x81 k/p/l`·`0x82 c`·`0x83 r`에 더해 Masked 전용 `0x81 's'`(마스크 시드)·`0x83 'm'`(마스크 회수)이 있다.
- **`[extra] Physical-AI-SCA/`** — **AI가 실험 설계·수집·분석·보고를 나누어 수행하는 사전 진단 환경.** 한 암호 구현을 세 방식으로 관측해(에뮬레이션·실물 전력·디버그 트레이스) 하나의 스키마·하나의 판정 규칙 위에 놓는다. 저장된 문서와 데모 출력은 에뮬레이션 경로의 과거 실행만 기록하며, 현재 `runs/`와 `traces/`에는 그 증거 파일이 없다. 실물 수집기 2종(`cw_power.py`·`cw_debugtrace.py`)은 미실행 골격이므로 동작한다고 주장하지 않는다.

  ISO/IEC 17825:2024 를 **준용**하되 **적합성 평가가 아니라 사전 진단(pre-assessment)**이다. §1 Scope 가 이 표준을 ISO/IEC 19790 적합성 판정용으로 정하고 24759 와 함께 암호모듈의 정의된 경계에서 쓰도록 하는데, 여기 IUT 는 모듈이 아니라 라이브러리이고 벤더와 시험자가 동일하며 승인 기관이 없다. 그래서 spec 의 `scope.not_claimed` 가 **비울 수 없는 필수 필드**다 — 무엇을 주장하지 않는지 적지 않으면 나머지가 전부 주장으로 읽힌다.

  CLI 는 `collect` → `analyze` → `report` → `verify` 이고 전부 `python3 -m physai.<이름>` 이다. **수치·판정·해시·요건 대조표는 전부 도구가 결정적으로 만든다.** LLM(`llm.py`, OpenAI 호환 함수 하나)은 보고서 서술 초안에만 관여하며, 환경변수가 없으면 서술 칸이 빈 채로 나머지가 다 채워진 문서가 나온다. 에이전트 루프·툴콜 파싱은 만들지 않는다 — 하네스가 할 일이다.

  필수 시험은 **TA·SPA·DPA 셋 모두**다(§7.3.2 `shall [07.03]`·§8.1 `shall [08.01]`). 순서는 TA→SPA→DPA 이나 **앞이 fail 이어도 뒤를 계속 수행한다** — 순서는 should, 전부 평가는 shall 이기 때문이다. **TA 는 캐시 유무와 무관하게 수행한다**(§8.2 의 캐시 면제는 Reference [50] 프레임워크에만 걸리며, Annex A 전체에서 `shall collect` 는 A.2.4 타이밍 하나뿐이다). 고차 제외는 **DPA 에만** 해당하고 TA 의 2차(분산) 검정은 의무다. CPA 는 판정이 아니라 배관 검증용 양성 대조다.

  누설 벡터는 `[hw_reg | hd_reg | hw_mem | hd_mem]` 연접이며 **HD 는 같은 저장소의 한 명령어 앞뒤 값끼리만** 계산한다(서로 다른 레지스터 쌍은 물리적 근거가 없고 오탐만 만든다). `sample_map` 이 샘플을 명령어 주소로 되짚어 주므로 결함 후보를 `addr2line` 으로 소스 행까지 옮길 수 있다 — 하네스를 `-gdwarf-2` 로 빌드하는 이유다.

  저장된 데모·진행 문서는 과거 실행에서 에뮬 명령어 수가 tiny 6,030 / masked 10,147로 일정했고, 골든 AES가 일치했으며, 비마스킹 대조군의 결함 후보에 `AddRoundKey`와 `SubBytes`가 포함됐다고 기록한다. 현재 실행 증거 번들이 없으므로 이 값과 소스 위치는 새 실행의 `results.json`·보고서·해시 번들로 다시 확인해야 한다.
- **`[extra] Presentation_Marp/`** — Marp 발표자료. `0. Template/presentation.md`가 템플릿이자 문법 레퍼런스다(`marp: true`, `size: "16:9"`, `lang: ko`, `math: mathjax`; 클래스 `lead`, `divider`, `small`, `tiny`, `code-small`, `code-tiny`). `marp` 바이너리는 설치되어 있지 않다 — 슬라이드는 에디터 확장에서 미리보기만 하며 여기서 빌드하지 않는다.

## 실무 메모

- 경로에 공백·한글·`[...]`가 들어 있다. 셸 명령에서는 항상 따옴표로 감싼다.
- 루트의 **`gitignore/`는 로컬 전용 보관함**이다. 루트 `.gitignore`가 `/gitignore/`로 통째로 제외하므로 그 안의 파일은 git에 전혀 나타나지 않는다. 커밋하면 안 되지만 작업에는 필요한 것을 여기 둔다 — 현재는 저작권 보호 문서인 ISO/IEC 17825:2024 원문(`ISO_IEC17825_2024_EN.pdf`)이 있다. **새로 클론한 사람에게는 이 디렉터리가 없으므로**, 여기 있는 파일에 의존하는 문서는 로컬 전용임을 밝히고 원본 출처(URL)를 함께 적는다.
- 이 저장소의 1차 소스는 노트북이다. JSON을 직접 고치기보다 노트북으로 편집(NotebookEdit)하고, 한국어 마크다운 셀과 그것이 설명하는 코드 셀을 함께 갱신한다.
- 컨테이너는 root로 동작하며 호스트 파일을 마운트하므로, 컨테이너 안에서 만든 파일은 호스트에서 root 소유가 된다. 이 UID 불일치로 git이 막히지 않도록 Dockerfile이 `git config --global --add safe.directory '*'`를 설정해 둔다.
