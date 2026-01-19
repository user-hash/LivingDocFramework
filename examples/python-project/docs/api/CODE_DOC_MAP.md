# Code Documentation Map - API

This doc-set covers the REST API endpoints and related services.

---

## Tier A (Critical)

Files requiring invariant citation before editing:

| File | Tier | Description | Invariant |
|------|------|-------------|-----------|
| `src/api/auth.py` | TIER A | Authentication endpoints | INV-API-001 |
| `src/api/permissions.py` | TIER A | Authorization logic | INV-API-002 |

---

## Tier B (Important)

Files requiring documentation awareness:

| File | Description |
|------|-------------|
| `src/api/users.py` | User CRUD endpoints |
| `src/api/products.py` | Product endpoints |

---

## Tier C (Standard)

| File | Description |
|------|-------------|
| `src/api/utils.py` | API utilities |
| `src/api/serializers.py` | Data serialization |

---

## Related Documentation

- [INVARIANTS.md](./INVARIANTS.md) - API safety rules
