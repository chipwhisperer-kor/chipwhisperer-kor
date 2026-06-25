CC=arm-none-eabi-gcc
CFLAGS=-O2
CFLAGS+=--specs=nosys.specs
CFLAGS+=-mcpu=cortex-m4
TARGET=tiny-aes

$(TARGET): aes.o aes_main.o
	$(CC) $(CFLAGS) -o tiny-aes aes.o aes_main.o

aes_main.o: aes.h aes_main.c
	$(CC) $(CFLAGS) -c -o aes_main.o aes_main.c

aes.o: aes.h aes.c
	$(CC) $(CFLAGS) -c -o aes.o aes.c
 

clean:
	rm -f *.o
	rm -f $(TARGET)
