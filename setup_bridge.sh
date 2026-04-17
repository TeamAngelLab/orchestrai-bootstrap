#!/bin/bash
GREEN='\033[0;32m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'
echo -e "${BOLD}OrchestrAI™ Inter-Agent Bridge Setup${NC}"

pip install fastmcp --break-system-packages -q

mkdir -p ~/ORCHESTRAI_v23
cp "$(dirname "$0")/bridge_server.py" ~/ORCHESTRAI_v23/bridge_server.py

# Add to Claude Desktop config
CONFIG_PATH="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
if [ -f "$CONFIG_PATH" ]; then
    echo -e "${CYAN}Found Claude Desktop config. Add this to mcpServers:${NC}"
else
    mkdir -p "$(dirname "$CONFIG_PATH")"
    cat > "$CONFIG_PATH" << EOF
{
  "mcpServers": {
    "orchestrai-bridge": {
      "command": "python3",
      "args": ["$HOME/ORCHESTRAI_v23/bridge_server.py"],
      "description": "OrchestrAI Inter-Agent Communication Bridge"
    }
  }
}
EOF
    echo -e "${GREEN}✓ Claude Desktop config created${NC}"
fi

echo -e "${GREEN}✓ Bridge installed at ~/ORCHESTRAI_v23/bridge_server.py${NC}"
echo -e "${BOLD}Restart Claude Desktop/Code to activate the bridge.${NC}"
