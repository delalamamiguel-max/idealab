---
description: Quick reference guide for parallel agent operating norms.
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

## Parallel Agents Quick Reference

### Status Values

| Status | Emoji | Meaning | When to Use |
|--------|-------|---------|-------------|
| Ready | ⏳ | Not started | Initial state |
| Working | 🔄 | In progress | Actively coding |
| Blocked | ⏸️ | Can't proceed | Waiting on decision/dependency |
| Complete | ✅ | All done | All subtasks finished |
| Error | ❌ | Needs help | Unrecoverable issue |

---

### Agent Rules

1. **Stay in your lane** - Only modify files matching your boundaries
2. **Update status** - Change STATUS.md when your state changes
3. **Escalate early** - Don't spin on decisions >30 minutes
4. **Commit often** - Small commits, clear messages
5. **Mark progress** - Check off subtasks in AGENTS.md as you complete them

---

### Escalation Protocol

**When to escalate:**
- Architectural decision needed
- Security-sensitive choice
- Dependency on another agent's incomplete work
- Unclear requirements
- Confidence <70% on approach

**How to escalate:**
1. Update STATUS.md to ⏸️ Blocked
2. Add row to AGENTS.md "Decisions Needed" table:
   | ID | Agent | Question | Options | Decision |
   |----|-------|----------|---------|----------|
   | 1 | [You] | [Question] | A, B, C | (pending) |
3. Continue other subtasks if possible

---

### Communication Log Format

Add entries to AGENTS.md Communication Log:

| Time | From | Message |
|------|------|---------|
| 10:30 | Database | User table schema complete, ready for API to consume |
| 10:45 | API | Acknowledged, starting auth endpoints |
| 11:00 | Frontend | Blocked on API contract for login response shape |

---

### Merge Order

Typical dependency layers:
1. **Foundation** (database, schemas) - merge first
2. **Service** (API, backend logic) - merge second
3. **Consumer** (frontend, tests) - merge last

---

### Workflow Commands

| Command | Purpose |
|---------|----------|
| `/scaffold-parallel-agent` | Start new parallel run |
| `/test-parallel-agent` | Check health of current run |
| `/debug-parallel-agent` | Fix issues with run |
| `/refactor-parallel-agent` | Merge all agents when complete |
| `/compare-parallel-agent` | Decide if task fits parallel model |

---

### File Locations

| File | Purpose |
|------|---------|
| `AGENTS.md` | Main coordination ledger |
| `STATUS.md` | Quick status dashboard |
| `.trees/wt-*` | Agent worktrees |
| `.parallel-archive/` | Completed run archives |

---

### Constitution

Full rules at: `${ARCHETYPES_BASEDIR}/parallel-agent/parallel-agent-constitution.md`

Key hard-stops:
- Never modify files outside your boundaries
- Never merge your own branch
- Never commit secrets
- Always update status when blocked

---

## Error Handling

**No Parallel Run Active**: Note that this is a reference guide; suggest `/scaffold-parallel-agent` to start.

**Unclear Role**: Clarify agent boundaries and file ownership rules.

**Protocol Confusion**: Provide specific section reference from this guide.

## Examples

### Example 1: Quick Reference

```
/document-parallel-agent "
Show me the escalation protocol.
"
```

### Example 2: Status Meanings

```
/document-parallel-agent "
What do the different status emojis mean?
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/parallel-agent/parallel-agent-constitution.md`
- **Start parallel**: Run `/scaffold-parallel-agent`
- **Health check**: Run `/test-parallel-agent`
