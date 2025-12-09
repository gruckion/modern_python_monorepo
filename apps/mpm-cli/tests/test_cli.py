"""Unit tests for CLI commands."""

import os
import re

from typer.testing import CliRunner

from mpm.cli import app

# Regex to strip ANSI escape codes from output (for CI compatibility)
_ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")


def strip_ansi(text: str) -> str:
    """Strip ANSI escape codes from text for reliable assertions."""
    return _ANSI_ESCAPE.sub("", text)


def test_version(cli_runner: CliRunner) -> None:
    """Test --version flag."""
    result = cli_runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "mpm version" in result.stdout


def test_help(cli_runner: CliRunner) -> None:
    """Test --help flag."""
    result = cli_runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = strip_ansi(result.stdout)
    assert "Modern Python Monorepo" in output
    assert "--monorepo" in output
    assert "--single" in output
    assert "new" in output
    assert "add" in output


def test_new_help(cli_runner: CliRunner) -> None:
    """Test mpm new --help."""
    result = cli_runner.invoke(app, ["new", "--help"])
    assert result.exit_code == 0
    output = strip_ansi(result.stdout)
    assert "PROJECT_NAME" in output
    assert "--monorepo" in output
    assert "--single" in output


def test_add_help(cli_runner: CliRunner) -> None:
    """Test mpm add --help."""
    result = cli_runner.invoke(app, ["add", "--help"])
    assert result.exit_code == 0
    output = strip_ansi(result.stdout)
    assert "lib" in output
    assert "app" in output


def test_add_lib_help(cli_runner: CliRunner) -> None:
    """Test mpm add lib --help."""
    result = cli_runner.invoke(app, ["add", "lib", "--help"])
    assert result.exit_code == 0
    output = strip_ansi(result.stdout)
    assert "Library name" in output


def test_add_app_help(cli_runner: CliRunner) -> None:
    """Test mpm add app --help."""
    result = cli_runner.invoke(app, ["add", "app", "--help"])
    assert result.exit_code == 0
    output = strip_ansi(result.stdout)
    assert "Application name" in output
    assert "--docker" in output


def test_basic_monorepo_creation(cli_runner: CliRunner, temp_dir) -> None:
    """Test basic monorepo creation with mpm new."""
    os.chdir(temp_dir)
    result = cli_runner.invoke(app, ["new", "test-project", "--monorepo", "-y"])
    assert result.exit_code == 0
    assert "Project Created" in result.stdout


def test_single_package_creation(cli_runner: CliRunner, temp_dir) -> None:
    """Test single package creation with mpm new."""
    os.chdir(temp_dir)
    result = cli_runner.invoke(app, ["new", "test-single", "--single", "-y"])
    assert result.exit_code == 0
    assert "Project Created" in result.stdout


def test_monorepo_with_defaults(cli_runner: CliRunner, temp_dir) -> None:
    """Test creating monorepo with just --monorepo flag (default project name)."""
    os.chdir(temp_dir)
    result = cli_runner.invoke(app, ["--monorepo", "-y"])
    assert result.exit_code == 0
    assert "Project Created" in result.stdout


def test_add_lib_sets_python_version(cli_runner: CliRunner, temp_dir) -> None:
    """Test that 'mpm add lib' correctly sets requires-python from .python-version."""

    os.chdir(temp_dir)

    # First create a monorepo project
    result = cli_runner.invoke(app, ["new", "test-project", "--monorepo", "-y"])
    assert result.exit_code == 0

    # Change to the project directory
    project_dir = temp_dir / "test-project"
    os.chdir(project_dir)

    # Verify .python-version exists and has a version
    python_version_file = project_dir / ".python-version"
    assert python_version_file.exists(), ".python-version file should exist"
    python_version = python_version_file.read_text().strip()
    assert python_version, ".python-version should not be empty"

    # Add a new library
    result = cli_runner.invoke(app, ["add", "lib", "myutils"])
    assert result.exit_code == 0
    assert "Created library" in result.stdout

    # Check that the generated pyproject.toml has valid requires-python
    lib_pyproject = project_dir / "libs" / "myutils" / "pyproject.toml"
    assert lib_pyproject.exists(), "Library pyproject.toml should exist"

    content = lib_pyproject.read_text()

    # The requires-python should NOT be just ">=" (the bug)
    assert (
        'requires-python = ">="' not in content
    ), 'requires-python should not be empty! Got invalid: requires-python = ">="'

    # It should have a valid version specifier
    assert (
        f">={python_version}" in content or 'requires-python = ">=3.' in content
    ), f"requires-python should contain a valid version. Content: {content}"


def test_add_app_sets_python_version(cli_runner: CliRunner, temp_dir) -> None:
    """Test that 'mpm add app' correctly sets requires-python from .python-version."""

    os.chdir(temp_dir)

    # First create a monorepo project
    result = cli_runner.invoke(app, ["new", "test-project", "--monorepo", "-y"])
    assert result.exit_code == 0

    # Change to the project directory
    project_dir = temp_dir / "test-project"
    os.chdir(project_dir)

    # Add a new application
    result = cli_runner.invoke(app, ["add", "app", "myapp"])
    assert result.exit_code == 0
    assert "Created application" in result.stdout

    # Check that the generated pyproject.toml has valid requires-python
    app_pyproject = project_dir / "apps" / "myapp" / "pyproject.toml"
    assert app_pyproject.exists(), "Application pyproject.toml should exist"

    content = app_pyproject.read_text()

    # The requires-python should NOT be just ">=" (the bug)
    assert (
        'requires-python = ">="' not in content
    ), 'requires-python should not be empty! Got invalid: requires-python = ">="'

    # It should have a valid version specifier
    assert 'requires-python = ">=3.' in content, f"requires-python should contain a valid version. Content: {content}"
