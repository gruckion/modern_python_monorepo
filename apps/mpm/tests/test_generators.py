"""Tests for generators."""

import tempfile
from pathlib import Path

import pytest

from modern_python_monorepo.mpm.config import (
    PackageConfig,
    PackageType,
    ProjectConfig,
    ProjectStructure,
)
from modern_python_monorepo.mpm.generators import generate_package, generate_project


class TestProjectGenerator:
    """Tests for project generation."""

    def test_monorepo_generation(self) -> None:
        """Test monorepo structure generation."""
        config = ProjectConfig(
            project_name="test_project",
            structure=ProjectStructure.MONOREPO,
            with_samples=False,
            init_git=False,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "test_project"
            generate_project(config, output)

            # Verify structure
            assert (output / "pyproject.toml").exists()
            assert (output / "README.md").exists()
            assert (output / ".gitignore").exists()
            assert (output / ".python-version").exists()
            assert (output / "apps").is_dir()
            assert (output / "libs").is_dir()

    def test_monorepo_with_samples(self) -> None:
        """Test monorepo with sample packages."""
        config = ProjectConfig(
            project_name="test_project",
            structure=ProjectStructure.MONOREPO,
            with_samples=True,
            init_git=False,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "test_project"
            generate_project(config, output)

            # Verify sample packages
            assert (output / "libs" / "greeter" / "pyproject.toml").exists()
            assert (output / "apps" / "printer" / "pyproject.toml").exists()
            assert (output / "libs" / "greeter" / "test_project" / "greeter" / "__init__.py").exists()
            assert (output / "apps" / "printer" / "test_project" / "printer" / "__init__.py").exists()

    def test_single_package_generation(self) -> None:
        """Test single package structure generation."""
        config = ProjectConfig(
            project_name="test_project",
            structure=ProjectStructure.SINGLE,
            init_git=False,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "test_project"
            generate_project(config, output)

            # Verify structure
            assert (output / "pyproject.toml").exists()
            assert (output / "src" / "test_project" / "__init__.py").exists()
            assert (output / "tests" / "test_import.py").exists()

    def test_with_docker(self) -> None:
        """Test generation with Docker support."""
        config = ProjectConfig(
            project_name="test_project",
            structure=ProjectStructure.MONOREPO,
            with_samples=True,
            init_git=False,
        )
        config.features.docker = True

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "test_project"
            generate_project(config, output)

            assert (output / "docker-compose.yml").exists()
            assert (output / "docker-bake.hcl").exists()
            assert (output / ".dockerignore").exists()

    def test_with_ci(self) -> None:
        """Test generation with CI/CD."""
        config = ProjectConfig(
            project_name="test_project",
            structure=ProjectStructure.MONOREPO,
            with_samples=False,
            init_git=False,
        )
        config.features.github_actions = True
        config.features.pypi_publish = True

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "test_project"
            generate_project(config, output)

            assert (output / ".github" / "workflows" / "pr.yml").exists()
            assert (output / ".github" / "workflows" / "release.yml").exists()


class TestPackageGenerator:
    """Tests for package generation."""

    def test_add_library(self) -> None:
        """Test adding a library package."""
        # First create a project
        project_config = ProjectConfig(
            project_name="test_project",
            structure=ProjectStructure.MONOREPO,
            with_samples=False,
            init_git=False,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "test_project"
            generate_project(project_config, project_dir)

            # Add a library
            pkg_config = PackageConfig(
                package_name="auth",
                package_type=PackageType.LIB,
                description="Auth utils",
                namespace="test_project",
            )
            generate_package(pkg_config, project_dir)

            # Verify
            assert (project_dir / "libs" / "auth" / "pyproject.toml").exists()
            assert (project_dir / "libs" / "auth" / "test_project" / "auth" / "__init__.py").exists()

    def test_add_application(self) -> None:
        """Test adding an application package."""
        project_config = ProjectConfig(
            project_name="test_project",
            structure=ProjectStructure.MONOREPO,
            with_samples=False,
            init_git=False,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "test_project"
            generate_project(project_config, project_dir)

            # Add an app
            pkg_config = PackageConfig(
                package_name="api",
                package_type=PackageType.APP,
                with_docker=True,
                namespace="test_project",
            )
            generate_package(pkg_config, project_dir)

            # Verify
            assert (project_dir / "apps" / "api" / "pyproject.toml").exists()
            assert (project_dir / "apps" / "api" / "Dockerfile").exists()

    def test_duplicate_package_fails(self) -> None:
        """Test that adding duplicate package fails."""
        project_config = ProjectConfig(
            project_name="test_project",
            structure=ProjectStructure.MONOREPO,
            with_samples=False,
            init_git=False,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "test_project"
            generate_project(project_config, project_dir)

            pkg_config = PackageConfig(
                package_name="auth",
                package_type=PackageType.LIB,
                namespace="test_project",
            )
            generate_package(pkg_config, project_dir)

            # Try to add again
            with pytest.raises(ValueError):
                generate_package(pkg_config, project_dir)
