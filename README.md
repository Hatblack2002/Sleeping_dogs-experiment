# Sleeping Dogs — native Android port experiment

This repository targets a **separately built, optimized native Android ARM64 implementation**. The reference APK is for architectural study only; it is not a runtime dependency or the implementation base.

## Hard architecture rules

- The game logic must execute as native ARM64 code in the Android process.
- **No Wine, Winlator, Box64, or FEX.** No Windows executable launched through a compatibility runtime, and no remote streaming.
- Do not copy or depend on the reference APK's `libnfsmw.so` or bundled DXVK libraries.
- Do not adopt DXVK as the project's renderer. Select a direct Android graphics backend after the actual native code/API boundary is verified.
- User-owned retail game files may be imported locally. Do not commit proprietary game assets/executables to this public repository without redistribution rights.
- CI must compile real native project code; an empty JNI library or launcher is not a deliverable.

## Current evidence and status

- A reference Android APK has been statically inspected. Its `NativeActivity`, large AArch64 library, and generated-looking guest-function symbols are consistent with a **likely static-recompilation-style architecture**. Its main library is named `libnfsmw.so`; the audit did not prove that its generated code belongs to Sleeping Dogs: Definitive Edition.
- The APK bundles DXVK D3D11/DXGI libraries and a Freedreno Vulkan driver. This is useful to understand the reference's graphics route, but the project will not inherit those binaries or depend on that stack.
- No canonical source repository or reproducible source/build pipeline for the community build has been verified.
- No native game APK built from verified source or successful target-device gameplay test currently exists in this repository.
- The Galaxy S20 FE has Snapdragon 865 / Adreno 650 and Android 13, but its approximately 5.76 GiB usable RAM is below the reference author's stated 8 GB minimum. This is a risk to measure, not proof of incompatibility.

## Work plan

1. Resolve source/provenance and verify the target game-code identity.
2. Establish an independent, reproducible ARM64 build path without Windows compatibility runtimes.
3. Integrate the required Android-native lifecycle, storage, input, audio, and graphics services.
4. Establish repeatable performance baselines, then optimize measured CPU, GPU, memory, I/O, and thermal bottlenecks.
5. Verify installation, game-data discovery, renderer initialization, real gameplay, input, save/load, memory, and thermal stability on the target device.

## Documentation

- [Reference APK static audit — 2026-10-25](docs/REFERENCE_APK_AUDIT_2026-10-25.md)
- [Community recompilation verification status](docs/COMMUNITY_RECOMP_STATUS.md)
- [Native route decision](docs/NATIVE_ROUTE_DECISION.md)
- [Native implementation strategy](docs/NATIVE_IMPLEMENTATION_STRATEGY.md)
- [Native optimization and benchmarking plan](docs/OPTIMIZATION_PLAN.md)
- [Native feasibility gate](docs/FEASIBILITY_GATE.md)
- [Renderer/platform audit](docs/RENDERER_PLATFORM_AUDIT.md)

## Static APK audit automation

The [Analyze Android runner APK workflow](.github/workflows/analyze-native-apk.yml) downloads a Google Drive APK share link, decodes Android resources with Apktool, decompiles DEX bytecode with JADX, inventories native libraries, and reports ELF dependencies, exported symbols, and selected strings. It publishes analysis reports and inventories only, not the APK or reconstructed source. Static findings do not establish source provenance or prove gameplay.

To run it: open **Actions → Analyze Android runner APK (native-port research) → Run workflow**, then supply an accessible Google Drive share URL if the default link is no longer valid.
