# Brave 1.98.60-r2 for macOS 12 — fullscreen input fix

**Package revision 2**, based on Brave Core **v1.98.60** and Chromium **156.0.8078.48**. Intel x86_64, minimum macOS **12.0**, Metal and automatic ANGLE OpenGL fallback. Application/bundle version remains **156.1.98.0**; `r2` identifies this repository's package revision.

## What changed

Fixed native fullscreen mouse input on macOS 12. On the tested OCLP MacBook, a transparent AppKit toolbar window overlapped the top 44 pixels of web content and intercepted events. Avito's business menu was visible but did not respond. The patch forwards mouse input from that empty region to the page, preserving real toolbar controls. It also resolves initially unassigned mouse-move events so hover works before the first click.

The workaround is enabled only on macOS 12. The issue has not been tested on other major macOS versions. Graphics selection, the stable profile directory and the base Release/PGO/ThinLTO configuration are retained. Source pins remain Brave Core `52db4b25c0aa3038e9a1c6021428b136cc3cb5fc` and Chromium `d0c02bfad08ec92a6ffcf989e53cd995e6381a4c`.

## Download and install

Download `brave-v1.98.60-r2-macos12-x64-metal-opengl.tar.gz` and its `.sha256` asset. Verify the checksum, extract, quit Brave and replace **Brave Browser.app** in Applications. Keep the existing `BraveSoftware/Brave-Browser` profile in Application Support.

- Archive SHA-256: `327e0274b628993c845d6defc687fcadeec6dea9516d8e6e944f656396306fc5`.
- Archive size: **300,759,860 bytes**.
- Framework SHA-256: `417389265f27abdcadb264efb399c2fc0f878c7bb775cd2408703b5fe42636b0`.

The framework read back from this exact archive matches the validated build installed on the MacBook. This is an independent community build without Developer ID signing/notarization; macOS may require manually opening the application.

## Validation of this revision

On an OCLP MacBookPro7,1 / GeForce 320M with macOS 12.7.6, the clean binary passed **40/40 trusted native clicks and 40/40 trusted pre-click hovers** across normal window, fullscreen with visible toolbar, hidden toolbar, restored toolbar, and return to normal window. The prior package passed 5/8 clicks in fullscreen and 0/8 with its toolbar hidden; this revision passed 8/8 of both input checks in every state.

Native right-click/context-menu delivery, a drag from the affected strip into the page, address-field mouse focus and tab-strip switching passed. After installation, the user's existing signed-in Avito session opened the business dropdown on hover and accepted a click in fullscreen. The stable profile was preserved and backed up before installation.

This revision's short functional checks do not establish extended stability or performance. The exact r2 binary has not been separately validated on the Metal desktop. The base static JPEG/WebP loading workaround is retained; these input tests do not establish whether it fixes every reported image-flicker scenario. WebGL2/WebGPU availability still depends on the GPU and driver; the GeForce 320M supports the previously validated GLES2/WebGL1 route. Proprietary service credentials remain placeholders.

[Patch and native investigation](https://github.com/amstel8/legacy-brave-electron-opengl/blob/main/docs/FULLSCREEN-INPUT-MACOS12.md) · [Machine-readable results](https://github.com/amstel8/legacy-brave-electron-opengl/blob/main/tests/macos12/fullscreen-input-results.json) · [Build recipe](https://github.com/amstel8/legacy-brave-electron-opengl/tree/main/recipes/brave-1.98.60).
