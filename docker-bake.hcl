// Docker Buildx Bake file for parallel multi-platform builds
// Run with: docker buildx bake

variable "TAG" {
  default = "latest"
}

variable "REGISTRY" {
  default = "ghcr.io/your-org"
}

// Python version - must match .python-version (sync manually or via CI)
variable "PYTHON_VERSION" {
  default = "3.13"
}

// Shared settings for all targets
group "default" {
  targets = ["printer"]
}

// Production build
target "printer" {
  context    = "."
  dockerfile = "apps/printer/Dockerfile"
  tags       = ["${REGISTRY}/modern_python_monorepo-printer:${TAG}"]
  platforms  = ["linux/amd64", "linux/arm64"]
  cache-from = ["type=gha"]
  cache-to   = ["type=gha,mode=max"]
  args = {
    PYTHON_VERSION = "${PYTHON_VERSION}"
  }
}

// Development build (single platform, faster)
target "printer-dev" {
  inherits = ["printer"]
  target   = "builder"
  tags     = ["modern_python_monorepo/printer:dev"]
  platforms = ["linux/amd64"]  // Single platform for speed
}

// CI build with all optimizations
target "ci" {
  inherits = ["printer"]
  cache-from = [
    "type=gha",
    "type=registry,ref=${REGISTRY}/modern_python_monorepo-printer:cache"
  ]
  cache-to = [
    "type=gha,mode=max",
    "type=registry,ref=${REGISTRY}/modern_python_monorepo-printer:cache,mode=max"
  ]
}
