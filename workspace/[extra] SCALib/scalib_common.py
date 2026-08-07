"""[extra] SCALib 예제 노트북 공용 정의.

10개 노트북이 모두 같은 AES 상수와 같은 데이터셋을 쓴다. 그 정의를 각 노트북에
복사하면 값을 고칠 때 고칠 곳이 10군데가 된다. 그래서 **정의는 여기 한 곳**에 두고,
각 노트북은 그 의미를 자기 문맥에서 다시 설명한다.
(AGENTS.md 원칙 1-2 "같은 정보를 두 곳에 기록하지 않는다",
 원칙 3과의 충돌은 "의미는 반복해도 되지만 정의는 반복하지 않는다"로 해소)

여기 있는 것은 **데이터와 규약**뿐이다. 분석 로직은 각 노트북이 직접 보여준다 —
그것이 노트북의 주제이기 때문이다.
"""

from pathlib import Path

import h5py
import numpy as np

# ── 데이터셋 ────────────────────────────────────────────────
DATASET = Path(__file__).parent / "traces" / "scalib_dataset.h5"

# ── AES-128 상수 ────────────────────────────────────────────
# SubBytes 치환표. 타겟 펌웨어(tiny-AES-c)가 쓰는 것과 같은 표준 S-box 다.
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

AES_BLOCK = 16


def sbox_out(plaintext, key):
    """1라운드 SBox 출력 = SBOX[plaintext XOR key].

    입력: 각각 (n, 16) 또는 (16,) uint8 배열. 브로드캐스트된다.
    출력: 입력과 같은 shape 의 uint8 배열.

    부채널 공격이 겨냥하는 가장 흔한 중간값이다. 평문 한 바이트와 키 한 바이트에만
    의존하므로, 키를 바이트 단위로 나누어 추측할 수 있다(분할 정복).
    """
    return SBOX[np.bitwise_xor(np.asarray(plaintext, dtype=np.uint8),
                               np.asarray(key, dtype=np.uint8))]


def open_dataset(path=None):
    """데이터셋을 열어 h5py.File 을 돌려준다 (with 문으로 쓴다).

    실패 조건: 파일이 없으면 FileNotFoundError 를 내며, 무엇을 먼저 실행해야
    하는지 안내한다. 예제 노트북은 데이터셋 없이는 아무것도 할 수 없다.
    """
    p = Path(path) if path else DATASET
    if not p.is_file():
        raise FileNotFoundError(
            "데이터셋이 없다: %s\n"
            "먼저 0.0.Dataset_Collect.ipynb 를 실행해 트레이스를 수집한다 "
            "(ChipWhisperer 하드웨어 필요, 약 77분)." % p)
    return h5py.File(p, "r")


def load_group(group, n=None, samples=None, path=None):
    """데이터셋의 한 그룹을 메모리로 읽는다.

    입력
        group   : 'explore' | 'profiling' | 'attack' | 'tvla_rk' | 'tvla_fk'
        n       : 앞에서 몇 장만 읽을지. None 이면 전부.
                  profiling 전량은 100,000 x 33,172 int16 = 약 6.6 GB 이므로
                  필요한 만큼만 읽는 것이 좋다.
        samples : 샘플 축 슬라이스. POI 구간만 읽어 메모리를 아낄 때 쓴다.
        path    : 데이터셋 경로 (기본 traces/scalib_dataset.h5)

    출력 (dict)
        k, p, o : (n, 16) uint8   키·평문·암호문
        t       : (n, ns) int16   전력 파형 (SCALib 이 요구하는 dtype 그대로)
        attrs   : dict            측정 조건 (ns, adc_mul, fixed_key 등)

    실패 조건: 그룹 이름이 틀리면 KeyError 를 내며 사용 가능한 이름을 알려준다.
    """
    with open_dataset(path) as h5:
        if group not in h5:
            raise KeyError("그룹 '%s' 가 없다. 사용 가능: %s" % (group, list(h5)))
        g = h5[group]
        sl = slice(None) if n is None else slice(0, n)
        ssl = samples if samples is not None else slice(None)
        return {
            "k": g["i_k"][sl],
            "p": g["i_p"][sl],
            "o": g["o"][sl],
            "t": g["t"][sl, ssl],
            "attrs": {key: h5.attrs[key] for key in h5.attrs},
        }


def dataset_summary(path=None):
    """데이터셋의 측정 조건과 그룹 구성을 문자열로 돌려준다.

    각 노트북 첫머리에서 "무엇을 분석하는 중인지"를 보여주는 데 쓴다.
    """
    with open_dataset(path) as h5:
        lines = ["측정 조건"]
        for key in ("created", "cipher", "platform", "ns", "adc_mul",
                    "adc_freq", "clk_hz", "gain_db", "trace_scale"):
            if key in h5.attrs:
                lines.append("  %-12s %s" % (key, h5.attrs[key]))
        lines.append("")
        lines.append("그룹")
        for name in h5:
            g = h5[name]
            lines.append("  /%-10s %6d 장 x %d 샘플   키=%s 평문=%s"
                         % (name, g["t"].shape[0], g["t"].shape[1],
                            g.attrs.get("key_mode", "?"), g.attrs.get("pt_mode", "?")))
        return "\n".join(lines)
