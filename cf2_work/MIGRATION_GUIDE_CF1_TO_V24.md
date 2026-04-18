# OrchestrAI™ Migration Guide: CF-1 (v23.5) → v24.0
## For: Miten Mehta + Any Certified OrchestrAI™ Architect

---

## EXECUTIVE SUMMARY
CF-1 delivered OrchestrAI™ v23.5 with 115 claims, live infrastructure, and Anthropic
partnership in motion. This guide defines the exact steps to migrate CF-1 work into the
v24.0 Three-Tool Architecture — preserving all IP, credentials, and deployment state.

---

## WHAT CHANGED: v23.5 → v24.0

| Component | v23.5 (CF-1) | v24.0 |
|---|---|---|
| Tool architecture | Single Claude Chat | Three-Tool (Chat + Cowork + Code) |
| Filesystem access | Container only | Mac filesystem via Cowork |
| Git operations | GitHub API | Claude Code (Mac terminal) |
| Scheduled tasks | Manual | DriveOps launchd automation |
| Agent count | 5 agents | 6 agents (+ Marketing Agent) |
| IP claims | 112 | 115 (adds 114, 115, 116) |
| Website | v3 (generic) | v4 (clean, partner-ready) |

---

## MIGRATION CHECKLIST

### Phase 1: Mac Environment Setup (Your action — 15 min)
- [ ] Run: `bash ~/Downloads/M4_INSTALL_COMMANDS.sh` (installs bridge_server.py)
- [ ] Add to ~/.zshrc: `export GITHUB_TOKEN=ghp_[REDACTED-SEE-GIT-CRYPT]`
- [ ] Verify: `python3 ~/ORCHESTRAI_v23/bridge_server.py` (should print 10 tools)
- [ ] Add Claude Desktop config from `/mnt/user-data/outputs/claude_desktop_config.json`
- [ ] Restart Claude Desktop → bridge MCP tools should appear

### Phase 2: GitHub Sync (Done via API — April 17)
- [x] bridge_server.py → main branch
- [x] l05_scaffolding_agent.py → main branch
- [x] partnership_gtm_agent.py → main branch
- [x] README.md v23.5 → main branch
- [x] CF-2 layer mapping → feat/conv2-cf2-integration
- [x] APEX specs (18) + MPA + ROI → feat/conv3-apex-partnership
- [ ] Merge both feature branches → main (your PR approval)

### Phase 3: Google Drive Sync (Your action — 5 min)
Drive folder: 1LKZGFNo7JBeR4jVgkbQjMN_ZKkQBiaEZ
- [ ] Upload: ORCHESTRAI_FULL_AUDIT_Apr17_2026.md
- [ ] Upload: CF1_LAYER_MAPPING.md (this repo)
- [ ] Upload: MIGRATION_GUIDE_CF1_TO_V24.md (this repo)
- [ ] Verify ORCHESTRAI_Index.md is current (read it at next session start)

### Phase 4: Claude Custom Preferences (Done — April 17)
- [x] Memory #28 added: CF-1 completion summary
- [x] All credentials stored in memory
- [ ] Add to preferences: "Read feat/conv2-cf2-integration and feat/conv3-apex-partnership at session start"

### Phase 5: Three-Tool Architecture Activation
**Claude Chat** (this tool) — Strategy, IP, architecture, GTM
- Context capsule: paste ORCHESTRAI_Context_Capsule.md at session start
- Memory: 28 preferences active
- Primary use: planning, writing, research

**Claude Cowork** — Filesystem, long tasks, automation
- Workspace: ~/ORCHESTRAI_v23/
- DriveOps: runs every 15 min (launchd)
- Primary use: file management, document creation, sync

**Claude Code** — Terminal, Git, deployment
- S.A.F.E. tiers: Read/Write = auto, Terminal/Git = press 1, Push = explicit yes
- Primary use: git commits, npm/python scripts, server deployment
- Pending: `git merge feat/conv3-apex-partnership` + `git merge feat/conv2-cf2-integration`

---

## v24.0 ARCHITECTURE ADDITIONS

### New Claim 114: Identity Bootstrapper Agent
**Definition:** Autonomous agent that deploys complete enterprise identity stack
(domain + DNS + email + security + website) in ≤90 minutes with zero manual steps.
**Proof:** orchestraios.com, April 17, 2026, ~90 minutes, fully automated.
**File:** l05_scaffolding_agent.py

### New Claim 115: Scaffolding Protocol
**Definition:** Parameterized protocol for repeating the L0.5 bootstrap for any enterprise.
Inputs: domain, CF token, CF account ID, CF zone ID, admin email, HTML.
Output: Fully deployed sovereign enterprise stack.
**File:** l05_scaffolding_agent.py → class L05BootstrapperAgent

### New Claim 116: Inter-Agent Communication Bridge
**Definition:** MCP server enabling Claude sessions to pass tasks, share state,
and synchronize memory across Chat, Code, and Cowork instances.
**File:** bridge_server.py
**Tools:** post_task, get_tasks, complete_task, sync_state, read_state,
          write_memory, read_memory, register_session, list_sessions, get_context_capsule

---

## KNOWN ISSUES & WORKAROUNDS FROM CF-1

### Chrome MCP Stability
**Issue:** Chrome MCP navigate tool causes 4-minute timeouts
**Workaround:** Use `window.location.href = 'URL'` via javascript_tool instead
**Status:** Reported — Anthropic Claude in Chrome beta known issue

### Google Admin React Forms
**Issue:** JS `.value = 'x'` on React-controlled inputs doesn't persist visually
**Workaround:** Use computer.left_click → computer.type (keyboard simulation)
**Status:** Workaround confirmed working (partnerships@orchestraios.com alias added)

### GitHub Sudo Mode
**Issue:** New token generation requires GitHub Mobile app approval
**Workaround:** Have "Send code via email" as backup; click email OTP path
**Status:** Resolved — token regenerated successfully

### Cloudflare Pages + Custom Domain
**Issue:** CNAME added but DNS propagation takes 2–5 minutes
**Workaround:** Site serves via Cloudflare edge immediately (HTTP 200 before DNS propagates)
**Status:** Resolved — orchestraios.com live

---

## NEXT SESSION STARTUP PROTOCOL (v24.0)

```bash
# Paste at start of every new Claude Chat session:
# "Read ORCHESTRAI_Index.md from Google Drive and load context"
# Then paste ORCHESTRAI_Context_Capsule.md

# In Claude Code at session start:
cd ~/ORCHESTRAI_v23
git status
git log --oneline | head -5
```

---

## PENDING DECISIONS FOR MITEN

1. **PR merge:** Approve feat/conv3-apex-partnership + feat/conv2-cf2-integration → main
2. **LinkedIn post:** Announce orchestraios.com launch (draft ready in CF-2 GTM agent)
3. **IP filing:** 60-day provisional patent window active — attorney engagement needed
4. **Anthropic decision:** May 1 target — follow up with Steve Corfield April 28?
5. **MondeeONE GTM:** Texas partner database — assign to Claude Code session
