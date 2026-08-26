#include <stdint.h>

#include "aes.h"

enum {
    AES_BLOCK_BYTES = 16,
    VIRTUAL_BUFFER_BLOCKS = 10,
};

/*
 * Unicorn 에뮬레이터와 데이터를 주고받는 고정 심볼이다. vir_IN의 첫 블록은 AES-128
 * 키, 둘째 블록은 평문이며 vir_OUT의 첫 블록에 암호문을 쓴다. 나머지 공간은 PRE-SCA
 * 입력·출력 ABI의 크기를 유지하기 위한 예약 영역이다.
 */
uint8_t vir_IN[AES_BLOCK_BYTES * VIRTUAL_BUFFER_BLOCKS] = {0};
uint8_t vir_OUT[AES_BLOCK_BYTES * VIRTUAL_BUFFER_BLOCKS] = {0};

/*
 * PRE-SCA 입력 형식을 공용 tiny-AES-c API에 연결하는 래퍼 함수다.
 *
 * 입력: 16바이트 AES-128 키와 16바이트 평문.
 * 출력: ciphertext가 가리키는 16바이트를 AES-128 ECB 암호문으로 덮어쓴다.
 * 실패: tiny-AES-c ECB API는 오류 값을 반환하지 않으므로 이 함수도 실패를 보고하지 않는다.
 * 부작용: ciphertext가 가리키는 메모리만 변경한다.
 */
void run_target(const uint8_t key[AES_BLOCK_BYTES],
                const uint8_t plaintext[AES_BLOCK_BYTES],
                uint8_t ciphertext[AES_BLOCK_BYTES])
{
    struct AES_ctx ctx;
    int i;

    for (i = 0; i < AES_BLOCK_BYTES; ++i) {
        ciphertext[i] = plaintext[i];
    }

    AES_init_ctx(&ctx, key);
    AES_ECB_encrypt(&ctx, ciphertext);
}

int main(void)
{
    run_target(vir_IN, vir_IN + AES_BLOCK_BYTES, vir_OUT);
    return 0;
}
