# Brave 1.99.56 / Chromium 157 — macOS 12 Intel

Pinned Brave Core v1.99.56: `4d1dfc472152bcc8f3217be190c8a7ad3007039f`. Chromium157.0.8103.50: `049750111b1e5c11565c792b2aeed5541f332bad`. Bundle reports157.1.99.0; source patch version remains1.99.56.

Use [previous full build recipe](../brave-1.98.60/README.md) as the configuration baseline, with these exact new revisions and this directory's patches. Keep private SDK15.5/Xcode14.2, deployment/plist12.0, official nondebug/noncomponent Release, pinned Chrome/V8PGO, optimizedThinLTO/fourbackendjobs, no DCHECK/Vizdebug overhead. Effective arguments were verified before compilation. Run `autoninja -C out/ReleaseOfficial -j12 brave` after Brave branding/configuration preparation. The old Brave wrapper ignored our Ninja concurrency option; direct invocation enforces twelve local jobs.

## Source preparation and patch order

Back up source HEADs/diffs/configuration before switching tags. Reuse the shared Git cache. Update its non-shallow Chromium mirror using an explicit tag refspec, `--no-tags --negotiation-tip=HEAD`, then verify the exact SHA and install the tag in the checkout using existing alternates. Do not directly shallow-fetch Chromium into an isolated checkout: that attempt downloaded millions of unnecessary objects. Cached fetch required9573objects instead.

Before Brave sync, apply `brave-build-hooks.patch` in Brave Core. It ports exact-revision sync to syncUtils.ts and disables prebuilt/test Omaha downloads for this recipe's `use_prebuilt_omaha4=false`. Export `PYTHONPATH=$SRC/brave/script` for upstream swift-format hook imports. Install locked pnpm dependencies, run normal Brave synchronization/upstream patches/hooks.

Apply these patches after upstream Brave patches (Chromium root unless specified):

1. chromium-macos12-sdk-compat.patch
2. brave-stable-profile-directory.patch (path inside Brave)
3. chromium-macos12-opengl-compat.patch
4. brave-opengl-newtab-backdrop.patch (Brave Core root)
5. chromium-macos12-auto-opengl.patch
6. chromium-macos12-opengl-static-image-loading.patch
7. chromium-macos12-fullscreen-input.patch

OpenGL patch has four context ports for Chromium157; retained GL GPU mode, Ganesh/GLES2 collection fallback and IOSurface contract. Other compatibility patches applied without behavioral changes. Historical incremental fullscreen patches are not required. All seven full patches are included here.

## Intel WASM dependency recovery

Brave EXTRA_DEPS omits the IntelMac auxiliary Rust overlay. The first segment failed at opaque_ke because wasm32-unknown-unknown stdlib was absent. Use the target-only libraries from the exact upstream macARM64 overlay for the SAME compiler revision; do not install its host executables:

https://brave-build-deps-public.s3.brave.com/rust-toolchain-aux/mac-arm64-rust-toolchain-1edd55dcfcd573872c727fa3e086369a71661ee0-1125-llvmorg-24-init-7747-g62397f8b-1.tar.xz

SHA256654ed527c2a2bab8ef4aff8e0e2a494bdeadda3524730506a0e6ef9c18d5949b, pinned in upstream EXTRA_DEPS. Run `python3 install-wasm-stdlib.py --src /absolute/src --archive /path/overlay.tar.xz`. It verifies the compiler/hash, copies only WASM target libraries and selects the native Chromium LLVM24 linker. The formerly failed WASM action passed after this recovery. Build resumed without clearing output:56193steps/11h38m52.57s, exit0, completed2026-11-12 19:55MSK (timing excludes initial failed segment).

[Release notes and exact validation scope](../../docs/RELEASE-1.99.56.md). User profiles and installed applications are outside the source recipe.
