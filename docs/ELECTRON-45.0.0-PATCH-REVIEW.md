# Electron 45 macOS 12 patch review — 2026-10-22

Static review of the compatibility patches and the affected Chromium 156 sources. This review does not establish runtime GPU correctness; Metal and the non-Metal MacBook still need validation after packaging.

## Necessary changes

- Electron deployment target assertion: permit 12.0. The assertion alone does not guarantee compatibility with all APIs; existing guards and runtime validation are still required.
- SDK guards: avoid compiling macOS 26 declarations with the prepared 15.5 SDK. NSScreen uses the existing older display-ID route.
- ScreenCaptureKit system audio capture: fail explicitly below macOS 13; this does not disable ordinary playback or microphone input. No new system-audio implementation for Monterey was added.
- Enable ANGLE OpenGL as an allowed backend; keep Metal first. Detect absent Metal device once at browser startup, respect explicit backend/disable-gpu choices. This is absence detection, not recovery from a later Metal driver failure.
- Disable Graphite only for the explicitly selected ANGLE GL route, so Ganesh can be used. Metal continues through the upstream Graphite decision.
- Restore IOSurface texture target capability across GPU/client IPC: CGL needs rectangle textures, Metal uses 2D textures. The field, serialization, factory and client changes are one connected mechanism, not independent workaround features. Removing only the IPC portion would break the producer/consumer contract. Test helper and test-source changes are maintenance code, not runtime rendering overhead.
- ThinLTO backend jobs cap: limits build-host memory pressure without disabling ThinLTO optimization or PGO.

## Confirmed defects fixed

1. The GL context fallback condition was inverted: !IsLegacyOpenGLBackendSelected() disabled GLES fallback for GL and enabled it for Metal. gpu_info_collector now permits fallback only when the legacy GL backend is selected, matching GLContextEGL semantics. Metal retains the original false setting.
2. Removed the service_utils WebGL2/ES3 fallback change entirely. An explicit ES3 request should remain strict rather than silently accepting ES2; WebGL1 remains the route for legacy GPUs. The compositor already uses default GLContextAttribs with fallback enabled, so modifying this explicit WebGL2 request is unnecessary.
3. Earlier GN semicolon fixed in preparation script, applied source and exported patch.

The active build was interrupted once with SIGINT for the review correction, then resumed incrementally with the same output directory and existing object files. Full-tree copying and duplicate workers had already been removed during recovery.

## Simplifications considered

IsLegacyOpenGLBackendSelected now has one production caller and can be inlined into gpu_info_collector, removing the helper declaration/definition from ui/gl. This is optional cleanup, with no demonstrated runtime benefit; left unchanged during this build. SharedImageInterface is passed by scoped_refptr in texture-target computation, adding small refcount work on shared-image creation; a borrowed reference could simplify ownership, but no benchmark currently identifies this as material.

## Limits

No complete claim of compatibility can be made from successful GN generation or compilation. After packaging, check Metal renderer selection, automatic GL selection on GeForce 320M, WebGL1 output, WebGL2 rejection on unsupported hardware, IOSurface video/canvas presentation and GPU process stability. Old GPU support does not add GLES3/WebGL2 capability to hardware that cannot expose it.

## Runtime follow-up before publication

The first distribution passed Metal/WebGL1 checks but failed forced GL on Radeon RX 6800 XT. This exposed another Chromium 156 change outside the initial patch set: GpuDataManagerImplPrivate initialized supports_gpu_mode_hardware_gl_ to false on macOS. With Graphite intentionally disabled for GL, no hardware rendering mode remained. The field now becomes true only for --use-angle=gl; the Metal route retains its upstream value. This was a missing compatibility change, not an observed driver crash despite Chromium's generic GPU-access error wording. A targeted rebuild and revalidation follow this correction.

## Final result

The targeted GPU-mode rebuild completed in 3m55.78s (9 executed steps), then repackaged in 24.84s. The final ZIP passed default Metal/Graphite and explicit OpenGL/Ganesh GUI/WebGL1 checks on Radeon RX 6800 XT. Hardware compositing/rasterization were enabled and the expected pixel was returned with GL error 0 in both short runs. Non-Metal GeForce 320M testing remains pending because the MacBook was unavailable. See electron/validation/45.0.0.json for the final archive hash and exact coverage.

## GeForce 320M follow-up — 2026-10-23

The exact published ZIP (SHA-256 2807aaa78ef959402e62cb5cc348d37809d0a77470c2b1883a70ccd6ae0fd1ed) was checked on the non-Metal OCLP MacBookPro7,1 with macOS 12.7.6. Launched through the GUI session with a separate profile and no graphics switches. It automatically chose ANGLE OpenGL 3.3, exposing GLES2, with GaneshGL. Hardware compositing/rasterization enabled. WebGL1 pixel [51,102,204,255], error 0; a distinct WebGL2 canvas returned null as expected. No child-process exit events during the short check. This resolves the legacy-hardware validation item left pending in the initial publication. No installed app or existing profile was changed.
