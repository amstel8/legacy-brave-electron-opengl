# Electron 45.1.0 for macOS 12 — Intel, Metal and OpenGL

Electron **45.1.0**, Chromium **156.0.8078.49**, Node **24.22.1**. x86_64, minimum macOS 12.0. Official Release optimization settings, Electron-pinned PGO and optimized ThinLTO. Independent third-party compatibility build, without Developer ID signing or notarization.

## Download

- `electron-v45.1.0-macos12-darwin-x64.zip` — 125,144,840 bytes.
- SHA-256: `fc813a0718e253f730c8b3c68225637b9d938b46910106add56f25c21d0c474f`.
- A matching `.sha256` file is attached.

## Changes from 45.0.0

Update Electron, Chromium and Node to the pinned versions above. Retain our macOS 12 compatibility patches, automatic ANGLE OpenGL selection when no Metal device exists, restored hardware-GL mode and IOSurface texture-target propagation. Metal-capable Macs retain the upstream default; explicit graphics switches are respected. The compatibility patches applied without source changes for this update.

Official Release, hash-verified Electron PGO, optimized ThinLTO, four linker backend jobs and twelve compile jobs. Compilation completed on 2026-10-29: 42,464 steps in 9h02m09s, followed by 28s ZIP packaging. Existing output was reused; these are this update's build timings.

## Validation of this exact ZIP

Both runs used the downloaded ZIP, verified against the build-host SHA-256, on macOS 12.7.6 with separate test profiles.

| Hardware | Selection | Renderer / Skia backend | Result |
| --- | --- | --- | --- |
| Radeon RX 6800 XT | Default | ANGLE Metal / GraphiteDawnMetal | Hardware compositing/rasterization enabled; WebGL1 pixel check passed |
| Radeon RX 6800 XT | Explicit `--use-angle=gl` | ANGLE OpenGL 4.1 / GaneshGL | Hardware compositing/rasterization enabled; WebGL1 pixel check passed |

Both runs read back `[51,102,204,255]`, GL error 0, without child-process exit events during these short checks. A separate WebGL2 canvas returned a context on this GPU; WebGL2 rendering itself was not tested. Runtime versions matched Electron 45.1.0, Chromium 156.0.8078.49 and Node 24.22.1; bundle minimum OS was 12.0. ZIP CRC integrity passed. [Machine-readable results](https://github.com/amstel8/legacy-brave-electron-opengl/blob/main/electron/validation/45.1.0.json).

**Non-Metal GeForce 320M / automatic OpenGL 3.3-GLES2 validation is pending for 45.1.0.** The MacBook was unreachable during this release's validation. The previous 45.0.0 ZIP passed that hardware check; those results do not validate this ZIP. OpenGL 4.1 above describes the RX 6800 XT, not a minimum requirement. OpenGL support does not imply WebGL2/WebGPU capability on older hardware. Extended media, conferencing, performance and stability checks remain pending.

## Compatibility notes

ScreenCaptureKit system-audio loopback is unavailable below macOS 13. Ordinary playback and microphone input are separate. Automatic GL selection detects absence of a Metal device; it does not recover from arbitrary later Metal driver failures. These standalone checks did not replace installed apps or existing profiles.

[Source patches and build instructions](https://github.com/amstel8/legacy-brave-electron-opengl/tree/main/electron). [Previous 45.0.0 release](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/electron-v45.0.0-macos12-x64). Brave remains the repository's Latest release.
