# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 이 저장소의 정체

ChipWhisperer 기반 부채널 분석(SCA)·오류주입(FA)을 가르치기 위한 **한국어 실습 저장소**다. 파이썬 패키지가 **아니다** — `setup.py`도, 테스트 스위트도, 린터도 없다. 산출물은 Jupyter 노트북, `make`로 빌드하는 타겟 펌웨어, 툴체인 전체를 담은 Docker 이미지, 그리고 각자 자기완결적인 `[extra]` 연구·문서 프로젝트들이다.

사용자가 읽는 모든 산문(README, 노트북 마크다운 셀, 코드 주석)은 **한국어**로 쓰여 있다. 수정할 때도 한국어를 유지하고, 기존 한국어 문서를 영어로 바꾸지 않는다.

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

**`scope`/`target`을 건드리는 모든 코드는 실장비가 있어야 하며 너는 검증할 수 없다.** 하드웨어 없이 돌아가는 유일한 프로젝트는 `[extra] PRE-SCA`(Unicorn 에뮬레이션)다. 코드가 맞아 보인다는 이유로 동작한다고 말하지 말고, 실행하지 않았다는 사실을 명시한다.

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

`MAX_DATA_LEN = 245`는 C 펌웨어와 노트북 **양쪽에 정의되어 있다** (SS_VER_2_1 최대 패킷 249바이트에서 프레이밍 제외). 바꾼다면 양쪽을 함께 바꾼다 — 불일치는 에러 없이 잘린 에코로만 나타난다.

## 파형 저장

**모든 파형 데이터셋은 저장소 루트의 `SCHEMA.md`를 따른다.** 용어는 `GLOSSARY.md`가 정본이며, 새 문서·주석·설명을 쓸 때 그 용어를 그대로 쓴다(정의는 영문, 파생 문서는 한글).

핵심만 요약하면: HDF5 파일 하나가 Dataset 한 벌(Target 1개 × Channel 1개)이고, 측정 조건은 **루트 HDF5 attrs**에, 실제 데이터는 `/<subset>/` 아래 행 정렬 배열 `trace`·`key`·`plaintext`·`ciphertext`(+선택 `mask`)로 둔다. subset 이름은 자유지만 `role`은 `SCHEMA.md` §4.1 목록에서 고른다. 캡처 루프가 확장할 수 있도록 `maxshape=(None, ...)`로 만든다.

주의할 함정 두 가지: OPTIMIST의 **Attributes**(`trace` 등)는 HDF5에서 *배열*로, OPTIMIST의 **Metadata**는 HDF5 *attrs*로 저장되어 이름이 엇갈린다(`GLOSSARY.md` §6). 그리고 **모르는 메타데이터는 추정치로 채우지 않는다** — 비워 두고 검증기가 "부분 준수"로 보고하게 둔다(`SCHEMA.md` §5.3).

준수 여부는 `scalib_common.validate_dataset(target=…)` 또는 `validate_dataset(path=…)`로 검사한다. 수집 직후 자동 호출된다.

시각화는 matplotlib이 아니라 `output_notebook()`을 쓰는 Bokeh다. 파형 파일은 용량이 크므로 요청받지 않는 한 커밋에 넣지 않는다.

현재 상태: `[extra] SCALib`의 h5 2개는 **완전 준수**, 튜토리얼 `workspace/traces/*.h5`는 스키마 제정 이전 수집분이라 **부분 준수**(복원 불가능한 측정 조건 4개 누락).

## `[extra]` 프로젝트 — 각자가 자기 규칙을 갖는다

`[extra]` 접두사가 붙은 디렉터리는 공식 튜토리얼 경로와 무관한 연구·부속 프로젝트다. 각각 자기완결적으로 작성되어 있으므로 손대기 전에 그 프로젝트의 README를 먼저 읽고, 경로는 **그 프로젝트 루트 기준 상대경로**로 유지한다(여러 프로젝트가 호스트 절대경로를 명시적으로 금지한다).

- **`[extra] Paper-Deep-Dive/`** — **자체 `CLAUDE.md`·`AGENTS.md`·`PROMPT.md`가 있고, 그 디렉터리 안에서는 이 파일보다 우선한다.** 역할별 단독 쓰기 소유가 엄격한 4역할 문서 파이프라인이며, Claude는 `director` 역할에 바인딩되어 `Papers/**`, `.Intermediate_Artifacts/papers/**`, `Presentation_Marp/**`에 쓰면 안 된다. 사본이 여러 개 존재하고 낡은 사본도 안에서 보면 구별되지 않으므로 `.Intermediate_Artifacts/SYNC.md`를 제일 먼저 확인한다.
- **`[extra] PRE-SCA/`** — ARM 펌웨어(tiny-AES)를 Unicorn/Capstone으로 에뮬레이션하는 pre-silicon SCA/FI 실험. 하드웨어가 필요 없는 유일한 프로젝트다. `[naive] PRE-SCA/`는 스크립트 버전으로 `python3 main.py`(또는 N회 반복 `./run_main.sh <N>`)로 실행하며, 설정은 전부 `config.py`에 있다. `config.py`는 자기 snake_case 변수명이 `elfParser`·`emul`·`logger`에서 이름으로 참조되니 리팩터링 시 바꾸지 말라고 경고한다. 노트북 결과는 `nb_output/`에 쌓인다.
- **`[extra] SCALib/`** — SCALib 0.6.4의 기능을 **기능 하나당 노트북 하나**로 보이되, **Normal AES(`tiny-AES-c`) ∥ Masked AES(`masked-aes-c`) 이중 타겟**을 단계마다 나란히 비교하는 예제 모음(SNR·Quantizer·Ttest·MTtest·CPA·LDA·MultiLDA·RLDA·SASCA·KeyRank). CW308+STM32F3에서 **실측한 파형**을 쓴다. **하드웨어가 필요한 노트북은 `0.0.Dataset_Collect_tiny-AES-c.ipynb`와 `0.1.Dataset_Collect_masked-aes-c.ipynb` 둘**이고, 그것이 만든 `traces/scalib_dataset_{tiny-AES-c,masked-aes-c}.h5`를 분석 노트북 10개가 읽는다(GB 단위라 커밋하지 않는다). 파형 길이는 상수가 아니라 `scope.adc.trig_count`로 정해 AES 연산 전체(키 스케줄+10라운드)를 담는다.

  경로·타겟 레지스트리·AES 상수·데이터셋 로더는 `scalib_common.py`(`TARGETS`, `load_group(target=…)`, `group_len`) 한 곳에만, 수집 공용 로직은 `dataset_collect_lib.py` 한 곳에만 있다. **분석 로직은 노트북이 직접 보여 준다** — 교육 목적이라 공용 모듈로 빼지 않는다.

  수집 중 캡처는 반드시 `Bench.capture()`(`dataset_collect_lib.py`)로 한다. 장시간 수집은 USB 단절과 Husky 먹통으로 깨지므로 단순 재시도 3회 → 재연결 2회 → **Husky 펌웨어 재기록 1회** 순으로 스스로 복구하고, 복구 뒤 측정 설정과 마스크 시드를 되돌린다. 사람이 다시 눌러 줄 필요가 없어야 한다. Husky 펌웨어 손상은 **버전을 정상값으로 보고하면서** `cw.scope()` 만 `Unknown hwInfoVer` 로 실패하는 형태로 나타나며, USB 전원 차단이나 물리적 재삽입으로는 낫지 않고 재기록만 듣는다.

  이 서브프로젝트 고유의 세 가지 규칙:
  1. **관점 분리** — Masked h5에는 연구용 마스크 `mask (n,10)`이 들어 있다. **공격자 관점 셀은 절대 `mask`를 참조하지 않는다.** 쓰는 절은 "연구자" 로 제목을 분리한다.
  2. **비교는 암호화 구간에서만** — `masked-aes-c`는 `CipherMasked`만 보호하고 `KeyExpansion`은 벤더 원본 비마스킹인데, 펌웨어가 키 스케줄을 트리거 안에서 돌린다. 전 구간 비교는 이 공통 누설에 지배된다(전 구간 TVLA `|t|`가 Normal 114 / Masked 116으로 차이가 없어 보인다). `1.0`이 평문 의존 누설 시작점 `enc_start`를 실측해 `nb_output/poi_*.npz`에 저장하고 `2.0`–`6.0`이 그 이후만 본다.
  3. **장수는 목표치가 아니라 실보유량** — `N_PROFILING` 같은 상수는 수집 목표다. 분석은 `group_len()`으로 실제 장수를 읽고, 타겟 간 비교는 양쪽을 같은 예산으로 맞춘다.

  Masked 데이터셋은 현재 **임시(`provisional=1`)** 상태다(profiling 18,520장, 편향된 마스크 RNG로 수집). 배경과 폐기 조건은 그 프로젝트 README §7에 있다. 커스텀 프로토콜은 공통 `0x81 k/p/l`·`0x82 c`·`0x83 r`에 더해 Masked 전용 `0x81 's'`(마스크 시드)·`0x83 'm'`(마스크 회수)이 있다.
- **`[extra] Presentation_Marp/`** — Marp 발표자료. `0. Template/presentation.md`가 템플릿이자 문법 레퍼런스다(`marp: true`, `size: "16:9"`, `lang: ko`, `math: mathjax`; 클래스 `lead`, `divider`, `small`, `tiny`, `code-small`, `code-tiny`). `marp` 바이너리는 설치되어 있지 않다 — 슬라이드는 에디터 확장에서 미리보기만 하며 여기서 빌드하지 않는다.

## 실무 메모

- 경로에 공백·한글·`[...]`가 들어 있다. 셸 명령에서는 항상 따옴표로 감싼다.
- 루트의 **`gitignore/`는 로컬 전용 보관함**이다. 루트 `.gitignore`가 `/gitignore/`로 통째로 제외하므로 그 안의 파일은 git에 전혀 나타나지 않는다. 커밋하면 안 되지만 작업에는 필요한 것을 여기 둔다 — 현재는 저작권 보호 문서인 ISO/IEC 17825:2024 원문(`ISO_IEC17825_2024_EN.pdf`)이 있다. **새로 클론한 사람에게는 이 디렉터리가 없으므로**, 여기 있는 파일에 의존하는 문서는 로컬 전용임을 밝히고 원본 출처(URL)를 함께 적는다.
- 이 저장소의 1차 소스는 노트북이다. JSON을 직접 고치기보다 노트북으로 편집(NotebookEdit)하고, 한국어 마크다운 셀과 그것이 설명하는 코드 셀을 함께 갱신한다.
- 컨테이너는 root로 동작하며 호스트 파일을 마운트하므로, 컨테이너 안에서 만든 파일은 호스트에서 root 소유가 된다. 이 UID 불일치로 git이 막히지 않도록 Dockerfile이 `git config --global --add safe.directory '*'`를 설정해 둔다.
