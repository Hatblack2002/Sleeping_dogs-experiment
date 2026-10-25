# Compatibility Route: Running the Retail PC Game on Android

## Decision

Prioritize an **emulation/compatibility proof of concept** before attempting a native renderer rewrite. This is separate from a native Android port: it runs the retail Windows executable through compatibility components and does not turn the incomplete TheoryEngine source into a playable native game.

## Findings from current community evidence

- Community reports dated October 23–24, 2026 describe Sleeping Dogs: Definitive Edition running through Android PC-compatibility stacks. One report says a Snapdragon 855+ / Adreno 640 device with 8 GB RAM sustained above 30 FPS; other reports mention newer Snapdragon devices and variable results. These are anecdotal, uncontrolled reports, not a guarantee for this target.
- A separate directory now lists a claimed “Android Native Port” / static recompilation, but labels it alpha, says no public download is available, and explicitly says it has no public source and has not been reviewed. This is not currently a reproducible source-based route for this repository.
- Therefore, the near-term testable route remains a known compatibility stack using the retail PC build. The native-recompilation claim should be monitored, but no APK from mirrors or re-uploads should be treated as trustworthy evidence.

## Target hardware

The project target is a Galaxy S20 FE 5G with Snapdragon 865 / Adreno 650 and 6 GB-class memory. That hardware is capable enough to justify testing a Direct3D-to-Vulkan compatibility stack, but sustained performance, memory pressure, thermals, game build, driver and wrapper versions require direct testing. No claim of successful execution on this exact phone is made here.

## Experiment order

1. Use a legitimate retail installation of **Sleeping Dogs: Definitive Edition**. Do not assume the original 2012 release behaves the same.
2. Establish a clean baseline in a current, reputable Winlator build using its default container configuration before changing many variables.
3. If the game fails, vary one dimension at a time: Box64 preset, DXVK version, Turnip driver, resolution, and required game redistributables. Record exact versions and observed failures.
4. Start at a conservative resolution such as 960x540 or 1280x720 and low graphics settings. Measure sustained performance and thermal throttling, not only initial FPS.
5. Treat boot to menu, loading into gameplay, a 10-minute gameplay session, audio, controls, and save/load as separate test gates.
6. Only after a compatibility baseline is understood should this repository consider a launcher/front-end. A custom launcher cannot itself replace Wine/Box64/DXVK/Turnip; bundling these components requires separate packaging, maintenance, and license review.

## What not to do

- Do not install a random driver APK expecting it to make Android appear to be a laptop. A graphics driver covers a particular API/device boundary; it does not implement Windows APIs or translate x86-64 machine code.
- Do not treat a successful GitHub Actions audit as evidence that the game runs.
- Do not copy proprietary game assets or executables into this repository.
- Do not describe a Winlator-based setup as a native Android port.
- Do not claim compatibility on the target phone until it has been directly tested.
- Do not install APKs from mirrors or re-uploads when the original developer, source, integrity, and permissions cannot be verified.

## Relationship to the native-port investigation

The TheoryEngine audit found that the public reimplementation is incomplete for a playable game port and its umbrella header fails an Android NDK syntax probe because it includes the Windows Direct3D header `d3d11.h`. That failure supports postponing a native renderer rewrite; it does not prevent a Windows compatibility layer from attempting to run the retail executable.

## References

- Winlator project and compatibility stack: https://github.com/brunodev85/winlator
- Official Steam page for Sleeping Dogs: Definitive Edition: https://store.steampowered.com/app/307690/Sleeping_Dogs_Definitive_Edition/
- Community report, Snapdragon 855+ / 8 GB RAM, October 24, 2026: https://www.reddit.com/r/AndroidNativePorts/comments/1xe5i3a/yoooo_the_sleeping_dogs_ports_is_really_good/
- Community discussion of the claimed Android static-recompilation port and its unverified status: https://droidports.com/games/sleeping-dogs-definitive-edition/
- Winlator's official README describes running Windows x86-64 software with Wine and Box64 and using graphics backends such as Turnip/DXVK: https://github.com/winebox64/winlator
- Community reports are anecdotal and not controlled benchmarks.

## Current status

**Research only; no APK or device-level test has been produced by this repository.** The next proof is a reproducible launch/gameplay test on the target hardware using a legally obtained game copy. The workflow audit passing only verifies the audit tooling, not the game.
