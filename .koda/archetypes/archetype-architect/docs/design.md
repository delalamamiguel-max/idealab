# Archetype Architect - Comprehensive Design

## Executive Summary

The **archetype-architect** is the meta-archetype responsible for creating, refining, quality-controlling, and documenting all archetypes in the ecosystem. It serves as the foundation for maintaining consistency, quality, and discoverability across the entire archetype inventory.

This design document establishes the architectural principles, interaction patterns, and quality standards that govern how archetype-architect operates and how it ensures all archetypes conform to ecosystem standards.

---

## Table of Contents

1. [Core Responsibilities](#core-responsibilities)
2. [Architectural Principles](#architectural-principles)
3. [Manifest Schema Design](#manifest-schema-design)
4. [Archetype Structure Standard](#archetype-structure-standard)
5. [Workflow Architecture](#workflow-architecture)
6. [Discovery and Routing](#discovery-and-routing)
7. [Quality Assurance Model](#quality-assurance-model)
8. [Delegation Patterns](#delegation-patterns)
9. [Circular Dependency Handling](#circular-dependency-handling)
10. [Integration Points](#integration-points)

---

## Core Responsibilities

### Primary Functions

```mermaid
graph TB
    subgraph AA["ARCHETYPE-ARCHITECT"]
        direction TB
        subgraph row1["Core Workflows"]
            SCAFFOLD["**SCAFFOLD**<br/>Create new<br/>archetypes"]
            REFACTOR["**REFACTOR**<br/>Improve existing<br/>archetypes"]
            TEST["**TEST**<br/>Validate quality<br/>standards"]
            DOCUMENT["**DOCUMENT**<br/>Generate docs<br/>for archetypes"]
        end
        subgraph row2["Analysis Workflows"]
            COMPARE["**COMPARE**<br/>Evaluate design<br/>options"]
            DEBUG["**DEBUG**<br/>Diagnose<br/>archetype issues"]
        end
    end
    
    style AA fill:#f5f5f5,stroke:#333,stroke-width:2px
    style SCAFFOLD fill:#e1f5fe,stroke:#0288d1
    style REFACTOR fill:#e8f5e9,stroke:#388e3c
    style TEST fill:#fff3e0,stroke:#f57c00
    style DOCUMENT fill:#fce4ec,stroke:#c2185b
    style COMPARE fill:#ede7f6,stroke:#512da8
    style DEBUG fill:#ffebee,stroke:#c62828
```

### Basic Vision

- Create, refine, and quality-control **any single archetype** at a time
- Ensure consistency with ecosystem standards
- Validate manifest, constitution, workflows, and structure

### Ultimate Vision

- Manage a **multi-archetype ecosystem**
- Guide users in creating new archetypes on-the-fly
- Prevent duplication by recommending existing archetypes
- Inventory-aware: Prompt expansion before creation if <50 archetypes exist

---

## Architectural Principles

### Principle 1: No Versioning in Core Assets

**Rationale**: Version information in manifests, constitutions, or workflows increases LLM token consumption and risks hallucinations from stale context.

**Implementation**:

- Version tracking belongs in `changelog.md` within each archetype
- Manifests reference changelog but never contain version fields
- Workflows never reference or check version numbers
- Only archetype-architect reads changelog during audit operations

```yaml
# WRONG - Version in manifest
archetype:
  name: example
version: '1.0'

# CORRECT - No version, separate changelog
archetype:
  name: example
  changelog: changelog.md  # Optional reference
```

### Principle 2: Leverage Core Orchestration

**Rationale**: Archetype-architect should not reinvent routing logic. Core orchestration provides battle-tested discovery and delegation.

**Implementation**:

```mermaid
flowchart LR
    subgraph AA["archetype-architect"]
        subgraph WF["scaffold-archetype-architect.md"]
            S1["Step 1: User Intent"]
            S2["Step 2: Inventory Check"]
            S3["Step 3: Archetype Design"]
            S4["Step 4: Delegate"]
            S5["Step 5: Quality Validation"]
            S1 --> S2 --> S3 --> S4 --> S5
        end
    end
    
    subgraph CO["00-core-orchestration"]
        SOL["/solution-scaffold"]
    end
    
    S4 -->|"delegate"| SOL
    
    style AA fill:#e3f2fd,stroke:#1565c0
    style CO fill:#e8f5e9,stroke:#2e7d32
```

### Principle 3: Maximize Routing Benefits

**Rationale**: Specialist archetypes exist for a reason. Documentation should be beautiful (documentation-evangelist), code should be correct (domain archetype).

**Implementation**:

```mermaid
flowchart LR
    DOC["document-archetype-architect"] --> SOL["/solution-document"]
    
    subgraph SOL["/solution-document"]
        DE["**documentation-evangelist**<br/>• Prose quality<br/>• Structure<br/>• Presentation"]
        DP["**data-pipeline-builder**<br/>• Domain accuracy<br/>• Technical detail<br/>• Code examples"]
    end
    
    style DOC fill:#e3f2fd,stroke:#1565c0
    style DE fill:#e8f5e9,stroke:#2e7d32
    style DP fill:#fff3e0,stroke:#ef6c00
```

*Example: Documenting a Data Pipeline Archetype - combines prose expertise with domain accuracy.*

### Principle 4: Inventory Awareness

**Rationale**: Creating new archetypes when similar ones exist leads to fragmentation and confusion.

**Implementation**:

```mermaid
flowchart TD
    REQ["User: Create an archetype for XYZ"] --> CHECK["Check Inventory Count<br/>discover-archetype.py --count"]
    
    CHECK --> DECIDE{Archetype Count?}
    
    DECIDE -->|"< 50"| PROMPT["⚠️ **PROMPT USER**<br/>Your ecosystem has only N archetypes.<br/>Consider expanding inventory first.<br/><br/>[Proceed] [Cancel]"]
    
    DECIDE -->|"≥ 50"| SIMILAR["Check for Similar Archetypes"]
    
    SIMILAR --> FOUND{Similar Found?}
    FOUND -->|"Yes"| SUGGEST["🔍 Found X with score% match<br/>Use existing?"]
    FOUND -->|"No"| CREATE["✓ Proceed with creation"]
    
    style REQ fill:#e3f2fd,stroke:#1565c0
    style PROMPT fill:#fff3e0,stroke:#ef6c00
    style SUGGEST fill:#e8f5e9,stroke:#2e7d32
    style CREATE fill:#e8f5e9,stroke:#2e7d32
```

### Principle 5: Graceful Circular Handling

**Rationale**: When archetype-architect modifies itself or archetypes that support modification, the model should not get confused.

**Implementation**:

```mermaid
flowchart TD
    subgraph META["Meta-Operation Pattern"]
        M1["1. Identify current best workflow"] --> M2["2. Execute workflow as normal"]
        M2 --> M3["3. Evaluate results"]
        M3 --> M4{"Modifying<br/>archetype-architect?"}
        M4 -->|"Yes"| M5["Changes take effect on<br/>NEXT invocation"]
        M4 -->|"No"| M6["Changes take effect<br/>immediately"]
        M5 --> M7["✓ Expected behavior"]
        M6 --> M7
    end
    
    style META fill:#f5f5f5,stroke:#333
    style M7 fill:#e8f5e9,stroke:#2e7d32
```

---

## Manifest Schema Design

### Current Schema (Deprecated)

```yaml
archetype:
  name: example-archetype
  display_name: Example Archetype
  description: Brief description
  keywords:
    - keyword1
    - keyword2
  workflows:
    scaffold: scaffold-example-archetype
    refactor: refactor-example-archetype
    compare: compare-example-archetype
    test: test-example-archetype
    debug: debug-example-archetype
    document: document-example-archetype
version: '1.0'  # DEPRECATED - REMOVE
```

### New Schema

```yaml
archetype:
  name: example-archetype
  display_name: Example Archetype
  description: Brief description of what this archetype does and when to use it
  
  keywords:
    - keyword1
    - keyword2
    # Keywords should be domain-relevant for discovery scoring
  
  constitution:
    path: example-archetype-constitution.md
    # Path relative to archetype root
  
  dependencies:
    - 00-core-orchestration  # Always required (implicit)
    # Only list HARD dependencies - archetypes that MUST be present
    # Soft dependencies are resolved via discovery at runtime
  
  workflows:
    scaffold: scaffold-example-archetype
    refactor: refactor-example-archetype
    compare: compare-example-archetype
    test: test-example-archetype
    debug: debug-example-archetype
    document: document-example-archetype

# NO version field - version history in changelog.md
```

### Schema Validation Rules

1. **Required Fields**: `name`, `display_name`, `description`, `keywords`, `workflows`
2. **Constitution**: Must exist if referenced; path must be valid
3. **Dependencies**: Must reference existing archetypes
4. **Workflows**: All 6 workflows must be defined (scaffold, refactor, compare, test, debug, document)
5. **Keywords**: Must be relevant to archetype domain (no generic terms)
6. **No Version**: Field must not exist

---

## Archetype Structure Standard

### Required Structure

```
{archetype-slug}/
│
├── manifest.yaml                      # REQUIRED: Discovery metadata
│   • name, display_name, description
│   • keywords for discovery scoring
│   • constitution path reference
│   • workflow mappings
│
├── {archetype-slug}-constitution.md   # REQUIRED: Rules and guardrails
│   • Hard-stop rules
│   • Mandatory patterns
│   • Preferred patterns
│   • Cross-platform guidelines
│
├── README.md                          # REQUIRED: Human-readable overview
│   • Purpose and use cases
│   • Quick start guide
│   • Workflow summary
│   • Related archetypes
│
├── .koda/
│   └── workflows/                     # REQUIRED: All 6 workflows
│       ├── scaffold-{slug}.md         # REQUIRED
│       ├── refactor-{slug}.md         # REQUIRED
│       ├── compare-{slug}.md          # REQUIRED
│       ├── test-{slug}.md             # REQUIRED
│       ├── debug-{slug}.md            # REQUIRED
│       └── document-{slug}.md         # REQUIRED
│
├── changelog.md                       # OPTIONAL: Version history
│   • Release dates
│   • Change summaries
│   • Migration notes
│
├── docs/                              # OPTIONAL: Extended documentation
│   ├── design.md                      # Architecture and design decisions
│   ├── implementation-plan.md         # Development roadmap
│   └── {other-docs}.md                # Additional documentation
│
├── scripts/                           # OPTIONAL: Archetype-specific scripts
│   └── {script-name}.py               # Only truly native scripts
│
└── templates/                         # OPTIONAL: Archetype-specific templates
    └── {template-name}.{ext}          # Only truly native templates
```

### Asset Ownership Rules

| Asset Type | Owned By | Location |
|------------|----------|----------|
| Discovery script | 00-core-orchestration | `00-core-orchestration/scripts/` |
| Core workflow templates | 00-core-orchestration | `00-core-orchestration/templates/` |
| Archetype-specific scripts | Archetype | `{archetype}/scripts/` |
| Archetype-specific templates | Archetype | `{archetype}/templates/` |
| Shared utilities | 00-core-orchestration | `00-core-orchestration/scripts/` |

**Rule**: If an asset could be useful to multiple archetypes, it belongs in 00-core-orchestration. If it's truly specific to one archetype's domain, it belongs in that archetype.

### archetype-architect Scripts

Scripts specific to archetype management (not discovery/routing):

| Script | Purpose | Usage |
|--------|---------|-------|
| `migrate-manifests.py` | Migrate manifests to new schema | `python scripts/migrate-manifests.py --dry-run` |

**migrate-manifests.py** capabilities:
- `--dry-run` - Preview changes without applying
- `--apply` - Apply schema migrations
- `--validate` - Validate manifests only
- `--basedir` - Override ARCHETYPES_BASEDIR

Migrations performed:
- Adds `constitution` field if missing
- Adds `dependencies` field if missing
- Removes deprecated `version` field
- Validates required fields

---

## Workflow Architecture

### Workflow Interaction Model

```mermaid
flowchart LR
    subgraph AA["archetype-architect"]
        AAW["scaffold-archetype-architect.md<br/>• Archetype design<br/>• Inventory check<br/>• Structure creation<br/>• Quality validation"]
    end
    
    subgraph CO["00-core-orchestration"]
        subgraph CW["Core Workflows"]
            C1["/scaffold"]
            C2["/refactor"]
            C3["/compare"]
            C4["/test"]
            C5["/debug"]
            C6["/document"]
        end
        
        subgraph SW["Solution Workflows"]
            S1["/solution-scaffold"]
            S2["/solution-document"]
            S3["/solution-refactor"]
        end
        
        subgraph DA["discover-archetype.py"]
            D1["• Query matching"]
            D2["• Keyword scoring"]
            D3["• Workflow routing"]
        end
    end
    
    AAW --> CW
    AAW --> SW
    
    style AA fill:#e3f2fd,stroke:#1565c0
    style CO fill:#f5f5f5,stroke:#333
    style CW fill:#e8f5e9,stroke:#2e7d32
    style SW fill:#fff3e0,stroke:#ef6c00
    style DA fill:#fce4ec,stroke:#c2185b
```

### Workflow Design Patterns

#### Pattern 1: Delegate General, Specialize Specific

```markdown
## Step N: Generate Comprehensive Documentation

Delegate to `/solution-document` with multi-archetype context:

**Primary Specialist**: documentation-evangelist
- Handles: Prose quality, structure, visual presentation
- Expertise: Technical writing, information architecture

**Domain Expert**: {target-archetype}
- Handles: Domain accuracy, code examples, configuration specifics
- Expertise: The actual technology being documented

// turbo
Execute `/solution-document` targeting both archetypes for combined output.
```

#### Pattern 2: Pre-Flight Inventory Check

```markdown
## Step 1: Inventory Assessment

Before creating a new archetype, assess ecosystem state:

// turbo
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py --count --json`

**If count < 50**:
```
⚠️ Your archetype ecosystem has only {count} archetypes.

Recommendation: Consider expanding your inventory with established
patterns before creating custom archetypes.

[Proceed Anyway] [Explore Existing Archetypes] [Cancel]
```

**If count ≥ 50**: Continue to similarity check.
```

#### Pattern 3: Similarity Check Before Creation

```markdown
## Step 2: Check for Similar Archetypes

// turbo
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py --query "{user_intent}" --top 3 --json`

**If match score ≥ 70%**:
```
🔍 Found similar archetype: {archetype_name}

Match Score: {score}%
Keywords: {matching_keywords}

Would you like to:
1. Use existing archetype: /{workflow}
2. Refactor existing archetype to add functionality
3. Proceed with new archetype (requires justification)
```

**If no close matches**: Proceed with archetype creation.
```

---

## Discovery and Routing

### Enhanced discover-archetype.py

The discovery script is the routing brain of the ecosystem. Enhancements needed:

```python
# New capabilities needed:

def discover_archetypes(basedir, include_constitution=False):
    """
    Scan all archetypes and return metadata.
    
    Args:
        basedir: Root directory containing archetypes
        include_constitution: If True, also load constitution metadata
    
    Returns:
        List of archetype metadata dictionaries
    """

def get_inventory_count(basedir):
    """
    Return total count of valid archetypes.
    
    Returns:
        Integer count of archetypes with valid manifests
    """

def validate_archetype_structure(archetype_dir):
    """
    Validate an archetype against the standard structure.
    
    Returns:
        Dictionary with:
        - is_valid: Boolean
        - missing_required: List of missing required files
        - missing_recommended: List of missing recommended files
        - issues: List of structural issues found
    """

def resolve_dependencies(archetype_name, basedir):
    """
    Resolve all dependencies for an archetype.
    
    Returns:
        Dictionary with:
        - hard_dependencies: List from manifest
        - resolved: Boolean (all dependencies exist)
        - missing: List of missing dependencies
    """
```

### Routing Decision Tree

```mermaid
flowchart TD
    REQ["User Request"] --> PARSE["Parse Intent<br/>Extract keywords"]
    PARSE --> DISCOVER["discover-archetype.py<br/>--query intent --top 3 --json"]
    
    DISCOVER --> SCORE{Score?}
    
    SCORE -->|"≥ 30"| HIGH["✓ Route directly to /{workflow}"]
    SCORE -->|"15-29"| MED["🤔 Prompt user to confirm"]
    SCORE -->|"< 15"| LOW["⚠️ Clarification needed"]
    
    MED --> CONFIRM{User confirms?}
    CONFIRM -->|"Yes"| ROUTE["Route to /{workflow}"]
    CONFIRM -->|"No"| ALT["Show alternatives"]
    
    LOW --> CLARIFY["Show category suggestions<br/>Ask for more context"]
    
    style HIGH fill:#e8f5e9,stroke:#2e7d32
    style MED fill:#fff3e0,stroke:#ef6c00
    style LOW fill:#ffebee,stroke:#c62828
```

**Score Reference** (from discover-archetype.py):
- Exact archetype name match: +50
- Display name match: +30
- Keyword match: +10 each
- Description word match: +2 each
- Workflow name match: +25

---

## Quality Assurance Model

### Archetype Quality Dimensions

```mermaid
graph TB
    subgraph QA["QUALITY ASSESSMENT"]
        direction TB
        subgraph SC["STRUCTURAL COMPLIANCE"]
            SC1["☐ manifest.yaml"]
            SC2["☐ constitution.md"]
            SC3["☐ README.md"]
            SC4["☐ workflows/"]
            SC5["☐ No version fields"]
        end
        
        subgraph CQ["CONTENT QUALITY"]
            CQ1["☐ Clear description"]
            CQ2["☐ Good keywords"]
            CQ3["☐ Complete rules"]
            CQ4["☐ Useful docs"]
            CQ5["☐ Working code"]
        end
        
        subgraph IH["INTEGRATION HEALTH"]
            IH1["☐ Dependencies valid"]
            IH2["☐ Paths correct"]
            IH3["☐ Scripts work"]
            IH4["☐ Templates valid"]
        end
        
        subgraph RE["ROUTING EFFECTIVENESS"]
            RE1["☐ Discoverable"]
            RE2["☐ Scores well"]
            RE3["☐ Routes right"]
            RE4["☐ Delegates well"]
        end
    end
    
    style QA fill:#f5f5f5,stroke:#333,stroke-width:2px
    style SC fill:#e3f2fd,stroke:#1565c0
    style CQ fill:#e8f5e9,stroke:#2e7d32
    style IH fill:#fff3e0,stroke:#ef6c00
    style RE fill:#fce4ec,stroke:#c2185b
```

### Quality Checks by Workflow

| Workflow | Quality Checks |
|----------|----------------|
| **scaffold** | Structure complete, manifest valid, constitution exists, workflows created |
| **refactor** | No version fields, paths updated, dependencies resolved, keywords relevant |
| **test** | All workflows execute, discovery scores correctly, routing works |
| **debug** | Root cause identified, fix doesn't break other archetypes |
| **compare** | Both options evaluated fairly, recommendation justified |
| **document** | README exists, docs comprehensive, examples work |

---

## Delegation Patterns

### Core Principle: Structural vs Content Quality

**archetype-architect specializes in STRUCTURAL and LOGICAL quality**, not content generation. For content, it delegates to specialist archetypes.

```mermaid
graph TB
    subgraph RM["ARCHETYPE-ARCHITECT RESPONSIBILITY MODEL"]
        subgraph OWNS["✓ WHAT ARCHETYPE-ARCHITECT OWNS<br/>(Structural & Logical Quality)"]
            O1["Manifest schema correctness"]
            O2["Constitution quality"]
            O3["Workflow consistency"]
            O4["File organization"]
            O5["Cross-references"]
            O6["Ecosystem integration"]
            O7["Naming consistency"]
            O8["Discovery performance"]
        end
        
        subgraph DELEGATES["→ WHAT ARCHETYPE-ARCHITECT DELEGATES<br/>(Content Quality)"]
            D1["Scripts → automation-scripter"]
            D2["Documentation → documentation-evangelist"]
            D3["Unit tests → unit-test-code-coverage"]
            D4["Regression tests → regression-test-coverage"]
            D5["User stories → jira-user-stories"]
            D6["CI/CD pipelines → microservice-cicd"]
            D7["Data validation → quality-guardian"]
        end
    end
    
    style RM fill:#f5f5f5,stroke:#333,stroke-width:2px
    style OWNS fill:#e8f5e9,stroke:#2e7d32
    style DELEGATES fill:#e3f2fd,stroke:#1565c0
```

### Delegation Decision Matrix

| Scenario | archetype-architect Action |
|----------|---------------------------|
| Script has bugs or poor patterns | **DELEGATE** to `/debug-automation` |
| Documentation is unclear | **DELEGATE** to `/refactor-documentation` |
| Tests are missing or weak | **DELEGATE** to `/scaffold-unit-test-code-coverage` |
| Manifest has wrong schema | **HANDLE directly** (structural) |
| Constitution rules incomplete | **HANDLE directly** (logical quality) |
| Workflow structure non-standard | **HANDLE directly** (consistency) |
| Cross-references broken | **HANDLE directly** (integration) |
| User stories needed for project | **DELEGATE** to `/scaffold-jira-user-stories` |

### Delegation Flow Pattern

```mermaid
flowchart TD
    A["archetype-architect identifies need:<br/>'This archetype needs a validation script'"]
    B["Delegates to:<br/>/scaffold-automation"]
    C["automation-scripter creates<br/>high-quality script"]
    D["archetype-architect integrates<br/>script into structure"]
    E["archetype-architect validates<br/>script reference in workflows"]
    
    A --> B --> C --> D --> E
    
    style A fill:#e3f2fd,stroke:#1565c0
    style B fill:#fff3e0,stroke:#ef6c00
    style C fill:#e8f5e9,stroke:#2e7d32
    style D fill:#e3f2fd,stroke:#1565c0
    style E fill:#e3f2fd,stroke:#1565c0
```

### Pattern: Multi-Archetype Documentation

When documenting an archetype, leverage multiple specialists:

*Input: "Document the data-pipeline-builder archetype"*

```mermaid
flowchart TD
    subgraph DOC["document-archetype-architect"]
        S1["**Step 1:** Gather archetype metadata<br/>• Read manifest.yaml<br/>• Read constitution.md<br/>• List workflows and scripts"]
        
        S2["**Step 2:** Delegate to /solution-document"]
        
        S3["**Step 3:** Assemble final documentation<br/>Merge outputs into README.md and docs/"]
        
        S1 --> S2 --> S3
    end
    
    subgraph SOL["/solution-document"]
        C1["**documentation-evangelist**<br/>• Structure the document<br/>• Write clear prose<br/>• Create visual diagrams"]
        C2["**data-pipeline-builder**<br/>• Domain-accurate content<br/>• Code examples<br/>• Technical validation"]
    end
    
    S2 --> C1
    S2 --> C2
    C1 --> S3
    C2 --> S3
    
    style DOC fill:#e3f2fd,stroke:#1565c0
    style SOL fill:#f5f5f5,stroke:#333
    style C1 fill:#e8f5e9,stroke:#2e7d32
    style C2 fill:#fff3e0,stroke:#ef6c00
```

### Pattern: Cross-Archetype Refactoring

When refactoring affects multiple archetypes:

*Input: "Update all archetypes to new manifest schema"*

```mermaid
flowchart TD
    subgraph REF["refactor-archetype-architect"]
        S1["**Step 1:** Scope Assessment<br/>• Identify affected archetypes<br/>• Classify changes"]
        S2["**Step 2:** Create Migration Plan<br/>• Generate migration script<br/>• Define validation criteria<br/>• Plan rollback strategy"]
        S3["**Step 3:** Execute via /solution-refactor<br/>• Batch process manifests<br/>• Validate each change<br/>• Report results"]
        S4["**Step 4:** Verify<br/>• Run discover-archetype.py<br/>• Confirm all discoverable"]
        
        S1 --> S2 --> S3 --> S4
    end
    
    style REF fill:#e3f2fd,stroke:#1565c0
    style S4 fill:#e8f5e9,stroke:#2e7d32
```

---

## Circular Dependency Handling

### Scenario: Modifying archetype-architect

*User: "Refactor the archetype-architect's scaffold workflow"*

```mermaid
flowchart TD
    subgraph META["META-OPERATION FLOW"]
        M1["**1. IDENTIFY CURRENT STATE**<br/>• Current scaffold workflow: v1<br/>• This is what we'll use"]
        M2["**2. EXECUTE USING CURRENT BEST**<br/>• Run /refactor-archetype-architect<br/>• Generate improvements<br/>• Save changes"]
        M3["**3. EVALUATE RESULTS**<br/>• New scaffold workflow: v2<br/>• Test with sample creation<br/>• Validate against constitution"]
        M4["**4. ACKNOWLEDGE META-STATE**<br/>Changes saved. Next scaffold<br/>operation will use updated workflow."]
        
        M1 --> M2 --> M3 --> M4
    end
    
    OK["✓ NO CONFUSION: Model understands<br/>this is expected behavior"]
    M4 --> OK
    
    style META fill:#f5f5f5,stroke:#333
    style OK fill:#e8f5e9,stroke:#2e7d32
```

### Scenario: Documenting the documentation archetype

*User: "Document the documentation-evangelist archetype"*

```mermaid
flowchart TD
    subgraph SELF["SELF-REFERENTIAL OPERATION"]
        S1["**1. RECOGNIZE THE SITUATION**<br/>Target: documentation-evangelist<br/>Tool: documentation-evangelist<br/>✓ This is valid - use best tool"]
        S2["**2. PROCEED NORMALLY**<br/>• Execute /solution-document<br/>• Same archetype provides structure + prose<br/>• Same archetype provides domain content"]
        S3["**3. DELIVER RESULT**<br/>High-quality self-documentation produced"]
        
        S1 --> S2 --> S3
    end
    
    OK["✓ NO PARADOX: Using a tool<br/>to document itself is normal"]
    S3 --> OK
    
    style SELF fill:#f5f5f5,stroke:#333
    style OK fill:#e8f5e9,stroke:#2e7d32
```

---

## Integration Points

### 00-core-orchestration Integration

archetype-architect integrates with 00-core-orchestration at three levels:

```mermaid
graph TB
    subgraph INTEGRATION["ARCHETYPE-ARCHITECT INTEGRATION MODEL"]
        subgraph L1["LEVEL 1: DISCOVERY SCRIPT"]
            DA["**discover-archetype.py**<br/>--query → Route to archetype<br/>--count → Inventory count<br/>--validate → Structure check<br/>--top N → Multiple matches"]
        end
        
        subgraph L2["LEVEL 2: CORE WORKFLOWS (1:1 Routing)"]
            direction LR
            CW1["/scaffold → /scaffold-arch"]
            CW2["/refactor → /refactor-arch"]
            CW3["/compare → /compare-arch"]
            CW4["/test → /test-arch"]
            CW5["/debug → /debug-arch"]
            CW6["/document → /document-arch"]
        end
        
        subgraph L3["LEVEL 3: SOLUTION WORKFLOWS (1:Many Routing)"]
            direction LR
            SW1["/solution-scaffold"]
            SW2["/solution-refactor"]
            SW3["/solution-compare"]
            SW4["/solution-test"]
            SW5["/solution-debug"]
            SW6["/solution-document"]
        end
    end
    
    style INTEGRATION fill:#f5f5f5,stroke:#333,stroke-width:2px
    style L1 fill:#fce4ec,stroke:#c2185b
    style L2 fill:#e8f5e9,stroke:#2e7d32
    style L3 fill:#e3f2fd,stroke:#1565c0
```

### archetype-architect Workflow Integration Map

```mermaid
flowchart LR
    subgraph AA["archetype-architect workflows"]
        SCAFFOLD["scaffold-archetype-architect"]
        REFACTOR["refactor-archetype-architect"]
        COMPARE["compare-archetype-architect"]
        TEST["test-archetype-architect"]
        DEBUG["debug-archetype-architect"]
        DOCUMENT["document-archetype-architect"]
    end
    
    subgraph USES["Uses discover-archetype.py"]
        U1["--count (inventory)"]
        U2["--query (similarity)"]
        U3["--validate (structure)"]
        U4["--top N (overlap)"]
    end
    
    subgraph DELEGATES["Delegates to"]
        D1["/solution-scaffold"]
        D2["/solution-refactor"]
        D3["/solution-compare"]
        D4["/solution-test"]
        D5["/solution-debug"]
        D6["/solution-document"]
        D7["/scaffold-automation"]
        D8["/test-unit-test-code-coverage"]
    end
    
    SCAFFOLD --> U1
    SCAFFOLD --> U2
    SCAFFOLD --> D1
    SCAFFOLD --> D7
    
    REFACTOR --> U3
    REFACTOR --> D2
    
    COMPARE --> U4
    COMPARE --> D3
    
    TEST --> U3
    TEST --> U2
    TEST --> D4
    TEST --> D8
    
    DEBUG --> U3
    DEBUG --> D5
    
    DOCUMENT --> D6
    
    style AA fill:#e3f2fd,stroke:#1565c0
    style USES fill:#fce4ec,stroke:#c2185b
    style DELEGATES fill:#e8f5e9,stroke:#2e7d32
```

### Routing Thresholds (Standardized)

All core and solution workflows use consistent numeric score thresholds:

| Score Range | Confidence | Action |
|-------------|------------|--------|
| ≥30 | High | Route directly to specialist workflow |
| 15-29 | Medium | Prompt user to confirm, show alternatives |
| <15 | Low | Request clarification, show category suggestions |

Score calculation (from discover-archetype.py):
- Exact archetype name match: +50
- Display name match: +30
- Keyword match: +10 each
- Description word match: +2 each
- Workflow name match: +25

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `ARCHETYPES_BASEDIR` | Root of archetype directories | Auto-detected from script location |

### Configuration Files

| File | Purpose | Location |
|------|---------|----------|
| `manifest.yaml` | Archetype metadata | Each archetype root |
| `*-constitution.md` | Rules and guardrails | Each archetype root |
| `changelog.md` | Version history | Each archetype root (optional) |

---

## Appendix: Templates

### Manifest Template

```yaml
archetype:
  name: {archetype-slug}
  display_name: {Human Readable Name}
  description: |
    Brief description of what this archetype does, when to use it,
    and what problems it solves.
  
  keywords:
    - {domain-keyword-1}
    - {domain-keyword-2}
    - {technology-keyword}
  
  constitution:
    path: {archetype-slug}-constitution.md
  
  dependencies:
    # Only hard dependencies - soft dependencies via discovery
    # - other-archetype-name
  
  workflows:
    scaffold: scaffold-{archetype-slug}
    refactor: refactor-{archetype-slug}
    compare: compare-{archetype-slug}
    test: test-{archetype-slug}
    debug: debug-{archetype-slug}
    document: document-{archetype-slug}
```

### README Template

```markdown
# {Archetype Display Name}

## Overview

{Brief description of the archetype's purpose and value proposition.}

## When to Use

- {Use case 1}
- {Use case 2}
- {Use case 3}

## Quick Start

```bash
# Scaffold a new {domain} solution
/scaffold-{archetype-slug} {arguments}
```

## Workflows

| Workflow | Purpose |
|----------|---------|
| `/scaffold-{slug}` | Create new {domain} solutions |
| `/refactor-{slug}` | Improve existing {domain} code |
| `/compare-{slug}` | Evaluate {domain} design options |
| `/test-{slug}` | Validate {domain} implementations |
| `/debug-{slug}` | Diagnose {domain} issues |
| `/document-{slug}` | Generate {domain} documentation |

## Related Archetypes

- `{related-archetype-1}` - {relationship description}
- `{related-archetype-2}` - {relationship description}

## References

- [Constitution](./{archetype-slug}-constitution.md)
- [Design](./docs/design.md)
```

---

## Document Information

- **Author**: archetype-architect (via /document workflow)
- **Purpose**: Define comprehensive design for archetype-architect refactoring
- **Audience**: Developers maintaining the archetype ecosystem
- **Related**: [Implementation Plan](./implementation-plan.md)
