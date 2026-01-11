#!/usr/bin/env python3
"""
Event Stream - Cognitive event logging for development sessions.

Part of the Living Documentation Framework.

This module provides event logging and querying for tracking significant
actions during development sessions.

Usage:
    from devmemory.event_stream import emit_event, query_events

    # Emit an event
    event_id = emit_event(
        event_type="code.edit",
        data={"file": "app.py", "lines_changed": 10},
        summary="Modified app.py"
    )

    # Query events
    events = query_events(event_type="code.*", limit=10)

Status: PARTIAL
- emit_event(): VERIFIED
- emit_code_edit(): EXPERIMENTAL
- emit_version_bump(): VERIFIED
- query_events(): EXPERIMENTAL
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

# Default storage location
DEFAULT_STORAGE_DIR = Path(".claude/devmemory")
DEFAULT_EVENTS_FILE = "events.jsonl"


class EventStream:
    """
    Manages cognitive event streaming.

    Status: PARTIAL
    """

    def __init__(self, storage_dir: Optional[Path] = None):
        """
        Initialize event stream.

        Args:
            storage_dir: Directory for event files. Defaults to .claude/devmemory
        """
        self.storage_dir = storage_dir or DEFAULT_STORAGE_DIR
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.events_file = self.storage_dir / DEFAULT_EVENTS_FILE

    def _generate_event_id(self, event_type: str) -> str:
        """Generate unique event ID."""
        timestamp = datetime.utcnow().isoformat()
        hash_input = f"{event_type}-{timestamp}-{id(self)}"
        short_hash = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        return f"E-{short_hash}"

    def emit(self,
             event_type: str,
             data: Dict[str, Any],
             summary: str,
             severity: str = "info",
             parent_id: Optional[str] = None) -> str:
        """
        Emit an event to the stream.

        Args:
            event_type: Event type (e.g., "code.edit", "bug.fix")
            data: Event data payload
            summary: Human-readable summary
            severity: Event severity (info, warning, error)
            parent_id: Optional parent event ID for causality

        Returns:
            Event ID

        Status: VERIFIED
        """
        event_id = self._generate_event_id(event_type)
        timestamp = datetime.utcnow().isoformat() + "Z"

        event = {
            "id": event_id,
            "type": event_type,
            "timestamp": timestamp,
            "severity": severity,
            "summary": summary,
            "data": data
        }

        if parent_id:
            event["parent_id"] = parent_id

        # Append to JSONL file
        with open(self.events_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event) + "\n")

        return event_id

    def query(self,
              event_type: Optional[str] = None,
              since: Optional[str] = None,
              limit: int = 100) -> List[Dict[str, Any]]:
        """
        Query events from the stream.

        Args:
            event_type: Filter by event type (supports wildcards like "code.*")
            since: Filter events after this timestamp
            limit: Maximum events to return

        Returns:
            List of matching events

        Status: EXPERIMENTAL
        """
        if not self.events_file.exists():
            return []

        events = []

        with open(self.events_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Filter by type
                if event_type:
                    if event_type.endswith("*"):
                        prefix = event_type[:-1]
                        if not event.get("type", "").startswith(prefix):
                            continue
                    elif event.get("type") != event_type:
                        continue

                # Filter by time
                if since:
                    event_time = event.get("timestamp", "")
                    if event_time < since:
                        continue

                events.append(event)

        # Return most recent, up to limit
        return events[-limit:]

    def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific event by ID.

        Status: EXPERIMENTAL
        """
        if not self.events_file.exists():
            return None

        with open(self.events_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    event = json.loads(line)
                    if event.get("id") == event_id:
                        return event
                except json.JSONDecodeError:
                    continue

        return None


# Global instance for convenience functions
_stream: Optional[EventStream] = None


def _get_stream() -> EventStream:
    """Get or create global event stream."""
    global _stream
    if _stream is None:
        _stream = EventStream()
    return _stream


def emit_event(event_type: str,
               data: Dict[str, Any],
               summary: str,
               severity: str = "info",
               parent_id: Optional[str] = None) -> str:
    """
    Emit an event to the stream.

    Status: VERIFIED
    """
    return _get_stream().emit(event_type, data, summary, severity, parent_id)


def query_events(event_type: Optional[str] = None,
                 since: Optional[str] = None,
                 limit: int = 100) -> List[Dict[str, Any]]:
    """
    Query events from the stream.

    Status: EXPERIMENTAL
    """
    return _get_stream().query(event_type, since, limit)


def get_event(event_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a specific event by ID.

    Status: EXPERIMENTAL
    """
    return _get_stream().get_event(event_id)


# Typed event helpers

def emit_code_edit(file: str,
                   lines_changed: List[int] = None,
                   edit_type: str = "modification",
                   tier: str = "C",
                   summary: str = None) -> str:
    """
    Emit a code edit event.

    Status: EXPERIMENTAL
    """
    data = {
        "file": file,
        "lines_changed": lines_changed or [],
        "edit_type": edit_type,
        "tier": tier
    }
    summary = summary or f"Edited {file}"
    return emit_event("code.edit", data, summary)


def emit_version_bump(old_version: str,
                      new_version: str,
                      commit: Optional[str] = None) -> str:
    """
    Emit a version bump event.

    Status: VERIFIED
    """
    data = {
        "old_version": old_version,
        "new_version": new_version,
        "commit": commit
    }
    summary = f"Version bump: {old_version} -> {new_version}"
    return emit_event("version.bump", data, summary, severity="info")


def emit_bug_status_change(bug_id: str,
                           old_status: str,
                           new_status: str,
                           version: Optional[str] = None) -> str:
    """
    Emit a bug status change event.

    Status: EXPERIMENTAL
    """
    data = {
        "bug_id": bug_id,
        "old_status": old_status,
        "new_status": new_status,
        "version": version
    }
    summary = f"Bug {bug_id}: {old_status} -> {new_status}"
    return emit_event("bug.status_change", data, summary)


def emit_confidence_snapshot(score: float,
                             trigger: str,
                             penalty_breakdown: Optional[Dict] = None,
                             inputs: Optional[Dict] = None) -> str:
    """
    Emit a confidence snapshot event.

    Status: EXPERIMENTAL
    """
    data = {
        "score": score,
        "trigger": trigger,
        "penalty_breakdown": penalty_breakdown,
        "inputs": inputs
    }
    summary = f"Confidence: {score}% (triggered by {trigger})"
    return emit_event("confidence.snapshot", data, summary)


if __name__ == "__main__":
    # Self-test
    print("Event Stream Self-Test")
    print("=" * 40)

    # Emit some events
    event_id = emit_event(
        "test.event",
        {"key": "value"},
        "Test event emitted"
    )
    print(f"Emitted event: {event_id}")

    code_id = emit_code_edit("src/app.py", [10, 11, 12], "modification")
    print(f"Emitted code edit: {code_id}")

    version_id = emit_version_bump("1.0.0", "1.0.1")
    print(f"Emitted version bump: {version_id}")

    # Query events
    events = query_events(limit=5)
    print(f"\nRecent events: {len(events)}")
    for e in events[-3:]:
        print(f"  - {e['type']}: {e['summary']}")

    print("\nSelf-test PASSED")
