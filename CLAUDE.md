# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 이 저장소의 정체

ChipWhisperer 기반 부채널 분석(SCA)·오류주입(FA)을 가르치기 위한 **한국어 실습 저장소**다. 파이썬 패키지가 **아니다** — `setup.py`도, 테스트 스위트도, 린터도 없다. 산출물은 Jupyter 노트북, `make`로 빌드하는 타겟 펌웨어, 툴체인 전체를 담은 Docker 이미지, 그리고 각자 자기완결적인 `[extra]` 연구·문서 프로젝트들이다.

사용자가 읽는 모든 산문(README, 노트북 마크다운 셀, 코드 주석)은 **한국어**로 쓰여 있다. 수정할 때도 한국어를 유지하고, 기존 한국어 문서를 영어로 바꾸지 않는다.

저장소 루트의 `AGENTS.md`는 모든 에이전트에게 구속력이 있으며 이 파일보다 우선한다. 3원칙 요약: (1) **단일 진실 공급원** — 기억이 아니라 실제 파일을 읽어 확인하고, 하나의 정의는 한 파일에만 둔다. (2) **단순함** — 요청된 문제만 풀고, 선제적 hook·wrapper·config flag를 만들지 않으며, 추상화는 실제 중복 3회 이후에, 불필요해진 코드는 주석 처리가 아니라 삭제한다. (3) **자기완결적 문서** — 배경 지식 없는 독자가 그 설명 하나로 이해할 수 있어야 하므로 *why*(제약, 버린 대안)를 쓰고, 코드와 문서를 같은 작업 안에서 함께 고친다. 사소하지 않은 변경 전에는 `AGENTS.md` 원문을 읽는다.

## 실행 모델 — 모든 것은 컨테이너 안에서 돈다

개발은 VMware **Ubuntu 게스트**에서 이뤄진다 (문서에서 "host"는 물리 PC가 아니라 이 게스트 = Docker 호스트를 가리킨다). `setup/docker-compose.yml`은 `workspace/`를 컨테이너의 `/workspace`에 bind-mount하고 `privileged` + `/dev/bus/usb` 매핑으로 ChipWhisperer 하드웨어에 접근한다. 노트북 실행과 펌웨어 빌드는 **컨테이너 안에서** 하는 것을 전제로 한다 — Python 3.9, `chipwhisperer`, `gcc-arm-none-eabi`, `gcc-avr`는 컨테이너에만 있고 호스트에는 보통 없다.

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

수집 결과는 `workspace/traces/*.h5`(`h5py` HDF5)에 저장된다. 캡처 루프가 확장할 수 있도록 `maxshape=(None, ...)`로 만든 행 정렬 데이터셋 4개를 쓴다: `i_k`(키), `i_p`(평문), `o`(타겟 출력), `t`(파형 샘플). 시각화는 matplotlib이 아니라 `output_notebook()`을 쓰는 Bokeh다. 파형 파일은 용량이 크므로 요청받지 않는 한 커밋에 넣지 않는다.

## `[extra]` 프로젝트 — 각자가 자기 규칙을 갖는다

`[extra]` 접두사가 붙은 디렉터리는 공식 튜토리얼 경로와 무관한 연구·부속 프로젝트다. 각각 자기완결적으로 작성되어 있으므로 손대기 전에 그 프로젝트의 README를 먼저 읽고, 경로는 **그 프로젝트 루트 기준 상대경로**로 유지한다(여러 프로젝트가 호스트 절대경로를 명시적으로 금지한다).

- **`[extra] Paper-Deep-Dive/`** — **자체 `CLAUDE.md`·`AGENTS.md`·`PROMPT.md`가 있고, 그 디렉터리 안에서는 이 파일보다 우선한다.** 역할별 단독 쓰기 소유가 엄격한 4역할 문서 파이프라인이며, Claude는 `director` 역할에 바인딩되어 `Papers/**`, `.Intermediate_Artifacts/papers/**`, `Presentation_Marp/**`에 쓰면 안 된다. 사본이 여러 개 존재하고 낡은 사본도 안에서 보면 구별되지 않으므로 `.Intermediate_Artifacts/SYNC.md`를 제일 먼저 확인한다.
- **`[extra] pdf2md/`** — 논문 PDF 아카이브 → Markdown → 리서치 갭 파이프라인. 그 프로젝트 루트에서 실행: `python3 kit/tools/list_pdf_queue.py --pending-only`, `pdf_to_markdown.py`, `run_candidates.py`, `diff_candidates.py`, `curate_to_verified.py`. 설계상 **텍스트 전용** — OCR도, 이미지 추출도 하지 않는다. 규격은 `kit/PDF_TO_MARKDOWN.md`, 허용 도구는 `kit/TOOL_ALLOWLIST.md`.
- **`[extra] PRE-SCA/`** — ARM 펌웨어(tiny-AES)를 Unicorn/Capstone으로 에뮬레이션하는 pre-silicon SCA/FI 실험. 하드웨어가 필요 없는 유일한 프로젝트다. `[naive] PRE-SCA/`는 스크립트 버전으로 `python3 main.py`(또는 N회 반복 `./run_main.sh <N>`)로 실행하며, 설정은 전부 `config.py`에 있다. `config.py`는 자기 snake_case 변수명이 `elfParser`·`emul`·`logger`에서 이름으로 참조되니 리팩터링 시 바꾸지 말라고 경고한다. 노트북 결과는 `nb_output/`에 쌓인다.
- **`[extra] TVLA/`** — tiny-AES-c 빌드를 대상으로 한 SCALib 기반 TVLA(누출 평가) 실험. 빌드 산출물이 함께 들어 있고 재구성이 진행 중이므로 경로가 고정이라고 가정하기 전에 `git status`를 확인한다.
- **`[extra] Presentation_Marp/`** — Marp 발표자료. `0. Template/presentation.md`가 템플릿이자 문법 레퍼런스다(`marp: true`, `size: "16:9"`, `lang: ko`, `math: mathjax`; 클래스 `lead`, `divider`, `small`, `tiny`, `code-small`, `code-tiny`). `marp` 바이너리는 설치되어 있지 않다 — 슬라이드는 에디터 확장에서 미리보기만 하며 여기서 빌드하지 않는다.

## 실무 메모

- 경로에 공백·한글·`[...]`가 들어 있다. 셸 명령에서는 항상 따옴표로 감싼다.
- 이 저장소의 1차 소스는 노트북이다. JSON을 직접 고치기보다 노트북으로 편집(NotebookEdit)하고, 한국어 마크다운 셀과 그것이 설명하는 코드 셀을 함께 갱신한다.
- 컨테이너는 root로 동작하며 호스트 파일을 마운트하므로, 컨테이너 안에서 만든 파일은 호스트에서 root 소유가 된다. 이 UID 불일치로 git이 막히지 않도록 Dockerfile이 `git config --global --add safe.directory '*'`를 설정해 둔다.
