# Hook Lifecycle

**Version:** 1.0.0

> Understanding when hooks fire during a Claude Code session.

---

## Overview

Hooks provide integration points throughout the Claude Code session lifecycle. Understanding when each hook fires is critical for designing effective cognitive infrastructure.

---

## Session Lifecycle Diagram

```
SESSION START
    │
    ▼
┌───────────────────────────────────────────────────┐
│  SessionStart Hook                                 │
│  • Load previous session context                   │
│  • Initialize DevMemory session                    │
│  • Sync version from CHANGELOG                     │
│  • Load cognitive context (invariants, patterns)   │
└───────────────────────────────────────────────────┘
    │
    ▼
┌───────────────────────────────────────────────────┐
│  CONVERSATION LOOP                                 │
│                                                    │
│  User Message                                      │
│       │                                            │
│       ▼                                            │
│  ┌─────────────────────────────────┐               │
│  │  Claude processes request       │               │
│  │  May invoke skill (/command)    │               │
│  └─────────────────────────────────┘               │
│       │                                            │
│       ▼                                            │
│  ┌─────────────────────────────────┐               │
│  │  For each tool call:            │               │
│  │                                 │               │
│  │  ┌─────────────────────┐        │               │
│  │  │ PreToolUse Hook     │◄───────│── Validate    │
│  │  │ • Check Tier A      │        │   before      │
│  │  │ • Load invariants   │        │   action      │
│  │  │ • Pre-flight check  │        │               │
│  │  └─────────────────────┘        │               │
│  │           │                     │               │
│  │           ▼                     │               │
│  │  ┌─────────────────────┐        │               │
│  │  │ Tool Executes       │        │               │
│  │  │ (Edit, Bash, etc.)  │        │               │
│  │  └─────────────────────┘        │               │
│  │           │                     │               │
│  │           ▼                     │               │
│  │  ┌─────────────────────┐        │               │
│  │  │ PostToolUse Hook    │◄───────│── Log &       │
│  │  │ • Emit event        │        │   update      │
│  │  │ • Update confidence │        │   after       │
│  │  │ • Refresh dashboard │        │               │
│  │  └─────────────────────┘        │               │
│  │                                 │               │
│  └─────────────────────────────────┘               │
│       │                                            │
│       ▼                                            │
│  Claude Response                                   │
│                                                    │
└───────────────────────────────────────────────────┘
    │
    ▼ (When skill/session ends)
┌───────────────────────────────────────────────────┐
│  Stop Hook                                         │
│  • Emit completion event                           │
│  • Generate session summary                        │
│  • Archive artifacts                               │
│  • Persist session memory                          │
└───────────────────────────────────────────────────┘
    │
    ▼
SESSION END
```

---

## Hook Timing Details

### SessionStart

**When:** Once at conversation start, before any user interaction is processed.

**Typical Actions:**
- Initialize session tracking (create session ID)
- Load previous session context (if resuming)
- Sync to latest version from CHANGELOG
- Load cognitive context (invariants, patterns, golden paths)
- Check document staleness

**Configuration:**
```json
// .claude/settings.json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "python .claude/tools/cognitive_engine.py session-start"
      }]
    }]
  }
}
```

---

### PreToolUse

**When:** Before each tool invocation (Edit, Bash, Write, etc.).

**Typical Actions:**
- Check if file is Tier A (require citation)
- Load relevant invariants for the file
- Validate proposed change against patterns
- Emit `tool.pre` event

**Configuration:**
```yaml
# In skill frontmatter
hooks:
  PreToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: "python .claude/tools/cognitive_engine.py pre-edit"
```

**Matcher Examples:**

| Matcher | Fires Before |
|---------|--------------|
| `"Edit"` | File modifications |
| `"Write"` | File creation |
| `"Bash"` | Shell commands |
| `"Task"` | Agent spawning |
| `""` | All tools |

---

### PostToolUse

**When:** After each tool invocation completes.

**Typical Actions:**
- Log the action as an event
- Update confidence score
- Trigger dashboard refresh (debounced)
- Check for documentation updates needed

**Configuration:**
```yaml
# In skill frontmatter
hooks:
  PostToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: "python .claude/tools/cognitive_engine.py post-edit"
```

---

### Stop

**When:** Skill-scoped hook that fires when the skill completes (conversation ends, user switches topics, or explicit stop).

**Typical Actions:**
- Emit `skill.complete` event
- Generate session summary
- Archive large artifacts
- Persist session memory for next session

**Configuration:**
```yaml
# In skill frontmatter
hooks:
  Stop:
    - hooks:
        - type: command
          command: "python .claude/tools/cognitive_engine.py skill-complete bug-fix"
```

---

## Hook Execution Order

Within a single tool call:

```
1. Global PreToolUse hooks (from settings.json)
2. Skill-scoped PreToolUse hooks (from frontmatter)
3. Tool execution
4. Global PostToolUse hooks
5. Skill-scoped PostToolUse hooks
```

**Note:** If both global and skill-scoped hooks match, both will fire. Design for this.

---

## Event Timeline Example

For a bug fix session editing `GridSyncManager.cs`:

```
13:00:00  SessionStart hook fires
          → session-start handler runs
          → Session S-abc123 created
          → Previous session context loaded

13:00:15  User invokes /bug-fix BUG-MP-042

13:00:20  Claude calls Edit tool
          → PreToolUse(Edit) fires
          → pre-edit handler runs
          → Detects Tier A file
          → Loads INV-MP.3, INV-MP.7

13:00:21  Edit executes (file modified)

13:00:22  PostToolUse(Edit) fires
          → post-edit handler runs
          → code.edit event emitted
          → Confidence recalculated: 94.1%
          → Dashboard refresh queued

13:00:45  User says "done, thank you"

13:00:46  Stop hook fires
          → skill-complete handler runs
          → bug.fixed event emitted
          → Session summary generated
          → Artifacts archived
```

---

## Debugging Hooks

### Check if hooks are firing

Add logging to your handler:

```python
import logging
from datetime import datetime

LOG_FILE = ".claude/logs/hooks.log"
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

def on_pre_edit():
    logging.debug(f"[{datetime.now()}] pre-edit fired")
    # ... rest of handler
```

### Common issues

1. **Hook not firing**
   - Check matcher matches exact tool name
   - Verify YAML frontmatter syntax
   - Ensure handler script is executable

2. **Hook fires but nothing happens**
   - Check handler script path is correct
   - Look for exceptions in handler
   - Add error logging

3. **Hook fires twice**
   - Both global and skill-scoped hooks matched
   - Deduplicate in handler or remove one source

---

## Best Practices

1. **Keep hooks fast** (<100ms ideally)
   - Hooks run synchronously
   - Slow hooks degrade user experience

2. **Use debouncing for expensive operations**
   - Dashboard refresh shouldn't fire on every edit
   - Batch operations where possible

3. **Log hook activity**
   - Essential for debugging
   - Track timing for performance

4. **Fail gracefully**
   - Don't block on non-critical hooks
   - Log errors but continue

5. **Test in isolation**
   - Run handler commands manually first
   - Verify expected output

---

## Related Documentation

- [CC-2.1.0-HOOKS.md](CC-2.1.0-HOOKS.md) - Frontmatter syntax and examples
- [../core/DEVMEMORY.md](../core/DEVMEMORY.md) - Event system that hooks emit to
- [../protocols/MANIFEST.md](../protocols/MANIFEST.md) - Manifest configuration
