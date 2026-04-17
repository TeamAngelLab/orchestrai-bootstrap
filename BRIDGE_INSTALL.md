# OrchestrAI™ Inter-Agent Bridge — Installation Guide
## Claim 116: Inter-Agent Communication Protocol

### What this does
Connects ALL Claude sessions (Chat, Code, Cowork) so they can:
- Post tasks to each other (`post_task`)
- Read each other's state (`read_state`, `sync_state`)  
- Share memory across sessions (`write_memory`, `read_memory`)
- Register in a live agent network (`register_session`, `list_sessions`)
- Bootstrap any new session with full context (`get_context_capsule`)

### Install (2 minutes)

```bash
# 1. Install FastMCP
pip install fastmcp --break-system-packages

# 2. Copy bridge server to ORCHESTRAI workspace
cp ~/Downloads/bridge_server.py ~/ORCHESTRAI_v23/bridge_server.py

# 3. Test it works
python ~/ORCHESTRAI_v23/bridge_server.py
# Should print: 🔥 OrchestrAI™ Inter-Agent Bridge v1.0

# 4. Add to Claude Code MCP config (~/.claude/claude_desktop_config.json)
```

### Claude Desktop / Claude Code MCP Config
Add this to `~/.claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "orchestrai-bridge": {
      "command": "python",
      "args": ["/Users/mitenmehta/ORCHESTRAI_v23/bridge_server.py"],
      "description": "OrchestrAI Inter-Agent Communication Bridge"
    }
  }
}
```

### How each session uses it

**At session START (paste in any Claude chat):**
```
Bridge init: register_session("CF-1", "Infrastructure & GTM", "Website deploy, Anthropic partner")
Check tasks: get_tasks("CF-1")
Read state: read_state("all")
```

**At session END:**
```
sync_state("CF-1", '{"completed": ["website deployed", "partner app submitted"], "pending": ["github README", "steve email"]}')
```

**To hand off work to CF-2:**
```
post_task("CF-1", "CF-2", "Update ORCHESTRAI_Index.md on Drive with v23.5 changes", priority="high")
post_task("CF-1", "CF-2", "Draft LinkedIn post announcing orchestraios.com launch", priority="normal")
```

### Session IDs Convention
| Session | ID | Role |
|---|---|---|
| Claude Chat (this) | CF-1 | Infrastructure, GTM, IP |
| Claude Chat 2 | CF-2 | Workflow, MondeeONE, Docs |
| Claude Code | CF-Code | Terminal, Git, Scripts |
| Claude Cowork | CF-Cowork | File management, Scheduled tasks |

### Current Task Queue (April 16, 2026)
CF-2 should pick up:
1. Update ORCHESTRAI_Index.md on Google Drive
2. MondeeONE GTM Texas partner database
3. LinkedIn post: OrchestrAI v23.0 launch announcement
4. tasks/todo.md + lessons.md update with today's lessons 6-10
