# Tool Extraction Guide

This guide explains how to extract the remaining tools from the Nebulae project.

## ✅ Extracted Tools

### 1. calculate_confidence.py (COMPLETE)
- **Source**: `.claude/tools/calculate_confidence.py` (504 lines)
- **Destination**: `tools/calculate_confidence.py` (370 lines generalized)
- **Generalizations applied**:
  - Uses `config.py` for all file paths
  - Replaces `.cs` extension matching with `config.code_extensions`
  - Uses `config.find_code_files()` instead of hardcoded path/extension patterns
  - Algorithm unchanged (universal)

## 📋 Remaining Tools to Extract

### Priority 1 - Dashboard Tools

#### dashboard-v3.sh (1,511 lines)
**Extraction Strategy**:
```bash
# Source configuration
source "$(dirname "$0")/../core/load-config.sh"

# Replace hardcoded paths
- find [code_root] -name "*.[ext]" → ldf_find_code
- Version file extraction → use $LDF_VERSION_FILE + $LDF_VERSION_PATTERN
- CHANGELOG.md → $LDF_CHANGELOG
- BUG_PATTERNS.md → $LDF_BUG_PATTERNS
- BUG_TRACKER.md → $LDF_BUG_TRACKER
- CODE_DOC_MAP.md → $LDF_CODE_DOC_MAP

# Keep intact
- Chart.js HTML generation (universal)
- Historical tracking logic
- Graph rendering code
```

**Key sections to generalize**:
- Lines 31-47: Data collection (use config variables)
- Lines 119-147: File counting (use `ldf_find_code`)
- Lines 169-183: Doc line counts (use config paths)
- Lines 250-1400: HTML generation (mostly universal, just update titles)

#### auto-doc-mapper.sh (381 lines)
**Extraction Strategy**:
```bash
# Generalize tier detection
TIER_A_KEYWORDS=(
    "${LDF_LANGUAGE_TIER_A_KEYWORDS[@]}"  # From language profile
    "CRITICAL" "INVARIANT" "SECURITY"      # Universal
)

# File finding
find "$LDF_CODE_ROOT" -name "*.$LDF_CODE_EXT"  # Uses config, not hardcoded

# Doc path references
echo "Updating $LDF_CODE_DOC_MAP"  # Not hardcoded CODE_DOC_MAP.md
```

### Priority 2 - Agent Tools

#### spawn-agent.sh
**Purpose**: Helper for spawning AI agents with protocol compliance
**Generalizations**:
- Use `$LDF_CLAUDE_MD` instead of hardcoded `CLAUDE.md`
- Use `$LDF_INVARIANTS` instead of `INVARIANTS.md`
- Load agent protocol from config

#### track-agent.sh
**Purpose**: Track agent execution and compliance
**Generalizations**:
- Use config paths for all doc references
- Make report format configurable

### Priority 3 - Session Tools

#### session-memory-pack.sh
**Purpose**: Create session context packages
**Generalizations**:
```bash
# Pack relevant files
- $LDF_CHANGELOG
- $LDF_BUG_TRACKER
- $LDF_CLAUDE_MD (or equivalent project guide)
- Recent git commits
```

### Priority 4 - Utility Tools

#### why-diff.sh
**Purpose**: Git diff analyzer
**Minimal changes**: Uses git commands (mostly language-agnostic)

#### validate-agent-report.sh
**Purpose**: Validate agent compliance reports
**Generalizations**: Use config for doc paths

#### living-docs-sync.sh
**Purpose**: Sync documentation across files
**Generalizations**: Use all config paths

#### doc-engine.py
**Purpose**: Document processing engine
**Generalizations**: Use `config.py` for all paths

#### dashboard/generator.py
**Purpose**: Python-based dashboard builder
**Generalizations**: Use `config.py`, similar to dashboard-v3.sh

#### dashboard-server.py
**Purpose**: Local web server for dashboard
**Minimal changes**: HTTP server logic is universal

#### dashboard-auto.py
**Purpose**: Automated dashboard generation
**Generalizations**: Use `config.py`

#### auto-mapper.py
**Purpose**: Python version of auto-doc-mapper
**Generalizations**: Use `config.py`, similar to .sh version

#### dashboard.sh (legacy)
**Status**: Can be deprecated in favor of dashboard-v3.sh

## Extraction Template

### For Shell Scripts

```bash
#!/bin/bash
# Tool Name - Purpose
# Part of Living Documentation Framework

set -e

# Load configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../core/load-config.sh"

echo "Processing $LDF_PROJECT_NAME ($LDF_LANGUAGE)"

# Use configuration variables
CODE_FILES=$(ldf_find_code)
FILE_COUNT=$(echo "$CODE_FILES" | wc -l)

echo "Found $FILE_COUNT files in $LDF_CODE_ROOT"

# Read documents using config paths
if [ -f "$LDF_CHANGELOG" ]; then
    echo "Reading changelog..."
fi

# [Tool-specific logic here]
```

### For Python Scripts

```python
#!/usr/bin/env python3
"""
Tool Name - Purpose
Part of Living Documentation Framework
"""

import sys
from pathlib import Path

# Load config
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR.parent / 'core'))
from config import get_config

def main():
    config = get_config()

    print(f"Processing {config.project_name} ({config.language})")

    # Use config
    code_files = config.find_code_files()
    print(f"Found {len(code_files)} files")

    # Read documents
    if config.changelog_path.exists():
        print("Reading changelog...")

    # [Tool-specific logic here]

if __name__ == '__main__':
    main()
```

## Quick Reference: Replacements

| Hardcoded (Original) | Generalized (Framework) |
|----------------------|-------------------------|
| `find [root] -name "*.[ext]"` | `ldf_find_code` (shell) or `config.find_code_files()` (Python) |
| `[ProjectConfig].cs` | `$LDF_VERSION_FILE` or `config.version_file` |
| `CHANGELOG.md` | `$LDF_CHANGELOG` or `config.changelog_path` |
| `BUG_PATTERNS.md` | `$LDF_BUG_PATTERNS` or `config.bug_patterns_path` |
| `BUG_TRACKER.md` | `$LDF_BUG_TRACKER` or `config.bug_tracker_path` |
| `CODE_DOC_MAP.md` | `$LDF_CODE_DOC_MAP` or `config.code_doc_map_path` |
| `INVARIANTS.md` | `$LDF_INVARIANTS` or `config.invariants_path` |
| `CLAUDE.md` | `$LDF_CLAUDE_MD` or `config.claude_md_path` |
| `.cs` extension | `$LDF_CODE_EXT` or `config.code_extensions` |
| `Assets/_Project/Scripts` | `$LDF_CODE_ROOT` or `config.code_root` |

## Testing Extracted Tools

After extracting each tool:

1. **Create test project**:
   ```bash
   mkdir test-python-project
   cd test-python-project
   cp path/to/LivingDocFramework/core/project-config.template.yaml living-doc-config.yaml
   # Edit to set language: python
   ```

2. **Create minimal docs**:
   ```bash
   touch BUG_TRACKER.md CODE_DOC_MAP.md CHANGELOG.md
   echo '{"history":[]}' > .claude/dashboard/history.json
   ```

3. **Run tool**:
   ```bash
   ../LivingDocFramework/tools/calculate_confidence.py
   ```

4. **Verify**:
   - No errors about missing files
   - Uses configured paths
   - Output makes sense for the language

## Status

- ✅ calculate_confidence.py - Extracted and generalized
- ⏳ dashboard-v3.sh - Ready to extract (large file)
- ⏳ auto-doc-mapper.sh - Ready to extract
- ⏳ Remaining 12 tools - Documented approach

**Next step**: Extract dashboard-v3.sh or move to Phase 3 (hooks) and circle back.
