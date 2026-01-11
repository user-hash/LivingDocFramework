"""
DevMemory - Cognitive Development Memory System

Part of the Living Documentation Framework.

This package provides:
- Session Memory: Auto-persist and restore session state (VERIFIED)
- Event Stream: Cognitive event logging (PARTIAL)
- Confidence Tracker: Track confidence changes (EXPERIMENTAL)
- Wiring: Integration between components (PARTIAL)

Quick Start:
    # Session management (VERIFIED)
    from devmemory.session_memory import SessionMemory

    session = SessionMemory()
    session.start(version="1.0.0", branch="main")
    session.save()

    # Event streaming (EXPERIMENTAL)
    from devmemory.event_stream import emit_event

    emit_event("code.edit", {"file": "app.py"}, "Edited app.py")

Version: 1.0.0
"""

__version__ = "1.0.0"

# Session Memory (VERIFIED)
from .session_memory import (
    SessionMemory,
    load_session,
    save_session,
    get_session_summary,
)

# Event Stream (PARTIAL)
from .event_stream import (
    emit_event,
    query_events,
    get_event,
    emit_code_edit,
    emit_version_bump,
)

# Wiring (PARTIAL)
from .wiring import (
    wire_session_start,
)

__all__ = [
    # Session Memory
    "SessionMemory",
    "load_session",
    "save_session",
    "get_session_summary",
    # Event Stream
    "emit_event",
    "query_events",
    "get_event",
    "emit_code_edit",
    "emit_version_bump",
    # Wiring
    "wire_session_start",
]
