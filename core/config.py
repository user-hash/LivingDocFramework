"""
Living Documentation Framework - Python Configuration Loader
Loads project configuration from living-doc-config.yaml
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List

class LDFConfig:
    """Living Documentation Framework configuration"""

    def __init__(self, config_path: Optional[str] = None):
        """
        Load configuration from YAML file

        Args:
            config_path: Path to living-doc-config.yaml (auto-detects if None)
        """
        self.project_root = self._find_project_root(config_path)
        self.config = self._load_config()
        self._load_language_profile()

    def _find_project_root(self, config_path: Optional[str]) -> Path:
        """Find project root by looking for living-doc-config.yaml"""
        if config_path:
            return Path(config_path).parent

        # Search upwards from current directory
        current = Path.cwd()
        while current != current.parent:
            if (current / "living-doc-config.yaml").exists():
                return current
            current = current.parent

        # Fallback: current directory
        return Path.cwd()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        config_file = self.project_root / "living-doc-config.yaml"

        if not config_file.exists():
            # Return defaults
            return {
                'project': {
                    'name': 'MyProject',
                    'language': 'python',
                    'main_branch': 'main'
                },
                'version': {
                    'file': '__init__.py',
                    'pattern': r'__version__\s*=\s*"([0-9.]+)"'
                },
                'code': {
                    'root': 'src/',
                    'extensions': ['py']
                },
                'tests': {
                    'pattern': '**/test_*.py',
                    'extensions': ['py']
                }
            }

        with open(config_file, 'r') as f:
            return yaml.safe_load(f)

    def _load_language_profile(self):
        """Load language-specific defaults"""
        language = self.config.get('project', {}).get('language', 'python')

        # Look for language profile
        profile_path = self.project_root / 'LivingDocFramework' / 'core' / 'languages' / f'{language}.yaml'
        if not profile_path.exists():
            # Try relative to this file
            profile_path = Path(__file__).parent / 'languages' / f'{language}.yaml'

        if profile_path.exists():
            with open(profile_path, 'r') as f:
                self.language_profile = yaml.safe_load(f)
        else:
            self.language_profile = {}

    # Property accessors for common config values

    @property
    def project_name(self) -> str:
        return self.config.get('project', {}).get('name', 'MyProject')

    @property
    def language(self) -> str:
        return self.config.get('project', {}).get('language', 'python')

    @property
    def main_branch(self) -> str:
        return self.config.get('project', {}).get('main_branch', 'main')

    @property
    def version_file(self) -> str:
        return self.config.get('version', {}).get('file', '__init__.py')

    @property
    def version_pattern(self) -> str:
        return self.config.get('version', {}).get('pattern', r'__version__\s*=\s*"([0-9.]+)"')

    @property
    def code_root(self) -> str:
        return self.config.get('code', {}).get('root', 'src/')

    @property
    def code_extensions(self) -> List[str]:
        return self.config.get('code', {}).get('extensions', ['py'])

    @property
    def test_pattern(self) -> str:
        return self.config.get('tests', {}).get('pattern', '**/test_*.py')

    @property
    def test_extensions(self) -> List[str]:
        return self.config.get('tests', {}).get('extensions', ['py'])

    # Document paths

    @property
    def changelog_path(self) -> Path:
        return self.project_root / "CHANGELOG.md"

    @property
    def bug_patterns_path(self) -> Path:
        return self.project_root / "BUG_PATTERNS.md"

    @property
    def bug_tracker_path(self) -> Path:
        return self.project_root / "BUG_TRACKER.md"

    @property
    def golden_paths_path(self) -> Path:
        return self.project_root / "docs" / "GOLDEN_PATHS.md"

    @property
    def invariants_path(self) -> Path:
        return self.project_root / "docs" / "INVARIANTS.md"

    @property
    def decisions_path(self) -> Path:
        return self.project_root / "docs" / "DECISIONS.md"

    @property
    def code_doc_map_path(self) -> Path:
        return self.project_root / "docs" / "CODE_DOC_MAP.md"

    @property
    def claude_md_path(self) -> Path:
        return self.project_root / "CLAUDE.md"

    @property
    def dashboard_dir(self) -> Path:
        return self.project_root / ".claude" / "dashboard"

    @property
    def history_file(self) -> Path:
        return self.dashboard_dir / "history.json"

    @property
    def dashboard_html(self) -> Path:
        return self.dashboard_dir / "index.html"

    # Utility methods

    def find_code_files(self, root: Optional[str] = None) -> List[Path]:
        """Find all code files matching configured extensions"""
        search_root = Path(root) if root else (self.project_root / self.code_root)
        files = []
        for ext in self.code_extensions:
            files.extend(search_root.rglob(f"*.{ext}"))
        return files

    def find_test_files(self, root: Optional[str] = None) -> List[Path]:
        """Find all test files matching configured pattern"""
        search_root = Path(root) if root else (self.project_root / self.code_root)
        # Simple glob-based search
        # For complex patterns, use fnmatch or glob
        test_files = []
        for ext in self.test_extensions:
            test_files.extend(search_root.rglob(f"*test*.{ext}"))
        return test_files

    def get_subsystems(self) -> List[Dict[str, Any]]:
        """Get configured subsystems"""
        return self.config.get('subsystems', [])

    def get_tiering_rules(self) -> Dict[str, Any]:
        """Get tiering configuration"""
        return self.config.get('tiering', {})


# Global config instance
_config: Optional[LDFConfig] = None

def load_config(config_path: Optional[str] = None) -> LDFConfig:
    """
    Load or get cached configuration

    Args:
        config_path: Path to living-doc-config.yaml (auto-detects if None)

    Returns:
        LDFConfig instance
    """
    global _config
    if _config is None or config_path is not None:
        _config = LDFConfig(config_path)
    return _config


# Convenience function for scripts
def get_config() -> LDFConfig:
    """Get configuration (loads if not already loaded)"""
    return load_config()
