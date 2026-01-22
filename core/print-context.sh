#!/usr/bin/env bash
# print-context.sh - Context lookup for LivingDocFramework
# Usage: ./print-context.sh <file-path>
#
# Returns tier, doc-set, and required reading for any file.
# Tier detection uses CODE_DOC_MAP.md table rows (not headings).
#
# Parsing Contract:
#   - File must be in a table row with backticks: `path/to/file`
#   - Tier extracted from same row: | A | or | B | or | C |
#   - If file not found in any CODE_DOC_MAP.md -> UNMAPPED
#
# Version: 0.2.0

set -euo pipefail

FILE="${1:-}"
if [ -z "$FILE" ]; then
    echo "Usage: print-context.sh <file-path>"
    echo ""
    echo "Looks up tier, doc-set, and required reading for any file."
    echo "Tier detection is based on CODE_DOC_MAP.md table structure."
    exit 1
fi

# Get search roots (pwd first, then git root as fallback)
# This allows both:
#   - Submodule usage: user runs from their project root
#   - Example testing: user runs from examples/doc-systems
SEARCH_ROOT="$(pwd)"
GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "")

# Convert to relative path (handle both absolute and relative input)
if [[ "$FILE" = /* ]]; then
    REL_FILE="${FILE#$SEARCH_ROOT/}"
else
    REL_FILE="$FILE"
fi

# Normalize path separators for cross-platform (Windows/Unix)
REL_FILE="${REL_FILE//\\//}"

# === SINGLE LOOKUP: Returns tier + doc-set + map file ===
# Avoids side effects and double-scanning
lookup_file() {
    local file="$1"
    local found_tier="UNMAPPED"
    local found_docset=""
    local found_map=""

    # Build list of search paths (pwd/docs first, then git root/docs if different)
    local search_paths=()
    if [ -d "$SEARCH_ROOT/docs" ]; then
        search_paths+=("$SEARCH_ROOT/docs")
    fi
    if [ -n "$GIT_ROOT" ] && [ "$GIT_ROOT" != "$SEARCH_ROOT" ] && [ -d "$GIT_ROOT/docs" ]; then
        search_paths+=("$GIT_ROOT/docs")
    fi

    # Search all CODE_DOC_MAP.md files in search paths
    for search_path in "${search_paths[@]}"; do
        while IFS= read -r map; do
            [ -z "$map" ] && continue

            # Find row containing this file (backtick-wrapped)
            local row
            row=$(grep -F "\`$file\`" "$map" 2>/dev/null || true)

            if [ -n "$row" ]; then
                found_map="$map"
                found_docset=$(dirname "$map")

                # Extract tier from row: look for | A |, | TIER A |, etc.
                if echo "$row" | grep -qiE '\|\s*(TIER\s+)?A\s*\|'; then
                    found_tier="A"
                    break 2  # Tier A takes priority, stop all searching
                elif echo "$row" | grep -qiE '\|\s*(TIER\s+)?B\s*\|'; then
                    found_tier="B"
                    # Continue searching in case Tier A exists elsewhere
                elif echo "$row" | grep -qiE '\|\s*(TIER\s+)?C\s*\|'; then
                    found_tier="C"
                else
                    # File found but no tier column - treat as mapped but untiered
                    found_tier="C"
                fi
            fi
        done < <(find "$search_path" -name "CODE_DOC_MAP.md" 2>/dev/null || true)

        # If found Tier A, we already broke out
        [ "$found_tier" = "A" ] && break
    done

    # Output as parseable key=value
    echo "tier=$found_tier"
    echo "docset=$found_docset"
    echo "map=$found_map"
}

# === EXTRACT INVARIANTS ===
list_invariants() {
    local inv_file="$1"
    if [ -f "$inv_file" ]; then
        # Match ## or ### followed by INV-XXX:
        grep -oE "^#{2,3} INV-[A-Z0-9-]+:.*$" "$inv_file" 2>/dev/null | \
            sed 's/^#* /  - /' | head -10 || true
    fi
}

# === MAIN ===

# Do the lookup once
eval "$(lookup_file "$REL_FILE")"

# Output
echo "File: $REL_FILE"

if [ "$tier" = "UNMAPPED" ]; then
    echo "Tier: UNMAPPED"
    echo "Doc-Set: (none)"
    echo ""
    echo "This file is not in any CODE_DOC_MAP.md."
    echo "Consider adding it to a doc-set."
    exit 0
fi

# Tier label
case "$tier" in
    A) echo "Tier: A (Critical)" ;;
    B) echo "Tier: B (Important)" ;;
    C) echo "Tier: C (Standard)" ;;
    *) echo "Tier: $tier" ;;
esac

# Doc-set info (make paths relative to search root)
rel_docset="${docset#$SEARCH_ROOT/}"
rel_map="${map#$SEARCH_ROOT/}"
echo "Doc-Set: $rel_docset"
echo "Map: $rel_map"
echo ""

# Required reading
echo "Required Reading:"
count=1
if [ -f "$docset/INVARIANTS.md" ]; then
    echo "  $count. $rel_docset/INVARIANTS.md"
    count=$((count + 1))
fi
if [ -f "$docset/BUG_PATTERNS.md" ]; then
    echo "  $count. $rel_docset/BUG_PATTERNS.md"
    count=$((count + 1))
fi
if [ -f "$docset/CODE_DOC_MAP.md" ]; then
    echo "  $count. $rel_docset/CODE_DOC_MAP.md"
fi

# Show invariants for Tier A
if [ "$tier" = "A" ] && [ -f "$docset/INVARIANTS.md" ]; then
    echo ""
    echo "Invariants:"
    list_invariants "$docset/INVARIANTS.md"
fi
