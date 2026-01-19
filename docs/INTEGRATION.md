# Integration Guide

Complete guide for integrating the Living Documentation Framework into existing codebases.

## Prerequisites

- **Git**: Version control system
- **Bash** 4.0+ (for hooks; use Git Bash on Windows)

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

subsystems:
  - name: "api"
    file_patterns: ["**/api/**", "**/views.py"]
    tier_default: "B"

  - name: "database"
    file_patterns: ["**/models/**", "**/db/**"]
    tier_default: "A"       # Critical = blocking enforcement

tiering:
  tier_a:
    patterns:
      - "**/config.py"
      - "**/settings.py"
    keywords: ["# CRITICAL", "# SECURITY"]
```

See [CONFIG.md](CONFIG.md) for all options.

## Step 3: Create Documentation Structure

```bash
mkdir -p docs
touch CODE_DOC_MAP.md BUG_PATTERNS.md CHANGELOG.md
touch docs/INVARIANTS.md docs/GOLDEN_PATHS.md

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
```

---

## Scaling: Small to Large Projects

### Small Project (< 20 files)

Single root-level `CODE_DOC_MAP.md`:

```
project/
├── CODE_DOC_MAP.md       # All files mapped here
├── CHANGELOG.md
├── BUG_PATTERNS.md
└── docs/
    └── INVARIANTS.md     # All invariants
```

**What you need:**
- Map your files in `CODE_DOC_MAP.md`
- Document bugs in `BUG_PATTERNS.md`
- Pre-commit hook for CHANGELOG enforcement

### Medium Project (20-100 files)

Start organizing by subsystem with **doc-sets**:

```
project/
├── CHANGELOG.md
└── docs/
    ├── api/
    │   ├── CODE_DOC_MAP.md    # <- This makes it a doc-set
    │   └── INVARIANTS.md
    └── database/
        ├── CODE_DOC_MAP.md    # <- Another doc-set
        └── INVARIANTS.md
```

**What you need:**
- Create doc-sets for major subsystems
- Each doc-set has its own `CODE_DOC_MAP.md` and `INVARIANTS.md`
- Hook automatically finds all doc-sets

### Large Project (100+ files)

Full doc-set structure:

```
project/
├── CHANGELOG.md
└── docs/
    ├── multiplayer/
    │   ├── CODE_DOC_MAP.md
    │   ├── INVARIANTS.md
    │   ├── BUG_PATTERNS.md
    │   ├── GOLDEN_PATHS.md
    │   └── DECISIONS/
    │       └── ADR-MP-001.md
    ├── audio/
    │   ├── CODE_DOC_MAP.md
    │   └── INVARIANTS.md
    └── global/
        ├── CODE_DOC_MAP.md   # Cross-cutting files
        └── INVARIANTS.md
```

**Key benefits:**
- Zero config - folder structure IS the configuration
- Each subsystem team owns their doc-set
- Tier A enforcement is automatic per doc-set

### Creating a Doc-Set

```bash
# Create multiplayer doc-set
mkdir -p docs/multiplayer
touch docs/multiplayer/CODE_DOC_MAP.md
touch docs/multiplayer/INVARIANTS.md

# Add Tier A files to the map
cat >> docs/multiplayer/CODE_DOC_MAP.md << 'EOF'
## Tier A (Critical)
| `src/Multiplayer/SyncManager.cs` | Core sync | INV-MP-001 |
EOF
```

**Rule:** A folder containing `CODE_DOC_MAP.md` IS a doc-set. No config needed.

See [CONFIG.md#per-subsystem-documentation-doc-sets](CONFIG.md#per-subsystem-documentation-doc-sets) for details.

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
```

### Rust
```yaml
project:
  language: "rust"
code:
  root: "src/"
  extensions: ["rs"]
version:
  file: "Cargo.toml"
  pattern: 'version\s*=\s*"([0-9.]+)"'
```

### C#
```yaml
project:
  language: "csharp"
code:
  root: "src/"
  extensions: ["cs"]
```

---

## Resources

- [README](../README.md) — Framework overview
- [CONFIG.md](CONFIG.md) — Full configuration reference
- [Git Hooks](../hooks/README.md) — Hook customization
- [Agent Protocol](../protocols/AGENT_PROTOCOL.md) — AI agent usage
