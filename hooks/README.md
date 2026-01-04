# Living Documentation Framework - Git Hooks

Git hooks enforce documentation requirements automatically at commit time.

## Available Hooks

### 1. install.sh
Installs all git hooks into your project's `.git/hooks/` directory.

**Usage**:
```bash
./LivingDocFramework/hooks/install.sh
```

### 2. pre-commit
**Purpose**: Validates documentation requirements before allowing commit

**Checks**:
- ✅ Tier A files have documentation
- ✅ VERSION file matches CHANGELOG
- ✅ CODE_DOC_MAP is up-to-date
- ✅ No orphaned doc entries
- ⚠️  Blast radius warning (>5 files changed)

**Configuration**: Edit `living-doc-config.yaml` to customize:
```yaml
hooks:
  pre_commit:
    - check: "tier_a_citation"
      enabled: true
      blocking: true  # Block commit if violated

    - check: "changelog_updated"
      enabled: true
      blocking: true

    - check: "blast_radius"
      threshold: 5  # Warn if > 5 files changed
      blocking: false
```

### 3. post-commit
**Purpose**: Automated actions after successful commit

**Actions**:
- 📊 Update dashboard
- 📈 Calculate confidence score
- 📝 Log commit to history

### 4. commit-msg
**Purpose**: Validate commit message format

**Requirements**:
- Starts with type: `feat:`, `fix:`, `docs:`, `refactor:`, etc.
- References docs if Tier A files changed
- Includes bug pattern ref if fixing bugs

## Installation

### Option 1: Automatic (Recommended)
```bash
cd your-project/
./LivingDocFramework/hooks/install.sh
```

### Option 2: Manual
```bash
cd your-project/.git/hooks/
ln -s ../../LivingDocFramework/hooks/pre-commit pre-commit
ln -s ../../LivingDocFramework/hooks/post-commit post-commit
ln -s ../../LivingDocFramework/hooks/commit-msg commit-msg
chmod +x pre-commit post-commit commit-msg
```

## Hook Templates

### pre-commit Template
```bash
#!/bin/bash
# Pre-commit hook - Documentation validation

# Load configuration
REPO_ROOT=$(git rev-parse --show-toplevel)
source "$REPO_ROOT/LivingDocFramework/core/load-config.sh"

# Check if Tier A files changed
TIER_A_CHANGED=$(git diff --cached --name-only | grep "$LDF_CODE_ROOT" | wc -l)

if [ "$TIER_A_CHANGED" -gt 0 ]; then
    # Verify INVARIANTS.md updated
    INVARIANTS_UPDATED=$(git diff --cached --name-only | grep -c "INVARIANTS")

    if [ "$INVARIANTS_UPDATED" -eq 0 ]; then
        echo "ERROR: Tier A files changed but INVARIANTS.md not updated"
        echo "Please cite relevant invariants or add new ones"
        exit 1
    fi
fi

# Check CHANGELOG updated
CHANGELOG_UPDATED=$(git diff --cached --name-only | grep -c "CHANGELOG")
if [ "$CHANGELOG_UPDATED" -eq 0 ]; then
    echo "WARNING: CHANGELOG not updated"
    echo "Consider adding entry to $LDF_CHANGELOG"
fi

exit 0
```

### post-commit Template
```bash
#!/bin/bash
# Post-commit hook - Update dashboard

REPO_ROOT=$(git rev-parse --show-toplevel)

# Update dashboard if available
if [ -f "$REPO_ROOT/LivingDocFramework/tools/calculate_confidence.py" ]; then
    python3 "$REPO_ROOT/LivingDocFramework/tools/calculate_confidence.py" --update 2>/dev/null
    echo "✅ Confidence score updated"
fi
```

## Customization

Edit hooks to match your workflow:

1. **Adjust enforcement levels**:
   - Change `exit 1` to `exit 0` for warnings instead of errors
   - Add `|| true` to make checks advisory

2. **Add project-specific checks**:
   ```bash
   # Check for TODO comments in production code
   if git diff --cached | grep -i "TODO.*FIXME"; then
       echo "WARNING: TODO/FIXME found in commit"
   fi
   ```

3. **Integrate with CI/CD**:
   ```bash
   # Trigger CI build
   curl -X POST https://ci-server.com/api/build
   ```

## Bypassing Hooks

**During emergencies only**:
```bash
git commit --no-verify -m "Emergency fix"
```

⚠️ **Warning**: Bypassing hooks can lead to documentation drift!

## Troubleshooting

### Hook not executing
```bash
# Check permissions
ls -l .git/hooks/pre-commit
# Should show: -rwxr-xr-x

# Fix if needed
chmod +x .git/hooks/pre-commit
```

### Hook failing incorrectly
```bash
# Run hook manually to see output
.git/hooks/pre-commit
echo $?  # Exit code (0 = success, 1 = failure)
```

### Disable specific check
Edit `living-doc-config.yaml`:
```yaml
hooks:
  pre_commit:
    - check: "tier_a_citation"
      enabled: false  # Temporarily disable
```

## Hooks to Extract

From Nebulae `.claude/hooks/`:

### Priority 1 (Extract first)
1. ✅ install-hooks.sh (99 lines) - Hook installer
2. ⏳ pre-commit-doc-check.sh (894 lines) - Main validation
3. ⏳ post-commit-dashboard.sh - Dashboard updates

### Priority 2
4. commit-msg-doc-check.sh - Message validation
5. validate-agent-report.sh - Agent compliance
6. auto-sync-doc-refs.sh - Reference syncing

### Priority 3
7. sync-doc-versions.sh - Version consistency
8. validate-doc-file-refs.sh - File reference validation
9. impact-forecast.sh - Change impact prediction
10. post-push.sh - Post-push actions

## Status

- Documentation: ✅ Complete
- Templates: ✅ Provided
- install.sh: ⏳ To extract
- pre-commit: ⏳ To extract
- Remaining hooks: ⏳ To extract

**Next**: Extract install-hooks.sh and pre-commit hook with generalization.
