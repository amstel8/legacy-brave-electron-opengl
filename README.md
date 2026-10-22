# Legacy Brave, Electron and OpenGL for macOS 12

Independent Brave **1.97.59 / Chromium 155.0.8059.85** and Electron **45.0.0** builds for Intel Macs on macOS 12. Release assets contain binaries; this repository contains the compatibility patches, SDK declarations and build instructions. Full Chromium/Brave/Electron sources are fetched from their pinned upstream revisions.

## Current Brave release

[**Download Brave 1.97.59 — Metal and automatic OpenGL**](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/v1.97.59-macos12-metal-opengl)

One x86_64 app retains Metal on supported GPUs and automatically selects ANGLE OpenGL when no Metal device exists. Explicit graphics switches are respected. It is not an Intel/Apple Silicon Universal 2 binary. The build targets macOS 12.0+, uses official Release settings, PGO and optimized ThinLTO, and retains the existing stable Brave profile directory.

Validated on a Radeon RX 6800 XT with Metal and an OCLP MacBookPro7,1 with GeForce 320M/OpenGL. No regression was observed against the preceding build in the local layout/animation comparison. The non-Metal test confirmed automatic OpenGL selection, accelerated compositing/rasterization, WebGL1 and the New Tab backdrop workaround. WebGL2 is unsupported on the tested 320M.

The bundle version remains 155.1.97.0 under the existing local build convention; source tag is v1.97.59 and the Chromium engine version is 155.0.8059.85. Read [release notes and installation instructions](docs/RELEASE-1.97.59.md) and [exact build/validation details](docs/UNIFIED-1.97.59.md).

These are unofficial builds without Developer ID signing/notarization. is_official_build=true is an optimization configuration, not endorsement by Brave/Electron. Proprietary service credentials were unavailable and placeholders were used; associated services may not work.

## Electron

[**Electron 45.0.0 / Chromium 156, macOS 12 x64**](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/electron-v45.0.0-macos12-x64) retains Metal and automatic OpenGL selection on non-Metal Macs. The updated Chromium 156 patches restore the removed hardware-GL route and IOSurface capability propagation. Validated on RX 6800 XT with Metal and explicit OpenGL, and on GeForce 320M with automatic OpenGL 3.3/GLES2, accelerated compositing/rasterization and WebGL1. Exact patches, build settings and instructions are in [electron/](electron/); validation coverage is in [release notes](electron/RELEASE.md). The previous 44.9.0 release remains available. Existing Pritunl packages use Electron 44.7.2.

## Earlier Brave releases

- [v155.1.97.0-macos12-metal](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/v155.1.97.0-macos12-metal) — v1.97.56 / Chromium 155.0.8059.40, original Metal baseline.
- [v155.1.97.0-macos12-opengl](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/v155.1.97.0-macos12-opengl) — v1.97.56 with opt-in OpenGL and the New Tab backdrop fix. This older release requires selecting OpenGL manually on non-Metal Macs.

## Source changes and build recipe

The original Brave port modified 23 files in four focused patches. The current release adds four startup/linkage files for automatic backend selection and an optional one-file dependency-sync improvement. Large upstream repositories are intentionally not mirrored here. Electron has its own compatibility patches and SDK preparation recipe.

See [build instructions and patch inventory](docs/BUILD.md), [current unified build](docs/UNIFIED-1.97.59.md), [OpenGL validation history](docs/OPENGL.md), and [original Metal release notes](docs/RELEASE.md). Upstream licenses continue to apply to all derived code and bundled resources.
