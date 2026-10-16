# Brave and Electron for macOS 12 (Intel)

Independent Brave 155.1.97.0 builds for Intel Macs on macOS 12. The binary is distributed as a GitHub Release asset; this repository contains the build recipe and source patches, not a Chromium source mirror.

## Releases

- [Metal build, v155.1.97.0-macos12-metal](https://github.com/amstel8/brave-macos12/releases/tag/v155.1.97.0-macos12-metal) — Metal path, verified on an AMD Radeon RX 6800 XT.
- [OpenGL build, v155.1.97.0-macos12-opengl](https://github.com/amstel8/brave-macos12/releases/tag/v155.1.97.0-macos12-opengl); ANGLE OpenGL/GaneshGL was verified on an NVIDIA GeForce 320M running macOS 12.7.6.

Both target x86_64, require macOS 12.0 or later, use Brave v1.97.56 and Chromium 155.0.8059.40, and were built with PGO and optimized ThinLTO. Both are unsigned and not notarized. is_official_build=true describes Chromium build configuration only; neither binary was built, signed, endorsed, or notarized by Brave Software. Credentials needed for proprietary services were unavailable and placeholders were used; those services may not work.

The OpenGL build leaves Metal as the default. On a non-Metal Mac, select OpenGL at brave://flags/#use-angle and restart. The old GPU path is GLES2 compatible; WebGL 1 is verified, while WebGL 2 is unsupported on the tested GeForce 320M. For that OpenGL mode, the New Tab page turns off backdrop blur to avoid a verified legacy rendering defect; the background, widgets, GPU compositing, and rasterization remain enabled.

## Why this repository is small

It records 23 modified source files as four focused patches: 6 Chromium macOS SDK/build files, 1 Brave profile-path adjustment, 14 Chromium OpenGL/IOSurface files, and 2 Brave New Tab backdrop files. Chromium and Brave themselves are fetched from their upstream pinned revisions during setup; mirroring their many gigabytes of source would obscure these changes and duplicate their licensing and release process.

See [build instructions and patch inventory](docs/BUILD.md), [OpenGL notes and validation](docs/OPENGL.md), and [Metal release notes](docs/RELEASE.md).

## Electron

[Electron 44.7.2 / Chromium 152 macOS 12 x64](https://github.com/amstel8/brave-macos12/releases/tag/electron-v44.7.2-macos12-x64) is an experimental compatibility build with automatic OpenGL selection when no Metal device exists. Its independent patches, exact GN configuration, SDK compatibility declarations and build recipe are in [electron/](electron/). Node-mode startup and initial Pritunl GUI startup on a non-Metal MacBookPro7,1 have been verified; its GPU child automatically uses OpenGL. Extended rendering/GPU stability and VPN checks remain pending.
