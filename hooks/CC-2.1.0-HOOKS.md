# Claude Code 2.1.0 Skill-Scoped Hooks

**Version:** 1.0.0 | **Requires:** Claude Code 2.1.0+

> Frontmatter-based hooks enable skills to define their own behavioral modifications without global configuration changes.

---

## Overview

Claude Code 2.1.0 introduced skill-scoped hooks via YAML frontmatter. This pattern allows each skill (command file in `.claude/commands/`) to define its own hooks that fire only when that skill is active.

**Benefits:**
- Skills are self-contained and portable
- No global settings.json pollution
- Hook behavior is documented in the skill itself
- Easy to enable/disable by editing skill file

---

## Frontmatter Syntax

Skills are markdown files with YAML frontmatter that defines hooks:

```yaml
---
name: skill-name
description: Brief description of what this skill does
hooks:
  PreToolUse:
    - matcher: "ToolName"
      hooks:
        - type: command
          command: "python .claude/tools/handler.py pre-action"
  PostToolUse:
    - matcher: "ToolName"
      hooks:
        - type: command
          command: "python .claude/tools/handler.py post-action"
  Stop:
    - hooks:
        - type: command
          command: "python .claude/tools/handler.py skill-complete skill-name"
---

# Skill Title

Skill content and instructions here...
```

---

## Hook Types

### PreToolUse

Fires **before** a tool executes. Use for:
- Validation checks
- Context loading
- Pre-flight verification
- Warning about Tier A files

```yaml
hooks:
  PreToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: "python .claude/tools/cognitive_engine.py pre-edit"
```

**Matcher Options:**
- `"Edit"` - Fires before file edits
- `"Bash"` - Fires before shell commands
- `"Task"` - Fires before agent spawning
- `"Write"` - Fires before file creation
- `""` (empty) - Fires for all tools

### PostToolUse

Fires **after** a tool executes. Use for:
- Logging/auditing
- Dashboard updates
- Event emission
- Validation of changes

```yaml
hooks:
  PostToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: "python .claude/tools/cognitive_engine.py post-edit"
```

### Stop

Fires when the skill completes (conversation ends or user changes topic). Use for:
- Cleanup
- Final reports
- Session summary
- Artifact archival

```yaml
hooks:
  Stop:
    - hooks:
        - type: command
          command: "python .claude/tools/cognitive_engine.py skill-complete bug-fix"
```

---

## Matcher Patterns

The `matcher` field supports exact tool name matching:

| Matcher | Fires For |
|---------|-----------|
| `"Edit"` | Edit tool calls |
| `"Bash"` | Bash tool calls |
| `"Task"` | Task/agent spawning |
| `"Write"` | Write tool calls |
| `"Read"` | Read tool calls |
| `"Glob"` | File pattern matching |
| `"Grep"` | Content searching |
| `""` | All tool calls (catch-all) |

**Note:** Matchers are case-sensitive and match exact tool names.

---

## Complete Example: Bug Fix Skill

```yaml
---
name: bug-fix
description: Cognitive Bug Fixing - Architecture-aware bug resolution
hooks:
  PreToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: "python .claude/tools/cognitive_engine.py pre-edit"
    - matcher: "Task"
      hooks:
        - type: command
          command: "python .claude/tools/cognitive_engine.py pre-task"
  PostToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: "python .claude/tools/cognitive_engine.py post-edit"
    - matcher: "Task"
      hooks:
        - type: command
          command: "python .claude/tools/cognitive_engine.py post-task"
  Stop:
    - hooks:
        - type: command
          command: "python .claude/tools/cognitive_engine.py skill-complete bug-fix"
---

# Bug Fix - Cognitive Bug Resolution

## Usage
```bash
/bug-fix BUG-XXX-001   # Fix specific bug by ID
/bug-fix "description" # Fix bug by description
```

## Protocol
1. **Locate** - Find bug in tracker or search codebase
2. **Analyze** - Understand root cause (don't assume)
3. **Plan** - Identify all affected files
4. **Fix** - Make minimal, focused changes
5. **Verify** - Check for regressions
6. **Document** - Update tracker and patterns
```

---

## Global vs Skill-Scoped Hooks

### Global Hooks (`.claude/settings.json`)

Apply to all conversations regardless of active skill:

```json
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

### Skill-Scoped Hooks (Frontmatter)

Apply only when that specific skill is invoked:

```yaml
---
hooks:
  PreToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: "python handler.py pre-edit"
---
```

### When to Use Which

| Use Case | Recommendation |
|----------|----------------|
| Session initialization | Global (SessionStart) |
| Always-on logging | Global |
| Skill-specific validation | Skill-scoped |
| Skill completion cleanup | Skill-scoped (Stop) |
| Context-specific pre-checks | Skill-scoped |

---

## Handler Script Pattern

Create a central handler that routes commands:

```python
# .claude/tools/cognitive_engine.py

import sys

def main():
    if len(sys.argv) < 2:
        return

    command = sys.argv[1]

    handlers = {
        "session-start": on_session_start,
        "pre-edit": on_pre_edit,
        "post-edit": on_post_edit,
        "pre-task": on_pre_task,
        "post-task": on_post_task,
        "skill-complete": on_skill_complete,
    }

    handler = handlers.get(command)
    if handler:
        handler(*sys.argv[2:])

def on_pre_edit():
    # Check if editing Tier A file
    # Load relevant invariants
    # Warn if needed
    pass

def on_post_edit():
    # Log the edit event
    # Update confidence score
    # Refresh dashboard
    pass

def on_skill_complete(skill_name):
    # Emit completion event
    # Generate summary
    # Archive session artifacts
    pass

if __name__ == "__main__":
    main()
```

---

## Best Practices

1. **Keep hooks fast** - They run synchronously; slow hooks degrade UX
2. **Handle failures gracefully** - Don't block on non-critical hooks
3. **Log hook activity** - Helps debug when things don't fire
4. **Use meaningful names** - `skill-complete bug-fix` not `done`
5. **Test hooks locally** - Run command manually first
6. **Document hook behavior** - In the skill file itself

---

## Troubleshooting

### Hooks not firing

1. Check skill file is in `.claude/commands/`
2. Verify YAML frontmatter syntax is valid
3. Ensure matcher matches exact tool name
4. Check handler script exists and is executable

### Hooks firing twice

Global and skill-scoped hooks can both match. If you have:
- Global: `PostToolUse` for `Edit`
- Skill: `PostToolUse` for `Edit`

Both will fire. Design accordingly or use one layer.

### Handler errors

Hook output is typically hidden. Add logging:

```python
import logging
logging.basicConfig(filename='.claude/logs/hooks.log', level=logging.DEBUG)
```

---

## Migration from Pre-2.1.0

If you have hooks in `settings.json`:

1. **Identify skill-specific hooks** - Which hooks only apply to certain workflows?
2. **Move to frontmatter** - Add `hooks:` section to relevant skill files
3. **Keep global hooks** - SessionStart and always-on hooks stay in settings.json
4. **Test each skill** - Verify hooks fire correctly

---

## Related Documentation

- [LIFECYCLE.md](LIFECYCLE.md) - Complete hook lifecycle diagram
- [../core/DEVMEMORY.md](../core/DEVMEMORY.md) - Event system architecture
- [../protocols/MANIFEST.md](../protocols/MANIFEST.md) - Manifest-driven configuration
