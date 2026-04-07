# Protocols

Protocols define how AI agents and humans interact with the living documentation system.

## Available Protocols

### SESSION_PROTOCOL.md

Context loading order for the start of every work session. Covers version sync, required reading, and pre-work checklist.

### AGENT_PROTOCOL.md

Guidelines for AI agents that modify code. Covers context loading before edits, invariant citation, documentation updates, and bug verification.

## Using Protocols

Protocols are reference documents. Include them in your AI instruction file (CLAUDE.md) or agent prompts when relevant. They are not mandatory checklists. Use what fits your workflow.

### In CLAUDE.md

Reference the session protocol so your code agent loads context at session start:

```markdown
## Session Start
Follow protocols/SESSION_PROTOCOL.md for context loading order.
```

### In Agent Prompts

When spawning sub-agents that will modify code, include the relevant protocol sections:

```markdown
Before editing any file, load its context:
./LivingDocFramework/core/print-context.sh <file>

If Tier A: read INVARIANTS.md and cite invariants in comments.
```

## Philosophy

Protocols are guidance, not bureaucracy. They exist to reduce mistakes and preserve context, not to slow down work. Adapt them to your needs.
