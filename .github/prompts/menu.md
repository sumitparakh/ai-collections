# AI Workflow Commands

Welcome to the AI-powered documentation workflow! Use these custom prompts to interact with the system.

## Available Commands

### 📋 `/update-docs` - Update Documentation
**File**: `#file:.github/prompts/update-docs.md`

Reviews recent changes and suggests documentation updates. Use this after making code or structural changes to keep docs in sync.

### 🔍 `/search-memory` - Search Conversation History  
**File**: `#file:.github/prompts/search-memory.md`

Search through past Copilot Chat conversations to find relevant context. Useful when you remember discussing something but need to recall the details.

### 📊 `/summarize-changes` - Summarize Recent Changes
**File**: `#file:.github/prompts/summarize-changes.md`

Get a human-readable summary of recent git commits and what they mean for the project.

### ✅ `/check-status` - Check Documentation Status
**File**: `#file:.github/prompts/check-status.md`

See which documentation files might be out of sync and need attention.

## How to Use

1. **Reference a prompt in chat**: Type `#file:.github/prompts/[prompt-name].md` in Copilot Chat
2. **Copilot reads the instructions**: The prompt file guides Copilot on what to do
3. **Copilot accesses context**: Automatically reads `.ai-workflow/state/` files for current repository state
4. **Get intelligent responses**: Copilot provides context-aware suggestions

## Example Usage

```
User: #file:.github/prompts/update-docs.md
Copilot: [Reads recent changes and suggests doc updates]

User: #file:.github/prompts/check-status.md  
Copilot: [Shows which docs need attention]
```

## Tips

- Commands work best after committing changes (triggers the post-commit hook)
- Combine commands: First check status, then update docs
- Regular memory saves help maintain conversation context
- Reference this menu anytime with `#file:.github/prompts/menu.md`
