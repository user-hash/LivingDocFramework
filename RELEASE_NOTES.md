# Living Documentation Framework - Release Notes

---

## v1.0.1 - Initial Public Release

**Release Date**: 2026-01-10
**Status**: Production Ready
**Extracted From**: Nebulae Project (v0.913+)

---

## v1.0.0 - Foundation Release

**Release Date**: 2026-01-04
**Status**: Production Ready
**Extracted From**: Nebulae Project (v0.913+)

---

## What's Included

### Core System
- 4 JSON schemas (pattern, golden-path, invariant, decision)
- 4 Markdown templates
- 2 generalized manifests (manifest.yaml, doc-system.yaml)
- 5 language profiles (Python, JavaScript, Go, Rust, C#)
- Project configuration template
- Configuration loaders (Shell + Python)

### Git Hooks
- install.sh - Hook installer
- pre-commit - Documentation validation
- post-commit - Automatic updates
- commit-msg - Message format validation

### Protocols & Commands
- AGENT_PROTOCOL.md - Mandatory agent compliance
- Slash command system
- living-docs.md - Health check command

### Examples
- Python project with complete configuration
- Incident example with real-world bug prevention

### Documentation
- README.md - Project overview
- docs/INTEGRATION.md - Integration guide
- docs/CONFIG.md - Configuration reference
- docs/SESSION_PROTOCOL.md - Version sync protocol
- CONTRIBUTING.md - Contribution guidelines

---

## Key Features

### 1. Language-Agnostic Architecture
Works with **any language**: Python, JavaScript, Go, Rust, C#, and more.
- Language profiles define language-specific defaults
- Config system uses placeholders
- File finding uses config helpers

### 2. Config-Driven
Everything configurable via `living-doc-config.yaml`:
```yaml
project:
  name: "MyProject"
  language: "python"

code:
  root: "src/"
  extensions: ["py"]
```

### 3. Automatic Enforcement
Git hooks validate:
- Tier A files have invariant citations
- CHANGELOG.md updated with code changes
- Blast radius warnings
- Commit message format

### 4. AI Agent Compliance
Protocol ensures agents:
- Read docs before making changes
- Update docs after making changes
- Cite invariants for critical files

### 5. Scalable Organization
Group docs by subsystem - each maintains its own patterns, invariants, decisions.

---

## Proven in Production

Extracted from Nebulae project:
- **181,048 lines** of code managed
- **284 files** tracked
- **64 bug patterns** documented
- **36 invariants** enforced
- **6 months** of production use

---

## Requirements

- Git
- Bash 4.0+

---

## License

AGPL v3 - See [LICENSE](LICENSE)
