---
description: Improve existing container setup for security, performance, or maintainability
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read refactoring guidance from:
`${ARCHETYPES_BASEDIR}/container-solution-architect/container-solution-architect-constitution.md`

### 2. Analyze Current State

Identify existing container artifacts:

```bash
# Find Containerfiles
find . -name "Containerfile*" -o -name "Dockerfile*"

# Find compose files
find . -name "compose*.yml" -o -name "docker-compose*.yml"

# Find scripts
find . -name "*.sh" -type f | head -20
```

### 3. Identify Refactoring Opportunities

#### 3.1 Security Improvements

| Issue | Detection | Refactoring |
|-------|-----------|-------------|
| Secrets in ENV | `grep -r "ENV.*KEY\|ENV.*PASSWORD\|ENV.*SECRET"` | Convert to build-arg + compile-credentials.sh |
| Running as root | No USER instruction or USER root | Add non-root user (UID 1001) |
| No resource limits | Missing deploy.resources in compose | Add memory/cpu limits |
| Public base images | `grep "^FROM " Containerfile` | Use corporate registry mirror |
| Latest tag | `grep ":latest" Containerfile` | Pin to specific version or digest |

#### 3.2 Performance Improvements

| Issue | Detection | Refactoring |
|-------|-----------|-------------|
| Single-stage build | One FROM statement only | Convert to multi-stage |
| Large image size | `podman images --format "{{.Size}}"` | Multi-stage, .dockerignore |
| No layer caching | COPY . before npm install | Reorder: copy package.json, install, copy rest |
| tmpfs for scratch | Mount type=tmpfs in compose | Convert to overlay FS |
| Sequential builds | dev-start.sh starts before build done | Phase 1 build, Phase 2 start |

#### 3.3 Maintainability Improvements

| Issue | Detection | Refactoring |
|-------|-----------|-------------|
| No health checks | Missing HEALTHCHECK instruction | Add HEALTHCHECK with /health endpoint |
| No process supervision | Multiple services, no supervisor | Add supervisord.conf |
| Missing dev scripts | No dev-start.sh/dev-stop.sh | Generate standard scripts |
| No .env.example | Credentials in code/docs | Extract to .env.example |

### 4. Apply Refactorings

#### 4.1 Convert to Multi-Stage Build

**Before**:
```dockerfile
FROM node:22-bookworm-slim
WORKDIR /app
COPY . .
RUN npm ci
RUN npm run build
CMD ["node", "dist/index.js"]
```

**After**:
```dockerfile
FROM node:22-bookworm-slim AS builder
WORKDIR /build
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-bookworm-slim
RUN groupadd -g 1001 app && useradd -r -u 1001 -g app app
WORKDIR /app
COPY --from=builder --chown=app:app /build/dist ./dist
COPY --from=builder --chown=app:app /build/node_modules ./node_modules
USER app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
```

#### 4.2 Add Credential Compilation

**Before** (secrets in ENV):
```dockerfile
ENV API_KEY=sk-xxx
ENV DATABASE_URL=postgres://...
```

**After**:
```dockerfile
ARG API_KEY
ARG DATABASE_URL
COPY scripts/compile-credentials.sh ./
RUN ./compile-credentials.sh
```

#### 4.3 Add Process Supervision

**Before** (multiple services, manual start):
```dockerfile
CMD ["sh", "-c", "node gateway.js & python sidecar.py"]
```

**After**:
```dockerfile
RUN apt-get update && apt-get install -y supervisor
COPY supervisord.conf /etc/supervisord.conf
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
```

#### 4.4 Add Phase-Based Build Script

**Before** (build and start interleaved):
```bash
podman-compose up -d
podman build -t app:latest .  # May OOM
```

**After**:
```bash
# Phase 1: Build all images
podman build -t app:base .
podman build -t app:user1 -f Containerfile.user .

# Phase 2: Start services
podman-compose up -d
```

### 5. Validate Refactoring

After refactoring, verify:

```bash
# Build succeeds
podman build -t refactored:test .

# Image size reduced
podman images refactored:test --format "{{.Size}}"

# Container starts and passes health check
podman run -d --name test refactored:test
sleep 10
podman exec test curl -f http://localhost:3000/health

# Clean up
podman rm -f test
```

### 6. Generate Refactoring Report

```
## Refactoring Report

**Files Modified**:
- {file_1}: {change_summary}
- {file_2}: {change_summary}

**Security Improvements**:
- ✅ {improvement_1}
- ✅ {improvement_2}

**Performance Improvements**:
- ✅ {improvement_1}
- ✅ {improvement_2}

**Image Size**: {before} → {after}

**Validation**:
- Build: ✅ Passed
- Health Check: ✅ Passed
- Resource Limits: ✅ Applied

**Constitution Compliance**: All hard-stop rules satisfied
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/container-solution-architect/container-solution-architect-constitution.md`
- **Related**: debug-container-solution-architect, test-container-solution-architect
