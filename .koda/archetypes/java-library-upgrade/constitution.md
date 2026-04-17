# Constitution: Java Library Upgrade

## Purpose
Ensure all Java dependencies are current, secure, and compatible with the codebase. This agent governs the detection, analysis, and upgrade of outdated libraries.

---

### I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any code or spec that violates these rules:

✘ No use of deprecated or unsupported libraries  
✘ No known vulnerabilities in dependencies (CVEs)  
✘ No unpinned versions in production builds  
✘ No breaking changes without mitigation plan  
✘ No upgrade without regression testing

---

### II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

✔ Use Maven/Gradle plugins to detect outdated libraries  
✔ Document upgrade rationale and changelog references  
✔ Validate compatibility with existing APIs  
✔ Update `pom.xml` or `build.gradle` with new versions  
✔ Run unit, integration, and regression tests post-upgrade  
✔ Include upgrade tasks in sprint planning or backlog  
✔ Harden concurrency upgrades with lock timeouts, deadlock detection hooks, and guaranteed lock release (`try/finally` or `tryLock`)  
✔ Ensure upgraded libraries align with approved Java integration patterns (e.g., Builder, Optional, CompletableFuture) and refactor call sites accordingly

---

### III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

➜ Use semantic versioning for upgrades  
➜ Prefer stable releases over beta/RC versions  
➜ Automate detection using tools like `Versions Maven Plugin`, `OWASP Dependency-Check`, or `Dependabot`  
➜ Notify stakeholders of breaking changes  
➜ Maintain a migration guide for major upgrades  
➜ Adopt modern Java language patterns when modernizing APIs (e.g., sealed interfaces, records, pattern matching) to capitalize on the new library capabilities

---

### Version
1.0.0

### Last Updated
2025-10-27
