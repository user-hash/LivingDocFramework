# Python Example Project with Living Documentation

This is a minimal example showing how to integrate the Living Documentation Framework into a Python project.

## Setup

1. **Install the framework**:
   ```bash
   cp -r /path/to/LivingDocFramework .
   ```

2. **Configure for your project**:
   ```bash
   cp LivingDocFramework/examples/python-project/living-doc-config.yaml .
   nano living-doc-config.yaml
   ```

3. **Install git hooks**:
   ```bash
   ./LivingDocFramework/hooks/install.sh
   ```

4. **Initialize docs**:
   ```bash
   mkdir -p docs
   touch CHANGELOG.md CODE_DOC_MAP.md BUG_PATTERNS.md
   touch docs/INVARIANTS.md docs/GOLDEN_PATHS.md
   ```

## Project Structure

```
python-example/
├── living-doc-config.yaml  # Configuration
├── LivingDocFramework/     # Framework
├── src/                    # Your code
│   ├── __init__.py
│   ├── api/
│   └── db/
├── tests/
│   └── test_*.py
├── docs/
│   ├── INVARIANTS.md
│   └── GOLDEN_PATHS.md
├── CHANGELOG.md
├── CODE_DOC_MAP.md
└── BUG_PATTERNS.md
```

## Usage

### Before Committing
Git hooks automatically run:
- Validates Tier A files have invariants
- Checks CHANGELOG.md updated
- Warns if >5 files changed

## Example Workflow

### 1. Session Start
```bash
git fetch && git pull
cat CHANGELOG.md | head -20
```

### 2. Make Changes
```bash
# Edit code
vim src/api/auth.py

# Update docs
vim docs/INVARIANTS.md  # If Tier A file
vim CHANGELOG.md
```

### 3. Commit
```bash
git add .
git commit -m "feat: Add authentication endpoint"
# Hooks run automatically
```

## Tips

- **Keep CHANGELOG.md updated**: Every commit should have an entry
- **Document Tier A files**: Critical files need invariant citations
- **Define subsystems**: Group related code in config

## Next Steps

1. Customize `living-doc-config.yaml` for your project
2. Define your subsystems
3. Identify Tier A files
4. Start documenting invariants

## Resources

- [Framework Documentation](../../README.md)
- [Configuration Reference](../../docs/CONFIG.md)
- [Agent Protocol](../../protocols/AGENT_PROTOCOL.md)
- [Hook Documentation](../../hooks/README.md)
