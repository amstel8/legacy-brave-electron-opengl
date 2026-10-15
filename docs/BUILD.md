# Build recipe and patch inventory

## Source and toolchain

Use Brave `v1.97.56` (`b01cdf43be4b4d5559bf7e58229e666e24454f50`) and its pinned Chromium source `155.0.8059.40` (`cfaadc5a132d78e1828635aa8405a499f3e14864`). Follow Brave's official macOS build prerequisites and `brave-browser` setup/sync instructions; this repository does not mirror Chromium or Brave source. The verified build used Node 24.21.0, pnpm 11.28.5, depot_tools, macOS SDK 15.5, and Xcode 14.2 host tools. The SDK path and output directory are machine-specific; point GN at a local SDK path valid for your checkout. Keep the deployment and minimum system versions at 12.0 and target CPU at x64.

For reproducible source retrieval, check out the Brave tag, sync the pinned dependencies using Brave's documented workflow, and apply the patches below in order:

1. From Chromium `src/`, apply `patches/chromium-macos12-sdk-compat.patch` with `git apply`.
2. From Chromium `src/`, apply `patches/brave-stable-profile-directory.patch` with `git apply`.

The Brave patch changes `src/brave/build/config.gni`, which is part of the Brave source checkout embedded in `src/`. Check whether Brave's setup scripts overwrite it after patching. Do not apply the unrelated OpenGL experiment from the original private build workspace.

Generate `out/ReleaseOfficial` with the following relevant GN arguments, retaining Brave's normal branding and the generated PGO profile paths:

```gn
target_cpu = "x64"
mac_deployment_target = "12.0"
mac_min_system_version = "12.0"
is_official_build = true
is_debug = false
is_component_build = false
dcheck_always_on = false
enable_expensive_dchecks = false
chrome_pgo_phase = 2
use_thin_lto = true
thin_lto_enable_optimizations = true
thin_lto_backend_jobs = 4
init_stack_vars_zero = true
use_prebuilt_omaha4 = false
```

Use the source-pinned macOS and V8 PGO profiles. Four ThinLTO backend jobs was the tested memory limit for the 32 GB build host, not a universal performance setting. Official GN configuration used the normal Chromium options for disabling iterator debugging, Viz debugger, Brave PageGraph WebAPI probes, and IPC fuzzing. Service credential values needed only to satisfy unavailable local GN assertions were dummy placeholders, not working credentials. Never publish credentials.

Then run GN generation and Brave's documented build target for the release app (the successful build used `autoninja -C out/ReleaseOfficial brave`). Build duration was about 12 hours on the tested host. The resulting app should report version `155.1.97.0` and minimum macOS `12.0`. Keep signing and notarization claims separate: this artifact is unsigned and unnotarized.

## Included patches

- `chromium-macos12-sdk-compat.patch`: use the older SDK-compatible `posix_spawn_file_actions_addchdir_np`; use `NSScreen.deviceDescription` for display IDs; compile-time guard macOS 26 HDR/AppKit APIs when building with older SDKs; cap ThinLTO backend jobs through a GN setting defaulting to upstream's unlimited behavior (`0`).
- `brave-stable-profile-directory.patch`: select the stable Brave product directory rather than `-Development`, so the release uses the expected stable profile location.

The source code belongs to the upstream Chromium and Brave projects and retains their respective licenses and notices. This repository provides modifications only; it does not relicense upstream code or bundle upstream source. Consult the [Chromium license](https://chromium.googlesource.com/chromium/src/+/main/LICENSE) and [Brave license](https://github.com/brave/brave-browser/blob/master/LICENSE) for source licensing terms.
