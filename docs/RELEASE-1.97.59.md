# Brave 1.97.59 for macOS 12 — Intel, Metal and automatic OpenGL

Based on Brave Core **v1.97.59** and Chromium **155.0.8059.85**. One x86_64 package supports Metal GPUs and automatically selects ANGLE OpenGL when no Metal device exists. This is an independent community build, not a Brave Software release. Minimum macOS: **12.0**. No arm64/Universal 2 binary is included.

## Download and installation

Download `brave-v1.97.59-macos12-x64-metal-opengl.tar.gz` and its `.sha256` asset. Extract the archive, quit Brave, and replace Brave Browser.app in Applications. Keep the existing profile; do not remove BraveSoftware/Brave-Browser from Application Support. macOS may require manually opening the app because it is not Developer ID signed or notarized. Install future versions of this port from its own releases; upstream auto-updates are not the distribution mechanism for these compatibility builds.

SHA-256: `3edb6e6c88e84490cf4474f1d74652de236d98e43d9efcaa204e140e15b85599`.

## Changes

- Updated Brave v1.97.56 → **v1.97.59**, Chromium 155.0.8059.40 → **155.0.8059.85**.
- Combined Metal and the legacy ANGLE/CGL/Ganesh rendering path in one package.
- Added automatic OpenGL selection if MTLCreateSystemDefaultDevice() returns no device. Explicit --use-angle, --use-gl and --disable-gpu choices are respected. This detects absence of Metal; it does not recover from every later Metal driver failure.
- Retained the macOS 12 SDK/API compatibility fixes, stable profile directory, GLES2 compatibility and IOSurface rectangle texture handling.
- Retained the OpenGL-only New Tab backdrop workaround for legacy GPU background corruption.
- Official Release configuration, source-pinned PGO and optimized ThinLTO; no debug/DCHECK/Viz debugger overhead.

The local build convention still reports **155.1.97.0** as the bundle/application version. It is built from **v1.97.59**, and the Chromium engine reports **155.0.8059.85**. Exact source revisions and binary hashes are documented in UNIFIED-1.97.59.md.

## Validation

- **Metal:** macOS 12.7.6, AMD Radeon RX 6800 XT, ANGLE Metal / GraphiteDawnMetal. Hardware compositing/rasterization enabled, zero GPU crashes. Compared to the previous build in six warmed layout samples per version and two animation runs per version: 3.205 → 3.180 ms layout, 51.7 → 53.3 synthetic FPS. These small differences are within ordinary variation; no regression was observed in the tested workloads.
- **Automatic OpenGL:** MacBookPro7,1, NVIDIA GeForce 320M, OCLP macOS 12.7.6. A fresh profile was launched without forcing GL. The GPU child selected ANGLE OpenGL 3.3 / Ganesh; hardware compositing/rasterization stayed enabled, GPU crashes 0. WebGL1 clear/readPixels returned [51,102,204,255], GL error 0. The New Tab workaround was active and native-window captures showed the expected background.
- Installed on both machines with full application/profile backups. Cookie counts were preserved after relaunch (2740 on the Metal Mac, 397 on the MacBook). No profiles or user data are distributed here.

## Limits

WebGL2 is unsupported on the tested GeForce 320M; WebGPU/video feature flags alone are not functional validation. GPU capabilities depend on the driver/OCLP installation. Upstream may still display its macOS support warning. Proprietary Brave service credentials were unavailable and placeholders are used, so associated services may not work. Wider site, video, conferencing and long-duration stability testing is still needed.

Source patches and build/validation details: [UNIFIED-1.97.59.md](https://github.com/amstel8/legacy-brave-electron-opengl/blob/main/docs/UNIFIED-1.97.59.md).
