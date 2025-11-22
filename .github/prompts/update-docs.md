# Update Documentation Prompt

## Your Task

Review the recent changes in this repository and suggest updates to documentation files.

## Context Files to Read

**IMPORTANT**: Before responding, read these files to understand what changed:

1. **Recent Changes**: `#file:.ai-workflow/state/recent_changes.md`  
   Shows what files were modified in recent commits

2. **Documentation Status**: `#file:.ai-workflow/state/docs_status.md`  
   Lists which documentation files may need updates

3. **Last Sync**: `#file:.ai-workflow/state/last_sync.md`  
   Shows when changes were last processed

## Instructions

1. **Analyze the changes** from `recent_changes.md`:
   - What categories were affected? (learning/, docs/, pocs/, etc.)
   - What type of changes were made? (new files, modifications, deletions)
   - Are there architectural or structural changes?

2. **Determine documentation impact**:
   - Does `README.md` need updates for new content?
   - Should `CONTRIBUTING.md` be updated with new patterns?
   - Does `.github/copilot-instructions.md` need new guidance?
   - Do category READMEs (learning/, docs/, pocs/) need updates?

3. **Check for conflicts**:
   - Review any warnings in `docs_status.md`
   - Flag if documentation was manually edited (may conflict with auto-updates)

4. **Provide specific suggestions**:
   - Quote the exact sections that need updating
   - Suggest new content to add
   - Explain WHY each update is needed
   - Provide the updated text in markdown format

## Response Format

```markdown
## Documentation Update Analysis

### Files Changed
[Summary of changes from recent_changes.md]

### Recommended Documentation Updates

#### 1. README.md
**Reason**: [Why this needs updating]
**Section**: [Which section to update]
**Suggested Change**:
```markdown
[Exact new content]
```

#### 2. [Other file]
[Same pattern]

### Conflicts/Warnings
[Any conflicts detected]

### Implementation Notes
[How to apply these updates safely]
```

## Remember

- Prioritize the user's immediate request first
- Add documentation suggestions at the END of your response
- Be specific - provide exact text changes, not vague suggestions
- Respect the repository's structure (learning/ vs docs/ vs pocs/)
- Follow existing documentation patterns and style
- Never suggest removing security features or API key protections
