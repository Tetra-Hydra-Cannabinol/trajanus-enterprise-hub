#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_emoji_encoding.py
Fixes garbled emoji characters in index.html
Run from: G:\My Drive\00 - Trajanus USA\00-Command-Center\05-Scripts\
Usage: python fix_emoji_encoding.py
"""

import os
import re

# Path to index.html (one folder up from Scripts)
script_dir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(os.path.dirname(script_dir), 'index.html')

print(f"Fixing: {index_path}")

with open(index_path, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Garbled emoji patterns to remove (these display as garbage)
emoji_patterns = [
    r'ðŸ"š', r'ðŸ"˜', r'ðŸ"‚', r'ðŸ"', r'ðŸ"‹', 
    r'ðŸ"¤', r'ðŸ¤–', r'ðŸ\'ï¸', r'ðŸŽ¨', r'ðŸ',
    r'ðŸ"Š', r'ðŸ"–', r'ðŸ"—'
]

# Text character fixes
text_fixes = {
    'â€"': '—',   # em dash
    'â€"': '–',   # en dash  
    'â†'': '→',   # arrow
    'â–²': '▲',   # up triangle
    'â–¼': '▼',   # down triangle
    'â€¢': '•',   # bullet
    'Ã—': '×',    # close button
}

# Remove broken emoji patterns
for pattern in emoji_patterns:
    content = content.replace(pattern, '')

# Fix text characters
for old, new in text_fixes.items():
    content = content.replace(old, new)

# Save with UTF-8 encoding
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("[SUCCESS] Emoji encoding fixed!")
