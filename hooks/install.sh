#!/usr/bin/env bash
# Living Documentation Framework - Hook Installer
# Installs git hooks for documentation validation.
# Run from project root: ./LivingDocFramework/hooks/install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMEWORK_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_ROOT="$(pwd)"
GIT_HOOKS_DIR="$PROJECT_ROOT/.git/hooks"

echo "Living Documentation Framework - Hook Installer"
echo "==============================================="
echo ""
echo "Framework: $FRAMEWORK_ROOT"
echo "Project:   $PROJECT_ROOT"
echo ""

# Check if .git directory exists
if [ ! -d "$PROJECT_ROOT/.git" ]; then
    echo "Error: Not a git repository"
    echo "Run this script from your project root directory"
    exit 1
fi

# Check if living-doc-config.yaml exists
if [ ! -f "$PROJECT_ROOT/living-doc-config.yaml" ]; then
    echo "Warning: living-doc-config.yaml not found"
    echo "Creating from template..."
    cp "$FRAMEWORK_ROOT/core/project-config.template.yaml" "$PROJECT_ROOT/living-doc-config.yaml"
    echo "Created living-doc-config.yaml - please customize it"
    echo ""
fi

# Create hooks directory if needed
mkdir -p "$GIT_HOOKS_DIR"

# Get relative path to framework
get_relative_path() {
    local target="$1"
    local base="$2"

    if command -v realpath &>/dev/null && realpath --relative-to="$base" "$target" 2>/dev/null; then
        return
    fi

    if command -v python3 &>/dev/null; then
        python3 -c "import os.path; print(os.path.relpath('$target', '$base'))"
        return
    fi

    if command -v python &>/dev/null; then
        python -c "import os.path; print(os.path.relpath('$target', '$base'))"
        return
    fi

    echo "LivingDocFramework"
}

REL_PATH=$(get_relative_path "$FRAMEWORK_ROOT" "$PROJECT_ROOT")

# Create pre-commit hook
cat > "$GIT_HOOKS_DIR/pre-commit" << EOF
#!/usr/bin/env bash
# Living Documentation Framework - Pre-Commit Hook

HOOK_SCRIPT="$REL_PATH/hooks/pre-commit"

if [ -f "\$HOOK_SCRIPT" ]; then
    bash "\$HOOK_SCRIPT"
    exit \$?
else
    echo "Warning: \$HOOK_SCRIPT not found"
    exit 0
fi
EOF

# Create commit-msg hook
cat > "$GIT_HOOKS_DIR/commit-msg" << EOF
#!/usr/bin/env bash
# Living Documentation Framework - Commit-Msg Hook

HOOK_SCRIPT="$REL_PATH/hooks/commit-msg"

if [ -f "\$HOOK_SCRIPT" ]; then
    bash "\$HOOK_SCRIPT" "\$1"
    exit \$?
else
    exit 0
fi
EOF

# Create post-commit hook
cat > "$GIT_HOOKS_DIR/post-commit" << EOF
#!/usr/bin/env bash
# Living Documentation Framework - Post-Commit Hook

HOOK_SCRIPT="$REL_PATH/hooks/post-commit"

if [ -f "\$HOOK_SCRIPT" ]; then
    bash "\$HOOK_SCRIPT"
fi
exit 0
EOF

# Make hooks executable
chmod +x "$GIT_HOOKS_DIR/pre-commit" 2>/dev/null || true
chmod +x "$GIT_HOOKS_DIR/commit-msg" 2>/dev/null || true
chmod +x "$GIT_HOOKS_DIR/post-commit" 2>/dev/null || true

chmod +x "$FRAMEWORK_ROOT/hooks/pre-commit" 2>/dev/null || true
chmod +x "$FRAMEWORK_ROOT/hooks/commit-msg" 2>/dev/null || true
chmod +x "$FRAMEWORK_ROOT/hooks/post-commit" 2>/dev/null || true

echo "Installed hooks:"
echo "   - pre-commit     Documentation validation"
echo "   - commit-msg     Commit message format"
echo "   - post-commit    Post-commit actions"
echo ""
echo "Hook locations:"
echo "   .git/hooks/pre-commit  -> $REL_PATH/hooks/pre-commit"
echo "   .git/hooks/commit-msg  -> $REL_PATH/hooks/commit-msg"
echo "   .git/hooks/post-commit -> $REL_PATH/hooks/post-commit"
echo ""
echo "Usage:"
echo "   Skip hooks:  git commit --no-verify"
echo "   Configure:   Edit living-doc-config.yaml"
echo ""
echo "Done! Hooks are now active."
