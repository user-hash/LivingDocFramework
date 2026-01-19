# Invariants - Multiplayer Subsystem

Safety rules that must never be violated.

## INV-MP-003: Structural State Transition Guard

**System**: Multiplayer
**Severity**: Critical
**Added**: v0.920.55
**Source**: Issue #624

### Rule

> All structural changes (genre, kit, step mode, pattern) MUST use `BeginStructuralTransition()` / `EndStructuralTransition()` to buffer incoming messages.

### Rationale

During structural changes, the grid dimensions change. Incoming network messages may reference indices that are valid for the old structure but invalid for the new one. Without buffering, these messages cause:
- Array index out of bounds exceptions
- State desync between host and clients
- Potential crashes

### Violation Example

```csharp
// VIOLATION - This breaks the invariant:
public void SetGenre(Genre genre) {
    _currentGenre = genre;
    RebuildGrid();  // Messages arriving here reference old grid
}
```

### Correct Example

```csharp
// CORRECT - This respects the invariant:
public void SetGenre(Genre genre) {
    BeginStructuralTransition();  // Start buffering
    _currentGenre = genre;
    RebuildGrid();
    EndStructuralTransition();    // Apply buffered messages safely
}
```

### Affected Files

Files that call structural change methods:
- `GridSyncManager.cs`
- `GenreManager.cs`
- `KitManager.cs`
- `StepModeController.cs`
- `PatternSlotManager.cs`

### Detection

```bash
# Find violations
grep -rn "SetGenre\|SetKit\|SetStepMode" --include="*.cs" | grep -v "BeginStructuralTransition"
```

### Prevents

- PATTERN-MP-024: Unguarded Structural Change
- Array index out of bounds during genre/kit changes
- Client-host state desync

### Citation Required

When editing any file that calls `SetGenre`, `SetKit`, `SetStepMode`, or `SetPattern`, you must cite this invariant:

```
Editing [file]. Relevant: INV-MP-003 - Using transition guard for structural change.
```
