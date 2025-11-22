#!/usr/bin/env python3
"""
Search Conversation Memory
Searches stored conversations for relevant context.
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from memory.manager import MemoryManager
except ImportError:
    print("Error: Could not import MemoryManager")
    sys.exit(1)


class MemorySearcher:
    """Searches conversation memory."""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.workflow_dir = self.repo_path / ".ai-workflow"
        self.memory_dir = self.workflow_dir / "memory"
        self.manager = MemoryManager(repo_path)
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search conversations for query string."""
        results = []
        
        user_dir = self.manager._get_user_session_dir()
        if not user_dir:
            return results
        
        # Case-insensitive search
        query_lower = query.lower()
        
        for session_file in sorted(user_dir.glob("*.md"), reverse=True):
            try:
                content = session_file.read_text()
                content_lower = content.lower()
                
                # Check if query appears in content
                if query_lower in content_lower:
                    # Extract metadata
                    lines = content.split('\n')
                    date = ""
                    summary = ""
                    
                    for line in lines:
                        if line.startswith("**Date**:"):
                            date = line.split(":", 1)[1].strip()
                        elif line.startswith("**Summary**:"):
                            summary = line.split(":", 1)[1].strip()
                    
                    # Find context around matches
                    matches = self._find_context(content, query, num_context_lines=3)
                    
                    results.append({
                        "filename": session_file.name,
                        "date": date,
                        "summary": summary,
                        "matches": matches,
                        "relevance": len(matches)  # Simple relevance score
                    })
            
            except Exception as e:
                print(f"Warning: Could not search {session_file.name}: {e}")
        
        # Sort by relevance and limit results
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results[:max_results]
    
    def _find_context(self, content: str, query: str, num_context_lines: int = 3) -> List[str]:
        """Find query with surrounding context."""
        lines = content.split('\n')
        query_lower = query.lower()
        matches = []
        
        for i, line in enumerate(lines):
            if query_lower in line.lower():
                # Get context lines
                start = max(0, i - num_context_lines)
                end = min(len(lines), i + num_context_lines + 1)
                
                context = '\n'.join(lines[start:end])
                matches.append(context)
        
        return matches[:3]  # Limit to 3 matches per session
    
    def generate_context_file(self, results: List[Dict]):
        """Generate relevant_context.md file."""
        output_file = self.memory_dir / "relevant_context.md"
        
        if not results:
            content = """# Relevant Context

No matching conversations found.

Try different search terms or check if conversations have been saved using:
```bash
python .ai-workflow/scripts/capture_session.py
```
"""
            output_file.write_text(content)
            return
        
        content = [
            "# Relevant Context\n",
            f"**Search completed**: Found {len(results)} relevant conversation(s)\n"
        ]
        
        for i, result in enumerate(results, 1):
            content.append(f"\n## {i}. {result['summary']}")
            content.append(f"**Date**: {result['date']}")
            content.append(f"**Relevance**: {result['relevance']} matches\n")
            
            if result['matches']:
                content.append("### Relevant Excerpts\n")
                for j, match in enumerate(result['matches'], 1):
                    content.append(f"#### Excerpt {j}\n")
                    content.append("```")
                    content.append(match)
                    content.append("```\n")
        
        output_file.write_text('\n'.join(content))
        print(f"✓ Context file generated: {output_file}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("""
Search Conversation Memory

Usage:
    python search_memory.py "search query"

Example:
    python search_memory.py "RAG implementation"

This searches stored conversations and generates a context file
that Copilot can read to provide better responses.
        """)
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    
    print(f"Searching for: '{query}'")
    
    repo_path = os.getenv("REPO_PATH", os.getcwd())
    searcher = MemorySearcher(repo_path)
    
    results = searcher.search(query)
    
    if results:
        print(f"\n✓ Found {len(results)} relevant conversation(s)")
        for result in results:
            print(f"  - {result['date']}: {result['summary']}")
        
        searcher.generate_context_file(results)
        print("\nCopilot can now read the context file:")
        print("  #file:.ai-workflow/memory/relevant_context.md")
    else:
        print("\n✗ No matching conversations found")
        searcher.generate_context_file([])


if __name__ == "__main__":
    main()
