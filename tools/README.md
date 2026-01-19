# Living Documentation Framework - Tools

This directory contains automation tools for the Living Documentation system.

---

## Extracted Tools (Ready to Use)

> **See [TOOLS_STATUS.md](TOOLS_STATUS.md) for detailed feature-by-feature status**

### confidence_engine.py ✅ VERIFIED
Advanced confidence scoring using exponential decay formula.

```bash
python tools/confidence_engine.py
# Output: Score, penalty breakdown, and formula details
```

**Features:**
- Configurable via JSON config file
- Saturating severity penalties (first bugs matter most)
- Fix ratio bonus for high resolution rates
- Self-test included

### github_sync.py 🔧 PARTIAL
GitHub Issues ↔ local JSON synchronization.

```bash
python tools/github_sync.py import   # GitHub → local (VERIFIED)
python tools/github_sync.py export   # local → GitHub (EXPERIMENTAL)
python tools/github_sync.py sync     # Bidirectional (EXPERIMENTAL)
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

# Load configuration
config = get_config()

# Access config values
print(f"Project: {config.project_name}")
print(f"Language: {config.language}")
print(f"Code root: {config.code_root}")

# Find files
code_files = config.find_code_files()
```

---

## Tools Still to Extract

### Priority 1 - Core Tools

1. **dashboard.sh** (1,511 lines)
   - Main dashboard generator with Grafana-style charts
   - Needs: Load config, replace hardcoded paths
   - Status: ⏳ Pending extraction

2. **auto-doc-mapper.sh** (381 lines)
   - Auto-generate CODE_DOC_MAP entries
   - Needs: Language-agnostic file patterns
   - Status: ⏳ Pending extraction

### Priority 2 - Supporting Tools

3. **doc-engine.py** (334 lines)
   - Document processing engine
   - Status: ⏳ Pending extraction

4. **dashboard/generator.py** (305 lines)
   - Python dashboard builder
   - Status: ⏳ Pending extraction

5. **spawn-agent.sh** (200+ lines)
   - Agent spawning helper
   - Status: ⏳ Pending extraction

6. **track-agent.sh** (200+ lines)
   - Agent execution tracker
   - Status: ⏳ Pending extraction

### Priority 3 - Utilities

7. **living-docs-sync.sh** - Doc synchronization
8. **validate-agent-report.sh** - Report validator
9. **why-diff.sh** - Git diff analyzer
10. **dashboard-auto.py** - Dashboard automation
11. **dashboard-server.py** - Local web server

---

## Generalization Checklist

When extracting a tool, ensure:

- [ ] Replace hardcoded paths with config variables
- [ ] Replace hardcoded extensions (.cs) with `$LDF_CODE_EXT`
- [ ] Replace project-specific paths with `$LDF_CODE_ROOT`
- [ ] Replace file find commands with `ldf_find_code` / `config.find_code_files()`
- [ ] Use `$LDF_VERSION_FILE` for version extraction
- [ ] Use `$LDF_BUG_TRACKER`, `$LDF_CHANGELOG`, etc. for doc paths
- [ ] Test with multiple language profiles (Python, JS, Go)
- [ ] Document any language-specific assumptions

---

## Extraction Pattern

### Shell Script Template

```bash
#!/bin/bash
# Tool Name - Brief description
# Part of Living Documentation Framework

set -e

# Load configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../core/load-config.sh"

# Use config variables
echo "Analyzing $LDF_PROJECT_NAME ($LDF_LANGUAGE)"

# Find files using helper functions
CODE_FILES=$(ldf_find_code)
FILE_COUNT=$(echo "$CODE_FILES" | wc -l)

echo "Found $FILE_COUNT code files"
```

### Python Script Template

```python
#!/usr/bin/env python3
"""
Tool Name - Brief description
Part of Living Documentation Framework
"""

import sys
from pathlib import Path

# Add core to path for imports
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR.parent / 'core'))

from config import get_config

def main():
    config = get_config()

    print(f"Analyzing {config.project_name} ({config.language})")

    # Use config
    code_files = config.find_code_files()
    print(f"Found {len(code_files)} code files")

if __name__ == '__main__':
    main()
```

---

## Testing

After extracting each tool:

1. **Test with Python project**:
   ```bash
   # Create living-doc-config.yaml for Python
   cp LivingDocFramework/core/project-config.template.yaml living-doc-config.yaml
   # Edit to set language: python
   # Run tool
   ./LivingDocFramework/tools/tool-name.sh
   ```

2. **Test with JavaScript project**:
   ```bash
   # Edit config to set language: javascript
   # Run tool
   ./LivingDocFramework/tools/tool-name.sh
   ```

3. **Verify output**:
   - Check metrics are calculated correctly
   - Check file paths are resolved
   - Check no hardcoded extensions remain

---

## Progress

- [x] Configuration system created (config.py, load-config.sh)
- [x] **confidence_engine.py** - Advanced confidence scoring (VERIFIED)
- [x] **github_sync.py** - GitHub sync (PARTIAL - import verified)
- [ ] Dashboard generator extracted
- [ ] Auto-doc-mapper extracted
- [ ] Remaining utilities extracted

---

## Dependencies

### Required
- bash 4.0+
- Python 3.8+
- jq (for JSON processing in shell scripts)

### For github_sync.py
- GitHub CLI (`gh`) - Install with `brew install gh` or `winget install GitHub.cli`

### Optional
- yq (for YAML parsing - more robust than grep)
- Chart.js (loaded via CDN for dashboards)

---

## Next Steps

1. Extract dashboard-v3.sh with full generalization
2. Extract auto-doc-mapper.sh
3. Create integration tests
4. Document tool APIs
