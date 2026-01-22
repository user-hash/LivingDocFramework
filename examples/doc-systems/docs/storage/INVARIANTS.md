# Invariants: Storage Subsystem

Constraints that must be preserved.

## INV-STORE-001: Data loss prevented

Storage operations must fail explicitly rather than silently lose data.

**Why:** Silent data loss is catastrophic and hard to detect.

**Must preserve:**
- Check backend availability before write
- Raise exception if backend unavailable
- Never return success without confirmation
