# Brave 1.98.60 for macOS 12 — Intel, Metal and automatic OpenGL

Based on Brave Core **v1.98.60** and Chromium **156.0.8078.48**. One x86_64 package uses Metal on supported Macs and automatically selects ANGLE OpenGL when no Metal device exists. Minimum macOS: **12.0**. This is an independent community build, not a Brave Software release. It does not include arm64/Universal 2 binaries.

## Download and installation

Download `brave-v1.98.60-macos12-x64-metal-opengl.tar.gz` and its `.sha256` asset. Verify the checksum, extract, quit Brave and replace Brave Browser.app in Applications. Retain the existing `BraveSoftware/Brave-Browser` profile in Application Support. These compatibility builds are distributed through this repository's releases; they are not Developer ID signed or notarized, so macOS may require manually opening the app.

Archive SHA-256: `aaedb01e401c701452c26040800938a5d25e9e2fa5e6982c1e42c49c9898e8f7`.

Archive size: **300,765,366 bytes**. Framework SHA-256: `696e583e6654830c40b46b8180c4916856ef9d0b991f40763da252915a026cff`. The framework read back from this archive matches the build installed on both test Macs.

## Changes

- Updated Brave **1.97.59 → 1.98.60** and Chromium **155.0.8059.85 → 156.0.8078.48**.
- Ported macOS 12 SDK/API guards to Chromium 156, including the newer native-window Glass code.
- Ported the legacy ANGLE/CGL/Ganesh rendering route, GLES2 GPU capability collection fallback and IOSurface texture-target propagation. Explicit WebGL2 requirements remain unchanged.
- Retained Metal, automatic GL selection when Metal is absent, explicit graphics-switch handling, the stable profile directory and the OpenGL-only New Tab backdrop workaround.
- Added an **OpenGL-only static image-loading workaround**: incomplete JPEG/WebP images wait until fully downloaded before appearing. This is intended to address reported Avito image flicker during loading. It removes progressive previews for those images; it is **not yet visually confirmed to resolve the reported bug**. Animated images, other formats and Metal are excluded.
- Official Release configuration with source-pinned PGO and optimized ThinLTO, without debug/component/DCHECK/Viz debugger overhead.

The application/bundle reports **156.1.98.0**, although its source is pinned to **v1.98.60**. The local version generation still omits the source patch number. No version-only rebuild or binary metadata alteration was performed.

## Checks completed for this build

- Build succeeded: **61,090 steps in 11h03m03s**, exit 0.
- Installed and launched on the macOS 12.7.6 Radeon RX 6800 XT desktop and OCLP MacBookPro7,1 / GeForce 320M.
- MacBook GPU process automatically selected `--use-angle=gl` without forcing GL on the browser command line.
- Installed framework hashes match on both machines and match the framework in this archive. Full old-app/profile backups were created before installation; the stable profile directory was preserved.

Detailed GPU feature reports, WebGL pixel checks, performance comparisons, Avito visual verification and extended stability checks **remain pending for this exact build**. Previous Brave/Electron validation is documented separately and should not be treated as validation of this binary.

## Limits

GPU capability depends on the hardware, driver and OCLP installation. WebGL2 is unsupported on the previously tested GeForce 320M; OpenGL support alone does not provide WebGL2/WebGPU. Proprietary Brave service credentials were unavailable and placeholders are used, so associated services may not work. Upstream may still display its macOS support warning.

Source patches and build details: [Chromium 156 recipe](https://github.com/amstel8/legacy-brave-electron-opengl/tree/main/recipes/brave-1.98.60), [exact inputs and build/installation evidence](https://github.com/amstel8/legacy-brave-electron-opengl/blob/main/docs/UNIFIED-1.98.60.md).
