# AI Collections - Copilot Instructions

## Repository Purpose

This is a **learning and reference repository** for AI development, organized into three main pillars:
- `learning/` - Educational tutorials and step-by-step guides
- `docs/` - Comprehensive documentation and best practices
- `pocs/` - Proof-of-concept implementations

**Critical**: This is NOT a production codebase. Each directory is self-contained and demonstrates specific AI concepts.

## Repository Structure & Navigation

### Three-Tier Organization
```
learning/       # Educational content - concepts, tutorials, exercises
  ├── fundamentals/
  ├── llm-workflows/
  ├── embeddings/
  ├── rag/
  ├── agents/
  └── mcp-servers/

docs/          # Reference documentation and guides
  ├── guides/
  ├── best-practices/
  ├── architecture/
  ├── api-references/
  ├── troubleshooting/
  └── resources/

pocs/          # Working implementations
  ├── llm-workflows/
  ├── embeddings/
  ├── rag/
  ├── agents/
  ├── mcp-servers/
  ├── automation/
  └── integrations/
```

### Navigation Principle
- Users exploring **concepts** → `learning/`
- Users seeking **guidance** → `docs/`
- Users wanting **working code** → `pocs/`

## Content Standards

### Every POC Directory Must Include
```
poc-name/
├── README.md          # Overview, objectives, setup, usage, limitations
├── .env.example       # Sample environment variables (NEVER actual keys)
├── src/               # Well-commented source code
├── examples/          # Usage examples with expected outputs
└── [package files]    # requirements.txt, package.json, or Cargo.toml
```

### README Template (POCs)
Each POC README should have:
1. **Overview** - What it demonstrates and why
2. **Prerequisites** - Required knowledge and dependencies
3. **Setup Instructions** - Exact steps to run
4. **Usage Examples** - Working code snippets
5. **Implementation Notes** - Key design decisions
6. **Limitations** - Known constraints or issues
7. **Future Improvements** - Potential enhancements

### README Template (Learning)
Each learning module README should include:
1. **Learning Objectives** - What you'll understand
2. **Prerequisites** - Required background knowledge
3. **Concepts Explained** - Core ideas with examples
4. **Code Examples** - Runnable demonstrations
5. **Exercises** (optional) - Practice problems
6. **Further Resources** - External links and references

## Multi-Language Support

### Language Distribution
- **Python** - Primary language for AI/ML examples (most learning content and POCs)
- **TypeScript/JavaScript** - Web integrations and Node.js examples
- **Rust** - Performance-critical or systems-level examples

### Language-Specific Conventions

**Python**
- Follow PEP 8
- Use type hints: `def generate_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:`
- Include docstrings for all functions
- Virtual environments: `python -m venv venv`

**TypeScript/JavaScript**
- Prefer TypeScript for type safety
- Use async/await over promises
- JSDoc comments: `/** @param {string} text - The text to embed */`
- Modern ES modules

**Rust**
- Run `cargo fmt` and `cargo clippy`
- Documentation comments: `/// Generate embedding for the given text`
- Async with tokio

## Security & Environment Variables

### Non-Negotiable Rules
1. **NEVER commit actual API keys** - Check `.gitignore` includes `.env` and `*.env`
2. Always provide `.env.example` with dummy values:
   ```bash
   # .env.example
   OPENAI_API_KEY=sk-your-key-here
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```
3. Load env vars in code:
   - Python: `from dotenv import load_dotenv; load_dotenv()`
   - Node: `import dotenv from 'dotenv'; dotenv.config();`

### Gitignore Coverage
Already includes: `.env`, `.env.local`, `*.env`, `*.key`, vector DB files, model binaries, venv/, node_modules/

## AI-Specific Patterns

### Common Topics Demonstrated
- **LLM Workflows** - Prompt engineering, function calling, streaming, multi-step
- **Embeddings** - Text embeddings, semantic search, vector databases
- **RAG** - Document processing, retrieval strategies, re-ranking, citation
- **Agents** - ReAct patterns, planning, tool use, multi-agent systems
- **MCP** - Model Context Protocol servers and client integration

### Architecture Patterns
When adding new POCs, follow established patterns:
1. **RAG Pipeline**: Ingest → Chunk → Embed → Store → Retrieve → Generate
2. **Agent Loop**: Plan → Execute → Observe → Reflect → Repeat
3. **MCP Server**: Tool definitions → Resource management → Server implementation

## Development Workflow

### Testing Setup Before Running Code
```bash
# Python
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Node.js
npm install

# Rust
cargo build
```

### No Centralized Dependencies
Each POC manages its own dependencies - there's no root-level `requirements.txt` or `package.json`. When creating POCs, always include dependency files in that POC's directory.

## Contributing Guidelines (from CONTRIBUTING.md)

### Commit Message Format
```
<type>: <short summary>

<detailed description>

<additional notes>
```
Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Quality Standards
1. **Tested code** - Ensure examples actually work
2. **Clear documentation** - Explain the "why" not just the "how"
3. **Complete examples** - Include setup, usage, and expected output
4. **Error handling** - Demonstrate proper error patterns
5. **Security awareness** - Never expose secrets

## When Creating New Content

### For Learning Materials
1. Choose correct category in `learning/`
2. Create descriptive subdirectory
3. Include comprehensive README with objectives, prerequisites, concepts, examples
4. Provide exercises if applicable
5. Link to related docs and POCs

### For POCs
1. Choose correct category in `pocs/`
2. Create dedicated directory with descriptive name
3. Follow POC directory structure template
4. Include working, tested code with comments
5. Document setup, usage, limitations, and future work
6. Provide `.env.example` if API keys needed

### For Documentation
1. Choose correct category in `docs/`
2. Write concisely with specific examples from codebase
3. Link to related learning materials and POCs
4. Keep up-to-date with code changes

## Common Pitfalls to Avoid

1. Don't create centralized dependency files - each POC is self-contained
2. Don't assume prior POCs exist - directories are mostly placeholders currently
3. Don't add generic "best practices" - document actual patterns from this codebase
4. Don't create production-grade code - focus on clarity and learning
5. Don't forget the README - it's the entry point for every directory

## Cost & Resource Awareness

Many examples use paid APIs. Always:
- Warn about API costs in README
- Suggest monitoring usage
- Provide cost estimation when possible
- Note free tier limitations

## AI Workflow Integration

This repository uses an intelligent workflow system to keep documentation synchronized with code changes.

### How It Works

1. **Post-commit hook** automatically detects changes and updates context files in `.ai-workflow/state/`
2. **Copilot Chat** reads these context files to understand recent repository changes
3. **Custom prompts** in `.github/prompts/` guide specific documentation tasks
4. **Conversation memory** preserves context across chat sessions (if git user.email is configured)

### Before Responding to ANY User Request

**CRITICAL**: Always check these context files FIRST:

1. **Recent Changes**: Read `#file:.ai-workflow/state/recent_changes.md` to see what was modified
2. **Documentation Status**: Check `#file:.ai-workflow/state/docs_status.md` for out-of-sync docs
3. **Last Sync**: Review `#file:.ai-workflow/state/last_sync.md` for timing context

### Response Priority

1. **Handle the user's immediate request FIRST** - Answer their question or complete their task
2. **Then append documentation suggestions** - If state files show pending updates, add a section at the END:
   ```markdown
   ## 📝 Documentation Update Suggestions
   
   Based on recent changes, consider updating:
   - [Specific file and reason]
   ```

### Custom Prompts Available

Users can reference these prompts for specific tasks:

- `#file:.github/prompts/menu.md` - List all available commands
- `#file:.github/prompts/update-docs.md` - Get documentation update suggestions
- `#file:.github/prompts/search-memory.md` - Search conversation history
- `#file:.github/prompts/summarize-changes.md` - Summarize recent commits
- `#file:.github/prompts/check-status.md` - Check documentation sync status

### Conflict Handling

If `.ai-workflow/state/docs_status.md` shows conflicts:
- **Warn the user** before suggesting edits to those files
- **Explain the conflict** (e.g., "This file was manually edited recently")
- **Ask for confirmation** before proceeding with changes
- **Never overwrite** without user approval

### Memory Preservation

When conversations involve important decisions or patterns:
- **Suggest saving**: "Would you like to save this conversation for future reference?"
- **Provide command**: `python .ai-workflow/scripts/capture_session.py`
- **Note**: Memory only works if `git config user.email` is set

### Workflow State Files

All state files are auto-generated and gitignored. Never edit these manually:
- `.ai-workflow/state/recent_changes.md` - What changed since last commit
- `.ai-workflow/state/docs_status.md` - Which docs need updates
- `.ai-workflow/state/last_sync.md` - Last processing timestamp
- `.ai-workflow/state/change_manifest.json` - Detailed change data
- `.ai-workflow/memory/` - Conversation history (private)

## Key Files to Reference

- `README.md` - Repository overview and navigation
- `CONTRIBUTING.md` - Detailed contribution guidelines and code standards
- `docs/guides/getting-started.md` - Prerequisites and first steps
- `docs/guides/setup.md` - Complete environment setup
- `.gitignore` - What not to commit (especially secrets)
- `.ai-workflow/README.md` - Workflow system documentation
