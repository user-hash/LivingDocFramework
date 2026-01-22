# adapter.py - Storage adapter (Tier B)
# Important file - warnings on changes without doc updates

def save_data(key, value):
    """
    Save data to storage backend.

    INV-STORE-001: Data loss prevented
    """
    if not _backend_available():
        raise StorageUnavailable("Backend not ready")
    return _backend_save(key, value)

def load_data(key):
    """Load data from storage backend."""
    return _backend_load(key)
