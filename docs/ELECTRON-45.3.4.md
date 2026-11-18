# Electron 45.3.4 macOS 12 build

Electron v45.3.4 commit f3d1a2f654d6e7ccdbc5ccdd022b147fa05f064e; Chromium 156.0.8078.100 commit 46876a0c2df3492ed67a8846950ba6d37170b58c; Node 24.22.3. Chromium objects/output reused from 45.3.2. Source/config/diffs backed up. Existing compatibility patches applied unchanged. Official Release, hash-pinned PGO, optimized ThinLTO with four backend jobs and twelve compile jobs, prepared SDK15.5, deployment/plist minimum12.0.

Completed 2026-11-18 07:31 MSK, exit0: 41235 steps in9h02m10.73s plus25.91s packaging. Exact ZIP passes SHA256/CRC/minimumOS/runtimeversion checks and short macOS12.7.6/RX6800XT defaultMetal and explicitGL WebGL1 checks, accelerated compositing/rasterization, expected pixelreadback, no childprocess exit events. GeForce320M automaticGL3.3, performance/media/conferencing/extendedstability remain pending. Installed apps and existing profiles unchanged.

[Current release notes](../electron/RELEASE.md). [Archived45.3.2 notes](ELECTRON-45.3.2-RELEASE.md).
