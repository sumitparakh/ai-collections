# Quick Start Guide

Get the AI Workflow running in 60 seconds.

## Setup (One-Time)

```bash
# Run setup script
bash .ai-workflow/setup.sh

# That's it! The workflow is now active.
```

## Usage

### After Every Commit

The workflow runs automatically:

```bash
git add .
git commit -m "Your changes"
# ✅ AI Workflow: Documentation context updated
```

### Check What Needs Updating

In Copilot Chat:
```
#file:.github/prompts/check-status.md
```

### Get Update Suggestions

In Copilot Chat:
```
#file:.github/prompts/update-docs.md
```

### See All Commands

In Copilot Chat:
```
#file:.github/prompts/menu.md
```

## Save Important Conversations

From Copilot Chat or terminal:
```bash
python .ai-workflow/scripts/capture_session.py
```

## Search Past Conversations

```bash
python .ai-workflow/scripts/search_memory.py "your query"
```

Then in Copilot Chat:
```
#file:.ai-workflow/memory/relevant_context.md
```

## Configuration

Edit: `.ai-workflow/config/workflow.local.yaml`

```yaml
memory:
  retention_days: 14      # Change retention period
  enabled: true           # Disable memory if needed

context:
  max_size_kb: 10         # Adjust context file size limit
```

## Troubleshooting

**Hook not running?**
```bash
bash .ai-workflow/setup.sh  # Reinstall
```

**Memory not working?**
```bash
git config user.email "your@email.com"
```

**Check logs:**
```bash
cat .ai-workflow/state/workflow.log
```

## Full Documentation

See [.ai-workflow/README.md](.ai-workflow/README.md) for complete details.
