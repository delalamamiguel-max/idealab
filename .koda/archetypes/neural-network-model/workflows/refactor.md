---
description: Refactor neural network code for maintainability, performance, and governance compliance (Neural Network Model)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype neural-network-model --json ` and parse for PYTORCH_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/neural-network-model/templates/env-config.yaml` for refactoring guidelines

### 3. Parse Input
Extract from $ARGUMENTS: code location (training scripts, model modules, data loaders), refactoring goals (modularity, performance, reproducibility, governance compliance), specific pain points (hard-coded values, monolithic code, missing tests, slow training). Request clarification if incomplete.

### 4. Analyze Code Quality

Assess current codebase: code organization (monolithic vs modular structure, separation of concerns), configuration management (hard-coded vs externalized parameters, config file usage), model architecture (reusable components, testable modules), training loop (callback support, checkpoint management), data pipeline (efficiency, reproducibility), testing coverage (unit tests, integration tests, regression tests), MLflow integration (tracking completeness, artifact logging), governance compliance (audit trails, model cards, fairness checks).

Identify refactoring opportunities and technical debt.

### 5. Generate Refactoring Plan

Create modular structure with organized directories (src/models/, src/data/, src/training/, src/utils/, reference/config/, tests/), configuration management (YAML/JSON configs, environment variable support, config validation), model architecture refactoring (composable modules, reusable blocks, unit-tested components), training infrastructure (Trainer class with callbacks, checkpoint management, early stopping, MLflow integration), data module refactoring (DataModule pattern, configurable transforms, efficient data loading), testing framework (pytest structure, fixtures, mocking strategies, CI/CD integration).

Provide file structure diagram and migration plan.

### 6. Implement Key Refactorings

Generate refactored code for priority areas: config-driven model instantiation, modular architecture with testable components, trainer class with callback system, MLflow logging callback, data loading optimization, comprehensive test suite, documentation updates.

Include before/after code examples showing improvements.

### 7. Validate and Report


Verify improvements: run pytest suite, check code coverage, validate MLflow tracking, test reproducibility with seeds, benchmark performance (training time, memory usage).

Generate refactoring report with code quality improvements, performance benchmarks, governance compliance enhancements, migration checklist. Report completion.

## Error Handling

**Large Codebase**: Prioritize incremental refactoring with backward compatibility.

**Breaking Changes**: Provide migration guide and deprecation warnings.

**Test Failures**: Fix issues before completing refactoring, add regression tests.

## Examples

**Example 1**: `/refactor-neural-model Convert monolithic train.py to modular structure` - Output: Organized codebase with src/ structure and config files

**Example 2**: `/refactor-neural-model Add MLflow tracking and callbacks to training loop` - Output: Trainer class with comprehensive logging

**Example 3**: `/refactor-neural-model Optimize data loading pipeline for 3x speedup` - Output: Efficient DataModule with prefetching and caching

## References

