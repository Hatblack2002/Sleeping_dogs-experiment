# Reference Android APK static audit — 2026-10-25

## Evidence identity

- APK SHA-256: `64bece33b795449aaf29146bc2cbb84686c8cccd578a4ba19994902fe3cdc9be`
- Package: `com.sdre.sleepingdogs.steam`
- Android entry component: `android.app.NativeActivity`
- Native ABI: ARM64 / AArch64
- Main native library: `lib/arm64-v8a/libnfsmw.so` (103,806,248 bytes)
- Other bundled libraries: `libdxvk2_d3d11.so`, `libdxvk2_dxgi.so`, `libdxvk_d3d11.so`, `libdxvk_dxgi.so`, `libhardware.so`, `libvulkan_freedreno.so`
- The APK contains no obvious Windows executable or retail game asset files in its ZIP inventory; it appears to expect game files supplied separately.
- CI job: [run 40230794634](https://github.com/Hatblack2002/Sleeping_dogs-experiment/actions/runs/40230794634)
- Report artifact: [sleeping-dogs-native-apk-audit](https://github.com/Hatblack2002/Sleeping_dogs-experiment/actions/runs/40230794634/artifacts/12613350746) (short-lived; expires after three days).

## Confirmed static observations

1. The manifest identifies a native Android activity, and the APK bundles an AArch64 shared library with `ANativeActivity_onCreate`.
2. The main library exports symbols consistent with a generated-code/recompilation framework, including `StartGuest`, `GuestAlloc`, `ApiThunkFor`, `RegisterApi`, and many generated-looking function symbols named `f_140001...`.
3. It exports graphics bridge symbols such as `NgfxD3D11CreateDevice` and `NgfxCreateDXGIFactory1`.
4. The APK bundles DXVK D3D11/DXGI libraries and a Freedreno Vulkan driver. The DXVK libraries contain DXVK/D3D11/Vulkan identifiers.
5. The APK contains only one Java source file after JADX analysis. This is consistent with a mostly native application, but decompilation coverage alone proves neither presence nor absence of runtime components.
6. The APK ZIP inventory does not include an obvious `sdhdship.exe`, `HKShip`, or Bink executable/library. The game-specific identity and external data-loading contract therefore remain unconfirmed by this static pass.

## Interpretation

**Architecture assessment: likely native ARM64 static-recompilation-style build, not proven end-to-end.**

The native activity, large ARM64 library, generated-looking `f_140001...` symbols, and `StartGuest`/guest-memory/API-thunk symbols are stronger evidence of ahead-of-time translated game code than the earlier summary recognized. Bundled DXVK appears to serve a Direct3D-to-Vulkan graphics boundary; DXVK by itself does not mean the game logic runs under Wine or Box64. The inspected APK inventory and ELF dependencies did not establish that Wine, Box64, FEX, or a separate Windows executable is used to execute game logic.

However, this static audit cannot yet prove that the generated functions correspond to Sleeping Dogs: Definitive Edition. The library's SONAME `libnfsmw.so` is a significant unexplained naming mismatch. It may be a reused build name, but that is only a hypothesis. No canonical source tree or reproducible build pipeline has been found in the public GitHub searches performed for this audit.

This is **not** a finding that the APK is fake or merely a wrapper. It is also **not** a source-level verification that the build is a correct Sleeping Dogs recompilation. The evidence currently supports a native-recompilation architecture while leaving game identity, provenance, and reproducibility open.

## Device compatibility implications

The author’s public Reddit post says the build was tested on RedMagic 11S Pro and RedMagic 9 Pro, expects Snapdragon/Adreno 6xx–8xx devices, requires Android 10+ 64-bit, about 17 GB free storage, and lists 8 GB RAM as a minimum (12 GB recommended for comfortable play). The target Galaxy S20 FE SM-G781U has Snapdragon 865 / Adreno 650 and Android 13, but approximately 5.76 GiB usable RAM. GPU/OS are in the claimed support family; RAM is below the author's stated minimum. That is a risk, not a conclusive incompatibility result.

Source for these author claims: https://www.reddit.com/r/AndroidNativePorts/comments/1x4ji39/finished_and_optimized_a_few_ports_of_different/

## Remaining verification gates

1. Identify the source of `libnfsmw.so` and establish why its name differs from the target game.
2. Obtain the author’s canonical source/build pipeline and verify the game version and generated-code provenance.
3. Trace the library's startup and data-loading path, including whether it expects `sdhdship.exe`-derived output or separately supplied retail files.
4. Reproduce a clean build from lawful, verifiable source. Keep retail game files and generated proprietary code out of this public repository unless their redistribution rights are established.
5. Install and test on the Galaxy S20 FE. Record installation, startup, data discovery, renderer, first scene, input, sustained gameplay, save/load, memory pressure, and thermal behavior separately.

## Decision

Keep this APK as the highest-priority architectural reference. Do not import its binary as the project's source implementation or claim a verified port yet. The next useful milestone is source/provenance discovery and a trace of the main library's game identity/data-loading behavior—not another wrapper or empty JNI scaffold.
