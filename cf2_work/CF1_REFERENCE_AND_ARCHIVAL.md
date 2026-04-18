# OrchestrAI™ CF-1 Reference & Archival Guide
## Session: April 17, 2026 | Permanent Record

---

## PURPOSE
This document is the permanent archival record of the CF-1 session.
It serves as the canonical reference for all future Claude sessions,
partner discussions, IP filings, and board presentations.

---

## SECTION 1: WHAT IS CF-1?

CF-1 (Claude Chat Instance 1) is the primary strategy and execution session
for OrchestrAI™ v23.5. It operates as the Manager agent in the 5-agent swarm,
routing tasks to Research, GTM, Architect, Writer, and Coder agents.

**Session date:** April 17, 2026
**Duration:** ~8 hours
**Outcome:** Complete OrchestrAI™ v23.5 stack deployed from zero

---

## SECTION 2: COMPLETE DELIVERABLE LOG

### Infrastructure (All Live)
| Deliverable | URL / Location | Status |
|---|---|---|
| orchestraios.com | https://orchestraios.com | HTTP 200 ✅ |
| miten@orchestraios.com | Google Workspace | LIVE ✅ |
| partnerships@orchestraios.com | Google Workspace alias | LIVE ✅ |
| Cloudflare DNS (8 records) | CF Zone 7763596e... | ACTIVE ✅ |
| DKIM 2048-bit | CF TXT record | VERIFIED ✅ |
| SPF | CF TXT record | ACTIVE ✅ |
| DMARC | CF TXT record | ACTIVE ✅ |

### GitHub Repository (All Pushed)
| File | Branch | Commit |
|---|---|---|
| README.md (v23.5) | main | 57abaeed |
| bridge_server.py (Claim 116) | main | pushed |
| BRIDGE_INSTALL.md | main | pushed |
| setup_bridge.sh | main | pushed |
| l05_scaffolding_agent.py | main | pushed |
| partnership_gtm_agent.py | main | pushed |
| orchestraios_website_v3.html | main | pushed |
| CF1_LAYER_MAPPING.md | feat/conv2-cf2-integration | this session |
| MIGRATION_GUIDE_CF1_TO_V24.md | feat/conv2-cf2-integration | this session |
| CF1_REFERENCE_AND_ARCHIVAL.md | feat/conv2-cf2-integration | this session |
| 18 APEX partnership specs | feat/conv3-apex-partnership | CONV-3 |
| MPA_TEMPLATE_v1.md | feat/conv3-apex-partnership | CONV-3 |
| ROI_CALCULATOR.md | feat/conv3-apex-partnership | CONV-3 |

### Partnership Actions
| Action | Target | Status |
|---|---|---|
| Claude Partner Network application | Anthropic portal | SUBMITTED ✅ |
| Direct email | steve@anthropic.com | SENT ✅ |
| Decision target | May 1, 2026 | PENDING |

### Website (v4 — Live)
| Section | Content | Status |
|---|---|---|
| Hero | "Control Plane for Claude" | LIVE ✅ |
| For Anthropic | Dedicated section | LIVE ✅ |
| 8 regulated verticals | All compliance chips | LIVE ✅ |
| Partner tiers (3) | Tier 1/2/3 defined | LIVE ✅ |
| Metrics row | 61+ agents, 115 claims, 90min | LIVE ✅ |
| ACE 9-step loop | Full visualization | LIVE ✅ |
| Social proof | Removed Mondee/BRAHM | CLEAN ✅ |

---

## SECTION 3: IP CLAIMS REGISTRY (CF-1 Session)

### Claims Active Before CF-1: 112
### Claims Added by CF-1: 3
### Total After CF-1: 115

| Claim # | Title | Proof | File |
|---|---|---|---|
| 114 | Identity Bootstrapper Agent | orchestraios.com (90 min) | l05_scaffolding_agent.py |
| 115 | Scaffolding Protocol | L05BootstrapperAgent class | l05_scaffolding_agent.py |
| 116 | Inter-Agent Bridge (A2A) | bridge_server.py (10 tools) | bridge_server.py |

### Patent Filing Status
- Provisional patent: 60-day window ACTIVE (started ~April 15)
- Deadline: ~June 14, 2026
- **Action required:** Engage patent attorney before June 1

---

## SECTION 4: LESSONS LEARNED (ExpeL Capture)

### Rule of Thumb 001: Chrome MCP Navigation
**Lesson:** Chrome MCP navigate tool causes 4-min timeouts on active sessions.
**Rule:** Always use `javascript_tool` with `window.location.href = 'URL'` for navigation.
**When applies:** Any Chrome automation requiring page navigation.

### Rule of Thumb 002: React Form Inputs
**Lesson:** JS `.value` assignment doesn't trigger React state updates visually.
**Rule:** For Google/React forms: left_click → computer.type (keyboard simulation only).
**When applies:** Any Google Admin, Google Cloud Console, GitHub form.

### Rule of Thumb 003: GitHub Token Generation
**Lesson:** New token creation requires GitHub sudo mode (Mobile app or email OTP).
**Rule:** Have both Mobile app and email OTP ready before starting token operations.
**When applies:** Any GitHub settings that require sudo mode.

### Rule of Thumb 004: Cloudflare Deploy
**Lesson:** `npx wrangler@3 pages deploy` works without local wrangler install.
**Rule:** Always use `npx wrangler@3` — no global install needed.
**When applies:** All Cloudflare Pages deployments from container.

### Rule of Thumb 005: Chrome MCP Keep-Alive
**Lesson:** Chrome MCP times out after ~4 minutes of inactivity.
**Rule:** Inject keep-alive immediately: `if (!window._kai) { window._kai = setInterval(() => { void document.title; }, 20000); }`
**When applies:** Every new Chrome MCP session start.

### Rule of Thumb 006: GitHub API Rate Limiting
**Lesson:** Unauthenticated GitHub API calls rate-limited at ~60/hour from shared IPs.
**Rule:** Always use token auth header: `-H 'Authorization: token $TOKEN'`
**When applies:** All GitHub API calls from container.

### Rule of Thumb 007: Separate Entity References
**Lesson:** Never include third-party company names (Mondee, BRAHM) as proof points
without explicit written consent, even if you built the system for them.
**Rule:** Use generic industry descriptions ("Enterprise Travel Client") until formal consent.
**When applies:** All website content, partner materials, press.

---

## SECTION 5: ARCHITECTURE STATE SNAPSHOT

```
OrchestrAI™ v23.5 — April 17, 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LIVE INFRASTRUCTURE
├── orchestraios.com (Cloudflare Pages + DNS)
├── miten@orchestraios.com (Google Workspace)
├── partnerships@orchestraios.com (alias)
└── github.com/TeamAngelLab/orchestrai-bootstrap

AGENTS (5 Active + Manager)
├── Manager: Claude Chat (CF-1)
├── Research: Perplexity + Claude
├── GTM: partnership_gtm_agent.py (7 tools)
├── Architect: Claude Code + IP claims
├── Writer: Claude Chat (board docs, LinkedIn)
└── Coder: Claude Code + GitHub API

CLAIMS: 115 (112 base + 114 + 115 + 116)
LAYERS: 23 + L0.5
VERSION: v23.5.0

PARTNERSHIPS
├── Anthropic: PENDING (May 1)
├── APEX pipeline: 18 specs, ~$25M identified
└── MPA template: ready for execution

PENDING (Miten's actions)
├── PR merge: feat/conv2 + feat/conv3 → main
├── Bridge install: M4_INSTALL_COMMANDS.sh on Mac
├── LinkedIn launch post
├── IP provisional patent filing
└── MondeeONE GTM Texas database
```

---

## SECTION 6: QUICK REFERENCE COMMANDS

```bash
# Check orchestraios.com status
curl -s -o /dev/null -w "%{http_code}" https://orchestraios.com

# Deploy website update
CLOUDFLARE_API_TOKEN=cfut_[REDACTED-SEE-GIT-CRYPT] \
CLOUDFLARE_ACCOUNT_ID=[CF-ACCOUNT-ID-REDACTED] \
npx wrangler@3 pages deploy ./site_dir --project-name=orchestraios --branch=main

# Push file to GitHub main
python3 push_to_github.py --token $GITHUB_TOKEN --file myfile.md --path myfile.md

# Start bridge server
python3 ~/ORCHESTRAI_v23/bridge_server.py

# Check DNS propagation
curl -s "https://dns.google/resolve?name=orchestraios.com&type=CNAME"
```

---
*CF-1 Archival Record — OrchestrAI™ v23.5 — April 17, 2026*
*Maintained by: CF-2 Integration Agent*
*Next review: Friday April 24, 2026 (Weekly ACE Ritual)*
