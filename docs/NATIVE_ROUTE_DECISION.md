# Native Android route decision — Sleeping Dogs: Definitive Edition

**Decision date:** 2026-10-25  
**Target:** Android ARM64, directly executed native code. Winlator, Wine, Box64, DXVK, remote streaming, and a Windows launcher are explicitly out of scope.

## Decision

The deliverable is a genuine native Android port, not a wrapper or a compatibility-layer launcher marketed as native. However, “native” does not mean the original game source must be present: a static recompilation can translate the original executable's functions into ARM64 machine code and load the user's legally owned game data at runtime. That is materially different from a container that runs the original Windows executable through Wine/Box64/DXVK.

The community APK must be classified from evidence, not its branding. If it is a launcher/container that accepts retail game files and delegates execution to another runtime, it is not the implementation target. If it contains generated ARM64 code corresponding to the game's executable and directly executes it in-process, it may be a useful technical reference, but its APK alone is not a reproducible source foundation.

The project should pursue a reproducible native implementation from verified source or generated ARM64 recompilation output. Do not spend further effort on wrapper UI or treat an APK's large native library as proof of the game's identity.

## Candidate assessment

### A. Community static recompilation — highest-priority lead, not yet reproducible

A newer Reddit post by `u/Lazy_Persimmon3059` states that the developer has a Sleeping Dogs: Definitive Edition Android build and says it is a **static recompilation** of `sdhdship.exe` and `bink2w64.dll`, not a Winlator/Wine/Box64/FEX launch. The author claims roughly 194,020 game functions were recompiled to ARM64, says the source is about 1.5 GB, and says a GitHub repository will be posted after optimization. These are the author's statements, not independently verified engineering evidence.

Source post: https://www.reddit.com/r/AndroidNativePorts/comments/1x4ji39/finished_and_optimized_a_few_ports_of_different/

The older DroidPorts entry still says there is no public source or download and has not reviewed the APK: https://droidports.com/games/sleeping-dogs-definitive-edition/. It may simply be stale relative to the newer announcement.

**Assessment:** This is now the strongest lead and is more promising than building from TheoryEngine. The right move is to locate the canonical GitHub repository when the developer publishes it, then inspect its build scripts and native libraries. Do not use APK mirrors or a prebuilt APK as a substitute for source inspection. A claimed static recompilation is not proven native merely by its name or reported FPS.

**Verification gate:**
1. Track the author's promised GitHub publication and identify the canonical repository; no matching public GitHub repository was found in this search pass as of 2026-10-25.
2. Inspect source code, generated ARM64 code, build scripts, and dependencies; check for calls to Wine/Winlator/Box64/FEX or Windows binary launch paths.
3. Inspect licensing/provenance and ensure no proprietary retail assets or executables are redistributed.
4. Reproduce the ARM64 build in CI from source.
5. Verify install, startup, game-data loading, and gameplay on hardware. The author's post lists RedMagic 9 Pro/11S Pro as tested and claims Adreno 6xx+ may work; it does not establish support for this project's Galaxy S20 FE Snapdragon 865.

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
