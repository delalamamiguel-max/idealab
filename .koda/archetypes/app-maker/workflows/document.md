---
description: Generate comprehensive documentation for web applications (App Maker)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype app-maker --json ` and parse for ENV_VALID.

### 2. Load Configuration
- The constitution rules are already loaded in context above.

### 3. Parse Input
Extract from $ARGUMENTS: documentation type (README, API docs, architecture, deployment, user guide), target audience (developers, users, stakeholders), level of detail. Request clarification if incomplete.

### 4. Analyze Application Structure

Examine project to understand:
- Technology stack (frontend, backend, database)
- Architecture patterns
- Key features and components
- API endpoints
- Authentication/authorization
- Deployment configuration
- Testing strategy

### 5. Generate README.md

Create comprehensive project overview:

```markdown
# <Project Name>

<Brief description of what the application does>

## ✨ Features

- **Feature 1**: Description
- **Feature 2**: Description
- **Feature 3**: Description
- **Authentication**: Microsoft Entra ID integration
- **Telemetry**: Azure Application Insights monitoring

## 🛠️ Technology Stack

**Frontend**: React 18 + TypeScript, Vite, TailwindCSS, React Query, Zod validation
**Backend**: FastAPI (Python 3.11+), PostgreSQL, JWT + Entra ID, OpenAPI
**DevOps**: GitHub Actions, Vercel/Azure, App Insights, Docker

## 📋 Prerequisites
Node.js 18+, pnpm, Python 3.11+, PostgreSQL 15+ (optional), Azure CLI

## 🚀 Quick Start

### 1. Clone the repository
\`\`\`bash
git clone <repository-url>
cd <project-name>
\`\`\`

### 2. Install dependencies
\`\`\`bash
cd frontend && pnpm install
cd ../../backend && pip install -r requirements.txt
\`\`\`

### 3. Configure environment
\`\`\`bash
cp frontend/.env.example frontend/.env.local
cp backend/.env.example backend/.env
# Edit .env files with your configuration
\`\`\`

### 4. Start servers
\`\`\`bash
cd frontend && pnpm dev  # http://localhost:5173
cd backend && uvicorn app.main:app --reload  # http://localhost:8000
\`\`\`

## 📁 Project Structure
\`\`\`
frontend/          React + TypeScript (src/app, components, lib, tests)
backend/           FastAPI + Python (api/v1, core, models, schemas, services)
docs/              API, architecture, deployment, security documentation
.github/CDO-AIFC/reference/workflows/ CI/CD pipelines
\`\`\`

## 🧪 Testing
\`\`\`bash
cd frontend && pnpm test        # Unit tests
cd frontend && pnpm test:e2e    # E2E tests
cd backend && pytest --cov      # Backend tests with coverage
\`\`\`

## 🚢 Deployment
See docs/DEPLOYMENT.md for details.
\`\`\`bash
cd frontend && vercel deploy --prod
cd backend && az webapp up --name <app-name> --resource-group <rg>
\`\`\`

## 🔒 Security
Environment variables for secrets, HTTPS enforced, CORS configured, input validation (frontend + backend), SQL injection prevention, XSS protection. See docs/SECURITY.md.

## 🎨 AT&T Brand Guidelines
AT&T Blue (#009FDB) dominant, Cobalt (#00388F) CTAs, ATT Aleck Sans typography, WCAG 2.1 AA compliant.

## 📚 Documentation
[API](docs/API.md) | [Architecture](docs/ARCHITECTURE.md) | [Deployment](docs/DEPLOYMENT.md) | [Security](docs/SECURITY.md)

## 🤝 Contributing

1. Create a feature branch: \`git checkout -b feature/my-feature\`
2. Make changes and commit: \`git commit -am 'Add my feature'\`
3. Push to branch: \`git push origin feature/my-feature\`
4. Submit a pull request

## 📄 License

AT&T Proprietary

## 👥 Support

For questions or issues, contact: <support-email>
```

### 6. Generate API Documentation

Create comprehensive API docs:

```markdown
# API Documentation

Base URL: \`https://api.example.com/api/v1\`

## Authentication
JWT tokens required: `Authorization: Bearer <token>`. Obtain via POST /auth/login with email/password.

## Endpoints

### Users

#### Example Endpoints
\`\`\`http
GET /users?limit=20&offset=0&search=query  # List users (paginated)
POST /users {email, name, password}         # Create user
GET /users/{id}                             # Get user details
PUT /users/{id}                             # Update user
DELETE /users/{id}                          # Delete user
\`\`\`

## Error Responses
Standard HTTP codes: 400 (validation), 401 (unauthorized), 403 (forbidden), 500 (server error).

## Rate Limiting
Public: 100/hour per IP. Authenticated: 1000/hour per user. Headers: X-RateLimit-*
```

### 7. Generate Architecture Documentation

```markdown
# Architecture Overview

## System Architecture

\`\`\`mermaid
graph TB
    Browser -->|HTTPS| CDN[Vercel/CDN]
    CDN --> React[React SPA]
    React -->|REST| FastAPI[FastAPI Backend]
    FastAPI --> DB[(PostgreSQL)]
    React -.OAuth.-> Auth[Entra ID]
    FastAPI -.OAuth.-> Auth
    FastAPI -.Logs.-> Monitor[App Insights]
\`\`\`

## Architecture
**Frontend**: Component hierarchy (App/Layouts/Pages/Features/UI), React Query for server state, Context for auth, React Hook Form for forms.

**Backend**: Layered (API/Service/Data/Core), versioned endpoints (/api/v1/), PostgreSQL with SQLAlchemy ORM, Alembic migrations.

**Security**: JWT tokens (1-hour expiry), role-based access control (RBAC), endpoint-level permission checks.

## Data Flow
**Read**: Component → React Query cache → API → Database → Cache → UI update
**Write**: Form → Zod validation → API → Pydantic validation → DB transaction → Cache invalidation → Optimistic UI

## Deployment
**Production**: Frontend (Vercel CDN), Backend (Azure App Service), Database (Azure PostgreSQL), Monitoring (App Insights), CI/CD (GitHub Actions)

## Design Decisions
**React**: Large ecosystem, TypeScript, AT&T enterprise adoption
**FastAPI**: Auto docs, built-in validation, async performance
**PostgreSQL**: ACID compliance, mature, excellent performance
```

### 8. Generate Additional Documentation

Create deployment guide (dev/staging/prod), security practices documentation, and user guide with screenshots if applicable.

### 11. Validate and Report

```
✅ Documentation Generated

📚 Documents Created:
   ✓ README.md - Project overview and quick start
   ✓ docs/API.md - Complete API documentation
   ✓ docs/ARCHITECTURE.md - System architecture
   ✓ docs/DEPLOYMENT.md - Deployment guide
   ✓ docs/SECURITY.md - Security practices
   ✓ docs/USER_GUIDE.md - End-user guide (if applicable)

📊 Documentation Coverage:
   ✓ Setup instructions
   ✓ Development workflow
   ✓ Testing procedures
   ✓ API endpoints (<count> documented)
   ✓ Architecture diagrams
   ✓ Security practices
   ✓ Deployment steps

🎨 AT&T Brand Documentation:
   ✓ Color palette reference
   ✓ Typography guidelines
   ✓ Accessibility standards

📋 Next Steps:
   1. Review generated documentation
   2. Add project-specific details
   3. Include screenshots/diagrams
   4. Keep docs updated with code changes

💡 Maintenance:
   - Update API docs when endpoints change
   - Document new features
   - Keep deployment steps current
   - Review security docs quarterly
```

## Error Handling

**Incomplete Project**: Request clarification on missing components or features.

**Complex Architecture**: Break into multiple focused documents.

**Outdated Code**: Warn about potential mismatches between code and docs.

## Examples

**Example 1**: `/document-app Generate complete documentation for customer portal`
Output: README, API docs, architecture, deployment guide

**Example 2**: `/document-app Create API documentation for all endpoints`
Output: Comprehensive API docs with examples and schemas

**Example 3**: `/document-app Write user guide for data entry application`
Output: Step-by-step user guide with screenshots

## References

Constitution: (pre-loaded above)
