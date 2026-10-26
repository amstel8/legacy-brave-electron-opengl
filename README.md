# Legacy Brave, Electron and OpenGL for macOS 12

Independent Brave **1.98.60-r2 / Chromium 156.0.8078.48** and Electron **45.0.0** builds for Intel Macs on macOS 12. Release assets contain binaries; this repository contains the compatibility patches, SDK declarations and build instructions. Full Chromium/Brave/Electron sources are fetched from their pinned upstream revisions.

## Current Brave release

[**Download Brave 1.98.60-r2 — fullscreen input fix, Metal and automatic OpenGL**](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/v1.98.60-r2-macos12-metal-opengl)

One x86_64 app retains Metal on supported GPUs and automatically selects ANGLE OpenGL when no Metal device exists. Explicit graphics switches are respected. It is not an Intel/Apple Silicon Universal 2 binary. The build targets macOS 12.0+, uses official Release settings, PGO and optimized ThinLTO, and retains the existing stable Brave profile directory.

Revision 2 was installed and checked on an OCLP MacBookPro7,1 with GeForce 320M. It fixes fullscreen mouse input and passed 40/40 native clicks and 40/40 pre-click hovers. The base revision was also installed and launched on a Radeon RX 6800 XT desktop; the exact r2 binary has not been separately validated there. The new Chromium 156 build includes an OpenGL-only workaround that waits for complete static JPEG/WebP downloads before displaying them, intended to avoid image-loading flicker. Visual confirmation on Avito, detailed GPU checks and performance comparison of this exact build remain pending; prior-version validation is documented separately.

The bundle version is **156.1.98.0**; the source tag is **v1.98.60** and Chromium is **156.0.8078.48**. Package revision is **r2**. Read [release notes and installation instructions](docs/RELEASE-1.98.60-r2.md) and the [version-specific patch/build recipe](recipes/brave-1.98.60/README.md).

These are unofficial builds without Developer ID signing/notarization. is_official_build=true is an optimization configuration, not endorsement by Brave/Electron. Proprietary service credentials were unavailable and placeholders were used; associated services may not work.

## macOS 12 fullscreen input fix

The r2 [fullscreen input patch](docs/FULLSCREEN-INPUT-MACOS12.md) fixes a native toolbar layer intercepting the top of web pages on Monterey. It passed 40/40 native clicks and 40/40 pre-click hover checks and was installed and checked on the non-Metal MacBook, including Avito's business menu. The patch, regression fixture and measured results are included in the source recipe; the r2 download above includes the fix.

## Electron

[**Electron 45.0.0 / Chromium 156, macOS 12 x64**](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/electron-v45.0.0-macos12-x64) retains Metal and automatic OpenGL selection on non-Metal Macs. The updated Chromium 156 patches restore the removed hardware-GL route and IOSurface capability propagation. Validated on RX 6800 XT with Metal and explicit OpenGL, and on GeForce 320M with automatic OpenGL 3.3/GLES2, accelerated compositing/rasterization and WebGL1. Exact patches, build settings and instructions are in [electron/](electron/); validation coverage is in [release notes](electron/RELEASE.md). The previous 44.9.0 release remains available.

## Earlier Brave releases

- [v1.98.60-macos12-metal-opengl](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/v1.98.60-macos12-metal-opengl) — first Chromium 156 package, before the fullscreen input fix.

- [v1.97.59-macos12-metal-opengl](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/v1.97.59-macos12-metal-opengl) — Chromium 155, previous Metal/automatic OpenGL build with detailed GPU and synthetic performance validation.

- [v155.1.97.0-macos12-metal](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/v155.1.97.0-macos12-metal) — v1.97.56 / Chromium 155.0.8059.40, original Metal baseline.
- [v155.1.97.0-macos12-opengl](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/v155.1.97.0-macos12-opengl) — v1.97.56 with opt-in OpenGL and the New Tab backdrop fix. This older release requires selecting OpenGL manually on non-Metal Macs.

## Source changes and build recipe

The current Chromium 156 patches, application order, pinned revisions and image-loading workaround are in [recipes/brave-1.98.60/](recipes/brave-1.98.60/README.md). Top-level `patches/` and [BUILD.md](docs/BUILD.md) retain the earlier Chromium 155 recipe; use the version-specific recipe for this release. Large upstream repositories are fetched from their pinned revisions. Electron has its own compatibility patches and SDK preparation recipe.

See the [current build details](docs/UNIFIED-1.98.60.md), [previous build validation](docs/UNIFIED-1.97.59.md) and [OpenGL validation history](docs/OPENGL.md). Upstream licenses continue to apply to all derived code and bundled resources.
