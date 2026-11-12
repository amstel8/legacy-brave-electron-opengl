# Electron 45.3.0 macOS 12 build

Electron4701f41b6c6eef25332111976d5869ed31c62a6e, Chromium156.0.8078.96/2ad9b7f5a86846e0b264090723a6a78964bb84c4, Node24.22.2. Existing compatibility patches retained unchanged. Official Release, pinnedPGO, optimizedThinLTO, fourbackendjobs/twelvecompilejobs, minimum12.0. Source backup deduplicates existing backup branches; shared non-shallow cache avoids redundant Chromium shallowfetch. Build42605steps9h04m36.19s + packaging28.76s, completed2026-11-12 08:11MSK exit0.

See [current release notes](../electron/RELEASE.md) and [archived45.2.3 release](ELECTRON-45.2.3-RELEASE.md). New exactZIP was checked on RX6800XT/defaultMetal and explicitGL; non-Metal320M validation remains pending. No installed apps/profiles changed.
