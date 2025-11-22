# Getting Started

Welcome to the AI Samples repository! This guide will help you get started with exploring and using the samples.

## What's in This Repository?

This repository contains:
- **Learning Materials** - Educational content and tutorials
- **Documentation** - Comprehensive guides and references
- **Proof of Concepts** - Working implementations and examples

## Quick Navigation

- 📚 [Learning Resources](../learning/README.md) - Start here if you're learning
- 📖 [Documentation](../README.md) - Guides and references
- 🔬 [POCs](../pocs/README.md) - Working examples and implementations

## Prerequisites

### Basic Requirements
- Programming knowledge in at least one of: Python, JavaScript/TypeScript, or Rust
- Understanding of APIs and HTTP requests
- Basic command line familiarity
- Git for version control

### Recommended Knowledge
- Basic understanding of machine learning concepts
- Familiarity with asynchronous programming
- JSON and data structures
- Environment variables and configuration

## Setting Up Your Environment

### 1. Clone the Repository
```bash
git clone https://github.com/sumitparakh/ai-samples.git
cd ai-samples
```

### 2. Choose Your Path

#### For Learning
Navigate to the [learning](../learning/README.md) directory and choose a topic:
- Start with [Fundamentals](../learning/fundamentals/README.md) if you're new
- Jump to specific topics if you have experience

#### For Building
Head to the [POCs](../pocs/README.md) directory:
- Find a relevant POC
- Follow its specific setup instructions
- Experiment and modify

#### For Reference
Check the [docs](../README.md) directory:
- Read guides for specific tasks
- Review best practices
- Consult API references

### 3. API Keys and Configuration

Many examples require API keys from:
- **OpenAI** - For GPT models
- **Anthropic** - For Claude models
- **Vector Databases** - Pinecone, Weaviate, etc.

Create a `.env` file (never commit this!):
```bash
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
# Add other keys as needed
```

### 4. Language-Specific Setup

#### Python
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt  # In specific POC directories
```

#### JavaScript/TypeScript
```bash
npm install  # In specific POC directories
# or
yarn install
```

#### Rust
```bash
cargo build  # In specific POC directories
```

## Your First Steps

1. **Explore the Structure** - Browse the directories to understand the organization
2. **Read a Learning Module** - Pick a topic that interests you
3. **Run a Simple POC** - Start with a basic example
4. **Experiment** - Modify and adapt the code
5. **Build Something** - Create your own project using the patterns

## Getting Help

- **Documentation** - Check the [docs](../README.md) directory
- **Troubleshooting** - See [troubleshooting guide](../troubleshooting/README.md)
- **Issues** - Open a GitHub issue for bugs or questions
- **Discussions** - Use GitHub Discussions for questions

## Best Practices

1. **Never commit API keys** - Use environment variables
2. **Start simple** - Begin with basic examples
3. **Read the docs** - Each POC has its own README
4. **Test incrementally** - Make small changes and test
5. **Monitor costs** - Be aware of API usage

## Next Steps

- Explore the [Learning](../learning/README.md) section
- Review [Best Practices](../best-practices/README.md)
- Try a [POC](../pocs/README.md)
- Read the [Architecture](../architecture/README.md) patterns

## Contributing

Want to contribute? See our [Contributing Guide](../../CONTRIBUTING.md)!

Happy coding! 🚀
