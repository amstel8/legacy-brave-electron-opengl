# Brave 1.99.56 / Chromium 157 — macOS 12 Intel

Brave Core **v1.99.56**, Chromium **157.0.8103.50**. x86_64, minimum macOS12.0. Bundle metadata remains157.1.99.0; source patch version is1.99.56.

## Download

`brave-v1.99.56-macos12-x64-metal-opengl.tar.gz` — 302,618,462bytes.

SHA256 `556099117af62f938bc1334678a9800a9aa535da3215de39be4bb7c9c392d0cd`. Matching checksum file attached. Independent third-party build without DeveloperID signing/notarization.

## Changes and build

Updates Brave1.99.55/Chromium157.0.8103.39 to1.99.56/157.0.8103.50. Retains all seven macOS12/Metal/automaticGL compatibility patches, including fullscreen-input and static-image loading workarounds. Official Release, pinnedPGO, optimizedThinLTO/fourbackendjobs/twelvecompilejobs, SDK15.5, stable profile directory retained. Completed2026-11-12 19:55MSK:56193steps in11h38m52.57s, exit0. [Full source recipe](../recipes/brave-1.99.56/README.md).

## Validation

Exact archive framework SHA256 `1be9fe29f467b426fb1023c35e3c9c7b9c43082a0ee8c3a5d1a71b8509a2bb8b` matched the tested candidate. macOS12.7.6 / RadeonRX6800XT: default ANGLEMetal and explicit `--use-angle=gl` ANGLEOpenGL4.1 both passed accelerated compositing/rasterization and WebGL1 readback `[51,102,204,255]`, GLerror0. Runtime Chromium157.0.8103.50 and minimumOS12.0 verified. Separate profiles, no installed browser/profile changes.

**Automatic non-Metal OpenGL3.3 on GeForce320M remains pending for this exact package.** Prior-version tests are not evidence for this binary. OpenGL4.1 above describes the testGPU and is not a minimum requirement. Fullscreen clicks, Avito partial-image behavior, extended stability, media and performance were not revalidated. Feature-status labels alone do not prove WebGL2/WebGPU or media capability.

[Machine-readable evidence](../tests/macos12/brave-1.99.56-validation.json). Previous releases retained. This archive is intended to replace the current Brave download; Electron releases are separate. ScreenCaptureKit system-audio loopback belowmacOS13 remains unavailable. Proprietary service credentials are placeholders, as in earlier releases.
