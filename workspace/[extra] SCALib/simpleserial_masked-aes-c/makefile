# Hey Emacs, this is a -*- makefile -*-
#----------------------------------------------------------------------------
#
# Makefile for ChipWhisperer SimpleSerial + masked-aes-c (AES-128 ECB, MASKED=1)
#
#----------------------------------------------------------------------------
# On command line:
#
# make all = Make software.
#
# make clean = Clean out built project files.
#
# make PLATFORM=CW308_STM32F3 CRYPTO_TARGET=NONE SS_VER=SS_VER_2_1
#----------------------------------------------------------------------------

# Target file name (without extension).
TARGET = simpleserial-base

# Local firmware sources
SRC += my_crypt.c
SRC += simpleserial-base.c

# masked-aes-c (ECB + boolean masking): 공용 IUT 트리의 소스를 직접 컴파일한다.
# 라이브러리는 workspace/iut/ 에 한 벌만 두고 펌웨어·에뮬 하네스가 함께 참조한다.
# 같은 소스를 컴파일해야 실측 파형과 에뮬레이션 결과를 나란히 비교할 근거가 생긴다.
VPATH += ../../iut/masked-aes-c
SRC += aes.c
EXTRAINCDIRS += ../../iut/masked-aes-c

# CBC/CTR 비활성, 마스킹 경로 활성
CFLAGS += -DCBC=0 -DCTR=0 -DMASKED=1

# -----------------------------------------------------------------------------

ifeq ($(CRYPTO_OPTIONS),)
CRYPTO_OPTIONS = AES128C
endif

#Add simpleserial project to build
include ../../base/simpleserial/Makefile.simpleserial

FIRMWAREPATH = ../../base/.
include $(FIRMWAREPATH)/Makefile.inc
