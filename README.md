# Sleeping Dogs — native Android port experiment

This repository targets a **native Android ARM64 implementation**. Winlator, Wine, Box64, DXVK, and launching the Windows game are outside the deliverable.

## Current state

- The public TheoryEngine repository is an incomplete reverse-engineered reference, not the original complete game engine.
- Its public tree does not provide a complete buildable game implementation or the proprietary retail assets.
- The previous `android-wrapper/` launcher was a mistaken detour: it merely opened Winlator and did not run the game natively. Do not treat its APK as a project deliverable.
- No native game APK, playable build, or successful device test is currently available.

## Native implementation gates

1. Establish a legally usable, complete engine/source foundation and document provenance.
2. Identify the actual gameplay, simulation, resource-loading, and rendering implementations required to run the game.
3. Build a minimal Android ARM64 native target with the Android NDK from real engine code—not a launcher or placeholder.
4. Add a renderer backend compatible with Android (Vulkan or GLES as supported by the actual engine), then integrate input, audio, assets, and lifecycle.
5. Produce an installable APK in CI and verify it installs, launches, and reaches real gameplay on target hardware.

## Existing research

- [Native feasibility gate](docs/FEASIBILITY_GATE.md)
- [Renderer/platform audit](docs/RENDERER_PLATFORM_AUDIT.md)
- [Compatibility research (not the target deliverable)](docs/COMPATIBILITY_ROUTE.md)

The native build is not considered successful until CI compiles actual native engine implementation code. A successful Android wrapper build or static audit does not satisfy this requirement.
