#!/usr/bin/env python3
"""
GitHub Sync for Living Documentation Framework

Two-way sync between GitHub Issues and local bugs JSON file.

Usage:
    python github_sync.py import         # GitHub -> local JSON
    python github_sync.py export         # local JSON -> GitHub
    python github_sync.py sync           # Bidirectional sync
    python github_sync.py create-labels  # Create standard labels in repo

Status: PARTIAL
- Import: VERIFIED (tested with 300+ issues)
- Export: EXPERIMENTAL
- Sync: EXPERIMENTAL

Dependencies:
- GitHub CLI (gh) must be installed and authenticated
- Run: gh auth login
"""

import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Configuration - Override via environment or config file
BUGS_FILE = os.environ.get("LDF_BUGS_FILE", "bugs.json")

# Label mappings - Customize for your project
SEVERITY_TO_LABEL = {
    "P0": "P0-critical",
    "P1": "P1-high",
    "P2": "P2-medium",
    "P3": "P3-low",
    "critical": "P0-critical",
    "high": "P1-high",
    "medium": "P2-medium",
    "low": "P3-low"
}

LABEL_TO_SEVERITY = {
    "P0-critical": "P0",
    "P1-high": "P1",
    "P2-medium": "P2",
    "P3-low": "P3"
}

# Default category labels - Customize for your project
DEFAULT_CATEGORY_LABELS = {
    "backend": "backend",
    "frontend": "frontend",
    "api": "api",
    "database": "database",
    "auth": "auth",
    "general": "general"
}

# Standard labels to create in repo
STANDARD_LABELS = [
    {"name": "bug", "color": "d73a4a", "description": "Something isn't working"},
    {"name": "enhancement", "color": "a2eeef", "description": "New feature or request"},
    {"name": "false-positive", "color": "cccccc", "description": "Not a real bug"},
    {"name": "P0-critical", "color": "b60205", "description": "Critical - blocks release"},
    {"name": "P1-high", "color": "d93f0b", "description": "High priority"},
    {"name": "P2-medium", "color": "fbca04", "description": "Medium priority"},
    {"name": "P3-low", "color": "0e8a16", "description": "Low priority"},
    {"name": "investigating", "color": "ff7619", "description": "Fix applied, awaiting verification"},
]

# Keywords that indicate false positive
FALSE_POSITIVE_KEYWORDS = [
    "false positive", "false-positive", "not a bug", "not bug",
    "already fixed", "already handled", "by design", "design choice",
    "enhancement not bug", "file does not exist", "non-existent file",
    "fabricated", "no evidence"
]


def find_gh_cli() -> str:
    """Find the GitHub CLI executable."""
    # Try common locations
    common_paths = [
        "gh",  # In PATH
        "/usr/bin/gh",
        "/usr/local/bin/gh",
        r"C:\Program Files\GitHub CLI\gh.exe",
        r"C:\Program Files (x86)\GitHub CLI\gh.exe",
    ]

    for path in common_paths:
        try:
            result = subprocess.run(
                [path, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return path
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

    return "gh"  # Fallback to PATH


GH_CLI = find_gh_cli()


def run_gh(args: List[str], capture: bool = True) -> Tuple[bool, str]:
    """
    Run gh CLI command and return (success, output).

    Status: VERIFIED
    """
    cmd = [GH_CLI] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            encoding='utf-8',
            timeout=60
        )
        return result.returncode == 0, result.stdout.strip() if capture and result.stdout else ""
    except FileNotFoundError:
        print("ERROR: GitHub CLI (gh) not found.")
        print("Install with: brew install gh (macOS) or winget install GitHub.cli (Windows)")
        return False, ""
    except subprocess.TimeoutExpired:
        print("ERROR: GitHub CLI command timed out")
        return False, ""


def load_bugs(bugs_file: Path) -> Dict:
    """Load bugs from JSON file."""
    if bugs_file.exists():
        try:
            with open(bugs_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in {bugs_file}: {e}")
    return {"schema_version": 1, "bugs": []}


def save_bugs(bugs_file: Path, data: Dict) -> None:
    """Save bugs to JSON file."""
    with open(bugs_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_github_issues() -> List[Dict]:
    """
    Fetch all issues from GitHub.

    Status: VERIFIED
    """
    success, output = run_gh([
        "issue", "list",
        "--state", "all",
        "--limit", "500",
        "--json", "number,title,body,labels,state,createdAt,closedAt"
    ])

    if not success:
        print("ERROR: Failed to fetch GitHub issues")
        return []

    try:
        return json.loads(output) if output else []
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON from gh: {output[:200]}")
        return []


def parse_issue_to_bug(issue: Dict, category_labels: Dict = None) -> Dict:
    """
    Convert GitHub issue to bug format.

    Status: VERIFIED
    """
    if category_labels is None:
        category_labels = DEFAULT_CATEGORY_LABELS

    labels = [l["name"] for l in issue.get("labels", [])]

    # Extract severity from labels
    severity = "P2"  # default
    for label in labels:
        if label in LABEL_TO_SEVERITY:
            severity = LABEL_TO_SEVERITY[label]
            break

    # Extract category from labels
    category = "general"
    label_to_category = {v: k for k, v in category_labels.items()}
    for label in labels:
        if label in label_to_category:
            category = label_to_category[label]
            break

    # Determine status
    is_false_positive = "false-positive" in labels
    body_lower = (issue.get("body", "") or "").lower()

    if not is_false_positive and issue.get("state") == "CLOSED":
        for keyword in FALSE_POSITIVE_KEYWORDS:
            if keyword in body_lower:
                is_false_positive = True
                break

    if is_false_positive:
        status = "false_positive"
    elif issue.get("state") == "CLOSED":
        status = "fixed"
    elif "investigating" in labels:
        status = "investigating"
    else:
        status = "open"

    # Parse body for file:line info
    body = issue.get("body", "") or ""
    file_path = ""
    line_num = 0

    for line in body.split("\n"):
        line_lower = line.lower()
        if "file:" in line_lower or "location:" in line_lower:
            parts = line.split(":", 1)
            if len(parts) > 1:
                loc = parts[1].strip()
                if ":" in loc:
                    file_path, line_str = loc.rsplit(":", 1)
                    try:
                        line_num = int(line_str)
                    except ValueError:
                        file_path = loc
                else:
                    file_path = loc

    # Determine type
    issue_type = "enhancement" if "enhancement" in labels else "bug"

    return {
        "id": f"GH-{issue['number']}",
        "github_number": issue["number"],
        "source": "github",
        "type": issue_type,
        "severity": severity,
        "category": category,
        "status": status,
        "title": issue["title"],
        "file": file_path,
        "line": line_num,
        "message": body[:500] if body else "",
        "first_seen": issue.get("createdAt", "")[:10],
        "labels": labels
    }


def bug_to_issue_body(bug: Dict) -> str:
    """Convert bug to GitHub issue body."""
    body_parts = []

    if bug.get("file"):
        loc = bug["file"]
        if bug.get("line"):
            loc += f":{bug['line']}"
        body_parts.append(f"**Location:** `{loc}`")

    if bug.get("message"):
        body_parts.append(f"\n**Description:**\n{bug['message']}")

    if bug.get("pattern_id"):
        body_parts.append(f"\n**Pattern:** {bug['pattern_id']}")

    body_parts.append(f"\n---\n*Synced from Living Documentation Framework*")

    return "\n".join(body_parts)


def get_bug_labels(bug: Dict, category_labels: Dict = None) -> List[str]:
    """Get GitHub labels for a bug."""
    if category_labels is None:
        category_labels = DEFAULT_CATEGORY_LABELS

    labels = ["bug"]

    # Severity label
    severity = bug.get("severity", "P2")
    if severity in SEVERITY_TO_LABEL:
        labels.append(SEVERITY_TO_LABEL[severity])

    # Category label
    category = bug.get("category", "general")
    if category in category_labels:
        labels.append(category_labels[category])

    return labels


def import_from_github(bugs_file: Path) -> None:
    """
    Import issues from GitHub to local JSON.

    Status: VERIFIED
    """
    print("Importing from GitHub...")

    issues = get_github_issues()
    if not issues:
        print("  No issues found or error fetching")
        return

    data = load_bugs(bugs_file)
    existing_ids = {b.get("id") for b in data["bugs"]}
    existing_gh_nums = {b.get("github_number") for b in data["bugs"] if b.get("github_number")}

    imported = 0
    updated = 0

    for issue in issues:
        gh_id = f"GH-{issue['number']}"

        if issue["number"] in existing_gh_nums:
            # Update existing bug
            parsed = parse_issue_to_bug(issue)
            for bug in data["bugs"]:
                if bug.get("github_number") == issue["number"]:
                    old_status = bug.get("status")
                    new_status = parsed["status"]
                    if old_status != new_status:
                        bug["status"] = new_status
                        bug["labels"] = parsed.get("labels", [])
                        updated += 1
                        print(f"  Updated {gh_id}: {old_status} -> {new_status}")
                    break
        elif gh_id not in existing_ids:
            # Import new bug
            bug = parse_issue_to_bug(issue)
            data["bugs"].append(bug)
            imported += 1
            print(f"  Imported {gh_id}: {issue['title'][:50]}")

    save_bugs(bugs_file, data)
    print(f"\nImport complete: {imported} new, {updated} updated")


def export_to_github(bugs_file: Path) -> None:
    """
    Export bugs from local JSON to GitHub Issues.

    Status: EXPERIMENTAL
    """
    print("Exporting to GitHub...")

    data = load_bugs(bugs_file)
    created = 0

    for bug in data["bugs"]:
        # Skip if already has GitHub number
        if bug.get("github_number"):
            continue

        # Skip if ID starts with GH- (already from GitHub)
        if bug.get("id", "").startswith("GH-"):
            continue

        title = f"[{bug.get('id', 'BUG')}] {bug.get('title', 'Untitled')}"
        body = bug_to_issue_body(bug)
        labels = get_bug_labels(bug)

        print(f"  Creating issue: {title[:60]}...")

        success, output = run_gh([
            "issue", "create",
            "--title", title,
            "--body", body,
            "--label", ",".join(labels)
        ])

        if success:
            if "/issues/" in output:
                issue_num = int(output.split("/issues/")[-1])
                bug["github_number"] = issue_num
                bug["synced"] = True
                created += 1
                print(f"    Created #{issue_num}")
            else:
                print(f"    Created (couldn't parse number)")
                created += 1
        else:
            print(f"    FAILED: {output[:100]}")

    save_bugs(bugs_file, data)
    print(f"\nExport complete: {created} issues created")


def sync_bidirectional(bugs_file: Path) -> None:
    """
    Sync both directions.

    Status: EXPERIMENTAL
    """
    print("=== Bidirectional Sync ===\n")
    import_from_github(bugs_file)
    print()
    export_to_github(bugs_file)
    print("\n=== Sync Complete ===")


def create_labels() -> None:
    """
    Create standard labels in the GitHub repo.

    Status: VERIFIED
    """
    print("Creating standard labels...")

    for label in STANDARD_LABELS:
        success, _ = run_gh([
            "label", "create", label["name"],
            "--color", label["color"],
            "--description", label["description"],
            "--force"
        ])
        status = "OK" if success else "SKIP"
        print(f"  [{status}] {label['name']}")

    print("\nLabels created/updated")


def test_connection() -> None:
    """Test GitHub CLI connection."""
    success, output = run_gh(["auth", "status"])
    print(f"gh auth status: {'OK' if success else 'FAILED'}")
    if output:
        # Avoid encoding issues by filtering non-ASCII
        safe_output = output.encode('ascii', 'replace').decode('ascii')
        print(safe_output)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1].lower()

    # Determine bugs file location
    bugs_file = Path(BUGS_FILE)
    if len(sys.argv) > 2 and sys.argv[2].endswith('.json'):
        bugs_file = Path(sys.argv[2])

    if command == "import":
        import_from_github(bugs_file)
    elif command == "export":
        export_to_github(bugs_file)
    elif command == "sync":
        sync_bidirectional(bugs_file)
    elif command == "create-labels":
        create_labels()
    elif command == "test":
        test_connection()
    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
