# Living Documentation Framework - Setup Guide

Complete installation and configuration guide for integrating the Living Documentation Framework into your project.

## Prerequisites

- **Git**: Version control system
- **Bash** 4.0+ (for shell tools)
- **Python** 3.8+ (for Python tools)
- **jq** (optional but recommended, for JSON processing)
- **yq** (optional, for robust YAML parsing)

## Quick Start (5 Minutes)

### 1. Add Framework to Your Project

**Option A: Git Submodule (Recommended)**
```bash
cd your-project/
git submodule add https://github.com/YOUR_USERNAME/LivingDocFramework.git
git submodule update --init --recursive
```

**Option B: Copy Directly**
```bash
cd your-project/
cp -r /path/to/LivingDocFramework .
```

### 2. Create Configuration

```bash
cp LivingDocFramework/core/project-config.template.yaml living-doc-config.yaml
```

Edit `living-doc-config.yaml`:
```yaml
project:
  name: "YourProject"
  language: "python"  # or javascript, go, rust, csharp
  main_branch: "main"

code:
  root: "src/"  # Where your code lives
  extensions: ["py"]

version:
  file: "__init__.py"  # Where version is defined
  pattern: '__version__\s*=\s*"([0-9.]+)"'
```

### 3. Initialize Documentation

```bash
# Create required directories
mkdir -p docs .claude/dashboard

# Create required files
touch CHANGELOG.md BUG_TRACKER.md BUG_PATTERNS.md
touch docs/INVARIANTS.md docs/GOLDEN_PATHS.md docs/DECISIONS.md docs/CODE_DOC_MAP.md
```

### 4. Install Git Hooks

```bash
./LivingDocFramework/hooks/install.sh
```

### 5. Test Installation

```bash
# Calculate confidence score
python3 LivingDocFramework/tools/calculate_confidence.py

# Make a test commit
git add .
git commit -m "feat: Add Living Documentation Framework"
# Hooks should run automatically
```

✅ **Done!** The framework is now active.

---

## Detailed Setup

### Language-Specific Configuration

#### Python Projects

```yaml
project:
  language: "python"

version:
  file: "__init__.py"
  pattern: '__version__\s*=\s*"([0-9.]+)"'

code:
  root: "src/"
  extensions: ["py"]

tests:
  pattern: "**/test_*.py"
  frameworks: [pytest]
```

#### JavaScript/TypeScript Projects

```yaml
project:
  language: "javascript"

version:
  file: "package.json"
  pattern: '"version":\s*"([0-9.]+)"'

code:
  root: "src/"
  extensions: ["js", "ts", "jsx", "tsx"]

tests:
  pattern: "**/*.test.{js,ts}"
  frameworks: [jest, mocha]
```

#### Go Projects

```yaml
project:
  language: "go"

version:
  file: "version.go"
  pattern: 'const Version = "([0-9.]+)"'

code:
  root: "./"
  extensions: ["go"]

tests:
  pattern: "**/*_test.go"
  frameworks: [testing]
```

### Defining Subsystems

Organize your docs by subsystem:

```yaml
subsystems:
  - name: "api"
    description: "REST API layer"
    file_patterns:
      - "**/api/**"
      - "**/routes/**"
    docs:
      - "API_ARCHITECTURE.md"
    tier_default: "B"

  - name: "database"
    description: "Data persistence"
    file_patterns:
      - "**/db/**"
      - "**/models/**"
    docs:
      - "DATABASE_ARCHITECTURE.md"
      - "INVARIANTS.md#database"
    tier_default: "A"  # Critical

  - name: "auth"
    description: "Authentication & authorization"
    file_patterns:
      - "**/auth/**"
    docs:
      - "AUTH_ARCHITECTURE.md"
      - "INVARIANTS.md#security"
    tier_default: "A"  # Critical
```

### Tier A File Configuration

Define which files are critical (Tier A):

```yaml
tiering:
  tier_a:
    patterns:
      - "**/config.py"        # Configuration files
      - "**/settings.py"      # Settings
      - "**/database/*.py"    # Database code
      - "**/*Manager.py"      # Manager classes
    keywords:
      - "# CRITICAL"
      - "# SECURITY"
      - "# INVARIANT"
    min_references: 10  # Auto-tier if 10+ files import it
```

### Hook Configuration

Customize enforcement:

```yaml
hooks:
  pre_commit:
    - check: "tier_a_citation"
      enabled: true
      blocking: true  # Block commit if violated

    - check: "changelog_updated"
      enabled: true
      blocking: true  # Block if CHANGELOG not updated

    - check: "blast_radius"
      threshold: 5  # Warn if > 5 files changed
      blocking: false  # Don't block, just warn
```

---

## Document Templates

### CHANGELOG.md

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-01-04

### Added
- Initial release
- Living Documentation Framework integration

### Changed
- [What changed]

### Fixed
- [What was fixed]
```

### BUG_TRACKER.md

```markdown
# Bug Tracker

**Summary**: {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
**Total**: 0 bugs tracked, 0 fixed

## Open Bugs

### P0 - Critical (Blocks Release)
None

### P1 - High Priority
None

### P2 - Medium Priority
None

### P3 - Low Priority / Improvements
None

## Fixed Bugs

[Bugs moved here when resolved]
```

### docs/INVARIANTS.md

```markdown
# Invariants

Safety rules that must never be violated.

## 1. Database

### INV-1.1: Connection Pooling
**Rule**: Always use connection pooling, never create raw connections
**Rationale**: Prevents connection leaks and improves performance
**Example**: Use `db.get_connection()` not `psycopg2.connect()`

## 2. API

### INV-2.1: Input Validation
**Rule**: Validate all user input before processing
**Rationale**: Prevents injection attacks
**Example**: Use `validator.sanitize(input)` on all endpoints

## 3. Security

### INV-3.1: Credential Storage
**Rule**: Never commit credentials to git
**Rationale**: Prevents security breaches
**Example**: Use environment variables or secrets manager
```

### docs/CODE_DOC_MAP.md

```markdown
# Code-Doc Map

Maps code files to their documentation.

## Quick Stats
- Total Files: 0
- Mapped: 0
- Unmapped: 0
- Tier A: 0

## Tier A (Critical Files)

| File | Path | Tier | Docs | Invariants | Patterns | Tests |
|------|------|------|------|------------|----------|-------|
| `config.py` | `src/` | TIER A | CONFIG.md | INV-3.1 | - | test_config.py |

## Tier B (Important Files)

[Standard files]

## Tier C (Normal Files)

[All other mapped files]
```

---

## Verification

After setup, verify everything works:

### 1. Check Configuration

```bash
# Should print config without errors
python3 -c "
import sys
sys.path.insert(0, 'LivingDocFramework/core')
from config import get_config
c = get_config()
print(f'Project: {c.project_name}')
print(f'Language: {c.language}')
print(f'Code root: {c.code_root}')
"
```

### 2. Test Confidence Calculator

```bash
python3 LivingDocFramework/tools/calculate_confidence.py
# Should show confidence score report
```

### 3. Test Hooks

```bash
# Make a test change
echo "test" >> README.md
git add README.md

# Try to commit (hooks should run)
git commit -m "test: Verify hooks work"
```

### 4. Check Hook Installation

```bash
ls -la .git/hooks/
# Should show: pre-commit, commit-msg, post-commit

# Test pre-commit manually
.git/hooks/pre-commit
echo $?  # Should be 0 (success)
```

---

## Troubleshooting

### Hooks Not Running

**Problem**: Git commits don't trigger hooks

**Solution**:
```bash
# Check permissions
ls -la .git/hooks/pre-commit
# Should be executable (-rwxr-xr-x)

# Fix if needed
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/commit-msg
chmod +x .git/hooks/post-commit
```

### Configuration Not Found

**Problem**: Tools can't find `living-doc-config.yaml`

**Solution**:
```bash
# Check file exists in project root
ls -la living-doc-config.yaml

# Check you're in the right directory
pwd  # Should be project root (where .git is)
```

### Wrong Language Detected

**Problem**: Framework uses wrong file patterns

**Solution**:
```yaml
# Edit living-doc-config.yaml
project:
  language: "python"  # Make sure this is correct

code:
  extensions: ["py"]  # Explicitly set extensions
```

### Python Module Not Found

**Problem**: `ImportError: No module named 'config'`

**Solution**:
```bash
# Check config.py exists
ls -la LivingDocFramework/core/config.py

# Run from project root
cd /path/to/project-root
python3 LivingDocFramework/tools/calculate_confidence.py
```

---

## Next Steps

1. ✅ Framework installed and configured
2. ✅ Hooks active
3. ✅ Documentation initialized

**Now**:
1. Start documenting invariants for critical files
2. Map files in CODE_DOC_MAP.md
3. Add entries to CHANGELOG.md as you work
4. Run `/living-docs` command to check health
5. Aim for 85%+ confidence score

## Resources

- [README](README.md) - Framework overview
- [Agent Protocol](protocols/AGENT_PROTOCOL.md) - How to use with AI agents
- [Hooks Documentation](hooks/README.md) - Git hook details
- [Examples](examples/) - Sample projects
- [Tool Documentation](tools/README.md) - Available automation tools
