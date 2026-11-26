# Brave 1.100.58 on Intel macOS 12

- Brave Core v1.100.58: `bd6d26d1bced03c17a98baa86d2cd3425d543d1b`
- Chromium 158.0.8127.42: `52bdd21723d5db0c9ab11716d38feac74828cf84`
- Bundle metadata: `158.1.100.0`. The source tag carries the full Brave version.
- Verified build: Intel x86_64, minimum macOS 12.0, 53,862 steps in 12h18m49s after the last resume. An isolated headless launch loaded a test page on macOS 12.7.6.

Use the [Chromium 157 recipe](../brave-1.99.56/README.md) as the configuration baseline. Keep the SDK 15.5 shim and Xcode 14.2 host tools. Prepare an official non-component Release with Chrome/V8 PGO, ThinLTO, four ThinLTO backend jobs, `use_prebuilt_omaha4=false`, and `mac_deployment_target` and `mac_min_system_version` set to `12.0`. Use the source-pinned PGO profiles.

## Patch sequence

Apply `brave-build-hooks.patch` in Brave Core before syncing. This lets sync use the resolved Chromium commit and skips the unused prebuilt Omaha updater download. Put the Brave Core `script` directory on `PYTHONPATH` for hooks and compilation. Run Brave's normal dependency sync and upstream patch application before applying these compatibility patches.

1. `chromium-macos12-sdk-compat.patch` in Chromium. This includes the SDK guard for the `vm_statistics64.swapped_count` field.
2. `brave-stable-profile-directory.patch` in Brave Core.
3. `chromium-macos12-opengl-compat.patch` in Chromium.
4. `brave-opengl-newtab-backdrop.patch` in Brave Core.
5. `chromium-macos12-auto-opengl.patch` in Chromium, or generate it with `add-brave-auto-opengl.py`.
6. `chromium-macos12-opengl-static-image-loading.patch` in Chromium.
7. `chromium-macos12-fullscreen-input.patch` in Chromium.

## Intel WebAssembly toolchain

Brave's auxiliary Rust overlay is not installed by the upstream hook on Intel Macs. Download the exact [macOS auxiliary archive](https://brave-build-deps-public.s3.brave.com/rust-toolchain-aux/mac-arm64-rust-toolchain-8a9dd7abdf013ec10cfeaaa3685feba18ef1c90c-1-llvmorg-24-init-14453-ge063be79-1.tar.xz) pinned in this version's `EXTRA_DEPS`. The installer checks the compiler and archive digest and extracts only `wasm32-unknown-unknown` files. Linking uses Chromium's native LLVM.

```sh
python3 install-wasm-stdlib.py --src /path/to/src --archive /path/to/overlay.tar.xz
export PATH="/path/to/src/third_party/rust-toolchain/bin:$PATH"
export PYTHONPATH="/path/to/src/brave/script${PYTHONPATH:+:$PYTHONPATH}"
```

After Brave branding and GN preparation, run `autoninja -C out/ReleaseOfficial -j12 brave` from `src`. Existing output can be reused after recovering the WebAssembly target or applying the SDK guard.
