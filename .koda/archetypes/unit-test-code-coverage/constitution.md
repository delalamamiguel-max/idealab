# Constitution: Unit Test Coverage

## Purpose
Ensure every line of code in the Java project is covered by meaningful unit tests. This agent governs the creation, execution, and validation of unit tests to maintain 100% code coverage.

---

### I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any code or spec that violates these rules:

✘ No uncovered methods, branches, or exception paths  
✘ No untestable code (e.g., static blocks, hidden dependencies)  
✘ No tests without assertions  
✘ No ignored or skipped tests in CI/CD  
✘ No reliance on manual testing for core logic

---

### II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

✔ Use a coverage tool (e.g., JaCoCo, Cobertura) integrated with Maven/Gradle  
✔ Write unit tests for all public and private methods using mocking frameworks (e.g., Mockito)  
✔ Validate edge cases, null inputs, and exception handling  
✔ Include tests for all conditional branches and loops  
✔ Run coverage checks in CI/CD pipelines with fail thresholds  
✔ Maintain a coverage report in HTML or XML format  
✔ Provide deterministic mock data fixtures (builders, JSON payloads, stubs) stored under `src/test/resources` or equivalent so tests never depend on production data sources.

---

### III. Preferred Patterns (Recommended)
➜ Use parameterized tests for input variations  
➜ Use test naming conventions (`shouldDoX_whenY`)  
➜ Refactor code to improve testability (e.g., dependency injection)  
➜ Use test data builders or factories for setup  
➜ Track coverage trends over time  
➜ Include coverage badges in README or dashboards

---

Version: 1.1.0  
Last Updated: 2025-10-27