# AKS Microservice Deployment Constitution

## Prerequisites

### Required Tools Installation

Before beginning any AKS microservice deployment, ensure the following tools are installed:

**macOS**:
```bash
# Azure CLI with kubelogin plugin
brew install azure-cli
brew install Azure/kubelogin/kubelogin

# Kubernetes tools
brew install kubectl
brew install helm
brew install kubectx  # Optional but recommended

# Container tools (try Docker first, fallback to Podman)
brew install docker  # If Docker Desktop is not already installed
# OR if Docker unavailable/incompatible:
brew install podman
podman machine init
podman machine start
```

**Linux**:
```bash
# Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
az aks install-cli  # Installs kubectl and kubelogin

# Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Container tools
sudo apt-get install docker.io
# OR
sudo apt-get install podman
```

**Verify Installation**:
```bash
az --version
kubelogin --version
kubectl version --client
helm version
docker --version || podman --version
```

### Required Environment Variables

```bash
# AT&T Artifactory PyPI credentials (for Python projects)
export PIP_INDEX_JFROG_CREDS="username:api_token"
# Format: attuid@att.com:reftkn:01:token_value

# Azure authentication
az login
az account set --subscription <subscription-id>

# Kubectl context
kubectl config use-context <aks-cluster-context>
```

### Required Permissions

- **Artifactory**: Write access to push repository (e.g., `apm0013448-dkr-gold`)
- **Artifactory**: Read access to pull repository (e.g., `apm0013448-dkr-group`)
- **AKS**: Contributor or higher on target cluster
- **Key Vault**: Read access for secrets (if used)
- **Container Registry**: Push/Pull permissions

### Pre-Deployment Checklist

- [ ] Tools installed and verified
- [ ] Authenticated with Azure CLI (`az login`)
- [ ] Kubectl context set to target cluster
- [ ] `PIP_INDEX_JFROG_CREDS` set (for Python)
- [ ] Docker config at `~/.docker/config.json` configured
- [ ] Artifactory write permissions verified
- [ ] Ingress host/domain confirmed (e.g., `fraudml.dev.att.com`)
- [ ] TLS secret available or can be copied
- [ ] Target namespace exists or can be created

## Purpose

This constitution unifies CI/CD governance with AKS deployment excellence for **multi-framework microservices** (Node.js, Python, Java, .NET). Every generated pipeline, Helm chart, and deployment manifest must uphold these principles while adapting to framework-specific needs.

**Source**: Merged from `microservice-cicd-architect-constitution.md` (CI/CD governance) and `aks-devops-deployment-constitution.md` (AKS deployment patterns), extended for polyglot support.

**Supported Frameworks**: Node.js, Python, Java, .NET Core

---

## I. Hard-Stop Rules (Non-Negotiable)

Violations require the AI agent to refuse, rewrite, or block the requested artifact.

### 1.1 Supply Chain Security
- ✘ **NEVER** publish container images without signing (Cosign, Notary, or equivalent).
- ✘ **NEVER** disable vulnerability, SBOM, or license scanning steps.
- ✘ **NEVER** use unversioned container images (e.g., `latest` tag without digest).
- ✔ **ALWAYS** enforce reproducible builds and pin base images with digest.
- ✔ **ALWAYS** attest pipeline provenance using in-toto or SLSA metadata.
- ✔ **ALWAYS** push images to Azure Container Registry (ACR) or approved registry.

### 1.2 Deployment Safety
- ✘ **NEVER** deploy directly to production without staged gates (canary, blue/green, or shadow).
- ✘ **NEVER** bypass production approvals unless emergency change protocol is explicitly referenced.
- ✘ **NEVER** deploy without staging validation first.
- ✔ **ALWAYS** include automated rollback or traffic shift reversal paths.
- ✔ **ALWAYS** freeze deploys during active P1/P0 incidents.
- ✔ **ALWAYS** use Helm for templated and version-controlled manifests.

### 1.3 Kubernetes Resource Governance
- ✘ **NEVER** deploy without resource limits and requests defined.
- ✘ **NEVER** deploy without health checks (liveness and readiness probes).
- ✘ **NEVER** make manual configuration changes in AKS clusters.
- ✔ **ALWAYS** use namespaces for environment isolation (dev, staging, prod).
- ✔ **ALWAYS** configure appropriate HPA (Horizontal Pod Autoscaler) policies.

### 1.4 Observability & Auditability
- ✘ **NEVER** push releases without emitting structured deploy events (timestamp, service, version, operator).
- ✘ **NEVER** discard release logs before retention policy (≥ 90 days) is met.
- ✔ **ALWAYS** integrate with Azure Monitor and Prometheus/Grafana for observability.
- ✔ **ALWAYS** map deployment KPIs (frequency, lead time, CFR, MTTR) into dashboards.
- ✔ **ALWAYS** capture change linkages (ticket, commit SHA, artifact digest).

### 1.5 Secrets & Credentials
- ✘ **NEVER** embed secrets within workflow YAML, scripts, manifests, or Dockerfiles.
- ✔ **ALWAYS** source credentials from Azure Key Vault or Kubernetes Secrets with RBAC.
- ✔ **ALWAYS** scope credentials to least privilege and rotate ≤ 90 days.
- ✔ **ALWAYS** use Workload Identity or Managed Identity for AKS pod authentication.

### 1.6 Compliance Alignment
- ✘ **NEVER** merge release automation that lacks traceability to a Request For Change (RFC).
- ✔ **ALWAYS** record CAB approval, change ID, and risk classification in release notes.
- ✘ **NEVER** fork or bypass standardized stages from `pipeline-orchestrator-constitution.md`.

### 1.7 Registry Configuration (AT&T Artifactory)
- ✘ **NEVER** use push repositories (dkr-gold) for Kubernetes image pulls.
- ✘ **NEVER** omit port `:22609` when configuring pull repositories (dkr-group) in Kubernetes manifests.
- ✘ **NEVER** create Kubernetes image pull secrets without matching the repository port in `--docker-server`.
- ✔ **ALWAYS** use push repositories WITHOUT port for `docker build` and `docker push`.
- ✔ **ALWAYS** use pull repositories WITH port `:22609` for Kubernetes deployments.
- ✔ **ALWAYS** ensure Kubernetes secret server matches the image repository URL exactly.

**Registry URL Rules**:
```bash
# PUSH (docker build/push) - NO PORT
docker push artifact.it.att.com/apm0013448-dkr-gold/myapp:1.0.0

# PULL (Kubernetes) - WITH PORT :22609
image: artifact.it.att.com:22609/apm0013448-dkr-group/myapp:1.0.0

# SECRET - MUST MATCH PULL URL PORT
kubectl create secret docker-registry ... \
  --docker-server=artifact.it.att.com:22609
```

### 1.8 Base Image Registry (Dockerfile FROM Statements)
- ✘ **NEVER** use public registries in Dockerfile FROM statements (docker.io, docker.hub, gcr.io, quay.io, mcr.microsoft.com).
- ✘ **NEVER** pull base images from unverified sources outside artifact.it.att.com.
- ✔ **ALWAYS** use AT&T internal registry `artifact.it.att.com/docker-proxy/` for ALL base images in Dockerfiles.
- ✔ **ALWAYS** use the `docker-proxy` virtual repository for public base images.
- ✔ **ALWAYS** pin base images with SHA256 digest for supply chain integrity when possible.
- ✔ **ALWAYS** build for `linux/amd64` architecture when deploying to AKS (even on ARM Macs).

**Base Image Mapping**:
```dockerfile
# ❌ WRONG - Public registries
FROM node:20-alpine
FROM python:3.11-slim
FROM mcr.microsoft.com/dotnet/sdk:8.0

# ✅ CORRECT - AT&T internal registry via docker-proxy
FROM artifact.it.att.com/docker-proxy/node:20-alpine
FROM artifact.it.att.com/docker-proxy/python:3.11-slim
FROM artifact.it.att.com/docker-proxy/dotnet/sdk:8.0
```

**Virtual Repository Path**:
```
Public Source                           → AT&T Internal Path
--------------------------------------------------------------------------------
Docker Hub (node, python, maven, etc.)  → artifact.it.att.com/docker-proxy/{image}
Microsoft Container Registry (MCR)      → artifact.it.att.com/docker-proxy/dotnet/{image}
All public registries                   → artifact.it.att.com/docker-proxy/{image}

Note: docker-proxy is a virtual repository that proxies public registries
```

**Refusal Template**:
```
❌ Request violates Hard-Stop rule {rule_id}. Provide evidence of signed artifacts, staged rollout, resource limits, health probes, structured deploy logs, CAB references, correct registry URLs (push without port, pull with :22609), and AT&T internal base images (artifact.it.att.com/docker-proxy/) before proceeding.
```

---

## II. Development Environment Prerequisites (Must Install)

**Before using this archetype, the following tools MUST be installed and configured:**

### 2.0.1 Container Tool (Docker or Podman)

**CRITICAL**: Always try Docker first, fallback to Podman if Docker unavailable.

#### Docker Desktop (Preferred)
- ✔ **PREFERRED** on macOS and Windows
- ✔ **ALWAYS** verify Docker daemon is accessible (`docker ps` succeeds)
- ✔ **ALWAYS** authenticate Docker with artifact.it.att.com

**Installation**:
- **macOS**: https://docs.docker.com/desktop/setup/install/mac-install/
- **Windows**: https://docs.docker.com/desktop/setup/install/windows-install/
- **Linux**: https://docs.docker.com/desktop/setup/install/linux/

**Verification**: `docker --version && docker ps`

#### Podman (Fallback Alternative)

**When to use Podman**:
- Docker Desktop not available
- Corporate policy restricts Docker
- Licensing concerns with Docker Desktop
- Running on ARM-based Mac (M1/M2/M3) and need AMD64 builds

**Installation**:
```bash
# macOS
brew install podman
podman machine init
podman machine start

# Linux
sudo apt-get install podman  # Debian/Ubuntu
sudo yum install podman       # RHEL/CentOS
```

**Verification**: `podman --version && podman ps`

**CRITICAL Podman Configuration**:

1. **Machine Resources** (macOS only):
```bash
# Give Podman machine enough resources for cross-platform builds
podman machine stop
podman machine set --cpus 4 --memory 8192
podman machine start
```

2. **Architecture-Specific Builds**:
```bash
# On Mac Silicon (ARM), ALWAYS build for AMD64 (AKS cluster architecture)
podman build --platform linux/amd64 -t myapp:1.0.0 .

# Verify architecture
podman inspect myapp:1.0.0 | grep Architecture
# Should show: "Architecture": "amd64"
```

3. **Build Secrets** (for private registries):
```bash
# File-based secrets (more reliable than env-based)
echo "$CREDENTIALS" > /tmp/creds.txt
podman build --secret id=CREDS,src=/tmp/creds.txt .
rm /tmp/creds.txt
```

**Common Podman Issues**:

| Issue | Error | Solution |
|-------|-------|----------|
| Machine not running | `cannot connect to Podman socket` | `podman machine start` |
| Cross-build fails | `exit status 137` (OOM) | Increase machine memory |
| Wrong architecture | `exec format error` in pod logs | Rebuild with `--platform linux/amd64` |
| Secret not found | `PIP_INDEX_JFROG_CREDS secret not found` | Use file-based secrets, not env |

### 2.0.2 Azure CLI
- ✘ **NEVER** attempt AKS deployment without Azure CLI
- ✔ **ALWAYS** verify login status before deployment (`az account show`)

**Installation**: 
```bash
# macOS
brew install azure-cli

# Windows
winget install Microsoft.AzureCLI

# Linux
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

**Verification**: `az --version && az account show`

### 2.0.3 kubectl
- ✘ **NEVER** deploy without kubectl configured for target cluster
- ✔ **ALWAYS** verify cluster connectivity before deployment
- ✔ **ALWAYS** configure kubectl context with subscription ID

**Installation**:
```bash
# macOS
brew install kubectl

# Windows
winget install Kubernetes.kubectl

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install kubectl /usr/local/bin/kubectl

# OR via Azure CLI
az aks install-cli
```

**Verification**: `kubectl version --client`

**Configure kubectl Context** (CRITICAL):
```bash
# Get AKS credentials (use YOUR values!)
az aks get-credentials \
  --resource-group <YOUR_RG> \
  --name <YOUR_CLUSTER> \
  --subscription <YOUR_SUBSCRIPTION_ID> \
  --overwrite-existing

# Example (FAMLI Dev):
az aks get-credentials \
  --resource-group Fml-30294-EastUs2-Dev-Infra-Rg \
  --name Fml-EastUs2-Dev-AKS-Cluster \
  --subscription 30740a9c-8a80-444e-9b58-3b63529bfae4 \
  --overwrite-existing

# Verify
kubectl config current-context
kubectl get nodes
```

### 2.0.4 kubelogin (Azure Kubernetes Authentication)
- ✔ **ALWAYS** install for Azure AD authentication with AKS
- Required for clusters using Azure AD integration

**Installation**:
```bash
# macOS
brew install Azure/kubelogin/kubelogin

# Windows
winget install kubelogin

# Linux
az aks install-cli
```

**Verification**: `kubelogin --version`

### 2.0.5 kubectx (Optional but Recommended)
- ✔ **RECOMMENDED** for easier context switching between clusters
- Simplifies multi-cluster management

**Installation**:
```bash
# macOS
brew install kubectx

# Windows
choco install kubectx

# Linux
sudo apt install kubectx  # Debian/Ubuntu
```

**Verification**: `kubectx --version`

### 2.0.6 Helm
- ✘ **NEVER** deploy without Helm 3.x installed
- ✔ **ALWAYS** use Helm for templated Kubernetes manifests

**Installation**:
```bash
# macOS
brew install helm

# Windows
choco install kubernetes-helm

# Linux
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

**Verification**: `helm version`

### 2.0.7 jq (JSON Processor)
- ✔ **ALWAYS** install for JSON processing in scripts
- Required for token extraction and configuration parsing

**Installation**:
```bash
# macOS
brew install jq

# Windows
choco install jq

# Linux
sudo apt-get install jq  # Debian/Ubuntu
sudo yum install jq      # RHEL/CentOS
```

**Verification**: `jq --version`

### 2.0.8 Python-Specific Requirements

**CRITICAL for Python projects**: Python dependencies installation requires special handling in corporate environments.

#### PIP_INDEX_JFROG_CREDS Environment Variable

- ✘ **NEVER** proceed with Python projects without `PIP_INDEX_JFROG_CREDS` set
- ✔ **ALWAYS** use AT&T internal PyPI mirror: `artifact.it.att.com/artifactory/api/pypi/apm-att-pypi-group/simple`
- ✔ **ALWAYS** include `--trusted-host` flags for corporate SSL certificates

**Setup**:
```bash
# Get your JFrog API token from artifact.it.att.com
# Format: username:password OR username:reftkn:01:token_value
export PIP_INDEX_JFROG_CREDS="mc944m@att.com:reftkn:01:YOUR_TOKEN_HERE"

# Add to ~/.zshrc or ~/.bashrc for persistence
echo 'export PIP_INDEX_JFROG_CREDS="mc944m@att.com:reftkn:01:YOUR_TOKEN"' >> ~/.zshrc
```

**Dockerfile Requirements**:
```dockerfile
# ❌ WRONG - Will timeout in corporate network
RUN pip install -r requirements.txt

# ✅ CORRECT - Uses AT&T internal PyPI with BuildKit secret
RUN --mount=type=secret,id=PIP_INDEX_JFROG_CREDS \
    PIP_CREDS=$(cat /run/secrets/PIP_INDEX_JFROG_CREDS) && \
    export PIP_INDEX_URL="https://${PIP_CREDS}@artifact.it.att.com/artifactory/api/pypi/apm-att-pypi-group/simple" && \
    export PIP_TRUSTED_HOST="artifact.it.att.com" && \
    pip install --user --no-cache-dir -r requirements.txt
```

**Build Command**:
```bash
# Docker
echo "$PIP_INDEX_JFROG_CREDS" > /tmp/pip_creds.txt
docker build --secret id=PIP_INDEX_JFROG_CREDS,src=/tmp/pip_creds.txt -t myapp .
rm /tmp/pip_creds.txt

# Podman
echo "$PIP_INDEX_JFROG_CREDS" > /tmp/pip_creds.txt
podman build --secret id=PIP_INDEX_JFROG_CREDS,src=/tmp/pip_creds.txt -t myapp .
rm /tmp/pip_creds.txt
```

**Common Python Build Issues**:

| Issue | Error | Solution |
|-------|-------|----------|
| PyPI timeout | `Connection timeout to pypi.org` | Use AT&T PyPI mirror |
| SSL errors | `SSL: CERTIFICATE_VERIFY_FAILED` | Add `--trusted-host artifact.it.att.com` |
| Auth errors | `401 Unauthorized` | Verify `PIP_INDEX_JFROG_CREDS` is correct |
| Secret not found | `PIP_INDEX_JFROG_CREDS secret not found` | Use file-based secrets in build command |
| Slow installs | Taking > 5 minutes | Add `gcc` to Dockerfile for compiled packages |

**Install gcc for compiled packages**:
```dockerfile
# Some Python packages (e.g., numpy, pandas) need compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*
```

### 2.0.9 Ingress Configuration Requirements

**CRITICAL**: Before deploying, gather ingress configuration details.

#### Required Information

- **Ingress Host**: Domain name (e.g., `fraudml.dev.att.com`)
- **Ingress Path**: Application path (e.g., `/my-api`)
- **TLS Secret**: Name of existing TLS secret (e.g., `fraudml-dev-ingress-tls`)
- **Source Namespace**: Namespace containing TLS secret (e.g., `com-att-fraud-runtime`)
- **Nginx Class**: Usually `nginx`

**Collect Before Deployment**:
```bash
# List available ingress hosts in cluster
kubectl get ingress --all-namespaces -o custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,HOST:.spec.rules[0].host

# Find TLS secret
kubectl get secret -n com-att-fraud-runtime | grep ingress-tls
```

**Copy TLS Secret to Target Namespace**:
```bash
# Copy from source namespace
kubectl get secret fraudml-dev-ingress-tls -n com-att-fraud-runtime -o yaml | \
  sed 's/namespace: com-att-fraud-runtime/namespace: dev/' | \
  kubectl apply -f -
```

**Standard Ingress Annotations** (AT&T Pattern):
```yaml
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
    - host: fraudml.dev.att.com
      paths:
        - path: /my-api(/|$)(.*)
          pathType: ImplementationSpecific
  tls:
    - secretName: fraudml-dev-ingress-tls
      hosts:
        - fraudml.dev.att.com
```

### 2.0.10 Prerequisites Validation

**Run preflight check** before any deployment:
```bash
./scripts/preflight-check.sh
```

This script validates:
- ✅ Container tool (Docker or Podman) installed and running
- ✅ Azure CLI installed and logged in
- ✅ kubectl installed and cluster accessible
- ✅ kubelogin available
- ✅ Helm installed
- ✅ jq available
- ✅ PIP_INDEX_JFROG_CREDS set (Python projects)
- ✅ Ingress configuration collected
- ✅ All required configurations set

**Refusal Template**:
```
❌ Missing required tool: {tool_name}. 
Install from: {installation_url}
Run preflight check: ./scripts/preflight-check.sh
See: PRE-DEPLOYMENT-CHECKLIST.md for complete setup instructions.
```

---

## III. Mandatory Patterns (Must Apply)

### 2.1 Progressive Delivery Workflow
- Implement canary or blue/green strategy with measurable guardrails.
- Require automated health checks (latency, error ratio, saturation) before traffic escalation.
- Use Helm release versioning for safe rollback capability.

### 2.2 Containerization (Framework-Specific)
All applications must be containerized using **multi-stage Docker builds**:

**CRITICAL**: All base images MUST use `artifact.it.att.com/docker-proxy/` prefix (see Hard-Stop Rule 1.8).

#### Node.js Applications:
```dockerfile
# Base: artifact.it.att.com/docker-proxy/node:20-alpine
# Build: npm ci (not npm install), run tests
# Runtime: Minimal alpine, non-root user
```

#### Python Applications:
```dockerfile
# Base: artifact.it.att.com/docker-proxy/python:3.11-slim
# Build: pip install with --trusted-host flags for corporate network
#        pip install --user --no-cache-dir \
#          --trusted-host pypi.org \
#          --trusted-host files.pythonhosted.org \
#          -r requirements.txt
# Test: run pytest with coverage
# Runtime: Minimal slim, non-root user (UID 1001)
```

#### Java Applications:
```dockerfile
# Base (builder): artifact.it.att.com/docker-proxy/maven:3.9-eclipse-temurin-17
# Base (runtime): artifact.it.att.com/docker-proxy/eclipse-temurin:17-jre-alpine
# Build: Maven/Gradle multi-stage, run tests
# Runtime: JRE-only, non-root user
```

#### .NET Applications:
```dockerfile
# Base (builder): artifact.it.att.com/docker-proxy/dotnet/sdk:8.0
# Base (runtime): artifact.it.att.com/docker-proxy/dotnet/aspnet:8.0
# Build: dotnet restore, dotnet publish, run tests
# Runtime: Minimal aspnet runtime, non-root user
```

### 2.3 CI/CD Integration
- Use Azure DevOps, GitHub Actions, or Jenkins to automate build, test, and deployment.
- Inherit guardrails from `microservice-cicd-architect-constitution.md` and `pipeline-orchestrator-constitution.md`.
- Framework-specific build steps:
  - **Node.js**: `npm ci`, `npm test`, `npm run build`
  - **Python**: `pip install`, `pytest`, build wheel/sdist
  - **Java**: `mvn clean install` or `gradle build`
  - **.NET**: `dotnet restore`, `dotnet test`, `dotnet publish`

### 2.4 Helm Chart Structure
- Deploy to AKS using Helm with versioned charts stored in ACR or Helm registry.
- Chart must include:
  - `values.yaml` with framework-specific defaults (port, health paths)
  - `deployment.yaml` with resource limits, probes, and security context
  - `service.yaml` and `ingress.yaml` as needed
  - `configmap.yaml` for non-sensitive configuration
  - `hpa.yaml` for autoscaling policies

### 2.5 Health Checks (Framework-Specific)

| Framework | Default Health Path | Port |
|-----------|---------------------|------|
| Node.js   | `/health` or `/healthz` | 3000 |
| Python    | `/health` or `/api/health` | 8000 |
| Java      | `/actuator/health` | 8080 |
| .NET      | `/health` or `/healthz` | 5000 |

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 30
  periodSeconds: 10
readinessProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 5
  periodSeconds: 5
```

### 2.6 Structured Logging & Telemetry
- Emit JSON logs with `timestamp`, `service`, `environment`, `version`, `stage`, and `result`.
- Forward metrics to shared observability namespace with deployment ID tags.
- Framework-specific logging:
  - **Node.js**: Winston, Pino, or Bunyan with JSON format
  - **Python**: structlog or python-json-logger
  - **Java**: Logback with JSON encoder
  - **.NET**: Serilog with JSON formatting

### 2.7 Policy as Code Gates
- Enforce policy checks (OPA/Sentinel, Azure Policy) for configuration, security, and change approval.
- Block pipeline if policy evaluation is inconclusive or returns soft-fail on high severity finding.

### 2.8 Automated Rollback & Feature Flags
- Provide documented rollback command: `helm rollback <release> <revision>`.
- Integrate feature flag toggles (LaunchDarkly, Azure App Configuration) for safe disablement.

### 2.9 Post-Deployment Verification
- Execute smoke tests, contract tests, and synthetic checks within rollout window.
- Framework-specific test runners:
  - **Node.js**: Jest, Mocha, or Supertest
  - **Python**: pytest, requests for API tests
  - **Java**: JUnit, RestAssured
  - **.NET**: xUnit, NUnit with WebApplicationFactory

### 2.10 Infrastructure as Code
- Use Bicep or Terraform for AKS cluster provisioning and configuration.
- Version control all IaC and store state securely (Azure Storage, Terraform Cloud).

---

## III. Preferred Patterns (Recommended)

### 3.1 Trunk-Based Development
- Favor short-lived branches with mandatory peer review and automated quality gates.

### 3.2 Deployment Windows & Freeze Automation
- Automate calendar-driven freeze windows with override workflows capturing executive approval.

### 3.3 Drift Detection Integration
- Continuously compare live manifests vs. Git desired state (ArgoCD, Flux) and alert on drift.

### 3.4 ChatOps
- Provide ChatOps commands to trigger deploy, promote, rollback, and status queries.

### 3.5 Golden Signals Dashboard
- Visualize latency, traffic, errors, saturation, deployment lead time, and CFR trends.
- Publish orchestrator-aligned pipeline diagrams illustrating stage reuse and shared tooling.

### 3.6 Framework-Specific Optimizations

#### Node.js:
- Use `.dockerignore` to exclude `node_modules`, `.git`
- Enable npm cache mounting for faster builds
- Use `npm ci --only=production` for production images

#### Python:
- Use multi-stage builds to separate build dependencies from runtime
- Pin exact versions in `requirements.txt` or use Poetry/Pipenv lock files
- Use `pip install --no-cache-dir` to reduce image size

#### Java:
- Use Maven/Gradle dependency caching layers
- Separate dependency downloads from application build
- Use `--no-daemon` for Gradle in CI to reduce memory footprint

#### .NET:
- Use `dotnet publish -c Release --self-contained false` for smaller images
- Enable ReadyToRun compilation for faster startup
- Use layer caching for NuGet packages

---

## IV. Quality Standards

- **Test Coverage**: ≥ 80% for all frameworks (90% for critical services).
- **Deployment Frequency Target**: ≥ 10 per service per week.
- **Lead Time Target**: ≤ 30 minutes from commit to production.
- **Change Failure Rate Target**: ≤ 5% over rolling 4 weeks.
- **MTTR Target**: ≤ 45 minutes for failed deploy recovery.
- **Container Image Size**: 
  - Node.js: ≤ 200 MB
  - Python: ≤ 250 MB
  - Java: ≤ 300 MB
  - .NET: ≤ 200 MB

---

## V. Framework-Specific Security Hardening

### Node.js:
- Run `npm audit` and fail on high/critical vulnerabilities
- Use `node:alpine` or distroless images
- Set `NODE_ENV=production`
- Drop all capabilities, run as non-root (USER node)

### Python:
- Run `pip-audit` or `safety check`
- Use `python:slim` or distroless images
- Set read-only filesystem where possible
- Drop all capabilities, run as non-root (USER app)

### Java:
- Run dependency-check or Snyk
- Use JRE-only images (not JDK) in production
- Enable Java security manager if applicable
- Drop all capabilities, run as non-root (USER app)

### .NET:
- Run `dotnet list package --vulnerable`
- Use minimal aspnet runtime images
- Enable HTTPS redirection and HSTS
- Drop all capabilities, run as non-root (USER app)

---

## VI. Enforcement Mechanisms

- Guardrail scripts (`check-guardrails.sh`) lint workflows for secrets, missing gates, resource limits, and probes.
- Environment validation (`validate-env.sh`) confirms CLI tooling, ACR access, Helm, kubectl, and policy configuration.
- CI pipeline fails fast on policy breaches, unsigned artifacts, missing health checks, or deployment evidence.
- Pre-commit hooks verify Dockerfile best practices and Helm chart validation.

---

## VII. Override Protocol

- Hard-stop overrides require SRE and Security sign-off, documented in change record with compensating controls.
- Preferred pattern deviations demand justification in pipeline comments and owner acknowledgement.
- Framework-specific deviations must include rationale and alternative security controls.

---

## VIII. Framework Selection Guide

Use this matrix to determine framework applicability:

| Use Case | Node.js | Python | Java | .NET |
|----------|---------|--------|------|------|
| REST APIs | ✓ | ✓ | ✓ | ✓ |
| GraphQL | ✓ | ✓ | ✓ | ✓ |
| WebSockets | ✓ | ✓ | ✓ | ✓ |
| Event Streaming | ✓ | ✓ | ✓ | ✓ |
| ML Inference | - | ✓✓ | ✓ | ✓ |
| High Concurrency | ✓✓ | - | ✓✓ | ✓ |
| Enterprise Integration | - | ✓ | ✓✓ | ✓✓ |
| Rapid Prototyping | ✓✓ | ✓✓ | - | ✓ |

✓✓ = Highly Recommended | ✓ = Supported | - = Not Recommended

---

---

## IX. Production-Tested Deployment Patterns (Nov 2025)

⚠️ **IMPORTANT - Project-Specific Values**:

The examples below use FAMLI project values (e.g., `fraudml.dev.att.com`, `Fml-EastUs2-Dev-AKS-Cluster`). **Your project will have different values**. Replace placeholders like `<YOUR_DOMAIN>`, `<YOUR_CLUSTER>`, etc. with your actual configuration.

Use `PROJECT-CONFIG.template` in the archetype to record your project-specific values:
```bash
cp PROJECT-CONFIG.template PROJECT-CONFIG.sh
# Fill in YOUR project values
source PROJECT-CONFIG.sh
```

### 9.1 Multi-Platform Docker Builds

**MANDATORY**: All images MUST be built for `linux/amd64` platform.

```bash
# Build script automatically includes:
docker build --platform linux/amd64 ...
```

**Rationale**: AKS runs Linux on AMD64 architecture. M1/M2 Mac builds default to arm64, causing "no match for platform in manifest" errors.

### 9.2 JFrog Artifact Registry Authentication

**AT&T Registry Configuration**:
- **Push Repository**: `artifact.it.att.com/apm0013448-dkr-gold/<service>` (no port)
- **Pull Repository**: `artifact.it.att.com:22609/apm0013448-dkr-group/<service>` (with port :22609)

**npm Authentication** (Node.js projects):
```bash
# Local setup (one-time)
TOKEN=$(cat ~/.docker/config.json | jq -r '.auths."https://artifact.it.att.com".auth')
cat > ~/.npmrc << EOF
//artifact.it.att.com/artifactory/api/npm/npm-virtual/:_auth=${TOKEN}
registry=https://artifact.it.att.com/artifactory/api/npm/npm-virtual/
EOF
```

**Dockerfile Integration**:
```dockerfile
# Use BuildKit secrets (NEVER embed tokens)
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci --only=production
```

**Build Command**:
```bash
DOCKER_BUILDKIT=1 docker build --secret id=npmrc,src=$HOME/.npmrc ...
```

### 9.2.1 CRITICAL: dkr-group Virtual Repository Configuration

**Problem Scenario:**
- Image pushed to `dkr-gold`: ✅ Success
- Kubernetes pulls from `dkr-group`: ❌ 401 Unauthorized
- Root Cause: `dkr-group` virtual repository not configured to include `dkr-gold`

**Error Message:**
```
Failed to pull image "artifact.it.att.com:22609/apm0013448-dkr-group/myapp:1.0.0"
failed to authorize: failed to fetch oauth token: 
unexpected status: 401
```

**Verification:**
```bash
# Test if group can see gold:
docker pull artifact.it.att.com:22609/apm0013448-dkr-group/python-sample-api:1.0.0

# If fails, test direct gold access:
docker pull artifact.it.att.com/apm0013448-dkr-gold/python-sample-api:1.0.0
```

**Fix Options:**

**Option A: Configure dkr-group to Include dkr-gold** (Recommended)
- Contact Artifactory administrator
- Request: Add `dkr-gold` to `dkr-group` virtual repository sources
- Maintains standard push-to-gold, pull-from-group workflow

**Option B: Pull Directly from dkr-gold** (Workaround)
```yaml
# In values.yaml:
image:
  repository: artifact.it.att.com/apm0013448-dkr-gold/myapp  # NO PORT
  tag: "1.0.0"
```

```bash
# Create secret WITHOUT port:
kubectl create secret docker-registry att-registry-secret \
  --docker-server=artifact.it.att.com \
  # NO PORT when using gold directly
  --docker-username=<user> \
  --docker-password=<token> \
  --namespace=<namespace>
```

**⚠️ CRITICAL:** Secret's `--docker-server` must EXACTLY match image repository URL:
- Using `dkr-group` with `:22609` → Secret needs `--docker-server=artifact.it.att.com:22609`
- Using `dkr-gold` without port → Secret needs `--docker-server=artifact.it.att.com`

### 9.3 Security Context Configuration

**CRITICAL**: Different user IDs based on base image.

**Backend Services (Node.js/Java/Python)**:
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1001
  fsGroup: 1001
```

**Frontend with nginx (Alpine nginx image)**:
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 101    # nginx user in Alpine
  fsGroup: 101
```

**nginx Dockerfile Requirements**:
```dockerfile
# Create cache directories BEFORE switching to non-root
RUN mkdir -p /var/cache/nginx/client_temp /var/cache/nginx/proxy_temp \
             /var/cache/nginx/fastcgi_temp /var/cache/nginx/uwsgi_temp \
             /var/cache/nginx/scgi_temp && \
    chown -R nginx:nginx /var/cache/nginx && \
    touch /var/run/nginx.pid /run/nginx.pid && \
    chown nginx:nginx /var/run/nginx.pid /run/nginx.pid

USER nginx
```

### 9.4 Context-Based Ingress Routing

**Pattern**: `/<app-name>-<service>(/|$)(.*)`

**Ingress Configuration**:
```yaml
ingress:
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
  hosts:
    - host: <YOUR_DOMAIN>  # Example: fraudml.dev.att.com (FAMLI), myapp.dev.att.com (Yours)
      paths:
        - path: /my-app-backend(/|$)(.*)
          pathType: ImplementationSpecific
          service: backend
        - path: /my-app-frontend(/|$)(.*)
          pathType: ImplementationSpecific
          service: frontend
```

**Frontend Configuration** (React/Vite):

**vite.config.js**:
```javascript
export default defineConfig({
  base: '/my-app-frontend/',  // MUST match ingress path
})
```

**Dockerfile**:
```dockerfile
ENV VITE_API_URL=/my-app-backend  # Backend context path
RUN npm run build
```

**Why**: Ingress rewrite removes context path. Frontend must be built with matching base path or assets will 404.

### 9.5 Kubernetes Image Pull Secret

**Create secret in target namespace**:
```bash
kubectl create secret docker-registry att-registry-secret \
  --docker-server=artifact.it.att.com:22609 \
  --docker-username=$(cat ~/.docker/config.json | jq -r '.auths."https://artifact.it.att.com".auth' | base64 -d | cut -d: -f1) \
  --docker-password=$(cat ~/.docker/config.json | jq -r '.auths."https://artifact.it.att.com".auth' | base64 -d | cut -d: -f2) \
  --namespace=<your-namespace>
```

**Reference in deployments**:
```yaml
spec:
  imagePullSecrets:
  - name: att-registry-secret
```

### 9.6 TLS Certificate Management

**Copy existing certificate to new namespace**:
```bash
# Replace with YOUR values:
# - TLS_SECRET_NAME: e.g., fraudml-dev-ingress-tls (FAMLI), myapp-dev-tls (Yours)
# - SOURCE_NAMESPACE: e.g., com-att-fraud-runtime (FAMLI), shared-certs (Yours)
# - APP_NAMESPACE: Your application namespace

kubectl get secret $TLS_SECRET_NAME -n $SOURCE_NAMESPACE -o yaml | \
  sed "s/namespace: $SOURCE_NAMESPACE/namespace: $APP_NAMESPACE/" | \
  kubectl apply -f -
```

**Reference in ingress**:
```yaml
tls:
  - secretName: <YOUR_TLS_SECRET>  # Example: fraudml-dev-ingress-tls (FAMLI)
    hosts:
      - <YOUR_DOMAIN>  # Example: fraudml.dev.att.com (FAMLI)
```

### 9.7 End-to-End Deployment Checklist

**Prerequisites (One-time)**:
- [ ] Configure `~/.docker/config.json` with JFrog token
- [ ] Configure `~/.npmrc` for Node.js projects
- [ ] Access to target AKS cluster

**Per Deployment**:
1. [ ] Update application code
2. [ ] Set context paths in vite.config.js (frontend)
3. [ ] Set VITE_API_URL in Dockerfile (frontend)
4. [ ] Build images: `./build-and-push.sh <version> apm0013448-dkr-gold`
5. [ ] Create namespace: `kubectl create namespace <name>`
6. [ ] Create image pull secret (see 9.5)
7. [ ] Copy TLS secret (see 9.6)
8. [ ] Update Helm values.yaml with correct:
   - Image repositories (with :22609 port for pull)
   - Image tags
   - Security contexts (101 for nginx, 1001 for others)
   - Ingress paths
9. [ ] Deploy: `helm upgrade --install <app> ./helm/<chart> -n <namespace>`
10. [ ] Verify: `kubectl get pods,svc,ingress -n <namespace>`

### 9.8 Common Issues & Solutions

| Issue | Symptom | Solution |
|-------|---------|----------|
| Platform mismatch | "no match for platform in manifest" | Build with `--platform linux/amd64` |
| Frontend 404s | Assets not loading | Set `base` in vite.config.js |
| nginx permissions | Permission denied on cache | Create dirs + chown before USER nginx |
| Image not found | ImagePullBackOff | Check repository name has :22609 port |
| TLS missing | Certificate errors | Copy secret from com-att-fraud-runtime |

### 9.9 Archetype Usage and Template Selection

**CRITICAL**: Only copy framework-specific templates. Do NOT copy all archetype files.

**❌ WRONG (copies everything, clutters project)**:
```bash
# This copies ALL framework Dockerfiles - DON'T DO THIS
cp -r .cdo-aifc/templates/05-infrastructure-devops/aks-microservice-deployment/* ./my-app/
```

**✅ CORRECT - Framework-Specific Copying**:

**Python Projects**:
```bash
cd my-app && mkdir -p api
cp .cdo-aifc/templates/.../Dockerfile.python api/Dockerfile
cp .cdo-aifc/templates/.../scripts/build-and-push.sh .
cp .cdo-aifc/templates/.../PROJECT-CONFIG.template .
cp .cdo-aifc/templates/.../.gitignore .
```

**Node.js Projects**:
```bash
cd my-app && mkdir -p api
cp .cdo-aifc/templates/.../Dockerfile.nodejs api/Dockerfile
cp .cdo-aifc/templates/.../scripts/build-and-push.sh .
# + common files (PROJECT-CONFIG.template, .gitignore)
```

**React/Vue Frontends**:
```bash
cd my-app && mkdir -p frontend
cp .cdo-aifc/templates/.../Dockerfile.react-nginx frontend/Dockerfile
cp .cdo-aifc/templates/.../examples/nginx.conf frontend/
cp .cdo-aifc/templates/.../examples/vite.config.js frontend/
cp .cdo-aifc/templates/.../scripts/build-and-push.sh .
# + common files
```

**Full-Stack (Node.js + React)**:
```bash
cd my-app
mkdir -p backend frontend

# Backend
cp .cdo-aifc/templates/.../Dockerfile.nodejs backend/Dockerfile

# Frontend
cp .cdo-aifc/templates/.../Dockerfile.react-nginx frontend/Dockerfile
cp .cdo-aifc/templates/.../examples/nginx.conf frontend/
cp .cdo-aifc/templates/.../examples/vite.config.js frontend/

# Common
cp .cdo-aifc/templates/.../scripts/build-and-push.sh .
cp .cdo-aifc/templates/.../PROJECT-CONFIG.template .
```

**Files NOT Needed by Framework**:

| Your Framework | Don't Copy These |
|---------------|------------------|
| Python only | Dockerfile.nodejs, .java, .dotnet, .react-nginx, nginx.conf, vite.config.js |
| Node.js only | Dockerfile.python, .java, .dotnet, .react-nginx (unless frontend) |
| React only | Dockerfile.python, .nodejs, .java, .dotnet (unless backend) |
| Java only | Dockerfile.python, .nodejs, .dotnet, .react-nginx, nginx.conf |

**Reference Documentation**:
- `PRE-DEPLOYMENT-CHECKLIST.md` - **START HERE FIRST** - Prerequisites validation (Step 0: Access verification)
- `docs/TROUBLESHOOTING.md` - **ERROR PREVENTION** - Comprehensive guide for ImagePullBackOff, SSL errors, repository issues
- `FRAMEWORK-GUIDE.md` - Framework-specific copy instructions (Python, Node.js, React, Java)
- `GETTING-STARTED.md` - Quick start with selective copying
- `docs/DEPLOYMENT-GUIDE.md` - Complete deployment guide (includes critical repository URL rules)
- `docs/QUICK-START.md` - One-page reference
- `PROJECT-CONFIG.template` - **CRITICAL** - Repository URL rules (push without port, pull with :22609)
- `examples/` - Production-tested configurations (copy only what you need)

### 9.10 Validation Checklist

Before considering deployment complete:
- [ ] All pods show `Running` status
- [ ] Health checks passing (liveness & readiness)
- [ ] Ingress shows ADDRESS assigned
- [ ] Frontend assets load from correct path
- [ ] API calls reach backend service
- [ ] TLS/HTTPS working
- [ ] HPA configured and functional
- [ ] Logs accessible via kubectl logs
- [ ] Metrics visible in monitoring

**Validation Commands**:
```bash
# Replace <namespace>, <app>, <host> with YOUR values
kubectl get pods -n <namespace>
kubectl get ingress -n <namespace>
kubectl logs -f deployment/<app>-backend -n <namespace>
curl -k https://<host>/<app>-backend/health

# Example (FAMLI):
# kubectl get pods -n com-att-fraud-runtime
# curl -k https://fraudml.dev.att.com/hello-world-backend/health
```

---

## X. Critical Documentation References

### Error Prevention & Troubleshooting
- **docs/TROUBLESHOOTING.md** - Start here when experiencing errors
  - ImagePullBackOff (repository URL issues, missing port :22609)
  - SSL Certificate failures (corporate network workarounds)
  - BuildKit secret errors
  - Helm lock conflicts
  - Kubernetes secret mismatches
  - Quick reference commands and debugging checklist

### Pre-Deployment
- **TOOLS-INSTALLATION-GUIDE.md** - **INSTALL TOOLS FIRST** - All required tools with platform-specific instructions
  - Docker Desktop (macOS, Windows, Linux links)
  - Azure CLI, kubectl, Helm, kubelogin, jq, kubectx
  - Quick install commands for each platform
  - Post-installation configuration steps
  
- **PRE-DEPLOYMENT-CHECKLIST.md** - Complete before any deployment
  - Step 0: Access verification (AKS & Artifactory)
  - Tool installation verification (Docker, Azure CLI, kubectl, Helm, kubelogin, jq)
  - Repository configuration (push vs pull URLs)
  - Namespace and TLS setup
  - Automated preflight check script

### Configuration
- **PROJECT-CONFIG.template** - Project-specific values
  - **CRITICAL**: Repository URL rules (push without port, pull with :22609)
  - Cluster context, namespace, ingress settings
  - Validation output and examples

### Deployment Guides
- **docs/DEPLOYMENT-GUIDE.md** - Complete deployment walkthrough
  - Critical repository URL rules at beginning
  - Step-by-step with commands
  - Framework-specific patterns
  - Troubleshooting section

- **docs/QUICK-START.md** - One-page quick reference
  - Copy-paste commands
  - Common patterns and gotchas

### Framework-Specific
- **FRAMEWORK-GUIDE.md** - What to copy for each framework
  - Python: SSL certificate workarounds, repository URLs
  - Node.js: npm authentication patterns
  - React: Context path configuration
  - Java: Multi-stage build patterns
  - Selective copying to avoid clutter

### Templates & Examples
- **Dockerfile.python** - Includes `--trusted-host` flags by default
- **Dockerfile.nodejs** - npm authentication patterns
- **Dockerfile.react-nginx** - Frontend with context paths
- **examples/nginx.conf** - Production-ready SPA configuration
- **examples/vite.config.js** - Context-based routing

### Workflow Documentation
- **GETTING-STARTED.md** - Quick start with selective copying
- **ARCHETYPE-UPDATES.md** - Change log and migration guide
- **CHANGELOG.md** - Detailed history of updates

---

## XI. Documentation Structure & Purpose

**The archetype maintains 11 focused documents with NO redundancy. Each serves a unique purpose.**

### Root Level Documentation (7 files)

#### 1. README.md - Navigation Hub ⭐
**Purpose**: Entry point to all documentation  
**Use When**: First time using archetype, need overview, looking for specific guide  
**Contains**: Overview, prerequisites summary, troubleshooting links, navigation to all guides

#### 2. PRE-DEPLOYMENT-CHECKLIST.md - Interactive Validation 📋
**Purpose**: Step-by-step prerequisites validation with checkboxes  
**Use When**: Before any deployment, validating environment setup  
**Contains**: Step 0 (access verification), tool installation checks, configuration validation, kubectl context setup

#### 3. TOOLS-INSTALLATION-GUIDE.md - Tool Reference 🛠️
**Purpose**: Complete tool installation for all platforms  
**Use When**: Missing tools, setting up new machine, helping team members  
**Contains**: Docker Desktop, Azure CLI, kubectl, Helm, kubelogin, jq, kubectx - all with macOS/Windows/Linux instructions

#### 4. FRAMEWORK-GUIDE.md - Selective Copying 🎯
**Purpose**: Framework-specific file selection  
**Use When**: Copying archetype templates to avoid clutter  
**Contains**: What to copy for Python, Node.js, React, Java - what NOT to copy, SSL workarounds, repository notes

#### 5. GETTING-STARTED.md - Fast Deployment 🚀
**Purpose**: Deploy in 5 minutes  
**Use When**: Quick deployment, already have prerequisites  
**Contains**: Configuration template, build commands, Helm deployment

#### 6. CHANGELOG.md - Version History 📝
**Purpose**: Track all changes over time  
**Use When**: Understanding what changed, checking breaking changes  
**Contains**: Chronological list of all updates, dates, descriptions

#### 7. ARCHETYPE-UPDATES.md - Recent Changes 🆕
**Purpose**: Summary of latest improvements  
**Use When**: Checking what's new, migration from old version  
**Contains**: Recent validation, new features, patterns documented

### docs/ Subdirectory (4 files)

#### 8. docs/DEPLOYMENT-GUIDE.md - Comprehensive Walkthrough 📖
**Purpose**: Complete end-to-end deployment guide  
**Use When**: First deployment, need detailed instructions, teaching others  
**Contains**: Repository URL rules, prerequisites, Docker building, Kubernetes deployment, troubleshooting

#### 9. docs/QUICK-START.md - Cheat Sheet ⚡
**Purpose**: One-page command reference  
**Use When**: Quick lookup, copy-paste commands, experienced users  
**Contains**: Common commands, gotchas, quick patterns

#### 10. docs/TROUBLESHOOTING.md - Error Resolution 🔧
**Purpose**: Fix common deployment errors  
**Use When**: Experiencing errors, debugging issues  
**Contains**: ImagePullBackOff fixes, SSL issues, repository problems, debugging checklist, quick reference commands

#### 11. docs/ATT-ARTIFACT-REGISTRY-SETUP.md - Registry Authentication 🔐
**Purpose**: Detailed registry authentication setup  
**Use When**: Setting up Docker/npm/Maven registry access  
**Contains**: Token generation, Docker config, npm registry, Maven settings

### Deleted Files (Redundant)

The following files were **removed** during consolidation as they duplicated content:
- ~~docs/SETUP.md~~ → Content moved to TOOLS-INSTALLATION-GUIDE.md and PRE-DEPLOYMENT-CHECKLIST.md
- ~~docs/USAGE.md~~ → Content covered by README.md, GETTING-STARTED.md, and DEPLOYMENT-GUIDE.md
- ~~docs/REGISTRY-CONFIGURATION.md~~ → Content fully covered by ATT-ARTIFACT-REGISTRY-SETUP.md

### Documentation Decision Tree

```
Question: What do I need?

├─ "I'm brand new, where do I start?"
│  └─ README.md → PRE-DEPLOYMENT-CHECKLIST.md → GETTING-STARTED.md
│
├─ "I need to install tools"
│  └─ TOOLS-INSTALLATION-GUIDE.md
│
├─ "What files do I copy for [Python/Node/etc]?"
│  └─ FRAMEWORK-GUIDE.md
│
├─ "I need detailed deployment steps"
│  └─ docs/DEPLOYMENT-GUIDE.md
│
├─ "I'm getting an error"
│  └─ docs/TROUBLESHOOTING.md
│
├─ "How do I authenticate with registry?"
│  └─ docs/ATT-ARTIFACT-REGISTRY-SETUP.md
│
├─ "I need quick command reference"
│  └─ docs/QUICK-START.md
│
└─ "What changed recently?"
   └─ ARCHETYPE-UPDATES.md or CHANGELOG.md
```

### Documentation Maintenance Rules

1. **NO Duplication**: Each concept appears in exactly ONE primary document
2. **Cross-Reference**: Use links when referencing concepts in other docs
3. **Clear Purpose**: Each doc has a single, well-defined purpose
4. **User Journey**: Docs flow logically for different user types
5. **Keep Updated**: When updating one doc, check cross-references

---

**Version**: 3.0.0  
**Last Updated**: 2025-11-05  
**Maintainer**: Platform Reliability Engineering  
**Validated With**: 
- FAMLI hello-world-aks (Node.js + React) on Fml-EastUs2-Dev-AKS-Cluster
- python-hello-aks (Python FastAPI) - Error recovery documented
**Parent Archetypes**: microservice-cicd-architect, aks-devops-deployment
