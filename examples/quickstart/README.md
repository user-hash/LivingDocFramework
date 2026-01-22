# Quickstart Example

A runnable example to experience LivingDocFramework in 5 minutes.

## Setup

```bash
cd examples/quickstart
git init
git add .
git commit -m "init"

# Install hooks (path relative to quickstart folder)
../../hooks/install.sh
```

## Try It

1. **Trigger a failure** - Edit `src/api/auth.py`, change `MAX_RETRY_ATTEMPTS = 3` to `5`
2. **Commit without docs** - `git add src/api/auth.py && git commit -m "test"`
3. **See the block** - Hook rejects because `docs/api/INVARIANTS.md` wasn't updated
4. **Fix it** - Update `docs/api/INVARIANTS.md` with your rationale
5. **Commit succeeds** - `git add docs/api/INVARIANTS.md && git commit -m "test"`

## Structure

```
quickstart/
├── src/api/
│   ├── __init__.py      # Version
│   └── auth.py          # TIER A file
├── docs/api/
│   ├── CODE_DOC_MAP.md  # Marks auth.py as Tier A
│   └── INVARIANTS.md    # Safety rules
├── living-doc-config.yaml
└── CHANGELOG.md
```

## Learn More

- [Tutorial](../../docs/TUTORIAL.md) - Full walkthrough
- [Integration Guide](../../docs/INTEGRATION.md) - Add to your project
