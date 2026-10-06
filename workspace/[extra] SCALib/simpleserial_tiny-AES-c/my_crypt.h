#ifndef _MY_CRYPT_H_
#define _MY_CRYPT_H_

#include <stdint.h>

/**
 * AES-128 ECB 암호화 (tiny-AES-c, Normal / 비마스킹).
 *
 * output : 암호문 16바이트를 쓴다 (input_p를 복사한 뒤 in-place로 암호화한다).
 * input_k: 키 16바이트다.
 * input_p: 평문 16바이트다.
 * len    : 16이어야 한다 (AES 블록 크기). 그 외에는 음수를 반환한다.
 *
 * 반환: 성공이면 0, 실패면 음수다.
 * 짝이 되는 타겟은 simpleserial_masked-aes-c다 (같은 시그니처에 마스크 export가 더해진다).
 */
int MY_AES_ECB(uint8_t *output, uint8_t *input_k, uint8_t *input_p, uint8_t len);

#endif
