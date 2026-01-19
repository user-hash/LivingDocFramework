# Agent Protocol - Mandatory Compliance

> **Purpose**: Ensures AI agents maintain living documentation when making code changes
> **Status**: MANDATORY - ALL AGENTS MUST FOLLOW
> **Version**: 2.0 (Language-Agnostic)

---

## 🛑 PRE-FLIGHT CHECKLIST

**STOP. Before launching ANY agent via Task tool, verify:**

```
□ 1. Have I read the living documentation this session?
□ 2. Am I including this AGENT PROTOCOL in the agent prompt?
□ 3. Is this a code-modifying agent? → Require doc updates in report
□ 4. Are target files Tier A? → Require invariant citations
□ 5. Have I specified the MANDATORY report format?
```

**If ANY checkbox is unchecked → DO NOT LAUNCH AGENT**

---

## Why This Protocol Exists

**Problem**: Sub-agents spawned via Task tool don't automatically inherit the Living Docs system rules. This leads to:
- Agents making changes without updating documentation
- Drift between code and docs
- Future sessions finding stale/incorrect documentation
- Compounding errors across sessions

**Solution**: This protocol is MANDATORY context for EVERY agent prompt.

---

## MANDATORY: Include In Every Agent Prompt

When spawning ANY agent via the Task tool, you MUST include this block:

```markdown
## Agent Protocol (MANDATORY COMPLIANCE)

### Documentation Requirements
Before making ANY code change:
1. READ the relevant section of CODE_DOC_MAP.md
2. READ docs/INVARIANTS.md if touching Tier A files
3. READ the relevant architecture doc (see CODE_DOC_MAP for which doc)
4. READ docs/DECISIONS.md if the file has an ADR (architectural decisions)

After making ANY code change:
1. UPDATE docs/INVARIANTS.md if any invariant values changed
2. UPDATE CODE_DOC_MAP.md if new files created
3. UPDATE the relevant architecture doc if behavior changed
4. UPDATE BUG_PATTERNS.md if new pattern discovered
5. UPDATE docs/DECISIONS.md if making a major architectural choice (add new ADR)

### Tier A Files (EXTRA SCRUTINY)
Files in CODE_DOC_MAP.md marked as "TIER A" require INVARIANT CITATION before editing.

**Before editing ANY Tier A file, cite the relevant invariant:**
```
I'm editing [FILE.ext].
Relevant: INV-X.Y: [Name] - [How I'm respecting it]
```

**Full list**: Check CODE_DOC_MAP.md for Tier A files

### Report Format (MANDATORY)
Your report MUST include:
```
## Documentation Updates
- Files updated: [list or "None required - read-only task"]
- INVARIANTS.md: [Updated section X / No change needed / N/A]
- CODE_DOC_MAP.md: [Updated / No change needed / N/A]
- Architecture docs: [Updated X / No change needed / N/A]

## Proof of Compliance
- [ ] Read CODE_DOC_MAP.md before changes
- [ ] Read INVARIANTS.md for Tier A files
- [ ] Updated all affected docs
- [ ] No drift introduced
```
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

- v2.0 (2026-01-04): Generalized for Living Documentation Framework
  - Removed Nebulae-specific file lists
  - Made language-agnostic
  - References CODE_DOC_MAP.md for Tier A files

- v1.1 (2026-01-02): CODE_DOC_MAP Hygiene
  - Added new/deleted/renamed file requirements
  - Pre-commit hook enforcement (Check 13)

- v1.0 (2026-01-01): Initial creation
  - Mandatory agent protocol block
  - Enforcement checkpoints
  - Standard templates

---

*This protocol is part of the Living Documentation Framework.*
*For project-specific customization, see your living-doc-config.yaml*
