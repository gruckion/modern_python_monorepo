"""Integration tests for MPM CLI - tests full CLI execution with various configs."""

from typing import Any

import pytest


class TestMonorepoGeneration:
    """Test monorepo project generation."""

    def test_basic_monorepo(self, run_mpm: Any) -> None:
        """Test basic monorepo generation."""
        exit_code, _output, project = run_mpm("test-project", "--monorepo", "-y")

        assert exit_code == 0
        assert project.exists()
        assert (project / "pyproject.toml").exists()
        assert (project / "libs").is_dir()
        assert (project / "apps").is_dir()
        assert (project / ".gitignore").exists()
        assert (project / ".python-version").exists()

    def test_monorepo_with_samples(self, run_mpm: Any) -> None:
        """Test monorepo with sample packages."""
        exit_code, _output, project = run_mpm("sample-project", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0

        # Verify greeter lib exists
        greeter = project / "libs" / "greeter"
        assert greeter.is_dir()
        assert (greeter / "pyproject.toml").exists()

        # Verify printer app exists
        printer = project / "apps" / "printer"
        assert printer.is_dir()
        assert (printer / "pyproject.toml").exists()

        # Verify namespace structure
        assert (greeter / "sample_project" / "greeter" / "__init__.py").exists()
        assert (printer / "sample_project" / "printer" / "__init__.py").exists()

        # Verify py.typed markers
        assert (greeter / "sample_project" / "greeter" / "py.typed").exists()
        assert (printer / "sample_project" / "printer" / "py.typed").exists()

    def test_monorepo_with_docker(self, run_mpm: Any) -> None:
        """Test monorepo with Docker configuration.

        Note: Without --with-samples, only .dockerignore is generated.
        docker-compose.yml and docker-bake.hcl require Dockerfiles to exist.
        """
        exit_code, _output, project = run_mpm("docker-project", "--monorepo", "--with-docker", "-y")

        assert exit_code == 0
        # .dockerignore is always generated with --with-docker
        assert (project / ".dockerignore").exists()
        # docker-compose.yml and docker-bake.hcl require samples (Dockerfile exists in apps/printer)
        # Without samples, these are not generated
        assert not (project / "docker-compose.yml").exists()
        assert not (project / "docker-bake.hcl").exists()

    def test_monorepo_with_ci(self, run_mpm: Any) -> None:
        """Test monorepo with GitHub Actions CI."""
        exit_code, _output, project = run_mpm("ci-project", "--monorepo", "--with-ci", "-y")

        assert exit_code == 0
        workflows = project / ".github" / "workflows"
        assert workflows.is_dir()
        assert (workflows / "pr.yml").exists()

    def test_monorepo_with_pypi(self, run_mpm: Any) -> None:
        """Test monorepo with PyPI publishing workflow."""
        exit_code, _output, project = run_mpm("pypi-project", "--monorepo", "--with-ci", "--with-pypi", "-y")

        assert exit_code == 0
        workflows = project / ".github" / "workflows"
        assert (workflows / "pr.yml").exists()
        assert (workflows / "release.yml").exists()

    def test_monorepo_with_docs_material(self, run_mpm: Any) -> None:
        """Test monorepo with MkDocs Material theme."""
        exit_code, _output, project = run_mpm(
            "docs-project", "--monorepo", "--with-docs", "--docs-theme", "material", "-y"
        )

        assert exit_code == 0
        assert (project / "mkdocs.yml").exists()
        assert (project / "docs" / "index.md").exists()

        mkdocs_content = (project / "mkdocs.yml").read_text()
        assert "material" in mkdocs_content.lower()

    def test_monorepo_with_docs_shadcn(self, run_mpm: Any) -> None:
        """Test monorepo with MkDocs shadcn theme."""
        exit_code, _output, project = run_mpm(
            "shadcn-project", "--monorepo", "--with-docs", "--docs-theme", "shadcn", "-y"
        )

        assert exit_code == 0
        assert (project / "mkdocs.yml").exists()

        mkdocs_content = (project / "mkdocs.yml").read_text()
        assert "shadcn" in mkdocs_content.lower()

    def test_monorepo_full_features(self, run_mpm: Any) -> None:
        """Test monorepo with all features enabled."""
        exit_code, _output, project = run_mpm(
            "full-project",
            "--monorepo",
            "--with-samples",
            "--with-docker",
            "--with-ci",
            "--with-pypi",
            "--with-docs",
            "-y",
        )

        assert exit_code == 0

        # All features present
        assert (project / "libs" / "greeter").is_dir()
        assert (project / "apps" / "printer").is_dir()
        assert (project / "docker-compose.yml").exists()
        assert (project / ".github" / "workflows" / "pr.yml").exists()
        assert (project / ".github" / "workflows" / "release.yml").exists()
        assert (project / "mkdocs.yml").exists()


class TestSinglePackageGeneration:
    """Test single package project generation."""

    def test_basic_single_package(self, run_mpm: Any) -> None:
        """Test basic single package generation."""
        exit_code, _output, project = run_mpm("single-project", "--single", "-y")

        assert exit_code == 0
        assert project.exists()
        assert (project / "pyproject.toml").exists()
        assert (project / "src" / "single_project" / "__init__.py").exists()
        assert (project / "src" / "single_project" / "py.typed").exists()

        # Should NOT have monorepo structure
        assert not (project / "libs").exists()
        assert not (project / "apps").exists()

    def test_single_package_with_docker(self, run_mpm: Any) -> None:
        """Test single package with Docker."""
        exit_code, _output, project = run_mpm("docker-single", "--single", "--with-docker", "-y")

        assert exit_code == 0
        assert (project / "Dockerfile").exists()
        assert (project / "docker-compose.yml").exists()

    def test_single_package_has_tests(self, run_mpm: Any) -> None:
        """Test single package includes tests directory."""
        exit_code, _output, project = run_mpm("test-single", "--single", "-y")

        assert exit_code == 0
        assert (project / "tests").is_dir()
        assert (project / "tests" / "test_import.py").exists()


class TestPythonVersions:
    """Test different Python version configurations."""

    @pytest.mark.parametrize("version", ["3.11", "3.12", "3.13"])
    def test_python_versions(self, run_mpm: Any, version: str) -> None:
        """Test generation with different Python versions."""
        exit_code, _output, project = run_mpm(
            f"py{version.replace('.', '')}-project",
            "--monorepo",
            "--python",
            version,
            "-y",
        )

        assert exit_code == 0

        pyproject = (project / "pyproject.toml").read_text()
        assert f">={version}" in pyproject

        python_version_file = (project / ".python-version").read_text()
        assert version in python_version_file


class TestLicenses:
    """Test different license configurations."""

    @pytest.mark.parametrize(
        ("license_type", "expected"),
        [
            ("MIT", "MIT License"),
            ("Apache-2.0", "Apache License"),
            ("GPL-3.0", "GNU GENERAL PUBLIC LICENSE"),
        ],
    )
    def test_license_types(self, run_mpm: Any, license_type: str, expected: str) -> None:
        """Test generation with different licenses."""
        exit_code, _output, project = run_mpm(
            f"{license_type.lower().replace('.', '')}-project",
            "--monorepo",
            "--license",
            license_type,
            "-y",
        )

        assert exit_code == 0
        assert (project / "LICENSE").exists()

        license_content = (project / "LICENSE").read_text()
        assert expected in license_content

    def test_no_license(self, run_mpm: Any) -> None:
        """Test generation without license."""
        exit_code, _output, project = run_mpm(
            "no-license-project",
            "--monorepo",
            "--license",
            "none",
            "-y",
        )

        assert exit_code == 0
        assert not (project / "LICENSE").exists()


class TestNoGit:
    """Test --no-git flag."""

    def test_no_git_initialization(self, run_mpm: Any) -> None:
        """Test that --no-git skips git init."""
        exit_code, _output, project = run_mpm("no-git-project", "--monorepo", "--no-git", "-y")

        assert exit_code == 0
        assert not (project / ".git").exists()


class TestGeneratedFileContents:
    """Test that generated file contents are correct."""

    def test_pyproject_toml_content(self, run_mpm: Any) -> None:
        """Verify pyproject.toml has correct structure."""
        exit_code, output, project = run_mpm("content-test", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0

        # Root pyproject.toml
        root_pyproject = (project / "pyproject.toml").read_text()
        assert "[tool.uv.workspace]" in root_pyproject
        assert "[tool.una]" in root_pyproject
        assert "[tool.ruff]" in root_pyproject
        assert "[tool.pytest.ini_options]" in root_pyproject
        assert "[tool.poe.tasks]" in root_pyproject

        # Lib pyproject.toml
        lib_pyproject = (project / "libs" / "greeter" / "pyproject.toml").read_text()
        assert 'dynamic = ["una"]' in lib_pyproject
        assert "hatchling" in lib_pyproject
        assert "hatch-una" in lib_pyproject
        assert "[tool.hatch.build.hooks.una-build]" in lib_pyproject

    def test_namespace_consistency(self, run_mpm: Any) -> None:
        """Verify namespace is consistent across all files."""
        exit_code, output, project = run_mpm("my-namespace-test", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0

        # Namespace should be "my_namespace_test" (underscores)
        expected_namespace = "my_namespace_test"

        # Check root pyproject.toml
        root_pyproject = (project / "pyproject.toml").read_text()
        assert f'namespace = "{expected_namespace}"' in root_pyproject

        # Check directory structure
        assert (project / "libs" / "greeter" / expected_namespace / "greeter").is_dir()

    def test_greeter_has_cowsay_dependency(self, run_mpm: Any) -> None:
        """Test that greeter sample has cowsay dependency."""
        exit_code, output, project = run_mpm("cowsay-test", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0

        greeter_pyproject = (project / "libs" / "greeter" / "pyproject.toml").read_text()
        assert "cowsay" in greeter_pyproject

    def test_printer_depends_on_greeter(self, run_mpm: Any) -> None:
        """Test that printer sample depends on greeter."""
        exit_code, output, project = run_mpm("dep-test", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0

        printer_pyproject = (project / "apps" / "printer" / "pyproject.toml").read_text()
        assert "greeter" in printer_pyproject
        assert "workspace = true" in printer_pyproject


class TestBugFixes:
    """Test that bug fixes from CLI_features_missing.md are applied."""

    def test_license_has_markdown_header(self, run_mpm: Any) -> None:
        """Verify LICENSE file has markdown header (A.7 fix)."""
        exit_code, output, project = run_mpm("license-header-test", "--monorepo", "--license", "MIT", "-y")

        assert exit_code == 0
        license_content = (project / "LICENSE").read_text()
        assert license_content.startswith("# MIT License")

    def test_license_has_current_year(self, run_mpm: Any) -> None:
        """Verify LICENSE file has current year (A.7 fix)."""
        from datetime import datetime

        exit_code, output, project = run_mpm("license-year-test", "--monorepo", "-y")

        assert exit_code == 0
        license_content = (project / "LICENSE").read_text()
        current_year = str(datetime.now().year)
        assert current_year in license_content

    def test_license_has_project_name(self, run_mpm: Any) -> None:
        """Verify LICENSE file has project name in copyright (A.7 fix)."""
        exit_code, output, project = run_mpm("my-cool-project", "--monorepo", "-y")

        assert exit_code == 0
        license_content = (project / "LICENSE").read_text()
        # Project name should be capitalized
        assert "My_cool_project Contributors" in license_content

    def test_precommit_has_header_comment(self, run_mpm: Any) -> None:
        """Verify .pre-commit-config.yaml has prek header comment (A.6 fix)."""
        exit_code, output, project = run_mpm("precommit-test", "--monorepo", "-y")

        assert exit_code == 0
        precommit = (project / ".pre-commit-config.yaml").read_text()
        assert "prek hooks configuration" in precommit
        assert "prek install" in precommit

    def test_precommit_has_ruff_config_args(self, run_mpm: Any) -> None:
        """Verify .pre-commit-config.yaml has --config=pyproject.toml for ruff (A.6 fix)."""
        exit_code, output, project = run_mpm("ruff-args-test", "--monorepo", "-y")

        assert exit_code == 0
        precommit = (project / ".pre-commit-config.yaml").read_text()
        assert "--config=pyproject.toml" in precommit

    def test_precommit_has_check_toml(self, run_mpm: Any) -> None:
        """Verify .pre-commit-config.yaml has check-toml hook (A.6 fix)."""
        exit_code, output, project = run_mpm("check-toml-test", "--monorepo", "-y")

        assert exit_code == 0
        precommit = (project / ".pre-commit-config.yaml").read_text()
        assert "check-toml" in precommit

    def test_precommit_has_maxkb_arg(self, run_mpm: Any) -> None:
        """Verify .pre-commit-config.yaml has --maxkb=1000 for large files (A.6 fix)."""
        exit_code, output, project = run_mpm("maxkb-test", "--monorepo", "-y")

        assert exit_code == 0
        precommit = (project / ".pre-commit-config.yaml").read_text()
        assert "--maxkb=1000" in precommit

    def test_precommit_uses_builtin_hooks(self, run_mpm: Any) -> None:
        """Verify .pre-commit-config.yaml uses builtin repo for prek (A.6 fix)."""
        exit_code, output, project = run_mpm("builtin-test", "--monorepo", "-y")

        assert exit_code == 0
        precommit = (project / ".pre-commit-config.yaml").read_text()
        assert "repo: builtin" in precommit

    def test_printer_import_is_correct(self, run_mpm: Any) -> None:
        """Verify printer __init__.py uses correct import (A.5 fix)."""
        exit_code, output, project = run_mpm("import-test", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0
        printer_init = (project / "apps" / "printer" / "import_test" / "printer" / "__init__.py").read_text()
        # Should import the namespace package, not greeter directly
        assert "from import_test import greeter" in printer_init

    def test_pryml_has_correct_format(self, run_mpm: Any) -> None:
        """Verify pr.yml has no YAML syntax errors (A.3 fix)."""
        import yaml

        exit_code, output, project = run_mpm("pr-yml-test", "--monorepo", "--with-ci", "-y")

        assert exit_code == 0
        pr_yml_path = project / ".github" / "workflows" / "pr.yml"
        pr_yml_content = pr_yml_path.read_text()
        # Should parse without errors
        parsed = yaml.safe_load(pr_yml_content)
        assert parsed is not None
        assert "jobs" in parsed

    def test_pryml_has_lockfile_check(self, run_mpm: Any) -> None:
        """Verify pr.yml has lockfile check step (A.3 fix)."""
        exit_code, output, project = run_mpm("lockfile-test", "--monorepo", "--with-ci", "-y")

        assert exit_code == 0
        pr_yml = (project / ".github" / "workflows" / "pr.yml").read_text()
        assert "Check lockfile is up to date" in pr_yml

    def test_pryll_has_prek_action(self, run_mpm: Any) -> None:
        """Verify pr.yml has prek action (A.3 fix)."""
        exit_code, output, project = run_mpm("prek-action-test", "--monorepo", "--with-ci", "-y")

        assert exit_code == 0
        pr_yml = (project / ".github" / "workflows" / "pr.yml").read_text()
        assert "j178/prek-action" in pr_yml

    def test_gitignore_is_minimal(self, run_mpm: Any) -> None:
        """Verify .gitignore is not bloated (issue 10 fix)."""
        exit_code, output, project = run_mpm("gitignore-test", "--monorepo", "-y")

        assert exit_code == 0
        gitignore_lines = (project / ".gitignore").read_text().strip().split("\n")
        # Should be under 25 lines (reference is ~19)
        assert len(gitignore_lines) < 25

    def test_gitignore_does_not_ignore_python_version(self, run_mpm: Any) -> None:
        """Verify .gitignore does not ignore .python-version (issue 10 fix)."""
        exit_code, output, project = run_mpm("pyversion-test", "--monorepo", "-y")

        assert exit_code == 0
        gitignore = (project / ".gitignore").read_text()
        assert ".python-version" not in gitignore

    def test_dockerignore_is_minimal(self, run_mpm: Any) -> None:
        """Verify .dockerignore is not bloated (issue 15 fix)."""
        exit_code, output, project = run_mpm("dockerignore-test", "--monorepo", "--with-docker", "-y")

        assert exit_code == 0
        dockerignore_lines = (project / ".dockerignore").read_text().strip().split("\n")
        # Should be under 25 lines (reference is ~20)
        assert len(dockerignore_lines) < 25

    def test_namespace_level_py_typed_exists(self, run_mpm: Any) -> None:
        """Verify namespace-level py.typed markers exist (issue 7 fix)."""
        exit_code, output, project = run_mpm("pytyped-test", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0

        # Check namespace-level py.typed in both lib and app
        assert (project / "libs" / "greeter" / "pytyped_test" / "py.typed").exists()
        assert (project / "apps" / "printer" / "pytyped_test" / "py.typed").exists()

    def test_vscode_config_exists(self, run_mpm: Any) -> None:
        """Verify .vscode directory is created (issue 13 fix)."""
        exit_code, output, project = run_mpm("vscode-test", "--monorepo", "-y")

        assert exit_code == 0
        assert (project / ".vscode").is_dir()
        assert (project / ".vscode" / "extensions.json").exists()
        assert (project / ".vscode" / "settings.json").exists()

    def test_pyproject_has_mermaid_plugin(self, run_mpm: Any) -> None:
        """Verify pyproject.toml includes mermaid plugin in docs deps (A.1 fix)."""
        exit_code, output, project = run_mpm("mermaid-test", "--monorepo", "--with-docs", "-y")

        assert exit_code == 0
        pyproject = (project / "pyproject.toml").read_text()
        assert "mkdocs-mermaid2-plugin" in pyproject

    def test_pyproject_has_hooks_task(self, run_mpm: Any) -> None:
        """Verify pyproject.toml has prek hooks task (A.1 fix)."""
        exit_code, output, project = run_mpm("hooks-test", "--monorepo", "-y")

        assert exit_code == 0
        pyproject = (project / "pyproject.toml").read_text()
        assert 'hooks = "prek install"' in pyproject
        assert '"hooks:run" = "prek run --all-files"' in pyproject

    def test_mkdocs_has_edit_uri(self, run_mpm: Any) -> None:
        """Verify mkdocs.yml has edit_uri (A.2 fix)."""
        exit_code, output, project = run_mpm("edituri-test", "--monorepo", "--with-docs", "-y")

        assert exit_code == 0
        mkdocs = (project / "mkdocs.yml").read_text()
        assert "edit_uri:" in mkdocs

    def test_mkdocs_has_mermaid2_plugin(self, run_mpm: Any) -> None:
        """Verify mkdocs.yml has mermaid2 plugin (A.2 fix)."""
        exit_code, output, project = run_mpm("mermaid2-test", "--monorepo", "--with-docs", "-y")

        assert exit_code == 0
        mkdocs = (project / "mkdocs.yml").read_text()
        assert "mermaid2" in mkdocs

    def test_dockerfile_has_cache_mounts(self, run_mpm: Any) -> None:
        """Verify Dockerfile has BuildKit cache mounts (A.4 fix)."""
        exit_code, output, project = run_mpm("cache-test", "--monorepo", "--with-docker", "--with-samples", "-y")

        assert exit_code == 0
        dockerfile = (project / "apps" / "printer" / "Dockerfile").read_text()
        assert "--mount=type=cache" in dockerfile

    def test_dockerfile_has_pinned_uv(self, run_mpm: Any) -> None:
        """Verify Dockerfile has pinned uv version (A.4 fix)."""
        exit_code, output, project = run_mpm("uv-pin-test", "--monorepo", "--with-docker", "--with-samples", "-y")

        assert exit_code == 0
        dockerfile = (project / "apps" / "printer" / "Dockerfile").read_text()
        assert "ghcr.io/astral-sh/uv:0.5.14" in dockerfile

    def test_dockerfile_no_git_install(self, run_mpm: Any) -> None:
        """Verify Dockerfile doesn't install git (A.4 fix)."""
        exit_code, output, project = run_mpm("nogit-test", "--monorepo", "--with-docker", "--with-samples", "-y")

        assert exit_code == 0
        dockerfile = (project / "apps" / "printer" / "Dockerfile").read_text()
        assert "apt-get install" not in dockerfile or "git" not in dockerfile

    def test_docker_compose_no_deprecated_version(self, run_mpm: Any) -> None:
        """Verify docker-compose.yml doesn't use deprecated version key."""
        exit_code, output, project = run_mpm("compose-ver", "--monorepo", "--with-docker", "--with-samples", "-y")

        assert exit_code == 0
        compose = (project / "docker-compose.yml").read_text()
        assert "version:" not in compose

    def test_docker_compose_has_buildkit_cache(self, run_mpm: Any) -> None:
        """Verify docker-compose.yml has BuildKit cache configuration."""
        exit_code, output, project = run_mpm("compose-cache", "--monorepo", "--with-docker", "--with-samples", "-y")

        assert exit_code == 0
        compose = (project / "docker-compose.yml").read_text()
        assert "cache_from:" in compose
        assert "cache_to:" in compose

    def test_docker_compose_has_image_tags(self, run_mpm: Any) -> None:
        """Verify docker-compose.yml has image tag definitions."""
        exit_code, output, project = run_mpm("compose-img", "--monorepo", "--with-docker", "--with-samples", "-y")

        assert exit_code == 0
        compose = (project / "docker-compose.yml").read_text()
        assert "image:" in compose
        assert "/printer:latest" in compose

    def test_docker_compose_has_dev_service(self, run_mpm: Any) -> None:
        """Verify docker-compose.yml has printer-dev development service."""
        exit_code, output, project = run_mpm("compose-dev", "--monorepo", "--with-docker", "--with-samples", "-y")

        assert exit_code == 0
        compose = (project / "docker-compose.yml").read_text()
        assert "printer-dev:" in compose
        assert "target: builder" in compose
        assert "develop:" in compose
        assert "watch:" in compose

    def test_docker_bake_has_variables(self, run_mpm: Any) -> None:
        """Verify docker-bake.hcl has TAG, REGISTRY, PYTHON_VERSION variables."""
        exit_code, output, project = run_mpm("bake-vars", "--monorepo", "--with-docker", "--with-samples", "-y")

        assert exit_code == 0
        bake = (project / "docker-bake.hcl").read_text()
        assert 'variable "TAG"' in bake
        assert 'variable "REGISTRY"' in bake
        assert 'variable "PYTHON_VERSION"' in bake

    def test_docker_bake_has_ci_target(self, run_mpm: Any) -> None:
        """Verify docker-bake.hcl has ci target with GHA cache."""
        exit_code, output, project = run_mpm("bake-ci", "--monorepo", "--with-docker", "--with-samples", "-y")

        assert exit_code == 0
        bake = (project / "docker-bake.hcl").read_text()
        assert 'target "ci"' in bake
        assert "type=gha" in bake

    def test_docker_bake_has_dev_target(self, run_mpm: Any) -> None:
        """Verify docker-bake.hcl has printer-dev target."""
        exit_code, output, project = run_mpm("bake-dev", "--monorepo", "--with-docker", "--with-samples", "-y")

        assert exit_code == 0
        bake = (project / "docker-bake.hcl").read_text()
        assert 'target "printer-dev"' in bake

    def test_release_yml_has_per_package_tags(self, run_mpm: Any) -> None:
        """Verify release.yml has per-package release tags."""
        exit_code, output, project = run_mpm(
            "rel-tags", "--monorepo", "--with-ci", "--with-pypi", "--with-samples", "-y"
        )

        assert exit_code == 0
        release = (project / ".github" / "workflows" / "release.yml").read_text()
        assert "greeter-v*.*.*" in release
        assert "printer-v*.*.*" in release

    def test_release_yml_has_workflow_dispatch(self, run_mpm: Any) -> None:
        """Verify release.yml has workflow_dispatch for manual releases."""
        exit_code, output, project = run_mpm(
            "rel-dispatch", "--monorepo", "--with-ci", "--with-pypi", "--with-samples", "-y"
        )

        assert exit_code == 0
        release = (project / ".github" / "workflows" / "release.yml").read_text()
        assert "workflow_dispatch:" in release

    def test_release_yml_has_test_pypi(self, run_mpm: Any) -> None:
        """Verify release.yml has TestPyPI support."""
        exit_code, output, project = run_mpm(
            "rel-testpypi", "--monorepo", "--with-ci", "--with-pypi", "--with-samples", "-y"
        )

        assert exit_code == 0
        release = (project / ".github" / "workflows" / "release.yml").read_text()
        assert "test-pypi:" in release
        assert "test.pypi.org" in release

    def test_release_yml_has_per_package_builds(self, run_mpm: Any) -> None:
        """Verify release.yml builds packages separately."""
        exit_code, output, project = run_mpm(
            "rel-builds", "--monorepo", "--with-ci", "--with-pypi", "--with-samples", "-y"
        )

        assert exit_code == 0
        release = (project / ".github" / "workflows" / "release.yml").read_text()
        assert "uv build --package greeter" in release
        assert "uv build --package printer" in release

    # README.md tests
    def test_readme_has_ci_badges(self, run_mpm: Any) -> None:
        """Verify README.md has CI badges when CI is enabled."""
        exit_code, output, project = run_mpm("readme-badges", "--monorepo", "--with-ci", "-y")

        assert exit_code == 0
        readme = (project / "README.md").read_text()
        assert "[![CI]" in readme
        assert "[![codecov]" in readme

    def test_readme_has_license_badge(self, run_mpm: Any) -> None:
        """Verify README.md has license badge."""
        exit_code, output, project = run_mpm("readme-lic-badge", "--monorepo", "-y")

        assert exit_code == 0
        readme = (project / "README.md").read_text()
        assert "[![License:" in readme

    def test_readme_has_prek_note(self, run_mpm: Any) -> None:
        """Verify README.md has prek note when precommit is enabled."""
        exit_code, output, project = run_mpm("readme-prek", "--monorepo", "-y")

        assert exit_code == 0
        readme = (project / "README.md").read_text()
        assert "prek" in readme
        assert "10x faster" in readme

    def test_readme_has_technology_stack(self, run_mpm: Any) -> None:
        """Verify README.md has technology stack table."""
        exit_code, output, project = run_mpm("readme-tech", "--monorepo", "-y")

        assert exit_code == 0
        readme = (project / "README.md").read_text()
        assert "Technology Stack" in readme
        assert "| Package manager |" in readme

    def test_readme_has_repository_layout(self, run_mpm: Any) -> None:
        """Verify README.md has repository layout for monorepo."""
        exit_code, output, project = run_mpm("readme-layout", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0
        readme = (project / "README.md").read_text()
        assert "Repository Layout" in readme
        assert "pyproject.toml" in readme
        assert "apps/" in readme
        assert "libs/" in readme

    def test_readme_has_commands_table(self, run_mpm: Any) -> None:
        """Verify README.md has development commands table."""
        exit_code, output, project = run_mpm("readme-cmds", "--monorepo", "-y")

        assert exit_code == 0
        readme = (project / "README.md").read_text()
        assert "Development Commands" in readme
        assert "`uv run poe fmt`" in readme
        assert "`uv run poe all`" in readme

    # Package pyproject.toml tests
    def test_package_pyproject_has_una_comment(self, run_mpm: Any) -> None:
        """Verify package pyproject.toml has una metadata hook comment."""
        exit_code, output, project = run_mpm("pkg-una-comment", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0
        greeter_pyproject = (project / "libs" / "greeter" / "pyproject.toml").read_text()
        assert "# needed for hatch-una" in greeter_pyproject

    # Sample package tests
    def test_printer_calls_greet_without_args(self, run_mpm: Any) -> None:
        """Verify printer sample calls greet() without arguments (matching reference)."""
        exit_code, output, project = run_mpm("printer-greet", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0
        printer_init = (project / "apps" / "printer" / "printer_greet" / "printer" / "__init__.py").read_text()
        assert "greeter.greet()" in printer_init
        # Should NOT have argument
        assert 'greeter.greet("' not in printer_init

    def test_greeter_has_no_module_docstring(self, run_mpm: Any) -> None:
        """Verify greeter sample has no module docstring (matching reference)."""
        exit_code, output, project = run_mpm("greeter-docstr", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0
        greeter_init = (project / "libs" / "greeter" / "greeter_docstr" / "greeter" / "__init__.py").read_text()
        # First non-empty line should be import, not docstring
        lines = [line for line in greeter_init.split("\n") if line.strip()]
        assert lines[0].startswith("import")

    def test_test_files_use_simple_format(self, run_mpm: Any) -> None:
        """Verify test files use simple format (matching reference)."""
        exit_code, output, project = run_mpm("test-format", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0
        test_file = (project / "libs" / "greeter" / "tests" / "test_greeter_import.py").read_text()
        # Should have import at top
        assert test_file.startswith("from test_format import greeter")
        # Function should be simple
        assert "def test_import():" in test_file
        # Should NOT have docstring or return type hint
        assert '"""Test' not in test_file
        assert "-> None" not in test_file


class TestDockerFileGeneration:
    """Test docker file generation logic for different project configurations."""

    def test_monorepo_with_samples_and_docker_generates_all_docker_files(self, run_mpm: Any) -> None:
        """Monorepo with samples and docker should have all docker files."""
        exit_code, output, project = run_mpm("docker-full", "--monorepo", "--with-docker", "--with-samples", "-y")

        assert exit_code == 0
        assert (project / "docker-compose.yml").exists()
        assert (project / "docker-bake.hcl").exists()
        assert (project / ".dockerignore").exists()
        assert (project / "apps" / "printer" / "Dockerfile").exists()

    def test_monorepo_without_samples_with_docker_no_compose(self, run_mpm: Any) -> None:
        """Monorepo without samples should NOT have docker-compose.yml even with --with-docker.

        This is because docker-compose.yml would reference Dockerfiles that don't exist.
        User can add apps with `mpm add app <name> --docker` later.
        """
        exit_code, output, project = run_mpm("docker-no-samples", "--monorepo", "--with-docker", "-y")

        assert exit_code == 0
        # Should have .dockerignore (useful for when user adds apps later)
        assert (project / ".dockerignore").exists()
        # Should NOT have docker-compose.yml or docker-bake.hcl (no Dockerfile to reference)
        assert not (project / "docker-compose.yml").exists()
        assert not (project / "docker-bake.hcl").exists()
        # Should NOT have root Dockerfile (that's for single package mode)
        assert not (project / "Dockerfile").exists()

    def test_single_package_with_docker_generates_all_docker_files(self, run_mpm: Any) -> None:
        """Single package with docker should have Dockerfile, compose, and bake."""
        exit_code, output, project = run_mpm("docker-single-pkg", "--single", "--with-docker", "-y")

        assert exit_code == 0
        assert (project / "Dockerfile").exists()
        assert (project / "docker-compose.yml").exists()
        assert (project / "docker-bake.hcl").exists()
        assert (project / ".dockerignore").exists()

    def test_monorepo_without_docker_no_docker_files(self, run_mpm: Any) -> None:
        """Monorepo without --with-docker should not have any docker files."""
        exit_code, output, project = run_mpm("no-docker", "--monorepo", "--with-samples", "-y")

        assert exit_code == 0
        assert not (project / ".dockerignore").exists()
        assert not (project / "docker-compose.yml").exists()
        assert not (project / "docker-bake.hcl").exists()
        assert not (project / "apps" / "printer" / "Dockerfile").exists()

    def test_single_package_docker_compose_has_correct_dockerfile_path(self, run_mpm: Any) -> None:
        """Single package docker-compose.yml should reference root Dockerfile."""
        exit_code, output, project = run_mpm("single-docker-path", "--single", "--with-docker", "-y")

        assert exit_code == 0
        compose = (project / "docker-compose.yml").read_text()
        assert "dockerfile: Dockerfile" in compose
        # Should NOT reference apps/ path
        assert "apps/" not in compose

    def test_monorepo_samples_docker_compose_has_correct_dockerfile_path(self, run_mpm: Any) -> None:
        """Monorepo with samples docker-compose.yml should reference apps/printer/Dockerfile."""
        exit_code, output, project = run_mpm("mono-docker-path", "--monorepo", "--with-docker", "--with-samples", "-y")

        assert exit_code == 0
        compose = (project / "docker-compose.yml").read_text()
        assert "apps/printer/Dockerfile" in compose

    def test_single_package_docker_bake_targets_app(self, run_mpm: Any) -> None:
        """Single package docker-bake.hcl should have 'app' target, not 'printer'."""
        exit_code, output, project = run_mpm("single-bake-target", "--single", "--with-docker", "-y")

        assert exit_code == 0
        bake = (project / "docker-bake.hcl").read_text()
        assert 'target "app"' in bake
        assert 'target "app-dev"' in bake
        # Should NOT have printer targets
        assert 'target "printer"' not in bake

    def test_monorepo_samples_docker_bake_targets_printer(self, run_mpm: Any) -> None:
        """Monorepo with samples docker-bake.hcl should have 'printer' target."""
        exit_code, output, project = run_mpm("mono-bake-target", "--monorepo", "--with-docker", "--with-samples", "-y")

        assert exit_code == 0
        bake = (project / "docker-bake.hcl").read_text()
        assert 'target "printer"' in bake
        assert 'target "printer-dev"' in bake

    def test_readme_docker_section_only_when_docker_files_exist(self, run_mpm: Any) -> None:
        """README should only have Docker section when docker files actually exist."""
        # Monorepo without samples: Docker section should NOT appear
        exit_code, _output, project = run_mpm("readme-no-docker-section", "--monorepo", "--with-docker", "-y")

        assert exit_code == 0
        readme = (project / "README.md").read_text()
        # Docker section should NOT appear because no docker-compose.yml is generated
        assert "## Docker" not in readme

    def test_readme_docker_section_with_samples(self, run_mpm: Any) -> None:
        """README should have Docker section when samples are included."""
        exit_code, _output, project = run_mpm(
            "readme-docker-section", "--monorepo", "--with-docker", "--with-samples", "-y"
        )

        assert exit_code == 0
        readme = (project / "README.md").read_text()
        # Docker section SHOULD appear
        assert "## Docker" in readme
        assert "docker buildx bake" in readme
        assert "docker compose watch printer-dev" in readme

    def test_readme_docker_section_single_package(self, run_mpm: Any) -> None:
        """README should have Docker section for single package mode."""
        exit_code, _output, project = run_mpm("readme-docker-single", "--single", "--with-docker", "-y")

        assert exit_code == 0
        readme = (project / "README.md").read_text()
        # Docker section SHOULD appear for single package
        assert "## Docker" in readme
        # But should NOT have printer-dev (that's monorepo sample specific)
        assert "printer-dev" not in readme


class TestAutoSync:
    """Test auto-sync feature that runs uv sync after project generation."""

    def test_no_sync_flag_skips_uv_sync(self, run_mpm: Any) -> None:
        """Test that --no-sync flag skips running uv sync."""
        exit_code, output, project = run_mpm("no-sync-test", "--monorepo", "--no-sync", "-y")

        assert exit_code == 0
        # Project should be created
        assert (project / "pyproject.toml").exists()
        # uv.lock should NOT exist because sync was skipped
        assert not (project / "uv.lock").exists()
        # Output should NOT mention "Dependencies installed"
        assert "Dependencies installed" not in output

    def test_auto_sync_creates_lockfile(self, run_mpm: Any) -> None:
        """Test that auto-sync (default) creates uv.lock file."""
        # Use with_sync=True to override the default --no-sync in tests
        exit_code, output, project = run_mpm("sync-test", "--monorepo", "-y", with_sync=True)

        assert exit_code == 0
        # Project should be created
        assert (project / "pyproject.toml").exists()
        # uv.lock SHOULD exist because sync was run
        assert (project / "uv.lock").exists()
        # Output should mention dependencies installed
        assert "Dependencies installed" in output

    def test_auto_sync_with_single_package(self, run_mpm: Any) -> None:
        """Test that auto-sync works for single package mode."""
        exit_code, output, project = run_mpm("sync-single-test", "--single", "-y", with_sync=True)

        assert exit_code == 0
        assert (project / "pyproject.toml").exists()
        # uv.lock should exist
        assert (project / "uv.lock").exists()
        assert "Dependencies installed" in output

    def test_no_sync_flag_in_help(self, cli_runner) -> None:
        """Test that --no-sync flag appears in help output."""
        from mpm.cli import app

        result = cli_runner.invoke(app, ["new", "--help"])
        assert result.exit_code == 0
        assert "--no-sync" in result.stdout
        assert "Skip running uv sync" in result.stdout
