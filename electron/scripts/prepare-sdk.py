#!/usr/bin/env python3
"""Apply the existing SDK 15.5 compatibility declarations to a private SDK copy."""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--sdk', required=True, type=Path)
args = parser.parse_args()
sdk = args.sdk.resolve()
frameworks = sdk / 'System/Library/Frameworks'
assets = Path(__file__).resolve().parents[1] / 'sdk-shims'
definitions = json.loads((assets / 'definitions.json').read_text())

def append_once(relative, marker, extra):
    f = frameworks / relative
    text = f.read_text()
    if marker not in text:
        f.write_text(text + '\n' + extra + '\n')

append_once('CoreGraphics.framework/Headers/CGImage.h',
            '#define kCGImageByteOrder16Host', '''#if defined(__BIG_ENDIAN__)
#define kCGImageByteOrder16Host kCGImageByteOrder16Big
#define kCGImageByteOrder32Host kCGImageByteOrder32Big
#else
#define kCGImageByteOrder16Host kCGImageByteOrder16Little
#define kCGImageByteOrder32Host kCGImageByteOrder32Little
#endif''')
append_once('ApplicationServices.framework/Frameworks/HIServices.framework/Headers/AXConstants.h',
            '#define kAXARIAAtomicAttribute', definitions['ax'])
append_once('AppKit.framework/Headers/NSAccessibilityConstants.h',
            '#define NSAccessibilitySearchTextKey', definitions['nsaccessibility'])
glass = frameworks / 'AppKit.framework/Headers/NSGlassEffectView.h'
if not glass.exists():
    glass.write_text((assets / 'NSGlassEffectView.h').read_text())
append_once('AppKit.framework/Headers/AppKit.h', '#import <AppKit/NSGlassEffectView.h>',
            '#import <AppKit/NSGlassEffectView.h>')
f = frameworks / 'AuthenticationServices.framework/Headers/ASAuthorizationWebBrowserPublicKeyCredentialManager.h'
s = f.read_text()
if 'isDeviceConfiguredForPasskeys' not in s:
    pos = s.rfind('@end')
    if pos < 0:
        raise SystemExit('Unexpected passkey manager header')
    s = s[:pos] + '+ (BOOL)isDeviceConfiguredForPasskeys API_AVAILABLE(macos(26.2));\n\n' + s[pos:]
    f.write_text(s)
print('SDK compatibility declarations prepared:', sdk)
