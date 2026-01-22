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

**Checks** (blocking vs warning):
- **Tier A files** require sibling INVARIANTS.md update (**blocks** commit)
- **Version mismatch** between version file and CHANGELOG (**blocks** commit)
- **Conflict detection** - file in multiple CODE_DOC_MAPs (**blocks** commit)
- **Changelog reminder** - warns if code changed but CHANGELOG not updated (warning only)
- **Blast radius warning** - warns if >5 files changed (warning only)

**Doc-Set Discovery**: The hook automatically scans all `docs/*/CODE_DOC_MAP.md` files. When a Tier A file changes, it requires the **sibling** `INVARIANTS.md` to be updated.

**Configuration** in `living-doc-config.yaml`:
```yaml
hooks:
  pre_commit:
    - check: "tier_a_citation"
      enabled: true
      blocking: true      # Blocks commit if INVARIANTS.md not updated

    - check: "changelog_updated"
      enabled: true
      blocking: false     # Warning only (doesn't block)

    - check: "blast_radius"
      threshold: 5
      blocking: false     # Warning only
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
bash LivingDocFramework/hooks/install.sh
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

## CODE_DOC_MAP Format Requirements

Entries in CODE_DOC_MAP.md **must** follow these rules for Tier-A detection to work:

### 1. Use Repo-Relative Paths

Paths must be relative to the project root, not basenames:

```markdown
| `src/api/auth.py` | TIER A | Authentication |     ← CORRECT
| `auth.py` | TIER A | Authentication |              ← WRONG (ambiguous)
```

**Why?** Basenames like `auth.py` or `Utils.cs` could match multiple files across subsystems. Repo-relative paths ensure deterministic matching.

### 2. Use Backticks Around Paths

The hook uses fixed-string grep matching on `` `path` `` format:

```markdown
| `src/api/auth.py` | TIER A | Authentication |     ← CORRECT (detected)
| src/api/auth.py | TIER A | Authentication |       ← WRONG (not detected)
```

**Why?** Backticks provide unambiguous delimiters for grep matching and are standard markdown code formatting.

### 3. Include "TIER A" on the Same Line

The Tier A token must appear on the same line as the file path:

```markdown
| `src/api/auth.py` | TIER A | Authentication |     ← CORRECT

## Tier A Files                                      ← Section header alone won't work
| `src/api/auth.py` | Critical | Authentication |   ← WRONG (no TIER A on this line)
```

---

## Known Limitations

### YAML Parser (Fallback)

When `yq` is not installed, the config loader uses a section-aware grep/awk parser. It handles most configurations correctly but expects:
- 2-space indentation for nested fields
- Standard YAML structure

For complex configurations, install `yq` for fully robust parsing:
```bash
# macOS
brew install yq

# Linux
sudo apt install yq  # or snap install yq
```

### Multi-Extension Support

The pre-commit hook supports multiple extensions via `$LDF_CODE_EXTS` (comma-separated, e.g., `js,ts,jsx,tsx`). Language profiles set this automatically based on the configured language.
