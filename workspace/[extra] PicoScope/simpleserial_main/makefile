# Composite AES-128 + SHA-256 workload for CW308_STM32F3.

TARGET = simpleserial-scope-compare

SRC += simpleserial-scope-compare.c

# Compile the repository's canonical AES implementation instead of carrying a
# second copy in this subproject.
VPATH += ../../iut/tiny-AES-c
SRC += aes.c
EXTRAINCDIRS += ../../iut/tiny-AES-c
CFLAGS += -DCBC=0 -DCTR=0

# Compile only mbedTLS SHA-256 with the local minimal configuration. The
# algorithm source stays canonical under workspace/base/crypto/mbedtls.
VPATH += ../../base/crypto/mbedtls/library
SRC += sha256.c
EXTRAINCDIRS += ../../base/crypto/mbedtls/include
CFLAGS += -DMBEDTLS_CONFIG_FILE='"picoscope_mbedtls_config.h"'

ifeq ($(CRYPTO_OPTIONS),)
CRYPTO_OPTIONS = AES128C
endif

include ../../base/simpleserial/Makefile.simpleserial

FIRMWAREPATH = ../../base/.
include $(FIRMWAREPATH)/Makefile.inc
