"""Shared test fixtures for MPM CLI tests."""

import os
import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
from typer.testing import CliRunner

from mpm.cli import app

# Store the original directory at module load time
_PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent.resolve()


@pytest.fixture
def cli_runner() -> CliRunner:
    """Typer CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_dir() -> Generator[Path]:
    """Create a temporary directory for test output."""
    # Always ensure we're in a valid directory before creating temp dir
    os.chdir(_PROJECT_ROOT)
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)
    # Ensure we restore to project root after temp dir is cleaned up
    os.chdir(_PROJECT_ROOT)


@pytest.fixture
def run_mpm(cli_runner: CliRunner, temp_dir: Path) -> Any:
    """Factory fixture to run MPM CLI in temp directory.

    By default, adds --no-sync to skip uv sync for faster tests.
    Tests that need sync behavior should run `uv sync` explicitly.
    """

    def _run_mpm(*args: str, with_sync: bool = False) -> tuple[int, str, Path]:
        """Run mpm new with args, return (exit_code, output, project_path).

        Args:
            *args: CLI arguments to pass to mpm new
            with_sync: If True, run uv sync after generation (default: False for speed)
        """
        os.chdir(temp_dir)
        try:
            # Prepend "new" command and add --no-sync by default for faster tests
            cmd_args = ["new", *args]
            if not with_sync and "--no-sync" not in args:
                cmd_args.append("--no-sync")
            result = cli_runner.invoke(app, cmd_args)
            # Find generated project directory
            dirs = [d for d in temp_dir.iterdir() if d.is_dir()]
            project_path = dirs[0] if dirs else temp_dir
            return result.exit_code, result.stdout, project_path
        finally:
            os.chdir(_PROJECT_ROOT)

    return _run_mpm


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest markers."""
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')")
