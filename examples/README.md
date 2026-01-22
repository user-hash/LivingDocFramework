# Living Documentation Framework - Examples

This directory contains example projects showing how to integrate the Living Documentation Framework.


## Recommended Starting Point

Start with **quickstart/** — includes actual code to trigger and fix violations.


## Available Examples

### 0. Quickstart (Start Here)
A minimal runnable example with actual Python code:
- Experience the failure/fix loop in 5 minutes
- Pre-configured for immediate use

See [quickstart/README.md](quickstart/README.md)

### 1. Python Project
A complete Python project example with:
- Full configuration
- Directory structure
- Sample documentation files

See [python-project/README.md](python-project/README.md)

### 2. Sample Workflow
A real-world example showing how the framework enables fast, accurate fixes:
- Scenario that led to a documented pattern
- Invariant that prevents recurrence
- Bug pattern documentation
- **External review workflow** - how reviewers use docs for quick fixes

See [sample_workflow/README.md](sample_workflow/README.md)

### 3. Incident Example (Legacy)
The original incident example. Kept for reference.

See [incident_example/README.md](incident_example/README.md)

## Quick Start with Examples

```bash
# Copy example config to your project
cp LivingDocFramework/examples/python-project/living-doc-config.yaml .

# Customize for your project
nano living-doc-config.yaml

# Install hooks
bash LivingDocFramework/hooks/install.sh
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
