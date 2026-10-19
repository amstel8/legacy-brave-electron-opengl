# macOS 12 build recipe and patch inventory

For the current v1.97.59 release with automatic Metal/OpenGL selection, see [UNIFIED-1.97.59.md](UNIFIED-1.97.59.md) and [release notes](RELEASE-1.97.59.md). The older pinned versions and manual OpenGL steps below describe the original v1.97.56 builds.

## Pinned source and tools

Use Brave v1.97.56 (b01cdf43be4b4d5559bf7e58229e666e24454f50) and its pinned Chromium 155.0.8059.40 (cfaadc5a132d78e1828635aa8405a499f3e14864). Follow Brave's documented macOS prerequisites and brave-browser dependency-sync workflow. The source checkout and its third-party dependencies are intentionally fetched upstream; this repository contains patches and release assets, not a Chromium fork. Tested tools: Node 24.21.0, pnpm 11.28.5, depot_tools, macOS SDK 15.5 and Xcode 14.2 host tools. Point GN to a valid local SDK path. Target x64 and macOS 12.0.

## Apply patches

1. From Chromium src/, apply patches/chromium-macos12-sdk-compat.patch.
2. From Chromium src/, apply patches/brave-stable-profile-directory.patch; it edits the embedded src/brave/build/config.gni.
3. For the Metal build, stop here. For OpenGL, also apply patches/chromium-macos12-opengl-compat.patch from src/, then change to src/brave/ and apply patches/brave-opengl-newtab-backdrop.patch there.

The patch paths are relative to different repositories: Chromium patches apply in src/; Brave patches apply in src/brave/. Apply OpenGL patches only as a pair. Check whether Brave setup scripts overwrite src/brave/build/config.gni after patching.

The patches cover 23 changed source files (6 macOS SDK/build, 1 Brave stable-profile, 14 OpenGL/IOSurface, and 2 OpenGL New Tab backdrop). They are intentionally small: most build effort was upstream source/dependency synchronization, downloading and checking in-source PGO profiles, GN configuration, the macOS 15.5 SDK with Xcode 14.2 host tools, and compiling/linking the original Brave/Chromium tree.

## GN configuration

Generate an x64 ReleaseOfficial output using the source-pinned macOS and V8 PGO profiles and these relevant arguments:

    target_cpu = "x64"
    mac_deployment_target = "12.0"
    mac_min_system_version = "12.0"
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
    init_stack_vars_zero = true
    use_prebuilt_omaha4 = false

The successful 32 GB host used four ThinLTO backend jobs to stay within its memory limit. This is not a universal value. The official configuration also disabled iterator debugging, the Viz debugger, Brave PageGraph WebAPI probes, and IPC fuzzing; enabled zero stack initialization; and kept the source-built updater. Credentials added only to satisfy unavailable local GN assertions were dummy placeholders, never publish real service credentials.

Use Brave's build wrapper to generate and build the brave target. The verified command used its Release/ReleaseOfficial configuration, macOS x64, --skip_signing, and 12 Ninja jobs. Equivalent toolchain, SDK, profiles, and GN args are required; local absolute paths are not portable. The clean official build completed 61,859 steps in about 12h13m on the 32 GB Mac Pro. The later OpenGL and New Tab changes reused that output; the final OpenGL backdrop rebuild completed 22 steps in 5m28s (link 4m42s). A fresh machine will perform the full build.

## Patch contents

- chromium-macos12-sdk-compat.patch (6 files): older-SDK posix_spawn_file_actions_addchdir_np, macOS screen-ID lookup through NSScreen.deviceDescription, guards for macOS 26 HDR/AppKit symbols, and a configurable ThinLTO backend-job limit.
- brave-stable-profile-directory.patch (1 file): use Brave's stable profile directory, not -Development.
- chromium-macos12-opengl-compat.patch (14 files): allow the existing ANGLE CGL backend; expose the OpenGL flag; use Ganesh for explicit OpenGL; scoped GLES2 fallback; restore rectangle IOSurface texture-target capability, IPC propagation, selection and tests.
- brave-opengl-newtab-backdrop.patch (2 files): disable backdrop blur only on New Tab in explicit macOS OpenGL mode to avoid the GeForce 320M corruption.

The code is derived from Chromium and Brave and remains under their upstream licenses. This repository provides modifications only; it does not relicense or vendor their source. See upstream Chromium and Brave licensing at https://github.com/brave/brave-browser/blob/master/LICENSE.
