"""AES-128-ECB 알고리즘 계약과 사전 지정된 1차 DPA 분할."""

import numpy as np

from .. import paths  # noqa: F401 - workspace/lib를 import 경로에 둔다.
from aes_ref import HW, aes_ecb_encrypt, sbox_out  # noqa: E402

ID = "aes-128-ecb"
KEY_BYTES = 16
INPUT_BYTES = 16
OUTPUT_BYTES = 16
DPA_TARGETS = ("round1-sbox-byte0-bit0",)
CPA_SUPPORTED = True
SOUNDNESS_SUPPORTED = True


def golden(key, plaintext):
    """16바이트 키와 평문을 받아 16바이트 AES-128-ECB 골든 암호문을 반환한다."""
    return aes_ecb_encrypt(key, plaintext)


def dpa_partition(plaintext, key, target="round1-sbox-byte0-bit0"):
    """첫 라운드 S-box 출력 byte 0의 bit 0으로 0/1 집단 라벨을 만든다.

    ``plaintext``와 ``key``는 같은 행 수의 ``(n,16)`` 배열이어야 한다. 결과는 uint16
    ``(n,)``이며 입력을 변경하지 않는다. target은 수집 전에 명세에 고정된 값만 받는다.
    """
    if target not in DPA_TARGETS:
        raise ValueError("AES DPA target 미지원: %s" % target)
    p = np.asarray(plaintext, dtype=np.uint8)
    k = np.asarray(key, dtype=np.uint8)
    if p.ndim != 2 or k.shape != p.shape or p.shape[1] != INPUT_BYTES:
        raise ValueError("AES DPA 입력 shape은 같은 (n,16)이어야 한다: %s %s"
                         % (p.shape, k.shape))
    return (sbox_out(p[:, 0], k[:, 0]) & 1).astype(np.uint16)


def cpa_predictions(plaintext_byte, guesses):
    """평문 한 바이트와 0..255 키 추측으로 HW(SBOX[p xor g]) 예측 행렬을 만든다."""
    p = np.asarray(plaintext_byte, dtype=np.uint8)
    g = np.asarray(guesses, dtype=np.uint8)
    return HW[sbox_out(p[None, :], g[:, None])]
