# Community ARM64 recompilation lead — verification update

**Checked:** 2026-10-25  
**Repository:** `Hatblack2002/Sleeping_dogs-experiment`  
**Status:** Static evidence now supports a native ARM64 recompilation-style architecture, but game identity, source provenance, and reproducibility remain unverified.

## New evidence from the reference APK

A successful GitHub Actions static audit inspected the reference APK:

- APK SHA-256: `64bece33b795449aaf29146bc2cbb84686c8cccd578a4ba19994902fe3cdc9be`
- Package: `com.sdre.sleepingdogs.steam`
- Entry: `android.app.NativeActivity`
- Main ARM64 library: `libnfsmw.so`, 103,806,248 bytes.
- The library exports `ANativeActivity_onCreate`, `StartGuest`, `GuestAlloc`, `ApiThunkFor`, `RegisterApi`, many generated-looking `f_140001...` functions, and graphics symbols `NgfxD3D11CreateDevice` / `NgfxCreateDXGIFactory1`.
- The APK bundles DXVK D3D11/DXGI libraries and `libvulkan_freedreno.so`.
- The ZIP inventory does not contain an obvious Windows game executable or retail assets, indicating game files are expected separately.
- [Full static audit and interpretation](REFERENCE_APK_AUDIT_2026-10-25.md)
- [GitHub Actions run](https://github.com/Hatblack2002/Sleeping_dogs-experiment/actions/runs/40230794634)

## Interpretation

The native activity, large AArch64 library, and guest-code/generated-function symbols are meaningful evidence for a static-recompilation-style application. DXVK is a graphics API translation layer; its presence alone does not show that game logic executes under Wine, Box64, or FEX. The static pass did not establish that such a compatibility runtime is present.

The important unresolved mismatch is the main library's SONAME, `libnfsmw.so`. The name could be reused from another project, but there is no evidence yet that explains it. The audit did not find a clear `sdhdship.exe`, `HKShip`, or Bink marker proving the generated functions are from Sleeping Dogs: Definitive Edition.

Therefore:
- **Likely:** native ARM64 recompilation-style architecture.
- **Not established:** exact game-code identity, author/source provenance, reproducible build, or successful gameplay.
- **Not justified:** calling the APK a fake/wrapper based only on DXVK or the library name.

## Public source status

The author’s Reddit post says future releases and updates will be in a Discord server and provides a Google Drive download, but no canonical source repository or reproducible build pipeline was identified in the public GitHub searches performed. The claims about function counts and ARM64 translation remain author claims until source or build evidence is obtained.

Source: https://www.reddit.com/r/AndroidNativePorts/comments/1x4ji39/finished_and_optimized_a_few_ports_of_different/

## Target-device risk

The author says Android 10+ 64-bit, roughly 17 GB free storage, and 8 GB RAM minimum (12 GB recommended) are needed; the reported tested devices are RedMagic 11S Pro and RedMagic 9 Pro. The Galaxy S20 FE SM-G781U has a Snapdragon 865 / Adreno 650 and Android 13, so its GPU/OS fit the stated family, but its approximately 5.76 GiB usable RAM is below the author's stated minimum. This is a risk to validate, not proof that it cannot run.

## Required verification sequence

1. Establish why the main library is named `libnfsmw.so`; trace the native startup and game-data loading path.
2. Find the author’s canonical source/build pipeline and verify game version, generated-code provenance, dependencies, and rights.
3. Reproduce a clean ARM64 build from lawful, verifiable source. Keep proprietary retail files out of the public repository.
4. Install on the target Snapdragon 865 device and record installation, startup, data discovery, renderer initialization, first scene, input, sustained gameplay, save/load, memory, and thermal results separately.

## Decision

Keep the reference APK as the highest-priority architectural lead. Do not import its binary as source implementation or claim a verified Sleeping Dogs port yet. The next milestone is source/provenance discovery and library/data-path tracing—not another wrapper APK.
