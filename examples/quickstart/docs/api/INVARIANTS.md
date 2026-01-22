# Invariants - API

## INV-AUTH-001: Retry attempts are bounded and rationale is documented

Any change to:
- MAX_RETRY_ATTEMPTS
- retry logic
- failure conditions

REQUIRES updating this invariant with rationale.

**Rationale:** Unbounded retries cause account lockout cascades.

**Enforced in:** `src/api/auth.py`

**Last verified:** Initial creation
