# Summarize Changes Prompt

## Your Task

Provide a human-readable summary of recent git commits and their significance for the project.

## Context Files to Read

1. **Recent Changes**: `#file:.ai-workflow/state/recent_changes.md`
2. **Change Manifest**: `#file:.ai-workflow/state/change_manifest.json` (if accessible)

## Instructions

1. **Read the recent changes**: Review what files were modified, added, or deleted

2. **Categorize by impact**:
   - **Learning content**: New tutorials, updated examples
   - **Documentation**: README updates, guide changes
   - **POCs**: New implementations, bug fixes
   - **Infrastructure**: Workflow changes, configuration updates

3. **Explain significance**:
   - What do these changes mean for users of this repository?
   - Are there new features or capabilities?
   - Are there breaking changes or important updates?
   - Do changes require action from contributors?

4. **Highlight important items**:
   - New POCs or learning modules
   - Breaking changes to existing patterns
   - Security-related updates
   - Configuration changes that affect setup

## Response Format

```markdown
## Recent Changes Summary

### Overview
[High-level summary of what changed]

### Changes by Category

#### Learning Materials
- [Summary of learning content changes]

#### Documentation
- [Summary of doc changes]

#### POCs (Proof of Concepts)
- [Summary of POC changes]

#### Infrastructure
- [Summary of workflow/config changes]

### Key Highlights
- 🌟 [Most important change]
- ⚠️ [Breaking change or action required]
- 💡 [Interesting addition]

### Impact Assessment
[How these changes affect users, contributors, and the project]

### Next Steps
[Recommended actions based on changes]
```

## Remember

- Focus on the "why" and "what it means", not just "what changed"
- Use clear, non-technical language where possible
- Flag anything that requires user action
- Connect related changes into coherent stories
- Prioritize information by importance to users
