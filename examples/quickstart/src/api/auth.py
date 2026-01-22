"""
Authentication module - TIER A (Critical)
Changes require updating docs/api/INVARIANTS.md
"""

MAX_RETRY_ATTEMPTS = 3  # INV-AUTH-001


def authenticate(username: str, password: str) -> bool:
    """Authenticate a user."""
    if not username or not password:
        return False
    return len(password) >= 8


def retry_login(username: str, password: str, attempts: int = 0) -> bool:
    """Retry login. Respects INV-AUTH-001."""
    if attempts >= MAX_RETRY_ATTEMPTS:
        return False
    if authenticate(username, password):
        return True
    return retry_login(username, password, attempts + 1)
