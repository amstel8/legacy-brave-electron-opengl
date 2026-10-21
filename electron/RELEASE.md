# Electron 44.9.0 for macOS 12 — Intel, Metal and automatic OpenGL

Electron v44.9.0 (`fd148b9908b83c8dc09924e45e6df44b83b6bfe7`), Chromium 152.0.7977.167 (`dd78960ccd8a03a2fe1f629543d27783885b78e9`), Node 24.22.0. Deployment minimum macOS 12.0, x86_64 only. Official Release configuration with Electron-pinned PGO and optimized ThinLTO; Xcode 14.2 host tools and prepared SDK 15.5.

Archive: `electron-v44.9.0-macos12-darwin-x64.zip`. SHA-256: `7e0be42f00e066d746bb7ab0958ecbe99fa94fb5df97e346b408cc8ae58837e2`.

Validated the actual macOS 12 runtime versions, Metal GUI/WebGL1 on Radeon RX 6800 XT, and automatic OpenGL GUI/WebGL1 on the non-Metal GeForce 320M MacBook. Hardware compositing and rasterization were enabled. Explicit GPU switches remain respected. OpenGL uses Ganesh and the existing GLES2/IOSurface compatibility path. It detects absence of a Metal device, not every later Metal driver crash.

Independent third-party compatibility release, without Developer ID signing/notarization. WebGL2 is unsupported on the tested 320M. ScreenCaptureKit system-audio capture below macOS 13 is unavailable. Wider application, media, conferencing and long-duration testing remain pending. No existing application or user profile was replaced by these standalone runtime checks.

Patch and build recipe: https://github.com/amstel8/legacy-brave-electron-opengl/tree/main/electron . The previous 44.7.2 release remains available.
