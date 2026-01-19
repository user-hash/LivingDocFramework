# Bug Pattern: PATTERN-MP-024

## Unguarded Structural Change

**Category**: Multiplayer / State Sync
**Severity**: Critical
**Frequency**: Occasional
**First Seen**: v0.920.50
**Fixed In**: v0.920.55
**Source**: Issue #624

## Summary

Structural state changes (genre, kit, step mode, pattern) without transition guards cause race conditions with incoming network messages.

## Root Cause

When the host changes structural state, the grid dimensions change. If a client message arrives during the transition window, it references indices valid for the OLD structure but invalid for the NEW one.

```
Host: genre = Rock (16 steps)
Client sends: pad_change(step=14)
Host: genre = Jazz (12 steps)  <-- transition
Host receives: pad_change(step=14)  <-- INDEX OUT OF BOUNDS
```

## Symptoms

- `IndexOutOfRangeException` in grid code
- Clients see different state than host
- Random crashes during genre/kit changes
- "Ghost notes" appearing/disappearing

## Detection

```bash
# Find structural changes without guards
grep -rn "SetGenre\|SetKit\|SetStepMode\|SetPattern" --include="*.cs" | \
  grep -v "BeginStructuralTransition" | \
  grep -v "// guarded" | \
  grep -v "test"
```

## Bad Code Example

```csharp
// DON'T DO THIS:
public void OnGenreButtonClicked(Genre newGenre) {
    _gridSync.SetGenre(newGenre);  // Messages can arrive during this!
    UpdateUI();
}

public void SetGenre(Genre genre) {
    _currentGenre = genre;
    RebuildGrid();  // Grid dimensions change here
    NotifyClients();
}
```

## Good Code Example

```csharp
// DO THIS INSTEAD:
public void OnGenreButtonClicked(Genre newGenre) {
    _gridSync.SetGenreSafe(newGenre);
    UpdateUI();
}

public void SetGenreSafe(Genre genre) {
    BeginStructuralTransition();  // Buffer all incoming messages
    try {
        _currentGenre = genre;
        RebuildGrid();
        NotifyClients();
    } finally {
        EndStructuralTransition();  // Process buffered messages with new grid
    }
}
```

## Fix Strategy

1. Wrap ALL structural changes with `BeginStructuralTransition()` / `EndStructuralTransition()`
2. Transition methods buffer incoming messages in a queue
3. After transition completes, process buffered messages with new grid dimensions
4. Messages with invalid indices are logged and discarded (not crashed)

## Prevention

- **Invariant**: INV-MP-003 requires transition guards
- **Pre-commit hook**: Checks for unguarded structural calls
- **Code review**: Flag any `SetGenre/Kit/StepMode/Pattern` without guards

## Related

- **Invariant**: INV-MP-003 (Structural State Transition Guard)
- **Files**: `GridSyncManager.cs`, `GenreManager.cs`
- **Issue**: #624
