# ORCHESTRAI Bootstrap Agent

One command to install your complete sovereign local AI stack.
No cloud. No API costs. No technical knowledge required.

## Quick Install

curl -fsSL https://raw.githubusercontent.com/mitenmehta/orchestrai-bootstrap/main/install.sh | sh

## What This Does

- Detects your hardware automatically
- Asks 3 questions: role, industry, use case
- Selects optimal AI models for your setup
- Downloads everything locally, zero data leaves your machine
- Creates your ORCHESTRAI workspace
- Runs a self-test and health report

## Requirements

- RAM: 8GB minimum, 16GB recommended
- Storage: 15GB free
- OS: macOS 12 or Ubuntu 20.04 or later
- Chip: Intel or Apple Silicon

## Models Installed

- phi4 (9GB) fast lightweight tasks, 8GB RAM minimum
- llama3.1 (4.9GB) general reasoning, 16GB RAM minimum
- qwen2.5-coder (4.7GB) code generation, 16GB RAM minimum

## After Installation

1. Test models: bash ~/ORCHESTRAI_v23/tasks/ollama_test.sh
2. Upload ~/ORCHESTRAI_v23/capsules/ to Google Drive
3. Paste Context Capsule into Claude at each session start
4. Set Friday reminder: ORCHESTRAI ACE Cycle 30 min

## Roadmap

- Phase 1 complete: Mac/Linux shell installer
- Phase 2: Python GUI + Windows + Google Drive scaffold
- Phase 3: Signed dmg Mac and exe Windows
- Phase 4: MCP server auto-configuration

## License

Apache 2.0

## Author

Built by Miten Mehta as part of ORCHESTRAI v23.0 Enterprise Agentic OS.

2026 ORCHESTRAI. Sovereign AI. FOSS Constitution. ACE Loop Active.
