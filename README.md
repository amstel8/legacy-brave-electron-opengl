# Legacy Brave, Electron and OpenGL for macOS 12

Independent Brave 155.1.97.0 and Electron 44.7.2 builds for Intel Macs on macOS 12, with Metal support and ANGLE OpenGL compatibility for older GPUs. Release assets contain the binaries; this repository contains source patches, SDK compatibility declarations and build instructions.

## Next Brave build: 1.97.59 with automatic OpenGL

The macOS 12 x64 recipe is being updated to Brave v1.97.59 / Chromium 155.0.8059.85. A single package retains Metal on supported GPUs and selects ANGLE OpenGL when no Metal device exists. This means one Intel binary with two rendering paths, not a Universal 2 (Intel + Apple Silicon) binary. Previously published releases remain available below; the new build is not yet a validated release.

See [the unified build notes](docs/UNIFIED-1.97.59.md). The additional [startup patch](patches/chromium-macos12-auto-opengl.patch) is applied after the existing compatibility patches.

## Releases

- [Electron 44.7.2, macOS 12 x64](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/electron-v44.7.2-macos12-x64) — automatically selects OpenGL when no Metal device exists.
- [Metal build, v155.1.97.0-macos12-metal](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/v155.1.97.0-macos12-metal) — Metal path, verified on an AMD Radeon RX 6800 XT.
- [OpenGL build, v155.1.97.0-macos12-opengl](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/v155.1.97.0-macos12-opengl); ANGLE OpenGL/GaneshGL was verified on an NVIDIA GeForce 320M running macOS 12.7.6.

Both Brave builds target x86_64, require macOS 12.0 or later, use Brave v1.97.56 and Chromium 155.0.8059.40, and were built with PGO and optimized ThinLTO. Both are unsigned and not notarized. is_official_build=true describes Chromium build configuration only; neither binary was built, signed, endorsed, or notarized by Brave Software. Credentials needed for proprietary services were unavailable and placeholders were used; those services may not work.

The OpenGL build leaves Metal as the default. On a non-Metal Mac, select OpenGL at brave://flags/#use-angle and restart. The old GPU path is GLES2 compatible; WebGL 1 is verified, while WebGL 2 is unsupported on the tested GeForce 320M. For that OpenGL mode, the New Tab page turns off backdrop blur to avoid a verified legacy rendering defect; the background, widgets, GPU compositing, and rasterization remain enabled.

## Why this repository is small

The Brave portion records 23 modified source files as four focused patches: 6 Chromium macOS SDK/build files, 1 Brave profile-path adjustment, 14 Chromium OpenGL/IOSurface files, and 2 Brave New Tab backdrop files. Chromium and Brave themselves are fetched from their upstream pinned revisions during setup; mirroring their many gigabytes of source would obscure these changes and duplicate their licensing and release process.

Electron has its own patches covering 12 source files plus SDK compatibility declarations; see [electron/](electron/).

See [build instructions and patch inventory](docs/BUILD.md), [OpenGL notes and validation](docs/OPENGL.md), and [Metal release notes](docs/RELEASE.md).

## Electron

[Electron 44.7.2 / Chromium 152 macOS 12 x64](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/electron-v44.7.2-macos12-x64) is an experimental compatibility build with automatic OpenGL selection when no Metal device exists. Its independent patches, exact GN configuration, SDK compatibility declarations and build recipe are in [electron/](electron/). Node-mode startup and initial Pritunl GUI startup on a non-Metal MacBookPro7,1 have been verified; its GPU child automatically uses OpenGL. Extended rendering/GPU stability and VPN checks remain pending.
