#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# Gmail Reports Claude Code Skill Uninstaller
# ============================================================

CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
AGENTS_DIR="${CLAUDE_DIR}/agents"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${YELLOW}Gmail Reports — Claude Code Skill Uninstaller${NC}"
echo ""
echo "This will remove the following:"
echo ""

# List what will be removed
[ -d "$SKILLS_DIR/gmail" ] && echo "  → ${SKILLS_DIR}/gmail/"
for skill_dir in "$SKILLS_DIR"/gmail-*/; do
    [ -d "$skill_dir" ] && echo "  → ${skill_dir}"
done
for agent_file in "$AGENTS_DIR"/gmail-*.md; do
    [ -f "$agent_file" ] && echo "  → ${agent_file}"
done

echo ""
read -p "Are you sure you want to uninstall? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstall cancelled."
    exit 0
fi

echo ""

# Remove main skill
if [ -d "$SKILLS_DIR/gmail" ]; then
    rm -rf "$SKILLS_DIR/gmail"
    echo -e "${GREEN}✓ Removed main skill${NC}"
fi

# Remove sub-skills
for skill_dir in "$SKILLS_DIR"/gmail-*/; do
    if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")
        rm -rf "$skill_dir"
        echo -e "${GREEN}✓ Removed ${skill_name}${NC}"
    fi
done

# Remove agents
for agent_file in "$AGENTS_DIR"/gmail-*.md; do
    if [ -f "$agent_file" ]; then
        agent_name=$(basename "$agent_file")
        rm -f "$agent_file"
        echo -e "${GREEN}✓ Removed ${agent_name}${NC}"
    fi
done

echo ""
echo -e "${GREEN}Gmail Reports skill has been uninstalled.${NC}"
echo ""
echo "Note: Python dependencies were not removed."
echo "To remove them manually:"
echo "  pip uninstall google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2 pandas matplotlib reportlab python-dateutil"
echo ""
echo -e "${YELLOW}Reminder:${NC} If you have OAuth credentials (credentials.json, token.json)"
echo "in your working directories, consider removing or revoking them at:"
echo "  https://myaccount.google.com/permissions"
echo ""
