# Sleeping Dogs Android experiment

Research and build-feasibility workspace for evaluating whether the Sleeping Dogs: Definitive Edition engine can be adapted to Android ARM64.

## Current objective

Produce reproducible evidence before attempting a game port:

1. Inspect the public TheoryEngine reimplementation and its platform assumptions.
2. Record licensing/provenance constraints before copying or adapting any code.
3. Inventory Windows/D3D11/x64-specific dependencies and likely porting boundaries.
4. Run the audit in GitHub Actions and publish the report as a workflow artifact.

## Important limitations

- This repository does **not** contain Sleeping Dogs game data, executables, PDB files, or other proprietary assets.
- TheoryEngine is an archived reverse-engineered reimplementation, not the original engine source. Its upstream repository states that it has no license because some code may resemble the original. Treat it as research/reference material unless permission and licensing are clarified.
- An audit report is not an Android port. No APK or gameplay support is claimed until an actual implementation is built and tested.
- The user's legally obtained game files must remain separate; do not upload proprietary game data to this public repository.

## First experiment

Open **Actions → TheoryEngine feasibility audit → Run workflow**. The workflow clones the public upstream into the temporary runner, scans platform and build assumptions, and uploads a Markdown report. It does not commit upstream source into this repository.

Upstream: https://github.com/SDmodding/TheoryEngine


## Current feasibility result

See docs/FEASIBILITY_GATE.md for evidence-based findings from the upstream tree and current engineering blockers. The scheduled audit and regression tests run through GitHub Actions.
