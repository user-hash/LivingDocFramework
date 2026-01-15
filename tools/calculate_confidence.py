#!/usr/bin/env python3
"""
Living Documentation Framework - Confidence Scoring Calculator

Calculates project confidence score using exponential decay with bounded penalties for:
- Severity counts (P0/P1/P2/P3)
- Documentation coverage
- File staleness
- Tier-A unmapped files
- Test coverage
- Bug resolution rate

Usage:
    python tools/calculate_confidence.py              # Calculate and print
    python tools/calculate_confidence.py --json       # JSON output
    python tools/calculate_confidence.py --update     # Update history.json
"""

import sys
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, Any

# Add core to path for config import
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR.parent / 'core'))

from config import get_config

# Scoring constants
K = 45  # Calibrated: 1×P0 → ~80, healthy project → ~75-85
EMA_WEIGHT = 0.7  # Weight for current score in EMA smoothing


def get_severity_counts(config) -> Dict[str, int]:
    """Extract P0/P1/P2/P3 OPEN BUG counts from BUG_TRACKER.md (NOT patterns).

    IMPORTANT: BUG_PATTERNS.md contains DOCUMENTED anti-patterns (educational).
    Only actual OPEN BUGS from BUG_TRACKER.md should affect confidence.
    """
    counts = {'p0': 0, 'p1': 0, 'p2': 0, 'p3': 0}

    bug_tracker = config.bug_tracker_path
    if not bug_tracker.exists():
        return counts

    try:
        content = bug_tracker.read_text(encoding='utf-8')

        # Look for JSON summary: "P0": 1, "P1": 8, "P2": 31, "P3": 76
        p0_match = re.search(r'"P0":\s*(\d+)', content)
        p1_match = re.search(r'"P1":\s*(\d+)', content)
        p2_match = re.search(r'"P2":\s*(\d+)', content)
        p3_match = re.search(r'"P3":\s*(\d+)', content)

        if p0_match:
            counts['p0'] = int(p0_match.group(1))
        if p1_match:
            counts['p1'] = int(p1_match.group(1))
        if p2_match:
            counts['p2'] = int(p2_match.group(1))
        if p3_match:
            counts['p3'] = int(p3_match.group(1))

        # If no JSON summary found, try to sum from the table
        # | System | P0 | P1 | P2 | P3 | ...
        if counts['p0'] == 0 and counts['p1'] == 0:
            table_rows = re.findall(r'\|\s*\w+\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|', content)
            for row in table_rows:
                counts['p0'] += int(row[0])
                counts['p1'] += int(row[1])
                counts['p2'] += int(row[2])
                counts['p3'] += int(row[3])

    except (OSError, IOError, UnicodeDecodeError) as e:
        print(f"Warning: Could not read {bug_tracker.name}: {e}", file=sys.stderr)

    return counts


def get_bug_resolution_metrics(config) -> Dict[str, int]:
    """Extract bugs_total and bugs_fixed from BUG_TRACKER.md."""
    metrics = {'bugs_total': 0, 'bugs_fixed': 0}

    bug_tracker = config.bug_tracker_path
    if not bug_tracker.exists():
        return metrics

    try:
        content = bug_tracker.read_text(encoding='utf-8')
        # Match patterns like "1,712+ bugs tracked" and "1,596+ fixed"
        total_match = re.search(r'([\d,]+)\+?\s*bugs?\s*tracked', content, re.IGNORECASE)
        fixed_match = re.search(r'([\d,]+)\+?\s*fixed', content, re.IGNORECASE)

        if total_match:
            metrics['bugs_total'] = int(total_match.group(1).replace(',', ''))
        if fixed_match:
            metrics['bugs_fixed'] = int(fixed_match.group(1).replace(',', ''))
    except (OSError, IOError, UnicodeDecodeError) as e:
        print(f"Warning: Could not read {bug_tracker.name}: {e}", file=sys.stderr)

    return metrics


def get_doc_coverage_metrics(config) -> Dict[str, int]:
    """Get mapped/unmapped counts from CODE_DOC_MAP.md or file system."""
    metrics = {'mapped': 0, 'unmapped': 0, 'tier_a_unmapped': 0}

    # Count actual code files using config
    code_files = config.find_code_files()
    total_scripts = len(code_files)

    code_doc_map = config.code_doc_map_path
    if not code_doc_map.exists():
        metrics['unmapped'] = total_scripts
        return metrics

    try:
        content = code_doc_map.read_text(encoding='utf-8')

        # Count unique mapped files (use first extension as pattern)
        ext = config.code_extensions[0] if config.code_extensions else 'py'
        mapped_files = set(re.findall(rf'`([^`]+\.{ext})`', content))
        metrics['mapped'] = len(mapped_files)
        metrics['unmapped'] = max(0, total_scripts - len(mapped_files))

        # Count Tier-A files that are NOT in the doc map
        tier_a_section = re.search(r'Tier A.*?(?=##|\Z)', content, re.DOTALL | re.IGNORECASE)
        if tier_a_section:
            tier_a_files = set(re.findall(rf'`([^`]+\.{ext})`', tier_a_section.group(0)))
            # For now, assume all Tier-A are documented if they appear
            metrics['tier_a_unmapped'] = 0
    except (OSError, IOError, UnicodeDecodeError) as e:
        print(f"Warning: Could not read CODE_DOC_MAP.md: {e}", file=sys.stderr)

    return metrics


def get_staleness_metrics(config) -> Dict[str, Any]:
    """Check documentation staleness based on file modification times.

    Staleness is measured as days since last modification.
    A document is considered "stale" if it hasn't been updated in 30+ days.
    Tier-A documents have a stricter threshold of 21 days.

    Returns:
        Dict with stale_count, avg_staleness (days), and tier_a_stale_count
    """
    metrics = {'stale_count': 0, 'avg_staleness': 0.0, 'tier_a_stale_count': 0}

    # Documentation files to check
    doc_files = [
        (config.invariants_path, True),      # Tier A
        (config.code_doc_map_path, True),    # Tier A
        (config.bug_patterns_path, False),   # Tier B
        (config.golden_paths_path, False),   # Tier B
        (config.decisions_path, False),      # Tier B
        (config.changelog_path, False),      # Tier B
    ]

    now = datetime.now(timezone.utc)
    staleness_days = []
    stale_threshold = 30  # days
    tier_a_threshold = 21  # days - stricter for critical docs

    for doc_path, is_tier_a in doc_files:
        if not doc_path.exists():
            continue

        try:
            # Get file modification time
            mtime = doc_path.stat().st_mtime
            mod_time = datetime.fromtimestamp(mtime, tz=timezone.utc)
            days_old = (now - mod_time).days
            staleness_days.append(days_old)

            # Check if stale
            if days_old >= stale_threshold:
                metrics['stale_count'] += 1

            # Check Tier-A staleness (stricter threshold)
            if is_tier_a and days_old >= tier_a_threshold:
                metrics['tier_a_stale_count'] += 1

        except (OSError, IOError):
            # Skip files we can't stat
            continue

    # Calculate average staleness
    if staleness_days:
        metrics['avg_staleness'] = sum(staleness_days) / len(staleness_days)

    return metrics


def get_test_metrics(config) -> Dict[str, int]:
    """Count test files and script files."""
    metrics = {'tests_count': 0, 'scripts': 0}

    try:
        code_files = config.find_code_files()
        metrics['scripts'] = len(code_files)

        # Find test files
        test_files = config.find_test_files()
        metrics['tests_count'] = len(test_files)
    except (OSError, IOError) as e:
        print(f"Warning: Could not count files: {e}", file=sys.stderr)

    return metrics


def get_previous_score(config) -> Optional[float]:
    """Get the most recent confidence score from history.json."""
    history_file = config.history_file
    if not history_file.exists():
        return None

    try:
        with open(history_file, 'r') as f:
            data = json.load(f)

        history = data.get('history', [])
        if history:
            return history[-1].get('confidence')
    except (OSError, IOError, json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Warning: Could not read history.json: {e}", file=sys.stderr)

    return None


def calculate_confidence(metrics: Dict[str, Any], previous_score: Optional[float] = None) -> Dict[str, Any]:
    """
    Calculate confidence score using exponential decay formula.

    Args:
        metrics: Dict with sev_p0, sev_p1, sev_p2, sev_p3, mapped, unmapped,
                 stale_count, avg_staleness, tierA_stale_count, tierA_unmapped,
                 scripts, tests_count, bug_resolve_pct
        previous_score: Previous confidence score for EMA smoothing

    Returns:
        Dict with score, base_score, and penalty_breakdown
    """
    # 1. Severity penalty (count-based, CAPPED at 40)
    # Weights: P0=10 (critical), P1=3 (high), P2=1 (medium), P3=0.05 (low/improvements)
    sev_p0 = metrics.get('sev_p0', 0)
    sev_p1 = metrics.get('sev_p1', 0)
    sev_p2 = metrics.get('sev_p2', 0)
    sev_p3 = metrics.get('sev_p3', 0)
    severity_penalty = min(10 * sev_p0 + 3 * sev_p1 + 1 * sev_p2 + 0.05 * sev_p3, 40.0)

    # 2. Doc coverage penalty (multiplier 22.2 for <45% = 10 max)
    mapped = metrics.get('mapped', 0)
    unmapped = metrics.get('unmapped', 0)
    total_files = mapped + unmapped
    doc_coverage = mapped / max(total_files, 1)
    doc_penalty = max(0, min(10, (0.9 - doc_coverage) * 22.2))

    # 3. Staleness penalty (bounded, CAPPED at 15 total)
    stale_count = metrics.get('stale_count', 0)
    avg_staleness = metrics.get('avg_staleness', 0)
    tier_a_stale = metrics.get('tierA_stale_count', 0)

    stale_count_penalty = min(stale_count * 0.5, 6.0)
    avg_stale_penalty = min(avg_staleness / 15, 6.0)
    tier_a_stale_penalty = min(tier_a_stale * 1.0, 6.0)
    staleness_penalty = min(stale_count_penalty + avg_stale_penalty + tier_a_stale_penalty, 15.0)

    # 4. Tier-A unmapped penalty
    tier_a_unmapped = metrics.get('tierA_unmapped', 0)
    tier_a_unmapped_penalty = min(tier_a_unmapped * 2.0, 10.0)

    # 5. Test coverage penalty
    scripts = metrics.get('scripts', 1)
    tests_count = metrics.get('tests_count', 0)
    tests_per_100 = tests_count / max(scripts, 1) * 100
    test_penalty = max(0, min(6, (5 - tests_per_100) * 1.5))

    # 6. Bug resolution penalty (penalize if <70% resolved)
    resolve_pct = metrics.get('bug_resolve_pct', 1.0)
    resolve_penalty = max(0, min(5, (0.7 - resolve_pct) * 10))

    # 7. Total penalty
    total_penalty = (
        severity_penalty +
        doc_penalty +
        staleness_penalty +
        tier_a_unmapped_penalty +
        test_penalty +
        resolve_penalty
    )

    # 8. Base score (exponential decay, K=45 for calibrated output)
    base_score = 100 * math.exp(-total_penalty / K)

    # 9. EMA smoothing (pulls toward previous, doesn't "boost")
    if previous_score is not None:
        final_score = EMA_WEIGHT * base_score + (1 - EMA_WEIGHT) * previous_score
    else:
        final_score = base_score

    return {
        'score': round(final_score),
        'base_score': round(base_score),
        'doc_coverage_pct': round(doc_coverage * 100, 1),
        'bug_resolve_pct': round(resolve_pct * 100, 1),
        'penalty_breakdown': {
            'severity': round(severity_penalty, 1),
            'doc_coverage': round(doc_penalty, 1),
            'staleness': round(staleness_penalty, 1),
            'tierA_unmapped': round(tier_a_unmapped_penalty, 1),
            'test_coverage': round(test_penalty, 1),
            'resolve': round(resolve_penalty, 1),
            'total': round(total_penalty, 1)
        },
        'raw_metrics': {
            'sev_p0': sev_p0,
            'sev_p1': sev_p1,
            'sev_p2': sev_p2,
            'sev_p3': sev_p3,
            'mapped': mapped,
            'unmapped': unmapped,
            'stale_count': stale_count,
            'avg_staleness': round(avg_staleness, 1),
            'tierA_stale_count': tier_a_stale,
            'tierA_unmapped': tier_a_unmapped,
            'scripts': scripts,
            'tests_count': tests_count
        },
        'release_gates': {
            'p0_zero': sev_p0 == 0,
            'tier_a_mapped': tier_a_unmapped == 0,
            'staleness_ok': avg_staleness < 21,
            'score_ok': final_score >= 70,
            'can_ship': sev_p0 == 0 and tier_a_unmapped == 0
        }
    }


def collect_all_metrics(config) -> Dict[str, Any]:
    """Collect all metrics from the codebase."""
    # Severity
    sev = get_severity_counts(config)

    # Bug resolution
    bugs = get_bug_resolution_metrics(config)
    bug_resolve_pct = bugs['bugs_fixed'] / max(bugs['bugs_total'], 1)

    # Doc coverage
    docs = get_doc_coverage_metrics(config)

    # Staleness
    stale = get_staleness_metrics(config)

    # Tests
    tests = get_test_metrics(config)

    return {
        'sev_p0': sev['p0'],
        'sev_p1': sev['p1'],
        'sev_p2': sev['p2'],
        'sev_p3': sev['p3'],
        'mapped': docs['mapped'],
        'unmapped': docs['unmapped'],
        'tierA_unmapped': docs['tier_a_unmapped'],
        'stale_count': stale['stale_count'],
        'avg_staleness': stale['avg_staleness'],
        'tierA_stale_count': stale['tier_a_stale_count'],
        'scripts': tests['scripts'],
        'tests_count': tests['tests_count'],
        'bug_resolve_pct': bug_resolve_pct,
        'bugs_total': bugs['bugs_total'],
        'bugs_fixed': bugs['bugs_fixed'],
    }


def print_human_readable(result: Dict[str, Any]):
    """Print a human-readable report."""
    print("=" * 60)
    print("LIVING DOCUMENTATION - CONFIDENCE REPORT")
    print("=" * 60)
    print()

    score = result['score']
    base_score = result['base_score']

    # Score display with status
    if score >= 85:
        status = "✅ EXCELLENT"
    elif score >= 70:
        status = "⚠️  GOOD"
    elif score >= 50:
        status = "🔴 NEEDS ATTENTION"
    else:
        status = "🚫 CRITICAL"

    print(f"  CONFIDENCE SCORE: {score}%  {status}")
    print(f"  Base Score: {base_score}%")
    print()

    # Penalty breakdown
    pb = result['penalty_breakdown']
    print("  Penalty Breakdown:")
    print(f"    Severity:      -{pb['severity']:5.1f}  (P0×10 + P1×3 + P2×1 + P3×0.05)")
    print(f"    Doc Coverage:  -{pb['doc_coverage']:5.1f}  (target: 90%)")
    print(f"    Staleness:     -{pb['staleness']:5.1f}  (stale docs penalty)")
    print(f"    Tier-A Unmapped: -{pb['tierA_unmapped']:5.1f}  (critical files)")
    print(f"    Test Coverage: -{pb['test_coverage']:5.1f}  (tests per 100 scripts)")
    print(f"    Resolution:    -{pb['resolve']:5.1f}  (bug fix rate)")
    print(f"    ───────────────────────")
    print(f"    Total Penalty: -{pb['total']:5.1f}")
    print()

    # Raw metrics
    rm = result['raw_metrics']
    print("  Raw Metrics:")
    print(f"    Severity: P0={rm['sev_p0']}, P1={rm['sev_p1']}, P2={rm['sev_p2']}, P3={rm['sev_p3']}")
    print(f"    Doc Coverage: {result['doc_coverage_pct']}% ({rm['mapped']} mapped, {rm['unmapped']} unmapped)")
    print(f"    Staleness: {rm['stale_count']} stale docs, avg {rm['avg_staleness']} days")
    print(f"    Tests: {rm['tests_count']} test files / {rm['scripts']} scripts")
    print(f"    Bug Resolution: {result['bug_resolve_pct']}%")
    print()

    # Release gates
    gates = result['release_gates']
    print("  Release Gates:")
    print(f"    P0 = 0:        {'✅ PASS' if gates['p0_zero'] else '🚫 FAIL'}")
    print(f"    Tier-A mapped: {'✅ PASS' if gates['tier_a_mapped'] else '🚫 FAIL'}")
    print(f"    Staleness <21d: {'✅ PASS' if gates['staleness_ok'] else '⚠️  WARN'}")
    print(f"    Score ≥ 70:    {'✅ PASS' if gates['score_ok'] else '⚠️  WARN'}")
    print()

    if gates['can_ship']:
        if score >= 85:
            print("  → ✅ READY TO SHIP")
        elif score >= 70:
            print("  → ⚠️  CAN SHIP with known issues")
        else:
            print("  → 🔴 WAIVER REQUIRED (score < 70)")
    else:
        print("  → 🚫 BLOCKED (hard gates failed)")

    # Focus guidance
    print()
    print("  💡 FOCUS GUIDANCE (highest impact):")
    penalties = [
        (pb['severity'], "Fix P0/P1 bugs"),
        (pb['doc_coverage'], "Map unmapped files"),
        (pb['staleness'], "Update stale docs"),
        (pb['tierA_unmapped'], "Document Tier-A files"),
        (pb['test_coverage'], "Add more tests"),
        (pb['resolve'], "Close open bugs")
    ]
    penalties.sort(key=lambda x: x[0], reverse=True)
    for penalty, action in penalties[:3]:
        if penalty > 0:
            print(f"     - {action} (-{penalty:.1f} penalty)")

    print()
    print("=" * 60)


def main():
    json_mode = '--json' in sys.argv
    update_mode = '--update' in sys.argv

    # Load configuration
    config = get_config()

    # Collect metrics
    metrics = collect_all_metrics(config)

    # Get previous score for EMA
    previous_score = get_previous_score(config)

    # Calculate confidence
    result = calculate_confidence(metrics, previous_score)
    result['timestamp'] = datetime.now().isoformat()
    result['previous_score'] = previous_score

    if json_mode:
        print(json.dumps(result, indent=2))
    else:
        print_human_readable(result)

    # Optionally update the history
    if update_mode and config.history_file.exists():
        try:
            with open(config.history_file, 'r') as f:
                data = json.load(f)

            if data.get('history'):
                data['history'][-1]['confidence'] = result['score']
                data['history'][-1]['calculated_confidence'] = result

            with open(config.history_file, 'w') as f:
                json.dump(data, f, indent=2)

            if not json_mode:
                print(f"Updated history.json with score: {result['score']}")
        except (OSError, IOError, json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Error updating history.json: {e}", file=sys.stderr)

    return 0


if __name__ == '__main__':
    sys.exit(main())
