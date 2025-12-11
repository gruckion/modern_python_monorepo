"""Unit tests for template rendering."""

from pathlib import Path

from mpm.generators.renderer import TemplateRenderer


def test_renderer_initialization() -> None:
    """Test TemplateRenderer initializes correctly."""
    renderer = TemplateRenderer()
    assert renderer.env is not None


def test_render_base_pyproject(temp_dir: Path) -> None:
    """Test rendering base pyproject.toml template."""
    renderer = TemplateRenderer()

    from mpm.config import DocsTheme, LicenseType, ProjectStructure, PythonVersion

    context = {
        "project_slug": "test-project",
        "project_description": "A test project",
        "python_version": PythonVersion.PY313,
        "namespace": "test_project",
        "structure": ProjectStructure.MONOREPO,
        "with_docs": False,
        "docs_theme": DocsTheme.MATERIAL,
        "license_type": LicenseType.MIT,
    }

    content = renderer.render("base/pyproject.toml.jinja", context)
    assert "test-project" in content
    assert "3.13" in content
    assert "test_project" in content
    assert "[tool.uv.workspace]" in content


def test_render_single_package_pyproject(temp_dir: Path) -> None:
    """Test rendering single package pyproject.toml."""
    renderer = TemplateRenderer()

    from mpm.config import DocsTheme, LicenseType, ProjectStructure, PythonVersion

    context = {
        "project_slug": "single-app",
        "project_description": "A single package",
        "python_version": PythonVersion.PY313,
        "namespace": "single_app",
        "structure": ProjectStructure.SINGLE,
        "with_docs": False,
        "docs_theme": DocsTheme.MATERIAL,
        "license_type": LicenseType.MIT,
    }

    content = renderer.render("base/pyproject.toml.jinja", context)
    assert "single-app" in content
    # Single package should not have workspace config
    assert "[tool.uv.workspace]" not in content


def test_render_to_file(temp_dir: Path) -> None:
    """Test rendering template directly to file."""
    renderer = TemplateRenderer()
    output_file = temp_dir / "test_output.txt"

    from mpm.config import DocsTheme, LicenseType, ProjectStructure, PythonVersion

    context = {
        "project_slug": "my-app",
        "python_version": PythonVersion.PY313,
        "namespace": "my_app",
        "structure": ProjectStructure.MONOREPO,
        "with_docs": False,
        "docs_theme": DocsTheme.MATERIAL,
        "license_type": LicenseType.MIT,
        "project_description": "",
    }

    renderer.render_to_file("base/pyproject.toml.jinja", output_file, context)

    assert output_file.exists()
    content = output_file.read_text()
    assert "my-app" in content


def test_render_readme(temp_dir: Path) -> None:
    """Test rendering README.md template."""
    renderer = TemplateRenderer()

    from mpm.config import DocsTheme, LicenseType, ProjectStructure, PythonVersion

    context = {
        "project_name": "Readme Test",
        "project_slug": "readme-test",
        "project_description": "Test description",
        "python_version": PythonVersion.PY313,
        "namespace": "readme_test",
        "structure": ProjectStructure.MONOREPO,
        "with_docs": True,
        "with_docker": True,
        "with_samples": True,
        "with_precommit": True,
        "docs_theme": DocsTheme.MATERIAL,
        "license_type": LicenseType.MIT,
        "github_owner": "testuser",
    }

    content = renderer.render("base/README.md.jinja", context)
    assert "# Readme Test" in content
    assert "Test description" in content
    assert "Docker" in content
    assert "Documentation" in content


def test_render_lib_pyproject(temp_dir: Path) -> None:
    """Test rendering library pyproject.toml template."""
    renderer = TemplateRenderer()

    from mpm.config import PythonVersion

    context = {
        "package_name": "mylib",
        "package_description": "My library",
        "namespace": "test_project",
        "python_version": PythonVersion.PY313,
    }

    content = renderer.render("monorepo/libs/pyproject.toml.jinja", context)
    assert 'name = "mylib"' in content
    assert 'dynamic = ["una"]' in content
    assert "hatchling" in content
    assert "hatch-una" in content


def test_copy_static(temp_dir: Path) -> None:
    """Test copying static files."""
    renderer = TemplateRenderer()
    output_file = temp_dir / ".gitignore"

    renderer.copy_static("base/.gitignore", output_file)

    assert output_file.exists()
    content = output_file.read_text()
    assert "__pycache__" in content
    assert ".venv" in content
