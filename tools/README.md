# Living Documentation Framework - Tools

This directory contains automation tools for the Living Documentation system.

---

## Available Tools

### github_sync.py (EXPERIMENTAL)

> **Status: EXPERIMENTAL** - Import feature works, export/sync features are untested.

GitHub Issues synchronization with local JSON.

```bash
python tools/github_sync.py import   # GitHub -> local (WORKING)
python tools/github_sync.py export   # local -> GitHub (EXPERIMENTAL)
python tools/github_sync.py sync     # Bidirectional (EXPERIMENTAL)
```

**Requires:** GitHub CLI (`gh`) installed and authenticated

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

### For Python Scripts (EXPERIMENTAL)

> **Note:** Python config module (`core/config.py`) is experimental.

```python
#!/usr/bin/env python3
from LivingDocFramework.core.config import get_config

config = get_config()
print(f"Project: {config.project_name}")
code_files = config.find_code_files()
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

### Python Script Template (EXPERIMENTAL)

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR.parent / 'core'))

from config import get_config

def main():
    config = get_config()
    print(f"Found {len(config.find_code_files())} code files")

if __name__ == '__main__':
    main()
```

---

## Feature Status

| Feature | Status | Notes |
|---------|--------|-------|
| Shell config loader | PROVEN | Used in production |
| Pre-commit hooks | PROVEN | Used in production |
| Version checking | PROVEN | Used in production |
| GitHub sync import | WORKING | Tested with GitHub CLI |
| GitHub sync export | EXPERIMENTAL | Needs testing |
| Python config module | EXPERIMENTAL | Needs implementation |

---

## Dependencies

### Required
- Bash 4.0+

### For github_sync.py
- Python 3.8+
- GitHub CLI (`gh`)

### Optional
- jq (JSON processing)
- yq (YAML parsing)
