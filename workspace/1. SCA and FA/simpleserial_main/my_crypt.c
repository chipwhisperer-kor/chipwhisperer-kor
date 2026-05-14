#include "my_crypt.h"


int MY_OTP(uint8_t *output, uint8_t *input_k, uint8_t *input_p, uint8_t len) {

	int i;

	for (i = 0; i < len; i++) output[i] = input_k[i] ^ input_p[i];
	
	return 0;
}