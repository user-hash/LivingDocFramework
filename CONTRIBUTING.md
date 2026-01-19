# Contributing to Living Documentation Framework

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

**Bug Reports**:
- Use GitHub Issues
- Include framework version
- Describe expected vs actual behavior
- Provide minimal reproduction example
- Include config file (sanitized)

**Feature Requests**:
- Describe the use case
- Explain why existing features don't solve it
- Propose API/configuration changes
- Consider backward compatibility

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Make changes**
4. **Test thoroughly**
5. **Update documentation**
6. **Submit PR**

### PR Checklist

- [ ] Code follows project style
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No breaking changes (or documented)
- [ ] All tests pass
- [ ] Example updated (if relevant)

## Development Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/LivingDocFramework.git
cd LivingDocFramework

# Create test project
mkdir test-project
cd test-project
../hooks/install.sh

# Test hooks
git add . && git commit -m "test: Test commit"
```

## Code Style

### Shell Scripts
- Use `set -e` for error handling
- Quote variables: `"$VAR"` not `$VAR`
- Use `$(...)` not backticks
- Comment non-obvious logic

### YAML
- 2-space indentation
- Use lowercase keys
- Comment complex sections

## Testing

### Manual Testing

Test with multiple languages:
```bash
cd examples/python-project
../../hooks/install.sh
git add . && git commit -m "test: Test hooks"
```

### Automated Testing

Run the test suite with pytest:

```bash
pip install pytest
pytest tests/test_config.py
```

## Adding Language Support

To add a new language profile:

1. **Create language file**:
   ```bash
   cp core/languages/python.yaml core/languages/newlang.yaml
   ```

2. **Edit configuration**:
   ```yaml
   language: newlang
   display_name: "New Language"

   version:
     files: ["version.ext"]
     patterns: ['PATTERN_HERE']

   code:
     extensions: ["ext"]
     root: "src/"
   ```

3. **Test with example**
4. **Update documentation**

## Adding Commands

To add a slash command:

1. **Create command file**: `commands/new-command.md`
2. **Follow format**:
   ```markdown
   ---
   description: What this command does
   ---

   # Task: Command Name

   [Full prompt here]
   ```
3. **Document in commands/README.md**

## Documentation

All user-facing changes need documentation:

- **README.md**: Overview, features, quick start
- **docs/INTEGRATION.md**: Installation and configuration
- **docs/CONFIG.md**: Configuration reference
- **hooks/README.md**: Hook-specific docs
- **examples/**: Example projects

## Release Process

1. **Update version**: `core/manifest.yaml`, `README.md`
2. **Update CHANGELOG.md**: Add release notes
3. **Tag release**: `git tag -a v1.x.x -m "Release vX.X.X"`
4. **Push tag**: `git push origin v1.x.x`
5. **Create GitHub release**: Add changelog excerpt

## Community Guidelines

- Be respectful and inclusive
- Help newcomers
- Share knowledge
- Give constructive feedback
- Credit contributors

Thank you for contributing!
