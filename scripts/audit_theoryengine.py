#!/usr/bin/env python3
"""Create a reproducible, conservative feasibility report for TheoryEngine."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import re

TEXT_SUFFIXES = {".h", ".hh", ".hpp", ".c", ".cc", ".cpp", ".cxx", ".cmake", ".txt", ".md", ".vcxproj", ".sln"}
PATTERNS = {
    "Direct3D 11 headers or symbols": re.compile(r"\b(d3d11\.h|ID3D11\w*|D3D11_\w+)\b", re.I),
    "Windows API / platform headers": re.compile(r"\b(windows\.h|Windows\.h|__debugbreak|__forceinline|WIN32|_WIN32)\b"),
    "x86/x64 assumptions": re.compile(r"\b(x64|x86_64|AMD64|_M_X64|__x86_64__)\b", re.I),
    "Windows build system references": re.compile(r"\b(msbuild|\.vcxproj|Visual Studio|DirectX SDK)\b", re.I),
    "Hard-coded PC platform defines": re.compile(r"^\s*#\s*define\s+(THEORY_WINDOWS|THEORY_PLATFORM_PC)\b", re.M),
}
SKIP_DIRS = {".git", ".vs", "build", "out", "bin", "obj"}

def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--revision", default="unknown")
    args = parser.parse_args()

    root = args.source.resolve()
    if not root.is_dir():
        raise SystemExit(f"Source directory does not exist: {root}")

    files = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)

    counts: Counter[str] = Counter()
    examples: dict[str, list[str]] = {key: [] for key in PATTERNS}
    for path in files:
        text = read_text(path)
        rel = path.relative_to(root).as_posix()
        for label, pattern in PATTERNS.items():
            matches = list(pattern.finditer(text))
            if matches:
                counts[label] += len(matches)
                if len(examples[label]) < 12:
                    line_numbers = [text.count("\n", 0, match.start()) + 1 for match in matches[:3]]
                    examples[label].append(f"- `{rel}` (line(s) {', '.join(map(str, line_numbers))}; {len(matches)} match(es))")

    readme = read_text(root / "README.md")
    theory = read_text(root / "theory.hh")
    cmake_files = [p for p in files if p.name.lower() in {"cmakelists.txt", "cmakepresets.json"}]
    license_files = [p for p in root.iterdir() if p.name.lower().startswith(("license", "licence", "copying"))]
    license_status = "A license-like file exists; inspect its scope and terms manually." if license_files else "No top-level LICENSE/LICENCE/COPYING file found. This is not permission to reuse the code."

    lines = [
        "# Sleeping Dogs Android feasibility audit",
        "",
        f"- Upstream: https://github.com/SDmodding/TheoryEngine",
        f"- Audited revision: `{args.revision}`",
        f"- Source files scanned: {len(files)}",
        f"- CMake entry points detected: {len(cmake_files)}",
        "",
        "## Executive finding",
        "",
        "This is a **static source scan**, not a successful Android build. The upstream project describes itself as a work-in-progress reimplementation based on Sleeping Dogs: Definitive Edition debug symbols, and its umbrella header declares PC/Windows platform assumptions. It should not be treated as an Android-ready engine or as the original game's complete source.",
        "",
        "## Licensing and provenance gate",
        "",
        license_status,
        "",
        "The upstream README states that it does not include a license because parts may be identical or similar to the original. Do not copy, vendor, redistribute, or make a derivative release from this code until the applicable rights and permissions have been reviewed. Keep this experiment limited to public-source inspection and independently authored tooling meanwhile.",
        "",
        "## Detected platform indicators",
        "",
    ]
    for label in PATTERNS:
        lines.append(f"### {label}: {counts[label]} occurrence(s)")
        lines.extend(examples[label] or ["- No matches found by this limited pattern scan."])
        lines.append("")

    lines += [
        "## Build-system observations",
        "",
        "- CMake entry points detected: " + (", ".join(f"`{p.relative_to(root).as_posix()}`" for p in cmake_files[:20]) if cmake_files else "none detected by filename"),
        "- Umbrella header has THEORY_WINDOWS / THEORY_PLATFORM_PC definitions: " + ("yes" if "THEORY_WINDOWS" in theory and "THEORY_PLATFORM_PC" in theory else "not detected"),
        "- Umbrella header includes Direct3D 11 conditionally under PC platform defines: " + ("yes" if "d3d11.h" in theory else "not detected"),
        "",
        "## What this means for Android",
        "",
        "1. A native Android port requires a deliberate platform abstraction, not just changing the target architecture.",
        "2. Windows process/file/timer/string implementations and Direct3D rendering paths must be replaced or isolated behind portable interfaces.",
        "3. Physics, streaming, resource formats, animation, audio, UI, and gameplay integration need separate dependency and runtime audits.",
        "4. This scan cannot establish whether the engine is complete enough to load the retail game, nor whether an ARM64 renderer can preserve the original content.",
        "",
        "## Next engineering gate",
        "",
        "Resolve the source-use permission question first. Then build an isolated ARM64 Android proof of concept around independently authored platform/rendering interfaces, and only integrate components whose provenance and portability are clear. Do not claim a playable port until an APK is installed and gameplay is verified on hardware.",
        "",
        "## Method",
        "",
        "The workflow shallow-clones the upstream repository into the ephemeral GitHub Actions runner, scans text source files for a small set of platform indicators, and publishes this report as an artifact. It does not upload game files, commit upstream source, or modify the user's game installation.",
        "",
    ]
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.output} ({len(files)} files scanned)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
