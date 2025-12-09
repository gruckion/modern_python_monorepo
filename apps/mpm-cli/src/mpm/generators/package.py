"""Package generator - creates lib and app packages."""

from pathlib import Path

from rich.console import Console

from mpm.generators.renderer import TemplateRenderer

console = Console()


def generate_lib_package(
    renderer: TemplateRenderer,
    project_root: Path,
    package_name: str,
    namespace: str,
    ctx: dict,
    is_sample: bool = False,
) -> None:
    """Generate a library package in libs/."""
    lib_dir = project_root / "libs" / package_name
    lib_dir.mkdir(parents=True, exist_ok=True)

    # Build context for this package
    pkg_ctx = {
        **ctx,
        "package_name": package_name,
        "package_description": f"{package_name.capitalize()} library",
        "namespace": namespace,
    }

    # Generate pyproject.toml (use sample template for greeter with cowsay)
    if is_sample and package_name == "greeter":
        renderer.render_to_file("samples/greeter/pyproject.toml.jinja", lib_dir / "pyproject.toml", pkg_ctx)
    else:
        renderer.render_to_file("monorepo/libs/pyproject.toml.jinja", lib_dir / "pyproject.toml", pkg_ctx)

    # Generate namespace package structure
    ns_dir = lib_dir / namespace / package_name
    ns_dir.mkdir(parents=True, exist_ok=True)

    # Generate __init__.py (use sample if is_sample, otherwise empty)
    if is_sample and package_name == "greeter":
        renderer.render_to_file("samples/greeter/__init__.py.jinja", ns_dir / "__init__.py", pkg_ctx)
    else:
        renderer.render_to_file("monorepo/libs/__init__.py.jinja", ns_dir / "__init__.py", pkg_ctx)

    # Create py.typed markers at both namespace and subpackage levels
    (lib_dir / namespace / "py.typed").touch()
    (ns_dir / "py.typed").touch()

    # Create tests directory
    tests_dir = lib_dir / "tests"
    tests_dir.mkdir(exist_ok=True)
    renderer.render_to_file("monorepo/libs/test_import.py.jinja", tests_dir / f"test_{package_name}_import.py", pkg_ctx)

    console.print(f"[green]\u2713[/green] Created library: libs/{package_name}")


def generate_app_package(
    renderer: TemplateRenderer,
    project_root: Path,
    package_name: str,
    namespace: str,
    ctx: dict,
    with_docker: bool = False,
    is_sample: bool = False,
) -> None:
    """Generate an application package in apps/."""
    app_dir = project_root / "apps" / package_name
    app_dir.mkdir(parents=True, exist_ok=True)

    # Build context for this package
    pkg_ctx = {
        **ctx,
        "package_name": package_name,
        "package_description": f"{package_name.capitalize()} application",
        "namespace": namespace,
        "with_docker": with_docker,
    }

    # For printer sample, it depends on greeter
    if is_sample and package_name == "printer":
        pkg_ctx["depends_on_greeter"] = True

    # Generate pyproject.toml
    renderer.render_to_file("monorepo/apps/pyproject.toml.jinja", app_dir / "pyproject.toml", pkg_ctx)

    # Generate namespace package structure
    ns_dir = app_dir / namespace / package_name
    ns_dir.mkdir(parents=True, exist_ok=True)

    # Generate __init__.py (use sample if is_sample, otherwise empty)
    if is_sample and package_name == "printer":
        renderer.render_to_file("samples/printer/__init__.py.jinja", ns_dir / "__init__.py", pkg_ctx)
    else:
        renderer.render_to_file("monorepo/apps/__init__.py.jinja", ns_dir / "__init__.py", pkg_ctx)

    # Create py.typed markers at both namespace and subpackage levels
    (app_dir / namespace / "py.typed").touch()
    (ns_dir / "py.typed").touch()

    # Create tests directory
    tests_dir = app_dir / "tests"
    tests_dir.mkdir(exist_ok=True)
    renderer.render_to_file("monorepo/apps/test_import.py.jinja", tests_dir / f"test_{package_name}_import.py", pkg_ctx)

    # Generate Dockerfile if requested
    if with_docker:
        renderer.render_to_file("docker/Dockerfile.jinja", app_dir / "Dockerfile", pkg_ctx)

    console.print(f"[green]\u2713[/green] Created application: apps/{package_name}")


def add_package(
    name: str,
    package_type: str,
    description: str = "",
    with_docker: bool = False,
    project_root: Path | None = None,
    namespace: str = "my_project",
) -> None:
    """Add a new package to an existing project."""
    from mpm.config import PythonVersion

    renderer = TemplateRenderer()
    root = project_root or Path.cwd()

    # Read Python version from .python-version file if it exists
    python_version = PythonVersion.PY313  # Default
    python_version_file = root / ".python-version"
    if python_version_file.exists():
        version_str = python_version_file.read_text().strip()
        # Map version string to PythonVersion enum
        version_map = {
            "3.11": PythonVersion.PY311,
            "3.12": PythonVersion.PY312,
            "3.13": PythonVersion.PY313,
        }
        # Handle versions like "3.13.1" by extracting major.minor
        major_minor = ".".join(version_str.split(".")[:2])
        if major_minor in version_map:
            python_version = version_map[major_minor]

    ctx = {
        "package_name": name,
        "package_description": description or f"{name.capitalize()} package",
        "namespace": namespace,
        "python_version": python_version,
        "with_docker": with_docker,
    }

    if package_type == "lib":
        generate_lib_package(renderer, root, name, namespace, ctx)
    else:
        generate_app_package(renderer, root, name, namespace, ctx, with_docker=with_docker)

    console.print("\n[dim]Run 'uv sync --all-packages' to update dependencies[/dim]")
