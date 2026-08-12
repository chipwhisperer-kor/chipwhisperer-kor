"""AES-128 참조 구현 — 저장소 공용.

부채널 분석은 "타겟이 어떤 중간값을 계산했는가"를 호스트에서 다시 계산해 라벨로 삼는다.
그 계산이 프로젝트마다 따로 있으면, 에뮬레이션 결과와 실측 결과가 **서로 다른 값**을
같은 이름으로 부르게 되어 비교가 조용히 무너진다. 그래서 정의는 여기 한 곳에 둔다.

여기 있는 것은 **하드웨어와 무관한 순수 계산**뿐이다. 장비 제어는 각 프로젝트에 있다.

쓰는 곳
    workspace/[extra] SCALib/scalib_common.py        (재노출 → 분석 노트북 12개)
    workspace/[extra] SCALib/dataset_collect_lib.py  (수집 중 골든 검증)
    workspace/[extra] Physical-AI-SCA/physai/        (에뮬 수집·누설 검정)
"""

import numpy as np

# SubBytes 치환표. 표준 AES S-box 이며 이 저장소의 두 IUT 펌웨어가 쓰는 것과 같다.
SBOX = np.array([
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
], dtype=np.uint8)

# 해밍 가중치표. HW[v] = v 의 1비트 개수. 전력 누설 모델의 기본형이다.
HW = np.array([bin(i).count("1") for i in range(256)], dtype=np.uint8)

RCON = np.array([0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
                 0x80, 0x1b, 0x36], dtype=np.uint8)

AES_BLOCK = 16
N_ROUNDS = 10


def sbox_out(plaintext, key):
    """1라운드 SBox 출력 = SBOX[plaintext XOR key].

    입력: 각각 (n, 16) 또는 (16,) uint8 배열. 브로드캐스트된다.
    출력: 입력과 같은 shape 의 uint8 배열.

    부채널 공격이 겨냥하는 가장 흔한 중간값이다. 평문 한 바이트와 키 한 바이트에만
    의존하므로 키를 바이트 단위로 나누어 추측할 수 있다(분할 정복).
    Masked 구현에서도 **공격자 관점** 라벨은 이 값이다(마스크는 모른다).

    입력은 수정하지 않는다. 두 형상이 브로드캐스트될 수 없으면 NumPy ``ValueError``가
    발생하며 값은 uint8로 변환되므로 원래 정수의 상위 비트는 버려진다.
    """
    return SBOX[np.bitwise_xor(np.asarray(plaintext, dtype=np.uint8),
                               np.asarray(key, dtype=np.uint8))]


def aes_ecb_encrypt(key16, plain16):
    """호스트 골든 모델: AES-128 ECB 한 블록.

    타겟이 낸 암호문과 대조해 통신·구현이 정상인지 확인하는 데 쓴다.
    입력을 bytes로 복사하고 16바이트 암호문을 반환하며 외부 상태는 변경하지 않는다.
    PyCryptodome이 없으면 ``ImportError``, 키나 평문 길이가 16이 아니면 하위 API의
    ``ValueError``가 발생한다.
    """
    from Crypto.Cipher import AES          # 분석 전용 환경에는 없을 수 있어 지연 import
    return AES.new(bytes(key16), AES.MODE_ECB).encrypt(bytes(plain16))


def _xtime(a):
    """uint8 값마다 GF(2^8)의 2를 곱한 같은 형상의 배열을 반환한다.

    입력은 NumPy 배열로 복사·변환하며 수정하지 않는다. 정수 범위를 벗어난 값은 uint8
    변환 규칙을 따르고, 배열로 변환할 수 없는 입력은 NumPy 예외를 발생시킨다.
    """
    a = np.asarray(a, dtype=np.uint8)
    return np.where(a & 0x80, ((a.astype(np.uint16) << 1) ^ 0x1B) & 0xFF,
                    (a.astype(np.uint16) << 1) & 0xFF).astype(np.uint8)


def key_schedule(key16):
    """AES-128 라운드 키 11개를 만든다.

    입력: (16,) 또는 (n, 16) uint8
    출력: (11, 16) 또는 (n, 11, 16) uint8

    KeyExpansion 은 두 IUT 모두 **비마스킹**이다(masked-aes-c 도 키 스케줄은 벤더 원본).
    그래서 이 값은 마스킹 여부와 무관하게 SPA 시험(ISO/IEC 17825 §8.3.1 이 지목하는
    key derivation)의 라벨로 쓸 수 있다.

    입력은 수정하지 않는다. 마지막 축이 16이 아니면 배열 대입 과정에서 NumPy 형상 오류가
    발생한다. 1차원 입력만 ``(11, 16)``으로 축약하고 그 밖에는 배치 축을 유지한다.
    """
    k = np.atleast_2d(np.asarray(key16, dtype=np.uint8))
    n = k.shape[0]
    rk = np.zeros((n, 11, 16), dtype=np.uint8)
    rk[:, 0] = k
    for r in range(1, 11):
        prev = rk[:, r - 1]
        t = prev[:, 12:16].copy()
        t = np.roll(t, -1, axis=1)                 # RotWord
        t = SBOX[t]                                # SubWord
        t[:, 0] ^= RCON[r]
        rk[:, r, 0:4] = prev[:, 0:4] ^ t
        for w in range(1, 4):
            rk[:, r, 4 * w:4 * w + 4] = (rk[:, r, 4 * (w - 1):4 * (w - 1) + 4]
                                         ^ prev[:, 4 * w:4 * w + 4])
    return rk[0] if np.ndim(key16) == 1 else rk


def _shift_rows(s):
    """열 우선 ``(n, 16)`` AES state에 ShiftRows를 적용한 새 배열을 반환한다.

    입력을 변경하지 않는다. 두 번째 축이 16보다 짧거나 2차원 인덱싱을 지원하지 않으면
    NumPy 인덱싱 예외가 발생한다.
    """
    idx = np.array([0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11])
    return s[:, idx]


def _mix_columns(s):
    """열 우선 AES state 배열에 MixColumns를 적용해 새 배열을 반환한다.

    입력은 `(n, 16)` uint8 배열이어야 한다. 입력을 변경하지 않으며, shape이 맞지 않으면
    NumPy 인덱싱 또는 브로드캐스팅 오류가 호출자에게 그대로 전파된다.
    """
    out = np.empty_like(s)
    for c in range(4):
        a = s[:, 4 * c:4 * c + 4]
        t = a[:, 0] ^ a[:, 1] ^ a[:, 2] ^ a[:, 3]
        out[:, 4 * c + 0] = a[:, 0] ^ t ^ _xtime(a[:, 0] ^ a[:, 1])
        out[:, 4 * c + 1] = a[:, 1] ^ t ^ _xtime(a[:, 1] ^ a[:, 2])
        out[:, 4 * c + 2] = a[:, 2] ^ t ^ _xtime(a[:, 2] ^ a[:, 3])
        out[:, 4 * c + 3] = a[:, 3] ^ t ^ _xtime(a[:, 3] ^ a[:, 0])
    return out


def intermediates(key16, plain16):
    """민감값(sensitive value) 라벨 묶음을 만든다.

    입력
        key16, plain16 : (16,) 또는 (n, 16) uint8

    출력 (dict, 값은 모두 (n, 16) uint8)
        add_rk0    : p ^ k              1라운드 AddRoundKey 출력
        sbox_out   : SBOX[p ^ k]        1라운드 SubBytes 출력  ← 가장 흔한 공격 표적
        round<r>   : r 라운드 종료 시 state (r = 1..10)
        roundkey<r>: r 라운드 키 (r = 0..10)

    **이 값들은 이 저장소의 soundness 검정이 쓰는 비마스킹 민감값 라벨이다.** 검정은
    관측한 HW·HD와 이 라벨의 통계적 종속성을 마스킹 구현 결함 후보로 보고한다. 종속성은
    후보를 좁히는 관측 결과이며, 그 자체만으로 물리 누설이나 공격 가능성을 확정하지 않는다.

    부작용 없음. 실패 조건: shape 이 (…,16) 이 아니면 ValueError.
    """
    k = np.atleast_2d(np.asarray(key16, dtype=np.uint8))
    p = np.atleast_2d(np.asarray(plain16, dtype=np.uint8))
    if k.shape[-1] != AES_BLOCK or p.shape[-1] != AES_BLOCK:
        raise ValueError("key/plaintext 의 마지막 축은 16이어야 한다: %s %s"
                         % (k.shape, p.shape))
    if k.shape[0] == 1 and p.shape[0] > 1:
        k = np.repeat(k, p.shape[0], axis=0)
    if p.shape[0] == 1 and k.shape[0] > 1:
        p = np.repeat(p, k.shape[0], axis=0)

    rk = key_schedule(k)
    if rk.ndim == 2:
        rk = rk[None, :, :]

    out = {}
    for r in range(11):
        out["roundkey%d" % r] = rk[:, r]

    state = p ^ rk[:, 0]
    out["add_rk0"] = state.copy()
    out["sbox_out"] = SBOX[state]

    for r in range(1, N_ROUNDS + 1):
        state = SBOX[state]
        state = _shift_rows(state)
        if r != N_ROUNDS:                    # 마지막 라운드에는 MixColumns 가 없다
            state = _mix_columns(state)
        state = state ^ rk[:, r]
        out["round%d" % r] = state.copy()
    return out
