#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# Gmail Reports Claude Code Skill Installer
# Installs the Gmail reporting skill suite for Claude Code
# ============================================================

REPO_URL="https://github.com/yourname/gmail-report-claude.git"
CLAUDE_DIR="${HOME}/.claude"
SKILLS_DIR="${CLAUDE_DIR}/skills"
AGENTS_DIR="${CLAUDE_DIR}/agents"
INSTALL_DIR="${SKILLS_DIR}/gmail"
TEMP_DIR=$(mktemp -d)

# Detect if running via curl pipe (no interactive input available)
INTERACTIVE=true
if [ ! -t 0 ]; then
    INTERACTIVE=false
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   Gmail Reports — Claude Code Skill Installer  ║${NC}"
    echo -e "${BLUE}║   Inbox reporting powered by Gmail API          ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}→ $1${NC}"
}

cleanup() {
    rm -rf "$TEMP_DIR"
}

trap cleanup EXIT

main() {
    print_header

    # ---- Check Prerequisites ----
    print_info "Checking prerequisites..."

    # Check for Git
    if ! command -v git &> /dev/null; then
        print_error "Git is required but not installed."
        echo "  Install: https://git-scm.com/downloads"
        exit 1
    fi
    print_success "Git found: $(git --version)"

    # Check for Python 3
    PYTHON_CMD=""
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
        if [ -n "$PYTHON_VERSION" ]; then
            MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
            MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
            if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 8 ]; then
                PYTHON_CMD="python"
            fi
        fi
    fi

    if [ -z "$PYTHON_CMD" ]; then
        print_error "Python 3.8+ is required but not found."
        echo "  Install: https://www.python.org/downloads/"
        exit 1
    fi
    print_success "Python found: $($PYTHON_CMD --version)"

    # Check for Claude Code
    if ! command -v claude &> /dev/null; then
        print_warning "Claude Code CLI not found in PATH."
        echo "  This tool requires Claude Code to function."
        echo "  Install: npm install -g @anthropic-ai/claude-code"
        echo ""
        if [ "$INTERACTIVE" = true ]; then
            read -p "Continue installation anyway? (y/n): " -n 1 -r
            echo ""
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        else
            print_info "Non-interactive mode — continuing anyway..."
        fi
    else
        print_success "Claude Code CLI found"
    fi

    # ---- Create Directories ----
    print_info "Creating directories..."

    mkdir -p "$SKILLS_DIR"
    mkdir -p "$AGENTS_DIR"
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$INSTALL_DIR/scripts"
    mkdir -p "$INSTALL_DIR/templates"

    print_success "Directory structure created"

    # ---- Clone or Copy Repository ----
    print_info "Fetching Gmail Reports skill files..."

    # Check if running from the repo directory (local install)
    # BASH_SOURCE may be empty when piped via curl, so handle gracefully
    SCRIPT_DIR=""
    if [ -n "${BASH_SOURCE[0]:-}" ] && [ "${BASH_SOURCE[0]}" != "bash" ]; then
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)" || true
    fi

    if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/gmail/SKILL.md" ]; then
        print_info "Installing from local directory..."
        SOURCE_DIR="$SCRIPT_DIR"
    else
        print_info "Cloning from repository..."
        git clone --depth 1 "$REPO_URL" "$TEMP_DIR/repo" || {
            print_error "Failed to clone repository. Check your internet connection."
            exit 1
        }
        SOURCE_DIR="${TEMP_DIR}/repo"
    fi

    # ---- Install Main Skill ----
    print_info "Installing main Gmail skill..."

    cp -r "$SOURCE_DIR/gmail/"* "$INSTALL_DIR/"
    print_success "Main skill installed → ${INSTALL_DIR}/"

    # ---- Install Sub-Skills ----
    print_info "Installing sub-skills..."

    SKILL_COUNT=0
    for skill_dir in "$SOURCE_DIR/skills"/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            target_dir="${SKILLS_DIR}/${skill_name}"
            mkdir -p "$target_dir"
            cp -r "$skill_dir"* "$target_dir/"
            SKILL_COUNT=$((SKILL_COUNT + 1))
            print_success "  ${skill_name}"
        fi
    done
    echo "  → ${SKILL_COUNT} sub-skills installed"

    # ---- Install Agents ----
    print_info "Installing subagents..."

    AGENT_COUNT=0
    for agent_file in "$SOURCE_DIR/agents/"*.md; do
        if [ -f "$agent_file" ]; then
            cp "$agent_file" "$AGENTS_DIR/"
            AGENT_COUNT=$((AGENT_COUNT + 1))
            print_success "  $(basename "$agent_file")"
        fi
    done
    echo "  → ${AGENT_COUNT} subagents installed"

    # ---- Install Scripts ----
    print_info "Installing utility scripts..."

    if [ -d "$SOURCE_DIR/scripts" ]; then
        cp -r "$SOURCE_DIR/scripts/"* "$INSTALL_DIR/scripts/"
        chmod +x "$INSTALL_DIR/scripts/"*.py 2>/dev/null || true
        print_success "Scripts installed → ${INSTALL_DIR}/scripts/"
    fi

    # ---- Install Report Templates ----
    print_info "Installing report templates..."

    if [ -d "$SOURCE_DIR/templates" ]; then
        cp -r "$SOURCE_DIR/templates/"* "$INSTALL_DIR/templates/"
        print_success "Report templates installed → ${INSTALL_DIR}/templates/"
    fi

    # ---- Install Python Dependencies ----
    print_info "Installing Python dependencies..."

    if [ -f "$SOURCE_DIR/requirements.txt" ]; then
        $PYTHON_CMD -m pip install -r "$SOURCE_DIR/requirements.txt" --quiet 2>/dev/null && {
            print_success "Python dependencies installed"
        } || {
            print_warning "Some Python dependencies failed to install."
            echo "  Run manually: $PYTHON_CMD -m pip install -r requirements.txt"
            cp "$SOURCE_DIR/requirements.txt" "$INSTALL_DIR/"
        }
    fi

    # ---- Gmail API Setup Hint ----
    echo ""
    print_info "Gmail API setup..."
    echo "  To use Gmail API features, you need OAuth credentials."
    echo "  1. Go to https://console.cloud.google.com/"
    echo "  2. Create a project and enable the Gmail API"
    echo "  3. Create OAuth 2.0 credentials (Desktop application)"
    echo "  4. Download credentials.json to your working directory"
    echo ""
    echo "  The skill will guide you through OAuth authentication"
    echo "  on first use. Only read-only scopes are requested."

    # ---- Verify Installation ----
    echo ""
    print_info "Verifying installation..."

    VERIFY_OK=true

    [ -f "$INSTALL_DIR/SKILL.md" ] && print_success "Main skill file" || { print_error "Main skill file missing"; VERIFY_OK=false; }
    [ -d "$SKILLS_DIR/gmail-report" ] && print_success "gmail-report sub-skill" || { print_error "gmail-report sub-skill missing"; VERIFY_OK=false; }
    [ -d "$SKILLS_DIR/gmail-summary" ] && print_success "gmail-summary sub-skill" || { print_error "gmail-summary sub-skill missing"; VERIFY_OK=false; }
    [ "$(ls "$AGENTS_DIR"/gmail-*.md 2>/dev/null | wc -l)" -gt 0 ] && print_success "Agent files" || { print_error "Agent files missing"; VERIFY_OK=false; }
    [ -d "$INSTALL_DIR/scripts" ] && print_success "Utility scripts" || { print_error "Scripts missing"; VERIFY_OK=false; }
    [ -d "$INSTALL_DIR/templates" ] && print_success "Report templates" || { print_error "Report templates missing"; VERIFY_OK=false; }

    # ---- Print Summary ----
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║         Installation Complete!                  ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════╝${NC}"
    echo ""
    echo "  Installed to: ${INSTALL_DIR}"
    echo "  Skills:       ${SKILL_COUNT} sub-skills"
    echo "  Agents:       ${AGENT_COUNT} subagents"
    echo ""
    echo -e "${BLUE}Quick Start:${NC}"
    echo "  Open Claude Code and try:"
    echo ""
    echo "    /gmail report today"
    echo "    /gmail summary week"
    echo "    /gmail unread today"
    echo "    /gmail senders month"
    echo "    /gmail trends year"
    echo ""
    echo -e "${BLUE}Available Commands:${NC}"
    echo "    /gmail report <period>          Full inbox report (today/week/month/year)"
    echo "    /gmail summary <period>         Quick snapshot of volume and top senders"
    echo "    /gmail unread <period>          Unread-only email report"
    echo "    /gmail spam <period>            Spam volume and trends"
    echo "    /gmail senders <period>         Top senders ranking"
    echo "    /gmail labels <period>          Label distribution analysis"
    echo "    /gmail categories <period>      Primary/Promotions/Social breakdown"
    echo "    /gmail attachments <period>     Attachment volume analysis"
    echo "    /gmail response-time <period>   Reply speed and follow-up behavior"
    echo "    /gmail trends <period>          Activity trends over time"
    echo "    /gmail custom --from --to       Custom date range with filters"
    echo "    /gmail report-pdf               Generate PDF report with charts"
    echo ""
    echo -e "${BLUE}Common Filters:${NC}"
    echo "    --include-spam    Include spam in analysis"
    echo "    --unread-only     Only unread messages"
    echo "    --label \"Work\"    Filter by Gmail label"
    echo "    --sender <email>  Filter by sender"
    echo "    --has-attachments  Only messages with attachments"
    echo ""
    echo "  Documentation: https://github.com/yourname/gmail-report-claude"
    echo ""
}

main "$@"
