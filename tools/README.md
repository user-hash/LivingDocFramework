# Living Documentation Framework - Tools

This directory contains automation tools for the Living Documentation system.

---

## Available Tools

### github_sync.py

GitHub Issues synchronization with local JSON.

```bash
python tools/github_sync.py import   # GitHub -> local
python tools/github_sync.py export   # local -> GitHub
python tools/github_sync.py sync     # Bidirectional
```

**Requires:** GitHub CLI (`gh`) installed and authenticated

---

## Configuration System

All tools use a unified configuration system:

### For Shell Scripts

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

### For Python Scripts

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

### Python Script Template

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

## Dependencies

### Required
- Bash 4.0+

### For github_sync.py
- Python 3.8+
- GitHub CLI (`gh`)

### Optional
- jq (JSON processing)
- yq (YAML parsing)
