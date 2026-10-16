Independent Electron **44.7.2** / Chromium **152.0.7977.149** / Node **24.21.0** for **macOS 12.0+, Intel x64**.

Includes macOS 12 compatibility, official Release optimization configuration with Electron PGO and ThinLTO, and automatic ANGLE OpenGL/Ganesh selection when no Metal device exists. Explicit renderer options take precedence. OpenGL/GLES/WebGL capabilities depend on the target driver.

The complete distribution ZIP is attached with a SHA-256 file. Its checksum is `f513ed330cc170a1339ce264db947d7bfaf39dcf726852c92c57bd8025136de7`.

Compilation and ZIP packaging succeeded. Node-mode startup on macOS 12 was verified; Pritunl 1.4.4777.90 has been compiled and packaged against this engine. Initial Pritunl GUI startup on a non-Metal MacBookPro7,1 running macOS 12.7.6 was verified; its GPU child automatically selects --use-angle=gl. Extended rendering/GPU stability and VPN connection checks remain pending. ScreenCaptureKit audio loopback remains unavailable on macOS 12.

This experimental third-party build has no Developer ID signature or notarization. See [patches, SDK preparation and build instructions](https://github.com/amstel8/brave-macos12/tree/main/electron) for the complete local changes and pinned inputs. Stock Electron 44 binaries are not replaced by this compatibility build on npm.
