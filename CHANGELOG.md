# Changelog

All notable changes to the Living Documentation Framework.

---

## [1.2.2] - 2025-01-22

### Fixed
- Set executable bit on `core/load-config.sh` (was 644, now 755)
- Added `nul` to .gitignore (Windows artifact)

### Changed
- Install commands now use `bash` prefix for better cross-platform reliability
  - Works even if scripts aren't marked executable after extraction

---

## [1.2.1] - 2025-01-22

### Fixed
- Hook execution on Windows/MSYS2 (Git Bash)
  - Fixed `set -e` exit when test_pattern config is empty
  - Fixed extension parsing matching both code and test extensions
  - Fixed CHANGELOG check producing invalid comparison

---

## [1.2.0] - 2025-01-22

### Added
- **Quickstart example**: Runnable example with actual Python code
  - `examples/quickstart/` with auth.py as Tier A file
  - Experience the failure/fix loop in under 5 minutes
- **Tutorial**: Step-by-step walkthrough in `docs/TUTORIAL.md`
- **Glossary**: Term definitions in `docs/GLOSSARY.md`

### Changed
- README completely rewritten for clarity
  - Clearer structure: Why → What → How
  - "What this is not" section for honest boundaries
  - AGPL clarification for adoption confidence
  - Design principles section

---

## [1.1.0] - 2025-01-19

### Added
- **Doc-Set Discovery**: Per-subsystem documentation folders
  - Any folder under `docs/` containing `CODE_DOC_MAP.md` is a doc-set
  - Each doc-set has its own `INVARIANTS.md` for Tier A enforcement
  - Zero YAML configuration required - folder structure IS the config
- New template: `core/templates/code-doc-map.template.md`
- Helper functions in `load-config.sh`:
  - `ldf_find_doc_sets()` - Find all doc-sets
  - `ldf_list_doc_sets()` - List doc-set names
  - `ldf_has_doc_set()` - Check if doc-set exists
- Example doc-sets in `examples/python-project/docs/api/` and `docs/database/`

### Changed
- `hooks/pre-commit`: Now scans all `docs/*/CODE_DOC_MAP.md` files for Tier A
- Tier A matching requires `TIER A` token on same line as file path
- Root `CODE_DOC_MAP.md` now deprecated (emits warning, still works)

### Fixed
- Tier A detection now uses repo-relative paths only (no false matches)
- Shell scripts use `while IFS= read -r` pattern (handles spaces in paths)

---

## [1.0.0] - 2025-01-18

### Added
- Initial framework release
- Pre-commit hooks for documentation enforcement
- Language profiles: Python, JavaScript, Go, Rust, C#
- Core documents: CODE_DOC_MAP, BUG_PATTERNS, INVARIANTS, GOLDEN_PATHS
- Agent Protocol for AI compliance
- Session Protocol for version syncing

### Removed
- Dashboard and confidence scoring (moved to separate tool)
- GitHub sync integration (experimental, removed)

---

## Version History

- **1.2.2**: Executable bit fix for load-config.sh
- **1.2.1**: Bug fixes for Windows/Git Bash compatibility
- **1.2.0**: Quickstart example and improved onboarding
- **1.1.0**: Doc-set discovery for per-subsystem documentation
- **1.0.0**: Initial public release

