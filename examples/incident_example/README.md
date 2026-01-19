# Incident Example: MP Desync Prevention

This example shows one way the framework is used.
The framework does not automatically prevent bugs — it enforces rules you define.

## What This Demonstrates

- How an invariant (INV-MP-003) codifies a safety rule
- How a bug pattern (PATTERN-MP-024) documents the anti-pattern with detection
- How a pre-commit hook can check for violations
- How before/after code shows the fix

## Files

| File | Contents |
|------|----------|
| `INCIDENT.md` | The real incident from Nebulae Issue #624 |
| `INVARIANTS.md` | The safety rule that prevents this class of bug |
| `BUG_PATTERN.md` | The documented anti-pattern with detection grep |
| `code_snippet.md` | Before/after code showing the guard pattern |

## How It Works

1. **Incident happens** → Document in `INCIDENT.md`
2. **Identify root cause** → Create invariant in `INVARIANTS.md`
3. **Document pattern** → Add to `BUG_PATTERN.md` with detection
4. **Pre-commit hook** → Checks for pattern violations
5. **Future changes** → Automatically checked against rules

## Context

This example is from Nebulae, a multiplayer music production app. The bug caused crashes and desync when the host changed musical genres mid-session while clients were sending pad changes.

The fix demonstrates the "State Transition Guard" pattern — buffering incoming messages during structural changes.
