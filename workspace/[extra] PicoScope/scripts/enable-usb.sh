#!/usr/bin/env bash
# Temporarily chmod Pico USB device nodes to 0666 without host sudo.
# Uses a local privileged container that bind-mounts /dev/bus/usb.
set -euo pipefail

python3 - <<PY
import os, subprocess, sys

image = os.environ.get("PICO_USB_DOCKER_IMAGE", "ubuntu:24.04")
nodes = []
for name in os.listdir("/sys/bus/usb/devices"):
    sysfs = f"/sys/bus/usb/devices/{name}"
    try:
        vendor = open(f"{sysfs}/idVendor").read().strip()
    except FileNotFoundError:
        continue
    if vendor != "0ce9":
        continue
    bus = open(f"{sysfs}/busnum").read().strip().zfill(3)
    dev = open(f"{sysfs}/devnum").read().strip().zfill(3)
    nodes.append(f"/dev/bus/usb/{bus}/{dev}")

if not nodes:
    print("Pico USB device not found (idVendor=0ce9)", file=sys.stderr)
    sys.exit(1)

for node in nodes:
    mode = os.stat(node).st_mode & 0o222
    if mode:
        print(f"{node} already writable ({oct(os.stat(node).st_mode & 0o777)})")
        continue
    subprocess.check_call(
        [
            "docker", "run", "--rm", "--privileged", "--network=none",
            "-v", "/dev/bus/usb:/dev/bus/usb",
            image, "chmod", "0666", node,
        ]
    )
    print(f"{node} -> {oct(os.stat(node).st_mode & 0o777)}")
PY
