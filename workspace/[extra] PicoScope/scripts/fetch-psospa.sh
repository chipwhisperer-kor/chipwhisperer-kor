#!/usr/bin/env bash
# Download the x86-64 Pico libpsospa Debian package and extract it into .vendor/.
# Input: network access plus curl and dpkg-deb; no command-line arguments.
# Output: the native library and headers under .vendor/picoscope.
# Failure: download, package extraction, or expected package layout errors.
# Side effect: replaces only the ignored .vendor/picoscope/lib and include trees;
# it does not install the PicoScope GUI or modify the host package database.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$REPO/.vendor/picoscope"
BASE="https://labs.picotech.com/picoscope7/debian"
DEB="libpsospa_1.1.7-0r5994_amd64.deb"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$TMP" "$DEST"
curl -fsSL -o "$TMP/$DEB" "$BASE/pool/main/libp/libpsospa/$DEB"
dpkg-deb -x "$TMP/$DEB" "$TMP/root"
rm -rf "$DEST/lib" "$DEST/include"
mkdir -p "$DEST/lib" "$DEST/include"
cp -a "$TMP/root/opt/picoscope/lib/libpsospa.so"* "$DEST/lib/"
cp -a "$TMP/root/opt/picoscope/include/libpsospa" "$DEST/include/"
echo "Installed $DEST/lib/libpsospa.so"
ls -lh "$DEST/lib"
