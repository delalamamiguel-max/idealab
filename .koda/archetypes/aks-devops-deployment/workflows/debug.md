---
description: Debug AKS microservice deployment failures, pod issues, and pipeline errors
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Pre-Debug Checklist

1. **Framework**: Identify application framework (Node.js | Python | Java | .NET)
2. **Failure Stage**: Build | Push | Deploy | Runtime
3. **Environment**: Dev | Staging | Production
4. **Error Message**: Copy exact error from logs
5. **Recent Changes**: Last commit or deployment

## Diagnostic Workflow

### Step 1: Constitution Compliance Check

Verify adherence to:
```
${ARCHETYPES_BASEDIR}/aks-devops-deployment/aks-microservice-deployment-constitution.md
```

Run guardrail check:
```bash
./scripts/check-guardrails.sh
```

### Step 2: Identify Failure Domain

#### A. Build Failures

**Symptoms**:
- Docker build fails
- Dependency installation errors
- Test failures during build

**Framework-Specific Diagnostics**:

##### Node.js:
```bash
# Check Node version
docker run --rm node:20-alpine node --version

# Test build locally
docker build --target builder -t test-build .

# Common issues:
# - npm ci failures → Delete package-lock.json, regenerate
# - Module not found → Check imports and case sensitivity
# - Memory errors → Increase Docker memory limit
```

##### Python:
```bash
# Check Python version
docker run --rm python:3.11-slim python --version

# Test build locally
docker build --target builder -t test-build .

# Common issues:
# - pip install failures → Check requirements.txt for version conflicts
# - ImportError → Verify PYTHONPATH and module structure
# - C extension build errors → Install build dependencies in Dockerfile
```

##### Java:
```bash
# Check Java version
docker run --rm eclipse-temurin:17-jre java -version

# Test build locally
docker build --target builder -t test-build .

# Common issues:
# - Maven/Gradle build failures → Check dependency conflicts
# - OutOfMemoryError → Increase JVM heap: ENV MAVEN_OPTS="-Xmx2g"
# - Test failures → Run mvn test locally first
```

##### .NET:
```bash
# Check .NET version
docker run --rm mcr.microsoft.com/dotnet/sdk:8.0 dotnet --version

# Test build locally
docker build --target builder -t test-build .

# Common issues:
# - NuGet restore failures → Clear cache, check package sources
# - MSBuild errors → Verify .csproj file validity
# - Test failures → Run dotnet test locally first
```

**Resolution Steps**:
1. Examine build logs for exact error line
2. Verify base image availability and digest
3. Check dependency version compatibility
4. Run build locally outside Docker
5. Review Dockerfile layer caching

#### B. Image Push Failures

**Symptoms**:
- Cannot push to ACR
- Authentication errors
- Image tag conflicts

**Diagnostics**:
```bash
# Check ACR login
az acr login --name your-acr

# Verify image exists locally
docker images | grep your-service

# Check image size (should meet constitution limits)
docker images --format "{{.Repository}}:{{.Tag}} {{.Size}}"

# Test manual push
docker push your-acr.azurecr.io/your-service:test
```

**Common Issues**:
- ❌ No ACR credentials → Configure service principal or managed identity
- ❌ Image too large → Review multi-stage build, remove unnecessary files
- ❌ Rate limiting → Implement retry logic with backoff
- ❌ Tag already exists → Use unique tags (commit SHA, build ID)

**Resolution Steps**:
1. Verify ACR service principal has `acrpush` role
2. Check image signing (Cosign) configuration
3. Verify network connectivity to ACR
4. Review CI/CD pipeline secrets configuration

#### C. Deployment Failures

**Symptoms**:
- Helm upgrade fails
- Pods in CrashLoopBackOff
- ImagePullBackOff errors
- Pod stuck in Pending state

**Diagnostics**:
```bash
# Check Helm release status
helm list -n <namespace>
helm status <release-name> -n <namespace>

# Check pod status
kubectl get pods -n <namespace> -l app=<service-name>

# Detailed pod description
kubectl describe pod <pod-name> -n <namespace>

# Check pod logs
kubectl logs <pod-name> -n <namespace> --previous

# Check events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
```

**Common Issues**:

##### ImagePullBackOff:
```bash
# Verify image exists
az acr repository show-tags --name your-acr --repository your-service

# Check image pull secret
kubectl get secrets -n <namespace>
kubectl describe secret <image-pull-secret> -n <namespace>

# Verify AKS-ACR integration
az aks check-acr --resource-group <rg> --name <aks-cluster> --acr <acr-name>
```

##### CrashLoopBackOff:

**Framework-Specific Checks**:

##### Node.js:
```bash
# Check container logs
kubectl logs <pod-name> -n <namespace>

# Common issues:
# - Module not found → Missing npm install in Dockerfile
# - Port already in use → Check PORT env var
# - Unhandled promise rejection → Add error handlers
# - Memory leak → Check for event listener leaks

# Debug with ephemeral container
kubectl debug <pod-name> -n <namespace> -it --image=node:20-alpine -- sh
```

##### Python:
```bash
# Check container logs
kubectl logs <pod-name> -n <namespace>

# Common issues:
# - ModuleNotFoundError → Missing dependencies in requirements.txt
# - Indentation errors → Fix in source code
# - Database connection failures → Check connection strings
# - Gunicorn/Uvicorn startup errors → Verify WSGI/ASGI app path

# Debug with ephemeral container
kubectl debug <pod-name> -n <namespace> -it --image=python:3.11-slim -- sh
```

##### Java:
```bash
# Check container logs
kubectl logs <pod-name> -n <namespace>

# Common issues:
# - ClassNotFoundException → Missing JAR in classpath
# - OutOfMemoryError → Increase memory limits in values.yaml
# - Port binding errors → Check server.port configuration
# - Spring Boot startup failures → Check application.properties

# Check JVM heap usage
kubectl exec <pod-name> -n <namespace> -- jcmd 1 VM.native_memory summary
```

##### .NET:
```bash
# Check container logs
kubectl logs <pod-name> -n <namespace>

# Common issues:
# - DLL not found → Verify dotnet publish output
# - Configuration errors → Check appsettings.json
# - Port binding errors → Verify ASPNETCORE_URLS
# - Dependency injection errors → Review Startup.cs

# Debug with ephemeral container
kubectl debug <pod-name> -n <namespace> -it --image=mcr.microsoft.com/dotnet/aspnet:8.0 -- sh
```

##### Pod Pending (Resource Issues):
```bash
# Check node resources
kubectl describe node <node-name>

# Check resource quotas
kubectl describe resourcequota -n <namespace>

# Check PVC status (if applicable)
kubectl get pvc -n <namespace>

# Common issues:
# - Insufficient CPU/memory → Scale nodes or reduce requests
# - No nodes match selector → Check nodeSelector/affinity
# - PVC not bound → Check StorageClass and PV availability
```

**Resolution Steps**:
1. Fix constitution violations (missing probes, resource limits)
2. Verify secrets and ConfigMaps are mounted correctly
3. Check environment variable configuration
4. Validate health check endpoints return 200 OK
5. Review security context settings

#### D. Runtime Issues

**Symptoms**:
- Service returning 5xx errors
- High latency
- Memory leaks
- Connection timeouts

**Diagnostics**:

```bash
# Check service endpoints
kubectl get svc -n <namespace>
kubectl describe svc <service-name> -n <namespace>

# Test service connectivity
kubectl run curl-test --image=curlimages/curl -i --rm --restart=Never \
  -- curl -v http://<service-name>.<namespace>.svc.cluster.local/health

# Check ingress
kubectl get ingress -n <namespace>
kubectl describe ingress <ingress-name> -n <namespace>

# Monitor real-time metrics
kubectl top pods -n <namespace> -l app=<service-name>

# Check HPA status
kubectl get hpa -n <namespace>
kubectl describe hpa <hpa-name> -n <namespace>
```

**Framework-Specific Performance Debugging**:

##### Node.js:
```bash
# Enable Node.js profiling
kubectl exec <pod-name> -n <namespace> -- node --prof app.js

# Check for memory leaks
kubectl exec <pod-name> -n <namespace> -- node --trace-gc app.js

# Heap snapshot
kubectl exec <pod-name> -n <namespace> -- node --inspect app.js
```

##### Python:
```bash
# Enable Python profiling
kubectl exec <pod-name> -n <namespace> -- python -m cProfile app.py

# Memory profiling
kubectl exec <pod-name> -n <namespace> -- python -m memory_profiler app.py

# Check async event loop
# Add to code: import asyncio; print(asyncio.all_tasks())
```

##### Java:
```bash
# JVM thread dump
kubectl exec <pod-name> -n <namespace> -- jstack 1

# Heap dump
kubectl exec <pod-name> -n <namespace> -- jmap -dump:live,format=b,file=/tmp/heap.hprof 1

# GC analysis
kubectl logs <pod-name> -n <namespace> | grep -E "GC|Full GC"
```

##### .NET:
```bash
# Dump process
kubectl exec <pod-name> -n <namespace> -- dotnet-dump collect -p 1

# Memory analysis
kubectl exec <pod-name> -n <namespace> -- dotnet-counters monitor -p 1

# CPU profiling
kubectl exec <pod-name> -n <namespace> -- dotnet-trace collect -p 1
```

### Step 3: Check Observability

```bash
# Prometheus metrics
curl http://<pod-ip>:8080/metrics

# Check Grafana dashboards
# Navigate to: https://grafana.example.com/d/<dashboard-id>

# Azure Monitor logs
az monitor log-analytics query \
  --workspace <workspace-id> \
  --analytics-query "ContainerLog | where ContainerName == '<service-name>' | order by TimeGenerated desc | take 100"
```

### Step 4: Verify Progressive Delivery

```bash
# Check canary/blue-green deployment
kubectl get pods -n <namespace> -L version

# Verify traffic split (if using service mesh)
kubectl describe virtualservice <service-name> -n <namespace>

# Check rollback history
helm history <release-name> -n <namespace>
```

### Step 5: Security & Compliance Debugging

```bash
# Check image signature
cosign verify --key cosign.pub <acr-name>.azurecr.io/<service-name>:<tag>

# Run vulnerability scan
trivy image <acr-name>.azurecr.io/<service-name>:<tag>

# Check pod security
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.securityContext}'

# Verify no hardcoded secrets
grep -r "password\|secret\|key" helm/*/templates/
```

### Step 6: Rollback Procedure

```bash
# Immediate rollback
helm rollback <release-name> -n <namespace>

# Rollback to specific revision
helm rollback <release-name> <revision> -n <namespace>

# Verify rollback success
kubectl rollout status deployment/<deployment-name> -n <namespace>
```

## Common Error Patterns

### Error: "OOMKilled"
**Cause**: Pod exceeded memory limit  
**Fix**: Increase memory limit in `values.yaml` or optimize application

### Error: "ContainerCannotRun"
**Cause**: Entrypoint/CMD incorrect or binary missing  
**Fix**: Verify Dockerfile CMD/ENTRYPOINT and test locally

### Error: "context deadline exceeded"
**Cause**: Health probe failing or slow startup  
**Fix**: Increase `initialDelaySeconds` in probe configuration

### Error: "secret not found"
**Cause**: Key Vault secret missing or RBAC issue  
**Fix**: Verify secret exists and pod identity has access

### Error: "Failed to pull image: unauthorized"
**Cause**: ACR authentication failed  
**Fix**: Attach ACR to AKS: `az aks update -n <aks> -g <rg> --attach-acr <acr>`

## Post-Debug Actions

1. **Document Root Cause**: Update incident post-mortem
2. **Create Regression Test**: Prevent same failure
3. **Update Monitoring**: Add alert for similar issues
4. **Review Runbook**: Enhance debug documentation
5. **Check Constitution**: Report any governance violations

## Constitution Violation Recovery

If debug reveals hard-stop violations:
```
❌ Missing resource limits → Add to deployment.yaml
❌ No health probes → Add liveness/readiness probes
❌ Unsigned image → Implement Cosign signing
❌ Hardcoded secrets → Migrate to Key Vault
❌ No rollback tested → Test helm rollback procedure
```

## Escalation Path

If issue persists after diagnostics:
1. Check Azure status: https://status.azure.com
2. Review AKS known issues: https://github.com/Azure/AKS/issues
3. Contact Platform Reliability Engineering
4. File incident ticket with diagnostic bundle
5. Request emergency CAB override if production impact

## Error Handling

**No Logs Available**: Check log retention settings; recommend extending retention period.

**Cannot Access Cluster**: Verify RBAC permissions and kubeconfig configuration.

**Multiple Failure Domains**: Address infrastructure issues first, then application issues.

## Examples

### Example 1: Pod Crash Loop

```
/debug-aks-devops-deployment "
fraud-api pods in CrashLoopBackOff.
Namespace: fraud-detection, started after last deployment.
"
```

### Example 2: Network Issues

```
/debug-aks-devops-deployment "
payment-service returning 503 errors.
Ingress shows healthy but service unreachable.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/aks-devops-deployment/aks-devops-deployment-constitution.md`
- **Troubleshooting Guide**: Constitution Section VII
- **Related**: test-aks-devops-deployment, refactor-aks-devops-deployment
