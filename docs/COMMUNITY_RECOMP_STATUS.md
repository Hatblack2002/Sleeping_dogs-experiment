# Community ARM64 recompilation lead — verification update

**Checked:** 2026-10-25  
**Repository:** `Hatblack2002/Sleeping_dogs-experiment`  
**Status:** An APK/build is being shared by a community poster, but a canonical source repository and reproducible build have not been verified.

## New evidence

- Reddit post by the account that says it produced the port: https://www.reddit.com/r/AndroidNativePorts/comments/1x4ji39/finished_and_optimized_a_few_ports_of_different/
  - The post describes a Sleeping Dogs: Definitive Edition Android build and says its game code was translated to ARM64; it reports 194,020 functions plus 636 Bink functions.
  - The post includes a Google Drive folder link and says the supported executable is supplied separately.
  - These are poster claims, not source-level verification. The post says future releases/updates will be in a Discord server and does not provide a canonical source repository in the post itself.
- A follow-up post on 2026-10-23 also points users to a download, but does not establish a source repository: https://www.reddit.com/r/AndroidNativePorts/comments/1xdhife/sleeping_dogs_definitive_edition_android_port/
- Current catalog entry: https://droidports.com/games/sleeping-dogs-definitive-edition/
  - It labels the port a static recompilation and says retail PC files are required.
  - It explicitly says there is no public source code and that its APK has not been reviewed.

## Interpretation of the earlier APK audit

The previously inspected APK contained a large `libnfsmw.so` and DXVK libraries. That is evidence of a native ARM64 library and a Direct3D-to-Vulkan component, but it does **not** identify the game code as Sleeping Dogs. The `nfsmw` name is a strong mismatch that requires explanation; library size, generated symbols, or DXVK presence cannot resolve it. Do not label that APK a verified Sleeping Dogs recompilation.

## Required verification sequence

1. Obtain the exact APK and its SHA-256 from the author-controlled release, then preserve the digest in the audit.
2. Inspect package metadata, every ABI library, ELF dependencies, exported symbols, and strings for `HKShip`, `sdhdship`, `bink2w64`, and game-specific resource names.
3. Determine whether the APK expects a supplied native `.so`, imports retail files, launches a compatibility layer, or actually contains statically translated game code. DXVK alone does not prove runtime emulation, but its presence conflicts with a strict no-DXVK project requirement and must be traced.
4. Locate and inspect the author’s canonical source repository and build instructions. A downloadable APK or Discord link is not a substitute for source.
5. Reproduce a clean ARM64 build in GitHub Actions from lawful source. Keep proprietary game executables/assets out of this public repository.
6. Install and test on the target Snapdragon 865 device; separately verify boot, asset loading, and gameplay. A CI compile or static report is not a gameplay test.

## Decision

Keep the community recompilation as the highest-priority lead, but **do not import its APK/library as the project implementation yet**. Do not cross-compile TheoryEngine as if it were a complete engine: the existing public tree is an incomplete, Windows/D3D11-oriented reverse-engineering reference with unresolved source-use rights. The next milestone is source/provenance verification, not another wrapper APK.
