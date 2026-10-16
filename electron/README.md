# Electron 44.7.2 for macOS 12 (Intel)

Independent compatibility build, targeting x86_64 and macOS 12.0. Electron commit `774d5d0a051374923758372a4ee4bf04f473151d` (tag v44.7.2), pinned Chromium 152.0.7977.149 (`ba6d62e0eacecd63aed843a9bf735a148efb93c4`) and Node 24.21.0. The archive is a GitHub Release asset; original Electron/Chromium sources are fetched upstream.

## Download and status

[Electron v44.7.2 macOS 12 x64 release](https://github.com/amstel8/brave-macos12/releases/tag/electron-v44.7.2-macos12-x64)

Archive: electron-v44.7.2-macos12-darwin-x64.zip. SHA-256: f513ed330cc170a1339ce264db947d7bfaf39dcf726852c92c57bd8025136de7.

Compilation and distribution ZIP completed successfully in approximately 10h06m on a 32 GB Intel Mac Pro. The engine runs on macOS 12 in ELECTRON_RUN_AS_NODE mode and reports the pinned versions. Pritunl 1.4.4777.90 has been compiled and packaged with this engine. Full GUI/GPU validation on a non-Metal Mac remains pending. This is an experimental third-party port, without Developer ID signing or notarization.

## Rendering behavior

On browser-process startup, query MTLCreateSystemDefaultDevice(). If no Metal device exists and no explicit --use-angle, --use-gl or --disable-gpu option is present, select --use-angle=gl. Metal-capable systems retain upstream behavior. This detects absence of a Metal device; it does not catch arbitrary later Metal driver crashes.

The OpenGL path uses ANGLE CGL and Skia Ganesh, retains GPU operation when the driver exposes GLES2 rather than GLES3, and selects rectangle textures for CGL IOSurfaces. Desktop OpenGL 3.3 is the intended legacy target, but the driver determines the negotiated version. WebGL2/WebGPU support is not implied. Chromium 152 still has shared-image capability/IPC propagation, so Brave's larger Chromium 155 restoration patch is unnecessary.

ScreenCaptureKit audio loopback capture returns failure below macOS 13; ordinary playback and microphone capture are separate features.

## Build

Use Electron's upstream macOS/manual GN prerequisites, shared depot_tools and Node 24.21.0. The successful host used Xcode 14.2 tools plus a separate macOS SDK 15.5 copy. Keep Electron's own Chromium checkout separate from Brave's.

1. Configure a gclient workspace named src/electron with https://github.com/electron/electron.git as an unmanaged solution; target_os = ["mac"]. Check out Electron tag v44.7.2, then run gclient sync --nohooks --revision src/electron@v44.7.2.
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
