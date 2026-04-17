---
description: Generate a frontend-only web UI (no backend changes) with React + TypeScript + Tailwind, accessibility, and testing (Frontend Only)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype frontend_only` and parse for NODE_VERSION and ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Read `${ARCHETYPES_BASEDIR}/frontend-only/templates/env-config.yaml` for project structure and brand guidelines.

### 3. Parse Input
Extract from $ARGUMENTS:
- app name
- UI type (dashboard/marketing/internal tool/component library/chatbot)
- routing (Vite SPA vs Next.js)
- data strategy (mocked data vs real API integration)
- auth strategy (client-side only vs OIDC via existing provider)
- styling (Tailwind required; optional design system library)
- AT&T branding required (yes/no)

Request clarification if any of these are missing.

### 4. Validate Constraints (frontend-only)
Hard stops:
- ✘ Do not generate or modify backend services, infra, or database schemas.
- ✘ Do not hardcode secrets (no tokens in source).
- ✘ Do not add server-side auth flows (frontend only; if auth needed, wire to existing OAuth/OIDC via env-config).
- ✘ Do not introduce new proprietary fonts without approval.
- ✘ Do not omit accessibility (WCAG 2.1 AA).
- ✘ Do not create Tailwind projects without `postcss.config.js`.

### 5. Generate Project Structure
If repo has no frontend yet, generate a minimal modern frontend:

```
frontend/
├── src/
│   ├── app/                    # Routes/pages (or Next.js app/)
│   ├── components/
│   │   ├── layouts/            # Page layouts, headers, footers
│   │   ├── features/           # Feature-specific components
│   │   └── ui/                 # Reusable UI primitives
│   ├── lib/
│   │   ├── api/                # Fetch/axios wrappers, typed clients
│   │   ├── hooks/              # Custom React hooks
│   │   └── utils/              # Utility functions
│   ├── styles/
│   │   └── globals.css         # Global styles, Tailwind imports
│   └── types/                  # TypeScript type definitions
├── tests/
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── e2e/                    # Playwright E2E tests
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── postcss.config.js
└── .env.example
```

If a frontend already exists, only add missing pieces and keep conventions.

### 6. Configure TailwindCSS with AT&T Colors and Fonts (if branding required)

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'att-blue': '#009FDB',      // Primary actions, links, loaders
        'att-cobalt': '#00388F',    // CTA buttons, emphasis
        'att-lime': '#91DC00',      // Success states
        'att-mint': '#49EEDC',      // Accents, highlights
      },
      fontFamily: {
        'att': ['ATT Aleck Sans', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'],
        'att-condensed': ['ATT Aleck Cd', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'],
      },
    },
  },
  plugins: [],
};

export default config;
```

```css
/* src/styles/fonts.css - AT&T Font Configuration */
@font-face {
  font-family: 'ATT Aleck Sans';
  src: url('/fonts/ATTAleckSans-Regular.woff2') format('woff2'),
       url('/fonts/ATTAleckSans-Regular.woff') format('woff');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'ATT Aleck Sans';
  src: url('/fonts/ATTAleckSans-Medium.woff2') format('woff2'),
       url('/fonts/ATTAleckSans-Medium.woff') format('woff');
  font-weight: 500;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'ATT Aleck Sans';
  src: url('/fonts/ATTAleckSans-Bold.woff2') format('woff2'),
       url('/fonts/ATTAleckSans-Bold.woff') format('woff');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'ATT Aleck Cd';
  src: url('/fonts/ATTAleckCd-Medium.woff2') format('woff2'),
       url('/fonts/ATTAleckCd-Medium.woff') format('woff');
  font-weight: 500;
  font-style: normal;
  font-display: swap;
}
```

```css
/* src/styles/globals.css - Import fonts and apply */
@import './fonts.css';
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply font-att;
  }
}
```

```javascript
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

### 7. Implement UI Components
- Provide 2-4 screens/components based on requested UI type.
- Use semantic HTML, keyboard navigation, ARIA labels.
- Use a consistent component pattern (props typed, no `any`).
- Minimum touch target: 44x44px for interactive elements.

**Common UI Patterns**:

**Floating Action Button (FAB)**:
```typescript
// src/components/ui/FloatingActionButton.tsx
interface FABProps {
  onClick: () => void;
  icon: React.ReactNode;
  label: string;
}

export function FloatingActionButton({ onClick, icon, label }: FABProps) {
  return (
    <button
      onClick={onClick}
      aria-label={label}
      className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-att-blue text-white 
                 shadow-lg hover:bg-att-cobalt focus:outline-none focus:ring-2 
                 focus:ring-att-blue focus:ring-offset-2 transition-colors"
    >
      {icon}
    </button>
  );
}
```

**Loading Spinner (AT&T style)**:
```typescript
// src/components/ui/Spinner.tsx
export function Spinner({ className = '' }: { className?: string }) {
  return (
    <div className={`flex space-x-1 ${className}`} aria-label="Loading">
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          className="w-2 h-2 bg-att-blue rounded-full animate-bounce"
          style={{ animationDelay: `${i * 0.15}s` }}
        />
      ))}
    </div>
  );
}
```

**Chat Input (Enter to send, Shift+Enter for newline)**:
```typescript
// src/components/features/ChatInput.tsx
interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [value, setValue] = useState('');

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (value.trim()) {
        onSend(value.trim());
        setValue('');
      }
    }
  };

  return (
    <div className="flex gap-2">
      <textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        placeholder="Type a message..."
        className="flex-1 resize-none rounded-lg border p-2 focus:ring-2 focus:ring-att-blue"
        rows={2}
      />
      <button
        onClick={() => { onSend(value.trim()); setValue(''); }}
        disabled={disabled || !value.trim()}
        className="px-4 py-2 bg-att-cobalt text-white rounded-lg disabled:opacity-50"
      >
        Send
      </button>
    </div>
  );
}
```

### 8. Form Handling with Zod + React Hook Form

Use schema-based validation for all forms:

```typescript
// src/lib/schemas/loginSchema.ts
import { z } from 'zod';

export const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

export type LoginFormData = z.infer<typeof loginSchema>;
```

```typescript
// src/components/features/LoginForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { loginSchema, type LoginFormData } from '@/lib/schemas/loginSchema';

export function LoginForm({ onSubmit }: { onSubmit: (data: LoginFormData) => void }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          {...register('email')}
          className="mt-1 block w-full rounded-lg border p-2 focus:ring-2 focus:ring-att-blue"
          aria-describedby={errors.email ? 'email-error' : undefined}
        />
        {errors.email && (
          <p id="email-error" className="mt-1 text-sm text-red-600" role="alert">
            {errors.email.message}
          </p>
        )}
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password
        </label>
        <input
          id="password"
          type="password"
          {...register('password')}
          className="mt-1 block w-full rounded-lg border p-2 focus:ring-2 focus:ring-att-blue"
          aria-describedby={errors.password ? 'password-error' : undefined}
        />
        {errors.password && (
          <p id="password-error" className="mt-1 text-sm text-red-600" role="alert">
            {errors.password.message}
          </p>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full rounded-lg bg-att-cobalt px-4 py-2 text-white hover:bg-att-blue disabled:opacity-50"
      >
        {isSubmitting ? 'Signing in...' : 'Sign In'}
      </button>
    </form>
  );
}
```

**Required Dependencies**:
```json
{
  "dependencies": {
    "react-hook-form": "^7.x",
    "@hookform/resolvers": "^3.x",
    "zod": "^3.x"
  }
}
```

### 9. File Upload Validation
When accepting file uploads, validate both MIME type AND file extension:

```typescript
// src/lib/utils/fileValidation.ts
export function validatePdfFile(file: File): { valid: boolean; error?: string } {
  const validMimeTypes = ['application/pdf'];
  const validExtensions = ['.pdf'];
  
  const extension = file.name.toLowerCase().slice(file.name.lastIndexOf('.'));
  const isValidMime = validMimeTypes.includes(file.type);
  const isValidExtension = validExtensions.includes(extension);
  
  if (!isValidMime && !isValidExtension) {
    return { valid: false, error: 'Please upload a PDF file.' };
  }
  
  return { valid: true };
}
```

### 9. Data Layer
- If mocked: include a `src/lib/api/mock.ts` with deterministic fixtures and simulated delays.
- If real API: create a minimal typed client (fetch wrapper) with timeouts, error mapping, and request cancellation.

```typescript
// src/lib/api/client.ts
const API_TIMEOUT = 10000;

export async function apiClient<T>(
  url: string,
  options?: RequestInit
): Promise<T> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
  } finally {
    clearTimeout(timeoutId);
  }
}
```

### 10. Testing
- Unit/component tests with React Testing Library (Vitest/Jest depending on stack).
- Add at least 1 accessibility check (axe).
- Add 1 Playwright smoke test for the primary flow (optional).

**Example Component Test**:
```typescript
// tests/unit/FloatingActionButton.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { FloatingActionButton } from '@/components/ui/FloatingActionButton';

describe('FloatingActionButton', () => {
  it('renders and handles click', () => {
    const handleClick = vi.fn();
    render(
      <FloatingActionButton 
        onClick={handleClick} 
        icon={<span>+</span>} 
        label="Open chat" 
      />
    );
    
    const button = screen.getByRole('button', { name: 'Open chat' });
    fireEvent.click(button);
    expect(handleClick).toHaveBeenCalledOnce();
  });
});
```

**Example File Validation Test**:
```typescript
// tests/unit/fileValidation.test.ts
import { validatePdfFile } from '@/lib/utils/fileValidation';

describe('validatePdfFile', () => {
  it('accepts valid PDF file', () => {
    const file = new File([''], 'document.pdf', { type: 'application/pdf' });
    expect(validatePdfFile(file)).toEqual({ valid: true });
  });

  it('rejects non-PDF file', () => {
    const file = new File([''], 'image.png', { type: 'image/png' });
    expect(validatePdfFile(file)).toEqual({ 
      valid: false, 
      error: 'Please upload a PDF file.' 
    });
  });
});
```

**Example Accessibility Test**:
```typescript
// tests/integration/accessibility.test.tsx
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import App from '@/app/App';

expect.extend(toHaveNoViolations);

describe('Accessibility', () => {
  it('has no accessibility violations', async () => {
    const { container } = render(<App />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

### 11. Documentation
Create or update:
- `frontend/README.md` (setup, scripts, env vars)
- `frontend/.env.example`

### 12. Generate Scaffold Report

```
🎨 Frontend Scaffold Complete

📁 Project Structure:
   ✓ frontend/src/app/
   ✓ frontend/src/components/{layouts,features,ui}/
   ✓ frontend/src/lib/{api,hooks,utils}/
   ✓ frontend/src/styles/
   ✓ frontend/src/types/
   ✓ frontend/tests/{unit,integration,e2e}/

📦 Configuration Files:
   ✓ package.json
   ✓ tsconfig.json
   ✓ tailwind.config.ts (with AT&T colors: {branding})
   ✓ postcss.config.js
   ✓ .env.example

🧩 Components Created:
   - {list of components}

🧪 Tests Created:
   - {list of test files}

💡 Run Commands:
   - Install: pnpm install
   - Dev: pnpm dev
   - Build: pnpm build
   - Test: pnpm test
   - Lint: pnpm lint

✅ Next Steps:
   1. Review generated components
   2. Add project-specific features
   3. Run tests locally
   4. Update README with project details
```

## Error Handling

**Missing Dependencies**: Identify required packages and add to package.json.

**Styling Issues**: Verify PostCSS and Tailwind configs exist and are properly configured.

**Test Failures**: Check component imports and mock setup.

## Examples

**Example 1**: `/scaffold-frontend Create a dashboard UI with Vite, mocked data, AT&T branding`

**Example 2**: `/scaffold-frontend Build a chatbot interface with floating action button and chat panel`

**Example 3**: `/scaffold-frontend Generate a file upload component with PDF validation`

## References

Constitution: (pre-loaded above)
Environment Config: `${ARCHETYPES_BASEDIR}/frontend-only/templates/env-config.yaml`
