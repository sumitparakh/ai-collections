#!/usr/bin/env bash
#
# AI Workflow Setup Script
# Initializes the agentic workflow for documentation maintenance
#

set -e  # Exit on error

echo "=== AI Workflow Setup ==="
echo

# Get repository root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ $? -ne 0 ]; then
    echo "❌ Error: Not a git repository"
    echo "   Run this script from within a git repository"
    exit 1
fi

echo "Repository: $REPO_ROOT"
echo

# Check for git user.email
USER_EMAIL=$(git config user.email 2>/dev/null)
if [ -z "$USER_EMAIL" ]; then
    echo "⚠️  Warning: Git user.email not configured"
    echo "   Memory preservation will be disabled"
    echo
    read -p "   Configure now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "   Enter your email: " EMAIL
        git config user.email "$EMAIL"
        echo "   ✓ Email configured"
    else
        echo "   You can configure later with: git config user.email \"your@email.com\""
    fi
    echo
fi

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed"
    echo "   Install Python 3.8+ to continue"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION found"
echo

# Check/Install Python dependencies
echo "Checking Python dependencies..."
REQUIRED_PACKAGES=("gitpython" "pyyaml")
MISSING_PACKAGES=()

for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! python3 -c "import ${package//-/_}" 2>/dev/null; then
        MISSING_PACKAGES+=("$package")
    fi
done

if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    echo "⚠️  Missing packages: ${MISSING_PACKAGES[*]}"
    read -p "   Install now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "   Installing packages..."
        pip3 install "${MISSING_PACKAGES[@]}"
        echo "   ✓ Packages installed"
    else
        echo "   Please install manually: pip3 install ${MISSING_PACKAGES[*]}"
        exit 1
    fi
else
    echo "✓ All dependencies installed"
fi
echo

# Create local configuration if it doesn't exist
WORKFLOW_DIR="$REPO_ROOT/.ai-workflow"
CONFIG_DIR="$WORKFLOW_DIR/config"
LOCAL_CONFIG="$CONFIG_DIR/workflow.local.yaml"

if [ ! -f "$LOCAL_CONFIG" ]; then
    echo "Creating local configuration..."
    cp "$CONFIG_DIR/workflow.local.yaml.example" "$LOCAL_CONFIG"
    echo "✓ Created $LOCAL_CONFIG"
    echo "  (You can customize settings here)"
else
    echo "✓ Local configuration exists"
fi
echo

# Install git hook
HOOK_SOURCE="$WORKFLOW_DIR/hooks/post-commit"
HOOK_DEST="$REPO_ROOT/.git/hooks/post-commit"

if [ -f "$HOOK_DEST" ]; then
    echo "⚠️  Post-commit hook already exists"
    read -p "   Overwrite? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp "$HOOK_SOURCE" "$HOOK_DEST"
        chmod +x "$HOOK_DEST"
        echo "✓ Hook installed (overwritten)"
    else
        echo "  Keeping existing hook"
    fi
else
    cp "$HOOK_SOURCE" "$HOOK_DEST"
    chmod +x "$HOOK_DEST"
    echo "✓ Post-commit hook installed"
fi
echo

# Initialize state directory and baseline
STATE_DIR="$WORKFLOW_DIR/state"
mkdir -p "$STATE_DIR"

# Mark current commit as baseline
CURRENT_COMMIT=$(git rev-parse HEAD)
echo "$CURRENT_COMMIT" > "$STATE_DIR/last_processed_commit.txt"
echo "✓ Baseline established at commit: ${CURRENT_COMMIT:0:8}"
echo

# Generate initial context files
echo "Generating initial context files..."
export REPO_PATH="$REPO_ROOT"
python3 "$WORKFLOW_DIR/scripts/detect_changes.py"
python3 "$WORKFLOW_DIR/scripts/generate_context.py"
echo

# Create empty memory index
MEMORY_DIR="$WORKFLOW_DIR/memory"
mkdir -p "$MEMORY_DIR"
if [ ! -f "$MEMORY_DIR/index.md" ]; then
    echo "# Conversation Index" > "$MEMORY_DIR/index.md"
    echo "" >> "$MEMORY_DIR/index.md"
    echo "✓ Memory index initialized"
fi
echo

# Display summary
echo "========================================="
echo "✅ AI Workflow Setup Complete!"
echo "========================================="
echo
echo "Next steps:"
echo
echo "1. Review configuration:"
echo "   nano $LOCAL_CONFIG"
echo
echo "2. Make some changes and commit:"
echo "   git add <files>"
echo "   git commit -m \"Your changes\""
echo "   (Post-commit hook will run automatically)"
echo
echo "3. Use Copilot Chat commands:"
echo "   #file:.github/prompts/menu.md         - Show available commands"
echo "   #file:.github/prompts/check-status.md - Check doc status"
echo "   #file:.github/prompts/update-docs.md  - Get update suggestions"
echo
echo "4. Save important conversations:"
echo "   python .ai-workflow/scripts/capture_session.py"
echo
echo "Documentation: .ai-workflow/README.md"
echo
