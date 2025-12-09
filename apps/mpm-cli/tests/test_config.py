"""Unit tests for Pydantic configuration models."""

import pytest
from pydantic import ValidationError

from mpm.config import (
    DocsTheme,
    LicenseType,
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
