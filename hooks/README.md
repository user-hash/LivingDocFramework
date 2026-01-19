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
- **Tier A files** require sibling INVARIANTS.md update (doc-set aware)
- VERSION file matches CHANGELOG
- Blast radius warning (>5 files changed)
- Conflict detection (file in multiple CODE_DOC_MAPs)

**Doc-Set Discovery**: The hook automatically scans all `docs/*/CODE_DOC_MAP.md` files. When a Tier A file changes, it requires the **sibling** `INVARIANTS.md` to be updated.

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

## Requirements

**Bash 4.0+** is required (for associative arrays used in Tier A tracking).

| Platform | How to get Bash 4+ |
|----------|-------------------|
| macOS | `brew install bash` (default `/bin/bash` is 3.2) |
| Windows | Git Bash (bundled with Git for Windows) |
| Linux | Usually already 4.0+, verify with `bash --version` |

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

## Known Limitations

### YAML Parser
The config loader uses a simple grep-based YAML parser (when `yq` is not installed). It expects:
- Exactly 2 spaces of indentation
- Standard field ordering

For complex configurations, install `yq` for robust parsing:
```bash
# macOS
brew install yq

# Linux
sudo apt install yq  # or snap install yq
```

### Code Extension Matching
The pre-commit hook supports multiple extensions via `$LDF_CODE_EXTS` (comma-separated, e.g., `js,ts,jsx,tsx`). Language profiles set this automatically.

### Path Format in CODE_DOC_MAP
Entries **must** use:
1. **Repo-relative paths** (e.g., `src/api/auth.py`, not just `auth.py`)
2. **Backticks around the path** for markdown table format

```markdown
# CORRECT - backticks and full path
| `src/api/auth.py` | TIER A | Authentication |

# WRONG - no backticks (won't be detected)
| src/api/auth.py | TIER A | Authentication |

# WRONG - basename only (ambiguous)
| `auth.py` | TIER A | Authentication |
```
