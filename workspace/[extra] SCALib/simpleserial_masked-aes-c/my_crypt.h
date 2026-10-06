#ifndef _MY_CRYPT_H_
#define _MY_CRYPT_H_

#include <stdint.h>

/**
 * AES-128 ECB 암호화 (masked-aes-c, MASKED=1).
 *
 * output : 암호문 16바이트를 쓴다 (input_p를 복사한 뒤 in-place로 암호화한다).
 * input_k: 키 16바이트다.
 * input_p: 평문 16바이트다.
 * len    : 16이어야 한다 (AES 블록 크기). 그 외에는 음수를 반환한다.
 *
 * 반환: 성공이면 0, 실패면 음수다.
 *
 * 부작용: 성공 시 이 연산에 쓰인 mask[10] 이 모듈 내부에 보관된다.
 *         MY_AES_get_last_masks()로 읽는다 (연구 수집용이다).
 */
int MY_AES_ECB(uint8_t *output, uint8_t *input_k, uint8_t *input_p, uint8_t len);

/** 마지막 MY_AES_ECB 에 쓰인 마스크 10바이트를 out 에 복사한다. */
void MY_AES_get_last_masks(uint8_t out[10]);

#endif
