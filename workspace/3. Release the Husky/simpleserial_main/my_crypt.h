#ifndef _MY_CRYPT_H_
#define _MY_CRYPT_H_

#include <stdint.h>

/* 길이 len의 두 입력을 바이트별 XOR해 output에 쓴다.
 * input_k와 input_p는 각각 len바이트 이상, output은 쓰기 가능한 len바이트 이상이어야
 * 한다. 길이·포인터를 검증하지 않으며 반환값 0은 연산 완료를 뜻한다. */
int MY_OTP(uint8_t *output, uint8_t *input_k, uint8_t *input_p, uint8_t len);

#endif
