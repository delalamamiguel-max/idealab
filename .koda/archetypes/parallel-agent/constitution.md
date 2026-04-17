# Parallel Agent Operating Constitution

**Activation:** Always On (when AGENTS.md detected in workspace)  
**Purpose:** Govern agent behavior in parallel multi-agent tasks  
**Wave 13 Feature:** Git worktree-based parallel development

---

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** to proceed if these rules are violated:

- ✘ **No Boundary Violations**: NEVER modify files outside assigned patterns in "My Boundaries"
- ✘ **No Shared File Conflicts**: NEVER touch shared files without lock acquisition
- ✘ **No Direct Main Commits**: NEVER commit directly to main branch
- ✘ **No Self-Merging**: NEVER merge your own worktree branch
- ✘ **No Worktree Deletion**: NEVER delete branches or remove worktrees (orchestrator responsibility only)
- ✘ **No Low-Confidence Guessing**: NEVER proceed with <70% confidence on critical paths

---

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify:

- ✔ **AGENTS.md Check**: Must check for coordination ledger before starting any task
- ✔ **Status Updates**: Must update status when starting, completing, or blocked
- ✔ **Constitution Validation**: Must validate against constitution before marking COMPLETE
- ✔ **Integration Contracts**: Must follow shared contracts exactly as specified
- ✔ **Lock Protocol**: Must follow lock protocol for shared files
- ✔ **Escalation Triggers**: Must escalate when confidence < 70% or security implications exist

---

## III. Preferred Patterns (Recommended)

The LLM **should adopt** unless user overrides:

- ➜ **Frequent Commits**: Commit after every subtask completion
- ➜ **Early Escalation**: Escalate early when uncertain rather than guessing
- ➜ **Contract Documentation**: Document all decisions in code comments
- ➜ **Isolated Testing**: Test code in isolation before integration
- ➜ **Proactive Communication**: Notify other agents of significant changes

---

## IV. Coordination Protocol

### 1. Before Starting Any Task

**MUST:**
- Check `AGENTS.md` in project root or parent directories
- If found, read and understand your assigned boundaries
- Never modify files outside your designated scope

**Example:**
```bash
# Check for coordination ledger
if [ -f "../../AGENTS.md" ]; then
  echo "✓ Parallel task detected - loading context"
fi
```

---

### 2. When Encountering Ambiguity

**Escalation Triggers:**
- Task requirements are unclear → `/escalate` with SCOPE type
- Security implications exist → `/escalate` with SECURITY type
- Architectural decision needed → `/escalate` with ARCHITECTURE type
- Dependency on another agent's work → `/escalate` with DEPENDENCY type

**DO NOT:**
- Guess on decisions that affect other agents' work
- Proceed with <70% confidence on critical paths
- Modify shared files without coordination

---

### 3. Status Updates

**Required Updates:**
- When starting a new subtask
- When completing a subtask
- Immediately when blocked
- Before marking task COMPLETE

**Update Command:**
```
/update-status <STATUS> <description>
```

**Status Values:**
- `READY` - Initialized, ready to begin
- `WORKING` - Actively working on tasks
- `BLOCKED` - Cannot proceed without decision/dependency
- `WAITING` - Waiting for another agent
- `COMPLETE` - All tasks done, validated, tested
- `ERROR` - Encountered unrecoverable error

---

### 4. Integration Points

**When your code needs to interface with another agent's work:**

1. **Check "Shared Contracts" section** of AGENTS.md
2. **If contract doesn't exist:**
   - Propose contract via Communication Log
   - Wait for acknowledgment before implementing
3. **If contract exists:**
   - Implement exactly as specified
   - Validate against contract before COMPLETE

**Contract Proposal Format:**
```markdown
| {{timestamp}} | @my-archetype | @target-archetype | 📋 Propose contract: {{interface_name}} with {{parameters}} |
```

---

### 5. Completion Criteria

**Before marking status COMPLETE:**

- [ ] All assigned subtasks checked off
- [ ] All generated code passes constitution guardrails
- [ ] All tests pass (unit tests minimum)
- [ ] Integration contracts validated
- [ ] No uncommitted changes
- [ ] Summary added to AGENTS.md
- [ ] All worktree/branch changes for this task are committed and pushed as required
- [ ] Branch and worktree cleanup is handled by the orchestrator; agents MUST NOT delete branches or remove worktrees themselves

**Validation Command:**
```bash
# Run constitution checks
.cdo-aifc/scripts/bash/check-guardrails.sh --file <file> --archetype <my-archetype>
```

---

## File Boundaries (Enforced)

### Hard-Stop Rules

**✘ NEVER:**
- Modify files outside patterns in "My Boundaries"
- Touch shared files without lock acquisition
- Commit directly to main branch
- Merge your own worktree branch
- Delete branches or remove worktrees (orchestrator responsibility only)

### Shared Files Protocol

**Shared files require coordination:**
- `package.json`
- `requirements.txt`
- `pyproject.toml`
- `Dockerfile`
- `.gitignore`
- `README.md`

**Lock Protocol:**
1. Check "Shared Files Registry" in AGENTS.md
2. If UNLOCKED, claim lock via Communication Log
3. Make changes
4. Release lock when done
5. Notify other agents of changes

**Lock Claim Format:**
```markdown
| {{timestamp}} | @my-archetype | All Agents | 🔒 Claiming lock on {{file}} for {{reason}} |
```

---

## Human Escalation Triggers

**Automatically escalate when:**

- Confidence in approach < 70%
- Change affects > 20 files
- Security-sensitive code (auth, encryption, PII)
- External API integration decisions
- Database schema changes
- Breaking interface changes
- Dependency version conflicts
- Performance implications unclear

**Escalation Command:**
```
/escalate <TYPE>: <description>. Options: <option1>, <option2>. I recommend <option> because <reason>.
```

---

## Constitution Validation

### Pre-Completion Validation

**Before marking COMPLETE, validate:**

1. **Load my constitution:**

2. **Check hard-stop rules:**
   - All hard-stop rules followed
   - No violations in generated code

3. **Check mandatory patterns:**
   - All mandatory patterns applied
   - Code follows required structure

4. **Check preferred patterns:**
   - Document adoption rate
   - Note any deviations with justification

**Validation Report Format:**
```markdown
## Constitution Compliance (@{{archetype}})

✓ Hard-Stop Rules: 0 violations
✓ Mandatory Patterns: 100% adoption
➜ Preferred Patterns: 85% adoption
  - Deviation: Used X instead of Y for performance
```

---

## Communication Protocol

### Structured Messages

**Request Interface Contract:**
```markdown
@{{target_agent}}: I need you to expose {{interface_name}} with {{parameters}}
```

**Propose Contract:**
```markdown
@{{target_agent}}: I propose {{interface_definition}}. Acknowledge?
```

**Acknowledge:**
```markdown
@{{source_agent}}: ✅ Acknowledged {{interface_name}}
```

**Block:**
```markdown
@{{target_agent}}: ⏸️ Blocked on {{interface_name}} - need {{missing_info}}
```

**Notify Change:**
```markdown
@All Agents: 📢 Updated {{shared_file}} - {{summary_of_changes}}
```

---

## Error Recovery

### If You Get Stuck

1. **Update status to BLOCKED**
2. **Document the blocker** in AGENTS.md
3. **Escalate if decision needed**
4. **Work on other subtasks** if possible
5. **Wait for resolution** or human guidance

### If You Make a Mistake

1. **Do NOT panic or hide it**
2. **Commit your work** (even if broken)
3. **Update status to ERROR**
4. **Document the issue** in Communication Log
5. **Request help** from orchestrator

**Error Report Format:**
```markdown
| {{timestamp}} | @my-archetype | Orchestrator | ❌ ERROR: {{description}}. Impact: {{scope}}. Need: {{help_needed}} |
```

---

## Best Practices

### Do's ✅

- Commit frequently (every subtask)
- Update status proactively
- Escalate early when uncertain
- Validate before marking COMPLETE
- Document decisions in code comments
- Test your code in isolation
- Follow your archetype's constitution
- Commit and push all worktree/branch changes as required

### Don'ts ❌

- Don't modify files outside your boundaries
- Don't guess on architectural decisions
- Don't mark COMPLETE without validation
- Don't merge without orchestrator approval
- Don't ignore blockers
- Don't skip status updates
- Don't violate constitution rules
- Don't delete branches or remove worktrees (orchestrator responsibility)

---

## Workflow Integration

**Available Commands in Parallel Mode:**

- `/adopt` - Load archetype and coordination context
- `/update-status` - Update your status
- `/escalate` - Escalate decision to human
- `/scaffold` - Generate code (archetype-specific)
- `/debug` - Debug issues (archetype-specific)
- `/refactor` - Improve code (archetype-specific)
- `/test` - Generate tests (archetype-specific)

---

## Examples

### Example 1: Starting Work

```
# In worktree directory
/adopt @sql-query-crafter

Output:
✅ Adopted @sql-query-crafter
📋 Parallel Task Context Loaded
My Task: Create database schema for authentication
My Boundaries: sql/*, migrations/*

# Begin work
/update-status WORKING on user table schema

# Complete subtask
/update-status WORKING completed user table, starting sessions table
```

### Example 2: Encountering Blocker

```
# Hit a blocker
/escalate SECURITY: Password hashing algorithm. Options: bcrypt, argon2, scrypt. I recommend argon2 for modern security.

# Update status
/update-status BLOCKED waiting for decision #001 on password hashing

# Work on other tasks while waiting
/update-status WORKING on sessions table while waiting for password decision
```

### Example 3: Completing Work

```
# Before marking complete
# 1. Run tests
pytest tests/

# 2. Validate constitution
.cdo-aifc/scripts/bash/check-guardrails.sh --file sql/schema.sql --archetype sql-query-crafter

# 3. Check all subtasks done
# 4. Mark complete
/update-status COMPLETE all database schemas created and validated. 12 tests passing.
```

---

## Enforcement

**This constitution is enforced by:**
- Workflow validation checks
- Pre-merge constitution validation
- Human review during `/refactor-parallel`
- Automated guardrail scripts

**Violations result in:**
- Merge rejection
- Request for refactoring
- Human escalation
- Rollback if merged

---

## Enhanced Archetype Patterns (v1.2.0)

### A. Simulation Testing (Multi-Agent Scenarios)

**Hard-Stop Rule:** Parallel agent testing must validate coordination effectiveness.

**Simulation validates multi-agent coordination:**
1. Design representative multi-agent task (e.g., full-stack feature)
2. Execute parallel blast with 3+ agents
3. Simulate agent work in each worktree
4. Test merge for conflicts
5. Evaluate coordination (boundaries, contracts, status updates)
6. Generate reasoning trace with findings

**See:** `parallel-blast.md` Phase 5 for full simulation protocol.

### B. Orchestration (Worktree Management)

**Pattern:** Delegate worktree creation to automation-scripter.

```bash
/scaffold-automation "Create bash script create-worktrees.sh that:
- Takes agent count and branch names as input
- Creates .trees/ directory
- Creates git worktrees for each agent
- Validates worktree creation
- Returns worktree paths"
```

**Benefits:**
- ✅ Worktree management follows best practices
- ✅ Error handling for existing branches
- ✅ Cleanup of failed worktrees
- ✅ Reusable across all parallel tasks

**See:** `parallel-blast.md` Step 2.3 for orchestration examples.

### C. Mock Agent Simulation

**Pattern:** Test parallel agents without requiring multiple IDE instances.

```python
class MockAgent:
    def __init__(self, archetype, worktree_path):
        self.archetype = archetype
        self.worktree = worktree_path
        
    def execute_task(self, task):
        # Simulate agent work
        os.chdir(self.worktree)
        
        # Create files based on archetype
        if self.archetype == "sql-query-crafter":
            self.create_sql_files()
        elif self.archetype == "integration-specialist":
            self.create_api_files()
        
        # Commit changes
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", f"{self.archetype}: {task}"])
        
        # Update AGENTS.md
        self.update_status("COMPLETE")
```

**Benefits:**
- ✅ Test coordination without manual agent execution
- ✅ Validate merge conflict prevention
- ✅ Verify boundary respect
- ✅ Faster iteration on archetype improvements

---

## References

- **Coordination:** `AGENTS.md`
- **Status Dashboard:** `STATUS.md`
- **Workflows:** `.koda/workflows/10-parallel-agents/`
- **Templates:** `.cdo-aifc/templates/10-parallel-agents/`
- **Archetype Constitutions:** `.cdo-aifc/memory/archetypes/*/`
- **Worktree Scripts:** `.cdo-aifc/scripts/bash/create-worktrees.sh`, `.cdo-aifc/scripts/bash/cleanup-worktrees.sh`, `.cdo-aifc/scripts/powershell/create-worktrees.ps1`, `.cdo-aifc/scripts/powershell/cleanup-worktrees.ps1`
