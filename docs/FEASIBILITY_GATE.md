# Android feasibility gate — Sleeping Dogs: Definitive Edition

**Status: research-only; no Android build target or playable port exists in this repository.**

## Evidence collected

- Upstream reference: https://github.com/SDmodding/TheoryEngine
- The upstream tree currently contains 186 entries: 142 C/C++ header files (.h, .hh), one README, one .gitattributes, and 42 directory entries. The recursive Git tree reports no .cpp/.cc translation units, CMakeLists.txt, Visual Studio solution, or explicit build entry point.
- The upstream README describes TheoryEngine as a work-in-progress reverse-engineered reimplementation of the Sleeping Dogs: Definitive Edition engine based on released debug symbols. It explicitly says the project is not a complete rewrite.
- The upstream umbrella header requires C++17 and describes the target as 64-bit x64. It hard-defines THEORY_WINDOWS and THEORY_PLATFORM_PC, includes Direct3D 11, and includes PC-specific process/string implementations.
- The upstream README says the project has no license because parts may be identical or similar to the original game's code. This is a provenance and permission blocker for copying or redistributing the source.
- GitHub Actions run #2 completed successfully and scanned 143 source/text files. Run #3 also passed the regression tests and generated the audit artifact.

## Engineering conclusion

Changing the compiler target to Android ARM64 is not enough. There is no upstream build configuration or conventional compiled source implementation to cross-compile in this tree. Even if the headers compile in isolation, that would not establish a functioning engine, asset loading, rendering, gameplay, or compatibility with retail game data.

Do not copy TheoryEngine into this repository or ship a derivative build until source-use rights are clarified. The responsible next step is to investigate lawful, independently authored platform/rendering infrastructure and determine whether any separately licensed components can support a demonstrable Android proof of concept. Keep proprietary retail game data out of this public repository.

## Acceptance gates before calling this a port

1. A documented, legally reviewable source and asset provenance.
2. A reproducible ARM64 Android build target, not merely a header syntax check.
3. An APK artifact produced by CI.
4. Automated startup/smoke tests where technically possible.
5. A real-device installation and gameplay verification before claiming it is playable.

This document records feasibility evidence, not a claim that the game has been ported.
