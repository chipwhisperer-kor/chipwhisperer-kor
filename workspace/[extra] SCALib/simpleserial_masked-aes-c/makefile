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

# masked-aes-c (ECB + boolean masking): 상위 폴더 소스를 직접 컴파일한다.
VPATH += ../masked-aes-c
SRC += aes.c
EXTRAINCDIRS += ../masked-aes-c

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
