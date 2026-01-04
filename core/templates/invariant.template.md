## INV-{SYSTEM}-{NUMBER}: {RULE_TITLE}

**System:** {SYSTEM}
**Severity:** {SEVERITY}
**Citation Required:** Yes

### Rule

> {RULE_STATEMENT}

### Rationale

{RATIONALE_DESCRIPTION}

### Violation Example

```csharp
// VIOLATION - This breaks the invariant:
{VIOLATION_CODE}
```

### Correct Example

```csharp
// CORRECT - This follows the invariant:
{CORRECT_CODE}
```

### Linked Tests

- `{TEST_FILE_1}::{TEST_METHOD_1}`
- `{TEST_FILE_2}::{TEST_METHOD_2}`

### Affected Files

- `{FILE_1}`
- `{FILE_2}`

### Prevents Patterns

- PATTERN-{N1}: {PATTERN_TITLE_1}
- PATTERN-{N2}: {PATTERN_TITLE_2}

### Automated Check

```bash
# Run this to check for violations:
{CHECK_COMMAND}
```
