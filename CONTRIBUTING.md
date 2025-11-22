# Contributing to AI Samples

Thank you for your interest in contributing! This guide will help you contribute effectively.

## Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest features or improvements
- 📝 Improve documentation
- 🎓 Add learning materials
- 🔬 Contribute POCs
- ✨ Improve existing code

## Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-samples.git
   cd ai-samples
   ```
3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Repository Structure

Understand the organization:
- `learning/` - Educational content and tutorials
- `docs/` - Documentation and guides
- `pocs/` - Proof-of-concept implementations

## Contribution Guidelines

### General Principles

1. **Quality over quantity** - Well-documented, working examples
2. **Clarity** - Clear explanations and comments
3. **Completeness** - Include setup instructions and examples
4. **Testing** - Ensure code works as documented
5. **Security** - Never commit API keys or secrets

### Code Standards

#### Python
- Follow PEP 8
- Use type hints where applicable
- Include docstrings
- Use meaningful variable names

```python
def generate_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """
    Generate embedding for the given text.
    
    Args:
        text: The text to embed
        model: The embedding model to use
        
    Returns:
        List of floats representing the embedding
    """
    # Implementation
```

#### JavaScript/TypeScript
- Use ESLint
- Prefer TypeScript for type safety
- Use async/await over promises
- Include JSDoc comments

```typescript
/**
 * Generate embedding for the given text
 * @param text - The text to embed
 * @param model - The embedding model to use
 * @returns Promise resolving to the embedding vector
 */
async function generateEmbedding(
  text: string, 
  model: string = "text-embedding-3-small"
): Promise<number[]> {
  // Implementation
}
```

#### Rust
- Use `cargo fmt`
- Use `cargo clippy`
- Include documentation comments
- Follow Rust conventions

```rust
/// Generate embedding for the given text
/// 
/// # Arguments
/// * `text` - The text to embed
/// * `model` - The embedding model to use
/// 
/// # Returns
/// Vector of f32 values representing the embedding
pub async fn generate_embedding(text: &str, model: &str) -> Result<Vec<f32>> {
    // Implementation
}
```

### Adding Learning Materials

1. **Choose the right category** - fundamentals, llm-workflows, embeddings, etc.
2. **Create a descriptive subdirectory**
3. **Include a comprehensive README**:
   - Learning objectives
   - Prerequisites
   - Concepts explained
   - Code examples
   - Exercises (optional)
   - Further resources

Example structure:
```
learning/topic/subtopic/
├── README.md
├── 01-introduction.md
├── 02-basic-example.py
├── 03-advanced-example.py
└── exercises/
    ├── exercise-1.md
    └── solution-1.py
```

### Adding Documentation

1. **Choose the right category** - guides, best-practices, architecture, etc.
2. **Write clearly and concisely**
3. **Include examples**
4. **Link to related resources**
5. **Keep it up-to-date**

### Adding POCs

1. **Create a descriptive directory** in the appropriate category
2. **Include a comprehensive README** with:
   - Overview and objectives
   - Prerequisites
   - Setup instructions
   - Usage examples
   - Implementation notes
   - Limitations
   - Future improvements

3. **Provide working code**:
   - Well-commented
   - Follows best practices
   - Includes error handling
   - Has example usage

4. **Example POC structure**:
```
pocs/category/poc-name/
├── README.md
├── .env.example        # Example environment variables
├── requirements.txt    # Python dependencies
├── package.json        # Node dependencies
├── src/
│   └── main.py        # Main implementation
├── examples/
│   └── basic-usage.py # Usage example
└── tests/             # Tests (if applicable)
```

### Environment Variables

- Never commit actual API keys
- Include `.env.example` with dummy values:
```bash
# .env.example
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Documentation Standards

- Use Markdown
- Include code blocks with language specification
- Add links to external resources
- Use headings for structure
- Include a table of contents for long documents

### Commit Messages

Write clear, descriptive commit messages:
```
Add RAG POC with re-ranking

- Implement basic RAG pipeline
- Add re-ranking with cross-encoder
- Include example usage
- Add comprehensive README
```

Format:
```
<type>: <short summary>

<detailed description>

<additional notes>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Submitting Changes

1. **Test your changes** thoroughly
2. **Update documentation** if needed
3. **Commit your changes** with clear messages
4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Create a Pull Request**:
   - Describe what you changed and why
   - Link to any related issues
   - Include screenshots for UI changes
   - List any breaking changes

## Pull Request Guidelines

- Keep PRs focused on a single change
- Update relevant documentation
- Ensure all examples work
- Respond to review feedback
- Be patient and respectful

## Code Review Process

1. Maintainers will review your PR
2. They may request changes
3. Make requested updates
4. Once approved, your PR will be merged

## Reporting Issues

When reporting bugs or issues:

1. **Check existing issues** first
2. **Use a descriptive title**
3. **Provide details**:
   - What you expected
   - What actually happened
   - Steps to reproduce
   - Your environment (OS, language version, etc.)
   - Error messages or logs

## Suggesting Features

When suggesting new features:

1. **Check existing suggestions**
2. **Describe the use case**
3. **Explain the benefit**
4. **Consider alternatives**
5. **Offer to implement it**

## Questions?

- Open a GitHub Discussion
- Check existing documentation
- Review similar implementations

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Give constructive feedback
- Assume good intentions
- No harassment or discrimination

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Recognition

Contributors will be:
- Listed in the repository contributors
- Acknowledged in release notes
- Appreciated for their work! 🙌

Thank you for contributing to AI Samples!
