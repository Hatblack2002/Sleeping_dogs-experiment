# Compatibility Route: Running the Retail PC Game on Android

## Decision

Prioritize an **emulation/compatibility proof of concept** before attempting a native renderer rewrite. This is a separate technical route from a native Android port: it runs the retail Windows executable through compatibility components and does not turn the incomplete TheoryEngine source into a playable native game.

## Why this route is credible

The retail PC release of Sleeping Dogs: Definitive Edition uses x86-64 Windows and Direct3D 11. Winlator provides a Windows compatibility stack based on Wine, Box64, and graphics translation through Vulkan-oriented components. Public community reports show Definitive Edition running through this general class of stack on Snapdragon 845 and Snapdragon 870 devices. That is evidence that the approach is plausible, not proof that it will work well on every phone or with every game build.

The target device associated with this project is a Galaxy S20 FE 5G with Snapdragon 865 / Adreno 650 and 6 GB-class memory. It is between those reported GPU generations on paper, but actual performance, memory pressure, thermals, game version, driver and wrapper versions still need direct testing. No claim of successful execution on this specific device is made here.

## Suggested experiment order

1. Use a legitimate retail installation of **Sleeping Dogs: Definitive Edition**; do not assume the original 2012 release behaves the same. Community reports include launch failures with the original release.
2. Establish a clean baseline in a current, reputable Winlator build using its default container configuration before changing many variables.
3. If the game fails, vary one compatibility dimension at a time: Box64 preset, DXVK version, Turnip driver, resolution, and required game redistributables. Record the exact version and observed failure for each attempt.
4. Begin at a conservative resolution (for example, 960x540 or 1280x720) and low graphics settings. Watch sustained performance and thermal throttling, not only a short initial FPS reading.
5. Treat boot to menu, loading into gameplay, a 10-minute gameplay session, audio, controls, and save/load as separate test gates.
6. Only after the compatibility baseline is understood should this repository consider a launcher or front-end. A custom launcher cannot itself replace Wine/Box64/DXVK/Turnip, and bundling those components requires separate packaging, maintenance, and license review.

## What not to do

- Do not install a random driver APK expecting it to make Android appear to be a laptop. A graphics driver only covers a particular API/device boundary; it does not implement Windows APIs or translate x86-64 machine code.
- Do not treat a successful GitHub Actions audit as evidence the game runs.
- Do not copy proprietary game assets or executables into this repository.
- Do not describe a Winlator-based setup as a native Android port.
- Do not claim compatibility on the target phone until it has been directly tested.

## Relationship to the native-port investigation

The separate TheoryEngine audit found that the public reimplementation is incomplete for a playable game port and its umbrella header currently fails an Android NDK syntax probe because it includes the Windows Direct3D header `d3d11.h`. That failure supports postponing a native renderer rewrite; it does not prevent a Windows compatibility layer from attempting to run the retail executable.

## Evidence and references

- Winlator's project README describes the Wine + Box86/Box64 stack and its graphics components: https://github.com/brunodev85/winlator
- Official Steam product page for Sleeping Dogs: Definitive Edition and its Windows requirements: https://store.steampowered.com/app/307690/Sleeping_Dogs_Definitive_Edition/
- Community demonstration on Snapdragon 870 / Adreno 650 (GameHub, 720p; reports some instability): https://www.youtube.com/watch?v=BpZF4ZmCvLg
- Community demonstration on Snapdragon 845 with Winlator 6.0 (older configuration; low settings and 30 FPS cap): https://www.youtube.com/watch?v=hOJij7EDk0Y
- The reports above are anecdotal community evidence, not controlled benchmarks or guarantees.

## Current status

**Research decision only.** No APK, bundled emulator, retail game files, or device-level test is produced by this document. The next useful proof is a reproducible launch/gameplay test on the actual target hardware using a legally obtained game copy.
