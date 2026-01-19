# Configuration Reference

Complete reference for `living-doc-config.yaml` options.

## Project Section

Basic project identification.

```yaml
project:
  name: "MyProject"           # Your project name
  language: "python"          # python | javascript | go | rust | csharp
  main_branch: "main"         # or "master"
```

## Version Section

Where is your project version defined?

```yaml
version:
  file: "__init__.py"         # File containing version
  pattern: '__version__\s*=\s*"([0-9.]+)"'  # Regex to extract
```

### Language-Specific Examples

| Language | File | Pattern |
|----------|------|---------|
| Python | `__init__.py` | `'__version__\s*=\s*"([0-9.]+)"'` |
| JavaScript | `package.json` | `'"version":\s*"([0-9.]+)"'` |
| Go | `version.go` | `'const Version = "([0-9.]+)"'` |
| Rust | `Cargo.toml` | `'version\s*=\s*"([0-9.]+)"'` |
| C# | `Config.cs` | `'public const string VERSION = "([0-9.]+)"'` |

## Code Section

Where your source code lives.

```yaml
code:
  root: "src/"                # Root directory for source code
  extensions: ["py"]          # File extensions to track
  exclude:                    # Patterns to ignore
    - "__pycache__/**"
    - "venv/**"
    - "node_modules/**"
    - "build/**"
    - "dist/**"
```

## Tests Section

Test file configuration.

```yaml
tests:
  pattern: "**/test_*.py"     # Glob pattern for test files
  extensions: ["py"]          # Test file extensions
  frameworks:                 # Test frameworks used
    - pytest
```

## Subsystems Section

Organize your project into logical subsystems.

```yaml
subsystems:
  - name: "api"
    description: "REST API endpoints"
    file_patterns:
      - "**/api/**"
      - "**/views.py"
    docs:
      - "API_ARCHITECTURE.md"
    tier_default: "B"

  - name: "database"
    description: "Database models"
    file_patterns:
      - "**/db/**"
      - "**/models/**"
    docs:
      - "DATABASE_ARCHITECTURE.md"
    tier_default: "A"         # Critical subsystem
```

### Subsystem Options

| Field | Description | Required |
|-------|-------------|----------|
| `name` | Subsystem identifier | Yes |
| `description` | Human-readable description | No |
| `file_patterns` | Glob patterns for files | Yes |
| `docs` | Related documentation files | No |
| `tier_default` | Default tier (A, B, C) | No |

## Per-Subsystem Documentation (Doc-Sets)

For scaling to large projects, organize documentation by subsystem using **doc-sets**.

### What is a Doc-Set?

A **doc-set** is any folder under `docs/` that contains a `CODE_DOC_MAP.md` file.

```
docs/
├── multiplayer/              # This IS a doc-set (has CODE_DOC_MAP.md)
│   ├── CODE_DOC_MAP.md       # <- Marker file
│   ├── INVARIANTS.md
│   └── BUG_PATTERNS.md
├── audio/                    # This IS a doc-set
│   ├── CODE_DOC_MAP.md       # <- Marker file
│   └── INVARIANTS.md
└── reference/                # This is NOT a doc-set (no CODE_DOC_MAP.md)
    └── glossary.md
```

### How Tier-A Enforcement Works

1. You edit a code file
2. Pre-commit hook searches all `docs/*/CODE_DOC_MAP.md` files
3. If file is listed as Tier A in a map, hook requires sibling `INVARIANTS.md` update
4. No pattern matching, no config complexity

### Creating a Doc-Set

```bash
# Create multiplayer doc-set
mkdir -p docs/multiplayer
touch docs/multiplayer/CODE_DOC_MAP.md
touch docs/multiplayer/INVARIANTS.md
touch docs/multiplayer/BUG_PATTERNS.md
```

Then add files to the map with repo-relative paths:

```markdown
## Tier A (Critical)
| `src/Multiplayer/SyncManager.cs` | Core sync | INV-MP-001 |
```

### Path Format Rules

All CODE_DOC_MAP entries **must** use repo-relative paths:

```markdown
# CORRECT - repo-relative path
| `src/Multiplayer/SyncManager.cs` | TIER A | Core sync |

# WRONG - basename only (ambiguous)
| `SyncManager.cs` | TIER A | Core sync |
```

### No Config Required

Unlike pattern-based approaches, doc-sets require **zero YAML configuration**.
The folder structure IS the configuration.

### Backward Compatibility

Root-level `CODE_DOC_MAP.md` is supported but deprecated. It will emit a warning:
```
Warning: Using deprecated root CODE_DOC_MAP.md
  -> Migrate to docs/<subsystem>/CODE_DOC_MAP.md
```

## Tiering Section

Configure automatic file classification.

```yaml
tiering:
  tier_a:
    patterns:
      - "**/config.py"
      - "**/settings.py"
    keywords:
      - "# CRITICAL"
      - "# SECURITY"
    min_references: 10

  tier_b:
    patterns:
      - "**/api/**/*.py"
    min_references: 5
```

### Tier Meanings

| Tier | Name | Enforcement |
|------|------|-------------|
| A | Critical | Blocking (must cite invariants) |
| B | Important | Warning |
| C | Normal | No enforcement |

## Documentation Section

Documentation enforcement rules.

```yaml
documentation:
  tier_a_citation_required: true
  changelog_required: true
  staleness_threshold: "7d"
  auto_map_new_files: true
```

## Hooks Section

Configure git hook behavior.

```yaml
hooks:
  pre_commit:
    - check: "tier_a_citation"
      enabled: true
      blocking: true

    - check: "changelog_updated"
      enabled: true
      blocking: true

    - check: "blast_radius"
      enabled: true
      blocking: false
      threshold: 5
```

### Available Checks

| Check | Description | Blocking? |
|-------|-------------|-----------|
| `tier_a_citation` | Tier A files must cite invariants | Configurable |
| `changelog_updated` | CHANGELOG must be updated | Configurable |
| `blast_radius` | Warn on large changes | Usually no |

## Agents Section

AI agent configuration.

```yaml
agents:
  required_reading:
    - "CODE_DOC_MAP.md"
    - "docs/INVARIANTS.md"
    - "AGENT_PROTOCOL.md"

  required_updates:
    on_bug_fix:
      - "BUG_PATTERNS.md"
      - "CHANGELOG.md"

    on_new_feature:
      - "GOLDEN_PATHS.md"
      - "CHANGELOG.md"
      - "CODE_DOC_MAP.md"

    on_tier_a_edit:
      - "docs/INVARIANTS.md"
```

---

## Language Profiles

Pre-configured defaults from `core/languages/*.yaml`:

| Language | Extensions | Version File | Test Pattern |
|----------|-----------|--------------|--------------|
| Python | .py | `__init__.py` | `test_*.py` |
| JavaScript | .js, .ts | `package.json` | `*.test.js` |
| Go | .go | `version.go` | `*_test.go` |
| Rust | .rs | `Cargo.toml` | Standard |
| C# | .cs | `Config.cs` | `*Tests.cs` |

---

## Minimal Example

```yaml
project:
  name: "MyProject"
  language: "python"
  main_branch: "main"

code:
  root: "src/"
  extensions: ["py"]
```

## Full Example

See `core/project-config.template.yaml` for all options.
