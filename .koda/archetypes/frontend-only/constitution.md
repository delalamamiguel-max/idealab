# Frontend Only Constitution

## Purpose

This constitution defines the non-negotiable rules for the **Frontend Only** archetype.

**Scope:** Frontend UI code only (components, styles, client-side routing, frontend tests, docs). The agent must not introduce any backend, database, or infrastructure changes.

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any output that violates these rules:

- ✘ **Frontend-only scope**: Do not create/modify backend services, APIs, databases, infra (Terraform/K8s), or server config. If the request requires backend changes, propose a frontend-only alternative and document what backend work would be needed.
- ✘ **No hardcoded secrets**: No tokens, API keys, client secrets, or credentials in source.
- ✘ **No insecure client-side auth**: Do not implement "fake security" (e.g., hiding routes only). If auth is required, integrate with an existing OAuth/OIDC provider using public client patterns and env vars.
- ✘ **No accessibility omissions**: Do not ship UI without semantic HTML, keyboard navigation, ARIA labels where appropriate, and focus management for dialogs/menus. Must meet WCAG 2.1 AA standards.
- ✘ **No XSS footguns**: Do not use `dangerouslySetInnerHTML` with untrusted content; sanitize if truly required.
- ✘ **No broken styling pipeline**: If Tailwind is used, ensure `postcss.config.js` and `tailwind.config.*` exist and styles are loaded.

## II. Mandatory Patterns (Must Apply)

- ✔ **Type safety**: Prefer TypeScript strictness; avoid `any`.
- ✔ **Component architecture**: Separate UI primitives (`components/ui`) from feature components (`components/features`) and layouts (`components/layouts`).
- ✔ **Forms**: Use schema-based validation (Zod + React Hook Form) for user input.
- ✔ **Error + loading states**: Provide consistent loading (skeleton loaders, spinners), empty, and error states.
- ✔ **Testing**: Add React Testing Library component tests + optional Playwright E2E smoke test for critical flows.
- ✔ **Accessibility checks**: Include at least one automated a11y check (axe) when adding new pages/dialogs.
- ✔ **File validation**: When accepting file uploads, validate MIME type AND file extension; show inline errors for invalid files.

## III. AT&T Brand Guidelines (When Applicable)

### Color Palette

Use these colors when AT&T brand compliance is required:

| Color Name | Hex Code | Usage |
|------------|----------|-------|
| AT&T Blue (Primary) | `#009FDB` | Primary actions, links, loaders |
| AT&T Cobalt (CTA) | `#00388F` | Call-to-action buttons, emphasis |
| AT&T Lime | `#91DC00` | Success states, positive indicators |
| AT&T Mint | `#49EEDC` | Accents, highlights |
| Neutral Background | `#F5F5F5` | Page backgrounds |

### Typography

**Primary Font**: ATT Aleck Sans
- Use for body text, UI elements, and general content
- Weights: Regular (400), Medium (500), Bold (700)
- Fallback chain: `'ATT Aleck Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif`

**Condensed Font**: ATT Aleck Cd
- Use for headlines, hero text, and space-constrained areas
- Weight: Medium (500)
- Fallback chain: `'ATT Aleck Cd', 'Helvetica Neue', Helvetica, Arial, sans-serif`

**Font Rules**:
- ✔ Always include system font fallbacks
- ✔ Use `font-display: swap` for web fonts to prevent FOIT
- ✔ Place font files in `/public/fonts/` directory
- ✔ Support both `.woff2` (primary) and `.woff` (fallback) formats
- ✘ Do not use proprietary AT&T fonts without proper licensing
- ✘ Do not hardcode font URLs to external CDNs

**TailwindCSS Configuration**:
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'att-blue': '#009FDB',
        'att-cobalt': '#00388F',
        'att-lime': '#91DC00',
        'att-mint': '#49EEDC',
      },
      fontFamily: {
        'att': ['ATT Aleck Sans', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'],
        'att-condensed': ['ATT Aleck Cd', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'],
      },
    },
  },
};
```

## IV. Preferred Patterns (Recommended)

- ➜ **State**: React Query for server state; Zustand/Context for simple client state.
- ➜ **Performance**: Route-level code splitting, avoid heavy dependencies, memoize hot components.
- ➜ **UX**: Use skeleton loaders, accessible toasts, predictable empty states.
- ➜ **Interactive elements**: FABs should be circular with shadow, hover/focus rings; minimum touch target 44x44px.
- ➜ **Chat/Dialog patterns**: Auto-scroll to latest message, Enter to send, Shift+Enter for newline.
- ➜ **Accessible UI libraries**: Prefer Radix UI or Headless UI for dialogs, drawers, and menus.

## V. Project Structure

Follow this folder hierarchy for new frontend projects:

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
├── tailwind.config.*
├── postcss.config.*
└── .env.example
```

**Version**: 1.1.0
**Last Updated**: 2026-01-21
