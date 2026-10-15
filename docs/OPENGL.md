# OpenGL compatibility build

## What it changes

Apply patches/chromium-macos12-opengl-compat.patch at the Chromium src/ root. It permits ANGLE's existing CGL/OpenGL backend while keeping Metal first/default; adds a macOS brave://flags/#use-angle choice; uses Skia Ganesh instead of the Metal-only Graphite/Dawn path for explicit OpenGL; and allows GLES2 fallback when this explicit legacy backend cannot create GLES3. The fallback is limited to explicit --use-angle=gl; default Metal behavior is unchanged.

Chromium removed its macOS IOSurface texture-target capability while cleaning up the always-2D path. CGL requires rectangle textures for native IOSurfaces, so the patch restores the macOS capability field and Mojo transport, chooses the right target in the shared-image client/factory, and restores related unit-test helpers. The factory retains 2D IOSurfaces for Metal and selects rectangle only for OpenGL. Keep this patch together; restoring only the ANGLE allowlist reproduces texture-target errors and prevents WebGL setup.

Apply patches/brave-opengl-newtab-backdrop.patch separately at src/brave/. The legacy CGL backdrop path produces corrupted New Tab backgrounds on the tested GeForce 320M. The WebUI initializer detects explicit OpenGL on macOS; only then the New Tab document disables CSS backdrop blur and the full-page background blur animation. Images, widgets and accelerated composition/rasterization remain. This targeted accommodation does not fix backdrop filters on arbitrary sites.

The supported flag is opt-in:

    brave://flags/#use-angle -> OpenGL -> Relaunch

or pass --use-angle=gl when launching. Metal remains the default for other installs.

## Validation

Target: MacBookPro7,1, NVIDIA GeForce 320M (256 MiB), macOS 12.7.6; its native driver reports desktop OpenGL 3.3 for a core context and 2.1 for a legacy context. ANGLE selected the hardware NVIDIA OpenGL 3.3 renderer, Skia reported GaneshGL, GPU compositing/rasterization were enabled, and GPU process crash count was zero. A WebGL 1 GLES2 canvas returned the expected pixel [51, 102, 204, 255] with GL error 0. Three native macOS window captures of the built New Tab page were clean. WebGL 2 was not supported by this GPU/driver configuration.

Build-time and runtime experiments showed that the tested corruption came from the New Tab backdrop filter path; disabling that page's blur cleared the native window while retaining OpenGL acceleration. The repository includes the evidence-backed workaround and does not claim a universal CGL driver fix. YouTube Shorts controls and video playback were not specifically validated in this release.

The independent OpenGL artifact is unsigned/unnotarized. “Official” build flags mean is_official_build=true; this is not an official Brave Software build. Proprietary-service keys were placeholders and services depending on them may not work.
