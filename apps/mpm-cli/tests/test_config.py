"""Unit tests for Pydantic configuration models."""

from datetime import UTC
from pathlib import Path

import pytest
from pydantic import ValidationError

from mpm.config import (
    DocsTheme,
    LicenseType,
    MpmConfig,
    ProjectConfig,
    ProjectStructure,
    PythonVersion,
)


def test_project_config_defaults() -> None:
    """Test ProjectConfig with minimal required fields."""
    config = ProjectConfig(
        project_name="my_project",
        project_slug="my-project",
    )
    assert config.structure == ProjectStructure.MONOREPO
    assert config.python_version == PythonVersion.PY313
    assert config.license_type == LicenseType.MIT
    assert config.with_samples is False
    assert config.with_docker is False
    assert config.init_git is True


def test_project_config_namespace() -> None:
    """Test namespace property."""
    config = ProjectConfig(
        project_name="my_awesome_project",
        project_slug="my-awesome-project",
    )
    assert config.namespace == "my_awesome_project"


def test_project_config_namespace_with_hyphens() -> None:
    """Test namespace property converts hyphens to underscores."""
    config = ProjectConfig(
        project_name="my-awesome-project",
        project_slug="my-awesome-project",
    )
    assert config.namespace == "my_awesome_project"


def test_project_config_all_options() -> None:
    """Test ProjectConfig with all options enabled."""
    config = ProjectConfig(
        project_name="full_project",
        project_slug="full-project",
        project_description="A full-featured project",
        structure=ProjectStructure.MONOREPO,
        python_version=PythonVersion.PY312,
        license_type=LicenseType.APACHE,
        with_samples=True,
        with_docker=True,
        with_ci=True,
        with_pypi=True,
        with_docs=True,
        docs_theme=DocsTheme.SHADCN,
        init_git=False,
    )
    assert config.with_samples is True
    assert config.docs_theme == DocsTheme.SHADCN
    assert config.python_version == PythonVersion.PY312
    assert config.license_type == LicenseType.APACHE
    assert config.init_git is False


def test_single_structure() -> None:
    """Test single package structure."""
    config = ProjectConfig(
        project_name="single_project",
        project_slug="single-project",
        structure=ProjectStructure.SINGLE,
    )
    assert config.structure == ProjectStructure.SINGLE


def test_python_versions() -> None:
    """Test all Python version options."""
    for version in PythonVersion:
        config = ProjectConfig(
            project_name="test",
            project_slug="test",
            python_version=version,
        )
        assert config.python_version == version


def test_license_types() -> None:
    """Test all license type options."""
    for license_type in LicenseType:
        config = ProjectConfig(
            project_name="test",
            project_slug="test",
            license_type=license_type,
        )
        assert config.license_type == license_type


def test_docs_themes() -> None:
    """Test all docs theme options."""
    for theme in DocsTheme:
        config = ProjectConfig(
            project_name="test",
            project_slug="test",
            docs_theme=theme,
        )
        assert config.docs_theme == theme


def test_invalid_python_version() -> None:
    """Test that invalid Python version raises error."""
    with pytest.raises(ValidationError):
        ProjectConfig(
            project_name="test",
            project_slug="test",
            python_version="2.7",  # type: ignore
        )


# MpmConfig tests


def test_mpm_config_defaults() -> None:
    """Test MpmConfig with minimal required fields."""
    config = MpmConfig(
        project_name="my_project",
        project_slug="my-project",
    )
    assert config.version == "0.1.0"
    assert config.structure == ProjectStructure.MONOREPO
    assert config.python_version == PythonVersion.PY313
    assert config.license_type == LicenseType.MIT
    assert config.with_samples is False
    assert config.with_docker is False
    assert config.with_ci is False
    assert config.with_pypi is False
    assert config.with_docs is False
    assert config.docs_theme == DocsTheme.MATERIAL
    assert config.with_precommit is True


def test_mpm_config_from_project_config() -> None:
    """Test creating MpmConfig from ProjectConfig."""
    project_config = ProjectConfig(
        project_name="test_project",
        project_slug="test-project",
        project_description="A test project",
        structure=ProjectStructure.MONOREPO,
        python_version=PythonVersion.PY312,
        license_type=LicenseType.APACHE,
        with_samples=True,
        with_docker=True,
        with_ci=True,
        with_pypi=True,
        with_docs=True,
        docs_theme=DocsTheme.SHADCN,
        with_precommit=False,
        author_name="Test Author",
        author_email="test@example.com",
        github_owner="testowner",
        github_repo="testrepo",
    )

    mpm_config = MpmConfig.from_project_config(project_config, version="1.0.0")

    assert mpm_config.version == "1.0.0"
    assert mpm_config.project_name == "test_project"
    assert mpm_config.project_slug == "test-project"
    assert mpm_config.project_description == "A test project"
    assert mpm_config.structure == ProjectStructure.MONOREPO
    assert mpm_config.python_version == PythonVersion.PY312
    assert mpm_config.license_type == LicenseType.APACHE
    assert mpm_config.with_samples is True
    assert mpm_config.with_docker is True
    assert mpm_config.with_ci is True
    assert mpm_config.with_pypi is True
    assert mpm_config.with_docs is True
    assert mpm_config.docs_theme == DocsTheme.SHADCN
    assert mpm_config.with_precommit is False
    assert mpm_config.author_name == "Test Author"
    assert mpm_config.author_email == "test@example.com"
    assert mpm_config.github_owner == "testowner"
    assert mpm_config.github_repo == "testrepo"


def test_mpm_config_to_toml_dict() -> None:
    """Test converting MpmConfig to TOML dict."""
    config = MpmConfig(
        project_name="my_project",
        project_slug="my-project",
        project_description="Test description",
        structure=ProjectStructure.SINGLE,
        python_version=PythonVersion.PY311,
        license_type=LicenseType.GPL,
        with_samples=True,
        with_docker=True,
        docs_theme=DocsTheme.MATERIAL,
    )

    toml_dict = config.to_toml_dict()

    assert toml_dict["mpm"]["version"] == "0.1.0"
    assert "created_at" in toml_dict["mpm"]
    assert toml_dict["project"]["name"] == "my_project"
    assert toml_dict["project"]["slug"] == "my-project"
    assert toml_dict["project"]["description"] == "Test description"
    assert toml_dict["generation"]["structure"] == "single"
    assert toml_dict["generation"]["python_version"] == "3.11"
    assert toml_dict["generation"]["license"] == "GPL-3.0"
    assert toml_dict["features"]["samples"] is True
    assert toml_dict["features"]["docker"] is True
    assert toml_dict["features"]["docs_theme"] == "material"


def test_mpm_config_from_toml(tmp_path: Path) -> None:
    """Test loading MpmConfig from TOML file."""
    mpm_toml = tmp_path / "mpm.toml"
    mpm_toml.write_text("""
[mpm]
version = "0.2.0"
created_at = "2024-01-01T00:00:00"

[project]
name = "loaded_project"
slug = "loaded-project"
description = "Loaded from TOML"

[generation]
structure = "monorepo"
python_version = "3.12"
license = "Apache-2.0"

[features]
samples = true
docker = false
ci = true
pypi = false
docs = true
docs_theme = "shadcn"
precommit = false

[metadata]
author_name = "Author Name"
author_email = "author@example.com"
github_owner = "owner"
github_repo = "repo"
""")

    config = MpmConfig.from_toml(mpm_toml)

    assert config.version == "0.2.0"
    assert config.project_name == "loaded_project"
    assert config.project_slug == "loaded-project"
    assert config.project_description == "Loaded from TOML"
    assert config.structure == ProjectStructure.MONOREPO
    assert config.python_version == PythonVersion.PY312
    assert config.license_type == LicenseType.APACHE
    assert config.with_samples is True
    assert config.with_docker is False
    assert config.with_ci is True
    assert config.with_pypi is False
    assert config.with_docs is True
    assert config.docs_theme == DocsTheme.SHADCN
    assert config.with_precommit is False
    assert config.author_name == "Author Name"
    assert config.author_email == "author@example.com"
    assert config.github_owner == "owner"
    assert config.github_repo == "repo"


def test_mpm_config_round_trip(tmp_path: Path) -> None:
    """Test round-trip serialization (create -> save -> load)."""
    from mpm.utils import load_mpm_config, save_mpm_config

    original = MpmConfig(
        project_name="roundtrip_project",
        project_slug="roundtrip-project",
        project_description="Round trip test",
        structure=ProjectStructure.MONOREPO,
        python_version=PythonVersion.PY313,
        license_type=LicenseType.MIT,
        with_samples=True,
        with_docker=True,
        with_ci=True,
        with_pypi=True,
        with_docs=True,
        docs_theme=DocsTheme.MATERIAL,
        with_precommit=True,
        author_name="Test Author",
        author_email="test@example.com",
        github_owner="owner",
        github_repo="repo",
    )

    mpm_toml = tmp_path / "mpm.toml"
    save_mpm_config(original, mpm_toml)

    loaded = load_mpm_config(mpm_toml)

    assert loaded.project_name == original.project_name
    assert loaded.project_slug == original.project_slug
    assert loaded.project_description == original.project_description
    assert loaded.structure == original.structure
    assert loaded.python_version == original.python_version
    assert loaded.license_type == original.license_type
    assert loaded.with_samples == original.with_samples
    assert loaded.with_docker == original.with_docker
    assert loaded.with_ci == original.with_ci
    assert loaded.with_pypi == original.with_pypi
    assert loaded.with_docs == original.with_docs
    assert loaded.docs_theme == original.docs_theme
    assert loaded.with_precommit == original.with_precommit
    assert loaded.author_name == original.author_name
    assert loaded.author_email == original.author_email
    assert loaded.github_owner == original.github_owner
    assert loaded.github_repo == original.github_repo


# Timezone-aware datetime tests


def test_mpm_config_default_created_at_is_timezone_aware() -> None:
    """Test that MpmConfig default created_at uses timezone-aware UTC datetime."""
    config = MpmConfig(
        project_name="my_project",
        project_slug="my-project",
    )
    # Verify created_at is set and is timezone-aware
    assert config.created_at is not None
    assert config.created_at.tzinfo is not None
    assert config.created_at.tzinfo == UTC


def test_mpm_config_from_project_config_created_at_is_timezone_aware() -> None:
    """Test that MpmConfig.from_project_config creates timezone-aware datetime."""
    project_config = ProjectConfig(
        project_name="test_project",
        project_slug="test-project",
    )
    mpm_config = MpmConfig.from_project_config(project_config)

    assert mpm_config.created_at is not None
    assert mpm_config.created_at.tzinfo is not None
    assert mpm_config.created_at.tzinfo == UTC


def test_mpm_config_from_toml_with_timezone_aware_datetime(tmp_path: Path) -> None:
    """Test loading MpmConfig from TOML with timezone-aware datetime."""
    mpm_toml = tmp_path / "mpm.toml"
    # Use ISO format with timezone offset
    mpm_toml.write_text("""
[mpm]
version = "0.2.0"
created_at = "2024-01-01T12:00:00+00:00"

[project]
name = "loaded_project"
slug = "loaded-project"
""")

    config = MpmConfig.from_toml(mpm_toml)

    assert config.created_at is not None
    assert config.created_at.tzinfo is not None


def test_mpm_config_from_toml_fallback_is_timezone_aware(tmp_path: Path) -> None:
    """Test that MpmConfig.from_toml fallback for missing created_at is timezone-aware."""
    mpm_toml = tmp_path / "mpm.toml"
    # TOML file without created_at field
    mpm_toml.write_text("""
[mpm]
version = "0.2.0"

[project]
name = "loaded_project"
slug = "loaded-project"
""")

    config = MpmConfig.from_toml(mpm_toml)

    assert config.created_at is not None
    assert config.created_at.tzinfo is not None
    assert config.created_at.tzinfo == UTC


def test_mpm_config_to_toml_dict_created_at_includes_timezone() -> None:
    """Test that to_toml_dict includes timezone info in created_at ISO string."""
    config = MpmConfig(
        project_name="my_project",
        project_slug="my-project",
    )

    toml_dict = config.to_toml_dict()

    created_at_str = toml_dict["mpm"]["created_at"]
    # Verify the ISO string includes timezone offset (+00:00 for UTC)
    assert "+00:00" in created_at_str or "Z" in created_at_str


def test_project_generator_context_created_at_includes_timezone(tmp_path: Path) -> None:
    """Test that project generator creates timezone-aware created_at in context."""
    from mpm.generators.project import _generate_base_files
    from mpm.generators.renderer import TemplateRenderer

    renderer = TemplateRenderer()
    ctx = {
        "project_name": "test_project",
        "project_slug": "test-project",
        "namespace": "test_project",
        "structure": "monorepo",
        "python_version": "3.13",
        "license_type": "MIT",
        "with_samples": False,
        "with_docker": False,
        "with_ci": False,
        "with_pypi": False,
        "with_docs": False,
        "docs_theme": "material",
        "with_precommit": False,
        "author_name": "",
        "author_email": "",
        "github_owner": "",
        "github_repo": "",
        "project_description": "",
    }

    _generate_base_files(renderer, tmp_path, ctx)

    # Verify created_at was added to context and includes timezone info
    assert "created_at" in ctx
    created_at_str = ctx["created_at"]
    assert isinstance(created_at_str, str)
    # Verify the ISO string includes timezone offset
    assert "+00:00" in created_at_str or "Z" in created_at_str
