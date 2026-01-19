# Living Documentation Framework

Git hooks that block commits when documentation falls out of sync with code.


## The Problem

Documentation drifts.

You change code, forget to update docs, and six months later nobody knows why auth.py contains that "temporary" retry logic.

Code review catches some of it. Most slips through.


## The Solution

Link critical code to documentation. Enforce the link at commit time.

If a file is marked critical, changing it requires updating the documentation that explains what must always remain true.

Example:

    You edit src/api/auth.py (marked Tier A in CODE_DOC_MAP.md)
    You try to commit without updating invariants:

    $ git commit -m "fix auth retry"

    ERROR: Tier A file changed but INVARIANTS not updated
       Missing update: docs/api/INVARIANTS.md

The commit is blocked until you document what changed and why.

No reminders. No dashboards. No bots. Just Git enforcing rules.


## What You Get

Enforced linkage — critical files cannot change without updating their documentation.

Tiered enforcement — Tier A blocks, Tier B warns, Tier C has no enforcement.

Scales with your codebase — single mapping file for small projects, per-subsystem doc-sets for large ones.

Zero external dependencies — just Git and Bash 4+.


## Quick Start

    # Add framework
    git submodule add https://github.com/user-hash/LivingDocFramework.git

    # Create config
    cp LivingDocFramework/core/project-config.template.yaml living-doc-config.yaml

    # Create docs
    mkdir -p docs
    touch CODE_DOC_MAP.md CHANGELOG.md docs/INVARIANTS.md

    # Install hooks
    ./LivingDocFramework/hooks/install.sh

That's it. The hooks are now active.


## How It Works

1. Map files to tiers

CODE_DOC_MAP.md defines which files matter and how much:

    | File                | Tier   | Description          |
    |---------------------|--------|----------------------|
    | `src/api/auth.py`   | TIER A | Authentication logic |
    | `src/api/users.py`  | TIER B | User endpoints       |
    | `src/utils.py`      | TIER C | Utilities            |

Tier A files must be documented when changed.


2. Document invariants

Invariants capture what must always remain true.

docs/INVARIANTS.md:

    ## INV-001: Auth retry must not exceed 3 attempts

    Why: Prevents account lockout cascades during outages.
    Enforced in: src/api/auth.py:45-67

These are not tutorials. They are rules the code must respect.


3. Commit normally

The pre-commit hook checks:

- Did you change a Tier A file? INVARIANTS.md must be staged.
- Same file listed in multiple doc-sets? Block (ambiguous ownership).
- Version file and CHANGELOG mismatch? Block.
- Code changed but CHANGELOG not updated? Warn.


## Folder Structure

Small project:

    project/
    ├── living-doc-config.yaml
    ├── CODE_DOC_MAP.md
    ├── BUG_PATTERNS.md
    ├── CHANGELOG.md
    ├── docs/
    │   ├── INVARIANTS.md
    │   └── GOLDEN_PATHS.md
    └── LivingDocFramework/

Large project with doc-sets:

    project/
    ├── living-doc-config.yaml
    ├── CHANGELOG.md
    ├── docs/
    │   ├── api/
    │   │   ├── CODE_DOC_MAP.md
    │   │   ├── INVARIANTS.md
    │   │   ├── BUG_PATTERNS.md
    │   │   ├── GOLDEN_PATHS.md
    │   │   └── DECISIONS/
    │   │       ├── ADR-001.md
    │   │       └── ADR-002.md
    │   ├── database/
    │   │   ├── CODE_DOC_MAP.md
    │   │   └── ...
    │   └── global/
    │       ├── CODE_DOC_MAP.md
    │       └── ...
    └── LivingDocFramework/

Any folder containing CODE_DOC_MAP.md is a doc-set. No config needed.


## Pre-Commit Checks

    Check                                          Behavior
    -----------------------------------------------------------
    Tier A file changed, invariants not updated    Block
    File listed in multiple CODE_DOC_MAPs          Block
    Version mismatch (version file vs CHANGELOG)   Block
    Code changed, CHANGELOG not updated            Warn
    Large commit (>5 files)                        Warn


## Requirements

- Git
- Bash 4.0+ (macOS: brew install bash, Windows: Git Bash, Linux: usually satisfied)


## Why It Exists

Built for a 181K LOC codebase where manual discipline stopped working.

External reviewers read the docs first and have full context before touching code. Bug fixes reference linked invariants — no archaeology to understand constraints. Cognitive load drops because the hooks remember what's critical.

64 bug patterns. 36 invariants. 284 mapped files. All enforced at commit time.


## Documentation

- docs/CONFIG.md — configuration options
- docs/INTEGRATION.md — integrating into existing projects
- hooks/README.md — hook behavior and customization


## License

AGPL v3
