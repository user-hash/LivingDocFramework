# Getting Started

Time: 5 minutes


## Why LivingDoc Blocks Commits

Blocking is intentional.

LivingDoc assumes:
- Critical code changes are expensive
- Documentation debt compounds faster than code debt
- Humans and AI both forget context

Blocking forces decisions to be recorded while context is fresh.


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
../../hooks/install.sh
```


## Step 2: Trigger a Failure (Intentional)

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

<details>
<summary>Why this happens</summary>

`auth.py` is TIER A in `docs/api/CODE_DOC_MAP.md`.

Tier A files require their sibling `INVARIANTS.md` to be updated.

This forces you to record *why* you changed critical code.
</details>


## Step 3: Fix It (2 min)

Open `docs/api/INVARIANTS.md`. Update the "Last verified" line:

```markdown
**Last verified:** [Today] - Increased to 5 because [your reason]
```

Commit:

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


## Escape Hatch

Use `--no-verify` only during active incidents. Follow up with a doc-fix commit.


## Typical Workflow

1. Developer or AI changes code
2. Hook blocks if context is missing
3. Developer records decision
4. Commit succeeds
5. Future changes inherit context


## What's Next

- [Integration Guide](INTEGRATION.md) - Add to your project
- [Configuration](CONFIG.md) - Customize behavior
- [Glossary](GLOSSARY.md) - Terminology
