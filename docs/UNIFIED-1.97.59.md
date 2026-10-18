# Brave 1.97.59: macOS 12 x64 with Metal and automatic OpenGL

Build requested 2026-10-18. Latest stable checked against brave/brave-browser releases: v1.97.59 (published 2026-10-16), Chromium 155.0.8059.85. Previous validated binaries use Brave v1.97.56 / Chromium 155.0.8059.40.

## Package and backend selection

One x86_64 package includes both existing Metal rendering and ANGLE/CGL/Ganesh compatibility. It is not an arm64/x64 Universal 2 binary.

Apply the four patches documented in BUILD.md, then `patches/chromium-macos12-auto-opengl.patch` from Chromium src/. The latter adds early browser-process detection via MTLCreateSystemDefaultDevice(), with explicit Metal.framework linkage. It appends --use-angle=gl only when no Metal device exists and --use-angle, --use-gl, --disable-gpu are absent. Helpers do not perform their own detection. Existing explicit command-line choices are respected. Selection runs before content/GPU initialization. It does not recover from arbitrary subsequent Metal driver crashes.

The existing OpenGL New Tab backdrop workaround remains necessary and is included. WebGL2, WebGPU and desktop OpenGL 3.3 are not guaranteed by this change; capabilities depend on the driver.

The idempotent source-edit helper `scripts/add-brave-auto-opengl.py --src /path/to/src` generates the same change; alternatively apply the patch, not both. Its optional --patch argument records only changes introduced by the helper, excluding Brave's upstream patches.

## Build configuration and update workflow

Use the official Release / PGO phase 2 / optimized ThinLTO configuration from BUILD.md, with macOS deployment and minimum system 12.0, Intel x64, non-component build, disabled DCHECK/Viz debugging, zero stack initialization, four ThinLTO backend jobs, and twelve local tasks. Fetch the new source-pinned Chrome and V8 PGO profiles after updating; do not silently retain a mismatched profile. Keep the prepared SDK 15.5 and Xcode 14.2 host tools.

On the existing build Mac Pro the working directory retains its historical name `~/Documents/chromium-build/projects/brave-stable-1.97.56/src` to reuse `out/ReleaseOfficial`. The directory name is not the selected source revision. Before the update, complete Chromium and Brave tracked diffs, source HEADs, private local environment, and GN arguments were saved in `backups/brave-before-1.97.59-*`. Private environment files are not published.

The update checks out Brave Core v1.97.59, runs its Chromium/dependency sync and upstream patch application, reapplies the macOS/OpenGL/profile patches, validates GN configuration and required PGO inputs, then invokes the existing Brave build wrapper. Installed browsers and profiles are not updated by this build request.

Persistent status on the build Mac Pro:

- `logs/brave-1.97.59-sync.log`, `.pid`, `.exit`: source/dependency update.
- `logs/brave-1.97.59-unified.log`, `.pid`, `.stage`, `.exit`: patching, validation and build.
- `logs/brave-1.97.59-build-unified.exit`: compiler wrapper exit code.

Detached nohup/caffeinate workers continue after SSH disconnect. Current status is taken from these files; this document does not claim that compilation or runtime validation has completed. Runtime checks should cover Metal and non-Metal GUI startup, actual renderer backend, ordinary pages, New Tab native-window rendering and WebGL1 before publishing a new binary.
