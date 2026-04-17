# Constitution: Python Library Upgrade

## Purpose
Ensure all dependencies are up-to-date, secure, and compatible with the current codebase for Python project.

---

### I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any code or spec that violates these rules:

✘ No unsupported libraries  
✘ No known vulnerabilities in dependencies  
✘ No deprecated APIs in use  
✘ No unpinned versions in production environments  
✘ No upgrades without documenting minimum/maximum supported versions and Python runtime compatibility.
---

### II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

✔ Use semantic versioning for upgrades  
✔ Validate compatibility with existing code  
✔ Run regression tests post-upgrade  
✔ Document upgrade rationale and impact  
✔ Update dependency lock files (e.g., `requirements.txt`, `poetry.lock`, `pip-tools` compilations)  
✔ Publish a version standard (supported major.minor.min patch ranges, EOL dates, required `python_requires`) in `docs/dependency-matrix.md` or equivalent and keep it synchronized with code changes.  
✔ Annotate upgrades with CVE remediation IDs (if applicable) and target release vehicle.

---

### III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

➜ Use automated tools for upgrade detection  
➜ Prefer stable releases over beta versions  
➜ Include changelog references in commit messages  
➜ Notify stakeholders of breaking changes  
➜ Include upgrade tasks in sprint planning

---

### Version
1.1.0

### Last Updated
2025-10-27
