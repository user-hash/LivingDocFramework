# Bug Pattern: PATTERN-MP-024

## Unguarded Structural Change

**Category**: State Synchronization
**Severity**: Critical
**Frequency**: Occasional

## Summary

Structural state changes without transition guards cause race conditions with incoming messages.

## Root Cause

When structural state changes, dimensions change. If a message arrives during the transition window, it references indices valid for the OLD structure but invalid for the NEW one.

```
State: config = A (16 elements)
Client sends: update(index=14)
State: config = B (12 elements)  <-- transition
Receive: update(index=14)  <-- INDEX OUT OF BOUNDS
```

## Symptoms

- `IndexOutOfRangeException` in state management code
- Clients see different state than host
- Random crashes during configuration changes
- "Ghost data" appearing/disappearing

## Detection

```bash
# Find structural changes without guards
grep -rn "structural_change_call" --include="*.ext" | \
  grep -v "BeginStructuralTransition" | \
  grep -v "// guarded" | \
  grep -v "test"
```

## Bad Code Example

```
// DON'T DO THIS:
public void OnConfigButtonClicked(Config newConfig) {
    _stateSync.SetConfig(newConfig);  // Messages can arrive during this!
    UpdateUI();
}

public void SetConfig(Config config) {
    _currentConfig = config;
    RebuildState();  // State dimensions change here
    NotifyClients();
}
```

## Good Code Example

```
// DO THIS INSTEAD:
public void OnConfigButtonClicked(Config newConfig) {
    _stateSync.SetConfigSafe(newConfig);
    UpdateUI();
}

public void SetConfigSafe(Config config) {
    BeginStructuralTransition();  // Buffer all incoming messages
    try {
        _currentConfig = config;
        RebuildState();
        NotifyClients();
    } finally {
        EndStructuralTransition();  // Process buffered messages with new state
    }
}
```

## Fix Strategy

1. Wrap ALL structural changes with `BeginStructuralTransition()` / `EndStructuralTransition()`
2. Transition methods buffer incoming messages in a queue
3. After transition completes, process buffered messages with new dimensions
4. Messages with invalid indices are logged and discarded (not crashed)

## Prevention

- **Invariant**: INV-MP-003 requires transition guards
- **Pre-commit hook**: Checks for unguarded structural calls
- **Code review**: Flag any structural changes without guards

## Related

- **Invariant**: INV-MP-003 (Structural State Transition Guard)
