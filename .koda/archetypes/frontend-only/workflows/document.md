---
description: Generate frontend-only documentation: setup, architecture, accessibility, and contributor guidelines (Frontend Only)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype frontend_only` and parse for ENV_VALID.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Read `${ARCHETYPES_BASEDIR}/frontend-only/templates/env-config.yaml` for project structure and brand guidelines.

### 3. Parse Input
Extract from $ARGUMENTS: project/app to document, target audience (developers/designers/stakeholders), documentation scope (README only/full docs/architecture). Request clarification if incomplete.

### 4. Analyze Project Structure

Scan project to identify:
- Components and their organization
- Routing structure
- State management approach
- API integration patterns
- Testing setup
- Build configuration

### 5. Generate README.md

```markdown
# {Project Name}

## Overview
{Brief description of the application and its purpose}

## Tech Stack
- **Framework**: React + TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **Testing**: Vitest + React Testing Library + Playwright
- **Package Manager**: pnpm

## Quick Start

### Prerequisites
- Node.js 18+
- pnpm 8+

### Installation
```bash
# Clone repository
git clone <repo-url>
cd {project-name}/frontend

# Install dependencies
pnpm install

# Copy environment variables
cp .env.example .env

# Start development server
pnpm dev
```

### Available Scripts
| Script | Description |
|--------|-------------|
| `pnpm dev` | Start development server |
| `pnpm build` | Build for production |
| `pnpm preview` | Preview production build |
| `pnpm test` | Run unit/component tests |
| `pnpm test:e2e` | Run Playwright E2E tests |
| `pnpm lint` | Lint code with ESLint |
| `pnpm format` | Format code with Prettier |

## Project Structure
```
frontend/
├── src/
│   ├── app/                    # Routes/pages
│   ├── components/
│   │   ├── layouts/            # Page layouts
│   │   ├── features/           # Feature components
│   │   └── ui/                 # Reusable UI primitives
│   ├── lib/
│   │   ├── api/                # API client
│   │   ├── hooks/              # Custom hooks
│   │   └── utils/              # Utilities
│   ├── styles/                 # Global styles
│   └── types/                  # TypeScript types
├── tests/
│   ├── unit/                   # Unit tests
│   ├── integration/            # Component tests
│   └── e2e/                    # Playwright tests
└── public/                     # Static assets
```

## Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_API_URL` | Backend API URL | No |
| `VITE_AUTHORITY` | OAuth authority URL | No |
| `VITE_CLIENT_ID` | OAuth client ID | No |

## Component Conventions

### File Naming
- Components: `PascalCase.tsx` (e.g., `Button.tsx`)
- Hooks: `camelCase.ts` with `use` prefix (e.g., `useDebounce.ts`)
- Utils: `camelCase.ts` (e.g., `fileValidation.ts`)
- Tests: `*.test.tsx` or `*.spec.ts`

### Component Structure
```typescript
// Props interface at top
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
}

// Named export
export function Button({ variant = 'primary', children }: ButtonProps) {
  return <button className={...}>{children}</button>;
}
```

## Testing

### Run Tests
```bash
# All tests
pnpm test

# With coverage
pnpm test --coverage

# Watch mode
pnpm test --watch

# E2E tests
pnpm test:e2e
```

### Test Coverage Target
- Minimum: 70% coverage
- Focus on: Component behavior, user interactions, accessibility

## Accessibility

This project follows WCAG 2.1 AA standards:
- Semantic HTML elements
- ARIA labels for interactive elements
- Keyboard navigation support
- Minimum 4.5:1 color contrast
- Minimum 44x44px touch targets

## Contributing

1. Create feature branch from `main`
2. Make changes following code conventions
3. Add/update tests
4. Run `pnpm lint` and `pnpm test`
5. Submit pull request

## License
Internal AT&T project - All rights reserved
```

### 6. Generate Architecture Documentation

**docs/architecture.md**:
```markdown
# Architecture Documentation

## Overview
{Project Name} is a frontend-only application built with React and TypeScript.

## Component Architecture

### Component Hierarchy
```
App
├── Layout
│   ├── Header
│   └── Footer
├── Pages
│   ├── HomePage
│   └── UploadPage
└── Features
    ├── FileUpload
    └── ChatPanel
        ├── MessageList
        └── ChatInput
```

### Component Categories

#### UI Components (`components/ui/`)
Reusable, stateless UI primitives:
- `Button` - Primary/secondary buttons with AT&T styling
- `Spinner` - Loading indicator
- `FloatingActionButton` - FAB for chat toggle

#### Feature Components (`components/features/`)
Business logic components:
- `ChatInput` - Message input with Enter/Shift+Enter handling
- `FileUpload` - PDF upload with validation
- `MessageList` - Chat message display

#### Layout Components (`components/layouts/`)
Page structure components:
- `MainLayout` - Header, content, footer structure
- `ChatLayout` - Chat panel layout

## State Management

### Local State
- Component-level state with `useState`
- Form state with React Hook Form

### Server State
- API calls with fetch/axios
- Caching with React Query (if applicable)

## Data Flow

```
User Action → Event Handler → State Update → Re-render
     ↓
API Call (if needed) → Response → State Update → Re-render
```

## Styling Architecture

### TailwindCSS Configuration
- Custom AT&T colors: `att-blue`, `att-cobalt`, `att-lime`, `att-mint`
- Responsive breakpoints: `sm`, `md`, `lg`, `xl`
- Dark mode: Not implemented (future consideration)

### Color Palette
| Name | Hex | Usage |
|------|-----|-------|
| AT&T Blue | `#009FDB` | Primary actions, links |
| AT&T Cobalt | `#00388F` | CTA buttons |
| AT&T Lime | `#91DC00` | Success states |
| AT&T Mint | `#49EEDC` | Accents |

## File Validation

PDF validation checks both MIME type and file extension:
```typescript
// Valid: application/pdf OR .pdf extension
// Invalid: Any other file type
```

## Error Handling

### Component Errors
- Error boundaries catch rendering errors
- Fallback UI displayed on error

### API Errors
- Timeout handling (10s default)
- User-friendly error messages
- Retry logic for transient failures

## Performance Considerations

- Code splitting with `React.lazy()`
- Memoization with `useMemo` and `useCallback`
- Image optimization
- Bundle size monitoring
```

### 7. Generate Accessibility Documentation

**docs/accessibility.md**:
```markdown
# Accessibility Guidelines

## Standards
This project follows **WCAG 2.1 Level AA** guidelines.

## Checklist

### Perceivable
- [ ] All images have alt text
- [ ] Color contrast ratio ≥ 4.5:1 for text
- [ ] Information not conveyed by color alone
- [ ] Text can be resized to 200% without loss

### Operable
- [ ] All functionality available via keyboard
- [ ] No keyboard traps
- [ ] Focus visible on all interactive elements
- [ ] Touch targets ≥ 44x44px
- [ ] Skip links for navigation

### Understandable
- [ ] Language declared in HTML
- [ ] Labels for all form inputs
- [ ] Error messages are descriptive
- [ ] Consistent navigation

### Robust
- [ ] Valid HTML
- [ ] ARIA used correctly
- [ ] Works with screen readers

## Implementation Patterns

### Buttons
```tsx
// Icon-only button needs aria-label
<button aria-label="Open menu">
  <MenuIcon aria-hidden="true" />
</button>
```

### Forms
```tsx
// Label associated with input
<label htmlFor="email">Email</label>
<input id="email" type="email" aria-describedby="email-error" />
<span id="email-error" role="alert">Invalid email</span>
```

### Dialogs
```tsx
// Focus management for modals
<dialog aria-labelledby="dialog-title" aria-modal="true">
  <h2 id="dialog-title">Dialog Title</h2>
  {/* Focus trapped inside dialog */}
</dialog>
```

### Loading States
```tsx
// Announce loading to screen readers
<div aria-live="polite" aria-busy={isLoading}>
  {isLoading ? <Spinner /> : <Content />}
</div>
```

## Testing

### Automated Testing
```bash
# Run axe accessibility tests
pnpm test tests/integration/accessibility.test.tsx
```

### Manual Testing
1. Navigate with keyboard only (Tab, Enter, Escape)
2. Test with screen reader (VoiceOver, NVDA)
3. Check color contrast with browser DevTools
4. Test at 200% zoom level

## Resources
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [axe DevTools](https://www.deque.com/axe/)
- [React Accessibility](https://reactjs.org/docs/accessibility.html)
```

### 8. Generate Documentation Report

```
📚 Documentation Generated

📄 Files Created:
   ✓ frontend/README.md - Project overview and quick start
   ✓ frontend/docs/architecture.md - Component and data flow architecture
   ✓ frontend/docs/accessibility.md - WCAG guidelines and patterns

📊 Documentation Coverage:
   ✓ Setup instructions
   ✓ Project structure
   ✓ Component conventions
   ✓ Environment configuration
   ✓ Testing guide
   ✓ Accessibility checklist
   ✓ Contributing guidelines

🎯 Target Audiences:
   ✓ Developers (setup, conventions)
   ✓ Designers (component patterns)
   ✓ QA (testing, accessibility)

✅ Next Steps:
   1. Review generated documentation
   2. Add project-specific details
   3. Update component examples
   4. Commit documentation to repository
```

## Error Handling

**Incomplete Project**: Request clarification on which areas to document.

**Missing Information**: Identify gaps and request details (components, API patterns).

**Complex Architecture**: Break down into multiple focused documents.

## Examples

**Example 1**: `/document-frontend Generate README for chatbot UI project`

**Example 2**: `/document-frontend Create architecture documentation for component library`

**Example 3**: `/document-frontend Generate accessibility guidelines for form components`

## References

Constitution: (pre-loaded above)
Environment Config: `${ARCHETYPES_BASEDIR}/frontend-only/templates/env-config.yaml`
