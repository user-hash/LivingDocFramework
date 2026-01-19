# How External Review Enables Fast, Accurate Fixes

## The Knowledge Transfer Problem

When a bug is reported:
- Developer may not have full context
- Root cause may be non-obvious
- Multiple systems may be involved

**Traditional approach:** Hours of exploration, trial-and-error fixes, repeated prompting.

**With Living Docs:** Minutes to understand, correct fix on first attempt.

## How Living Docs Solve This

Mapping code to bug patterns, invariants, and decisions gives reviewers the context they need upfront. Less archaeology, correct fix on first attempt.

### 1. Code Maps Provide File Context

The CODE_DOC_MAP tells the reviewer:
- Which files are Tier A (critical)
- What documentation exists for each file
- Related architecture docs

### 2. Existing Patterns Provide Historical Context

BUG_PATTERNS shows:
- Similar bugs that happened before
- Root causes that were found
- Fixes that worked

### 3. Invariants Provide Safety Rules

INVARIANTS tells the reviewer:
- Rules that must not be violated
- Why those rules exist
- What happens if violated

## Sample Workflow: State Sync Fix

**Problem:** "Sometimes works" behavior when state changes occur

**Reviewer's Knowledge Sources:**
1. Read INVARIANTS.md → Found INV-MP-003 (transition guard rule)
2. Read BUG_PATTERNS.md → Found PATTERN-MP-024 (similar issue)
3. Read code-maps → Identified critical files

**Fast Diagnosis:**
- Checked handlers for transition guard
- Found: NO guard, handlers apply to changing state
- Found: Early return would DROP messages (wrong fix)

**Correct Fix (from pattern knowledge):**
- Queue + apply-on-ready (not drop)
- Deep copy data buffers (prevent reuse corruption)
- Deterministic apply order

**Time to fix:** ~30 minutes (vs hours without context)

## The Workflow

```
1. RECEIVE bug report
   ↓
2. READ CODE_DOC_MAP.md
   → Identify affected files and their tier
   → Find related architecture docs
   ↓
3. READ INVARIANTS.md
   → Find safety rules for this area
   → Understand what MUST NOT be violated
   ↓
4. READ BUG_PATTERNS.md
   → Find similar bugs
   → Understand proven fix patterns
   ↓
5. APPLY known pattern
   → Use detection commands to verify fix
   → Cite invariants in commit
   ↓
6. UPDATE docs
   → Add new pattern if novel
   → Update invariant if needed
```

## Key Insight

The Living Documentation system doesn't just document bugs — it **transfers the knowledge** needed to:
1. Quickly understand the problem space
2. Avoid repeating mistakes
3. Apply proven fix patterns

## Metrics

| Metric | Without Living Docs | With Living Docs |
|--------|---------------------|------------------|
| Time to understand codebase | Hours | Minutes |
| Fix attempts before correct | 3-5 | 1 |
| Regression rate | High | Low |
| Knowledge transfer | Lost | Preserved |
