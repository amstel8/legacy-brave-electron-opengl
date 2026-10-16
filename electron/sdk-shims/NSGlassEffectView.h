/*
    NSGlassEffectView.h
    Application Kit
    Copyright (c) 2025, Apple Inc.
    All rights reserved.

    FX-APPKIT-MACOS26-SHIM: this header is not part of the SDK 15.5 that this
    fork builds against. The declarations below were copied verbatim from the
    macOS 26.5 SDK so that tip-of-tree Chromium code guarded by
    `@available(macOS 26, *)` still compiles. None of these APIs exist at
    runtime on the macOS 12 target; every call site in Chromium is reachable
    only via explicit @available() guards.
*/


#import <AppKit/NSView.h>

NS_HEADER_AUDIT_BEGIN(nullability, sendability)
APPKIT_API_UNAVAILABLE_BEGIN_MACCATALYST

typedef NS_ENUM(NSInteger, NSGlassEffectViewStyle) {
    /// Standard glass effect style.
    NSGlassEffectViewStyleRegular,
    /// Clear glass effect style.
    NSGlassEffectViewStyleClear
} API_AVAILABLE(macos(26.0)) NS_SWIFT_NAME(NSGlassEffectView.Style);


/// A view that embeds its content view in a dynamic glass effect.
///
/// FX-APPKIT-MACOS26-SHIM: weak_import so the linker tolerates the missing
/// OBJC_CLASS_$_NSGlassEffectView symbol in the SDK 15.5 AppKit.tbd
/// (Chromium subclasses this class in browser_native_widget_mac.mm).
API_AVAILABLE(macos(26.0))
__attribute__((weak_import))
@interface NSGlassEffectView: NSView
/// The view to embed in glass.
@property (nullable, strong) __kindof NSView *contentView;

/// The amount of curvature for all corners of the glass.
@property CGFloat cornerRadius;

/// The color the glass effect view uses to tint the background and glass effect toward.
@property (nullable, copy) NSColor *tintColor;

/// The style of glass this view uses.
@property NSGlassEffectViewStyle style;
@end

/// A view that efficiently merges descendant glass effect views together when they are within a specified proximity to each other.
API_AVAILABLE(macos(26.0))
@interface NSGlassEffectContainerView: NSView
/// The view that contains descendant views to merge together when in proximity to each other.
@property (nullable, strong) __kindof NSView *contentView;

/// The proximity at which the glass effect container view begins merging eligible descendent glass effect views.
@property CGFloat spacing;
@end

API_UNAVAILABLE_END
NS_HEADER_AUDIT_END(nullability, sendability)