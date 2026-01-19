#!/usr/bin/env python3
"""
Tests for the Living Documentation Framework configuration loader.
"""

import sys
import tempfile
from pathlib import Path

import pytest

# Add core to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))

from config import LDFConfig, load_config


class TestLDFConfig:
    """Tests for LDFConfig class."""

    def test_default_values(self, tmp_path):
        """Test that default values are returned when no config exists."""
        config = LDFConfig(config_path=str(tmp_path / "nonexistent.yaml"))

        # Should return defaults
        assert config.language == 'python'
        assert config.main_branch == 'main'
        assert config.code_root == 'src'
        assert 'py' in config.code_extensions

    def test_config_with_yaml(self, tmp_path):
        """Test loading configuration from YAML file."""
        config_content = """
project:
  name: test-project
  language: javascript
  main_branch: develop

code:
  root: lib
  extensions:
    - js
    - ts
"""
        config_file = tmp_path / "living-doc-config.yaml"
        config_file.write_text(config_content)

        config = LDFConfig(config_path=str(config_file))

        assert config.project_name == 'test-project'
        assert config.language == 'javascript'
        assert config.main_branch == 'develop'
        assert config.code_root == 'lib'
        assert 'js' in config.code_extensions
        assert 'ts' in config.code_extensions

    def test_document_paths(self, tmp_path):
        """Test document path properties."""
        config_file = tmp_path / "living-doc-config.yaml"
        config_file.write_text("project:\n  name: test\n")

        config = LDFConfig(config_path=str(config_file))

        # Paths should be Path objects
        assert isinstance(config.changelog_path, Path)
        assert isinstance(config.bug_patterns_path, Path)
        assert isinstance(config.invariants_path, Path)
        assert isinstance(config.code_doc_map_path, Path)

    def test_find_code_files_empty_dir(self, tmp_path):
        """Test find_code_files with empty directory."""
        config_file = tmp_path / "living-doc-config.yaml"
        config_file.write_text(f"""
project:
  name: test
code:
  root: src
  extensions:
    - py
""")
        src_dir = tmp_path / "src"
        src_dir.mkdir()

        config = LDFConfig(config_path=str(config_file))
        files = config.find_code_files(root=str(src_dir))

        assert files == []

    def test_find_code_files_with_files(self, tmp_path):
        """Test find_code_files finds Python files."""
        config_file = tmp_path / "living-doc-config.yaml"
        config_file.write_text("""
project:
  name: test
code:
  root: src
  extensions:
    - py
""")
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        (src_dir / "main.py").write_text("print('hello')")
        (src_dir / "utils.py").write_text("def helper(): pass")
        (src_dir / "readme.txt").write_text("not a python file")

        config = LDFConfig(config_path=str(config_file))
        files = config.find_code_files(root=str(src_dir))

        # Should find 2 Python files
        assert len(files) == 2
        file_names = [f.name for f in files]
        assert "main.py" in file_names
        assert "utils.py" in file_names
        assert "readme.txt" not in file_names


class TestLoadConfig:
    """Tests for load_config function."""

    def test_load_config_caching(self, tmp_path):
        """Test that load_config caches the configuration."""
        config_file = tmp_path / "living-doc-config.yaml"
        config_file.write_text("project:\n  name: cached-test\n")

        # Load twice
        config1 = load_config(str(config_file))
        config2 = load_config(str(config_file))

        # Should be the same instance (cached)
        assert config1 is config2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
