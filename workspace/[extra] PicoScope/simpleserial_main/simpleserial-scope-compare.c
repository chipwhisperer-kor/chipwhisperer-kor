/*
 * AES-128 + SHA-256 measurement workload for three simultaneous oscilloscopes.
 *
 * Inputs arrive over SimpleSerial 2.1 outside the trigger window. Command
 * 0x82/'c' emits one HIGH pulse around AES key expansion and encryption, a
 * short LOW marker, and a second HIGH pulse around SHA-256. The two pulses
 * let PicoScope channel B identify both algorithm regions without guessing
 * from the analogue waveform. UART output is sent only after both regions.
 *
 * The command changes the stored key/message/result and the target trigger
 * pin. Invalid subcommands, payload lengths, or missing inputs return a
 * SimpleSerial error and do not start a cryptographic operation.
 */

#include <stdint.h>
#include <string.h>

#include "aes.h"
#include "hal.h"
#include "mbedtls/sha256.h"
#include "simpleserial.h"

#define AES_KEY_BYTES 16U
#define MESSAGE_BYTES 64U
#define AES_RESULT_BYTES 16U
#define SHA_RESULT_BYTES 32U
#define RESULT_BYTES (AES_RESULT_BYTES + SHA_RESULT_BYTES)
#define STAGE_GAP_CYCLES 64U

static uint8_t key[AES_KEY_BYTES];
static uint8_t message[MESSAGE_BYTES];
static uint8_t result[RESULT_BYTES];
static uint8_t key_is_set;
static uint8_t message_is_set;
static uint8_t result_is_ready;

static void stage_gap(void)
{
    uint32_t i;

    /* A fixed low marker separates AES and SHA even at one ADC sample per
     * target clock. It is excluded from both algorithm statistics. */
    for (i = 0; i < STAGE_GAP_CYCLES; ++i) {
        __asm__ volatile("nop");
    }
}

static uint8_t set_input(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t *data)
{
    (void)cmd;

    if (scmd == (uint8_t)'k') {
        if (len != AES_KEY_BYTES) {
            return SS_ERR_LEN;
        }
        memcpy(key, data, AES_KEY_BYTES);
        key_is_set = 1U;
        result_is_ready = 0U;
        simpleserial_put((char)scmd, AES_KEY_BYTES, key);
        return SS_ERR_OK;
    }

    if (scmd == (uint8_t)'m') {
        if (len != MESSAGE_BYTES) {
            return SS_ERR_LEN;
        }
        memcpy(message, data, MESSAGE_BYTES);
        message_is_set = 1U;
        result_is_ready = 0U;
        simpleserial_put((char)scmd, MESSAGE_BYTES, message);
        return SS_ERR_OK;
    }

    return SS_ERR_CMD;
}

static uint8_t run_composite(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t *data)
{
    struct AES_ctx aes_context;
    mbedtls_sha256_context sha_context;
    uint8_t completed = 1U;

    (void)cmd;
    (void)data;

    if (scmd != (uint8_t)'c') {
        return SS_ERR_CMD;
    }
    if (len != 0U) {
        return SS_ERR_LEN;
    }
    if (!key_is_set || !message_is_set) {
        return SS_ERR_CMD;
    }

    memcpy(result, message, AES_RESULT_BYTES);

    trigger_high();
    AES_init_ctx(&aes_context, key);
    AES_ECB_encrypt(&aes_context, result);
    trigger_low();

    stage_gap();

    trigger_high();
    mbedtls_sha256_init(&sha_context);
    mbedtls_sha256_starts(&sha_context, 0);
    mbedtls_sha256_update(&sha_context, message, MESSAGE_BYTES);
    mbedtls_sha256_update(&sha_context, result, AES_RESULT_BYTES);
    mbedtls_sha256_finish(&sha_context, result + AES_RESULT_BYTES);
    mbedtls_sha256_free(&sha_context);
    trigger_low();

    result_is_ready = 1U;
    simpleserial_put((char)scmd, 1U, &completed);
    return SS_ERR_OK;
}

static uint8_t get_result(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t *data)
{
    (void)cmd;
    (void)data;

    if (scmd != (uint8_t)'r') {
        return SS_ERR_CMD;
    }
    if (len != 0U) {
        return SS_ERR_LEN;
    }
    if (!result_is_ready) {
        return SS_ERR_CMD;
    }

    simpleserial_put((char)scmd, RESULT_BYTES, result);
    return SS_ERR_OK;
}

int main(void)
{
    platform_init();
    init_uart();
    trigger_setup();
    trigger_low();

    simpleserial_init();
    simpleserial_addcmd((char)0x81, MESSAGE_BYTES, set_input);
    simpleserial_addcmd((char)0x82, 0U, run_composite);
    simpleserial_addcmd((char)0x83, 0U, get_result);

    while (1) {
        simpleserial_get();
    }
}
