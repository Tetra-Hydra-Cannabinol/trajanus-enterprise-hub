#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
TRAJANUS MD CONVERTER TOOL
═══════════════════════════════════════════════════════════════════════════════
REAL MD to Google Docs converter using Trajanus Workspace branding.
Copied EXACT styling from trajanus_file_browser.py

Usage:
    python MD_CONVERTER_TOOL.py

    # Or import as module:
    from MD_CONVERTER_TOOL import MDConverterApp, convert_md_to_gdoc
═══════════════════════════════════════════════════════════════════════════════
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import re
from pathlib import Path
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════
# TRAJANUS BRAND PALETTE (EXACT from trajanus_file_browser.py)
# ═══════════════════════════════════════════════════════════════════════════
COLORS = {
    'bg_base': '#0a0a0a',
    'bg_elevated': '#1a1a1a',
    'bg_hover': '#2a2a2a',
    'bg_panel': '#0f0f0f',
    'accent': '#00AAFF',
    'accent_light': '#33BBFF',
    'accent_dark': '#0088CC',
    'silver': '#c0c0c0',
    'silver_light': '#e0e0e0',
    'silver_dark': '#a0a0a0',
    'text_white': '#ffffff',
    'text_muted': '#808080',
    'folder_yellow': '#FFD700',
    'file_silver': '#c0c0c0',
    'success': '#4ade80',
    'warning': '#fbbf24',
    'error': '#f87171',
    'border': '#00AAFF',
    'border_subtle': '#333333',
}

DEFAULT_PATH = r"G:\My Drive\00 - Trajanus USA"

# Google API imports
try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False

# ═══════════════════════════════════════════════════════════════════════════
# STANDALONE CONVERSION FUNCTION (for reuse)
# ═══════════════════════════════════════════════════════════════════════════
def convert_md_to_gdoc(filepath, drive_service, docs_service, folder_id=None):
    """
    Convert a single MD file to Google Doc.
    Returns doc_id on success, raises Exception on failure.

    Usage:
        from MD_CONVERTER_TOOL import convert_md_to_gdoc
        doc_id = convert_md_to_gdoc("file.md", drive_svc, docs_svc)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.splitext(os.path.basename(filepath))[0]

    doc_metadata = {
        'name': filename,
        'mimeType': 'application/vnd.google-apps.document'
    }
    if folder_id:
        doc_metadata['parents'] = [folder_id]

    doc = drive_service.files().create(body=doc_metadata).execute()
    doc_id = doc['id']

    requests = [{
        'insertText': {
            'location': {'index': 1},
            'text': content
        }
    }]
    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': requests}
    ).execute()

    return doc_id

# ═══════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════
class MDConverterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Trajanus - MD Converter")
        self.root.configure(bg=COLORS['bg_base'])

        # Window sizing (85% of screen)
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        win_w = int(screen_w * 0.85)
        win_h = int(screen_h * 0.85)
        x = (screen_w - win_w) // 2
        y = (screen_h - win_h) // 2
        self.root.geometry(f"{win_w}x{win_h}+{x}+{y}")
        self.root.minsize(1000, 700)

        # State
        self.current_path = DEFAULT_PATH
        self.files_to_convert = []
        self.completed_files = []
        self.failed_files = []
        self.is_converting = False

        # Google API
        self.docs_service = None
        self.drive_service = None
        self.folder_ids = {}

        # Build UI
        self._create_header()
        self._create_main_layout()
        self._init_google_api()

    def _create_header(self):
        """Branded header bar - EXACT from trajanus_file_browser.py"""
        header = tk.Frame(self.root, bg=COLORS['bg_base'], height=55)
        header.pack(fill='x')
        header.pack_propagate(False)

        # Logo area with accent bar
        logo_frame = tk.Frame(header, bg=COLORS['bg_base'])
        logo_frame.pack(side='left', padx=15, pady=8)

        name_frame = tk.Frame(logo_frame, bg=COLORS['bg_base'])
        name_frame.pack(side='left')

        # Accent bar
        accent_bar = tk.Frame(name_frame, bg=COLORS['accent'], width=4)
        accent_bar.pack(side='left', fill='y', padx=(0, 10))

        text_frame = tk.Frame(name_frame, bg=COLORS['bg_base'])
        text_frame.pack(side='left')

        tk.Label(text_frame,
            text="TRAJANUS",
            font=('Segoe UI', 20, 'bold'),
            bg=COLORS['bg_base'],
            fg=COLORS['accent']).pack(anchor='w')

        tk.Label(text_frame,
            text="Engineering Intelligence™",
            font=('Segoe UI', 8, 'italic'),
            bg=COLORS['bg_base'],
            fg=COLORS['silver']).pack(anchor='w')

        # Tool indicator
        tool_frame = tk.Frame(header, bg=COLORS['accent'], padx=12, pady=4)
        tool_frame.pack(side='left', padx=30, pady=12)

        tk.Label(tool_frame,
            text="MD → GOOGLE DOCS",
            font=('Segoe UI', 9, 'bold'),
            bg=COLORS['accent'],
            fg=COLORS['bg_base']).pack()

        # Status
        self.status_label = tk.Label(header,
            text="Initializing...",
            font=('Segoe UI', 9),
            bg=COLORS['bg_base'],
            fg=COLORS['text_muted'])
        self.status_label.pack(side='right', padx=15)

    def _create_panel(self, parent, title):
        """Create a standard panel with header"""
        frame = tk.Frame(parent, bg=COLORS['bg_panel'],
                        highlightbackground=COLORS['border'],
                        highlightthickness=2)

        # Panel header
        header = tk.Frame(frame, bg=COLORS['bg_elevated'], height=30)
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(header,
            text=title,
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['bg_elevated'],
            fg=COLORS['accent']).pack(side='left', padx=10, pady=5)

        # Content area
        content = tk.Frame(frame, bg=COLORS['bg_panel'])
        content.pack(fill='both', expand=True, padx=5, pady=5)

        return frame, content, header

    def _create_main_layout(self):
        """Create 3-panel layout"""
        main_frame = tk.Frame(self.root, bg=COLORS['bg_base'])
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Panel 1: File Browser
        browser_frame = tk.Frame(main_frame, bg=COLORS['bg_panel'], width=450)
        browser_frame.pack(side='left', fill='both', expand=True, padx=(0, 3))
        browser_frame.pack_propagate(False)
        self._create_browser_panel(browser_frame)

        # Panel 2: Pending + Completed
        middle_frame = tk.Frame(main_frame, bg=COLORS['bg_panel'], width=350)
        middle_frame.pack(side='left', fill='both', expand=True, padx=3)
        middle_frame.pack_propagate(False)
        self._create_queue_panel(middle_frame)

        # Panel 3: Progress + Log
        right_frame = tk.Frame(main_frame, bg=COLORS['bg_panel'], width=400)
        right_frame.pack(side='left', fill='both', expand=True, padx=(3, 0))
        right_frame.pack_propagate(False)
        self._create_progress_panel(right_frame)

    def _create_browser_panel(self, parent):
        """Panel 1: File browser"""
        frame, content, header = self._create_panel(parent, "1. SELECT FILES")
        frame.pack(fill='both', expand=True)

        # Path bar
        path_frame = tk.Frame(content, bg=COLORS['bg_panel'])
        path_frame.pack(fill='x', pady=(0, 5))

        tk.Label(path_frame, text="Path:", font=('Segoe UI', 9),
            bg=COLORS['bg_panel'], fg=COLORS['silver']).pack(side='left')

        self.path_var = tk.StringVar(value=self.current_path)
        self.path_entry = tk.Entry(path_frame,
            textvariable=self.path_var,
            font=('Consolas', 9),
            bg=COLORS['bg_elevated'],
            fg=COLORS['text_white'],
            insertbackground=COLORS['accent'],
            relief='flat')
        self.path_entry.pack(side='left', fill='x', expand=True, padx=5)
        self.path_entry.bind('<Return>', lambda e: self._populate_tree())

        refresh_btn = tk.Button(path_frame, text="Refresh",
            font=('Segoe UI', 8), bg=COLORS['bg_elevated'], fg=COLORS['silver'],
            activebackground=COLORS['bg_hover'], relief='flat', cursor='hand2',
            command=self._populate_tree)
        refresh_btn.pack(side='right', padx=2)

        # Tree view
        tree_frame = tk.Frame(content, bg=COLORS['bg_panel'])
        tree_frame.pack(fill='both', expand=True)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Browser.Treeview',
            background=COLORS['bg_base'],
            foreground=COLORS['text_white'],
            fieldbackground=COLORS['bg_base'])
        style.map('Browser.Treeview',
            background=[('selected', COLORS['bg_hover'])],
            foreground=[('selected', COLORS['accent'])])

        self.tree = ttk.Treeview(tree_frame, style='Browser.Treeview',
            columns=('path',), show='tree', selectmode='extended')
        self.tree.column('#0', width=400)
        self.tree.column('path', width=0, stretch=False)

        vsb = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        self.tree.pack(fill='both', expand=True)

        self.tree.bind('<<TreeviewOpen>>', self._on_tree_expand)
        self.tree.tag_configure('folder', foreground=COLORS['folder_yellow'])
        self.tree.tag_configure('file', foreground=COLORS['file_silver'])
        self.tree.tag_configure('md_file', foreground=COLORS['success'])

        # Add button
        btn_frame = tk.Frame(content, bg=COLORS['bg_panel'])
        btn_frame.pack(fill='x', pady=(5, 0))

        add_btn = tk.Button(btn_frame,
            text="➤ ADD TO CONVERSION QUEUE",
            font=('Segoe UI', 10, 'bold'),
            bg=COLORS['accent'],
            fg=COLORS['bg_base'],
            activebackground=COLORS['accent_light'],
            relief='flat', cursor='hand2',
            padx=15, pady=8,
            command=self._add_to_queue)
        add_btn.pack(fill='x')

    def _create_queue_panel(self, parent):
        """Panel 2: Pending and Completed lists"""
        frame, content, header = self._create_panel(parent, "2. CONVERSION QUEUE")
        frame.pack(fill='both', expand=True)

        # Pending section
        pending_header = tk.Frame(content, bg=COLORS['warning'])
        pending_header.pack(fill='x', pady=(0, 5))
        tk.Label(pending_header, text="  PENDING",
            font=('Segoe UI', 9, 'bold'),
            bg=COLORS['warning'], fg=COLORS['bg_base']).pack(side='left', pady=3)

        self.pending_count = tk.Label(pending_header, text="0",
            font=('Segoe UI', 9, 'bold'),
            bg=COLORS['warning'], fg=COLORS['bg_base'])
        self.pending_count.pack(side='right', padx=10, pady=3)

        pending_frame = tk.Frame(content, bg=COLORS['bg_elevated'])
        pending_frame.pack(fill='both', expand=True, pady=(0, 10))

        self.pending_listbox = tk.Listbox(pending_frame,
            font=('Consolas', 9),
            bg=COLORS['bg_base'],
            fg=COLORS['warning'],
            selectbackground=COLORS['bg_hover'],
            activestyle='none', relief='flat',
            highlightthickness=0)
        self.pending_listbox.pack(fill='both', expand=True, padx=2, pady=2)

        pending_btn = tk.Frame(content, bg=COLORS['bg_panel'])
        pending_btn.pack(fill='x', pady=(0, 10))

        tk.Button(pending_btn, text="Remove", font=('Segoe UI', 8),
            bg=COLORS['bg_hover'], fg=COLORS['silver'], relief='flat',
            command=self._remove_from_queue).pack(side='left', padx=2)
        tk.Button(pending_btn, text="Clear All", font=('Segoe UI', 8),
            bg=COLORS['bg_hover'], fg=COLORS['silver'], relief='flat',
            command=self._clear_queue).pack(side='left', padx=2)

        # Completed section
        completed_header = tk.Frame(content, bg=COLORS['success'])
        completed_header.pack(fill='x', pady=(0, 5))
        tk.Label(completed_header, text="  COMPLETED",
            font=('Segoe UI', 9, 'bold'),
            bg=COLORS['success'], fg=COLORS['bg_base']).pack(side='left', pady=3)

        self.completed_count = tk.Label(completed_header, text="0",
            font=('Segoe UI', 9, 'bold'),
            bg=COLORS['success'], fg=COLORS['bg_base'])
        self.completed_count.pack(side='right', padx=10, pady=3)

        completed_frame = tk.Frame(content, bg=COLORS['bg_elevated'])
        completed_frame.pack(fill='both', expand=True)

        self.completed_listbox = tk.Listbox(completed_frame,
            font=('Consolas', 9),
            bg=COLORS['bg_base'],
            fg=COLORS['success'],
            activestyle='none', relief='flat',
            highlightthickness=0)
        self.completed_listbox.pack(fill='both', expand=True, padx=2, pady=2)

    def _create_progress_panel(self, parent):
        """Panel 3: Progress and Convert button"""
        frame, content, header = self._create_panel(parent, "3. CONVERT")
        frame.pack(fill='both', expand=True)

        # Progress bar (animated)
        progress_label = tk.Label(content, text="PROGRESS",
            font=('Segoe UI', 9, 'bold'),
            bg=COLORS['bg_panel'], fg=COLORS['silver'])
        progress_label.pack(anchor='w', pady=(0, 5))

        self.progress_canvas = tk.Canvas(content, height=30,
            bg=COLORS['bg_elevated'],
            highlightthickness=2,
            highlightbackground=COLORS['border'])
        self.progress_canvas.pack(fill='x', pady=(0, 5))
        self.progress_value = 0
        self._draw_progress()

        self.progress_text = tk.Label(content, text="0 / 0 files",
            font=('Segoe UI', 9),
            bg=COLORS['bg_panel'], fg=COLORS['text_muted'])
        self.progress_text.pack(anchor='w', pady=(0, 15))

        # Convert button
        self.convert_btn = tk.Button(content,
            text="▶  CONVERT ALL TO GOOGLE DOCS",
            font=('Segoe UI', 12, 'bold'),
            bg=COLORS['success'],
            fg=COLORS['bg_base'],
            activebackground='#6ee7a0',
            relief='flat', cursor='hand2',
            padx=20, pady=12,
            state='disabled',
            command=self._start_conversion)
        self.convert_btn.pack(fill='x', pady=(0, 15))

        # Log
        log_label = tk.Label(content, text="CONVERSION LOG",
            font=('Segoe UI', 9, 'bold'),
            bg=COLORS['bg_panel'], fg=COLORS['silver'])
        log_label.pack(anchor='w', pady=(0, 5))

        log_frame = tk.Frame(content, bg=COLORS['bg_elevated'])
        log_frame.pack(fill='both', expand=True)

        self.log_text = tk.Text(log_frame,
            font=('Consolas', 9),
            bg=COLORS['bg_base'],
            fg=COLORS['text_white'],
            relief='flat', wrap='word',
            highlightthickness=0)
        vsb = ttk.Scrollbar(log_frame, orient='vertical', command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        self.log_text.pack(fill='both', expand=True, padx=2, pady=2)

        self._log("Ready. Click 'Refresh' to load files.")

    # ═══════════════════════════════════════════════════════════════════════
    # FILE TREE
    # ═══════════════════════════════════════════════════════════════════════
    def _populate_tree(self):
        """Load file tree"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        path = self.path_var.get()
        if not os.path.exists(path):
            self._set_status(f"Path not found: {path}", 'error')
            return

        self.current_path = path
        self._set_status(f"Loading: {path}")

        try:
            self._populate_folder('', path)
            self._set_status(f"Loaded: {path}", 'success')
        except Exception as e:
            self._set_status(f"Error: {e}", 'error')

    def _populate_folder(self, parent_id, folder_path, max_items=150):
        """Populate folder contents"""
        try:
            items = sorted(os.listdir(folder_path),
                key=lambda x: (not os.path.isdir(os.path.join(folder_path, x)), x.lower()))[:max_items]

            for name in items:
                item_path = os.path.join(folder_path, name)
                is_dir = os.path.isdir(item_path)
                is_md = name.lower().endswith('.md')

                if is_dir:
                    tag = 'folder'
                    prefix = '📁 '
                elif is_md:
                    tag = 'md_file'
                    prefix = '📄 '
                else:
                    tag = 'file'
                    prefix = '   '

                item_id = self.tree.insert(parent_id, 'end',
                    text=f"{prefix}{name}",
                    values=(item_path,),
                    tags=(tag,))

                if is_dir:
                    self.tree.insert(item_id, 'end', text='Loading...')

        except PermissionError:
            pass

    def _on_tree_expand(self, event):
        """Handle folder expansion"""
        item_id = self.tree.focus()
        children = self.tree.get_children(item_id)

        if len(children) == 1 and self.tree.item(children[0], 'text') == 'Loading...':
            self.tree.delete(children[0])
            folder_path = self.tree.set(item_id, 'path')
            if folder_path and os.path.isdir(folder_path):
                self._populate_folder(item_id, folder_path)

    # ═══════════════════════════════════════════════════════════════════════
    # QUEUE OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════
    def _add_to_queue(self):
        """Add selected .md files to queue"""
        selections = self.tree.selection()
        if not selections:
            self._set_status("Select .md files first", 'warning')
            return

        added = 0
        for item_id in selections:
            item_path = self.tree.set(item_id, 'path')
            if item_path and item_path.lower().endswith('.md'):
                if item_path not in self.files_to_convert:
                    self.files_to_convert.append(item_path)
                    self.pending_listbox.insert('end', os.path.basename(item_path))
                    added += 1

        self._update_counts()
        if added:
            self._log(f"Added {added} file(s) to queue")
            self._set_status(f"Added {added} file(s)", 'success')
        else:
            self._set_status("Select .md files only", 'warning')

    def _remove_from_queue(self):
        """Remove selected from queue"""
        selection = self.pending_listbox.curselection()
        if selection:
            for idx in reversed(selection):
                self.pending_listbox.delete(idx)
                del self.files_to_convert[idx]
            self._update_counts()

    def _clear_queue(self):
        """Clear all pending"""
        self.pending_listbox.delete(0, 'end')
        self.files_to_convert.clear()
        self._update_counts()

    def _update_counts(self):
        """Update count displays"""
        pending = len(self.files_to_convert)
        completed = len(self.completed_files)
        self.pending_count.config(text=str(pending))
        self.completed_count.config(text=str(completed))
        self.progress_text.config(text=f"{completed} / {pending + completed} files")
        self.convert_btn.config(state='normal' if pending > 0 and self.drive_service else 'disabled')

    # ═══════════════════════════════════════════════════════════════════════
    # GOOGLE API
    # ═══════════════════════════════════════════════════════════════════════
    def _init_google_api(self):
        """Initialize Google API"""
        if not GOOGLE_API_AVAILABLE:
            self._log("Google API not installed. pip install google-api-python-client google-auth", 'error')
            self._set_status("No Google API", 'error')
            return

        # Search for token.json
        search_paths = [
            os.path.dirname(__file__),
            os.path.dirname(os.path.dirname(__file__)),
            r"G:\My Drive\00 - Trajanus USA\00-Command-Center",
        ]

        token_path = None
        for p in search_paths:
            candidate = os.path.join(p, 'token.json')
            if os.path.exists(candidate):
                token_path = candidate
                break

        if token_path:
            try:
                creds = Credentials.from_authorized_user_file(token_path)
                self.docs_service = build('docs', 'v1', credentials=creds)
                self.drive_service = build('drive', 'v3', credentials=creds)
                self._log(f"✓ Google API connected")
                self._set_status("Ready - Google API connected", 'success')
                self._update_counts()
            except Exception as e:
                self._log(f"✗ Google API error: {e}", 'error')
                self._set_status("API Error", 'error')
        else:
            self._log("token.json not found", 'warning')
            self._set_status("No Auth - token.json not found", 'warning')

    # ═══════════════════════════════════════════════════════════════════════
    # CONVERSION - REAL
    # ═══════════════════════════════════════════════════════════════════════
    def _start_conversion(self):
        """Start REAL conversion"""
        if not self.files_to_convert:
            return
        if not self.drive_service:
            messagebox.showerror("Error", "Google API not connected")
            return
        if self.is_converting:
            return

        self.is_converting = True
        self.convert_btn.config(state='disabled')
        self._set_status("Converting...", 'info')

        thread = threading.Thread(target=self._run_conversion, daemon=True)
        thread.start()

    def _run_conversion(self):
        """Background conversion - REAL GOOGLE API CALLS"""
        total = len(self.files_to_convert)
        converted = 0

        for i, filepath in enumerate(self.files_to_convert[:]):
            filename = os.path.basename(filepath)

            try:
                self.root.after(0, lambda f=filename: self._log(f"Converting: {f}"))

                # REAL CONVERSION
                doc_id = convert_md_to_gdoc(filepath, self.drive_service, self.docs_service)

                self.completed_files.append(filepath)
                converted += 1

                self.root.after(0, lambda f=filename: self._mark_done(f))
                self.root.after(0, lambda f=filename: self._log(f"✓ Done: {f}"))

            except Exception as e:
                self.failed_files.append((filepath, str(e)))
                self.root.after(0, lambda f=filename, e=str(e): self._log(f"✗ Failed: {f} - {e}"))

            # Update progress
            progress = int((i + 1) / total * 100)
            self.root.after(0, lambda p=progress: self._update_progress(p))

        self.root.after(0, lambda c=converted, t=total: self._conversion_done(c, t))

    def _mark_done(self, filename):
        """Move from pending to completed"""
        self.completed_listbox.insert('end', f"✓ {filename}")
        items = list(self.pending_listbox.get(0, 'end'))
        for i, item in enumerate(items):
            if item == filename:
                self.pending_listbox.delete(i)
                if self.files_to_convert and i < len(self.files_to_convert):
                    del self.files_to_convert[i]
                break
        self._update_counts()

    def _update_progress(self, value):
        """Update progress bar"""
        self.progress_value = value
        self._draw_progress()

    def _draw_progress(self):
        """Draw animated progress bar"""
        self.progress_canvas.delete('all')
        w = self.progress_canvas.winfo_width() or 300
        h = 30

        if self.progress_value > 0:
            fill_w = int(w * (self.progress_value / 100))
            # Main fill
            self.progress_canvas.create_rectangle(0, 0, fill_w, h,
                fill=COLORS['accent_dark'], outline='')
            # Highlight edge
            if fill_w > 3:
                self.progress_canvas.create_rectangle(fill_w-4, 0, fill_w, h,
                    fill=COLORS['accent_light'], outline='')

        # Percentage
        self.progress_canvas.create_text(w/2, h/2,
            text=f"{self.progress_value}%",
            font=('Segoe UI', 11, 'bold'),
            fill=COLORS['text_white'])

    def _conversion_done(self, converted, total):
        """Conversion complete"""
        self.is_converting = False
        self.convert_btn.config(state='normal' if self.files_to_convert else 'disabled')

        if converted == total:
            self._set_status(f"✓ Converted {total} files", 'success')
            self._log(f"═══ COMPLETE: {total} files converted ═══")
        else:
            self._set_status(f"Done: {converted}/{total}", 'warning')
            self._log(f"═══ DONE: {converted} of {total} succeeded ═══")

    # ═══════════════════════════════════════════════════════════════════════
    # UTILITIES
    # ═══════════════════════════════════════════════════════════════════════
    def _log(self, message, level='info'):
        """Add to log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.insert('end', f"[{timestamp}] {message}\n")
        self.log_text.see('end')

    def _set_status(self, message, status_type='info'):
        """Update status"""
        colors = {
            'info': COLORS['silver'],
            'success': COLORS['success'],
            'warning': COLORS['warning'],
            'error': COLORS['error']
        }
        self.status_label.config(text=message, fg=colors.get(status_type, COLORS['silver']))

    def run(self):
        """Start app"""
        self.root.mainloop()


if __name__ == '__main__':
    app = MDConverterApp()
    app.run()
