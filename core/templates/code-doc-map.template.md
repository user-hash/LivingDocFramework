# Code Documentation Map - {{SUBSYSTEM}}

This file defines which source files belong to this doc-set and their documentation tiers.

> **Doc-Set Rule**: Any folder containing `CODE_DOC_MAP.md` is a doc-set.
> When a Tier A file changes, the sibling `INVARIANTS.md` must be updated.

---

## Tier A (Critical)

Files requiring invariant citation before editing.

| File | Tier | Description | Invariant |
|------|------|-------------|-----------|
| `src/{{subsystem}}/Manager.{{ext}}` | TIER A | Core manager | INV-{{ID}}-001 |

<!--
IMPORTANT: Use repo-relative paths from project root.
Example: `src/Multiplayer/SyncManager.cs` (CORRECT)
         `SyncManager.cs` (WRONG - basename only)
-->

---

## Tier B (Important)

Files requiring documentation awareness.

| File | Description |
|------|-------------|
| `src/{{subsystem}}/Service.{{ext}}` | Service layer |

---

## Tier C (Standard)

Regular files with standard documentation.

| File | Description |
|------|-------------|
| `src/{{subsystem}}/Utils.{{ext}}` | Utilities |

---

## Related Documentation

- [INVARIANTS.md](./INVARIANTS.md) - Safety rules for this subsystem
- [BUG_PATTERNS.md](./BUG_PATTERNS.md) - Known issues and prevention
- [GOLDEN_PATHS.md](./GOLDEN_PATHS.md) - Best practices
- [DECISIONS/](./DECISIONS/) - Architecture decisions (ADR-{{ID}}-NNN)

---

<!--
Path Format Rules:
- All entries MUST use repo-relative paths from project root
- No basename-only entries (ambiguous across subsystems)
- No absolute paths (non-portable)

Tier A Enforcement:
- When Tier A file changes, pre-commit hook requires sibling INVARIANTS.md update
- Hook matches TIER A + file path on the SAME LINE (case-insensitive)
-->
