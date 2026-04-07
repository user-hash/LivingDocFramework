# Getting Started

Time: 10 minutes


## What You Will Learn

This tutorial walks you through the core LDF experience: classifying a file, writing an invariant, and seeing the enforcement loop in action.

You do not need to adopt every part of LDF to get value. Start here, expand when you need to.


## Prerequisites

- Git
- Bash 4.0+ (macOS: `brew install bash`, Windows: Git Bash)


## Step 1: Set Up (1 min)

```bash
cd examples/quickstart
git init
git add .
git commit -m "init"

# Install hooks (path relative to quickstart folder)
bash ../../hooks/install.sh
```


## Step 2: Understand the Structure

Look at what the quickstart gives you:

```
quickstart/
├── src/api/
│   ├── __init__.py      # Version
│   └── auth.py          # Classified as Tier A
├── docs/api/
│   ├── CODE_DOC_MAP.md  # Maps auth.py to Tier A
│   └── INVARIANTS.md    # Safety rules for this doc-set
├── living-doc-config.yaml
└── CHANGELOG.md
```

`docs/api/CODE_DOC_MAP.md` explicitly classifies `auth.py` as Tier A. This means changes to `auth.py` trigger enforcement.


## Step 3: Trigger Enforcement (Intentional)

Open `src/api/auth.py`. Change:

```python
MAX_RETRY_ATTEMPTS = 3
```

to:

```python
MAX_RETRY_ATTEMPTS = 5
```

Commit without updating docs:

```bash
git add src/api/auth.py
git commit -m "increase retry limit"
```

You will see:

```
Living Documentation - Pre-Commit Validation

Files staged: 1

Tier A: src/api/auth.py
   Mapped in: docs/api/CODE_DOC_MAP.md
   Requires:  docs/api/INVARIANTS.md

ERROR: Tier A file changed but INVARIANTS not updated
   Missing update: docs/api/INVARIANTS.md

   Please:
     1. Read the invariants in docs/api/INVARIANTS.md
     2. Cite which invariants you're respecting
     3. Add new invariants if needed

   To skip (emergency only): git commit --no-verify
```

This is the enforcement loop: you changed a critical file, the system asks you to record your reasoning.


## Step 4: Record Your Decision (2 min)

Open `docs/api/INVARIANTS.md`. Update or add a note:

```markdown
**Last verified:** [Today] - Increased to 5 because [your reason]
```

Commit both files:

```bash
git add docs/api/INVARIANTS.md src/api/auth.py
git commit -m "increase retry limit with rationale"
```

Output:

```
Living Documentation - Pre-Commit Validation

Files staged: 2

Tier A: src/api/auth.py
   Mapped in: docs/api/CODE_DOC_MAP.md
   Requires:  docs/api/INVARIANTS.md

Pre-commit checks passed
```


## Step 5: Try Context Loading

From the quickstart directory, look up the context for any file:

```bash
../../core/print-context.sh src/api/auth.py
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
```

This is the proactive side of LDF: load context before editing, not just after.


## When to Use Enforcement

The hooks are one tool, not a mandate. In practice:

- **Use hooks** when you want automated reminders for critical files
- **Skip hooks** (`--no-verify`) during emergencies, follow up with a doc-fix commit
- **Don't use hooks at all** if your team prefers manual knowledge hardening

The core value is the structure (doc-sets, invariants, code maps), not the enforcement mechanism.


## What's Next

- [Integration Guide](INTEGRATION.md) — Add LDF to your project
- [Configuration](CONFIG.md) — Customize behavior
- [Glossary](GLOSSARY.md) — Terminology
- Back to [README](../README.md) — Full methodology
