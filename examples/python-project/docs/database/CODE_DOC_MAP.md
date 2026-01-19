# Code Documentation Map - Database

This doc-set covers database models, migrations, and data access.

---

## Tier A (Critical)

Files requiring invariant citation before editing:

| File | Tier | Description | Invariant |
|------|------|-------------|-----------|
| `src/db/models.py` | TIER A | Core data models | INV-DB-001 |
| `src/db/migrations.py` | TIER A | Schema migrations | INV-DB-002 |
| `src/db/transactions.py` | TIER A | Transaction handling | INV-DB-003 |

---

## Tier B (Important)

| File | Description |
|------|-------------|
| `src/db/queries.py` | Query builders |
| `src/db/indexes.py` | Index definitions |

---

## Tier C (Standard)

| File | Description |
|------|-------------|
| `src/db/utils.py` | Database utilities |

---

## Related Documentation

- [INVARIANTS.md](./INVARIANTS.md) - Database safety rules
