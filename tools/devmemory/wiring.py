#!/usr/bin/env python3
"""
DevMemory Wiring - Integration point for DevMemory components.

Part of the Living Documentation Framework.

This module provides hook functions that integrate DevMemory components:
- Session start hook (loads previous session)
- Command output handling
- Agent spawn context

Usage:
    # At session start
    from devmemory.wiring import wire_session_start
    context = wire_session_start()
    print(f"Session: {context['current_session_id']}")

Status: PARTIAL
- wire_session_start(): VERIFIED
- Other functions: EXPERIMENTAL
"""

import json
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List


# Handle imports for both module and direct execution
try:
    from .session_memory import SessionMemory
    from .event_stream import emit_event, emit_version_bump
except ImportError:
    from session_memory import SessionMemory
    from event_stream import emit_event, emit_version_bump


def wire_session_start(
    version: Optional[str] = None,
    branch: Optional[str] = None,
    changelog_path: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Wire session start - loads previous session and initializes new one.

    Called at the start of a Claude Code session.

    Args:
        version: Current project version (auto-detected if None)
        branch: Current git branch (auto-detected if None)
        changelog_path: Path to CHANGELOG.md for version detection

    Returns:
        Dict with:
        - previous_session: Summary of last session
        - current_session_id: New session ID
        - inherited_context: Context from last session

    Status: VERIFIED
    """

    session = SessionMemory()
    result = {
        "previous_session": None,
        "current_session_id": None,
        "inherited_context": {}
    }

    # Get last session summary
    last_session = session.get_last_session_summary()
    if last_session:
        result["previous_session"] = last_session
        result["inherited_context"] = {
            "last_version": last_session.get("version"),
            "last_confidence": last_session.get("confidence"),
            "last_bugs_open": last_session.get("bugs_open")
        }

    # Auto-detect git branch
    if not branch:
        try:
            proc = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if proc.returncode == 0:
                branch = proc.stdout.strip()
        except Exception:
            pass

    # Auto-detect version from CHANGELOG.md
    if not version:
        try:
            if changelog_path is None:
                changelog_path = Path("CHANGELOG.md")

            if changelog_path.exists():
                content = changelog_path.read_text(encoding='utf-8')
                match = re.search(r'## \[(\d+\.\d+\.\d+)\]', content)
                if match:
                    version = match.group(1)
        except Exception:
            pass

    # Start/resume session
    session_id = session.start(version=version, branch=branch)
    result["current_session_id"] = session_id

    # Emit session start event
    emit_event(
        "session.start" if not last_session else "session.resume",
        {
            "session_id": session_id,
            "previous_session": last_session.get("session_id") if last_session else None,
            "version": version,
            "branch": branch
        },
        f"Session {'started' if not last_session else 'resumed'}: {session_id}",
        severity="info"
    )

    return result


def wire_session_end() -> Dict[str, Any]:
    """
    Wire session end - saves session state.

    Status: VERIFIED
    """

    session = SessionMemory()
    summary = session.get_summary()

    if summary:
        emit_event(
            "session.end",
            summary,
            f"Session ended: {summary.get('session_id', 'unknown')}",
            severity="info"
        )
        session.save()

    return summary


def wire_version_change(
    old_version: str,
    new_version: str,
    commit: Optional[str] = None
) -> str:
    """
    Wire version change - updates session and emits event.

    Status: VERIFIED
    """

    session = SessionMemory()
    if session.is_initialized():
        session._session_data["version_current"] = new_version
        session.save()

    return emit_version_bump(old_version, new_version, commit)


# CLI for testing
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: wiring.py <command>")
        print("Commands:")
        print("  session-start  - Wire session start")
        print("  session-end    - Wire session end")
        sys.exit(1)

    command = sys.argv[1]

    if command == "session-start":
        result = wire_session_start()
        print(f"Session started: {result['current_session_id']}")
        if result['previous_session']:
            print(f"Previous session: {result['previous_session']}")
        print(f"Inherited context: {result['inherited_context']}")

    elif command == "session-end":
        summary = wire_session_end()
        print(f"Session ended: {summary}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
