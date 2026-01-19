# Sample Workflow: MP Desync Prevention

This example shows how the Living Documentation Framework enables fast, accurate fixes by providing architectural context upfront.

## Why This Matters

By mapping code to explicit bug patterns, invariants, and decisions, AI agents receive the correct architectural context upfront. This enables accurate analysis and fixes on first contact with large codebases, cutting debugging and review time from days to hours without repeated prompting.

## What This Demonstrates

- How an invariant (INV-MP-003) codifies a safety rule
- How a bug pattern (PATTERN-MP-024) documents the anti-pattern with detection
- How a pre-commit hook can check for violations
- How before/after code shows the fix
- **NEW:** How external review uses these docs to fix bugs quickly

## Files

| File | Contents |
|------|----------|
| `SCENARIO.md` | The scenario that led to this pattern |
| `INVARIANTS.md` | The safety rule that prevents this class of bug |
| `BUG_PATTERN.md` | The documented anti-pattern with detection grep |
| `code_snippet.md` | Before/after code showing the guard pattern |
| `EXTERNAL_REVIEW_WORKFLOW.md` | How reviewers use these docs for fast fixes |

## The Knowledge Transfer Flow

```
1. Scenario happens     → Document what broke and why
2. Identify root cause  → Create invariant (the rule)
3. Document pattern     → Add to patterns with detection
4. Pre-commit hook      → Checks for violations automatically
5. External review      → Reviewer reads docs, fixes in minutes not hours
```

## Context

This example shows a state synchronization bug in a multiplayer application. The bug caused crashes and desync when structural changes occurred while messages were in flight.

The fix demonstrates the "State Transition Guard" pattern — buffering incoming messages during structural changes.

## Key Insight

The Living Documentation system doesn't just document bugs — it **transfers the knowledge** needed to:
1. Quickly understand the problem space
2. Avoid repeating mistakes
3. Apply proven fix patterns

A reviewer with no prior context can read these docs and apply the correct fix pattern on first attempt.
