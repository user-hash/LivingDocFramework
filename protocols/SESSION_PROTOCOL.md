# Session Protocol

> Read this at the start of every work session.

## 1. Version Sync (When Loading Specific Version)

**Trigger words:** "load", "sync", "version", "checkout", "tag"

**Mandatory first actions (exact order):**

```bash
# 1. Fetch all tags
git fetch origin --tags --prune

# 2. Find the version
git tag -l | grep "<version>"

# 3. Verify
git log --oneline -1 <tag>

# 4. Checkout and branch
git checkout <tag>
git checkout -b work/<task>-<date>
```

**BLOCKED until version synced:**
- File searches
- Reading code files (except protocol files)
- Making any changes
- Launching sub-agents

## 2. Cognitive Context Loading

Before ANY work, read these files in order:

| Priority | File | When Required |
|----------|------|---------------|
| 1 | PROJECT_CONTEXT.md | Always (project memory) |
| 2 | CHANGELOG.md | Always (current version) |
| 3 | CODE_DOC_MAP.md | If editing files |
| 4 | INVARIANTS.md | If touching Tier A files |
| 5 | BUG_PATTERNS.md | If fixing bugs |

## 3. Pre-Work Checklist

Before first action, verify:

- [ ] Synced to correct version?
- [ ] Read PROJECT_CONTEXT.md this session?
- [ ] Know current project version?
- [ ] If editing Tier A files, read INVARIANTS.md?

## 4. Context Lookup Command

To find relevant docs for any file:

```bash
./LivingDocFramework/core/print-context.sh path/to/file.py
```

Output shows: tier, doc-set, required docs to read.

**Example output:**

```
File: src/api/auth.py
Tier: A (Critical)
Doc-Set: docs/api/
Map: docs/api/CODE_DOC_MAP.md

Required Reading:
  1. docs/api/INVARIANTS.md
  2. docs/api/CODE_DOC_MAP.md

Invariants:
  - INV-AUTH-001: Retry attempts bounded
```

## 5. Session End

Before ending a session:

- [ ] All changes committed?
- [ ] Docs updated for changes made?
- [ ] PROJECT_CONTEXT.md updated if major decisions?
- [ ] Handoff notes for next session?
