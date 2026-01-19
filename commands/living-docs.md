---
description: Check documentation health and suggest updates
---

# Living Documentation Health Check

Analyze the current state of living documentation and provide actionable recommendations.

## Objective

Scan the project for documentation issues and suggest specific actions to improve documentation health.

## Steps

### 1. Configuration Check
- Verify `living-doc-config.yaml` exists and is valid
- Check all configured paths exist
- Validate language profile loaded correctly

### 2. File Coverage Analysis
- Count total code files in configured code root
- Check how many are mapped in CODE_DOC_MAP.md
- Identify unmapped files
- Suggest mappings for new files

### 3. Documentation Completeness
- Check all required docs exist:
  - CHANGELOG.md
  - BUG_PATTERNS.md
  - docs/INVARIANTS.md
  - docs/GOLDEN_PATHS.md
  - CODE_DOC_MAP.md
- Flag any missing documents
- Suggest creating missing docs from templates

### 4. Tier A Validation
- Extract Tier A files from CODE_DOC_MAP.md
- Verify each has corresponding INVARIANTS.md entry
- Flag Tier A files without invariants
- Suggest invariants to add

### 5. Staleness Detection
- Check git log for files modified recently
- Compare against last doc update dates
- Flag potentially stale documentation
- Suggest docs to review

### 6. Bug Pattern Health
- Check BUG_PATTERNS.md for documented bugs
- Verify each has prevention pattern
- Flag incomplete patterns

## Output Format

```markdown
# Living Documentation Health Report

## Overview
- Project: [name]
- Language: [language]
- Code Files: [mapped]/[total] ([X]% coverage)

## Issues Found

### Critical (Fix First)
1. [Issue description] - [Suggested action]

### Important (Fix Soon)
1. [Issue description] - [Suggested action]

### Minor (Low Priority)
1. [Issue description] - [Suggested action]

## Strengths
- [What's working well]

## Recommended Actions (Priority Order)

1. **[Action Name]** - [Why this matters]
   ```bash
   [Command to run]
   ```

## Metrics

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| Coverage | [X]% | 90% | [gap] |
| Stale Docs | [N] | <3 | [gap] |
```

## Success Criteria

- Report generated without errors
- At least 3 actionable recommendations
- All critical issues flagged

## Notes

- Run this command at session start
- Run after major changes
- Run before releases

---

*This command helps close the feedback loop by identifying documentation gaps and suggesting specific fixes.*
