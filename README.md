# LivingDocFramework

How to keep a codebase architecturally coherent when AI writes most of the code.

LDF is not a hook system or a documentation generator. It is a set of principles and conventions for structuring codebases so that architecture survives velocity. We built this while shipping a 400k LOC Unity project with AI assistance. This is what works for us.

Any AI tool. Any programming language. Any team size. This repo includes a reference implementation in Bash and Markdown, but the framework is tool-agnostic. Take what works, leave the rest.

---

## The Problem

AI can produce code faster than anyone can review it. The bottleneck is no longer writing code. It is **architectural coherence**.

Without explicit structure:

- Pure domain boundaries erode (platform types leak into business logic)
- Hardcoded values replace framework calls (magic numbers instead of perceptual color math)
- Invariants are violated silently (safety rules that exist only in someone's memory)
- Decisions disappear (why this pattern, why this boundary, why not the obvious approach)
- AI agents repeat the same mistakes across sessions (no persistent instruction surface)

Code volume is no longer the constraint. **Architectural awareness is.**

---

## Core Ideas

LivingDocFramework is built on seven interlocking ideas. Each stands alone, but they compound when combined.

### 1. Hexagonal Architecture (Ports & Adapters)

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

### 2. Pure Assemblies / Modules

Group code into compilation units with explicit dependency rules. Some assemblies are **pure**: zero platform/engine references, testable and analyzable in isolation.

```
Pure (no engine references):
  Domain, Core, App, Config, MusicTheory, Audio.DSP,
  Contracts, Math, PatternEngine

Platform-coupled:
  Presentation, Infrastructure, Adapters, Editor
```

If a file in `Domain` tries to import a platform namespace, the build fails. The dependency graph IS the architecture.

### 3. Invariant-Driven Development

Critical rules are written as numbered, citable invariants with a unique ID prefix. They live in documentation files, are referenced in code comments and commit messages, and can be enforced by hooks and ratchet tests.

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

### 4. Framework Over Hardcoding

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

### 5. Tiered Code Classification

Not all code is equal. Classify files by criticality. Enforcement scales with importance.

| Tier | Name | Enforcement |
|------|------|-------------|
| **A** | Critical | Commit blocked unless invariants updated |
| **B** | Important | Warning issued |
| **C** | Standard | No enforcement |

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

### 6. The AI Instruction File (CLAUDE.md)

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

### 7. Ratchet Testing

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

---

## Roslyn: Semantic Code Understanding for C# and .NET

> Roslyn is Microsoft's open-source compiler platform for C# and Visual Basic. This section is specific to .NET codebases, but the principle is universal: **every language needs a semantic analysis layer that AI agents can use to understand code meaning, not just text.** Python has `ast` and `mypy`. TypeScript has the compiler API. Rust has `syn` and `rust-analyzer`. None of them are as mature or as deeply integrated as Roslyn. **This is the single biggest gap in AI-assisted development today.** Until every major language has a Roslyn-equivalent, agents will keep making semantic mistakes that compile clean but fail silently at runtime.

### Why Text is Not Enough

LDF v1 enforces at the text level: "you changed a Tier A file, update the docs or the commit is blocked." That works. But an agent can bump the doc version, decide to disobey, go around the invariant, or just ignore it.

Grep finds strings. Roslyn sees the lifeblood flowing through the codebase.

Grep tells you a function name appears in 12 files. Roslyn tells you which 8 are real callers, which 3 are dead code, and which 1 is a comment.

### What This Looks Like in Practice

We develop **DAWG Beatcraft** ([dawgtools.org](https://dawgtools.org), also on [itch.io](https://dawg-tools.itch.io/)), a Unity project: 406,000 lines of C#, 51 assemblies, real-time audio DSP, multiplayer networking, MIDI integration, and a complex UI layer. Roslyn is not a nice-to-have for us. It is essential infrastructure for AI-assisted development at this scale.

**DSP flow verification:** Our audio pipeline processes samples on the audio thread with strict rules: no allocations, no main-thread calls, specific processing order. Roslyn scans method bodies in the DSP assembly and instantly detects violations that would compile fine but produce audio glitches or crashes at runtime. When an AI agent writes DSP code, Roslyn catches wrong argument ordering in reflection calls, identifies math operations where the precise function is actually faster than the approximated version, and verifies that filter coefficients are identical across mono and stereo paths. Text search cannot do any of this.

**Real story: the rogue frequency.** We spent a week chasing a rogue frequency in the audio output. Traditional debugging (grep, breakpoints, reading code) could not find the source. Roslyn traced the actual signal flow through the DSP graph and instantly showed that a wet signal was being fed into the wrong buffer, which cascaded into multiple downstream effects. A week of manual diagnosis versus seconds of semantic analysis. This is the difference between seeing text and seeing the lifeblood of the codebase.

**Dead code detection:** In a 400k line codebase, knowing what is alive and what is dead is crucial. Roslyn traces actual call chains and type references through the full graph. When we remove a public method, Roslyn verifies every caller first, including indirect references through interfaces, generics, and reflection. Grep misses these. We learned this the hard way: three separate times an AI agent claimed something was "unused" based on grep, and three separate times it broke callers that grep could not see.

**Architecture boundary enforcement in real time:** With hexagonal architecture, the most important rule is that domain code never references platform code. Roslyn verifies this at the type level, inside method bodies, not just at the `using` statement level. It catches developers (and AI agents) who write `UnityEngine.Debug.Log()` with a fully qualified name to bypass the using-guard.

**Silent runtime bugs:** Roslyn caught a reflection call with arguments in the wrong order. It found that an advanced math operation was both faster and 15% more precise than the approximation an AI agent substituted. These bugs compile clean but fail in production.

### What Roslyn Enables vs Text

| What text-level tools see | What Roslyn sees |
|------|------|
| "File X was modified" | "File X now references a type from a forbidden namespace" |
| "Invariant doc wasn't updated" | "The invariant itself is violated in the code" |
| "Tier A file changed" | "This change affects 47 downstream files; here's the blast radius" |
| Manual tier classification | Automatic tier inference from coupling metrics |
| Namespace-level boundary checks | Method-body-level verification |
| "This function name appears in N files" | "This function has N real callers and M dead references" |

### Architecture Rule Enforcement

Define rules in a simple JSON file:

```json
{
  "rules": [
    { "source": "MyApp.Domain", "must_not_reference": "MyApp.Infrastructure" },
    { "source": "MyApp.Core", "must_not_reference": "UnityEngine" }
  ]
}
```

Roslyn validates every edge in the dependency graph against these rules. Violations are flagged with source file, target file, and the exact rule broken.

### Automatic Tier Detection

Instead of manually classifying every file:

```
1. Assembly has noEngineReferences: true  -> Pure
2. Assembly has Editor-only platforms     -> Tooling
3. File contains only interfaces          -> Boundary
4. File references no platform types      -> Boundary
5. File inherits MonoBehaviour            -> Runtime
6. Default                                -> Runtime
```

Assembly-level detection is authoritative. File-level detection is heuristic for assemblies without explicit flags.

### Coupling Metrics

Fan-in (how many nodes depend on this), fan-out (how many this depends on), instability (Ce / (Ca + Ce)). Computed from the real dependency graph, not from text matches. Stable nodes should be abstract. Unstable nodes should be concrete. Roslyn measures this directly, across the entire codebase, in seconds.

### The Key Insight

Roslyn turns documentation enforcement from reactive ("you changed a file, update the docs") into proactive ("your change violates this specific constraint, here's the proof").

Combined with hexagonal architecture, Roslyn can automatically:

- Classify tiers from coupling metrics instead of manual tagging
- Detect boundary violations at the type level, not just the namespace level
- Compute blast radius so you know which doc-sets need updating when a port interface changes
- Find stale invariants that reference code paths that no longer exist
- Show you the actual lifeblood of the codebase: what is alive, what is dead, what is critical, what is drifting

**LDF provides the structure. Architecture provides the boundaries. Roslyn provides the semantic verification. This combination is crucial for AI-assisted development on complex codebases.**

---

## Intentional Knowledge Hardening

LDF is not forced on every commit. You activate it when you need it:

- **Tighten architecture when the work is done.** After a subsystem stabilizes, lock in what you learned. Write the invariants. Map the files. Record the decisions. Now you have a foundation that future work (and future AI sessions) can build on.
- **Use it to solve a problem.** Chasing a bug for a week? Document the signal flow, write the invariant that prevents recurrence, add a bug pattern. LDF gives the solution a structured home.
- **Refresh when you have a decision.** Made a meaningful architectural choice? Record it. Chose hexagonal over layered? Write it down while the reasoning is fresh.
- **Granular hexagonal architecture as you need it.** You do not need to hexagonalize the entire codebase on day one. Extract one port, one adapter, one pure assembly. When that works, do another. LDF supports incremental architecture the same way it supports incremental documentation.

When you decide to capture knowledge, the structure is already there. You know where to put it.

**Update docs when you need to, when you have a hard crack to solve, when you are happy with the results. Not always. Only when it matters.**

---

## The Enforcement Layer (Reference Implementation)

The ideas above are the methodology. Below is one way to enforce them, included as a reference implementation in this repository.

### Commit-Time Hooks

Git pre-commit hooks run automatically:

- **Tier A check:** If a Tier A file is modified, the commit is blocked unless the corresponding `INVARIANTS.md` was also updated
- **Changelog check:** Code changes trigger a reminder (configurable: warning or blocking)
- **Blast radius warning:** Large changesets trigger a warning
- **Emergency escape:** `git commit --no-verify` (explicit, auditable)

No CI required. No runtime overhead. Git + Bash only.

These hooks are one implementation. You can also use CI, IDE tooling, semantic analyzers, or just team conventions.

### Context Loading

Before editing any file, look up its context:

```bash
./LivingDocFramework/core/print-context.sh path/to/file.py
```

Output:

```
File: src/api/auth.py
Tier: A (Critical)
Doc-Set: docs/api
Map: docs/api/CODE_DOC_MAP.md

Required Reading:
  1. docs/api/INVARIANTS.md
  2. docs/api/CODE_DOC_MAP.md

Invariants:
  - INV-AUTH-001: Retry attempts bounded
  - INV-AUTH-002: Password never logged
```

### Agent Protocol

AI agents that modify code should:

1. Load the relevant doc-set context before making changes
2. Cite invariants in code comments when editing Tier A files
3. Update documentation when behavior changes
4. Verify bugs exist in current code before reporting them

Full protocol: [protocols/AGENT_PROTOCOL.md](protocols/AGENT_PROTOCOL.md)

### Session Protocol

Context loading order for work sessions:

1. Version sync (correct tag checked out)
2. Read PROJECT_CONTEXT.md (persistent project memory)
3. Read CHANGELOG.md (current state)
4. If editing: read CODE_DOC_MAP.md
5. If Tier A: read INVARIANTS.md

Full protocol: [protocols/SESSION_PROTOCOL.md](protocols/SESSION_PROTOCOL.md)

---

## Who Does What: Human, Code Agent, Chat Agent

AI agents maintain the docs. The human architects. Here is how we split the work.

### The Human

You are the architect. You decide:

- When to harden knowledge (not every commit, only when it matters)
- What the invariants are (the AI writes them down, you identify the rule)
- Architecture direction (what goes where, which boundaries to enforce)
- When to override the AI (escape hatches exist for a reason)
- What to feed to the chat agent for a second opinion

You do not manually update CHANGELOG, CODE_DOC_MAP, or BUG_PATTERNS on every change. That is what the code agent is for.

### The Code Agent (embedded)

Your AI coding tool with full codebase access. File system, git, terminal, Roslyn, MCP tools. It lives inside the codebase.

What it does:

- Reads CLAUDE.md and respects invariants before writing code
- Maintains CHANGELOG entries when committing
- Updates CODE_DOC_MAP when files are created or renamed
- Writes bug pattern entries after fixing bugs (when you say it is worth documenting)
- Runs Roslyn verification to check boundary violations
- Executes ratchet tests
- Loads context via print-context.sh before editing

Deep context, narrow perspective. Sees every line of code but can get tunnel vision.

### The Chat Agent (disconnected)

A separate AI, ideally from a different provider, with NO direct access to the codebase. You feed it only what it needs.

What it does:

- Broad architectural review ("here is our assembly map, does this make sense?")
- Spots holes the code agent misses ("you have 13 pure assemblies but Math depends on nothing, is that intentional?")
- Challenges assumptions ("why is this a port and not a direct dependency?")
- Offers design alternatives ("three ways to structure this, here are the tradeoffs")
- Sanity checks invariants ("INV-DSP-003 says audio-thread-only, but what about the preview path?")

Cannot grep, cannot run tests, cannot verify. That is its strength.

### Why Two Agents, Two Providers

A single AI develops blind spots. A disconnected chat agent from a different provider brings:

- **Different training biases.** What one model overlooks, another catches.
- **Forced context compression.** You have to explain the architecture to feed it. That forces you to clarify your own thinking.
- **No codebase anchoring.** It judges the design on its merits, not on what is already there.
- **Cheap second opinions.** A 5-minute chat conversation can save hours of wrong-direction work.

In practice our workflow looks like this:

```
1. Human identifies a problem or decision
2. Chat agent discusses architecture, tradeoffs, approach
3. Human decides direction
4. Code agent implements with full codebase context
5. Code agent maintains docs as it works
6. Human reviews and decides what to harden
```

Zip the codebase and feed it to the chat. Ours fits in one conversation. Or just feed it a specific question and the relevant files.

**The code agent executes. The chat agent thinks. The human decides.**

---

## What This Looks Like in Practice: DAWG

We build **DAWG Beatcraft** ([dawgtools.org](https://dawgtools.org) | [itch.io](https://dawg-tools.itch.io/)). This is what works for us.

**The codebase:**

- 1,718 C# source files, 406,000+ lines of code
- 51 assemblies, 13 of which are pure (zero engine references, compiler-enforced)
- Real-time audio DSP, multiplayer networking, MIDI integration, complex UI
- Built by a solo developer using AI-assisted development (Claude Code) over 5 months
- Started from zero Unity experience

**What the methodology gives us:**

- **13 pure assemblies** mean the AI literally cannot introduce platform coupling in domain code. The compiler stops it.
- **146+ invariants** (INV-xxx) actively enforced across domain, DSP, multiplayer, UI, and serialization. The AI reads them at session start and respects them.
- **CLAUDE.md at 400+ lines** is the single most impactful file. Every AI session starts with full architectural context. No repeated explanations, no drifting behavior.
- **Ratchet tests** cap the monolith at 146 files / 40,600 LOC. It was 200+ files. It can only shrink.
- **Framework-first** (OKLab for perceptual color, Smooth Pro for spring animation, UIFactory for all elements, token-resolved themes) means the AI uses the right tools from the start instead of hardcoding values that drift.
- **Roslyn via X-Ray PRO** (our companion tool, also built on this methodology): 40 C# files, 7,000+ LOC. Scans the full codebase in seconds. Architecture rule validation, tier detection from assembly metadata, coupling metrics (fan-in/fan-out/instability), circular dependency detection, hub/bridge detection, blast radius analysis, and dead code identification. When we ask "is this safe to remove?", Roslyn answers with proof, not guesses.

**The hard lesson:** AI agents are great at producing code volume but terrible at maintaining architectural coherence across sessions. Without LDF, each session introduced small boundary violations, magic numbers, subtle invariant breaks. With LDF the codebase improved monotonically. Every session left it strictly no worse.

**Visualization of the codebase using taxonomy principles and LDF:** [YouTube demo](https://www.youtube.com/watch?v=UQ2W9P4EIZQ)

### What the Documentation Tree Looks Like at Scale

Here is an anonymized version of what LDF produces in a real 400k LOC project. This grew organically over months. Nobody sat down and planned all of it on day one. Each piece was added when it was needed: after a hard bug, after stabilizing a subsystem, after making a decision worth preserving.

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

**Key observations:**

- **76 invariant codes** across 35 scopes did not exist on day one. They accumulated over months as real constraints were discovered. Each one was written after something went wrong or after a decision solidified.
- **Bug patterns** are the largest files (one is 142KB). Failures are where the deepest knowledge lives.
- **Code maps** tie files to their doc-sets. When an AI agent asks "what context do I need before editing this file?", the code map answers instantly.
- **Architecture documents** capture the plan and the reasoning. The DSP architecture masterplan is a 10-phase roadmap. It was not written all at once. Each phase was added when the previous one shipped.
- **13 pure assemblies** out of 51 total. Each pure assembly is a compiler-enforced boundary that no AI agent can violate. The number grew from 3 to 13 as the architecture matured.
- **The archive** matters. Old docs get archived, not deleted. History is searchable.

Start with 5 invariants. The structure grows when you need it.

---

## Getting Started

Start with the principles, not the tooling.

### Suggested Path

1. **Read the Core Ideas section above.** Understand doc-sets, invariants, tiered classification, and context loading.
2. **Explore the examples** in `examples/` to see the structure in practice.
3. **Write your AI instruction file** (CLAUDE.md) first. This is the highest-value artifact.
4. **Identify your Tier A files.** The 10 files where a mistake costs the most.
5. **Write invariants for them.** The rules that must never break.
6. **Create your first doc-set.** One subsystem is enough to start.
7. **Add enforcement only when you want it.** Hooks, CI, semantic analysis: pick what fits.

You do not need to classify every file or adopt every piece on day one.

### Adding the Reference Implementation

```bash
# Add as submodule
git submodule add https://github.com/user-hash/LivingDocFramework.git
bash LivingDocFramework/hooks/install.sh

# Create first doc-set
mkdir -p docs/core
touch docs/core/CODE_DOC_MAP.md
touch docs/core/INVARIANTS.md
```

Full installation guide: [docs/INTEGRATION.md](docs/INTEGRATION.md)

---

## Document Types

| Document | Purpose | When to Update |
|----------|---------|----------------|
| `CLAUDE.md` | AI instruction file: architecture rules, invariants, mandates | When rules change |
| `CODE_DOC_MAP.md` | Maps files to tiers | New file created or renamed |
| `INVARIANTS.md` | Safety rules that must hold | When you discover or refine a constraint |
| `BUG_PATTERNS.md` | Known failure modes with prevention | After solving a hard bug |
| `GOLDEN_PATHS.md` | Recommended implementation patterns | When a pattern proves its value |
| `PROJECT_CONTEXT.md` | Persistent project memory across sessions | When decisions are worth preserving |
| `DECISIONS/` | Architecture Decision Records | When a significant choice is made |

---

## Repository Structure

```
LivingDocFramework/
├── core/
│   ├── doc-system.yaml            # Document type schema
│   ├── manifest.yaml              # Master configuration schema
│   ├── load-config.sh             # Config loader (Git + Bash)
│   ├── print-context.sh           # Context lookup tool
│   ├── project-config.template.yaml
│   ├── languages/                 # Language profiles (py, js, go, rs, cs)
│   ├── schemas/                   # JSON schemas for document types
│   └── templates/                 # Document templates
├── hooks/                         # Reference implementation: Git hooks
│   ├── pre-commit                 # Commit-time enforcement
│   └── install.sh
├── protocols/
│   ├── SESSION_PROTOCOL.md        # Session start checklist
│   └── AGENT_PROTOCOL.md         # AI agent compliance guidance
├── commands/
│   └── living-docs.md             # Health check command
├── docs/
│   ├── TUTORIAL.md                # Getting started walkthrough
│   ├── GLOSSARY.md                # Term definitions
│   ├── CONFIG.md                  # Full configuration reference
│   └── INTEGRATION.md            # Installation guide
└── examples/
    ├── quickstart/                # 5-minute onboarding
    ├── doc-systems/               # Doc-set testbed
    └── python-project/            # Structural example
```

---

## Design Principles

1. **Architecture first.** Good architecture makes good docs possible. Not the other way around.
2. **Let the compiler do the work.** Pure assemblies and dependency rules catch more than any code review.
3. **Write it down.** Tiers, invariants, decisions. If it is not written, it does not exist.
4. **Keep it simple.** Git + Bash. No complex CI, no vendor lock-in.
5. **Built for AI.** CLAUDE.md and invariants exist so agents know the rules before they write code.
6. **Start small.** 5 invariants on day one. 76 after five months. It grows with you.
7. **Block, don't suggest.** A blocked commit changes behavior. A wiki suggestion does not.
8. **Only when it matters.** You decide when to harden knowledge. The framework does not nag.

---

## When Not to Use This

- Throwaway prototypes with no architecture to protect
- Projects where you do not control git hooks or the build system
- Teams that already have heavy formal processes
- If you want auto-generated documentation (LDF is manual and intentional)

---

## Requirements

- Git
- Bash 4.0+ (macOS: `brew install bash`, Windows: Git Bash, Linux: usually satisfied)
- For semantic enforcement: Roslyn (C#/.NET), or your language's compiler API equivalent

---

## License

AGPL v3

Using LivingDocFramework as a submodule, reference, or workflow pattern does not impose AGPL obligations on your application code. The license applies to modifications of LivingDocFramework itself.
