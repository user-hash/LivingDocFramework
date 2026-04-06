Hey!

thanks for checking LDF!

I plan to update the repo shortly. During recent development I have learned a lot some new stuff that will greatly benefiting the Living Doc Framework.
For now I will just dump it here, but I plan to follow up with the repo update when I have more time.

In short - for AI assisted development it is crucial to have proper architecture and framework from the start. So as soon as you have builded a prototype that is working, start progressing into hexagonal architecture (of ports and adapters). 

1. Using Hexagonal Architecture as a core component of LDF , we gain modularity, testability, abillity to replace and swap components and much more. https://medium.com/ssense-tech/hexagonal-architecture-there-are-always-two-sides-to-every-story-bc0780ed7d9c
2. The second piece of the puzzle is to use Roslyn (or something similar for your programming language) that enables semantic code understanding - not just text level pattern matching, but actually detecting the lifeblood flowing though codebases. https://github.com/dotnet/roslyn
 
LDF v1 enforced at the text level: "you changed a Tier A file, update the docs or the commit is blocked." That works. But agent can also just bump the doc version, decide to disobey, go around the invariant or just ignore it entierly.

Roslyn breaks through that ceiling by understanding what code means, not just what it says:

● What LDF checks today (text) → What Roslyn enables (semantic)

  - "File X was modified" → "File X now references a type from a forbidden namespace"
  - "Invariant doc wasn't updated" → "The invariant itself is violated in the code"
  - "Tier A file changed" → "This change affects 47 downstream files - here's the blast radius"
  - Manual tier classification → Automatic tier inference from coupling metrics
  - Namespace-level boundary checks → Method-body-level verification - catches fully qualified references that bypass using

  Why this matters for LDF and your codebase too: Text-based hooks can enforce "did you update the docs?" — but Roslyn powered hooks can enforce did your change actually violate an invariant?
  That's the difference between process enforcement and semantic enforcement.

  For example, an invariant like INV-AUTH-001: Password never logged can be verified by Roslyn scanning method bodies for Debug.Log/Console.Write calls that reference fields typed as
  password/credential — something no grep pattern can reliably do.

  Combined with hexagonal architecture, Roslyn can automatically:
  - Classify tiers from coupling metrics instead of manual tagging
  - Detect boundary violations at the type level, not just the namespace level
  - Compute blast radius so you know which doc sets need updating when a port interface changes
  - Find stale invariants that reference code paths that no longer exist

  The key insight: Roslyn turns documentation enforcement from reactive ("you changed a file, update the docs") into proactive ("your change violates this specific constraint, here's the proof").
  It also brings a LOT of benefits to the codebase itself, like live verifications of various calculations, argument ordering, and type level correctness bugs that compile clean, but fail silently at
  runtime. In my own project, Roslyn caught a reflection call where arguments were passed in the wrong order and detected that more advanced math operation would still be better and almost as fastthan appoximated function (while beeing 15% more precise) Roslyn sees the semantic contract, not just the syntax!




# LivingDocFramework

Living documentation enforced at commit time — and loaded before you edit.

LivingDocFramework is a lightweight, tool-agnostic framework that treats context as a first-class artifact in a codebase. It binds critical code to explicit, enforceable documentation using Git hooks and simple protocols — so decisions are recorded while context still exists, not months later.

It does not generate documentation.
It does not analyze correctness.
It forces context to be written, read, and preserved.


## Why this exists

Modern development has a new bottleneck:

- Code is cheap to write (humans, AI, automation)
- Changes happen fast
- Context decays immediately

Critical decisions — why something exists, what must never change, what failed before — are lost first.

LivingDocFramework exists to stop context loss at the moment it happens, using the same enforcement we already trust for tests and formatting.

**The core idea (one sentence):** If code is critical, its context must be explicit — and enforced.


## What LivingDocFramework does

LivingDocFramework introduces four simple concepts.

### 1. Code Tiers

You explicitly classify files by importance:

| Tier | Enforcement |
|------|-------------|
| **Tier A (Critical)** | Changes block commits unless invariants are updated |
| **Tier B (Important)** | Changes warn, but allow commit |
| **Tier C (Standard)** | No enforcement |

This classification is explicit — not inferred.

### 2. Doc-Sets (documentation lives next to code)

Each subsystem owns its documentation:

```
docs/api/
├── CODE_DOC_MAP.md    # Maps files to tiers
├── INVARIANTS.md      # Constraints that must be preserved
└── BUG_PATTERNS.md    # Known issues and patterns
```

- Presence of `CODE_DOC_MAP.md` defines a doc-set
- Files are mapped explicitly to tiers
- Invariants and bug knowledge live where they belong
- No central wiki. No hidden knowledge.

### 3. Enforcement at commit time (reactive)

Git pre-commit hooks enforce the rules:

- Modify Tier A code → you must update invariants
- Forget → commit is blocked
- Emergency → `git commit --no-verify` (explicit escape hatch)

No CI required. No runtime overhead. Git + Bash only.

### 4. Context loading before editing (proactive)

LivingDocFramework provides a portable context lookup tool:

```bash
./LivingDocFramework/core/print-context.sh path/to/file.py
```

It tells you:

- Which tier the file is
- Which doc-set it belongs to
- Which documents must be read
- Which invariants apply

This enables a better workflow:

```
Load context → understand → edit with intent → verify → persist learning
```

**Commit blocking is the seatbelt. Context loading is the engine.**


## What this gives you (in practice)

- Architectural decisions don't disappear
- Critical assumptions are written down when they change
- AI-generated code cannot silently bypass constraints
- Refactors remain explainable months later
- "Why is this like this?" has an answer in the repo

Especially valuable for:

- Fast-moving projects
- AI-assisted workflows
- Small teams with large codebases
- Long-lived systems without heavy process


## What this is not

LivingDocFramework is **not**:

- Automatic documentation generation
- A linter
- A style guide
- A correctness checker
- An AI replacement

It enforces **accountability**, not correctness.


## Quickstart (5 minutes)

The fastest way to understand LivingDocFramework is to feel it work.

**Start here:** [examples/quickstart/](examples/quickstart/)

In under 5 minutes you will:

1. Install hooks
2. Change a Tier A file
3. Get blocked with a clear error
4. Update documentation
5. Commit successfully

That failure → fix loop is the core learning experience.


## Typical workflow

1. Developer (or automation) changes code
2. Tier A change is detected
3. Commit is blocked if invariants aren't updated
4. Rationale is written while context is fresh
5. Commit succeeds
6. Future changes inherit that context

No meetings. No tickets. No tribal knowledge.


## Repository structure

```
LivingDocFramework/
├── core/
│   ├── load-config.sh
│   ├── print-context.sh           # Context lookup (portable core)
│   └── templates/
│       └── project-context.template.md
├── hooks/
│   ├── pre-commit                 # Enforcement
│   └── install.sh
├── protocols/                     # Human-readable rules
│   ├── SESSION_PROTOCOL.md        # Version sync + loading order
│   └── AGENT_PROTOCOL.md          # Sub-agent compliance
├── docs/
│   ├── TUTORIAL.md
│   ├── GLOSSARY.md
│   ├── CONFIG.md
│   └── INTEGRATION.md
└── examples/
    ├── quickstart/                # Runnable onboarding example
    ├── doc-systems/               # Testbed for print-context.sh
    └── python-project/            # Structural example
```


## Installation (existing project)

```bash
# From your repo root
git submodule add https://github.com/user-hash/LivingDocFramework.git
bash LivingDocFramework/hooks/install.sh
```

Then:

1. Create a doc-set (`docs/*/CODE_DOC_MAP.md`)
2. Define tiers in `CODE_DOC_MAP.md`
3. Add invariants
4. Commit with confidence

Full instructions: [docs/INTEGRATION.md](docs/INTEGRATION.md)


## Using proactive context loading

To see required context for any file:

```bash
./LivingDocFramework/core/print-context.sh src/api/auth.py
```

Example output:

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

The core framework does not depend on any IDE or AI tool.


## Design principles

- **Locality** — docs live next to code
- **Explicitness** — nothing inferred, nothing magic
- **Minimalism** — Git + Bash only in core
- **Enforcement over advice**
- **Human-readable over clever**


## When not to use this

LivingDocFramework may not be a good fit if:

- Your codebase is throwaway
- You don't control commit hooks
- You already enforce design via heavy process
- You want auto-generated documentation


## Requirements

- Git
- Bash 4.0+ (macOS: `brew install bash`, Windows: Git Bash, Linux: usually satisfied)


## Status

- Used in production
- Actively developed
- Stable core, evolving onboarding
- Designed for long-lived codebases


## License

AGPL v3

Using LivingDocFramework as a submodule or hook does not impose AGPL obligations on your application code. The license applies to modifications of LivingDocFramework itself.
