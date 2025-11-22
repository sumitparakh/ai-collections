# Search Memory Prompt

## Your Task

Search through past Copilot Chat conversations to find relevant context for the current query.

## How It Works

This prompt triggers a search of stored conversation history in `.ai-workflow/memory/sessions/`.

## Instructions for User

To search conversations:

1. **Run the search script**:
   ```bash
   python .ai-workflow/scripts/search_memory.py "your search query"
   ```

2. **Copilot will read the results**:
   The script generates `.ai-workflow/memory/relevant_context.md` with matching conversations.

3. **Ask your question again**:
   After running the script, ask Copilot your question. It will now have access to relevant past conversations.

## Example Workflow

```bash
# User wants to remember discussion about RAG patterns
python .ai-workflow/scripts/search_memory.py "RAG implementation"

# Then in Copilot Chat:
User: "What did we discuss about RAG implementations?"
Copilot: [References relevant_context.md and previous conversations]
```

## For Copilot

When this prompt is referenced:

1. **Check if search results exist**: Read `#file:.ai-workflow/memory/relevant_context.md`

2. **If results exist**:
   - Summarize what was found
   - Reference specific past conversations by timestamp
   - Use that context to inform your current response

3. **If no results**:
   - Inform user they need to run the search script first
   - Provide the command to run
   - Offer to help with their query using available context

## Search Tips

- Use specific keywords related to your topic
- Try different search terms if first attempt doesn't find relevant results
- Searches look through conversation summaries, not full transcripts
- More recent conversations are weighted higher in results

## Alternative: Execute from Chat

You can also ask Copilot to run the search script directly:

```
User: "Run search_memory.py with query 'agent patterns'"
Copilot: [Executes script with approval, then reads results]
```
