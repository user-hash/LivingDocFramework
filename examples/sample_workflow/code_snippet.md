# Code Snippet: State Transition Guard Pattern

Before/after showing the fix for PATTERN-MP-024.

## Before (Vulnerable)

```
// StateManager - BEFORE

public void SetConfiguration(Config config) {
    _currentConfig = config;
    RebuildState();  // Danger: messages arriving NOW reference old dimensions
    BroadcastChange();
}

public void SetMode(Mode mode) {
    _currentMode = mode;
    RebuildState();  // Same problem
    BroadcastChange();
}

private void HandleIncomingUpdate(UpdateMessage msg) {
    // Crash if msg.Index > current state size
    _state[msg.Index] = msg.Value;
}
```

**Problem**: No protection during the window between `RebuildState()` starting and completing.

## After (With Guard)

```
// StateManager - AFTER

private bool _inStructuralTransition = false;
private Queue<Message> _transitionBuffer = new();

public void SetConfiguration(Config config) {
    BeginStructuralTransition();
    try {
        _currentConfig = config;
        RebuildState();
        BroadcastChange();
    } finally {
        EndStructuralTransition();
    }
}

public void SetMode(Mode mode) {
    BeginStructuralTransition();
    try {
        _currentMode = mode;
        RebuildState();
        BroadcastChange();
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

private void HandleIncomingUpdate(UpdateMessage msg) {
    if (_inStructuralTransition) {
        // Buffer for later - state is changing
        _transitionBuffer.Enqueue(msg);
        return;
    }

    // Validate before applying
    if (msg.Index >= _state.Count) {
        Log.Warning($"Discarding stale message: index {msg.Index} > state size {_state.Count}");
        return;
    }

    _state[msg.Index] = msg.Value;
}

private void ProcessBufferedMessages() {
    while (_transitionBuffer.TryDequeue(out var msg)) {
        HandleIncomingMessage(msg);  // Now validated against new state
    }
}
```

## Key Changes

1. **Transition flag**: `_inStructuralTransition` tracks when state is changing
2. **Message buffer**: Queue holds messages during transition
3. **Buffering**: `HandleIncomingUpdate` checks flag before applying
4. **Validation**: Messages with stale indices are logged and discarded
5. **Processing**: Buffered messages applied after transition completes

## Why This Works

```
T0: BeginStructuralTransition() - flag = true, buffer cleared
T1: Client message arrives - buffered (not applied)
T2: State rebuilds with new dimensions
T3: EndStructuralTransition() - flag = false
T4: Buffered messages processed with NEW validation
T5: Stale indices safely discarded, valid ones applied
```

**No crashes. No desync. Safe handling of race conditions.**
