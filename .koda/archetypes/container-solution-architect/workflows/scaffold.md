---
description: Generate complete containerized solution with Containerfile, scripts, and compose
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

**SUCCESS CRITERIA**:
- Search for directory: "00-core-orchestration"
- Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory

**HALT IF**:
- Directory "00-core-orchestration" is not found
- `${ARCHETYPES_BASEDIR}` is not set

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Constitution Validation

Read and apply guardrails from:
`${ARCHETYPES_BASEDIR}/container-solution-architect/container-solution-architect-constitution.md`

Verify no hard-stop rule violations in user requirements.

### 2. Gather Container Requirements

**PROMPT THE USER FOR ALL OF THE FOLLOWING before starting scaffold:**

#### 2.1 Project Basics
- **Project Name**: Container/image identifier
- **Description**: What the container does
- **Base Runtime**: Node.js | Python | Java | Go | Multi-language

#### 2.2 Container Architecture
- **Single or Multi-Service**: One process or multiple?
- **Process Supervisor**: supervisord | s6-overlay | none
- **Services List**: If multi-service, list each service and its port

#### 2.3 Credential Requirements
- **Secrets Needed**: List secrets to compile at build time (e.g., GITHUB_PAT, AUTH_KEY)
- **Secret Owner UID**: Which UID owns compiled credentials? (default: 1001)

#### 2.4 Resource Requirements
- **Memory Limit**: e.g., 2GB
- **CPU Limit**: e.g., 1.0 cores
- **Scratch Storage**: overlay FS recommended

#### 2.5 Network & Health
- **Exposed Ports**: List ports (e.g., 3000, 8000)
- **Health Endpoint**: Path for health check (default: /health)

#### 2.6 Base Image Strategy
- **Corporate Proxy**: Behind TLS MITM proxy?
- **Registry Mirror**: e.g., artifact.it.att.com/docker-proxy/
- **Base Image**: e.g., node:22-bookworm-slim

#### 2.7 Multi-User Support
- **Multi-User**: Per-user credential overlays? (base + overlay pattern)

**⛔ STOP: Do not proceed until all requirements gathered.**

---

### 3. Generate Project Structure

Create directory structure based on constitution Section II patterns:

```
{project-name}/
├── container/
│   ├── Containerfile              # Multi-stage build
│   ├── Containerfile.user         # Per-user overlay (if multi-user)
│   └── supervisord.conf           # Process supervision (if multi-service)
├── scripts/
│   ├── compile-credentials.sh     # Credential compilation
│   ├── dev-start.sh               # Dev startup
│   └── dev-stop.sh                # Dev shutdown
├── deploy/dev/
│   └── compose.yml                # Development compose
├── .env.example
└── README.md
```

### 4. Generate Containerfile

Follow constitution Section 2.1 (Multi-Stage Dockerfile):

**Key requirements:**
- Use corporate registry prefix for base image
- Handle CORPORATE_CA_CERT build arg for proxy environments
- Create non-root user (UID 1001)
- Multi-stage: builder stage with dev deps, production stage minimal
- Include HEALTHCHECK instruction
- Copy compile-credentials.sh and run at build time

**Template structure:**
1. Builder stage FROM {registry}/{base-image} AS builder
2. Handle corporate CA cert if provided
3. Install build dependencies
4. Copy and build application
5. Production stage FROM {registry}/{base-image}
6. Create non-root user/group (1001)
7. Copy built artifacts with correct ownership
8. Copy and chmod compile-credentials.sh
9. If multi-service: install supervisor, copy supervisord.conf
10. HEALTHCHECK instruction
11. EXPOSE ports
12. USER and CMD instructions

### 5. Generate Credential Compilation Script

Follow constitution Section 2.2 pattern:

**Key requirements:**
- Read secrets from build args (AUTH_KEY, GITHUB_PAT, etc.)
- Write JSON config to /opt/app/config/credentials.compiled
- Hash sensitive values (auth_key_hash using sha256)
- chmod 440, chown to service UID
- Echo confirmation message

### 6. Generate Per-User Overlay (If Multi-User)

Follow constitution Section 2.4 (Base + Overlay Architecture):

**Key requirements:**
- ARG BASE_IMAGE={project}:base
- FROM ${BASE_IMAGE}
- ARG for each credential
- RUN compile-credentials.sh
- Unset sensitive ENV after compilation

### 7. Generate Supervisord Config (If Multi-Service)

Follow constitution Section 2.3 pattern:

**Key requirements:**
- nodaemon=true
- Each service as [program:name] section
- user=1001 for each program
- stdout/stderr to /dev/stdout, /dev/stderr
- autostart=true, autorestart=true

### 8. Generate Dev Scripts

Follow BluePearl dev-start.sh pattern from constitution:

**dev-start.sh requirements:**
- Phase 1: Build ALL images before starting containers (avoids OOM)
- Phase 2: Start compose services
- Health check loop with timeout
- Handle --skip-build flag
- Handle CORPORATE_CA_CERT

**dev-stop.sh requirements:**
- Stop containers by label filter
- Run compose down

### 9. Generate Compose File

**Requirements:**
- Service with resource limits (memory, cpus)
- Labels for container identification
- Health check
- Network definition
- Optional: postgres if database needed

### 10. Generate Documentation

**README.md requirements:**
- Quick start instructions
- Container layout diagram
- Build process explanation
- Resource limits table
- Health check info
- Troubleshooting section

**.env.example requirements:**
- All credential variables (empty)
- Corporate proxy variables
- DEV_USERS variable

---

## Post-Scaffold Checklist

```
✅ Containerfile with multi-stage build
✅ Credential compilation script (chmod 440)
✅ Process supervision (if multi-service)
✅ Dev scripts (start/stop)
✅ Compose with resource limits
✅ Environment template
✅ Documentation

🔧 Next Steps:
1. cp .env.example .env
2. Fill in credentials
3. bash scripts/dev-start.sh
4. Verify: curl http://localhost:{port}/health
```

---

## Examples

### Example 1: Single Service API
```
/scaffold-container-solution-architect "
Node.js API service
Name: order-api, Port: 3000
Secrets: DATABASE_URL, API_KEY
"
```

### Example 2: Multi-Service Workspace
```
/scaffold-container-solution-architect "
Workspace with gateway, mcp-server, python-sidecar
Name: dev-workspace
Ports: 3000, 3100, 3002
Secrets: GITHUB_PAT, LITELLM_API_KEY, AUTH_KEY
Multi-user overlay pattern
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/container-solution-architect/container-solution-architect-constitution.md`
- **Related**: debug-container-solution-architect, test-container-solution-architect
