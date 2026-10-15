# Release v155.1.97.0-macos12-opengl

Brave 155.1.97.0 / Chromium 155.0.8059.40, x86_64, minimum macOS 12.0. Built independently from Brave v1.97.56 with the SDK, profile-path, ANGLE/OpenGL IOSurface, GLES2 fallback, and New Tab backdrop patches in this repository. PGO phase 2 and optimized ThinLTO are enabled. This is unsigned and unnotarized; is_official_build=true describes Chromium build options, not the publisher. Proprietary-service keys were placeholders.

Graphics default to Metal; on non-Metal hardware select OpenGL at brave://flags/#use-angle and relaunch. OpenGL was validated on a GeForce 320M: ANGLE OpenGL 3.3, Skia GaneshGL, accelerated composition/rasterization and WebGL 1 passed. WebGL 2 is not supported on that test GPU/driver. To avoid a verified New Tab corruption on this legacy CGL path, the OpenGL build disables New Tab backdrop blur only. Other sites' backdrop filters were not validated.

Asset SHA-256: 7061b381125efe68fb217a35d59f94723abbb92d10da4d4815e32338a11106f6 (brave-macos12-x64-155.1.97.0-opengl.tar.gz). Verify the downloaded archive with its adjacent .sha256 file before extracting. Replace Brave only after quitting it, and keep a backup of the application and profile at ~/Library/Application Support/BraveSoftware/Brave-Browser. A newer version may migrate profile data; restoring the old app may require restoring its matching profile.
