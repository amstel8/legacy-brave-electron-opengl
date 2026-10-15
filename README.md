# Brave for macOS 12 (Intel, Metal)

An independently built Brave 155 release for Intel Macs running macOS 12 or later. This repository records the build recipe, the small macOS SDK compatibility patches, and the exact released binary. The binary is attached to the GitHub Release, not stored in Git.

**Download:** [v155.1.97.0-macos12-metal](https://github.com/amstel8/brave-macos12/releases/tag/v155.1.97.0-macos12-metal)

- Brave `155.1.97.0`; Chromium `155.0.8059.40`
- Source: Brave tag `v1.97.56` (`b01cdf43be4b4d5559bf7e58229e666e24454f50`)
- Intel x86_64; minimum macOS `12.0`
- Uses ANGLE Metal / Graphite Dawn Metal where supported; this release does not restore OpenGL
- Unpacked app size: approximately 572 MiB

This build is unsigned and not notarized. `is_official_build=true` describes Chromium build optimization settings only; Brave Software did not build, sign, endorse, or notarize this artifact. Proprietary service credentials unavailable to this independent build are placeholders, so services requiring those credentials may not work.

## Install

Download the `.tar.gz` and matching `.sha256` from Releases. Verify the archive before extracting:

```sh
shasum -a 256 -c brave-macos12-x64-155.1.97.0-official.tar.gz.sha256
```

Quit Brave before replacing it. Back up the existing app and the profile directory `~/Library/Application Support/BraveSoftware/Brave-Browser` first. Move the extracted `Brave Browser.app` into `/Applications`. For rollback, restore the old app and its matching profile together; a newer browser may migrate profile data.

## Hardware and validation limits

The release was verified on macOS 12.7.6 with an AMD Radeon RX 6800 XT: ANGLE Metal / GraphiteDawnMetal, GPU compositing, rasterization and video decode were enabled, with zero GPU crashes in diagnostic launches. A GeForce 320M without Metal falls back to software rendering. Do not assume GPU acceleration on non-Metal Macs, OpenCore Legacy Patcher systems, or other untested GPUs. OpenGL compatibility changes are intentionally excluded.

A controlled synthetic layout/rendering comparison measured 3.246 ms mean layout and 53.5–53.6 FPS for this build, versus 3.380 ms and 50.1–53.3 FPS for Brave 150. The workload used 3,500 flex-layout elements and controlled profiles, fonts, viewport and launch order. These results do not predict every site's performance. YouTube Shorts volume-control interaction was not validated.

See [build and patch notes](docs/BUILD.md) and [release notes](docs/RELEASE.md).
