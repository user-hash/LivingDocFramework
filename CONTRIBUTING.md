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

# Make changes
# ... edit files ...

# Test locally
python3 ../tools/calculate_confidence.py
```

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Docstrings for public functions
- Max line length: 100

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
# Test Python
cd examples/python-project
../../hooks/install.sh
python3 ../../tools/calculate_confidence.py

# Test JavaScript (when example exists)
cd examples/js-project
../../hooks/install.sh
# ... test ...
```

### Automated Testing

(TODO: Add automated tests)

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

   # ... customize ...
   ```

3. **Test with example**:
   ```bash
   mkdir examples/newlang-project
   # Create example config
   # Test hooks
   ```

4. **Update documentation**:
   - Add to supported languages list
   - Create example in `examples/`
   - Document any quirks

## Adding Tools

To add a new automation tool:

1. **Create tool file**: `tools/new-tool.py` or `tools/new-tool.sh`
2. **Use config system**:
   ```python
   from config import get_config
   config = get_config()
   ```
3. **Document in tools/README.md**
4. **Add usage examples**
5. **Test with multiple languages**

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
4. **Test command execution**

## Documentation

All user-facing changes need documentation:

- **README.md**: Overview, features, quick start
- **SETUP.md**: Installation and configuration
- **tools/README.md**: Tool-specific docs
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

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Thanked publicly

## Questions?

- Open an issue for questions
- Join discussions
- Check existing issues first

Thank you for contributing!
