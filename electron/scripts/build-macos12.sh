#!/bin/bash
set -euo pipefail
RECIPE=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
: "${ELECTRON_WORKSPACE:?Set ELECTRON_WORKSPACE to the gclient workspace containing src/electron}"
: "${MACOS_SDK_PATH:?Set MACOS_SDK_PATH to the private prepared MacOSX15.5.sdk copy}"
SRC="$ELECTRON_WORKSPACE/src"
apply_once() {
  local repo=$1 patch=$2
  if git -C "$repo" apply --reverse --check "$patch" 2>/dev/null; then return; fi
  git -C "$repo" apply --check "$patch"
  git -C "$repo" apply "$patch"
}
# Run gclient sync/hooks per README before this script, including Electron's
# upstream patch series. The dependency-install patch belongs before hooks.
apply_once "$SRC/electron" "$RECIPE/patches/electron-macos12.patch"
apply_once "$SRC" "$RECIPE/patches/chromium-macos12.patch"
B="$SRC/out/ReleaseMacOS12"
mkdir -p "$B/sdk"
if [ ! -e "$B/sdk/MacOSX15.5.sdk" ]; then ln -s "$MACOS_SDK_PATH" "$B/sdk/MacOSX15.5.sdk"; fi
cp "$RECIPE/configs/macos12-x64-release.gn" "$B/args.gn"
export CHROMIUM_BUILDTOOLS_PATH="$SRC/buildtools"
export DEVELOPER_DIR="${DEVELOPER_DIR:-/Applications/Xcode.app/Contents/Developer}"
cd "$SRC"
buildtools/mac/gn gen out/ReleaseMacOS12 --fail-on-unused-args
autoninja -C out/ReleaseMacOS12 -j12 electron
autoninja -C out/ReleaseMacOS12 -j12 electron:electron_dist_zip
