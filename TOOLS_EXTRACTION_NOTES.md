# Tool Extraction Notes

## Critical Tools (Extract with full generalization)

### 1. calculate_confidence.py (504 lines)
**Purpose**: Calculate project confidence score with exponential decay penalties
**Generalizations needed**:
- Replace `BUG_TRACKER_FILE = PROJECT_ROOT / 'BUG_TRACKER.md'` → Use `config.bug_tracker_path`
- Replace hardcoded paths → Use config properties
- Keep scoring algorithm intact (universal)
- Status: ✅ Ready to extract

### 2. auto-doc-mapper.sh (381 lines)
**Purpose**: Auto-generate CODE_DOC_MAP entries with smart tiering
**Generalizations needed**:
- Replace `find Assets -name "*.cs"` → `ldf_find_code`
- Replace tier keywords (add language-specific from profiles)
- Replace hardcoded doc paths → Use `$LDF_CODE_DOC_MAP`
- Status: ✅ Ready to extract

### 3. dashboard-v3.sh (1511 lines)
**Purpose**: Generate Grafana-style HTML dashboard with Chart.js
**Generalizations needed**:
- Replace version extraction from BeatGridConfig.cs → Use `$LDF_VERSION_FILE` with `$LDF_VERSION_PATTERN`
- Replace `find Assets -name "*.cs"` → `ldf_find_code`
- Replace hardcoded doc paths → Use config variables
- Keep Chart.js HTML generation (universal)
- Status: ✅ Ready to extract (large file - extract core logic)

## Supporting Tools (Extract key functionality)

### 4. session-memory-pack.sh (271 lines)
**Purpose**: Create session context packages for quick loading
**Status**: Extract with config paths

### 5. spawn-agent.sh (200+ lines)
**Purpose**: Helper for spawning AI agents with protocol compliance
**Status**: Extract with config paths

### 6. track-agent.sh (200+ lines)
**Purpose**: Track agent execution and compliance
**Status**: Extract with config paths

## Utility Tools (Document approach, provide templates)

7. **doc-engine.py** - Document processing engine
8. **dashboard/generator.py** - Python dashboard builder
9. **living-docs-sync.sh** - Doc synchronization
10. **validate-agent-report.sh** - Report validator
11. **why-diff.sh** - Git diff analyzer
12. **dashboard-auto.py** - Dashboard automation
13. **dashboard-server.py** - Local web server
14. **dashboard.sh** (legacy) - Original dashboard
15. **auto-mapper.py** - Python doc mapper

## Extraction Strategy

**Approach**: Given 15 tools totaling ~6000+ lines, we'll:

1. ✅ Extract confidence calculator fully (universal algorithm)
2. ✅ Extract auto-mapper with generalization
3. ✅ Extract dashboard generator core (config-driven)
4. ✅ Extract session/agent tools
5. 📝 For remaining tools: Create README with extraction notes and reference originals

**Rationale**: The top 6 tools provide 80% of the value. Remaining tools can be extracted later or by users as needed.

## Tool Dependencies

```
calculate_confidence.py
  └─ Reads: BUG_TRACKER.md, CODE_DOC_MAP.md, history.json
  └─ Writes: Confidence score to stdout/JSON

dashboard-v3.sh
  └─ Calls: calculate_confidence.py
  └─ Reads: All doc files, history.json
  └─ Writes: .claude/dashboard/index.html, history.json

auto-doc-mapper.sh
  └─ Reads: Code files, doc files
  └─ Writes: CODE_DOC_MAP.md (new entries)

session-memory-pack.sh
  └─ Reads: Git log, doc files
  └─ Writes: .claude/session-packs/*.pack.md

spawn-agent.sh
  └─ Reads: AGENT_PROTOCOL.md
  └─ Writes: Agent prompt files

track-agent.sh
  └─ Reads: Agent logs
  └─ Writes: AGENT_ACTION_LOG.md
```

## Status

- Phase 2b Progress: Starting extraction
- Estimated completion: 6 tools extracted, 9 documented
