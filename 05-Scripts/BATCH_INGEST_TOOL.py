#!/usr/bin/env python3
"""
TRAJANUS BATCH INGEST TOOL
Ingest files into the knowledge base with embeddings
Enhanced with 3D buttons and scrollable interface
"""

import os
import sys
import io
import threading
from pathlib import Path
from datetime import datetime
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class BeveledButton(tk.Canvas):
    """3D Beveled button with machine indicator light effect"""

    def __init__(self, parent, text, command=None, width=180, height=40,
                 style='primary', palette=None, **kwargs):
        super().__init__(parent, width=width, height=height,
                        bg=parent.cget('bg'), highlightthickness=0, **kwargs)

        self.command = command
        self.text = text
        self.width = width
        self.height = height
        self.style = style
        self.pressed = False

        # Use palette colors if provided, otherwise use defaults
        if palette and style == 'primary':
            self.colors = {
                'face': palette.get('btn_face', '#d4a574'),
                'light': palette.get('btn_light', '#f0c896'),
                'dark': palette.get('btn_dark', '#8a6b4a'),
                'text': palette.get('btn_text', '#0a0a0a'),
                'glow': palette.get('btn_glow', '#ffe4c4')
            }
        elif palette and style == 'dark':
            self.colors = {
                'face': palette.get('bg_light', '#1a1a1a'),
                'light': palette.get('border', '#333333'),
                'dark': palette.get('bg', '#0a0a0a'),
                'text': palette.get('text', '#ffffff'),
                'glow': '#555555'
            }
        else:
            self.schemes = {
                'primary': {
                    'face': '#d4a574',
                    'light': '#f0c896',
                    'dark': '#8a6b4a',
                    'text': '#0a0a0a',
                    'glow': '#ffe4c4'
                },
                'dark': {
                    'face': '#404040',
                    'light': '#606060',
                    'dark': '#252525',
                    'text': '#ffffff',
                    'glow': '#555555'
                },
                'success': {
                    'face': '#4a9f4a',
                    'light': '#6abf6a',
                    'dark': '#2a7f2a',
                    'text': '#ffffff',
                    'glow': '#7fcf7f'
                }
            }
            self.colors = self.schemes.get(style, self.schemes['primary'])

        self.draw_button()

        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_press)
        self.bind('<ButtonRelease-1>', self.on_release)

    def draw_button(self, pressed=False):
        self.delete('all')
        w, h = self.width, self.height
        bevel = 3
        colors = self.colors

        if pressed:
            outer_light = colors['dark']
            outer_dark = colors['light']
            face = colors['dark']
        else:
            outer_light = colors['light']
            outer_dark = colors['dark']
            face = colors['face']

        self.create_polygon(8, 0, w-8, 0, w, 8, w-bevel, 8+bevel,
            8+bevel, bevel, bevel, 8+bevel, bevel, h-8-bevel,
            0, h-8, 0, 8, fill=outer_light, outline='')

        self.create_polygon(w, 8, w, h-8, w-8, h, 8, h,
            8+bevel, h-bevel, w-8-bevel, h-bevel,
            w-bevel, h-8-bevel, w-bevel, 8+bevel, fill=outer_dark, outline='')

        self.create_rectangle(bevel+1, bevel+1, w-bevel-1, h-bevel-1,
            fill=face, outline='')

        if not pressed:
            self.create_rectangle(bevel+4, bevel+2, w-bevel-4, bevel+5,
                fill=colors['glow'], outline='')

        self.create_text(w/2, h/2 + (2 if pressed else 0),
            text=self.text, font=('Segoe UI', 10, 'bold'), fill=colors['text'])

    def on_enter(self, event):
        self.config(cursor='hand2')

    def on_leave(self, event):
        self.config(cursor='')
        if self.pressed:
            self.pressed = False
            self.draw_button(pressed=False)

    def on_press(self, event):
        self.pressed = True
        self.draw_button(pressed=True)

    def on_release(self, event):
        if self.pressed:
            self.pressed = False
            self.draw_button(pressed=False)
            if self.command:
                self.command()


class TrajanusBatchIngestGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Trajanus - Batch Ingest Tool")
        self.root.geometry("750x650")
        self.root.resizable(True, True)
        self.root.minsize(650, 550)

        # Black/Gold palette (standard for all tools)
        self.colors = {
            'bg': '#0a0a0a',
            'bg_light': '#1a1a1a',
            'card': '#252525',
            'accent': '#d4a574',
            'hover': '#e8b88a',
            'text': '#ffffff',
            'text_dim': '#888888',
            'success': '#4a9f4a',
            'warning': '#e8922a',
            'error': '#e74c3c',
            'border': '#333333',
            'divider': '#d4a574',
            'btn_face': '#d4a574',
            'btn_light': '#f0c896',
            'btn_dark': '#8a6b4a',
            'btn_text': '#0a0a0a',
            'btn_glow': '#ffe4c4'
        }

        self.root.configure(bg=self.colors['bg'])

        # State
        self.supabase = None
        self.openai_client = None
        self.processing = False
        self.source_category = tk.StringVar(value="General")

        # Results storage
        self.processed_files = []
        self.skipped_files = []
        self.error_files = []
        self.total_chunks = 0

        # Current frame reference
        self.current_frame = None
        self.scroll_canvas = None

        self.setup_header()
        self.connect_services()
        self.show_welcome_screen()

    def setup_header(self):
        """Create compact header (matches conversion tool)"""
        self.header = tk.Frame(self.root, bg=self.colors['accent'], height=35)
        self.header.pack(fill='x')
        self.header.pack_propagate(False)

        title = tk.Label(self.header,
            text="TRAJANUS BATCH INGEST",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['accent'],
            fg='#1a1a1a')
        title.pack(pady=7)

        # Connection status bar
        self.status_bar = tk.Frame(self.root, bg=self.colors['border'], height=24)
        self.status_bar.pack(fill='x')
        self.status_bar.pack_propagate(False)

        self.connection_label = tk.Label(self.status_bar,
            text="Connecting to services...",
            font=('Segoe UI', 8),
            bg=self.colors['border'],
            fg=self.colors['text_dim'])
        self.connection_label.pack(side='left', padx=10, pady=3)

        self.connection_status = tk.Label(self.status_bar,
            text="",
            font=('Segoe UI', 8, 'bold'),
            bg=self.colors['border'],
            fg=self.colors['warning'])
        self.connection_status.pack(side='right', padx=10, pady=3)

    def create_scrollable_frame(self):
        """Create a scrollable content area"""
        container = tk.Frame(self.root, bg=self.colors['bg'])
        container.pack(fill='both', expand=True)

        self.scroll_canvas = tk.Canvas(container, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient='vertical', command=self.scroll_canvas.yview)

        self.scrollable_frame = tk.Frame(self.scroll_canvas, bg=self.colors['bg'])
        self.scrollable_frame.bind('<Configure>',
            lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox('all')))

        self.canvas_window = self.scroll_canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.scroll_canvas.bind('<Configure>', self.on_canvas_configure)
        self.scroll_canvas.configure(yscrollcommand=scrollbar.set)
        self.scroll_canvas.bind_all('<MouseWheel>', self.on_mousewheel)

        scrollbar.pack(side='right', fill='y')
        self.scroll_canvas.pack(side='left', fill='both', expand=True)

        return self.scrollable_frame

    def on_canvas_configure(self, event):
        self.scroll_canvas.itemconfig(self.canvas_window, width=event.width)

    def on_mousewheel(self, event):
        if self.scroll_canvas:
            self.scroll_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')

    def create_section_divider(self, parent, title=""):
        """Create a gold divider line with optional title"""
        divider_frame = tk.Frame(parent, bg=self.colors['bg'])
        divider_frame.pack(fill='x', pady=(15, 10))

        if title:
            tk.Label(divider_frame, text=title, font=('Segoe UI', 9, 'bold'),
                    bg=self.colors['bg'], fg=self.colors['accent']).pack(anchor='w')

        tk.Frame(divider_frame, bg=self.colors['divider'], height=2).pack(fill='x', pady=(3, 0))

    def clear_content(self):
        """Clear current content frame"""
        if self.current_frame:
            self.current_frame.destroy()
        if self.scroll_canvas:
            self.scroll_canvas.unbind_all('<MouseWheel>')
            self.scroll_canvas.master.destroy()
            self.scroll_canvas = None

    def show_welcome_screen(self):
        """Display 3-section welcome screen with black/gold theme"""
        self.clear_content()

        # Create scrollable container
        scrollable = self.create_scrollable_frame()
        self.current_frame = tk.Frame(scrollable, bg=self.colors['bg'])
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=12)

        # ═══════════════════════════════════════════════════════════════
        # SECTION 1: TOOL DESCRIPTION
        # ═══════════════════════════════════════════════════════════════
        tk.Label(self.current_frame,
            text="TOOL DESCRIPTION",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['accent']).pack(anchor='w')

        tk.Label(self.current_frame,
            text="Ingest files into the Trajanus Knowledge Base.\nFiles are chunked, embedded with OpenAI, and stored in Supabase for semantic search.",
            font=('Segoe UI', 9),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            justify='left').pack(anchor='w', pady=(4, 8))

        # Gold divider line
        tk.Frame(self.current_frame, bg=self.colors['divider'], height=2).pack(fill='x', pady=(0, 12))

        # ═══════════════════════════════════════════════════════════════
        # SECTION 2: INGEST MODE DESCRIPTIONS
        # ═══════════════════════════════════════════════════════════════
        tk.Label(self.current_frame,
            text="INGEST MODES",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['accent']).pack(anchor='w')

        # Mode explanations
        mode_info = tk.Frame(self.current_frame, bg=self.colors['bg'])
        mode_info.pack(fill='x', pady=(6, 8))

        tk.Label(mode_info,
            text="SINGLE FILE",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']).pack(anchor='w')
        tk.Label(mode_info,
            text="Select and ingest one file at a time. Best for adding individual documents or testing the ingest process.",
            font=('Segoe UI', 8),
            bg=self.colors['bg'],
            fg=self.colors['text_dim'],
            wraplength=560,
            justify='left').pack(anchor='w', pady=(0, 6))

        tk.Label(mode_info,
            text="BATCH FOLDER",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']).pack(anchor='w')
        tk.Label(mode_info,
            text="Select a folder and ingest all supported files within it. Processes .txt, .md, .json, .py and other text formats.",
            font=('Segoe UI', 8),
            bg=self.colors['bg'],
            fg=self.colors['text_dim'],
            wraplength=560,
            justify='left').pack(anchor='w', pady=(0, 6))

        tk.Label(mode_info,
            text="MULTI-SELECT",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']).pack(anchor='w')
        tk.Label(mode_info,
            text="Select multiple specific files from different locations. Hold Ctrl to select multiple files in the dialog.",
            font=('Segoe UI', 8),
            bg=self.colors['bg'],
            fg=self.colors['text_dim'],
            wraplength=560,
            justify='left').pack(anchor='w')

        # Gold divider line
        tk.Frame(self.current_frame, bg=self.colors['divider'], height=2).pack(fill='x', pady=(12, 12))

        # ═══════════════════════════════════════════════════════════════
        # SECTION 3: ACTION BUTTONS
        # ═══════════════════════════════════════════════════════════════
        tk.Label(self.current_frame,
            text="SELECT ACTION",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['accent']).pack(anchor='w', pady=(0, 8))

        # Category selection row
        cat_row = tk.Frame(self.current_frame, bg=self.colors['bg'])
        cat_row.pack(fill='x', pady=(0, 10))

        tk.Label(cat_row,
            text="CATEGORY:",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']).pack(side='left')

        categories = ["General", "Documentation", "Transcripts", "Research", "Code", "Meeting Notes", "Procedures"]
        cat_dropdown = ttk.Combobox(cat_row, textvariable=self.source_category,
            values=categories, state='readonly', width=18)
        cat_dropdown.pack(side='left', padx=(10, 0))

        # Button row
        btn_row = tk.Frame(self.current_frame, bg=self.colors['bg'])
        btn_row.pack(fill='x', pady=(0, 8))

        BeveledButton(btn_row, "SINGLE FILE",
                     command=self.select_single_file, width=140, height=36, palette=self.colors).pack(side='left', padx=(0, 10))
        BeveledButton(btn_row, "BATCH FOLDER",
                     command=self.select_folder, width=140, height=36, palette=self.colors).pack(side='left', padx=(0, 10))
        BeveledButton(btn_row, "MULTI-SELECT",
                     command=self.select_multiple_files, width=140, height=36, palette=self.colors).pack(side='left')

        # Exit button row
        exit_row = tk.Frame(self.current_frame, bg=self.colors['bg'])
        exit_row.pack(fill='x', pady=(4, 0))
        BeveledButton(exit_row, "EXIT", command=self.root.quit,
                     width=80, height=30, style='dark', palette=self.colors).pack(side='right')

    def create_mode_card(self, parent, title, subtitle, description, command, side='left'):
        """Create a mode selection card - entire card is clickable"""
        card = tk.Frame(parent, bg=self.colors['card'], padx=20, pady=20, cursor='hand2')
        card.pack(side=side, padx=(0, 15), fill='both', expand=True)

        def on_enter(e):
            card.config(bg=self.colors['sidebar'])
            for child in card.winfo_children():
                try:
                    child.config(bg=self.colors['sidebar'])
                except:
                    pass

        def on_leave(e):
            card.config(bg=self.colors['card'])
            for child in card.winfo_children():
                try:
                    child.config(bg=self.colors['card'])
                except:
                    pass

        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)
        card.bind('<Button-1>', lambda e: command())

        title_label = tk.Label(card,
            text=title,
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['accent'],
            cursor='hand2')
        title_label.pack(anchor='w')
        title_label.bind('<Button-1>', lambda e: command())

        subtitle_label = tk.Label(card,
            text=subtitle,
            font=('Segoe UI', 10),
            bg=self.colors['card'],
            fg=self.colors['text'],
            cursor='hand2')
        subtitle_label.pack(anchor='w', pady=(5, 0))
        subtitle_label.bind('<Button-1>', lambda e: command())

        desc_label = tk.Label(card,
            text=description,
            font=('Segoe UI', 9),
            bg=self.colors['card'],
            fg=self.colors['text_dim'],
            cursor='hand2')
        desc_label.pack(anchor='w', pady=(3, 15))
        desc_label.bind('<Button-1>', lambda e: command())

        btn = tk.Button(card,
            text=title,
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['accent'],
            fg='#1a1a1a',
            activebackground=self.colors['hover'],
            activeforeground='#1a1a1a',
            padx=20, pady=10,
            cursor='hand2',
            relief='flat',
            width=15,
            command=command)
        btn.pack(fill='x', pady=(5, 0))

    def show_progress_screen(self, total_files):
        """Display processing progress screen"""
        self.clear_content()

        self.current_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.current_frame.pack(fill='both', expand=True, padx=40, pady=30)

        tk.Label(self.current_frame,
            text="Processing Files...",
            font=('Segoe UI', 16),
            bg=self.colors['bg'],
            fg=self.colors['text']).pack(pady=(0, 20))

        progress_card = tk.Frame(self.current_frame, bg=self.colors['card'], padx=30, pady=25)
        progress_card.pack(fill='x', pady=(0, 20))

        self.progress_status = tk.Label(progress_card,
            text="Preparing...",
            font=('Segoe UI', 11),
            bg=self.colors['card'],
            fg=self.colors['text'])
        self.progress_status.pack(anchor='w', pady=(0, 15))

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Gold.Horizontal.TProgressbar",
            troughcolor=self.colors['border'],
            background=self.colors['accent'],
            darkcolor=self.colors['accent'],
            lightcolor=self.colors['accent'],
            bordercolor=self.colors['border'])

        self.progress_bar = ttk.Progressbar(progress_card,
            style="Gold.Horizontal.TProgressbar",
            length=500,
            mode='determinate')
        self.progress_bar.pack(fill='x', pady=(0, 10))

        self.progress_text = tk.Label(progress_card,
            text=f"0 of {total_files} files",
            font=('Segoe UI', 10),
            bg=self.colors['card'],
            fg=self.colors['text_dim'])
        self.progress_text.pack(anchor='w')

        stats_frame = tk.Frame(progress_card, bg=self.colors['card'])
        stats_frame.pack(fill='x', pady=(20, 0))

        self.live_processed = self.create_live_stat(stats_frame, "Processed:", "0", self.colors['success'])
        self.live_chunks = self.create_live_stat(stats_frame, "Chunks:", "0", self.colors['accent'])
        self.live_errors = self.create_live_stat(stats_frame, "Errors:", "0", self.colors['error'])

        self.current_file_label = tk.Label(self.current_frame,
            text="",
            font=('Consolas', 9),
            bg=self.colors['bg'],
            fg=self.colors['text_dim'])
        self.current_file_label.pack(pady=(10, 0))

        # Log area
        log_frame = tk.Frame(self.current_frame, bg=self.colors['sidebar'])
        log_frame.pack(fill='both', expand=True, pady=(15, 0))

        tk.Label(log_frame, text="PROCESSING LOG",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['border'],
            fg=self.colors['accent']).pack(fill='x', pady=5)

        self.log_text = tk.Text(log_frame,
            bg=self.colors['sidebar'],
            fg=self.colors['accent'],
            font=('Consolas', 9),
            height=8,
            wrap='word',
            state='disabled')
        self.log_text.pack(fill='both', expand=True, padx=10, pady=10)

    def create_live_stat(self, parent, label, value, color):
        """Create a live stat display"""
        frame = tk.Frame(parent, bg=self.colors['card'])
        frame.pack(side='left', padx=(0, 30))

        tk.Label(frame, text=label, font=('Segoe UI', 10),
            bg=self.colors['card'], fg=self.colors['text_dim']).pack(side='left')

        val_label = tk.Label(frame, text=value, font=('Segoe UI', 10, 'bold'),
            bg=self.colors['card'], fg=color)
        val_label.pack(side='left', padx=(5, 0))
        return val_label

    def log(self, message):
        """Add message to log"""
        def do_log():
            self.log_text.config(state='normal')
            self.log_text.insert('end', message + '\n')
            self.log_text.see('end')
            self.log_text.config(state='disabled')
        self.root.after(0, do_log)

    def show_completion_screen(self):
        """Display completion screen with results"""
        self.clear_content()

        self.current_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.current_frame.pack(fill='both', expand=True, padx=40, pady=30)

        header_frame = tk.Frame(self.current_frame, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, 20))

        tk.Label(header_frame,
            text="INGESTION COMPLETE",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['success']).pack(side='left')

        summary_card = tk.Frame(self.current_frame, bg=self.colors['card'], padx=25, pady=20)
        summary_card.pack(fill='x', pady=(0, 20))

        stats_frame = tk.Frame(summary_card, bg=self.colors['card'])
        stats_frame.pack(fill='x')

        self.create_result_stat(stats_frame, "Processed", len(self.processed_files), self.colors['success'])
        self.create_result_stat(stats_frame, "Chunks Added", self.total_chunks, self.colors['accent'])
        self.create_result_stat(stats_frame, "Errors", len(self.error_files), self.colors['error'])

        if self.processed_files:
            self.create_file_list("PROCESSED FILES", self.processed_files, self.colors['success'])

        if self.error_files:
            self.create_file_list("FAILED FILES", self.error_files, self.colors['error'])

        btn_frame = tk.Frame(self.current_frame, bg=self.colors['bg'])
        btn_frame.pack(fill='x', pady=(20, 0))

        more_btn = tk.Button(btn_frame,
            text="Ingest More Files",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['accent'],
            fg='#1a1a1a',
            activebackground=self.colors['hover'],
            activeforeground='#1a1a1a',
            padx=25, pady=10,
            cursor='hand2',
            relief='flat',
            command=self.show_welcome_screen)
        more_btn.pack(side='left')

        exit_btn = tk.Button(btn_frame,
            text="Exit",
            font=('Segoe UI', 11),
            bg=self.colors['border'],
            fg=self.colors['text'],
            activebackground='#444444',
            activeforeground=self.colors['text'],
            padx=35, pady=10,
            cursor='hand2',
            relief='flat',
            command=self.root.quit)
        exit_btn.pack(side='right')

    def create_result_stat(self, parent, label, value, color):
        """Create a result statistic display"""
        frame = tk.Frame(parent, bg=self.colors['card'])
        frame.pack(side='left', padx=(0, 40))

        tk.Label(frame, text=str(value), font=('Segoe UI', 24, 'bold'),
            bg=self.colors['card'], fg=color).pack()
        tk.Label(frame, text=label, font=('Segoe UI', 10),
            bg=self.colors['card'], fg=self.colors['text_dim']).pack()

    def create_file_list(self, title, files, color):
        """Create a scrollable file list"""
        list_frame = tk.Frame(self.current_frame, bg=self.colors['sidebar'])
        list_frame.pack(fill='x', pady=(0, 15))

        header = tk.Frame(list_frame, bg=self.colors['border'])
        header.pack(fill='x')
        tk.Label(header, text=title, font=('Segoe UI', 9, 'bold'),
            bg=self.colors['border'], fg=color,
            padx=15, pady=5).pack(anchor='w')

        display_files = files[:5]
        for f in display_files:
            tk.Label(list_frame, text=f"  {f}", font=('Consolas', 9),
                bg=self.colors['sidebar'], fg=self.colors['accent'],
                anchor='w').pack(fill='x', padx=10, pady=2)

        if len(files) > 5:
            tk.Label(list_frame, text=f"  ... and {len(files) - 5} more",
                font=('Consolas', 9, 'italic'),
                bg=self.colors['sidebar'], fg=self.colors['accent'],
                anchor='w').pack(fill='x', padx=10, pady=2)

    # ==================== FILE SELECTION ====================

    def select_single_file(self):
        """Select a single file to ingest"""
        if not self.supabase:
            messagebox.showerror("Error", "Not connected to services.\nPlease wait for connection.")
            return

        self.root.attributes('-topmost', False)
        self.root.update()

        file = filedialog.askopenfilename(
            title="Select File to Ingest",
            initialdir="G:/My Drive/00 - Trajanus USA",
            filetypes=[
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
                ("JSON files", "*.json"),
                ("Python files", "*.py"),
                ("All files", "*.*")
            ],
            parent=self.root)

        self.root.lift()
        self.root.focus_force()

        if file:
            self.process_files([Path(file)])

    def select_folder(self):
        """Select a folder to ingest all supported files"""
        if not self.supabase:
            messagebox.showerror("Error", "Not connected to services.\nPlease wait for connection.")
            return

        self.root.attributes('-topmost', False)
        self.root.update()

        folder = filedialog.askdirectory(
            title="Select Folder to Ingest",
            initialdir="G:/My Drive/00 - Trajanus USA",
            parent=self.root)

        self.root.lift()
        self.root.focus_force()

        if folder:
            supported = ['.txt', '.md', '.json', '.py', '.js', '.html', '.css', '.yaml', '.xml']
            files = []
            for ext in supported:
                files.extend(Path(folder).glob(f'*{ext}'))

            if files:
                self.process_files(files)
            else:
                messagebox.showinfo("No Files", f"No supported files found in:\n{folder}")

    def select_multiple_files(self):
        """Select multiple files to ingest"""
        if not self.supabase:
            messagebox.showerror("Error", "Not connected to services.\nPlease wait for connection.")
            return

        self.root.attributes('-topmost', False)
        self.root.update()

        files = filedialog.askopenfilenames(
            title="Select Files to Ingest (Ctrl+Click for multiple)",
            initialdir="G:/My Drive/00 - Trajanus USA",
            filetypes=[
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
                ("JSON files", "*.json"),
                ("Python files", "*.py"),
                ("All files", "*.*")
            ],
            parent=self.root)

        self.root.lift()
        self.root.focus_force()

        if files:
            self.process_files([Path(f) for f in files])

    # ==================== PROCESSING ====================

    def chunk_text(self, text, chunk_size=1000, overlap=200):
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            if end < len(text):
                search_start = max(start, end - 100)
                sentence_end = max(
                    text.rfind('. ', search_start, end),
                    text.rfind('! ', search_start, end),
                    text.rfind('? ', search_start, end)
                )
                if sentence_end != -1:
                    end = sentence_end + 1
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start = end - overlap
        return chunks

    def process_files(self, files):
        """Process a list of files"""
        if not files:
            return

        self.processed_files = []
        self.skipped_files = []
        self.error_files = []
        self.total_chunks = 0

        self.show_progress_screen(len(files))
        self.processing = True

        def do_process():
            total = len(files)
            category = self.source_category.get()

            for i, filepath in enumerate(sorted(files)):
                percent = ((i + 1) / total) * 100
                self.root.after(0, lambda p=percent: self.progress_bar.configure(value=p))
                self.root.after(0, lambda i=i, t=total: self.progress_text.config(
                    text=f"{i + 1} of {t} files"))
                self.root.after(0, lambda f=filepath.name: self.current_file_label.config(
                    text=f"Processing: {f}"))

                chunks_added = self.process_single_file(filepath, category)

                if chunks_added > 0:
                    self.processed_files.append(filepath.name)
                    self.total_chunks += chunks_added
                    self.root.after(0, lambda: self.live_processed.config(
                        text=str(len(self.processed_files))))
                    self.root.after(0, lambda c=self.total_chunks: self.live_chunks.config(
                        text=str(c)))
                elif chunks_added == 0:
                    self.skipped_files.append(filepath.name)
                else:
                    self.error_files.append(filepath.name)
                    self.root.after(0, lambda: self.live_errors.config(
                        text=str(len(self.error_files))))

            self.processing = False
            self.root.after(0, self.show_completion_screen)

        threading.Thread(target=do_process, daemon=True).start()

    def process_single_file(self, filepath, category):
        """Process a single file and return chunks added"""
        self.log(f"Processing: {filepath.name}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.log(f"  ERROR: Could not read file - {e}")
            return -1

        if len(content) < 50:
            self.log(f"  SKIP: File too short ({len(content)} chars)")
            return 0

        chunks = self.chunk_text(content)
        self.log(f"  Created {len(chunks)} chunks")

        added = 0
        for i, chunk in enumerate(chunks, 1):
            try:
                response = self.openai_client.embeddings.create(
                    input=chunk,
                    model="text-embedding-3-small"
                )
                embedding = response.data[0].embedding
            except Exception as e:
                self.log(f"  ERROR: Chunk {i} embedding failed")
                continue

            try:
                relative_path = str(filepath).replace("G:\\My Drive\\00 - Trajanus USA\\", "")
                data = {
                    "url": f"file:///{relative_path}",
                    "chunk_number": i,
                    "title": f"{filepath.stem} (Part {i})",
                    "summary": ' '.join(chunk.split()[:20]) + '...',
                    "content": chunk,
                    "metadata": {
                        "source": category,
                        "filename": filepath.name,
                        "file_type": filepath.suffix,
                        "total_chunks": len(chunks),
                        "processed_at": datetime.now().isoformat()
                    },
                    "embedding": embedding
                }
                self.supabase.table('knowledge_base').insert(data).execute()
                added += 1
                time.sleep(0.1)
            except Exception as e:
                if '23505' not in str(e):
                    self.log(f"  ERROR: Chunk {i} DB insert failed")

        self.log(f"  DONE: Added {added}/{len(chunks)} chunks")
        return added

    # ==================== SERVICES ====================

    def connect_services(self):
        """Connect to Supabase and OpenAI"""
        def do_connect():
            try:
                self.load_env()

                from openai import OpenAI
                from supabase import create_client

                self.supabase = create_client(
                    os.getenv('SUPABASE_URL'),
                    os.getenv('SUPABASE_ANON_KEY')
                )
                self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

                self.root.after(0, lambda: self.connection_status.config(
                    text="Connected", fg=self.colors['success']))
            except Exception as e:
                self.root.after(0, lambda: self.connection_status.config(
                    text="Connection Failed", fg=self.colors['error']))

        threading.Thread(target=do_connect, daemon=True).start()

    def load_env(self):
        """Load .env file"""
        env_path = Path('G:/My Drive/00 - Trajanus USA/00-Command-Center/.env')
        with open(env_path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

    def run(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        self.root.mainloop()


def main():
    app = TrajanusBatchIngestGUI()
    app.run()


if __name__ == '__main__':
    main()
