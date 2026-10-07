# CLAUDE.md

이 문서는 이 저장소에서 작업하는 Claude Code(claude.ai/code)의 프로젝트별 작업 기준이다.

## 이 저장소의 정체

ChipWhisperer 기반 부채널 분석(SCA)과 오류주입(FA)을 가르치기 위한 한국어 실습 저장소다. 파이썬 패키지가 아니므로 `setup.py`도, 테스트 스위트도, 린터도 없다. 산출물은 Jupyter 노트북, `make`로 빌드하는 타겟 펌웨어, 툴체인 전체를 담은 Docker 이미지, 그리고 각자 독립적으로 읽히는 `[extra]` 연구·문서 프로젝트들이다.

프로젝트가 작성한 활성 산문(README, 노트북 Markdown 셀, 코드 주석·docstring, 보고서 템플릿, 오류 메시지)은 한국어 위주로 쓴다. 문체는 `GLOSSARY.md` §1.4가 정한다. 종결어미는 한다/이다/했다이고, em-dash("—") 대신 콜론(":")과 두 문장 나누기를 쓰며, 이모지·본문 굵은 글씨·콜아웃 제목·경구체 단정을 쓰지 않고, §1.4의 어휘 대응표에 있는 단어(규약·정본·되읽기·배관·배선 등)는 쓰지 않는다. 남은 것은 루트의 `python3 style_check.py`로 센다. 용어 정의문과 코드 식별자·두문자어에는 `GLOSSARY.md` §1.1의 표기 규칙을 적용한다. 상위 프로젝트 원본과 외부 소스의 문구는 임의로 번역하지 않는다.

저장소 루트의 `AGENTS.md`는 모든 에이전트에게 구속력이 있으며 이 파일보다 우선한다. 3원칙을 요약하면 다음과 같다. 첫째, 단일 기준이다. 기억이 아니라 실제 파일을 읽어 확인하고, 하나의 정의는 한 파일에만 둔다. 둘째, 단순함이다. 요청된 문제만 풀고, 선제적 hook·wrapper·config flag를 만들지 않으며, 추상화는 실제 중복이 3회 생긴 뒤에 도입하고, 불필요해진 코드는 주석 처리가 아니라 삭제한다. 셋째, 자기완결적 문서다. 배경 지식 없는 독자가 그 설명 하나로 이해할 수 있어야 하므로 why(제약, 버린 대안)를 쓰고, 코드와 문서를 같은 작업 안에서 함께 고친다. 사소하지 않은 변경 전에는 `AGENTS.md` 원문을 읽는다.

## 실행 모델: 모든 것은 컨테이너 안에서 돈다

개발은 VMware Ubuntu 게스트에서 이뤄진다. 문서에서 "host"는 물리 PC가 아니라 이 게스트, 곧 Docker 호스트를 가리킨다. `setup/docker-compose.yml`은 `workspace/`를 컨테이너의 `/workspace`에 bind-mount하고 `privileged`와 `/dev/bus/usb` 매핑으로 ChipWhisperer 하드웨어에 접근한다. 노트북 실행과 펌웨어 빌드는 컨테이너 안에서 하는 것을 전제로 한다. Python 3.12, `chipwhisperer`, `gcc-arm-none-eabi`, `gcc-avr`는 컨테이너에만 있고 호스트에는 보통 없다.

파이썬 버전은 3.12가 상한이다. chipwhisperer 6.0.0이 `numpy<=1.26.4`를 요구하는데 numpy 1.26.4에는 cp313 휠이 없다. 또한 chipwhisperer가 `capture/trace/TraceWhisperer.py`에서 `pkg_resources`를 import하고 이 모듈은 `import chipwhisperer`만으로 로드되므로, `setuptools<82` 핀이 필요하다(pkg_resources는 82.0.0에서 삭제됐다). 두 제약 모두 `setup/cw-build/requirements.txt`에 이유와 함께 적혀 있다.

```bash
cd setup/
docker compose up -d --build        # cw-build/requirements.txt · extensions.txt 수정 시 재빌드 필수
docker compose ps / logs -f / restart / down
docker exec -it chipwhisperer-kor bash   # 컨테이너 셸, 작업 디렉터리 /workspace

# 호스트 최초 1회 설정 (udev + 그룹), 이후 재부팅:
sudo cp ./setup/50-newae.rules /etc/udev/rules.d/50-newae.rules && sudo udevadm control --reload-rules
sudo groupadd -fr chipwhisperer && sudo usermod -aG chipwhisperer,plugdev,docker $USER
```

같은 컨테이너에 두 가지 방식으로 붙는다. 하나는 브라우저 code-server(`http://localhost:8080`, `--auth none`)이고, 다른 하나는 host VS Code의 *Dev Containers: Attach to Running Container*다. 확장 목록은 `setup/cw-build/extensions.txt`(code-server용)와 `setup/cw-build/Dockerfile`의 `devcontainer.metadata` LABEL(원격 세션용) 두 곳에 따로 있다. 한쪽만 고치면 다른 쪽은 바뀌지 않는다.

`scope`/`target`을 건드리는 코드는 필요한 실장비가 연결된 세션에서 직접 실행해야만 검증할 수 있다. 하드웨어 없이 돌아가는 것은 `[extra] PRE-SCA`(Unicorn 에뮬레이션)와 `[extra] Physical-AI-SCA`의 에뮬레이션 경로다. Physical-AI-SCA의 `cw_power`는 통합 데모 006·007에서 실행되었지만, 새 장비나 변경된 코드는 별도 실행 근거가 필요하다. 코드가 맞아 보인다는 이유로 동작한다고 말하지 말고, 검증에 쓴 장치·경로와 실행 결과를 명시한다.

## 펌웨어 빌드 (`workspace/base/` + 튜토리얼별 `simpleserial_main/`)

`workspace/base/`는 ChipWhisperer 원본 펌웨어 트리(`Makefile.inc`, `hal/`, `crypto/`, `simpleserial/`)이며, 상위 플랫폼 지원을 유지하기 위해 수정하지 않는다. 각 튜토리얼은 자기 `simpleserial_main/`(또는 `simpleserial-trace/`)에서 `TARGET`·`SRC`만 정하고 `FIRMWAREPATH = ../../base/.`로 `../../base/Makefile.inc`를 `include`한다. 빌드는 항상 그 프로젝트 디렉터리에서 하고, 빌드 변수는 전부 명령줄로 넘긴다.

```bash
cd "workspace/1. SCA and FA/simpleserial_main"
make PLATFORM=CW308_STM32F3 CRYPTO_TARGET=NONE SS_VER=SS_VER_2_1 clean
make PLATFORM=CW308_STM32F3 CRYPTO_TARGET=NONE SS_VER=SS_VER_2_1
# → simpleserial-base-CW308_STM32F3.hex  (오브젝트는 objdir-$(PLATFORM)/ 아래)
```

플랫폼 이름은 `workspace/base/hal/Makefile.hal`의 `PLATFORM_LIST`에서 온다. 여기서 쓰는 둘은 `CW308_STM32F3`(CW308 UFO + STM32F303)와 `CWHUSKY`(CW312_SAM4S의 별칭)다. 출력 파일명이 `$(TARGET)-$(PLATFORM)` 형태라 다른 플랫폼의 낡은 바이너리를 실수로 프로그래밍하기 쉽다. 노트북들이 빌드 전후로 모든 플랫폼·`SS_VER` 조합을 `clean`하는 이유다.


## FPGA 비트스트림 빌드 (`workspace/4. FPGA CW310/fpga/`, 호스트에서 · 로컬 전용, git 제외)

저장소에는 비트스트림 2개(`fpga/build/{aes,wide}/cw310_top.bit`)와 레지스터 맵 `fpga/common/cw310_defines.v`만 둔다. 노트북이 읽는 FPGA 파일은 이 셋이 전부이고, Vivado가 유료라 실습자는 비트스트림만 받는다. HDL(`aes/`, `wide/`, `common/`의 나머지)·`cw310.xdc`·`build.tcl`·`build.sh`·Vivado 산출물은 이 머신의 로컬 연구용이며 새로 클론한 사람에게는 없다. 출처는 NewAE cw310-bergen-board 저장소의 `fpga/aes` 예제(https://github.com/newaetech/cw310-bergen-board)와 Google `aes_core`(Apache 2.0)다. 로컬 수정 내용은 XADC·ILA IP 제거, `O_clksettings` 포트 연결(`REG_CLKSETTINGS` 동작), `wide` 변종(폭 1024비트 + `xor_core` 더미)이다. 비트스트림이 어떤 빌드인지는 노트북이 `.bit` 헤더의 빌드 시각으로 확인한다.

```bash
cd "workspace/4. FPGA CW310/fpga"
./build.sh aes     # → build/aes/cw310_top.bit   (AES-128 레퍼런스)
./build.sh wide    # → build/wide/cw310_top.bit  (1024-bit 레지스터 + xor_core 더미)
```

`build.sh`는 Vivado를 `bwrap --unshare-net`(bubblewrap) 샌드박스 안에서 돌려 외부 통신을 막는다. `/home/user/vivado_local.sh`가 `sudo systemd-run -p IPAddressDeny=any`로 하던 것과 같은 목적이지만, root 권한이 필요 없고(비밀번호 프롬프트 없음) 산출물이 현재 사용자 소유다. 루트 파일시스템은 읽기 전용이고 `build/<design>/`·`~/.Xilinx`·`/tmp`만 쓰기 가능하며 `/sys`는 빈 tmpfs로 가린다. 네트워크 네임스페이스 안에서 호스트 sysfs가 보이면 Vivado 2018.2 라이선스 관리자가 libudev 장치 열거 중 메모리 오류로 죽기 때문이다. 이 오류는 라우팅 직후 WebTalk 단계에서 재현됐다. `XILINXD_LICENSE_FILE`(기본 `/home/user/SW/vivado2018+IPs.lic`, xc7k410t는 WebPACK 밖)를 환경변수로 넘긴다. `read_verilog` 등은 인자를 Tcl 리스트로 해석하므로 공백이 든 경로는 `build.tcl`에서 `[list …]`로 감싼다. `build.tcl`은 non-project 흐름(read_verilog → synth → opt → place → route → 타이밍 판정 → write_bitstream)이며, WNS/WHS가 음수면 `.bit`를 만들지 않고 exit 1 한다. 설계별 소스 목록은 `build.tcl`의 `srcs(...)`가 정의한다(glob 없음).

## 노트북 연결 구조

`1. SCA and FA/1.0.SCA_main.ipynb`, `2.0.FA_main.ipynb`, `2. TraceWhisperer/1.0.TraceWhisperer_main.ipynb`는 각각 자기완결적이다. 각 노트북은 내부 셀에서 필요한 패키지를 임포트하고 펌웨어를 clean·build한 뒤, 노트북 전용 `HUSKY_SERIAL_NUMBER`를 `cw.scope(sn=...)`에 전달해 지정 장비만 연결한다. 시리얼 없는 연결이나 다른 장비로의 fallback은 강의 장비 역할을 뒤바꿀 수 있으므로 두지 않는다.

SCA·FA는 독립 A–Z 실행을 위해 `reset_target`, `my_fsr_cmd`, `my_setting_num_samples`, `my_get_trace`와 SimpleSerial 2.1 빌드·프로그래밍을 각각 포함한다. TraceWhisperer는 자체 SimpleSerial 1.1 빌드·프로그래밍·trace 설정을 사용한다. `base/My_Setup.ipynb`와 `base/Setup_Generic.ipynb`는 다른 사용처를 위해 유지하지만 이 세 입문 노트북은 실행하지 않는다.

`3. Release the Husky`의 두 와이어태핑 노트북도 자기완결적이다. 두 노트북은 `HUSKY_SERIAL_NUMBER`와 `LITE_SERIAL_NUMBER`를 각각 `cw.scope(sn=...)`에 전달하며, Lite는 프로그래밍·통신·클럭 공급을, Husky는 수동 관측(SCA) 또는 수동 관측·전압 글리치(FA)를 담당한다. 필요한 헬퍼는 각 노트북 안에 있어 별도 공용 헬퍼 노트북을 실행하지 않는다.

`4. FPGA CW310`의 두 노트북(`1.0.CW310_AES_main.ipynb`, `2.0.CW310_WideReg_main.ipynb`)도 자기완결적이다. 각각 `CW1200_SERIAL_NUMBER`를 `cw.scope(sn=…)`에, `CW310_SERIAL_NUMBER`를 `cw.target(scope, cw.targets.CW310, bsfile=…, defines_files=[…], force=True, sn=…)`에 넘겨 지정 장비만 연다. USB에 Husky·Lite가 함께 꽂혀 있으므로 시리얼 없는 `cw.scope()`는 "Multiple ChipWhisperers connected"로 실패한다. `defines_files`는 꼭 넘겨야 한다. chipwhisperer 6.0.0의 기본 경로(`…/firmware/fpgas/aes/hdl/cw305_aes_defines.v`)가 설치본에 없기 때문이다. `force=True`가 없으면 이미 프로그래밍된 FPGA를 다시 쓰지 않는다.

비트스트림은 컨테이너가 아니라 호스트에서 `4. FPGA CW310/fpga/build.sh aes|wide`로 만든다. Vivado 2018.2는 호스트 `/opt/Xilinx`에만 있다. 산출물 `fpga/build/<design>/cw310_top.bit`(15.9 MB)은 git에 포함한다. 실습자는 Vivado 없이 노트북만 실행하기 때문이다. 노트북은 Xilinx `.bit` 헤더(설계명·부품 `7k410tfbg676`·빌드 날짜/시각)를 읽어 부품을 확인한 뒤 프로그래밍한다. 레지스터 맵의 단일 정의는 `fpga/common/cw310_defines.v`이고 Vivado(`include`)와 노트북(`defines_files`)이 같은 파일을 읽는다. `CW310.registers == 12`이므로 define 수를 바꾸면 경고가 난다. HDL은 NewAE cw310-bergen-board의 AES 예제를 정리한 로컬 전용 사본(git 제외)으로, XADC·ILA IP를 빼고 `O_clksettings` 포트를 연결해 `REG_CLKSETTINGS`가 동작하게 했다. 이유는 로컬 `fpga/aes/cw310_top.v` 머리 주석에 있다.

CW310에서 주의할 점은 다섯 가지다.

1. `REG_CRYPT_GO`는 쓰기 자체가 start 펄스이고 읽기는 busy다. `target.go()`(쓰기 1회)만 쓰고 `go_reg()`(1 쓰고 0 쓰기, 곧 2회 실행)는 쓰지 않는다. `is_done()`은 CW310에서 항상 True라 노트북이 busy를 직접 폴링한다.
2. `print(target)`은 이 설계에 없는 XADC 레지스터를 읽어 쓰레기 값을 찍으므로 쓰지 않는다.
3. 레지스터 바이트 0이 벡터 최하위 바이트라 `loadEncryptionKey/loadInput/readOutput`이 `[::-1]`을 쓴다.
4. 클럭 순서는 ‘CDCE906 PLL 출력(`PLL_OUT_FPGA`) → `REG_CLKSETTINGS=0x09`(PLL1 선택 + HS1 출력) → CW1200 `freq_ctr`로 HS1 확인 → `adc_src='extclk_x4'` → `adc_locked`’이다. 이 보드는 실측상 PLL 출력 2가 `PLL_CLK1`이며 노트북이 주파수 카운터로 매번 확정한다. HS1에 클럭이 없으면 DCM이 lock되지 않는다. Husky의 `clkgen_src/adc_mul`은 CW1200(Pro)에서 무효다.
5. 전원은 CW310의 USB-C 전원 포트에 PD 공급기(15 V/20 V, 1 A 이상)가 있어야 한다. 일반 5 V USB 전원이면 K410T가 설정 완료 직후 브라운아웃되어 DONE·INIT_B가 떨어지고 레지스터가 0xFF/플로팅으로 읽힌다(2026-10-06 실장비에서 관측; STUSB4500 RDO=0, CC=기본 전류).

128바이트 레지스터 쓰기는 32바이트 청크로 나눠 `_naeusb.cmdWriteMem`으로 보낸다. 48바이트 이상은 벌크 엔드포인트로 가는데 CW310 펌웨어 1.5.0이 벌크 쓰기를 레지스터에 반영하지 않기 때문이다. 실측으로 48·64·128 B 쓰기는 0으로 읽혔고, 47 B까지는 정상이었으며, 벌크 읽기는 정상이었다. 노트북은 모든 쓰기를 다시 읽어 검증한다. 이득은 35 dB를 쓴다. 25 dB는 봉우리가 0.1 미만이고 45 dB는 AES 포화 위험이 있다.

두 노트북의 Dataset은 1강과 같은 Schema 1.0을 쓴다. 1.1은 power 채널에 `bandwidth_hz`를 요구하는데 CW1200 아날로그 대역폭의 실측값도 명목값도 없어 추정값으로 채우지 않는다.

### 커스텀 SimpleSerial 2.1 프로토콜

`simpleserial_main/simpleserial-base.c`의 펌웨어는 기본 `'k'`/`'p'` SimpleSerial 명령을 쓰지 않는다. 아래 3개 명령을 등록하며, 노트북도 정확히 이 프로토콜로 통신한다.

| cmd | scmd | 의미 |
|-----|------|------|
| `0x81` | `'k'` / `'p'` / `'l'` | 키 / 평문 / 출력 길이 쓰기. 타겟이 저장한 값을 그대로 에코 |
| `0x82` | `'c'` | `trigger_high()`와 `trigger_low()` 사이에서 연산 수행(기본 `MY_OTP`), 응답 페이로드는 `0x82` |
| `0x83` | `'r'` | 결과 `global_len` 바이트 회수 |

C 펌웨어의 `MAX_DATA_LEN = 245`는 SimpleSerial 핸들러와 전역 버퍼의 수용 한도다.
튜토리얼 노트북은 같은 이름을 현재 전송할 payload 길이로 사용하며, 통신 점검에서는 245,
Dataset 수집에서는 16처럼 셀마다 다시 정한다. 둘은 같은 정의가 아니다. 노트북 값은 C의
수용 한도를 넘으면 안 되고, `0x81 'l'`로 보낸 1바이트 값이 실제 `global_len`이 된다.
같은 식별자가 두 뜻을 갖는 구조는 코드 리팩터링 전까지 유지되는 제약이므로, 새 설명에서
두 값을 하나의 공유 상수처럼 서술하지 않는다.

## Trace(트레이스) 저장

모든 Trace Dataset(데이터셋)은 저장소 루트의 `SCHEMA.md`를 따른다. 용어는
`GLOSSARY.md`가 기준이다. 기준 문서의 정의문은 영문을 유지하고, 파생 문서·주석·설명은 한국인
연구자를 독자로 삼아 한글 위주로 쓴다. 코드 식별자와 두문자어는 영문 원형을 유지한다.

구조의 기본은 HDF5 파일 하나가 Dataset 한 벌(Target 1개 × Channel 1개)이라는 것이다.
측정 조건은 루트 HDF5 attrs에, Record(레코드)별 Attributes(어트리뷰트)는
`/<subset>/` 아래의 HDF5 dataset(배열)에 둔다. 필수·선택 필드와 현재 판번호는
`SCHEMA.md`에서만 정의한다.

주의할 점은 두 가지다. OPTIMIST의 Attributes(`trace` 등)는 HDF5에서 배열로, OPTIMIST의 Metadata는 HDF5 attrs로 저장되어 이름이 엇갈린다(`GLOSSARY.md` §6). 그리고 모르는 메타데이터는 추정치로 채우지 않는다. 비워 두고 검증기가 "부분 준수"로 보고하게 둔다(`SCHEMA.md` §5.3).

준수 여부는 `workspace/lib/sca_schema.py`의 `validate_dataset(path=…)`로 검사한다. 실물 전력과 에뮬레이션이 같은 검증기를 통과해야 "준수"의 뜻이 하나로 유지되므로 저장소 공용 트리에 있다. `[extra] SCALib/scalib_common.py`는 이 함수를 같은 이름으로 다시 제공하므로 그 프로젝트 노트북 12개는 종전대로 `validate_dataset(target=…)`을 쓴다. 공용 트리로 옮기면서 노트북을 한 줄도 고치지 않기 위한 방법이다.

검증기는 파일에 적힌 판번호의 규칙을 적용한다. 나중 규칙으로 기존 Dataset을 소급
판정하지 말고, 수집 코드는 실제로 기록하는 필드에 맞는 판번호를 써야 한다.

## 저장소 공용 트리: `workspace/lib/`·`workspace/iut/`

한 서브프로젝트 안에만 두면 두 번째 소비자가 생기는 순간 사본이 생기는 것들을 올려 둔 곳이다(AGENTS.md 1-2).

| 위치 | 내용 | 쓰는 곳 |
|---|---|---|
| `workspace/lib/sca_schema.py` | 스키마 상수·검증기·경로 기반 로더 | 서로 다른 관측 경로 전부 |
| `workspace/lib/aes_ref.py` | `SBOX`·`HW`·`sbox_out`·`aes_ecb_encrypt`·`intermediates()` | 수집 코드의 골든 검증, 분석의 민감값 라벨 |
| `workspace/lib/elfParser.py` | `ElfParser`. ELF 심볼·섹션·메모리 배치 조회 | `[extra] Physical-AI-SCA`의 에뮬레이션 수집 코드 |
| `workspace/iut/{tiny-AES-c,masked-aes-c}/` | IUT(테스트 대상 구현) 암호 라이브러리 | PRE-SCA 타겟, SCALib 펌웨어 2종, 에뮬레이션 실행 프로그램 2종 |

암호 라이브러리를 공용 트리에 둔 이유는 다음과 같다. 실물 펌웨어와 에뮬레이션 실행 프로그램이 같은 `aes.c`를 같은 플래그(`-Os`)로 컴파일해야 "에뮬에서 찾은 결함이 실측 타겟에도 있다"고 말할 근거가 생긴다. 최적화 수준이 전이 누설을 만들기도 하고 없애기도 하므로, 플래그가 다르면 다른 구현을 분석하는 것과 같다. 경로를 옮기면 makefile 2개·수집 노트북 2개·SCALib README·`workspace/iut/README.md`를 함께 고치고 `clean` 재빌드한다. 빌드 산출물에 소스 경로가 문자열로 박히기 때문이다.

`intermediates()`가 공용인 이유도 같다. 에뮬과 실측이 서로 다른 값을 같은 이름으로 부르면 비교가 표시 없이 무너진다.

시각화는 matplotlib이 아니라 `output_notebook()`을 쓰는 Bokeh다. 트레이스 파일은 용량이 크므로 요청받지 않는 한 커밋에 넣지 않는다.

`[extra] SCALib/traces/`의 생성 HDF5 파일은 Git에서 제외되므로 clone에는 들어오지 않으며,
로컬 존재 여부는 작업 환경마다 다르다. 발견한 파일의 준수 여부는 컨테이너 안에서 공용
검증기로 직접 확인한다. 튜토리얼의 `workspace/traces/20260825_220525_SCA_DB.h5`는
Schema 1.0 검증을 통과하지만, 뒤 판에서 추가된 시험 요건 Metadata는 요구하지 않는 파일이다.

## `[extra]` 프로젝트: 각자가 자기 규칙을 갖는다

`[extra]` 접두사가 붙은 디렉터리는 공식 튜토리얼 경로와 무관한 연구·부속 프로젝트다. 각각 독립적으로 작성되어 있으므로 손대기 전에 그 프로젝트의 README를 먼저 읽고, 경로는 그 프로젝트 루트 기준 상대경로로 유지한다. 여러 프로젝트가 호스트 절대경로를 명시적으로 금지한다.

### `[extra] PRE-SCA/`

ARM 펌웨어(tiny-AES)를 Unicorn/Capstone으로 에뮬레이션하는 pre-silicon SCA/FI 실험이다. 하드웨어가 필요 없다(`[extra] Physical-AI-SCA`의 에뮬 경로도 그렇다). 전부 `PRE-SCA.ipynb` 한 파일에 들어 있으며, ELF 파싱·디스어셈블·트레이스 로깅·오류주입 시나리오·결정성 검증까지 셀 순서대로 이어진다. 분석 대상 ELF는 `source/tiny-aes`이다. `source/target-firmware/target_main.c`가 에뮬레이터 I/O 래퍼와 `main`만 정의하고, 같은 폴더의 `Makefile`이 공용 기준 소스 `workspace/iut/tiny-AES-c`를 직접 컴파일해 ELF를 만든다. 실행 산출물은 `nb_output/`에 쌓이며 Git에서 제외한다. 초기 스크립트판 `[naive] PRE-SCA/`는 노트북이 같은 내용을 전부 담게 되어 2026-08-19에 삭제했다. 공개 메서드·상수·산출물을 대조해 확인했고, 노트북이 만드는 디스어셈블은 스크립트판의 회귀 기준선과 바이트 단위로 같았다. 그때 유일한 외부 소비자였던 `elfParser.py`만 `workspace/lib/`로 옮겼다. `[extra] Physical-AI-SCA`의 `collectors/emulation.py`가 이것을 import한다.

### `[extra] SCALib/`

SCALib 0.6.4의 기능을 기능 하나당 노트북 하나로 보이되, Normal AES(`tiny-AES-c`) ∥ Masked AES(`masked-aes-c`) 이중 타겟을 단계마다 나란히 비교하는 예제 모음이다(SNR·Quantizer·Ttest·MTtest·CPA·LDA·MultiLDA·RLDA·SASCA·KeyRank). 하드웨어가 필요한 노트북은 `0.0.Dataset_Collect_tiny-AES-c.ipynb`와 `0.1.Dataset_Collect_masked-aes-c.ipynb` 둘이고, CW308+STM32F3에서 수집한 전력 Trace를 `traces/scalib_dataset_{tiny-AES-c,masked-aes-c}.h5`에 만든다. 분석 노트북 10개는 그 파일을 읽지만 GB 단위 생성물이라 Git에서 제외한다. 로컬 파일의 존재·준수 여부는 실제 경로와 검증기 결과로 확인한다. Trace 길이는 수집 시 `scope.adc.trig_count`에서 정하며 AES 연산 전체(키 스케줄+10라운드)를 담도록 설계되어 있다.

암호 라이브러리는 이 서브프로젝트 밖의 `workspace/iut/{tiny-AES-c,masked-aes-c}/`에 있다. 펌웨어 makefile이 `../../iut/<lib>/aes.c`를 직접 컴파일한다. 실물 전력과 에뮬레이션이 같은 소스를 봐야 결과를 나란히 놓을 수 있어서 저장소 공용 트리로 올렸다. 출처와 패치 내역은 `workspace/iut/README.md`에 있다.

경로·타겟 레지스트리·AES 상수·데이터셋 로더는 `scalib_common.py`(`TARGETS`, `load_group(target=…)`, `group_len`) 한 곳에만, 수집 공용 로직은 `dataset_collect_lib.py` 한 곳에만 있다. 분석 로직은 노트북이 직접 보여 준다. 교육 목적이라 공용 모듈로 빼지 않는다.

수집 중 캡처는 `Bench.capture()`(`dataset_collect_lib.py`)를 사용한다. 구현된 복구 순서는 ‘단순 재시도 3회 → 재연결 2회 → Husky 펌웨어 재기록 1회’이며, 재연결 뒤 측정 설정과 마스크 시드를 다시 적용한다. 펌웨어 재기록은 장치 상태를 덮어쓰는 부작용이 있으므로 `capture()`의 앞 단계가 모두 실패했을 때만 실행한다. 과거 Masked 수집의 저장된 노트북 출력에는 `reflash`, `reconnect`, `reconnect`가 기록되어 있지만, 현재 HDF5 파일이 없으므로 새 수집에서는 복구 이력과 설정 복원을 다시 확인해야 한다.

이 서브프로젝트 고유의 규칙은 세 가지다.

1. 관점을 분리한다. Masked h5에는 연구용 마스크 `mask (n,10)`이 들어 있다. 공격자 관점 셀은 `mask`를 참조하지 않는다. 쓰는 절은 "연구자"로 제목을 분리한다.
2. 비교는 암호화 구간에서만 한다. `masked-aes-c`는 `CipherMasked`만 보호하고 `KeyExpansion`은 벤더 원본 비마스킹인데, 펌웨어가 키 스케줄을 트리거 안에서 돌린다. 전 구간 비교는 이 공통 누설에 지배된다. 저장된 `2.0.Ttest.ipynb` 출력은 전 구간 최대 `|t|`가 Normal 114.31 / Masked 113.81임을 보여 준다. `1.0`은 Dataset에서 평문 의존 누설 시작점 `enc_start`를 산출해 `nb_output/poi_*.npz`에 저장하고 `2.0`–`6.0`은 그 이후만 보도록 작성되어 있다.
3. 트레이스 수는 목표치가 아니라 실제 보유량이다. `N_PROFILING` 같은 상수는 수집 목표다. 분석은 `group_len()`으로 실제 트레이스 수를 읽고, 타겟 간 비교는 양쪽을 같은 예산으로 맞춘다.

저장된 수집 노트북 출력은 두 과거 실행이 profiling 목표 100,000 Record를 채웠고 검증기에서 위반을 보고하지 않았다고 기록한다. Masked 출력에는 `reflash`·`reconnect`·`reconnect` 복구 이력도 있다. 이는 현재 파일의 준수 증거가 아니므로 HDF5를 다시 만들면 검증기를 재실행한다. 마스크 RNG 패치는 벤더 원본 `rand() % 0xFF`가 제외하던 `0xFF`를 `rand() & 0xFF`로 포함하지만, `rand()`를 암호학적으로 안전한 RNG로 만들지는 않는다(`workspace/iut/masked-aes-c/aes.c`). 커스텀 프로토콜은 공통 `0x81 k/p/l`·`0x82 c`·`0x83 r`에 더해 Masked 전용 `0x81 's'`(마스크 시드)·`0x83 'm'`(마스크 회수)이 있다.

### `[extra] Physical-AI-SCA/`

AI가 실험 설계·수집·분석·보고를 나누어 수행하는 사전 진단 환경이다. 한 암호 구현을 에뮬레이션과 실물 전력으로 관측해 하나의 스키마·하나의 판정 규칙 위에 놓는다. Git에는 문서와 데모 출력만 추적하며, 생성되는 `runs/`·`traces/`는 제외한다. 로컬 번들은 `verify`를 통과해야만 현재 증거로 쓸 수 있다. `cw_power.py`의 현재 동작 근거는 통합 데모 006·007의 Dataset과 manifest다.

ISO/IEC 17825:2024를 준용하되 적합성 평가가 아니라 사전 진단(pre-assessment)이다. §1 Scope가 이 표준을 ISO/IEC 19790 적합성 판정용으로 정하고 24759와 함께 암호모듈의 정의된 경계에서 쓰도록 하는데, 여기 IUT는 모듈이 아니라 라이브러리이고 벤더와 시험자가 동일하며 승인 기관이 없다. 그래서 spec의 `scope.not_claimed`는 비울 수 없는 필수 필드다. 무엇을 주장하지 않는지 적지 않으면 나머지가 전부 주장으로 읽힌다.

CLI는 `collect` → `analyze` → `report` → `verify`이고 전부 `python3 -m physai.<이름>`이다. 수치·판정·해시·요건 대조표는 전부 도구가 결정적으로 만든다. LLM(`llm.py`, OpenAI 호환 함수 하나)은 보고서 서술 초안에만 관여하며, 환경변수가 없으면 서술 칸이 빈 채로 나머지가 다 채워진 문서가 나온다. 에이전트 루프·툴콜 파싱은 만들지 않는다. 이 도구를 호출하는 쪽의 실행 환경이 할 일이다.

필수 시험은 TA·SPA·DPA 셋 모두다(§7.3.2 `shall [07.03]`·§8.1 `shall [08.01]`). 순서는 TA→SPA→DPA이지만 앞이 fail이어도 뒤를 계속 수행한다. 순서는 should이고 전부 평가는 shall이기 때문이다. TA는 캐시 유무와 무관하게 수행한다. §8.2의 캐시 면제는 Reference [50] 프레임워크에만 걸리며, Annex A 전체에서 `shall collect`는 A.2.4 타이밍 하나뿐이다. 고차 제외는 DPA에만 해당하고 TA의 2차(분산) 검정은 의무다. CPA는 판정이 아니라 처리 흐름을 점검하는 양성 대조다.

누설 벡터는 `[hw_reg | hd_reg | hw_mem | hd_mem]` 연접이며 HD는 같은 저장소의 한 명령어 앞뒤 값끼리만 계산한다. 서로 다른 레지스터 쌍은 물리적 근거가 없고 오탐만 만든다. `sample_map`이 샘플을 명령어 주소로 대응시켜 주므로, 누설이 의심되는 명령어 위치인 결함 후보를 `addr2line`으로 소스 행까지 옮길 수 있다. 에뮬레이션 실행 프로그램을 `-gdwarf-2`로 빌드하는 이유다.

저장된 데모·진행 문서는 과거 실행에서 에뮬 명령어 수가 tiny 6,030 / masked 10,147로 일정했고, 골든 AES가 일치했으며, 비마스킹 대조군의 결함 후보에 `AddRoundKey`와 `SubBytes`가 포함됐다고 기록한다. 이 값과 소스 위치는 로컬 `results.json`·보고서·해시 번들이 함께 존재하고 `verify`를 통과할 때만 현재 증거로 인용한다.

## 실무 메모

- 경로에 공백·한글·`[...]`가 들어 있다. 셸 명령에서는 항상 따옴표로 감싼다.
- 루트의 `gitignore/`는 로컬 전용 보관함이다. 루트 `.gitignore`가 `/gitignore/`로 통째로 제외하므로 그 안의 파일은 git에 전혀 나타나지 않는다. 커밋하면 안 되지만 작업에는 필요한 것을 여기 둔다. 현재는 저작권 보호 문서인 ISO/IEC 17825:2024 원문(`ISO_IEC17825_2024_EN.pdf`)이 있다. 새로 클론한 사람에게는 이 디렉터리가 없으므로, 여기 있는 파일에 의존하는 문서는 로컬 전용임을 밝히고 원본 출처(URL)를 함께 적는다.
- 이 저장소의 1차 소스는 노트북이다. JSON을 직접 고치기보다 노트북으로 편집(NotebookEdit)하고, 한국어 마크다운 셀과 그것이 설명하는 코드 셀을 함께 갱신한다.
- 컨테이너는 root로 동작하며 호스트 파일을 마운트하므로, 컨테이너 안에서 만든 파일은 호스트에서 root 소유가 된다. 이 UID 불일치로 git이 막히지 않도록 Dockerfile이 `git config --global --add safe.directory '*'`를 설정해 둔다.
