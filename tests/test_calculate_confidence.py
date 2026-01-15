#!/usr/bin/env python3
"""
Tests for the Living Documentation Framework confidence calculator.
"""

import sys
import math
from pathlib import Path

import pytest

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'tools'))

from calculate_confidence import (
    calculate_confidence,
    K,
    EMA_WEIGHT,
)


class TestCalculateConfidence:
    """Tests for calculate_confidence function."""

    def test_perfect_score(self):
        """Test that perfect metrics yield a high score."""
        metrics = {
            'sev_p0': 0,
            'sev_p1': 0,
            'sev_p2': 0,
            'sev_p3': 0,
            'mapped': 100,
            'unmapped': 0,
            'stale_count': 0,
            'avg_staleness': 0,
            'tierA_stale_count': 0,
            'tierA_unmapped': 0,
            'scripts': 100,
            'tests_count': 100,
            'bug_resolve_pct': 1.0,
        }

        result = calculate_confidence(metrics)

        # Perfect score should be 100 (or very close)
        assert result['score'] >= 95
        assert result['base_score'] >= 95

    def test_p0_penalty(self):
        """Test that P0 bugs heavily penalize the score."""
        # Baseline without P0
        baseline_metrics = {
            'sev_p0': 0,
            'sev_p1': 0,
            'sev_p2': 0,
            'sev_p3': 0,
            'mapped': 100,
            'unmapped': 0,
            'stale_count': 0,
            'avg_staleness': 0,
            'tierA_stale_count': 0,
            'tierA_unmapped': 0,
            'scripts': 100,
            'tests_count': 100,
            'bug_resolve_pct': 1.0,
        }

        # With 1 P0
        p0_metrics = baseline_metrics.copy()
        p0_metrics['sev_p0'] = 1

        baseline_result = calculate_confidence(baseline_metrics)
        p0_result = calculate_confidence(p0_metrics)

        # P0 should significantly drop the score (P0 weight is 10)
        assert p0_result['score'] < baseline_result['score']
        assert p0_result['penalty_breakdown']['severity'] >= 10

    def test_severity_penalty_cap(self):
        """Test that severity penalty is capped at 40."""
        metrics = {
            'sev_p0': 10,  # Would be 100 without cap
            'sev_p1': 10,  # Would be 30 without cap
            'sev_p2': 100, # Would be 100 without cap
            'sev_p3': 1000,
            'mapped': 100,
            'unmapped': 0,
            'stale_count': 0,
            'avg_staleness': 0,
            'tierA_stale_count': 0,
            'tierA_unmapped': 0,
            'scripts': 100,
            'tests_count': 100,
            'bug_resolve_pct': 1.0,
        }

        result = calculate_confidence(metrics)

        # Severity penalty should be capped at 40
        assert result['penalty_breakdown']['severity'] == 40

    def test_doc_coverage_penalty(self):
        """Test documentation coverage penalty."""
        # 50% coverage
        metrics = {
            'sev_p0': 0,
            'sev_p1': 0,
            'sev_p2': 0,
            'sev_p3': 0,
            'mapped': 50,
            'unmapped': 50,
            'stale_count': 0,
            'avg_staleness': 0,
            'tierA_stale_count': 0,
            'tierA_unmapped': 0,
            'scripts': 100,
            'tests_count': 100,
            'bug_resolve_pct': 1.0,
        }

        result = calculate_confidence(metrics)

        # Should have doc coverage penalty (target is 90%)
        assert result['penalty_breakdown']['doc_coverage'] > 0
        assert result['doc_coverage_pct'] == 50.0

    def test_staleness_penalty(self):
        """Test staleness penalty calculation."""
        metrics = {
            'sev_p0': 0,
            'sev_p1': 0,
            'sev_p2': 0,
            'sev_p3': 0,
            'mapped': 100,
            'unmapped': 0,
            'stale_count': 5,
            'avg_staleness': 30,
            'tierA_stale_count': 2,
            'tierA_unmapped': 0,
            'scripts': 100,
            'tests_count': 100,
            'bug_resolve_pct': 1.0,
        }

        result = calculate_confidence(metrics)

        # Should have staleness penalty
        assert result['penalty_breakdown']['staleness'] > 0

    def test_ema_smoothing(self):
        """Test EMA smoothing with previous score."""
        metrics = {
            'sev_p0': 0,
            'sev_p1': 0,
            'sev_p2': 0,
            'sev_p3': 0,
            'mapped': 100,
            'unmapped': 0,
            'stale_count': 0,
            'avg_staleness': 0,
            'tierA_stale_count': 0,
            'tierA_unmapped': 0,
            'scripts': 100,
            'tests_count': 100,
            'bug_resolve_pct': 1.0,
        }

        # Calculate without previous score
        result_no_ema = calculate_confidence(metrics)

        # Calculate with lower previous score
        result_with_ema = calculate_confidence(metrics, previous_score=50)

        # EMA should pull score toward previous
        # final = EMA_WEIGHT * base + (1 - EMA_WEIGHT) * previous
        expected = EMA_WEIGHT * result_no_ema['base_score'] + (1 - EMA_WEIGHT) * 50
        assert abs(result_with_ema['score'] - round(expected)) <= 1

    def test_release_gates(self):
        """Test release gates calculation."""
        # Perfect metrics - all gates should pass
        good_metrics = {
            'sev_p0': 0,
            'sev_p1': 0,
            'sev_p2': 0,
            'sev_p3': 0,
            'mapped': 100,
            'unmapped': 0,
            'stale_count': 0,
            'avg_staleness': 0,
            'tierA_stale_count': 0,
            'tierA_unmapped': 0,
            'scripts': 100,
            'tests_count': 100,
            'bug_resolve_pct': 1.0,
        }

        result = calculate_confidence(good_metrics)

        assert result['release_gates']['p0_zero'] is True
        assert result['release_gates']['tier_a_mapped'] is True
        assert result['release_gates']['staleness_ok'] is True
        assert result['release_gates']['can_ship'] is True

    def test_release_gates_blocked(self):
        """Test that P0 bugs block shipping."""
        blocked_metrics = {
            'sev_p0': 1,  # This blocks shipping
            'sev_p1': 0,
            'sev_p2': 0,
            'sev_p3': 0,
            'mapped': 100,
            'unmapped': 0,
            'stale_count': 0,
            'avg_staleness': 0,
            'tierA_stale_count': 0,
            'tierA_unmapped': 0,
            'scripts': 100,
            'tests_count': 100,
            'bug_resolve_pct': 1.0,
        }

        result = calculate_confidence(blocked_metrics)

        assert result['release_gates']['p0_zero'] is False
        assert result['release_gates']['can_ship'] is False

    def test_raw_metrics_returned(self):
        """Test that raw metrics are included in result."""
        metrics = {
            'sev_p0': 1,
            'sev_p1': 2,
            'sev_p2': 3,
            'sev_p3': 4,
            'mapped': 50,
            'unmapped': 50,
            'stale_count': 1,
            'avg_staleness': 10,
            'tierA_stale_count': 0,
            'tierA_unmapped': 1,
            'scripts': 100,
            'tests_count': 10,
            'bug_resolve_pct': 0.8,
        }

        result = calculate_confidence(metrics)

        # Check raw metrics are returned
        assert result['raw_metrics']['sev_p0'] == 1
        assert result['raw_metrics']['sev_p1'] == 2
        assert result['raw_metrics']['mapped'] == 50
        assert result['raw_metrics']['unmapped'] == 50

    def test_exponential_decay_formula(self):
        """Test the exponential decay formula directly."""
        # With zero penalty, score should be 100
        metrics_zero_penalty = {
            'sev_p0': 0, 'sev_p1': 0, 'sev_p2': 0, 'sev_p3': 0,
            'mapped': 100, 'unmapped': 0,
            'stale_count': 0, 'avg_staleness': 0, 'tierA_stale_count': 0,
            'tierA_unmapped': 0, 'scripts': 100, 'tests_count': 100,
            'bug_resolve_pct': 1.0,
        }

        result = calculate_confidence(metrics_zero_penalty)

        # Base score = 100 * e^(-0/K) = 100 * e^0 = 100
        assert result['base_score'] == 100


class TestPenaltyCalculations:
    """Tests for individual penalty calculations."""

    def test_test_coverage_penalty(self):
        """Test that low test coverage incurs penalty."""
        # No tests
        no_tests = {
            'sev_p0': 0, 'sev_p1': 0, 'sev_p2': 0, 'sev_p3': 0,
            'mapped': 100, 'unmapped': 0,
            'stale_count': 0, 'avg_staleness': 0, 'tierA_stale_count': 0,
            'tierA_unmapped': 0,
            'scripts': 100,
            'tests_count': 0,  # No tests
            'bug_resolve_pct': 1.0,
        }

        result = calculate_confidence(no_tests)

        # Should have test coverage penalty
        assert result['penalty_breakdown']['test_coverage'] > 0

    def test_bug_resolution_penalty(self):
        """Test that low bug resolution rate incurs penalty."""
        low_resolve = {
            'sev_p0': 0, 'sev_p1': 0, 'sev_p2': 0, 'sev_p3': 0,
            'mapped': 100, 'unmapped': 0,
            'stale_count': 0, 'avg_staleness': 0, 'tierA_stale_count': 0,
            'tierA_unmapped': 0,
            'scripts': 100, 'tests_count': 100,
            'bug_resolve_pct': 0.5,  # Only 50% resolved
        }

        result = calculate_confidence(low_resolve)

        # Should have resolution penalty (threshold is 70%)
        assert result['penalty_breakdown']['resolve'] > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
