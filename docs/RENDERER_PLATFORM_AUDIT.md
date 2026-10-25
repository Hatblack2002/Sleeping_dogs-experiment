# Renderer and platform boundary audit

**Decision: the current TheoryEngine tree is not a drop-in Android engine.** This is a source-structure audit of the public reference repository, not an Android implementation.

## Rendering boundary

The code does contain a nominal platform seam, but the concrete platform implementation exposed by the umbrella header is Windows/PC:

- illusion/pc/modelplat.hh defines GPU buffers around ID3D11Buffer and ID3D11ShaderResourceView.
- illusion/pc/textureplat.hh stores D3D11_TEXTURE2D_DESC, ID3D11Resource, ID3D11ShaderResourceView, and ID3D11SamplerState.
- theory.hh hard-defines THEORY_WINDOWS and THEORY_PLATFORM_PC and includes d3d11.h under the PC define.
- illusion/renderstate.hh uses Microsoft-specific __declspec(align(16)).
- The engine exposes WaitUntilGPUDone() as a TODO in illusion/illusion.hh; a functioning cross-platform GPU synchronization path is not supplied there.
- Shader/resource declarations describe engine data structures but do not by themselves provide an Android renderer, shader conversion pipeline, swapchain, or frame presentation path.

A Vulkan renderer for Android/Adreno would be a substantial backend, not a header rename. It would need explicit implementations for buffers, textures, resource lifetime, shader binaries/pipelines, render state, synchronization, and presentation, plus validated mappings for the game's material/shader semantics.

## OS/platform boundary

- quark/pc/processplat.hh uses Windows primitives such as Sleep, GetCurrentThreadId, CloseHandle, ResetEvent, and _Interlocked*.
- quark/pc/stringplat.hh is mostly portable memory/string logic, but it relies on the platform's compiler conventions inherited from the umbrella header.
- quark/file.hh declares the file abstraction, but a declaration alone does not establish an Android-backed implementation compatible with the game's resource streaming and memory mapping assumptions.
- The umbrella header uses __forceinline, while other headers use Microsoft calling-convention and alignment annotations. These require portability shims or source-level changes and must be validated with Clang/NDK.

## Game integration boundary

The inspected main/mainloop.hh only initializes engine systems (qInit, Illusion::gEngine.Init, render-state initialization and RenderWorldState::Init) and closes the engine. It is not a complete game entry point and does not implement the retail game's gameplay loop, platform input, boot flow, or presentation.

The public tree is predominantly headers, has no detected CMake entry point or conventional compiled translation units, and does not include the retail game executable or proprietary game data. The upstream project explicitly states that it is not a complete rewrite and has no license because some code may resemble the original.

## Recommended next engineering decision

Do not start by writing a Vulkan backend against this tree and imply that it will produce Sleeping Dogs. First resolve source-use rights and establish a complete, legally usable engine implementation and game-data path. If those gates cannot be satisfied, a direct native port based on this reference is a no-go; the alternative would be a separately scoped compatibility/emulation experiment, clearly labelled as such rather than a native port.

## Evidence links

- TheoryEngine umbrella header: https://github.com/SDmodding/TheoryEngine/blob/main/theory.hh
- D3D11 model backend: https://github.com/SDmodding/TheoryEngine/blob/main/illusion/pc/modelplat.hh
- D3D11 texture backend: https://github.com/SDmodding/TheoryEngine/blob/main/illusion/pc/textureplat.hh
- Windows process backend: https://github.com/SDmodding/TheoryEngine/blob/main/quark/pc/processplat.hh
- Engine initialization entry point: https://github.com/SDmodding/TheoryEngine/blob/main/main/mainloop.hh
