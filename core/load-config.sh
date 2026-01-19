#!/usr/bin/env bash
# Living Documentation Framework - Configuration Loader
# Sources project configuration and exports environment variables
# Usage: source LivingDocFramework/core/load-config.sh

# Find project root (where living-doc-config.yaml exists)
find_project_root() {
    local current_dir="$PWD"
    # Handle both Unix and Windows paths
    while [ "$current_dir" != "/" ] && [ "$current_dir" != "" ]; do
        if [ -f "$current_dir/living-doc-config.yaml" ]; then
            echo "$current_dir"
            return 0
        fi
        # Check for Windows root (e.g., C:, D:)
        if [[ "$current_dir" =~ ^[A-Za-z]:/?$ ]]; then
            break
        fi
        current_dir=$(dirname "$current_dir")
    done
    # Fallback: current directory
    echo "$PWD"
}

# Export configuration as environment variables
PROJECT_ROOT=$(find_project_root)
export LDF_PROJECT_ROOT="$PROJECT_ROOT"

# Check if config exists
CONFIG_FILE="$PROJECT_ROOT/living-doc-config.yaml"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Warning: living-doc-config.yaml not found. Using defaults." >&2
    export LDF_PROJECT_NAME="MyProject"
    export LDF_LANGUAGE="python"
    export LDF_CODE_ROOT="src/"
    export LDF_CODE_EXT="py"
    export LDF_VERSION_FILE="__init__.py"
    export LDF_VERSION_PATTERN='__version__\s*=\s*"([0-9.]+)"'
    export LDF_TEST_PATTERN="**/test_*.py"
    export LDF_MAIN_BRANCH="main"
    return 0 2>/dev/null || exit 0
fi

# Parse YAML (improved grep-based parser)
# Handles flexible indentation and section-aware field extraction
parse_yaml() {
    local file="$1"

    # Helper: extract value from "key: value" or "key: "value""
    extract_value() {
        sed 's/.*: *"\?\([^"]*\)"\?.*/\1/' | tr -d '\n\r'
    }

    # Helper: get field value from a specific section
    # Usage: get_section_field "section:" "field:" file
    get_section_field() {
        local section="$1"
        local field="$2"
        local file="$3"
        # Find section, then get first matching field after it (before next section)
        awk -v section="$section" -v field="$field" '
            $0 ~ "^"section { in_section=1; next }
            in_section && /^[a-z]/ { in_section=0 }
            in_section && $0 ~ "^  "field {
                gsub(/.*: *"?/, ""); gsub(/"? *$/, ""); print; exit
            }
        ' "$file"
    }

    # Project section (unique fields - simple grep works)
    local proj_name=$(grep -E "^  name:" "$file" | head -1 | extract_value)
    [ -n "$proj_name" ] && export LDF_PROJECT_NAME="$proj_name"

    local lang=$(grep -E "^  language:" "$file" | extract_value)
    [ -n "$lang" ] && export LDF_LANGUAGE="$lang"

    local branch=$(grep -E "^  main_branch:" "$file" | extract_value)
    [ -n "$branch" ] && export LDF_MAIN_BRANCH="$branch"

    # Version section - use section-aware extraction
    local ver_file=$(get_section_field "version:" "file:" "$file")
    [ -n "$ver_file" ] && export LDF_VERSION_FILE="$ver_file"

    local ver_pattern=$(get_section_field "version:" "pattern:" "$file")
    [ -n "$ver_pattern" ] && export LDF_VERSION_PATTERN="$ver_pattern"

    # Code section
    local code_root=$(get_section_field "code:" "root:" "$file")
    [ -n "$code_root" ] && export LDF_CODE_ROOT="$code_root"

    # Tests section
    local test_pattern=$(get_section_field "tests:" "pattern:" "$file")
    [ -n "$test_pattern" ] && export LDF_TEST_PATTERN="$test_pattern"
}

# Helper: get yq value or default (yq returns "null" string for missing keys)
yq_get() {
    local result
    result=$(yq eval "$1" "$CONFIG_FILE" 2>/dev/null)
    if [ -z "$result" ] || [ "$result" = "null" ]; then
        echo "$2"
    else
        echo "$result"
    fi
}

# If yq is available, use it (more robust)
if command -v yq &>/dev/null; then
    export LDF_PROJECT_NAME=$(yq_get '.project.name' "MyProject")
    export LDF_LANGUAGE=$(yq_get '.project.language' "python")
    export LDF_MAIN_BRANCH=$(yq_get '.project.main_branch' "main")
    export LDF_VERSION_FILE=$(yq_get '.version.file' "__init__.py")
    export LDF_VERSION_PATTERN=$(yq_get '.version.pattern' '__version__\s*=\s*"([0-9.]+)"')
    export LDF_CODE_ROOT=$(yq_get '.code.root' "src/")
    export LDF_TEST_PATTERN=$(yq_get '.tests.pattern' "**/test_*.py")
else
    parse_yaml "$CONFIG_FILE" ""
fi

# Load language profile defaults
if [ -n "$LDF_LANGUAGE" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    LANG_PROFILE="$SCRIPT_DIR/languages/$LDF_LANGUAGE.yaml"

    if [ -f "$LANG_PROFILE" ]; then
        if command -v yq &>/dev/null; then
            CODE_EXTS=$(yq eval '.code.extensions | join(",")' "$LANG_PROFILE" 2>/dev/null)
            [ "$CODE_EXTS" = "null" ] && CODE_EXTS=""
        else
            # Extract extensions from YAML array: ["py", "pyw"] -> py,pyw
            CODE_EXTS=$(grep "extensions:" "$LANG_PROFILE" | sed 's/.*\[\([^]]*\)\].*/\1/' | tr -d ' "')
        fi
        if [ -n "$CODE_EXTS" ]; then
            export LDF_CODE_EXTS="$CODE_EXTS"
            export LDF_CODE_EXT=$(echo "$CODE_EXTS" | cut -d',' -f1)
        fi
    fi
fi

# Default values if not set
: ${LDF_CODE_EXT:="py"}
: ${LDF_TEST_EXT:="$LDF_CODE_EXT"}
: ${LDF_PROJECT_NAME:="MyProject"}
: ${LDF_LANGUAGE:="python"}
: ${LDF_CODE_ROOT:="src/"}
: ${LDF_MAIN_BRANCH:="main"}

# Document paths (configurable via env vars)
export LDF_CHANGELOG="${LDF_CHANGELOG:-CHANGELOG.md}"
export LDF_BUG_PATTERNS="${LDF_BUG_PATTERNS:-BUG_PATTERNS.md}"
export LDF_GOLDEN_PATHS="${LDF_GOLDEN_PATHS:-docs/GOLDEN_PATHS.md}"
export LDF_INVARIANTS="${LDF_INVARIANTS:-docs/INVARIANTS.md}"
export LDF_CODE_DOC_MAP="${LDF_CODE_DOC_MAP:-CODE_DOC_MAP.md}"

# Debug output
if [ "${LDF_DEBUG:-0}" = "1" ]; then
    echo "Living Documentation Framework Configuration:" >&2
    echo "  Project: $LDF_PROJECT_NAME" >&2
    echo "  Language: $LDF_LANGUAGE" >&2
    echo "  Code Root: $LDF_CODE_ROOT" >&2
    echo "  Code Extension: $LDF_CODE_EXT" >&2
fi

# Helper functions
ldf_find_code() {
    local root="${1:-$LDF_CODE_ROOT}"
    find "$root" -name "*.${LDF_CODE_EXT}" 2>/dev/null
}

ldf_find_tests() {
    local root="${1:-$LDF_CODE_ROOT}"
    # Note: -name works for simple patterns like "test_*.py"
    # For complex patterns, users should use their own find/glob
    local pattern=$(basename "$LDF_TEST_PATTERN")
    find "$root" -name "$pattern" 2>/dev/null
}

export -f ldf_find_code 2>/dev/null || true
export -f ldf_find_tests 2>/dev/null || true

# =============================================================================
# DOC-SET DISCOVERY HELPERS
# A "doc-set" is any folder under docs/ containing CODE_DOC_MAP.md
# =============================================================================

# Find all doc-sets (folders with CODE_DOC_MAP.md)
ldf_find_doc_sets() {
    find "$LDF_PROJECT_ROOT/docs" -name "CODE_DOC_MAP.md" -exec dirname {} \; 2>/dev/null
}

# Safer alternative using while-read pattern (handles spaces in paths)
ldf_find_doc_sets_safe() {
    while IFS= read -r map; do
        dirname "$map"
    done < <(find "$LDF_PROJECT_ROOT/docs" -name "CODE_DOC_MAP.md" 2>/dev/null)
}

# Get doc-set name from path (e.g., "docs/multiplayer" -> "multiplayer")
ldf_doc_set_name() {
    local path="$1"
    basename "$path"
}

# Check if a doc-set exists by name
ldf_has_doc_set() {
    local name="$1"
    [ -f "$LDF_PROJECT_ROOT/docs/$name/CODE_DOC_MAP.md" ]
}

# List all doc-set names
ldf_list_doc_sets() {
    ldf_find_doc_sets | while IFS= read -r path; do
        basename "$path"
    done
}

export -f ldf_find_doc_sets 2>/dev/null || true
export -f ldf_find_doc_sets_safe 2>/dev/null || true
export -f ldf_doc_set_name 2>/dev/null || true
export -f ldf_has_doc_set 2>/dev/null || true
export -f ldf_list_doc_sets 2>/dev/null || true
