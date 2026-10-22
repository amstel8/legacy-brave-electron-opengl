# Electron 45.0.0 for macOS 12 — Intel, Metal and OpenGL

Electron **45.0.0**, Chromium **156.0.8078.48**, Node **24.22.0**. x86_64, minimum macOS 12.0. Official Release optimization settings, Electron-pinned PGO and optimized ThinLTO. Independent third-party compatibility build, without Developer ID signing or notarization.

## Download

- `electron-v45.0.0-macos12-darwin-x64.zip` — 125,049,171 bytes.
- SHA-256: `2807aaa78ef959402e62cb5cc348d37809d0a77470c2b1883a70ccd6ae0fd1ed`.
- A matching `.sha256` file is attached.

## Changes from 44.9.0

- Update Electron 44.9.0 / Chromium 152 to Electron 45.0.0 / Chromium 156.
- Retain Metal on supported GPUs and automatic ANGLE OpenGL selection when no Metal device exists; explicit graphics options are respected.
- Restore Chromium 156's removed macOS hardware-GL route only when ANGLE GL is selected. Metal retains its upstream GPU-mode policy.
- Restore the IOSurface texture-target contract across the shared-image factory, IPC and client for CGL rectangle textures.
- Permit GLES2 fallback for legacy GPU collection while retaining strict WebGL2/ES3 context requests.
- Guard macOS 26 APIs absent from the prepared SDK, including CALayer HDR properties.
- Keep PGO/ThinLTO optimization and limit linker backend concurrency for build-host memory.

## Validation of this exact ZIP

All checks below used the exact published ZIP on macOS 12.7.6, with separate test profiles.

| Hardware | Selection | Renderer / Skia backend | Result |
| --- | --- | --- | --- |
| Radeon RX 6800 XT | Default | ANGLE Metal / GraphiteDawnMetal | Hardware compositing/rasterization enabled; WebGL1 passed |
| Radeon RX 6800 XT | Explicit `--use-angle=gl` | ANGLE OpenGL 4.1 / GaneshGL | Hardware compositing/rasterization enabled; WebGL1 passed |
| **GeForce 320M — OCLP MacBookPro7,1** | **Automatic, no graphics switches** | **ANGLE OpenGL 3.3 / GLES2 / GaneshGL** | **Hardware compositing/rasterization enabled; WebGL1 passed; WebGL2 correctly unavailable** |

All three runs read back `[51,102,204,255]` with GL error 0; no child-process exit events were recorded during these short checks. Runtime versions were Electron 45.0.0, Chromium 156.0.8078.48 and Node 24.22.0. [Machine-readable results](https://github.com/amstel8/legacy-brave-electron-opengl/blob/main/electron/validation/45.0.0.json).

**GeForce 320M validation completed on 2026-10-23.** Automatic OpenGL selection and GLES2 operation are verified on this non-Metal MacBook. The OpenGL 4.1 result above belongs to the RX 6800 XT; it is not a minimum requirement. Extended media, conferencing, performance and stability checks remain pending. OpenGL support does not imply WebGL2/WebGPU capability on old hardware.

## Compatibility notes

ScreenCaptureKit system-audio loopback is unavailable below macOS 13. Ordinary playback and microphone input are separate. The automatic GL decision detects absence of a Metal device; it does not recover from arbitrary later Metal driver failures. No installed apps or user profiles were replaced during these standalone checks. Existing Pritunl packages continue using Electron 44.7.2.

[Source patches and build instructions](https://github.com/amstel8/legacy-brave-electron-opengl/tree/main/electron). Previous releases remain available; Brave remains the repository's Latest release.
