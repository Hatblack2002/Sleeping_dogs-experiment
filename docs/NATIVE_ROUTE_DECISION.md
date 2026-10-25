# Native Android route decision — Sleeping Dogs: Definitive Edition

**Decision date:** 2026-10-25  
**Target:** Android ARM64, directly executed native code. Winlator, Wine, Box64, DXVK, remote streaming, and a Windows launcher are explicitly out of scope.

## Decision

Do not start by writing a new Android shell or by trying to cross-compile the existing TheoryEngine headers. The highest-value lead is to verify whether the reported community static-recompilation project has a real, obtainable source/release and reproducible build. Until its maintainers publish or provide verifiable source and build evidence, treat it as an **unverified lead, not an available implementation**.

If that lead cannot be verified, the current public code does not provide a practical, lawful, complete foundation for a playable native port. In that case, the project needs a new source foundation or a clean-room engine reimplementation, which is a substantial engine-development effort—not an NDK flag change.

## Candidate assessment

### A. Community static recompilation claim — investigate first, do not trust yet

DroidPorts lists a Sleeping Dogs: Definitive Edition “Android Native Port” and describes it as an alpha/static recompilation requiring the user's own PC game files, including `HKShip.exe`. The same page explicitly says there is **no public download**, no public source code, and that the listing has not been reviewed by DroidPorts.

Source: https://droidports.com/games/sleeping-dogs-definitive-edition/

**Assessment:** Potentially the shortest path *if and only if* an authentic maintainer, source repository, build instructions, or verifiable release can be located. The directory entry alone does not establish that the project exists in a reproducible form, that it supports the target device, or that it is safe. Do not download APKs from mirrors or build a project around an anonymous claim.

**Verification gate:**
1. Identify the actual maintainer and canonical project page.
2. Find source code or a signed/canonical release and build instructions.
3. Verify the code performs static recompilation/native ARM64 execution rather than calling a Windows compatibility layer.
4. Inspect licensing/provenance and required PC files.
5. Reproduce the ARM64 build in CI, then test startup and gameplay on hardware.

### B. SDmodding TheoryEngine — useful reverse-engineering reference, not a port foundation by itself

Upstream: https://github.com/SDmodding/TheoryEngine

The upstream README describes a work-in-progress reverse-engineered reimplementation guided by the retail debug symbols, explicitly says it is not a complete rewrite, and states the project is no longer under active public development. Its repository says it has no license because some portions may be identical or similar to original code. Its umbrella header documents C++17 and a 64-bit x64 target; the current Android NDK probe in this repository fails on the Windows/Direct3D 11 include path.

**Assessment:** Use its public documentation and independently verified technical observations as research leads only. Do not assume its headers constitute a complete game engine, do not treat a header syntax check as a port, and do not copy or redistribute code without resolving the rights issue. A clean-room implementation can use lawful, independently gathered behavioural knowledge, but must not silently inherit unlicensed implementation code.

### C. Reimplement the engine from scratch — technically possible in principle, not a shortcut

A real native port needs far more than an Android Activity and a renderer: executable/game logic, resource and archive loading, scene/world streaming, animation, physics, AI, scripting, audio, UI, save state, platform services, and a rendering backend. Sleeping Dogs is a large 3D open-world game. Replacing all of this from scratch is a multi-stage engine project and cannot honestly be represented as a quick APK build.

**Assessment:** Fallback only if a lawful, sufficiently complete engine/recompilation foundation cannot be obtained and the project accepts a long reverse-engineering/reimplementation programme.

## Non-negotiable architecture

- Native Android application package with an ARM64 native engine/runtime.
- Vulkan or OpenGL ES backend only after the actual renderer and dependency path is identified.
- The user's own legally acquired game files may be imported locally; proprietary game assets/executables must not be committed to this public repository.
- CI must compile real native engine/recompilation code, not only Java/Kotlin, an empty JNI library, a header probe, or a launcher.
- A build is not a playable port until it installs, starts, loads real game data, and reaches verified gameplay on the target device.
- No Winlator/Wine/Box64/DXVK execution path.

## Evidence and limitations

- DroidPorts listing (unverified lead; no source or public download stated): https://droidports.com/games/sleeping-dogs-definitive-edition/
- TheoryEngine repository and its own status/licensing statements: https://github.com/SDmodding/TheoryEngine
- Native-port definition and distinction from emulation: https://github.com/abduznik/awesome-android-native-ports

This report records a route decision, not a claim that an Android port exists or that gameplay has been achieved. The next engineering step is to verify candidate A from a canonical maintainer/source. Do not fabricate a substitute APK if that gate fails.
