---
description: Merge all agent branches back to main branch after parallel work is complete.
---

User input: $ARGUMENTS (optional: specific agents to merge, or "all")

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

## Prerequisites

Before merging, verify:
- [ ] All agents show Complete in STATUS.md
- [ ] No pending items in AGENTS.md "Decisions Needed"
- [ ] Each agent has committed all work

---

## Step 1: Pre-Merge Checklist

```bash
# Check all worktrees are clean (cross-platform)
git worktree list

# For each worktree, verify no uncommitted changes
cd .trees/wt-[role]
git status
cd ../..
```

If any worktree has uncommitted changes, have that agent commit first.

---

## Step 2: Create Safety Checkpoint

```bash
# Tag current state for easy rollback
git tag pre-parallel-merge-$(date +%Y%m%d-%H%M%S)
# Windows PowerShell: git tag pre-parallel-merge-$(Get-Date -Format 'yyyyMMdd-HHmmss')
```

---

## Step 3: Determine Merge Order

Check AGENTS.md "Merge Order" section. Merge in dependency order:
1. Foundation layer first (no dependencies)
2. Service layer second (depends on foundation)
3. Consumer layer last (depends on services)

---

## Step 4: Prepare for Merge (Avoid Conflicts)

**Move coordination files out of the way to prevent merge conflicts:**

```bash
# Create archive directory
mkdir -p .parallel-archive
# Windows PowerShell: New-Item -ItemType Directory -Force -Path .parallel-archive

# Move coordination files temporarily
mv AGENTS.md .parallel-archive/AGENTS-temp.md
mv STATUS.md .parallel-archive/STATUS-temp.md
mv MANIFEST.md .parallel-archive/MANIFEST-temp.md 2>/dev/null || true
# Windows PowerShell: Move-Item AGENTS.md .parallel-archive/AGENTS-temp.md
```

---

## Step 5: Execute Merges

For each agent branch, in order:

```bash
# Merge first agent (foundation) - cross-platform
git merge feat/parallel-[first-agent] --no-ff -m "Merge parallel agent: [role]"

# If conflict in coordination files (AGENTS.md, STATUS.md, MANIFEST.md):
#   git checkout --ours [file]  # Keep our version
#   git add [file]
#   git commit

# If conflict in actual code:
#   1. Resolve conflicts in affected files
#   2. git add [resolved files]
#   3. git commit

# Merge second agent
git merge feat/parallel-[second-agent] --no-ff -m "Merge parallel agent: [role]"

# Continue for remaining agents...
```

---

## Step 6: Post-Merge Validation

```bash
# Run project tests (cross-platform)
# Adjust command for your project:
npm test          # Node.js projects
# pytest          # Python projects
# mvn test        # Java projects

# Verify application still works
# Start dev server and smoke test
```

---

## Step 7: Cleanup

After successful merge:

```bash
# Remove worktrees (cross-platform)
git worktree remove .trees/wt-[role1]
git worktree remove .trees/wt-[role2]
git worktree remove .trees/wt-[role3]

# Remove worktree directory
rm -rf .trees
# Windows PowerShell: Remove-Item -Recurse -Force .trees

# Delete coordination files (already preserved in git history)
rm -f AGENTS.md STATUS.md MANIFEST.md
# Windows PowerShell: Remove-Item -Force AGENTS.md, STATUS.md, MANIFEST.md -ErrorAction SilentlyContinue

# Commit cleanup
git add -A
git commit -m "chore: Clean up parallel agent coordination files and worktrees"

# MANDATORY: Delete feature branches created for parallel task
echo "Cleaning up parallel branches..."
git branch -d feat/parallel-[role1]
git branch -d feat/parallel-[role2]
git branch -d feat/parallel-[role3]

# Verify no parallel branches remain
echo "Verifying cleanup..."
git branch | grep "feat/parallel-" || echo " All parallel branches cleaned up successfully"
```

---

## Rollback (If Needed)

If merge goes wrong:

```bash
# Reset to pre-merge state (cross-platform)
git reset --hard pre-parallel-merge-[timestamp]

# Worktrees still exist, agents can continue working
```

---

## Output Summary

After successful merge, output:

```
═══════════════════════════════════════════════════════════════
 PARALLEL MERGE COMPLETE
═══════════════════════════════════════════════════════════════

Agents merged: [list]
Branches cleaned: [list]
Feature branches deleted: [list]
Coordination files: Deleted (preserved in git history)
Worktrees: Removed
Git cleanup:  Verified (no orphaned branches)

Rollback tag: pre-parallel-merge-[timestamp]

**Next Steps:**
1. Review changes: git log --oneline -10
2. Push to remote: git push origin [branch]
3. All parallel artifacts have been cleaned up
```

---

## Error Handling

**Merge Conflicts**: Pause merge, show conflict files, and provide resolution guidance.

**Incomplete Agent**: Block merge for agents not marked Complete in STATUS.md.

**Failed Cleanup**: Retry worktree removal; report any that require manual cleanup.

## Examples

### Example 1: Merge All Agents

```
/refactor-parallel-agent "all"
```

### Example 2: Merge Specific Agents

```
/refactor-parallel-agent "
Merge only database and api agents.
Frontend not ready yet.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/parallel-agent/parallel-agent-constitution.md`
- **Troubleshooting**: Run `/debug-parallel-agent` if merge fails
- **Health Check**: Run `/test-parallel-agent` before merging

