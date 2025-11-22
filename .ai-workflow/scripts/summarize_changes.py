#!/usr/bin/env python3
"""
Summarize Recent Changes
Formats recent git history into readable markdown.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

try:
    import git
except ImportError:
    print("Error: gitpython not installed. Run: pip install gitpython")
    sys.exit(1)


def summarize_changes(repo_path: str, num_commits: int = 10):
    """Generate a summary of recent commits."""
    try:
        repo = git.Repo(repo_path)
    except git.InvalidGitRepositoryError:
        print("Error: Not a git repository")
        sys.exit(1)
    
    # Get recent commits
    commits = list(repo.iter_commits('HEAD', max_count=num_commits))
    
    if not commits:
        print("No commits found")
        return
    
    # Build summary
    content = []
    content.append("# Recent Commits Summary\n")
    content.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    content.append(f"**Commits analyzed**: {len(commits)}\n")
    
    for i, commit in enumerate(commits, 1):
        content.append(f"## {i}. {commit.summary}")
        content.append(f"**Author**: {commit.author.name}")
        content.append(f"**Date**: {datetime.fromtimestamp(commit.committed_date).strftime('%Y-%m-%d %H:%M')}")
        content.append(f"**SHA**: `{commit.hexsha[:8]}`\n")
        
        # Get changed files
        if commit.parents:
            diffs = commit.parents[0].diff(commit)
            
            if diffs:
                content.append("**Changed files**:")
                for diff in diffs[:10]:  # Limit to 10 files per commit
                    path = diff.b_path or diff.a_path
                    change_type = diff.change_type
                    content.append(f"- `{path}` ({change_type})")
                
                if len(diffs) > 10:
                    content.append(f"- ... and {len(diffs) - 10} more files")
        
        content.append("")
    
    # Save to state directory
    workflow_dir = Path(repo_path) / ".ai-workflow"
    state_dir = workflow_dir / "state"
    state_dir.mkdir(parents=True, exist_ok=True)
    
    summary_file = state_dir / "commit_summary.md"
    summary_file.write_text('\n'.join(content))
    
    print(f"✓ Summary generated: {summary_file}")
    print(f"  Analyzed {len(commits)} commits")


def main():
    """Main entry point."""
    repo_path = os.getenv("REPO_PATH", os.getcwd())
    
    # Check for command line arguments
    num_commits = 10
    if len(sys.argv) > 1:
        try:
            num_commits = int(sys.argv[1])
        except ValueError:
            print("Usage: python summarize_changes.py [num_commits]")
            sys.exit(1)
    
    summarize_changes(repo_path, num_commits)


if __name__ == "__main__":
    main()
