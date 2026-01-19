"""
Config Loader - Dynamic configuration loading for cognitive graph system.

All graph configuration is loaded from JSON files in .claude/devmemory/schema/
This eliminates hardcoded values and enables dynamic customization.

Usage:
    from config_loader import ConfigLoader

    config = ConfigLoader()
    node_types = config.get_node_types()
    tier_a_files = config.get_tier_files("A")
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Set


class ConfigLoader:
    """Load all graph configuration from JSON schema files."""

    # Default schema directory relative to project root
    DEFAULT_SCHEMA_DIR = ".claude/devmemory/schema"

    def __init__(self, schema_dir: Optional[str] = None, project_root: Optional[Path] = None):
        """
        Initialize config loader.

        Args:
            schema_dir: Path to schema directory (relative or absolute)
            project_root: Project root directory (auto-detected if None)
        """
        if project_root is None:
            # Auto-detect project root by finding .claude directory
            project_root = self._find_project_root()

        self.project_root = Path(project_root)

        if schema_dir is None:
            self.schema_dir = self.project_root / self.DEFAULT_SCHEMA_DIR
        else:
            schema_path = Path(schema_dir)
            if schema_path.is_absolute():
                self.schema_dir = schema_path
            else:
                self.schema_dir = self.project_root / schema_path

        self._cache: Dict[str, Any] = {}

    def _find_project_root(self) -> Path:
        """Find project root by looking for .claude directory."""
        current = Path(__file__).resolve()

        # Walk up directory tree
        for parent in [current] + list(current.parents):
            if (parent / ".claude").exists():
                return parent

        # Fallback to current working directory
        return Path.cwd()

    def _load(self, filename: str) -> Dict[str, Any]:
        """Load a JSON schema file with caching."""
        if filename in self._cache:
            return self._cache[filename]

        filepath = self.schema_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Schema file not found: {filepath}")

        try:
            content = filepath.read_text(encoding='utf-8')
            data = json.loads(content)
            self._cache[filename] = data
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {filepath}: {e}")

    def clear_cache(self) -> None:
        """Clear the config cache to force reload."""
        self._cache.clear()

    # ==================== Node Types ====================

    def get_node_types(self) -> List[Dict[str, Any]]:
        """Get all node type definitions."""
        return self._load("node-types.json")["node_types"]

    def get_node_type(self, type_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific node type by ID."""
        for node_type in self.get_node_types():
            if node_type["id"] == type_id:
                return node_type
        return None

    def get_enabled_node_types(self) -> List[Dict[str, Any]]:
        """Get only enabled node types."""
        return [nt for nt in self.get_node_types() if nt.get("enabled", True)]

    def get_node_colors(self) -> Dict[str, str]:
        """Get node type ID to color mapping."""
        return {nt["id"]: nt["color"] for nt in self.get_node_types()}

    # ==================== Edge Types ====================

    def get_edge_types(self) -> List[Dict[str, Any]]:
        """Get all edge type definitions."""
        return self._load("edge-types.json")["edge_types"]

    def get_edge_type(self, type_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific edge type by ID."""
        for edge_type in self.get_edge_types():
            if edge_type["id"] == type_id:
                return edge_type
        return None

    def get_enabled_edge_types(self) -> List[Dict[str, Any]]:
        """Get only enabled edge types."""
        return [et for et in self.get_edge_types() if et.get("enabled", True)]

    def get_edge_colors(self) -> Dict[str, str]:
        """Get edge type ID to color mapping."""
        return {et["id"]: et["color"] for et in self.get_edge_types()}

    # ==================== Tiers ====================

    def get_tiers(self) -> Dict[str, Dict[str, Any]]:
        """Get all tier definitions."""
        return self._load("tiers.json")["tiers"]

    def get_tier(self, tier_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific tier by ID (A, B, C, D)."""
        return self.get_tiers().get(tier_id)

    def get_tier_files(self, tier_id: str) -> Set[str]:
        """Get set of files for a specific tier."""
        tier = self.get_tier(tier_id)
        if tier:
            return set(tier.get("files", []))
        return set()

    def get_tier_patterns(self, tier_id: str) -> List[str]:
        """Get glob patterns for a specific tier."""
        tier = self.get_tier(tier_id)
        if tier:
            return tier.get("patterns", [])
        return []

    def get_default_tier(self) -> str:
        """Get the default tier for unmatched files."""
        return self._load("tiers.json").get("default_tier", "C")

    def get_tier_for_file(self, filename: str) -> str:
        """Determine tier for a given filename."""
        import fnmatch
        clean_name = Path(filename).name

        # Check explicit file lists (highest priority)
        for tier_id in ["A", "B", "C", "D"]:
            if clean_name in self.get_tier_files(tier_id):
                return tier_id

        # Check patterns (in order of priority)
        for tier_id in ["D", "B"]:  # D and B have patterns, A is explicit, C is default
            for pattern in self.get_tier_patterns(tier_id):
                if fnmatch.fnmatch(clean_name, pattern) or fnmatch.fnmatch(filename, pattern):
                    return tier_id

        return self.get_default_tier()

    def get_tier_colors(self) -> Dict[str, str]:
        """Get tier ID to color mapping."""
        return {tid: t["color"] for tid, t in self.get_tiers().items()}

    # ==================== Categories ====================

    def get_categories(self) -> List[Dict[str, Any]]:
        """Get all category definitions."""
        return self._load("categories.json")["categories"]

    def get_category(self, category_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific category by ID."""
        for cat in self.get_categories():
            if cat["id"] == category_id:
                return cat
        return None

    def get_default_category(self) -> str:
        """Get the default category ID."""
        for cat in self.get_categories():
            if cat.get("is_default", False):
                return cat["id"]
        return "General"

    def get_category_for_file(self, filepath: str) -> str:
        """Determine category for a given file path."""
        for cat in self.get_categories():
            if cat.get("is_default"):
                continue

            # Check path patterns
            for pattern in cat.get("path_patterns", []):
                if re.search(pattern, filepath, re.IGNORECASE):
                    return cat["id"]

            # Check keywords in filename
            filename = Path(filepath).stem.lower()
            for keyword in cat.get("keywords", []):
                if keyword.lower() in filename:
                    return cat["id"]

        return self.get_default_category()

    def get_category_colors(self) -> Dict[str, str]:
        """Get category ID to color mapping."""
        return {cat["id"]: cat["color"] for cat in self.get_categories()}

    # ==================== Discovery Passes ====================

    def get_discovery_passes(self) -> List[Dict[str, Any]]:
        """Get all discovery pass definitions."""
        return self._load("discovery-passes.json")["passes"]

    def get_enabled_passes(self) -> List[Dict[str, Any]]:
        """Get only enabled discovery passes."""
        return [p for p in self.get_discovery_passes() if p.get("enabled", True)]

    def get_pass_confidence(self, pass_name: str) -> float:
        """Get confidence level for a specific pass."""
        for p in self.get_discovery_passes():
            if p["name"] == pass_name:
                return p.get("confidence", 1.0)
        return 1.0

    # ==================== Regex Patterns ====================

    def get_regex_patterns(self) -> Dict[str, str]:
        """Get all regex patterns."""
        return self._load("regex-patterns.json")["patterns"]

    def get_regex(self, name: str) -> str:
        """Get a specific regex pattern by name."""
        patterns = self.get_regex_patterns()
        if name not in patterns:
            raise KeyError(f"Unknown regex pattern: {name}")
        return patterns[name]

    def get_compiled_regex(self, name: str, flags: int = 0) -> re.Pattern:
        """Get a compiled regex pattern."""
        return re.compile(self.get_regex(name), flags)

    # ==================== Utility ====================

    def validate(self) -> List[str]:
        """Validate all schema files exist and are valid JSON."""
        errors = []

        required_files = [
            "node-types.json",
            "edge-types.json",
            "tiers.json",
            "categories.json",
            "discovery-passes.json",
            "regex-patterns.json"
        ]

        for filename in required_files:
            filepath = self.schema_dir / filename
            if not filepath.exists():
                errors.append(f"Missing schema file: {filename}")
            else:
                try:
                    self._load(filename)
                except (json.JSONDecodeError, ValueError) as e:
                    errors.append(f"Invalid JSON in {filename}: {e}")

        return errors

    def get_schema_version(self, filename: str) -> str:
        """Get version from a schema file."""
        return self._load(filename).get("version", "unknown")

    def export_for_dashboard(self) -> Dict[str, Any]:
        """Export config data formatted for dashboard consumption."""
        return {
            "node_types": self.get_node_types(),
            "edge_types": self.get_edge_types(),
            "tiers": self.get_tiers(),
            "categories": self.get_categories(),
            "colors": {
                "nodes": self.get_node_colors(),
                "edges": self.get_edge_colors(),
                "tiers": self.get_tier_colors(),
                "categories": self.get_category_colors()
            }
        }


# Singleton instance for convenience
_default_loader: Optional[ConfigLoader] = None

def get_config() -> ConfigLoader:
    """Get the default ConfigLoader instance."""
    global _default_loader
    if _default_loader is None:
        _default_loader = ConfigLoader()
    return _default_loader

def reload_config() -> ConfigLoader:
    """Reload configuration (clear cache and return fresh loader)."""
    global _default_loader
    if _default_loader is not None:
        _default_loader.clear_cache()
    else:
        _default_loader = ConfigLoader()
    return _default_loader


if __name__ == "__main__":
    # Test the config loader
    config = ConfigLoader()

    # Validate all schemas
    errors = config.validate()
    if errors:
        print("Validation errors:")
        for e in errors:
            print(f"  - {e}")
    else:
        print("All schemas valid!")

    # Print summary
    print(f"\nNode types: {len(config.get_node_types())}")
    print(f"Edge types: {len(config.get_edge_types())}")
    print(f"Tiers: {list(config.get_tiers().keys())}")
    print(f"Categories: {len(config.get_categories())}")
    print(f"Discovery passes: {len(config.get_discovery_passes())}")
    print(f"Regex patterns: {len(config.get_regex_patterns())}")
