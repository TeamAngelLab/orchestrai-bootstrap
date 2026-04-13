#!/bin/bash
# ORCHESTRAI™ Bootstrap Agent v1.0
# https://github.com/TeamAngelLab/orchestrai-bootstrap
# Apache 2.0 License — © 2026 Miten Mehta / ORCHESTRAI™

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

clear
echo -e "${BLUE}${BOLD}"
echo "============================================================"
echo "         ORCHESTRAI™ Bootstrap Agent v1.0                  "
echo "   Sovereign Local AI Stack — No Cloud Required            "
echo "============================================================"
echo -e "${NC}"

OS="$(uname -s)"
ARCH="$(uname -m)"
if [[ "$OS" == "Darwin" ]]; then
    RAM_BYTES=$(sysctl -n hw.memsize 2>/dev/null || echo 8589934592)
    RAM_GB=$(( RAM_BYTES / 1024 / 1024 / 1024 ))
    CHIP=$(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo "Apple Silicon")
    PLATFORM="macOS"
elif [[ "$OS" == "Linux" ]]; then
    RAM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    RAM_GB=$(( RAM_KB / 1024 / 1024 ))
    CHIP="Linux CPU"
    PLATFORM="Linux"
else
    echo -e "${RED}Windows not yet supported. Use WSL2 or wait for Phase 2.${NC}"
    exit 1
fi

echo -e "${GREEN}Platform:  $PLATFORM ($ARCH)${NC}"
echo -e "${GREEN}Chip:      $CHIP${NC}"
echo -e "${GREEN}RAM:       ${RAM_GB}GB detected${NC}"
echo ""
echo "What is your primary role?"
echo "  1) Business Leader (CTO / CAIO / CEO / Board)"
echo "  2) GTM / Partnerships / Sales"
echo "  3) Developer / Engineer"
echo "  4) Researcher / Analyst"
echo "  5) Operations / Finance"
echo ""
read -p "Enter number (1-5): " ROLE_NUM
case $ROLE_NUM in
    1) ROLE="Business Leader" ;;
    2) ROLE="GTM and Partnerships" ;;
    3) ROLE="Developer" ;;
    4) ROLE="Researcher" ;;
    5) ROLE="Operations" ;;
    *) ROLE="Business Leader" ;;
esac
echo -e "${GREEN}Role: $ROLE${NC}"
echo ""

echo "What is your primary industry?"
echo "  1) Financial Services"
echo "  2) Healthcare"
echo "  3) Real Estate"
echo "  4) Education"
echo "  5) Technology"
echo "  6) Other"
echo ""
read -p "Enter number (1-6): " INDUSTRY_NUM
case $INDUSTRY_NUM in
    1) INDUSTRY="Financial Services" ;;
    2) INDUSTRY="Healthcare" ;;
    3) INDUSTRY="Real Estate" ;;
    4) INDUSTRY="Education" ;;
    5) INDUSTRY="Technology" ;;
    *) INDUSTRY="Enterprise" ;;
esac
echo -e "${GREEN}Industry: $INDUSTRY${NC}"
echo ""
MODELS=()
MODEL_REASONS=()
MODELS+=("phi4")
MODEL_REASONS+=("Fast lightweight tasks (9GB)")
if [ "$RAM_GB" -ge 16 ]; then
    MODELS+=("llama3.1")
    MODEL_REASONS+=("General reasoning (4.9GB)")
fi
if [ "$RAM_GB" -ge 16 ] && [[ "$ROLE" == "Developer" ]]; then
    MODELS+=("qwen2.5-coder")
    MODEL_REASONS+=("Code generation (4.7GB)")
fi

echo "Based on your profile, installing:"
for i in "${!MODELS[@]}"; do
    echo -e "  ${GREEN}${MODELS[$i]}${NC} — ${MODEL_REASONS[$i]}"
done
echo ""
read -p "Proceed? (y/n): " CONFIRM
if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
    echo "Installation cancelled."
    exit 0
fi

if command -v ollama &> /dev/null; then
    echo -e "${GREEN}Ollama already installed${NC}"
else
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

for i in "${!MODELS[@]}"; do
    echo -e "${CYAN}Downloading ${MODELS[$i]}...${NC}"
    ollama pull "${MODELS[$i]}"
    echo -e "${GREEN}${MODELS[$i]} ready${NC}"
done
mkdir -p ~/ORCHESTRAI_v23/tasks ~/ORCHESTRAI_v23/agents ~/ORCHESTRAI_v23/manifests ~/ORCHESTRAI_v23/capsules ~/ORCHESTRAI_v23/audit_logs ~/ORCHESTRAI_v23/knowledge

echo "# ORCHESTRAI Context Capsule" > ~/ORCHESTRAI_v23/capsules/ORCHESTRAI_Context_Capsule.md
echo "Role: $ROLE | Industry: $INDUSTRY | Platform: $PLATFORM ${RAM_GB}GB" >> ~/ORCHESTRAI_v23/capsules/ORCHESTRAI_Context_Capsule.md
echo "Models: $(IFS=', '; echo "${MODELS[*]}")" >> ~/ORCHESTRAI_v23/capsules/ORCHESTRAI_Context_Capsule.md
echo "Generated: $(date)" >> ~/ORCHESTRAI_v23/capsules/ORCHESTRAI_Context_Capsule.md

echo "# ExpeL Lessons Database" > ~/ORCHESTRAI_v23/tasks/lessons.md
echo "Started: $(date)" >> ~/ORCHESTRAI_v23/tasks/lessons.md
echo "Lesson 001: Use phi4 for fast tasks, llama3.1 for reasoning" >> ~/ORCHESTRAI_v23/tasks/lessons.md

PASS=0; FAIL=0
command -v ollama &>/dev/null && PASS=$((PASS+1)) || FAIL=$((FAIL+1))
for m in "${MODELS[@]}"; do
    ollama list 2>/dev/null | grep -q "$m" && PASS=$((PASS+1)) || FAIL=$((FAIL+1))
done
[ -d ~/ORCHESTRAI_v23 ] && PASS=$((PASS+1)) || FAIL=$((FAIL+1))

echo ""
echo "============================================================"
echo "         ORCHESTRAI™ HEALTH REPORT                         "
echo "============================================================"
echo "Profile:  $ROLE | $INDUSTRY | $PLATFORM ${RAM_GB}GB"
echo "Models:   $(IFS=', '; echo "${MODELS[*]}")"
echo "Tests:    $PASS passed, $FAIL failed"
echo "Workspace: ~/ORCHESTRAI_v23/"
echo ""
echo "NEXT STEPS:"
echo "1. bash ~/ORCHESTRAI_v23/tasks/ollama_test.sh"
echo "2. Upload ~/ORCHESTRAI_v23/capsules/ to Google Drive"
echo "3. Paste Context Capsule into Claude at each session start"
echo "4. Set Friday reminder: ORCHESTRAI ACE Cycle 30 min"
echo "============================================================"
echo "ORCHESTRAI™ v23.0 — Sovereign AI Stack Active."
