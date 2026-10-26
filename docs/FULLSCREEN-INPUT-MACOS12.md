# macOS 12 fullscreen mouse-input fix

Status: built, validated without diagnostic injection, and installed on the OCLP MacBook on 2026-10-26.

## Reproduction

On an OCLP MacBookPro7,1 with GeForce 320M and macOS 12.7.6, the Avito “Для бизнеса” menu did not react to native hover/click in fullscreen. At the visible menu position (220,112), accessibility hit testing returned a native 1280×125 fullscreen layer. Visible tabs/address chrome occupied only 81 pixels, leaving an overlap over the first 44 pixels of page content. Lower page controls worked. Exiting fullscreen removed the extra layer and immediately restored this menu without restarting or reloading the page. This evidence localizes the failure to native fullscreen input interception; it does not establish a graphics-driver root cause.

The first diagnostic grid started below the affected strip and missed it. The refined fixture places small buttons inside the first 44 CSS pixels of the document. First-run infobars must be dismissed in the diagnostic profile; otherwise they move the fixture below the affected region.

## Patch

Apply `recipes/brave-1.98.60/chromium-macos12-fullscreen-input.patch` to the pinned Chromium 156 tree after the existing Brave patch series. It modifies only `immersive_mode_controller_cocoa.mm`. It is a post-release patch, absent from the original `v1.98.60-macos12-metal-opengl` archive.

On macOS 12, the fullscreen accessory host installs a local mouse-event monitor for its AppKit toolbar window. It forwards events only when their screen position is inside the browser content view and outside every visible titlebar accessory. Event coordinates are converted to the destination window. Button events use normal NSWindow dispatch, retaining native web-content hit testing; mouse moves use the hit-tested content subview because AppKit's tracking state still belongs to the toolbar window. Initial mouse moves can have no assigned event window or be associated with the main browser. For those cases, the monitor also verifies that the topmost native window at the screen position is exactly this fullscreen host before forwarding. The monitor is removed when the host moves or is destroyed.

This is an input-routing workaround, not a change to toolbar layout or graphics settings. It does not inject page JavaScript in normal use. Other macOS versions, real toolbar controls and other windows keep their existing event path. Covered events are left/right button down/up, move and drag. Scrolling, auxiliary mouse buttons, gestures and pointer-lock behavior are not rewritten; they are outside the validation claim.

## Build

Same Brave Core v1.98.60 and Chromium 156.0.8078.48 pins and official Release/PGO/ThinLTO settings as [the base recipe](UNIFIED-1.98.60.md). A single modified Objective-C++ object, its archive and the framework were rebuilt. The final incremental build succeeded in 5m11.42s (7 steps), exit 0.

Final candidate framework SHA-256: `417389265f27abdcadb264efb399c2fc0f878c7bb775cd2408703b5fe42636b0`.

Native pointermove logging exposed two distinct requirements: direct dispatch to the hit-tested content subview, and resolution of initially unassigned mouse events. The first click must not be used to activate hover handling; the regression check observes trusted pointermove targets before clicking.

## Native regression procedure

1. Open [the fixture](../tests/macos12/fullscreen-input-grid.html) in a separate Brave profile. Dismiss first-run infobars there and leave the everyday profile untouched.
2. Capture the actual window and locate the colored buttons on screen. Do not scale fullscreen captures using CGWindow bounds blindly: on Monterey they can exclude the toolbar while the image includes it.
3. Click visible button centers using physical input or `python3 tests/macos12/native-input.py click X Y`. Compare the logged trusted click and pointermove targets with the visible button IDs.
4. Repeat in an ordinary window, fullscreen with visible toolbar, fullscreen with hidden toolbar, restored toolbar, and normal window after fullscreen. Wait until the temporary fullscreen instruction is gone before capture.
5. Check the Avito business menu inside the top strip, plus the address bar, tab strip and context menu. Test further transitions and input modes before making wider stability claims.

The generic CoreGraphics helper supports `windows PID`, `move X Y`, `hover X Y`, `click X Y`, `rightclick X Y`, `drag X Y TO_X TO_Y`, and `key KEYCODE FLAGS`. macOS accessibility/input and window-capture permissions must already be available; the GUI session must be unlocked. It targets the active desktop, so run it only while deliberately testing that Mac.

## Baseline measurements

Eight native clicks were attempted per state in a separate profile on the MacBook. Validated original-build counts:

| State | Correct click targets |
| --- | ---: |
| Normal window | 8/8 |
| Fullscreen, toolbar visible | 5/8 |
| Fullscreen, toolbar hidden | 0/8 |
| Fullscreen, toolbar restored | 5/8 |
| Normal after fullscreen | 8/8 |

## Final validation and installation

The exact framework hash above passed **40/40 trusted native clicks and 40/40 trusted pre-click hovers** across the same five states, with 8/8 of each per state. The largest click-center rounding deviation was one CSS pixel. The process was launched normally and verified to have no `DYLD_INSERT_LIBRARIES` environment entry. [Machine-readable results](../tests/macos12/fullscreen-input-results.json).

A native right click in the affected strip reached the fixture's context-menu handler. After dismissing the native menu with Escape, a drag starting there produced trusted pointer-down and pointer-up events inside the page. Mouse focus of the address field, opening a tab, and returning to the original tab by clicking its tab-strip position also passed. These are short functional checks, not a full input-mode matrix.

The separate test profile encountered an Avito IP restriction during the last site reload, so that page was not treated as a successful final check. After installation, the existing signed-in stable session loaded Avito normally. Native hover at the previously blocked business menu position opened its dropdown in fullscreen; a subsequent native click also reached the menu. The signed-in avatar remained visible.

The installed framework was verified against the build hash. The stable profile directory was retained; the prior application and complete profile were backed up, with twelve important profile files verified before replacement. No debugging port or diagnostic library was added to the everyday browser. The bundle version remains `156.1.98.0`; this is an additional compatibility patch over the same source tag.

The original published release archive is unchanged and does not contain this post-release fix. These short checks do not establish extended browsing stability or performance.
