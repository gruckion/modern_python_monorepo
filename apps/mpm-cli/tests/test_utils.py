"""Unit tests for utility functions."""

from pathlib import Path

from mpm.config import MpmConfig, ProjectStructure, PythonVersion
from mpm.utils import (
    find_mpm_config,
    find_project_root,
    get_namespace_from_project,
    load_mpm_config,
    save_mpm_config,
    validate_project_name,
)


def test_find_mpm_config_exists(tmp_path: Path) -> None:
    """Test finding mpm.toml when it exists."""
    mpm_toml = tmp_path / "mpm.toml"
    mpm_toml.write_text("[mpm]\nversion = '0.1.0'")

    result = find_mpm_config(tmp_path)
    assert result == mpm_toml


def test_find_mpm_config_not_exists(tmp_path: Path) -> None:
    """Test finding mpm.toml when it doesn't exist."""
    result = find_mpm_config(tmp_path)
    assert result is None


def test_find_mpm_config_in_parent(tmp_path: Path) -> None:
    """Test finding mpm.toml in parent directory."""
    mpm_toml = tmp_path / "mpm.toml"
    mpm_toml.write_text("[mpm]\nversion = '0.1.0'")

    subdir = tmp_path / "subdir" / "nested"
    subdir.mkdir(parents=True)

    result = find_mpm_config(subdir)
    assert result == mpm_toml


def test_find_project_root_with_mpm_toml(tmp_path: Path) -> None:
    """Test project root detection via mpm.toml."""
    mpm_toml = tmp_path / "mpm.toml"
    mpm_toml.write_text("[mpm]\nversion = '0.1.0'")

    result = find_project_root(tmp_path)
    assert result == tmp_path


def test_find_project_root_requires_mpm_toml(tmp_path: Path) -> None:
    """Test that find_project_root only detects mpm.toml, not pyproject.toml."""
    # Create a pyproject.toml with workspace config (but no mpm.toml)
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""
[project]
name = "test"

[tool.uv.workspace]
members = ["apps/*", "libs/*"]
""")

    # Should NOT find project root without mpm.toml
    result = find_project_root(tmp_path)
    assert result is None


def test_find_project_root_not_found(tmp_path: Path) -> None:
    """Test project root detection returns None when not found."""
    result = find_project_root(tmp_path)
    assert result is None


def test_find_project_root_from_subdirectory(tmp_path: Path) -> None:
    """Test project root detection from a subdirectory."""
    mpm_toml = tmp_path / "mpm.toml"
    mpm_toml.write_text("[mpm]\nversion = '0.1.0'")

    subdir = tmp_path / "src" / "package"
    subdir.mkdir(parents=True)

    result = find_project_root(subdir)
    assert result == tmp_path


def test_get_namespace_from_mpm_toml(tmp_path: Path) -> None:
    """Test getting namespace from mpm.toml."""
    mpm_toml = tmp_path / "mpm.toml"
    mpm_toml.write_text("""
[project]
name = "my_namespace"
slug = "my-namespace"
""")

    result = get_namespace_from_project(tmp_path)
    assert result == "my_namespace"


def test_get_namespace_requires_mpm_toml(tmp_path: Path) -> None:
    """Test that get_namespace only reads from mpm.toml, not pyproject.toml."""
    # Create pyproject.toml with una namespace (but no mpm.toml)
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""
[tool.una]
namespace = "una_namespace"
""")

    # Should NOT find namespace without mpm.toml
    result = get_namespace_from_project(tmp_path)
    assert result is None


def test_get_namespace_not_found(tmp_path: Path) -> None:
    """Test getting namespace when no config exists."""
    result = get_namespace_from_project(tmp_path)
    assert result is None


def test_load_mpm_config(tmp_path: Path) -> None:
    """Test loading mpm.toml."""
    mpm_toml = tmp_path / "mpm.toml"
    mpm_toml.write_text("""
[mpm]
version = "0.1.0"
created_at = "2024-01-01T00:00:00"

[project]
name = "test_project"
slug = "test-project"
description = ""

[generation]
structure = "monorepo"
python_version = "3.13"
license = "MIT"

[features]
samples = false
docker = false
ci = false
pypi = false
docs = false
docs_theme = "material"
precommit = true

[metadata]
author_name = ""
author_email = ""
github_owner = ""
github_repo = ""
""")

    config = load_mpm_config(mpm_toml)

    assert config.project_name == "test_project"
    assert config.project_slug == "test-project"
    assert config.structure == ProjectStructure.MONOREPO
    assert config.python_version == PythonVersion.PY313


def test_save_mpm_config(tmp_path: Path) -> None:
    """Test saving mpm.toml."""
    config = MpmConfig(
        project_name="saved_project",
        project_slug="saved-project",
        project_description="Saved description",
    )

    mpm_toml = tmp_path / "mpm.toml"
    save_mpm_config(config, mpm_toml)

    assert mpm_toml.exists()
    content = mpm_toml.read_text()

    # Check header comment
    assert "# mpm.toml - Modern Python Monorepo Configuration" in content

    # Check content
    assert 'name = "saved_project"' in content
    assert 'slug = "saved-project"' in content
    assert 'description = "Saved description"' in content


def test_save_mpm_config_creates_valid_toml(tmp_path: Path) -> None:
    """Test that saved mpm.toml is valid and can be reloaded."""
    original = MpmConfig(
        project_name="valid_project",
        project_slug="valid-project",
    )

    mpm_toml = tmp_path / "mpm.toml"
    save_mpm_config(original, mpm_toml)

    # Should be able to load without errors
    loaded = load_mpm_config(mpm_toml)
    assert loaded.project_name == original.project_name


# ============================================================================
# validate_project_name tests
# ============================================================================


class TestValidateProjectName:
    """Tests for the validate_project_name function."""

    def test_valid_names(self) -> None:
        """Test that valid project names pass validation."""
        valid_names = [
            "my_project",
            "my-project",
            "myproject",
            "MyProject",
            "project123",
            "a",
            "abc",
        ]
        for name in valid_names:
            is_valid, error = validate_project_name(name)
            assert is_valid, f"'{name}' should be valid but got error: {error}"

    def test_empty_name(self) -> None:
        """Test that empty names are rejected."""
        is_valid, error = validate_project_name("")
        assert not is_valid
        assert "empty" in error.lower()

    def test_name_too_long(self) -> None:
        """Test that overly long names are rejected."""
        long_name = "a" * 101
        is_valid, error = validate_project_name(long_name)
        assert not is_valid
        assert "too long" in error.lower()

    def test_path_traversal_rejected(self) -> None:
        """Test that path traversal attempts are rejected."""
        dangerous_names = [
            "../etc/passwd",
            "..\\windows\\system32",
            "project/../../../etc",
            "my/project",
            "my\\project",
        ]
        for name in dangerous_names:
            is_valid, error = validate_project_name(name)
            assert not is_valid, f"'{name}' should be rejected"
            assert "path" in error.lower() or "separator" in error.lower()

    def test_spaces_rejected(self) -> None:
        """Test that names with spaces are rejected."""
        is_valid, error = validate_project_name("my project")
        assert not is_valid
        assert "space" in error.lower()

    def test_special_characters_rejected(self) -> None:
        """Test that names with special characters are rejected."""
        invalid_names = [
            "project!",
            "project@name",
            "project#1",
            "project$",
            "project%",
            "project&",
            "project*",
            "project()",
            "project+",
            "project=",
        ]
        for name in invalid_names:
            is_valid, error = validate_project_name(name)
            assert not is_valid, f"'{name}' should be rejected"

    def test_names_starting_with_number_rejected(self) -> None:
        """Test that names starting with a number are rejected."""
        is_valid, error = validate_project_name("123project")
        assert not is_valid
        assert "start with a letter" in error.lower()

    def test_python_keywords_rejected(self) -> None:
        """Test that Python keywords are rejected."""
        keywords = ["class", "import", "from", "def", "return", "if", "while", "for"]
        for keyword in keywords:
            is_valid, error = validate_project_name(keyword)
            assert not is_valid, f"'{keyword}' should be rejected"
            assert "keyword" in error.lower()

    def test_reserved_names_rejected(self) -> None:
        """Test that reserved names are rejected."""
        reserved = ["__init__", "__main__", "test", "tests", "src", "lib", "apps"]
        for name in reserved:
            is_valid, error = validate_project_name(name)
            assert not is_valid, f"'{name}' should be rejected"
            assert "reserved" in error.lower()

    def test_dunder_names_rejected(self) -> None:
        """Test that __dunder__ style names are rejected."""
        is_valid, error = validate_project_name("__init__")
        assert not is_valid

    def test_case_insensitive_keyword_check(self) -> None:
        """Test that keyword check is case insensitive."""
        is_valid, error = validate_project_name("CLASS")
        assert not is_valid
        assert "keyword" in error.lower()

    def test_hyphenated_names_valid(self) -> None:
        """Test that hyphenated names are valid."""
        is_valid, error = validate_project_name("my-awesome-project")
        assert is_valid, f"Should be valid but got error: {error}"

    def test_underscored_names_valid(self) -> None:
        """Test that underscored names are valid."""
        is_valid, error = validate_project_name("my_awesome_project")
        assert is_valid, f"Should be valid but got error: {error}"

    def test_mixed_case_valid(self) -> None:
        """Test that mixed case names are valid."""
        is_valid, error = validate_project_name("MyAwesomeProject")
        assert is_valid, f"Should be valid but got error: {error}"
