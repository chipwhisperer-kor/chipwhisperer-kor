CC := arm-none-eabi-gcc

# AES 구현은 저장소 공용 IUT가 정본이다. 이 디렉터리에 사본을 두지 않고 정본을 직접
# 컴파일해야 PRE-SCA가 다른 실험과 같은 구현을 분석한다.
IUT_DIR := ../../../iut/tiny-AES-c
TARGET := ../tiny-aes
OBJECTS := aes.o target_main.o

CPPFLAGS := -I$(IUT_DIR)
CFLAGS := -O2 -mcpu=cortex-m4
# PRE-SCA의 ELF 로더는 Flash의 가상주소와 파일 오프셋이 같은 레이아웃을 사용한다.
# 64 KiB 최대 페이지를 명시하면 GNU ld 버전이 달라도 그 레이아웃과 RAM 분리가 유지된다.
LDFLAGS := --specs=nosys.specs -mcpu=cortex-m4 -Wl,-z,max-page-size=0x10000

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(LDFLAGS) -o $@ $(OBJECTS)

aes.o: $(IUT_DIR)/aes.c $(IUT_DIR)/aes.h
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o $@ $(IUT_DIR)/aes.c

target_main.o: target_main.c $(IUT_DIR)/aes.h
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o $@ target_main.c

clean:
	rm -f $(OBJECTS) $(TARGET)
