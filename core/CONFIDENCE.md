# Confidence Scoring Methodology

**Version:** 1.0.0

> A 2-layer explainable scoring system that measures project health objectively.

---

## Overview

Traditional project health is measured by vibes: "Feels stable" or "Seems buggy." This framework provides **objective, explainable confidence scoring** that:

1. **Quantifies health** - A number (0-100%) that means something
2. **Explains factors** - Know exactly why the score changed
3. **Tracks trends** - See improvement or degradation over time
4. **Separates concerns** - Code issues vs knowledge gaps

---

## 2-Layer Scoring Model

```
┌─────────────────────────────────────────────────────────────────┐
│                      OVERALL CONFIDENCE                          │
│                          (0-100%)                                │
│                                                                  │
│  ┌─────────────────────────────┬─────────────────────────────┐  │
│  │      CODE HEALTH (60%)      │   KNOWLEDGE HEALTH (40%)    │  │
│  │                             │                             │  │
│  │  • Open bugs (-severity)    │  • Invariant coverage (+)   │  │
│  │  • Unprotected files (-)    │  • Pattern documentation (+)│  │
│  │  • Test coverage gaps (-)   │  • ADR completeness (+)     │  │
│  │  • Regression rate (-)      │  • Doc freshness (-)        │  │
│  │  • Build status (-)         │  • Tier A coverage (+)      │  │
│  │                             │                             │  │
│  └─────────────────────────────┴─────────────────────────────┘  │
│                                                                  │
│                 OVERALL = (CH × 0.6) + (KH × 0.4)                │
└─────────────────────────────────────────────────────────────────┘
```

**Why 60/40?** Code issues cause immediate user-facing problems. Knowledge gaps cause slower degradation through accumulated technical debt. The weighting reflects urgency of impact.

---

## Layer 1: Code Health (60%)

Measures runtime risk factors that directly affect users.

### Factors

| Factor | Impact | Calculation |
|--------|--------|-------------|
| **Open Bugs** | Variable | P1: -15 each, P2: -8 each, P3: -3 each |
| **Unprotected Tier A** | -5 each | Tier A files without invariant coverage |
| **Test Coverage Gaps** | -10 each | Tier A files without test coverage |
| **Regression Rate** | -20 if >10% | Bugs that reappeared after being fixed |
| **Build Failures** | -25 | Any failing CI checks |
| **Security Issues** | -30 each | Known vulnerabilities |

### Formula

```
CodeHealth = max(0, 100 - Σ(bug_penalties) - Σ(protection_penalties) - Σ(other_penalties))
```

### Example Calculation

```
Starting: 100

Open Bugs:
  - 1 P1 bug: -15
  - 2 P2 bugs: -16
  - 5 P3 bugs: -15

Unprotected Tier A:
  - 2 files without invariants: -10

Test Gaps:
  - 1 file without tests: -10

CodeHealth = 100 - 15 - 16 - 15 - 10 - 10 = 34%
```

---

## Layer 2: Knowledge Health (40%)

Measures cognitive coverage that prevents future issues.

### Factors

| Factor | Impact | Calculation |
|--------|--------|-------------|
| **Invariant Coverage** | +2 each | Files protected by invariants |
| **Pattern Documentation** | +1 each | Documented bug patterns |
| **ADR Completeness** | +0.5 each | Architecture decisions recorded |
| **Golden Paths** | +1.5 each | Documented proven patterns |
| **Doc Freshness** | -5 each | Documents stale >7 days |
| **Cross-References** | +0.5 each | Links between code and docs |

### Formula

```
KnowledgeHealth = min(100, Σ(coverage_bonuses) - Σ(staleness_penalties))
```

### Example Calculation

```
Invariant Coverage:
  - 15 Tier A files protected: +30

Pattern Documentation:
  - 96 patterns documented: +96 (capped at +50)

ADR Completeness:
  - 15 ADRs: +7.5

Golden Paths:
  - 10 golden paths: +15

Doc Freshness:
  - 3 stale documents: -15

KnowledgeHealth = 30 + 50 + 7.5 + 15 - 15 = 87.5%
```

---

## Overall Confidence

```
Overall = (CodeHealth × 0.6) + (KnowledgeHealth × 0.4)
        = (34 × 0.6) + (87.5 × 0.4)
        = 20.4 + 35
        = 55.4%
```

---

## Confidence Levels

| Score | Level | Meaning |
|-------|-------|---------|
| 90-100% | Excellent | Production ready, well documented |
| 75-89% | Good | Stable, minor gaps |
| 60-74% | Fair | Usable but accumulating debt |
| 40-59% | Concerning | Active issues, risky changes |
| <40% | Critical | Major problems, avoid changes |

---

## Trend Analysis

Track confidence over time to detect patterns:

```python
from confidence_tracker import get_trend

trend = get_trend(days=7)
# Returns:
# {
#   "direction": "improving",  # or "declining", "stable"
#   "delta": +3.2,
#   "datapoints": [
#     {"date": "2024-01-05", "score": 88.1},
#     {"date": "2024-01-06", "score": 89.5},
#     {"date": "2024-01-07", "score": 91.3}
#   ]
# }
```

### Trend Triggers

| Condition | Alert |
|-----------|-------|
| 3 consecutive declines | Warning: degrading health |
| Drop >10% in single session | Alert: significant regression |
| Below 60% for >3 days | Critical: intervention needed |
| Improvement after bug fix | Positive: verify fix worked |

---

## Explainability

Every score change comes with explanation:

```json
{
  "overall": 94.1,
  "previous": 91.2,
  "change": "+2.9",
  "reason": "Bug fix reduced penalties",
  "factors": [
    {"factor": "P2 bug fixed", "impact": "+8"},
    {"factor": "Pattern added", "impact": "+1"},
    {"factor": "Doc went stale", "impact": "-5"},
    {"factor": "Invariant added", "impact": "+2"}
  ]
}
```

This enables:
- Understanding why score changed
- Prioritizing what to fix
- Validating that fixes worked
- Communicating health to stakeholders

---

## Dashboard Integration

Confidence is visualized in the dashboard:

```
┌──────────────────────────────────────┐
│  CONFIDENCE: 94.1%                   │
│  ████████████████████░░░░            │
│                                      │
│  Code Health:      92.0%             │
│  ████████████████████░░░░            │
│                                      │
│  Knowledge Health: 97.3%             │
│  █████████████████████░░░            │
│                                      │
│  Trend: +2.9% (7 days)               │
│  ↗ Improving                         │
└──────────────────────────────────────┘
```

---

## Customization

Adjust weights and penalties in config:

```json
// .claude/devmemory/config.json
{
  "confidence": {
    "code_health_weight": 0.6,
    "knowledge_health_weight": 0.4,
    "bug_penalties": {
      "P1": 15,
      "P2": 8,
      "P3": 3
    },
    "coverage_bonuses": {
      "invariant": 2,
      "pattern": 1,
      "adr": 0.5,
      "golden_path": 1.5
    },
    "staleness_penalty": 5,
    "staleness_threshold_days": 7
  }
}
```

---

## Implementation Example

```python
class ConfidenceTracker:
    def calculate(self) -> ConfidenceScore:
        code_health = self._calculate_code_health()
        knowledge_health = self._calculate_knowledge_health()

        overall = (
            code_health * self.config.code_health_weight +
            knowledge_health * self.config.knowledge_health_weight
        )

        return ConfidenceScore(
            overall=overall,
            code_health=code_health,
            knowledge_health=knowledge_health,
            factors=self._get_factors()
        )

    def _calculate_code_health(self) -> float:
        score = 100

        # Bug penalties
        for bug in self.bugs.open:
            score -= self.config.bug_penalties[bug.severity]

        # Protection penalties
        for file in self.tier_a_files:
            if not file.has_invariant:
                score -= 5
            if not file.has_tests:
                score -= 10

        return max(0, score)

    def _calculate_knowledge_health(self) -> float:
        score = 0

        # Coverage bonuses
        score += len(self.invariants) * 2
        score += min(len(self.patterns), 50)  # Cap at 50
        score += len(self.adrs) * 0.5
        score += len(self.golden_paths) * 1.5

        # Staleness penalties
        for doc in self.stale_docs:
            score -= 5

        return min(100, score)
```

---

## Best Practices

1. **Track regularly** - Calculate after every session
2. **Investigate drops** - Don't ignore declining scores
3. **Celebrate improvements** - Positive reinforcement matters
4. **Tune weights** - Adjust to match your project's priorities
5. **Export for stakeholders** - Share health metrics externally

---

## Related Documentation

- [DEVMEMORY.md](DEVMEMORY.md) - Memory system architecture
- [../hooks/LIFECYCLE.md](../hooks/LIFECYCLE.md) - When confidence updates
- [../protocols/MANIFEST.md](../protocols/MANIFEST.md) - Configuration
