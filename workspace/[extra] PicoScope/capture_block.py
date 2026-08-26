#!/usr/bin/env python3
"""Capture channel A once while the PicoScope AWG is running.

The command needs an attached scope, a loadable ``libpsospa``, and USB write
access. It configures the AWG, channel A, and an auto-trigger; then it overwrites
``captures/chA_block.csv`` and ``captures/chA_block.png``. Driver and device
errors propagate to the caller, while the opened scope is always closed.

An AWG-to-channel-A BNC loopback shows the generated sine wave. With no
loopback, the same capture path records open-input noise.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import pico_env  # noqa: F401
import pypicosdk as psdk

SAMPLES = 10_000
SAMPLE_RATE_MSPS = 10
AWG_HZ = 10_000
AWG_PK2PK = 1.0
OUT_DIR = Path(__file__).resolve().parent / "captures"


def main() -> int:
    """Run the configured capture and return zero after both output files exist."""
    scope = psdk.psospa()
    scope.open_unit()
    try:
        variant = scope.get_unit_info(psdk.UNIT_INFO.PICO_VARIANT_INFO)
        serial = scope.get_unit_serial()
        sig = scope.set_siggen(
            frequency=AWG_HZ,
            pk2pk=AWG_PK2PK,
            wave_type=psdk.WAVEFORM.SINE,
        )
        scope.set_channel(channel=psdk.CHANNEL.A, range=psdk.RANGE.V2)
        # 100 ms auto-trigger so an open BNC still completes.
        scope.set_simple_trigger(
            channel=psdk.CHANNEL.A,
            threshold=0,
            auto_trigger=100_000,
        )
        timebase = scope.sample_rate_to_timebase(
            sample_rate=SAMPLE_RATE_MSPS, unit=psdk.SAMPLE_RATE.MSPS
        )
        actual_rate = scope.get_actual_sample_rate()
        buffers, time_axis = scope.run_simple_block_capture(timebase, SAMPLES)
        ch_a = np.asarray(buffers[psdk.CHANNEL.A], dtype=float)
    finally:
        scope.close_unit()

    OUT_DIR.mkdir(exist_ok=True)
    stem = OUT_DIR / "chA_block"
    np.savetxt(
        f"{stem}.csv",
        np.column_stack([time_axis, ch_a]),
        delimiter=",",
        header="time_ns,chA_mV",
        comments="",
    )

    plt.figure(figsize=(10, 4))
    plt.plot(time_axis, ch_a, linewidth=0.8)
    plt.xlabel("Time (ns)")
    plt.ylabel("Channel A (mV)")
    plt.title(f"{variant} {serial}  {actual_rate:g} S/s")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{stem}.png", dpi=120)
    plt.close()

    peak = float(np.max(np.abs(ch_a)))
    rms = float(np.sqrt(np.mean(ch_a * ch_a)))
    print(f"variant     : {variant}")
    print(f"serial      : {serial}")
    print(f"awg         : {sig}")
    print(f"sample rate : {actual_rate:g} S/s  (requested {SAMPLE_RATE_MSPS} MS/s)")
    print(f"samples     : {ch_a.size}")
    print(f"chA min/max : {ch_a.min():.3f} / {ch_a.max():.3f} mV")
    print(f"chA rms/peak: {rms:.3f} / {peak:.3f} mV")
    print(f"wrote       : {stem}.csv")
    print(f"wrote       : {stem}.png")
    if peak < 100:
        print(
            "hint: peak < 100 mV — 열린 입력(또는 접지)입니다. "
            "AWG BNC를 채널 A에 연결하면 10 kHz 정현파가 보여야 합니다."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
