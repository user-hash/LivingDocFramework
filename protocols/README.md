# Living Documentation Framework - Protocols

Protocols define how AI agents and humans should interact with the living documentation system.

## Core Protocols

### AGENT_PROTOCOL.md
**Purpose**: Mandatory compliance rules for ALL AI agents

**Key Requirements**:
- Read docs before making changes
- Update docs after making changes
- Cite invariants for Tier A files
- Include proof of compliance in reports

**When to Use**:
- Include in EVERY agent prompt via Task tool
- Reference when reviewing agent work
- Enforce via git hooks

### Using the Agent Protocol

#### In Agent Prompts

```markdown
## Task: Fix authentication bug

[... task description ...]

## Agent Protocol (MANDATORY COMPLIANCE)
{paste full protocol from AGENT_PROTOCOL.md}

## Report Format
Your report MUST include:
- Documentation Updates section
- Proof of Compliance checklist
```

#### Enforcing Compliance

1. **Pre-Launch**: Check agent prompt includes protocol
2. **Post-Completion**: Verify report has compliance proof
3. **Pre-Commit**: Git hooks validate doc updates

## Additional Protocols (To Extract)

### FIX_AGENT_PROTOCOL.md
**Purpose**: Bug-fix specific requirements
**Status**: ⏳ To extract from Nebulae

### CLAUDE_PROTOCOL.md
**Purpose**: Claude-specific workflows
**Status**: ⏳ To extract from Nebulae

### AGENT_ENFORCEMENT.md
**Purpose**: How to enforce agent compliance
**Status**: ⏳ To extract from Nebulae

## Best Practices

### For Spawning Agents

1. ✅ **Always include protocol**: Don't assume agents know the rules
2. ✅ **Specify report format**: Tell agents exactly what to return
3. ✅ **Read docs first**: Load context before launching agents
4. ✅ **Verify compliance**: Check agent reports have required sections

### For Writing Agents

If you're the agent:
1. ✅ **Read first, code second**: Always load docs before making changes
2. ✅ **Document as you go**: Update docs immediately after code changes
3. ✅ **Prove compliance**: Include the checklist in your report
4. ✅ **Ask when unclear**: Better to ask than drift

## Common Mistakes

### ❌ Launching Without Protocol
```markdown
## Task: Fix bug in auth.py
Please fix the authentication issue
```

**Problem**: Agent doesn't know to update docs

### ✅ Correct Approach
```markdown
## Task: Fix bug in auth.py

[... description ...]

## Agent Protocol (MANDATORY COMPLIANCE)
{full protocol here}

Your report MUST include proof of doc updates
```

### ❌ Missing Compliance Proof
```markdown
## Summary
Fixed the bug by adding null check

## Files Changed
- auth.py
```

**Problem**: No documentation updates, no proof of compliance

### ✅ Correct Report
```markdown
## Summary
Fixed the bug by adding null check

## Documentation Updates
- Files updated: auth.py
- INVARIANTS.md: Updated INV-4.2 (null check enforcement)
- CODE_DOC_MAP.md: No change needed (file already mapped)

## Proof of Compliance
- [x] Read CODE_DOC_MAP.md before changes
- [x] Read INVARIANTS.md for Tier A files
- [x] Updated all affected docs
- [x] No drift introduced
```

## Integration with Hooks

Git hooks automatically enforce protocol compliance:

```bash
# pre-commit checks:
- Tier A files changed? → INVARIANTS.md must be updated
- New files created? → CODE_DOC_MAP.md must be updated
- Version changed? → CHANGELOG.md must be updated
```

## Customization

Edit `AGENT_PROTOCOL.md` to match your project:

1. **Add project-specific rules**:
   ```markdown
   ### Project-Specific Requirements
   - All database changes require migration file
   - All API changes require OpenAPI spec update
   ```

2. **Define your Tier A criteria**:
   ```markdown
   ### Tier A Files (Project-Specific)
   - All files in src/core/
   - All *Manager.py files
   - All database models
   ```

3. **Customize report format**:
   ```markdown
   ### Report Format
   Must include:
   - Summary
   - Test results
   - Performance impact
   - Documentation updates
   ```

## Status

- ✅ AGENT_PROTOCOL.md - Extracted and generalized
- ⏳ FIX_AGENT_PROTOCOL.md - To extract
- ⏳ CLAUDE_PROTOCOL.md - To extract
- ⏳ AGENT_ENFORCEMENT.md - To extract

**Next**: Extract remaining protocols or move to commands extraction.
