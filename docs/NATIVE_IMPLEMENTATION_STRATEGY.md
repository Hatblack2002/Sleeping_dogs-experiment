# Native implementation strategy — Sleeping Dogs: Definitive Edition

## Product definition

The target is a real Android ARM64 application that executes translated/recompiled game code directly on the device. It must not start a Windows compatibility container or merely hide a launcher behind a native-looking interface.

The original retail game assets and required user-supplied files may remain external and be imported locally. Their absence from the APK is not, by itself, evidence that the app is a container. The key distinction is what executes the game logic:
- **Static recompilation:** functions from the original executable are translated ahead of time into ARM64 native machine code; the Android process calls that generated code and supplies the game data at runtime.
- **Compatibility/container launcher:** the app launches or embeds a runtime that interprets/translates the original Windows executable, such as Wine/Box64 or a DXVK graphics path.
- **Thin wrapper:** the app merely opens another installed app or runtime.

Only the first route is a candidate for the project's stated target. A Vulkan renderer or JNI library alone does not establish which architecture is present.

## Work plan and decision gates

### Gate 1 — Establish the actual community APK architecture
1. Preserve the exact APK's SHA-256 and package/version metadata.
2. Inventory all DEX, assets, and ABI libraries; inspect ELF dependencies, symbols, and strings.
3. Trace startup from Android entry activity through JNI/native entry points to the game execution path.
4. Look specifically for evidence of generated ARM64 code and game-specific executable symbols; distinguish this from a generic runtime library.
5. Trace all references to Wine, Box64, FEX, DXVK, external app launches, and user-provided executable paths.
6. Record conclusions as confirmed, contradicted, or unknown. Do not infer architecture from APK size, FPS claims, or a library name alone.

### Gate 2 — Obtain reproducible implementation inputs
1. Locate the developer's canonical source repository or an explicit source release.
2. Verify build scripts, generated-code provenance, dependencies, license/provenance, and supported game version.
3. If the source is not public, do not represent reverse-engineering of a compiled APK as equivalent to obtaining a maintainable source base. A compiled APK can help characterize interfaces and required files, but cannot substitute for generated code and its build pipeline.
4. Keep proprietary executable/assets out of the public repository; use CI secrets or a local import step only where legally appropriate.

### Gate 3 — Build native Android integration
1. Build real ARM64 game/recompiled code with Android NDK and a reproducible CI workflow.
2. Implement Android platform services required by the codebase: lifecycle, storage/file access, audio, input/touch mapping, threading, and graphics presentation.
3. Choose Vulkan/OpenGL ES based on the actual renderer boundary and available code, not by adding DXVK to an otherwise empty Android wrapper.
4. Add automated build and artifact checks; fail CI if the job only packages Java/Kotlin or an empty JNI stub.

### Gate 4 — Validate on the target device
Test in sequence: APK installation, process startup, data discovery, renderer initialization, first scene, input, sustained gameplay, save/load, and thermal/memory stability. Report each stage separately. Do not call the port playable until actual gameplay has been observed on hardware.

## Current known blockers

- The public TheoryEngine repository is an incomplete Windows/D3D11-oriented reverse-engineering reference, not a complete Android-ready engine.
- The community's claimed static recompilation remains unverified at source/build level.
- The earlier APK audit's `libnfsmw.so` and DXVK libraries do not prove that it contains Sleeping Dogs game code. Its architecture must be traced.
- The project has no verified native APK or target-device gameplay test yet.

## Immediate next action

Use the exact APK supplied by the user as an evidence sample, trace its startup and native execution path, and classify it. Then pursue the canonical source/build pipeline for a true static recompilation. Do not create another launcher APK as a substitute for the native engine.
