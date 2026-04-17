---
description: Generate comprehensive test suite for backend API services with unit, integration, and load tests (Backend Only)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype backend_only` and parse for PYTHON_VERSION, PYTEST_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.

### 3. Parse Input
Extract from $ARGUMENTS: target modules/endpoints to test, test types needed (unit/integration/load/security), coverage goals, specific scenarios. Request clarification if incomplete.

### 4. Analyze Code Structure

Scan backend service to identify:
- API endpoints and routes
- Database models and repositories
- Service layer business logic
- External integrations
- Background workers and jobs
- Authentication/authorization logic
- Configuration and settings

### 5. Generate Test Structure

Create comprehensive test suite:

```
tests/
├── unit/
│   ├── test_models.py           # Database model tests
│   ├── test_schemas.py          # Pydantic schema tests
│   ├── test_services.py         # Business logic tests
│   └── test_utils.py            # Utility function tests
├── integration/
│   ├── test_api_endpoints.py    # API integration tests
│   ├── test_database.py         # Database integration tests
│   └── test_external_apis.py   # External service tests
├── load/
│   └── test_performance.py      # Load and performance tests
├── security/
│   └── test_auth.py             # Security and auth tests
├── conftest.py                  # Pytest fixtures
└── __init__.py
```

### 6. Generate Unit Tests

**A. Model Tests**:
```python
# tests/unit/test_models.py
import pytest
from datetime import datetime
from app_api.models.user import User

class TestUserModel:
    def test_user_creation(self):
        """Test creating a user instance"""
        user = User(
            email="test@att.com",
            name="Test User",
            created_at=datetime.utcnow()
        )
        assert user.email == "test@att.com"
        assert user.name == "Test User"
        assert user.created_at is not None
    
    def test_user_email_validation(self):
        """Test email validation"""
        with pytest.raises(ValueError):
            User(email="invalid-email", name="Test")
    
    def test_user_repr(self):
        """Test string representation"""
        user = User(email="test@att.com", name="Test User")
        assert "test@att.com" in repr(user)
```

**B. Schema Tests**:
```python
# tests/unit/test_schemas.py
import pytest
from pydantic import ValidationError
from app_api.schemas.user import UserCreate, UserResponse

class TestUserSchemas:
    def test_user_create_valid(self):
        """Test valid user creation schema"""
        data = {
            "email": "test@att.com",
            "name": "Test User",
            "password": "SecurePass123!"
        }
        user = UserCreate(**data)
        assert user.email == "test@att.com"
        assert user.name == "Test User"
    
    def test_user_create_invalid_email(self):
        """Test invalid email validation"""
        with pytest.raises(ValidationError):
            UserCreate(
                email="not-an-email",
                name="Test",
                password="SecurePass123!"
            )
    
    def test_user_create_short_password(self):
        """Test password length validation"""
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@att.com",
                name="Test",
                password="short"
            )
    
    def test_user_response_excludes_password(self):
        """Test response schema doesn't include password"""
        user_data = {
            "id": 1,
            "email": "test@att.com",
            "name": "Test User"
        }
        user = UserResponse(**user_data)
        assert not hasattr(user, 'password')
```

**C. Service Tests**:
```python
# tests/unit/test_services.py
import pytest
from unittest.mock import Mock, AsyncMock, patch
from app_api.services.user_service import UserService
from app_api.schemas.user import UserCreate

class TestUserService:
    @pytest.fixture
    def mock_db(self):
        return AsyncMock()
    
    @pytest.fixture
    def user_service(self, mock_db):
        return UserService(mock_db)
    
    @pytest.mark.asyncio
    async def test_create_user_success(self, user_service, mock_db):
        """Test successful user creation"""
        user_data = UserCreate(
            email="test@att.com",
            name="Test User",
            password="SecurePass123!"
        )
        
        mock_db.execute.return_value = Mock(id=1)
        
        result = await user_service.create(user_data)
        
        assert result.id == 1
        assert mock_db.execute.called
    
    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(self, user_service, mock_db):
        """Test duplicate email handling"""
        from sqlalchemy.exc import IntegrityError
        
        user_data = UserCreate(
            email="test@att.com",
            name="Test User",
            password="SecurePass123!"
        )
        
        mock_db.execute.side_effect = IntegrityError("", "", "")
        
        with pytest.raises(ValueError, match="already exists"):
            await user_service.create(user_data)
    
    @pytest.mark.asyncio
    async def test_get_user_by_id(self, user_service, mock_db):
        """Test retrieving user by ID"""
        mock_user = Mock(id=1, email="test@att.com")
        mock_db.execute.return_value.scalar_one_or_none.return_value = mock_user
        
        result = await user_service.get_by_id(1)
        
        assert result.id == 1
        assert result.email == "test@att.com"
```

### 7. Generate Integration Tests

**A. API Endpoint Tests**:
```python
# tests/integration/test_api_endpoints.py
import pytest
from httpx import AsyncClient
from app_api.main import app

@pytest.mark.asyncio
class TestUserEndpoints:
    @pytest.fixture
    async def client(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac
    
    async def test_create_user_success(self, client):
        """Test POST /api/v1/users endpoint"""
        response = await client.post(
            "/api/v1/users",
            json={
                "email": "test@att.com",
                "name": "Test User",
                "password": "SecurePass123!"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@att.com"
        assert "password" not in data
    
    async def test_create_user_invalid_data(self, client):
        """Test validation error handling"""
        response = await client.post(
            "/api/v1/users",
            json={
                "email": "invalid-email",
                "name": "Test"
            }
        )
        
        assert response.status_code == 422
    
    async def test_get_users_pagination(self, client):
        """Test GET /api/v1/users with pagination"""
        response = await client.get(
            "/api/v1/users?skip=0&limit=10"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) <= 10
    
    async def test_get_user_by_id(self, client):
        """Test GET /api/v1/users/{id}"""
        # First create a user
        create_response = await client.post(
            "/api/v1/users",
            json={
                "email": "test@att.com",
                "name": "Test User",
                "password": "SecurePass123!"
            }
        )
        user_id = create_response.json()["id"]
        
        # Then retrieve it
        response = await client.get(f"/api/v1/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
    
    async def test_get_user_not_found(self, client):
        """Test 404 for non-existent user"""
        response = await client.get("/api/v1/users/99999")
        assert response.status_code == 404
```

**B. Database Integration Tests**:
```python
# tests/integration/test_database.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app_api.models.base import Base
from app_api.models.user import User

@pytest.fixture
async def test_db():
    """Create test database"""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=True
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()

@pytest.mark.asyncio
class TestDatabaseOperations:
    async def test_create_and_retrieve_user(self, test_db):
        """Test creating and retrieving a user"""
        user = User(email="test@att.com", name="Test User")
        test_db.add(user)
        await test_db.commit()
        
        result = await test_db.get(User, user.id)
        assert result.email == "test@att.com"
    
    async def test_unique_email_constraint(self, test_db):
        """Test email uniqueness constraint"""
        from sqlalchemy.exc import IntegrityError
        
        user1 = User(email="test@att.com", name="User 1")
        test_db.add(user1)
        await test_db.commit()
        
        user2 = User(email="test@att.com", name="User 2")
        test_db.add(user2)
        
        with pytest.raises(IntegrityError):
            await test_db.commit()
```

### 8. Generate Authentication Tests

**tests/security/test_auth.py**:
```python
import pytest
from jose import jwt
from datetime import datetime, timedelta
from app_api.core.security import create_access_token, verify_token

class TestAuthentication:
    def test_create_access_token(self):
        """Test JWT token creation"""
        data = {"sub": "user@att.com"}
        token = create_access_token(data)
        
        assert token is not None
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        assert decoded["sub"] == "user@att.com"
    
    def test_token_expiration(self):
        """Test token expiration"""
        data = {"sub": "user@att.com"}
        token = create_access_token(data, expires_delta=timedelta(seconds=-1))
        
        with pytest.raises(jwt.ExpiredSignatureError):
            verify_token(token)
    
    @pytest.mark.asyncio
    async def test_protected_endpoint_without_token(self, client):
        """Test accessing protected endpoint without token"""
        response = await client.get("/api/v1/protected")
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_protected_endpoint_with_valid_token(self, client):
        """Test accessing protected endpoint with valid token"""
        token = create_access_token({"sub": "user@att.com"})
        response = await client.get(
            "/api/v1/protected",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
```

### 9. Generate Load Tests

**tests/load/test_performance.py**:
```python
import pytest
import asyncio
from httpx import AsyncClient
from time import time

@pytest.mark.asyncio
class TestPerformance:
    async def test_endpoint_response_time(self, client):
        """Test endpoint response time under load"""
        start = time()
        response = await client.get("/api/v1/users")
        duration = time() - start
        
        assert response.status_code == 200
        assert duration < 0.5  # Should respond in < 500ms
    
    async def test_concurrent_requests(self):
        """Test handling concurrent requests"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            tasks = [
                client.get("/api/v1/users")
                for _ in range(100)
            ]
            
            start = time()
            responses = await asyncio.gather(*tasks)
            duration = time() - start
            
            assert all(r.status_code == 200 for r in responses)
            assert duration < 5.0  # 100 requests in < 5 seconds
    
    async def test_database_connection_pool(self):
        """Test connection pool doesn't exhaust"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            tasks = [
                client.post("/api/v1/users", json={
                    "email": f"user{i}@att.com",
                    "name": f"User {i}",
                    "password": "SecurePass123!"
                })
                for i in range(50)
            ]
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Should not have connection pool errors
            assert not any(isinstance(r, Exception) for r in responses)
```

### 10. Generate Test Fixtures

**tests/conftest.py**:
```python
import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app_api.main import app
from app_api.models.base import Base
from app_api.core.config import settings

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def test_db():
    """Test database fixture"""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()

@pytest.fixture
async def client():
    """HTTP client fixture"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def sample_user_data():
    """Sample user data fixture"""
    return {
        "email": "test@att.com",
        "name": "Test User",
        "password": "SecurePass123!"
    }
```

### 11. Generate Test Configuration

**pytest.ini**:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
markers =
    unit: Unit tests
    integration: Integration tests
    load: Load and performance tests
    security: Security tests
addopts = 
    -v
    --strict-markers
    --cov=app_api
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
```

### 12. Validate Tests

Run test suite:
```bash
poetry run pytest tests/ -v --cov=app_api --cov-report=html
```

### 13. Generate Test Report

```
🧪 Test Suite Generated

📊 Test Coverage:
   Unit Tests: <count> tests
   Integration Tests: <count> tests
   Security Tests: <count> tests
   Load Tests: <count> tests
   Total: <count> tests

📁 Test Structure:
   ✓ tests/unit/ - Model, schema, service tests
   ✓ tests/integration/ - API endpoint tests
   ✓ tests/security/ - Authentication tests
   ✓ tests/load/ - Performance tests
   ✓ tests/conftest.py - Shared fixtures

✅ Coverage Goals:
   Target: 80% minimum
   Current: <percentage>%
   
   Covered:
   - API endpoints: <percentage>%
   - Business logic: <percentage>%
   - Database models: <percentage>%
   - Utilities: <percentage>%

🎯 Test Scenarios:
   ✓ Happy path scenarios
   ✓ Error handling
   ✓ Edge cases
   ✓ Validation errors
   ✓ Authentication/authorization
   ✓ Concurrent requests
   ✓ Database constraints

💡 Run Commands:
   - All tests: poetry run pytest
   - Unit only: poetry run pytest tests/unit/
   - With coverage: poetry run pytest --cov
   - Specific file: poetry run pytest tests/unit/test_models.py
   - Watch mode: poetry run pytest-watch

✅ Next Steps:
   1. Review generated tests
   2. Add project-specific test cases
   3. Run test suite locally
   4. Integrate into CI/CD pipeline
   5. Monitor coverage trends
```

## Error Handling

**Missing Dependencies**: Identify required test dependencies and add to pyproject.toml.

**Async Test Issues**: Ensure pytest-asyncio is configured correctly.

**Database Test Failures**: Verify test database setup and cleanup.

## Examples

**Example 1**: `/test-backend Generate unit tests for user service`

**Example 2**: `/test-backend Create integration tests for order API endpoints`

**Example 3**: `/test-backend Add load tests for high-traffic endpoints`

**Example 4**: `/test-backend Generate security tests for authentication`

## References

Constitution: (pre-loaded above)
Testing Standards: `vibe_cdo/mlops_engineer/team_standards.md`
