# Electron 45.4.1 for macOS 12 — Intel, Metal and OpenGL

Electron **45.4.1**, Chromium **156.0.8078.100**, Node **24.22.3**. Minimum macOS 12.0, x86_64. Independent compatibility build, unsigned and not notarized.

## Download

`electron-v45.4.1-macos12-darwin-x64.zip` — 125,161,715 bytes.

SHA-256: `d743a48f98215046a5fe6f36dd23dd5feee12ff0f97b85d25c35ed2b538d0231`. Matching checksum file attached.

## Build

Updated from Electron 45.3.4 to upstream tag v45.4.1, commit `deaded07eebdfe9a3737884933b1acbe65971f64`. Chromium and Node versions are unchanged. Existing macOS 12, Metal and automatic OpenGL compatibility patches are retained. Official Release settings, Electron-pinned PGO and optimized ThinLTO. Build completed successfully on 2026-11-21.

## Validation of this exact ZIP

On macOS 12.7.6 with Radeon RX 6800 XT, separate fresh profiles passed default Metal and explicit `--use-angle=gl` (OpenGL 4.1) checks. Both enabled hardware compositing/rasterization, returned WebGL1 pixels `[51,102,204,255]` with GL error 0, and recorded no child-process exit events during the short checks. Runtime versions, ZIP CRC, SHA-256 and Info.plist minimum OS 12.0 were verified.

[Machine-readable evidence](../electron/validation/45.4.1.json). Automatic OpenGL 3.3/GLES2 on GeForce 320M remains pending for this exact ZIP. Extended media, conferencing, performance and stability checks remain pending. These tests did not change installed applications or user profiles.

ScreenCaptureKit system audio requires macOS 13. Automatic OpenGL selection detects absence of a Metal device; later Metal driver failures are not covered.

[Source patches and build instructions](https://github.com/amstel8/legacy-brave-electron-opengl/tree/main/electron). Brave remains the repository's Latest release.
