# Scenario: Structural Changes Cause State Desync

**Category**: Multiplayer / State Synchronization
**Priority**: P1 - High
**Resolution**: State Transition Guard pattern

## What Happened

During structural changes (configuration, mode switches, slot changes), incoming messages reference old state dimensions or invalid indices.

## Impact

- Array index out of bounds
- State desync between clients
- Potential crashes

## Reproduction Steps

1. Connect 2+ clients
2. Host changes configuration mid-session while client is sending updates
3. Client messages arrive referencing old state dimensions
4. Crash or desync

## Root Cause

No buffering/guard during structural state transitions. Messages sent during the transition window reference stale dimensions.

**Timeline:**
```
T0: Host initiates structural change
T1: Host state starts rebuilding (dimensions changing)
T2: Client message arrives with old indices
T3: Host tries to apply message to new state
T4: Index out of bounds / desync
```

## How Living Docs Help

### 1. Invariant (INVARIANTS.md)

**INV-MP-003: Structural State Transition Guard**
> "All structural changes MUST use `BeginStructuralTransition()` / `EndStructuralTransition()` to buffer messages."

This rule is documented. Any code touching these methods must cite this invariant.

### 2. Bug Pattern (BUG_PATTERN.md)

**PATTERN-MP-024: Unguarded Structural Change**

Detection command finds structural changes without the guard pattern.

### 3. Pre-commit Hook

Hook checks: If a file contains a structural change call, verify that the transition guard is also present.

## Resolution

See `code_snippet.md` for the before/after fix.

## Lessons Learned

1. Structural state changes need explicit boundaries
2. Incoming messages during transitions must be buffered
3. Document invariants immediately after discovering them
4. Add detection commands to catch future violations
