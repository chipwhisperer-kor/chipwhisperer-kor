#!/usr/bin/env python3
"""Identify an attached 3418E by sweeping its front-panel LEDs.

The command needs a loadable ``libpsospa``, USB write access, and an available
scope. It changes the A, B, C, D, AUX, and AWG LED states, prints completion,
and creates no files. Driver and device errors propagate, while the opened
scope is always closed and the LEDs are left off after a successful sweep.
"""

from __future__ import annotations

import time

import pico_env  # noqa: F401
import pypicosdk as psdk

LEDS = ["A", "B", "C", "D", "AUX", "AWG"]


def main() -> int:
    """Run two LED sweeps and return zero when the final off state is applied."""
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
