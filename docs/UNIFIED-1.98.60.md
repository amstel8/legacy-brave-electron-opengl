# Brave 1.98.60 / Chromium 156 unified build

## Exact inputs and artifact

- Brave Core v1.98.60: `52db4b25c0aa3038e9a1c6021428b136cc3cb5fc`.
- Chromium 156.0.8078.48: `d0c02bfad08ec92a6ffcf989e53cd995e6381a4c`.
- Bundle/application version: `156.1.98.0`; CFBundleVersion: `198.0`.
- Framework SHA-256: `696e583e6654830c40b46b8180c4916856ef9d0b991f40763da252915a026cff`.
- Minimum macOS: 12.0. Architecture: x86_64. Application size: approximately 577 MiB.
- Output: `out/ReleaseOfficial/Brave Browser.app`.

The worker attempted `ignore_patch_version_number=false`, but bundle metadata still omits the patch number. The source revisions above identify this build; no version-only rebuild or binary version alteration was performed.

## Configuration and source changes

Use the [Chromium 156 recipe](../recipes/brave-1.98.60/README.md) for patch order and scope. Retain the SDK preparation/prerequisites described in the earlier [build instructions](BUILD.md), using the pinned versions above rather than the older Chromium 155 revisions.

The actual build used Xcode 14.2 host tools and the prepared macOS 15.5 SDK. Relevant GN settings:

```gn
target_cpu = "x64"
mac_deployment_target = "12.0"
mac_min_system_version = "12.0"
mac_sdk_min = "13"
# Point mac_sdk_path to your prepared local SDK 15.5.
is_official_build = true
is_debug = false
is_component_build = false
dcheck_always_on = false
enable_expensive_dchecks = false
chrome_pgo_phase = 2
use_thin_lto = true
thin_lto_enable_optimizations = true
thin_lto_backend_jobs = 4
symbol_level = 0
blink_symbol_level = 0
use_clang_modules = false
use_unified_system_module = false
clang_use_chrome_plugins = false
treat_warnings_as_errors = false
enable_precompiled_headers = false
use_prebuilt_omaha4 = false
mac_allow_system_xcode_for_official_builds_for_testing = true
```

Preflight also confirmed zero stack initialization and the Viz debugger disabled. Chromium and V8 PGO profiles were downloaded from the source-pinned revisions. The Brave wrapper used `pnpm run build Release -C ReleaseOfficial --target_os=mac --target_arch=x64 --skip_signing`, the GN arguments above, and twelve Ninja jobs. Host-specific SDK paths and proprietary service keys are not distributed. Missing proprietary service credentials use placeholders; related services may not function.

Build succeeded on 2026-10-25 at 14:57:58 MSK: exit 0, 61,090 steps in 11h03m03s. Dependency synchronization reused exact Chromium 156 dependency objects from a local Electron checkout where available. This optimization does not change the pinned source commits.

## Installation and validation boundary

Installed and launched on the macOS 12.7.6 desktop (Radeon RX 6800 XT) and OCLP MacBookPro7,1 (GeForce 320M). The installed framework on both machines matched the hash above. Existing stable profile directories were retained; complete previous-app/profile backups were made, with 13 and 11 important profile files verified respectively before replacement. Both browsers were reopened through their graphical sessions with session restoration. The MacBook GPU child automatically used `--use-angle=gl` without forcing that option at launch.

This is startup/installation evidence. Detailed WebGL pixel checks, GPU feature reports, performance comparisons and long-duration validation have not been completed for this build. Validation results for the older Brave/Electron releases must not be treated as results for this exact binary.

The new incomplete-image workaround is included but Avito flicker resolution has not been visually confirmed. Static JPEG/WebP images on legacy GL appear only after downloading fully. Metal, animated images and other formats retain their prior behavior. See the [recipe](../recipes/brave-1.98.60/README.md) for the mechanism and limitations.
