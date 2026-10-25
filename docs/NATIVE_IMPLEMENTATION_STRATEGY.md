# Native implementation strategy — Sleeping Dogs: Definitive Edition

## Product definition

Build a separately maintained Android ARM64 implementation that directly executes verified native game/recompiled code. It must not launch a Windows compatibility container or depend on the community APK's binaries.

The original retail game assets and required user-supplied files may be imported locally. Their absence from an APK does not by itself prove an app is a container. The key distinction is what executes the game logic:
- **Static recompilation:** original executable functions are translated ahead of time into ARM64 native machine code; the Android process calls the generated code and loads user-supplied game data.
- **Compatibility/container launcher:** the app launches or embeds a runtime such as Wine/Box64/FEX to execute the Windows binary.
- **Thin wrapper:** the app opens another app/runtime.

Only a verified direct-native execution route is in scope. The reference APK is a study sample, not a dependency. Its large native library or symbols are not source code and do not prove exact game identity.

## Architecture constraints

- No Wine, Winlator, Box64, FEX, or Windows executable launch path.
- Do not copy or depend on the community APK's `libnfsmw.so` or DXVK libraries.
- Do not adopt DXVK as the project's renderer. Select a direct Android graphics backend after verifying the actual source boundary; prefer Vulkan if feasible, evaluate GLES only when justified.
- No proprietary game files in the public repository without explicit redistribution rights.
- CI must build real native ARM64 code, not an empty JNI stub or launcher.

## Gates

### Gate 1 — Establish lawful source and code identity
1. Locate the canonical source/build pipeline for the community static recompilation or determine a legally reviewed independent route.
2. Verify game version, generated-code provenance, licensing/rights, and source completeness.
3. Confirm the output is ARM64 machine code executed in-process.
4. Characterize game data formats and required user-supplied files without publishing proprietary data.

### Gate 2 — Design the Android-native platform boundary
1. Map lifecycle, file access, audio, input/touch, threading, storage and graphics APIs.
2. Implement only APIs required by the verified code path; don't create speculative stubs for an unknown engine.
3. Establish a direct Android renderer boundary. Avoid a D3D11-to-Vulkan translation stack as the default plan.
4. Add structured diagnostics for startup, asset discovery, renderer creation, and fatal errors.

### Gate 3 — Build and test
1. Build actual ARM64 code with Android NDK and reproducible CI.
2. Verify APK ABI, linked libraries, unresolved symbols, and forbidden runtime dependencies.
3. Run automated native startup/smoke tests where feasible.
4. Keep the user's retail files local and test data discovery against their known version.

### Gate 4 — Baseline and optimize
Use repeatable measurements on the Galaxy S20 FE: startup stages, frame-time percentiles, CPU/GPU utilization, memory peaks, asset I/O, stalls, thermal behavior and correctness. Optimize measured hot paths, one subsystem per change, and record before/after results. The detailed procedure is in [OPTIMIZATION_PLAN.md](OPTIMIZATION_PLAN.md).

### Gate 5 — Device acceptance
Test APK installation, process startup, game-data discovery, renderer initialization, first scene, touch/gamepad input, sustained gameplay, audio, save/load, low-memory behavior and thermal stability. Do not call it playable until gameplay is observed on hardware.

## Current blockers

- The reference APK looks consistent with static recompilation but its `libnfsmw.so` naming mismatch is unexplained.
- No canonical public source repository or reproducible source/build pipeline has been verified.
- TheoryEngine is incomplete, Windows/D3D11/x64-oriented, and has unresolved source-use rights.
- No native game APK built from verified source or gameplay test exists yet.

## Immediate next action

Continue source/provenance discovery and define the independently built ARM64 code path. Use the reference APK only to understand expected architecture and behavior; do not build on its binary or introduce Wine/Box64/DXVK as runtime dependencies.
