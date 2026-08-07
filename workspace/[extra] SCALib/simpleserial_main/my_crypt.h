#ifndef _MY_CRYPT_H_
#define _MY_CRYPT_H_

#include <stdint.h>

/**
 * AES-128 ECB 암호화 (tiny-AES-c).
 *
 * output : 암호문 16바이트 (input_p 를 복사한 뒤 in-place 암호화)
 * input_k: 키 16바이트
 * input_p: 평문 16바이트
 * len    : 반드시 16 (AES 블록 크기). 그 외에는 음수 반환.
 *
 * 반환: 0 성공, 음수 실패.
 */
int MY_AES_ECB(uint8_t *output, uint8_t *input_k, uint8_t *input_p, uint8_t len);

#endif
