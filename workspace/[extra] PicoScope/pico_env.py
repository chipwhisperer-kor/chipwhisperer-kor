"""Select the native ``libpsospa`` used by all PicoScope entry points.

Importing this module prefers the ignored, project-local driver downloaded by
``scripts/fetch-psospa.sh`` and otherwise accepts the system PicoSDK location.
Selecting the local copy changes pypicosdk's process-wide lookup directory. If
neither library exists, import fails with ``FileNotFoundError`` before a USB
device is opened.
"""

from __future__ import annotations

from pathlib import Path

import pypicosdk as psdk

REPO = Path(__file__).resolve().parent
VENDOR_LIB = REPO / ".vendor" / "picoscope" / "lib" / "libpsospa.so"
SYSTEM_LIB = Path("/opt/picoscope/lib/libpsospa.so")


def configure_sdk() -> Path:
    """Return the selected library path and configure pypicosdk when local."""
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
