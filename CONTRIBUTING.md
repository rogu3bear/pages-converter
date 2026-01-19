# Contributing to Pages Converter

Thank you for your interest in contributing to Pages Converter! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Set up development environment**:
   ```bash
   git clone https://github.com/yourusername/pages-converter.git
   cd pages-converter
   uv sync
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
5. **Run tests** to ensure everything works:
   ```bash
   uv run python tests/test_converter.py
   ```

## 📝 Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write descriptive variable and function names
- Keep functions focused on single responsibilities

### Testing

- **Write tests** for all new functionality
- **Run the full test suite** before submitting:
  ```bash
  uv run python tests/test_converter.py
  ```
- **Ensure deterministic output** for converter functions
- **Test edge cases** and error conditions

### Documentation

- **Update README.md** for new features
- **Add docstrings** to all public functions
- **Update CHANGELOG.md** with changes
- **Provide usage examples** for new functionality

## 🐛 Reporting Issues

### Bug Reports

When reporting bugs, please include:

1. **Clear title** describing the issue
2. **Steps to reproduce** the problem
3. **Expected behavior** vs actual behavior
4. **Environment details**:
   - Python version
   - Operating system
   - Input files (if applicable)
5. **Error messages** and stack traces

### Feature Requests

For feature requests, please:

1. **Describe the problem** you're trying to solve
2. **Explain why** the feature would be valuable
3. **Provide examples** of how it would work
4. **Consider alternatives** you've thought about

## 🔧 Making Changes

### Adding New Features

1. **Discuss first** - Open an issue to discuss the feature before implementing
2. **Write tests first** - Implement tests before the feature code
3. **Keep it simple** - Start with minimal viable implementation
4. **Update documentation** - README, docstrings, and examples

### Code Changes

1. **Make small, focused commits** with clear messages
2. **Test thoroughly** - Ensure all existing tests pass
3. **Update dependencies** if needed (update pyproject.toml)
4. **Follow the existing code structure**

### File Formats

When adding support for new input formats:

1. **Extend the PagesConverter class** with new methods
2. **Add format detection** in convert_file()
3. **Implement proper XML generation** for Pages compatibility
4. **Add comprehensive tests** for the new format

## 🔍 Code Review Process

### For Contributors

1. **Self-review** your code before submitting
2. **Run all tests** and ensure they pass
3. **Test manually** with various input files
4. **Update documentation** as needed

### For Maintainers

1. **Review code** for style, correctness, and security
2. **Test the changes** thoroughly
3. **Check for breaking changes** and version implications
4. **Ensure documentation** is complete and accurate

## 🏷️ Commit Messages

Use clear, descriptive commit messages:

```
feat: add support for YAML input format
fix: handle empty markdown files gracefully
docs: update README with new batch conversion examples
test: add comprehensive edge case testing
```

## 📚 Resources

### Apple Pages Documentation
- Pages '09 XML Schema (legacy but still compatible)
- Pages file format structure
- Apple Developer Documentation

### Python Development
- PEP 8 Style Guide
- Type Hints (PEP 484)
- Testing with unittest/pytest

### Git Workflow
- Feature branch workflow
- Pull request best practices
- Semantic versioning

## 🙏 Recognition

Contributors will be acknowledged in:
- CHANGELOG.md for their changes
- GitHub contributors list
- Project documentation

Thank you for contributing to Pages Converter! 🎯📄