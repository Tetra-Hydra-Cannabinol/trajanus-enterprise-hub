#!/usr/bin/env python3
"""
FIX_SCRIPT_ENCODING.py
======================
Run this ONCE to add UTF-8 encoding fix to all Python scripts.

This fixes the Windows PowerShell emoji encoding error:
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4c4'

Author: Claude (Paul successor)
Date: December 6, 2025
For: Bill King, Trajanus USA
"""

import os
import sys

# The encoding fix to add at the top of scripts
ENCODING_FIX = '''# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
'''

# Marker to check if script already has the fix
MARKER = "sys.stdout = io.TextIOWrapper"

def fix_python_file(filepath):
    """Add encoding fix to a single Python file if not already present."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already fixed
        if MARKER in content:
            return "SKIPPED (already fixed)"
        
        # Skip this script itself
        if "FIX_SCRIPT_ENCODING" in content:
            return "SKIPPED (this script)"
        
        # Find where to insert (after shebang and docstrings if present)
        lines = content.split('\n')
        insert_index = 0
        
        # Skip shebang
        if lines and lines[0].startswith('#!'):
            insert_index = 1
        
        # Skip encoding declaration if present
        if insert_index < len(lines) and '# -*-' in lines[insert_index]:
            insert_index += 1
        
        # Build new content
        new_lines = lines[:insert_index]
        new_lines.append(ENCODING_FIX.strip())
        new_lines.append('')  # blank line
        new_lines.extend(lines[insert_index:])
        
        new_content = '\n'.join(new_lines)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return "FIXED"
        
    except Exception as e:
        return f"ERROR: {e}"

def main():
    # Default scripts folder
    scripts_folder = r"G:\My Drive\00 - Trajanus USA\00-Command-Center\Scripts"
    
    # Allow override from command line
    if len(sys.argv) > 1:
        scripts_folder = sys.argv[1]
    
    if not os.path.exists(scripts_folder):
        print(f"ERROR: Folder not found: {scripts_folder}")
        print("Usage: python fix_script_encoding.py [path_to_scripts_folder]")
        return 1
    
    print("=" * 60)
    print("TRAJANUS SCRIPT ENCODING FIXER")
    print("=" * 60)
    print(f"Target folder: {scripts_folder}")
    print()
    
    # Find all .py files
    py_files = [f for f in os.listdir(scripts_folder) if f.endswith('.py')]
    
    if not py_files:
        print("No Python files found in folder.")
        return 0
    
    print(f"Found {len(py_files)} Python files:")
    print("-" * 60)
    
    results = {"FIXED": 0, "SKIPPED": 0, "ERROR": 0}
    
    for filename in sorted(py_files):
        filepath = os.path.join(scripts_folder, filename)
        result = fix_python_file(filepath)
        
        # Categorize result
        if result == "FIXED":
            results["FIXED"] += 1
            status = "[FIXED]"
        elif result.startswith("SKIPPED"):
            results["SKIPPED"] += 1
            status = "[SKIP]"
        else:
            results["ERROR"] += 1
            status = "[ERR]"
        
        print(f"  {status} {filename}")
        if result.startswith("ERROR"):
            print(f"         {result}")
    
    print("-" * 60)
    print(f"SUMMARY: {results['FIXED']} fixed, {results['SKIPPED']} skipped, {results['ERROR']} errors")
    print("=" * 60)
    
    if results["FIXED"] > 0:
        print("\nSUCCESS! Scripts are now Windows PowerShell compatible.")
        print("Emoji characters will display as [?] but scripts will RUN.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
