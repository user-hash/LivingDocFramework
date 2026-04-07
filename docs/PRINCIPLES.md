# Core Principles

The seven ideas behind LDF. Each stands alone, but they compound when combined.

[Back to README](../README.md)

---

## 1. Hexagonal Architecture (Ports & Adapters)

Separate domain logic from infrastructure. The domain has zero imports from the host environment. No game engine types, no framework types, no platform APIs. All communication crosses explicit port interfaces.

An AI writing code inside a pure domain assembly cannot introduce platform coupling. The compiler rejects it.

**Structure:**

```
Domain/          # Pure logic. Zero platform imports. Leaf dependency.
  ├── State/     # Immutable state containers
  ├── Commands/  # State mutation definitions
  └── Ports/     # Interface definitions (IXxxPort, IXxxProvider)

App/             # Orchestration. References Domain only.
  ├── Services/  # Use-case coordination
  └── Controllers/ # State mutations via Command/Dispatch

Infrastructure/  # Platform adapters. Implements ports.
  ├── Adapters/  # Concrete implementations of port interfaces
  └── Bridges/   # Legacy/monolith integration seams
```

**Port interface naming convention:**

| Suffix | Purpose | Direction |
|--------|---------|-----------|
| `IXxxPort` | Environment abstraction (time, input, audio, rendering) | Domain ← Infra |
| `IXxxProvider` | Data/service supplier (read-oriented) | Domain ← Infra |
| `IXxxHost` | Reverse callbacks; composition root implements these | Infra → Domain |
| `IXxxService` | Seam to singletons during extraction | Transitional |

**Rule:** No platform types in port interfaces. No `Color`, no `Vector3`, no `HttpClient`. Ports use primitives, enums, or domain types only.

---

## 2. Pure Assemblies / Modules

Group code into compilation units with explicit dependency rules. Some assemblies are **pure**: zero platform/engine references, testable and analyzable in isolation.

```
Pure (no engine references):
  Domain, Core, App, Config, MusicTheory, Audio.DSP,
  Contracts, Math, PatternEngine

Platform-coupled:
  Presentation, Infrastructure, Adapters, Editor
```

If a file in `Domain` tries to import a platform namespace, the build fails. The dependency graph IS the architecture.

---

## 3. Invariant-Driven Development

Critical rules written as numbered, citable invariants with a unique ID prefix. They live in documentation files and are referenced in code comments and commit messages. How you verify them is up to you: hooks, ratchet tests, Roslyn, CI, or just team discipline.

**Format:**

```
INV-{SCOPE}-{NNN}: {Rule statement}
```

**Examples:**

```
INV-AUTH-001: Retry attempts must be bounded to MAX_RETRIES.
INV-DSP-003: Voice mutation is audio-thread-only. Main thread writes command queues.
INV-ASM-001: Domain assembly: noEngineReferences true, near-leaf.
INV-BASS-001: Bass is monophonic: MaxVoices=1.
INV-SAVE-ID-001: All persistent IDs are language-agnostic (enums, GUIDs, stable strings).
```

**In code:**

```csharp
// INV-AUTH-001: Retry attempts bounded to MAX_RETRIES
for (int attempt = 0; attempt < MAX_RETRIES; attempt++) { ... }
```

**In commits:**

```
fix: Add retry limit to auth flow

Respects INV-AUTH-001 (retry attempts bounded).
```

When an AI agent reads `INV-DSP-003: Voice mutation is audio-thread-only`, it knows a hard boundary before writing any code.

---

## 4. Framework Over Hardcoding

Every domain that has an established framework or system must use it. No hardcoded values when a framework provides the answer.

| Domain | Framework/System | Use instead of |
|--------|-----------------|----------------|
| Colors | Perceptual color library (OKLab) | Raw RGB/hex values |
| Animation | Spring/easing library | Manual `Lerp` calls |
| UI elements | Factory methods (`CreateLabel`, `CreateButton`) | Raw `new GameObject` + `AddComponent` |
| Theme colors | Centralized palette / token system | Hardcoded `Color` constants |
| Contrast | Perceptual contrast check (deltaL >= threshold) | Eyeballed text colors |
| Math | Dedicated math assembly | Inline math utilities |

No magic numbers for colors, sizes, or timing that already have a token, constant, or framework API. Without this rule, every AI session introduces new literal values that drift from the design system.

---

## 5. Tiered Code Classification

Not all code is equal. Classify files by criticality. Enforcement scales with importance.

| Tier | Name | Enforcement |
|------|------|-------------|
| **A** | Critical | Highest attention. Update invariants when changing these. |
| **B** | Important | Worth documenting when you change them. |
| **C** | Standard | No special requirements. |

Classification is explicit, written in `CODE_DOC_MAP.md`, not guessed from file paths.

**Doc-sets** organize documentation by subsystem:

```
docs/
├── api/
│   ├── CODE_DOC_MAP.md    # Presence = this is a doc-set
│   └── INVARIANTS.md      # Tier A enforcement target
├── audio/
│   ├── CODE_DOC_MAP.md
│   └── INVARIANTS.md
└── multiplayer/
    ├── CODE_DOC_MAP.md
    ├── INVARIANTS.md
    └── BUG_PATTERNS.md
```

Folder structure IS the configuration. No YAML routing needed.

---

## 6. The AI Instruction File (CLAUDE.md)

A single file at the project root that AI coding tools load automatically at session start. It contains:

- **Invariants:** every INV-xxx rule the AI must respect
- **Architecture boundaries:** which assemblies are pure, which reference what
- **Framework mandates:** use OKLab for colors, not raw hex
- **Naming conventions:** port suffixes, namespace rules
- **Data authority chains:** which system is the source of truth for what
- **Anti-patterns:** what NOT to do, with the reason why

This is the most impactful file in the repository. A machine-readable instruction set for AI behavior.

**Structure of a good AI instruction file:**

```markdown
## Architecture
[Hexagonal layout, key files, composition root location]

## Invariants
[Every INV-xxx rule, grouped by domain]

## Frameworks (MANDATORY, no hardcoding)
[Table: domain -> framework -> what it replaces]

## Assembly Map
[Which assemblies are pure, dependency rules]

## Data Authority
[Editing truth -> scheduling truth -> serialization truth]

## Rules for Adding Features
[Where new state goes, where new mutations go,
 where new UI goes, where business logic goes]
```

---

## 7. Ratchet Testing

Metrics that can only improve, never regress. A ratchet test defines a ceiling or floor. If a future change violates it, the build fails.

**Examples:**

```
Monolith file count: cap at 146 files (was 200+, can only decrease)
Monolith LOC: cap at 40,600 (can only decrease)
Direct singleton access in presentation code: cap at 0
Platform imports in domain assembly: cap at 0
Hardcoded English strings: ceiling N, lower as strings migrate to i18n
```

Ratchets prevent regression without requiring perfection today.
