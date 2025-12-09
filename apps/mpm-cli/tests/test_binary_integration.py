"""Integration tests for MPM CLI installed as a standalone binary.

These tests verify that the mpm CLI works correctly when installed via `uv tool install`.
They test the full workflow: generate project, sync dependencies, run mkdocs server, and curl.
"""

import os
import shutil
import signal
import socket
import subprocess
import tempfile
import time
from pathlib import Path

import pytest


def find_free_port() -> int:
    """Find a free port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        s.listen(1)
        return s.getsockname()[1]


def wait_for_server(port: int, timeout: float = 30.0) -> bool:
    """Wait for a server to be ready on the given port."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect(("127.0.0.1", port))
                return True
        except (TimeoutError, ConnectionRefusedError):
            time.sleep(0.5)
    return False


@pytest.fixture
def mpm_binary() -> str:
    """Get the path to the mpm binary, ensuring it's installed."""
    # Check if mpm is available
    result = subprocess.run(["which", "mpm"], capture_output=True, text=True)
    if result.returncode != 0:
        pytest.skip("mpm binary not installed - run `uv tool install` first")
    return result.stdout.strip()


@pytest.fixture
def temp_project_dir():
    """Create a temporary directory for the test project."""
    tmpdir = tempfile.mkdtemp(prefix="mpm_binary_test_")
    yield Path(tmpdir)
    # Cleanup
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="Server tests are flaky in CI due to timing constraints",
)
class TestBinaryIntegration:
    """Test the mpm binary with full project generation and docs serving."""

    @pytest.mark.slow
    def test_binary_generates_project_with_material_docs(self, mpm_binary: str, temp_project_dir: Path) -> None:
        """Test that the binary generates a project with material docs that can be served."""
        project_name = "test-material-binary"
        port = find_free_port()

        # Step 1: Generate project using the standalone mpm binary
        result = subprocess.run(
            [
                mpm_binary,
                "new",
                project_name,
                "--monorepo",
                "--with-docs",
                "--docs-theme",
                "material",
                "-y",
            ],
            cwd=temp_project_dir,
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, f"mpm new failed: {result.stderr}"

        project_path = temp_project_dir / project_name
        assert project_path.exists(), "Project directory was not created"
        assert (project_path / "mkdocs.yml").exists(), "mkdocs.yml was not created"
        assert (project_path / "docs" / "index.md").exists(), "docs/index.md was not created"

        # Verify mkdocs.yml has material theme
        mkdocs_content = (project_path / "mkdocs.yml").read_text()
        assert "name: material" in mkdocs_content, "Material theme not configured"

        # Step 2: Sync dependencies in the generated project
        result = subprocess.run(
            ["uv", "sync", "--group", "docs"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=120,
        )
        assert result.returncode == 0, f"uv sync failed: {result.stderr}"

        # Step 3: Start mkdocs server
        server_process = subprocess.Popen(
            ["uv", "run", "mkdocs", "serve", "-a", f"127.0.0.1:{port}"],
            cwd=project_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid,  # Create new process group for cleanup
        )

        try:
            # Wait for server to be ready
            assert wait_for_server(port, timeout=30), "Server did not start in time"

            # Step 4: Curl the docs server
            # The site_url in mkdocs.yml causes a redirect, so we need to follow redirects
            result = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-L", f"http://127.0.0.1:{port}/"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            assert result.stdout.strip() == "200", f"Expected HTTP 200, got {result.stdout}"

        finally:
            # Cleanup: kill the server process group
            os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
            server_process.wait(timeout=5)

    @pytest.mark.slow
    def test_binary_generates_project_with_shadcn_docs(self, mpm_binary: str, temp_project_dir: Path) -> None:
        """Test that the binary generates a project with shadcn docs that can be served."""
        project_name = "test-shadcn-binary"
        port = find_free_port()

        # Step 1: Generate project using the standalone mpm binary
        result = subprocess.run(
            [
                mpm_binary,
                "new",
                project_name,
                "--monorepo",
                "--with-docs",
                "--docs-theme",
                "shadcn",
                "-y",
            ],
            cwd=temp_project_dir,
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, f"mpm new failed: {result.stderr}"

        project_path = temp_project_dir / project_name
        assert project_path.exists(), "Project directory was not created"
        assert (project_path / "mkdocs.yml").exists(), "mkdocs.yml was not created"

        # Verify mkdocs.yml has shadcn theme
        mkdocs_content = (project_path / "mkdocs.yml").read_text()
        assert "name: shadcn" in mkdocs_content, "Shadcn theme not configured"

        # Step 2: Sync dependencies in the generated project
        result = subprocess.run(
            ["uv", "sync", "--group", "docs"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=120,
        )
        assert result.returncode == 0, f"uv sync failed: {result.stderr}"

        # Step 3: The shadcn theme requires git commits to exist, make one
        subprocess.run(["git", "add", "."], cwd=project_path, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            cwd=project_path,
            capture_output=True,
        )

        # Step 4: Start mkdocs server
        server_process = subprocess.Popen(
            ["uv", "run", "mkdocs", "serve", "-a", f"127.0.0.1:{port}"],
            cwd=project_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid,
        )

        try:
            # Wait for server to be ready
            assert wait_for_server(port, timeout=30), "Server did not start in time"

            # Step 5: Curl the docs server
            result = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-L", f"http://127.0.0.1:{port}/"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            assert result.stdout.strip() == "200", f"Expected HTTP 200, got {result.stdout}"

        finally:
            # Cleanup: kill the server process group
            os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
            server_process.wait(timeout=5)

    @pytest.mark.slow
    def test_binary_version(self, mpm_binary: str) -> None:
        """Test that the binary reports its version."""
        result = subprocess.run(
            [mpm_binary, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "0.1.0" in result.stdout or "mpm" in result.stdout.lower()

    @pytest.mark.slow
    def test_binary_help(self, mpm_binary: str) -> None:
        """Test that the binary shows help."""
        result = subprocess.run(
            [mpm_binary, "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "Modern Python Monorepo CLI" in result.stdout
        assert "new" in result.stdout
        assert "add" in result.stdout
