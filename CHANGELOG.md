# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-19

### Added
- **Direct .pages file creation** - Generate authentic Apple Pages documents without opening Pages
- **Pages default styles support** - Uses Pages' built-in Title, Heading, and Body styles
- **Markdown processing** - Converts markdown with proper heading hierarchy
- **Text file processing** - Converts plain text with automatic heading detection
- **Batch conversion** - Process multiple files at once
- **Deterministic output** - Same input always produces identical .pages files
- **Comprehensive testing** - Full test suite with deterministic verification
- **Cross-platform compatibility** - Works on any system with Python

### Technical Features
- **Pages '09 XML schema** - Compatible with modern Pages applications
- **Proper bundle structure** - Includes metadata, thumbnails, and version info
- **XML escaping** - Handles special characters correctly
- **Font and style mapping** - Maps to Pages' Helvetica-based typography
- **ZIP compression** - Efficient .pages file generation

### Development
- **Modern Python packaging** - Uses pyproject.toml with uv
- **Comprehensive documentation** - README, API reference, examples
- **Test automation** - Automated testing with hash verification
- **Code organization** - Clean separation of concerns

### Examples
- **Sample markdown file** - Demonstrates heading and formatting conversion
- **Sample text file** - Shows text processing capabilities
- **Demo scripts** - Interactive demonstrations

---

## Types of changes
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities