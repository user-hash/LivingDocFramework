---
description: Initialize session with latest context and sync state
---

# Session Start Protocol

Initialize a new development session with full context loading.

## Steps

### 1. Git Sync
```bash
git fetch origin
git status
```

Check current branch and any pending changes.

### 2. Load Version Context
Read CHANGELOG.md to get current version:
```bash
head -20 CHANGELOG.md
```

### 3. Calculate Confidence Score
Run the confidence engine to get project health:
```bash
python tools/confidence_engine.py
```

### 4. Load Previous Session (if available)
Check for previous session context:
```bash
python tools/devmemory/wiring.py session-start
```

### 5. Show Recent Activity
Display recent commits and changes:
```bash
git log --oneline -10
```

### 6. Report Session Status

Output format:
```
SESSION STARTED
===============
Version: [from CHANGELOG.md]
Branch: [current branch]
Confidence: [score]%
Previous Session: [session ID or "none"]
Open Bugs: [count]

Ready to continue development.
```

## What This Does

- Ensures you're on the latest code
- Loads project version from CHANGELOG.md
- Calculates confidence score based on bug count
- Restores context from previous session
- Shows what was recently changed

## Integration

This command can be triggered automatically via Claude Code hooks.
Add to your `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python tools/confidence_engine.py session-start"
          }
        ]
      }
    ]
  }
}
```

## Status

- Git sync: VERIFIED
- Version loading: VERIFIED
- Confidence calculation: VERIFIED
- Session memory: VERIFIED
- Previous session restore: VERIFIED
