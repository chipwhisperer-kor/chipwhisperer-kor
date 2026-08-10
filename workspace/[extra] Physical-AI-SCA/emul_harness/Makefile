# 에뮬레이션용 베어메탈 ELF 빌드
#
#   make IUT=tiny-AES-c        →  build/tiny-AES-c.elf
#   make IUT=masked-aes-c      →  build/masked-aes-c.elf   (-DMASKED=1)
#   make clean
#
# 소스는 복사하지 않는다. 저장소 공용 트리 workspace/iut/<IUT>/aes.c 를 직접 컴파일한다.
# 실물 펌웨어(`[extra] SCALib/simpleserial_<IUT>/`)가 같은 파일을 컴파일하므로,
# 에뮬레이션에서 찾은 결함이 실측 타겟에도 있다고 말할 근거가 생긴다.

IUT ?= tiny-AES-c

IUT_DIR   := ../../iut/$(IUT)
BUILD_DIR := build
TARGET    := $(BUILD_DIR)/$(IUT).elf

CC := arm-none-eabi-gcc

# ── 컴파일 플래그 — 실물 펌웨어와 같아야 한다 ──────────────────────────────
#
# 최적화 수준과 ABI 가 다르면 컴파일러가 다른 기계어를 낸다. 전이 누설은 레지스터
# 할당·명령어 선택에서 생기므로, 플래그가 다르면 **다른 구현을 분석하는 셈**이 된다.
# 아래 값은 `[extra] SCALib/simpleserial_<IUT>/makefile` 이 상속하는
# `workspace/base/Makefile.inc` 의 실제 빌드 명령에서 그대로 옮겼다:
#
#   -mcpu=cortex-m4 -mthumb -mfloat-abi=soft -Os -funsigned-char
#   -funsigned-bitfields -fshort-enums -std=gnu99 -ffunction-sections -gdwarf-2
#
# 특히 **-Os** 다. `[extra] PRE-SCA` 의 기존 하네스는 -O2 를 쓰는데, 그 빌드는
# 실측 펌웨어와 기계어가 다르므로 여기서는 따르지 않는다.
CFLAGS := -mcpu=cortex-m4 -mthumb -mfloat-abi=soft
CFLAGS += -Os
CFLAGS += -funsigned-char -funsigned-bitfields -fshort-enums
CFLAGS += -std=gnu99 -ffunction-sections -fmessage-length=0
CFLAGS += -gdwarf-2                    # 누설 지점을 소스 행으로 되짚기 위해 필요
CFLAGS += -I$(IUT_DIR) -I.
CFLAGS += -DCBC=0 -DCTR=0              # 펌웨어와 동일 — ECB 경로만 컴파일

ifeq ($(IUT),masked-aes-c)
CFLAGS += -DMASKED=1
endif

# --specs=nosys.specs : 베어메탈 링크. rand/srand/memcpy 를 newlib 에서 가져오고
# 시스템 콜은 스텁으로 채운다. 링커 스크립트를 따로 주지 않으므로 기본 스크립트가
# .text 를 0x8000 에, _stack 을 0x80000 에 놓는다 — ElfParser 가 그 심볼들을 읽는다.
LDFLAGS := $(CFLAGS) --specs=nosys.specs

OBJS := $(BUILD_DIR)/$(IUT)/main.o $(BUILD_DIR)/$(IUT)/aes.o

.PHONY: all clean flags
all: $(TARGET)

# 수집기가 `build_flags` 메타데이터를 채울 때 이 타깃에게 묻는다.
# Makefile 을 텍스트로 파싱하면 조건부 블록(ifeq)까지 긁어 **없는 플래그를 있다고
# 기록하게 된다** — 실제로 그런 버그가 있었다. 정본은 make 자신이므로 make 에게 묻는다.
flags:
	@echo '$(CFLAGS)'

$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $(OBJS)
	@echo "=== $(IUT) ==="
	@arm-none-eabi-size $@
	@arm-none-eabi-nm -n $@ | grep -E " (_init|main|AES_init_ctx|AES_ECB_encrypt|exit|_exit|vir_IN|vir_OUT|_stack)$$"

$(BUILD_DIR)/$(IUT)/main.o: main.c $(IUT_DIR)/aes.h | $(BUILD_DIR)/$(IUT)
	$(CC) $(CFLAGS) -c -o $@ main.c

$(BUILD_DIR)/$(IUT)/aes.o: $(IUT_DIR)/aes.c $(IUT_DIR)/aes.h | $(BUILD_DIR)/$(IUT)
	$(CC) $(CFLAGS) -c -o $@ $(IUT_DIR)/aes.c

$(BUILD_DIR)/$(IUT):
	mkdir -p $@

clean:
	rm -rf $(BUILD_DIR)
