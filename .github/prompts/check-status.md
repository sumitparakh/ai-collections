# Check Documentation Status Prompt

## Your Task

Review which documentation files may be out of sync and need attention.

## Context Files to Read

1. **Documentation Status**: `#file:.ai-workflow/state/docs_status.md`
2. **Recent Changes**: `#file:.ai-workflow/state/recent_changes.md`
3. **Last Sync**: `#file:.ai-workflow/state/last_sync.md`

## Instructions

1. **Read the status files** to understand:
   - When changes were last processed
   - Which documentation areas have updates
   - Any conflicts or warnings

2. **Assess urgency**:
   - Critical: Documentation is wrong or misleading
   - Important: Documentation is outdated but functional
   - Optional: Nice-to-have improvements

3. **Provide actionable information**:
   - List specific files that need updates
   - Explain why each file needs attention
   - Suggest priority order for updates

## Response Format

```markdown
## Documentation Status Report

### Last Sync
[When was the last sync, what commit]

### Status Overview
✅ **Up to date**: [Number] files  
⚠️ **Needs review**: [Number] files  
❌ **Out of sync**: [Number] files  

### Files Needing Attention

#### Priority: Critical
1. **[filename]**
   - Why: [Reason it needs updating]
   - Impact: [What's wrong if not updated]
   - Affected sections: [Which parts]

#### Priority: Important
[Same format]

#### Priority: Optional
[Same format]

### Conflicts Detected
[Any files that were manually edited and might conflict]

### Recommended Action Plan
1. [First thing to update]
2. [Second thing to update]
3. [etc.]

### Notes
[Additional context or warnings]
```

## Special Cases

- **No changes detected**: Report that everything is up to date
- **First run**: Explain baseline was just established
- **Conflicts**: Warn about manual edits that might be overwritten
- **Errors**: Report if status files can't be read

## Remember

- Be honest about status - don't say "all good" if there are issues
- Prioritize by impact, not file count
- Consider user's current work context when suggesting priorities
- Flag security-related documentation issues as critical
