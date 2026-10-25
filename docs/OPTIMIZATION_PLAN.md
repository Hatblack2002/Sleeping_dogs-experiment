# Native optimization plan — Sleeping Dogs: Definitive Edition

## Objective

Build and optimize an Android ARM64 implementation that executes game code directly. The community APK is an **architecture and behavior reference only**: it is not the project's runtime dependency, source foundation, or binary to redistribute.

Hard exclusions for the game execution path:
- Wine / Winlator
- Box64
- FEX
- Windows executable launched by a compatibility runtime
- Remote/streamed gameplay

The implementation must not require any of those components. DXVK is also not a project dependency or chosen renderer: it is present in the reference APK, but this project will implement or adapt a lawful native Android rendering boundary instead of inheriting the reference's DXVK stack. Vulkan is the preferred Android graphics API if the available game/recompilation code can be connected to it; otherwise evaluate OpenGL ES based on measured requirements and existing code.

## Engineering principle

Do not optimize by guesswork or by stripping features until the game appears to run. Establish a repeatable baseline, measure each bottleneck, change one subsystem at a time, and preserve correctness. The reference APK can help us observe expected startup stages, input behavior, data layout, rendering expectations, and memory needs; it is not proof that its binaries can be reused.

## Stage 0 — Establish a reproducible code source

Before performance work can begin:
1. Obtain the canonical, lawful source/build pipeline for a static recompilation of the target executable, or define a legally reviewed independent reimplementation path.
2. Verify target game version and provenance of generated functions.
3. Confirm the output is ARM64 machine code executed in-process, not an emulator or Windows compatibility runtime.
4. Define Android system-service and graphics API boundaries.
5. Keep retail executables/assets out of the public repository; import user-owned files locally.

No performance patch to a mystery 100 MB binary can replace this stage.

## Stage 1 — Baseline on target hardware

Capture a baseline on the Galaxy S20 FE (Snapdragon 865 / Adreno 650, Android 13) for every stage that can be reached:
- APK install and cold start
- native initialization
- discovery and validation of game data
- renderer/device/swapchain initialization
- first rendered scene
- input response
- sustained scene or gameplay
- save/load
- memory use, low-memory events, temperature and throttling

Record device model, Android build, game build, asset version, graphics settings, resolution, frame-time percentiles (P50/P90/P95/P99), average FPS, peak and steady-state RAM, CPU/GPU load where available, and run duration. Separate a cold run from warmed runs. A CI compile or screenshot is not proof of gameplay.

## Stage 2 — Profile before changing code

Use Android-native tools and app instrumentation to identify whether each bottleneck is CPU, GPU, memory bandwidth, storage/I/O, synchronization, or thermal. Collect:
- frame-time traces and missed-frame counts
- CPU sampling/per-thread timing and scheduler behavior
- Vulkan validation/debug output if Vulkan is selected
- allocations, peak resident memory and asset cache sizes
- shader/pipeline compilation stalls
- storage read volume, decompression time and streaming stalls
- lock contention, job-queue idle time and worker utilization

Do not infer performance from library size, function count, or one FPS figure.

## Stage 3 — Optimization order

### A. Correctness and startup
- Make file paths and data discovery deterministic.
- Validate archive/index parsing and report missing or mismatched files.
- Avoid repeated full scans of game data; cache verified indexes and metadata where legally and technically appropriate.
- Keep initialization asynchronous where safe, with explicit lifecycle/cancellation handling.

### B. Memory pressure (high priority for this device)
- Measure allocations before changing memory policy.
- Reuse temporary buffers and object pools only for proven hot allocation paths.
- Bound caches; use streaming and eviction rather than loading all world assets at once when the engine supports it.
- Release GPU resources and staging buffers deterministically.
- Handle Android low-memory callbacks and lifecycle pauses without corrupting game state.
- Test texture/audio compression and mip policies against visual quality and GPU support; never silently substitute missing assets.

### C. CPU and translated game code
- Preserve deterministic guest state and exception/flag behavior in any static recompilation.
- Profile hot functions and generated-code dispatch overhead.
- Remove redundant thunks or state synchronization only when call graphs and correctness tests prove they are redundant.
- Avoid unsafe blanket compiler flags, fast-math, or disabled checks until per-subsystem tests demonstrate correctness.
- Tune thread affinity, worker count, and job granularity from measurements; do not hard-pin all threads without evidence.

### D. Rendering
- Use a direct Android Vulkan renderer if a viable lawful renderer boundary exists; consider GLES only if required by source constraints or measured compatibility.
- Minimize pipeline and descriptor churn, redundant state changes, and CPU/GPU synchronization.
- Cache shader/pipeline artifacts with driver/device/version keys.
- Use asynchronous resource upload and staging buffers where beneficial.
- Apply resolution scaling, level-of-detail, texture streaming, and shadow-quality controls only where the engine supports them and measured GPU time justifies them.
- Do not add DXVK as a shortcut or retain a Windows D3D11 dependency by default.

### E. Streaming, storage and audio
- Measure archive reads and decompression separately from CPU/GPU frame time.
- Prioritize and schedule world streaming to avoid blocking the render/game thread.
- Bound I/O queues and decompression workers to avoid RAM spikes.
- Keep audio callbacks real-time safe; no blocking storage or allocation in callbacks.

### F. Thermal stability
- Run at least 20–30 minute repeatable workloads after functional gameplay exists.
- Track frame-time degradation as device temperature rises.
- Reduce workload through measured quality scaling or adaptive resolution before resorting to arbitrary frame caps.
- Test plugged/unplugged and cool/warm starting conditions separately.

## Stage 4 — Acceptance criteria

The project cannot be called playable until the game is installed and observed running on the target device with real game data and responsive input.

For each optimization, keep a before/after record with:
- exact commit and build configuration
- identical scene, resolution, settings and run duration
- P50/P90/P95/P99 frame time and average FPS
- peak/steady RAM, temperature/throttling observations
- functional regression checks (scene, input, audio, saves, loading)
- reproducible logs or traces

Accept an optimization only if it improves a measured target without unacceptable correctness, visual, stability, or memory regressions.

## Current status

The project has not yet obtained a verified, reproducible source/build pipeline for the game's translated code. Consequently, no claim is made that any performance optimization has already been implemented or benchmarked. The immediate task is to establish the independent native code path; profiling and tuning follow once there is executable project code.
