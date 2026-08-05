"""
Fixed-vs-random TVLA (|t|) from two HDF5 trace groups — full-RAM path.

=============================================================================
SINGLE SOURCE OF TRUTH (this file)
=============================================================================
- Project truths for Python TVLA live only under this package directory
  (``tvla/``). Session notes, chat, and external wikis are not authoritative.
- **This module header + the function bodies below** are the sole definition of
  the TVLA math, memory contract, and full-load algorithm for Python.
- When changing the formula or memory rules: edit **this file only**, then keep
  short summaries elsewhere in sync if they exist. Do not copy the long formula
  into other modules.
- MATLAB ``+tvla/h5onMem.m`` is a legacy reference for comparison; **runtime
  behavior SSOT is this Python module**, not the .m file.
- Driver CLI paths / loop / plot-save: SSOT is ``run_tvla.py`` (not here).

=============================================================================
PURPOSE
=============================================================================
Compute, for every time sample, the absolute Welch-style t-statistic that
compares group A (e.g. fixed-key/plaintext) against group B (e.g. random).

Same math as the historical MATLAB port, with one intentional difference for
~1 TB groups: sum-of-squares uses **in-place** squaring (MEMORY CONTRACT).

=============================================================================
INPUT ASSUMPTIONS
=============================================================================
- Each HDF5 dataset is a 2-D array with shape:

      (n_samples, n_traces)

  row  = time sample index
  col  = trace index
  (MATLAB: size(TR, 2) == number of traces.)

- Typical dtype on disk: float32 (1 TB scale). Reductions and final t use
  float64 accumulators for numerical stability.

- Groups A and B may live in different files; dataset path strings are arguments.

=============================================================================
FORMULA  (authoritative prose form — implementers: match welch_abs body)
=============================================================================
For one group with matrix TR (samples x traces):

    N  = n_traces
    S  = sum over traces of TR           -> length n_samples
    Q  = sum over traces of TR.^2        -> length n_samples
    mu = S / N
    m2 = Q / N

After both groups:

    t = (mu_A - mu_B)
        / sqrt( (m2_A - mu_A^2) / N_A  +  (m2_B - mu_B^2) / N_B )

    return abs(t)

Notes:
- Variance per sample is (m2 - mu^2) = E[X^2] - E[X]^2.
- The terms under the sqrt use /N (not /(N-1)), same as the MATLAB port.

=============================================================================
MEMORY CONTRACT  (critical for ~1 TB groups on ~1.5 TiB RAM)
=============================================================================
Allowed peak: about sizeof(one group) + a few small vectors.

Sequence (never hold A and B together):

    1. Load group A fully from SSD into RAM   (~1 x group size)
    2. Reduce A to (N_A, S_A, Q_A)            (small vectors)
    3. Delete A
    4. Load group B fully
    5. Reduce B to (N_B, S_B, Q_B)
    6. Delete B
    7. Form t from the six small vectors

How Q is obtained without a second 1 TB array:

    S = sum(TR, axis=1)
    TR *= TR                # IN-PLACE square — no temporary TR**2
    Q = sum(TR, axis=1)
    del TR

FORBIDDEN:
    - out-of-place square: tmp = TR**2  or  np.square(TR) without out=
    - loading A and B at the same time
    - putting the full ~1 TB group into GPU VRAM

=============================================================================
PROCESSING ORDER
=============================================================================
    log "group A" -> load A -> stats_in_place(A) -> free
    log "group B" -> load B -> stats_in_place(B) -> free
    log "TVLA"    -> welch_abs(...) -> |t|

=============================================================================
USAGE EXAMPLE
=============================================================================
    from tvla.h5_on_mem import h5_on_mem

    t = h5_on_mem(
        path_a="/data/SCA_fixed_0.h5",
        dset_a="/t_hw",
        path_b="/data/SCA_random.h5",
        dset_b="/t_hw",
    )
    # t.shape == (n_samples,)

    # Synthetic (no files); destroys arrays in-place:
    from tvla.h5_on_mem import tvla_from_arrays
    import numpy as np
    A = np.random.randn(1000, 500).astype(np.float32)
    B = np.random.randn(1000, 500).astype(np.float32)
    t = tvla_from_arrays(A, B)

=============================================================================
MATLAB CORRESPONDENCE  (formula restated above; .m file not required to read)
=============================================================================
Legacy MATLAB used sum(TR,2) and sum(TR.^2,2) then the same t with /N under
the sqrt. Out-of-place TR.^2 can need ~2x RAM; this module only changes that
to in-place squaring. Executable SSOT for Python is this file, not the .m.
"""

from __future__ import annotations

from datetime import datetime
from typing import Tuple

import h5py
import numpy as np


def _now() -> str:
    return datetime.now().strftime("%y-%m-%d-%H-%M-%S")


def _dset_path(dset: str) -> str:
    """HDF5 dataset path with a single leading slash (SSOT for path shape)."""
    return dset if dset.startswith("/") else "/" + dset


def load_traces(path: str, dset: str) -> np.ndarray:
    """
    Load one HDF5 dataset entirely into RAM.

    path : HDF5 file path.
    dset : dataset inside the file (with or without leading /).

    Returns array shape (n_samples, n_traces). Caller frees after reduce.
    Peak RAM contribution ≈ dataset nbytes (+ library overhead).
    """
    dset = _dset_path(dset)
    with h5py.File(path, "r") as f:
        if dset not in f:
            raise KeyError(f"dataset {dset!r} not in {path!r}; keys={list(f.keys())}")
        arr = f[dset][()]
    if arr.ndim != 2:
        raise ValueError(
            f"expected 2-D (n_samples, n_traces), got shape {arr.shape} from {path}{dset}"
        )
    return arr


def stats_in_place(tr: np.ndarray) -> Tuple[int, np.ndarray, np.ndarray]:
    """
    Reduce one group to (N, S, Q) and destroy tr in-place.

    Order (why):
      1) S = sum(tr) while values are still raw samples
      2) tr *= tr  — in-place square; avoids a second full-size array (~1 TB)
      3) Q = sum(tr) on the squared values
      4) caller must drop the last reference to tr immediately after

    Returns
      N : int — n_traces (tr.shape[1])
      S, Q : float64 vectors length n_samples — sum and sum-of-squares

    After return, tr holds squares, not raw samples. Do not reuse as traces.
    """
    if tr.ndim != 2:
        raise ValueError(f"tr must be 2-D (samples, traces), got {tr.shape}")

    n_traces = int(tr.shape[1])
    if n_traces == 0:
        raise ValueError("n_traces == 0")

    # axis=1: sum across traces (columns)
    S = np.sum(tr, axis=1, dtype=np.float64)

    # In-place square — never: tmp = tr ** 2
    tr *= tr

    Q = np.sum(tr, axis=1, dtype=np.float64)
    return n_traces, S, Q


def welch_abs(
    S_a: np.ndarray,
    Q_a: np.ndarray,
    n_a: int,
    S_b: np.ndarray,
    Q_b: np.ndarray,
    n_b: int,
) -> np.ndarray:
    """
    |t| from precomputed per-sample sums (S) and sums-of-squares (Q).

    Implements the module-header FORMULA (mu=S/N, m2=Q/N, then Welch-style t).
    Change the math in the module header and this body together; this body is
    the executable truth.

    Inputs: 1-D length n_samples (or broadcastable). Returns abs(t).
    Zero denominator → NaN (same class of undefined as 0/0), then abs.
    """
    if n_a <= 0 or n_b <= 0:
        raise ValueError(f"N must be positive, got n_a={n_a}, n_b={n_b}")

    mu_a = S_a / n_a
    mu_b = S_b / n_b
    m2_a = Q_a / n_a
    m2_b = Q_b / n_b

    # (E[X^2]-E[X]^2)/N per group, then combine under sqrt
    var_mean_a = (m2_a - mu_a * mu_a) / n_a
    var_mean_b = (m2_b - mu_b * mu_b) / n_b

    with np.errstate(divide="ignore", invalid="ignore"):
        t = (mu_a - mu_b) / np.sqrt(var_mean_a + var_mean_b)

    return np.abs(t)


def h5_on_mem(
    path_a: str,
    dset_a: str,
    path_b: str,
    dset_b: str,
) -> np.ndarray:
    """
    Full-RAM TVLA for one dataset pair: return |t| of length n_samples.

    Order: load A → stats_in_place → del A → load B → stats_in_place → del B
    → welch_abs. Never holds both groups; squares in-place (see module header).
    """
    da, db = _dset_path(dset_a), _dset_path(dset_b)

    print(f"그룹 A 시작  {_now()}  {path_a}{da}")
    tr = load_traces(path_a, da)
    n_a, S_a, Q_a = stats_in_place(tr)
    del tr

    print(f"그룹 B 시작  {_now()}  {path_b}{db}")
    tr = load_traces(path_b, db)
    n_b, S_b, Q_b = stats_in_place(tr)
    del tr

    if S_a.shape != S_b.shape:
        raise ValueError(
            f"sample-length mismatch: A {S_a.shape} vs B {S_b.shape}"
        )

    print(f"TVLA 시작  {_now()}  N_A={n_a}  N_B={n_b}  n_samples={S_a.shape[0]}")
    return welch_abs(S_a, Q_a, n_a, S_b, Q_b, n_b)


def tvla_from_arrays(tr_a: np.ndarray, tr_b: np.ndarray) -> np.ndarray:
    """
    Same TVLA as h5_on_mem from arrays already in RAM (tests / small data).

    WARNING: destroys tr_a and tr_b in-place (squares them). Copy first if
    raw traces are still needed.
    """
    n_a, S_a, Q_a = stats_in_place(tr_a)
    n_b, S_b, Q_b = stats_in_place(tr_b)
    if S_a.shape != S_b.shape:
        raise ValueError(
            f"sample-length mismatch: A {S_a.shape} vs B {S_b.shape}"
        )
    return welch_abs(S_a, Q_a, n_a, S_b, Q_b, n_b)


def list_datasets(path: str) -> list[str]:
    """
    Names of all datasets in an HDF5 file (visititems; usual SCA: root-level).
    """
    names: list[str] = []

    def _visitor(name, obj):
        if isinstance(obj, h5py.Dataset):
            names.append(name)

    with h5py.File(path, "r") as f:
        f.visititems(_visitor)
    return names
