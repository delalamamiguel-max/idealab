---
description: Validate enterprise microservice pipeline for architecture, testing, and governance readiness across Java/Spring Boot and Python/FastAPI stacks (Enterprise Microservice)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR [⋯]

**SUCCESS CRITERIA**:
- Search for directory: "00-core-orchestration"
- Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory

**HALT IF**:
- Directory "00-core-orchestration" is not found
- `${ARCHETYPES_BASEDIR}` is not set

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Environment Setup
// turbo
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype enterprise-microservice` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/enterprise-microservice/enterprise-microservice-constitution.md` for testing standards and enterprise requirements
- Read `${ARCHETYPES_BASEDIR}/backend-only/backend-only-constitution.md` for inherited testing standards

### 3. Parse Input
Extract from $ARGUMENTS: target modules/endpoints to test, technology stack (Java/Python), test types needed (unit/integration/load/security/contract), coverage goals, specific scenarios. Request clarification if incomplete.

### 4. Detect Technology Stack

Identify service stack from project files:
- **Java/Spring Boot**: `pom.xml`, `build.gradle`, `application.yaml`
- **Python/FastAPI**: `pyproject.toml`, `requirements.txt`, `main.py`

### 5. Analyze Code Structure

Scan service to identify testable components:

**Java/Spring Boot**:
- Controllers and REST endpoints
- Service layer business logic
- Repository/DAO layer
- Configuration classes
- Security filters and interceptors
- Scheduled tasks
- Custom health indicators

**Python/FastAPI**:
- API routers and endpoints
- Service layer functions
- Database models and repositories
- Pydantic schemas
- Background workers
- Authentication middleware

### 6. Generate Test Structure

**Java/Spring Boot**:
```
src/test/
├── java/{package}/
│   ├── controller/
│   │   └── UserControllerTest.java
│   ├── service/
│   │   └── UserServiceTest.java
│   ├── repository/
│   │   └── UserRepositoryTest.java
│   ├── integration/
│   │   └── UserApiIntegrationTest.java
│   └── security/
│       └── AuthenticationTest.java
└── resources/
    └── application-test.yaml
```

**Python/FastAPI**:
```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_schemas.py
│   └── test_services.py
├── integration/
│   ├── test_api_endpoints.py
│   └── test_database.py
├── security/
│   └── test_auth.py
├── load/
│   └── test_performance.py
├── conftest.py
└── __init__.py
```

### 7. Generate Unit Tests

**A. Java/Spring Boot Unit Tests**:

```java
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Test
    void shouldReturnUserById() throws Exception {
        UserDto user = new UserDto(1L, "test@att.com", "Test User");
        when(userService.findById(1L)).thenReturn(Optional.of(user));

        mockMvc.perform(get("/api/v1/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.email").value("test@att.com"));
    }

    @Test
    void shouldReturn404WhenUserNotFound() throws Exception {
        when(userService.findById(99L)).thenReturn(Optional.empty());

        mockMvc.perform(get("/api/v1/users/99"))
            .andExpect(status().isNotFound());
    }
}

@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserServiceImpl userService;

    @Test
    void shouldCreateUser() {
        User user = new User("test@att.com", "Test User");
        when(userRepository.save(any(User.class))).thenReturn(user);

        UserDto result = userService.create(new CreateUserDto("test@att.com", "Test User"));

        assertThat(result.getEmail()).isEqualTo("test@att.com");
        verify(userRepository).save(any(User.class));
    }
}
```

**B. Python/FastAPI Unit Tests**:

```python
# tests/unit/test_services.py
import pytest
from unittest.mock import Mock, AsyncMock
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
        user_data = UserCreate(
            email="test@att.com",
            name="Test User",
            password="SecurePass123!"
        )
        mock_db.execute.return_value = Mock(id=1)
        result = await user_service.create(user_data)
        assert result.id == 1
```

### 8. Generate Integration Tests

**A. Java/Spring Boot Integration Tests**:

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureMockMvc
class UserApiIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void shouldCreateAndRetrieveUser() throws Exception {
        String response = mockMvc.perform(post("/api/v1/users")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"email\":\"test@att.com\",\"name\":\"Test User\"}"))
            .andExpect(status().isCreated())
            .andReturn().getResponse().getContentAsString();

        Long userId = JsonPath.read(response, "$.id");

        mockMvc.perform(get("/api/v1/users/" + userId))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.email").value("test@att.com"));
    }
}
```

**B. Python/FastAPI Integration Tests**:

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
        response = await client.post("/api/v1/users", json={
            "email": "test@att.com",
            "name": "Test User",
            "password": "SecurePass123!"
        })
        assert response.status_code == 201
        assert "password" not in response.json()
```

### 9. Generate Health Check Tests

**A. Java/Spring Boot Actuator Tests**:

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class ActuatorHealthTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void shouldReturnHealthUp() {
        ResponseEntity<String> response = restTemplate.getForEntity(
            "/actuator/health", String.class);
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(response.getBody()).contains("UP");
    }

    @Test
    void shouldReturnLivenessUp() {
        ResponseEntity<String> response = restTemplate.getForEntity(
            "/actuator/health/liveness", String.class);
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
    }

    @Test
    void shouldReturnReadinessUp() {
        ResponseEntity<String> response = restTemplate.getForEntity(
            "/actuator/health/readiness", String.class);
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
    }
}
```

**B. Python/FastAPI Health Tests**:

```python
@pytest.mark.asyncio
class TestHealthEndpoints:
    async def test_liveness(self, client):
        response = await client.get("/monitor/liveness")
        assert response.status_code == 200
        assert response.json()["status"] == "alive"

    async def test_readiness(self, client):
        response = await client.get("/monitor/readiness")
        assert response.status_code == 200
        assert response.json()["status"] == "ready"
```

### 10. Generate Security Tests

Both Stacks:
- Test authentication required on protected endpoints
- Test token validation and expiration
- Test role-based access control
- Test CORS configuration
- Test input validation rejects malicious input

### 11. Generate Contract Tests

Validate API contracts:
- OpenAPI specification matches implementation
- Response schemas match documented formats
- Error responses follow RFC 7807 (Java) or consistent format (Python)

### 12. Generate Test Configuration

**Java** (`application-test.yaml`):
```yaml
spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
  jpa:
    hibernate:
      ddl-auto: create-drop
```

**Python** (`conftest.py`):
```python
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

@pytest.fixture
async def test_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # setup and teardown
```

### 13. Validate Tests

// turbo
Run test suite based on stack:

*Java*:
```bash
./mvnw test -Dspring.profiles.active=test
```

*Python*:
```bash
poetry run pytest tests/ -v --cov --cov-report=html --cov-fail-under=80
```

### 14. Generate Test Report

```
🧪 Enterprise Microservice Test Suite

📍 Technology Stack: <Java/Spring Boot | Python/FastAPI>

📊 Test Coverage:
   Unit Tests: <count> tests
   Integration Tests: <count> tests
   Security Tests: <count> tests
   Health Check Tests: <count> tests
   Contract Tests: <count> tests
   Total: <count> tests

✅ Coverage Goals:
   Target: 80% minimum
   Current: <percentage>%

🏢 Enterprise Validation:
   ✓ Health endpoint tests
   ✓ Graceful shutdown tests
   ✓ Authentication tests
   ✓ Input validation tests
   ✓ Error handling tests

💡 Run Commands:
   Java: ./mvnw test
   Python: poetry run pytest

✅ Next Steps:
   1. Review generated tests
   2. Add project-specific test cases
   3. Integrate into CI/CD pipeline
   4. Monitor coverage trends
```

## Error Handling

**Missing Dependencies**: Identify required test dependencies for the detected stack.

**Async Test Issues**: Ensure pytest-asyncio (Python) or @Async test support (Java) configured.

**Database Test Failures**: Verify test database setup (H2 for Java, SQLite for Python).

## Examples

**Example 1**: `/test-enterprise-microservice Generate unit tests for Spring Boot order service`

**Example 2**: `/test-enterprise-microservice Create integration tests for FastAPI user API endpoints`

**Example 3**: `/test-enterprise-microservice Add health check and security tests for Java payment-service`

## References

Constitution: `${ARCHETYPES_BASEDIR}/enterprise-microservice/enterprise-microservice-constitution.md`
Backend-Only Constitution: `${ARCHETYPES_BASEDIR}/backend-only/backend-only-constitution.md`
