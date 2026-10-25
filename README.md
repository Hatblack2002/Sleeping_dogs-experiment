# Sleeping Dogs — native Android port experiment

This repository targets a **native Android ARM64 implementation**. Winlator, Wine, Box64, DXVK, and launching the Windows game are outside the deliverable.

## Current state

- The public TheoryEngine repository is an incomplete reverse-engineered reference, not the original complete game engine.
- A community developer has now publicly claimed to have a native ARM64 static recompilation of Sleeping Dogs: Definitive Edition, with source intended for a GitHub release after optimization. That is the most promising lead, but the source/release and reproducible build still need independent verification.
- The previous `android-wrapper/` launcher was a mistaken detour: it merely opened Winlator and did not run the game natively. Do not treat its APK as a project deliverable.
- No native game APK built from verified source, playable build produced by this repository, or successful device test is currently available.

## Native implementation gates

1. Verify a canonical source/release for the claimed ARM64 static recompilation and inspect its provenance.
2. Build from real engine/recompilation code with Android NDK/CI; reject any path that invokes Winlator, Wine, Box64/FEX, or DXVK to run the Windows executable.
3. Verify required retail game files are imported locally, not committed to this public repository.
4. Produce an installable APK in CI and verify it installs, launches, loads game data, and reaches gameplay on target hardware.

## Existing research

- [Native route decision and candidate verification plan](docs/NATIVE_ROUTE_DECISION.md)
- [Native feasibility gate](docs/FEASIBILITY_GATE.md)
- [Renderer/platform audit](docs/RENDERER_PLATFORM_AUDIT.md)
- [Compatibility research (not the target deliverable)](docs/COMPATIBILITY_ROUTE.md)

The native build is not considered successful until CI compiles actual native engine/recompilation implementation code. A successful Android wrapper build or static audit does not satisfy this requirement.
