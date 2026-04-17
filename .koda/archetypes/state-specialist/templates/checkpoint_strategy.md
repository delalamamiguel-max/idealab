# Checkpoint Strategy for LangGraph Agents

## Overview

Checkpointing enables agents to:
- Resume from interruption points
- Implement human-in-the-loop patterns
- Recover from crashes
- Debug agent execution
- Replay conversations

## Checkpoint Storage Options

### 1. MemorySaver (Development/Testing)

**Use Case:** Development, testing, short-lived sessions

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
```

**Pros:**
- Fast (in-memory)
- No setup required
- Good for testing

**Cons:**
- Lost on restart
- Not suitable for production
- No persistence

### 2. SqliteSaver (Production - Single Instance)

**Use Case:** Production agents, single-instance deployments

```python
from pathlib import Path
from langgraph.checkpoint.sqlite import SqliteSaver

db_path = str(Path(AGENT_DATA) / agent_name / "checkpoints.db")
checkpointer = SqliteSaver.from_conn_string(db_path)
app = workflow.compile(checkpointer=checkpointer)
```

**Pros:**
- Persistent across restarts
- Good performance
- No external dependencies
- Built-in cleanup support

**Cons:**
- Single-instance only
- Not suitable for distributed systems

### 3. PostgreSQL/Redis (Production - Distributed)

**Use Case:** Production agents, distributed deployments, high availability

```python
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:pass@host:5432/dbname"
)
app = workflow.compile(checkpointer=checkpointer)
```

**Pros:**
- Supports multiple instances
- High availability
- Scalable
- Production-grade

**Cons:**
- Requires external service
- More complex setup
- Higher latency than SQLite

## Checkpoint Configuration

### Thread ID Strategy

Thread IDs identify conversation sessions:

```python
# User-based thread ID
thread_id = f"user_{user_id}"

# Session-based thread ID
thread_id = f"session_{session_id}"

# Conversation-based thread ID
thread_id = f"conv_{conversation_id}"

# Invoke with thread ID
result = app.invoke(
    input_data,
    config={"configurable": {"thread_id": thread_id}}
)
```

### Checkpoint Metadata

Add metadata to checkpoints for filtering and debugging:

```python
result = app.invoke(
    input_data,
    config={
        "configurable": {
            "thread_id": thread_id,
            "checkpoint_metadata": {
                "user_id": user_id,
                "session_type": "support",
                "environment": "production"
            }
        }
    }
)
```

## Checkpoint Cleanup Strategies

### Time-Based Retention

```python
from datetime import datetime, timedelta
from langgraph.checkpoint.sqlite import SqliteSaver

def cleanup_old_checkpoints(checkpointer: SqliteSaver, retention_days: int = 30):
    """Remove checkpoints older than retention period."""
    cutoff = datetime.now() - timedelta(days=retention_days)
    
    # Implementation depends on checkpointer type
    # For SQLite:
    conn = checkpointer.conn
    conn.execute(
        "DELETE FROM checkpoints WHERE created_at < ?",
        (cutoff.isoformat(),)
    )
    conn.commit()
```

### Session-Based Cleanup

```python
def cleanup_completed_sessions(checkpointer, thread_ids: list[str]):
    """Remove checkpoints for completed sessions."""
    for thread_id in thread_ids:
        checkpointer.delete_thread(thread_id)
```

### Size-Based Cleanup

```python
def cleanup_by_size(checkpointer, max_checkpoints: int = 1000):
    """Keep only the most recent N checkpoints per thread."""
    # Get all threads
    threads = checkpointer.list_threads()
    
    for thread_id in threads:
        checkpoints = checkpointer.list_checkpoints(thread_id)
        
        if len(checkpoints) > max_checkpoints:
            # Keep most recent, delete oldest
            to_delete = checkpoints[:-max_checkpoints]
            for checkpoint in to_delete:
                checkpointer.delete_checkpoint(checkpoint.id)
```

## Human-in-the-Loop Pattern

Use `interrupt_before` to pause execution for human approval:

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("analyze", analyze_node)
workflow.add_node("execute", execute_node)

# Add edges
workflow.add_edge("analyze", "execute")
workflow.add_edge("execute", END)

# Set entry point
workflow.set_entry_point("analyze")

# Compile with interrupt
app = workflow.compile(
    checkpointer=checkpointer,
    interrupt_before=["execute"]  # Pause before execute node
)

# First invocation - stops at interrupt
result = app.invoke(
    {"input": "delete all data"},
    config={"configurable": {"thread_id": "user_123"}}
)

# Human reviews and approves
if user_approves():
    # Resume from checkpoint
    result = app.invoke(
        None,  # No new input needed
        config={"configurable": {"thread_id": "user_123"}}
    )
```

## Checkpoint Recovery

### Crash Recovery

```python
def recover_from_crash(agent_name: str, thread_id: str):
    """Recover agent execution after crash."""
    # Load checkpointer
    from pathlib import Path
    db_path = str(Path(AGENT_DATA) / agent_name / "checkpoints.db")
    checkpointer = SqliteSaver.from_conn_string(db_path)
    
    # Recompile app with same checkpointer
    app = workflow.compile(checkpointer=checkpointer)
    
    # Resume from last checkpoint
    result = app.invoke(
        None,  # Resume with existing state
        config={"configurable": {"thread_id": thread_id}}
    )
    
    return result
```

### Checkpoint Replay

```python
def replay_conversation(thread_id: str):
    """Replay conversation from checkpoints."""
    checkpoints = checkpointer.list_checkpoints(thread_id)
    
    for checkpoint in checkpoints:
        state = checkpointer.get(checkpoint.id)
        print(f"Step {checkpoint.step}:")
        print(f"  State: {state}")
        print(f"  Timestamp: {checkpoint.timestamp}")
```

## Best Practices

### 1. Choose Appropriate Checkpointer

- **Development:** MemorySaver
- **Production (single instance):** SqliteSaver
- **Production (distributed):** PostgresSaver or Redis

### 2. Implement Cleanup Policies

```python
# Schedule cleanup job
import schedule

schedule.every().day.at("02:00").do(
    cleanup_old_checkpoints,
    checkpointer=checkpointer,
    retention_days=30
)
```

### 3. Monitor Checkpoint Storage

```python
def get_checkpoint_stats(agent_name: str) -> dict:
    """Get checkpoint storage statistics."""
    db_path = f"{AGENT_DATA}/{agent_name}/checkpoints.db"
    
    return {
        "db_size_mb": Path(db_path).stat().st_size / (1024 * 1024),
        "total_checkpoints": checkpointer.count_checkpoints(),
        "active_threads": len(checkpointer.list_threads())
    }
```

### 4. Set Checkpoint TTL

```python
# Add TTL to checkpoint metadata
config = {
    "configurable": {
        "thread_id": thread_id,
        "checkpoint_metadata": {
            "ttl_hours": 24,
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
        }
    }
}
```

### 5. Backup Critical Checkpoints

```python
import shutil
from datetime import datetime

def backup_checkpoints(agent_name: str):
    """Backup checkpoint database."""
    db_path = f"{AGENT_DATA}/{agent_name}/checkpoints.db"
    backup_path = f"{AGENT_DATA}/{agent_name}/backups/checkpoints_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    
    Path(backup_path).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(db_path, backup_path)
```

## Troubleshooting

### Checkpoint Not Found

```python
try:
    result = app.invoke(input_data, config=config)
except CheckpointNotFoundError:
    # Start fresh conversation
    result = app.invoke(input_data, config={
        "configurable": {"thread_id": f"new_{uuid.uuid4()}"}
    })
```

### Checkpoint Corruption

```python
def validate_checkpoint(checkpoint_id: str) -> bool:
    """Validate checkpoint integrity."""
    try:
        state = checkpointer.get(checkpoint_id)
        # Validate state structure
        assert "messages" in state
        assert isinstance(state["messages"], list)
        return True
    except Exception as e:
        logger.error(f"Checkpoint {checkpoint_id} corrupted: {e}")
        return False
```

### Performance Issues

```python
# Index thread_id for faster lookups
checkpointer.conn.execute(
    "CREATE INDEX IF NOT EXISTS idx_thread_id ON checkpoints(thread_id)"
)

# Vacuum database periodically
checkpointer.conn.execute("VACUUM")
```
