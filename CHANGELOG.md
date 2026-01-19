# Changelog

All notable changes to the Living Documentation Framework.

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

- **1.1.0**: Doc-set discovery for per-subsystem documentation
- **1.0.0**: Initial public release

