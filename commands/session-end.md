---
description: Save session state and prepare for handoff
---

# Session End Protocol

Properly close a development session with state preservation.

## Steps

### 1. Save Session State
Persist current session to memory:
```bash
python tools/devmemory/wiring.py session-end
```

### 2. Update Documentation
Ensure all docs are current:
- [ ] CHANGELOG.md updated with version
- [ ] BUG_TRACKER.md reflects current state
- [ ] Architecture docs match code

### 3. Calculate Final Confidence
Get end-of-session confidence score:
```bash
python tools/confidence_engine.py
```

### 4. Git Status Check
Verify all changes are committed:
```bash
git status
git log --oneline -5
```

### 5. Push Changes (if ready)
```bash
git push -u origin [branch-name]
```

### 6. Report Session Summary

Output format:
```
SESSION ENDED
=============
Session ID: [session ID]
Duration: [time]
Version: [start] -> [end]
Confidence: [start]% -> [end]%
Files Modified: [count]
Commits: [count]

Changes saved. Ready for next session.
```

## What This Does

- Saves session state for next session
- Records what files were modified
- Tracks confidence score changes
- Ensures changes are pushed to git
- Creates handoff context for next session

## What Gets Preserved

The session memory stores:
- Session ID and timestamps
- Version at start and end
- Confidence score trajectory
- List of modified files
- Agents spawned during session
- Event count

This allows the next session to:
- Know what was worked on
- See version progression
- Track confidence trends
- Avoid redoing completed work

## Integration

For automatic session end tracking, the confidence engine
tracks session state throughout. Manual invocation ensures
proper cleanup.

## Status

- Session save: VERIFIED
- State persistence: VERIFIED
- Git integration: VERIFIED
- Summary generation: VERIFIED
