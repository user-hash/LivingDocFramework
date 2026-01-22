# Code-Doc Map: API Subsystem

Maps API source files to their documentation and tier.

## File Mapping

| File | Tier | Description |
|------|------|-------------|
| `src/api/auth.py` | A | Authentication + retry behavior |
| `src/api/users.py` | B | User management endpoints |

## Tier Definitions

- **Tier A (Critical)**: Commits blocked if INVARIANTS.md not updated
- **Tier B (Important)**: Warning issued, commit allowed
- **Tier C (Standard)**: No enforcement

## Related Docs

- [INVARIANTS.md](INVARIANTS.md) - Constraints that must be preserved
- [BUG_PATTERNS.md](BUG_PATTERNS.md) - Known issues and patterns
