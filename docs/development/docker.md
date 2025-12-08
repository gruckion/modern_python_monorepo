# Docker Guide

This guide covers building and running containers for the Modern Python Monorepo.

## Overview

The project includes Docker support with:

- **Multi-stage builds** for minimal production images
- **BuildKit cache mounts** for fast rebuilds
- **Docker Compose** for local development
- **Buildx Bake** for multi-platform builds

## Quick Start

### Build and Run

```bash
# Build the printer app image
docker compose build printer

# Run the container
docker compose up printer
```

### Development with Live Reload

```bash
# Start development container with file watching
docker compose watch printer-dev
```

This mounts source directories and rebuilds on changes.

## Docker Compose Services

The `docker-compose.yml` defines two services:

### `printer` (Production)

Production-ready container with minimal footprint:

```yaml
services:
  printer:
    build:
      context: .
      dockerfile: apps/printer/Dockerfile
    image: modern_python_monorepo/printer:latest
```

### `printer-dev` (Development)

Development container with live reload:

```yaml
services:
  printer-dev:
    build:
      context: .
      dockerfile: apps/printer/Dockerfile
      target: builder  # Uses builder stage (has uv)
    volumes:
      - ./libs/greeter/modern_python_monorepo:/app/libs/greeter/modern_python_monorepo:ro
      - ./apps/printer/modern_python_monorepo:/app/apps/printer/modern_python_monorepo:ro
    develop:
      watch:
        - action: sync
          path: ./libs/greeter/modern_python_monorepo
          target: /app/libs/greeter/modern_python_monorepo
```

## Dockerfile Structure

The Dockerfile uses a multi-stage build pattern:

### Stage 1: Builder

```dockerfile
FROM python:3.13-slim-bookworm AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.14 /uv /uvx /bin/

# Configure for container builds
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

# Install dependencies (cached layer)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-workspace --no-dev

# Copy source and install workspace packages
COPY libs/ apps/ ./
RUN uv sync --frozen --no-dev --no-editable
```

### Stage 2: Runtime

```dockerfile
FROM python:3.13-slim-bookworm AS runtime

# Copy only the virtual environment
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Run as non-root user
RUN useradd --create-home app
USER app

CMD ["python", "-c", "from modern_python_monorepo.printer import run; run()"]
```

## Multi-Platform Builds with Bake

For building images for multiple architectures (amd64 + arm64):

### Build for All Platforms

```bash
docker buildx bake
```

### Build Specific Target

```bash
# Development build (single platform, faster)
docker buildx bake printer-dev

# CI build with caching
docker buildx bake ci
```

### Bake Configuration

The `docker-bake.hcl` file defines build targets:

```hcl
variable "TAG" {
  default = "latest"
}

variable "REGISTRY" {
  default = "ghcr.io/your-org"
}

target "printer" {
  context    = "."
  dockerfile = "apps/printer/Dockerfile"
  tags       = ["${REGISTRY}/modern_python_monorepo-printer:${TAG}"]
  platforms  = ["linux/amd64", "linux/arm64"]
  cache-from = ["type=gha"]
  cache-to   = ["type=gha,mode=max"]
}
```

## Build Optimizations

### Layer Caching

The Dockerfile is structured for optimal layer caching:

1. **Dependencies first**: `pyproject.toml` and `uv.lock` are copied before source code
2. **Source code last**: Changes to source only rebuild the final layer
3. **Cache mounts**: uv's download cache is preserved across builds

### Image Size

The multi-stage build produces minimal images:

- Builder stage: ~500MB (includes uv, build tools)
- Runtime stage: ~150MB (only Python + dependencies)

### BuildKit Features

Enable BuildKit for best performance:

```bash
export DOCKER_BUILDKIT=1
```

Or in `docker-compose.yml`:

```yaml
services:
  printer:
    build:
      cache_from:
        - type=local,src=/tmp/.buildx-cache
      cache_to:
        - type=local,dest=/tmp/.buildx-cache-new,mode=max
```

## Common Commands

| Command | Description |
|---------|-------------|
| `docker compose build` | Build all services |
| `docker compose up` | Start all services |
| `docker compose up -d` | Start in detached mode |
| `docker compose down` | Stop and remove containers |
| `docker compose logs -f` | Follow container logs |
| `docker compose watch` | Start with file watching |
| `docker buildx bake` | Multi-platform build |

## Troubleshooting

### Build Fails with Cache Error

Clear the build cache:

```bash
docker builder prune
docker compose build --no-cache
```

### Image Not Found

Ensure you've built the image first:

```bash
docker compose build printer
```

### Permission Denied

The container runs as non-root user `app`. If you need root access for debugging:

```bash
docker compose run --user root printer /bin/bash
```
