---
description: Initialize a parallel run (create worktrees, ledger, STATUS) and adopt agents; resumes existing runs if found.
---

User input: $ARGUMENTS (task description)

## Overview

This workflow helps you split a complex task across multiple Cascade agents working in parallel. Each agent gets its own Git worktree (isolated workspace) and coordinates through shared AGENTS.md and STATUS.md files.

---

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

**SUCCESS CRITERIA**:
- Search for directory: "00-core-orchestration"
- Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory

**HALT IF**:
- Directory "00-core-orchestration" is not found
- `${ARCHETYPES_BASEDIR}` is not set

Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

---

## Step 1: Analyze the Task

**Option A: Simple Domain Split**
Parse $ARGUMENTS to identify natural boundaries (database, API, frontend, tests).

**Option B: Complex Solution Architecture**
If the task involves multiple technical domains (ML + Data + Infrastructure), check if `/solution-scaffold` should be run first to identify the correct archetypes and integration patterns.

Identify:
- **Domains involved** (database, API, frontend, tests, docs, etc.)
- **Natural boundaries** (files/folders each agent owns exclusively)
- **Dependencies** (which work must complete before other work can start)

**Good parallel candidates:**
- Work spans 2-4 distinct domains
- Each domain has clear file ownership
- Minimal shared files between domains

**Bad parallel candidates:**
- Tightly coupled changes across many files
- Single-file refactoring
- Unclear ownership boundaries

---

## Step 2: Check for Existing Run

Look for `.trees/` directory and `AGENTS.md` in project root.

**If found:** Show resume instructions:
```
⚠️ Existing parallel run detected!

To resume:
1. Check AGENTS.md for current status
2. Open worktrees listed in .trees/
3. Continue from where agents left off

To start fresh:
1. Run: rm -rf .trees AGENTS.md STATUS.md
2. Re-run /scaffold-parallel
```

**If not found:** Continue to Step 3.

---

## Step 3: Design Agent Assignments

For the task, create 2-4 agent assignments. Each agent needs:
- **Role name** (short, descriptive)
- **Archetype** (from the available archetypes)
- **File boundaries** (glob patterns for exclusive ownership)
- **Subtasks** (3-5 specific deliverables)

**Example for "Add user authentication":**

| Agent | Archetype | Boundaries | Subtasks |
|-------|-----------|------------|----------|
| Database | sql-query-crafter | `sql/*`, `migrations/*` | User table, sessions table, indexes |
| API | integration-specialist | `backend/api/*`, `backend/auth/*` | Login endpoint, token refresh, middleware |
| Frontend | app-maker | `frontend/src/auth/*`, `frontend/src/pages/Login*` | Login form, auth context, protected routes |

---

## Step 4: Create Worktrees

For each agent, create an isolated Git worktree:

```bash
# Create worktree directory (works on Mac/Linux/Windows Git Bash)
mkdir -p .trees

# Windows PowerShell alternative:
# New-Item -ItemType Directory -Force -Path .trees

# Create worktree for each agent (example for 3 agents)
git worktree add .trees/wt-database feat/parallel-database
git worktree add .trees/wt-api feat/parallel-api  
git worktree add .trees/wt-frontend feat/parallel-frontend
```

---

## Step 5: Create AGENTS.md

Create `AGENTS.md` in project root with this structure:

```markdown
# Parallel Agent Coordination

**Task:** [Task description from $ARGUMENTS]
**Created:** [Current timestamp]
**Status:** 🟡 In Progress

## Agents

### Agent 1: [Role Name]
- **Worktree:** `.trees/wt-[role]`
- **Branch:** `feat/parallel-[role]`
- **Archetype:** @[archetype_1]
- **Boundaries:** `[glob patterns]`
- **Status:** ⏳ Ready
- **Subtasks:**
  - [ ] [Subtask 1]
  - [ ] [Subtask 2]
  - [ ] [Subtask 3]

### Agent 2: [Role Name]
[Same structure...]

## Merge Order
1. [First agent - no dependencies]
2. [Second agent - depends on first]
3. [Third agent - depends on second]

## Decisions Needed
| ID | Agent | Question | Options | Decision |
|----|-------|----------|---------|----------|
| - | - | - | - | - |

## Communication Log
| Time | From | Message |
|------|------|---------|
| [now] | Orchestrator | Parallel run initialized |
```

---

## Step 6: Create STATUS.md

Create `STATUS.md` in project root:

```markdown
# Agent Status Dashboard

**Last Updated:** [timestamp]

| Agent | Status | Current Task | Blocked By |
|-------|--------|--------------|------------|
| [Role 1] | ⏳ Ready | Waiting to start | - |
| [Role 2] | ⏳ Ready | Waiting to start | - |
| [Role 3] | ⏳ Ready | Waiting to start | - |

## Status Legend
- ⏳ Ready - Not started
- 🔄 Working - In progress  
- ⏸️ Blocked - Waiting on decision/dependency
- ✅ Complete - All subtasks done
- ❌ Error - Needs help
```

---

## Step 7: Generate Agent Launch Instructions

**This is the key output.** Generate copy-paste ready text for each agent window.

**IMPORTANT:** Identify which agents have dependencies and mark them clearly.

For each agent, output:

```
═══════════════════════════════════════════════════════════════
🤖 AGENT [N]: [ROLE NAME]
═══════════════════════════════════════════════════════════════

⚠️ DEPENDENCY: [If agent depends on others, say: "WAIT for Agent X to complete before starting" | Otherwise: "No dependencies - start immediately"]

💰 CREDIT TIP: [If sequential: "Save credits - start this agent AFTER Agent X completes" | If parallel: "Can run in parallel with other agents"]

📂 OPEN THIS FOLDER IN A NEW WINDSURF WINDOW:
   [absolute path to worktree]
   (Windows: C:\project\.trees\wt-[role])
   (Mac/Linux: /path/to/project/.trees/wt-[role])

📋 PASTE THIS INTO THAT WINDOW'S CASCADE CHAT:
───────────────────────────────────────────────────────────────
I am Agent [N] ([Role Name]) in a parallel development task.

**My Assignment:**
- Archetype: @[AGENT_ARCHETYPE]
- Branch: feat/parallel-[role]
- Boundaries: [glob patterns]

**My Subtasks:**
1. [Subtask 1]
2. [Subtask 2]
3. [Subtask 3]

**Rules:**
- Only modify files matching my boundaries
- Create MANIFEST.md documenting all changes
- Update STATUS.md when I change status
- Add to AGENTS.md Communication Log if I need help
- Mark subtasks complete in AGENTS.md as I finish them
- Commit work when complete

**Important Files:**
- Read: ../AGENTS.md (main coordination)
- Read: ${ARCHETYPES_BASEDIR}/parallel-agent/parallel-agent-constitution.md
- Update: ../STATUS.md (your status)
- Create: MANIFEST.md (your changes)

Start with subtask 1. Let's go!
───────────────────────────────────────────────────────────────
```

---

## Step 8: Orchestrator Instructions

Tell the user (orchestrator) what to do:

```
═══════════════════════════════════════════════════════════════
🎯 ORCHESTRATOR INSTRUCTIONS (This Window)
═══════════════════════════════════════════════════════════════

**LAUNCH SEQUENCE:**

1. **Start Independent Agents First** (no dependencies):
   - Open new Windsurf windows for agents marked "No dependencies"
   - Copy-paste their launch text
   - Let them work in parallel

2. **Start Dependent Agents After** (marked with WAIT):
   - Wait for prerequisite agents to show ✅ Complete in STATUS.md
   - Then open windows for dependent agents
   - This saves Windsurf credits!

3. **Monitor Progress:**
   - Check STATUS.md regularly: `cat STATUS.md`
   - Answer questions in AGENTS.md "Decisions Needed"
   - Help blocked agents

4. **Merge When Complete:**
   - All agents show ✅ Complete in STATUS.md
   - Run: `/refactor-parallel`

**💰 CREDIT OPTIMIZATION:**
- Agents with dependencies should start AFTER their prerequisites
- Only run truly independent agents in parallel
- Check "DEPENDENCY" warnings in agent launch instructions

**Quick Commands:**
- Check status: `cat STATUS.md`
- See full state: `cat AGENTS.md`
- Merge when ready: `/refactor-parallel`
```

---

## Error Handling

**Branch Exists**: Offer to reuse existing branch or create new unique branch name.

**Worktree Creation Fails**: Clean up partial state, report error, suggest fix.

**Insufficient Agents**: Recommend minimum of 2 agents; maximum of 4 for practical coordination.

---

## Examples

### Example 1: Web App Development

```
/scaffold-parallel-agent "
Build customer dashboard with React frontend,
FastAPI backend, and PostgreSQL schema.
Deadline: Friday.
"
```

### Example 2: Resume Existing Run

```
/scaffold-parallel-agent "
Resume work on ticket-123 parallel run.
I'm taking over Agent-2 (API).
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/parallel-agent/parallel-agent-constitution.md`
- **Troubleshooting**: Run `/debug-parallel-agent` if issues arise
- **Merge**: Run `/refactor-parallel-agent` when all agents complete
- **Health Check**: Run `/test-parallel-agent` to validate run status
