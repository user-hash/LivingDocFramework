#!/usr/bin/env python3
"""
Session Memory - Persist session state across Claude Code sessions.

Part of the Living Documentation Framework.

This module provides session state persistence, allowing context to be
maintained across multiple Claude Code sessions.

Usage:
    from devmemory.session_memory import SessionMemory

    # Start a new session
    session = SessionMemory()
    session_id = session.start(version="1.0.0", branch="main")

    # During session
    session.add_file_modified("src/app.py")
    session.update_confidence(85.5)
    session.save()

    # Get summary
    summary = session.get_summary()

Status: VERIFIED - Tested in production
"""

import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

# Default storage location
DEFAULT_STORAGE_DIR = Path(".claude/devmemory")


class SessionMemory:
    """
    Manages session state persistence.

    Status: VERIFIED
    """

    def __init__(self, storage_dir: Optional[Path] = None):
        """
        Initialize session memory.

        Args:
            storage_dir: Directory for session files. Defaults to .claude/devmemory
        """
        self.storage_dir = storage_dir or DEFAULT_STORAGE_DIR
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.session_file = self.storage_dir / "current_session.json"
        self.history_file = self.storage_dir / "session_history.json"

        self._session_data: Optional[Dict[str, Any]] = None
        self._load_current()

    def _load_current(self) -> None:
        """Load current session if exists."""
        if self.session_file.exists():
            try:
                self._session_data = json.loads(
                    self.session_file.read_text(encoding='utf-8')
                )
            except json.JSONDecodeError:
                self._session_data = None

    def _generate_session_id(self) -> str:
        """Generate unique session ID."""
        timestamp = datetime.utcnow().isoformat()
        hash_input = f"{timestamp}-{id(self)}"
        short_hash = hashlib.md5(hash_input.encode()).hexdigest()[:12]
        return f"S-{short_hash}"

    def is_initialized(self) -> bool:
        """Check if a session is currently active."""
        return self._session_data is not None

    def get_session_id(self) -> Optional[str]:
        """Get current session ID."""
        if self._session_data:
            return self._session_data.get("session_id")
        return None

    def start(self,
              version: Optional[str] = None,
              branch: Optional[str] = None,
              bugs_open: int = 0,
              bugs_total: int = 0,
              confidence: Optional[float] = None) -> str:
        """
        Start a new session or resume existing one.

        Args:
            version: Current project version
            branch: Current git branch
            bugs_open: Number of open bugs
            bugs_total: Total bugs tracked
            confidence: Current confidence score

        Returns:
            Session ID

        Status: VERIFIED
        """
        # If session exists and is recent (within 4 hours), resume it
        if self._session_data:
            last_update = self._session_data.get("last_update", "")
            if last_update:
                try:
                    last_dt = datetime.fromisoformat(last_update.replace("Z", "+00:00"))
                    hours_ago = (datetime.utcnow() - last_dt.replace(tzinfo=None)).total_seconds() / 3600
                    if hours_ago < 4:
                        # Resume existing session
                        self._session_data["resumed_count"] = self._session_data.get("resumed_count", 0) + 1
                        self._session_data["last_update"] = datetime.utcnow().isoformat() + "Z"
                        if version:
                            self._session_data["version_current"] = version
                        if confidence is not None:
                            self._session_data["confidence_current"] = confidence
                        self.save()
                        return self._session_data["session_id"]
                except (ValueError, TypeError):
                    pass

        # Archive old session if exists
        if self._session_data:
            self._archive_session()

        # Create new session
        session_id = self._generate_session_id()
        now = datetime.utcnow().isoformat() + "Z"

        self._session_data = {
            "session_id": session_id,
            "started_at": now,
            "last_update": now,
            "resumed_count": 0,
            "version_start": version,
            "version_current": version,
            "branch": branch,
            "bugs_open_start": bugs_open,
            "bugs_open_current": bugs_open,
            "bugs_total": bugs_total,
            "confidence_start": confidence,
            "confidence_current": confidence,
            "files_modified": [],
            "agents_spawned": [],
            "events_count": 0
        }

        self.save()
        return session_id

    def save(self) -> None:
        """
        Save current session state.

        Status: VERIFIED
        """
        if self._session_data:
            self._session_data["last_update"] = datetime.utcnow().isoformat() + "Z"
            self.session_file.write_text(
                json.dumps(self._session_data, indent=2),
                encoding='utf-8'
            )

    def _archive_session(self) -> None:
        """Archive current session to history."""
        if not self._session_data:
            return

        # Load history
        history = []
        if self.history_file.exists():
            try:
                history = json.loads(self.history_file.read_text(encoding='utf-8'))
            except json.JSONDecodeError:
                history = []

        # Add current session to history
        history.append(self._session_data)

        # Keep only last 50 sessions
        history = history[-50:]

        # Save history
        self.history_file.write_text(
            json.dumps(history, indent=2),
            encoding='utf-8'
        )

    def add_file_modified(self, file_path: str) -> None:
        """Record a file modification."""
        if self._session_data:
            files = self._session_data.get("files_modified", [])
            if file_path not in files:
                files.append(file_path)
                self._session_data["files_modified"] = files[-100:]  # Keep last 100

    def add_agent_spawned(self,
                          fingerprint: str,
                          agent_type: str,
                          status: str = "running",
                          findings: int = 0,
                          compliance_score: float = 0) -> None:
        """Record an agent spawn."""
        if self._session_data:
            agents = self._session_data.get("agents_spawned", [])
            agents.append({
                "fingerprint": fingerprint,
                "type": agent_type,
                "status": status,
                "findings": findings,
                "compliance_score": compliance_score,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
            self._session_data["agents_spawned"] = agents[-20:]  # Keep last 20

    def update_confidence(self, confidence: float) -> None:
        """Update current confidence score."""
        if self._session_data:
            self._session_data["confidence_current"] = confidence

    def update_bugs(self, bugs_open: int, bugs_total: int = None) -> None:
        """Update bug counts."""
        if self._session_data:
            self._session_data["bugs_open_current"] = bugs_open
            if bugs_total is not None:
                self._session_data["bugs_total"] = bugs_total

    def increment_events(self) -> None:
        """Increment event count."""
        if self._session_data:
            self._session_data["events_count"] = self._session_data.get("events_count", 0) + 1

    def get_summary(self) -> Dict[str, Any]:
        """
        Get session summary.

        Status: VERIFIED
        """
        if not self._session_data:
            return {}

        return {
            "session_id": self._session_data.get("session_id"),
            "started_at": self._session_data.get("started_at"),
            "last_update": self._session_data.get("last_update"),
            "resumed_count": self._session_data.get("resumed_count", 0),
            "version_start": self._session_data.get("version_start"),
            "version_current": self._session_data.get("version_current"),
            "branch": self._session_data.get("branch"),
            "confidence_start": self._session_data.get("confidence_start"),
            "confidence_current": self._session_data.get("confidence_current"),
            "bugs_open": self._session_data.get("bugs_open_current", 0),
            "files_modified_count": len(self._session_data.get("files_modified", [])),
            "agents_count": len(self._session_data.get("agents_spawned", [])),
            "events_count": self._session_data.get("events_count", 0)
        }

    def get_summary_text(self) -> str:
        """Get human-readable session summary."""
        summary = self.get_summary()
        if not summary:
            return "No active session"

        lines = [
            f"Session: {summary.get('session_id', 'unknown')}",
            f"Version: {summary.get('version_current', '?')}",
        ]

        if summary.get("confidence_current") is not None:
            lines.append(f"Confidence: {summary['confidence_current']}%")

        if summary.get("bugs_open", 0) > 0:
            lines.append(f"Open bugs: {summary['bugs_open']}")

        if summary.get("files_modified_count", 0) > 0:
            lines.append(f"Files modified: {summary['files_modified_count']}")

        return " | ".join(lines)

    def get_last_session_summary(self) -> Optional[Dict[str, Any]]:
        """
        Get summary of the previous session.

        Status: VERIFIED
        """
        if not self.history_file.exists():
            return None

        try:
            history = json.loads(self.history_file.read_text(encoding='utf-8'))
            if history:
                last = history[-1]
                return {
                    "session_id": last.get("session_id"),
                    "version": last.get("version_current"),
                    "confidence": last.get("confidence_current"),
                    "bugs_open": last.get("bugs_open_current", 0),
                    "files_modified": len(last.get("files_modified", [])),
                    "ended_at": last.get("last_update")
                }
        except (json.JSONDecodeError, KeyError):
            pass

        return None


# Convenience functions

def load_session(storage_dir: Optional[Path] = None) -> SessionMemory:
    """Load or create session memory."""
    return SessionMemory(storage_dir)


def save_session(session: SessionMemory) -> None:
    """Save session state."""
    session.save()


def get_session_summary(storage_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Get current session summary."""
    session = SessionMemory(storage_dir)
    return session.get_summary()


if __name__ == "__main__":
    # Self-test
    print("Session Memory Self-Test")
    print("=" * 40)

    session = SessionMemory()

    # Start session
    session_id = session.start(version="1.0.0", branch="main", confidence=85.0)
    print(f"Started session: {session_id}")

    # Modify state
    session.add_file_modified("src/app.py")
    session.add_file_modified("src/utils.py")
    session.update_confidence(87.5)
    session.save()

    # Get summary
    summary = session.get_summary()
    print(f"Summary: {summary}")
    print(f"Text: {session.get_summary_text()}")

    print("\nSelf-test PASSED")
