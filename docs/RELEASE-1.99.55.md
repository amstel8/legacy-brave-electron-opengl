# Brave 1.99.55 / Chromium 157 — macOS 12 Intel

Independent x86_64 compatibility build of Brave Core v1.99.55 / Chromium157.0.8103.39, minimum macOS12.0. Official Release, pinnedPGO, optimizedThinLTO. Metal default; automatic ANGLEOpenGL/Ganesh when no Metal device exists.

## Download

`brave-v1.99.55-macos12-x64-metal-opengl.tar.gz` — 291,646,220 bytes.

SHA256: `e19edefed4a5d41c6cf87e6f9559d479b3beb33f4b218c2f2b616f1c591bdbf8`. Matching checksum file attached.

Bundle metadata reports157.1.99.0; exact source version is BraveCore1.99.55. Unsigned third-party build without DeveloperID/notarization.

## Changes

Updates Chromium156 to157. Retains macOS12 SDK/API guards, stable profile directory, GL hardware mode/IOSurface target propagation/Ganesh/GLES2 collection fallback, automatic non-Metal selection, new-tab backdrop workaround, partial static JPEG/WebP loading workaround and macOS12 native fullscreen input routing. Four OpenGL patch contexts were ported to157 without intended behavior changes. Adds Intel-host RustWASM dependency recovery and current source synchronization recipe.

## Validation of this exact archive

Archive framework was read back and matched the tested/installed candidate SHA256 `391734a9d30345d52a9ebf89b82111532f89397fe8f23c774581cbb4c187dd39`.

| Machine / macOS12.7.6 | Default backend | Result |
| --- | --- | --- |
| RadeonRX6800XT desktop | ANGLEMetal / Graphite | Accelerated compositing/rasterization, WebGL1 pixel readback passed |
| OCLP MacBookPro7,1 / GeForce320M | Automatic ANGLEOpenGL3.3 / Ganesh | Accelerated compositing/rasterization, WebGL1 pixel readback passed |

Both returned `[51,102,204,255]`, GLerror0, and Chromium157.0.8103.39. Separate test profiles, no graphics switches. No claim of WebGL2/WebGPU capability is made from feature-status labels; only WebGL1 rendering was exercised. These are short launch/GPU checks, not a performance or stability benchmark. Fullscreen hit testing and Avito progressive-image behavior were not revalidated for this version. Runtime feature labels do not prove media acceleration.

[Machine-readable evidence](https://github.com/amstel8/legacy-brave-electron-opengl/blob/main/tests/macos12/brave-1.99.55-validation.json). [Full patch inventory and build instructions](https://github.com/amstel8/legacy-brave-electron-opengl/tree/main/recipes/brave-1.99.55).

Stable profile path remains BraveSoftware/Brave-Browser. Existing profile backups should be retained when upgrading across Chromium majors. ScreenCaptureKit system-audio loopback belowmacOS13 remains unavailable. Previous release archives remain available.
