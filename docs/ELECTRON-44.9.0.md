> Archived documentation for the 44.9.0 release. Build recipe and patch paths below refer to repository commit `e4e9327`; current `electron/` targets 45.0.0.

# Electron 44.9.0 for macOS 12 (Intel)

Independent compatibility build, targeting x86_64 and macOS 12.0. Electron commit `fd148b9908b83c8dc09924e45e6df44b83b6bfe7` (tag v44.9.0), pinned Chromium 152.0.7977.167 (`dd78960ccd8a03a2fe1f629543d27783885b78e9`) and Node 24.22.0. The archive is a GitHub Release asset; original Electron/Chromium sources are fetched upstream.

## Download and status

[Electron v44.9.0 macOS 12 x64 release](https://github.com/amstel8/legacy-brave-electron-opengl/releases/tag/electron-v44.9.0-macos12-x64)

Archive: electron-v44.9.0-macos12-darwin-x64.zip. SHA-256: 7e0be42f00e066d746bb7ab0958ecbe99fa94fb5df97e346b408cc8ae58837e2.

Compilation completed successfully in 9h44m15s (41,857 steps), followed by successful distribution ZIP packaging. Node-mode version checks and GUI/WebGL1 checks passed on Metal and automatic OpenGL; details are below. Pritunl 1.4.4777.90 was built with the previous 44.7.2 engine and was not rebuilt with 44.9.0. This is an independent third-party compatibility release, without Developer ID signing or notarization.

## Rendering behavior

On browser-process startup, query MTLCreateSystemDefaultDevice(). If no Metal device exists and no explicit --use-angle, --use-gl or --disable-gpu option is present, select --use-angle=gl. Metal-capable systems retain upstream behavior. This detects absence of a Metal device; it does not catch arbitrary later Metal driver crashes.

The OpenGL path uses ANGLE CGL and Skia Ganesh, retains GPU operation when the driver exposes GLES2 rather than GLES3, and selects rectangle textures for CGL IOSurfaces. Desktop OpenGL 3.3 is the intended legacy target, but the driver determines the negotiated version. WebGL2/WebGPU support is not implied. Chromium 152 still has shared-image capability/IPC propagation, so Brave's larger Chromium 155 restoration patch is unnecessary.

ScreenCaptureKit audio loopback capture returns failure below macOS 13; ordinary playback and microphone capture are separate features.

## Build

Use Electron's upstream macOS/manual GN prerequisites, shared depot_tools and Node 24.21.0. The successful host used Xcode 14.2 tools plus a separate macOS SDK 15.5 copy. Keep Electron's own Chromium checkout separate from Brave's.

1. Configure a gclient workspace named src/electron with https://github.com/electron/electron.git as an unmanaged solution; target_os = ["mac"]. Check out Electron tag v44.9.0, then run gclient sync --nohooks --revision src/electron@v44.9.0.
2. Apply patches/electron-dependency-install.patch from src/electron before hooks. It adds --mode=skip-build to immutable Yarn install, avoiding compilation of test-only native fixture packages with the host Xcode libc++. It does not disable building Electron or its Node engine.
3. Run gclient runhooks once to apply Electron's upstream patch series, install JavaScript dependencies, download tools, and fetch Electron's hash-pinned macOS/V8 PGO profiles. A runhooks retry must not reapply already-applied upstream patches: on the tested snapshot the patch_chromium hook was suppressed through a .gclient custom_hooks override only after its first successful application. Re-enable it when syncing a fresh revision.
4. Make a private copy of a legally obtained SDK 15.5. Run python3 electron/scripts/prepare-sdk.py --sdk /absolute/path/to/MacOSX15.5.sdk against that copy. It adds the same CGImage byte-order aliases, AX/NSAccessibility constants, Glass declarations and guarded passkey declaration as the previously used shared compatibility SDK. Apple SDK declarations retain their upstream copyright; the original SDK is not distributed here. Source guards prevent unsupported runtime API calls on macOS 12.
5. Add depot_tools to PATH, set ELECTRON_WORKSPACE to the gclient workspace and MACOS_SDK_PATH to the prepared SDK copy, and run electron/scripts/build-macos12.sh from this recipe repository. The script applies the remaining two patches after upstream hooks, copies configs/macos12-x64-release.gn, generates GN, builds electron and electron:electron_dist_zip. Output is src/out/ReleaseMacOS12/dist.zip.

The configuration uses official Release mode, PGO phase 2 with Electron's profiles, optimized ThinLTO, four ThinLTO backend jobs, twelve local build jobs, no component build, and disabled debug/DCHECK modes. mac_sdk_min=13 permits discovery of the host Xcode's SDK; mac_sdk_path explicitly uses the prepared SDK 15.5 for compilation. Both deployment and plist minimum are 12.0. No private service credentials are required.

## Modification inventory

- patches/electron-dependency-install.patch: Electron DEPS Yarn install hook (one file).
- patches/electron-macos12.patch: deployment assertion and Metal framework linkage in BUILD.gn, automatic backend selection in electron_library_main.mm (two files).
- patches/chromium-macos12.patch: older SDK/process/display APIs, guarded Glass recognition, ThinLTO job cap, guarded audio loopback, ANGLE OpenGL allowlist, Ganesh selection, GLES2 retention and CGL IOSurface texture target (nine files).
- configs/: exact successful GN arguments.
- sdk-shims/ and scripts/prepare-sdk.py: compatibility declarations for the private SDK copy.

Electron and Chromium modifications remain under their original upstream licenses. The build is not published, endorsed or supported by the Electron project.

## 44.9.0 validation

The exact distribution passed Node-mode version checks and separate GUI/WebGL1 pixel checks on macOS 12: Radeon RX 6800 XT with Metal and a non-Metal GeForce 320M MacBook with automatic OpenGL selection. Hardware compositing/rasterization were enabled. Existing Pritunl packaging evidence above describes the earlier 44.7.2 port; Pritunl was not rebuilt with 44.9.0 as part of this update. Extended application and stability tests remain pending.
