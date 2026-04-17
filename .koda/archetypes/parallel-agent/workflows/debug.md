---
description: Unblock or repair a parallel run (escalations, ledger/status fixes, worktree repair, rollback support).
---

User input: $ARGUMENTS (issue description, or blank for general health check)

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

## Step 1: Diagnose the Problem

Check which issue applies:

### Issue A: Agent is Blocked
**Symptoms:** STATUS.md shows ⏸️ Blocked, agent can't proceed

**Fix:**
1. Check AGENTS.md "Decisions Needed" section
2. If decision pending → make the decision, update the table
3. If dependency on another agent → check that agent's status
4. Update STATUS.md to 🔄 Working after unblocking

---

### Issue B: Worktree Missing or Broken
**Symptoms:** `.trees/wt-[role]` doesn't exist or has detached HEAD

**Fix:**
```bash
# List current worktrees (cross-platform)
git worktree list

# If worktree missing, recreate from branch
git worktree add .trees/wt-[role] feat/parallel-[role]

# If detached HEAD, re-checkout branch
cd .trees/wt-[role]
git checkout feat/parallel-[role]
cd ../..  # Return to project root
```

---

### Issue C: AGENTS.md or STATUS.md Out of Sync
**Symptoms:** Files don't reflect actual state, agents confused

**Fix:**
1. Check each worktree's actual git status
2. Update AGENTS.md subtask checkboxes to match reality
3. Update STATUS.md agent statuses
4. Add note to Communication Log explaining the sync

---

### Issue D: Merge Conflict During /refactor-parallel-agent
**Symptoms:** Git merge failed, branches won't combine

**Fix:**
```bash
# Abort the failed merge
git merge --abort

# Create backup tag (cross-platform)
git tag backup-before-merge-$(date +%Y%m%d-%H%M%S)
# Windows PowerShell: git tag backup-before-merge-$(Get-Date -Format 'yyyyMMdd-HHmmss')

# Try merging one branch at a time in dependency order
git merge feat/parallel-[first-agent] --no-ff
# Resolve conflicts if any, then:
git merge feat/parallel-[second-agent] --no-ff
# Continue for each agent...
```

---

### Issue E: Agent Crashed or Window Closed
**Symptoms:** Work was in progress, window closed unexpectedly

**Fix:**
1. Open the worktree folder in a new Windsurf window
2. Check `git status` for uncommitted changes
3. Commit any work in progress: `git add . && git commit -m "WIP: [description]"`
4. Re-paste the agent launch instructions from AGENTS.md
5. Continue from last completed subtask

---

### Issue F: Need to Add/Remove an Agent
**Symptoms:** Scope changed, need different agent count

**To add an agent:**
```bash
# Create new worktree (cross-platform)
git worktree add .trees/wt-[newrole] feat/parallel-[newrole]

# Add agent section to AGENTS.md
# Add row to STATUS.md
# Generate launch instructions (see /scaffold-parallel-agent Step 7)
```

**To remove an agent:**
```bash
# Merge or abandon their work first!
git worktree remove .trees/wt-[role]
git branch -d feat/parallel-[role]  # or -D to force

# Remove from AGENTS.md and STATUS.md
```

---

## Step 2: Validate the Fix

After applying any fix, run `/test-parallel-agent` to confirm:
- All worktrees exist and are on correct branches
- AGENTS.md and STATUS.md are consistent
- No agents stuck in ⏸️ Blocked without a decision

---

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "fatal: 'X' is already checked out" | Branch in use elsewhere | Use different branch name or remove other worktree |
| "error: pathspec 'X' did not match" | Branch doesn't exist | Create branch first: `git branch feat/parallel-X` |
| "CONFLICT (content)" | Merge conflict | Resolve manually, commit, continue merge |

---

## Error Handling

**No Parallel Run Found**: Report that no `.trees/` directory exists and suggest running `/scaffold-parallel-agent` first.

**Multiple Issues**: Address blocking issues first, then worktree issues, then sync issues.

**Unrecoverable State**: Recommend starting fresh with new worktrees if state is too corrupted.

## Examples

### Example 1: Unblock Agent

```
/debug-parallel-agent "
Agent-2 (API) is blocked waiting on Agent-1 (Database).
Database schema not finalized.
"
```

### Example 2: Fix Broken Worktree

```
/debug-parallel-agent "
Worktree .trees/wt-frontend has detached HEAD.
Agent can't commit changes.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/parallel-agent/parallel-agent-constitution.md`
- **Validate**: Run `/test-parallel-agent` after fixes
- **Merge**: Run `/refactor-parallel-agent` when ready
