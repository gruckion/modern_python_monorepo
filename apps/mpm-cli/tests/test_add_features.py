"""Tests for mpm add feature commands (docker, ci, pypi, docs)."""

import os
import tomllib
from pathlib import Path
from typing import Any

from typer.testing import CliRunner

from mpm.cli import app


class TestAddDockerCommand:
    """Test 'mpm add docker' command."""

    def test_add_docker_to_monorepo(self, run_mpm: Any, temp_dir: Path) -> None:
        """Test adding docker to a monorepo."""
        # Create project without docker
        exit_code, _output, project = run_mpm("docker-test", "--monorepo", "-y")
        assert exit_code == 0
        assert not (project / ".dockerignore").exists()

        runner = CliRunner()
        original_dir = os.getcwd()
        os.chdir(project)

        try:
            result = runner.invoke(app, ["add", "docker"])
            assert result.exit_code == 0
            assert "Added Docker configuration" in result.stdout

            # Check files were created
            assert (project / ".dockerignore").exists()

            # Check mpm.toml was updated
            with open(project / "mpm.toml", "rb") as f:
                config = tomllib.load(f)
            assert config["features"]["docker"] is True
        finally:
            os.chdir(original_dir)

    def test_add_docker_to_monorepo_with_samples(self, run_mpm: Any, temp_dir: Path) -> None:
        """Test adding docker to a monorepo that has sample apps with Dockerfiles."""
        # Create project with samples but without docker
        exit_code, _output, project = run_mpm("docker-samples-test", "--monorepo", "--with-samples", "-y")
        assert exit_code == 0

        # Manually add Dockerfile to printer app (simulating --docker option)
        printer_dir = project / "apps" / "printer"
        dockerfile = printer_dir / "Dockerfile"
        dockerfile.write_text("# Test Dockerfile\nFROM python:3.13\n")

        runner = CliRunner()
        original_dir = os.getcwd()
        os.chdir(project)

        try:
            result = runner.invoke(app, ["add", "docker"])
            assert result.exit_code == 0

            # Should create docker-compose.yml and docker-bake.hcl when Dockerfiles exist
            assert (project / ".dockerignore").exists()
            assert (project / "docker-compose.yml").exists()
            assert (project / "docker-bake.hcl").exists()
        finally:
            os.chdir(original_dir)

    def test_add_docker_to_single_package(self, run_mpm: Any, temp_dir: Path) -> None:
        """Test adding docker to a single package project."""
        exit_code, _output, project = run_mpm("docker-single-test", "--single", "-y")
        assert exit_code == 0

        runner = CliRunner()
        original_dir = os.getcwd()
        os.chdir(project)

        try:
            result = runner.invoke(app, ["add", "docker"])
            assert result.exit_code == 0

            # Single package should get all docker files
            assert (project / ".dockerignore").exists()
            assert (project / "Dockerfile").exists()
            assert (project / "docker-compose.yml").exists()
            assert (project / "docker-bake.hcl").exists()
        finally:
            os.chdir(original_dir)

    def test_add_docker_idempotent(self, run_mpm: Any, temp_dir: Path) -> None:
        """Test that running add docker twice is idempotent."""
        exit_code, _output, project = run_mpm("docker-idem-test", "--single", "-y")
        assert exit_code == 0

        runner = CliRunner()
        original_dir = os.getcwd()
        os.chdir(project)

        try:
            # First add
            result = runner.invoke(app, ["add", "docker"])
            assert result.exit_code == 0

            # Second add should warn but not fail
            result = runner.invoke(app, ["add", "docker"])
            assert result.exit_code == 0
            assert "already enabled" in result.stdout
        finally:
            os.chdir(original_dir)


class TestAddCiCommand:
    """Test 'mpm add ci' command."""

    def test_add_ci_to_project(self, run_mpm: Any, temp_dir: Path) -> None:
        """Test adding CI to a project."""
        exit_code, _output, project = run_mpm("ci-test", "--monorepo", "-y")
        assert exit_code == 0
        assert not (project / ".github" / "workflows" / "pr.yml").exists()

        runner = CliRunner()
        original_dir = os.getcwd()
        os.chdir(project)

        try:
            result = runner.invoke(app, ["add", "ci"])
            assert result.exit_code == 0
            assert "Added GitHub Actions CI" in result.stdout

            # Check workflow was created
            assert (project / ".github" / "workflows" / "pr.yml").exists()

            # Check mpm.toml was updated
            with open(project / "mpm.toml", "rb") as f:
                config = tomllib.load(f)
            assert config["features"]["ci"] is True
        finally:
            os.chdir(original_dir)

    def test_add_ci_idempotent(self, run_mpm: Any, temp_dir: Path) -> None:
        """Test that running add ci twice is idempotent."""
        exit_code, _output, project = run_mpm("ci-idem-test", "--monorepo", "-y")
        assert exit_code == 0

        runner = CliRunner()
        original_dir = os.getcwd()
        os.chdir(project)

        try:
            runner.invoke(app, ["add", "ci"])
            result = runner.invoke(app, ["add", "ci"])
            assert result.exit_code == 0
            assert "already enabled" in result.stdout
        finally:
            os.chdir(original_dir)


class TestAddPypiCommand:
    """Test 'mpm add pypi' command."""

    def test_add_pypi_to_project(self, run_mpm: Any, temp_dir: Path) -> None:
        """Test adding PyPI publishing to a project."""
        exit_code, _output, project = run_mpm("pypi-test", "--monorepo", "-y")
        assert exit_code == 0

        runner = CliRunner()
        original_dir = os.getcwd()
        os.chdir(project)

        try:
            result = runner.invoke(app, ["add", "pypi"])
            assert result.exit_code == 0
            assert "Added PyPI publishing" in result.stdout

            # Should warn about CI not being enabled
            assert "CI is not enabled" in result.stdout

            # Check workflow was created
            assert (project / ".github" / "workflows" / "release.yml").exists()

            # Check mpm.toml was updated
            with open(project / "mpm.toml", "rb") as f:
                config = tomllib.load(f)
            assert config["features"]["pypi"] is True
        finally:
            os.chdir(original_dir)

    def test_add_pypi_with_ci(self, run_mpm: Any, temp_dir: Path) -> None:
        """Test adding PyPI after CI (no warning)."""
        exit_code, _output, project = run_mpm("pypi-ci-test", "--monorepo", "-y")
        assert exit_code == 0

        runner = CliRunner()
        original_dir = os.getcwd()
        os.chdir(project)

        try:
            # Add CI first
            runner.invoke(app, ["add", "ci"])

            # Then add PyPI
            result = runner.invoke(app, ["add", "pypi"])
            assert result.exit_code == 0

            # Should NOT warn about CI
            assert "CI is not enabled" not in result.stdout
        finally:
            os.chdir(original_dir)


class TestAddDocsCommand:
    """Test 'mpm add docs' command."""

    def test_add_docs_material_theme(self, run_mpm: Any, temp_dir: Path) -> None:
        """Test adding docs with material theme."""
        exit_code, _output, project = run_mpm("docs-test", "--monorepo", "-y")
        assert exit_code == 0

        runner = CliRunner()
        original_dir = os.getcwd()
        os.chdir(project)

        try:
            result = runner.invoke(app, ["add", "docs", "--theme", "material"])
            assert result.exit_code == 0
            assert "Added MkDocs documentation" in result.stdout

            # Check files were created
            assert (project / "mkdocs.yml").exists()
            assert (project / "docs" / "index.md").exists()

            # Check mkdocs.yml content
            mkdocs_content = (project / "mkdocs.yml").read_text()
            assert "material" in mkdocs_content.lower()

            # Check mpm.toml was updated
            with open(project / "mpm.toml", "rb") as f:
                config = tomllib.load(f)
            assert config["features"]["docs"] is True
            assert config["features"]["docs_theme"] == "material"
        finally:
            os.chdir(original_dir)

    def test_add_docs_shadcn_theme(self, run_mpm: Any, temp_dir: Path) -> None:
        """Test adding docs with shadcn theme."""
        exit_code, _output, project = run_mpm("docs-shadcn-test", "--monorepo", "-y")
        assert exit_code == 0

        runner = CliRunner()
        original_dir = os.getcwd()
        os.chdir(project)

        try:
            result = runner.invoke(app, ["add", "docs", "--theme", "shadcn"])
            assert result.exit_code == 0

            # Check mkdocs.yml has shadcn theme
            mkdocs_content = (project / "mkdocs.yml").read_text()
            assert "shadcn" in mkdocs_content.lower() or "terminal" in mkdocs_content.lower()

            # Check mpm.toml was updated
            with open(project / "mpm.toml", "rb") as f:
                config = tomllib.load(f)
            assert config["features"]["docs_theme"] == "shadcn"
        finally:
            os.chdir(original_dir)

    def test_add_docs_invalid_theme(self, run_mpm: Any, temp_dir: Path) -> None:
        """Test adding docs with invalid theme."""
        exit_code, _output, project = run_mpm("docs-invalid-test", "--monorepo", "-y")
        assert exit_code == 0

        runner = CliRunner()
        original_dir = os.getcwd()
        os.chdir(project)

        try:
            result = runner.invoke(app, ["add", "docs", "--theme", "invalid"])
            assert result.exit_code == 1
            assert "Invalid theme" in result.stdout
        finally:
            os.chdir(original_dir)

    def test_add_docs_updates_pyproject(self, run_mpm: Any, temp_dir: Path) -> None:
        """Test that add docs updates pyproject.toml with deps and tasks."""
        exit_code, _output, project = run_mpm("docs-pyproject-test", "--monorepo", "-y")
        assert exit_code == 0

        runner = CliRunner()
        original_dir = os.getcwd()
        os.chdir(project)

        try:
            result = runner.invoke(app, ["add", "docs"])
            assert result.exit_code == 0

            # Check pyproject.toml was updated
            with open(project / "pyproject.toml", "rb") as f:
                pyproject = tomllib.load(f)

            # Check mkdocs dependency was added
            dev_deps = pyproject.get("dependency-groups", {}).get("dev", [])
            assert any("mkdocs" in dep for dep in dev_deps)
        finally:
            os.chdir(original_dir)


class TestAddFeaturesRequiresMpmToml:
    """Test that feature commands require mpm.toml."""

    def test_add_docker_requires_project(self, temp_dir: Path) -> None:
        """Test that add docker fails outside a project."""
        runner = CliRunner()
        os.chdir(temp_dir)

        result = runner.invoke(app, ["add", "docker"])
        assert result.exit_code == 1
        assert "Not in an mpm project" in result.stdout

    def test_add_ci_requires_project(self, temp_dir: Path) -> None:
        """Test that add ci fails outside a project."""
        runner = CliRunner()
        os.chdir(temp_dir)

        result = runner.invoke(app, ["add", "ci"])
        assert result.exit_code == 1
        assert "Not in an mpm project" in result.stdout

    def test_add_docker_requires_mpm_toml(self, temp_dir: Path) -> None:
        """Test that add docker fails with workspace pyproject but no mpm.toml."""
        # Create a pyproject.toml with workspace config but no mpm.toml
        pyproject = temp_dir / "pyproject.toml"
        pyproject.write_text("""
[project]
name = "test"

[tool.uv.workspace]
members = ["apps/*", "libs/*"]
""")

        runner = CliRunner()
        os.chdir(temp_dir)

        result = runner.invoke(app, ["add", "docker"])
        assert result.exit_code == 1
        assert "No mpm.toml found" in result.stdout
