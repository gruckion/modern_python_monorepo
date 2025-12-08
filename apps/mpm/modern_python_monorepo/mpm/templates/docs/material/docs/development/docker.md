# Docker

## Building Images

### Single Image

```bash
docker build -f apps/<app>/Dockerfile -t <app>:latest .
```

### All Images

```bash
docker buildx bake
```

## Running Containers

### With Docker Compose

```bash
docker compose up -d
```

### Standalone

```bash
docker run --rm <app>:latest
```

## Multi-Platform Builds

Build for both AMD64 and ARM64:

```bash
docker buildx bake --set *.platform=linux/amd64,linux/arm64
```

## Build Caching

GitHub Actions cache:

```bash
docker buildx bake --set *.cache-from=type=gha --set *.cache-to=type=gha,mode=max
```
