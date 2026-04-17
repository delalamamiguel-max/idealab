# UI Theme Architect Constitution

## Purpose

This constitution defines enforceable guardrails and operational standards for building semantic token theming systems within AT&T enterprise applications. All generated CSS, theme hooks, component variants, and documentation must comply with these rules while adapting to each project's brand and design language.

**Core Focus Areas**:

- CSS custom property semantic token systems following BluePearl's dark-first `:root` / `html.light` override architecture
- WCAG 2.1 AA contrast enforcement across every foreground/background token pair in both modes
- Live system preference detection via `prefers-color-scheme` with real-time OS-level change handling
- SVG and canvas theme resolution through `getComputedStyle` combined with `MutationObserver` on `<html>` class transitions
- Syntax highlighting token coverage for code blocks, inline code, and Lexical-based rich-text editors
- Scrollbar, text selection, focus ring, and modal backdrop theming using semantic tokens exclusively
- AT&T brand compliance with accessible color palettes derived from corporate design systems

---

## I. Hard-Stop Rules (Non-Negotiable)

Violations require the AI agent to refuse, rewrite, or block the requested artifact.

### 1.1 No Hardcoded Colors in Components

- ✘ **NEVER** embed raw color literals (`#1a1a2e`, `rgb(26,26,46)`, `hsl(240,28%,14%)`, `red`) inside component source files
- ✘ **NEVER** reference Tailwind palette utilities (`text-blue-500`, `bg-slate-900`, `border-zinc-700`) in application components
- ✘ **NEVER** apply inline style objects containing literal color values such as `style={{ color: '#0057b8' }}`
- ✔ **ALWAYS** consume semantic CSS custom properties through framework utilities (`bg-background`, `text-foreground`, `border-border`)
- ✔ **ALWAYS** record intentional exceptions (data-visualization categorical palettes, AT&T brand logos, git-diff indicators) in a dedicated `THEME_EXCEPTIONS.md` at the project root

**Rationale**: Scattered literal colors create an unmaintainable matrix where every theme addition requires touching hundreds of files. BluePearl's own codebase enforces zero hardcoded colors across 200+ component files.

**Compliant example**:
```tsx
{/* All color references resolve through semantic tokens */}
<aside className="bg-sidebar text-sidebar-foreground border-r border-sidebar-border">
  <h2 className="text-primary font-semibold">Navigation</h2>
  <p className="text-muted-foreground text-sm">Select a workspace</p>
</aside>
```

**Non-compliant example**:
```tsx
{/* Literal palette references — breaks theme switching */}
<aside className="bg-slate-950 text-slate-100 border-r border-slate-800">
  <h2 className="text-blue-400 font-semibold">Navigation</h2>
  <p className="text-slate-400 text-sm">Select a workspace</p>
</aside>
```

### 1.2 Semantic Token Naming Only

- ✘ **NEVER** derive token names from their visual appearance (`--blue-primary`, `--dark-background`, `--light-text-color`)
- ✘ **NEVER** mirror Tailwind or Material palette nomenclature (`--slate-900`, `--zinc-50`, `--indigo-600`)
- ✔ **ALWAYS** name tokens by their UI purpose using the pattern `--{role}` or `--{role}-{modifier}` (e.g., `--card`, `--card-foreground`, `--sidebar-border`)
- ✔ **ALWAYS** pair each background token with a corresponding `-foreground` token for text rendered on that surface

**Rationale**: A token named `--blue-500` communicates nothing about its role and becomes misleading when brand colors change. BluePearl uses 40+ semantically named tokens — none reference a hue or shade.

**Naming pattern reference**:
```css
/* Compliant — purpose-driven naming */
--background: oklch(0.145 0.014 265);
--foreground: oklch(0.94 0.01 265);
--primary: oklch(0.62 0.214 255);
--primary-foreground: oklch(0.975 0.005 255);
--muted: oklch(0.24 0.018 265);
--muted-foreground: oklch(0.58 0.016 265);
--destructive: oklch(0.54 0.195 27);

/* Non-compliant — palette-derived naming */
--slate-950: oklch(0.145 0.014 265);
--blue-500: oklch(0.62 0.214 255);
--red-600: oklch(0.54 0.195 27);
```

### 1.3 WCAG 2.1 AA Contrast Enforcement

- ✘ **NEVER** ship a foreground/background token pair that violates WCAG 2.1 AA minimum contrast ratios
- ✘ **NEVER** exempt informational text from contrast requirements by labeling it "decorative"
- ✔ **ALWAYS** achieve a minimum 4.5:1 contrast ratio for normal-weight text below 18pt (24px) or bold text below 14pt (18.67px)
- ✔ **ALWAYS** achieve a minimum 3:1 contrast ratio for large text (18pt+ or 14pt+ bold) and interactive UI components (borders, icons, form controls)
- ✔ **ALWAYS** validate contrast in both dark and light themes — passing in one mode does not exempt the other

**Rationale**: WCAG AA compliance is legally mandated under Section 508 and the ADA for AT&T's public-facing and internal applications. Low-contrast text excludes users with low vision.

**Required contrast validation pairs**:

| Foreground | Background | Required Ratio | Usage |
|-----------|-----------|---------------|-------|
| `--foreground` | `--background` | 4.5:1 | Body text on page |
| `--card-foreground` | `--card` | 4.5:1 | Text inside cards |
| `--popover-foreground` | `--popover` | 4.5:1 | Dropdown/tooltip text |
| `--primary-foreground` | `--primary` | 4.5:1 | Text on primary buttons |
| `--muted-foreground` | `--background` | 4.5:1 | Secondary body text |
| `--muted-foreground` | `--muted` | 4.5:1 | Text on muted surfaces |
| `--destructive-foreground` | `--destructive` | 4.5:1 | Error action text |
| `--primary` | `--background` | 3:1 | Primary icons/borders on page |
| `--border` | `--background` | 3:1 | Visible borders on page |
| `--ring` | `--background` | 3:1 | Focus indicators |

### 1.4 System Preference Detection Required

- ✘ **NEVER** ship a theme system that ignores the user's operating system color scheme preference
- ✘ **NEVER** detect system preference only at page load and then discard the listener
- ✔ **ALWAYS** query `window.matchMedia('(prefers-color-scheme: light)')` on initialization
- ✔ **ALWAYS** attach a persistent `change` event listener so the UI responds instantly when the user toggles their OS between dark and light
- ✔ **ALWAYS** expose three user-selectable modes: **dark**, **light**, and **system** (which follows the OS)

**Rationale**: AT&T applications serve millions of users across devices. Ignoring `prefers-color-scheme` forces every single user to manually configure their preference — a poor UX that violates platform integration expectations.

**BluePearl reference**: `frontend/src/lib/hooks/use-theme.ts` reads from Zustand state, checks `matchMedia`, toggles the `.light` class on `<html>`, and keeps a live `change` listener active for the lifetime of the app.

### 1.5 Theme Parity — Both Modes Must Be Complete

- ✘ **NEVER** introduce a CSS custom property in `:root` (dark) without a corresponding override in `html.light`
- ✘ **NEVER** add a token to the light theme override block without ensuring the dark default exists in `:root`
- ✔ **ALWAYS** maintain identical token counts between the dark default block and the light override block
- ✔ **ALWAYS** audit token parity whenever new tokens are added — a simple line-count comparison catches most drift

**Rationale**: A missing token in one mode silently inherits the other mode's value, producing invisible text (white-on-white), unreadable contrast, or broken visual hierarchy that only surfaces for users of that specific mode.

**Audit technique**:
```bash
# Count tokens per section — numbers should match
grep -c "^\s*--" src/index.css | head -2
# :root section count
# html.light section count
```

### 1.6 CSS Custom Properties Are the Single Source of Truth

- ✘ **NEVER** define token values inside a JavaScript theme object, Tailwind config, or CSS-in-JS runtime and then try to synchronize them back to CSS
- ✘ **NEVER** use Tailwind's `theme()` function or `@apply` with palette colors as the origin of token values
- ✔ **ALWAYS** author all token definitions as plain CSS custom properties in a single CSS file (e.g., `index.css` or `tokens.css`)
- ✔ **ALWAYS** treat framework registrations (Tailwind `@theme`, CSS-in-JS adapters) as downstream consumers of the CSS file — never as producers

**Rationale**: When the CSS file is the single source of truth, tokens are inspectable in browser DevTools, portable across any framework, and auditable with simple grep commands. BluePearl's `frontend/src/index.css` defines every token, and the Tailwind `@theme` block merely re-exports them as utility classes.

---

## II. Mandatory Patterns

### 2.1 Token System Architecture — Dark-First `:root` with `.light` Override

Every theme implementation must follow BluePearl's proven dark-first architecture where `:root` establishes the dark palette as the default and `html.light` selectively overrides only the values that change.

**Required structure in the main CSS file**:

```css
/* === Dark Theme (Default) === */
:root {
  color-scheme: dark;

  /* Surface tokens */
  --background: oklch(0.145 0.014 265.1);
  --foreground: oklch(0.94 0.01 264.5);
  --card: oklch(0.185 0.014 265.1);
  --card-foreground: oklch(0.94 0.01 264.5);
  --popover: oklch(0.185 0.014 265.1);
  --popover-foreground: oklch(0.94 0.01 264.5);

  /* Action tokens */
  --primary: oklch(0.623 0.214 255.1);
  --primary-foreground: oklch(0.975 0.005 255.1);
  --secondary: oklch(0.255 0.03 264.5);
  --secondary-foreground: oklch(0.895 0.008 264.5);

  /* State tokens */
  --muted: oklch(0.24 0.018 265.1);
  --muted-foreground: oklch(0.583 0.016 264.5);
  --accent: oklch(0.295 0.03 265.1);
  --accent-foreground: oklch(0.895 0.008 264.5);
  --destructive: oklch(0.543 0.195 27.3);
  --destructive-foreground: oklch(0.975 0.005 27.3);

  /* Chrome tokens */
  --border: oklch(0.295 0.018 265.1);
  --input: oklch(0.295 0.018 265.1);
  --ring: oklch(0.623 0.214 255.1);
  --radius: 0.5rem;
}

/* === Light Theme (Override) === */
html.light {
  color-scheme: light;

  --background: oklch(0.985 0.002 247);
  --foreground: oklch(0.145 0.014 265.1);
  --card: oklch(0.975 0.002 247);
  --card-foreground: oklch(0.145 0.014 265.1);
  --popover: oklch(0.975 0.002 247);
  --popover-foreground: oklch(0.145 0.014 265.1);

  --primary: oklch(0.488 0.217 264.4);
  --primary-foreground: oklch(0.985 0.002 247);
  --secondary: oklch(0.925 0.012 264.5);
  --secondary-foreground: oklch(0.205 0.018 264.5);

  --muted: oklch(0.935 0.008 264.5);
  --muted-foreground: oklch(0.435 0.02 264.5);
  --accent: oklch(0.935 0.008 264.5);
  --accent-foreground: oklch(0.205 0.018 264.5);
  --destructive: oklch(0.535 0.21 27.3);
  --destructive-foreground: oklch(0.985 0.002 247);

  --border: oklch(0.885 0.008 264.5);
  --input: oklch(0.885 0.008 264.5);
  --ring: oklch(0.488 0.217 264.4);
}
```

**Key architectural rules**:

- `color-scheme` property must appear in both blocks for native form control rendering
- All color values should use the `oklch()` color space for perceptual uniformity across hue adjustments
- Token groups should be organized by purpose (surface, action, state, chrome) with inline comments
- The `:root` block owns the dark defaults; `html.light` overrides only changed values

### 2.2 Theme Application Hook with Live System Preference

Every project must include a theme management hook that synchronizes the user's preference with the DOM. BluePearl's implementation reads from a Zustand store and applies the `.light` class on `<html>`.

**Required behavior**:

1. Accept one of three modes: `'dark'`, `'light'`, or `'system'`
2. When mode is `'system'`, resolve via `matchMedia('(prefers-color-scheme: light)')`
3. Toggle the `.light` class on `document.documentElement`
4. Attach a live `change` listener on the `matchMedia` object so OS-level switches propagate immediately
5. Clean up the listener on unmount or mode change

**BluePearl reference pattern** (`frontend/src/lib/hooks/use-theme.ts`):

```typescript
// Theme application hook — original BluePearl implementation pattern
// Reads the selected mode from application state and applies it to the DOM.
// When 'system' is chosen, a matchMedia listener keeps the UI in sync
// with the operating system's color scheme setting in real time.

import { useEffect } from 'react';

type ThemeMode = 'dark' | 'light' | 'system';

export function useApplyTheme(selectedMode: ThemeMode): void {
  useEffect(() => {
    const htmlElement = document.documentElement;

    const setLightClass = (isLight: boolean) => {
      if (isLight) {
        htmlElement.classList.add('light');
      } else {
        htmlElement.classList.remove('light');
      }
    };

    if (selectedMode !== 'system') {
      setLightClass(selectedMode === 'light');
      return;
    }

    // System mode — resolve from OS preference and listen for changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: light)');
    setLightClass(mediaQuery.matches);

    const onSystemChange = (event: MediaQueryListEvent) => {
      setLightClass(event.matches);
    };

    mediaQuery.addEventListener('change', onSystemChange);
    return () => mediaQuery.removeEventListener('change', onSystemChange);
  }, [selectedMode]);
}
```

### 2.3 SVG and Canvas Theme Resolution Hook

Non-CSS rendering contexts (inline SVG with JavaScript-driven fills, `<canvas>`, WebGL) cannot read CSS custom properties natively. A dedicated hook must bridge the gap.

**Required behavior**:

1. Read computed CSS variable values via `getComputedStyle(document.documentElement)`
2. Observe `<html>` class attribute changes with a `MutationObserver` scoped to `attributeFilter: ['class']`
3. Re-resolve all requested token values when a mutation is detected
4. Return the resolved values as a reactive state object

**BluePearl reference pattern** (`frontend/src/lib/hooks/use-theme-colors.ts`):

```typescript
// SVG/Canvas theme color resolver — original BluePearl implementation pattern
// Provides runtime-resolved CSS variable values for rendering contexts
// that cannot consume CSS custom properties directly.
// Watches for class mutations on <html> to detect theme transitions.

import { useState, useEffect, useCallback, useRef } from 'react';

export function useResolvedThemeColors(tokenNames: readonly string[]) {
  const tokenNamesRef = useRef(tokenNames);

  const resolveCurrentValues = useCallback(() => {
    const computedStyle = getComputedStyle(document.documentElement);
    const resolved: Record<string, string> = {};
    for (const tokenName of tokenNamesRef.current) {
      const rawValue = computedStyle.getPropertyValue(`--${tokenName}`).trim();
      resolved[tokenName] = rawValue;
    }
    return resolved;
  }, []);

  const [themeColors, setThemeColors] = useState(resolveCurrentValues);

  useEffect(() => {
    // Re-resolve when the light/dark class toggles on <html>
    const mutationHandler = () => {
      setThemeColors(resolveCurrentValues());
    };

    const observer = new MutationObserver(mutationHandler);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class'],
    });

    return () => observer.disconnect();
  }, [resolveCurrentValues]);

  return themeColors;
}
```

**Usage in an SVG component**:

```tsx
function ThemedChart() {
  const colors = useResolvedThemeColors(['primary', 'muted', 'destructive']);

  return (
    <svg viewBox="0 0 200 100">
      <rect width="60" height="80" fill={colors.primary} />
      <rect x="70" width="60" height="50" fill={colors.muted} />
      <rect x="140" width="60" height="30" fill={colors.destructive} />
    </svg>
  );
}
```

### 2.4 Syntax Highlighting Token Set

Every theme system that renders code (code blocks, inline code, Lexical/ProseMirror editors, terminal output) must include a dedicated set of syntax highlighting tokens. BluePearl defines 25 syntax tokens covering all common language constructs.

**Minimum required tokens (10)**:

```css
:root {
  --syntax-keyword: oklch(0.748 0.153 303.5);
  --syntax-string: oklch(0.746 0.12 152.3);
  --syntax-number: oklch(0.748 0.118 82.4);
  --syntax-comment: oklch(0.498 0.018 264.5);
  --syntax-function: oklch(0.796 0.148 222.8);
  --syntax-variable: oklch(0.848 0.098 62.5);
  --syntax-operator: oklch(0.698 0.098 32.1);
  --syntax-type: oklch(0.748 0.118 182.3);
  --syntax-property: oklch(0.796 0.098 252.1);
  --syntax-punctuation: oklch(0.598 0.018 264.5);
}

html.light {
  --syntax-keyword: oklch(0.445 0.19 303.5);
  --syntax-string: oklch(0.395 0.14 152.3);
  --syntax-number: oklch(0.445 0.14 82.4);
  --syntax-comment: oklch(0.498 0.025 264.5);
  --syntax-function: oklch(0.39 0.18 222.8);
  --syntax-variable: oklch(0.42 0.12 62.5);
  --syntax-operator: oklch(0.44 0.12 32.1);
  --syntax-type: oklch(0.395 0.14 182.3);
  --syntax-property: oklch(0.42 0.12 252.1);
  --syntax-punctuation: oklch(0.398 0.025 264.5);
}
```

**Extended tokens (recommended for full language coverage)**: `--syntax-tag`, `--syntax-attribute`, `--syntax-selector`, `--syntax-regex`, `--syntax-inserted`, `--syntax-deleted`, `--syntax-class-name`, `--syntax-constant`, `--syntax-decorator`, `--syntax-namespace`, `--syntax-builtin`, `--syntax-char`, `--syntax-symbol`, `--syntax-template-string`, `--syntax-line-highlight`

### 2.5 Scrollbar, Selection, and Focus Ring Theming

Browser chrome elements (scrollbars, text selection highlights, focus indicators) must participate in the theme system. Leaving them at browser defaults creates jarring visual inconsistencies, especially in dark mode where bright scrollbars and blue selection rectangles clash with the dark surface palette.

**Required CSS rules**:

```css
/* Thin scrollbar using semantic tokens */
:root {
  scrollbar-color: var(--muted) var(--background);
  scrollbar-width: thin;
}

/* Text selection uses primary with reduced opacity */
::selection {
  background-color: oklch(from var(--primary) l c h / 0.3);
  color: var(--foreground);
}

/* Focus indicator using the ring token — visible on all backgrounds */
:focus-visible {
  outline: 2px solid var(--ring);
  outline-offset: 2px;
}
```

**BluePearl reference**: `frontend/src/index.css` lines 280-310 define scrollbar theming with `scrollbar-color`, selection highlighting with `::selection`, and focus rings that meet the 3:1 contrast requirement for non-text UI elements.

### 2.6 Component Variant System Built on Semantic Tokens

All component variant definitions (buttons, badges, alerts, inputs) must reference only semantic token utilities. No variant may contain a Tailwind palette class or literal color value.

**Required pattern** (using `class-variance-authority` or equivalent):

```typescript
// Button variants — every color reference resolves through semantic tokens
import { cva } from 'class-variance-authority';

export const buttonStyles = cva(
  [
    'inline-flex items-center justify-center gap-2',
    'rounded-md text-sm font-medium',
    'transition-colors duration-150',
    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
    'disabled:pointer-events-none disabled:opacity-50',
  ].join(' '),
  {
    variants: {
      intent: {
        primary: 'bg-primary text-primary-foreground shadow-sm hover:bg-primary/90',
        danger: 'bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90',
        outline: 'border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground',
        subtle: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        sm: 'h-8 px-3 text-xs',
        md: 'h-9 px-4',
        lg: 'h-10 px-6 text-base',
        icon: 'h-9 w-9',
      },
    },
    defaultVariants: { intent: 'primary', size: 'md' },
  }
);
```

**Verification**: Run `grep -rn "text-blue\|bg-blue\|text-red\|bg-red\|text-green\|bg-green\|text-gray\|bg-gray\|text-slate\|bg-slate" src/components/` — the result should be empty (zero matches) for a compliant codebase.

### 2.7 Tailwind v4 `@theme` Registration (or v3 Config Equivalent)

When using Tailwind CSS, all semantic tokens must be registered as first-class theme values so that utilities like `bg-background`, `text-primary`, and `border-border` work without arbitrary value syntax.

**Tailwind v4 pattern** (CSS-based configuration):

```css
@theme {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-destructive-foreground: var(--destructive-foreground);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --color-sidebar: var(--sidebar);
  --color-sidebar-foreground: var(--sidebar-foreground);
  --color-sidebar-border: var(--sidebar-border);
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
}
```

**Tailwind v3 fallback** (JavaScript-based configuration):

```javascript
// tailwind.config.js — v3 equivalent
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: 'var(--background)',
        foreground: 'var(--foreground)',
        primary: {
          DEFAULT: 'var(--primary)',
          foreground: 'var(--primary-foreground)',
        },
        secondary: {
          DEFAULT: 'var(--secondary)',
          foreground: 'var(--secondary-foreground)',
        },
        muted: {
          DEFAULT: 'var(--muted)',
          foreground: 'var(--muted-foreground)',
        },
        accent: {
          DEFAULT: 'var(--accent)',
          foreground: 'var(--accent-foreground)',
        },
        destructive: {
          DEFAULT: 'var(--destructive)',
          foreground: 'var(--destructive-foreground)',
        },
        border: 'var(--border)',
        input: 'var(--input)',
        ring: 'var(--ring)',
        card: {
          DEFAULT: 'var(--card)',
          foreground: 'var(--card-foreground)',
        },
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
    },
  },
};
```

**Key rule**: The `@theme` block or config file must not contain any literal color values — only `var()` references back to the CSS custom properties defined in Section 2.1.

---

## III. Preferred Patterns (Recommended)

The LLM should adopt these unless the user explicitly overrides.

### 3.1 → No-FOUC Theme Initialization Script

Prevent flash of wrong theme on initial page load by injecting a synchronous script in `<head>` that runs before any CSS or JavaScript bundles parse. This is critical for SSR/SSG frameworks (Next.js, Remix, Astro) where the HTML arrives before client JavaScript hydrates.

**Pattern**:

```html
<!-- Place inside <head> before any stylesheet links -->
<script>
  // Synchronous theme resolver — runs before first paint
  // Reads stored preference from localStorage, falls back to OS preference
  ;(function() {
    try {
      var stored = localStorage.getItem('bluepearl-theme');
      var preferLight = stored === 'light' ||
        (!stored && window.matchMedia('(prefers-color-scheme: light)').matches);
      if (preferLight) document.documentElement.classList.add('light');
    } catch (e) {
      // localStorage may be blocked in private browsing — fall through to CSS default
    }
  })();
</script>
```

**Why this matters**: Without this script, the browser renders `:root` (dark) tokens first, then JavaScript loads, detects the user wants light mode, and toggles `.light` — causing a visible dark-to-light flash. The synchronous script eliminates the flash by setting the class before the first paint frame.

### 3.2 → Reduced Motion Preference Support

Applications with transitions, animations, or scroll-based effects must respect `prefers-reduced-motion`. AT&T applications serve users with vestibular disorders, photosensitive epilepsy, and attention difficulties — motion reduction is an accessibility requirement, not an optional enhancement.

**Pattern**:

```css
/* Disable non-essential motion when user requests it */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**Note**: Essential motion (progress indicators, loading spinners that convey system state) may be exempt, but must be documented in `THEME_EXCEPTIONS.md`.

### 3.3 → High Contrast Mode Support

For users who activate `prefers-contrast: more` at the OS level, provide token overrides that increase border visibility, text weight, and focus ring prominence.

**Pattern**:

```css
@media (prefers-contrast: more) {
  :root {
    --border: oklch(0.50 0.02 265);
    --muted-foreground: oklch(0.73 0.02 265);
    --ring: oklch(0.78 0.24 255);
  }

  html.light {
    --border: oklch(0.38 0.02 265);
    --muted-foreground: oklch(0.28 0.02 265);
    --ring: oklch(0.38 0.24 255);
  }
}
```

### 3.4 → Token Documentation Page

Generate a living visual catalog that renders every token as a color swatch alongside its name, oklch value in both modes, contrast ratio against its paired background, and a usage example. This page serves as the single reference for designers and developers.

**Recommended output**: A React component or static HTML page that iterates over a token manifest array and renders a grid of swatches. The test workflow validates that this catalog stays synchronized with the actual CSS file.

### 3.5 → Programmatic Variants via `color-mix()`

Instead of defining separate hover/active/disabled token variants, use CSS `color-mix()` to derive interactive states algorithmically. This reduces token count and ensures consistent state feedback across all surfaces.

**Pattern**:

```css
/* Darken on hover, darken further on active — works in both light and dark modes */
.btn-primary:hover {
  background-color: color-mix(in oklch, var(--primary) 90%, black);
}

.btn-primary:active {
  background-color: color-mix(in oklch, var(--primary) 80%, black);
}

/* Lighten borders on hover for subtle interactive feedback */
.card:hover {
  border-color: color-mix(in oklch, var(--border) 70%, var(--foreground));
}
```

**Browser support**: `color-mix()` is supported in all evergreen browsers as of 2024. For legacy support, fall back to opacity modifiers (`bg-primary/90`).

### 3.6 → Multi-Brand Token Abstraction

For AT&T applications that serve multiple brands or white-label deployments, add a brand layer above the theme layer using a `data-brand` attribute on the root element.

**Pattern**:

```css
/* Brand layer — loaded dynamically based on deployment config */
:root[data-brand="att-consumer"] {
  --primary: oklch(0.55 0.24 255);
  --primary-foreground: oklch(0.98 0.005 255);
}

:root[data-brand="att-business"] {
  --primary: oklch(0.48 0.18 210);
  --primary-foreground: oklch(0.98 0.005 210);
}

:root[data-brand="firstnet"] {
  --primary: oklch(0.52 0.22 145);
  --primary-foreground: oklch(0.98 0.005 145);
}
```

**Architecture**: Brand CSS files are loaded conditionally via a `<link>` element whose `href` is set at deployment time. The brand layer only overrides action tokens (`--primary`, `--destructive`); surface tokens (`--background`, `--card`) remain consistent for visual cohesion.

---

## IV. Token Inventory

### 4.1 Minimum Required Tokens (20 Core)

Every theme system scaffolded by this archetype must define at minimum these 20 tokens in both `:root` and `html.light`:

| Token | Purpose |
|-------|---------|
| `--background` | Page and application background surface |
| `--foreground` | Default body text color |
| `--card` | Card, panel, and elevated surface backgrounds |
| `--card-foreground` | Text rendered on card surfaces |
| `--popover` | Popover, dropdown, and tooltip backgrounds |
| `--popover-foreground` | Text inside popovers and dropdowns |
| `--primary` | Primary brand and call-to-action color |
| `--primary-foreground` | Text on primary-colored surfaces |
| `--secondary` | Secondary action and neutral emphasis |
| `--secondary-foreground` | Text on secondary surfaces |
| `--muted` | Muted and subtle background surfaces |
| `--muted-foreground` | De-emphasized secondary text |
| `--accent` | Accent highlights and hover states |
| `--accent-foreground` | Text on accent surfaces |
| `--destructive` | Error, danger, and destructive action color |
| `--destructive-foreground` | Text on destructive surfaces |
| `--border` | Default border and separator color |
| `--input` | Form input border and outline color |
| `--ring` | Focus ring and keyboard navigation indicator |
| `--radius` | Default border radius unit |

### 4.2 Extended Tokens (Recommended)

| Token | Purpose |
|-------|---------|
| `--success` | Positive confirmation and success indicators |
| `--success-foreground` | Text on success surfaces |
| `--warning` | Caution and warning indicators |
| `--warning-foreground` | Text on warning surfaces |
| `--info` | Informational callouts and notices |
| `--info-foreground` | Text on info surfaces |
| `--sidebar` | Sidebar and navigation panel background |
| `--sidebar-foreground` | Sidebar text color |
| `--sidebar-border` | Sidebar border and separator |
| `--chart-1` through `--chart-5` | Data visualization categorical palette |

---

## V. Troubleshooting Guide

### 5.1 Flash of Wrong Theme (FOUC)

**Symptom**: Page loads showing the dark theme for a fraction of a second before switching to light (or vice versa).

**Root Cause**: The CSS default (`:root` dark) renders before client JavaScript runs and applies the `.light` class.

**Solution**: Add the synchronous no-FOUC script from Section III.1 inside `<head>` before any `<link>` or `<style>` elements. For Next.js, use `next/script` with `strategy="beforeInteractive"`. For Remix, place it in the `<head>` section of `root.tsx`.

### 5.2 SVG or Canvas Elements Not Responding to Theme Toggle

**Symptom**: SVG fills, strokes, or canvas-drawn colors remain fixed when the user switches between dark and light.

**Root Cause**: SVG `fill` and `stroke` attributes set to literal color values, or canvas `fillStyle` set once at mount and never updated.

**Solution**: Replace literal SVG attributes with `currentColor` where possible, or use the `useResolvedThemeColors` hook from Section II.3 to read computed CSS variable values and re-render on theme change. For canvas, re-draw in the `MutationObserver` callback.

### 5.3 WCAG Contrast Ratio Failures

**Symptom**: Automated accessibility testing (axe-core, Lighthouse) flags text elements as having insufficient contrast.

**Root Cause**: Token values chosen for aesthetic preference without validating the contrast ratio between the foreground and background pair.

**Solution**: Use the test workflow's contrast validation step to check all required pairs from Section I.3. Adjust the oklch lightness channel — for dark mode, foreground lightness should be ≥ 0.85; for light mode, foreground lightness should be ≤ 0.25 for body text.

### 5.4 Token Parity Mismatch Between Modes

**Symptom**: A component renders correctly in dark mode but shows invisible or wrong-colored text in light mode (or vice versa).

**Root Cause**: A new CSS custom property was added to `:root` but the corresponding `html.light` override was forgotten.

**Solution**: Count tokens in each block — they should match. Use the audit command from Section I.5 or run the test workflow which reports parity mismatches automatically.

### 5.5 Tailwind Semantic Utilities Not Recognized

**Symptom**: Classes like `bg-background`, `text-foreground`, or `border-border` produce no styling or trigger Tailwind warnings.

**Root Cause**: The `@theme` block (v4) or `tailwind.config.js` `theme.extend.colors` (v3) is missing the token registration.

**Solution**: Verify Section II.7 registration is present. Restart the Tailwind dev server after config changes — Tailwind caches its class scanning results.

### 5.6 System Preference Not Detected or Not Updating

**Symptom**: The app ignores the OS dark/light mode toggle, or it detects the initial preference but doesn't respond when the user changes it mid-session.

**Root Cause**: Either `matchMedia` is not called, or the `change` event listener is missing or was cleaned up prematurely.

**Solution**: Verify the theme hook from Section II.2 is mounted at the application root (not inside a lazy-loaded route). Ensure the `addEventListener('change', ...)` is registered in the `'system'` mode branch and only cleaned up when the mode changes or the component unmounts.

---

## VI. Security and Performance Checklist

Before shipping any theme system generated by this archetype:

- [ ] No hardcoded color values in any component source file
- [ ] All tokens use semantic purpose-driven names (no palette references)
- [ ] All foreground/background token pairs meet WCAG 2.1 AA contrast ratios in both modes
- [ ] `prefers-color-scheme` detected and honored with live `change` listener
- [ ] Three modes supported: dark, light, system
- [ ] Every token defined in both `:root` (dark) and `html.light` blocks
- [ ] Token counts match between dark and light blocks
- [ ] `color-scheme` CSS property set in both blocks
- [ ] Tailwind `@theme` (v4) or `config` (v3) registers all tokens as utilities
- [ ] Syntax highlighting tokens defined if code rendering is present
- [ ] Scrollbar, text selection, and focus ring themed with semantic tokens
- [ ] No-FOUC initialization script in `<head>` (if SSR/SSG applicable)
- [ ] `prefers-reduced-motion` respected if animations are present
- [ ] SVG/canvas elements use theme resolution hook if dynamically colored
- [ ] Intentional color exceptions documented in `THEME_EXCEPTIONS.md`
- [ ] Token documentation page or catalog is current

---

## VII. Refusal Template

When a user request violates a hard-stop rule, the AI agent must refuse and guide the user toward compliance:

```text
❌ This request violates Hard-Stop Rule {rule_number}: {rule_title}

Specifically: {description_of_the_violation}

To proceed compliantly, you must:
1. {remediation_step_1}
2. {remediation_step_2}

Compliant alternative:
{code_example_showing_correct_approach}

Reference: ui-theme-architect-constitution.md Section I.{subsection}
```

**Example refusal**:

```text
❌ This request violates Hard-Stop Rule 1.1: No Hardcoded Colors in Components

Specifically: The requested component uses `className="bg-slate-900 text-white"` which
embeds Tailwind palette classes directly.

To proceed compliantly, you must:
1. Replace `bg-slate-900` with `bg-background` (semantic surface token)
2. Replace `text-white` with `text-foreground` (semantic text token)

Compliant alternative:
<div className="bg-background text-foreground">...</div>

Reference: ui-theme-architect-constitution.md Section I.1
```

---

## VIII. Related Documents

- **Frontend Scaffolding**: Use `frontend-only` archetype for component library, routing, and state management setup
- **Accessibility Testing**: Use `test-ui-theme-architect` workflow for automated WCAG contrast validation
- **Container Deployment**: Use `container-solution-architect` for containerizing the built frontend
- **BluePearl Reference Implementation**: `frontend/src/index.css`, `frontend/src/lib/hooks/use-theme.ts`, `frontend/src/lib/hooks/use-theme-colors.ts`
- **W3C Design Tokens Community Group**: <https://design-tokens.github.io/community-group/format/>
- **WCAG 2.1 Contrast Requirements**: <https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html>
- **oklch Color Space Reference**: <https://oklch.com/>

---

**Version**: 1.0.0
**Last Updated**: 2026-03-02
**Source**: Generated by Archetype Architect from BluePearl reference implementation
