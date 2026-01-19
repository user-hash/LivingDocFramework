# Living Documentation Framework - Git Hooks

Git hooks enforce documentation requirements automatically at commit time.

## Available Hooks

### install.sh
Installs all git hooks into your project's `.git/hooks/` directory.

```bash
./LivingDocFramework/hooks/install.sh
```

### pre-commit
Validates documentation requirements before allowing commit.

**Checks**:
- Tier A files have documentation
- VERSION file matches CHANGELOG
- Blast radius warning (>5 files changed)

**Configuration** in `living-doc-config.yaml`:
```yaml
hooks:
  pre_commit:
    - check: "tier_a_citation"
      enabled: true
      blocking: true

    - check: "changelog_updated"
      enabled: true
      blocking: true

    - check: "blast_radius"
      threshold: 5
      blocking: false
```

### post-commit
Automated actions after successful commit.

### commit-msg
Validates commit message format.

**Requirements**:
- Starts with type: `feat:`, `fix:`, `docs:`, `refactor:`, etc.
- References docs if Tier A files changed

## Installation

### Automatic (Recommended)
```bash
cd your-project/
./LivingDocFramework/hooks/install.sh
```

### Manual
```bash
cd your-project/.git/hooks/
ln -s ../../LivingDocFramework/hooks/pre-commit pre-commit
ln -s ../../LivingDocFramework/hooks/commit-msg commit-msg
chmod +x pre-commit commit-msg
```

## Customization

Edit hooks to match your workflow:

1. **Adjust enforcement levels**:
   - Change `exit 1` to `exit 0` for warnings instead of errors

2. **Add project-specific checks**:
   ```bash
   if git diff --cached | grep -i "TODO.*FIXME"; then
       echo "WARNING: TODO/FIXME found in commit"
   fi
   ```

## Bypassing Hooks

**During emergencies only**:
```bash
git commit --no-verify -m "Emergency fix"
```

Warning: Bypassing hooks can lead to documentation drift!

## Troubleshooting

### Hook not executing
```bash
ls -l .git/hooks/pre-commit   # Check permissions
chmod +x .git/hooks/pre-commit # Fix if needed
```

### Hook failing
```bash
.git/hooks/pre-commit  # Run manually to see output
echo $?                 # Check exit code
```

### Disable specific check
Edit `living-doc-config.yaml`:
```yaml
hooks:
  pre_commit:
    - check: "tier_a_citation"
      enabled: false
```
