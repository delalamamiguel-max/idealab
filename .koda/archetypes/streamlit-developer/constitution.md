# Streamlit Developer Constitution

## Purpose

This constitution defines the foundational principles and hard-stop rules for the Streamlit Developer archetype, which generates production-ready data applications adhering to AT&T brand guidelines.

**Source**: Created for data application development with Streamlit/Python stack and AT&T brand compliance

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any code or design that violates these rules:

- ✘ **No hardcoded secrets**: Do not include API keys, credentials, or secrets directly in code; use `.streamlit/secrets.toml` or environment variables.
- ✘ **AT&T Blue dominance**: Do not create designs where AT&T Blue (#009FDB) is not the dominant color in custom themes.
- ✘ **No non-ATT fonts**: Do not use fonts other than ATT Aleck family (exception: system fallbacks only).
- ✘ **No public licenses**: Do not use public licenses, always use AT&T Proprietary.
- ✘ **No missing input validation**: Do not accept user input without validation.
- ✘ **No accessibility violations**: Do not omit `help` parameters in widgets or ignore color contrast.
- ✘ **HTTPS enforcement**: Do not deploy without HTTPS in production.
- ✘ **No SQL injection**: Do not construct SQL queries with string concatenation; use parameterized queries.
- ✘ **No incompatible dependency versions**: Do not specify Python package versions without verifying compatibility.
- ✘ **No plaintext or weak password storage**: Never store user passwords or secrets without strong hashing.
- ✘ **No logging of secrets or PII**: Do not log tokens, passwords, SSNs, credit card numbers, emails, phone numbers, or access keys.
- ✘ **No use of eval/new Function/dynamic code execution**: Prohibit `eval` or Python `exec` on user-influenced data.
- ✘ **No unsanitized file uploads**: Disallow accepting files without size/type validation.
- ✘ **No unbounded pagination/queries**: Always enforce limits and pagination; refuse requests without bounds.
- ✘ **No silent error swallowing**: Disallow catching exceptions without logging structured diagnostics.

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

### Brand Compliance
- ✔ **ATT Aleck font**: Configure Streamlit theme to use sans serif font family.
- ✔ **AT&T color palette**: Use AT&T Blue, White, Cobalt, Lime, Mint as defined in ATT_COLORS.md.
- ✔ **Theme Configuration**: Create `.streamlit/config.toml` with AT&T brand colors.
  - Primary Color: #009FDB
  - Background Color: #FFFFFF
  - Secondary Background Color: #F2F2F2
  - Text Color: #212121

### Application Architecture
- ✔ **Multi-page App Structure**: Use `pages/` directory for multi-page applications.
- ✔ **Session State Management**: Use `st.session_state` for state persistence across reruns.
- ✔ **Caching**: Use `@st.cache_data` for data fetching and `@st.cache_resource` for connections/models.
- ✔ **Component Modularization**: Break down complex UIs into functions or custom components.
- ✔ **Error Handling**: Use `try-except` blocks with `st.error` for user feedback.
- ✔ **Loading States**: Use `st.spinner` or `st.status` for long-running operations.

### Data Handling
- ✔ **Pandas Optimization**: Use appropriate dtypes (category, int8/16/32) to minimize memory usage.
- ✔ **Vectorization**: Prefer vectorized operations over loops for data manipulation.
- ✔ **Input Validation**: Validate widget inputs before processing.

### Python Dependency Management
- ✔ **Version pinning**: Pin all production dependencies to specific versions in requirements.txt.
- ✔ **Compatibility verification**: Use tested version combinations.
- ✔ **Lock file usage**: Generate a deterministic lock (e.g., `requirements.lock`).

### Security
- ✔ **Secrets Management**: Store secrets in `.streamlit/secrets.toml` (gitignored).
- ✔ **Input sanitization**: Sanitize all user inputs.
- ✔ **Least Privilege**: Database users should have minimum necessary permissions.

## III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

- ➜ **Responsive Layout**: Use `st.columns` for responsive layouts that adapt to screen size.
- ➜ **Progressive Disclosure**: Show advanced options behind expandable sections (`st.expander`).
- ➜ **Meaningful Feedback**: Provide toast notifications (`st.toast`) for quick confirmations.
- ➜ **Download Options**: Offer data export with `st.download_button` for user-generated reports.
- ➜ **Custom Components**: Create reusable components for complex UI patterns.
- ➜ **Performance Monitoring**: Add execution time logging for data operations.

---

**Version**: 1.0.0
**Last Updated**: 2025-01-28
**Source**: Created for Streamlit data application development with AT&T brand compliance
