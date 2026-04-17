---
description: Generate backend-only API service with FastAPI, Poetry, Docker, Helm, and Azure DevOps CI/CD (Backend Only)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype backend-only --json` and parse for PYTHON_VERSION, POETRY_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.

### 3. Parse Input
Extract from $ARGUMENTS: 
- Project name and app acronym
- API type (REST/GraphQL/gRPC)
- Database requirement (PostgreSQL/Redis/None)
- Authentication (Entra ID/JWT/None)
- Background workers needed (Celery/None)
- Scheduled jobs/cronjobs needed
- Deployment target (AKS/Azure App Service)
- Monorepo structure (single module vs multiple modules)

Request clarification if incomplete.

### 4. Validate Constraints
Check against hard-stop rules:
- ✘ Refuse if secrets would be hardcoded
- ✘ Refuse if JFrog token not using Azure DevOps variable groups
- ✘ Refuse if not using cookiecutter template structure
- ✘ Refuse if resources not restricted to AT&T proxy CIDRs
- ✘ Refuse if private endpoints not configured
- ✘ Refuse if Istio sidecar not enabled for AKS deployment
- ✘ Refuse if workload identity not configured for Key Vault access

If violated, explain clearly and suggest compliant alternative.

### 5. Generate Project Structure

Create monorepo backend service following AT&T DevOps cookiecutter standards:

```
{project_name}/
├── api/                           # API module
│   ├── src/{package_prefix}_api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── settings.py
│   │   └── routers/
│   ├── test/
│   ├── docker/
│   │   └── start_server.sh
│   ├── Dockerfile
│   ├── pipeline.yaml
│   ├── pyproject.toml
│   └── README.md
├── worker/                        # Worker module (if needed)
│   ├── src/{package_prefix}_worker/
│   ├── test/
│   ├── Dockerfile
│   ├── pipeline.yaml
│   ├── pyproject.toml
│   └── README.md
├── jobs/                          # Jobs module (if needed)
│   ├── src/{package_prefix}_jobs/
│   ├── test/
│   ├── Dockerfile
│   ├── pipeline.yaml
│   ├── pyproject.toml
│   └── README.md
├── shared/                        # Shared package (CRITICAL)
│   ├── src/{package_prefix}_shared/
│   │   ├── __init__.py
│   │   ├── models/              # Database models
│   │   ├── schemas/             # Pydantic schemas
│   │   └── utils/               # Shared utilities
│   ├── test/
│   ├── alembic/                 # Database migrations
│   ├── alembic.ini
│   ├── pipeline.yaml
│   ├── pyproject.toml
│   └── README.md
├── helm/{app_name}/              # Helm charts
│   ├── templates/
│   │   ├── api/
│   │   ├── worker/
│   │   ├── jobs/
│   │   └── common/
│   ├── values/
│   │   ├── nprdValues.yaml
│   │   ├── stageValues.yaml
│   │   └── prodValues.yaml
│   ├── Chart.yaml
│   └── values.yaml
├── .gitignore
└── README.md
```

### 6. Generate Shared Module

Create `shared/pyproject.toml`:
```toml
[tool.poetry]
name = "{package_prefix}_shared"
version = "0.1.0"
description = "Shared package for {project_name}"
packages = [
    { include = "{package_prefix}_shared", from = "src"}
]

[tool.poetry.dependencies]
python = ">=3.11,<3.13"
sqlalchemy = {extras = ["asyncio"], version = "^2.0.21"}
asyncpg = {version = "^0.29.0", optional = true}
psycopg2-binary = {version = "^2.9.9", optional = true}
alembic = "^1.12.0"
pydantic = "^2.9.0"

[tool.poetry.extras]
asyncpg = ["asyncpg"]
psycopg2 = ["psycopg2-binary"]

[[tool.poetry.source]]
name = "aaa-pypi-proxy"
url = "https://artifact.it.att.com/artifactory/api/pypi/apm0013367-pyp-group/simple/"
priority = "primary"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### 7. Generate FastAPI Application

Create `api/src/{package_prefix}_api/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from .settings import settings
from .routers import health

app = FastAPI(
    title="{project_name} API",
    root_path=settings.API_ROOT_PATH
)

# Configure OpenTelemetry
if settings.INSIGHTS_CONNECTION_STRING:
    configure_azure_monitor(connection_string=settings.INSIGHTS_CONNECTION_STRING)
    FastAPIInstrumentor.instrument_app(app)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/monitor", tags=["monitoring"])

@app.get("/")
async def root():
    return {"message": "Welcome to {project_name} API"}
```

Create `api/src/{package_prefix}_api/settings.py`:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_PORT: int = 8100
    API_ROOT_PATH: str = "/{package_prefix}/api"
    NUM_API_WORKERS: int = 3
    
    # Database
    POSTGRESQL_CONNECTION_STRING: str | None = None
    
    # Redis
    REDIS_HOST: str | None = None
    REDIS_PORT: int = 6380
    REDIS_USE_SSL: bool = True
    REDIS_PASSWORD: str | None = None
    
    # Auth
    CLIENT_ID: str | None = None
    
    # Observability
    INSIGHTS_CONNECTION_STRING: str | None = None
    TRACER_NAME: str = "{package_prefix}-api"
    
    class Config:
        env_prefix = "{APP_ACRONYM}_"
        case_sensitive = False

settings = Settings()
```

Create `api/src/{package_prefix}_api/routers/health.py`:
```python
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/liveness")
async def liveness():
    return {"status": "alive"}

@router.get("/readiness")
async def readiness():
    # Add checks for database, redis, etc.
    checks = {
        "api": True,
    }
    
    if all(checks.values()):
        return {"status": "ready", "checks": checks}
    else:
        raise HTTPException(status_code=503, detail=checks)
```

Create `api/docker/start_server.sh`:
```bash
#!/bin/bash
set -e

echo "Starting {project_name} API..."
echo "Port: ${APP_ACRONYM}_API_PORT"
echo "Workers: ${APP_ACRONYM}_NUM_API_WORKERS"

exec poetry run gunicorn {package_prefix}_api.main:app \
    --workers ${APP_ACRONYM}_NUM_API_WORKERS \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:${APP_ACRONYM}_API_PORT \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
```

### 8. Generate API Poetry Configuration

Create `api/pyproject.toml`:
```toml
[tool.poetry]
name = "{package_prefix}_api"
version = "0.1.0"
description = "REST API Package for {project_name}"
license = "Copyright AT&T. All Rights Reserved."
authors = ["Ask AT&T Analytics Team <askatt-prodsupt@list.att.com>"]
readme = "README.md"
packages = [
    { include = "{package_prefix}_api", from = "src"}
]

[tool.poetry.dependencies]
python = ">=3.11,<3.13"
{package_prefix}_shared = { path = "../shared/", develop = true, extras = ["asyncpg"]}

uvicorn = "^0.28.0"
fastapi = "^0.110.0"
msal = "^1.26.0"
orjson = "^3.9.10"
gunicorn = "^21.2.0"
azure-monitor-opentelemetry = "^1.0.0b16"
pydantic-settings = "^2.2.1"
aaa-common = {version = "^0.1.38145", source = "aaa-py-stage"}
opentelemetry-instrumentation-fastapi = "^0.49b1"
fastapi-azure-auth = "^5.0"
redis = {extras = ["hiredis"], version = "^5.0.1", optional = true}

[tool.poetry.group.dev.dependencies]
jupyter = "^1.0.0"

[tool.poetry.group.test.dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.1"
pytest-cov = "^4.1.0"
httpx = "^0.27.0"
pytest-azurepipelines = "^1.0.5"
pytest-mock = "^3.14.0"

[[tool.poetry.source]]
name = "aaa-pypi-proxy"
url = "https://artifact.it.att.com/artifactory/api/pypi/apm0013367-pyp-group/simple/"
priority = "primary"

[[tool.poetry.source]]
name = "aaa-py-stage"
url = "https://artifact.it.att.com/artifactory/api/pypi/apm0013367-pyp-stage/simple/"
priority = "explicit"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### 9. Generate Multi-Stage Dockerfile

Create `api/Dockerfile`:
```dockerfile
FROM cerebroacr.azurecr.io/aaa/python-poetry:3.11 AS builder
ARG JFROG_USER
ARG JFROG_KEY

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /{package_prefix}

# Copy shared module first
COPY shared/pyproject.toml shared/poetry.lock shared/README.md ./shared/
COPY shared/src/ ./shared/src/

# Copy API module
COPY api/pyproject.toml api/poetry.lock api/README.md api/docker/start_server.sh ./api/
COPY api/src ./api/src

WORKDIR /{package_prefix}/api

# Single RUN layer for JFrog auth, install, and cleanup
RUN env && \
    python -m poetry config http-basic.aaa-pypi-proxy $JFROG_USER $JFROG_KEY --local && \
    python -m poetry config http-basic.aaa-py-stage $JFROG_USER $JFROG_KEY --local && \
    python -m poetry install --all-extras --only main && \
    python -m poetry config http-basic.aaa-pypi-proxy --unset && \
    python -m poetry config http-basic.aaa-py-stage --unset

# Runtime stage
FROM cerebroacr.azurecr.io/aaa/python-poetry:3.11-slim

COPY --from=builder /{package_prefix} /{package_prefix}

WORKDIR /{package_prefix}/api

# Create non-root user and group
RUN groupadd -r appgroup && useradd -r -g appgroup -u 1000 appuser
RUN chown -R appuser:appgroup /{package_prefix}
USER appuser

ARG API_PORT=8100
ENV {APP_ACRONYM}_API_PORT=$API_PORT

ARG NUM_API_WORKERS=3
ENV {APP_ACRONYM}_NUM_API_WORKERS=$NUM_API_WORKERS

CMD ["/bin/bash", "./start_server.sh"]
```

### 10. Generate Azure DevOps Pipeline

Create `api/pipeline.yaml`:
```yaml
jobs:
  - job: Unit_Test
    displayName: "Run Unit Tests"
    container: python
    variables:
      HTTP_PROXY: 'http://proxy.conexus.svc.local:3128'
      HTTPS_PROXY: 'http://proxy.conexus.svc.local:3128'
    steps:
      - script: |
          cd api
          python -m poetry config http-basic.aaa-pypi-proxy "$(jfrog-mechid)@att.com" "$(jfrog-token)" --local
          python -m poetry config http-basic.aaa-py-stage "$(jfrog-mechid)@att.com" "$(jfrog-token)" --local
          python -m poetry config repositories.aaa-py-stage https://artifact.it.att.com/artifactory/api/pypi/apm0013367-pyp-stage/
        displayName: "JFrog Authentication."
      
      - script: |
          cd api
          python -m poetry install -v --only main,test
        displayName: 'Install package with test dependencies.'
      
      - script: |
          cd api
          python -m poetry run pytest --test-run-title="{project_name} API" --cov=. --cov-report=html --cov-report=xml:api-coverage.xml --no-coverage-upload
          exit_code=$?
          if [ $exit_code -eq 0 ]; then
            echo "##vso[task.setvariable variable=TestsPassed;isOutput=true]true"
          else
            echo "##vso[task.setvariable variable=TestsPassed;isOutput=true]false"
          fi
          exit $exit_code
        displayName: 'Run unit tests.'
      
      - script: |
          cd api
          sed --debug -i "s|$(pwd)|./api|g" api-coverage.xml
        name: UpdatePaths
        displayName: 'Replace absolute paths'
      
      - publish: $(System.DefaultWorkingDirectory)/api/api-coverage.xml
        artifact: APICoverage
        displayName: "Publish Coverage Report"
      
      - script: |
          if [ $(RunTests.TestsPassed) != 'true' ]; then
            echo "Unit tests failed. Marking job as failed."
            exit 1
          fi
        displayName: "Check Test Results and Fail if Tests Failed"
      
      - script: |
          cd api
          python -m poetry config http-basic.aaa-pypi-proxy --unset
          python -m poetry config http-basic.aaa-py-stage --unset
        displayName: "Clear Authentication."
        condition: always()

  - job: Build_Container
    displayName: "Build Container"
    dependsOn: Unit_Test
    steps:
      - task: Docker@2
        displayName: "Build Docker Image"
        inputs:
          command: 'build'
          Dockerfile: 'api/Dockerfile'
          buildContext: '.'
          containerRegistry: 'cerebroacr-service-connection'
          repository: 'aaa/{package_prefix}-api'
          arguments: |
            --build-arg HTTP_PROXY=http://proxy.conexus.svc.local:3128
            --build-arg HTTPS_PROXY=http://proxy.conexus.svc.local:3128
            --build-arg JFROG_USER=$(jfrog-mechid)@att.com
            --build-arg JFROG_KEY=$(jfrog-token)
          tags: |
            0.1.0-$(Build.BuildId)
            latest
      
      - task: Docker@2
        displayName: "Push to cerebroacr"
        inputs:
          command: 'push'
          containerRegistry: 'cerebroacr-service-connection'
          repository: 'aaa/{package_prefix}-api'
          tags: |
            0.1.0-$(Build.BuildId)
            latest
```

### 11. Generate Helm Charts

Create `helm/{app_name}/values.yaml`:
```yaml
ingress:
  className: ingress-nginx
  hosts:
    - label: "aaa"
      hostname: aaa.dev.att.com
    - label: "askatt-analytics"
      hostname: askatt-analytics.dev.att.com

image:
  version:

auth:
  aad:
    clientId:
  appInsights:
    key: "InstrumentationKey=..."

keyVault:
  name:
  resourceGroup:
  subscriptionId:
  tenantId: e741d71c-c6b6-47b0-803c-0f3b32b07556

workload:
  serviceAccountName: workload-identity-sa
  clientId:

api:
  replicas: 1
  image:
    name: cerebroacr.azurecr.io/aaa/{package_prefix}-api
  port: 8100
  root_path: /{package_prefix}/api
  num_workers: 3

worker:
  replicas: 1
  image:
    name: cerebroacr.azurecr.io/aaa/{package_prefix}-worker

jobs:
  image:
    name: cerebroacr.azurecr.io/aaa/{package_prefix}-jobs

common:
  redis:
    host:
    port: 6380
    useSsl: "True"
```

Create `helm/{app_name}/templates/api/deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {package_prefix}-api
spec:
  replicas: {{{{.Values.api.replicas}}}}
  selector:
    matchLabels:
      app: {package_prefix}-api
  template:
    metadata:
      labels:
        app: {package_prefix}-api
        azure.workload.identity/use: "true"
    spec:
      serviceAccountName: "{{{{ .Values.workload.serviceAccountName }}}}"
      containers:
        - name: {package_prefix}-api
          image: "{{{{.Values.api.image.name}}}}:{{{{.Values.image.version}}}}"
          resources:
            requests:
              cpu: 500m
              memory: "256Mi"
            limits:
              cpu: 1000m
              memory: "1Gi"
          env:
            - name: {APP_ACRONYM}_API_PORT
              value: "{{{{.Values.api.port}}}}"
            - name: {APP_ACRONYM}_API_ROOT_PATH
              value: {{{{.Values.api.root_path}}}}
            - name: {APP_ACRONYM}_NUM_API_WORKERS
              value: "{{{{.Values.api.num_workers}}}}"
            - name: {APP_ACRONYM}_CLIENT_ID
              value: {{{{.Values.auth.aad.clientId}}}}
            - name: {APP_ACRONYM}_POSTGRESQL_CONNECTION_STRING
              valueFrom:
                secretKeyRef:
                  name: {package_prefix}-common-secrets
                  key: pg-async-uri
            - name: {APP_ACRONYM}_REDIS_HOST
              value: {{{{ .Values.common.redis.host }}}}
            - name: {APP_ACRONYM}_REDIS_PORT
              value: "{{{{ .Values.common.redis.port }}}}"
            - name: {APP_ACRONYM}_REDIS_USE_SSL
              value: "{{{{ .Values.common.redis.useSsl }}}}"
            - name: {APP_ACRONYM}_REDIS_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: {package_prefix}-common-secrets
                  key: redis-password
            - name: {APP_ACRONYM}_INSIGHTS_CONNECTION_STRING
              value: {{{{ .Values.auth.appInsights.key }}}}
            - name: OTEL_RESOURCE_ATTRIBUTES
              value: "service.namespace={package_prefix},service.instance.id={package_prefix}-api"
            - name: OTEL_SERVICE_NAME
              value: "{package_prefix}-api"
          startupProbe:
            httpGet:
              path: /monitor/liveness
              port: {{{{.Values.api.port}}}}
            failureThreshold: 30
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /monitor/liveness
              port: {{{{.Values.api.port}}}}
            failureThreshold: 3
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /monitor/readiness
              port: {{{{.Values.api.port}}}}
            failureThreshold: 1
            periodSeconds: 15
          volumeMounts:
            - name: {package_prefix}-common-secrets
              mountPath: /mnt/secrets-store
              readOnly: true
      volumes:
        - name: {package_prefix}-common-secrets
          csi:
            driver: secrets-store.csi.k8s.io
            readOnly: true
            volumeAttributes:
              secretProviderClass: {package_prefix}-common-kv
```

Create `helm/{app_name}/templates/api/service.yaml`:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {package_prefix}-api-svc
spec:
  type: ClusterIP
  ports:
    - port: {{{{.Values.api.port}}}}
      targetPort: {{{{.Values.api.port}}}}
      protocol: TCP
  selector:
    app: {package_prefix}-api
```

Create `helm/{app_name}/templates/api/ingress.yaml`:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {package_prefix}-api-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  ingressClassName: {{{{.Values.ingress.className}}}}
  rules:
  {{{{- range .Values.ingress.hosts}}}}
    - host: {{{{.hostname}}}}
      http:
        paths:
          - path: /{package_prefix}/api(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: {package_prefix}-api-svc
                port:
                  number: {{{{$.Values.api.port}}}}
  {{{{- end}}}}
```

Create `helm/{app_name}/templates/api/virtual_service.yaml`:
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: {package_prefix}-api-vs
spec:
  hosts:
  {{{{- range .Values.ingress.hosts}}}}
    - {{{{.hostname}}}}
  {{{{- end}}}}
  gateways:
    - istio-ingress/istio-gateway
  http:
    - match:
        - uri:
            prefix: "/{package_prefix}/api"
      rewrite:
        uri: "/"
      route:
        - destination:
            host: {package_prefix}-api-svc
            port:
              number: {{{{.Values.api.port}}}}
```

Create `helm/{app_name}/templates/common/key_vault.yaml`:
```yaml
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: {package_prefix}-common-kv
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade
    "helm.sh/hook-weight": "0"
spec:
  provider: azure
  parameters:
    usePodIdentity: "false"
    keyvaultName: {{{{ required "A valid keyVault.name entry required!" .Values.keyVault.name }}}}
    resourceGroup: {{{{ required "A valid keyVault.resourceGroup entry required!" .Values.keyVault.resourceGroup }}}}
    subscriptionId: {{{{ required "A valid keyVault.subscriptionId entry required!" .Values.keyVault.subscriptionId }}}}
    tenantId: {{{{ required "A valid keyVault.tenantId entry required!" .Values.keyVault.tenantId }}}}
    clientID:
    objects: |
      array:
        - |
          objectName: redis-password
          objectType: secret
        - |
          objectName: pg-async-uri
          objectType: secret
        - |
          objectName: pg-sync-uri
          objectType: secret
  secretObjects:
  - secretName: {package_prefix}-common-secrets
    type: Opaque
    data:
      - objectName: redis-password
        key: redis-password
      - objectName: pg-async-uri
        key: pg-async-uri
      - objectName: pg-sync-uri
        key: pg-sync-uri
```

### 12. Generate Background Worker Module (If Needed)

Create `worker/Dockerfile` (similar to API but without start_server.sh):
```dockerfile
FROM cerebroacr.azurecr.io/aaa/python-poetry:3.11 AS builder
ARG JFROG_USER
ARG JFROG_KEY

ENV POETRY_VIRTUALENVS_IN_PROJECT=true
WORKDIR /{package_prefix}

COPY shared/pyproject.toml shared/poetry.lock shared/README.md ./shared/
COPY shared/src/ ./shared/src/

COPY worker/pyproject.toml worker/poetry.lock worker/README.md ./worker/
COPY worker/src ./worker/src

WORKDIR /{package_prefix}/worker

RUN env && \
    python -m poetry config http-basic.aaa-pypi-proxy $JFROG_USER $JFROG_KEY --local && \
    python -m poetry config http-basic.aaa-py-stage $JFROG_USER $JFROG_KEY --local && \
    python -m poetry install --all-extras --only main && \
    python -m poetry config http-basic.aaa-pypi-proxy --unset && \
    python -m poetry config http-basic.aaa-py-stage --unset

FROM cerebroacr.azurecr.io/aaa/python-poetry:3.11-slim

COPY --from=builder /{package_prefix} /{package_prefix}
WORKDIR /{package_prefix}/worker

RUN groupadd -r appgroup && useradd -r -g appgroup -u 1000 appuser
RUN chown -R appuser:appgroup /{package_prefix}
USER appuser

CMD ["poetry", "run", "celery", "-A", "{package_prefix}_worker.celery_app", "worker", "--loglevel=info"]
```

Create `helm/{app_name}/templates/worker/deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {package_prefix}-worker
spec:
  replicas: {{{{.Values.worker.replicas}}}}
  selector:
    matchLabels:
      app: {package_prefix}-worker
  template:
    metadata:
      labels:
        app: {package_prefix}-worker
        azure.workload.identity/use: "true"
    spec:
      serviceAccountName: "{{{{ .Values.workload.serviceAccountName }}}}"
      containers:
        - name: {package_prefix}-worker
          image: "{{{{.Values.worker.image.name}}}}:{{{{.Values.image.version}}}}"
          resources:
            requests:
              cpu: 500m
              memory: "512Mi"
            limits:
              cpu: 1000m
              memory: "2Gi"
          env:
            - name: {APP_ACRONYM}_REDIS_HOST
              value: {{{{ .Values.common.redis.host }}}}
            - name: {APP_ACRONYM}_REDIS_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: {package_prefix}-common-secrets
                  key: redis-password
          volumeMounts:
            - name: {package_prefix}-common-secrets
              mountPath: /mnt/secrets-store
              readOnly: true
      volumes:
        - name: {package_prefix}-common-secrets
          csi:
            driver: secrets-store.csi.k8s.io
            readOnly: true
            volumeAttributes:
              secretProviderClass: {package_prefix}-common-kv
```

### 13. Generate Scheduled Jobs Module (If Needed)

Create `jobs/Dockerfile`:
```dockerfile
FROM cerebroacr.azurecr.io/aaa/python-poetry:3.11 AS builder
ARG JFROG_USER
ARG JFROG_KEY

ENV POETRY_VIRTUALENVS_IN_PROJECT=true
WORKDIR /{package_prefix}

COPY shared/pyproject.toml shared/poetry.lock shared/README.md ./shared/
COPY shared/src/ ./shared/src/

COPY jobs/pyproject.toml jobs/poetry.lock jobs/README.md ./jobs/
COPY jobs/src ./jobs/src

WORKDIR /{package_prefix}/jobs

RUN env && \
    python -m poetry config http-basic.aaa-pypi-proxy $JFROG_USER $JFROG_KEY --local && \
    python -m poetry config http-basic.aaa-py-stage $JFROG_USER $JFROG_KEY --local && \
    python -m poetry install --all-extras --only main && \
    python -m poetry config http-basic.aaa-pypi-proxy --unset && \
    python -m poetry config http-basic.aaa-py-stage --unset

FROM cerebroacr.azurecr.io/aaa/python-poetry:3.11

COPY --from=builder /{package_prefix} /{package_prefix}
WORKDIR /{package_prefix}/jobs

RUN groupadd -r appgroup && useradd -r -g appgroup -u 1000 appuser
RUN chown -R appuser:appgroup /{package_prefix}
USER appuser

CMD ["poetry", "run", "python", "-m", "{package_prefix}_jobs.main"]
```

Create `helm/{app_name}/templates/jobs/cronjob.yaml`:
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: {package_prefix}-cronjob
spec:
  schedule: "0 3 * * *"  # Daily at 3 AM
  jobTemplate:
    spec:
      template:
        metadata:
          labels:
            azure.workload.identity/use: "true"
        spec:
          serviceAccountName: "{{{{ .Values.workload.serviceAccountName }}}}"
          restartPolicy: Never
          containers:
            - name: {package_prefix}-job
              image: "{{{{ .Values.jobs.image.name}}}}:{{{{ .Values.image.version}}}}"
              command: ["/bin/bash", "-c"]
              args:
                - |
                  echo "Waiting for Istio sidecar to be ready..."
                  trap "curl --max-time 2 -s -f -XPOST http://127.0.0.1:15020/quitquitquit" EXIT
                  while ! curl -s -f http://127.0.0.1:15020/healthz/ready; do sleep 1; done
                  echo "Ready!"
                  poetry run python -m {package_prefix}_jobs.main
              env:
                - name: {APP_ACRONYM}_INSIGHTS_CONNECTION_STRING
                  value: {{{{ .Values.auth.appInsights.key }}}}
                - name: {APP_ACRONYM}_POSTGRESQL_CONNECTION_STRING
                  valueFrom:
                    secretKeyRef:
                      name: {package_prefix}-common-secrets
                      key: pg-sync-uri
                - name: OTEL_RESOURCE_ATTRIBUTES
                  value: "service.namespace={package_prefix},service.instance.id={package_prefix}-jobs"
                - name: OTEL_SERVICE_NAME
                  value: "{package_prefix}-jobs"
              volumeMounts:
                - name: {package_prefix}-common-secrets
                  mountPath: /mnt/secrets-store
                  readOnly: true
          volumes:
            - name: {package_prefix}-common-secrets
              csi:
                driver: secrets-store.csi.k8s.io
                readOnly: true
                volumeAttributes:
                  secretProviderClass: {package_prefix}-common-kv
  successfulJobsHistoryLimit: 1
  failedJobsHistoryLimit: 1
  concurrencyPolicy: Forbid
  startingDeadlineSeconds: 120
```

### 14. Generate Environment-Specific Values

Create `helm/{app_name}/values/nprdValues.yaml`, `stageValues.yaml`, `prodValues.yaml` with environment-specific overrides for:
- App Registration Client IDs
- Key Vault names and resource groups
- Workload Identity Client IDs
- Redis/Database connection strings
- Ingress hostnames

### 15. Generate Documentation

Create comprehensive documentation:
- README.md: Project overview, monorepo structure, setup instructions
- docs/API.md: OpenAPI documentation, endpoint descriptions
- docs/DEPLOYMENT.md: Helm deployment guide, environment configuration, Key Vault setup
- docs/ARCHITECTURE.md: System architecture, module interactions, data flow

### 16. Validate and Report


**Report Completion**:
```
✅ Backend Service Scaffolded

📦 Project: {app_name}
   Stack: FastAPI + Poetry + Docker + Helm + AKS
   Modules: API + Worker + Jobs
   Database: {database_choice}
   Auth: {auth_choice}

📂 Monorepo Structure:
   ├── api/                       FastAPI REST API
   ├── worker/                    Background workers (optional)
   ├── jobs/                      Scheduled jobs (optional)
   ├── shared/                    Shared package (models, schemas, utils)
   ├── helm/{app_name}/           Helm charts
   │   ├── templates/
   │   │   ├── api/              (deployment, service, ingress, virtual_service)
   │   │   ├── worker/           (deployment)
   │   │   ├── jobs/             (cronjob)
   │   │   └── common/           (key_vault)
   │   ├── values/               (nprdValues, stageValues, prodValues)
   │   ├── Chart.yaml
   │   └── values.yaml
   └── README.md

🔒 DevOps Compliance:
   ✓ Cookiecutter structure
   ✓ JFrog auth via ADO variable groups
   ✓ Multi-stage Docker (non-root)
   ✓ Workload identity for Key Vault
   ✓ Istio sidecar enabled
   ✓ Resource limits configured
   ✓ Probes configured
   ✓ OpenTelemetry instrumentation
   ✓ Environment variable prefix: {APP_ACRONYM}_

📋 Next Steps:
   1. Update infrastructure repo Terraform
   2. Configure Key Vault secrets
   3. Install: cd api && poetry install
   4. Run: cd api && poetry run uvicorn {package_prefix}_api.main:app --reload
   5. Test: poetry run pytest
   6. Deploy: Run ADO pipeline
```

## Error Handling

**Hard-Stop Violations**: Explain violation, suggest compliant alternative.

**Incomplete Input**: List missing information with examples.

**Environment Failure**: Report missing dependencies with installation steps.

## Examples

**Example 1**: `/scaffold-backend Create REST API for data processing with PostgreSQL and Redis`

**Example 2**: `/scaffold-backend Build microservice with scheduled cleanup jobs`

**Example 3**: `/scaffold-backend Create GraphQL API with Entra ID authentication`

## References

Constitution: (pre-loaded above)
DevOps Standards: `vibe_cdo/2025.12.04-DevOpsArchetypeNotes.md`
