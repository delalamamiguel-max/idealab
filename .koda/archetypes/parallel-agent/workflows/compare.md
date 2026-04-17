---
description: Decide when/why/how to use parallel vs single-stream delivery; choose agent counts/roles and risk controls.
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

**SUCCESS CRITERIA**:
- Search for directory: "00-core-orchestration"
- Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory

**HALT IF**:
- Directory "00-core-orchestration" is not found
- `${ARCHETYPES_BASEDIR}` is not set

Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

## Purpose

Help decide whether a task should use parallel agents or single-stream development.

---

### 🔄 Relationship with Solution Archetype

**Use `/solution-scaffold` first when:**
- You need to define a new architecture with multiple components
- You aren't sure which archetypes are needed
- You need integration contracts between components

**Use `/scaffold-parallel-agent` when:**
- You know what needs to be built and who should build it
- You just need to split the execution work
- You are implementing a solution that has already been designed

---

## Evaluation Criteria

### ✅ Good Fit for Parallel Agents

| Criterion | Example |
|-----------|----------|
| **Multiple distinct domains** | Database + API + Frontend |
| **Clear file ownership** | Each agent owns separate folders |
| **Loose coupling** | Agents can work without waiting on each other |
| **2-4 natural divisions** | Not too few, not too many |
| **Time-sensitive** | Need to parallelize to meet deadline |

### ❌ Poor Fit for Parallel Agents

| Criterion | Example |
|-----------|----------|
| **Single file changes** | Refactoring one large file |
| **Tight coupling** | Every change affects other areas |
| **Unclear boundaries** | Can't define who owns what |
| **Sequential dependencies** | B can't start until A finishes |
| **Simple task** | Overhead of coordination exceeds benefit |

---

## Decision Framework

Score the task (1-5 for each):

| Factor | Score | Notes |
|--------|-------|-------|
| Domain separation | _/5 | How cleanly can work be divided? |
| File ownership clarity | _/5 | Can each agent have exclusive files? |
| Independence | _/5 | Can agents work without waiting? |
| Complexity | _/5 | Is it complex enough to benefit? |
| Time pressure | _/5 | Is parallelization worth the overhead? |

**Total: _/25**

- **20-25:** Strong candidate for parallel agents
- **15-19:** Possible, but consider carefully
- **10-14:** Probably better as single stream
- **<10:** Definitely single stream

---

## Agent Count Guidelines

| Task Size | Recommended Agents | Example |
|-----------|-------------------|----------|
| Small | 2 | Backend + Frontend |
| Medium | 3 | Database + API + Frontend |
| Large | 4 | Database + API + Frontend + Tests |
| Very Large | 4 max | More agents = more coordination overhead |

**Rule of thumb:** Start with fewer agents. You can always add more.

---

## Risk Assessment

### High Risk Factors
- [ ] Shared configuration files (package.json, requirements.txt)
- [ ] Database migrations from multiple agents
- [ ] Overlapping API routes
- [ ] Shared state management

**Mitigation:** Assign one agent as owner of shared files; others request changes.

### Medium Risk Factors
- [ ] Cross-cutting concerns (logging, auth)
- [ ] Shared types/interfaces
- [ ] Common utilities

**Mitigation:** Define contracts upfront in AGENTS.md.

---

## Output: Recommendation

Generate one of:

**If parallel is recommended:**
```
═══════════════════════════════════════════════════════════════
✅ RECOMMENDATION: Use Parallel Agents
═══════════════════════════════════════════════════════════════

Score: [X]/25
Suggested agents: [N]
Proposed split:
  1. [Role] - [archetype] - [boundaries]
  2. [Role] - [archetype] - [boundaries]
  3. [Role] - [archetype] - [boundaries]

Risks to watch:
  - [risk 1]
  - [risk 2]

**Next step:** Run `/scaffold-parallel-agent [task description]`
```

**If single stream is recommended:**
```
═══════════════════════════════════════════════════════════════
⚠️ RECOMMENDATION: Use Single Stream
═══════════════════════════════════════════════════════════════

Score: [X]/25
Reason: [why parallel doesn't fit]

Suggested approach:
  - Work on [area] first
  - Then [area]
  - Finally [area]

**Next step:** Just start working on the task directly.
```

---

## Error Handling

**Unclear Task Scope**: Ask clarifying questions about domains and dependencies before recommending.

**Edge Case**: If score is borderline (12-15), present both options with trade-offs.

**Complex Architecture**: Recommend `/solution-scaffold` first for multi-component designs.

## Examples

### Example 1: Good Parallel Candidate

```
/compare-parallel-agent "
Build customer portal with:
- React frontend
- FastAPI backend
- PostgreSQL schema
Need to deliver by Friday.
"
```

### Example 2: Poor Parallel Candidate

```
/compare-parallel-agent "
Refactor auth module to use new JWT library.
Changes span multiple files in same directory.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/parallel-agent/parallel-agent-constitution.md`
- **Start parallel**: Run `/scaffold-parallel-agent`
