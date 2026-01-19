#!/usr/bin/env python3
"""
Demo script showing how to use the Pages Converter
"""

import os
import subprocess
from pathlib import Path

def demo_conversion():
    """Demonstrate the Pages Converter functionality"""

    print("Pages Converter Demo")
    print("=" * 50)

    # Check if test files exist
    test_files = [
        "examples/sample.md",
        "examples/sample.txt",
        "target/docx/test_document.docx",  # Our existing test file
    ]

    print("Available input files:")
    for file in test_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✓ {file} ({size} bytes)")
        else:
            print(f"  ✗ {file} (missing)")

    print("\nConverting files to Pages-compatible DOCX format...")

    # Convert markdown file
    if os.path.exists("examples/sample.md"):
        print("\n1. Converting Markdown to DOCX:")
        result = subprocess.run([
            "uv", "run", "python", "pages_converter.py",
            "--input", "examples/sample.md",
            "--output", "target/pages/sample_converted.docx"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("   ✓ Successfully converted markdown")
            if os.path.exists("target/pages/sample_converted.docx"):
                size = os.path.getsize("target/pages/sample_converted.docx")
                print(f"   📄 Output: target/pages/sample_converted.docx ({size} bytes)")
        else:
            print(f"   ✗ Conversion failed: {result.stderr}")

    # Convert text file
    if os.path.exists("examples/sample.txt"):
        print("\n2. Converting Text to DOCX:")
        result = subprocess.run([
            "uv", "run", "python", "pages_converter.py",
            "--input", "examples/sample.txt",
            "--output", "target/pages/sample_text.docx"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("   ✓ Successfully converted text")
            if os.path.exists("target/pages/sample_text.docx"):
                size = os.path.getsize("target/pages/sample_text.docx")
                print(f"   📄 Output: target/pages/sample_text.docx ({size} bytes)")
        else:
            print(f"   ✗ Conversion failed: {result.stderr}")

    # Show all generated files
    print("\n3. Generated Pages-compatible files:")
    pages_dir = Path("target/pages")
    if pages_dir.exists():
        docx_files = list(pages_dir.glob("*.docx"))
        if docx_files:
            for docx_file in sorted(docx_files):
                size = docx_file.stat().st_size
                print(f"   📄 {docx_file} ({size} bytes)")
        else:
            print("   No DOCX files found")

    print("\n4. How to open in Pages:")
    print("   • Open Pages application")
    print("   • File → Open")
    print("   • Select the .docx file from target/pages/")
    print("   • Pages will import it with full formatting")

    print("\n5. Batch conversion example:")
    print("   uv run python pages_converter.py --batch-input examples --batch-output target/pages")

    print("\n" + "=" * 50)
    print("✅ Demo complete!")
    print("\nThe DOCX files in target/pages/ can be opened directly in Pages")
    print("for full document editing and formatting capabilities.")

if __name__ == "__main__":
    demo_conversion()