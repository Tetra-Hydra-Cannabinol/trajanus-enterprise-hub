#!/usr/bin/env python3
"""
TRAJANUS QUERY KB TOOL
Search and browse the knowledge base
Enhanced with 3D buttons and scrollable interface
"""

import os
import sys
import io
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

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
                'face': palette.get('btn_face', '#c0c0c0'),
                'light': palette.get('btn_light', '#e0e0e0'),
                'dark': palette.get('btn_dark', '#808080'),
                'text': palette.get('btn_text', '#1a1a1a'),
                'glow': palette.get('btn_glow', '#f0f0f0')
            }
        elif palette and style == 'dark':
            self.colors = {
                'face': palette.get('bg_light', '#1b263b'),
                'light': palette.get('border', '#2d4a6a'),
                'dark': palette.get('bg', '#0d1b2a'),
                'text': palette.get('text', '#ffffff'),
                'glow': palette.get('border', '#3a5a7a')
            }
        else:
            # Fallback schemes
            schemes = {
                'primary': {
                    'face': '#c0c0c0', 'light': '#e0e0e0', 'dark': '#808080',
                    'text': '#1a1a1a', 'glow': '#f0f0f0'
                },
                'dark': {
                    'face': '#404040', 'light': '#606060', 'dark': '#252525',
                    'text': '#ffffff', 'glow': '#555555'
                }
            }
            self.colors = schemes.get(style, schemes['primary'])

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


class TrajanusQueryKBGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Trajanus - Knowledge Base Query")
        self.root.geometry("620x420")
        self.root.resizable(True, True)
        self.root.minsize(550, 380)

        # ============ COLOR PALETTES ============
        # Change ACTIVE_PALETTE to test different themes
        ACTIVE_PALETTE = "navy_silver"  # Options: gold, navy_silver, ocean, forest, midnight, green_silver, black_silver, black_red, brown_orange, navy_gold, black_gold

        PALETTES = {
            'gold': {
                'bg': '#1a1a1a',
                'bg_light': '#2d2d2d',
                'card': '#363636',
                'accent': '#d4a574',
                'hover': '#e8922a',
                'text': '#ffffff',
                'text_dim': '#888888',
                'success': '#4a9f4a',
                'warning': '#e8922a',
                'error': '#e74c3c',
                'border': '#444444',
                'divider': '#d4a574',
                'btn_face': '#d4a574',
                'btn_light': '#f0c896',
                'btn_dark': '#8a6b4a',
                'btn_text': '#1a1a1a',
                'btn_glow': '#ffe4c4'
            },
            'navy_silver': {
                'bg': '#0d1b2a',
                'bg_light': '#1b263b',
                'card': '#243447',
                'accent': '#c0c0c0',
                'hover': '#e0e0e0',
                'text': '#ffffff',
                'text_dim': '#8892a0',
                'success': '#4a9f4a',
                'warning': '#e8922a',
                'error': '#e74c3c',
                'border': '#2d4a6a',
                'divider': '#c0c0c0',
                'btn_face': '#c0c0c0',
                'btn_light': '#e0e0e0',
                'btn_dark': '#808080',
                'btn_text': '#0d1b2a',
                'btn_glow': '#f0f0f0'
            },
            'ocean': {
                'bg': '#0a1628',
                'bg_light': '#112240',
                'card': '#1a3a5c',
                'accent': '#64b5f6',
                'hover': '#90caf9',
                'text': '#ffffff',
                'text_dim': '#8aa8c7',
                'success': '#4a9f4a',
                'warning': '#e8922a',
                'error': '#e74c3c',
                'border': '#1e4976',
                'divider': '#64b5f6',
                'btn_face': '#64b5f6',
                'btn_light': '#90caf9',
                'btn_dark': '#1976d2',
                'btn_text': '#0a1628',
                'btn_glow': '#bbdefb'
            },
            'forest': {
                'bg': '#0d1f0d',
                'bg_light': '#1a3a1a',
                'card': '#245024',
                'accent': '#81c784',
                'hover': '#a5d6a7',
                'text': '#ffffff',
                'text_dim': '#8faf8f',
                'success': '#4caf50',
                'warning': '#e8922a',
                'error': '#e74c3c',
                'border': '#2e6b2e',
                'divider': '#81c784',
                'btn_face': '#81c784',
                'btn_light': '#a5d6a7',
                'btn_dark': '#388e3c',
                'btn_text': '#0d1f0d',
                'btn_glow': '#c8e6c9'
            },
            'midnight': {
                'bg': '#1a1a2e',
                'bg_light': '#252542',
                'card': '#2d2d4a',
                'accent': '#b39ddb',
                'hover': '#d1c4e9',
                'text': '#ffffff',
                'text_dim': '#9090b0',
                'success': '#4a9f4a',
                'warning': '#e8922a',
                'error': '#e74c3c',
                'border': '#3d3d6b',
                'divider': '#b39ddb',
                'btn_face': '#b39ddb',
                'btn_light': '#d1c4e9',
                'btn_dark': '#7e57c2',
                'btn_text': '#1a1a2e',
                'btn_glow': '#ede7f6'
            },
            'green_silver': {
                'bg': '#0a1a0a',
                'bg_light': '#1a2a1a',
                'card': '#243424',
                'accent': '#c0c0c0',
                'hover': '#e0e0e0',
                'text': '#ffffff',
                'text_dim': '#8a9a8a',
                'success': '#4a9f4a',
                'warning': '#e8922a',
                'error': '#e74c3c',
                'border': '#2a4a2a',
                'divider': '#c0c0c0',
                'btn_face': '#c0c0c0',
                'btn_light': '#e0e0e0',
                'btn_dark': '#808080',
                'btn_text': '#0a1a0a',
                'btn_glow': '#f0f0f0'
            },
            'black_silver': {
                'bg': '#0a0a0a',
                'bg_light': '#1a1a1a',
                'card': '#252525',
                'accent': '#c0c0c0',
                'hover': '#e0e0e0',
                'text': '#ffffff',
                'text_dim': '#888888',
                'success': '#4a9f4a',
                'warning': '#e8922a',
                'error': '#e74c3c',
                'border': '#333333',
                'divider': '#c0c0c0',
                'btn_face': '#c0c0c0',
                'btn_light': '#e0e0e0',
                'btn_dark': '#808080',
                'btn_text': '#0a0a0a',
                'btn_glow': '#f0f0f0'
            },
            'black_red': {
                'bg': '#0a0a0a',
                'bg_light': '#1a1a1a',
                'card': '#252525',
                'accent': '#e53935',
                'hover': '#ff6659',
                'text': '#ffffff',
                'text_dim': '#888888',
                'success': '#4a9f4a',
                'warning': '#e8922a',
                'error': '#e74c3c',
                'border': '#333333',
                'divider': '#e53935',
                'btn_face': '#e53935',
                'btn_light': '#ff6659',
                'btn_dark': '#a00000',
                'btn_text': '#ffffff',
                'btn_glow': '#ff8a80'
            },
            'brown_orange': {
                'bg': '#1a120a',
                'bg_light': '#2a1f14',
                'card': '#3a2a1a',
                'accent': '#ff9800',
                'hover': '#ffb74d',
                'text': '#ffffff',
                'text_dim': '#a08060',
                'success': '#4a9f4a',
                'warning': '#e8922a',
                'error': '#e74c3c',
                'border': '#4a3a2a',
                'divider': '#ff9800',
                'btn_face': '#ff9800',
                'btn_light': '#ffb74d',
                'btn_dark': '#c66900',
                'btn_text': '#1a120a',
                'btn_glow': '#ffe0b2'
            },
            'navy_gold': {
                'bg': '#0d1b2a',
                'bg_light': '#1b263b',
                'card': '#243447',
                'accent': '#d4a574',
                'hover': '#e8b88a',
                'text': '#ffffff',
                'text_dim': '#8892a0',
                'success': '#4a9f4a',
                'warning': '#e8922a',
                'error': '#e74c3c',
                'border': '#2d4a6a',
                'divider': '#d4a574',
                'btn_face': '#d4a574',
                'btn_light': '#f0c896',
                'btn_dark': '#8a6b4a',
                'btn_text': '#0d1b2a',
                'btn_glow': '#ffe4c4'
            },
            'black_gold': {
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
        }

        self.colors = PALETTES[ACTIVE_PALETTE]

        self.root.configure(bg=self.colors['bg'])

        # State
        self.supabase = None
        self.openai_client = None
        self.searching = False
        self.sources_list = []

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
            text="TRAJANUS KNOWLEDGE BASE QUERY",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['accent'],
            fg='#1a1a1a')
        title.pack(pady=5)

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
            text="Query and retrieve documents from the Trajanus Knowledge Base.\nSupports AI-powered semantic search, category browsing, and recent document access.",
            font=('Segoe UI', 9),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            justify='left').pack(anchor='w', pady=(4, 8))

        # Gold divider line
        tk.Frame(self.current_frame, bg=self.colors['divider'], height=2).pack(fill='x', pady=(0, 12))

        # ═══════════════════════════════════════════════════════════════
        # SECTION 2: SEARCH TYPE DESCRIPTIONS
        # ═══════════════════════════════════════════════════════════════
        tk.Label(self.current_frame,
            text="SEARCH TYPES",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['accent']).pack(anchor='w')

        # Search type explanations
        search_info = tk.Frame(self.current_frame, bg=self.colors['bg'])
        search_info.pack(fill='x', pady=(6, 8))

        tk.Label(search_info,
            text="SEMANTIC SEARCH",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']).pack(anchor='w')
        tk.Label(search_info,
            text="Find documents using AI-powered natural language matching. Enter any query and the system finds relevant content based on meaning, not just keywords.",
            font=('Segoe UI', 8),
            bg=self.colors['bg'],
            fg=self.colors['text_dim'],
            wraplength=560,
            justify='left').pack(anchor='w', pady=(0, 6))

        tk.Label(search_info,
            text="BROWSE SOURCES",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']).pack(anchor='w')
        tk.Label(search_info,
            text="Navigate documents organized by category and document type. View the full catalog structure and select specific documents to examine.",
            font=('Segoe UI', 8),
            bg=self.colors['bg'],
            fg=self.colors['text_dim'],
            wraplength=560,
            justify='left').pack(anchor='w', pady=(0, 6))

        tk.Label(search_info,
            text="RECENT",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']).pack(anchor='w')
        tk.Label(search_info,
            text="View the most recently added documents to the knowledge base. Useful for finding new content and tracking what's been ingested.",
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

        # Button row
        btn_row = tk.Frame(self.current_frame, bg=self.colors['bg'])
        btn_row.pack(fill='x', pady=(0, 8))

        BeveledButton(btn_row, "SEMANTIC SEARCH",
                     command=self.show_search_screen, width=160, height=36, palette=self.colors).pack(side='left', padx=(0, 10))
        BeveledButton(btn_row, "BROWSE SOURCES",
                     command=self.show_sources_screen, width=160, height=36, palette=self.colors).pack(side='left', padx=(0, 10))
        BeveledButton(btn_row, "RECENT",
                     command=self.show_recent_screen, width=100, height=36, palette=self.colors).pack(side='left')

        # Exit button row
        exit_row = tk.Frame(self.current_frame, bg=self.colors['bg'])
        exit_row.pack(fill='x', pady=(4, 0))
        BeveledButton(exit_row, "EXIT", command=self.root.quit,
                     width=80, height=30, style='dark', palette=self.colors).pack(side='right')

    def show_results_screen(self, filename, operation, results):
        """Display results after a search operation with file actions"""
        self.clear_content()

        # Create scrollable container
        scrollable = self.create_scrollable_frame()
        self.current_frame = tk.Frame(scrollable, bg=self.colors['bg'])
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=12)

        # ═══════════════════════════════════════════════════════════════
        # SECTION 1: OPERATION RESULTS
        # ═══════════════════════════════════════════════════════════════
        tk.Label(self.current_frame,
            text="OPERATION RESULTS",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['accent']).pack(anchor='w')

        # Results info
        info_frame = tk.Frame(self.current_frame, bg=self.colors['bg'])
        info_frame.pack(fill='x', pady=(8, 8))

        # Filename
        tk.Label(info_frame,
            text=f"FILENAME: {filename}",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']).pack(anchor='w')

        # Operation
        tk.Label(info_frame,
            text=f"OPERATION: {operation}",
            font=('Segoe UI', 9),
            bg=self.colors['bg'],
            fg=self.colors['text_dim']).pack(anchor='w', pady=(2, 0))

        # Results
        tk.Label(info_frame,
            text=f"RESULTS: {results}",
            font=('Segoe UI', 9),
            bg=self.colors['bg'],
            fg=self.colors['success']).pack(anchor='w', pady=(2, 0))

        # Gold divider line
        tk.Frame(self.current_frame, bg=self.colors['divider'], height=2).pack(fill='x', pady=(12, 12))

        # ═══════════════════════════════════════════════════════════════
        # SECTION 2: FILE ACTIONS
        # ═══════════════════════════════════════════════════════════════
        tk.Label(self.current_frame,
            text="FILE ACTIONS",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['accent']).pack(anchor='w', pady=(0, 8))

        # Action buttons
        action_row = tk.Frame(self.current_frame, bg=self.colors['bg'])
        action_row.pack(fill='x', pady=(0, 8))

        BeveledButton(action_row, "SAVE",
                     command=lambda: self.file_action('save'), width=120, height=36, palette=self.colors).pack(side='left', padx=(0, 10))
        BeveledButton(action_row, "DOWNLOAD",
                     command=lambda: self.file_action('download'), width=120, height=36, palette=self.colors).pack(side='left', padx=(0, 10))
        BeveledButton(action_row, "ADD TO PROJECT",
                     command=lambda: self.file_action('add_project'), width=140, height=36, palette=self.colors).pack(side='left')

        # Gold divider line
        tk.Frame(self.current_frame, bg=self.colors['divider'], height=2).pack(fill='x', pady=(12, 12))

        # Navigation
        nav_row = tk.Frame(self.current_frame, bg=self.colors['bg'])
        nav_row.pack(fill='x')
        BeveledButton(nav_row, "BACK",
                     command=self.show_welcome_screen, width=80, height=30, style='dark', palette=self.colors).pack(side='left')
        BeveledButton(nav_row, "EXIT", command=self.root.quit,
                     width=80, height=30, style='dark', palette=self.colors).pack(side='right')

    def file_action(self, action_type):
        """Handle file actions - placeholder for future implementation"""
        from tkinter import filedialog
        if action_type == 'save':
            path = filedialog.asksaveasfilename(title="Save File As")
            if path:
                self.connection_label.config(text=f"Save location: {path}")
        elif action_type == 'download':
            path = filedialog.askdirectory(title="Select Download Location")
            if path:
                self.connection_label.config(text=f"Download to: {path}")
        elif action_type == 'add_project':
            path = filedialog.askdirectory(title="Select Project Folder")
            if path:
                self.connection_label.config(text=f"Add to project: {path}")

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

    # ==================== SEARCH SCREEN ====================

    def show_search_screen(self):
        """Display semantic search screen"""
        self.clear_content()

        self.current_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.current_frame.pack(fill='both', expand=True, padx=40, pady=30)

        # Title
        tk.Label(self.current_frame,
            text="Semantic Search",
            font=('Segoe UI', 16),
            bg=self.colors['bg'],
            fg=self.colors['text']).pack(pady=(0, 20))

        # Search input card
        search_card = tk.Frame(self.current_frame, bg=self.colors['card'], padx=25, pady=20)
        search_card.pack(fill='x', pady=(0, 20))

        tk.Label(search_card,
            text="Enter your query:",
            font=('Segoe UI', 11),
            bg=self.colors['card'],
            fg=self.colors['text']).pack(anchor='w', pady=(0, 10))

        self.search_entry = tk.Entry(search_card,
            font=('Segoe UI', 12),
            bg=self.colors['sidebar'],
            fg=self.colors['accent'],
            insertbackground=self.colors['accent'],
            relief='flat',
            width=60)
        self.search_entry.pack(fill='x', pady=(0, 15), ipady=8)
        self.search_entry.bind('<Return>', lambda e: self.do_search())

        # Options row
        options_frame = tk.Frame(search_card, bg=self.colors['card'])
        options_frame.pack(fill='x')

        tk.Label(options_frame, text="Results:", font=('Segoe UI', 10),
            bg=self.colors['card'], fg=self.colors['text_dim']).pack(side='left')

        self.limit_var = tk.StringVar(value="5")
        limit_combo = ttk.Combobox(options_frame, textvariable=self.limit_var,
            values=["3", "5", "10", "15", "20"], state='readonly', width=5)
        limit_combo.pack(side='left', padx=(10, 30))

        search_btn = tk.Button(options_frame,
            text="Search",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['accent'],
            fg='#1a1a1a',
            activebackground=self.colors['hover'],
            activeforeground='#1a1a1a',
            padx=25, pady=5,
            cursor='hand2',
            relief='flat',
            command=self.do_search)
        search_btn.pack(side='right')

        # Results area
        results_header = tk.Frame(self.current_frame, bg=self.colors['border'])
        results_header.pack(fill='x')
        tk.Label(results_header, text="RESULTS",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['border'],
            fg=self.colors['accent'],
            pady=5).pack(anchor='w', padx=15)

        # Scrollable results frame
        results_container = tk.Frame(self.current_frame, bg=self.colors['sidebar'])
        results_container.pack(fill='both', expand=True)

        canvas = tk.Canvas(results_container, bg=self.colors['sidebar'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(results_container, orient='vertical', command=canvas.yview)
        self.results_frame = tk.Frame(canvas, bg=self.colors['sidebar'])

        self.results_frame.bind('<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        canvas.create_window((0, 0), window=self.results_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Initial message
        tk.Label(self.results_frame,
            text="Enter a query and click Search",
            font=('Segoe UI', 11),
            bg=self.colors['sidebar'],
            fg=self.colors['text_dim']).pack(pady=20)

        # Bottom buttons
        btn_frame = tk.Frame(self.current_frame, bg=self.colors['bg'])
        btn_frame.pack(fill='x', pady=(15, 0))

        back_btn = tk.Button(btn_frame,
            text="Back to Menu",
            font=('Segoe UI', 10),
            bg=self.colors['border'],
            fg=self.colors['text'],
            activebackground='#444444',
            activeforeground=self.colors['text'],
            padx=20, pady=8,
            cursor='hand2',
            relief='flat',
            command=self.show_welcome_screen)
        back_btn.pack(side='left')

    def do_search(self):
        """Perform semantic search"""
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query")
            return

        if not self.supabase:
            messagebox.showerror("Error", "Not connected to services")
            return

        # Clear results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        tk.Label(self.results_frame,
            text="Searching...",
            font=('Segoe UI', 11),
            bg=self.colors['sidebar'],
            fg=self.colors['warning']).pack(pady=20)

        def do_query():
            try:
                # Generate embedding
                response = self.openai_client.embeddings.create(
                    input=query,
                    model="text-embedding-3-small"
                )
                query_embedding = response.data[0].embedding

                # Search
                limit = int(self.limit_var.get())
                result = self.supabase.rpc(
                    'match_knowledge_base',
                    {
                        'query_embedding': query_embedding,
                        'match_threshold': 0.3,
                        'match_count': limit
                    }
                ).execute()

                docs = result.data
                self.root.after(0, lambda: self.display_results(docs))

            except Exception as e:
                self.root.after(0, lambda: self.display_error(str(e)))

        threading.Thread(target=do_query, daemon=True).start()

    def display_results(self, docs):
        """Display search results"""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if not docs:
            tk.Label(self.results_frame,
                text="No results found",
                font=('Segoe UI', 11),
                bg=self.colors['sidebar'],
                fg=self.colors['text_dim']).pack(pady=20)
            return

        for i, doc in enumerate(docs, 1):
            self.create_result_card(doc, i)

    def create_result_card(self, doc, index):
        """Create a result card"""
        card = tk.Frame(self.results_frame, bg=self.colors['card'], padx=15, pady=12)
        card.pack(fill='x', padx=10, pady=5)

        # Header row
        header = tk.Frame(card, bg=self.colors['card'])
        header.pack(fill='x')

        similarity = doc.get('similarity', 0) * 100
        tk.Label(header,
            text=f"#{index}",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['accent']).pack(side='left')

        tk.Label(header,
            text=f"{similarity:.0f}% match",
            font=('Segoe UI', 9),
            bg=self.colors['card'],
            fg=self.colors['success'] if similarity > 70 else self.colors['warning']).pack(side='right')

        # Title
        tk.Label(card,
            text=doc.get('title', 'Untitled'),
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text'],
            anchor='w').pack(fill='x', pady=(5, 0))

        # Source
        source = doc.get('metadata', {}).get('source', 'Unknown')
        tk.Label(card,
            text=f"Source: {source}",
            font=('Segoe UI', 9),
            bg=self.colors['card'],
            fg=self.colors['text_dim'],
            anchor='w').pack(fill='x')

        # Content preview
        content = doc.get('content', '')[:200] + '...'
        tk.Label(card,
            text=content,
            font=('Consolas', 9),
            bg=self.colors['card'],
            fg=self.colors['accent'],
            anchor='w',
            wraplength=600,
            justify='left').pack(fill='x', pady=(5, 0))

    def display_error(self, error):
        """Display error message"""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        tk.Label(self.results_frame,
            text=f"Error: {error}",
            font=('Segoe UI', 11),
            bg=self.colors['sidebar'],
            fg=self.colors['error']).pack(pady=20)

    # ==================== SOURCES SCREEN ====================

    def show_sources_screen(self):
        """Display browse by sources screen"""
        self.clear_content()

        self.current_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.current_frame.pack(fill='both', expand=True, padx=40, pady=30)

        tk.Label(self.current_frame,
            text="Browse by Source",
            font=('Segoe UI', 16),
            bg=self.colors['bg'],
            fg=self.colors['text']).pack(pady=(0, 20))

        # Sources list
        sources_header = tk.Frame(self.current_frame, bg=self.colors['border'])
        sources_header.pack(fill='x')
        tk.Label(sources_header, text="AVAILABLE SOURCES",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['border'],
            fg=self.colors['accent'],
            pady=5).pack(anchor='w', padx=15)

        self.sources_frame = tk.Frame(self.current_frame, bg=self.colors['sidebar'])
        self.sources_frame.pack(fill='both', expand=True)

        tk.Label(self.sources_frame,
            text="Loading sources...",
            font=('Segoe UI', 11),
            bg=self.colors['sidebar'],
            fg=self.colors['warning']).pack(pady=20)

        # Bottom buttons
        btn_frame = tk.Frame(self.current_frame, bg=self.colors['bg'])
        btn_frame.pack(fill='x', pady=(15, 0))

        back_btn = tk.Button(btn_frame,
            text="Back to Menu",
            font=('Segoe UI', 10),
            bg=self.colors['border'],
            fg=self.colors['text'],
            padx=20, pady=8,
            cursor='hand2',
            relief='flat',
            command=self.show_welcome_screen)
        back_btn.pack(side='left')

        # Load sources
        self.load_sources()

    def load_sources(self):
        """Load available sources"""
        def do_load():
            try:
                result = self.supabase.table('knowledge_base').select('metadata').execute()

                sources = {}
                for doc in result.data:
                    source = doc.get('metadata', {}).get('source', 'Unknown')
                    sources[source] = sources.get(source, 0) + 1

                self.sources_list = sorted(sources.items(), key=lambda x: x[1], reverse=True)
                self.root.after(0, self.display_sources)

            except Exception as e:
                self.root.after(0, lambda: self.display_error(str(e)))

        threading.Thread(target=do_load, daemon=True).start()

    def display_sources(self):
        """Display sources list"""
        for widget in self.sources_frame.winfo_children():
            widget.destroy()

        for source, count in self.sources_list:
            self.create_source_card(source, count)

    def create_source_card(self, source, count):
        """Create a source card"""
        card = tk.Frame(self.sources_frame, bg=self.colors['card'], padx=15, pady=10, cursor='hand2')
        card.pack(fill='x', padx=10, pady=3)

        def on_click(e=None):
            self.browse_source(source)

        card.bind('<Button-1>', on_click)

        tk.Label(card,
            text=source,
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['accent'],
            cursor='hand2').pack(side='left')

        tk.Label(card,
            text=f"{count} chunks",
            font=('Segoe UI', 10),
            bg=self.colors['card'],
            fg=self.colors['text_dim'],
            cursor='hand2').pack(side='right')

    def browse_source(self, source):
        """Browse documents from a specific source"""
        if not self.supabase:
            return

        # Show loading
        for widget in self.sources_frame.winfo_children():
            widget.destroy()

        tk.Label(self.sources_frame,
            text=f"Loading documents from: {source}",
            font=('Segoe UI', 11),
            bg=self.colors['sidebar'],
            fg=self.colors['warning']).pack(pady=20)

        def do_load():
            try:
                result = self.supabase.table('knowledge_base')\
                    .select('*')\
                    .eq('metadata->>source', source)\
                    .order('created_at', desc=True)\
                    .limit(20)\
                    .execute()

                docs = result.data
                self.root.after(0, lambda: self.display_source_docs(source, docs))

            except Exception as e:
                self.root.after(0, lambda: self.display_error(str(e)))

        threading.Thread(target=do_load, daemon=True).start()

    def display_source_docs(self, source, docs):
        """Display documents from a source"""
        for widget in self.sources_frame.winfo_children():
            widget.destroy()

        # Back to sources button
        back_btn = tk.Button(self.sources_frame,
            text="< Back to Sources",
            font=('Segoe UI', 9),
            bg=self.colors['border'],
            fg=self.colors['text'],
            padx=10, pady=5,
            cursor='hand2',
            relief='flat',
            command=self.load_sources)
        back_btn.pack(anchor='w', padx=10, pady=10)

        tk.Label(self.sources_frame,
            text=f"Source: {source} ({len(docs)} documents)",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['sidebar'],
            fg=self.colors['accent']).pack(anchor='w', padx=10, pady=(0, 10))

        for doc in docs:
            self.create_doc_preview(doc)

    def create_doc_preview(self, doc):
        """Create a document preview"""
        card = tk.Frame(self.sources_frame, bg=self.colors['card'], padx=12, pady=8)
        card.pack(fill='x', padx=10, pady=3)

        tk.Label(card,
            text=doc.get('title', 'Untitled'),
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text'],
            anchor='w').pack(fill='x')

        content = doc.get('content', '')[:100] + '...'
        tk.Label(card,
            text=content,
            font=('Consolas', 9),
            bg=self.colors['card'],
            fg=self.colors['accent'],
            anchor='w').pack(fill='x')

    # ==================== RECENT SCREEN ====================

    def show_recent_screen(self):
        """Display recent sessions screen"""
        self.clear_content()

        self.current_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.current_frame.pack(fill='both', expand=True, padx=40, pady=30)

        tk.Label(self.current_frame,
            text="Recent Sessions",
            font=('Segoe UI', 16),
            bg=self.colors['bg'],
            fg=self.colors['text']).pack(pady=(0, 20))

        # Recent list
        recent_header = tk.Frame(self.current_frame, bg=self.colors['border'])
        recent_header.pack(fill='x')
        tk.Label(recent_header, text="RECENT ENTRIES",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['border'],
            fg=self.colors['accent'],
            pady=5).pack(anchor='w', padx=15)

        self.recent_frame = tk.Frame(self.current_frame, bg=self.colors['sidebar'])
        self.recent_frame.pack(fill='both', expand=True)

        tk.Label(self.recent_frame,
            text="Loading recent entries...",
            font=('Segoe UI', 11),
            bg=self.colors['sidebar'],
            fg=self.colors['warning']).pack(pady=20)

        # Bottom buttons
        btn_frame = tk.Frame(self.current_frame, bg=self.colors['bg'])
        btn_frame.pack(fill='x', pady=(15, 0))

        back_btn = tk.Button(btn_frame,
            text="Back to Menu",
            font=('Segoe UI', 10),
            bg=self.colors['border'],
            fg=self.colors['text'],
            padx=20, pady=8,
            cursor='hand2',
            relief='flat',
            command=self.show_welcome_screen)
        back_btn.pack(side='left')

        # Load recent
        self.load_recent()

    def load_recent(self):
        """Load recent entries"""
        def do_load():
            try:
                result = self.supabase.table('knowledge_base')\
                    .select('*')\
                    .order('created_at', desc=True)\
                    .limit(15)\
                    .execute()

                docs = result.data
                self.root.after(0, lambda: self.display_recent(docs))

            except Exception as e:
                self.root.after(0, lambda: self.display_error(str(e)))

        threading.Thread(target=do_load, daemon=True).start()

    def display_recent(self, docs):
        """Display recent entries"""
        for widget in self.recent_frame.winfo_children():
            widget.destroy()

        if not docs:
            tk.Label(self.recent_frame,
                text="No entries found",
                font=('Segoe UI', 11),
                bg=self.colors['sidebar'],
                fg=self.colors['text_dim']).pack(pady=20)
            return

        for doc in docs:
            card = tk.Frame(self.recent_frame, bg=self.colors['card'], padx=12, pady=8)
            card.pack(fill='x', padx=10, pady=3)

            header = tk.Frame(card, bg=self.colors['card'])
            header.pack(fill='x')

            tk.Label(header,
                text=doc.get('title', 'Untitled'),
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['card'],
                fg=self.colors['text']).pack(side='left')

            date = doc.get('created_at', '')[:10]
            tk.Label(header,
                text=date,
                font=('Segoe UI', 9),
                bg=self.colors['card'],
                fg=self.colors['text_dim']).pack(side='right')

            source = doc.get('metadata', {}).get('source', 'Unknown')
            tk.Label(card,
                text=f"Source: {source}",
                font=('Segoe UI', 9),
                bg=self.colors['card'],
                fg=self.colors['accent'],
                anchor='w').pack(fill='x')

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
                    os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_ANON_KEY')
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
    app = TrajanusQueryKBGUI()
    app.run()


if __name__ == '__main__':
    main()
