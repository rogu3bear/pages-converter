#!/usr/bin/env python3
"""
Pages Converter - Direct .pages file creation

This script creates actual Apple Pages (.pages) files by generating Pages '09
compatible XML format and packaging it properly. No manual Pages opening required.

Usage:
    python pages_converter.py --input examples/sample.md --output target/pages/converted.pages
    python pages_converter.py --input examples/sample.txt --output target/pages/text.pages
"""

import argparse
import os
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any
import markdown
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE


class PagesConverter:
    """Deterministic converter for creating Pages-compatible documents"""

    def __init__(self, target_dir: str = "target"):
        self.target_dir = Path(target_dir)
        self.target_dir.mkdir(exist_ok=True)

    def convert_file(self, input_path: str, output_path: str, **options) -> bool:
        """
        Convert input file to actual .pages format.

        Args:
            input_path: Path to input file (txt, md, etc.)
            output_path: Path for output .pages file
            options: Conversion options

        Returns:
            True if successful, False otherwise
        """
        input_path = Path(input_path)
        output_path = Path(output_path)

        if not input_path.exists():
            print(f"Error: Input file {input_path} does not exist")
            return False

        # Read input content
        content = self._read_input_file(input_path)

        # Generate Pages '09 XML content
        if input_path.suffix.lower() == '.md':
            xml_content = self._content_to_pages_xml(content, 'markdown')
        elif input_path.suffix.lower() == '.txt':
            xml_content = self._content_to_pages_xml(content, 'text')
        else:
            xml_content = self._content_to_pages_xml(content, 'text')

        # Create .pages bundle
        success = self._create_pages_bundle(xml_content, output_path)

        if success:
            print(f"✓ Converted {input_path} → {output_path}")
        return success

    def _read_input_file(self, input_path: Path) -> str:
        """Read input file with deterministic encoding detection"""
        # Try UTF-8 first, fallback to latin-1 for deterministic behavior
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(input_path, 'r', encoding='latin-1') as f:
                return f.read()


    def _content_to_pages_xml(self, content: str, content_type: str) -> str:
        """Convert content to Pages '09 compatible XML format"""
        if content_type == 'markdown':
            return self._markdown_to_pages_xml(content)
        else:
            return self._text_to_pages_xml(content)

    def _text_to_pages_xml(self, text_content: str) -> str:
        """Convert plain text to Pages XML with default styles"""
        # Split into paragraphs
        paragraphs = [p.strip() for p in text_content.split('\n\n') if p.strip()]

        # Generate Pages XML structure using Pages default styles
        xml_parts = []

        # XML header and root with Pages default styles
        xml_parts.append('''<?xml version="1.0" encoding="UTF-8"?>
<sl:document xmlns:sl="http://developer.apple.com/namespaces/sl" version="72028102400000000">
  <sl:metadata>
    <sl:author>Pages Converter</sl:author>
    <sl:creation-date>2024-01-01T12:00:00Z</sl:creation-date>
  </sl:metadata>
  <sl:styles>
    <sl:paragraph-style sfa:ID="paragraph-style-0" sf:name="Body">
      <sl:font sfa:fontName="Helvetica" sfa:fontSize="12"/>
    </sl:paragraph-style>
    <sl:paragraph-style sfa:ID="paragraph-style-1" sf:name="Heading">
      <sl:font sfa:fontName="Helvetica-Bold" sfa:fontSize="18"/>
    </sl:paragraph-style>
  </sl:styles>
  <sl:body>
    <sl:section>
      <sl:layout-style-ref sfa:IDref="layout-style-0"/>
''')

        # Add paragraphs using Pages default styles
        for i, para in enumerate(paragraphs):
            # Check for headings (simple heuristic)
            if para.isupper() and len(para) < 100:
                # Use Pages "Heading" style for ALL CAPS text
                xml_parts.append(f'''      <sl:p sf:style="paragraph-style-1">
        <sf:text>{self._escape_xml(para)}</sf:text>
      </sl:p>''')
            else:
                # Use Pages "Body" style for regular text
                xml_parts.append(f'''      <sl:p sf:style="paragraph-style-0">
        <sf:text>{self._escape_xml(para)}</sf:text>
      </sl:p>''')

        # Close XML structure
        xml_parts.append('''    </sl:section>
  </sl:body>
</sl:document>''')

        return '\n'.join(xml_parts)

    def _markdown_to_pages_xml(self, markdown_content: str) -> str:
        """Convert markdown to Pages XML using default styles"""
        import markdown

        # Convert markdown to HTML, then parse
        html = markdown.markdown(markdown_content)

        # Simple HTML to Pages XML conversion using default styles
        xml_parts = []

        # XML header and root with Pages default styles defined
        xml_parts.append('''<?xml version="1.0" encoding="UTF-8"?>
<sl:document xmlns:sl="http://developer.apple.com/namespaces/sl" version="72028102400000000">
  <sl:metadata>
    <sl:author>Pages Converter</sl:author>
    <sl:creation-date>2024-01-01T12:00:00Z</sl:creation-date>
  </sl:metadata>
  <sl:styles>
    <sl:paragraph-style sfa:ID="paragraph-style-0" sf:name="Body">
      <sl:font sfa:fontName="Helvetica" sfa:fontSize="12"/>
    </sl:paragraph-style>
    <sl:paragraph-style sfa:ID="paragraph-style-1" sf:name="Heading">
      <sl:font sfa:fontName="Helvetica-Bold" sfa:fontSize="18"/>
    </sl:paragraph-style>
    <sl:paragraph-style sfa:ID="paragraph-style-2" sf:name="Title">
      <sl:font sfa:fontName="Helvetica-Bold" sfa:fontSize="24"/>
    </sl:paragraph-style>
  </sl:styles>
  <sl:body>
    <sl:section>
      <sl:layout-style-ref sfa:IDref="layout-style-0"/>
''')

        # Parse HTML and convert to Pages XML using default styles
        lines = html.replace('<p>', '').replace('</p>', '\n').replace('<br>', '\n')
        lines = lines.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith('<h1>'):
                heading = line.replace('<h1>', '').replace('</h1>', '')
                # Use Pages "Title" style for H1
                xml_parts.append(f'''      <sl:p sf:style="paragraph-style-2">
        <sf:text>{self._escape_xml(heading)}</sf:text>
      </sl:p>''')
            elif line.startswith('<h2>') or line.startswith('<h3>'):
                heading = line.replace('<h2>', '').replace('</h2>', '').replace('<h3>', '').replace('</h3>', '')
                # Use Pages "Heading" style for H2/H3
                xml_parts.append(f'''      <sl:p sf:style="paragraph-style-1">
        <sf:text>{self._escape_xml(heading)}</sf:text>
      </sl:p>''')
            elif line.startswith('<strong>') or line.startswith('<b>'):
                text = line.replace('<strong>', '').replace('</strong>', '').replace('<b>', '').replace('</b>', '')
                # Bold text using Pages default body style
                xml_parts.append('''      <sl:p sf:style="paragraph-style-0">
        <sf:text>''' + self._escape_xml(text) + '''</sf:text>
      </sl:p>''')
            elif line.startswith('<li>'):
                text = line.replace('<li>', '').replace('</li>', '').replace('<ul>', '').replace('</ul>', '').replace('<ol>', '').replace('</ol>', '')
                # Bullet list using Pages default body style
                xml_parts.append(f'''      <sl:p sf:style="paragraph-style-0">
        <sf:text>• {self._escape_xml(text)}</sf:text>
      </sl:p>''')
            else:
                # Regular paragraph
                clean_text = line.replace('<', '').replace('>', '').strip()
                if clean_text:
                    # Use Pages default body text style
                    xml_parts.append(f'''      <sl:p sf:style="paragraph-style-0">
        <sf:text>{self._escape_xml(clean_text)}</sf:text>
      </sl:p>''')

        # Close XML structure
        xml_parts.append('''    </sl:section>
  </sl:body>
</sl:document>''')

        return '\n'.join(xml_parts)

    def _escape_xml(self, text: str) -> str:
        """Escape XML special characters"""
        return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&apos;'))

    def _create_pages_bundle(self, xml_content: str, output_path: Path) -> bool:
        """Create a .pages bundle (ZIP archive) with the XML content"""
        import zipfile
        import tempfile
        from datetime import datetime

        # Create temporary directory for bundle structure
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create index.xml
            index_xml_path = temp_path / "index.xml"
            with open(index_xml_path, 'w', encoding='utf-8') as f:
                f.write(xml_content)

            # Create buildVersionHistory.plist
            plist_content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>BuildVersion</key>
    <string>192</string>
    <key>ProductVersion</key>
    <string>4.0</string>
</dict>
</plist>'''
            plist_path = temp_path / "buildVersionHistory.plist"
            with open(plist_path, 'w', encoding='utf-8') as f:
                f.write(plist_content)

            # Create QuickLook thumbnail directory and dummy thumbnail
            ql_dir = temp_path / "QuickLook"
            ql_dir.mkdir()
            thumbnail_path = ql_dir / "Thumbnail.jpg"
            # Create a minimal 1x1 pixel JPEG thumbnail
            with open(thumbnail_path, 'wb') as f:
                # Minimal JPEG header for 1x1 black pixel
                f.write(bytes.fromhex('FFD8FFE000104A46494600010100000100010000FFDB004300080606070605080707070909080A0C140D0C0B0B0C1912130F141D1A1F1E1D1A1C1C20242E2720222C231C1C2837292C30313434341F27393D38323C2E333432FF C00011080001000103012200021101031101FFC4001500010100000000000000000000000000000008FFC40014100100000000000000000000000000000000FFC40014110100000000000000000000000000000000FFC40014120100000000000000000000000000000000FFC40014130100000000000000000000000000000000FFC0 0011080001000103011100021101031101FFDA000C03010002110311003F00B2C0FFD9'))

            # ZIP everything into .pages file
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                # Add files to ZIP
                for file_path in temp_path.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(temp_path)
                        zf.write(file_path, arcname)

        return output_path.exists()

    def _create_base_document(self) -> Document:
        """Create a base DOCX document with deterministic settings"""
        from datetime import datetime

        doc = Document()

        # Set document properties (deterministic)
        doc.core_properties.title = "Converted Document"
        doc.core_properties.author = "Pages Converter"
        # Use fixed datetime for deterministic output
        doc.core_properties.created = datetime(2024, 1, 1, 12, 0, 0)

        # Set default font and size (deterministic)
        style = doc.styles['Normal']
        font = style.font
        font.name = 'Helvetica'
        font.size = Pt(12)

        return doc

    def batch_convert(self, input_dir: str, output_dir: str, pattern: str = "*") -> int:
        """
        Batch convert all files in input directory to output directory.

        Returns number of files converted successfully.
        """
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)

        if not input_dir.exists():
            print(f"Error: Input directory {input_dir} does not exist")
            return 0

        converted = 0

        # Find all files matching pattern
        for input_file in input_dir.glob(pattern):
            if input_file.is_file():
                # Generate deterministic output path
                relative_path = input_file.relative_to(input_dir)
                output_file = output_dir / relative_path.with_suffix('.pages')
                output_file.parent.mkdir(parents=True, exist_ok=True)

                if self.convert_file(str(input_file), str(output_file)):
                    converted += 1

        return converted

    def get_file_hash(self, file_path: str) -> str:
        """Get deterministic hash of file for verification"""
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()[:16]


def main():
    parser = argparse.ArgumentParser(
        description="Convert files to Pages-compatible DOCX format"
    )
    parser.add_argument('--input', '-i', help='Input file to convert')
    parser.add_argument('--output', '-o', help='Output .pages file')
    parser.add_argument('--batch-input', help='Input directory for batch conversion')
    parser.add_argument('--batch-output', help='Output directory for batch conversion')
    parser.add_argument('--verify', help='Verify output file hash')

def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(
        description="Convert files to Pages-compatible .pages format"
    )
    parser.add_argument('--input', '-i', help='Input file to convert')
    parser.add_argument('--output', '-o', help='Output .pages file')
    parser.add_argument('--batch-input', help='Input directory for batch conversion')
    parser.add_argument('--batch-output', help='Output directory for batch conversion')
    parser.add_argument('--verify', help='Verify output file hash')

    args = parser.parse_args()

    converter = PagesConverter()

    if args.verify:
        # Verify file integrity
        if os.path.exists(args.verify):
            hash_value = converter.get_file_hash(args.verify)
            print(f"File hash: {hash_value}")
        else:
            print(f"File {args.verify} does not exist")

    elif args.batch_input and args.batch_output:
        # Batch conversion
        print(f"Batch converting from {args.batch_input} to {args.batch_output}")
        converted = converter.batch_convert(args.batch_input, args.batch_output)
        print(f"Converted {converted} files")

    elif args.input and args.output:
        # Single file conversion
        success = converter.convert_file(args.input, args.output)
        if success:
            # Show hash for verification
            hash_value = converter.get_file_hash(args.output)
            print(f"Output hash: {hash_value}")
        else:
            exit(1)

    else:
        parser.print_help()
        print("\nExamples:")
        print("  pages-converter --input examples/sample.md --output output.pages")
        print("  pages-converter --batch-input examples --batch-output ./pages")


if __name__ == "__main__":
    main()