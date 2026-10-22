# Electron 45.0.0 macOS 12 build notes

## Sources and configuration

- Electron tag v45.0.0: `54f961b44b83e4ece81065ab60a182fd0c38c01e`.
- Chromium 156.0.8078.48: `d0c02bfad08ec92a6ffcf989e53cd995e6381a4c`, followed by Electron upstream patches and the compatibility patch.
- Embedded Node 24.22.0, V8 15.6.75.19-electron.0.
- Intel x86_64, macOS deployment and plist minimum 12.0.
- Xcode 14.2 host, private prepared SDK 15.5, Electron's own pinned PGO profiles, optimized ThinLTO with four backend jobs, twelve local compile jobs.

## Migration from 44.9.0

The existing Electron workspace and output directory were reused. Initial synchronization stopped because an old standalone aria-practices dependency conflicted with newly tracked Chromium files. The directory was moved to a backup. Electron itself was still on 44.9.0, causing gclient to read its older DEPS despite an earlier Chromium 156 tag fetch. Explicit checkout and exact revision overrides fixed that mismatch. Duplicate waiting workers were stopped, and accidental whole-tree backup logic was replaced with configuration/diff backups.

Electron's upstream dependency patches were applied once before hooks. The patch hook was then suppressed during repeated runhooks so retries could not reapply the series. Yarn immutable install used skip-build mode for native test fixture packages. PGO profile hashes and effective Official Release GN arguments were checked before compilation.

## Compatibility review and corrections

The first preparation script had an invalid GN semicolon in the ThinLTO declaration; corrected before compilation. The static review also found an inverted GLES fallback condition: fixed so the GPU collection context permits GLES2 fallback only on legacy ANGLE GL. The change to explicit WebGL2/ES3 contexts was removed, retaining upstream strict behavior.

Compilation later required an additional SDK guard around CALayer macOS 26 HDR properties. Runtime availability checks alone cannot compile declarations absent from SDK 15.5; the compile-time guard excludes that block while retaining the older path.

Chromium 156 removed the IOSurface texture-target capability and macOS hardware-GL GPU mode. The patch restores the complete factory/IPC/client texture target contract and enables hardware-GL mode only for explicitly selected ANGLE GL. Metal retains the upstream GPU-mode policy. Without the latter change, the Metal runtime check passed while forced GL entered software rendering; that check prevented publishing the incomplete first ZIP.

The first compile/package sequence finished on 2026-10-22 at 21:19 MSK. The final resumed compilation segment took 6h46m53s, followed by 25s ZIP packaging. These timings exclude earlier interrupted segments and the subsequent targeted GL-mode correction/relink.

## Final artifact

See [release notes](../electron/RELEASE.md) for the final archive checksum and exact validation coverage.

## GeForce 320M follow-up — 2026-10-23

The exact published ZIP (SHA-256 2807aaa78ef959402e62cb5cc348d37809d0a77470c2b1883a70ccd6ae0fd1ed) was checked on the non-Metal OCLP MacBookPro7,1 with macOS 12.7.6. Launched through the GUI session with a separate profile and no graphics switches. It automatically chose ANGLE OpenGL 3.3, exposing GLES2, with GaneshGL. Hardware compositing/rasterization enabled. WebGL1 pixel [51,102,204,255], error 0; a distinct WebGL2 canvas returned null as expected. No child-process exit events during the short check. This resolves the legacy-hardware validation item left pending in the initial publication. No installed app or existing profile was changed.
