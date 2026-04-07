# Case Study: DAWG (Digital Audio Workstation Game)

[Back to README](../README.md)

---

We build **DAWG** (Digital Audio Workstation Game) ([dawgtools.org](https://dawgtools.org) | [itch.io](https://dawg-tools.itch.io/)). A DAW made in Unity game engine. This is what works for us.

## The Codebase

- 1,718 C# source files, 406,000+ lines of code
- 51 assemblies, 13 of which are pure (zero engine references, compiler-enforced)
- Real-time audio DSP, multiplayer networking, MIDI integration, complex UI
- Built by a solo developer using AI-assisted development (Claude Code) over 5 months
- Started from zero Unity experience

## What the Methodology Gives Us

- **13 pure assemblies** mean the AI literally cannot introduce platform coupling in domain code. The compiler stops it.
- **146+ invariants** (INV-xxx) actively enforced across domain, DSP, multiplayer, UI, and serialization. The AI reads them at session start and respects them.
- **CLAUDE.md at 400+ lines** is the single most impactful file. Every AI session starts with full architectural context. No repeated explanations, no drifting behavior.
- **Ratchet tests** cap the monolith at 146 files / 40,600 LOC. It was 200+ files. It can only shrink.
- **Framework-first** (OKLab for perceptual color, Smooth Pro for spring animation, UIFactory for all elements, token-resolved themes) means the AI uses the right tools from the start instead of hardcoding values that drift.
- **Roslyn via X-Ray PRO** (our companion tool, also built on this methodology): 40 C# files, 7,000+ LOC. Scans the full codebase in seconds. Architecture rule validation, tier detection from assembly metadata, coupling metrics (fan-in/fan-out/instability), circular dependency detection, hub/bridge detection, blast radius analysis, and dead code identification.

## The Hard Lesson

AI agents are great at producing code volume but terrible at maintaining architectural coherence across sessions. Without LDF, each session introduced small boundary violations, magic numbers, invariant breaks. Agents make duplicated content or they do not wire the functions to finish the task. Most AI projects fall apart because of this, tightly connected with not testing the result.

**Visualization of the codebase using taxonomy principles and LDF:** [YouTube demo](https://www.youtube.com/watch?v=UQ2W9P4EIZQ)

---

## Documentation Tree at Scale

This grew organically over months. Nobody sat down and planned all of it on day one. Each piece was added when it was needed.

```
project/
│
├── CLAUDE.md                        # AI instruction file (400+ lines)
│                                    #   35 invariant scopes, 76 INV codes
│                                    #   Architecture boundaries, framework mandates
│                                    #   Assembly map, data authority chains
│                                    #   Rules for adding features
│
├── CHANGELOG.md                     # Version history (Tier A)
├── ARCHITECTURE.md                  # Module layout overview
│
├── docs/
│   │
│   ├── invariants/                  # Safety rules by domain (18 files)
│   │   ├── INDEX.md                 #   Master invariant index
│   │   ├── AUDIO.md                 #   INV-DSP-001..015, voice, pipeline
│   │   ├── CORE.md                  #   INV-ABG, INV-DESTROY, INV-CANONICAL
│   │   ├── MULTIPLAYER.md           #   INV-SEAM, INV-THIN, sync rules
│   │   ├── SERIALIZATION.md         #   INV-SAVE-ID, persistence rules
│   │   ├── UI_LAYOUT.md             #   INV-GRID, INV-SURFACE, INV-MIXER
│   │   ├── THREAD_SAFETY.md         #   Audio thread, main thread boundaries
│   │   ├── MEMORY_SAFETY.md         #   Allocation-free DSP, pool rules
│   │   └── ...                      #   (ANIMATION, PLATFORM, VALIDATION...)
│   │
│   ├── bug-patterns/                # Known failure modes (10 files)
│   │   ├── INDEX.md                 #   Anti-pattern catalog
│   │   ├── AUDIO.md                 #   Wet signal routing, filter clipping
│   │   ├── GENERAL.md               #   Cross-cutting patterns (46KB)
│   │   ├── MULTIPLAYER.md           #   ACK format, reconnect, init-order
│   │   ├── UI_GRID.md               #   Grid rendering, pagination, viewport
│   │   └── ...                      #   (PLATFORM, RECORDING, SAVELOAD...)
│   │
│   ├── golden-paths/                # Best practices (6 files)
│   │   ├── INDEX.md
│   │   ├── PERFORMANCE.md           #   Allocation-free audio, pooling
│   │   ├── THREAD_SAFETY.md         #   Command queues, lock patterns
│   │   ├── FILE_IO.md               #   Save/load, migration patterns
│   │   └── ...
│   │
│   ├── code-maps/                   # Code-to-doc mapping (11 files)
│   │   ├── INDEX.md                 #   Master code map
│   │   ├── CORE.md                  #   Core subsystem files + tiers
│   │   ├── AUDIO.md                 #   DSP files + tiers
│   │   ├── MULTIPLAYER.md           #   MP files + tiers
│   │   └── ...                      #   (CONFIG, RECORDING, TESTS...)
│   │
│   ├── decisions/                   # Architecture Decision Records
│   │   ├── INDEX.md
│   │   ├── ADR-0001.md              #   Hexagonal architecture adoption
│   │   ├── ADR-0028.md              #   Bank-only preview path
│   │   └── ...
│   │
│   ├── architecture/                # Architecture documents (23 files)
│   │   ├── DSP_ARCHITECTURE.md      #   10-phase DSP refactor plan
│   │   ├── SIGNAL_FLOW.md           #   Audio signal routing map
│   │   ├── COMPOSITION_ROOTS.md     #   Wiring and lifecycle
│   │   ├── DEPENDENCY_GRAPH.md      #   Assembly dependency rules
│   │   ├── MULTIPLAYER.md           #   Thin MP architecture
│   │   ├── STARTUP_MASTERPLAN.md    #   Boot sequence optimization
│   │   └── ...
│   │
│   └── archive/                     # Historical docs (still searchable)
│       ├── agent-reports/           #   Past audit findings
│       ├── plans/                   #   Completed plans
│       └── legacy/                  #   Superseded docs
│
├── Assets/
│   └── _Project/
│       └── Scripts/
│           ├── Domain/              # Pure assembly (0 engine imports)
│           ├── Core/                # Pure assembly
│           ├── App/                 # Pure assembly
│           ├── Audio/DSP/           # Pure assembly (allocation-free)
│           ├── Math/                # Pure assembly
│           ├── Contracts/           # Pure assembly (port interfaces)
│           ├── MusicTheory/         # Pure assembly
│           ├── Config/              # Pure assembly
│           ├── Presentation/        # Platform-coupled (UI, rendering)
│           ├── Infrastructure/      # Platform adapters
│           └── Multiplayer/         # Isolated (no core imports)
│
└── xray.json                        # Architecture rules for Roslyn
                                     #   "Domain must_not_reference Infrastructure"
                                     #   "Core must_not_reference UnityEngine"
```

## Key Observations

- **76 invariant codes** across 35 scopes did not exist on day one. They accumulated as real constraints were discovered.
- **Bug patterns** are the largest files (one is 142KB). Failures are where the deepest knowledge lives.
- **Code maps** tie files to their doc-sets. When an AI asks "what context do I need?", the code map answers instantly.
- **13 pure assemblies** out of 51 total. Each is a compiler-enforced boundary. The number grew from 3 to 13 as the architecture matured.
- **The archive** matters. Old docs get archived, not deleted. History is searchable.

Start with 5 invariants. The structure grows when you need it.
