---
description: Diagnose container build failures, health check issues, and process supervision problems
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read troubleshooting guidance from:
`${ARCHETYPES_BASEDIR}/container-solution-architect/container-solution-architect-constitution.md`

Focus on Section V (Troubleshooting Guide).

### 2. Identify Problem Category

Categorize the reported issue:

| Category | Symptoms | Common Causes |
|----------|----------|---------------|
| **Build Failure** | podman build fails, image not created | Base image pull, dependency install, compile errors |
| **Health Check Failure** | Container starts but unhealthy | Service not binding, wrong port, network isolation |
| **Process Supervision** | Services crash, restart loops | Wrong user, missing deps, config errors |
| **Credential Issues** | Auth failures, 401/403 errors | Missing build args, wrong permissions, hash mismatch |
| **Resource Issues** | OOM, CPU throttling, slow builds | Memory limits, concurrent builds, tmpfs vs overlay |
| **Network Issues** | Can't reach services, DNS failures | Host/container binding, network mode, proxy |

### 3. Collect Diagnostic Information

**For Build Failures:**
```bash
# Check build logs
podman build -t {image}:debug . 2>&1 | tee build.log

# Check base image availability
podman images | grep {base-image}

# Check build args
echo "AUTH_KEY set: ${AUTH_KEY:+yes}"
echo "GITHUB_PAT set: ${GITHUB_PAT:+yes}"
```

**For Health Check Failures:**
```bash
# Check container status
podman ps -a --filter name={container}

# Check container logs
podman logs {container} --tail 100

# Check health from inside container (macOS workaround)
podman exec {container} curl -f http://127.0.0.1:{port}/health

# Check what's listening
podman exec {container} netstat -tlnp
```

**For Process Supervision:**
```bash
# Check supervisord status
podman exec {container} supervisorctl status

# Check individual service logs
podman exec {container} supervisorctl tail -f {service}

# Check supervisord config
podman exec {container} cat /etc/supervisord.conf
```

**For Credential Issues:**
```bash
# Verify credential file exists
podman exec {container} ls -la /opt/app/config/credentials.compiled

# Check permissions (should be 440, owned by service UID)
podman exec {container} stat /opt/app/config/credentials.compiled

# Verify content (without exposing secrets)
podman exec {container} cat /opt/app/config/credentials.compiled | jq 'keys'
```

### 4. Common Issues and Solutions

#### 4.1 Corporate Proxy TLS Issues

**Symptom**: `x509: negative serial number` when pulling images

**Diagnosis**:
```bash
# Check if proxy is intercepting
curl -v https://registry-1.docker.io 2>&1 | grep -i "issuer"
```

**Solution**:
- Use corporate artifact registry mirror
- Pre-pull images with `podman pull artifact.it.att.com/docker-proxy/{image}`
- Tag for local use: `podman tag artifact.it.att.com/... {image}`
- Build with `--pull=never`

#### 4.2 Health Check Failures on macOS

**Symptom**: curl from host can't reach container IP (10.89.0.x)

**Diagnosis**:
```bash
# This will fail on macOS
curl http://$(podman inspect {container} --format '{{.NetworkSettings.IPAddress}}'):3000/health
```

**Solution**: Use podman exec for health checks:
```bash
podman exec {container} node -e "require('http').get('http://127.0.0.1:3000/health', r => process.exit(r.statusCode === 200 ? 0 : 1))"
```

#### 4.3 OOM During Multi-Image Builds

**Symptom**: Build killed, "out of memory" errors

**Diagnosis**:
```bash
# Check Podman VM memory
podman machine inspect | jq '.Resources.Memory'

# Check if containers running during build
podman ps
```

**Solution**: Phase builds - build ALL images before starting ANY containers:
```bash
# Stop all containers
podman stop $(podman ps -q)

# Build images with full RAM
podman build -t base:latest .
podman build -t user1:latest -f Containerfile.user .

# Then start containers
podman-compose up -d
```

#### 4.4 Service Not Binding to 0.0.0.0

**Symptom**: Services can't reach each other, only localhost works

**Diagnosis**:
```bash
podman exec {container} netstat -tlnp | grep {port}
# Shows 127.0.0.1:{port} instead of 0.0.0.0:{port}
```

**Solution**: Configure service to bind to all interfaces:
```typescript
// Node.js with Hono
serve({ port: 3000, hostname: '0.0.0.0' })

// Python with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### 4.5 Credential Permission Errors

**Symptom**: Service can't read credentials.compiled

**Diagnosis**:
```bash
podman exec {container} ls -la /opt/app/config/
podman exec {container} id  # Check running user
```

**Solution**: Ensure compile-credentials.sh sets correct ownership:
```bash
chmod 440 "$CONFIG_DIR/credentials.compiled"
chown ${SERVICE_UID}:${SERVICE_GID} "$CONFIG_DIR/credentials.compiled"
```

#### 4.6 Supervisor Service Restart Loops

**Symptom**: Service keeps restarting, BACKOFF state

**Diagnosis**:
```bash
podman exec {container} supervisorctl status
podman exec {container} supervisorctl tail {service} stderr
```

**Solution**: Check service startup requirements:
- Dependencies available?
- Config files present?
- User has permission to execute?
- Environment variables set?

### 5. Generate Debug Report

After diagnosis, provide:

```
## Debug Report

**Issue Category**: {category}
**Root Cause**: {root_cause}

**Diagnostic Commands Run**:
- {command_1}: {result_1}
- {command_2}: {result_2}

**Solution**:
{step_by_step_solution}

**Prevention**:
{how_to_prevent_recurrence}

**Constitution Reference**: Section {section}
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/container-solution-architect/container-solution-architect-constitution.md` Section V
- **Related**: scaffold-container-solution-architect, refactor-container-solution-architect
