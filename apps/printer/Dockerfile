# syntax=docker/dockerfile:1
FROM python:3.13-slim-bookworm

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy workspace files needed for dependency resolution
COPY pyproject.toml uv.lock ./
COPY libs/greeter/pyproject.toml libs/greeter/pyproject.toml
COPY apps/printer/pyproject.toml apps/printer/pyproject.toml

# Install dependencies (without the actual source yet for better caching)
RUN uv sync --frozen --no-install-workspace

# Copy source code
COPY libs/greeter/gpt_architecture libs/greeter/gpt_architecture
COPY apps/printer/gpt_architecture apps/printer/gpt_architecture

# Install the workspace packages
RUN uv sync --frozen

# Run the printer app
CMD ["/app/.venv/bin/python", "-c", "from gpt_architecture.printer import run; run()"]
