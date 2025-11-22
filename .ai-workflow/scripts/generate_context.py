#!/usr/bin/env python3
"""
Context File Generator
Generates markdown context files for GitHub Copilot to read.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

try:
    import git
    import yaml
except ImportError:
    print("Error: Required packages not installed. Run: pip install gitpython pyyaml")
    sys.exit(1)


class ContextGenerator:
    """Generates context files from change detection results."""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.workflow_dir = self.repo_path / ".ai-workflow"
        self.state_dir = self.workflow_dir / "state"
        self.config_dir = self.workflow_dir / "config"
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize git repo
        try:
            self.repo = git.Repo(self.repo_path)
        except git.InvalidGitRepositoryError:
            print("Error: Not a git repository")
            sys.exit(1)
    
    def _load_config(self) -> Dict:
        """Load workflow configuration."""
        config_file = self.config_dir / "workflow.yaml"
        local_config = self.config_dir / "workflow.local.yaml"
        
        config = {}
        
        if config_file.exists():
            with open(config_file) as f:
                config = yaml.safe_load(f) or {}
        
        if local_config.exists():
            with open(local_config) as f:
                local = yaml.safe_load(f) or {}
                config.update(local)
        
        return config
    
    def _load_change_manifest(self) -> Dict:
        """Load the latest change detection manifest."""
        manifest_file = self.state_dir / "change_manifest.json"
        if not manifest_file.exists():
            return {}
        
        with open(manifest_file) as f:
            return json.load(f)
    
    def _summarize_if_needed(self, content: str, max_size_kb: int = 10) -> tuple[str, bool]:
        """Summarize content if it exceeds size limit."""
        size_kb = len(content.encode('utf-8')) / 1024
        
        if size_kb <= max_size_kb:
            return content, False
        
        # Content is too large, summarize
        lines = content.split('\n')
        
        # Keep header and summary info
        summary_lines = []
        summary_lines.append("# Recent Changes (Summarized)")
        summary_lines.append(f"\n⚠️ **Note**: Full diff exceeded {max_size_kb}KB limit. Showing summary only.\n")
        
        # Extract file changes without full diffs
        in_diff = False
        current_file = None
        
        for line in lines:
            if line.startswith('## ') or line.startswith('# '):
                summary_lines.append(line)
                in_diff = False
            elif line.startswith('### File:'):
                current_file = line
                summary_lines.append(line)
                in_diff = False
            elif line.startswith('```diff'):
                in_diff = True
                summary_lines.append("```")
                summary_lines.append("(Diff content omitted for brevity)")
                summary_lines.append("```")
            elif line.startswith('```') and in_diff:
                in_diff = False
            elif not in_diff:
                summary_lines.append(line)
        
        return '\n'.join(summary_lines), True
    
    def generate_recent_changes(self) -> str:
        """Generate recent_changes.md file."""
        manifest = self._load_change_manifest()
        
        if not manifest or manifest.get("first_run") or manifest.get("no_changes"):
            return self._generate_no_changes_message(manifest)
        
        content = []
        content.append("# Recent Changes")
        content.append(f"\n**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append(f"\n**Current Commit**: `{manifest.get('current_commit', 'N/A')[:8]}`")
        content.append(f"**Last Processed**: `{manifest.get('last_commit', 'N/A')[:8]}`\n")
        
        # Add statistics
        stats = manifest.get("stats", {})
        total_changes = sum(stats.values())
        
        content.append(f"## Summary\n")
        content.append(f"Total files changed: **{total_changes}**\n")
        
        if stats:
            content.append("### Changes by Category\n")
            for category, count in stats.items():
                if count > 0:
                    content.append(f"- **{category}**: {count} files")
            content.append("")
        
        # Add conflicts if any
        conflicts = manifest.get("conflicts", [])
        if conflicts:
            content.append(f"## ⚠️ Potential Conflicts ({len(conflicts)})\n")
            for conflict in conflicts:
                content.append(f"- **{conflict['file']}**: {conflict['reason']}")
            content.append("")
        
        # Add detailed changes by category
        changes = manifest.get("changes", {})
        
        for category in ["learning", "docs", "pocs", "root-docs", "copilot-instructions", "other"]:
            category_changes = changes.get(category, [])
            if not category_changes:
                continue
            
            content.append(f"\n## {category.replace('-', ' ').title()} Changes\n")
            
            for change in category_changes:
                path = change.get("path", "Unknown")
                change_type = change.get("change_type", "M")
                
                content.append(f"### File: `{path}`")
                content.append(f"**Change Type**: {self._format_change_type(change_type)}\n")
                
                # Add diff preview (limited)
                diff = change.get("additions", "")
                if diff and len(diff) < 5000:  # Only show small diffs
                    content.append("```diff")
                    content.append(diff[:2000])  # Limit diff size
                    if len(diff) > 2000:
                        content.append("\n... (diff truncated)")
                    content.append("```\n")
        
        full_content = '\n'.join(content)
        
        # Check size and summarize if needed
        max_size = self.config.get("context", {}).get("max_size_kb", 10)
        final_content, was_summarized = self._summarize_if_needed(full_content, max_size)
        
        if was_summarized:
            print(f"⚠️ Context file summarized (exceeded {max_size}KB)")
        
        return final_content
    
    def _generate_no_changes_message(self, manifest: Dict) -> str:
        """Generate message when no changes detected."""
        content = []
        content.append("# Recent Changes\n")
        content.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        if manifest.get("first_run"):
            content.append("ℹ️ **First run** - Baseline established. No changes to report yet.")
        elif manifest.get("no_changes"):
            content.append("✓ **No changes detected** since last sync.")
        else:
            content.append("ℹ️ No change data available.")
        
        return '\n'.join(content)
    
    def _format_change_type(self, change_type: str) -> str:
        """Format git change type."""
        types = {
            "A": "Added",
            "D": "Deleted",
            "M": "Modified",
            "R": "Renamed",
            "T": "Type changed"
        }
        return types.get(change_type, change_type)
    
    def generate_docs_status(self) -> str:
        """Generate docs_status.md file."""
        manifest = self._load_change_manifest()
        
        content = []
        content.append("# Documentation Status\n")
        content.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        changes = manifest.get("changes", {})
        conflicts = manifest.get("conflicts", [])
        
        # Determine which docs need updates
        needs_update = []
        
        if changes.get("learning"):
            needs_update.append("- Learning module READMEs may need updates")
        
        if changes.get("docs"):
            needs_update.append("- Documentation files may need updates")
        
        if changes.get("pocs"):
            needs_update.append("- POC READMEs may need updates")
        
        if changes.get("root-docs"):
            needs_update.append("- Root documentation (README.md, CONTRIBUTING.md) may need review")
        
        if changes.get("copilot-instructions"):
            needs_update.append("- Copilot instructions file was modified directly")
        
        if needs_update:
            content.append("## 📝 Documentation Updates Needed\n")
            content.extend(needs_update)
            content.append("")
        else:
            content.append("✓ **All documentation appears up-to-date**\n")
        
        # Add conflict warnings
        if conflicts:
            content.append(f"\n## ⚠️ Conflicts Detected ({len(conflicts)})\n")
            for conflict in conflicts:
                content.append(f"### {conflict['file']}")
                content.append(f"- **Issue**: {conflict['reason']}")
                content.append(f"- **Severity**: {conflict['severity']}\n")
        
        return '\n'.join(content)
    
    def generate_last_sync(self) -> str:
        """Generate last_sync.md file."""
        manifest = self._load_change_manifest()
        
        content = []
        content.append("# Last Sync Status\n")
        
        timestamp = manifest.get("timestamp", "Unknown")
        current_commit = manifest.get("current_commit", "N/A")
        last_commit = manifest.get("last_commit", "N/A")
        
        content.append(f"**Last Sync**: {timestamp}")
        content.append(f"**Current Commit**: `{current_commit[:8] if current_commit != 'N/A' else 'N/A'}`")
        content.append(f"**Previous Commit**: `{last_commit[:8] if last_commit != 'N/A' else 'N/A'}`\n")
        
        if manifest.get("first_run"):
            content.append("**Status**: ✓ Initial baseline established")
        elif manifest.get("no_changes"):
            content.append("**Status**: ✓ No changes detected")
        elif manifest.get("error"):
            content.append(f"**Status**: ❌ Error - {manifest.get('error')}")
        else:
            total_changes = sum(manifest.get("stats", {}).values())
            content.append(f"**Status**: ✓ {total_changes} changes processed")
        
        return '\n'.join(content)
    
    def generate_all(self):
        """Generate all context files."""
        # Generate recent_changes.md
        recent_changes = self.generate_recent_changes()
        recent_changes_file = self.state_dir / "recent_changes.md"
        recent_changes_file.write_text(recent_changes)
        
        # Generate docs_status.md
        docs_status = self.generate_docs_status()
        docs_status_file = self.state_dir / "docs_status.md"
        docs_status_file.write_text(docs_status)
        
        # Generate last_sync.md
        last_sync = self.generate_last_sync()
        last_sync_file = self.state_dir / "last_sync.md"
        last_sync_file.write_text(last_sync)
        
        print("✓ Context files generated successfully")


def main():
    """Main entry point."""
    repo_path = os.getenv("REPO_PATH", os.getcwd())
    
    generator = ContextGenerator(repo_path)
    generator.generate_all()


if __name__ == "__main__":
    main()
