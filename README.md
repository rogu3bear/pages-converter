# Pages Converter

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A powerful command-line tool that converts text and Markdown files directly into Apple Pages (`.pages`) documents with proper formatting and Pages' built-in default styles.

## ✨ Features

- **Direct .pages Creation** - Generate authentic Apple Pages documents without opening Pages
- **Pages Default Styles** - Uses Pages' built-in Title, Heading, and Body styles for native appearance
- **Multiple Input Formats** - Supports Markdown and plain text files
- **Deterministic Output** - Same input always produces identical .pages files
- **Batch Processing** - Convert multiple files at once
- **Cross-Platform** - Works on any system with Python

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pages-converter.git
cd pages-converter

# Install with uv (recommended)
uv sync

# Or with pip
pip install -e .
```

### Basic Usage

```bash
# Convert Markdown to Pages
uv run python pages_converter.py --input document.md --output document.pages

# Convert text file to Pages
uv run python pages_converter.py --input notes.txt --output notes.pages

# Batch convert all files in a directory
uv run python pages_converter.py --batch-input ./docs --batch-output ./output
```

## 📖 Usage Examples

### Single File Conversion

```bash
# Markdown with headings and formatting
uv run python pages_converter.py --input README.md --output presentation.pages

# Plain text document
uv run python pages_converter.py --input manuscript.txt --output manuscript.pages
```

### Batch Processing

```bash
# Convert all markdown files in docs/ to pages/
uv run python pages_converter.py --batch-input docs --batch-output pages

# Convert all text files
uv run python pages_converter.py --batch-input ./notes --batch-output ./pages
```

### Advanced Options

```bash
# Verify file integrity
uv run python pages_converter.py --verify output.pages

# Get help
uv run python pages_converter.py --help
```

## 🎯 How It Works

### Input Processing

**Markdown Files:**
- `# Heading 1` → Pages "Title" style (Helvetica Bold, 24pt)
- `## Heading 2` → Pages "Heading" style (Helvetica Bold, 18pt)
- `### Heading 3` → Pages "Heading" style (Helvetica Bold, 18pt)
- Regular text → Pages "Body" style (Helvetica, 12pt)

**Text Files:**
- ALL CAPS text → Pages "Heading" style
- Regular paragraphs → Pages "Body" style

### Output Format

Creates authentic `.pages` documents with:
- **Proper XML structure** using Pages '09 schema
- **Pages default styles** (Title, Heading, Body)
- **Complete bundle** with metadata and thumbnails
- **ZIP compression** for efficient storage

## 🏗️ Architecture

```
pages-converter/
├── pages_converter.py      # Main conversion engine
├── tests/
│   └── test_converter.py   # Comprehensive test suite
├── scripts/
│   └── demo_converter.py   # Usage demonstrations
├── examples/
│   ├── sample.md          # Markdown example
│   └── sample.txt         # Text example
└── docs/                  # Documentation
```

## 🔧 Technical Details

### Dependencies

- `python-docx` - For DOCX reference (not used in core conversion)
- `markdown` - For Markdown to HTML preprocessing
- `uv` - Modern Python package management

### Style Mapping

| Input | Pages Style | Font | Size |
|-------|-------------|------|------|
| H1/Markdown # | Title | Helvetica Bold | 24pt |
| H2/H3 Markdown | Heading | Helvetica Bold | 18pt |
| ALL CAPS text | Heading | Helvetica Bold | 18pt |
| Body text | Body | Helvetica | 12pt |

### File Structure

Generated `.pages` files contain:
- `index.xml` - Document content and structure
- `buildVersionHistory.plist` - Compatibility metadata
- `QuickLook/Thumbnail.jpg` - Preview thumbnail

## 🧪 Testing

Run the comprehensive test suite:

```bash
uv run python tests/test_converter.py
```

Tests verify:
- ✅ Deterministic output (same input = same file hash)
- ✅ Proper XML generation
- ✅ Valid .pages bundle creation
- ✅ Batch processing functionality

## 📚 API Reference

### PagesConverter Class

```python
from pages_converter import PagesConverter

converter = PagesConverter()
success = converter.convert_file("input.md", "output.pages")
```

### Methods

- `convert_file(input_path, output_path)` - Convert single file
- `batch_convert(input_dir, output_dir)` - Convert directory
- `get_file_hash(file_path)` - Get deterministic file hash

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

### Development Setup

```bash
# Clone and setup
git clone https://github.com/yourusername/pages-converter.git
cd pages-converter
uv sync

# Run tests
uv run python tests/test_converter.py

# Format code
uv run black .
uv run isort .
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on extensive research into Apple Pages file formats
- Uses Pages '09 XML schema for compatibility
- Inspired by the need for programmatic Pages document creation

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/pages-converter/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/pages-converter/discussions)

---

**Convert your documents to Pages format programmatically!** 🎯📄✨