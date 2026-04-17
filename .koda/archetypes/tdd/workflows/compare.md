---
description: "ANALYSIS ONLY — Compare TDD approaches and testing strategies for a given subject. NEVER generate code, files, or run commands. Always output a comparison matrix regardless of user prompt content."
---

User input: $ARGUMENTS

## ⛔ WORKFLOW OVERRIDE — READ FIRST

> **This workflow was SELECTED by the user. Selection of this workflow overrides the user's prompt intent.**
>
> No matter what the user's prompt says — even if it says "build", "create", "implement", "scaffold", "code", "generate", "write", "deploy", or any other action verb — **this workflow ALWAYS produces a COMPARISON ANALYSIS DOCUMENT and NOTHING else.**
>
> The user chose `tdd-compare`. That choice means: **show me the comparison**. Respect the workflow selection, not the literal wording of the prompt.
>
> - If the user's prompt contains implementation language (e.g., "build me a user authentication service"), **extract the SUBJECT** ("user authentication service") **as the comparison topic** and produce a comparison of TDD approaches for that subject. Do NOT act on the verb.
> - If the user's prompt is purely a question (e.g., "which is better, BDD or classic TDD?"), treat it as a comparison request between the mentioned TDD approaches.
>
> **There are ZERO exceptions to this rule. No prompt wording can override this workflow's analysis-only behavior.**

## Behavioral Rules

> **⛔ ABSOLUTE RULE — THIS WORKFLOW NEVER WRITES CODE. NO EXCEPTIONS.**
>
> This workflow produces **ONLY a comparison plan file**. It does not — under any circumstances, regardless of the user's prompt — generate, write, scaffold, or output code, scripts, configuration files, directories, or any implementation artifact.
>
> - **DO NOT** write, generate, scaffold, or output any code, scripts, or files.
> - **DO NOT** create directories, install packages, or execute commands.
> - **DO NOT** use `edit_file`, `write_file`, `run_terminal_command`, or any file-modifying tools.
> - **DO NOT** start coding even if the user's prompt explicitly asks to "build", "create", "implement", "scaffold", "code", "generate", "write", "deploy", or any other action verb. Extract the **subject** as the comparison topic and produce a comparison — never act on the verb.
> - **ALWAYS** present findings as a structured comparison plan with a comparison matrix.
> - **ALWAYS** provide narrative comparison text explaining the trade-offs, strengths, and weaknesses of each solution.
> - Your **ONLY** output is a formatted analysis containing: identified solutions, component mappings, a star-rated comparison matrix, narrative comparison, and a recommendation.
> - **MANDATORY**: Every response MUST end with "Next Steps" section directing the user to choose either `tdd-scaffold` (for new implementation) or `tdd-refactor` (for refactoring existing code) to proceed with their chosen solution.
> - If the user asks you to "build", "implement", "scaffold", or "refactor" after comparing, **DO NOT** start coding — remind them to explicitly invoke the appropriate workflow (`tdd-scaffold` or `tdd-refactor`).
> - **If you are ever uncertain whether an action counts as "coding"** — it does. Do not do it. Only produce the comparison plan document.

## Execution Steps

### 0. Parse Input

Extract solution requirements and comparison criteria from $ARGUMENTS.

Identify:
- What solutions are being compared
- What dimensions to compare on (performance, cost, complexity, etc.)
- Any specific requirements or constraints
- Technology preferences or limitations

### 0.5. Document Assumptions

Explicitly state assumptions made during comparison. If user hasn't provided these, use reasonable defaults and document them:

- **Expected scale:** Users, data volume, transactions/sec
- **Team expertise:** Skill level with relevant technologies
- **Budget constraints:** Infrastructure and operational budget
- **Timeline requirements:** Time to market, delivery deadlines
- **Existing infrastructure:** Current tech stack and platforms
- **Compliance requirements:** Regulatory, security, data governance needs

**Skip context inference if:**
- User provides abstract/theoretical comparison request
- No specific files or directories are referenced
- Request is purely conceptual (e.g., "compare microservices vs monolith")

### 1. Infer Context from User's Assets

**Before discovering components, analyze the user's context to augment queries.**

**If user references a PROJECT or DIRECTORY:**
```
Analyze directory structure to infer composition:
- Look for package.json, requirements.txt, pom.xml → Application type
- Look for .tf, terraform/ → Infrastructure as Code
- Look for .py + mlflow/, model/ → ML/Data Science
- Look for Dockerfile, helm/, k8s/ → Container/Kubernetes
- Look for .sql, dbt_project.yml → Data Engineering
- Look for airflow/, dags/ → Orchestration
- Look for tests/, pytest.ini → Testing focus
- Look for manifest.yaml + constitution.md → Archetype

Generate context description:
"Project composition: {inferred_type} with {key_technologies}"
```

**If user references a FILE:**
```
Analyze file to infer purpose and framework from imports/content:
- .py → Python (check imports for framework: fastapi, pyspark, sklearn, etc.)
- .sql → SQL queries
- .tf → Terraform infrastructure
- .tsx/.jsx → React frontend
- .yaml/.yml → Configuration (check content: k8s, airflow, etc.)
- .sh/.bash → Automation scripts
- .java → Java (check imports: Spring, Maven, etc.)
- .md → Documentation

Generate context description:
"File type: {extension}, Purpose: {inferred_purpose}, Framework: {detected_framework}"
```

**Build Augmented Query:**
```
${AUGMENTED_QUERY} = "${CONTEXT_DESCRIPTION}. User request: $ARGUMENTS"
```

### 2. Discover Components via Keyword Matching

**Score each component against the user's query using this process:**

1. **Exact name match** in query → +50 points
2. **Display name match** in query → +30 points
3. **Keyword match** (exact) → +10 points per keyword
4. **Keyword partial match** (hyphenated sub-word) → +3 points per partial
5. **Description word overlap** (words ≥4 chars) → +2 points per shared word
6. **File context keyword match** (if file provided) → +5 points per keyword

Select all components scoring > 0 and rank by score descending.

### 3. Identify TDD Approach Patterns

Map the subject to applicable TDD approach patterns from the catalog below. Select the patterns most relevant to the subject's domain and team context:

**Pattern: Classic TDD — Inside-Out (Detroit / Chicago School)**
- Categories: Unit Testing → Refactoring → Integration
- Components: unit-test-code-coverage, code-reviewer, regression-test-coverage, quality-guardian
- Method: Write smallest failing unit test → make it pass with minimal code → refactor
- Cycle: Red → Green → Refactor
- Use cases: Algorithm-heavy logic, pure functions, business rules, data transformations, utility libraries
- Frameworks: pytest, JUnit, Jest, Mocha, NUnit, RSpec

**Pattern: Outside-In TDD (London School / Mockist)**
- Categories: Integration Testing → Mocking → Unit Testing
- Components: unit-test-code-coverage, regression-test-coverage, integration-specialist, code-reviewer
- Method: Start from high-level acceptance/integration test → use mocks/stubs for collaborators → drive implementation inward
- Cycle: Acceptance Test (failing) → Unit Test → Implement → Pass Acceptance Test
- Use cases: API development, layered architectures, microservices, dependency-heavy services
- Frameworks: pytest with unittest.mock, Mockito, Sinon, WireMock, jest.mock()

**Pattern: BDD (Behavior Driven Development)**
- Categories: Acceptance Testing → Collaboration → Documentation
- Components: unit-test-code-coverage, regression-test-coverage, documentation-evangelist, jira-user-stories
- Method: Define behavior in Given/When/Then scenarios → write step definitions → implement to pass
- Cycle: Feature File → Step Definitions → Implementation → Living Documentation
- Use cases: User-facing features, API behavior specification, cross-team collaboration, living documentation
- Frameworks: Cucumber, SpecFlow, Behave, Pytest-BDD, Gherkin

**Pattern: ATDD (Acceptance Test Driven Development)**
- Categories: Acceptance Testing → Requirements → Software Quality
- Components: regression-test-coverage, jira-user-stories, documentation-evangelist, unit-test-code-coverage, quality-guardian
- Method: Define acceptance criteria first → automate criteria as tests → implement until all tests pass
- Cycle: Acceptance Criteria → Automated Test → Implementation → Validation
- Use cases: Customer-specified requirements, regulated environments, end-to-end delivery pipelines
- Frameworks: FitNesse, Robot Framework, Cucumber, Selenium with page objects, Playwright

**Pattern: Contract-First TDD**
- Categories: API Testing → Integration → Documentation
- Components: integration-specialist, unit-test-code-coverage, documentation-evangelist, aks-devops-deployment
- Method: Define API contract (OpenAPI/Pact) → write consumer/provider contract tests → implement to satisfy
- Cycle: Contract Definition → Consumer Test → Provider Test → Implementation
- Use cases: Microservices, multi-team APIs, third-party integrations, consumer-driven contract testing
- Frameworks: Pact, Spring Cloud Contract, OpenAPI Generator, Prism, Dredd

**Pattern: Property-Based TDD**
- Categories: Unit Testing → Generative Testing → Data Quality
- Components: unit-test-code-coverage, quality-guardian, data-validation, interpretability-analyst
- Method: Define invariants and properties that must always hold → generate test cases automatically → implement
- Cycle: Property Definition → Automated Case Generation → Shrinking to Minimal Failure → Fix
- Use cases: Data transformations, serialization/parsing, math operations, protocol implementations
- Frameworks: Hypothesis (Python), fast-check (JS/TS), jqwik (Java), ScalaCheck

**Pattern: TDD for Data Pipelines**
- Categories: Data Engineering → Software Quality → Data Governance
- Components: unit-test-code-coverage, quality-guardian, data-pipeline-builder, transformation-alchemist, data-validation
- Method: Write schema/contract tests → write transformation unit tests → implement pipeline stages
- Cycle: Data Contract → Pipeline Unit Test → Integration Test → Quality Gate
- Use cases: ETL pipelines, data ingestion, transformation logic, data quality enforcement
- Frameworks: pytest + PySpark testing, dbt tests, great-expectations, deequ, pandera

**Pattern: TDD for ML Models**
- Categories: ML Testing → Model Validation → ML Operations
- Components: unit-test-code-coverage, language-model-evaluation, model-architect, quality-guardian, model-ops-steward
- Method: Define evaluation metric thresholds → write model evaluation test harness → train/tune until tests pass
- Cycle: Metric Specification → Evaluation Tests → Model Training → Threshold Validation
- Use cases: Model training pipelines, feature engineering validation, inference testing, evaluation harnesses
- Frameworks: pytest, MLflow evaluation, Deepchecks, Evidently, great-expectations

### 4. Generate Alternative Solutions

For each identified pattern, build solution alternatives:

**Consider Hybrid Solutions:**
- Can components from different TDD patterns be combined (e.g., Classic TDD for unit layer + BDD for acceptance layer)?
- Are there phased approaches (start with Classic TDD, evolve to BDD as team matures)?
- Document hybrid approach as additional solution when applicable
- Identify adoption paths between TDD strategies

**Component Identification via Keywords:**

| Domain | Keywords |
|--------|----------|
| TDD approach | TDD, test-driven, red-green-refactor, unit-first, classic, Detroit, Chicago, inside-out |
| Outside-In TDD | outside-in, London, mockist, top-down, acceptance-first, collaboration, double-loop |
| BDD | BDD, behavior, gherkin, cucumber, given-when-then, scenario, step-definition, living-doc |
| ATDD | ATDD, acceptance, acceptance-criteria, FitNesse, robot-framework, end-to-end, stakeholder |
| Contract testing | contract, pact, consumer-driven, provider, API contract, OpenAPI, Dredd, Prism |
| Property-based | property-based, hypothesis, fuzz, invariant, generative, shrinking, QuickCheck |
| Test coverage | coverage, code-coverage, branch-coverage, mutation, threshold, jacoco, istanbul |
| Mocking | mock, stub, spy, fake, double, test-double, mockito, sinon, unittest.mock, wiremock |
| Test frameworks | pytest, junit, jest, mocha, nunit, rspec, jasmine, vitest, spock, testify |
| Data ingestion | pipeline, ingest, load, extract, import, source, batch, streaming |
| Data transformation | transform, process, clean, enrich, aggregate, ETL, pyspark, spark, SQL |
| Data quality | validate, quality, check, test, verify, governance, threshold, deequ |
| ML training | model, train, machine learning, ML, algorithm, hyperparameter, experiment |
| ML inference | serve, deploy, predict, inference, endpoint, AKS, scoring |
| ML monitoring | drift, monitor, model-ops, lifecycle, compliance, retrain |
| Frontend | UI, frontend, React, Vue, Angular, web app, SPA, SSR |
| Backend API | API, REST, GraphQL, backend, service, endpoint, FastAPI |
| Full-stack app | application, app, web, fullstack, maker |
| Database/SQL | SQL, database, query, schema, data store, Snowflake, CTE |
| Infrastructure | deploy, infrastructure, Kubernetes, container, cloud, Terraform, IaC |
| CI/CD | CI, CD, pipeline, build, release, deploy, microservice |
| Security | security, vulnerability, CVE, OWASP, secret, remediation, scan |
| Testing | test, coverage, unit, regression, load, quality assurance |
| Code review | review, pull request, risk, code quality, audit |
| Documentation | document, docs, guide, readme, release notes, changelog |
| User stories | JIRA, user story, acceptance criteria, backlog, requirements |

**For each solution approach, document:**
- Component list with specific component names from the catalog
- Technology choices for each component
- Integration points between components
- Special considerations or trade-offs

### 5. Create Comparison Matrix (MANDATORY)

> **This step is REQUIRED. Every response MUST include a comparison matrix table.**
> Do not skip this step. Do not replace it with prose. The matrix must be a markdown table.

Compare TDD approaches across key dimensions relevant to test-driven development:

**Feedback Speed**
- Test execution time (unit ms vs integration seconds vs e2e minutes)
- Feedback loop latency during development cycle
- IDE/tooling support for immediate in-editor feedback
- Parallelization support in CI pipelines

**Adoption Cost**
- Learning curve for the development team
- Tooling, framework, and infrastructure setup effort
- Time to establish team conventions and practices
- Training, coaching, and onboarding requirements

**Complexity**
- Test setup and teardown overhead
- Mocking, stubbing, and test-double complexity
- Test scenario design and maintenance difficulty
- Ceremony overhead (e.g., feature files, step definitions)

**Refactoring Safety**
- Confidence tests catch regressions when implementation changes
- Test brittleness (how often tests break for non-functional reasons)
- Coverage of edge cases, boundary conditions, and error paths
- Ability to safely modify and evolve the codebase over time

**Coverage Depth**
- Behavioral coverage of functional requirements
- Validation of integration points and contracts
- End-to-end scenario and acceptance criteria coverage
- Property/invariant coverage for data correctness

**Team Collaboration**
- Shared understanding between Dev, QA, and Business Analysts
- Test scenarios readable and verifiable by non-developers
- Degree to which stakeholders can participate in test definition
- Support for cross-team contract and API collaboration

**Developer Experience**
- IDE tooling, test runner, and debugging support
- Clarity and readability of failing test messages
- Test report, coverage report, and documentation quality
- Integration with CI/CD pipelines and pull request workflows

**Rate each dimension** per solution using this scale:
- ⭐⭐⭐⭐⭐ (5 points): Excellent - Best-in-class capability
- ⭐⭐⭐⭐ (4 points): Good - Exceeds requirements
- ⭐⭐⭐ (3 points): Acceptable - Meets requirements adequately
- ⭐⭐ (2 points): Poor - Significant limitations
- ⭐ (1 point): Critical Issues - Major concerns

**Required Matrix Format (always output this):**
```
| Dimension            | Solution A (name) | Solution B (name) | Winner |
|----------------------|-------------------|-------------------|--------|
| Performance          | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | A or B |
| Cost                 | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | A or B |
| Complexity           | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | A or B |
| Reliability          | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | A or B |
| Scalability          | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | A or B |
| Security             | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | A or B |
| Developer Experience | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | A or B |
| Time to Market       | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | A or B |
| Vendor Lock-in       | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | A or B |
| Use Case Fit         | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ | A or B |
| **TOTAL SCORE**      | **X/100**         | **X/100**         | A or B |
```
Add or remove rows as appropriate for the specific comparison. Always include at least 5 dimensions plus TOTAL SCORE.

**TOTAL SCORE Calculation:**
- Sum all dimension scores for each solution
- Convert to percentage: (Total Points / (Number of Dimensions × 5)) × 100
- Display as: **X/100** where X is the percentage rounded to nearest integer
- Example: If 10 dimensions with scores summing to 42 points: (42/50) × 100 = **84/100**

**For 3+ Solutions:**
Use extended format with additional columns:
```
| Dimension       | Sol A | Sol B | Sol C | Best Choice |
|-----------------|-------|-------|-------|-------------|
| Performance     | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | A, C (tie)  |
| **TOTAL SCORE** | **X/100** | **X/100** | **X/100** | A |
```

### 6. Provide Narrative Comparison (MANDATORY)

> **This step is REQUIRED. Every response MUST include narrative comparison text.**
> Do not skip this step. The comparison matrix alone is not sufficient.

**Write a narrative comparison that includes:**

- **Strengths and Weaknesses:** For each solution, explain what it does well and where it falls short
- **Trade-off Analysis:** Describe the key trade-offs between solutions (e.g., "Solution A trades higher cost for better performance")
- **Use Case Fit:** Explain which solution is best suited for which scenarios
- **Risk Assessment:** Identify risks specific to each solution and how to mitigate them
- **Decision Criteria:** What factors should drive the choice between solutions

**Format:** 2-4 paragraphs of prose that synthesizes the comparison matrix into actionable insights.

### 7. Provide Recommendations

Based on comparison matrix and narrative analysis, recommend optimal solution:

**Analysis:**
- Summarize strengths and weaknesses of each solution
- Identify which solution best meets the stated requirements
- Note any trade-offs or compromises

**Recommendation Format:**

1. **Primary Choice:** [Solution X] - One sentence justification based on requirements
2. **Key Trade-offs:** 
   - What you gain with this choice
   - What you sacrifice compared to alternatives
3. **When to Choose Alternative:** 
   - Specific conditions where other solutions would be better
   - Threshold criteria for switching recommendations
4. **Decision Factors:** 
   - Variables that would change the recommendation
   - Sensitivity analysis of key assumptions
5. **Implementation Readiness:**
   - Prerequisites before starting
   - Team skills required
   - Infrastructure dependencies
6. **Migration Path:**
   - How to start simple and evolve
   - Phased implementation approach if applicable

### 8. Next Steps (MANDATORY)

> **This section is REQUIRED. Every response MUST end with this section.**
> Do not skip this step. This is how users proceed after comparison.

**After reviewing the comparison above, you have two options to proceed:**

1. **To implement a NEW solution from scratch:**
   - Use the `tdd-scaffold` workflow
   - Command: `@tdd-scaffold <your chosen solution>`
   - This will generate a complete project structure with all necessary components

2. **To REFACTOR existing code to match a solution:**
   - Use the `tdd-refactor` workflow
   - Command: `@tdd-refactor <path/to/existing/code> <target solution>`
   - This will analyze your existing code and refactor it to align with the chosen architecture

**Example:**
```
# If you choose Classic TDD (Inside-Out):
@tdd-scaffold user authentication service using classic TDD

# Or to add TDD to existing code:
@tdd-refactor src/auth/ outside-in TDD with integration tests
```

**Key Decisions to Make Before Proceeding:**
- Which solution best fits your requirements (based on the comparison above)
- Whether you're starting fresh (scaffold) or refactoring existing code (refactor)
- Any customizations or constraints to communicate to the workflow
- Team readiness and skill gaps to address

---

## Component Catalog Reference

Complete inventory of 72 components organized by category. Use this for discovery and keyword matching.

### ML Models (11)
| Component | Keywords |
|-----------|----------|
| clustering-ml-models | clustering, databricks, delta, governance, mlflow, models, notebook, scala, validation |
| collaborative-filtering-model | collaborative, filtering, governance, databricks, delta, devops, mlflow, model |
| dbscan-model | dbscan, model, monitoring, notebook, observability, python |
| forecasting-analyst | forecasting, analyst, databricks, delta, devops, governance, mlflow, monitoring |
| gradient-boosted-trees | gradient, boosted, trees, governance, lightgbm, mlflow, monitoring, validation, xgboost |
| isolation-forest-model | isolation, forest, model, monitoring, notebook, python, rest |
| logistic-regression-specialist | logistic, regression, databricks, devops, governance, mlflow, monitoring, notebook, observability |
| neural-network-model | neural, network, model, governance, mlflow, monitoring, numpy, observability, python |
| q-learning-model | q-learning, learning, model, numpy, observability, python, scala, validation |
| random-forest-model | random, forest, model, delta, governance, mlflow, monitoring, python, rest |
| siamese-neural-network | siamese, neural, network, mlflow, observability, rest, scala, validation |

### ML Operations (8)
| Component | Keywords |
|-----------|----------|
| experiment-scientist | experiment, scientist, databricks, delta, devops, governance, mlflow, monitoring |
| feature-architect | feature, architect, store, databricks, delta, devops, engineering, governance, point-in-time, training-data |
| inference-orchestrator | inference, orchestrator, aks, deployment, devops, endpoint, helm, kafka, prediction, serving |
| interpretability-analyst | interpretability, analyst, compliance, mlflow, notebook |
| language-model-evaluation | language, model, evaluation, LLM, grader, monitoring, testing, validation |
| model-architect | model, architect, experiment, feature, governance, hyperparameter, mlflow, monitoring, training |
| model-ops-steward | model-ops, steward, aks, lifecycle, compliance, databricks, delta, devops, governance, mlflow |
| insight-reporter | insight, reporter, performance, narratives, KPI, notebook, observability |

### Data Engineering (10)
| Component | Keywords |
|-----------|----------|
| data-pipeline-builder | pipeline, builder, data, databricks, delta, ingestion, loading, batch, incremental, streaming, python, scala |
| data-solution-architect | data, solution, architect, airflow, databricks, governance, python, rest, scala |
| data-sourcing-specialist | data, sourcing, specialist, databricks, delta, governance, notebook, python |
| databricks-developer-workflow | databricks, developer, workflow, jupyter, monitoring, notebook, devops |
| databricks-workflow-creator | databricks, workflow, creator, delta, devops, governance, kafka, mlflow |
| eda-navigator | eda, navigator, exploratory, analysis, databricks, delta, devops, governance, mlflow |
| elasticsearch-stream | elasticsearch, stream, eventhub, databricks, jupyter, notebook, python |
| pipeline-orchestrator | pipeline, orchestrator, airflow, cron, dag, orchestration, scheduling, task, tws, workflow |
| sql-query-crafter | sql, query, crafter, cte, database, governance, join, select, snowflake, testing |
| transformation-alchemist | transformation, alchemist, data-quality, databricks, dataframe, delta, etl, pyspark, python, scala, spark, sql |

### Data Governance (6)
| Component | Keywords |
|-----------|----------|
| data-classification-policy | data, classification, policy, compliance, governance, monitoring, security, PII, SPI |
| data-reliability | data, reliability, availability, freshness, quality, latency, lineage, governance, monitoring, observability |
| data-security | data, security, encryption, SPI, retention, masking, compliance, governance, observability |
| data-validation | data, validation, complete, accurate, timely, consistent, contract, governance |
| quality-guardian | quality, guardian, data-quality, deequ, delta, great-expectations, pandas, python, scala, testing, threshold, validation |
| ai-ethics-advisor | ethics, advisor, compliance, governance, monitoring, security, testing, bias, fairness |

### Infrastructure & DevOps (9)
| Component | Keywords |
|-----------|----------|
| aks-devops-deployment | aks, deployment, CI/CD, container, devops, docker, fastapi, governance, helm, kubernetes, microservice |
| automation-scripter | automation, scripter, CI/CD, compliance, governance, monitoring, security, testing |
| container-solution-architect | container, docker, dockerfile, podman, multi-stage, health-check, lifecycle, process-supervision, resource-limits |
| dev-ops-engineer | devops, engineer, governance, observability, ops, security, validation |
| key-vault-config-steward | key-vault, config, steward, airflow, fastapi, governance, observability, secrets |
| microservice-cicd-architect | microservice, CI/CD, compliance, devops, governance, observability, security |
| observability | observability, traces, metrics, logs, monitoring, opentelemetry, fastapi, python, react, telemetry |
| performance-tuner | performance, tuner, bottleneck, optimization, profiling, spark, tuning |
| terraform-cicd-architect | terraform, CI/CD, infrastructure, IaC, compliance, drift, governance, monitoring, policy, security |

### Application Development (7)
| Component | Keywords |
|-----------|----------|
| app-maker | app, application, maker, backend, fastapi, frontend, python, react, rest, security, UI, web |
| backend-only | backend, API, aks, docker, fastapi, helm, kubernetes, devops |
| demo-producer | demo, producer, playwright, python, react, testing, validation |
| frontend-only | frontend, react, security, testing, validation |
| integration-specialist | integration, specialist, fastapi, graphql, python, rest, security |
| ppt-maker | ppt, maker, powerpoint, python, presentation, slides |
| streamlit-developer | streamlit, developer, pandas, python, sql, data-app, validation |

### Graph Analytics (3)
| Component | Keywords |
|-----------|----------|
| general-graph-ontology | graph, ontology, general, databricks, delta, governance, monitoring, pyspark, security, spark |
| graph-community-detection | graph, community, detection, databricks, delta, governance, kafka, mlflow |
| ontology-engineer | ontology, engineer, RelationalAI, Snowflake, jupyter, monitoring, notebook, python |

### Software Quality (10)
| Component | Keywords |
|-----------|----------|
| code-reviewer | code-review, reviewer, snowflake, sql, python, tws, databricks, quality-gate, security |
| git-secret-remediation | git, secret, remediation, compliance, security, testing |
| java-library-upgrade | java, library, upgrade, dependency |
| java-security-vulnerability | java, security, vulnerability, CVE |
| pub-sub-load-testing | pub-sub, load, testing, kafka, validation |
| pull-review-risk | pull, review, risk, compliance, governance, monitoring, security |
| python-library-upgrade | python, library, upgrade, dependency, pip, poetry |
| python-security-vulnerability | python, security, vulnerability, CVE |
| regression-test-coverage | regression, test, coverage, automation, quality-assurance |
| unit-test-code-coverage | unit, test, coverage, java, validation |

### Documentation & Requirements (4)
| Component | Keywords |
|-----------|----------|
| documentation-evangelist | documentation, evangelist, compliance, databricks, governance, notebook, pandas, python, testing |
| jira-user-stories | jira, user, stories, acceptance-criteria, requirements, backlog |
| notebook-collaboration-coach | notebook, collaboration, coach, jupyter, jupytext, reproducibility |
| software-release-notes | release, notes, software, changelog, sprint, jira |

### Meta & Specialized (4)
| Component | Keywords |
|-----------|----------|
| archetype-architect | archetype, meta, template, generator, constitution, workflow, scaffold, quality, standard, ecosystem |
| impact-analyzer | impact, analyzer, databricks, python, scala, sql, testing |
| parallel-agent | parallel, agent, docker, python, scala, security, sql, testing |
| responsible-prompting | responsible, prompting, prompt, safety, compliance, governance, LLM |

---

## Examples

**Example 1: Classic TDD vs Outside-In TDD for a REST API**
```
User: Compare TDD approaches for a user authentication REST API

Solution A (Classic TDD — Inside-Out):
- Components: unit-test-code-coverage + code-reviewer + regression-test-coverage + quality-guardian
- Cycle: Write unit tests for password hashing, token generation → implement → refactor → wire up
- Strengths: Fast feedback, simple setup, strong unit isolation, easy to debug failures
- Weaknesses: Integration gaps discovered late, mocks may not reflect real dependencies

Solution B (Outside-In TDD — London School):
- Components: unit-test-code-coverage + regression-test-coverage + integration-specialist + code-reviewer
- Cycle: Write failing integration test for POST /login endpoint → mock dependencies → implement controller → implement services
- Strengths: API contract defined upfront, integration verified early, clear design intent
- Weaknesses: Heavy mocking overhead, slower initial feedback, brittle with implementation changes

Comparison Matrix:
| Dimension           | Solution A (Classic TDD)    | Solution B (Outside-In TDD) | Winner |
|---------------------|-----------------------------|-----------------------------|--------|
| Feedback Speed      | ⭐⭐⭐⭐⭐ (ms unit loops)     | ⭐⭐⭐ (integration overhead) | A      |
| Adoption Cost       | ⭐⭐⭐⭐⭐ (low ceremony)      | ⭐⭐⭐ (mocking expertise)    | A      |
| Complexity          | ⭐⭐⭐⭐ (simple setup)        | ⭐⭐⭐ (mock orchestration)   | A      |
| Refactoring Safety  | ⭐⭐⭐⭐ (unit safety)          | ⭐⭐⭐⭐⭐ (end-to-end safety)  | B      |
| Coverage Depth      | ⭐⭐⭐ (unit-level gaps)       | ⭐⭐⭐⭐⭐ (contract covered)   | B      |
| Team Collaboration  | ⭐⭐⭐ (dev-only)              | ⭐⭐⭐⭐ (API-driven clarity)  | B      |
| Developer Experience| ⭐⭐⭐⭐⭐ (great tooling)      | ⭐⭐⭐⭐ (WireMock/Sinon)      | A      |
| **TOTAL SCORE**     | **29/35 = 83/100**          | **27/35 = 77/100**          | A      |

Recommendation: Solution A for teams new to TDD or for logic-heavy services.
Solution B when API contracts with other teams or services must be verified from the beginning.
```

**Example 2: BDD vs ATDD for a Checkout Feature**
```
User: Compare BDD and ATDD for implementing an e-commerce checkout flow

Solution A (BDD — Behavior Driven Development):
- Components: unit-test-code-coverage + regression-test-coverage + documentation-evangelist + jira-user-stories
- Cycle: Write Gherkin feature file → implement step definitions → implement feature → auto-generate living docs
- Strengths: Business-readable specs, living documentation, strong Dev/QA/BA alignment
- Weaknesses: Step definition maintenance overhead, Gherkin can become verbose

Solution B (ATDD — Acceptance Test Driven Development):
- Components: regression-test-coverage + jira-user-stories + documentation-evangelist + unit-test-code-coverage + quality-guardian
- Cycle: Capture acceptance criteria from JIRA stories → automate as Robot Framework/Playwright tests → implement
- Strengths: Criteria directly from stakeholders, framework-neutral, drives full delivery pipeline
- Weaknesses: Less readable than Gherkin, requires QA involvement to write tests

Comparison Matrix:
| Dimension           | Solution A (BDD)             | Solution B (ATDD)            | Winner |
|---------------------|------------------------------|------------------------------|--------|
| Feedback Speed      | ⭐⭐⭐ (e2e test suite)         | ⭐⭐⭐ (e2e test suite)         | Tie    |
| Adoption Cost       | ⭐⭐⭐ (Gherkin learning curve)  | ⭐⭐⭐⭐ (criteria-to-test flow) | B      |
| Complexity          | ⭐⭐⭐ (step definition sync)    | ⭐⭐⭐⭐ (simpler test files)    | B      |
| Refactoring Safety  | ⭐⭐⭐⭐⭐ (scenario coverage)    | ⭐⭐⭐⭐⭐ (criteria coverage)   | Tie    |
| Coverage Depth      | ⭐⭐⭐⭐ (scenario-based)         | ⭐⭐⭐⭐⭐ (criteria-exhaustive)  | B      |
| Team Collaboration  | ⭐⭐⭐⭐⭐ (business-readable)    | ⭐⭐⭐⭐ (criteria-driven)       | A      |
| Developer Experience| ⭐⭐⭐⭐ (Cucumber IDE support)   | ⭐⭐⭐ (framework-dependent)    | A      |
| **TOTAL SCORE**     | **25/35 = 71/100**           | **28/35 = 80/100**           | B      |

Recommendation: Solution A (BDD) when cross-functional team alignment and living documentation are priorities.
Solution B (ATDD) when acceptance criteria already exist in JIRA/tickets and you want a lower-ceremony path to automated validation.
```

**Example 3: Classic TDD vs Contract-First TDD for Microservices**
```
User: Compare TDD strategies for a payment microservice integrating with an order service

Solution A (Classic TDD — Inside-Out):
- Components: unit-test-code-coverage + code-reviewer + regression-test-coverage + quality-guardian
- Cycle: Unit-test payment logic in isolation → mock order service calls → integration-test internally
- Strengths: Fast feedback, strong business logic coverage, simple CI setup
- Weaknesses: Integration contract with order service verified only at deploy time

Solution B (Contract-First TDD — Pact):
- Components: integration-specialist + unit-test-code-coverage + documentation-evangelist + aks-devops-deployment
- Cycle: Define Pact contract between payment (consumer) and order (provider) → run consumer tests → share contract → provider verifies
- Strengths: Cross-team API contract guaranteed, integration issues caught before deployment, consumer-driven design
- Weaknesses: Pact broker infrastructure required, both teams must participate, higher setup cost

Comparison Matrix:
| Dimension           | Solution A (Classic TDD)     | Solution B (Contract-First)  | Winner |
|---------------------|------------------------------|------------------------------|--------|
| Feedback Speed      | ⭐⭐⭐⭐⭐ (instant unit loops)  | ⭐⭐⭐⭐ (fast Pact tests)       | A      |
| Adoption Cost       | ⭐⭐⭐⭐⭐ (minimal tooling)     | ⭐⭐ (Pact broker, team buy-in)| A      |
| Complexity          | ⭐⭐⭐⭐⭐ (simple)              | ⭐⭐⭐ (broker + two-team sync) | A      |
| Refactoring Safety  | ⭐⭐⭐ (misses API breaks)      | ⭐⭐⭐⭐⭐ (API breaks caught)   | B      |
| Coverage Depth      | ⭐⭐⭐ (unit-only integration)  | ⭐⭐⭐⭐⭐ (contract verified)   | B      |
| Team Collaboration  | ⭐⭐ (teams work in isolation) | ⭐⭐⭐⭐⭐ (explicit contract)   | B      |
| Developer Experience| ⭐⭐⭐⭐⭐ (familiar tooling)    | ⭐⭐⭐⭐ (Pact DSL + broker UI)  | A      |
| **TOTAL SCORE**     | **27/35 = 77/100**           | **28/35 = 80/100**           | B      |

Recommendation: Solution B (Contract-First) when services are owned by separate teams and API breaking changes are a deployment risk.
Solution A for single-team services or when Pact infrastructure cannot be justified.
```

**Example 4: Classic TDD vs Property-Based TDD for Data Transformation**
```
User: Compare TDD approaches for a data transformation pipeline that normalizes customer records

Solution A (Classic TDD — Example-Based):
- Components: unit-test-code-coverage + quality-guardian + data-validation + code-reviewer
- Cycle: Write specific test cases (null name, duplicate email, invalid phone) → implement normalizer → refactor
- Strengths: Clear, readable tests, fast execution, easy to debug specific failures
- Weaknesses: Edge cases not thought of upfront are missed; manual test case enumeration

Solution B (Property-Based TDD — Hypothesis):
- Components: unit-test-code-coverage + quality-guardian + data-validation + interpretability-analyst
- Cycle: Define properties (output email is always lowercase, output phone is always E.164) → Hypothesis generates thousands of inputs → fix shrunk failure cases
- Strengths: Discovers unexpected edge cases automatically, stronger correctness guarantees, shrinks to minimal failure
- Weaknesses: Slower test runs, harder to read failing output, properties can be hard to define

Comparison Matrix:
| Dimension           | Solution A (Example-Based)   | Solution B (Property-Based)  | Winner |
|---------------------|------------------------------|------------------------------|--------|
| Feedback Speed      | ⭐⭐⭐⭐⭐ (instant, deterministic)| ⭐⭐⭐ (generative overhead)  | A      |
| Adoption Cost       | ⭐⭐⭐⭐⭐ (no new concepts)     | ⭐⭐⭐ (property thinking)     | A      |
| Complexity          | ⭐⭐⭐⭐⭐ (straightforward)     | ⭐⭐⭐ (property definition)   | A      |
| Refactoring Safety  | ⭐⭐⭐ (known cases only)       | ⭐⭐⭐⭐⭐ (broad input space)  | B      |
| Coverage Depth      | ⭐⭐⭐ (manually enumerated)    | ⭐⭐⭐⭐⭐ (auto-generated)     | B      |
| Team Collaboration  | ⭐⭐⭐⭐⭐ (readable by all)     | ⭐⭐⭐ (requires explanation)  | A      |
| Developer Experience| ⭐⭐⭐⭐⭐ (familiar)            | ⭐⭐⭐⭐ (Hypothesis UX is good)| A      |
| **TOTAL SCORE**     | **29/35 = 83/100**           | **27/35 = 77/100**           | A      |

Recommendation: Solution A for most teams as the primary approach.
Add Solution B for critical transformation logic (e.g., PII normalization, financial calculations) where exhaustive edge-case coverage is required.
```

## Pre-Response Validation

Before delivering your response, verify:
- [ ] At least 2 distinct solutions identified
- [ ] Each solution has specific component names from catalog (not generic descriptions)
- [ ] Assumptions and constraints documented
- [ ] Comparison matrix is a properly formatted markdown table
- [ ] Matrix has ≥5 dimensions with star ratings (⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐)
- [ ] **TOTAL SCORE row calculated and included as X/100 format**
- [ ] Total score calculated correctly: (sum of points / (dimensions × 5)) × 100
- [ ] Winner column is populated for each dimension
- [ ] **Narrative comparison section included (2-4 paragraphs of prose)**
- [ ] Recommendation follows the 6-part format (Primary Choice, Trade-offs, Alternatives, Decision Factors, Readiness, Migration Path)
- [ ] **Next Steps section included with explicit instructions to use tdd-scaffold or tdd-refactor**
- [ ] Next steps include example commands for both workflows
- [ ] No code, scripts, or implementation details included
- [ ] No file writes, edits, or terminal commands executed

## Required Output Structure

Every response from this workflow MUST contain ALL of the following sections in order:

1. **Assumptions & Constraints** — Document scale, expertise, budget, timeline, infrastructure, compliance assumptions
2. **Solutions Identified** — Name and briefly describe each solution alternative (minimum 2)
3. **Component Mapping** — List the specific components from the catalog for each solution
4. **Comparison Matrix** — A markdown table rating each solution on ≥5 dimensions using ⭐⭐⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐/⭐⭐/⭐ with Winner column and **TOTAL SCORE out of 100**
5. **Narrative Comparison** — 2-4 paragraphs of prose explaining strengths, weaknesses, trade-offs, and decision criteria
6. **Recommendation** — Follow 6-part format: Primary Choice, Trade-offs, Alternatives, Decision Factors, Readiness, Migration Path
7. **Next Steps** — Explicit instructions to use `tdd-scaffold` or `tdd-refactor` with example commands

If any section is missing, the output is incomplete. Do not substitute prose summaries for the matrix table. Do not skip the narrative comparison or next steps sections.

## Notes

- **This is an analysis-only workflow. Never output code, scripts, config files, or shell commands.**
- **Never use file-modifying tools (edit_file, write_file, run_terminal_command) in this workflow.**
- **Always provide both matrix comparison AND narrative comparison — the matrix alone is insufficient.**
- **Always end with Next Steps section directing users to tdd-scaffold or tdd-refactor.**
- This workflow is completely standalone and does not depend on external files, scripts, or directory structures
- Component discovery uses inline keyword matching against the embedded catalog above
- TDD approach comparisons should consider team skill level, project domain, and existing test infrastructure
- All recommendations should be based on objective analysis of trade-offs between TDD strategies
- When comparing TDD approaches, always consider adoption paths from simpler to more rigorous methods
- The component catalog contains 72 components across 10 categories — use it as a lookup reference for relevant testing components
- **For NEW TDD implementation after comparison:** direct users to `tdd-scaffold` workflow
- **For adding TDD to existing code after comparison:** direct users to `tdd-refactor` workflow
- If user asks to "build", "implement", "scaffold", or "refactor" after comparing, **remind them to explicitly invoke the appropriate workflow** — do not start coding yourself
