#ifndef _MY_CRYPT_H_
#define _MY_CRYPT_H_

#include <stdint.h>

int MY_OTP(uint8_t *output, uint8_t *input_k, uint8_t *input_p, uint8_t len);

#endif
