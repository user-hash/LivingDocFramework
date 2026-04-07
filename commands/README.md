# Commands

Reusable workflows for common documentation tasks. These can be invoked via Claude Code's slash command system or adapted for other AI tools.

## Available Commands

### /living-docs

Check documentation health and suggest updates.

**What it does:**
- Scans for unmapped files
- Checks for stale docs
- Suggests invariants to add
- Recommends patterns to document

**Usage:** `/living-docs`

See [living-docs.md](living-docs.md) for the full prompt.

## Creating Custom Commands

Create a markdown file in `.claude/commands/` (or your tool's equivalent):

```markdown
---
description: Brief description
---

# Task: Command Name

## Steps
1. Load context for the target file
2. Perform the action
3. Update docs if behavior changed
4. Report results
```

Commands are just structured prompts. They work with any AI tool that supports custom command definitions.

## Integration

Commands can also be called from hooks or CI:

```bash
# In a pre-commit hook or CI step
claude "/living-docs --quiet"
```
