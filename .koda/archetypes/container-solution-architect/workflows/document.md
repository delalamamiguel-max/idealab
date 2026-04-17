---
description: Generate comprehensive documentation for container architecture and operations
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read documentation standards from:
`${ARCHETYPES_BASEDIR}/container-solution-architect/container-solution-architect-constitution.md`

### 2. Identify Documentation Scope

Based on $ARGUMENTS, determine documentation type:

| Type | Purpose | Audience |
|------|---------|----------|
| **Architecture** | Container layout, services, dependencies | Architects, Developers |
| **Operations** | Build, deploy, troubleshoot procedures | DevOps, SRE |
| **Security** | Credential handling, permissions, hardening | Security, Compliance |
| **Developer** | Local setup, development workflow | Developers |
| **Runbook** | Incident response, debugging | On-call engineers |

### 3. Gather Container Information

Analyze existing container artifacts:

```bash
# Containerfile analysis
grep -E "^FROM|^ARG|^ENV|^USER|^EXPOSE|^HEALTHCHECK|^CMD" container/Containerfile

# Compose analysis
cat deploy/dev/compose.yml | grep -E "image:|ports:|memory:|cpus:|healthcheck:"

# Script analysis
head -20 scripts/dev-start.sh scripts/dev-stop.sh
```

### 4. Generate Architecture Documentation

Create `docs/architecture.md`:

```markdown
# {Project Name} Container Architecture

## Overview

{Brief description of the containerized solution}

## Container Layout

{ASCII diagram of container structure}

## Services

| Service | Port | User | Purpose |
|---------|------|------|---------|
| {service} | {port} | UID {uid} | {purpose} |

## Dependencies

- **Base Image**: {base-image}
- **Runtime**: {runtime}
- **Process Supervisor**: {supervisor}

## Resource Requirements

| Resource | Limit | Request |
|----------|-------|---------|
| Memory | {mem-limit} | {mem-request} |
| CPU | {cpu-limit} | {cpu-request} |

## Network

- **Exposed Ports**: {ports}
- **Network Mode**: {network}
- **Health Endpoint**: {health-path}

## Build Process

1. Builder stage compiles code and dependencies
2. Production stage copies minimal artifacts
3. Credentials compiled at build time (never in ENV)
4. Health check configured

## Credential Flow

{Diagram showing credential compilation flow}
```

### 5. Generate Operations Documentation

Create `docs/operations.md`:

```markdown
# {Project Name} Operations Guide

## Prerequisites

- Podman or Docker installed
- Access to container registry
- Environment variables configured

## Build

### Base Image

{Build command for base image}

### Per-User Overlay (if applicable)

{Build command for user overlay}

## Deploy

### Development

{dev-start.sh usage}

### Production

{Production deployment steps}

## Health Monitoring

### Health Check Endpoint

- **URL**: http://localhost:{port}/health
- **Expected Response**: HTTP 200
- **Timeout**: 3 seconds

### Monitoring Commands

{Commands to check container health}

## Logs

### View Logs

{Commands to view container logs}

### Log Locations

| Service | Location |
|---------|----------|
| {service} | {log-path} |

## Lifecycle Operations

### Start

{Start command}

### Stop

{Stop command}

### Restart

{Restart command}

### Rebuild

{Rebuild steps}

## Troubleshooting

### Common Issues

{Table of common issues and solutions}
```

### 6. Generate Security Documentation

Create `docs/security.md`:

```markdown
# {Project Name} Security Model

## Credential Handling

### Build-Time Compilation

Credentials are compiled at image build time using `compile-credentials.sh`.
They are NEVER stored in:
- Environment variables at runtime
- Git repositories
- Container logs

### Credential File

- **Location**: /opt/app/config/credentials.compiled
- **Permissions**: 440
- **Owner**: UID {service-uid}

### Secrets Required

| Secret | Purpose | Rotation |
|--------|---------|----------|
| {secret} | {purpose} | {rotation-policy} |

## Privilege Separation

### Users

| UID | Purpose |
|-----|---------|
| 1001 | Application services |
| 1000 | User executor (if applicable) |

### Capabilities

All capabilities dropped by default.

## Container Hardening

- [x] Non-root user
- [x] Read-only root filesystem (if applicable)
- [x] No privileged mode
- [x] Resource limits enforced
- [x] Health checks enabled

## Compliance

### Constitution Alignment

This container follows all hard-stop rules from:
`container-solution-architect-constitution.md`
```

### 7. Generate Developer Documentation

Create `docs/developer.md`:

```markdown
# {Project Name} Developer Guide

## Quick Start

{Step-by-step setup instructions}

## Prerequisites

- {prerequisite-1}
- {prerequisite-2}

## Local Development

### Environment Setup

{Instructions to set up .env}

### Start Development Environment

{dev-start.sh usage}

### Stop Development Environment

{dev-stop.sh usage}

## Building

### Build Base Image

{Build command}

### Build with Credentials

{Build with credentials command}

## Testing

### Run Tests Inside Container

{Test commands}

### Health Check

{Health check command}

## Debugging

### View Logs

{Log viewing commands}

### Shell Access

{Shell access command}

### Debug Tools

{Available debug tools}

## Common Tasks

### Add a New Service

{Steps to add a service}

### Update Dependencies

{Steps to update dependencies}

### Rotate Credentials

{Steps to rotate credentials}
```

### 8. Generate Runbook

Create `docs/runbook.md`:

```markdown
# {Project Name} Runbook

## Incident Response

### Container Not Starting

**Symptoms**: Container exits immediately or stays in Created state

**Diagnosis**:
{Diagnostic commands}

**Resolution**:
{Resolution steps}

### Health Check Failing

**Symptoms**: Container unhealthy, service unavailable

**Diagnosis**:
{Diagnostic commands}

**Resolution**:
{Resolution steps}

### Service Crash Loop

**Symptoms**: Service keeps restarting, BACKOFF state

**Diagnosis**:
{Diagnostic commands}

**Resolution**:
{Resolution steps}

### Credential Errors

**Symptoms**: Authentication failures, 401/403 errors

**Diagnosis**:
{Diagnostic commands}

**Resolution**:
{Resolution steps}

### Out of Memory

**Symptoms**: Container killed, OOM errors

**Diagnosis**:
{Diagnostic commands}

**Resolution**:
{Resolution steps}

## Maintenance Procedures

### Rebuild Container

{Rebuild procedure}

### Rotate Credentials

{Credential rotation procedure}

### Update Base Image

{Base image update procedure}

## Escalation

| Severity | Response Time | Escalation Path |
|----------|---------------|-----------------|
| P1 | 15 min | {escalation} |
| P2 | 1 hour | {escalation} |
| P3 | 4 hours | {escalation} |
```

### 9. Generate Documentation Index

Create `docs/README.md`:

```markdown
# {Project Name} Documentation

## Contents

- [Architecture](architecture.md) - Container layout and design
- [Operations](operations.md) - Build, deploy, and manage
- [Security](security.md) - Credential handling and hardening
- [Developer](developer.md) - Local development setup
- [Runbook](runbook.md) - Incident response procedures

## Quick Links

- **Start Dev Environment**: `bash scripts/dev-start.sh`
- **Stop Dev Environment**: `bash scripts/dev-stop.sh`
- **Health Check**: `curl http://localhost:{port}/health`

## Constitution

This container follows the Container Solution Architect constitution.
See: `container-solution-architect-constitution.md`
```

---

## Post-Documentation Checklist

```
✅ Architecture documentation
✅ Operations guide
✅ Security model
✅ Developer guide
✅ Runbook
✅ Documentation index

Files created in docs/:
- README.md
- architecture.md
- operations.md
- security.md
- developer.md
- runbook.md
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/container-solution-architect/container-solution-architect-constitution.md`
- **Related**: scaffold-container-solution-architect, debug-container-solution-architect
