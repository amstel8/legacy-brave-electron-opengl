# Electron 45.2.3 validation evidence

Electron 45.2.3 for macOS 12 is pinned to `d0a18d02058b21ff292e25d5f53f00bd120f2f61`; Chromium is `fb096c0011f9d50f0a264a9376420cdea9c421e3`. The archive is 125,207,097 bytes with SHA-256 `075b57a0c7e86f85766b3675ecfb87445cd327d0b4909d8af82a5ba1a3293bcc`.

On macOS 12.7.6 x86_64 with Radeon RX 6800 XT, separate profiles passed the 10-second GUI/WebGL1 helper with default Metal and explicit `--use-angle=gl`. Both produced `[51,102,204,255]`, GL error 0, no child-process exit events, and enabled GPU compositing/rasterization. The runtime reported Electron 45.2.3, Chromium 156.0.8078.80 and Node 24.22.2; ZIP CRC and minimum macOS 12.0 passed.

GeForce 320M automatic OpenGL 3.3/GLES2 remains pending for this exact ZIP. These are short functional checks, not performance, stability, media or conferencing validation. Full machine-readable evidence is in [electron/validation/45.2.3.json](../electron/validation/45.2.3.json).
