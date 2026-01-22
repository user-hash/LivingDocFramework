# Invariants: API Subsystem

Constraints that must be preserved. Update this when changing Tier A files.

## INV-AUTH-001: Retry attempts bounded

Authentication retries are limited to `MAX_RETRIES` (currently 3).

**Why:** Unbounded retries can cause:
- Account lockouts at identity provider
- Denial of service on auth backend
- Infinite loops if credential is invalid

**Must preserve:**
- Loop uses `range(MAX_RETRIES)`, not `while True`
- Retry count is configurable but bounded

## INV-AUTH-002: Password never logged

Passwords must never appear in logs, errors, or debug output.

**Why:** Credential exposure in logs is a security incident.

**Must preserve:**
- No `print(password)` or `log(password)`
- Error messages use sanitized output
- Debug mode does not change this rule
