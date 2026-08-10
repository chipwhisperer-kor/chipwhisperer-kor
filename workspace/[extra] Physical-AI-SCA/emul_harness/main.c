/* 에뮬레이션 하네스 — Unicorn 이 실행할 베어메탈 ELF 의 진입점.
 *
 * 목적
 *   호스트(수집기)가 메모리에 직접 써 넣은 키·평문으로 AES 한 블록을 암호화하고
 *   결과를 다시 메모리에서 읽어 가게 한다. UART 도 SimpleSerial 도 없다 —
 *   에뮬레이터는 메모리를 직접 읽고 쓸 수 있으므로 통신 계층이 필요 없고,
 *   통신 코드가 없어야 트레이스에 암호 연산만 남는다.
 *
 * 입출력 규약 (수집기와 이 파일 양쪽에 있다. 바꾸면 둘 다 바꾼다)
 *   vir_IN [ 0:16] = key
 *   vir_IN [16:32] = plaintext
 *   vir_IN [32:36] = mask 난수 시드 (uint32, little-endian)  ← MASKED 빌드만 사용
 *   vir_OUT[ 0:16] = ciphertext
 *   vir_OUT[16:26] = AES_get_last_masks()  10바이트          ← MASKED 빌드만
 *
 * 이 규약은 `[extra] PRE-SCA` 의 `vir_IN`/`vir_OUT` 관례를 그대로 따른다.
 * 심볼 이름과 크기를 ELF 에서 읽어 주소를 찾으므로 이름을 바꾸면 안 된다.
 *
 * 관측 구간
 *   실측 펌웨어(`simpleserial-base.c` 의 MY_AES_ECB)는 트리거를
 *   AES_init_ctx(KeyExpansion) + AES_ECB_encrypt 전체에 건다.
 *   비교가 성립하려면 에뮬도 같은 구간을 잘라야 하므로, 두 함수를 연속 호출하고
 *   그 사이에 다른 일을 하지 않는다. 구간 경계는 수집기가 심볼 주소로 찾는다.
 *
 * 시드를 왜 호스트가 주는가
 *   masked-aes-c 는 마스크를 rand() 로 만든다. 에뮬레이터에는 엔트로피원이 없어
 *   srand() 를 부르지 않으면 매 실행 같은 마스크가 재생되고, 그러면 마스킹이
 *   없는 것과 같아져 분석이 통째로 무의미해진다. 실물 타겟(STM32F303)도 TRNG 가
 *   없어 같은 이유로 호스트가 0x81 's' 로 시드를 준다 — 규약이 양쪽에서 같다.
 */

#include <stdint.h>
#include <stdlib.h>

#include "aes.h"

/* PRE-SCA 와 같은 크기. 실제로 쓰는 것은 앞 36 / 26 바이트뿐이지만, 크기를 맞춰 두면
 * 기존 도구가 같은 방식으로 덤프할 수 있다. */
#define BUFFER_BLOCK 16
#define BUFFER_NUM   10

unsigned char vir_IN[BUFFER_BLOCK * BUFFER_NUM]  = {0};
unsigned char vir_OUT[BUFFER_BLOCK * BUFFER_NUM] = {0};

int main(void)
{
    uint8_t key[16];
    uint8_t buf[16];
    struct AES_ctx ctx;
    int i;

#if defined(MASKED) && (MASKED == 1)
    uint32_t seed;

    seed = (uint32_t)vir_IN[32]
         | ((uint32_t)vir_IN[33] << 8)
         | ((uint32_t)vir_IN[34] << 16)
         | ((uint32_t)vir_IN[35] << 24);
    /* 관측 구간 밖에서 시드를 심는다. srand() 자체는 암호 연산이 아니므로
     * 트레이스에 섞이면 안 된다. */
    srand(seed);
#endif

    for (i = 0; i < 16; i++) {
        key[i] = vir_IN[i];
        buf[i] = vir_IN[16 + i];
    }

    /* ── 관측 구간 시작 ── */
    AES_init_ctx(&ctx, key);
    AES_ECB_encrypt(&ctx, buf);
    /* ── 관측 구간 끝 ── */

    for (i = 0; i < 16; i++) {
        vir_OUT[i] = buf[i];
    }

#if defined(MASKED) && (MASKED == 1)
    /* 관측 구간 밖에서 회수한다. 실물에서 0x83 'm' 을 trigger_low 이후에 부르는 것과
     * 같은 이유 — 마스크를 꺼내는 동작이 파형에 섞이면 안 된다. */
    AES_get_last_masks(&vir_OUT[16]);
#endif

    return 0;
}
