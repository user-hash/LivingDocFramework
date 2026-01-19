# Integration Guide

Complete guide for integrating the Living Documentation Framework into existing codebases.

## Prerequisites

- **Git**: Version control system
- **Bash** 4.0+ (for shell tools; use Git Bash on Windows)
- **Python** 3.8+ (for confidence scoring)
- **jq** (optional, for JSON processing)

## Step 1: Add Framework

**Option A: Git Submodule** (recommended)
```bash
cd your-project/
git submodule add https://github.com/user-hash/LivingDocFramework.git
git submodule update --init --recursive
```

**Option B: Copy/Vendor**
```bash
cd your-project/
cp -r /path/to/LivingDocFramework .
```

## Step 2: Configure for YOUR Project

```bash
cp LivingDocFramework/core/project-config.template.yaml living-doc-config.yaml
```

Edit `living-doc-config.yaml` for your project:

```yaml
project:
  name: "YourProject"
  language: "python"        # python | javascript | go | rust | csharp
  main_branch: "main"

code:
  root: "src/"              # YOUR code root
  extensions: ["py"]        # YOUR file extensions
  exclude:
    - "**/__pycache__/**"
    - "**/venv/**"

# Define YOUR subsystems
subsystems:
  - name: "api"
    file_patterns: ["**/api/**", "**/views.py"]
    docs: ["API_ARCHITECTURE.md"]
    tier_default: "B"

  - name: "database"
    file_patterns: ["**/models/**", "**/db/**"]
    docs: ["DATABASE_ARCHITECTURE.md"]
    tier_default: "A"       # Critical = blocking enforcement

# Mark YOUR critical files
tiering:
  tier_a:
    patterns:
      - "**/config.py"
      - "**/settings.py"
    keywords: ["# CRITICAL", "# SECURITY"]
    min_references: 10      # Auto-tier if 10+ imports
```

See [CONFIG.md](CONFIG.md) for all options.

## Step 3: Create Documentation Structure

```bash
# Create directories
mkdir -p docs

# Create core files
touch CODE_DOC_MAP.md BUG_PATTERNS.md CHANGELOG.md
touch docs/INVARIANTS.md docs/GOLDEN_PATHS.md docs/DECISIONS.md

# Optional: copy templates
cp LivingDocFramework/core/templates/bug-patterns.template.md BUG_PATTERNS.md
```

### What Each File Is For

| File | Purpose | When to Update |
|------|---------|----------------|
| `CODE_DOC_MAP.md` | Maps files to their docs | New file created |
| `BUG_PATTERNS.md` | Documented bugs with prevention | Bug fixed |
| `INVARIANTS.md` | Safety rules | Critical file changed |
| `GOLDEN_PATHS.md` | Best practices | Pattern established |
| `CHANGELOG.md` | Release history | Every release |

## Step 4: Install Git Hooks

```bash
./LivingDocFramework/hooks/install.sh
```

**Windows users**: Run from Git Bash, or manually copy hooks:
```bash
cp LivingDocFramework/hooks/pre-commit .git/hooks/
cp LivingDocFramework/hooks/commit-msg .git/hooks/
cp LivingDocFramework/hooks/post-commit .git/hooks/
chmod +x .git/hooks/*
```

### What Hooks Enforce

| Hook | Check | Blocking |
|------|-------|----------|
| pre-commit | CHANGELOG updated | Yes (configurable) |
| pre-commit | Tier A files cite invariants | Yes (configurable) |
| pre-commit | Blast radius warning | No (just warns) |
| commit-msg | Message format | No |

## Step 5: Verify Installation

```bash
# Check confidence score
python3 LivingDocFramework/tools/calculate_confidence.py

# Make a test commit
git add .
git commit -m "feat: Add Living Documentation Framework"
# Hooks should run automatically
```

### Troubleshooting

**Hooks not running?**
```bash
ls -la .git/hooks/pre-commit  # Check exists
chmod +x .git/hooks/*         # Fix permissions
```

**Config not found?**
```bash
ls living-doc-config.yaml     # Must be in project root
pwd                           # Verify you're in project root
```

---

## Scaling Your Documentation

### Small Project (< 10 files)

**Start with:**
- `CODE_DOC_MAP.md` — map your files
- `BUG_PATTERNS.md` — document bugs as you fix them
- Pre-commit hook for CHANGELOG enforcement

**Skip:**
- Subsystems (not needed yet)
- Tier A configuration (everything is important at this scale)
- Confidence scoring (too few metrics to matter)

### Medium Project (10-50 files)

**Add:**
- Subsystems in config (group related files)
- `INVARIANTS.md` for critical rules
- Tier A marking for critical files
- Confidence scoring to track health

**Config example:**
```yaml
subsystems:
  - name: "api"
    file_patterns: ["**/api/**"]
    tier_default: "B"
  - name: "database"
    file_patterns: ["**/db/**"]
    tier_default: "A"

tiering:
  tier_a:
    patterns: ["**/config.py", "**/auth/**"]
```

### Large Project (50+ files)

**Add:**
- Per-subsystem architecture docs (e.g., `API_ARCHITECTURE.md`)
- Full tiering configuration with keywords
- `GOLDEN_PATHS.md` for established patterns
- Regular confidence scoring
- `DECISIONS.md` for ADRs

**Consider:**
- Multiple invariant sections by subsystem
- Team-specific doc ownership
- CI integration for confidence checks

---

## Language-Specific Examples

### Python
```yaml
project:
  language: "python"
code:
  root: "src/"
  extensions: ["py"]
version:
  file: "__init__.py"
  pattern: '__version__\s*=\s*"([0-9.]+)"'
tests:
  pattern: "**/test_*.py"
  frameworks: [pytest]
```

### JavaScript/TypeScript
```yaml
project:
  language: "javascript"
code:
  root: "src/"
  extensions: ["js", "ts", "jsx", "tsx"]
version:
  file: "package.json"
  pattern: '"version":\s*"([0-9.]+)"'
tests:
  pattern: "**/*.test.{js,ts}"
  frameworks: [jest]
```

### Go
```yaml
project:
  language: "go"
code:
  root: "./"
  extensions: ["go"]
version:
  file: "version.go"
  pattern: 'const Version = "([0-9.]+)"'
tests:
  pattern: "**/*_test.go"
```

### C#
```yaml
project:
  language: "csharp"
code:
  root: "src/"
  extensions: ["cs"]
version:
  file: "Config.cs"
  pattern: 'public const string VERSION = "([0-9.]+)"'
```

---

## Next Steps

After integration:

1. Map your existing files in `CODE_DOC_MAP.md`
2. Document any known invariants
3. Fix a bug? Add it to `BUG_PATTERNS.md`
4. Run confidence scoring weekly
5. Aim for 85%+ confidence score

## Resources

- [README](../README.md) — Framework overview
- [CONFIG.md](CONFIG.md) — Full configuration reference
- [Git Hooks](../hooks/README.md) — Hook customization
- [Agent Protocol](../protocols/AGENT_PROTOCOL.md) — AI agent usage
- [Examples](../examples/) — Sample projects
