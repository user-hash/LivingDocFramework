# Bug Patterns

Documented anti-patterns discovered through debugging. These patterns help prevent recurring bugs and provide quick diagnosis for common issues.

**Summary**: {PATTERN_COUNT} patterns documented, {CATEGORY_COUNT} categories

---

## Quick Reference

| ID | Pattern | Category | Severity | First Seen |
|----|---------|----------|----------|------------|
| PATTERN-001 | [Example Pattern Name](#pattern-001-example-pattern-name) | Threading | High | 2026-01-01 |

---

## Threading Patterns

### PATTERN-001: Example Pattern Name

**Category:** Threading
**Severity:** High
**Frequency:** Common
**First Seen:** 2026-01-01
**Occurrences:** 3

#### Root Cause

Brief description of why this bug occurs. What is the underlying technical reason?

#### Symptoms

- Observable symptom 1 (e.g., "Application freezes on startup")
- Observable symptom 2 (e.g., "Log shows deadlock warning")
- Observable symptom 3 (e.g., "CPU spikes to 100%")

#### Detection

```bash
# Grep pattern to find potential instances:
grep -rn "lock.*while" --include="*.py"
```

#### Bad Code Example

```python
# DON'T DO THIS:
def process_data():
    with lock:
        while condition:  # Holding lock while waiting
            time.sleep(0.1)
```

#### Good Code Example

```python
# DO THIS INSTEAD:
def process_data():
    while True:
        with lock:
            if not condition:
                break
            # Quick operation only
        time.sleep(0.1)  # Sleep outside lock
```

#### Fix

Release the lock before any waiting operation. Use condition variables or events for proper synchronization.

#### Prevention

- Never hold locks while sleeping or waiting
- Use timeout-based locks: `lock.acquire(timeout=1.0)`
- Prefer condition variables for wait/notify patterns

#### Related

- Patterns: PATTERN-002 (if related)
- Files: `src/threading/worker.py`
- Commits: abc1234

---

## API Patterns

### PATTERN-002: [Pattern Name]

[Use the same structure as above]

---

## Database Patterns

### PATTERN-003: [Pattern Name]

[Use the same structure as above]

---

## Adding New Patterns

When you discover a bug that might recur:

1. **Assign an ID**: Use the next available PATTERN-XXX number
2. **Categorize**: Choose the most relevant category (Threading, API, Database, UI, etc.)
3. **Document root cause**: Explain WHY this bug occurs
4. **Show examples**: Include bad AND good code examples
5. **Add detection**: Provide grep/search patterns to find similar issues
6. **Link related**: Connect to invariants, files, and commits

### Template

Copy from `core/templates/pattern.template.md` for a single pattern entry.

---

## Integration with Bug Tracker

When fixing bugs:
1. Check BUG_PATTERNS.md for existing patterns
2. If bug matches a pattern, reference it in your fix
3. If new pattern discovered, add it here
4. Update BUG_TRACKER.md to link to the pattern

---

*This file is part of the Living Documentation system. Update whenever new patterns are discovered.*
