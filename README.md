# Sleeping Dogs Android experiment

Research and build-feasibility workspace for evaluating whether the Sleeping Dogs: Definitive Edition engine can be adapted to Android ARM64.

## Current objective

Produce reproducible evidence before attempting a game port:

1. Inspect the public TheoryEngine reimplementation and its platform assumptions.
2. Record licensing/provenance constraints before copying or adapting any code.
3. Inventory Windows/D3D11/x64-specific dependencies and likely porting boundaries.
4. Run the audit in GitHub Actions and publish the report as a workflow artifact.
5. Evaluate Windows compatibility/emulation as a separate, potentially more practical route.

## Important limitations

- This repository does **not** contain Sleeping Dogs game data, executables, PDB files, or other proprietary assets.
- TheoryEngine is an archived reverse-engineered reimplementation, not the original engine source. Its upstream repository states that it has no license because some code may resemble the original. Treat it as research/reference material unless permission and licensing are clarified.
- An audit report is not an Android port. No APK or gameplay support is claimed until an actual implementation is built and tested.
- The user's legally obtained game files must remain separate; do not upload proprietary game data to this public repository.

## First experiment

Open **Actions → TheoryEngine feasibility audit → Run workflow**. The workflow clones the public upstream into the temporary runner, scans platform and build assumptions, and uploads a Markdown report. It does not commit upstream source into this repository.

Upstream: https://github.com/SDmodding/TheoryEngine

## Current feasibility result

- [FEASIBILITY_GATE.md](docs/FEASIBILITY_GATE.md): evidence-based native-port gates.
- [RENDERER_PLATFORM_AUDIT.md](docs/RENDERER_PLATFORM_AUDIT.md): renderer, OS, and game-integration boundaries.
- [COMPATIBILITY_ROUTE.md](docs/COMPATIBILITY_ROUTE.md): separate Windows-compatibility route and test plan.

The scheduled audit, NDK probe, and regression tests run through GitHub Actions. Compatibility/emulation is not a native port, and no APK or playable result is claimed until it has been built and tested on hardware.


## Android launcher prototype

A first Java-based Android launcher prototype now exists in [`android-wrapper/`](android-wrapper/). It builds a debug APK in the **Android compatibility app build** workflow. The app checks for common Winlator package IDs and opens Winlator; if absent, it opens the official release page.

This is a real compile-tested APK artifact, **not the game itself** and not a native Sleeping Dogs port. It does not bundle Winlator, proprietary game data, or an automatic `HKShip.exe` launch integration. The next engineering gate is testing installation and the Winlator hand-off on Android, then validating the actual game launch separately.

Latest build artifact: [Android compatibility app build #10](https://github.com/Hatblack2002/Sleeping_dogs-experiment/actions/runs/40229201754). Open the run page and download `sleeping-dogs-android-wrapper-debug` under **Artifacts** (available for 14 days).
