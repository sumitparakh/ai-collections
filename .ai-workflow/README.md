# AI Workflow System

An intelligent, prompt-based agentic workflow for maintaining documentation in sync with code changes, using GitHub Copilot Chat.

## Overview

This workflow system automatically detects repository changes and generates context files that GitHub Copilot reads to provide intelligent documentation suggestions - **without requiring external APIs, extensions, or manual work**.

### How It Works

```
┌─────────────┐
│  Git Commit │
└──────┬──────┘
       │
       ▼
┌──────────────────────┐
│ Post-Commit Hook     │
│ (.git/hooks/)        │
└──────┬───────────────┘
       │
       ├──▶ detect_changes.py ──▶ Change Manifest (.ai-workflow/state/change_manifest.json)
       │
       └──▶ generate_context.py ─┬──▶ recent_changes.md (What changed)
                                  ├──▶ docs_status.md (What needs updating)
                                  └──▶ last_sync.md (When last processed)
       
┌─────────────────────┐
│ Copilot Chat        │
│ Reads context files │
└─────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ User asks anything                   │
│ Copilot responds + suggests doc      │
│ updates if needed                    │
└──────────────────────────────────────┘
```

## Key Features

### 🤖 Automated Change Detection
- Runs on every git commit via post-commit hook
- Tracks file changes by category (learning/, docs/, pocs/)
- Detects potential documentation conflicts
- No manual intervention required

### 📝 Intelligent Context Generation
- Generates markdown files Copilot automatically reads
- Summarizes changes with automatic size limits
- Flags which documentation needs updates
- Preserves full git context

### 💬 Custom Copilot Commands
- Pre-built prompts for common tasks
- Documentation update suggestions
- Change summarization
- Status checking
- Memory search

### 🧠 Conversation Memory (Optional)
- Save important Copilot Chat sessions
- Search past conversations for context
- Automatic cleanup based on retention period
- Privacy-first (hashed user IDs, gitignored)

## Directory Structure

```
.ai-workflow/
├── config/
│   ├── workflow.yaml              # Configuration template (tracked)
│   └── workflow.local.yaml        # User overrides (gitignored)
├── hooks/
│   └── post-commit                # Git hook template
├── memory/                        # Conversation history (gitignored)
│   ├── sessions/{user-hash}/      # User-specific sessions
│   ├── index.md                   # Session index
│   └── relevant_context.md        # Search results
├── scripts/
│   ├── detect_changes.py          # Change detection engine
│   ├── generate_context.py        # Context file generator
│   ├── search_memory.py           # Memory search
│   ├── summarize_changes.py       # Commit summarizer
│   └── capture_session.py         # Save conversations
├── state/                         # Context files (gitignored)
│   ├── recent_changes.md          # Recent git changes
│   ├── docs_status.md             # Documentation status
│   ├── last_sync.md               # Last sync info
│   ├── change_manifest.json       # Detailed change data
│   ├── last_processed_commit.txt  # Baseline commit
│   └── workflow.log               # Activity log
└── setup.sh                       # Setup automation

.github/prompts/                   # Custom Copilot prompts (tracked)
├── menu.md                        # Command list
├── update-docs.md                 # Documentation updates
├── check-status.md                # Status check
├── summarize-changes.md           # Change summary
└── search-memory.md               # Memory search
```

## Setup

### Prerequisites

- Git repository
- Python 3.8+
- Git `user.email` configured (for memory features)

### Installation

Run the setup script:

```bash
bash .ai-workflow/setup.sh
```

This will:
1. Verify prerequisites
2. Install Python dependencies (gitpython, pyyaml)
3. Create local configuration
4. Install post-commit git hook
5. Establish baseline commit
6. Generate initial context files

### Configuration

Edit `.ai-workflow/config/workflow.local.yaml`:

```yaml
# Memory settings
memory:
  retention_days: 14        # How long to keep conversations
  enabled: true             # Enable/disable memory
  max_session_size_kb: 100  # Max session file size

# Context file settings
context:
  max_size_kb: 10           # Max context file size before summarization
  commits_to_track: 10      # Number of commits to analyze
  auto_summarize: true      # Auto-compress large diffs

# Documentation targets
documentation:
  conflict_detection: true  # Warn about manual doc edits

# Logging
logging:
  level: INFO               # DEBUG, INFO, WARNING, ERROR
```

## Usage

### Basic Workflow

1. **Make changes and commit**:
   ```bash
   git add <files>
   git commit -m "Add new feature"
   # Post-commit hook runs automatically
   ```

2. **Check status in Copilot Chat**:
   ```
   #file:.github/prompts/check-status.md
   ```

3. **Get documentation suggestions**:
   ```
   #file:.github/prompts/update-docs.md
   ```

4. **Apply suggested changes** and commit again

### Custom Prompts

All available commands are in `.github/prompts/`:

#### 📋 Show Menu
```
#file:.github/prompts/menu.md
```
Lists all available workflow commands.

#### 📝 Update Documentation
```
#file:.github/prompts/update-docs.md
```
Analyzes recent changes and suggests specific documentation updates.

#### ✅ Check Status
```
#file:.github/prompts/check-status.md
```
Shows which documentation files are out of sync.

#### 📊 Summarize Changes
```
#file:.github/prompts/summarize-changes.md
```
Provides human-readable summary of recent commits.

#### 🔍 Search Memory
```
#file:.github/prompts/search-memory.md
```
Search past conversations (requires running search script first).

### Conversation Memory

#### Save a Session

From Copilot Chat, execute:
```bash
python .ai-workflow/scripts/capture_session.py
```

Or run manually:
```bash
cd /path/to/repo
python .ai-workflow/scripts/capture_session.py
```

#### Search Past Conversations

```bash
python .ai-workflow/scripts/search_memory.py "your search query"
```

Then in Copilot Chat:
```
#file:.ai-workflow/memory/relevant_context.md
```

## How Copilot Integration Works

### Context Files Copilot Reads

Copilot automatically reads these markdown files when you chat:

1. **`.ai-workflow/state/recent_changes.md`**  
   - What files changed
   - Categorized by type (learning/, docs/, pocs/)
   - Conflict warnings

2. **`.ai-workflow/state/docs_status.md`**  
   - Which docs need updates
   - Why they need updating
   - Priority levels

3. **`.ai-workflow/state/last_sync.md`**  
   - When last processed
   - Current commit
   - Processing status

4. **`.github/copilot-instructions.md`**  
   - Overall repository guidance
   - Workflow integration instructions
   - Response priorities

### No External APIs Required

- Uses GitHub Copilot's built-in context reading
- No OpenAI/Anthropic API calls needed
- No VS Code extensions to install
- Works entirely through prompts and file references

## Architecture Decisions

### Why `.ai-workflow/` Directory?

- Avoids conflicts with `.github/copilot-*` (official Copilot)
- Avoids conflicts with `.vscode/` (VS Code settings)
- Clearly indicates purpose
- Easy to identify and exclude from git

### Why Prompt-Based?

- No extension development needed
- No API costs or rate limits
- Works with existing Copilot subscription
- Easy to customize and extend
- Transparent and auditable

### Why Post-Commit Hook?

- Runs automatically after every commit
- No GitHub Actions setup needed
- Works offline
- Instant feedback
- User controls execution (local only)

### Why Markdown Context Files?

- Copilot naturally reads markdown
- Human-readable and debuggable
- Easy to version control templates
- Natural language for AI understanding

## Troubleshooting

### Hook Not Running

Check if installed:
```bash
ls -la .git/hooks/post-commit
```

Reinstall:
```bash
bash .ai-workflow/setup.sh
```

### Memory Not Working

Check git config:
```bash
git config user.email
```

Set if missing:
```bash
git config user.email "your@email.com"
```

### Missing Dependencies

Install manually:
```bash
pip3 install gitpython pyyaml
```

### Context Files Not Generated

Run manually:
```bash
export REPO_PATH=$(pwd)
python3 .ai-workflow/scripts/detect_changes.py
python3 .ai-workflow/scripts/generate_context.py
```

Check logs:
```bash
cat .ai-workflow/state/workflow.log
```

### Large Diff Summaries

Context files are automatically summarized when they exceed configured size limit (default 10KB). Adjust in `workflow.local.yaml`:

```yaml
context:
  max_size_kb: 20  # Increase limit
```

## Advanced Usage

### Manual Change Detection

Force re-detection:
```bash
export REPO_PATH=$(pwd)
python3 .ai-workflow/scripts/detect_changes.py
python3 .ai-workflow/scripts/generate_context.py
```

### Commit History Summary

Generate summary of last N commits:
```bash
python3 .ai-workflow/scripts/summarize_changes.py 20
```

### View Memory Index

```bash
cat .ai-workflow/memory/index.md
```

### Cleanup Old Sessions Manually

Delete sessions older than retention period:
```bash
python3 .ai-workflow/memory/manager.py
```

## Customization

### Add New Prompts

Create a new file in `.github/prompts/`:

```markdown
# My Custom Prompt

## Your Task
[Description of what Copilot should do]

## Context Files to Read
1. `#file:.ai-workflow/state/recent_changes.md`
2. [Other files]

## Instructions
[Step-by-step instructions for Copilot]

## Response Format
[Expected output format]
```

Reference in chat:
```
#file:.github/prompts/my-custom-prompt.md
```

### Extend Change Detection

Edit `.ai-workflow/scripts/detect_changes.py` to add custom categorization or detection logic.

### Custom Context Files

Edit `.ai-workflow/scripts/generate_context.py` to generate additional context files for your specific needs.

## Limitations

### What This System Does NOT Do

- ❌ Automatically apply documentation changes (requires human review)
- ❌ Run on remote pushes (post-commit is local only)
- ❌ Generate code or implementations (only documentation suggestions)
- ❌ Replace manual code review
- ❌ Work without Copilot subscription

### Current Constraints

- Requires local git commits to trigger
- Copilot context window limits apply
- Memory search is keyword-based (not semantic)
- No multi-repository support
- Requires Python 3.8+

## Future Enhancements

Possible improvements (not yet implemented):

- Semantic memory search with embeddings
- GitHub Actions integration for CI/CD
- Multi-repository workspace support
- Automatic PR generation for doc updates
- Integration with issue tracking
- Custom LLM backends (local models)

## Security & Privacy

### What's Tracked

- File paths and change types
- Git commit metadata (hash, author, date)
- Conversation summaries (if you save them)

### What's NOT Tracked

- File contents (only in gitignored state files)
- API keys or secrets
- Personal data beyond git user.email (hashed)

### Data Storage

- All sensitive data in `.ai-workflow/memory/` and `.ai-workflow/state/` (gitignored)
- User IDs hashed with SHA-256
- No external services or APIs called
- Everything stored locally

## Contributing

To improve this workflow:

1. Test changes locally
2. Update this README
3. Add examples if adding features
4. Document configuration options
5. Submit PR with clear description

## License

Same as parent repository.

## Support

- Check this README first
- Review `.ai-workflow/state/workflow.log` for errors
- Open an issue with logs and configuration
- Reference `.github/copilot-instructions.md` for guidance

---

**Happy workflow automation! 🤖**
