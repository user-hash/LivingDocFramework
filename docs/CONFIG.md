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
    - ".venv/**"
    - "node_modules/**"
    - "vendor/**"
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
    description: "REST API endpoints and handlers"
    file_patterns:
      - "**/api/**"
      - "**/views.py"
      - "**/endpoints/**"
    docs:
      - "API_ARCHITECTURE.md"
      - "INVARIANTS.md#api"
    tier_default: "B"         # Default tier for files in this subsystem

  - name: "database"
    description: "Database models and migrations"
    file_patterns:
      - "**/db/**"
      - "**/models/**"
      - "**/migrations/**"
    docs:
      - "DATABASE_ARCHITECTURE.md"
      - "INVARIANTS.md#database"
    tier_default: "A"         # Critical subsystem

  - name: "auth"
    description: "Authentication and authorization"
    file_patterns:
      - "**/auth/**"
      - "**/authentication/**"
    docs:
      - "AUTH_ARCHITECTURE.md"
      - "INVARIANTS.md#security"
    tier_default: "A"         # Security is critical
```

### Subsystem Options

| Field | Description | Required |
|-------|-------------|----------|
| `name` | Subsystem identifier | Yes |
| `description` | Human-readable description | No |
| `file_patterns` | Glob patterns for files | Yes |
| `docs` | Related documentation files | No |
| `tier_default` | Default tier (A, B, C) | No |

## Tiering Section

Configure automatic file classification.

```yaml
tiering:
  tier_a:
    # Files matching these patterns are CRITICAL
    patterns:
      - "**/config.py"
      - "**/settings.py"
      - "**/database/*.py"
      - "**/*Manager.py"
    # Files containing these keywords are CRITICAL
    keywords:
      - "# CRITICAL"
      - "# INVARIANT"
      - "# SECURITY"
    # Auto-tier to A if N+ files import it
    min_references: 10

  tier_b:
    patterns:
      - "**/api/**/*.py"
      - "**/services/**/*.py"
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
  # Tier A files must cite invariants before editing
  tier_a_citation_required: true

  # CHANGELOG must be updated on code changes
  changelog_required: true

  # Maximum age before docs are "stale"
  staleness_threshold: "7d"    # 7 days

  # Auto-add new files to CODE_DOC_MAP
  auto_map_new_files: true
```

## Hooks Section

Configure git hook behavior.

```yaml
hooks:
  pre_commit:
    - check: "tier_a_citation"
      enabled: true
      blocking: true          # Block commit if violated

    - check: "changelog_updated"
      enabled: true
      blocking: true

    - check: "blast_radius"
      enabled: true
      blocking: false         # Just warn
      threshold: 5            # Warn if > 5 files changed

  post_commit:
    - action: "update_dashboard"
      enabled: true

    - action: "calculate_confidence"
      enabled: true
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
  # Files agents must read before changes
  required_reading:
    - "CODE_DOC_MAP.md"
    - "docs/INVARIANTS.md"
    - "AGENT_PROTOCOL.md"

  # Files agents must update per action type
  required_updates:
    on_bug_fix:
      - "BUG_TRACKER.md"
      - "BUG_PATTERNS.md"
      - "CHANGELOG.md"

    on_new_feature:
      - "GOLDEN_PATHS.md"
      - "CHANGELOG.md"
      - "CODE_DOC_MAP.md"

    on_tier_a_edit:
      - "docs/INVARIANTS.md"
```

## Confidence Section

Confidence scoring weights.

```yaml
confidence:
  weights:
    documentation_coverage: 0.30   # 30%
    pattern_prevention: 0.25       # 25%
    invariant_compliance: 0.25     # 25%
    freshness: 0.15                # 15%
    test_coverage: 0.05            # 5%

  thresholds:
    excellent: 90    # 90%+ = excellent
    good: 75         # 75-89% = good
    acceptable: 60   # 60-74% = acceptable
    # Note: scores below 60% are considered "needs improvement"
```

## Dashboard Section

Dashboard output configuration.

```yaml
dashboard:
  output_dir: ".claude/dashboard"
  history_retention: "all"     # or "90d", "1y", etc.

  custom_metrics:
    - name: "test_coverage"
      source_file: "coverage.json"
      pattern: '"coverage":\s*([0-9.]+)'
      dashboard: true
```

## Integrations Section (Optional)

External service integrations.

```yaml
integrations:
  github:
    enabled: false
    # repo: "username/repo"
    # auto_link_issues: true

  jira:
    enabled: false
    # server: "https://yourcompany.atlassian.net"
    # project_key: "PROJ"

  slack:
    enabled: false
    # webhook_url: "https://hooks.slack.com/services/..."
    # notify_on_stale: true
```

---

## Language Profiles

Pre-configured defaults are loaded from `core/languages/*.yaml`:

| Language | Extensions | Version File | Test Pattern |
|----------|-----------|--------------|--------------|
| Python | .py | `__init__.py` | `test_*.py` |
| JavaScript | .js, .ts, .jsx, .tsx | `package.json` | `*.test.js` |
| Go | .go | `version.go` | `*_test.go` |
| Rust | .rs | `Cargo.toml` | Standard |
| C# | .cs | `Config.cs` | `*Tests.cs` |

Language profiles provide defaults. Your `living-doc-config.yaml` overrides them.

---

## Minimal Example

The simplest working config:

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

See `core/project-config.template.yaml` for a comprehensive example with all options documented.
