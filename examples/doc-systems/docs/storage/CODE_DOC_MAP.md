# Code-Doc Map: Storage Subsystem

Maps storage source files to their documentation and tier.

## File Mapping

| File | Tier | Description |
|------|------|-------------|
| `src/storage/adapter.py` | B | Storage backend adapter |
| `src/storage/cache.py` | C | Caching layer |

## Tier Definitions

- **Tier A (Critical)**: Commits blocked if INVARIANTS.md not updated
- **Tier B (Important)**: Warning issued, commit allowed
- **Tier C (Standard)**: No enforcement

## Related Docs

- [INVARIANTS.md](INVARIANTS.md) - Constraints that must be preserved
