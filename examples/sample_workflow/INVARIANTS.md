# Invariants - Sample Subsystem

Safety rules that must never be violated.

## INV-MP-003: Structural State Transition Guard

**System**: State Synchronization
**Severity**: Critical
**Source**: Desync scenario

### Rule

> All structural changes MUST use `BeginStructuralTransition()` / `EndStructuralTransition()` to buffer incoming messages.

### Rationale

During structural changes, state dimensions change. Incoming network messages may reference indices that are valid for the old structure but invalid for the new one. Without buffering, these messages cause:
- Array index out of bounds exceptions
- State desync between clients
- Potential crashes

### Violation Example

```
// VIOLATION - This breaks the invariant:
public void SetConfiguration(Config config) {
    _currentConfig = config;
    RebuildState();  // Messages arriving here reference old state
}
```

### Correct Example

```
// CORRECT - This respects the invariant:
public void SetConfiguration(Config config) {
    BeginStructuralTransition();  // Start buffering
    _currentConfig = config;
    RebuildState();
    EndStructuralTransition();    // Apply buffered messages safely
}
```

### Affected Files

Files that call structural change methods should be checked for guard usage.

### Detection

```bash
# Find violations - structural changes without guards
grep -rn "structural_change_method" --include="*.ext" | grep -v "BeginStructuralTransition"
```

### Prevents

- PATTERN-MP-024: Unguarded Structural Change
- Array index out of bounds during configuration changes
- Client state desync

### Citation Required

When editing any file that performs structural changes, cite this invariant:

```
Editing [file]. Relevant: INV-MP-003 - Using transition guard for structural change.
```
