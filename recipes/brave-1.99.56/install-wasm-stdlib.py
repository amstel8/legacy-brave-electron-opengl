#!/usr/bin/env python3
"""Install matching target-only WASM libraries on Intel macOS (no ARM host tools)."""
import argparse, hashlib, shutil, subprocess, tarfile
from pathlib import Path
parser=argparse.ArgumentParser()
parser.add_argument('--src',type=Path,required=True)
parser.add_argument('--archive',type=Path,required=True)
a=parser.parse_args();src=a.src.resolve();dest=src/'third_party/rust-toolchain'
assert '1edd55dcfcd573872c727fa3e086369a71661ee0' in subprocess.check_output([str(dest/'bin/rustc'),'-Vv'],text=True)
assert hashlib.sha256(a.archive.read_bytes()).hexdigest()=='654ed527c2a2bab8ef4aff8e0e2a494bdeadda3524730506a0e6ef9c18d5949b'
with tarfile.open(a.archive) as archive:
 for member in archive.getmembers():
  if not member.name.startswith('lib/rustlib/wasm32-unknown-unknown/'):continue
  assert '..' not in Path(member.name).parts and not member.issym() and not member.islnk()
  path=dest/member.name
  if member.isdir():path.mkdir(parents=True,exist_ok=True)
  elif member.isfile():
   path.parent.mkdir(parents=True,exist_ok=True)
   with archive.extractfile(member) as source,path.open('wb') as output:shutil.copyfileobj(source,output)
link=dest/'bin/rust-lld';target=src/'third_party/llvm-build/Release+Asserts/bin/lld'
assert target.is_file()
if not link.exists():link.symlink_to(target)
else:assert link.resolve()==target.resolve(), 'Inspect existing linker before replacing it'
print('WASM stdlib installed; native Chromium LLVM linker selected')
