# Glossary


## Doc-Set

Folder containing `CODE_DOC_MAP.md`. Example: `docs/api/`


## Tier A

Files that BLOCK commits without doc updates. Example: `src/api/auth.py`


## Tier B

Files that WARN without doc updates. Example: `src/api/users.py`


## Tier C

Files with no enforcement. Example: `src/utils.py`


## Invariant

Rule that must always hold. Example: `INV-AUTH-001: Retry attempts must be bounded.`


## CODE_DOC_MAP.md

Maps files to tiers. Presence defines a doc-set.


## INVARIANTS.md

Safety rules. Required for Tier A enforcement.


## BUG_PATTERNS.md

Documented bugs with prevention. Example: `BUG-DB-003: Pool exhaustion under load.`
