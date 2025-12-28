#!/usr/bin/env python3
"""
TRAJANUS SCRIPT BROWSER
Organized view of all Python scripts by category
Standard Tool UI Template
"""

import os
import sys
import subprocess
import re
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

# Script metadata - define categories and descriptions
SCRIPT_METADATA = {
    # Converters
    'CONVERT_MD_TO_GDOCS_PERMANENT.py': {
        'category': 'Converters',
        'description': 'Convert Markdown files to Google Docs',
        'has_gui': True
    },
    'CONVERT_TXT_TO_GDOCS.py': {
        'category': 'Converters',
        'description': 'Convert text files to Google Docs',
        'has_gui': True
    },
    'CONVERT_DOCX_TO_GDOCS.py': {
        'category': 'Converters',
        'description': 'Convert Word docs to Google Docs',
        'has_gui': True
    },
    'CONVERT_GDOCS_TO_DOCX.py': {
        'category': 'Converters',
        'description': 'Export Google Docs to Word format',
        'has_gui': True
    },
    'CONVERT_MD_TO_DOCX.py': {
        'category': 'Converters',
        'description': 'Convert Markdown to Word format',
        'has_gui': False
    },

    # KB Tools
    'BATCH_INGEST_TOOL.py': {
        'category': 'KB Tools',
        'description': 'Ingest files into knowledge base',
        'has_gui': True
    },
    'QUERY_KB_TOOL.py': {
        'category': 'KB Tools',
        'description': 'Search and query knowledge base',
        'has_gui': True
    },
    'query_kb.py': {
        'category': 'KB Tools',
        'description': 'Command-line KB query tool',
        'has_gui': False
    },
    'file_ingestion.py': {
        'category': 'KB Tools',
        'description': 'Interactive file ingestion menu',
        'has_gui': False
    },
    'batch_ingest_files.py': {
        'category': 'KB Tools',
        'description': 'Batch ingest from command line',
        'has_gui': False
    },

    # Agents
    'research_agent.py': {
        'category': 'Agents',
        'description': 'AI research agent with web search',
        'has_gui': False
    },
    'youtube_playlist_crawler.py': {
        'category': 'Agents',
        'description': 'Crawl YouTube playlists for transcripts',
        'has_gui': False
    },
    'batch_extract_transcripts.py': {
        'category': 'Agents',
        'description': 'Extract transcripts from video list',
        'has_gui': False
    },

    # Utilities
    'SCRIPT_BROWSER.py': {
        'category': 'Utilities',
        'description': 'This script - browse all tools',
        'has_gui': True
    },
}

# Category definitions with icons (using text since no emojis)
CATEGORIES = {
    'All': {'color': '#d4a574'},
    'Converters': {'color': '#4a9f4a'},
    'KB Tools': {'color': '#e8922a'},
    'Agents': {'color': '#9b59b6'},
    'Utilities': {'color': '#3498db'},
}

# Folders to scan
SCRIPT_FOLDERS = [
    Path('G:/My Drive/00 - Trajanus USA/00-Command-Center/05-Scripts'),
    Path('G:/My Drive/00 - Trajanus USA/00-Command-Center/01 Code-Repository'),
]


class TrajanusScriptBrowserGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Trajanus - Script Browser")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        self.root.minsize(550, 450)

        # Standard colors
        self.colors = {
            'bg': '#2d2d2d',
            'sidebar': '#252525',
            'card': '#363636',
            'accent': '#d4a574',
            'hover': '#e8922a',
            'text': '#ffffff',
            'text_dim': '#888888',
            'success': '#4a9f4a',
            'warning': '#e8922a',
            'error': '#e74c3c',
            'border': '#333333'
        }

        self.root.configure(bg=self.colors['bg'])

        # State
        self.scripts = []
        self.selected_category = 'All'
        self.script_widgets = []

        self.setup_header()
        self.setup_content()
        self.scan_scripts()
        self.show_scripts()

    def setup_header(self):
        """Create persistent header"""
        self.header = tk.Frame(self.root, bg=self.colors['accent'], height=50)
        self.header.pack(fill='x')
        self.header.pack_propagate(False)

        title = tk.Label(self.header,
            text="TRAJANUS SCRIPT BROWSER",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['accent'],
            fg='#1a1a1a')
        title.pack(pady=12)

        # Stats bar
        self.stats_bar = tk.Frame(self.root, bg=self.colors['border'], height=25)
        self.stats_bar.pack(fill='x')
        self.stats_bar.pack_propagate(False)

        self.stats_label = tk.Label(self.stats_bar,
            text="Scanning scripts...",
            font=('Segoe UI', 9),
            bg=self.colors['border'],
            fg=self.colors['text_dim'])
        self.stats_label.pack(side='left', padx=15, pady=3)

    def setup_content(self):
        """Create main content area"""
        self.content = tk.Frame(self.root, bg=self.colors['bg'])
        self.content.pack(fill='both', expand=True, padx=20, pady=15)

        # Category buttons
        cat_frame = tk.Frame(self.content, bg=self.colors['bg'])
        cat_frame.pack(fill='x', pady=(0, 15))

        tk.Label(cat_frame,
            text="CATEGORIES:",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text_dim']).pack(side='left', padx=(0, 10))

        self.cat_buttons = {}
        for cat_name, cat_info in CATEGORIES.items():
            btn = tk.Button(cat_frame,
                text=cat_name,
                font=('Segoe UI', 9),
                bg=self.colors['card'] if cat_name != 'All' else self.colors['accent'],
                fg=self.colors['text'] if cat_name != 'All' else '#1a1a1a',
                activebackground=self.colors['hover'],
                activeforeground='#1a1a1a',
                padx=12, pady=4,
                cursor='hand2',
                relief='flat',
                command=lambda c=cat_name: self.select_category(c))
            btn.pack(side='left', padx=2)
            self.cat_buttons[cat_name] = btn

        # Scripts list header
        list_header = tk.Frame(self.content, bg=self.colors['border'])
        list_header.pack(fill='x')

        self.list_title = tk.Label(list_header,
            text="ALL SCRIPTS",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['border'],
            fg=self.colors['accent'],
            pady=5)
        self.list_title.pack(anchor='w', padx=10)

        # Scrollable scripts container
        container = tk.Frame(self.content, bg=self.colors['sidebar'])
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container, bg=self.colors['sidebar'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        self.scripts_frame = tk.Frame(canvas, bg=self.colors['sidebar'])

        self.scripts_frame.bind('<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        canvas.create_window((0, 0), window=self.scripts_frame, anchor='nw', width=650)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Bind mousewheel
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        canvas.bind_all('<MouseWheel>', on_mousewheel)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.canvas = canvas

        # Bottom buttons
        btn_frame = tk.Frame(self.content, bg=self.colors['bg'])
        btn_frame.pack(fill='x', pady=(10, 0))

        refresh_btn = tk.Button(btn_frame,
            text="Refresh",
            font=('Segoe UI', 10),
            bg=self.colors['card'],
            fg=self.colors['accent'],
            activebackground=self.colors['sidebar'],
            activeforeground=self.colors['accent'],
            padx=15, pady=5,
            cursor='hand2',
            relief='flat',
            command=self.refresh_scripts)
        refresh_btn.pack(side='left')

        exit_btn = tk.Button(btn_frame,
            text="Exit",
            font=('Segoe UI', 10),
            bg=self.colors['border'],
            fg=self.colors['text'],
            activebackground='#444444',
            activeforeground=self.colors['text'],
            padx=20, pady=5,
            cursor='hand2',
            relief='flat',
            command=self.root.quit)
        exit_btn.pack(side='right')

    def scan_scripts(self):
        """Scan folders for Python scripts"""
        self.scripts = []

        for folder in SCRIPT_FOLDERS:
            if not folder.exists():
                continue

            for py_file in folder.glob('*.py'):
                if py_file.name.startswith('__'):
                    continue

                # Get metadata or auto-categorize
                if py_file.name in SCRIPT_METADATA:
                    meta = SCRIPT_METADATA[py_file.name]
                else:
                    meta = self.auto_categorize(py_file)

                self.scripts.append({
                    'name': py_file.name,
                    'path': py_file,
                    'category': meta.get('category', 'Utilities'),
                    'description': meta.get('description', 'No description'),
                    'has_gui': meta.get('has_gui', False)
                })

        # Sort by name
        self.scripts.sort(key=lambda x: x['name'].lower())

        # Count by category
        counts = {'All': len(self.scripts)}
        for script in self.scripts:
            cat = script['category']
            counts[cat] = counts.get(cat, 0) + 1

        self.stats_label.config(text=f"Found {len(self.scripts)} scripts in {len(SCRIPT_FOLDERS)} folders")

    def auto_categorize(self, py_file):
        """Auto-categorize script based on name and content"""
        name = py_file.name.lower()

        # Check name patterns
        if 'convert' in name or 'export' in name:
            category = 'Converters'
        elif 'ingest' in name or 'query' in name or '_kb' in name:
            category = 'KB Tools'
        elif 'agent' in name or 'crawl' in name or 'extract' in name:
            category = 'Agents'
        else:
            category = 'Utilities'

        # Try to get description from docstring
        description = 'No description'
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read(500)
                # Look for docstring
                match = re.search(r'"""(.+?)"""', content, re.DOTALL)
                if match:
                    desc = match.group(1).strip().split('\n')[0]
                    if len(desc) < 100:
                        description = desc
        except:
            pass

        # Check if has GUI
        has_gui = 'tkinter' in name or name.isupper()

        return {
            'category': category,
            'description': description,
            'has_gui': has_gui
        }

    def select_category(self, category):
        """Select a category and update display"""
        self.selected_category = category

        # Update button styles
        for cat_name, btn in self.cat_buttons.items():
            if cat_name == category:
                btn.config(bg=self.colors['accent'], fg='#1a1a1a')
            else:
                btn.config(bg=self.colors['card'], fg=self.colors['text'])

        # Update title
        self.list_title.config(text=f"{category.upper()} SCRIPTS" if category != 'All' else "ALL SCRIPTS")

        self.show_scripts()

    def show_scripts(self):
        """Display scripts for selected category"""
        # Clear existing
        for widget in self.scripts_frame.winfo_children():
            widget.destroy()

        # Filter scripts
        if self.selected_category == 'All':
            filtered = self.scripts
        else:
            filtered = [s for s in self.scripts if s['category'] == self.selected_category]

        if not filtered:
            tk.Label(self.scripts_frame,
                text="No scripts in this category",
                font=('Segoe UI', 11),
                bg=self.colors['sidebar'],
                fg=self.colors['text_dim']).pack(pady=30)
            return

        # Create script cards
        for script in filtered:
            self.create_script_card(script)

    def create_script_card(self, script):
        """Create a card for a script"""
        card = tk.Frame(self.scripts_frame, bg=self.colors['card'], padx=15, pady=10)
        card.pack(fill='x', padx=8, pady=4)

        # Header row
        header = tk.Frame(card, bg=self.colors['card'])
        header.pack(fill='x')

        # Script name
        name_label = tk.Label(header,
            text=script['name'],
            font=('Consolas', 10, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['accent'])
        name_label.pack(side='left')

        # Category badge
        cat_color = CATEGORIES.get(script['category'], {}).get('color', self.colors['text_dim'])
        cat_label = tk.Label(header,
            text=script['category'],
            font=('Segoe UI', 8),
            bg=cat_color,
            fg='#1a1a1a',
            padx=6, pady=1)
        cat_label.pack(side='right')

        # GUI indicator
        if script['has_gui']:
            gui_label = tk.Label(header,
                text="GUI",
                font=('Segoe UI', 8),
                bg=self.colors['success'],
                fg='#1a1a1a',
                padx=6, pady=1)
            gui_label.pack(side='right', padx=(0, 5))

        # Description
        tk.Label(card,
            text=script['description'],
            font=('Segoe UI', 9),
            bg=self.colors['card'],
            fg=self.colors['text_dim'],
            anchor='w').pack(fill='x', pady=(5, 8))

        # Button row
        btn_row = tk.Frame(card, bg=self.colors['card'])
        btn_row.pack(fill='x')

        run_btn = tk.Button(btn_row,
            text="RUN",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['accent'],
            fg='#1a1a1a',
            activebackground=self.colors['hover'],
            activeforeground='#1a1a1a',
            padx=20, pady=3,
            cursor='hand2',
            relief='flat',
            command=lambda s=script: self.run_script(s))
        run_btn.pack(side='left')

        open_btn = tk.Button(btn_row,
            text="Open Location",
            font=('Segoe UI', 8),
            bg=self.colors['border'],
            fg=self.colors['text_dim'],
            activebackground='#444444',
            activeforeground=self.colors['text'],
            padx=10, pady=3,
            cursor='hand2',
            relief='flat',
            command=lambda s=script: self.open_location(s))
        open_btn.pack(side='left', padx=(10, 0))

        edit_btn = tk.Button(btn_row,
            text="Edit",
            font=('Segoe UI', 8),
            bg=self.colors['border'],
            fg=self.colors['text_dim'],
            activebackground='#444444',
            activeforeground=self.colors['text'],
            padx=10, pady=3,
            cursor='hand2',
            relief='flat',
            command=lambda s=script: self.edit_script(s))
        edit_btn.pack(side='left', padx=(5, 0))

    def run_script(self, script):
        """Run the selected script"""
        try:
            if script['has_gui']:
                # Run GUI script directly
                subprocess.Popen(['python', str(script['path'])],
                    creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                # Run in terminal
                subprocess.Popen(['cmd', '/k', 'python', str(script['path'])],
                    creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run script:\n{e}")

    def open_location(self, script):
        """Open folder containing script"""
        try:
            subprocess.run(['explorer', '/select,', str(script['path'])])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open location:\n{e}")

    def edit_script(self, script):
        """Open script in VS Code"""
        try:
            subprocess.Popen(['code', str(script['path'])])
        except:
            # Fallback to notepad
            try:
                subprocess.Popen(['notepad', str(script['path'])])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to edit script:\n{e}")

    def refresh_scripts(self):
        """Refresh script list"""
        self.scan_scripts()
        self.show_scripts()

    def run(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        self.root.mainloop()


def main():
    app = TrajanusScriptBrowserGUI()
    app.run()


if __name__ == '__main__':
    main()
