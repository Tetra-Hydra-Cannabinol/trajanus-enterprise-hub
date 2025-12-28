#!/usr/bin/env python3
"""
MARKDOWN TO DOCX CONVERTER
Converts Markdown (.md) files to Word (.docx) format.
Includes file/folder selection dialog.
Requires: pip install pypandoc
"""

import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

def safe_print(text):
    """Safe print that handles unicode on Windows"""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'ignore').decode('ascii'))

def select_folder():
    """Open folder selection dialog"""
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.lift()
    root.focus_force()

    folder_path = filedialog.askdirectory(
        title="Select folder containing Markdown files",
        initialdir="G:/My Drive/00 - Trajanus USA",
        parent=root
    )

    root.destroy()
    return folder_path

def select_files():
    """Open file selection dialog for multiple markdown files"""
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.lift()
    root.focus_force()

    file_paths = filedialog.askopenfilenames(
        title="Select Markdown files to convert",
        initialdir="G:/My Drive/00 - Trajanus USA",
        filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
        parent=root
    )

    root.destroy()
    return file_paths

def convert_md_to_docx(md_file, output_folder=None):
    """Convert a Markdown file to DOCX using pypandoc"""
    try:
        import pypandoc
    except ImportError:
        safe_print("[ERROR] pypandoc not installed. Run: pip install pypandoc")
        return None

    md_path = Path(md_file)

    if output_folder:
        output_path = Path(output_folder) / f"{md_path.stem}.docx"
    else:
        output_path = md_path.with_suffix('.docx')

    # Skip if docx already exists
    if output_path.exists():
        safe_print(f"  SKIP: {output_path.name} already exists")
        return None

    try:
        pypandoc.convert_file(
            str(md_path),
            'docx',
            outputfile=str(output_path),
            extra_args=['--standalone']
        )
        return output_path

    except Exception as e:
        safe_print(f"  ERROR: {e}")
        return None

def main():
    safe_print("=" * 70)
    safe_print("MARKDOWN TO DOCX CONVERTER")
    safe_print("=" * 70)

    # Check for pypandoc
    try:
        import pypandoc
        # Ensure pandoc is available
        pypandoc.get_pandoc_version()
    except ImportError:
        safe_print("[ERROR] pypandoc not installed")
        safe_print("Run: pip install pypandoc")
        sys.exit(1)
    except OSError:
        safe_print("[ERROR] pandoc not found")
        safe_print("Install pandoc from: https://pandoc.org/installing.html")
        safe_print("Or run: pypandoc.download_pandoc()")
        sys.exit(1)

    # Get source from command line or dialog
    if len(sys.argv) > 1:
        source_path = Path(sys.argv[1])

        if source_path.is_file():
            md_files = [source_path]
            output_folder = source_path.parent
        elif source_path.is_dir():
            md_files = list(source_path.glob('*.md'))
            output_folder = source_path
        else:
            safe_print(f"[ERROR] Path not found: {source_path}")
            sys.exit(1)
    else:
        safe_print("[SELECT] Choose selection mode:")
        safe_print("  1. Select folder (convert all .md files)")
        safe_print("  2. Select individual files")

        choice = input("\nEnter 1 or 2: ").strip()

        if choice == '1':
            folder_path = select_folder()
            if not folder_path:
                safe_print("[CANCELLED] No folder selected")
                sys.exit(0)
            source_path = Path(folder_path)
            md_files = list(source_path.glob('*.md'))
            output_folder = source_path
        elif choice == '2':
            file_paths = select_files()
            if not file_paths:
                safe_print("[CANCELLED] No files selected")
                sys.exit(0)
            md_files = [Path(f) for f in file_paths]
            output_folder = md_files[0].parent if md_files else None
        else:
            safe_print("[ERROR] Invalid choice")
            sys.exit(1)

    safe_print(f"Found: {len(md_files)} Markdown files")
    safe_print("")

    if len(md_files) == 0:
        safe_print("[WARNING] No Markdown files found")
        sys.exit(0)

    # Convert each file
    converted = 0
    skipped = 0

    for md_file in sorted(md_files):
        safe_print(f"[CONVERT] {md_file.name}")

        result = convert_md_to_docx(md_file, output_folder)

        if result:
            safe_print(f"  DONE: {result.name}")
            converted += 1
        else:
            skipped += 1

    # Summary
    safe_print("")
    safe_print("=" * 70)
    safe_print("COMPLETE")
    safe_print("=" * 70)
    safe_print(f"Total: {len(md_files)}")
    safe_print(f"Converted: {converted}")
    safe_print(f"Skipped: {skipped}")
    safe_print("=" * 70)

if __name__ == '__main__':
    main()
