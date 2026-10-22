# Electron 45.0.0 for macOS 12 (Intel)

Independent x86_64 compatibility build of Electron **v45.0.0**, Chromium **156.0.8078.48**, Node **24.22.0**, targeting macOS 12.0+. Upstream sources are downloaded separately; this repository contains the compatibility changes and build recipe.

## Download

[Electron 45.0.0 macOS 12 x64 release](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/electron-v45.0.0-macos12-x64)

Archive: `electron-v45.0.0-macos12-darwin-x64.zip`. See the release assets for its SHA-256 file and [release notes](RELEASE.md) for validation results.

## Pinned sources

| Component | Version | Upstream commit |
| --- | --- | --- |
| Electron | v45.0.0 | `54f961b44b83e4ece81065ab60a182fd0c38c01e` |
| Chromium | 156.0.8078.48 | `d0c02bfad08ec92a6ffcf989e53cd995e6381a4c` |
| Embedded Node | 24.22.0 | Pinned by Electron DEPS |

## Rendering

The browser process calls `MTLCreateSystemDefaultDevice()` before GPU initialization. When no Metal device exists and no explicit `--use-angle`, `--use-gl` or `--disable-gpu` option is present, it selects `--use-angle=gl`. Metal-capable Macs retain the upstream route. This detects an absent Metal device; it does not recover from arbitrary later Metal driver crashes.

The GL route uses ANGLE/CGL and Skia Ganesh. GLES2 fallback is permitted for GPU capability collection; explicit WebGL2/ES3 requests remain strict. Hardware incapable of GLES3 does not gain WebGL2 support. Desktop OpenGL 3.3 is the intended legacy target; negotiated capabilities depend on the driver.

Chromium 156 removed macOS hardware-GL mode and the IOSurface texture-target capability used by the legacy route. The patches restore hardware GL only when ANGLE GL is selected and propagate rectangle texture targets through the shared-image factory, IPC and client. Metal continues using 2D textures. Test helper changes cover that shared-image contract and do not add rendering work to the app.

## Build

The successful host used macOS 12, Xcode 14.2 tools, a private prepared SDK 15.5 copy, depot_tools and Node 24.21.0. Electron uses its own Chromium workspace, separate from Brave.

1. Create a gclient workspace with an unmanaged `src/electron` solution pointing to `https://github.com/electron/electron.git`, `deps_file: DEPS`, and `target_os = ["mac"]`. Fetch and check out Electron v45.0.0 explicitly. Sync without hooks using the exact Electron and Chromium commits in the table, for example:

   ```sh
   gclient sync --nohooks --force --reset --no-history --jobs=8 \
     --revision src/electron@54f961b44b83e4ece81065ab60a182fd0c38c01e \
     --revision src@d0c02bfad08ec92a6ffcf989e53cd995e6381a4c
   ```

   Back up existing work before reset. When reusing an older dependency tree, move conflicting obsolete dependency directories aside instead of deleting unrelated files. For large shared Git caches, `git -c core.alternateRefsCommand=true` avoids scanning every alternate-cache ref; the sync host used the equivalent scoped Git environment configuration.
2. Apply `patches/electron-dependency-install.patch` in `src/electron` before hooks. Immutable Yarn install skips native test fixture builds, without disabling compilation of Electron or its Node engine.
3. Apply Electron's upstream patch series once, using `python3 src/electron/script/apply_all_patches.py src/electron/patches/config.json` from the workspace. Then suppress the `patch_chromium` hook with `custom_hooks: [{"name": "patch_chromium"}]` in the solution and run `gclient runhooks` for tools, JavaScript dependencies and pinned PGO profiles. Do not reapply the upstream patch series on each retry. Fresh upstream revisions require their own patch application and hook state.
4. Prepare a private, legally obtained SDK 15.5 copy with `python3 electron/scripts/prepare-sdk.py --sdk /absolute/path/to/MacOSX15.5.sdk` from this repository. The original Apple SDK is not redistributed. The helper adds compatibility declarations; source guards exclude unsupported macOS 26 APIs.
5. Add depot_tools and host Node to `PATH`, export `ELECTRON_WORKSPACE` as the gclient workspace and `MACOS_SDK_PATH` as the prepared SDK directory, then run `electron/scripts/build-macos12.sh`. Output: `src/out/ReleaseMacOS12/dist.zip`. Use `nohup caffeinate -s ...` with redirected stdin/stdout for a detached remote build.

The GN configuration is Official Release, PGO phase 2 with Electron's own hash-pinned macOS/V8 profiles, optimized ThinLTO, four linker backend jobs, twelve local build jobs, no component build, no debug/DCHECK mode. Both deployment and bundle minimum are 12.0. `mac_sdk_min=13` allows host SDK discovery; `mac_sdk_path` selects the prepared SDK 15.5 used by the compiler.

## Compatibility inventory

- `patches/electron-dependency-install.patch`: Yarn dependency hook.
- `patches/electron-macos12.patch`: deployment assertion, Metal linkage and automatic backend choice (two files).
- `patches/chromium-macos12.patch`: SDK/API guards; ScreenCaptureKit audio guard; ThinLTO job cap; GL allowlist and GPU mode; Ganesh selection; GPU collection GLES fallback; restored IOSurface capability, serialization and clients.
- `configs/macos12-x64-release.gn`: exact build arguments.
- `sdk-shims/` and `scripts/prepare-sdk.py`: private SDK preparation.

See [45.0.0 patch review](../docs/ELECTRON-45.0.0-PATCH-REVIEW.md). The [previous 44.9.0 release](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/electron-v44.9.0-macos12-x64) and its [archived notes](../docs/ELECTRON-44.9.0.md) remain available. Existing Pritunl packages still use Electron 44.7.2; they were not rebuilt for this release.

## Validation

The exact release ZIP passed macOS 12.7.6 GUI/WebGL1 checks on Radeon RX 6800 XT with Metal and explicit OpenGL 4.1, and on a non-Metal GeForce 320M with **automatic OpenGL 3.3 / GLES2**. Hardware compositing/rasterization were enabled. The 320M correctly rejected WebGL2. No child-process exit events were recorded during these short checks; extended stability remains untested. [Evidence](validation/45.0.0.json).

## Limits

Independent third-party release, without Developer ID signing or notarization. Upstream licenses apply. ScreenCaptureKit system-audio loopback is unavailable below macOS 13; ordinary playback and microphone input are separate. Runtime validation coverage and outstanding checks are listed in the release notes.
