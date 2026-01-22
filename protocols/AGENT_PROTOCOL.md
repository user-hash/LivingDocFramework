# Agent Protocol - Mandatory Compliance

> **Purpose**: Ensures AI agents maintain living documentation when making code changes
> **Status**: MANDATORY - ALL AGENTS MUST FOLLOW
> **Version**: 0.2 (Tool-Agnostic)

---

## Quick Start: Context Lookup

Before editing any file, run:

```bash
./LivingDocFramework/core/print-context.sh <file>
```

This tells you the tier, doc-set, and required reading.

---

## 1. Bug Verification Rule

**No bug report without code verification.**

Before ANY bug report:
1. Read the ACTUAL file (not from memory/cache)
2. Find the specific line with the issue
3. Verify the bug EXISTS in current code
4. If NOT FOUND -> DO NOT REPORT

**Why:** Pattern-matching on theoretical concerns creates false positives.

---

## 2. Pre-Work Requirements

**Before ANY code change:**
1. Run: `./LivingDocFramework/core/print-context.sh <file>`
2. READ the docs listed in output
3. If Tier A: READ INVARIANTS.md and CITE invariants in comments

**After ANY code change:**
1. UPDATE docs if behavior changed
2. UPDATE INVARIANTS.md if constraints changed
3. REPORT compliance proof (see format below)

---

## 3. Mandatory Report Format

Every agent report MUST end with:

```markdown
## Files Changed
- [list of files modified]

## Docs Updated
- [list of docs updated, or "None needed"]

## Compliance Proof
- [ ] Read docs before changes
- [ ] Cited invariants if Tier A
- [ ] Updated affected docs
- [ ] Verified changes in current code
```

---

## 4. Agent Prompt Template

When launching sub-agents, include this block:

```markdown
---Agent Protocol (MANDATORY)

Before ANY code change:
1. Run: ./LivingDocFramework/core/print-context.sh <file>
2. READ the docs listed in output
3. CITE invariants in code comments if Tier A

After ANY code change:
1. UPDATE docs if behavior changed
2. REPORT compliance proof

Your report MUST include:
## Files Changed | ## Docs Updated | ## Compliance Proof
---
```

---

## 5. Tier A Rules

Tier A files are critical. Extra requirements:

- **Must read INVARIANTS.md** before editing
- **Must cite invariant IDs** in commit message or code comments
- **Commit will be blocked** if INVARIANTS.md not updated

Example citation in code:
```python
# INV-AUTH-001: Retry attempts bounded to MAX_RETRIES
for attempt in range(MAX_RETRIES):
    ...
```

Example citation in commit:
```
fix: Add retry limit to auth flow

Respects INV-AUTH-001 (retry attempts bounded).
```

---

## Agent Categories and Requirements

### Read-Only Agents (Research/Audit)
- MUST: Read docs before analyzing code
- MUST: Report any doc staleness found
- NOT REQUIRED: Update docs (read-only)

### Code-Modifying Agents (Bug Fix/Feature)
- MUST: Read docs before making changes
- MUST: Update ALL affected docs after changes
- MUST: Include proof of compliance in report
- MUST: List doc updates in report

### Cognitive Pass Agents (Multi-Agent Analysis)
- MUST: Read living docs first
- MUST: Flag any doc staleness in report
- SHOULD: Recommend doc updates
- NOT REQUIRED: Make code changes

---

## 🔴 CRITICAL: Search Agent Verification Rule

**LESSON LEARNED**: Search agents that report bugs MUST verify bugs exist in CURRENT code, not cached/stale versions.

### The Rule

**ALL Search/Audit agents that report bugs MUST:**

1. **CHECK CURRENT CODE** before creating patterns
   ```
   ## Before Creating PATTERN-XXX
   - [ ] Read the CURRENT file content (not cached/stale)
   - [ ] Verify the bug ACTUALLY EXISTS in HEAD
   - [ ] If already fixed, note when (git blame/log)
   ```

2. **Include Verification in Report**
   ```markdown
   ## Bug Verification
   | Bug | File:Line | Current State | Evidence |
   |-----|-----------|---------------|----------|
   | Lock on array | Audio.py:45 | ✅ BUG EXISTS | `lock(arr)` found |
   | Missing null check | Config.go:12 | ❌ ALREADY FIXED | Now has `if x != nil` |
   ```

3. **For Bulk Scans (10+ bugs found)**
   - Verify at least 30% of bugs before reporting
   - Run verification pass before creating patterns

---

## 🧹 CODE_DOC_MAP Hygiene

### Why This Matters

The CODE_DOC_MAP is the **master file-to-doc registry**. When it drifts:
- New files don't get documented
- Deleted files clutter the map
- Agents lose trust in the system

**Doc-Set Note**: With per-subsystem doc-sets, each `docs/{subsystem}/CODE_DOC_MAP.md` owns its files. Update the relevant doc-set, not a global map.

### Hygiene Rules

**For EVERY agent that creates/deletes/renames files:**

1. **New Files** → Add to CODE_DOC_MAP.md
   ```
   | `NewFile.py` | `services/` | NORMAL | API_ARCH.md | - | - | - |
   ```
   - Set tier: TIER A for safety-critical, HIGH for important, NORMAL otherwise
   - Link to relevant architecture doc

2. **Deleted Files** → Remove from CODE_DOC_MAP.md
   - Search for filename and remove the row
   - Update Quick Stats count if Tier A

3. **Renamed Files** → Update entry in CODE_DOC_MAP.md
   - Find old name, replace with new name
   - Update path if directory changed

### In Agent Reports

If your agent creates/deletes/renames files, include:

```markdown
## CODE_DOC_MAP Hygiene
- New files added to map: [list or "None"]
- Files removed from map: [list or "None"]
- Files renamed in map: [list or "None"]
```

---

## Enforcement Checkpoints

### Pre-Launch Verification
Before launching ANY agent, verify:
- [ ] Agent prompt includes AGENT_PROTOCOL block
- [ ] Agent has doc update requirements if code-modifying
- [ ] Agent has mandatory report format

### Post-Completion Verification
After agent completes, verify:
- [ ] Report includes Documentation Updates section
- [ ] Report includes Proof of Compliance checklist
- [ ] If code-modifying: docs were actually updated
- [ ] No new drift introduced

### Escalation
If an agent returns without proper documentation:
1. DO NOT commit the changes
2. Manually update the affected docs
3. Note in CURRENT_WORK.md that agent skipped docs
4. Consider re-running with stricter prompt

---

## Template: Standard Agent Prompt

```markdown
## Task: [DESCRIPTION]

### Files to Work With
[FILE LIST]

### Instructions
[SPECIFIC TASK INSTRUCTIONS]

### Agent Protocol (MANDATORY COMPLIANCE)
[PASTE THE FULL AGENT PROTOCOL BLOCK FROM ABOVE]

### Expected Output
[WHAT TO RETURN]

Your report MUST end with:
## Documentation Updates
- Files updated: [list]
- INVARIANTS.md: [status]
- CODE_DOC_MAP.md: [status]

## Proof of Compliance
- [ ] Read docs before changes
- [ ] Updated affected docs
- [ ] No drift introduced
```

---

## Quick Reference: What Each Agent Must Do

| Agent Type | Read Docs | Update Docs | Proof Required |
|------------|-----------|-------------|----------------|
| Research/Audit | Yes | No | Read confirmation |
| Bug Fix | Yes | Yes | Full compliance |
| Feature | Yes | Yes | Full compliance |
| Cognitive Pass | Yes | Recommend | Staleness report |
| Verification | Yes | No | Verification result |

---

## Version History

- v0.2 (2025-01-22): print-context.sh Integration
  - Added Quick Start with print-context.sh command
  - Streamlined pre-work requirements
  - Tool-agnostic: Git + Bash only
  - Bug verification rule prominent

- v2.1 (2025-01-19): Doc-Set Discovery Support
  - Updated for per-subsystem doc-sets (`docs/*/CODE_DOC_MAP.md`)
  - Sibling INVARIANTS.md requirement for Tier A files
  - Doc-set hygiene notes added

- v2.0 (2025-01-04): Generalized for Living Documentation Framework
  - Removed Nebulae-specific file lists
  - Made language-agnostic
  - References CODE_DOC_MAP.md for Tier A files

- v1.1 (2025-01-02): CODE_DOC_MAP Hygiene
  - Added new/deleted/renamed file requirements
  - Pre-commit hook enforcement (Check 13)

- v1.0 (2025-01-01): Initial creation
  - Mandatory agent protocol block
  - Enforcement checkpoints
  - Standard templates

---

*This protocol is part of the Living Documentation Framework.*
*For project-specific customization, see your living-doc-config.yaml*
