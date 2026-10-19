# Brave 1.97.59: macOS 12 x64 with Metal and automatic OpenGL

Build requested 2026-10-18. Latest stable checked against brave/brave-browser releases: v1.97.59 (published 2026-10-16), Chromium 155.0.8059.85. Pinned Brave Core commit: `c7357bfd2a76c2467ba1ae62593a81ae92c05205`; Chromium commit: `0e66b94549a8bd85f03fbdf189b752d6e7b63c32`. Previous validated binaries use Brave v1.97.56 / Chromium 155.0.8059.40.

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

## Small sync optimization and disk cleanup

For an existing shallow Chromium checkout, fetch the new tag explicitly first:

```sh
git -C src fetch --depth=1 origin refs/tags/155.0.8059.85:refs/tags/155.0.8059.85
```

The optional build-tool patch `patches/brave-sync-exact-revision.patch` applies inside src/brave before source sync. It resolves an already available Chromium tag to its exact SHA before passing --revision to gclient; this avoids gclient's unconditional upstream fetch for a tag-valued revision. It does not change the selected commit. Use the normal fallback behavior if the tag is not yet available. Existing installed JavaScript build dependencies were reused after checking that the sync modules load; npm metadata requests were timing out. The lockfile was not edited.

Removed 35.04 GiB of historical out/Release, out/ReleasePGO and out/OfficialAudit outputs on the build Mac. SDK subdirectories and their symlink chain were explicitly retained. Previous GN argument files were saved in docs/cleanup-20261018-233828. Current ReleaseOfficial, Electron and source/tool caches were preserved. Free space after cleanup was approximately 465 GiB, with sync active.

## Compilation started

Source sync and hooks completed successfully. All compatibility patches applied without conflicts. The new source-pinned Chrome profile and V8 15.5.35.25 profiles were downloaded with V8 revision validation. GN preflight and a second check after Brave's build wrapper verified the intended official/PGO/ThinLTO settings and actual Blink OFFICIAL_BUILD, -O2, -flto=thin, -fprofile-use and zero-init compiler flags. Compilation is running detached in ReleaseOfficial (build id a5872ca3-0ae6-48c0-add8-723e5d7e7dee); the first observed progress was 289 completed actions with a dynamically pruned graph of approximately 82,000 actions. This is startup progress, not a completion or runtime validation result.

## Completed build and local performance comparison — 2026-10-19

Build succeeded with exit 0: 59,661 steps in 12h09m37s. Final app size is approximately 572 MiB. Framework SHA-256: `cb470ea3eaeb63691a7ad370305991f96dd85e05f90972ac29e6e56d62905517`. Transfer archive SHA-256: `3edb6e6c88e84490cf4474f1d74652de236d98e43d9efcaa204e140e15b85599`.

Compared the installed v1.97.56 build with the v1.97.59 candidate on the same macOS 12 Intel Mac with Radeon RX 6800 XT. Used separate test profiles, identical Arial/DOM/root geometry and viewport between builds, warmed layout loops, six layout samples per build, and launch order old/new/new/old. Mean synchronous layout: previous 3.20456 ms, candidate 3.17956 ms (0.78% lower). Two 120-frame synthetic animation samples per build averaged 51.66 versus 53.31 FPS. Background system activity was present, so these small differences are not evidence of a general performance improvement. No regression appeared in these workloads. Both reported ANGLE Metal, GraphiteDawnMetal, enabled GPU compositing/rasterization, and zero GPU crashes.

Installed the candidate on the local Mac after the comparison. Preserved the complete prior application and stable profile; 13 important profile/session files matched the backup by SHA-256 before app replacement. The active profile retained all 2,740 cookies after relaunch. User data is not included in this repository. The app and GPU child launched; no forced OpenGL/software flag was present. Both old and new apps retain bundle version 155.1.97.0 under the existing local development-version convention, so source revisions and framework hashes identify the builds.

Raw local comparison evidence: Library/Caches/BraveBuildTransfer/gpu-diagnostics/brave-1.97.59-compare-1792402876081. Comparison scripts/results remain there. The new automatic non-Metal path has not yet been runtime-tested on the MacBook; new binary release publication remains pending.
