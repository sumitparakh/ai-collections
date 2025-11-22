# Development Setup

Complete guide for setting up your development environment for AI projects.

## Prerequisites

### Required Tools
- Git
- Code editor (VS Code, PyCharm, or similar)
- Terminal/Command line
- Package managers (pip, npm, cargo)

### Language Runtimes

#### Python
- Python 3.8 or higher
- pip package manager
- virtualenv or venv

```bash
# Check version
python --version

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

#### Node.js/TypeScript
- Node.js 16 or higher
- npm or yarn

```bash
# Check versions
node --version
npm --version

# Install dependencies
npm install
```

#### Rust
- Rust 1.70 or higher
- Cargo package manager

```bash
# Check version
rustc --version
cargo --version
```

## API Keys Setup

### Getting API Keys

1. **OpenAI**
   - Visit https://platform.openai.com/api-keys
   - Create an account or sign in
   - Generate a new API key
   - Note: Keep this secure!

2. **Anthropic**
   - Visit https://console.anthropic.com/
   - Sign up for access
   - Generate API key

3. **Vector Databases**
   - Pinecone: https://www.pinecone.io/
   - Weaviate: https://weaviate.io/
   - Others as needed

### Environment Variables

Create a `.env` file in the root directory:

```bash
# LLM Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Vector Databases
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=...
WEAVIATE_URL=...
WEAVIATE_API_KEY=...

# Other services
GOOGLE_API_KEY=...
```

**Important**: Add `.env` to `.gitignore`!

```bash
# .gitignore
.env
.env.local
*.env
```

## IDE Configuration

### VS Code

Recommended extensions:
- Python
- Pylance
- ESLint
- Prettier
- Rust Analyzer (for Rust)

Settings (`.vscode/settings.json`):
```json
{
  "python.linting.enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "typescript.preferences.importModuleSpecifier": "relative"
}
```

### PyCharm

1. Configure Python interpreter
2. Enable environment variables from `.env`
3. Set up code style preferences

## Project Structure

Typical project structure:
```
project-name/
├── .env                 # Environment variables (gitignored)
├── .gitignore          # Git ignore file
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies
├── package.json        # Node dependencies
├── Cargo.toml         # Rust dependencies
├── src/               # Source code
├── tests/             # Test files
└── examples/          # Usage examples
```

## Installing Dependencies

### Python Projects
```bash
# Install from requirements.txt
pip install -r requirements.txt

# Or install common packages
pip install openai anthropic langchain chromadb
pip install python-dotenv  # For .env files
```

### Node.js Projects
```bash
# Install from package.json
npm install

# Or install common packages
npm install openai @anthropic-ai/sdk langchain
npm install dotenv  # For .env files
```

### Rust Projects
```bash
# Build project (installs dependencies)
cargo build

# Add common dependencies
cargo add tokio serde serde_json reqwest
```

## Testing Your Setup

### Python Test
```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
print(f"API key loaded: {api_key[:10]}..." if api_key else "No API key found")
```

### Node.js Test
```javascript
import dotenv from 'dotenv';
dotenv.config();

const apiKey = process.env.OPENAI_API_KEY;
console.log(apiKey ? `API key loaded: ${apiKey.substring(0, 10)}...` : 'No API key found');
```

## Common Issues

### API Key Not Found
- Check `.env` file exists
- Verify environment variables are loaded
- Check for typos in variable names

### Module Not Found
- Ensure virtual environment is activated (Python)
- Run `npm install` or `pip install -r requirements.txt`
- Check import paths

### Version Conflicts
- Update to recommended versions
- Use virtual environments to isolate projects
- Check compatibility in documentation

## Development Workflow

1. **Start**: Activate virtual environment
2. **Code**: Write and test incrementally
3. **Test**: Run tests frequently
4. **Commit**: Commit working changes
5. **Document**: Update README and comments

## Best Practices

1. **Use version control** - Commit often
2. **Never commit secrets** - Use `.env` files
3. **Test incrementally** - Don't write too much before testing
4. **Read error messages** - They usually tell you what's wrong
5. **Monitor API usage** - Set up billing alerts

## Next Steps

- Review [Best Practices](../best-practices/README.md)
- Explore [Learning Resources](../../learning/README.md)
- Try running a [POC](../../pocs/README.md)

## Getting Help

If you encounter issues:
1. Check the [Troubleshooting Guide](../troubleshooting/README.md)
2. Search existing GitHub issues
3. Create a new issue with details
