#!/bin/bash
set -euo pipefail
RECIPE=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
: "${ELECTRON_WORKSPACE:?Set ELECTRON_WORKSPACE to the gclient workspace containing src/electron}"
: "${MACOS_SDK_PATH:?Set MACOS_SDK_PATH to the private prepared MacOSX15.5.sdk copy}"
SRC="$ELECTRON_WORKSPACE/src"
# Refuse an accidental rebuild of the previous Electron checkout.
git -C "$SRC/electron" merge-base --is-ancestor \
  45d20ec03000aac41e73b2abdb707936b4f98ed0 HEAD
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
buildtools/mac/gn args out/ReleaseMacOS12 --list --json > out/ReleaseMacOS12/effective-args.json
python3 - <<'VERIFY'
import hashlib
import json
from pathlib import Path
src = Path.cwd()
args = {v['name']: v.get('current', v['default'])['value']
        for v in json.loads((src/'out/ReleaseMacOS12/effective-args.json').read_text())}
expected = {
    'is_official_build': 'true', 'is_debug': 'false',
    'is_component_build': 'false', 'chrome_pgo_phase': '2',
    'use_thin_lto': 'true', 'thin_lto_enable_optimizations': 'true',
    'thin_lto_backend_jobs': '4', 'dcheck_always_on': 'false',
    'enable_expensive_dchecks': 'false',
    'mac_deployment_target': '"12.0"', 'mac_min_system_version': '"12.0"',
}
for key, value in expected.items():
    if args.get(key) != value:
        raise SystemExit(f'Unexpected GN argument {key}: {args.get(key)}')
profiles = src/'electron/build/pgo_profiles'
for state in ['macos-x64', 'v8-builtins']:
    fields = (profiles/(state+'.pgo.txt')).read_text().split()
    name = fields[0] if state != 'v8-builtins' else 'electron-v8-builtins.profile'
    if hashlib.sha256((profiles/name).read_bytes()).hexdigest() != fields[1]:
        raise SystemExit('Profile hash mismatch: '+state)
print('Official Release arguments and Electron PGO profiles verified.')
VERIFY
autoninja -C out/ReleaseMacOS12 -j12 electron
autoninja -C out/ReleaseMacOS12 -j12 electron:electron_dist_zip
