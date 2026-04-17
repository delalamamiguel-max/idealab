---
description: Add/upgrade frontend-only test coverage: unit, component, accessibility, and E2E smoke tests (Frontend Only)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype frontend_only` and parse for NODE_VERSION, ENV_VALID.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Read `${ARCHETYPES_BASEDIR}/frontend-only/templates/env-config.yaml` for testing requirements.

### 3. Parse Input
Extract from $ARGUMENTS: target modules/components to test, test types needed (unit/component/integration/e2e/accessibility), coverage goals, specific scenarios. Request clarification if incomplete.

### 4. Identify Stack
Detect: React/Vue/Svelte, Vite/Next, test runner (Vitest/Jest), and E2E (Playwright/Cypress).
If unknown, default to Vitest + React Testing Library + Playwright.

### 5. Analyze Code Structure

Scan frontend to identify:
- UI components (buttons, forms, modals)
- Feature components (chat, upload, dashboard)
- Custom hooks
- Utility functions
- API client functions
- Form validation schemas

### 6. Generate Test Structure

Create comprehensive test suite:

```
tests/
├── unit/
│   ├── utils/
│   │   └── fileValidation.test.ts
│   └── hooks/
│       └── useDebounce.test.ts
├── integration/
│   ├── components/
│   │   ├── Button.test.tsx
│   │   ├── ChatInput.test.tsx
│   │   └── FileUpload.test.tsx
│   └── accessibility.test.tsx
└── e2e/
    └── smoke.spec.ts
```

### 7. Generate Unit Tests

**A. Utility Function Tests**:
```typescript
// tests/unit/utils/fileValidation.test.ts
import { describe, it, expect } from 'vitest';
import { validatePdfFile } from '@/lib/utils/fileValidation';

describe('validatePdfFile', () => {
  it('accepts valid PDF file with correct MIME type', () => {
    const file = new File(['content'], 'document.pdf', { type: 'application/pdf' });
    expect(validatePdfFile(file)).toEqual({ valid: true });
  });

  it('accepts PDF file with correct extension but no MIME', () => {
    const file = new File(['content'], 'document.pdf', { type: '' });
    expect(validatePdfFile(file)).toEqual({ valid: true });
  });

  it('rejects non-PDF file', () => {
    const file = new File(['content'], 'image.png', { type: 'image/png' });
    expect(validatePdfFile(file)).toEqual({
      valid: false,
      error: 'Please upload a PDF file.',
    });
  });

  it('rejects file with PDF extension but wrong MIME', () => {
    const file = new File(['content'], 'fake.pdf.exe', { type: 'application/x-msdownload' });
    expect(validatePdfFile(file)).toEqual({
      valid: false,
      error: 'Please upload a PDF file.',
    });
  });
});
```

**B. Custom Hook Tests**:
```typescript
// tests/unit/hooks/useDebounce.test.ts
import { renderHook, act } from '@testing-library/react';
import { useDebounce } from '@/lib/hooks/useDebounce';

describe('useDebounce', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('returns initial value immediately', () => {
    const { result } = renderHook(() => useDebounce('initial', 500));
    expect(result.current).toBe('initial');
  });

  it('debounces value changes', () => {
    const { result, rerender } = renderHook(
      ({ value }) => useDebounce(value, 500),
      { initialProps: { value: 'initial' } }
    );

    rerender({ value: 'updated' });
    expect(result.current).toBe('initial');

    act(() => {
      vi.advanceTimersByTime(500);
    });

    expect(result.current).toBe('updated');
  });
});
```

### 8. Generate Component Tests

**A. UI Component Tests**:
```typescript
// tests/integration/components/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '@/components/ui/Button';

describe('Button', () => {
  it('renders with children', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument();
  });

  it('handles click events', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledOnce();
  });

  it('applies primary variant styles by default', () => {
    render(<Button>Primary</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('bg-att-cobalt');
  });

  it('applies secondary variant styles', () => {
    render(<Button variant="secondary">Secondary</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('bg-gray-200');
  });

  it('can be disabled', () => {
    render(<Button disabled>Disabled</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

**B. Feature Component Tests**:
```typescript
// tests/integration/components/ChatInput.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ChatInput } from '@/components/features/ChatInput';

describe('ChatInput', () => {
  it('renders textarea and send button', () => {
    render(<ChatInput onSend={vi.fn()} />);
    
    expect(screen.getByPlaceholderText('Type a message...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /send/i })).toBeInTheDocument();
  });

  it('calls onSend when clicking send button', async () => {
    const handleSend = vi.fn();
    const user = userEvent.setup();
    render(<ChatInput onSend={handleSend} />);
    
    await user.type(screen.getByPlaceholderText('Type a message...'), 'Hello');
    await user.click(screen.getByRole('button', { name: /send/i }));
    
    expect(handleSend).toHaveBeenCalledWith('Hello');
  });

  it('calls onSend when pressing Enter', async () => {
    const handleSend = vi.fn();
    const user = userEvent.setup();
    render(<ChatInput onSend={handleSend} />);
    
    const textarea = screen.getByPlaceholderText('Type a message...');
    await user.type(textarea, 'Hello{enter}');
    
    expect(handleSend).toHaveBeenCalledWith('Hello');
  });

  it('does not send on Shift+Enter (allows newline)', async () => {
    const handleSend = vi.fn();
    const user = userEvent.setup();
    render(<ChatInput onSend={handleSend} />);
    
    const textarea = screen.getByPlaceholderText('Type a message...');
    await user.type(textarea, 'Line 1{shift>}{enter}{/shift}Line 2');
    
    expect(handleSend).not.toHaveBeenCalled();
    expect(textarea).toHaveValue('Line 1\nLine 2');
  });

  it('disables send button when input is empty', () => {
    render(<ChatInput onSend={vi.fn()} />);
    expect(screen.getByRole('button', { name: /send/i })).toBeDisabled();
  });

  it('clears input after sending', async () => {
    const user = userEvent.setup();
    render(<ChatInput onSend={vi.fn()} />);
    
    const textarea = screen.getByPlaceholderText('Type a message...');
    await user.type(textarea, 'Hello');
    await user.click(screen.getByRole('button', { name: /send/i }));
    
    expect(textarea).toHaveValue('');
  });
});
```

**C. File Upload Tests**:
```typescript
// tests/integration/components/FileUpload.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { FileUpload } from '@/components/features/FileUpload';

describe('FileUpload', () => {
  it('renders upload button', () => {
    render(<FileUpload onUpload={vi.fn()} />);
    expect(screen.getByRole('button', { name: /upload/i })).toBeInTheDocument();
  });

  it('accepts valid PDF file', async () => {
    const handleUpload = vi.fn();
    render(<FileUpload onUpload={handleUpload} />);
    
    const file = new File(['content'], 'document.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText(/upload/i);
    
    fireEvent.change(input, { target: { files: [file] } });
    
    await waitFor(() => {
      expect(handleUpload).toHaveBeenCalledWith(file);
    });
  });

  it('shows error for non-PDF file', async () => {
    render(<FileUpload onUpload={vi.fn()} />);
    
    const file = new File(['content'], 'image.png', { type: 'image/png' });
    const input = screen.getByLabelText(/upload/i);
    
    fireEvent.change(input, { target: { files: [file] } });
    
    await waitFor(() => {
      expect(screen.getByText('Please upload a PDF file.')).toBeInTheDocument();
    });
  });

  it('does not call onUpload for invalid file', async () => {
    const handleUpload = vi.fn();
    render(<FileUpload onUpload={handleUpload} />);
    
    const file = new File(['content'], 'image.png', { type: 'image/png' });
    const input = screen.getByLabelText(/upload/i);
    
    fireEvent.change(input, { target: { files: [file] } });
    
    await waitFor(() => {
      expect(handleUpload).not.toHaveBeenCalled();
    });
  });
});
```

### 9. Generate Accessibility Tests

```typescript
// tests/integration/accessibility.test.tsx
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { Button } from '@/components/ui/Button';
import { ChatInput } from '@/components/features/ChatInput';
import { FloatingActionButton } from '@/components/ui/FloatingActionButton';

expect.extend(toHaveNoViolations);

describe('Accessibility', () => {
  describe('Button', () => {
    it('has no accessibility violations', async () => {
      const { container } = render(<Button>Click me</Button>);
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });
  });

  describe('ChatInput', () => {
    it('has no accessibility violations', async () => {
      const { container } = render(<ChatInput onSend={vi.fn()} />);
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });
  });

  describe('FloatingActionButton', () => {
    it('has no accessibility violations', async () => {
      const { container } = render(
        <FloatingActionButton
          onClick={vi.fn()}
          icon={<span>+</span>}
          label="Open chat"
        />
      );
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });

    it('has accessible name via aria-label', () => {
      render(
        <FloatingActionButton
          onClick={vi.fn()}
          icon={<span>+</span>}
          label="Open chat"
        />
      );
      expect(screen.getByRole('button', { name: 'Open chat' })).toBeInTheDocument();
    });
  });
});
```

### 10. Generate E2E Tests (Optional)

```typescript
// tests/e2e/smoke.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Smoke Tests', () => {
  test('homepage loads successfully', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/Document Q&A/);
  });

  test('FAB opens chat panel', async ({ page }) => {
    await page.goto('/');
    
    // Click floating action button
    await page.click('[aria-label="Open chat"]');
    
    // Verify chat panel is visible
    await expect(page.locator('[data-testid="chat-panel"]')).toBeVisible();
    
    // Verify welcome message
    await expect(page.locator('text=Hi! Upload a PDF')).toBeVisible();
  });

  test('file upload accepts PDF', async ({ page }) => {
    await page.goto('/');
    
    // Upload a PDF file
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles({
      name: 'test.pdf',
      mimeType: 'application/pdf',
      buffer: Buffer.from('PDF content'),
    });
    
    // Verify upload success
    await expect(page.locator('text=test.pdf')).toBeVisible();
  });

  test('file upload rejects non-PDF', async ({ page }) => {
    await page.goto('/');
    
    // Try to upload a non-PDF file
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles({
      name: 'image.png',
      mimeType: 'image/png',
      buffer: Buffer.from('PNG content'),
    });
    
    // Verify error message
    await expect(page.locator('text=Please upload a PDF file')).toBeVisible();
  });

  test('chat requires PDF upload before answering', async ({ page }) => {
    await page.goto('/');
    
    // Open chat
    await page.click('[aria-label="Open chat"]');
    
    // Send a message without uploading PDF
    await page.fill('[placeholder="Type a message..."]', 'What is this about?');
    await page.click('button:has-text("Send")');
    
    // Verify guidance message
    await expect(page.locator('text=upload a PDF first')).toBeVisible();
  });
});
```

### 11. Generate Test Configuration

**vitest.config.ts**:
```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./tests/setup.ts'],
    include: ['tests/**/*.{test,spec}.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      exclude: ['node_modules/', 'tests/'],
      thresholds: {
        statements: 70,
        branches: 70,
        functions: 70,
        lines: 70,
      },
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

**tests/setup.ts**:
```typescript
import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});
```

**playwright.config.ts**:
```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'pnpm dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
});
```

### 12. Validate Tests

Run test suite: `pnpm test`

### 13. Generate Test Report

```
🧪 Test Suite Generated

📊 Test Coverage:
   Unit Tests: <count> tests
   Component Tests: <count> tests
   Accessibility Tests: <count> tests
   E2E Tests: <count> tests
   Total: <count> tests

📁 Test Structure:
   ✓ tests/unit/ - Utility and hook tests
   ✓ tests/integration/ - Component tests
   ✓ tests/integration/accessibility.test.tsx - Axe tests
   ✓ tests/e2e/ - Playwright smoke tests

✅ Coverage Goals:
   Target: 70% minimum
   Current: <percentage>%

🎯 Test Scenarios:
   ✓ Happy path scenarios
   ✓ Error handling
   ✓ Edge cases
   ✓ File validation (PDF only)
   ✓ Chat input (Enter/Shift+Enter)
   ✓ Accessibility (axe)
   ✓ Keyboard navigation

💡 Run Commands:
   - All tests: pnpm test
   - Unit only: pnpm test tests/unit/
   - With coverage: pnpm test --coverage
   - Watch mode: pnpm test --watch
   - E2E: pnpm exec playwright test

✅ Next Steps:
   1. Review generated tests
   2. Add project-specific test cases
   3. Run test suite locally
   4. Integrate into CI/CD pipeline
```

## Error Handling

**Missing Dependencies**: Identify required test packages and add to package.json.

**Test Environment Issues**: Verify jsdom setup and React Testing Library config.

**Flaky Tests**: Ensure deterministic tests (no random values, stable selectors).

## Examples

**Example 1**: `/test-frontend Generate component tests for ChatInput`

**Example 2**: `/test-frontend Add accessibility tests for all UI components`

**Example 3**: `/test-frontend Create E2E smoke test for file upload flow`

**Example 4**: `/test-frontend Add unit tests for file validation utility`

## References

Constitution: (pre-loaded above)
Environment Config: `${ARCHETYPES_BASEDIR}/frontend-only/templates/env-config.yaml`
