# Living Documentation Framework

> Documentation that enforces itself through git hooks.

**Disclaimer**: This repository documents a documentation enforcement framework, not a full product. Features documented here are extracted and production-tested.

![Documentation Structure](docs/images/publish/DocTree.png)

---

## What It Does

- Maps code files to documentation
- Documents bugs as reusable prevention patterns
- Blocks commits that skip documentation updates

**Config-driven**: Paths, extensions, subsystems, and hook rules are configured in YAML.

---

## Quick Start

### 1. Add Framework

**Option A: Git Submodule** (recommended)
```bash
git submodule add https://github.com/user-hash/LivingDocFramework.git
```

**Option B: Copy/Vendor**
```bash
cp -r /path/to/LivingDocFramework ./LivingDocFramework
```

### 2. Setup

```bash
# Create config
cp LivingDocFramework/core/project-config.template.yaml living-doc-config.yaml

# Create doc files
mkdir -p docs
touch CODE_DOC_MAP.md BUG_PATTERNS.md CHANGELOG.md
touch docs/INVARIANTS.md docs/GOLDEN_PATHS.md

# Install hooks (requires Bash - use Git Bash on Windows)
./LivingDocFramework/hooks/install.sh
```

---

## Target Folder Structure

```
your-project/
├── living-doc-config.yaml    # Controls everything
├── LivingDocFramework/       # Framework
├── CODE_DOC_MAP.md           # File → doc mappings
├── BUG_PATTERNS.md           # Anti-patterns
├── CHANGELOG.md              # Release notes
└── docs/
    ├── INVARIANTS.md         # Safety rules
    └── GOLDEN_PATHS.md       # Best practices
```

---

## Minimal Configuration

```yaml
project:
  name: "MyProject"
  language: "python"  # python | javascript | go | rust | csharp
  main_branch: "main"

code:
  root: "src/"
  extensions: ["py"]

hooks:
  pre_commit:
    - check: "changelog_updated"
      enabled: true
      blocking: true
```

See [docs/CONFIG.md](docs/CONFIG.md) for full reference.

---

## Core Documents

| Document | Purpose |
|----------|---------|
| `CODE_DOC_MAP.md` | Maps files to their documentation |
| `BUG_PATTERNS.md` | Documented bugs with prevention patterns |
| `INVARIANTS.md` | Safety rules that block violations |
| `CHANGELOG.md` | Release history |

---

## Documentation

- [Integration Guide](docs/INTEGRATION.md) — Setup for existing codebases
- [Configuration Reference](docs/CONFIG.md) — Full YAML options
- [Git Hooks](hooks/README.md) — Customization
- [Agent Protocol](protocols/AGENT_PROTOCOL.md) — AI agent compliance rules
- [Example: Real Incident](examples/incident_example/) — How the system prevents bugs

---

## Proven in Production

Extracted from the **Nebulae project** (181K LOC, 6+ months production use):

- 64 bug patterns documented
- 36 invariants enforced
- 284 files mapped

---

## Requirements

- Git
- Bash 4.0+ (Git Bash on Windows)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

AGPL v3 — See [LICENSE](LICENSE)

---

*Transform scattered context into enforced understanding.*
