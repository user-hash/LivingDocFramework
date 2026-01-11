# DevMemory: Cognitive Development Memory

**Version:** 1.0.0

> An event-driven cognitive memory system that persists context across AI sessions.

---

## Overview

DevMemory solves a fundamental problem with AI-assisted development: **sessions are stateless**. When a conversation ends, context is lost. Next session, the AI starts fresh with no memory of:

- What files were edited
- Which bugs were investigated
- What patterns were discovered
- Current confidence level
- Session-to-session trends

DevMemory provides **persistent cognitive memory** by:

1. **Event Streaming** - Log every significant action
2. **Session Tracking** - Maintain context across sessions
3. **Confidence Scoring** - Track project health over time
4. **Semantic Graph** - Map relationships between files, docs, and patterns

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         DevMemory System                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │ Event Stream │───▶│   Session    │───▶│   Confidence     │   │
│  │              │    │   Memory     │    │   Tracker        │   │
│  │ • emit()     │    │ • context    │    │ • 2-layer score  │   │
│  │ • query()    │    │ • summary    │    │ • trends         │   │
│  └──────────────┘    └──────────────┘    └──────────────────┘   │
│         │                   │                     │              │
│         └───────────────────┼─────────────────────┘              │
│                             │                                    │
│                             ▼                                    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │ Graph Builder│◀──▶│  Artifact    │    │    Wiring        │   │
│  │              │    │  Manager     │    │                  │   │
│  │ • 15-pass    │    │ • offload    │    │ • hook handlers  │   │
│  │ • semantic   │    │ • LRU cache  │    │ • integrations   │   │
│  └──────────────┘    └──────────────┘    └──────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Modules

### 1. Event Stream (`event_stream.py`)

Central event logging with strict schema validation.

**Event Structure:**
```python
{
    "id": "E-ABC12345",        # Unique event ID
    "type": "code.edit",       # Event type (from allowed list)
    "timestamp": "ISO-8601",   # When it happened
    "session_id": "S-xyz789", # Which session
    "data": {                  # Type-specific payload
        "file": "GridSync.cs",
        "lines_changed": 42
    },
    "summary": "Modified GridSync.cs"  # Human-readable
}
```

**Allowed Event Types (27 total):**

| Category | Types |
|----------|-------|
| `code.*` | `code.edit`, `code.create`, `code.delete`, `code.refactor` |
| `doc.*` | `doc.update`, `doc.create`, `doc.link` |
| `bug.*` | `bug.found`, `bug.fixed`, `bug.reopened`, `bug.pattern_added` |
| `version.*` | `version.bump`, `version.tag`, `version.release` |
| `agent.*` | `agent.spawn`, `agent.complete`, `agent.error` |
| `session.*` | `session.start`, `session.end`, `session.resume` |
| `confidence.*` | `confidence.snapshot`, `confidence.change` |
| `skill.*` | `skill.start`, `skill.complete` |
| `dashboard.*` | `dashboard.refresh` |

**Usage:**
```python
from devmemory.event_stream import emit_event, query_events

# Emit an event
emit_event(
    event_type="code.edit",
    data={"file": "GridSync.cs", "lines_changed": 42},
    summary="Modified GridSync.cs"
)

# Query events
recent_edits = query_events(
    event_type="code.*",
    since="2024-01-10",
    limit=100
)
```

---

### 2. Session Memory (`session_memory.py`)

Maintains context across sessions.

**Session Structure:**
```python
{
    "id": "S-abc12345def",
    "started_at": "2024-01-11T13:00:00Z",
    "version_start": "0.916.16",
    "version_current": "0.916.36",
    "events_count": 399,
    "files_touched": ["GridSync.cs", "BeatManager.cs"],
    "bugs_fixed": ["BUG-MP-042"],
    "confidence_start": 91.2,
    "confidence_current": 94.1
}
```

**Features:**
- Session ID persists across conversation restarts
- Inherits context from previous session
- Tracks version progression
- Maintains file change history

**Usage:**
```python
from devmemory.session_memory import SessionMemory

# Start or resume session
session = SessionMemory.start()
print(f"Session: {session.id}")
print(f"Previous: {session.get_summary()}")

# At session end
session.end(summary="Fixed 3 bugs, added pattern GP-THREAD-004")
```

---

### 3. Confidence Tracker (`confidence_tracker.py`)

Implements 2-layer confidence scoring with trend analysis.

**2-Layer Scoring:**

| Layer | Weight | Measures |
|-------|--------|----------|
| Code Health | 60% | Runtime risk factors |
| Knowledge Health | 40% | Cognitive coverage |

**Code Health Factors:**
- Open bugs by severity (P1: -15, P2: -8, P3: -3)
- Unprotected Tier A files (-5 each)
- Missing test coverage (-10 per gap)
- Regression rate (-20 if >10%)

**Knowledge Health Factors:**
- Invariant coverage (+2 per protected file)
- Pattern documentation (+1 per pattern)
- ADR completeness (+0.5 per decision)
- Stale documentation (-5 per stale doc)

**Usage:**
```python
from devmemory.confidence_tracker import track_confidence, get_trend

# Calculate current confidence
score = track_confidence()
print(f"Overall: {score.overall}%")
print(f"Code Health: {score.code_health}%")
print(f"Knowledge Health: {score.knowledge_health}%")

# Analyze trend
trend = get_trend(days=7)
print(f"7-day trend: {trend.direction} ({trend.delta:+.1f}%)")
```

---

### 4. Graph Builder (`graph_builder.py`)

Builds semantic knowledge graph with 15-pass discovery.

**Graph Structure:**
```
Nodes: Files, Docs, Invariants, Patterns, Decisions
Edges: references, protects, documents, implements
```

**Discovery Passes:**

| Pass | Confidence | Source |
|------|------------|--------|
| 1-3 | 1.00 | Explicit links (CODE_DOC_MAP.md) |
| 4-6 | 0.95 | Structural analysis (imports, inheritance) |
| 7-10 | 0.85 | Content analysis (mentions, patterns) |
| 11-15 | 0.70 | Inferred relationships |

**Usage:**
```python
from devmemory.graph_builder import discover, validate

# Build graph
graph = discover()
print(f"Nodes: {len(graph.nodes)}")
print(f"Edges: {len(graph.edges)}")

# Validate coverage
gaps = validate(graph)
for gap in gaps:
    print(f"Gap: {gap.file} missing {gap.missing}")
```

---

### 5. Graph Query (`graph_query.py`)

Query interface for the semantic graph.

**Query Types:**

```python
from devmemory.graph_query import GraphQuery

gq = GraphQuery()

# Find invariants protecting a file
invariants = gq.invariants_for("GridSyncManager.cs")
# Returns: [INV-MP.3, INV-MP.7, INV-THREAD.1]

# Trace bug to root cause
trace = gq.trace_bug("GH-507")
# Returns: {pattern: PATTERN-068, files: [...], invariants: [...]}

# Find coverage gaps
gaps = gq.gaps(tier="A")
# Returns: [{file: "NewFile.cs", missing: ["invariant", "test"]}]

# Get file context
context = gq.context_for("BeatManager.cs")
# Returns: {invariants: [...], patterns: [...], decisions: [...]}
```

---

### 6. Artifact Manager (`artifact_manager.py`)

Offloads large outputs to prevent context bloat.

**Features:**
- LRU cache with configurable max size
- Automatic cleanup of old artifacts
- Reference linking in events

**Usage:**
```python
from devmemory.artifact_manager import store, retrieve, cleanup

# Store large output
artifact_id = store(
    content=large_analysis_result,
    type="agent_report",
    session_id=current_session.id
)

# Reference in event
emit_event(
    event_type="agent.complete",
    data={"artifact": artifact_id}
)

# Retrieve later
content = retrieve(artifact_id)

# Cleanup old artifacts
cleanup(max_age_days=7)
```

---

### 7. Wiring (`wiring.py`)

Integration hooks that connect DevMemory to Claude Code.

**Hook Handlers:**

```python
# Called by hooks in settings.json or skill frontmatter
python .claude/tools/devmemory/wiring.py session-start
python .claude/tools/devmemory/wiring.py pre-edit
python .claude/tools/devmemory/wiring.py post-edit
python .claude/tools/devmemory/wiring.py skill-complete bug-fix
```

**Integration Points:**

| Hook | DevMemory Action |
|------|------------------|
| `session-start` | Create/resume session, load context |
| `pre-edit` | Load invariants for file |
| `post-edit` | Emit code.edit event, update confidence |
| `post-task` | Log agent spawn/complete |
| `skill-complete` | Emit skill.complete, generate summary |

---

## Data Storage

```
.claude/
└── devmemory/
    ├── config.json          # Configuration
    ├── sessions/
    │   └── S-abc123.json    # Session files
    ├── events/
    │   └── events.jsonl     # Event stream (append-only)
    ├── graph/
    │   └── semantic.json    # Knowledge graph
    └── artifacts/
        └── A-xyz789.json    # Large artifacts
```

---

## Configuration

```json
// .claude/devmemory/config.json
{
  "event_stream": {
    "max_events": 10000,
    "rotation_days": 30
  },
  "session": {
    "timeout_hours": 24,
    "auto_resume": true
  },
  "confidence": {
    "code_health_weight": 0.6,
    "knowledge_health_weight": 0.4
  },
  "graph": {
    "discovery_passes": 15,
    "confidence_thresholds": [1.0, 0.95, 0.85, 0.70]
  },
  "artifacts": {
    "max_size_mb": 100,
    "cleanup_days": 7
  }
}
```

---

## Integration with Dashboard

DevMemory feeds the dashboard control plane:

```python
# refresh_dashboard.py calls:
from devmemory.session_memory import get_current_session
from devmemory.confidence_tracker import track_confidence
from devmemory.event_stream import get_recent_events

# Generates .claude/dashboard/cp-devmemory.json
{
    "session": {...},
    "events": {"total": 399, "recent": [...]},
    "confidence": {"start": 91.2, "current": 94.1}
}
```

---

## Best Practices

1. **Emit events liberally** - More data enables better analysis
2. **Use structured data** - Consistent schemas enable queries
3. **Archive large outputs** - Keep context window clean
4. **Query efficiently** - Use indexes where possible
5. **Clean up regularly** - Old artifacts consume space

---

## Related Documentation

- [../hooks/CC-2.1.0-HOOKS.md](../hooks/CC-2.1.0-HOOKS.md) - Hook configuration
- [../hooks/LIFECYCLE.md](../hooks/LIFECYCLE.md) - When hooks fire
- [CONFIDENCE.md](CONFIDENCE.md) - Detailed scoring methodology
