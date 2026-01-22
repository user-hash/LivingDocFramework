# LivingDocFramework

Living documentation enforced at commit time — before context is lost.

LivingDocFramework is a lightweight framework that binds critical code to explicit, enforceable documentation using Git hooks.

It does not generate docs.
It does not analyze correctness.
It forces context to be written while it still exists.


## Why this exists

Modern development has a new bottleneck:

- Code is cheap to write
- Changes happen fast
- Context decays immediately

Whether changes come from humans or automated tools, the result is the same: Critical decisions get lost.

LivingDocFramework treats context as a first-class artifact and enforces it the same way we enforce tests or formatting.

If critical code changes, the framework requires you to explain why.


## What LivingDocFramework does

LivingDocFramework introduces three simple ideas:

### 1. Code Tiers

You explicitly classify files by importance:

- **Tier A (Critical)** – blocks commits if documentation isn't updated
- **Tier B (Important)** – warns, but allows commit
- **Tier C (Standard)** – no enforcement

### 2. Doc-Sets

Each subsystem owns its documentation, stored next to it:

```
docs/api/
├── CODE_DOC_MAP.md
├── INVARIANTS.md
└── BUG_PATTERNS.md
```

Presence of `CODE_DOC_MAP.md` defines a doc-set.

### 3. Git Hook Enforcement

Pre-commit hooks enforce the rules:

- Modify Tier A code → you must update its invariants
- Forget → commit is blocked
- Emergency → `--no-verify` exists (explicit escape hatch)

No CI required.
No runtime overhead.
No dependencies beyond Git + Bash.


## What this gives you (in practice)

- Architectural decisions don't disappear
- Critical assumptions are written down when they change
- AI-generated code cannot silently bypass constraints
- Refactors stay explainable months later
- "Why is this like this?" has an answer in the repo

This is especially valuable in:

- Fast-moving projects
- AI-assisted workflows
- Small teams with large codebases
- Long-lived systems without heavy process


## What this is not

LivingDocFramework is **not**:

- Automatic documentation generation
- A linter
- A style guide
- An AI replacement
- Correctness verification

LivingDoc enforces *accountability*, not correctness.


## Quickstart (5 minutes)

The fastest way to understand LivingDocFramework is to feel it block a commit.

**Start here:** [examples/quickstart/](examples/quickstart/)

In under 5 minutes you will:

1. Install hooks
2. Change a critical file
3. Get blocked with a clear error
4. Update documentation
5. Commit successfully

This failure → fix loop is the core learning experience.


## Typical workflow

1. Developer (or automation) changes code
2. Commit hook detects Tier A change
3. Commit is blocked if invariants aren't updated
4. Rationale is written while context is fresh
5. Commit succeeds
6. Future changes inherit that context

No meetings. No tickets. No tribal knowledge.


## Repository structure

```
LivingDocFramework/
├── hooks/                 # Pre-commit hooks (core enforcement)
├── docs/                  # Framework documentation
│   ├── TUTORIAL.md
│   ├── GLOSSARY.md
│   ├── CONFIG.md
│   └── INTEGRATION.md
├── examples/
│   ├── quickstart/        # Runnable onboarding example (recommended)
│   └── python-project/    # Structural example
└── core/templates/        # Doc-set templates
```


## Installation (existing project)

Basic flow:

```bash
# From your repo root
git submodule add https://github.com/user-hash/LivingDocFramework.git
./LivingDocFramework/hooks/install.sh
```

Then:

1. Create a doc-set
2. Define tiers in `CODE_DOC_MAP.md`
3. Add invariants
4. Commit with confidence

Full instructions: [docs/INTEGRATION.md](docs/INTEGRATION.md)


## Configuration

LivingDocFramework is configured via YAML.

You can control:

- Tier enforcement behavior
- Warning vs blocking
- File discovery
- Version tracking

See: [docs/CONFIG.md](docs/CONFIG.md)


## Documentation

- [docs/TUTORIAL.md](docs/TUTORIAL.md) — getting started (5 min)
- [docs/GLOSSARY.md](docs/GLOSSARY.md) — terminology
- [docs/CONFIG.md](docs/CONFIG.md) — configuration options
- [docs/INTEGRATION.md](docs/INTEGRATION.md) — integrating into existing projects
- [hooks/README.md](hooks/README.md) — hook behavior and customization


## Design principles

- **Locality** – docs live next to code
- **Explicitness** – nothing inferred
- **Minimalism** – Git + Bash only
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
- Designed for long-lived codebases
- Stable core, evolving onboarding


## License

AGPL v3

Using LivingDocFramework as a submodule or hook does not impose AGPL obligations on your application code. The license applies to modifications of LivingDocFramework itself.
