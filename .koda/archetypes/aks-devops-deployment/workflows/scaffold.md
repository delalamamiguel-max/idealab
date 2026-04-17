---
description: Generate AKS microservice deployment with framework-specific CI/CD, Helm charts, and governance guardrails
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Validate Prerequisites

```bash
# Check all required tools
az --version || echo "❌ Install Azure CLI: brew install azure-cli"
kubelogin --version || echo "❌ Install kubelogin: brew install Azure/kubelogin/kubelogin"
kubectl version --client || echo "❌ Install kubectl: brew install kubectl"
helm version || echo "❌ Install helm: brew install helm"
docker --version || podman --version || echo "❌ Install Docker or Podman"
jq --version || echo "❌ Install jq: brew install jq"

# Check authentication
az account show || az login
kubectl cluster-info || echo "❌ Configure kubectl context"

# Framework-specific checks
# Python projects only
[ -n "$PIP_INDEX_JFROG_CREDS" ] || echo "⚠️  Set PIP_INDEX_JFROG_CREDS for Python projects"

# Node.js projects only
[ -f ~/.npmrc ] || echo "⚠️  Create ~/.npmrc for Node.js projects (see prerequisites)"
```

**If ANY checks fail, STOP and install missing tools before proceeding.**

See: `${ARCHETYPES_BASEDIR}/aks-devops-deployment/aks-microservice-deployment-constitution.md` Section II for detailed installation instructions.

### Step 0.5: Gather Required Configuration

**PROMPT THE USER FOR ALL OF THE FOLLOWING before starting scaffold:**

#### 1. Framework Detection
- **Framework**: Node.js | Python | Java | .NET
- Auto-detect from project files or ask user

#### 2. Target AKS Cluster
- **Cluster Name**: e.g., `Fml-EastUs2-Dev-AKS-Cluster`
- **Resource Group**: e.g., `Fml-30294-EastUs2-Dev-Infra-Rg`
- **Subscription ID**: e.g., `30740a9c-8a80-444e-9b58-3b63529bfae4`
- **Target Namespace**: e.g., `dev`, `staging`, `prod`

#### 3. Container Configuration
- **Container Tool**: Docker or Podman? (Check: `docker --version || podman --version`)
- **Architecture**: ARM (M1/M2 Mac) or AMD64? (ARM requires `--platform linux/amd64`)

#### 4. Registry Configuration
- **Push Repository** (no port): e.g., `apm0013448-dkr-gold`
- **Pull Repository** (with :22609): e.g., `apm0013448-dkr-group`
- Note: Push and pull use different repositories per AT&T standards

#### 5. Ingress Configuration
- **Ingress Host**: e.g., `fraudml.dev.att.com`
- **Ingress Path**: e.g., `/my-api` (will be expanded to `/my-api(/|$)(.*)` pattern)
- **TLS Secret Name**: e.g., `fraudml-dev-ingress-tls`
- **TLS Source Namespace**: e.g., `com-att-fraud-runtime` (namespace where TLS secret currently exists)

#### 6. Framework-Specific Prerequisites

**For Python Projects:**
- [ ] **PIP_INDEX_JFROG_CREDS** environment variable set
  ```bash
  # Format: username:reftkn:01:token_value
  export PIP_INDEX_JFROG_CREDS="user@att.com:reftkn:01:YOUR_TOKEN"
  # Verify it's set
  echo $PIP_INDEX_JFROG_CREDS
  ```
- [ ] Verify access to `artifact.it.att.com/artifactory/api/pypi/apm-att-pypi-group/simple`

**For Node.js Projects:**
- [ ] **~/.npmrc** configured with JFrog credentials
  ```bash
  # Generate token from ~/.docker/config.json
  TOKEN=$(cat ~/.docker/config.json | jq -r '.auths."https://artifact.it.att.com".auth')
  cat > ~/.npmrc << EOF
//artifact.it.att.com/artifactory/api/npm/npm-virtual/:_auth=${TOKEN}
registry=https://artifact.it.att.com/artifactory/api/npm/npm-virtual/
EOF
  # Verify it exists
  cat ~/.npmrc
  ```
- [ ] Confirm `.npmrc` will be mounted as BuildKit secret during build

#### 7. Confirm Cluster Access

```bash
# Set kubectl context to target cluster
az aks get-credentials \
  --resource-group <RESOURCE_GROUP_FROM_STEP_2> \
  --name <CLUSTER_NAME_FROM_STEP_2> \
  --subscription <SUBSCRIPTION_ID_FROM_STEP_2> \
  --overwrite-existing

# Verify connectivity
kubectl config current-context
kubectl get nodes
kubectl get namespaces | grep <TARGET_NAMESPACE>
```

**⛔ STOP: Do not proceed with scaffolding until ALL prerequisites are validated and configuration is gathered.**

## Configuration Summary

After gathering all prerequisites from Step 0.5, you should have:

1. ✅ **Framework**: Node.js | Python | Java | .NET
2. ✅ **Service Name**: Microservice identifier (e.g., `order-api`, `user-service`)
3. ✅ **Target AKS Cluster**: Name, resource group, subscription ID
4. ✅ **Target Namespace**: Kubernetes namespace for deployment
5. ✅ **Port**: Application listening port (default: 3000 for Node.js, 8000 for Python, 8080 for Java, 5000 for .NET)
6. ✅ **Container Tool**: Docker or Podman confirmed working
7. ✅ **Artifactory Push Repo**: e.g., `apm0013448-dkr-gold` (NO PORT)
8. ✅ **Artifactory Pull Repo**: e.g., `apm0013448-dkr-group` (WITH PORT :22609)
9. ✅ **Ingress Host**: e.g., `fraudml.dev.att.com`
10. ✅ **Ingress Path**: e.g., `/my-api`
11. ✅ **TLS Secret Name**: e.g., `fraudml-dev-ingress-tls`
12. ✅ **TLS Source Namespace**: Namespace where TLS secret currently exists
13. ✅ **Python**: PIP_INDEX_JFROG_CREDS environment variable set (if Python)
14. ✅ **Node.js**: ~/.npmrc file configured (if Node.js)

## Workflow Steps

### 1. Constitution Validation

Read and apply guardrails from:
```
${ARCHETYPES_BASEDIR}/aks-devops-deployment/aks-microservice-deployment-constitution.md
```

Verify no hard-stop rule violations in user requirements.

### 2. Framework Detection & Scaffold Selection

If framework not explicitly provided, detect from:
- `package.json` → Node.js
- `requirements.txt` or `pyproject.toml` → Python
- `pom.xml` or `build.gradle` → Java
- `*.csproj` → .NET

### 3. Generate Dockerfile

**CRITICAL: Base Image Registry Requirement**
- ✘ **NEVER** use public registries (docker.io, docker.hub, gcr.io, quay.io, mcr.microsoft.com)
- ✔ **ALWAYS** use AT&T internal registry: `artifact.it.att.com/docker-proxy/`
- ✔ **ALWAYS** use the `docker-proxy` virtual repository for all base images in Dockerfile FROM statements
- ✔ **ALWAYS** pin images with SHA256 digest for supply chain security when possible

**Base Image Mapping**:
```
Public Registry → AT&T Internal Registry
--------------------------------------------------------------------
node:20-alpine → artifact.it.att.com/docker-proxy/node:20-alpine
python:3.11-slim → artifact.it.att.com/docker-proxy/python:3.11-slim
maven:3.9-eclipse-temurin-17 → artifact.it.att.com/docker-proxy/maven:3.9-eclipse-temurin-17
eclipse-temurin:17-jre-alpine → artifact.it.att.com/docker-proxy/eclipse-temurin:17-jre-alpine
mcr.microsoft.com/dotnet/sdk:8.0 → artifact.it.att.com/docker-proxy/dotnet/sdk:8.0
mcr.microsoft.com/dotnet/aspnet:8.0 → artifact.it.att.com/docker-proxy/dotnet/aspnet:8.0

Note: docker-proxy is a virtual repository that proxies all public registries
```

Create multi-stage Dockerfile at `./Dockerfile`:

#### Node.js Example:
```dockerfile
# syntax=docker/dockerfile:1
# CRITICAL: Use artifact.it.att.com/docker-proxy/ for base images
FROM artifact.it.att.com/docker-proxy/node:20-alpine AS builder
WORKDIR /app

# Copy package files
COPY package*.json ./

# CRITICAL: Use BuildKit secret for .npmrc
# Requires ~/.npmrc to be configured with JFrog credentials
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci --only=production

COPY . .
RUN npm run build

FROM artifact.it.att.com/docker-proxy/node:20-alpine
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
WORKDIR /app
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/package.json ./package.json

USER nodejs
EXPOSE 3000
ENV NODE_ENV=production
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

CMD ["node", "dist/index.js"]
```

**Node.js Build Command**:
```bash
# CRITICAL: Verify .npmrc exists
if [ ! -f ~/.npmrc ]; then
  echo "❌ ERROR: ~/.npmrc not found"
  echo "   Create it with:"
  echo "   TOKEN=\$(cat ~/.docker/config.json | jq -r '.auths.\"https://artifact.it.att.com\".auth')"
  echo "   cat > ~/.npmrc << EOF"
  echo "//artifact.it.att.com/artifactory/api/npm/npm-virtual/:_auth=\${TOKEN}"
  echo "registry=https://artifact.it.att.com/artifactory/api/npm/npm-virtual/"
  echo "EOF"
  exit 1
fi

# Build with .npmrc as BuildKit secret
DOCKER_BUILDKIT=1 docker build --platform linux/amd64 \
  --secret id=npmrc,src=$HOME/.npmrc \
  -t artifact.it.att.com/apm0013448-dkr-gold/myapp:1.0.0 .

# OR with Podman
podman build --platform linux/amd64 \
  --secret id=npmrc,src=$HOME/.npmrc \
  -t artifact.it.att.com/apm0013448-dkr-gold/myapp:1.0.0 .
```

#### Python Example:
```dockerfile
# syntax=docker/dockerfile:1
# CRITICAL: Use artifact.it.att.com/docker-proxy/ for base images
FROM artifact.it.att.com/docker-proxy/python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies (for packages like numpy, pandas)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .

# CRITICAL: Use AT&T internal PyPI with BuildKit secret
# Requires PIP_INDEX_JFROG_CREDS environment variable
RUN --mount=type=secret,id=PIP_INDEX_JFROG_CREDS \
    PIP_CREDS=$(cat /run/secrets/PIP_INDEX_JFROG_CREDS 2>/dev/null || echo "") && \
    if [ -z "$PIP_CREDS" ]; then \
        echo "ERROR: PIP_INDEX_JFROG_CREDS secret not found or empty"; \
        exit 1; \
    fi && \
    export PIP_INDEX_URL="https://${PIP_CREDS}@artifact.it.att.com/artifactory/api/pypi/apm-att-pypi-group/simple" && \
    export PIP_TRUSTED_HOST="artifact.it.att.com" && \
    pip install --user --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Production stage
FROM artifact.it.att.com/docker-proxy/python:3.11-slim

# Create non-root user
RUN groupadd -g 1001 appuser && useradd -r -u 1001 -g appuser appuser

WORKDIR /app

# Copy dependencies and app from builder
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local
COPY --chown=appuser:appuser app ./app

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Python Build Command**:
```bash
# CRITICAL: Verify PIP_INDEX_JFROG_CREDS is set
if [ -z "$PIP_INDEX_JFROG_CREDS" ]; then
  echo "❌ ERROR: PIP_INDEX_JFROG_CREDS environment variable not set"
  echo "   Set it with: export PIP_INDEX_JFROG_CREDS='user@att.com:reftkn:01:YOUR_TOKEN'"
  exit 1
fi

# Create temporary credentials file
echo "$PIP_INDEX_JFROG_CREDS" > /tmp/pip_creds.txt
chmod 600 /tmp/pip_creds.txt

# Build with secret (Docker or Podman)
docker build --platform linux/amd64 \
  --secret id=PIP_INDEX_JFROG_CREDS,src=/tmp/pip_creds.txt \
  -t artifact.it.att.com/apm0013448-dkr-gold/myapp:1.0.0 .

# OR with Podman
podman build --platform linux/amd64 \
  --secret id=PIP_INDEX_JFROG_CREDS,src=/tmp/pip_creds.txt \
  -t artifact.it.att.com/apm0013448-dkr-gold/myapp:1.0.0 .

# Clean up
rm /tmp/pip_creds.txt
```

#### Java Example:
```dockerfile
# syntax=docker/dockerfile:1
# CRITICAL: Use artifact.it.att.com/docker-proxy/ for base images
FROM artifact.it.att.com/docker-proxy/maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn clean package -DskipTests

FROM artifact.it.att.com/docker-proxy/eclipse-temurin:17-jre-alpine
RUN addgroup -g 1001 app && adduser -D -u 1001 -G app app
WORKDIR /app
COPY --from=builder --chown=app:app /app/target/*.jar app.jar

USER app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

CMD ["java", "-jar", "app.jar"]
```

#### .NET Example:
```dockerfile
# syntax=docker/dockerfile:1
# CRITICAL: Use artifact.it.att.com/docker-proxy/ for base images
FROM artifact.it.att.com/docker-proxy/dotnet/sdk:8.0 AS builder
WORKDIR /app
COPY *.csproj .
RUN dotnet restore
COPY . .
RUN dotnet publish -c Release -o out --no-restore

FROM artifact.it.att.com/docker-proxy/dotnet/aspnet:8.0
RUN useradd -m -u 1001 app
WORKDIR /app
COPY --from=builder --chown=app:app /app/out .

USER app
EXPOSE 5000
ENV ASPNETCORE_URLS=http://+:5000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

ENTRYPOINT ["dotnet", "YourApp.dll"]
```

Also create `.dockerignore`:
```
node_modules
__pycache__
*.pyc
target
bin
obj
.git
.env
*.log
```

### 4. Generate Helm Chart

Create Helm chart structure at `./helm/<service-name>/`:

**Chart.yaml**:
```yaml
apiVersion: v2
name: {service-name}
description: A Helm chart for {service-name} microservice
type: application
version: 1.0.0
appVersion: "1.0.0"
```

**values.yaml**:
```yaml
replicaCount: 2

image:
  # CRITICAL: Use pull repository with port :22609 (dkr-group)
  # If ImagePullBackOff occurs, see troubleshooting section 9.2.1
  repository: artifact.it.att.com:22609/{pull-repo}/{service-name}
  pullPolicy: IfNotPresent
  tag: "latest"

imagePullSecrets:
  - name: att-registry-secret  # Must match repository server exactly

framework: {nodejs|python|java|dotnet}

service:
  type: ClusterIP
  port: 80
  targetPort: {framework-port}

ingress:
  enabled: true
  className: nginx
  annotations:
    nginx.ingress.kubernetes.io/proxy-body-size: 500m
    nginx.ingress.kubernetes.io/proxy-connect-timeout: 1500s
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.org/client-max-body-size: 2000m
  hosts:
    - host: {ingress-host}  # e.g., fraudml.dev.att.com
      paths:
        - path: {ingress-path}(/|$)(.*)
          pathType: ImplementationSpecific  # CRITICAL: Use ImplementationSpecific, NOT Prefix
  tls:
    - secretName: {tls-secret-name}  # e.g., fraudml-dev-ingress-tls
      hosts:
        - {ingress-host}

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 250m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

healthCheck:
  liveness:
    path: {framework-health-path}
    initialDelaySeconds: 30
    periodSeconds: 10
  readiness:
    path: {framework-health-path}
    initialDelaySeconds: 5
    periodSeconds: 5

securityContext:
  runAsNonRoot: true
  runAsUser: 1001
  fsGroup: 1001
  capabilities:
    drop:
      - ALL

env: []
  # - name: DATABASE_URL
  #   valueFrom:
  #     secretKeyRef:
  #       name: db-secret
  #       key: url

keyVault:
  enabled: false
  # name: my-keyvault
  # tenantId: "your-tenant-id"
  # secrets: []
```

**templates/deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "{service-name}.fullname" . }}
  labels:
    {{- include "{service-name}.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "{service-name}.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "{{ .Values.service.targetPort }}"
        prometheus.io/path: "/metrics"
      labels:
        {{- include "{service-name}.selectorLabels" . | nindent 8 }}
    spec:
      securityContext:
        {{- toYaml .Values.securityContext | nindent 8 }}
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: {{ .Values.service.targetPort }}
          protocol: TCP
        livenessProbe:
          httpGet:
            path: {{ .Values.healthCheck.liveness.path }}
            port: http
          initialDelaySeconds: {{ .Values.healthCheck.liveness.initialDelaySeconds }}
          periodSeconds: {{ .Values.healthCheck.liveness.periodSeconds }}
        readinessProbe:
          httpGet:
            path: {{ .Values.healthCheck.readiness.path }}
            port: http
          initialDelaySeconds: {{ .Values.healthCheck.readiness.initialDelaySeconds }}
          periodSeconds: {{ .Values.healthCheck.readiness.periodSeconds }}
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
        env:
        {{- range .Values.env }}
        - name: {{ .name }}
          {{- if .value }}
          value: {{ .value | quote }}
          {{- else if .valueFrom }}
          valueFrom:
            {{- toYaml .valueFrom | nindent 14 }}
          {{- end }}
        {{- end }}
```

**templates/service.yaml**, **templates/ingress.yaml**, **templates/hpa.yaml**, **templates/_helpers.tpl** (standard Helm templates).

### 5. Generate CI/CD Pipeline

#### For Azure DevOps:

Create `azure-pipelines.yml`:

```yaml
trigger:
  branches:
    include:
      - main
      - develop

variables:
  acrName: 'your-acr'
  imageName: '{service-name}'
  helmChartPath: './helm/{service-name}'
  
stages:
- stage: Build
  displayName: 'Build and Test'
  jobs:
  - job: BuildJob
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    # Framework-specific build steps
    {{- if nodejs }}
    - task: NodeTool@0
      inputs:
        versionSpec: '20.x'
    - script: |
        npm ci
        npm run lint
        npm test
        npm run build
      displayName: 'Build and Test Node.js'
    {{- else if python }}
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.11'
    - script: |
        pip install -r requirements.txt
        pip install pytest pytest-cov flake8
        flake8 .
        pytest --cov=. --cov-report=xml
      displayName: 'Build and Test Python'
    {{- else if java }}
    - task: Maven@3
      inputs:
        mavenPomFile: 'pom.xml'
        goals: 'clean verify'
    {{- else if dotnet }}
    - task: UseDotNet@2
      inputs:
        version: '8.x'
    - script: |
        dotnet restore
        dotnet build --no-restore
        dotnet test --no-build --verbosity normal
      displayName: 'Build and Test .NET'
    {{- end }}
    
    # Security Scanning
    - task: Bash@3
      displayName: 'Run Trivy vulnerability scan'
      inputs:
        targetType: 'inline'
        script: |
          docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
            aquasec/trivy:latest image --severity HIGH,CRITICAL \
            --exit-code 1 $(imageName):$(Build.BuildId)
    
    # Build and Push Docker Image
    - task: Docker@2
      displayName: 'Build Docker Image'
      inputs:
        command: 'build'
        repository: '$(acrName).azurecr.io/$(imageName)'
        dockerfile: './Dockerfile'
        tags: |
          $(Build.BuildId)
          latest
    
    - task: Docker@2
      displayName: 'Push to ACR'
      inputs:
        command: 'push'
        repository: '$(acrName).azurecr.io/$(imageName)'
        tags: |
          $(Build.BuildId)
          latest
    
    # Sign Image with Cosign
    - task: Bash@3
      displayName: 'Sign container image'
      inputs:
        targetType: 'inline'
        script: |
          cosign sign --key cosign.key $(acrName).azurecr.io/$(imageName):$(Build.BuildId)

- stage: DeployDev
  displayName: 'Deploy to Dev'
  dependsOn: Build
  jobs:
  - deployment: DeployDevJob
    environment: 'dev'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: HelmDeploy@0
            inputs:
              connectionType: 'Azure Resource Manager'
              azureSubscription: 'your-subscription'
              azureResourceGroup: 'your-rg'
              kubernetesCluster: 'your-aks-dev'
              namespace: 'dev'
              command: 'upgrade'
              chartType: 'FilePath'
              chartPath: '$(helmChartPath)'
              releaseName: '{service-name}'
              overrideValues: 'image.tag=$(Build.BuildId)'
              install: true
          
          # Post-deployment smoke tests
          - task: Bash@3
            displayName: 'Run smoke tests'
            inputs:
              targetType: 'inline'
              script: |
                kubectl wait --for=condition=ready pod -l app={service-name} -n dev --timeout=300s
                curl -f https://{service-name}-dev.example.com/health || exit 1

- stage: DeployStaging
  displayName: 'Deploy to Staging'
  dependsOn: DeployDev
  jobs:
  - deployment: DeployStagingJob
    environment: 'staging'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: HelmDeploy@0
            inputs:
              connectionType: 'Azure Resource Manager'
              azureSubscription: 'your-subscription'
              azureResourceGroup: 'your-rg'
              kubernetesCluster: 'your-aks-staging'
              namespace: 'staging'
              command: 'upgrade'
              chartType: 'FilePath'
              chartPath: '$(helmChartPath)'
              releaseName: '{service-name}'
              overrideValues: 'image.tag=$(Build.BuildId)'
              install: true

- stage: DeployProd
  displayName: 'Deploy to Production (Canary)'
  dependsOn: DeployStaging
  jobs:
  - deployment: DeployProdJob
    environment: 'production'
    strategy:
      canary:
        increments: [10, 25, 50, 100]
        preDeploy:
          steps:
          - task: Bash@3
            displayName: 'Pre-deployment checks'
            inputs:
              targetType: 'inline'
              script: |
                # Check for active incidents
                echo "Checking incident status..."
                # Add your incident check logic here
        deploy:
          steps:
          - task: HelmDeploy@0
            inputs:
              connectionType: 'Azure Resource Manager'
              azureSubscription: 'your-subscription'
              azureResourceGroup: 'your-rg'
              kubernetesCluster: 'your-aks-prod'
              namespace: 'production'
              command: 'upgrade'
              chartType: 'FilePath'
              chartPath: '$(helmChartPath)'
              releaseName: '{service-name}'
              overrideValues: 'image.tag=$(Build.BuildId)'
              install: true
        postRouteTra:
          steps:
          - task: Bash@3
            displayName: 'Monitor golden signals'
            inputs:
              targetType: 'inline'
              script: |
                # Monitor error rate, latency, throughput
                echo "Monitoring deployment health..."
                sleep 300  # 5 minutes soak time
                # Add your monitoring validation here
        on:
          failure:
            steps:
            - task: HelmDeploy@0
              displayName: 'Rollback on failure'
              inputs:
                connectionType: 'Azure Resource Manager'
                azureSubscription: 'your-subscription'
                azureResourceGroup: 'your-rg'
                kubernetesCluster: 'your-aks-prod'
                namespace: 'production'
                command: 'rollback'
                releaseName: '{service-name}'
```

#### For GitHub Actions:

Create `.github/workflows/deploy.yml` with similar structure adapted for GitHub Actions syntax.

### 6. Generate Infrastructure as Code

Create `infra/bicep/main.bicep` or `infra/terraform/main.tf` for AKS cluster provisioning (if needed).

### 7. Generate Observability Configuration

Create `observability/prometheus-rules.yaml`:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: {service-name}-alerts
spec:
  groups:
  - name: {service-name}
    interval: 30s
    rules:
    - alert: HighErrorRate
      expr: rate(http_requests_total{job="{service-name}",status=~"5.."}[5m]) > 0.05
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "High error rate detected"
    - alert: HighLatency
      expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="{service-name}"}[5m])) > 1
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High latency detected (p95 > 1s)"
```

Create `observability/grafana-dashboard.json` with pre-configured dashboards.

### 8. Generate Documentation

Create `README.md`:
```markdown
# {Service Name}

## Overview
{Brief description}

## Technology Stack
- Framework: {framework}
- Container: Docker
- Orchestration: Kubernetes (AKS)
- Deployment: Helm
- CI/CD: {Azure DevOps | GitHub Actions}

## Prerequisites
- Azure CLI
- kubectl
- Helm 3.x
- Docker

## Local Development
\`\`\`bash
# Framework-specific commands
{npm install | pip install -r requirements.txt | mvn install | dotnet restore}
{npm run dev | uvicorn main:app --reload | mvn spring-boot:run | dotnet run}
\`\`\`

## Build and Deploy
\`\`\`bash
# Build Docker image
docker build -t {service-name}:latest .

# Deploy to AKS
helm upgrade --install {service-name} ./helm/{service-name} \
  --namespace {environment} \
  --set image.tag=latest
\`\`\`

## Health Endpoints
- Liveness: `{health-path}`
- Readiness: `{health-path}`
- Metrics: `/metrics`

## Rollback
\`\`\`bash
helm rollback {service-name} -n {environment}
\`\`\`

## Monitoring
- Grafana: https://grafana.example.com/d/{dashboard-id}
- Prometheus: https://prometheus.example.com

## Governance
This deployment follows:
- Constitution: (pre-loaded above)
- Hard-stop rules enforced via pre-commit hooks and CI gates

## Troubleshooting
### Common Issues & Solutions (Lessons Learned - Nov 2025)

### Issue 1: Container Tool Not Available

**Problem**: Docker not installed or unavailable  
**Error**: `docker: command not found`

**Solution**:
```bash
# Try Docker first
brew install docker

# If Docker unavailable, use Podman
brew install podman
podman machine init
podman machine start
echo "Checking Dockerfile..."
if ! grep -q "USER" Dockerfile; then
  echo "❌ Dockerfile must run as non-root user"
  exit 1
fi

# Check for public registry usage
echo "Checking for public registries in Dockerfile..."
if grep -E "^FROM (node:|python:|maven:|eclipse-temurin:|mcr\.microsoft\.com|docker\.io|gcr\.io|quay\.io)" Dockerfile; then
  echo "❌ Dockerfile must use artifact.it.att.com/docker-proxy/ for all base images"
  echo "   Found public registry reference. Use: artifact.it.att.com/docker-proxy/{image-name}"
  exit 1
fi

# Validate Helm charts
echo "Checking Helm charts..."
helm lint ./helm/*

# Check resource limits
if ! grep -q "resources:" helm/*/templates/deployment.yaml; then
  echo "❌ Deployment must define resource limits"
  exit 1
fi

# Check health probes
if ! grep -q "livenessProbe:" helm/*/templates/deployment.yaml; then
  echo "❌ Deployment must define liveness probe"
  exit 1
fi

echo "✅ All guardrails passed"
```

Create `scripts/validate-env.sh` for environment validation.

### 10. Post-Scaffold Summary

Present checklist:
```
✅ Dockerfile created with multi-stage build and security hardening
   ⚠️  CRITICAL: All base images use artifact.it.att.com/docker-proxy/ (NOT public registries)
✅ Helm chart generated with resource limits, probes, and HPA
✅ CI/CD pipeline configured with security scanning and canary deployment
✅ Observability configured (Prometheus rules, Grafana dashboards)
✅ Documentation and runbooks created
✅ Governance validation scripts added
   ✓ Includes check for public registry usage in Dockerfiles

🔧 Next Steps:
1. Configure Docker authentication with AT&T registry (see docs/ATT-ARTIFACT-REGISTRY-SETUP.md)
2. Update repository name (e.g., apm0013448-dkr-gold) and AKS cluster details in CI/CD pipeline
3. Configure Azure Key Vault integration for secrets
4. Review and customize resource limits in values.yaml
5. Set up monitoring alerts in Azure Monitor
6. Run: `./scripts/check-guardrails.sh` before first commit (validates registry usage)
7. Push to repo to trigger first deployment

⚠️ CRITICAL: Base Image Registry Requirement
ALL Dockerfile FROM statements MUST use: artifact.it.att.com/docker-proxy/
- Docker Hub images → artifact.it.att.com/docker-proxy/{image}
- Microsoft images → artifact.it.att.com/docker-proxy/dotnet/{image}
- All public registries → artifact.it.att.com/docker-proxy/{image}
- Using public registries (node:, python:, mcr.microsoft.com) will FAIL guardrails check
- Note: docker-proxy is a virtual repository that proxies all public registries

⚠️ COMMON PITFALL: ImagePullBackOff (401 Unauthorized)
If deployment fails with ImagePullBackOff:
1. Verify dkr-group includes dkr-gold repository (contact Artifactory admin)
2. Alternative: Pull directly from dkr-gold without port (see constitution 9.2.1)
3. Ensure image pull secret server matches repository URL exactly
4. See: docs/TROUBLESHOOTING.md#issue-4 for full details
```

---

## Error Handling

**Missing Framework**: Default to Python/FastAPI if not specified; ask user to confirm.

**Invalid Cluster**: Validate AKS cluster exists before generating deployment configs.

**Registry Auth Failure**: Provide setup guide for artifact.it.att.com authentication.

**Resource Conflicts**: Check for existing deployments and offer merge strategy.

## Examples

### Example 1: Python ML Service

```
/scaffold-aks-devops-deployment "
Create ML inference service with FastAPI.
Cluster: aks-ml-prod, Service: fraud-detector
Need GPU support and auto-scaling.
"
```

### Example 2: Node.js API

```
/scaffold-aks-devops-deployment "
Deploy Node.js REST API for customer portal.
Framework: Express, Cluster: aks-web-prod
Need canary deployment with 10% traffic split.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/aks-devops-deployment/aks-devops-deployment-constitution.md`
- **Registry Setup**: Constitution Section IX
- **Related**: debug-aks-devops-deployment, test-aks-devops-deployment

---

## Constitution Alignment

This scaffold enforces all hard-stop rules from `aks-microservice-deployment-constitution.md`:
- ✅ Multi-stage Docker builds with digest pinning
- ✅ Image signing with Cosign
- ✅ Progressive delivery with canary strategy
- ✅ Resource limits and health probes
- ✅ Secrets from Key Vault (not hardcoded)
- ✅ Structured logging and telemetry
- ✅ Automated rollback capability
- ✅ 90-day log retention in CI/CD
- ✅ CAB approval gates for production
