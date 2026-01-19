# Living Documentation Framework - Examples

This directory contains example projects showing how to integrate the Living Documentation Framework.

## Available Examples

### 1. Python Project
A complete Python project example with:
- Full configuration
- Directory structure
- Sample documentation files

See [python-project/README.md](python-project/README.md)

### 2. Incident Example
A real-world example showing how the framework prevents bugs:
- Actual incident from production
- Invariant that prevents recurrence
- Bug pattern documentation

See [incident_example/README.md](incident_example/README.md)

## Quick Start with Examples

```bash
# Copy example config to your project
cp LivingDocFramework/examples/python-project/living-doc-config.yaml .

# Customize for your project
nano living-doc-config.yaml

# Install hooks
./LivingDocFramework/hooks/install.sh
```

## Creating Your Own Example

1. Copy the python-project structure
2. Modify `living-doc-config.yaml` for your language
3. Add language-specific patterns
4. Submit a PR!

## Contributing Examples

We welcome examples for:
- JavaScript/TypeScript projects
- Go projects
- Rust projects
- C# projects
- Multi-language monorepos

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.
