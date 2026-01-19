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

# Parse YAML (simple grep-based parser)
parse_yaml() {
    local file="$1"

    local proj_name=$(grep "^  name:" "$file" | sed 's/.*name: *"\?\([^"]*\)"\?.*/\1/' | tr -d '\n')
    [ -n "$proj_name" ] && export LDF_PROJECT_NAME="$proj_name"

    local lang=$(grep "^  language:" "$file" | sed 's/.*language: *"\?\([^"]*\)"\?.*/\1/' | tr -d '\n')
    [ -n "$lang" ] && export LDF_LANGUAGE="$lang"

    local branch=$(grep "^  main_branch:" "$file" | sed 's/.*main_branch: *"\?\([^"]*\)"\?.*/\1/' | tr -d '\n')
    [ -n "$branch" ] && export LDF_MAIN_BRANCH="$branch"

    local ver_file=$(grep "^  file:" "$file" | head -1 | sed 's/.*file: *"\?\([^"]*\)"\?.*/\1/' | tr -d '\n')
    [ -n "$ver_file" ] && export LDF_VERSION_FILE="$ver_file"

    local ver_pattern=$(grep "^  pattern:" "$file" | head -1 | sed 's/.*pattern: *"\?\([^"]*\)"\?.*/\1/' | tr -d '\n')
    [ -n "$ver_pattern" ] && export LDF_VERSION_PATTERN="$ver_pattern"

    local code_root=$(grep "^  root:" "$file" | head -1 | sed 's/.*root: *"\?\([^"]*\)"\?.*/\1/' | tr -d '\n')
    [ -n "$code_root" ] && export LDF_CODE_ROOT="$code_root"

    local test_pattern=$(grep "^  pattern:" "$file" | tail -1 | sed 's/.*pattern: *"\?\([^"]*\)"\?.*/\1/' | tr -d '\n')
    [ -n "$test_pattern" ] && export LDF_TEST_PATTERN="$test_pattern"
}

# If yq is available, use it (more robust)
if command -v yq &>/dev/null; then
    export LDF_PROJECT_NAME=$(yq eval '.project.name' "$CONFIG_FILE" 2>/dev/null || echo "MyProject")
    export LDF_LANGUAGE=$(yq eval '.project.language' "$CONFIG_FILE" 2>/dev/null || echo "python")
    export LDF_MAIN_BRANCH=$(yq eval '.project.main_branch' "$CONFIG_FILE" 2>/dev/null || echo "main")
    export LDF_VERSION_FILE=$(yq eval '.version.file' "$CONFIG_FILE" 2>/dev/null || echo "__init__.py")
    export LDF_VERSION_PATTERN=$(yq eval '.version.pattern' "$CONFIG_FILE" 2>/dev/null || echo '__version__\s*=\s*"([0-9.]+)"')
    export LDF_CODE_ROOT=$(yq eval '.code.root' "$CONFIG_FILE" 2>/dev/null || echo "src/")
    export LDF_TEST_PATTERN=$(yq eval '.tests.pattern' "$CONFIG_FILE" 2>/dev/null || echo "**/test_*.py")
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
            export LDF_CODE_EXT=$(echo "$CODE_EXTS" | cut -d',' -f1)
            export LDF_CODE_EXTS="$CODE_EXTS"
        else
            CODE_EXTS=$(grep "extensions:" "$LANG_PROFILE" | sed 's/.*\[\([^]]*\)\].*/\1/' | tr -d ' "' | tr ',' '\n' | head -1)
            export LDF_CODE_EXT="$CODE_EXTS"
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
    find "$root" -path "$LDF_TEST_PATTERN" 2>/dev/null
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
