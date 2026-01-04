# Living Documentation Framework

**AI-Powered, Schema-Driven Documentation System for Software Projects**

> Extracted from [Nebulae](https://github.com/user-hash/Nebulae) - A 181K-line Unity project managed entirely with AI assistance

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](CHANGELOG.md)
[![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)]()

---

## What is This?

Living Documentation Framework (LDF) is a **production-tested system** that keeps your documentation automatically synchronized with your code through AI-powered agents, git hooks, and dynamic dashboards.

**Born from real need**: Managing 181,000 lines across 284 files with 64 bug patterns, 36 invariants, and 93% system confidence.

---

## Key Features

✅ **Schema-Driven** - Zero hardcoding, configure everything in YAML
✅ **Auto-Discovery** - New files automatically categorized and mapped
✅ **Group Organization** - Subsystems get dedicated doc ecosystems (e.g., MP has 17 docs)
✅ **Interactive Dashboard** - Grafana-style HTML with historical metrics tracking
✅ **Git Hook Enforcement** - Automatic validation at commit time
✅ **AI Agent Protocols** - Ensure AI agents maintain docs
✅ **Session Context** - Fast session loading with memory packs
✅ **Release Gates** - Automated quality checks before shipping

---

## Quick Start

```bash
# Clone the framework
git clone https://github.com/user/living-doc-framework.git
cd your-project

# Initialize (copies framework into .living-docs/)
./living-doc-framework/install.sh

# Configure for your project
edit .living-docs/core/manifest.yaml

# Generate dashboard
.living-docs/tools/dashboard.sh

# Open dashboard
open .living-docs/dashboard/index.html
```

---

## What It Manages

### Document Categories (Auto-Discovered)

| Category | Purpose | Example |
|----------|---------|---------|
| **Patterns** | Bug patterns & anti-patterns | "PATTERN-001: Race in peer registration" |
| **Invariants** | Safety rules that must never break | "INV-1.1: Never lock() in audio thread" |
| **Golden Paths** | Best practices & recommended approaches | "GP-001: Use Monitor.TryEnter for audio" |
| **Decisions** | Architecture Decision Records (ADRs) | "ADR-012: Partial class organization" |
| **Bugs** | Current bug tracking with severity | P0/P1/P2/P3 classification |
| **Code Map** | File-to-documentation mappings | Links code files to their docs |

### Auto-Grouping by Subsystem

Documents automatically group by system tags:
- **Multiplayer**: 24 patterns, 8 invariants, 4 ADRs
- **Audio**: 12 patterns, 6 invariants, 2 ADRs
- **UI**: 8 patterns, 4 invariants, 1 ADR
- **Threading**: 6 patterns, 10 invariants, 1 ADR

---

## Dashboard

![Dashboard Preview](docs/images/dashboard-preview.png)

**Real-time metrics**:
- System confidence % (calculated automatically)
- Bug severity distribution (P0/P1/P2/P3)
- Pattern count by system
- Documentation coverage
- Historical trends

**Charts**:
- Multi-metric health over time
- Pattern distribution (doughnut)
- Bug severity breakdown (doughnut)
- Subsystem confidence (radar)
- Coverage progress (line)

---

## How It Works

### 1. Schema-Driven Configuration

Everything configured in `manifest.yaml`:

```yaml
categories:
  patterns:
    subcategories:
      - name: "multiplayer"
        pattern: '\*\*System:\*\*.*Multiplayer'
      - name: "audio"
        pattern: '\*\*System:\*\*.*Audio'

  auto_mapping:
    rules:
      - file_pattern: "**/Multiplayer/**"
        docs:
          - "MULTIPLAYER_ARCHITECTURE.md"
          - "INVARIANTS.md#7"
```

### 2. Auto-Discovery

```bash
# System scans for:
# - New files → Auto-suggests tier (A/B/C/D)
# - New patterns → Auto-categorizes by system tag
# - New sections → Auto-maps to architecture docs
```

### 3. Git Hook Enforcement

```bash
# Pre-commit checks:
# ✓ Tier A files have documentation
# ✓ Version numbers match across files
# ✓ No orphaned doc entries
# ✓ Agent reports include compliance proof
```

### 4. AI Agent Compliance

```markdown
## Agent Protocol (MANDATORY)
Before changes: READ CODE_DOC_MAP.md, INVARIANTS.md
After changes: UPDATE affected docs, include proof

## Proof of Compliance
- [ ] Read docs before changes
- [ ] Updated affected docs
- [ ] No drift introduced
```

---

## Real-World Results

**From Nebulae Project**:

| Metric | Value | Change |
|--------|-------|--------|
| System Confidence | 93% | +43% |
| Documentation Coverage | 96% (273/284 files) | +96% |
| Bug Patterns Documented | 64 | +64 |
| Invariants Codified | 36 | +36 |
| Stale Documentation | 0 files | -15 |

**Time Savings**:
- Doc updates: Manual (2 hours) → Automatic (<1 minute)
- Context loading: Reading (30 min) → Memory pack (30 seconds)
- Bug categorization: Manual → Auto-discovered by system tag

---

## Documentation

| Document | Description |
|----------|-------------|
| [SETUP.md](docs/SETUP.md) | Installation & configuration |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design & components |
| [SCHEMAS.md](docs/SCHEMAS.md) | Schema & template reference |
| [DASHBOARD.md](docs/DASHBOARD.md) | Dashboard configuration |
| [HOOKS.md](docs/HOOKS.md) | Git hook system |
| [AGENTS.md](docs/AGENTS.md) | AI agent protocols |
| [WORKFLOWS.md](docs/WORKFLOWS.md) | Slash command reference |
| [BEST_PRACTICES.md](docs/BEST_PRACTICES.md) | Lessons learned |

---

## Language Support

**Tested**:
- ✅ C# (Unity) - Nebulae project
- ✅ Python - Example included
- ✅ JavaScript/TypeScript - Example included

**Easy to adapt**:
- Go, Rust, Java, C++, Swift, Kotlin
- Any language with version files and doc comments

---

## Requirements

- **Git** (for hooks)
- **Bash** 4.0+ (for tools)
- **Python** 3.8+ (optional, for confidence calculator & doc-engine)
- **Chart.js** 4.4.1+ (bundled in dashboard HTML)

---

## Examples

### Python Project

```bash
cd your-python-project
./living-doc-framework/install.sh --language python

# manifest.yaml auto-configures:
# - version_file: __init__.py
# - code_root: src/
# - version_pattern: __version__ = "([0-9.]+)"
```

### JavaScript/TypeScript Project

```bash
cd your-js-project
./living-doc-framework/install.sh --language javascript

# manifest.yaml auto-configures:
# - version_file: package.json
# - code_root: src/
# - version_pattern: "version": "([0-9.]+)"
```

---

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT License - See [LICENSE](LICENSE)

---

## Acknowledgments

**Original Project**: [Nebulae - Producer Journey](https://github.com/user-hash/Nebulae)
- 6 months of AI-assisted development
- 181,000 lines of Unity C# code
- Living proof that AI + Human collaboration scales

**Powered by**: [Claude](https://claude.ai) by Anthropic

---

## Support

- **Issues**: [GitHub Issues](https://github.com/user/living-doc-framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/user/living-doc-framework/discussions)

---

**Transform your codebase into a living, self-documenting organism.** 🌱
