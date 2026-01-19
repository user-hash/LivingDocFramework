# Living Documentation Framework - Slash Commands

Slash commands are reusable workflows for common documentation tasks. They can be invoked via Claude Code's command system.

## What Are Slash Commands?

Slash commands let you create custom workflows that expand into full prompts. Instead of typing the same instructions repeatedly, you define them once and invoke with `/command-name`.

### Example

Instead of typing:
```
Please review the code changes in src/auth.py, check against INVARIANTS.md,
verify tests exist, update CODE_DOC_MAP.md if needed, and create a summary.
```

You type:
```
/code-review src/auth.py
```

## Setting Up Commands

### For Claude Code

1. Create `.claude/commands/` in your project root
2. Add markdown files (one per command)
3. Commands auto-discovered by Claude Code
4. Invoke with `/command-name`

### Command File Format

```markdown
---
description: Brief description for /help menu
---

Full prompt that gets expanded when command is invoked.

Supports placeholders: {{arg1}}, {{arg2}}, etc.
```

## Available Commands

### /living-docs
**Purpose**: Check documentation health and suggest updates

**Usage**: `/living-docs`

**What it does**:
- Scans for unmapped files
- Checks for stale docs
- Suggests invariants to add
- Recommends patterns to document

### /code-review
**Purpose**: Multi-agent code review with doc validation

**Usage**: `/code-review <file-path>`

**What it does**:
- Reviews code quality
- Checks against invariants
- Validates tests exist
- Verifies documentation up-to-date

### /bug-fix
**Purpose**: Structured bug fixing with pattern documentation

**Usage**: `/bug-fix <bug-id>`

**What it does**:
- Loads bug details from BUG_TRACKER.md
- Checks for existing patterns
- Fixes bug with invariant citations
- Updates BUG_PATTERNS.md
- Updates BUG_TRACKER.md

## Creating Custom Commands

### Basic Command Template

Create `.claude/commands/my-command.md`:

```markdown
---
description: Does something useful
---

# Task: My Custom Command

Load configuration and perform task.

## Steps
1. Read relevant docs
2. Perform action
3. Update docs
4. Report results

## Agent Protocol
{Include AGENT_PROTOCOL.md if spawning agents}

## Output Format
Provide structured summary
```

### Advanced Command with Placeholders

Create `.claude/commands/refactor-file.md`:

```markdown
---
description: Refactor file with doc updates
---

# Task: Refactor {{file_path}}

## Pre-Refactor
1. Read CODE_DOC_MAP.md entry for {{file_path}}
2. Read relevant architecture doc
3. Read INVARIANTS.md if Tier A

## Refactor
Apply refactoring while respecting invariants

## Post-Refactor
1. Update architecture doc if behavior changed
2. Update CODE_DOC_MAP.md if structure changed
3. Add entry to CHANGELOG.md

## Report
- What was refactored
- Why the refactoring was needed
- What docs were updated
```

Invoke with: `/refactor-file src/auth/login.py`

## Command Best Practices

### ✅ DO

1. **Include context loading**: Read relevant docs first
2. **Specify output format**: Tell what you expect back
3. **Include protocol**: Reference AGENT_PROTOCOL.md if spawning agents
4. **Make reusable**: Use placeholders for arguments

### ❌ DON'T

1. **Don't hardcode paths**: Use placeholders or config
2. **Don't skip doc updates**: Always update docs in workflow
3. **Don't assume context**: Explicitly load what you need

## Commands Status

### Available Commands
1. ✅ living-docs.md - Doc health check

### To Extract from Nebulae
4. ⏳ bug-fix.md - Structured bug fixing
5. ⏳ code-review.md - Multi-agent review
6. ⏳ bug-hunt.md - Multi-agent bug discovery
7. ⏳ cognitive-fix.md - Pattern-aware fixing
8. ⏳ perf-check.md - Performance analysis
9. ⏳ quick-fix.md - Single bug fixes
10. ⏳ sync-tag.md - Version tagging

## Integration Examples

### With Git Hooks

```bash
# In pre-commit hook
echo "Running /living-docs check..."
claude "/living-docs" --quiet
```

### With CI/CD

```yaml
# In GitHub Actions
- name: Check documentation
  run: claude "/living-docs --json" > docs-report.json
```

### Automated Workflows

```bash
# Morning routine
claude "/session-start"
claude "/living-docs"
# Shows what needs attention
```

## Status

- ✅ Commands directory structure created
- ✅ README with usage guide
- ✅ living-docs.md command available

**Next**: Extract additional commands (bug-fix, code-review) as needed.
