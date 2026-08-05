#!/usr/bin/env python3
"""
Driver: fixed-vs-random TVLA over datasets in two HDF5 files.

=============================================================================
ROLE OF THIS FILE (self-contained for the driver)
=============================================================================
This script only:

  1. Resolves paths to the fixed (group A) and random (group B) HDF5 files.
  2. Chooses which dataset name(s) to process (all in A, or --dset one name).
  3. For each name, calls ``h5_on_mem(path_a, name, path_b, name)``.
  4. Plots |t| or saves a .npy dict, or runs --self-test.

CLI defaults and loop/plot/save behavior are defined **only here**
(Single Source of Truth for how you invoke a batch run).

What each call does operationally (enough to run safely without opening
other docs):

  - Loads **one** full trace group into RAM at a time (scale: up to ~1 TB).
  - Reduces it to per-sample sum and sum-of-squares, then frees that group.
  - Squares samples **in-place** on the loaded array (no second full copy).
  - Never keeps group A and group B resident together.
  - Returns a 1-D |t| vector (one value per time sample).

Exact symbols, algebraic formula, and the full forbidden list for memory are
**defined and implemented only in** ``h5_on_mem`` (this package). Do not
duplicate that long formula here; change math only in that module.

=============================================================================
USAGE  (run from the parent of package ``tvla``, i.e. Matlab_mCode)
=============================================================================
    python -m tvla.run_tvla \\
        --folder /home/user/docker-server/data/ing_AES_with_thpark/ \\
        --fixed SCA_fixed_0.h5 \\
        --random SCA_random.h5

    python -m tvla.run_tvla --folder ... --save
    python -m tvla.run_tvla --folder ... --dset t_hw
    python -m tvla.run_tvla --self-test

Default --folder / --fixed / --random match the historical MATLAB driver paths.
"""

from __future__ import annotations

import argparse
import os
from datetime import datetime

import numpy as np

from tvla.h5_on_mem import h5_on_mem, list_datasets, tvla_from_arrays


def _now() -> str:
    return datetime.now().strftime("%y-%m-%d-%H-%M-%S")


def plot_tvla(t: np.ndarray, title: str, y_range=None) -> None:
    """
    Plot |t| vs sample index.

    t : 1-D absolute t-statistic per sample.
    title : figure title (usually dataset name).
    y_range : optional (ymin, ymax); omit to autoscale.
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 4), facecolor="w")
    ax.plot(t)
    ax.set_xlim(0, max(len(t) - 1, 0))
    ax.set_title(title if title else "|t|")
    ax.set_xlabel("sample")
    ax.set_ylabel("|t|")
    if y_range is not None and not (isinstance(y_range, float) and np.isnan(y_range)):
        ax.set_ylim(y_range)
    fig.tight_layout()
    plt.show()


def run(
    folder: str,
    fixed_name: str,
    random_name: str,
    dset: str | None,
    do_save: bool,
    no_plot: bool,
) -> None:
    """
    Walk datasets and compute TVLA.

    folder/fixed_name  -> group A file
    folder/random_name -> group B file
    dset: if set, only that dataset; else every dataset found in the fixed file
          (same name is required in the random file when h5_on_mem opens it).
    """
    path_a = os.path.join(folder, fixed_name)
    path_b = os.path.join(folder, random_name)

    if not os.path.isfile(path_a):
        raise FileNotFoundError(path_a)
    if not os.path.isfile(path_b):
        raise FileNotFoundError(path_b)

    if dset is not None:
        names = [dset.lstrip("/")]
    else:
        names = list_datasets(path_a)
        if not names:
            raise RuntimeError(f"no datasets in {path_a}")

    results: dict[str, np.ndarray] = {}
    for name in names:
        key = name if name.startswith("/") else "/" + name
        print(f"=== dataset {key}  {_now()} ===")
        t = h5_on_mem(path_a, key, path_b, key)
        results[name] = t
        print(f"    done  max|t|={float(np.nanmax(t)):.4f}  n_samples={t.shape[0]}")

    if do_save:
        out = os.path.join(folder, f"TVLA-result-{_now()}.npy")
        # load: np.load(path, allow_pickle=True).item()  -> dict name -> array
        np.save(out, results, allow_pickle=True)
        print(f"TVLA 결과 저장  {_now()}  {out}")
    elif not no_plot:
        for name, t in results.items():
            plot_tvla(t, name)


def self_test() -> None:
    """
    Numeric smoke test without HDF5 files.

    Compares tvla_from_arrays (production in-place path) to a tiny reference
    that may use out-of-place squares only because the arrays are small.
    Also checks that working copies were squared in-place.
    """
    rng = np.random.default_rng(0)
    n_samples, n_a, n_b = 64, 200, 180
    A = rng.standard_normal((n_samples, n_a), dtype=np.float64)
    B = rng.standard_normal((n_samples, n_b), dtype=np.float64) + 0.05

    Sa = A.sum(axis=1)
    Qa = (A ** 2).sum(axis=1)
    Sb = B.sum(axis=1)
    Qb = (B ** 2).sum(axis=1)
    mu_a, mu_b = Sa / n_a, Sb / n_b
    m2_a, m2_b = Qa / n_a, Qb / n_b
    denom = np.sqrt((m2_a - mu_a**2) / n_a + (m2_b - mu_b**2) / n_b)
    with np.errstate(divide="ignore", invalid="ignore"):
        t_ref = np.abs((mu_a - mu_b) / denom)

    A2 = A.copy()
    B2 = B.copy()
    t = tvla_from_arrays(A2, B2)

    # finite entries only (denom>0)
    mask = np.isfinite(t_ref) & np.isfinite(t)
    err = np.max(np.abs(t[mask] - t_ref[mask]) / np.maximum(t_ref[mask], 1e-15))
    print(f"self-test max relative error = {err:.3e}")
    if err > 1e-10:
        raise AssertionError(f"TVLA mismatch vs reference, err={err}")

    if not np.allclose(A2, A * A):
        raise AssertionError("stats_in_place did not square group A in-place")
    if not np.allclose(B2, B * B):
        raise AssertionError("stats_in_place did not square group B in-place")

    print("self-test OK")


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(
        description="Fixed-vs-random TVLA over HDF5 trace datasets (full-RAM, sequential groups)."
    )
    p.add_argument(
        "--folder",
        default="/home/user/docker-server/data/ing_AES_with_thpark/",
        help="Directory containing the two H5 files",
    )
    p.add_argument("--fixed", default="SCA_fixed_0.h5", help="Group A filename")
    p.add_argument("--random", default="SCA_random.h5", help="Group B filename")
    p.add_argument(
        "--dset",
        default=None,
        help="Single dataset name (default: all datasets in the fixed file)",
    )
    p.add_argument(
        "--save",
        action="store_true",
        help="Save results to TVLA-result-<timestamp>.npy instead of plotting",
    )
    p.add_argument(
        "--no-plot",
        action="store_true",
        help="Compute only (no plot); useful headless without --save",
    )
    p.add_argument(
        "--self-test",
        action="store_true",
        help="Run synthetic numeric check and exit",
    )
    args = p.parse_args(argv)

    if args.self_test:
        self_test()
        return

    run(
        folder=args.folder,
        fixed_name=args.fixed,
        random_name=args.random,
        dset=args.dset,
        do_save=args.save,
        no_plot=args.no_plot,
    )


if __name__ == "__main__":
    main()
