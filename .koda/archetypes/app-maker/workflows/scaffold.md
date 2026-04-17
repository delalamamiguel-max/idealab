---
description: Generate ready-to-deploy web application with React/FastAPI following AT&T brand guidelines (App Maker)
auto_execution_mode: 1
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype app-maker --json ` and parse for NODE_VERSION, PYTHON_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.

### 3. Parse Input
Extract from $ARGUMENTS: project name, description, features needed, database choice (PostgreSQL/SQLite/None), authentication requirement (Entra ID yes/no), CI/CD requirement (GitHub Actions yes/no), telemetry requirement (Azure App Insights yes/no), environment config strategy (multi/single). Request clarification if incomplete.

### 4. Validate Constraints
Check against hard-stop rules:
- ✘ Refuse if database credentials would be hardcoded
- ✘ Refuse if non-ATT fonts specified
- ✘ Refuse if AT&T Blue not dominant color
- ✘ Refuse if missing input validation requirements
- ✘ Refuse if accessibility requirements omitted
If violated, explain clearly and suggest compliant alternative.

### 5. Generate Project Structure

Create complete project with structure: frontend (React + TypeScript + TailwindCSS), backend (FastAPI + Python), database setup if requested, authentication integration if enabled, CI/CD pipeline if enabled, telemetry integration if enabled.

**Frontend Structure** (src/):
```
frontend/
├── public/
├── src/
│   ├── app/                    # Routes and pages
│   ├── components/
│   │   ├── ui/                 # shadcn/ui components
│   │   ├── features/           # Feature components
│   │   └── layouts/            # Layout components
│   ├── lib/
│   │   ├── api/                # API client
│   │   ├── hooks/              # Custom hooks
│   │   └── utils/              # Utilities
│   ├── styles/
│   │   └── globals.css         # TailwindCSS + ATT styles
│   ├── assets/
│   │   └── fonts/
│   │       └── att-brand/      # ATT Aleck fonts
│   └── types/                  # TypeScript types
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── package.json
├── tsconfig.json
├── tailwind.config.js          # ATT colors configured
├── vite.config.ts              # or next.config.js
├── .eslintrc.json
├── .prettierrc
└── .env.example
```

**Backend Structure** (backend/):
```
backend/
├── app/
│   ├── api/
│   │   └── v1/                 # API version 1
│   │       ├── endpoints/
│   │       └── dependencies.py
│   ├── core/
│   │   ├── config.py           # Settings
│   │   ├── security.py         # Auth & security
│   │   └── logging.py
│   ├── models/                 # Database models
│   ├── schemas/                # Pydantic schemas
│   ├── services/               # Business logic
│   └── main.py                 # FastAPI app
├── tests/
│   ├── unit/
│   └── integration/
├── requirements.txt
├── Dockerfile
└── .env.example
```

### 6. Generate Frontend Code

**A. TailwindCSS Config with AT&T Colors**:
```javascript
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        'att-blue': '#009FDB',
        'att-cobalt': '#00388F',
        'att-lime': '#91DC00',
        'att-mint': '#49EEDC',
      },
      fontFamily: {
        sans: ['ATT Aleck Sans', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
```

**B. Global Styles with ATT Typography**:
```css
/* src/styles/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@font-face {
  font-family: 'ATT Aleck Sans';
  src: url('../../assets/fonts/att-brand/ATTAleckSans-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
}

@layer base {
  body {
    @apply font-sans text-black bg-white;
  }
  h1, h2, h3 {
    @apply text-att-blue font-bold;
  }
}

@layer components {
  .btn-primary {
    @apply bg-att-cobalt text-white px-6 py-3 rounded-lg hover:opacity-90 transition-opacity;
  }
}
```

**C. API Client Setup**:
```typescript
// src/lib/api/client.ts
import axios from 'axios';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
```

**D. Main App Component**:
```typescript
// src/App.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ErrorBoundary } from 'react-error-boundary';

const queryClient = new QueryClient();

function App() {
  return (
    <ErrorBoundary fallback={<ErrorFallback />}>
      <QueryClientProvider client={queryClient}>
        {/* Router and routes */}
      </QueryClientProvider>
    </ErrorBoundary>
  );
}
```

### 7. Generate Backend Code

**A. FastAPI Main App**:
```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

**B. Configuration**:
```python
# backend/app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    DATABASE_URL: str | None = None
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**C. Input Validation Example**:
```python
# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
```

**D. Requirements.txt with Tested Versions**:
```python
# backend/requirements.txt
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Database ORM (compatible with Pydantic 2.9.x)
sqlalchemy==2.0.35
aiosqlite==0.19.0

# Data Validation (compatible with SQLAlchemy 2.0.35)
pydantic==2.9.2
pydantic-settings==2.5.2
python-json-logger==2.0.7

# Testing
pytest
pytest-asyncio
httpx

# Version compatibility verified: FastAPI 0.104.1 + Pydantic 2.9.2 + SQLAlchemy 2.0.35
```

### 7.5. Validate Python Dependencies and Database Schema

Run `${ARCHETYPES_BASEDIR}/app-maker/scripts/validate-dependencies.py --requirements backend/requirements.txt --json` to check for version compatibility issues.

**If violations found**:
- Report specific incompatibilities with package versions
- Suggest compatible version combinations from constitutional rules
- Halt generation until resolved or user acknowledges risk

**If database schema generated**:
Run `${ARCHETYPES_BASEDIR}/app-maker/scripts/validate-sql-keywords.py --schema database/schema.sql --engine sqlalchemy --json` to check for reserved keyword usage.

**If violations found**:
- Report identifiers conflicting with SQLAlchemy reserved attributes
- Suggest safe alternatives (e.g., `metadata` → `workflow_metadata`)
- Auto-fix by applying suggested alternatives to schema

**Validation Report**:
```
✓ Python Dependencies: Compatible versions verified
✓ Database Schema: No reserved keyword conflicts
```

### 7.6. Generate Test Infrastructure (MANDATORY)

Create test directories, configuration, and example test files for both frontend and backend.

**Frontend Tests**:

Create `frontend/vitest.config.ts`:
```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './tests/setup.ts',
  },
});
```

Create `frontend/tests/setup.ts`:
```typescript
import '@testing-library/jest-dom';
```

Create `frontend/tests/unit/App.test.tsx`:
```typescript
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from '../../src/App';

describe('App', () => {
  it('renders without crashing', () => {
    render(<App />);
    expect(document.body).toBeTruthy();
  });
});
```

Create `frontend/playwright.config.ts`:
```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  use: { baseURL: 'http://localhost:5173' },
  webServer: { command: 'npm run dev', port: 5173 },
});
```

Create `frontend/tests/e2e/health.spec.ts`:
```typescript
import { test, expect } from '@playwright/test';

test('app loads', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/Vite/);
});
```

Update `frontend/package.json` to include test dependencies and scripts:
```json
"scripts": {
  "test": "vitest",
  "test:e2e": "playwright test"
},
"devDependencies": {
  "@playwright/test": "latest",
  "@testing-library/jest-dom": "latest",
  "@testing-library/react": "latest",
  "@vitest/ui": "latest",
  "jsdom": "latest",
  "vitest": "latest"
}
```

**Backend Tests**:

Create `backend/pytest.ini`:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
asyncio_mode = auto
```

Create `backend/tests/conftest.py`:
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)
```

Create `backend/tests/unit/test_health.py`:
```python
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

Create `backend/tests/integration/test_api.py`:
```python
def test_api_v1_health(client):
    response = client.get("/api/v1/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

**Ensure all test directories exist**:
- Create `frontend/tests/unit/`
- Create `frontend/tests/integration/`
- Create `frontend/tests/e2e/`
- Create `backend/tests/unit/`
- Create `backend/tests/integration/`

### 8. Add Authentication (if enabled)

**Microsoft Entra ID Integration**:
- Frontend: MSAL.js library for authentication flow
- Backend: JWT validation using azure-identity
- Protected routes with auth middleware
- Token refresh logic

### 9. Add CI/CD (if enabled)

**GitHub Actions Workflow**:
```yaml
# .github/CDO-AIFC/reference/workflows/ci.yml
name: CI/CD
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run frontend tests
        run: cd frontend && npm test
      - name: Run backend tests
        run: cd backend && pytest
```

### 10. Add Documentation

Generate comprehensive documentation:
- **README.md**: Project overview, setup instructions, architecture
- **docs/SETUP.md**: Detailed setup guide for local development
- **docs/API.md**: API documentation with examples
- **docs/DEPLOYMENT.md**: Deployment instructions
- **docs/SECURITY.md**: Security practices and guidelines

### 11. Validate and Report


**Report Completion**:
```
✅ Web Application Scaffolded

📦 Project: <PROJECT_NAME>
   Stack: React + FastAPI
   Database: <DATABASE>
   Auth: <Entra ID status>
   CI/CD: <GitHub Actions status>

📂 Structure Generated:
   ├── frontend/          React + TypeScript + TailwindCSS (with tests/)
   ├── backend/           FastAPI + Python (with tests/)
   ├── .github/           CI/CD workflows (if enabled)
   └── docs/              Complete documentation

🧪 Testing Infrastructure:
   ✓ Frontend: Vitest (unit/integration) + Playwright (E2E)
   ✓ Backend: Pytest with async support
   ✓ Test fixtures and configurations included
   ✓ Example tests for all levels
   ✓ CI/CD pipeline with test automation
   ✓ Code coverage reporting

🎨 AT&T Brand Compliance:
   ✓ AT&T Blue dominant color scheme
   ✓ ATT Aleck Sans font configured
   ✓ Cobalt CTA buttons
   ✓ 4.5:1 contrast ratio for text
   ✓ Responsive design (mobile-first)

🔒 Security Features:
   ✓ Environment variables for secrets
   ✓ Input validation (frontend + backend)
   ✓ CORS configured
   ✓ HTTPS enforcement ready
   ✓ CSRF protection
   ✓ Secure headers configured

📋 Next Steps:
   1. Install dependencies: cd frontend && npm install
   2. Install backend: cd backend && pip install -r requirements.txt
   3. Configure .env files from .env.example
   4. Start dev servers: npm run dev (frontend), uvicorn app.main:app (backend)
   5. Run tests: npm test (frontend), pytest (backend)
   6. Review and customize generated code

💡 Commands:
   - Frontend dev: cd frontend && npm run dev
   - Backend dev: cd backend && uvicorn app.main:app --reload
   - Run tests: npm test && cd ../../backend && pytest
   - Build production: npm run build
   - Lint: npm run lint
```

## Error Handling

**Hard-Stop Violations**: Explain violation (e.g., non-ATT font), suggest compliant alternative with ATT Aleck configuration.

**Incomplete Input**: List missing information (project name, features, database choice), provide example.

**Environment Failure**: Report missing Node.js or Python, suggest installation steps.

## Examples

**Example 1**: `/scaffold-app Create customer dashboard with user authentication and data visualization`
Output: Full-stack app with Entra ID auth, charts, AT&T-branded UI

**Example 2**: `/scaffold-app Build internal tool for data entry with PostgreSQL database`
Output: React form-heavy UI, FastAPI CRUD API, PostgreSQL integration

**Example 3**: `/scaffold-app Create public-facing product catalog with search`
Output: SEO-optimized Next.js app, FastAPI search API, AT&T brand styling

## References

Constitution: (pre-loaded above)
