#include "my_crypt.h"

#include <string.h>

#include "aes.h"

int MY_AES_ECB(uint8_t *output, uint8_t *input_k, uint8_t *input_p, uint8_t len)
{
	struct AES_ctx ctx;

	/* AES-128 ECB: 한 블록(16바이트)만 지원한다. MASKED=1 이면 CipherMasked. */
	if (len != AES_BLOCKLEN) {
		return -1;
	}
	if (output == 0 || input_k == 0 || input_p == 0) {
		return -1;
	}

	AES_init_ctx(&ctx, input_k);
	memcpy(output, input_p, AES_BLOCKLEN);
	AES_ECB_encrypt(&ctx, output);

	return 0;
}

void MY_AES_get_last_masks(uint8_t out[10])
{
	AES_get_last_masks(out);
}
