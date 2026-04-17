# Container Solution Architect Constitution

## Purpose

This constitution provides enforceable guardrails and operational excellence standards for designing, building, and managing containerized solutions using Podman/Docker. Every generated Containerfile, script, and compose configuration must uphold these principles while adapting to project-specific needs.

**Core Focus Areas**:
- Multi-stage container builds with security hardening
- Credential compilation at build time (never runtime ENV)
- Process supervision for multi-service containers
- Dev (Podman) and Prod (Kubernetes) runtime abstractions
- Resource limits, health checks, and observability

---

## I. Hard-Stop Rules (Non-Negotiable)

Violations require the AI agent to refuse, rewrite, or block the requested artifact.

### 1.1 Credential Security

- ✘ **NEVER** hard-code secrets (PATs, API keys, passwords) directly in Containerfiles
- ✘ **NEVER** pass secrets via `ENV` instructions in Containerfiles
- ✘ **NEVER** expose secrets in runtime environment variables (visible via `docker inspect`)
- ✔ **ALWAYS** use build-time `--build-arg` with `compile-credentials.sh` pattern
- ✔ **ALWAYS** store compiled credentials with restrictive permissions (chmod 440, UID-specific)
- ✔ **ALWAYS** use BuildKit secrets (`--mount=type=secret`) for build-time dependencies

**Credential Compilation Pattern**:
```bash
# Correct: Compile at build time, never in runtime ENV
podman build \
  --build-arg GITHUB_PAT=ghp_xxx \
  --build-arg AUTH_KEY=bp_tok_xxx \
  --build-arg LITELLM_API_KEY=sk-xxx \
  -t myapp:latest .

# Inside Containerfile:
ARG GITHUB_PAT
ARG AUTH_KEY
RUN ./compile-credentials.sh && \
    chmod 440 /opt/app/config/credentials.compiled && \
    chown 1001:1001 /opt/app/config/credentials.compiled
```

### 1.2 Privilege Separation

- ✘ **NEVER** run application processes as root (UID 0) without documented justification
- ✘ **NEVER** use `--privileged` flag without security review
- ✘ **NEVER** expose the Docker/Podman socket to application containers
- ✔ **ALWAYS** create dedicated non-root users (UID 1000-1001) for application processes
- ✔ **ALWAYS** use `USER` instruction to switch from root after setup
- ✔ **ALWAYS** drop all capabilities (`--cap-drop=ALL`) unless specific caps required

**User Creation Pattern**:
```dockerfile
# Create non-root user
RUN groupadd -g 1001 appgroup && \
    useradd -r -u 1001 -g appgroup appuser

# Set ownership before switching user
COPY --chown=appuser:appgroup . /app

# Switch to non-root user
USER appuser
```

### 1.3 Build Reproducibility

- ✘ **NEVER** use `latest` tag without SHA256 digest in production builds
- ✘ **NEVER** pull from public registries (docker.io, gcr.io) on corporate networks without proxy
- ✘ **NEVER** omit `--pull=never` on corporate networks with TLS MITM proxies
- ✔ **ALWAYS** pin base images with specific versions or digests
- ✔ **ALWAYS** use corporate artifact registry (e.g., `artifact.it.att.com/docker-proxy/`)
- ✔ **ALWAYS** use multi-stage builds to separate build and runtime dependencies

**Corporate Proxy Pattern**:
```dockerfile
# Use corporate registry mirror
FROM artifact.it.att.com/docker-proxy/node:22-bookworm-slim

# Handle corporate CA certificates
ARG CORPORATE_CA_CERT
RUN if [ -n "$CORPORATE_CA_CERT" ]; then \
      echo "$CORPORATE_CA_CERT" > /usr/local/share/ca-certificates/corporate.crt && \
      update-ca-certificates; \
    fi
```

### 1.4 Resource Governance

- ✘ **NEVER** deploy containers without memory limits
- ✘ **NEVER** deploy containers without CPU limits
- ✘ **NEVER** use tmpfs for scratch storage in multi-container scenarios (memory exhaustion)
- ✔ **ALWAYS** specify `--memory` and `--cpus` flags on container run
- ✔ **ALWAYS** use overlay FS for scratch storage (zero memory overhead)
- ✔ **ALWAYS** document resource requirements in compose files

**Resource Limits Pattern**:
```bash
podman run -d \
  --name myapp \
  --memory 2g \
  --cpus 1.0 \
  myapp:latest
```

### 1.5 Health & Observability

- ✘ **NEVER** deploy containers without health check endpoints
- ✘ **NEVER** omit liveness and readiness probes
- ✘ **NEVER** use simple process checks when HTTP health endpoints are available
- ✔ **ALWAYS** implement `/health` endpoint returning HTTP 200 when healthy
- ✔ **ALWAYS** include `HEALTHCHECK` instruction in Containerfiles
- ✔ **ALWAYS** log structured JSON for observability

**Health Check Pattern**:
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', r => process.exit(r.statusCode === 200 ? 0 : 1)).on('error', () => process.exit(1))"
```

---

## II. Mandatory Patterns

### 2.1 Multi-Stage Dockerfile

All production Containerfiles must use multi-stage builds:

```dockerfile
# Stage 1: Builder (includes dev dependencies)
FROM node:22-bookworm-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production (minimal runtime)
FROM node:22-bookworm-slim
RUN groupadd -g 1001 app && useradd -r -u 1001 -g app app
WORKDIR /app
COPY --from=builder --chown=app:app /app/dist ./dist
COPY --from=builder --chown=app:app /app/node_modules ./node_modules
USER app
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### 2.2 Credential Compilation Script

Every container with secrets must include a `compile-credentials.sh` script:

```bash
#!/usr/bin/env bash
# compile-credentials.sh — Compile build args into runtime config
set -euo pipefail

CONFIG_DIR="${CONFIG_DIR:-/opt/app/config}"
mkdir -p "$CONFIG_DIR"

# Read from build args (passed via --build-arg)
cat > "$CONFIG_DIR/credentials.compiled" << EOF
{
  "auth_key_hash": "$(echo -n "${AUTH_KEY:-}" | sha256sum | cut -d' ' -f1)",
  "github_pat": "${GITHUB_PAT:-}",
  "litellm_base_url": "${LITELLM_BASE_URL:-}",
  "litellm_api_key": "${LITELLM_API_KEY:-}",
  "container_id": "${CONTAINER_ID:-}",
  "compiled_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

# Secure permissions — only service user can read
chmod 440 "$CONFIG_DIR/credentials.compiled"
chown ${SERVICE_UID:-1001}:${SERVICE_GID:-1001} "$CONFIG_DIR/credentials.compiled"

echo "Credentials compiled to $CONFIG_DIR/credentials.compiled"
```

### 2.3 Process Supervision (Multi-Service Containers)

For containers running multiple services, use supervisord:

```ini
# supervisord.conf
[supervisord]
nodaemon=true
user=root
logfile=/var/log/supervisord.log
pidfile=/var/run/supervisord.pid

[program:gateway]
command=/opt/app/gateway/start.sh
user=1001
directory=/opt/app/gateway
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0

[program:sidecar]
command=/opt/app/sidecar/start.sh
user=1001
directory=/opt/app/sidecar
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
```

### 2.4 Base Image + Overlay Architecture

For multi-user scenarios, use a two-layer image strategy:

**Layer 1: Base Image (built once, heavy)**
```dockerfile
# Containerfile — builds base image with all dependencies
FROM node:22-bookworm-slim AS base

# Install system dependencies (cached layer)
RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install application dependencies
WORKDIR /opt/app
COPY package*.json ./
RUN npm ci --production

# Copy application code
COPY . .
RUN npm run build
```

**Layer 2: Per-User Credential Overlay (built per user, thin)**
```dockerfile
# Containerfile.user — thin overlay with credentials
ARG BASE_IMAGE=myapp:base
FROM ${BASE_IMAGE}

# Credential compilation args
ARG AUTH_KEY
ARG GITHUB_PAT
ARG LITELLM_BASE_URL
ARG LITELLM_API_KEY
ARG CONTAINER_ID

# Compile credentials (seconds, not minutes)
RUN ./compile-credentials.sh

CMD ["supervisord", "-c", "/etc/supervisord.conf"]
```

### 2.5 Dev Environment Scripts

Every container project should include lifecycle scripts:

**dev-start.sh**:
```bash
#!/usr/bin/env bash
# dev-start.sh — Start development environment
set -euo pipefail

# Phase 1: Build all images (no containers running = max RAM for builds)
echo "▸ Phase 1: Building images..."
podman build --pull=never -t myapp:base -f Containerfile .
podman build --pull=never \
  --build-arg BASE_IMAGE=myapp:base \
  --build-arg AUTH_KEY="${AUTH_KEY}" \
  -t myapp:dev -f Containerfile.user .

# Phase 2: Start containers
echo "▸ Phase 2: Starting containers..."
podman-compose -f compose.yml up -d

# Health check
for i in $(seq 1 20); do
  if curl -sf http://localhost:3000/health > /dev/null 2>&1; then
    echo "✅ Container healthy"
    break
  fi
  sleep 2
done
```

**dev-stop.sh**:
```bash
#!/usr/bin/env bash
# dev-stop.sh — Stop development environment
set -euo pipefail

# Stop containers by label
for cid in $(podman ps -a --filter "label=app.name=myapp" --format '{{.Names}}'); do
  podman rm -f "$cid" && echo "Stopped $cid"
done

# Stop compose services
podman-compose -f compose.yml down
```

---

## III. Container Runtime Abstraction

### 3.1 Runtime Interface

Abstract container operations behind an interface for dev/prod portability:

```typescript
interface ContainerRuntime {
  build(imageName: string, buildArgs: Record<string, string>): Promise<void>;
  create(containerName: string, image: string, options: ContainerOptions): Promise<string>;
  start(containerName: string): Promise<void>;
  stop(containerName: string): Promise<void>;
  remove(containerName: string): Promise<void>;
  inspect(containerName: string): Promise<ContainerInfo>;
  logs(containerName: string, options?: LogOptions): AsyncIterable<string>;
  healthCheck(containerName: string): Promise<HealthStatus>;
}

interface ContainerOptions {
  network?: string;
  memory?: string;      // e.g., "2g"
  cpus?: number;        // e.g., 1.0
  env?: Record<string, string>;
  labels?: Record<string, string>;
  ports?: string[];     // e.g., ["3000:3000"]
}
```

### 3.2 Podman Implementation (Dev)

```typescript
class PodmanRuntime implements ContainerRuntime {
  private socketPath: string;

  constructor(socketPath = '/run/podman/podman.sock') {
    this.socketPath = socketPath;
  }

  async build(imageName: string, buildArgs: Record<string, string>): Promise<void> {
    const args = Object.entries(buildArgs)
      .map(([k, v]) => `--build-arg ${k}=${v}`)
      .join(' ');
    await execAsync(`podman build --pull=never ${args} -t ${imageName} .`);
  }

  async create(name: string, image: string, opts: ContainerOptions): Promise<string> {
    const flags = [
      opts.memory ? `--memory ${opts.memory}` : '',
      opts.cpus ? `--cpus ${opts.cpus}` : '',
      opts.network ? `--network ${opts.network}` : '',
      ...Object.entries(opts.labels || {}).map(([k, v]) => `--label ${k}=${v}`),
      ...Object.entries(opts.env || {}).map(([k, v]) => `-e ${k}=${v}`),
    ].filter(Boolean).join(' ');
    
    const { stdout } = await execAsync(`podman create ${flags} --name ${name} ${image}`);
    return stdout.trim();
  }

  async healthCheck(name: string): Promise<HealthStatus> {
    // Use podman exec for health check (works on macOS where host can't reach VM network)
    const { exitCode } = await execAsync(
      `podman exec ${name} node -e "require('http').get('http://127.0.0.1:3000/health', r => process.exit(r.statusCode === 200 ? 0 : 1))"`
    );
    return exitCode === 0 ? 'healthy' : 'unhealthy';
  }
}
```

### 3.3 Kubernetes Implementation (Prod)

```typescript
class KubernetesRuntime implements ContainerRuntime {
  private namespace: string;
  private k8sApi: CoreV1Api;

  constructor(namespace = 'default') {
    this.namespace = namespace;
    const kc = new KubeConfig();
    kc.loadFromDefault();
    this.k8sApi = kc.makeApiClient(CoreV1Api);
  }

  async create(name: string, image: string, opts: ContainerOptions): Promise<string> {
    const pod: V1Pod = {
      metadata: { name, labels: opts.labels },
      spec: {
        containers: [{
          name: 'app',
          image,
          resources: {
            limits: {
              memory: opts.memory || '2Gi',
              cpu: String(opts.cpus || 1),
            },
          },
          livenessProbe: {
            httpGet: { path: '/health', port: 3000 },
            initialDelaySeconds: 30,
            periodSeconds: 10,
          },
        }],
      },
    };
    const { body } = await this.k8sApi.createNamespacedPod(this.namespace, pod);
    return body.metadata!.uid!;
  }
}
```

---

## IV. Compose Configuration

### 4.1 Development Compose

```yaml
# compose.yml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: devpassword
      POSTGRES_DB: app
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s
      timeout: 5s
      retries: 5

  app:
    image: myapp:dev
    depends_on:
      postgres:
        condition: service_healthy
    ports:
      - "3000:3000"
    labels:
      app.name: myapp
      app.component: main
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:3000/health', r => process.exit(r.statusCode === 200 ? 0 : 1))"]
      interval: 30s
      timeout: 3s
      retries: 3

networks:
  default:
    name: app-net

volumes:
  postgres-data:
```

---

## V. Troubleshooting Guide

### 5.1 Corporate Proxy TLS Issues

**Problem**: `x509: negative serial number` when pulling images

**Solution**: Use corporate artifact registry with pre-pulled images:
```bash
# Pull from corporate registry
podman pull artifact.it.att.com/docker-proxy/node:22-bookworm-slim

# Tag for local use
podman tag artifact.it.att.com/docker-proxy/node:22-bookworm-slim node:22-bookworm-slim

# Build with --pull=never
podman build --pull=never -t myapp:latest .
```

### 5.2 Health Check Failures on macOS

**Problem**: Host can't reach Podman VM network IPs (10.89.0.x)

**Solution**: Use `podman exec` for health checks:
```bash
# Instead of: curl http://10.89.0.5:3000/health
# Use:
podman exec myapp node -e "require('http').get('http://127.0.0.1:3000/health', r => process.exit(r.statusCode === 200 ? 0 : 1))"
```

### 5.3 OOM During Multi-Image Builds

**Problem**: Building multiple images concurrently causes memory exhaustion

**Solution**: Phase builds — build ALL images before starting ANY containers:
```bash
# Phase 1: Build all images (full RAM available)
podman build -t base:latest .
podman build -t user1:latest -f Containerfile.user .
podman build -t user2:latest -f Containerfile.user .

# Phase 2: Start containers (builds complete)
podman-compose up -d
```

### 5.4 Gateway Binding Issues

**Problem**: Services default to localhost, can't reach each other

**Solution**: Bind to 0.0.0.0 in container services:
```typescript
// Wrong: serve({ port: 3000 })
// Correct:
serve({ port: 3000, hostname: '0.0.0.0' })
```

---

## VI. Security Checklist

Before deploying any container:

- [ ] No secrets in Containerfile `ENV` instructions
- [ ] Credentials compiled at build time with restrictive permissions
- [ ] Non-root user (UID 1000-1001) runs application processes
- [ ] Base images pinned with version or digest
- [ ] Multi-stage build separates build/runtime dependencies
- [ ] Resource limits specified (memory, CPU)
- [ ] Health check endpoint implemented
- [ ] HEALTHCHECK instruction in Containerfile
- [ ] No public registry references on corporate network
- [ ] Overlay FS for scratch storage (not tmpfs)

---

## VII. Refusal Template

When a request violates hard-stop rules:

```
❌ Request violates Hard-Stop rule {rule_id}: {rule_description}

To proceed, you must:
1. {specific_remediation_step_1}
2. {specific_remediation_step_2}

Example of compliant approach:
{code_example}

See: container-solution-architect-constitution.md Section I.{subsection}
```

---

## VIII. Related Documents

- **AKS Deployment**: Use `aks-devops-deployment` archetype for Kubernetes deployment
- **CI/CD Pipelines**: Use `microservice-cicd-architect` for pipeline generation
- **Process Supervision**: supervisord documentation at http://supervisord.org/
