# Doc-Systems Example

A minimal testbed demonstrating:
- Tier A/B/C file classification
- Doc-set structure
- print-context.sh behavior

## Structure

```
doc-systems/
├── src/
│   ├── api/auth.py         # Tier A (Critical)
│   └── storage/adapter.py  # Tier B (Important)
└── docs/
    ├── api/
    │   ├── CODE_DOC_MAP.md
    │   └── INVARIANTS.md
    └── storage/
        ├── CODE_DOC_MAP.md
        └── INVARIANTS.md
```

## Testing print-context.sh

From this directory:

```bash
# Tier A file
../../core/print-context.sh src/api/auth.py

# Expected output:
# File: src/api/auth.py
# Tier: A (Critical)
# Doc-Set: docs/api
# ...

# Tier B file
../../core/print-context.sh src/storage/adapter.py

# Expected output:
# File: src/storage/adapter.py
# Tier: B (Important)
# Doc-Set: docs/storage
# ...

# Unmapped file
../../core/print-context.sh src/utils.py

# Expected output:
# File: src/utils.py
# Tier: UNMAPPED
# Doc-Set: (none)
# ...
```

## CODE_DOC_MAP.md Format

The parsing contract requires:
- File paths in backticks: `` `src/api/auth.py` ``
- Tier in same row: `| A |` or `| B |` or `| C |`
- Standard Markdown table format
