# Brave 1.98.60 / Chromium 156: macOS 12 Intel build recipe

Status: build completed successfully on 2026-10-25 and installed on both the Metal desktop and non-Metal MacBook. Both browsers started; the MacBook GPU process automatically selected ANGLE GL. Detailed GPU, performance and Avito flicker validation of this version remains pending.

## Pinned inputs

- Brave Core v1.98.60: `52db4b25c0aa3038e9a1c6021428b136cc3cb5fc`.
- Chromium 156.0.8078.48: `d0c02bfad08ec92a6ffcf989e53cd995e6381a4c`.
- x86_64, macOS 12.0 deployment/plist minimum, prepared private SDK 15.5 and Xcode 14.2 host.
- Official Release, source-pinned Chrome and V8 PGO, optimized ThinLTO with four backend jobs, twelve local tasks, no component/debug/DCHECK/Viz-debug overhead.
- The worker exported `ignore_patch_version_number=false`, but the resulting bundle still reports `156.1.98.0` (CFBundleVersion `198.0`). This release is pinned to source v1.98.60; do not infer the source patch version from bundle metadata. Stable profile-directory patch remains applied.

## Patch order

After Brave's source synchronization and upstream patch series:

1. `chromium-macos12-sdk-compat.patch` in Chromium: older SDK guards, macOS 26 Glass/HDR guards, audio loopback guard and ThinLTO job cap. Glass guards are ported to the Chromium 156 implementation.
2. `brave-stable-profile-directory.patch` in Chromium.
3. `chromium-macos12-opengl-compat.patch` in Chromium: Chromium 156 GL mode, allowlist, Ganesh, GLES2 GPU collection fallback and IOSurface factory/IPC/client propagation. Based on the same Chromium version validated with Electron 45, plus Brave's backend selection UI.
4. `brave-opengl-newtab-backdrop.patch` in Brave Core.
5. `chromium-macos12-auto-opengl.patch` in Chromium, or generate it with `add-brave-auto-opengl.py`; do not apply both.
6. `chromium-macos12-opengl-static-image-loading.patch` in Chromium, described below.
7. `chromium-macos12-fullscreen-input.patch` in Chromium: post-release macOS 12 native fullscreen input workaround. See [reproduction, build and native validation](../../docs/FULLSCREEN-INPUT-MACOS12.md). This additional patch is absent from the original published 1.98.60 archive.

The optional `brave-sync-exact-revision.patch` applies in Brave Core before sync and resolves an already fetched Chromium tag to its SHA. For the build workspace, `prefetch-local-deps.py` reuses exact dependency commits from the existing Electron checkout before gclient; set `GIT_CACHE_PATH` to the shared cache. This avoids fetching full upstream dependency histories when the same Chromium 156 objects are already local. The helper expects the gclient revinfo JSON in the host logs directory; it is an operational reuse helper, not a replacement for normal Brave dependency synchronization.

## Avito image loading workaround

Reported symptom on the non-Metal GeForce 320M MacBook: images blink while downloading, and become stable when fully loaded. Inspection of a separate installed-Brave profile on avito.ru observed WebP card responses with HTTP 200 and no backdrop-filter elements. This distinguishes the scenario from the known NTP blur workaround; it does not prove a driver/root cause.

The added patch passes `--disable-legacy-gl-partial-images` to renderers only when the browser selected ANGLE GL. Blink then defers incomplete static JPEG/WebP images until all data has arrived. Completed images still use normal GPU rendering. Animated WebP, GIF, other formats and Metal remain outside this workaround. The normal completion notification invalidates cached frames and repaints the completed image.

Tradeoff: static JPEG/WebP images have no progressive preview in legacy GL. This is a targeted display workaround, not a confirmed synchronization fix. Visual verification on Avito with the resulting binary is still pending. Short generic WebGL checks cannot establish that this bug is fixed.

## Workspace handling

Existing tracked changes, source HEADs, private environment and GN arguments were backed up before switching source tags. Source/output directory names can retain their old version suffix to reuse existing objects. Existing installed browsers and real user profiles are not modified by this build recipe. Apple SDK binaries and private environment files are not distributed here.
