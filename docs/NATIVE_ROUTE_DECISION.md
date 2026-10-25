# Native Android route decision — Sleeping Dogs: Definitive Edition

**Decision date:** 2026-10-25  
**Target:** Android ARM64 with directly executed native code. Wine, Winlator, Box64, FEX, DXVK-as-a-project-dependency, remote streaming, and a Windows launcher are out of scope.

## User requirement

The reference APK is for **study only**. The project must not depend on that APK or its binaries, and must not run the game through Wine/Winlator/Box64/FEX. The objective is a separately built, optimized Android ARM64 implementation.

## Decision

Pursue a reproducible native implementation from verified source or generated ARM64 recompilation output. The reference APK can inform the architecture, expected data import, lifecycle, graphics requirements, and performance test design, but it is not the source foundation and must not be treated as a runtime dependency.

A static recompilation can translate the target executable's functions ahead of time into ARM64 machine code; the resulting Android process executes that code directly while loading the user's legally owned game data. This differs from launching the original Windows executable through a compatibility runtime. We must verify the implementation's provenance and generated-code identity rather than trusting a label, APK size, or FPS claim.

The user specifically excludes Wine/Box64 execution. DXVK is a graphics API translation layer, not by itself proof of Wine/Box64 execution; nevertheless, this project will **not adopt the reference APK's DXVK stack as a shortcut**. A native Android graphics boundary should be selected from the verified code available, preferably Vulkan if technically feasible, or OpenGL ES if the real source constraints justify it.

## Candidate assessment

### A. Community static recompilation — research lead only, not a project dependency

A Reddit post by `u/Lazy_Persimmon3059` says the developer has an Android build and describes a static recompilation of `sdhdship.exe` and `bink2w64.dll`, with about 194,020 game functions translated to ARM64. These are author claims, not independently verified source-level facts.

Source: https://www.reddit.com/r/AndroidNativePorts/comments/1x4ji39/finished_and_optimized_a_few_ports_of_different/

The reference APK static audit found `NativeActivity`, a large ARM64 library named `libnfsmw.so`, guest-function-looking symbols, and bundled DXVK libraries. That evidence supports a likely static-recompilation-style architecture, but the library-name mismatch and absence of a canonical source/build pipeline remain unresolved. The APK is useful to study, not a binary dependency or a substitute for source.

### B. SDmodding TheoryEngine — research reference, not a port foundation by itself

Upstream: https://github.com/SDmodding/TheoryEngine

The upstream README describes a work-in-progress reverse-engineered reimplementation, not a complete rewrite. The public tree is primarily headers, Windows/D3D11/x64-oriented, has no conventional compiled source/build entry point, and states there is no license due to possible similarity with original code.

Use lawful public documentation and independently verified behavioral observations as research leads only. Do not copy/redistribute unlicensed code or call a header probe a port.

### C. Independent engine/reimplementation — fallback, not a shortcut

A complete implementation needs game logic, resource/archive loading, world streaming, animation, physics, AI, scripting, audio, UI, saves, Android lifecycle and rendering. This is a major reverse-engineering effort. It is viable only as a staged program with lawful inputs and clear milestone tests, not a quick empty JNI APK.

## Non-negotiable architecture

- Android APK with an ARM64 native process that directly executes the verified native game/recompiled code.
- No Wine/Winlator/Box64/FEX, no Windows executable launched by a compatibility runtime, and no streaming.
- Do not depend on the community APK or copy its binary libraries into the implementation.
- Do not adopt DXVK as the project's graphics backend; implement/adapt a direct Android renderer at a verified API boundary.
- The user's legally owned retail files may be imported locally; proprietary assets/executables must not be committed to this public repository unless redistribution rights are established.
- CI must compile actual native project code and validate the produced ARM64 artifacts, not only package Java/Kotlin or an empty JNI stub.
- A build is not a playable port until it installs, loads real game data, renders gameplay, and accepts input on the target device.

## Required gates

1. Verify lawful source and provenance for generated ARM64 code or define a lawful independent implementation route.
2. Trace game-code identity, data loading, startup, platform APIs and renderer boundaries.
3. Build a reproducible ARM64 Android target in CI without a Windows compatibility runtime.
4. Establish target-device baseline measurements before optimization.
5. Optimize measured bottlenecks, one subsystem at a time, and preserve before/after traces.
6. Verify installation, startup, data discovery, rendering, gameplay, input, save/load, memory, and thermal behavior on the Galaxy S20 FE.

See [native optimization plan](OPTIMIZATION_PLAN.md) for the measurement-driven performance strategy.
