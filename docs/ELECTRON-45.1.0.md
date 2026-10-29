# Electron 45.1.0 macOS 12 build notes

- Electron v45.1.0: `45d20ec03000aac41e73b2abdb707936b4f98ed0`.
- Chromium 156.0.8078.49: `29eb03535d5f2f4f899b95f22a92413ffde5284e`, followed by Electron upstream patches and compatibility patches.
- Embedded Node 24.22.1.
- Intel x86_64, deployment and bundle minimum 12.0.
- Existing Electron workspace/output reused; old configuration, local diffs and Git HEAD references preserved before reset.
- Electron checked out before exact-revision dependency synchronization. Upstream patch series applied once; duplicate patch hook suppressed. Immutable Yarn install uses skip-build mode for test fixtures.
- Published 45.0.0 compatibility patches applied without source changes. Official Release effective arguments and Electron PGO hashes verified before compilation.
- Compilation: 42,464 steps, 9h02m09.11s; packaging: 3 steps, 28.32s; worker exit 0, completed 2026-10-29 07:38 MSK.

See [release notes](../electron/RELEASE.md) for exact artifact identity and fresh validation scope. Older non-Metal hardware validation is pending for this ZIP; previous release results are retained separately.
