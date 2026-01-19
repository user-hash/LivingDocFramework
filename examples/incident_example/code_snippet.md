# Code Snippet: State Transition Guard Pattern

Before/after showing the fix for PATTERN-MP-024.

## Before (Vulnerable)

```csharp
// GridSyncManager.cs - BEFORE

public void SetGenre(Genre genre) {
    _currentGenre = genre;
    RebuildGrid();  // Danger: messages arriving NOW reference old dimensions
    BroadcastStructuralChange();
}

public void SetKit(Kit kit) {
    _currentKit = kit;
    RebuildGrid();  // Same problem
    BroadcastStructuralChange();
}

private void HandleIncomingPadChange(PadChangeMessage msg) {
    // Crash if msg.StepIndex > current grid size
    _grid[msg.PadIndex, msg.StepIndex] = msg.Value;
}
```

**Problem**: No protection during the window between `RebuildGrid()` starting and completing.

## After (With Guard)

```csharp
// GridSyncManager.cs - AFTER

private bool _inStructuralTransition = false;
private Queue<NetworkMessage> _transitionBuffer = new();

public void SetGenre(Genre genre) {
    BeginStructuralTransition();
    try {
        _currentGenre = genre;
        RebuildGrid();
        BroadcastStructuralChange();
    } finally {
        EndStructuralTransition();
    }
}

public void SetKit(Kit kit) {
    BeginStructuralTransition();
    try {
        _currentKit = kit;
        RebuildGrid();
        BroadcastStructuralChange();
    } finally {
        EndStructuralTransition();
    }
}

private void BeginStructuralTransition() {
    _inStructuralTransition = true;
    _transitionBuffer.Clear();
}

private void EndStructuralTransition() {
    _inStructuralTransition = false;
    ProcessBufferedMessages();
}

private void HandleIncomingPadChange(PadChangeMessage msg) {
    if (_inStructuralTransition) {
        // Buffer for later - grid is changing
        _transitionBuffer.Enqueue(msg);
        return;
    }

    // Validate before applying
    if (msg.StepIndex >= _grid.StepCount) {
        Debug.LogWarning($"Discarding stale message: step {msg.StepIndex} > grid size {_grid.StepCount}");
        return;
    }

    _grid[msg.PadIndex, msg.StepIndex] = msg.Value;
}

private void ProcessBufferedMessages() {
    while (_transitionBuffer.TryDequeue(out var msg)) {
        HandleIncomingMessage(msg);  // Now validated against new grid
    }
}
```

## Key Changes

1. **Transition flag**: `_inStructuralTransition` tracks when grid is changing
2. **Message buffer**: Queue holds messages during transition
3. **Buffering**: `HandleIncomingPadChange` checks flag before applying
4. **Validation**: Messages with stale indices are logged and discarded
5. **Processing**: Buffered messages applied after transition completes

## Why This Works

```
T0: BeginStructuralTransition() - flag = true, buffer cleared
T1: Client message arrives - buffered (not applied)
T2: Grid rebuilds with new dimensions
T3: EndStructuralTransition() - flag = false
T4: Buffered messages processed with NEW validation
T5: Stale indices safely discarded, valid ones applied
```

**No crashes. No desync. Safe handling of race conditions.**
