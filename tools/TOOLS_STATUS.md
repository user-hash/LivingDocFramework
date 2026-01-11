# Tools Status - What Works vs What Doesn't

> **Last Updated:** 2026-01-11
> **Framework Version:** 1.0.1

This document provides honest status information about each tool in the Living Documentation Framework.

---

## Status Legend

| Status | Meaning |
|--------|---------|
| ✅ **VERIFIED** | Tested in production, works reliably |
| ⚠️ **EXPERIMENTAL** | Works in testing, not fully production-proven |
| 🔧 **PARTIAL** | Core features work, some features untested |
| ❌ **BROKEN** | Known issues, do not use |

---

## Core Tools

### confidence_engine.py
**Status:** ✅ **VERIFIED**

Calculates project confidence score using exponential decay formula.

| Feature | Status | Notes |
|---------|--------|-------|
| Score calculation | ✅ VERIFIED | Tested with 90+ bugs |
| Config loading | ✅ VERIFIED | Falls back to defaults if no config |
| Penalty breakdown | ✅ VERIFIED | All components calculated correctly |
| Subsystem scores | ⚠️ EXPERIMENTAL | Works but less tested |

**Dependencies:** None (standalone)

---

### github_sync.py
**Status:** 🔧 **PARTIAL**

Syncs bugs between local JSON and GitHub Issues.

| Feature | Status | Notes |
|---------|--------|-------|
| Import from GitHub | ✅ VERIFIED | Tested with 300+ issues |
| Export to GitHub | ⚠️ EXPERIMENTAL | Works but less tested |
| Bidirectional sync | ⚠️ EXPERIMENTAL | Use with caution |
| Create labels | ✅ VERIFIED | Creates standard label set |
| False positive detection | ✅ VERIFIED | Detects from keywords |

**Dependencies:** GitHub CLI (`gh`) must be installed and authenticated

**Known Issues:**
- Windows encoding issue with Unicode checkmarks in output (cosmetic only)

---

## DevMemory Module

### devmemory/__init__.py
**Status:** ✅ **VERIFIED**

Package initialization and exports.

---

### devmemory/session_memory.py
**Status:** ✅ **VERIFIED**

Session state persistence across Claude Code sessions.

| Feature | Status | Notes |
|---------|--------|-------|
| Session start | ✅ VERIFIED | Creates session with unique ID |
| Session resume | ✅ VERIFIED | Restores previous session state |
| Version tracking | ✅ VERIFIED | Tracks version at session start/end |
| Summary generation | ✅ VERIFIED | Produces readable summaries |
| File modification tracking | ⚠️ EXPERIMENTAL | Works but less tested |

**Dependencies:** None

---

### devmemory/event_stream.py
**Status:** 🔧 **PARTIAL**

Cognitive event logging system.

| Feature | Status | Notes |
|---------|--------|-------|
| emit_event() | ✅ VERIFIED | Core event emission works |
| emit_code_edit() | ⚠️ EXPERIMENTAL | Works in testing |
| emit_confidence_snapshot() | ⚠️ EXPERIMENTAL | Works in testing |
| emit_version_bump() | ✅ VERIFIED | Tested |
| emit_agent_launched/completed() | ⚠️ EXPERIMENTAL | Works in testing |
| query_events() | ⚠️ EXPERIMENTAL | Basic queries work |
| Regression tracking | ⚠️ EXPERIMENTAL | New feature, less tested |

**Dependencies:** None

---

### devmemory/confidence_tracker.py
**Status:** ⚠️ **EXPERIMENTAL**

Tracks confidence score changes over time.

| Feature | Status | Notes |
|---------|--------|-------|
| track_confidence() | ⚠️ EXPERIMENTAL | Works in testing |
| Trajectory analysis | ⚠️ EXPERIMENTAL | Basic functionality |
| Two-layer scoring | ⚠️ EXPERIMENTAL | Advanced feature |

**Dependencies:** event_stream.py

---

### devmemory/agent_context.py
**Status:** ⚠️ **EXPERIMENTAL**

Provides context inheritance between agents.

| Feature | Status | Notes |
|---------|--------|-------|
| get_agent_context() | ⚠️ EXPERIMENTAL | Works in testing |
| get_3layer_context() | ⚠️ EXPERIMENTAL | Advanced feature |
| save_findings() | ⚠️ EXPERIMENTAL | Works in testing |
| Context inheritance | ⚠️ EXPERIMENTAL | Works but complex |

**Dependencies:** session_memory.py, graph_query.py

---

### devmemory/artifact_manager.py
**Status:** ⚠️ **EXPERIMENTAL**

Manages large output artifacts with smart retention.

| Feature | Status | Notes |
|---------|--------|-------|
| store() | ⚠️ EXPERIMENTAL | Works in testing |
| retrieve() | ⚠️ EXPERIMENTAL | Works in testing |
| Retention policies | ⚠️ EXPERIMENTAL | Configurable |
| Auto-cleanup | ⚠️ EXPERIMENTAL | Basic functionality |

**Dependencies:** None

---

### devmemory/graph_builder.py
**Status:** ⚠️ **EXPERIMENTAL**

Builds semantic graph from codebase.

| Feature | Status | Notes |
|---------|--------|-------|
| discover() | ⚠️ EXPERIMENTAL | Scans files |
| validate() | ⚠️ EXPERIMENTAL | Checks consistency |
| ProtectedSurface | ⚠️ EXPERIMENTAL | Advanced feature |

**Dependencies:** None

**Known Issues:**
- Large codebases may be slow (>1000 files)

---

### devmemory/graph_query.py
**Status:** ⚠️ **EXPERIMENTAL**

Queries the semantic graph.

| Feature | Status | Notes |
|---------|--------|-------|
| invariants_for() | ⚠️ EXPERIMENTAL | Works in testing |
| trace_bug() | ⚠️ EXPERIMENTAL | Works in testing |
| find_gaps() | ⚠️ EXPERIMENTAL | Works in testing |
| CLI interface | ⚠️ EXPERIMENTAL | Basic commands work |

**Dependencies:** graph_builder.py

---

### devmemory/wiring.py
**Status:** 🔧 **PARTIAL**

Integration wiring between DevMemory components.

| Feature | Status | Notes |
|---------|--------|-------|
| wire_session_start() | ✅ VERIFIED | Session initialization |
| wire_command_output() | ⚠️ EXPERIMENTAL | Artifact offloading |
| wire_agent_spawn() | ⚠️ EXPERIMENTAL | Agent context |
| wire_agent_complete() | ⚠️ EXPERIMENTAL | Findings save |
| wire_bug_fix() | ⚠️ EXPERIMENTAL | Regression tracking |

**Dependencies:** All devmemory modules

---

## Session Workflow Status

```
SESSION START ────────────────────────────────────────────────────
│
├── wire_session_start()           ✅ VERIFIED
│   ├── SessionMemory.start()      ✅ VERIFIED
│   ├── Load previous session      ✅ VERIFIED
│   └── emit_event("session.start")✅ VERIFIED
│
├── Version detection              ✅ VERIFIED
│   └── Read from CHANGELOG.md     ✅ VERIFIED
│
DURING SESSION ───────────────────────────────────────────────────
│
├── Confidence calculation         ✅ VERIFIED
│   └── confidence_engine.py       ✅ VERIFIED
│
├── Event emission                 ⚠️ EXPERIMENTAL
│   ├── emit_code_edit()           ⚠️ EXPERIMENTAL
│   └── emit_confidence_snapshot() ⚠️ EXPERIMENTAL
│
├── Agent context                  ⚠️ EXPERIMENTAL
│   ├── get_3layer_context()       ⚠️ EXPERIMENTAL
│   └── Context inheritance        ⚠️ EXPERIMENTAL
│
├── GitHub sync                    🔧 PARTIAL
│   ├── Import issues              ✅ VERIFIED
│   └── Export bugs                ⚠️ EXPERIMENTAL
│
SESSION END ──────────────────────────────────────────────────────
│
├── Session save                   ✅ VERIFIED
│   └── SessionMemory.save()       ✅ VERIFIED
│
└── Version tracking               ✅ VERIFIED
    └── Stored in session          ✅ VERIFIED
```

---

## Recommendations

### For Production Use
Use these features confidently:
- Session management (start, resume, save)
- Version tracking
- Confidence scoring (confidence_engine.py)
- GitHub import

### For Testing/Development
Use with monitoring:
- Event streaming
- Agent context
- Artifact management
- Graph queries

### Not Recommended Yet
Wait for more testing:
- Bidirectional GitHub sync (use import only)
- Full regression tracking
- Large codebase graph building

---

## Reporting Issues

If you encounter issues:
1. Check this status document first
2. File an issue at: https://github.com/user-hash/LivingDocFramework/issues
3. Include: tool name, feature used, error message, Python version
