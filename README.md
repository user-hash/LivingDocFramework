# Living Documentation Framework

**Version:** v1.0.0 | **Status:** Production Ready | **License:** MIT

> Documentation that enforces its own correctness.

A governance layer for AI-assisted software development where understanding, intent, and architecture persist across sessions, agents, and team changes.

---

## The 30-Second Version

**Problem:** AI agents lose context between sessions. Bugs reappear. Documentation drifts. Critical files get broken.

**Solution:** This framework makes documentation *enforceable*. If code changes, docs must change too — or the commit is blocked.

```
Code change without doc update? → Blocked.
Tier A file edited without invariant citation? → Blocked.
Bug fixed without pattern documented? → Warning.
```

**Result:** 93% system confidence maintained across 6 months and 181K lines of code.

---

## Why Not Just Use MCP / RALPH / Context Files?

| Approach | What It Does | Limitation |
|----------|--------------|------------|
| **MCP Servers** | Connect AI to external tools/data | No enforcement. AI can ignore context. |
| **RALPH / Memory Systems** | Store conversation history | Memory without governance. No blocking. |
| **Context Files (.claude, AGENTS.md)** | Provide static context to AI | Read-only. No validation. Drifts silently. |
| **Living Documentation** | **Enforce documentation as code** | Requires initial setup investment |

### The Key Difference

Other tools operate at the **prompt level** — they give AI more context.

This framework operates at the **commit level** — it prevents bad changes from entering the codebase.

```
MCP/RALPH: "Here's context, please use it" (advisory)
Living Docs: "You cannot commit without updating docs" (enforced)
```

### Why This Matters

- **Session-resistant**: Context survives session boundaries because it's in git, not memory
- **Agent-resistant**: Works regardless of which AI model or version you use
- **Turnover-resistant**: New team members (human or AI) inherit documented decisions
- **Drift-resistant**: Stale documentation automatically degrades confidence scores

---

## What This Framework Does

### Treats Understanding as a First-Class Artifact

| Instead of... | This framework creates... |
|---------------|--------------------------|
| Bugs that reappear | **Bug Patterns** — documented anti-patterns with detection rules |
| Tribal knowledge | **Invariants** — codified safety rules that block violations |
| "Why did we do this?" | **Decisions** — recorded rationale with context |
| Fragile critical files | **Tier A Protection** — enforced review for core code |
| Stale documentation | **Confidence Scoring** — measurable documentation health |

### Enforces at Commit Time

```bash
# What happens when you commit:

✓ Check: Are Tier A files documented?
✓ Check: Is CHANGELOG updated?
✓ Check: Do invariants have citations?
⚠ Warn: Blast radius > 5 files
✗ Block: Missing required documentation
```

---

## Who This Is For

### Solo Developers
- Stop re-debugging the same issues
- Build a knowledge base that compounds over time
- AI assistants become more effective with documented context

### Teams
- Onboard new developers (human or AI) faster
- Reduce "why did we do this?" questions
- Enforce consistency without constant code review

### Enterprises
- Auditable documentation trail
- Measurable system health metrics
- Governance that scales with codebase size

### AI-Heavy Workflows
- Multi-agent systems maintain coherence
- Context persists across session boundaries
- Agents cite invariants, not just code

---

## What's Included

### Core System (17 files)
- **4 JSON Schemas**: Patterns, golden paths, invariants, decisions
- **4 Markdown Templates**: Structured documentation formats
- **2 Manifests**: `manifest.yaml`, `doc-system.yaml`
- **5 Language Profiles**: Python, JavaScript, Go, Rust, C#
- **Configuration Loaders**: Shell + Python

### Automation
- **`calculate_confidence.py`**: Exponential-decay health scoring
- **14 additional tools**: Documented with extraction guide

### Git Hooks
- **`pre-commit`**: Documentation enforcement
- **`post-commit`**: Auto-updates
- **`commit-msg`**: Message validation
- **`install.sh`**: One-command setup

### Protocols
- **`AGENT_PROTOCOL.md`**: Mandatory AI compliance rules
- **Slash commands**: `/living-docs`, `/bug-fix`, `/code-review`

---

## Quick Start

```bash
# 1. Add to your project
git submodule add https://github.com/YOUR_USERNAME/LivingDocFramework.git

# 2. Configure
cp LivingDocFramework/core/project-config.template.yaml living-doc-config.yaml
# Edit living-doc-config.yaml for your project

# 3. Install hooks
./LivingDocFramework/hooks/install.sh

# 4. Initialize documentation
mkdir -p docs
touch CHANGELOG.md BUG_TRACKER.md
cp LivingDocFramework/core/templates/bug-patterns.template.md BUG_PATTERNS.md
touch docs/INVARIANTS.md docs/GOLDEN_PATHS.md docs/DECISIONS.md docs/CODE_DOC_MAP.md

# 5. Check health
python3 LivingDocFramework/tools/calculate_confidence.py
```

See [SETUP.md](SETUP.md) for detailed configuration.

---

## Key Features

### 1. Language-Agnostic
Works with Python, JavaScript, Go, Rust, C#, or any language. Configuration uses placeholders — no hardcoded paths.

```yaml
project:
  name: "MyProject"
  language: "python"
code:
  root: "src/"
  extensions: ["py"]
```

### 2. Automatic Enforcement
Git hooks block commits that violate documentation rules:
- Tier A files require invariant citations
- Code changes require CHANGELOG updates
- Blast-radius warnings for large changes

### 3. AI Agent Compliance
Agents are treated as contributors, not exceptions:
- Must read required docs before changes
- Must update docs after changes
- Must cite invariants for critical files
- Must provide proof-of-compliance in reports

### 4. Confidence Scoring
Measurable health signal using exponential decay:
- Bug severity (P0–P3)
- Documentation coverage and staleness
- Tier A file protection
- Test coverage and bug resolution rate

### 5. Scalable Organization
Subsystems maintain their own documentation:
- Multiplayer subsystem → 17 specialized docs
- Audio subsystem → 8 specialized docs
- No monolithic documentation blob

---

## Proven in Production

Extracted from the **Nebulae project**:

| Metric | Value |
|--------|-------|
| Lines of Code | 181,048 |
| Script Files | 284 |
| Bug Patterns Documented | 64 |
| Enforced Invariants | 36 |
| System Confidence | 93% |
| Production Use | 6+ months |

---

## Limitations & Hard Lessons

### The Honest Truth: AI Agents Don't Always Follow Protocols

Even with explicit instructions, AI coders frequently:
- Skip reading required docs before making changes
- "Forget" to update documentation after code changes
- Create bug patterns for issues that were already fixed
- Ignore invariant citation requirements
- Provide superficial "proof of compliance" checklists

**This framework helps, but it doesn't solve the problem completely.**

### Failure Modes We've Encountered

| Problem | Frequency | Impact |
|---------|-----------|--------|
| Agent skips doc reading | Common | Makes changes that violate invariants |
| Agent "verifies" without actually checking | Common | Reports bugs that don't exist in current code |
| Agent updates docs superficially | Occasional | Documentation technically updated but unhelpful |
| Agent ignores Tier A warnings | Occasional | Critical files modified without proper review |
| Sub-agents lose protocol context | Common | Task tool spawns agents without governance |

### Safeguards We've Implemented

**For Claude / Primary AI Coder:**
1. **Pre-flight checklists** in AGENT_PROTOCOL.md — explicit "STOP" before proceeding
2. **Mandatory report format** — forces structure even if content is weak
3. **Git hooks as hard blocks** — can't commit without docs (catches what AI missed)
4. **Confidence decay** — stale docs automatically hurt the score (visible consequence)

**For Sub-Agents (Task tool):**
1. **Protocol injection** — AGENT_PROTOCOL block must be included in every agent prompt
2. **Verification requirements** — agents must prove they checked current code, not cached
3. **Proof of compliance section** — mandatory in all agent reports
4. **Escalation path** — if agent returns without docs, don't commit

**For Humans:**
1. **Dashboard visibility** — see confidence score trends over time
2. **Blast radius warnings** — know when changes are high-risk
3. **CODE_DOC_MAP** — single source of truth for what needs what docs

### What Still Doesn't Work Well

- **Agents still skip docs** — protocols are advisory until git hooks catch them
- **Verification is shallow** — agents check boxes without deep verification
- **Context window limits** — large codebases can't fit all relevant docs
- **No runtime enforcement** — only catches issues at commit time
- **Human discipline required** — someone must review agent compliance reports

### Our Recommendation

```
Don't trust. Verify.
```

1. **Review agent reports** — actually read the "proof of compliance"
2. **Spot-check doc updates** — are they meaningful or checkbox-filling?
3. **Run confidence scoring regularly** — watch for unexpected drops
4. **Use git hooks as safety net** — they catch what protocols miss

This framework raises the floor, not the ceiling. It makes careless mistakes harder, but doesn't guarantee careful work.

---

## Documentation

| Document | Description |
|----------|-------------|
| [SETUP.md](SETUP.md) | Installation & configuration |
| [Hooks README](hooks/README.md) | Git hook system |
| [Agent Protocol](protocols/AGENT_PROTOCOL.md) | AI agent compliance rules |
| [Commands README](commands/README.md) | Slash command reference |
| [Tools README](tools/README.md) | Tool documentation & extraction |
| [Examples](examples/) | Sample project configurations |

---

## Requirements

**Minimum:** Git, Bash 4.0+, Python 3.8+

**Recommended:** jq, yq, AI coding assistant

---

## Roadmap

- [ ] Extract remaining 13 tools
- [ ] JavaScript/TypeScript example
- [ ] Go example
- [ ] Automated test suite
- [ ] CI/CD integration examples
- [ ] Web-based dashboard viewer

---

## License

MIT License — see [LICENSE](LICENSE)

---

## Acknowledgments

- **Nebulae Project** — original source (181K LOC Unity project)
- **Claude AI** — development partner
- **Living Documentation community** — inspiration and feedback

---

## Support

- **Issues**: [GitHub Issues](https://github.com/user/living-doc-framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/user/living-doc-framework/discussions)

---

*Transform scattered context into enforced understanding.*
