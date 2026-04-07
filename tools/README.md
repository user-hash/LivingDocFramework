# Tools

Automation utilities for the Living Documentation system.

## Configuration System

All tools use a unified configuration system via `core/load-config.sh`:

```bash
source "$(dirname "$0")/../core/load-config.sh"

echo "Project: $LDF_PROJECT_NAME"
echo "Language: $LDF_LANGUAGE"
echo "Code root: $LDF_CODE_ROOT"
```

## Creating New Tools

```bash
#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../core/load-config.sh"

echo "Analyzing $LDF_PROJECT_NAME ($LDF_LANGUAGE)"
```

## Dependencies

**Required:** Bash 4.0+

**Optional:** yq (robust YAML parsing), jq (JSON processing)
