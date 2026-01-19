# Incident: Genre/Kit Changes Cause Desync and Crashes

**Source**: Nebulae Issue #624
**Priority**: P1 - High
**Version**: Fixed in v0.920.55

## What Broke

During structural changes (genre, kit, step mode, pattern slot), incoming messages reference old grid dimensions or invalid indices.

## Impact

- Array index out of bounds
- State desync between clients
- Potential crashes

## Repro Steps

1. Connect 2+ players
2. Host changes genre mid-session while client is sending pad changes
3. Client messages arrive referencing old grid dimensions
4. Crash or desync

## Root Cause

No buffering/guard during structural state transitions. Messages sent during the transition window reference stale grid dimensions.

**Timeline:**
```
T0: Host initiates genre change
T1: Host grid starts rebuilding (dimensions changing)
T2: Client message arrives with old grid indices
T3: Host tries to apply message to new grid
T4: Index out of bounds / desync
```

## How This System Prevents It

### 1. Invariant (docs/INVARIANTS.md)

**INV-MP-003: Structural State Transition Guard**
> "All structural changes (genre, kit, step mode, pattern) MUST use `BeginStructuralTransition()` / `EndStructuralTransition()` to buffer messages."

This rule is now documented. Any code touching these methods must cite this invariant.

### 2. Bug Pattern (BUG_PATTERNS.md)

**PATTERN-MP-024: Unguarded Structural Change**

Detection grep:
```bash
grep -rn "SetGenre\|SetKit\|SetStepMode\|SetPattern" --include="*.cs" | grep -v "BeginStructuralTransition"
```

This grep finds structural changes that don't use the guard pattern.

### 3. Pre-commit Hook

Hook checks: If a file contains a structural change call (`SetGenre`, `SetKit`, etc.), verify that `BeginStructuralTransition` is also present in the same file or a clear delegation exists.

## Resolution

See `code_snippet.md` for the before/after fix.

## Files Changed

- `GridSyncManager.cs` - Add transition state and buffer
- `GridSyncManager.IncomingMessages.cs` - Check transition state before processing

## Lessons Learned

1. Structural state changes need explicit boundaries
2. Incoming messages during transitions must be buffered
3. Document invariants immediately after discovering them
4. Add detection greps to catch future violations
