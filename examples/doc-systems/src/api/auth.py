# auth.py - Authentication module (Tier A)
# This is a critical file - changes require INVARIANTS.md update

MAX_RETRIES = 3

def authenticate(username, password):
    """
    Authenticate user with bounded retry attempts.

    INV-AUTH-001: Retry attempts bounded to MAX_RETRIES
    """
    for attempt in range(MAX_RETRIES):
        result = _try_auth(username, password)
        if result.success:
            return result
    return AuthResult(success=False, error="Max retries exceeded")

def _try_auth(username, password):
    # INV-AUTH-002: Password never logged
    # Note: password is not included in any log output
    return _backend_auth(username, password)
