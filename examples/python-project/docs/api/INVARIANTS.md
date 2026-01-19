# Invariants - API

Safety rules for the API subsystem.

---

## INV-API-001: Authentication Token Validation

**Rule:** All protected endpoints MUST validate authentication tokens before processing.

**Rationale:** Prevents unauthorized access to user data and system resources.

**Violation Example:**
```python
# WRONG - No auth check
@app.route('/api/user/profile')
def get_profile():
    return current_user.profile  # Who is current_user?
```

**Correct Example:**
```python
# CORRECT - Auth required
@app.route('/api/user/profile')
@require_auth  # Validates token first
def get_profile():
    return current_user.profile
```

**Linked Tests:** `test_api_auth.py::test_protected_endpoints_require_auth`

---

## INV-API-002: Permission Checks

**Rule:** Resource access MUST check user permissions before returning data.

**Rationale:** Users should only access resources they own or have explicit permission for.

**Violation Example:**
```python
# WRONG - No permission check
def get_document(doc_id):
    return Document.query.get(doc_id)  # Any user can get any doc
```

**Correct Example:**
```python
# CORRECT - Permission check
def get_document(doc_id):
    doc = Document.query.get(doc_id)
    if not current_user.can_access(doc):
        raise Forbidden()
    return doc
```

**Linked Tests:** `test_api_permissions.py::test_document_access_control`

---

## Version History

- 2024-01-15: Initial invariants for API doc-set
