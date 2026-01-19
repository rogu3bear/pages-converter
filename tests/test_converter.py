#!/usr/bin/env python3
"""
Test script for Pages Converter deterministic behavior
"""

import os
import subprocess
import tempfile
from pathlib import Path

def test_deterministic_conversion():
    """Test that the same input produces the same output hash"""
    print("Testing deterministic conversion...")

    # Test with our sample files
    test_cases = [
        ("examples/sample.md", "target/pages/test_md_output.pages"),
        ("examples/sample.txt", "target/pages/test_txt_output.pages"),
    ]

    hashes = {}

    for input_file, output_file in test_cases:
        if not os.path.exists(input_file):
            print(f"⚠️  Skipping {input_file} - file not found")
            continue

        # Convert file using direct Python import
        result = subprocess.run([
            "uv", "run", "python", "-c",
            f"from pages_converter import PagesConverter; c = PagesConverter(); c.convert_file('{input_file}', '{output_file}')"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            # Get hash for verification
            hash_result = subprocess.run([
                "uv", "run", "python", "-c",
                f"from pages_converter import PagesConverter; c = PagesConverter(); print(f'File hash: {{c.get_file_hash(\"{output_file}\")}}')"
            ], capture_output=True, text=True)

            if hash_result.returncode == 0:
                file_hash = hash_result.stdout.strip().split(": ")[1]
                hashes[output_file] = file_hash
                print(f"✓ {input_file} → {output_file}")
                print(f"  Hash: {file_hash}")
            else:
                print(f"✗ Failed to get hash for {output_file}")
        else:
            print(f"✗ Failed to convert {input_file}: {result.stderr}")

    # Test determinism - run conversion again and verify same hash
    print("\nTesting determinism (same input = same output)...")

    for input_file, output_file in test_cases:
        if not os.path.exists(input_file):
            continue

        # Backup original
        backup_file = output_file + ".backup"
        if os.path.exists(output_file):
            os.rename(output_file, backup_file)

        # Convert again
        result = subprocess.run([
            "python", "pages_converter.py",
            "--input", input_file,
            "--output", output_file
        ], capture_output=True, text=True)

        if result.returncode == 0:
            hash_result = subprocess.run([
                "uv", "run", "python", "-c",
                f"from pages_converter import PagesConverter; c = PagesConverter(); print(f'File hash: {{c.get_file_hash(\"{output_file}\")}}')"
            ], capture_output=True, text=True)

            if hash_result.returncode == 0:
                new_hash = hash_result.stdout.strip().split(": ")[1]
                original_hash = hashes.get(output_file)

                if original_hash and new_hash == original_hash:
                    print(f"✓ Deterministic: {output_file} hash matches")
                else:
                    print(f"✗ Non-deterministic: {output_file} hash changed")
                    print(f"  Original: {original_hash}")
                    print(f"  New: {new_hash}")

        # Restore backup
        if os.path.exists(backup_file):
            os.rename(backup_file, output_file)

    return True

def test_batch_conversion():
    """Test batch conversion functionality"""
    print("\nTesting batch conversion...")

    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Copy our test files
        import shutil
        shutil.copy("examples/sample.md", temp_path / "test1.md")
        shutil.copy("examples/sample.txt", temp_path / "test2.txt")

        # Create output directory
        output_dir = temp_path / "output"
        output_dir.mkdir()

        # Run batch conversion
        result = subprocess.run([
            "uv", "run", "python", "-c",
            f"from pages_converter import PagesConverter; c = PagesConverter(); print(c.batch_convert('{temp_path}', '{output_dir}'))"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            # Check output files
            output_files = list(output_dir.glob("*.pages"))
            print(f"✓ Batch conversion created {len(output_files)} files:")
            for f in output_files:
                print(f"  - {f.name}")
        else:
            print(f"✗ Batch conversion failed: {result.stderr}")

    return True

def main():
    print("Pages Converter Test Suite")
    print("=" * 40)

    if not Path("examples/sample.md").exists():
        print("❌ Test files not found. Run from project root directory.")
        return False

    try:
        test_deterministic_conversion()
        test_batch_conversion()

        print("\n" + "=" * 40)
        print("✅ All tests completed!")
        print("\nTo use the converter:")
        print("  uv run python pages_converter.py --input examples/sample.md --output target/pages/output.pages")
        print("  uv run python pages_converter.py --batch-input examples --batch-output target/pages")

        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)