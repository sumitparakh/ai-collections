#!/usr/bin/env python3
"""
Capture Copilot Chat Session
Interactive script to save conversation summaries.
Can be executed from Copilot Chat with user approval.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from memory.manager import MemoryManager
except ImportError:
    print("Error: Could not import MemoryManager")
    sys.exit(1)


def capture_session():
    """Interactively capture a conversation session."""
    print("=== Copilot Chat Session Capture ===\n")
    
    # Get repository path
    repo_path = os.getenv("REPO_PATH", os.getcwd())
    
    # Initialize manager
    manager = MemoryManager(repo_path)
    
    # Check if memory is enabled
    if not manager.config.get("memory", {}).get("enabled", True):
        print("❌ Memory preservation is disabled in configuration.")
        print("Enable it in .ai-workflow/config/workflow.local.yaml")
        return
    
    # Check for git user
    if not manager._get_user_hash():
        print("❌ Git user.email not configured.")
        print("Run: git config user.email \"your@email.com\"")
        return
    
    print("Enter conversation summary (one line):")
    summary = input("> ").strip()
    
    if not summary:
        print("❌ Summary cannot be empty")
        return
    
    print("\nEnter conversation content (paste full chat, then press Ctrl+D on new line):")
    print("(Or press Ctrl+C to cancel)\n")
    
    try:
        # Read multiline input
        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break
        
        content = '\n'.join(lines)
        
        if not content.strip():
            print("\n❌ Content cannot be empty")
            return
        
        # Save session
        print("\nSaving session...")
        success = manager.save_session(content, summary)
        
        if success:
            print("✅ Session captured successfully!")
            print(f"Retention: {manager.config.get('memory', {}).get('retention_days', 14)} days")
        else:
            print("❌ Failed to save session")
    
    except KeyboardInterrupt:
        print("\n❌ Cancelled")
        return


def main():
    """Main entry point."""
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-h", "--help"]:
            print("""
Capture Copilot Chat Session

Usage:
    python capture_session.py

This script interactively captures and saves a Copilot Chat conversation.

You can also run this from Copilot Chat:
    User: "Run .ai-workflow/scripts/capture_session.py"
    Copilot: [Requests approval, then executes]

After running, you'll be prompted for:
1. A brief summary of the conversation
2. The full conversation content

Sessions are saved in .ai-workflow/memory/sessions/ and automatically
cleaned up after the configured retention period (default: 14 days).
            """)
            return
    
    capture_session()


if __name__ == "__main__":
    main()
