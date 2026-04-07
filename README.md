# LivingDocFramework

How to keep a codebase architecturally coherent when AI writes most of the code.

We built this while shipping a 400k LOC Unity project with AI assistance. This is what works for us. Any AI tool, any programming language, any team size.

**How to use this repo:** Read the principles below. Tell your AI agent to read them too. Implement what makes sense for your project. The reference implementation (hooks, scripts) is a bonus, not the point.

---

## The Problem

AI produces code faster than anyone can review it. The bottleneck is no longer writing code. It is **architectural coherence**.

Without explicit structure, every AI session introduces boundary violations, magic numbers, and subtle invariant breaks. The codebase drifts. Architecture erodes. Nobody notices until it is expensive.

---

## Seven Core Ideas

Each stands alone. They compound when combined. [Full details with examples](docs/PRINCIPLES.md)

### 1. Hexagonal Architecture
Separate domain logic from infrastructure. Pure domain has zero platform imports. The compiler enforces the boundary, not code review.

### 2. Pure Assemblies
Group code into modules with explicit dependency rules. Some are pure: zero platform references, compiler-enforced. AI cannot break what the build system protects.

### 3. Invariant-Driven Development
Critical rules written as numbered codes: `INV-DSP-003: Voice mutation is audio-thread-only`. The AI reads them before writing code. They are enforced, not aspirational.

### 4. Framework Over Hardcoding
If a system already provides the answer, use it. OKLab for colors, not raw hex. Springs for animation, not manual lerp. Factory methods for UI, not raw constructors.

### 5. Tiered Code Classification
Not all code is equal. Tier A = critical (commits blocked without doc updates). Tier B = important (warnings). Tier C = standard. Classification is explicit in `CODE_DOC_MAP.md`.

### 6. AI Instruction File (CLAUDE.md)
One file at the project root. Every invariant, every boundary, every framework mandate. AI loads it at session start. Most impactful file in the repo.

### 7. Ratchet Testing
Metrics that can only improve. Monolith file count capped. LOC capped. Platform imports in domain = 0. Every session leaves the codebase no worse.

---

## Roslyn: Semantic Code Understanding

Grep finds strings. Roslyn sees the lifeblood flowing through the codebase. For C#/.NET, this is a game changer. **Every language needs a Roslyn equivalent.** [Full Roslyn deep-dive](docs/ROSLYN.md)

Highlights:
- Traced a rogue frequency to a wet signal fed into the wrong buffer. Seconds vs a week of manual debugging.
- Catches architecture violations inside method bodies, not just at the `using` level.
- Finds dead code by tracing real call chains, not text matches.
- Silent runtime bugs that compile clean but fail in production.

---

## Two AI Agents + Human

The code agent executes. The chat agent thinks. The human decides. [Full workflow](docs/WORKFLOW.md)

- **Code agent** (embedded): full codebase access, maintains docs, runs verification
- **Chat agent** (disconnected): no terminal, no git, fresh codebase every conversation. Spots what the code agent misses. Ideally a different provider.
- **Human**: architects, decides when to harden knowledge, picks direction

---

## Proven on DAWG Beatcraft

406,000 lines of C#. 51 assemblies, 13 pure. 76 invariants across 35 scopes. Solo dev, 5 months, zero prior Unity experience. [Full case study with anonymized doc tree](docs/CASE_STUDY.md)

[dawgtools.org](https://dawgtools.org) | [itch.io](https://dawg-tools.itch.io/) | [YouTube visualization](https://www.youtube.com/watch?v=UQ2W9P4EIZQ)

---

## Getting Started

1. Read the [principles](docs/PRINCIPLES.md)
2. Write your CLAUDE.md. This is the highest-value artifact.
3. Identify 10 critical files. Write 5 invariants.
4. Create a doc-set: `docs/core/CODE_DOC_MAP.md` + `docs/core/INVARIANTS.md`
5. Add enforcement when you want it (hooks, CI, Roslyn, or just conventions)

**Optional:** add the reference implementation as a submodule:
```bash
git submodule add https://github.com/user-hash/LivingDocFramework.git
bash LivingDocFramework/hooks/install.sh
```

---

## Document Types

| Document | Purpose | When to Update |
|----------|---------|----------------|
| `CLAUDE.md` | AI instruction file | When rules change |
| `CODE_DOC_MAP.md` | Maps files to tiers | File created or renamed |
| `INVARIANTS.md` | Safety rules | When you discover a constraint |
| `BUG_PATTERNS.md` | Known failure modes | After solving a hard bug |
| `GOLDEN_PATHS.md` | Best practices | When a pattern proves its value |
| `PROJECT_CONTEXT.md` | Project memory | When decisions worth preserving |

---

## Design Principles

1. **Architecture first.** Good architecture makes good docs possible. Not the other way around.
2. **Let the compiler do the work.** Pure assemblies catch more than any code review.
3. **Write it down.** If it is not written, it does not exist.
4. **Keep it simple.** Git + Bash. No complex CI, no vendor lock-in.
5. **Built for AI.** CLAUDE.md and invariants exist so agents know the rules before they write code.
6. **Start small.** 5 invariants on day one. 76 after five months. It grows with you.
7. **Block, don't suggest.** A blocked commit changes behavior.
8. **Only when it matters.** You decide when to harden knowledge. The framework does not nag.

---

## Deep Dives

| Page | What it covers |
|------|---------------|
| [Principles](docs/PRINCIPLES.md) | Full 7 pillars with code examples and conventions |
| [Roslyn](docs/ROSLYN.md) | Semantic code understanding for C#/.NET |
| [Workflow](docs/WORKFLOW.md) | Human + Code Agent + Chat Agent, knowledge hardening |
| [Case Study](docs/CASE_STUDY.md) | DAWG numbers, anonymized doc tree, lessons |
| [Tutorial](docs/TUTORIAL.md) | 10-minute hands-on walkthrough |
| [Integration](docs/INTEGRATION.md) | Adding LDF to an existing project |
| [Configuration](docs/CONFIG.md) | Full config reference |
| [Glossary](docs/GLOSSARY.md) | Term definitions |

---

## Repo Structure

```
LivingDocFramework/
├── docs/               # Deep-dive pages (principles, roslyn, workflow, case study)
├── core/               # Config loader, context lookup, templates, schemas, language profiles
├── hooks/              # Reference implementation: pre-commit, commit-msg, installer
├── protocols/          # Session and agent protocols
├── commands/           # Reusable AI command workflows
└── examples/           # Quickstart, doc-systems testbed, sample workflow
```

---

## License

AGPL v3. Using LDF as a submodule or reference does not impose AGPL on your code. The license applies to modifications of LDF itself.
