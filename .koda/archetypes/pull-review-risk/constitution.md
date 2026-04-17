# Constitution: Pull Review Risk Analysis

## Purpose
Ensure comprehensive identification and remediation of production risks and security vulnerabilities in pull requests, safeguarding system reliability, data integrity, and user trust through structured governance and quality gates.

---

### I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any code or spec that violates these rules:

✘ No insecure deserialization of untrusted data  
✘ No weak cryptographic algorithms or improper key management  
✘ No hardcoded credentials, secrets, or tokens  
✘ No use of dangerous APIs (e.g., `Runtime.exec`, `System.exit`) without strict validation  
✘ No unvalidated process exits or error handling gaps  
✘ No performance bottlenecks due to memory leaks or inefficient resource management  
✘ No improper use of reflection exposing internal logic

---

### II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

✔ Use static analysis tools (e.g., SpotBugs, SonarQube) to scan for serialization, security, and performance issues  
✔ Validate all external inputs and outputs, especially in serialization and deserialization  
✔ Use secure cryptographic libraries and enforce strong algorithms  
✔ Store secrets securely using environment variables or vaults  
✔ Review and document all uses of reflection and dangerous APIs  
✔ Implement robust error and exception handling with logging and monitoring  
✔ Optimize memory usage and resource management in performance-critical code  
✔ Log exceptions as error with 3rd party interfaces

---

### III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

➜ Automate risk and vulnerability scanning in CI/CD pipelines  
➜ Use dependency management tools to detect outdated or vulnerable libraries  
➜ Document all security and stability fixes with references to CVEs or issue trackers  
➜ Include security and stability unit tests, including fuzzing for serialization  
➜ Notify stakeholders of critical risks and remediation timelines  
➜ Maintain a production risk response playbook  
➜ Apply thread safety analysis for concurrent code (e.g., FindBugs concurrency checks)

---

### IV. Review & Reporting Instructions

**Scope:**
- Scan all files in target branch for production risks: serialization, error handling, performance, hardcoded values, security flaws
- Review all merged pull requests for production risks or regressions
- Assess PRs against governance matrix with standardized notation

**Output Requirements:**
- Generate comprehensive HTML report categorizing findings by type (performance, security, stability) and severity
- Include governance matrix with risk scores and action items
- Provide constitution compliance assessment (Hard-Stop, Mandatory, Preferred)
- Document PR metadata: modules, change types, risk level, status
- Suggest quality gate tests and process improvements

**Standard Notation:**
- **Hard-Stop Flags:** HS-Secret, HS-Deserial, HS-Crypto, HS-API, HS-PII, HS-Auth, HS-Network, HS-Tests, HS-CVE, HS-Loop
- **Mandatory Gaps:** M-Deps, M-Docs, M-Config, M-Logging, M-Exceptions, M-Threading, M-DataModel, M-Pipeline, M-Validation, M-Tests

---

Version: 1.0.0  
Last Updated: 2025-11-19
