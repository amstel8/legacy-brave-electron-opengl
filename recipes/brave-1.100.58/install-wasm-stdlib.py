#!/usr/bin/env python3
"""Install the WASM target libraries for the pinned Chromium Rust toolchain."""

import argparse
import hashlib
import os
import subprocess
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

RUST_PACKAGE = "8a9dd7abdf013ec10cfeaaa3685feba18ef1c90c-1-llvmorg-24-init-14453-ge063be79"
OVERLAY_SHA256 = "0a6c83437d269b833542df4dc1ad52c15e8722009b0a83cab1fcfb59e74f0ba8"
TARGET = "wasm32-unknown-unknown"
PREFIX = ("lib", "rustlib", TARGET)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--src", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()

    src = args.src.resolve()
    rust = src / "third_party/rust-toolchain"
    version = subprocess.check_output([rust / "bin/rustc", "-Vv"], text=True)
    if RUST_PACKAGE not in version or "host: x86_64-apple-darwin\n" not in version:
        parser.error("Expected the pinned Chromium compiler for Intel macOS")
    with args.archive.open("rb") as archive_file:
        if hashlib.file_digest(archive_file, "sha256").hexdigest() != OVERLAY_SHA256:
            parser.error("The auxiliary archive SHA-256 does not match Brave EXTRA_DEPS")

    linker = src / "third_party/llvm-build/Release+Asserts/bin/lld"
    linker_link = rust / "bin/rust-lld"
    target = rust.joinpath(*PREFIX)
    if not os.access(linker, os.X_OK):
        parser.error("Chromium's native LLVM linker is missing")
    if not linker_link.is_symlink() and linker_link.exists():
        parser.error("rust-lld already exists; inspect it before changing it")
    if linker_link.is_symlink() and linker_link.resolve() != linker.resolve():
        parser.error("rust-lld points to a different linker")
    if target.exists() or target.is_symlink():
        parser.error(f"{target} already exists; remove a stale copy before reinstalling")

    with tempfile.TemporaryDirectory(dir=target.parent) as temp:
        with tarfile.open(args.archive, "r:xz") as archive:
            members = []
            for member in archive:
                parts = PurePosixPath(member.name).parts
                if parts[:len(PREFIX)] != PREFIX:
                    continue
                if ".." in parts or not (member.isdir() or member.isfile()):
                    parser.error(f"Unexpected entry in the WASM target: {member.name}")
                members.append(member)
            if not any(member.isfile() for member in members):
                parser.error("The auxiliary archive contains no WASM target files")
            archive.extractall(temp, members=members, filter="data")
        Path(temp).joinpath(*PREFIX).rename(target)

    if not linker_link.is_symlink():
        linker_link.symlink_to(os.path.relpath(linker, linker_link.parent))
    print(f"Installed {TARGET}; add {rust / 'bin'} to PATH for compilation")


if __name__ == "__main__":
    main()
