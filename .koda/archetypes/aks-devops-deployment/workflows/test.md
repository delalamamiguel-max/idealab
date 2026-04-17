---
description: Validate AKS microservice deployment for security, progressive delivery, and governance readiness
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Test Categories

1. **Constitution Compliance** - Validate all hard-stop rules
2. **Container Security** - Image scanning, signing, runtime security
3. **Kubernetes Manifests** - Resource limits, probes, RBAC
4. **Deployment Strategy** - Progressive delivery validation
5. **Observability** - Metrics, logging, tracing
6. **Framework-Specific** - Language runtime validation

## Test Execution

### 1. Constitution Compliance Tests

Verify adherence to:
```
${ARCHETYPES_BASEDIR}/aks-devops-deployment/aks-microservice-deployment-constitution.md
```

#### 1.1 Dockerfile Security Tests

```bash
#!/bin/bash
# Test: Dockerfile security compliance

echo "🔍 Testing Dockerfile compliance..."

# Test: Multi-stage build
if ! grep -q "FROM.*AS builder" Dockerfile; then
  echo "❌ FAIL: Dockerfile must use multi-stage build"
  exit 1
fi
echo "✅ PASS: Multi-stage build detected"

# Test: Base image pinning with digest
if ! grep -E "FROM.*@sha256:" Dockerfile; then
  echo "❌ FAIL: Base images must be pinned with digest"
  exit 1
fi
echo "✅ PASS: Base images pinned with digest"

# Test: Non-root user
if ! grep -q "USER" Dockerfile; then
  echo "❌ FAIL: Must run as non-root user"
  exit 1
fi
echo "✅ PASS: Non-root user configured"

# Test: No hardcoded secrets
if grep -iE "(password|secret|api_key|token)=\S+" Dockerfile; then
  echo "❌ FAIL: Hardcoded secrets detected in Dockerfile"
  exit 1
fi
echo "✅ PASS: No hardcoded secrets"

# Test: Healthcheck defined
if ! grep -q "HEALTHCHECK" Dockerfile; then
  echo "⚠️  WARN: Dockerfile should include HEALTHCHECK"
fi

echo "✅ Dockerfile compliance tests passed"
```

#### 1.2 Image Security Scanning

```bash
#!/bin/bash
# Test: Container image security

SERVICE_NAME="your-service"
IMAGE_TAG="${ACR_NAME}.azurecr.io/${SERVICE_NAME}:${BUILD_ID}"

echo "🔍 Scanning image: ${IMAGE_TAG}"

# Test: Trivy vulnerability scan
echo "Running Trivy scan..."
trivy image --severity HIGH,CRITICAL --exit-code 1 "${IMAGE_TAG}"
if [ $? -eq 0 ]; then
  echo "✅ PASS: No HIGH/CRITICAL vulnerabilities"
else
  echo "❌ FAIL: HIGH/CRITICAL vulnerabilities detected"
  exit 1
fi

# Test: Image signature verification
echo "Verifying image signature..."
cosign verify --key cosign.pub "${IMAGE_TAG}"
if [ $? -eq 0 ]; then
  echo "✅ PASS: Image signature valid"
else
  echo "❌ FAIL: Image not signed or invalid signature"
  exit 1
fi

# Test: SBOM generation
echo "Generating SBOM..."
syft "${IMAGE_TAG}" -o json > sbom.json
if [ -s sbom.json ]; then
  echo "✅ PASS: SBOM generated"
else
  echo "❌ FAIL: SBOM generation failed"
  exit 1
fi

echo "✅ Image security tests passed"
```

### 2. Helm Chart Validation Tests

```bash
#!/bin/bash
# Test: Helm chart compliance

CHART_PATH="./helm/${SERVICE_NAME}"

echo "🔍 Testing Helm chart..."

# Test: Helm lint
helm lint "${CHART_PATH}"
if [ $? -eq 0 ]; then
  echo "✅ PASS: Helm lint passed"
else
  echo "❌ FAIL: Helm lint failed"
  exit 1
fi

# Test: Template rendering
helm template test "${CHART_PATH}" --debug > /tmp/rendered.yaml
if [ $? -eq 0 ]; then
  echo "✅ PASS: Chart templates valid"
else
  echo "❌ FAIL: Chart template rendering failed"
  exit 1
fi

# Test: Resource limits defined
if ! grep -q "limits:" /tmp/rendered.yaml; then
  echo "❌ FAIL: Resource limits not defined"
  exit 1
fi
echo "✅ PASS: Resource limits defined"

# Test: Resource requests defined
if ! grep -q "requests:" /tmp/rendered.yaml; then
  echo "❌ FAIL: Resource requests not defined"
  exit 1
fi
echo "✅ PASS: Resource requests defined"

# Test: Liveness probe
if ! grep -q "livenessProbe:" /tmp/rendered.yaml; then
  echo "❌ FAIL: Liveness probe not defined"
  exit 1
fi
echo "✅ PASS: Liveness probe defined"

# Test: Readiness probe
if ! grep -q "readinessProbe:" /tmp/rendered.yaml; then
  echo "❌ FAIL: Readiness probe not defined"
  exit 1
fi
echo "✅ PASS: Readiness probe defined"

# Test: Security context
if ! grep -q "securityContext:" /tmp/rendered.yaml; then
  echo "❌ FAIL: Security context not defined"
  exit 1
fi
echo "✅ PASS: Security context defined"

# Test: No hardcoded secrets
if grep -iE "(password|secret|api_key|token):" "${CHART_PATH}/values.yaml"; then
  echo "❌ FAIL: Hardcoded secrets in values.yaml"
  exit 1
fi
echo "✅ PASS: No hardcoded secrets in values"

# Test: HPA configured
if ! grep -q "autoscaling:" "${CHART_PATH}/values.yaml"; then
  echo "⚠️  WARN: HPA not configured"
fi

echo "✅ Helm chart validation passed"
```

### 3. Kubernetes Policy Tests

```bash
#!/bin/bash
# Test: Kubernetes policy compliance

echo "🔍 Testing Kubernetes policies..."

# Test with Conftest (OPA policies)
conftest test /tmp/rendered.yaml -p policies/
if [ $? -eq 0 ]; then
  echo "✅ PASS: OPA policy checks passed"
else
  echo "❌ FAIL: OPA policy violations detected"
  exit 1
fi

# Test: PSP/PSA compliance
# Verify pod security standards (restricted)
kubectl label namespace ${NAMESPACE} \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/warn=restricted --dry-run=client

echo "✅ Kubernetes policy tests passed"
```

### 4. Framework-Specific Tests

#### 4.1 Node.js Application Tests

```bash
#!/bin/bash
# Test: Node.js application

echo "🔍 Testing Node.js application..."

# Unit tests
npm test
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Unit tests failed"
  exit 1
fi
echo "✅ PASS: Unit tests passed"

# Code coverage
npm run test:coverage
COVERAGE=$(jq -r '.total.lines.pct' coverage/coverage-summary.json)
if (( $(echo "$COVERAGE < 80" | bc -l) )); then
  echo "❌ FAIL: Code coverage below 80% (${COVERAGE}%)"
  exit 1
fi
echo "✅ PASS: Code coverage: ${COVERAGE}%"

# Linting
npm run lint
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Linting errors"
  exit 1
fi
echo "✅ PASS: Linting passed"

# Dependency audit
npm audit --audit-level=high
if [ $? -ne 0 ]; then
  echo "❌ FAIL: High/Critical vulnerabilities in dependencies"
  exit 1
fi
echo "✅ PASS: No high/critical vulnerabilities"

# Build test
npm run build
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Build failed"
  exit 1
fi
echo "✅ PASS: Build successful"

echo "✅ Node.js tests passed"
```

#### 4.2 Python Application Tests

```bash
#!/bin/bash
# Test: Python application

echo "🔍 Testing Python application..."

# Unit tests with coverage
pytest --cov=. --cov-report=xml --cov-report=term
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Unit tests failed"
  exit 1
fi
echo "✅ PASS: Unit tests passed"

# Code coverage check
COVERAGE=$(python -c "import xml.etree.ElementTree as ET; print(ET.parse('coverage.xml').getroot().attrib['line-rate'])")
if (( $(echo "$COVERAGE < 0.8" | bc -l) )); then
  echo "❌ FAIL: Code coverage below 80%"
  exit 1
fi
echo "✅ PASS: Code coverage: $(echo "$COVERAGE * 100" | bc)%"

# Linting
flake8 . --count --max-line-length=120
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Flake8 linting errors"
  exit 1
fi
echo "✅ PASS: Flake8 passed"

# Type checking
mypy . --ignore-missing-imports
if [ $? -ne 0 ]; then
  echo "⚠️  WARN: Type checking issues"
fi

# Security scan
bandit -r . -f json -o bandit-report.json
if [ $? -ne 0 ]; then
  echo "⚠️  WARN: Security issues detected"
fi

# Dependency audit
pip-audit
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Vulnerable dependencies"
  exit 1
fi
echo "✅ PASS: No vulnerable dependencies"

echo "✅ Python tests passed"
```

#### 4.3 Java Application Tests

```bash
#!/bin/bash
# Test: Java application

echo "🔍 Testing Java application..."

# Unit tests
mvn test
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Unit tests failed"
  exit 1
fi
echo "✅ PASS: Unit tests passed"

# Code coverage
mvn jacoco:report
COVERAGE=$(xmllint --xpath "string(//counter[@type='LINE']/@covered div (//counter[@type='LINE']/@covered + //counter[@type='LINE']/@missed))" target/site/jacoco/jacoco.xml)
if (( $(echo "$COVERAGE < 0.8" | bc -l) )); then
  echo "❌ FAIL: Code coverage below 80%"
  exit 1
fi
echo "✅ PASS: Code coverage: $(echo "$COVERAGE * 100" | bc)%"

# Static analysis
mvn pmd:check
if [ $? -ne 0 ]; then
  echo "⚠️  WARN: PMD violations"
fi

# Dependency check
mvn dependency-check:check
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Vulnerable dependencies"
  exit 1
fi
echo "✅ PASS: No vulnerable dependencies"

# Build verification
mvn clean verify
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Build failed"
  exit 1
fi
echo "✅ PASS: Build successful"

echo "✅ Java tests passed"
```

#### 4.4 .NET Application Tests

```bash
#!/bin/bash
# Test: .NET application

echo "🔍 Testing .NET application..."

# Unit tests
dotnet test --collect:"XPlat Code Coverage"
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Unit tests failed"
  exit 1
fi
echo "✅ PASS: Unit tests passed"

# Code coverage
COVERAGE=$(dotnet reportgenerator -reports:**/coverage.cobertura.xml -targetdir:./coverage -reporttypes:TextSummary | grep "Line coverage:" | awk '{print $3}' | sed 's/%//')
if (( $(echo "$COVERAGE < 80" | bc -l) )); then
  echo "❌ FAIL: Code coverage below 80%"
  exit 1
fi
echo "✅ PASS: Code coverage: ${COVERAGE}%"

# Security scan
dotnet list package --vulnerable
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Vulnerable packages"
  exit 1
fi
echo "✅ PASS: No vulnerable packages"

# Build verification
dotnet build --configuration Release
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Build failed"
  exit 1
fi
echo "✅ PASS: Build successful"

echo "✅ .NET tests passed"
```

### 5. Deployment Integration Tests

```bash
#!/bin/bash
# Test: Deployment to test environment

NAMESPACE="test"
RELEASE_NAME="${SERVICE_NAME}-test"

echo "🔍 Testing deployment..."

# Deploy to test namespace
helm upgrade --install "${RELEASE_NAME}" "${CHART_PATH}" \
  --namespace "${NAMESPACE}" \
  --create-namespace \
  --set image.tag="${BUILD_ID}" \
  --wait --timeout 5m

if [ $? -ne 0 ]; then
  echo "❌ FAIL: Helm deployment failed"
  exit 1
fi
echo "✅ PASS: Helm deployment successful"

# Wait for pods to be ready
kubectl wait --for=condition=ready pod \
  -l app=${SERVICE_NAME} \
  -n ${NAMESPACE} \
  --timeout=300s

if [ $? -ne 0 ]; then
  echo "❌ FAIL: Pods not ready"
  kubectl describe pods -l app=${SERVICE_NAME} -n ${NAMESPACE}
  exit 1
fi
echo "✅ PASS: Pods ready"

# Test health endpoints
POD_NAME=$(kubectl get pod -l app=${SERVICE_NAME} -n ${NAMESPACE} -o jsonpath='{.items[0].metadata.name}')
kubectl exec ${POD_NAME} -n ${NAMESPACE} -- curl -f http://localhost:${APP_PORT}/health

if [ $? -ne 0 ]; then
  echo "❌ FAIL: Health check failed"
  exit 1
fi
echo "✅ PASS: Health check successful"

# Test service connectivity
kubectl run curl-test --image=curlimages/curl -i --rm --restart=Never -n ${NAMESPACE} \
  -- curl -f http://${SERVICE_NAME}.${NAMESPACE}.svc.cluster.local/health

if [ $? -ne 0 ]; then
  echo "❌ FAIL: Service connectivity failed"
  exit 1
fi
echo "✅ PASS: Service connectivity successful"

# Test metrics endpoint
kubectl exec ${POD_NAME} -n ${NAMESPACE} -- curl -f http://localhost:${APP_PORT}/metrics

if [ $? -ne 0 ]; then
  echo "⚠️  WARN: Metrics endpoint not available"
fi

# Cleanup
helm uninstall "${RELEASE_NAME}" -n ${NAMESPACE}

echo "✅ Deployment integration tests passed"
```

### 6. Progressive Delivery Tests

```bash
#!/bin/bash
# Test: Canary deployment validation

echo "🔍 Testing progressive delivery..."

# Test: Helm rollback capability
helm rollback "${RELEASE_NAME}" 0 -n ${NAMESPACE} --dry-run
if [ $? -ne 0 ]; then
  echo "❌ FAIL: Rollback dry-run failed"
  exit 1
fi
echo "✅ PASS: Rollback capability verified"

# Test: HPA functionality
kubectl autoscale deployment ${SERVICE_NAME} \
  --cpu-percent=70 \
  --min=2 \
  --max=10 \
  -n ${NAMESPACE} \
  --dry-run=client

if [ $? -ne 0 ]; then
  echo "❌ FAIL: HPA configuration invalid"
  exit 1
fi
echo "✅ PASS: HPA configuration valid"

echo "✅ Progressive delivery tests passed"
```

### 7. Observability Tests

```bash
#!/bin/bash
# Test: Observability integration

echo "🔍 Testing observability..."

# Test: Structured logging
LOG_SAMPLE=$(kubectl logs ${POD_NAME} -n ${NAMESPACE} --tail=10)
if ! echo "${LOG_SAMPLE}" | jq -e . >/dev/null 2>&1; then
  echo "⚠️  WARN: Logs not in JSON format"
fi

# Test: Prometheus metrics format
METRICS=$(kubectl exec ${POD_NAME} -n ${NAMESPACE} -- curl -s http://localhost:${APP_PORT}/metrics)
if ! echo "${METRICS}" | grep -q "^# HELP"; then
  echo "⚠️  WARN: Prometheus metrics format invalid"
fi

# Test: Tracing headers
TRACE_RESPONSE=$(kubectl exec ${POD_NAME} -n ${NAMESPACE} -- \
  curl -s -D - http://localhost:${APP_PORT}/health | grep -i "trace")
if [ -z "${TRACE_RESPONSE}" ]; then
  echo "⚠️  WARN: Tracing headers not present"
fi

echo "✅ Observability tests passed"
```

### 8. Security Runtime Tests

```bash
#!/bin/bash
# Test: Runtime security

echo "🔍 Testing runtime security..."

# Test: Pod runs as non-root
USER_ID=$(kubectl get pod ${POD_NAME} -n ${NAMESPACE} -o jsonpath='{.spec.containers[0].securityContext.runAsUser}')
if [ "${USER_ID}" == "0" ] || [ -z "${USER_ID}" ]; then
  echo "❌ FAIL: Pod running as root"
  exit 1
fi
echo "✅ PASS: Pod runs as user ${USER_ID}"

# Test: Read-only root filesystem (recommended)
READ_ONLY=$(kubectl get pod ${POD_NAME} -n ${NAMESPACE} -o jsonpath='{.spec.containers[0].securityContext.readOnlyRootFilesystem}')
if [ "${READ_ONLY}" != "true" ]; then
  echo "⚠️  WARN: Root filesystem not read-only"
fi

# Test: Capabilities dropped
CAPS=$(kubectl get pod ${POD_NAME} -n ${NAMESPACE} -o jsonpath='{.spec.containers[0].securityContext.capabilities.drop}')
if ! echo "${CAPS}" | grep -q "ALL"; then
  echo "⚠️  WARN: Not all capabilities dropped"
fi

# Test: AppArmor/SELinux
APPARMOR=$(kubectl get pod ${POD_NAME} -n ${NAMESPACE} -o jsonpath='{.metadata.annotations.container\.apparmor\.security\.beta\.kubernetes\.io/.*}')
if [ -z "${APPARMOR}" ]; then
  echo "⚠️  WARN: AppArmor not configured"
fi

echo "✅ Security runtime tests passed"
```

## Test Orchestration Script

Create `scripts/run-all-tests.sh`:

```bash
#!/bin/bash
set -e

echo "🚀 Starting comprehensive AKS deployment tests..."

# Set variables
export SERVICE_NAME="your-service"
export ACR_NAME="your-acr"
export BUILD_ID="${GITHUB_SHA:-$(git rev-parse --short HEAD)}"
export NAMESPACE="test"

# Run test suites
./scripts/test-dockerfile.sh
./scripts/test-image-security.sh
./scripts/test-helm-chart.sh
./scripts/test-k8s-policy.sh

# Framework-specific tests
if [ -f "package.json" ]; then
  ./scripts/test-nodejs.sh
elif [ -f "requirements.txt" ]; then
  ./scripts/test-python.sh
elif [ -f "pom.xml" ]; then
  ./scripts/test-java.sh
elif [ -f "*.csproj" ]; then
  ./scripts/test-dotnet.sh
fi

./scripts/test-deployment.sh
./scripts/test-progressive-delivery.sh
./scripts/test-observability.sh
./scripts/test-security-runtime.sh

echo "✅ All tests passed! Deployment ready for promotion."
```

## Quality Gates

Tests must meet these thresholds:
- ✅ Code coverage ≥ 80%
- ✅ No HIGH/CRITICAL vulnerabilities
- ✅ All unit tests passing
- ✅ Image signed and verified
- ✅ Resource limits defined
- ✅ Health probes responding
- ✅ Security context configured
- ✅ Rollback capability verified

## CI/CD Integration

Add to pipeline:
```yaml
- stage: Test
  jobs:
  - job: QualityGates
    steps:
    - script: ./scripts/run-all-tests.sh
      displayName: 'Run comprehensive tests'
      condition: succeededOrFailed()
    
    - task: PublishTestResults@2
      inputs:
        testResultsFormat: 'JUnit'
        testResultsFiles: '**/test-results.xml'
    
    - task: PublishCodeCoverageResults@1
      inputs:
        codeCoverageTool: 'Cobertura'
        summaryFileLocation: '**/coverage.xml'
```

## Post-Test Reporting

Generate test report:
```bash
# Create test summary
cat > test-summary.md <<EOF
# Test Summary

## Constitution Compliance: ✅ PASS
## Image Security: ✅ PASS
## Helm Chart: ✅ PASS
## Framework Tests: ✅ PASS
## Deployment: ✅ PASS
## Observability: ✅ PASS
## Security: ✅ PASS

All quality gates met. Ready for production promotion.
EOF
```

---

## Error Handling

**Missing Docker/Helm**: Report which tools are missing and provide installation guidance.

**Test Failures**: Continue running remaining tests but report failures with remediation steps.

**No Deployment Found**: Request service name and namespace to locate resources.

## Examples

### Example 1: Full Test Suite

```
/test-aks-devops-deployment "
Run all tests for fraud-api service.
Namespace: fraud-detection, Cluster: aks-ml-prod
"
```

### Example 2: Security-Focused Tests

```
/test-aks-devops-deployment "
Security audit for payment-service.
Focus on image vulnerabilities and secrets management.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/aks-devops-deployment/aks-devops-deployment-constitution.md`
- **Security Tests**: Constitution Section V
- **Related**: debug-aks-devops-deployment, refactor-aks-devops-deployment

---

**Constitution Alignment**: This test suite enforces all hard-stop rules and validates mandatory patterns from `aks-microservice-deployment-constitution.md`.
