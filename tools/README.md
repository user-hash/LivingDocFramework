# Living Documentation Framework - Tools

This directory contains automation tools for the Living Documentation system.

---

## Configuration System

All tools use a unified configuration system:

### For Shell Scripts (PROVEN)

```bash
# Source the configuration loader
source "$(dirname "$0")/../core/load-config.sh"

# Use environment variables
echo "Project: $LDF_PROJECT_NAME"
echo "Language: $LDF_LANGUAGE"
echo "Code root: $LDF_CODE_ROOT"

# Find code files
ldf_find_code "$LDF_CODE_ROOT" | wc -l
```

---

## Creating New Tools

### Shell Script Template

```bash
#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../core/load-config.sh"

echo "Analyzing $LDF_PROJECT_NAME ($LDF_LANGUAGE)"
```

---

## Feature Status

| Feature | Status | Notes |
|---------|--------|-------|
| Shell config loader | PROVEN | Used in production |
| Pre-commit hooks | PROVEN | Used in production |
| Version checking | PROVEN | Used in production |

---

## Dependencies

### Required
- Bash 4.0+

### Optional
- jq (JSON processing)
- yq (YAML parsing)
