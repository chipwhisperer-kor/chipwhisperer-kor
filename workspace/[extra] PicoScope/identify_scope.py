#!/usr/bin/env python3
"""Print identity of the attached PicoScope 3000E (psospa)."""

from __future__ import annotations

import sys

import pico_env  # noqa: F401  # sets pypicosdk library path
import pypicosdk as psdk

INFO = (
    ("variant", psdk.UNIT_INFO.PICO_VARIANT_INFO),
    ("serial", psdk.UNIT_INFO.PICO_BATCH_AND_SERIAL),
    ("usb", psdk.UNIT_INFO.PICO_USB_VERSION),
    ("cal", psdk.UNIT_INFO.PICO_CAL_DATE),
    ("hw", psdk.UNIT_INFO.PICO_HARDWARE_VERSION),
    ("fw1", psdk.UNIT_INFO.PICO_FIRMWARE_VERSION_1),
    ("fw2", psdk.UNIT_INFO.PICO_FIRMWARE_VERSION_2),
    ("driver", psdk.UNIT_INFO.PICO_DRIVER_VERSION),
)


def main() -> int:
    scope = psdk.psospa()
    try:
        enumerated = scope.get_enumerated_units()
    except psdk.PicoSDKException as err:
        print(err, file=sys.stderr)
        print(
            "USB 쓰기 권한이 없으면 장치가 보이지 않습니다. "
            "./scripts/enable-usb.sh 를 먼저 실행하세요.",
            file=sys.stderr,
        )
        return 1

    power = scope.open_unit()
    try:
        print("PicoScope")
        for label, code in INFO:
            print(f"  {label:7s}: {scope.get_unit_info(code)}")
        print("  api    : psospa")
        print(f"  lib    : {pico_env.SDK_LIB}")
        if isinstance(enumerated, tuple) and len(enumerated) >= 2:
            print(f"  enumerated: {enumerated[1]} (count={enumerated[0]})")
        else:
            print(f"  enumerated: {enumerated}")
        likely = getattr(power, "powerErrorLikely_", None)
        if likely is not None:
            print(f"  powerErrorLikely: {likely}")
    finally:
        scope.close_unit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
