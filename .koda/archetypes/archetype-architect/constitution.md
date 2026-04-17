# Archetype Architect Constitution

## Purpose

Define foundational principles and hard-stop rules for the Archetype Architect archetype, which helps create new archetypes in the vibe_cdo system.

**Domain:** Meta-architecture, code generation, workflow design  
**Use Cases:** Creating new archetypes, extending vibe_cdo capabilities, standardizing archetype patterns

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any code that violates:

- ✘ **No incomplete archetypes**: Never create an archetype without all 6 workflow files (scaffold, debug, refactor, test, compare, document)
- ✘ **No missing constitution**: Every archetype must have a constitution file with hard-stop rules, mandatory patterns, and preferred patterns
- ✘ **No missing metadata**: Every archetype must have a manifest.yaml at its root with name, display_name, description, keywords, and workflows
- ✘ **No slug inconsistency**: Archetype slug must be identical across all files (directory name, workflow files, constitution, metadata key)
- ✘ **No duplicate slugs**: Never create an archetype with a slug that already exists in the same category
- ✘ **No insufficient keywords**: Manifest must have minimum 5 keywords for effective discovery
- ✘ **No weak constitutions**: Constitution must have minimum 3 hard-stop rules, 5 mandatory patterns, and 2 preferred patterns
- ✘ **No simulation-less validation**: test-{archetype-slug} workflow must include Phase 2 simulation testing that actually executes the archetype to validate effectiveness
- ✘ **No orchestration-less generation**: scaffold-{archetype-slug} workflow must use discover-archetype.py for sub-tasks when confidence ≥ threshold (0.80 for scripts, 0.75 for docs)
- ✘ **No platform-specific scripts without wrappers**: All bash scripts must have PowerShell equivalents or use cross-platform Python wrappers
- ✘ **No hardcoded OS assumptions**: Never assume Unix/Linux environment; archetypes must work on Windows, Mac, and Linux

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify:

- ✔ **Kebab-case slugs**: All archetype slugs must use kebab-case format (e.g., "kubernetes-operator-builder")
- ✔ **YAML frontmatter**: All workflow files must have valid YAML frontmatter with description field
- ✔ **$ARGUMENTS placeholder**: All workflow files must use $ARGUMENTS to receive user input
- ✔ **Execution Steps section**: All workflow files must have "## Execution Steps" section with numbered steps
- ✔ **Error Handling section**: All workflow files must have "## Error Handling" section
- ✔ **Examples section**: All workflow files must have "## Examples" section with 2-3 concrete examples
- ✔ **References section**: All workflow files must have "## References" section linking to constitution
- ✔ **Turbo annotations**: Use `// turbo` for safe auto-executable steps (validation, environment checks)
- ✔ **Constitution structure**: Constitution must have three sections: I. Hard-Stop Rules, II. Mandatory Patterns, III. Preferred Patterns
- ✔ **Environment config sections**: env-config.yaml must have performance, variables, and validation sections
- ✔ **Index updates**: After creating archetype, update all 4 INDEX.md files (category, main, constitution, templates)
- ✔ **Discovery testing**: Test archetype discovery with primary keywords and verify ≥80% confidence
- ✔ **File naming convention**: Workflow files must follow pattern: `{action}-{archetype-slug}.md`
- ✔ **Simulation testing**: test workflow must design representative task, execute target archetype, and generate reasoning trace
- ✔ **Reasoning traces**: test workflow must document execution log, issues found, and recommendations for improvement
- ✔ **Orchestration integration**: scaffold workflow must delegate sub-tasks to specialized archetypes using discover-archetype.py
- ✔ **Confidence-based routing**: Use 0.80 threshold for scripts/tests, 0.75 for docs, 0.85 for infrastructure
- ✔ **Cross-platform script execution**: Use Python wrappers or conditional OS detection for all validation/utility scripts
- ✔ **Virtual environment detection**: Detect and use correct Python executable path based on OS (Windows: `.venv\Scripts\python.exe`, Unix/Mac: `.venv/bin/python`)
- ✔ **Path normalization**: Use `os.path.join()` or `pathlib.Path` for all file paths; never hardcode `/` or `\` separators
- ✔ **Platform compatibility testing**: Test workflows include cross-platform validation for Windows, Mac, and Linux

## III. Preferred Patterns (Recommended)

The LLM **should adopt** unless user overrides:

- ➜ **Rich examples**: Include 3-5 examples per workflow showing different use cases
- ➜ **Detailed error handling**: Provide specific error messages and recovery steps
- ➜ **Discovery optimization**: Add high-confidence phrases to metadata for better routing
- ➜ **Cross-references**: Link related archetypes in documentation
- ➜ **Version tracking**: Include version number and last updated date in constitution
- ➜ **Validation scripts**: Reference existing validation scripts (validate_env.py)
- ➜ **Progressive disclosure**: Start with simple examples, then show advanced usage
- ➜ **Category alignment**: Choose category that best fits archetype's primary purpose
- ➜ **Reuse patterns**: Study similar archetypes and adapt proven patterns
- ➜ **Test-driven creation**: Create test workflow first to define validation criteria
- ➜ **Python-first approach**: Prefer Python scripts over bash/PowerShell for maximum portability
- ➜ **OS detection utility**: Create reusable OS detection helper for complex platform logic
- ➜ **Graceful degradation**: Provide fallbacks when platform-specific features unavailable
- ➜ **Platform documentation**: Include platform requirements and OS-specific instructions in generated docs

---

## IV. Cross-Platform Compatibility Guidelines

### Script Execution
- **Python-first**: Use Python scripts for validation, utilities, and automation
- **Dual scripts**: If bash/PowerShell required, provide both versions
- **OS detection**: Use conditional logic to route to correct script

### Path Handling
- **Use pathlib**: `from pathlib import Path` for all file operations
- **Avoid hardcoded separators**: Never use `\` or `/` directly in paths
- **Normalize paths**: Use `os.path.normpath()` for user-provided paths

### Virtual Environments
- **Detect activation**: Check for `.venv` directory and use correct Python path
- **Document requirements**: Specify Python version requirements clearly

### Testing
- **Platform matrix**: Test on Windows, Mac, and Linux
- **CI/CD coverage**: Include all platforms in automated testing
- **User feedback**: Collect platform-specific issues from users

---

**Version**: 1.3.0  
**Last Updated**: 2026-01-18  
**Source**: Generated for Archetype Architect meta-archetype

**Changelog:**
- v1.3.0 (2026-01-18): Added cross-platform compatibility hard-stop rules, mandatory patterns, and Section IV guidelines
- v1.2.0 (2025-01-06): Added orchestration hard-stop rule and mandatory patterns for sub-task delegation
- v1.1.0 (2025-01-06): Added simulation testing hard-stop rule and mandatory patterns
- v1.0.0 (2024-12-27): Initial constitution
