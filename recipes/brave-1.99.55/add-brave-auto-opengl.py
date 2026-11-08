#!/usr/bin/env python3
"""Add early non-Metal OpenGL selection to an already patched Brave checkout."""
import argparse
import difflib
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--src', required=True, type=Path)
parser.add_argument('--patch', type=Path)
args = parser.parse_args()
src = args.src
originals = {}

def edit(name, before, after):
    path = src / name
    text = path.read_text()
    originals.setdefault(name, text)
    if after in text:
        return
    if text.count(before) != 1:
        raise SystemExit(f'Unexpected source layout: {name}')
    path.write_text(text.replace(before, after, 1))

edit('chrome/app/chrome_main_mac.h',
     'void SetUpBundleOverrides();',
     'void SetUpBundleOverrides();\n\n'
     '// Select ANGLE OpenGL before GPU initialization when no Metal device exists.\n'
     'void MaybeSelectOpenGLOnMac();')
edit('chrome/app/chrome_main_mac.mm',
     '#import <Cocoa/Cocoa.h>',
     '#import <Cocoa/Cocoa.h>\n#import <Metal/Metal.h>')
edit('chrome/app/chrome_main_mac.mm',
     'void SetUpBundleOverrides() {',
     '''void MaybeSelectOpenGLOnMac() {
  auto* command_line = base::CommandLine::ForCurrentProcess();
  if (command_line->HasSwitch(switches::kProcessType) ||
      command_line->HasSwitch("use-angle") ||
      command_line->HasSwitch("use-gl") ||
      command_line->HasSwitch("disable-gpu")) {
    return;
  }

  @autoreleasepool {
    id<MTLDevice> device = MTLCreateSystemDefaultDevice();
    if (!device) {
      // Keep GPU compositing through ANGLE/CGL and the Ganesh path.
      command_line->AppendSwitchASCII("use-angle", "gl");
    }
  }
}

void SetUpBundleOverrides() {''')
edit('chrome/app/chrome_main.cc',
     '  SetUpBundleOverrides();',
     '  MaybeSelectOpenGLOnMac();\n  SetUpBundleOverrides();')
edit('chrome/BUILD.gn',
     '    if (is_component_build) {\n      frameworks = [ "Carbon.framework" ]\n    }',
     '    frameworks = [ "Metal.framework" ]\n'
     '    if (is_component_build) {\n      frameworks += [ "Carbon.framework" ]\n    }')
print('Automatic non-Metal OpenGL selection applied.')

if args.patch:
    chunks = []
    for name, before in originals.items():
        after = (src / name).read_text()
        if before != after:
            chunks.append(f'diff --git a/{name} b/{name}\n')
            chunks.extend(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile=f'a/{name}', tofile=f'b/{name}'))
    args.patch.write_text(''.join(chunks))
