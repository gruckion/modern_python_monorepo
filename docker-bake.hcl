// Docker Buildx Bake file for parallel multi-platform builds
// Run with: docker buildx bake

variable "TAG" {
  default = "latest"
}

variable "REGISTRY" {
  default = "ghcr.io/your-org"
}

// Shared settings for all targets
group "default" {
  targets = ["printer"]
}

// Production build
target "printer" {
  context    = "."
  dockerfile = "apps/printer/Dockerfile"
  tags       = ["${REGISTRY}/gpt_architecture-printer:${TAG}"]
  platforms  = ["linux/amd64", "linux/arm64"]
  cache-from = ["type=gha"]
  cache-to   = ["type=gha,mode=max"]
}

// Development build (single platform, faster)
target "printer-dev" {
  inherits = ["printer"]
  target   = "builder"
  tags     = ["gpt_architecture/printer:dev"]
  platforms = ["linux/amd64"]  // Single platform for speed
}

// CI build with all optimizations
target "ci" {
  inherits = ["printer"]
  cache-from = [
    "type=gha",
    "type=registry,ref=${REGISTRY}/gpt_architecture-printer:cache"
  ]
  cache-to = [
    "type=gha,mode=max",
    "type=registry,ref=${REGISTRY}/gpt_architecture-printer:cache,mode=max"
  ]
}
