"""마스킹 구현의 1차 누설 검출 — 결함이 있는 **명령어를 지목**한다.

## 무엇을 판정하나

논문이 증명하는 것: **올바르게 마스킹된 구현에서는 모든 연산의 HW·HD 가 비마스킹
알고리즘의 민감값과 통계적으로 독립이다.**

여기서 검사하는 것은 그 명제가 **이 구현에서도 성립하는가**다. 성립하지 않는 샘플이
있으면 그 샘플을 `sample_map` 으로 되짚어 **(성분, 명령어 주소, 소스 행)** 을 낸다.
"샌다" 가 아니라 "여기서 샌다" 여야 고칠 수 있다.

`tests/dpa.py` 와 **같은 판정 규칙**(spec 의 `criteria`)을 쓴다. 다른 것은 채널과
라벨링뿐이다 — 그래야 에뮬레이션과 실측 결과를 나란히 놓을 수 있다.

## 통계량과 임계 — 왜 귀무분포를 실측하는가

잡음이 0이어도 **표본이 유한하면 SNR 은 0이 아니다.** 그래서 임계를 이론값으로 정하지
않고, **같은 데이터에 라벨을 무작위로 섞어** 귀무분포를 만든 뒤 그 상위 분위수를 쓴다.
라벨만 섞으면 종속성은 사라지고 표본 크기·클래스 분포·트레이스의 통계적 성질은 그대로
유지되므로, "이 데이터에서 우연히 나올 수 있는 최댓값" 을 실측하는 셈이 된다.

다중비교 보정은 이 방식에 이미 들어 있다 — 귀무분포를 **전 샘플의 최댓값** 분포로 잡기
때문이다(family-wise). §8.4 `shall [08.03]` 이 요구하는 보정의 목적을 그대로 만족한다.

## 관점 분리

이 모듈은 **연구자 관점**이다 — 키를 알고, Masked 데이터셋이면 마스크도 안다.
공격 가능성을 재는 것이 아니라 **설계 명제가 구현에서 지켜졌는지**를 재기 때문이다.
공격자 관점 수치(키 복구 가능 여부)는 `cpa` 가 따로 낸다.
"""

import numpy as np
from scalib.metrics import SNR

from . import paths          # noqa: F401 — workspace/lib 를 sys.path 에 넣는다

import sca_schema as S       # noqa: E402
from aes_ref import intermediates   # noqa: E402

BATCH = 500

# 검사할 민감값. 이름 → intermediates() 의 키.
# 1라운드 두 값이 주 표적이고, 라운드키는 §8.3.1 이 지목한 key schedule 표적이다.
DEFAULT_LABELS = ("add_rk0", "sbox_out", "roundkey0", "roundkey1", "round1")


def _snr_over_bytes(traces, labels, nc=256):
    """(n, ns) 트레이스와 (n, 16) 라벨로 바이트별 SNR 을 잰다 → (16, ns).

    SCALib 의 SNR 은 클래스별 평균의 분산 대 클래스 내 분산의 비다.
    독립이면 분자가 0에 가까우므로, 이 값이 크다는 것은 곧 종속이라는 뜻이다.

    SCALib 은 변수(바이트) 16개를 한 번에 받는다 — 라벨 배열을 (n, 16) 으로 주면
    (16, ns) 를 돌려준다. 바이트마다 따로 돌리면 트레이스를 16번 훑게 되어 느리다.
    """
    n = traces.shape[0]
    snr = SNR(nc=nc)
    x = np.ascontiguousarray(labels.astype(np.uint16))
    for beg in range(0, n, BATCH):
        tr = np.ascontiguousarray(traces[beg:beg + BATCH], dtype=np.int16)
        snr.fit_u(tr, x[beg:beg + BATCH])
    return np.asarray(snr.get_snr())


def _null_threshold(traces, labels, n_perm, rng, nc=256):
    """라벨을 섞어 만든 귀무분포에서 family-wise 임계를 얻는다.

    반환: (임계값, 순열별 최댓값 목록)
    임계는 순열 최댓값들의 **최댓값**이다 — n_perm 회 중 한 번도 넘지 않은 선.
    순열 수가 적으면 보수적이지 않을 수 있으므로 결과에 n_perm 을 함께 싣는다.
    """
    maxima = []
    n = traces.shape[0]
    for _ in range(int(n_perm)):
        perm = rng.permutation(n)
        s = _snr_over_bytes(traces, labels[perm], nc=nc)
        maxima.append(float(np.nanmax(s)))
    if not maxima:
        return float("nan"), maxima
    th = float(np.max(maxima))
    # 임계가 유한하지 않으면 **아무것도 검출되지 않는다** — 그리고 그것은 "누설 없음"
    # 처럼 보인다. 이 도구가 낼 수 있는 가장 나쁜 결과이므로 조용히 넘어가지 않고
    # NaN 을 돌려보내 호출측이 `inconclusive` 로 보고하게 한다.
    return (th if np.isfinite(th) else float("nan")), maxima


def run(dataset_path, spec, subset="profiling", labels=DEFAULT_LABELS,
        n_traces=None, n_perm=8, sensitive_window=None, seed=None):
    """1차 독립성 검정을 수행하고 결함 후보를 명령어 단위로 낸다.

    입력
        subset          : 쓸 subset (기본 profiling — 키가 랜덤이라 라벨이 고르게 퍼진다)
        labels          : 검사할 민감값 이름들
        n_traces        : 앞에서 몇 장만. None 이면 전부
        n_perm          : 귀무분포용 라벨 순열 횟수
        sensitive_window: (start, end) 명령어 인덱스 — Annex H 민감 경계.
                          **경계 밖의 검출은 fail 로 세지 않고 따로 보고한다.**

    출력 dict — `verdict`, 라벨별 결과, 결함 후보 목록(주소·성분 포함).

    실패 조건: 데이터셋에 sample_map 이 없으면 KeyError (명령어 축이 아니라는 뜻).
    """
    rng = np.random.RandomState(int(spec["seed"]) if seed is None else seed)
    smap = S.load_sample_map(dataset_path)          # (ns, 3) segment_id, insn_idx, addr
    attrs = S.root_attrs(dataset_path)
    segs = _parse_segments(str(attrs.get("leakage_segments", "")))

    g = S.load_group(dataset_path, subset, n=n_traces,
                     fields=[S.F_TRACE, S.F_KEY, S.F_PLAINTEXT])
    traces = g[S.F_TRACE]
    inter = intermediates(g[S.F_KEY], g[S.F_PLAINTEXT])

    n, ns = traces.shape
    results, candidates = {}, []
    for name in labels:
        if name not in inter:
            results[name] = {"error": "모르는 민감값 이름"}
            continue
        lab = inter[name]
        snr = _snr_over_bytes(traces, lab)                       # (16, ns)
        th, maxima = _null_threshold(traces, lab, n_perm, rng)

        if not np.isfinite(th):
            # 임계를 세울 수 없으면 **판정하지 않는다.** 검출 0 을 "누설 없음" 으로
            # 보고하면 검정력이 없어서 못 본 것과 정말 없는 것을 구분할 수 없게 된다.
            results[name] = {
                "label": name, "n_traces": int(n),
                "snr_max": float(np.nanmax(snr)),
                "null_threshold": None, "null_max_per_perm": maxima,
                "n_perm": int(n_perm), "verdict": "inconclusive",
                "error": ("귀무 임계를 세울 수 없다(순열 SNR 이 유한하지 않다). "
                          "이 라벨은 판정하지 않는다 — 검출 0 을 '누설 없음' 으로 "
                          "보고하면 거짓 안전이 된다."),
                "n_over": 0, "n_over_in_window": 0, "n_over_outside_window": 0,
            }
            continue

        peak = snr.max(axis=0)                                   # 바이트 중 최댓값
        over = np.flatnonzero(peak > th)
        in_win, out_win = _split_window(over, smap, sensitive_window)

        results[name] = {
            "label": name,
            "n_traces": int(n),
            "snr_max": float(np.nanmax(snr)),
            "null_threshold": th,
            "null_max_per_perm": maxima,
            "n_perm": int(n_perm),
            "n_over": int(over.size),
            "n_over_in_window": int(in_win.size),
            "n_over_outside_window": int(out_win.size),
        }
        for idx in in_win[:200]:
            candidates.append(_describe(idx, smap, segs, float(peak[idx]), th, name, True))
        for idx in out_win[:50]:
            candidates.append(_describe(idx, smap, segs, float(peak[idx]), th, name, False))

    n_fail = sum(r.get("n_over_in_window", 0) for r in results.values()
                 if isinstance(r, dict))
    n_incon = sum(1 for r in results.values()
                  if isinstance(r, dict) and r.get("verdict") == "inconclusive")
    # 검출이 없더라도 판정하지 못한 라벨이 있으면 `pass` 라고 쓰지 않는다.
    verdict = "fail" if n_fail else ("inconclusive" if n_incon else "pass")

    return {
        "verdict": verdict,
        "perspective": "연구자 — 키를 알고 검정한다. 공격 가능성이 아니라 설계 명제의 성립 여부를 잰다.",
        "proposition": ("올바르게 마스킹된 구현에서는 모든 연산의 HW·HD 가 비마스킹 "
                        "알고리즘의 민감값과 통계적으로 독립이다."),
        "subset": subset,
        "n_traces": int(n),
        "samples": int(ns),
        "order": 1,
        "order_note": ("1차 한정. 고차 DPA 는 ISO/IEC 17825 Fig.1 NOTE 3 에 따라 필수 시험이 "
                       "아니며, 1차 부울 마스킹이 2차에서 뚫리는 것은 이론적으로 정상이라 "
                       "결함으로 보고할 수 없다."),
        "threshold_method": ("라벨 무작위 순열 %d회의 family-wise 최댓값. 유한 표본에서 "
                             "우연히 나올 수 있는 SNR 상한을 실측한 값이다." % n_perm),
        "labels": results,
        "n_candidates": len(candidates),
        "candidates": candidates,
        "sensitive_window": (None if sensitive_window is None
                             else [int(sensitive_window[0]), int(sensitive_window[1])]),
    }


def _parse_segments(text):
    """`"hw_reg:0-6051,hd_reg:6051-12102"` → [(name, lo, hi), …]"""
    out = []
    for part in text.split(","):
        part = part.strip()
        if not part or ":" not in part:
            continue
        name, _, rng_ = part.partition(":")
        lo, _, hi = rng_.partition("-")
        try:
            out.append((name, int(lo), int(hi)))
        except ValueError:
            continue
    return out


def _split_window(over, smap, window):
    """민감 경계 안/밖으로 나눈다. 경계는 **명령어 인덱스** 기준이다.

    샘플 인덱스로 자르면 성분마다 경계가 어긋난다 — `hw_reg` 의 5000번 샘플과
    `hd_reg` 의 5000번 샘플은 서로 다른 명령어다. `sample_map` 의 명령어 인덱스로 판단한다.
    """
    if window is None or over.size == 0:
        return over, np.array([], dtype=int)
    lo, hi = window
    insn_idx = smap[over, 1]
    m = (insn_idx >= lo) & (insn_idx < hi)
    return over[m], over[~m]


def _describe(sample_idx, smap, segs, value, threshold, label, in_window):
    """검출된 샘플을 사람이 고칠 수 있는 형태로 옮긴다."""
    seg_id, insn_idx, addr = (int(x) for x in smap[sample_idx])
    seg_name = segs[seg_id][0] if seg_id < len(segs) else "seg%d" % seg_id
    return {
        "sample": int(sample_idx),
        "component": seg_name,
        "instruction_index": insn_idx,
        "address": "0x%x" % addr,
        "label": label,
        "statistic": value,
        "threshold": threshold,
        "in_sensitive_window": bool(in_window),
    }
