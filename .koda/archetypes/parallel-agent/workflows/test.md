---
description: Validate coordination health: AGENTS/STATUS consistency, worktree presence, blockers, and pre-merge checks.
---

User input: $ARGUMENTS (optional: "quick" for fast check, or blank for full validation)

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

## Quick Health Check

Run these commands and report results:

```bash
# 1. Check coordination files exist (cross-platform)
ls AGENTS.md STATUS.md .trees 2>/dev/null && echo "Files exist" || echo "Missing files"
# Windows PowerShell: Test-Path AGENTS.md; Test-Path STATUS.md; Test-Path .trees

# 2. List worktrees (cross-platform)
git worktree list

# 3. Show current status (cross-platform)
cat STATUS.md
# Windows PowerShell: Get-Content STATUS.md
```

---

## Full Validation Checklist

### Check 1: Coordination Files
- [ ] `AGENTS.md` exists in project root
- [ ] `STATUS.md` exists in project root
- [ ] `.trees/` directory exists

**If missing:** Run `/scaffold-parallel-agent` to initialize or `/debug-parallel-agent` to repair.

---

### Check 2: Worktree Integrity

For each agent listed in AGENTS.md:

```bash
# Verify worktree exists (cross-platform)
ls .trees/wt-[role] 2>/dev/null && echo "Exists" || echo "Missing"
# Windows PowerShell: Test-Path .trees/wt-[role]

# Verify correct branch (cross-platform)
cd .trees/wt-[role]
git branch --show-current  # Should match AGENTS.md
cd ../..
```

- [ ] All worktrees exist
- [ ] All worktrees on correct branches (not detached HEAD)
- [ ] No extra worktrees not in AGENTS.md

**If issues:** Run `/debug-parallel-agent` Issue B.

---

### Check 3: Status Consistency

Compare AGENTS.md and STATUS.md:
- [ ] Same agents listed in both files
- [ ] Status values match between files
- [ ] No agent stuck in ⏸️ Blocked for >30 minutes without escalation

**If mismatch:** Run `/debug-parallel-agent` Issue C.

---

### Check 4: Blocker Review

Check AGENTS.md "Decisions Needed" section:
- [ ] All blocked agents have corresponding decision request
- [ ] No stale decisions (decided but agent still blocked)

**If blockers:** Orchestrator should make decisions, then agents continue.

---

### Check 5: Pre-Merge Readiness (if all agents ✅ Complete)

For each agent:
```bash
# Cross-platform git commands
cd .trees/wt-[role]
git status  # Should be clean
git log -1 --oneline  # Verify recent commits
cd ../..
```

- [ ] All worktrees have clean git status
- [ ] All subtasks checked off in AGENTS.md
- [ ] Merge order defined in AGENTS.md

**If ready:** Run `/refactor-parallel-agent` to merge.

---

## Output Report

Generate summary:

```
═══════════════════════════════════════════════════════════════
📋 PARALLEL RUN HEALTH CHECK
═══════════════════════════════════════════════════════════════

✅ Coordination Files: OK
✅ Worktree Integrity: OK (3/3 worktrees valid)
✅ Status Consistency: OK
⚠️ Blockers: 1 pending decision
⏳ Pre-Merge: Not ready (2/3 agents complete)

**Next Action:** Answer decision #1 in AGENTS.md, then agents can continue.
```

---

## Error Handling

**No Parallel Run**: Report that no coordination files exist and suggest `/scaffold-parallel-agent`.

**Inconsistent State**: Flag specific mismatches and recommend `/debug-parallel-agent`.

**Merge Not Ready**: List incomplete agents and pending decisions.

## Examples

### Example 1: Quick Check

```
/test-parallel-agent "quick"
```

### Example 2: Full Validation

```
/test-parallel-agent "
Full pre-merge validation.
Check all 3 agents are ready.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/parallel-agent/parallel-agent-constitution.md`
- **Fix issues**: Run `/debug-parallel-agent`
- **Merge when ready**: Run `/refactor-parallel-agent`
