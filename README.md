# Legacy Brave, Electron and OpenGL for macOS 12

Independent Brave **1.99.55 / Chromium 157.0.8103.39** and Electron **45.3.0** builds for Intel Macs on macOS 12. Release assets contain binaries; this repository contains the compatibility patches, SDK declarations and build instructions. Full Chromium/Brave/Electron sources are fetched from their pinned upstream revisions.

## Current Brave release

[**Download Brave 1.99.55 / Chromium 157 — Metal and automatic OpenGL**](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/v1.99.55-macos12-metal-opengl).

One x86_64 app targets macOS 12.0+ with Official Release, PGO and optimized ThinLTO. This exact archive passed short macOS 12.7.6 checks on RX 6800 XT with default Metal and GeForce 320M OCLP with automatic OpenGL 3.3: accelerated compositing/rasterization and WebGL1 pixel readback. Stable profile directory and existing compatibility patches are retained. It is an Intel binary, not Universal 2.

Bundle version **157.1.99.0**, source Brave Core **v1.99.55**, Chromium **157.0.8103.39**. See [release notes](docs/RELEASE-1.99.55.md), [validation evidence](tests/macos12/brave-1.99.55-validation.json) and [all source patches/build recipe](recipes/brave-1.99.55/README.md).

The macOS 12 [fullscreen input workaround](docs/FULLSCREEN-INPUT-MACOS12.md) and legacy-GL partial static-image workaround remain included. Fullscreen clicks, Avito image behavior, performance and extended stability were not revalidated for this version; earlier measurements apply only to their original binaries.

These are unofficial builds without Developer ID signing/notarization. is_official_build=true selects optimization settings, not endorsement by Brave/Electron. Proprietary service credentials were unavailable and placeholders were used; associated services may not work.

## Electron

[**Electron 45.3.0 / Chromium 156, macOS 12 x64**](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/electron-v45.3.0-macos12-x64) includes Node 24.22.2 and retains Metal plus automatic OpenGL selection on non-Metal Macs. This ZIP passed macOS 12.7.6 checks on RX 6800 XT with default Metal and explicit OpenGL, accelerated compositing/rasterization and WebGL1 pixel readback. **Automatic OpenGL 3.3/GLES2 on GeForce 320M remains pending for 45.3.0**; older release results do not validate this ZIP. Exact patches, build instructions and current validation coverage are in [electron/](electron/) and [release notes](electron/RELEASE.md). Earlier releases remain available.

## Earlier Brave releases

- [1.98.60-r2](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/v1.98.60-r2-macos12-metal-opengl) — Chromium 156 with the native fullscreen input fix.

- [v1.98.60-macos12-metal-opengl](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/v1.98.60-macos12-metal-opengl) — first Chromium 156 package, before the fullscreen input fix.

- [v1.97.59-macos12-metal-opengl](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/v1.97.59-macos12-metal-opengl) — Chromium 155, previous Metal/automatic OpenGL build with detailed GPU and synthetic performance validation.

- [v155.1.97.0-macos12-metal](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/v155.1.97.0-macos12-metal) — v1.97.56 / Chromium 155.0.8059.40, original Metal baseline.
- [v155.1.97.0-macos12-opengl](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/v155.1.97.0-macos12-opengl) — v1.97.56 with opt-in OpenGL and the New Tab backdrop fix. This older release requires selecting OpenGL manually on non-Metal Macs.

## Source changes and build recipe

The previous Chromium 156 patches, application order, pinned revisions and image-loading workaround are in [recipes/brave-1.98.60/](recipes/brave-1.98.60/README.md). Top-level `patches/` and [BUILD.md](docs/BUILD.md) retain the earlier Chromium 155 recipe; use [the Chromium 157 recipe](recipes/brave-1.99.55/README.md) for the current release. Large upstream repositories are fetched from their pinned revisions. Electron has its own compatibility patches and SDK preparation recipe.

See the [previous Chromium 156 build details](docs/UNIFIED-1.98.60.md), [previous build validation](docs/UNIFIED-1.97.59.md) and [OpenGL validation history](docs/OPENGL.md). Upstream licenses continue to apply to all derived code and bundled resources.
