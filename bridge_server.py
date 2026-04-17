#!/usr/bin/env python3
"""
OrchestrAI™ Inter-Agent Bridge — MCP Server
Claim 116: Inter-Agent Communication Protocol
Enables all Claude sessions to communicate, share state, and pass tasks.

Run: python bridge_server.py
All Claude sessions connect via MCP on port 8765
"""

import json
import time
import os
from pathlib import Path
from datetime import datetime

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Installing FastMCP...")
    os.system("pip install fastmcp --break-system-packages -q")
    from mcp.server.fastmcp import FastMCP

# State store — in production, back this with Redis or Drive
STORE_PATH = Path.home() / "ORCHESTRAI_v23" / "bridge"
STORE_PATH.mkdir(parents=True, exist_ok=True)

mcp = FastMCP("OrchestrAI-Bridge")

def _load(key: str) -> dict:
    f = STORE_PATH / f"{key}.json"
    if f.exists():
        return json.loads(f.read_text())
    return {}

def _save(key: str, data: dict):
    f = STORE_PATH / f"{key}.json"
    f.write_text(json.dumps(data, indent=2))

# ── TASK QUEUE ────────────────────────────────────────────────────────────────

@mcp.tool()
def post_task(from_session: str, to_session: str, task: str, priority: str = "normal", context: str = "") -> str:
    """Post a task from one Claude session to another.
    
    Args:
        from_session: Sender session ID (e.g. 'CF-1', 'CF-Code', 'CF-Cowork')
        to_session: Recipient session ID
        task: Task description
        priority: 'high', 'normal', or 'low'
        context: Optional context JSON string
    """
    queue = _load("task_queue")
    task_id = f"task_{int(time.time()*1000)}"
    queue[task_id] = {
        "id": task_id,
        "from": from_session,
        "to": to_session,
        "task": task,
        "priority": priority,
        "context": context,
        "status": "pending",
        "created": datetime.utcnow().isoformat(),
        "updated": datetime.utcnow().isoformat()
    }
    _save("task_queue", queue)
    return f"Task {task_id} posted to {to_session}"

@mcp.tool()
def get_tasks(session_id: str, status: str = "pending") -> str:
    """Get all tasks assigned to a session.
    
    Args:
        session_id: Session to get tasks for
        status: 'pending', 'in_progress', 'done', or 'all'
    """
    queue = _load("task_queue")
    my_tasks = [
        t for t in queue.values()
        if t["to"] == session_id and (status == "all" or t["status"] == status)
    ]
    my_tasks.sort(key=lambda t: {"high": 0, "normal": 1, "low": 2}[t["priority"]])
    return json.dumps(my_tasks, indent=2)

@mcp.tool()
def complete_task(task_id: str, session_id: str, result: str = "") -> str:
    """Mark a task as complete.
    
    Args:
        task_id: Task ID to complete
        session_id: Session completing the task
        result: Optional result summary
    """
    queue = _load("task_queue")
    if task_id not in queue:
        return f"Task {task_id} not found"
    queue[task_id]["status"] = "done"
    queue[task_id]["result"] = result
    queue[task_id]["completed_by"] = session_id
    queue[task_id]["updated"] = datetime.utcnow().isoformat()
    _save("task_queue", queue)
    return f"Task {task_id} marked complete"

# ── STATE SYNC ─────────────────────────────────────────────────────────────────

@mcp.tool()
def sync_state(session_id: str, state: str) -> str:
    """Broadcast this session's current state to all other sessions.
    
    Args:
        session_id: Your session ID
        state: JSON string of your current state
    """
    states = _load("session_states")
    states[session_id] = {
        "state": state,
        "updated": datetime.utcnow().isoformat()
    }
    _save("session_states", states)
    return f"State synced for {session_id}"

@mcp.tool()
def read_state(session_id: str = "all") -> str:
    """Read state from other sessions.
    
    Args:
        session_id: Specific session ID, or 'all' for all sessions
    """
    states = _load("session_states")
    if session_id == "all":
        return json.dumps(states, indent=2)
    return json.dumps(states.get(session_id, {}), indent=2)

# ── SHARED MEMORY ──────────────────────────────────────────────────────────────

@mcp.tool()
def write_memory(key: str, value: str, session_id: str = "unknown") -> str:
    """Write a shared memory entry accessible to all sessions.
    
    Args:
        key: Memory key (e.g. 'current_version', 'active_tasks')
        value: Value to store
        session_id: Session writing this memory
    """
    mem = _load("shared_memory")
    mem[key] = {
        "value": value,
        "written_by": session_id,
        "updated": datetime.utcnow().isoformat()
    }
    _save("shared_memory", mem)
    return f"Memory key '{key}' written"

@mcp.tool()
def read_memory(key: str = "all") -> str:
    """Read shared memory. Use key='all' to read everything.
    
    Args:
        key: Specific key or 'all'
    """
    mem = _load("shared_memory")
    if key == "all":
        return json.dumps({k: v["value"] for k, v in mem.items()}, indent=2)
    entry = mem.get(key, {})
    return entry.get("value", f"Key '{key}' not found")

# ── SESSION REGISTRY ───────────────────────────────────────────────────────────

@mcp.tool()
def register_session(session_id: str, role: str, description: str = "") -> str:
    """Register this Claude session in the agent network.
    
    Args:
        session_id: Unique ID for this session (e.g. 'CF-1', 'CF-Code')
        role: Role description (e.g. 'Infrastructure & GTM', 'Coding Agent')
        description: What this session is currently working on
    """
    registry = _load("session_registry")
    registry[session_id] = {
        "role": role,
        "description": description,
        "registered": datetime.utcnow().isoformat(),
        "last_seen": datetime.utcnow().isoformat(),
        "status": "active"
    }
    _save("session_registry", registry)
    return f"Session {session_id} registered as '{role}'"

@mcp.tool()
def list_sessions() -> str:
    """List all registered Claude sessions in the agent network."""
    registry = _load("session_registry")
    return json.dumps(registry, indent=2)

# ── BOOTSTRAP ─────────────────────────────────────────────────────────────────

@mcp.tool()
def get_context_capsule() -> str:
    """Get the full OrchestrAI context capsule for session initialization.
    Returns the canonical state all sessions need at startup.
    """
    capsule_path = Path.home() / "ORCHESTRAI_v23" / "capsules" / "ORCHESTRAI_Context_Capsule.md"
    if capsule_path.exists():
        return capsule_path.read_text()
    return "Context capsule not found at ~/ORCHESTRAI_v23/capsules/ORCHESTRAI_Context_Capsule.md"

if __name__ == "__main__":
    print("🔥 OrchestrAI™ Inter-Agent Bridge v1.0")
    print("   Claim 116: Inter-Agent Communication Protocol")
    print(f"   State store: {STORE_PATH}")
    print("   Tools: post_task, get_tasks, complete_task, sync_state,")
    print("          read_state, write_memory, read_memory,")
    print("          register_session, list_sessions, get_context_capsule")
    print()
    mcp.run(transport="stdio")
