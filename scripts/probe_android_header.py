#!/usr/bin/env python3
"""Diagnostic C++17 syntax probe against the upstream umbrella header."""
import argparse
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compiler", required=True)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--sysroot", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    sysroot = args.sysroot.resolve()
    if not source.is_dir():
        parser.error(f"source directory does not exist: {source}")
    if not sysroot.is_dir():
        parser.error(f"Android NDK sysroot does not exist: {sysroot}")

    command = [
        args.compiler, "--target=aarch64-linux-android26",
        f"--sysroot={sysroot}", "-std=c++17", "-fsyntax-only",
        "-I", str(source), "-x", "c++", "-",
    ]
    probe = '#include "theory.hh"\nint main() { return 0; }\n'
    result = subprocess.run(
        command, input=probe, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, check=False,
    )
    lines = result.stdout.splitlines()
    excerpt = lines[:100]
    status = "PASS" if result.returncode == 0 else "FAIL"
    report = [
        "# Android ARM64 header compatibility probe", "",
        f"- Status: **{status}**",
        "- Target: aarch64-linux-android26",
        "- Language mode: C++17",
        "- Operation: syntax-only include of upstream theory.hh",
        "- This is not a full engine build and does not produce an APK.",
        f"- Compiler exit code: {result.returncode}",
        f"- Diagnostic lines: {len(lines)}", "",
        "## Compiler diagnostics", "",
        *(excerpt if excerpt else ["No diagnostics."]),
    ]
    if len(lines) > len(excerpt):
        report.extend(["", f"Output truncated to first {len(excerpt)} lines."])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    # A compiler failure is diagnostic data, not an audit-workflow failure.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
