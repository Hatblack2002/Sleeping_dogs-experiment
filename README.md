# Sleeping Dogs — native Android port experiment

This repository targets a **native Android ARM64 implementation**. The objective is not to disguise a container or launcher as a native app; the project must execute game logic compiled/recompiled for ARM64 on Android.

## Current state

- The public TheoryEngine repository is an incomplete reverse-engineered reference, not the original complete game engine.
- A reference Android APK has now been statically inspected. Its `NativeActivity`, large AArch64 library, and generated-looking guest-function symbols support a **likely static-recompilation-style architecture**. Its main library is named `libnfsmw.so`, however, and the audit did not prove that the generated code belongs to Sleeping Dogs: Definitive Edition.
- The APK bundles DXVK D3D11/DXGI libraries and a Freedreno Vulkan driver. DXVK alone does not prove game logic is executed through Wine/Box64/FEX; its actual role must be traced against the project's graphics requirements.
- No canonical source repository or reproducible source/build pipeline for the community build has been verified.
- No native game APK built from verified source, playable build produced by this repository, or successful target-device gameplay test is currently available.
- The target Galaxy S20 FE has Snapdragon 865 / Adreno 650 and Android 13, but its approximately 5.76 GiB usable RAM is below the reference author's stated 8 GB minimum. This is a risk to test, not a proven incompatibility.

## Next gates

1. Resolve the `libnfsmw.so` naming mismatch and trace the native library's startup and game-data loading.
2. Obtain and verify the author's canonical source/build pipeline, game version, generated-code provenance, and relevant rights.
3. Build real ARM64 game/recompilation code reproducibly with Android NDK/CI; do not substitute an empty JNI stub or a launcher.
4. Keep proprietary retail game files out of this public repository unless redistribution rights are established.
5. Test installation, launch, data discovery, renderer initialization, first scene, touch/gamepad input, sustained gameplay, save/load, memory pressure, and thermal behavior on the target device.

## Evidence and research

- [Reference APK static audit — 2026-10-25](docs/REFERENCE_APK_AUDIT_2026-10-25.md)
- [Community recompilation verification status](docs/COMMUNITY_RECOMP_STATUS.md)
- [Native route decision and candidate verification plan](docs/NATIVE_ROUTE_DECISION.md)
- [Native implementation strategy and architecture gates](docs/NATIVE_IMPLEMENTATION_STRATEGY.md)
- [Native feasibility gate](docs/FEASIBILITY_GATE.md)
- [Renderer/platform audit](docs/RENDERER_PLATFORM_AUDIT.md)
- [Compatibility research (not the target deliverable)](docs/COMPATIBILITY_ROUTE.md)

## Static APK audit automation

The [Analyze Android runner APK workflow](.github/workflows/analyze-native-apk.yml) downloads a Google Drive APK share link, decodes Android resources with Apktool, decompiles DEX bytecode with JADX, inventories native libraries, and reports ELF dependencies, exported symbols, and selected strings. It publishes the analysis report and inventories only, not the APK or reconstructed source. Static findings are evidence for manual review; they do not establish source provenance or prove gameplay.

To run it: open **Actions → Analyze Android runner APK (native-port research) → Run workflow**, then supply an accessible Google Drive share URL if the default link is no longer valid.
