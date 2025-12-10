"""End-to-end tests - verify generated projects actually work."""

import subprocess
from pathlib import Path
from typing import Any

import pytest


class TestGeneratedProjectsWork:
    """Test that generated projects can be installed and used."""

    @pytest.mark.slow
    def test_monorepo_uv_sync(self, run_mpm: Any) -> None:
        """Test that generated monorepo can run 'uv sync'."""
        exit_code, _output, project = run_mpm("e2e-sync-test", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0

        # Run uv sync in the generated project
        result = subprocess.run(
            ["uv", "sync", "--all-packages"],
            cwd=project,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"uv sync failed: {result.stderr}"
        assert (project / "uv.lock").exists()

    @pytest.mark.slow
    def test_monorepo_lint_passes(self, run_mpm: Any) -> None:
        """Test that generated code passes linting."""
        exit_code, _output, project = run_mpm("e2e-lint-test", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0

        # Install dependencies first
        subprocess.run(["uv", "sync", "--all-packages"], cwd=project, check=True)

        # Run ruff check
        result = subprocess.run(
            ["uv", "run", "ruff", "check", "."],
            cwd=project,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Linting failed: {result.stdout}\n{result.stderr}"

    @pytest.mark.slow
    def test_monorepo_format_passes(self, run_mpm: Any) -> None:
        """Test that generated code passes format check."""
        exit_code, _output, project = run_mpm("e2e-fmt-test", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0

        subprocess.run(["uv", "sync", "--all-packages"], cwd=project, check=True)

        result = subprocess.run(
            ["uv", "run", "ruff", "format", "--check", "."],
            cwd=project,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Format check failed: {result.stdout}\n{result.stderr}"

    @pytest.mark.slow
    def test_monorepo_type_check_passes(self, run_mpm: Any) -> None:
        """Test that generated code passes type checking."""
        exit_code, _output, project = run_mpm("e2e-typecheck-test", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0

        subprocess.run(["uv", "sync", "--all-packages"], cwd=project, check=True)

        result = subprocess.run(
            ["uv", "run", "ty", "check"],
            cwd=project,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Type check failed: {result.stdout}\n{result.stderr}"

    @pytest.mark.slow
    def test_monorepo_tests_pass(self, run_mpm: Any) -> None:
        """Test that generated project tests pass."""
        exit_code, _output, project = run_mpm("e2e-test-test", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0

        subprocess.run(["uv", "sync", "--all-packages"], cwd=project, check=True)

        result = subprocess.run(
            ["uv", "run", "pytest"],
            cwd=project,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Tests failed: {result.stdout}\n{result.stderr}"

    @pytest.mark.slow
    def test_monorepo_poe_all(self, run_mpm: Any) -> None:
        """Test that 'poe all' passes (fmt, lint, check, test)."""
        exit_code, _output, project = run_mpm("e2e-poe-test", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0

        subprocess.run(["uv", "sync", "--all-packages"], cwd=project, check=True)

        result = subprocess.run(
            ["uv", "run", "poe", "all"],
            cwd=project,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"poe all failed: {result.stdout}\n{result.stderr}"

    @pytest.mark.slow
    def test_single_package_works(self, run_mpm: Any) -> None:
        """Test that single package project works."""
        exit_code, _output, project = run_mpm("e2e-single-test", "--single", "-y")

        assert exit_code == 0

        result = subprocess.run(
            ["uv", "sync"],
            cwd=project,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"uv sync failed: {result.stderr}"

    @pytest.mark.slow
    def test_single_package_lint_passes(self, run_mpm: Any) -> None:
        """Test that single package code passes linting."""
        exit_code, _output, project = run_mpm("e2e-single-lint", "--single", "-y")

        assert exit_code == 0

        subprocess.run(["uv", "sync"], cwd=project, check=True)

        result = subprocess.run(
            ["uv", "run", "ruff", "check", "."],
            cwd=project,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Linting failed: {result.stdout}\n{result.stderr}"

    @pytest.mark.slow
    def test_single_package_tests_pass(self, run_mpm: Any) -> None:
        """Test that single package tests pass."""
        exit_code, _output, project = run_mpm("e2e-single-tests", "--single", "-y")

        assert exit_code == 0

        subprocess.run(["uv", "sync"], cwd=project, check=True)

        result = subprocess.run(
            ["uv", "run", "pytest"],
            cwd=project,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Tests failed: {result.stdout}\n{result.stderr}"

    @pytest.mark.slow
    @pytest.mark.skip(reason="Una doesn't support building wheels from sdist - known limitation")
    def test_lib_can_be_built(self, run_mpm: Any) -> None:
        """Test that a generated lib can be built into a wheel."""
        exit_code, _output, project = run_mpm("e2e-build-test", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0

        subprocess.run(["uv", "sync", "--all-packages"], cwd=project, check=True)

        greeter_dir = project / "libs" / "greeter"
        result = subprocess.run(
            ["uv", "build"],
            cwd=greeter_dir,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Build failed: {result.stderr}"
        assert (greeter_dir / "dist").is_dir()


class TestAddPackageCommand:
    """Test 'mpm add' command for adding packages to existing projects."""

    @pytest.mark.slow
    def test_add_lib_to_existing_project(self, run_mpm: Any, temp_dir: Path) -> None:
        """Test adding a library to existing project."""
        import os

        from typer.testing import CliRunner

        from mpm.cli import app

        # First create a project
        exit_code, _output, project = run_mpm("add-test", "--monorepo", "-y")
        assert exit_code == 0

        # Now add a library
        runner = CliRunner()
        original_dir = os.getcwd()
        os.chdir(project)

        try:
            result = runner.invoke(app, ["add", "lib", "auth"])

            assert result.exit_code == 0
            assert (project / "libs" / "auth").is_dir()
            assert (project / "libs" / "auth" / "pyproject.toml").exists()
        finally:
            os.chdir(original_dir)

    @pytest.mark.slow
    def test_add_app_with_docker(self, run_mpm: Any, temp_dir: Path) -> None:
        """Test adding an app with Docker support."""
        import os

        from typer.testing import CliRunner

        from mpm.cli import app

        exit_code, _output, project = run_mpm("add-app-test", "--monorepo", "-y")
        assert exit_code == 0

        runner = CliRunner()
        original_dir = os.getcwd()
        os.chdir(project)

        try:
            result = runner.invoke(app, ["add", "app", "api", "--docker"])

            assert result.exit_code == 0
            assert (project / "apps" / "api").is_dir()
            assert (project / "apps" / "api" / "Dockerfile").exists()
        finally:
            os.chdir(original_dir)

    @pytest.mark.slow
    def test_add_lib_reads_mpm_toml(self, run_mpm: Any, temp_dir: Path) -> None:
        """Test that 'mpm add lib' reads configuration from mpm.toml."""
        import os

        from typer.testing import CliRunner

        from mpm.cli import app

        # Create project with specific python version
        exit_code, _output, project = run_mpm("mpm-toml-test", "--monorepo", "--python", "3.12", "-y")
        assert exit_code == 0

        # Verify mpm.toml was created with correct python version
        assert (project / "mpm.toml").exists()

        runner = CliRunner()
        original_dir = os.getcwd()
        os.chdir(project)

        try:
            result = runner.invoke(app, ["add", "lib", "mylib"])
            assert result.exit_code == 0

            # Check that output mentions reading from mpm.toml
            assert "mpm.toml" in result.stdout

            # Check namespace was read from mpm.toml (project_name: mpm_toml_test)
            lib_dir = project / "libs" / "mylib" / "mpm_toml_test" / "mylib"
            assert lib_dir.is_dir(), (
                f"Expected namespace dir mpm_toml_test, got: " f"{list((project / 'libs' / 'mylib').iterdir())}"
            )

            # Check python version was read from mpm.toml
            lib_pyproject = project / "libs" / "mylib" / "pyproject.toml"
            content = lib_pyproject.read_text()
            assert 'requires-python = ">=3.12"' in content, f"Expected 3.12, got: {content}"
        finally:
            os.chdir(original_dir)

    @pytest.mark.slow
    def test_add_app_reads_mpm_toml(self, run_mpm: Any, temp_dir: Path) -> None:
        """Test that 'mpm add app' reads configuration from mpm.toml."""
        import os

        from typer.testing import CliRunner

        from mpm.cli import app

        # Create project with specific python version
        exit_code, _output, project = run_mpm("app-toml-test", "--monorepo", "--python", "3.11", "-y")
        assert exit_code == 0

        runner = CliRunner()
        original_dir = os.getcwd()
        os.chdir(project)

        try:
            result = runner.invoke(app, ["add", "app", "myapp"])
            assert result.exit_code == 0

            # Check namespace was read from mpm.toml (project_name: app_toml_test)
            app_dir = project / "apps" / "myapp" / "app_toml_test" / "myapp"
            assert app_dir.is_dir(), "Expected namespace dir app_toml_test"

            # Check python version was read from mpm.toml
            app_pyproject = project / "apps" / "myapp" / "pyproject.toml"
            content = app_pyproject.read_text()
            assert 'requires-python = ">=3.11"' in content
        finally:
            os.chdir(original_dir)


class TestAddAllFeaturesE2E:
    """E2E tests for adding all features sequentially."""

    @pytest.mark.slow
    def test_add_all_features_sequentially(self, run_mpm: Any, temp_dir: Path) -> None:
        """Test adding all features one by one to a project."""
        import os
        import tomllib

        from typer.testing import CliRunner

        from mpm.cli import app

        # Create a basic project
        exit_code, _output, project = run_mpm("full-e2e-test", "--monorepo", "-y")
        assert exit_code == 0
        assert (project / "mpm.toml").exists()

        runner = CliRunner()
        original_dir = os.getcwd()
        os.chdir(project)

        try:
            # Add docker
            result = runner.invoke(app, ["add", "docker"])
            assert result.exit_code == 0

            # Add CI
            result = runner.invoke(app, ["add", "ci"])
            assert result.exit_code == 0

            # Add PyPI
            result = runner.invoke(app, ["add", "pypi"])
            assert result.exit_code == 0

            # Add docs
            result = runner.invoke(app, ["add", "docs"])
            assert result.exit_code == 0

            # Verify all features are enabled in mpm.toml
            with open(project / "mpm.toml", "rb") as f:
                config = tomllib.load(f)

            assert config["features"]["docker"] is True
            assert config["features"]["ci"] is True
            assert config["features"]["pypi"] is True
            assert config["features"]["docs"] is True

            # Verify files exist
            assert (project / ".dockerignore").exists()
            assert (project / ".github" / "workflows" / "pr.yml").exists()
            assert (project / ".github" / "workflows" / "release.yml").exists()
            assert (project / "mkdocs.yml").exists()
            assert (project / "docs" / "index.md").exists()

        finally:
            os.chdir(original_dir)

    @pytest.mark.slow
    def test_project_works_after_adding_features(self, run_mpm: Any, temp_dir: Path) -> None:
        """Test that project still works after adding all features."""
        import os
        import subprocess

        from typer.testing import CliRunner

        from mpm.cli import app

        # Create a project with samples
        exit_code, _output, project = run_mpm("e2e-work-test", "--monorepo", "--with-samples", "-y")
        assert exit_code == 0

        runner = CliRunner()
        original_dir = os.getcwd()
        os.chdir(project)

        try:
            # Add all features
            runner.invoke(app, ["add", "docker"])
            runner.invoke(app, ["add", "ci"])
            runner.invoke(app, ["add", "pypi"])
            runner.invoke(app, ["add", "docs"])

            # Sync and verify project works
            result = subprocess.run(
                ["uv", "sync", "--all-packages"],
                capture_output=True,
                text=True,
            )
            assert result.returncode == 0, f"uv sync failed: {result.stderr}"

            # Run linting
            result = subprocess.run(
                ["uv", "run", "ruff", "check", "."],
                capture_output=True,
                text=True,
            )
            assert result.returncode == 0, f"Linting failed: {result.stdout}"

            # Run tests
            result = subprocess.run(
                ["uv", "run", "pytest"],
                capture_output=True,
                text=True,
            )
            assert result.returncode == 0, f"Tests failed: {result.stdout}"

        finally:
            os.chdir(original_dir)
