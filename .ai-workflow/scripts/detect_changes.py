#!/usr/bin/env python3
"""
Change Detection Script
Compares current HEAD with last processed commit to detect changes.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional

try:
    import git
    import yaml
except ImportError:
    print("Error: Required packages not installed. Run: pip install gitpython pyyaml")
    sys.exit(1)


class ChangeDetector:
    """Detects and categorizes changes in the repository."""
    
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
        
        # Load base config
        if config_file.exists():
            with open(config_file) as f:
                config = yaml.safe_load(f) or {}
        
        # Override with local config
        if local_config.exists():
            with open(local_config) as f:
                local = yaml.safe_load(f) or {}
                config.update(local)
        
        return config
    
    def _get_last_processed_commit(self) -> Optional[str]:
        """Get the last processed commit hash."""
        commit_file = self.state_dir / "last_processed_commit.txt"
        if commit_file.exists():
            return commit_file.read_text().strip()
        return None
    
    def _save_last_processed_commit(self, commit_hash: str):
        """Save the last processed commit hash."""
        commit_file = self.state_dir / "last_processed_commit.txt"
        commit_file.write_text(commit_hash)
    
    def _categorize_file(self, filepath: str) -> str:
        """Categorize file by directory."""
        path = Path(filepath)
        
        if path.parts[0] == "learning":
            return "learning"
        elif path.parts[0] == "docs":
            return "docs"
        elif path.parts[0] == "pocs":
            return "pocs"
        elif filepath in ["README.md", "CONTRIBUTING.md"]:
            return "root-docs"
        elif filepath == ".github/copilot-instructions.md":
            return "copilot-instructions"
        elif filepath.startswith(".ai-workflow"):
            return "workflow"
        else:
            return "other"
    
    def _detect_conflicts(self, changed_files: Set[str]) -> List[Dict]:
        """Detect potential documentation conflicts."""
        conflicts = []
        
        if not self.config.get("documentation", {}).get("conflict_detection", True):
            return conflicts
        
        tracked_patterns = self.config.get("documentation", {}).get("tracked_files", [])
        
        for file in changed_files:
            # Check if file matches tracked patterns
            for pattern in tracked_patterns:
                if self._matches_pattern(file, pattern):
                    # Check if this is a documentation file
                    if file.endswith(".md"):
                        conflicts.append({
                            "file": file,
                            "reason": "Documentation file modified - may need review",
                            "severity": "info"
                        })
                    break
        
        return conflicts
    
    def _matches_pattern(self, filepath: str, pattern: str) -> bool:
        """Check if filepath matches glob pattern."""
        from fnmatch import fnmatch
        return fnmatch(filepath, pattern)
    
    def detect_changes(self) -> Dict:
        """Detect changes since last processed commit."""
        current_commit = self.repo.head.commit.hexsha
        last_commit = self._get_last_processed_commit()
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "current_commit": current_commit,
            "last_commit": last_commit,
            "changes": {
                "learning": [],
                "docs": [],
                "pocs": [],
                "root-docs": [],
                "copilot-instructions": [],
                "workflow": [],
                "other": []
            },
            "stats": {},
            "conflicts": []
        }
        
        if last_commit is None:
            # First run - mark current as baseline
            self._save_last_processed_commit(current_commit)
            result["first_run"] = True
            return result
        
        if last_commit == current_commit:
            # No changes
            result["no_changes"] = True
            return result
        
        # Get changed files
        try:
            last_commit_obj = self.repo.commit(last_commit)
            current_commit_obj = self.repo.commit(current_commit)
            
            diffs = last_commit_obj.diff(current_commit_obj)
            
            changed_files = set()
            
            for diff in diffs:
                # Handle different types of changes
                if diff.a_path:
                    changed_files.add(diff.a_path)
                if diff.b_path:
                    changed_files.add(diff.b_path)
                
                category = self._categorize_file(diff.b_path or diff.a_path)
                
                change_info = {
                    "path": diff.b_path or diff.a_path,
                    "change_type": diff.change_type,
                    "additions": diff.diff.decode('utf-8', errors='ignore') if diff.diff else ""
                }
                
                result["changes"][category].append(change_info)
            
            # Calculate stats
            for category, changes in result["changes"].items():
                result["stats"][category] = len(changes)
            
            # Detect conflicts
            result["conflicts"] = self._detect_conflicts(changed_files)
            
            # Save current commit as processed
            self._save_last_processed_commit(current_commit)
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def save_change_manifest(self, changes: Dict):
        """Save change detection results as JSON manifest."""
        manifest_file = self.state_dir / "change_manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(changes, f, indent=2)


def main():
    """Main entry point."""
    # Get repository path
    repo_path = os.getenv("REPO_PATH", os.getcwd())
    
    detector = ChangeDetector(repo_path)
    changes = detector.detect_changes()
    detector.save_change_manifest(changes)
    
    # Print summary
    if changes.get("first_run"):
        print("✓ First run - baseline established")
    elif changes.get("no_changes"):
        print("✓ No changes detected")
    else:
        total_changes = sum(changes.get("stats", {}).values())
        print(f"✓ Detected {total_changes} changes")
        
        if changes.get("conflicts"):
            print(f"⚠ {len(changes['conflicts'])} potential conflicts detected")


if __name__ == "__main__":
    main()
