"""Locate libpsospa and apply pypicosdk.override_directory before opening a scope."""

from __future__ import annotations

from pathlib import Path

import pypicosdk as psdk

REPO = Path(__file__).resolve().parent
VENDOR_LIB = REPO / ".vendor" / "picoscope" / "lib" / "libpsospa.so"
SYSTEM_LIB = Path("/opt/picoscope/lib/libpsospa.so")


def configure_sdk() -> Path:
    if VENDOR_LIB.exists():
        psdk.override_directory(str(VENDOR_LIB.parent.parent))
        return VENDOR_LIB
    if SYSTEM_LIB.exists():
        return SYSTEM_LIB
    raise FileNotFoundError(
        "libpsospa.so 가 없습니다. scripts/fetch-psospa.sh 를 실행하거나 "
        "Pico libpsospa 패키지를 설치하세요."
    )


SDK_LIB = configure_sdk()
