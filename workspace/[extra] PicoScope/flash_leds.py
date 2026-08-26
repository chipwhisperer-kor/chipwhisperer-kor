#!/usr/bin/env python3
"""Sweep the 3418E front-panel LEDs so the physical unit can be identified."""

from __future__ import annotations

import time

import pico_env  # noqa: F401
import pypicosdk as psdk

LEDS = ["A", "B", "C", "D", "AUX", "AWG"]


def main() -> int:
    scope = psdk.psospa()
    scope.open_unit()
    try:
        scope.set_all_led_colours("blue")
        scope.set_all_led_states("off")
        states = ["off"] * len(LEDS)
        for _ in range(2):
            for i in range(len(LEDS)):
                states[i] = "on"
                scope.set_led_states(LEDS, states)
                time.sleep(0.15)
                states[i] = "off"
                scope.set_led_states(LEDS, states)
        scope.set_all_led_states("off")
        print("LED sweep finished (A B C D AUX AWG).")
    finally:
        scope.close_unit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
