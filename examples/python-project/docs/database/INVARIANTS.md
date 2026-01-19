# Invariants - Database

Safety rules for the database subsystem.

---

## INV-DB-001: Model Field Validation

**Rule:** All model fields MUST have appropriate validation constraints.

**Rationale:** Prevents invalid data from entering the database.

**Violation Example:**
```python
# WRONG - No validation
class User(Model):
    email = Column(String)  # No length limit, no format check
```

**Correct Example:**
```python
# CORRECT - Proper validation
class User(Model):
    email = Column(String(255), nullable=False)

    @validates('email')
    def validate_email(self, key, value):
        assert '@' in value, "Invalid email"
        return value
```

**Linked Tests:** `test_models.py::test_field_validation`

---

## INV-DB-002: Migration Safety

**Rule:** Migrations MUST be reversible and MUST NOT delete data without backup.

**Rationale:** Allows rollback in case of issues; prevents accidental data loss.

**Violation Example:**
```python
# WRONG - Irreversible, data loss
def upgrade():
    op.drop_column('users', 'legacy_field')
```

**Correct Example:**
```python
# CORRECT - Reversible, data preserved
def upgrade():
    op.rename_column('users', 'legacy_field', 'legacy_field_deprecated')

def downgrade():
    op.rename_column('users', 'legacy_field_deprecated', 'legacy_field')
```

**Linked Tests:** `test_migrations.py::test_migration_reversibility`

---

## INV-DB-003: Transaction Boundaries

**Rule:** Multi-step database operations MUST use explicit transactions.

**Rationale:** Ensures atomicity - all steps succeed or all fail together.

**Violation Example:**
```python
# WRONG - No transaction, partial failure possible
def transfer_funds(from_id, to_id, amount):
    from_account.balance -= amount
    db.session.commit()  # What if next line fails?
    to_account.balance += amount
    db.session.commit()
```

**Correct Example:**
```python
# CORRECT - Atomic transaction
def transfer_funds(from_id, to_id, amount):
    with db.session.begin():
        from_account.balance -= amount
        to_account.balance += amount
        # Both commit together or both rollback
```

**Linked Tests:** `test_transactions.py::test_atomic_operations`

---

## Version History

- 2024-01-15: Initial invariants for database doc-set
