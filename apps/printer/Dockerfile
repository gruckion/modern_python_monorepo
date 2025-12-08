# syntax=docker/dockerfile:1.7
# Multi-stage build with BuildKit cache mounts for efficient builds
# Reference: https://docs.astral.sh/uv/guides/integration/docker/

# Python version - must match .python-version (sync manually or via CI)
ARG PYTHON_VERSION=3.13

# =============================================================================
# Stage 1: Builder
# =============================================================================
FROM python:${PYTHON_VERSION}-slim-bookworm AS builder

# Pin uv version for reproducibility
COPY --from=ghcr.io/astral-sh/uv:0.5.14 /uv /uvx /bin/

# Configure uv for container builds
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Copy workspace dependency files first (changes less frequently)
COPY pyproject.toml uv.lock ./
COPY libs/greeter/pyproject.toml libs/greeter/pyproject.toml
COPY apps/printer/pyproject.toml apps/printer/pyproject.toml

# Install dependencies only (cached layer)
# --mount=type=cache reuses uv's download cache across builds
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-workspace --no-dev

# Copy source code (changes more frequently)
COPY libs/greeter/modern_python_monorepo libs/greeter/modern_python_monorepo
COPY apps/printer/modern_python_monorepo apps/printer/modern_python_monorepo

# Install workspace packages (non-editable for production)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable

# =============================================================================
# Stage 2: Runtime (minimal image)
# =============================================================================
FROM python:${PYTHON_VERSION}-slim-bookworm AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Copy only the virtual environment from builder (no uv, no source needed)
COPY --from=builder /app/.venv /app/.venv

# Add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Run as non-root user for security
RUN useradd --create-home --shell /bin/bash app
USER app

# Health check verifies Python environment is functional
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from modern_python_monorepo.printer import run" || exit 1

# Run the printer app
CMD ["python", "-c", "from modern_python_monorepo.printer import run; run()"]
