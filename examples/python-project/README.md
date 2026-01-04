# Python Example Project with Living Documentation

This is a minimal example showing how to integrate the Living Documentation Framework into a Python project.

## Setup

1. **Install the framework**:
   ```bash
   # Clone or copy LivingDocFramework into your project
   cp -r /path/to/LivingDocFramework .
   ```

2. **Configure for your project**:
   ```bash
   # Copy the example config
   cp LivingDocFramework/examples/python-project/living-doc-config.yaml .

   # Edit to match your project
   nano living-doc-config.yaml
   ```

3. **Install git hooks**:
   ```bash
   ./LivingDocFramework/hooks/install.sh
   ```

4. **Initialize docs**:
   ```bash
   mkdir -p docs
   touch CHANGELOG.md BUG_TRACKER.md BUG_PATTERNS.md
   touch docs/INVARIANTS.md docs/GOLDEN_PATHS.md docs/DECISIONS.md docs/CODE_DOC_MAP.md
   ```

## Project Structure

```
python-example/
├── living-doc-config.yaml  # Configuration
├── LivingDocFramework/     # Framework (from git submodule or copy)
├── src/                    # Your code
│   ├── __init__.py
│   ├── api/
│   ├── db/
│   └── utils/
├── tests/                  # Your tests
│   └── test_*.py
├── docs/                   # Living documentation
│   ├── INVARIANTS.md
│   ├── GOLDEN_PATHS.md
│   ├── DECISIONS.md
│   └── CODE_DOC_MAP.md
├── CHANGELOG.md
├── BUG_TRACKER.md
└── BUG_PATTERNS.md
```

## Usage

### Check Documentation Health
```bash
python LivingDocFramework/tools/calculate_confidence.py
```

### Before Committing
Git hooks automatically run:
- Validates Tier A files have invariants
- Checks CHANGELOG.md updated
- Warns if >5 files changed

### After Committing
Hooks automatically:
- Update confidence score
- Refresh dashboard

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

### 4. Check Health
```bash
python LivingDocFramework/tools/calculate_confidence.py
```

## Tips

- **Keep CHANGELOG.md updated**: Every commit should have an entry
- **Document Tier A files**: Critical files need invariant citations
- **Use slash commands**: Create commands in `.claude/commands/`
- **Review confidence score**: Aim for 85%+

## Next Steps

1. Customize `living-doc-config.yaml` for your project
2. Define your subsystems
3. Identify Tier A files
4. Start documenting invariants
5. Run `/living-docs` command to check health

## Integration with Tools

### pytest
```python
# In conftest.py
def pytest_sessionfinish(session, exitstatus):
    """Update docs after test run"""
    import subprocess
    subprocess.run([
        "python", "LivingDocFramework/tools/calculate_confidence.py", "--update"
    ])
```

### pre-commit (Python tool)
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: living-docs
        name: Living Documentation Check
        entry: bash LivingDocFramework/hooks/pre-commit
        language: system
```

## Resources

- [Framework Documentation](../../README.md)
- [Configuration Reference](../../core/project-config.template.yaml)
- [Agent Protocol](../../protocols/AGENT_PROTOCOL.md)
- [Hook Documentation](../../hooks/README.md)
