"""Tests for CLI."""

import tempfile
from pathlib import Path

from typer.testing import CliRunner

from modern_python_monorepo.mpm.cli import app

runner = CliRunner()


class TestCLI:
    """Tests for CLI commands."""

    def test_version(self) -> None:
        """Test version flag."""
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "mpm version" in result.stdout

    def test_help(self) -> None:
        """Test help flag."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Modern Python Monorepo" in result.stdout

    def test_create_project_non_interactive(self) -> None:
        """Test creating project in non-interactive mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with runner.isolated_filesystem(temp_dir=tmpdir):
                result = runner.invoke(app, ["new", "my-project", "--monorepo", "--yes"])
                assert result.exit_code == 0
                assert (Path.cwd() / "my-project" / "pyproject.toml").exists()

    def test_create_project_with_docker(self) -> None:
        """Test creating project with Docker."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with runner.isolated_filesystem(temp_dir=tmpdir):
                result = runner.invoke(
                    app,
                    ["new", "my-project", "--monorepo", "--with-docker", "--with-samples", "--yes"],
                )
                assert result.exit_code == 0
                assert (Path.cwd() / "my-project" / "docker-compose.yml").exists()

    def test_add_subcommand_help(self) -> None:
        """Test add subcommand help."""
        result = runner.invoke(app, ["add", "--help"])
        assert result.exit_code == 0
        assert "package" in result.stdout.lower()

    def test_add_lib_help(self) -> None:
        """Test add-lib help."""
        result = runner.invoke(app, ["add-lib", "--help"])
        assert result.exit_code == 0
        assert "library" in result.stdout.lower()

    def test_add_app_help(self) -> None:
        """Test add-app help."""
        result = runner.invoke(app, ["add-app", "--help"])
        assert result.exit_code == 0
        assert "application" in result.stdout.lower()
