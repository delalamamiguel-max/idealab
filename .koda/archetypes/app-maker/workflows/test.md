---
description: Generate comprehensive test suite for web applications (App Maker)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype app-maker --json ` and parse for test tools (Vitest, Playwright, pytest).

### 2. Load Configuration
- The constitution rules are already loaded in context above.

### 3. Parse Input
Extract from $ARGUMENTS: components/endpoints to test, test types needed (unit/integration/e2e), coverage goals, specific scenarios. Request clarification if incomplete.

### 4. Core Testing Principle

⚠️ **CRITICAL: When tests fail, fix the APPLICATION CODE, not the tests.**

Tests are the source of truth. If a test fails:
- The application code has a bug that needs fixing
- Do NOT modify test assertions to make them pass
- Do NOT weaken validation logic or remove checks
- Only modify tests if they have genuine technical errors (wrong endpoint, invalid mock, flawed logic)

This workflow generates HIGH-QUALITY tests that enforce correctness. Preserve test integrity.

### 5. Analyze Application Structure

Identify testable components:

**Frontend Tests**:
- React components (unit tests)
- Custom hooks (unit tests)
- API integration (integration tests)
- User flows (E2E tests)
- Accessibility (a11y tests)

**Backend Tests**:
- API endpoints (integration tests)
- Business logic (unit tests)
- Database operations (integration tests)
- Authentication (integration tests)

**Brand Compliance Tests**:
- Color palette verification
- Typography checks
- Accessibility standards

### 5. Generate Frontend Unit Tests

**A. Component Tests** (React Testing Library):
```typescript
// tests/unit/components/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '@/components/ui/Button';

describe('Button Component', () => {
  it('renders and handles clicks', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledOnce();
  });

  it('applies ATT Cobalt for primary variant', () => {
    render(<Button variant="primary">CTA</Button>);
    expect(screen.getByRole('button')).toHaveClass('bg-att-cobalt');
  });
});
```

**B. Custom Hook Tests**:
```typescript
// tests/unit/hooks/useAuth.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { useAuth } from '@/lib/hooks/useAuth';

describe('useAuth Hook', () => {
  it('authenticates user correctly', async () => {
    const { result } = renderHook(() => useAuth());
    await result.current.login('test@example.com', 'password');
    await waitFor(() => expect(result.current.isAuthenticated).toBe(true));
  });
});
```

**C. Form Validation Tests** (Zod):
```typescript
// tests/unit/validators/userSchema.test.ts
import { userSchema } from '@/lib/validators/userSchema';

describe('User Schema', () => {
  it('validates correct data', () => {
    expect(() => userSchema.parse({
      email: 'test@example.com', name: 'John', password: 'SecurePass123'
    })).not.toThrow();
  });

  it('rejects invalid email and short password', () => {
    expect(() => userSchema.parse({email: 'bad', name: 'J', password: '123'})).toThrow();
  });
});
```

### 6. Generate Frontend Integration Tests

**A. API Integration Tests** (Mock Service Worker):
```typescript
// tests/integration/api/users.test.tsx
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import { renderHook, waitFor } from '@testing-library/react';
import { useUsers } from '@/lib/api/hooks/useUsers';

const server = setupServer(
  rest.get('/api/v1/users', (req, res, ctx) => 
    res(ctx.json([{ id: 1, name: 'User 1' }, { id: 2, name: 'User 2' }]))
  )
);

beforeAll(() => server.listen());
afterAll(() => server.close());

describe('useUsers API', () => {
  it('fetches users successfully', async () => {
    const { result } = renderHook(() => useUsers(), { wrapper: QueryWrapper });
    await waitFor(() => expect(result.current.data).toHaveLength(2));
  });

  it('handles errors', async () => {
    server.use(rest.get('/api/v1/users', (req, res, ctx) => res(ctx.status(500))));
    const { result } = renderHook(() => useUsers(), { wrapper: QueryWrapper });
    await waitFor(() => expect(result.current.isError).toBe(true));
  });
});
```

### 7. Generate E2E Tests

**A. User Flow Tests** (Playwright):
```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('successful login flow', async ({ page }) => {
    await page.goto('/login');
    const btn = page.locator('button[type="submit"]');
    await expect(btn).toHaveCSS('background-color', 'rgb(0, 56, 143)'); // ATT Cobalt
    
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'password123');
    await btn.click();
    
    await expect(page).toHaveURL('/dashboard');
  });

  test('invalid credentials show error', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'wrong@example.com');
    await page.fill('[name="password"]', 'wrong');
    await page.click('button[type="submit"]');
    await expect(page.locator('text=Invalid credentials')).toBeVisible();
  });

  test('protected routes redirect', async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page).toHaveURL('/login');
  });
});
```

**B. Accessibility Tests**:
```typescript
// tests/e2e/accessibility.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('no violations on homepage', async ({ page }) => {
    await page.goto('/');
    const results = await new AxeBuilder({ page }).analyze();
    expect(results.violations).toEqual([]);
  });

  test('keyboard navigation works', async ({ page }) => {
    await page.goto('/contact');
    await page.keyboard.press('Tab');
    await expect(page.locator('[name="name"]')).toBeFocused();
    await page.keyboard.press('Tab');
    await expect(page.locator('[name="email"]')).toBeFocused();
  });
});
```

### 8. Generate Backend Tests

**A. API Endpoint Tests** (pytest + FastAPI TestClient):
```python
# tests/integration/test_users_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/api/v1/users", json={
        "email": "new@example.com", "name": "New User", "password": "SecurePass123"
    })
    assert response.status_code == 201
    assert "password" not in response.json()

def test_invalid_email():
    response = client.post("/api/v1/users", json={"email": "bad", "name": "U", "password": "p"})
    assert response.status_code == 422

def test_auth_required():
    assert client.get("/api/v1/users").status_code == 401
    token = get_auth_token()
    response = client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
```

**B. Business Logic Tests**:
```python
# tests/unit/test_user_service.py
from app.services.user_service import UserService

def test_password_hashing():
    service = UserService()
    user = service.create_user({"email": "test@example.com", "password": "plaintext"})
    assert user.password != "plaintext" and len(user.password) > 20

def test_password_validation():
    service = UserService()
    user = service.create_user({"email": "test@example.com", "password": "correct"})
    assert service.validate_password(user, "correct") is True
    assert service.validate_password(user, "wrong") is False
```

### 9. Generate Brand Compliance Tests

```typescript
// tests/integration/brand-compliance.test.tsx
import { render } from '@testing-library/react';
import { App } from '@/App';

describe('AT&T Brand', () => {
  it('uses ATT Aleck Sans font', () => {
    render(<App />);
    expect(window.getComputedStyle(document.body).fontFamily).toContain('ATT Aleck Sans');
  });

  it('uses AT&T Blue (#009FDB) and Cobalt (#00388F)', () => {
    const { container } = render(<App />);
    const header = container.querySelector('header');
    expect(window.getComputedStyle(header!).backgroundColor).toBe('rgb(0, 159, 219)');
    const btn = container.querySelector('.btn-primary');
    expect(window.getComputedStyle(btn!).backgroundColor).toBe('rgb(0, 56, 143)');
  });
});
```

### 10. Generate Test Configuration

**A. Vitest Config**:
```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    coverage: { provider: 'v8', reporter: ['text', 'html'], exclude: ['node_modules/', 'tests/'] }
  }
});
```

**B. Playwright Config**:
```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests/e2e',
  use: { baseURL: 'http://localhost:5173', screenshot: 'only-on-failure' },
  webServer: { command: 'npm run dev', port: 5173 }
});
```

**C. Pytest Config**:
```ini
# pytest.ini
[pytest]
testpaths = tests
addopts = --cov=app --cov-report=html -v
```

### 11. Validate and Report

Run test suite: `npm test && cd backend && pytest`

**If Tests Fail - Critical Protocol**:

🚨 **Fix Application Code, NOT Tests**:
- Failing tests indicate bugs in the APPLICATION CODE
- **NEVER** modify test assertions to make them pass
- **NEVER** weaken test validation logic
- **NEVER** remove or comment out failing tests
- Only modify tests if they contain genuine errors (wrong API, incorrect mock setup, invalid assertion logic)

**Proper Test Failure Response**:
1. **Analyze the failure**: Read error messages and stack traces
2. **Locate the bug**: Identify which application code causes the failure
3. **Fix the root cause**: Modify the application code (not the test)
4. **Re-run tests**: Verify the fix resolves the issue
5. **Only modify tests if**: The test itself is incorrectly written (e.g., wrong endpoint path, invalid mock data structure, flawed test logic)

**Example - Correct Approach**:
❌ **WRONG**: Test expects 201 status but gets 200 → Change test to expect 200
✅ **CORRECT**: Test expects 201 status but gets 200 → Fix API endpoint to return 201

❌ **WRONG**: Test expects user.password to be hashed but it's plaintext → Remove password assertion
✅ **CORRECT**: Test expects user.password to be hashed but it's plaintext → Fix UserService to hash passwords

**Report Results**:
```
✅ Test Suite Generated

📊 Test Coverage:
   Frontend: <coverage>% (<files> files, <tests> tests)
   Backend: <coverage>% (<files> files, <tests> tests)

📝 Tests Created:
   Unit Tests: <count>
   Integration Tests: <count>
   E2E Tests: <count>
   Accessibility Tests: <count>
   Brand Compliance Tests: <count>

✓ Component Tests: <count> components covered
✓ API Tests: <count> endpoints covered
✓ User Flow Tests: <count> critical paths
✓ Accessibility Tests: WCAG 2.1 AA compliance
✓ Brand Tests: AT&T guidelines verified

📋 Next Steps:
   1. Review generated tests
   2. Run test suite: npm test
   3. Check coverage: npm run coverage
   4. Run E2E tests: npx playwright test
   5. Add to CI/CD pipeline

💡 Commands:
   - Run all tests: npm test && pytest
   - Watch mode: npm test -- --watch
   - E2E tests: npx playwright test
   - Coverage: npm run coverage
```

## Error Handling

**Test Failures**: **ALWAYS fix application code, not tests**. Only modify tests if they contain genuine technical errors (wrong API path, invalid mock structure, flawed assertion logic). Never weaken tests to make them pass.

**Missing Test Data**: Generate mock data or fixtures for tests.

**Complex Component**: Break into smaller testable units, suggest refactoring.

**External Dependencies**: Use MSW for API mocking, suggest test doubles.

**Flaky Tests**: Investigate and fix race conditions or timing issues in application code. Add proper waits/synchronization, don't just skip or weaken the test.

## Examples

**Example 1**: `/test-app Generate tests for UserProfile component`
Output: Unit tests, integration tests with API mocking, accessibility tests

**Example 2**: `/test-app Create E2E tests for checkout flow`
Output: Playwright tests covering add to cart, payment, confirmation

**Example 3**: `/test-app Add tests for authentication API endpoints`
Output: pytest integration tests for login, logout, token refresh

## References

Constitution: (pre-loaded above)
