---
description: Compare Flywheel component choices, layout patterns, form strategies, and integration approaches for building AT&T-branded web applications
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read comparison criteria from:
`${ARCHETYPES_BASEDIR}/flywheel-frontend-architect/flywheel-frontend-architect-constitution.md`

### 2. Identify Comparison Type

Based on $ARGUMENTS, determine what to compare:

| Comparison Type | Examples |
|-----------------|----------|
| **Layout Pattern** | Sidebar + content vs Top nav + content vs Combined layout |
| **Form Strategy** | React Hook Form + Zod vs Formik + Yup vs native HTML forms |
| **Navigation** | Top Navigation vs Sidebar vs Breadcrumb-based vs Tabs |
| **Data Display** | Table vs Card grid vs Tree View for hierarchical data |
| **State Management** | React Query vs SWR vs raw fetch for server state |
| **Overlay Pattern** | Dialog vs Sheet vs Drawer vs Bottom Sheet for secondary content |
| **Notification** | Toast vs Alert vs Inline validation for user feedback |
| **Component Choice** | Autocomplete vs Select vs Command for search/filter UI |
| **Theming Approach** | Single brand vs Multi-brand switching vs Custom token extension |
| **Build/Deploy** | Vite SPA vs Next.js SSR vs Remix for AT&T applications |

### 3. Define Comparison Criteria

Apply Flywheel-aligned evaluation criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Flywheel Compliance** | High | Full compatibility with @forge/ui-tokens, @flywheel/react-icons |
| **Accessibility** | High | WCAG 2.1 AA, keyboard nav, screen reader support |
| **AT&T Brand Alignment** | High | Works with Business/FirstNet/Consumer themes |
| **Component Reuse** | Medium | Leverages existing Flywheel components vs custom code |
| **Mobile Responsiveness** | Medium | Works across AT&T's device range |
| **Developer Experience** | Medium | Ease of implementation, maintainability |
| **Performance** | Medium | Bundle size, rendering efficiency |
| **Full-Stack Readiness** | Medium | Clean API integration points for backend archetypes |

### 4. Analyze Option A

For the first approach, evaluate:

```markdown
## Option A: {name}

### Description
{Brief description of the approach}

### Flywheel Compliance
- Components used: {list of Flywheel components leveraged}
- Token usage: {how semantic tokens are used}
- Icon library: {@flywheel/react-icons compatibility}

### Accessibility
- Keyboard navigation: {built-in or custom}
- ARIA support: {automatic via Flywheel or manual}
- Focus management: {trapping, restoration}

### AT&T Brand Alignment
- Theme switching: {supports Business/FirstNet/Consumer}
- Dark mode: {.dark class compatibility}
- Brand tokens: {uses --fw-* primitives or --primary, etc.}

### Component Reuse
- Pre-built components: {count of Flywheel components used}
- Custom components needed: {count and complexity}
- Block reuse: {any pre-built blocks applicable}

### Mobile Responsiveness
- Mobile pattern: {how mobile is handled}
- Breakpoint strategy: {Flywheel responsive sizes or custom}
- Touch targets: {44×44px minimum}

### Developer Experience
- Setup complexity: {steps to implement}
- Maintenance burden: {ongoing effort}
- Team familiarity: {typical React team knowledge}

### Performance
- Bundle impact: {additional dependencies}
- Render cost: {component count, re-render patterns}

### Full-Stack Readiness
- API integration: {clean boundaries for backend archetype}
- State management: {React Query compatible}
```

### 5. Analyze Option B

Evaluate the second approach using the same template as Step 4.

### 6. Analyze Option C (If Applicable)

If three or more options are being compared, evaluate additional options.

### 7. Generate Comparison Matrix

```markdown
## Comparison Matrix

| Criterion | Option A | Option B | Winner |
|-----------|----------|----------|--------|
| **Flywheel Compliance** | | | |
| Token compatibility | {a} | {b} | {winner} |
| Icon library support | {a} | {b} | {winner} |
| Component reuse | {a} | {b} | {winner} |
| **Accessibility** | | | |
| Keyboard navigation | {a} | {b} | {winner} |
| Screen reader support | {a} | {b} | {winner} |
| Focus management | {a} | {b} | {winner} |
| **AT&T Brand** | | | |
| Multi-brand themes | {a} | {b} | {winner} |
| Dark mode | {a} | {b} | {winner} |
| **Developer Experience** | | | |
| Setup complexity | {a} | {b} | {winner} |
| Maintenance | {a} | {b} | {winner} |
| **Performance** | | | |
| Bundle size | {a} | {b} | {winner} |
| Render efficiency | {a} | {b} | {winner} |
| **Full-Stack Readiness** | | | |
| API integration | {a} | {b} | {winner} |

**Overall Score**: Option A: {score}/10, Option B: {score}/10
```

### 8. Provide Recommendation

```markdown
## Recommendation

### Recommended: {Option A or B}

**Rationale**:
{Why this option best aligns with Flywheel constitution and project needs}

### When to Choose Option A
- {scenario}
- {scenario}

### When to Choose Option B
- {scenario}
- {scenario}

### Implementation Path
{Steps to implement the recommended option using Flywheel components}

### Components to Install
{List of npx shadcn add @forge/<name> commands}
```

---

## Common Comparisons

### Layout: Sidebar vs Top Navigation

| Aspect | Sidebar Layout | Top Navigation Layout |
|--------|---------------|----------------------|
| Component | `@forge/sidebar` | `@forge/top-navigation` |
| Best for | Admin dashboards, complex apps | Customer-facing portals, marketing |
| Mobile | Sheet-based overlay | Hamburger menu (custom) |
| Content area | Maximized horizontal space | Full width |
| AT&T pattern | Internal tools | Public-facing sites |

### Data Display: Table vs Card Grid

| Aspect | Data Table | Card Grid |
|--------|-----------|-----------|
| Component | `@forge/table` | `@forge/card` |
| Best for | Tabular data, sorting, filtering | Visual items, products, summaries |
| Density | High information density | Lower density, more visual |
| Mobile | Horizontal scroll or stacked | Responsive column layout |
| Accessibility | Built-in row selection states | Requires manual ARIA |

### Overlay: Dialog vs Sheet vs Drawer

| Aspect | Dialog | Sheet | Drawer/Bottom Sheet |
|--------|--------|-------|-------------------|
| Component | `@forge/dialog` | `@forge/sheet` | `@forge/drawer` |
| Best for | Confirmations, small forms | Side panels, detail views | Mobile actions, order summaries |
| Position | Centered | Left/right edge | Bottom edge |
| Size | Fixed (sm/md/lg) | Full height, configurable width | Configurable height |
| Mobile | Works but can feel heavy | Covers full screen | Native mobile pattern |

### Form Components: Select vs Autocomplete vs Command

| Aspect | Select | Autocomplete | Command |
|--------|--------|-------------|---------|
| Component | `@forge/select` | `@forge/autocomplete` | `@forge/command` |
| Best for | Small option lists (<20) | Search in large lists | Power user search, actions |
| Search | No built-in search | Client-side filter | Fuzzy search |
| Custom rendering | Limited | Full control via renderOption | Grouped results |
| Keyboard | Arrow keys + Enter | Arrow keys + type-ahead | Cmd+K pattern |

---

## Error Handling

- **Comparison type unclear**: Ask user to clarify which two (or more) approaches they want evaluated
- **Component not in Flywheel**: Note the gap and suggest the closest Flywheel alternative or custom component pattern
- **Framework comparison requested**: Flywheel currently targets Vite SPA — note Next.js/Remix as alternatives with caveats

## Examples

### Example 1: Layout Comparison
```
/compare-flywheel-frontend-architect Compare sidebar layout vs top navigation layout for an internal admin dashboard
```

### Example 2: Form Strategy
```
/compare-flywheel-frontend-architect Compare React Hook Form + Zod vs Formik + Yup for form validation in a Flywheel app
```

### Example 3: Data Display
```
/compare-flywheel-frontend-architect Should I use a data table or card grid for displaying customer accounts?
```

## References

- Constitution: `${ARCHETYPES_BASEDIR}/flywheel-frontend-architect/flywheel-frontend-architect-constitution.md`
