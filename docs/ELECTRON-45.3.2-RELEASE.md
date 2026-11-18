# Electron 45.3.2 for macOS 12 — Intel, Metal and OpenGL

Electron **45.3.2**, Chromium **156.0.8078.100**, Node **24.22.2**. x86_64, minimum macOS 12.0. Official Release optimization settings, Electron-pinned PGO and optimized ThinLTO. Independent third-party compatibility build, without Developer ID signing or notarization.

## Download

- `electron-v45.3.2-macos12-darwin-x64.zip` — 125,179,129 bytes.
- SHA-256: `00b92e40030bac4525448f8f99a993029360007b63185797a23d17ff7bf622b0`.
- A matching `.sha256` file is attached.

## Changes from 45.3.0

Electron and Chromium are updated; Node remains 24.22.2. Exact revisions are listed in [the recipe](README.md). The macOS 12 compatibility patches, automatic ANGLE OpenGL selection, restored hardware-GL mode and IOSurface texture-target propagation are retained; the 45.2.1 patches applied without porting changes.

This was an Official Release build with Electron PGO, optimized ThinLTO, four linker backend jobs and twelve compile jobs. Build exit 0 completed on 2026-11-14 at 09:47 MSK; the recorded build took 9:09:00.45 for 42,231 steps and packaging took 25.86 s.

## Validation of this exact ZIP

Both runs used the downloaded ZIP on macOS 12.7.6 x86_64 with separate fresh profiles and an AMD Radeon RX 6800 XT:

| Selection | Renderer / Skia backend | Result |
| --- | --- | --- |
| Default | ANGLE Metal | Hardware compositing/rasterization enabled; WebGL1 pixel check passed |
| Explicit `--use-angle=gl` | ANGLE OpenGL 4.1 / GaneshGL | Hardware compositing/rasterization enabled; WebGL1 pixel check passed |

Both runs read `[51,102,204,255]`, GL error 0, and had no child-process exit events. The short helper checks lasted 10 seconds and are not performance or stability tests. Runtime versions, ZIP CRC and minimum OS 12.0 were also verified. [Machine-readable results](https://github.com/amstel8/legacy-brave-electron-opengl/blob/main/electron/validation/45.3.2.json).

**GeForce 320M / automatic OpenGL 3.3-GLES2 validation is pending for 45.3.2.** The MacBook was not used for this release; older results do not validate this ZIP. Extended media, conferencing, performance and stability checks remain pending.

## Compatibility notes

ScreenCaptureKit system-audio loopback is unavailable below macOS 13. Ordinary playback and microphone input are separate. Automatic GL selection detects absence of a Metal device; it does not recover from arbitrary later Metal driver failures. These standalone checks did not replace installed applications or existing profiles.

[Source patches and build instructions](https://github.com/amstel8/legacy-brave-electron-opengl/tree/main/electron). Previous releases remain available. Brave remains the repository's Latest release.
