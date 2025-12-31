#!/usr/bin/env python3
"""
TRAJANUS MARKDOWN TO GOOGLE DOCS CONVERTER
Enhanced with scrollable interface, 3D buttons, and KB integration
"""

import os
import sys
import pickle
import threading
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


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

        # Bind events
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_press)
        self.bind('<ButtonRelease-1>', self.on_release)

    def draw_button(self, pressed=False):
        """Draw the 3D beveled button"""
        self.delete('all')

        w, h = self.width, self.height
        r = 8  # Corner radius
        bevel = 3  # Bevel thickness

        colors = self.colors

        if pressed:
            # Pressed state - inverted bevel
            outer_light = colors['dark']
            outer_dark = colors['light']
            face = colors['dark']
        else:
            outer_light = colors['light']
            outer_dark = colors['dark']
            face = colors['face']

        # Outer bevel (light edge - top/left)
        self.create_polygon(
            r, 0, w-r, 0, w, r, w-bevel, r+bevel,
            r+bevel, bevel, bevel, r+bevel, bevel, h-r-bevel,
            0, h-r, 0, r,
            fill=outer_light, outline=''
        )

        # Outer bevel (dark edge - bottom/right)
        self.create_polygon(
            w, r, w, h-r, w-r, h, r, h,
            r+bevel, h-bevel, w-r-bevel, h-bevel,
            w-bevel, h-r-bevel, w-bevel, r+bevel,
            fill=outer_dark, outline=''
        )

        # Main face with rounded corners effect
        self.create_rectangle(
            bevel+1, bevel+1, w-bevel-1, h-bevel-1,
            fill=face, outline=''
        )

        # Indicator light effect (subtle glow at top)
        if not pressed:
            self.create_rectangle(
                bevel+4, bevel+2, w-bevel-4, bevel+5,
                fill=colors['glow'], outline=''
            )

        # Text
        self.create_text(
            w/2, h/2 + (2 if pressed else 0),
            text=self.text,
            font=('Segoe UI', 10, 'bold'),
            fill=colors['text']
        )

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


class TrajanusConverterGUI:
    def __init__(self, initial_path=None):
        self.root = tk.Tk()
        self.root.title("Trajanus - MD-GDocs Converter")
        self.root.geometry("750x650")
        self.root.resizable(True, True)
        self.root.minsize(650, 550)

        # Navy/Silver palette (standard for all tools)
        self.colors = {
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
            'btn_light': '#f0c896',
            'btn_dark': '#808080',
            'btn_text': '#0d1b2a',
            'btn_glow': '#f0f0f0'
        }

        self.root.configure(bg=self.colors['bg'])

        # State
        self.service = None
        self.converting = False
        self.initial_path = initial_path
        self.last_folder_path = None

        # Results storage - now stores tuples of (md_name, gdoc_name)
        self.converted_files = []
        self.skipped_files = []
        self.error_files = []

        # Current frame reference
        self.current_frame = None
        self.scroll_canvas = None

        self.setup_header()
        self.connect_drive()

        # Show welcome screen or process initial path
        if self.initial_path:
            self.root.after(500, lambda: self.process_initial_path())
        else:
            self.show_welcome_screen()

    def setup_header(self):
        """Create compact header (50% smaller)"""
        self.header = tk.Frame(self.root, bg=self.colors['accent'], height=35)
        self.header.pack(fill='x')
        self.header.pack_propagate(False)

        title = tk.Label(self.header,
            text="TRAJANUS MD-GDOCS CONVERTER",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['accent'],
            fg='#1a1a1a')
        title.pack(pady=7)

        # Connection status bar
        self.status_bar = tk.Frame(self.root, bg=self.colors['border'], height=24)
        self.status_bar.pack(fill='x')
        self.status_bar.pack_propagate(False)

        self.connection_label = tk.Label(self.status_bar,
            text="Connecting to Google Drive...",
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
        # Container for canvas and scrollbar
        container = tk.Frame(self.root, bg=self.colors['bg'])
        container.pack(fill='both', expand=True)

        # Canvas for scrolling
        self.scroll_canvas = tk.Canvas(container, bg=self.colors['bg'],
                                       highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient='vertical',
                                  command=self.scroll_canvas.yview)

        # Scrollable frame inside canvas
        self.scrollable_frame = tk.Frame(self.scroll_canvas, bg=self.colors['bg'])

        self.scrollable_frame.bind(
            '<Configure>',
            lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox('all'))
        )

        self.canvas_window = self.scroll_canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor='nw'
        )

        # Bind canvas resize to adjust frame width
        self.scroll_canvas.bind('<Configure>', self.on_canvas_configure)

        self.scroll_canvas.configure(yscrollcommand=scrollbar.set)

        # Mouse wheel scrolling
        self.scroll_canvas.bind_all('<MouseWheel>', self.on_mousewheel)

        scrollbar.pack(side='right', fill='y')
        self.scroll_canvas.pack(side='left', fill='both', expand=True)

        return self.scrollable_frame

    def on_canvas_configure(self, event):
        """Adjust scrollable frame width when canvas resizes"""
        self.scroll_canvas.itemconfig(self.canvas_window, width=event.width)

    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        if self.scroll_canvas:
            self.scroll_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')

    def clear_content(self):
        """Clear current content frame"""
        if self.current_frame:
            self.current_frame.destroy()
        if self.scroll_canvas:
            self.scroll_canvas.unbind_all('<MouseWheel>')
            self.scroll_canvas.master.destroy()
            self.scroll_canvas = None

    def create_section_divider(self, parent, title=""):
        """Create a gold divider line with optional title"""
        divider_frame = tk.Frame(parent, bg=self.colors['bg'])
        divider_frame.pack(fill='x', pady=(15, 10))

        if title:
            tk.Label(divider_frame, text=title, font=('Segoe UI', 9, 'bold'),
                    bg=self.colors['bg'], fg=self.colors['accent']).pack(anchor='w')

        # Gold line
        tk.Frame(divider_frame, bg=self.colors['divider'], height=2).pack(fill='x', pady=(3, 0))

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
            text="Convert Markdown (.md) files to native Google Docs format.\nFiles are uploaded to Google Drive and converted automatically.",
            font=('Segoe UI', 9),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            justify='left').pack(anchor='w', pady=(4, 8))

        # Gold divider line
        tk.Frame(self.current_frame, bg=self.colors['divider'], height=2).pack(fill='x', pady=(0, 12))

        # ═══════════════════════════════════════════════════════════════
        # SECTION 2: CONVERSION MODE DESCRIPTIONS
        # ═══════════════════════════════════════════════════════════════
        tk.Label(self.current_frame,
            text="CONVERSION MODES",
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
            text="Select and convert one .md file at a time. Creates a Google Doc in the same Drive location.",
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
            text="Select a folder and convert all .md files within it. Already converted files are skipped automatically.",
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
            text="Select multiple specific .md files from different locations. Hold Ctrl to select multiple files.",
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

    def show_progress_screen(self, total_files):
        """Display conversion progress screen"""
        self.clear_content()

        self.current_frame = self.create_scrollable_frame()
        content = tk.Frame(self.current_frame, bg=self.colors['bg'])
        content.pack(fill='both', expand=True, padx=30, pady=20)

        # Title
        tk.Label(content,
            text="Converting Files...",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']).pack(pady=(0, 15))

        # Progress info card
        progress_card = tk.Frame(content, bg=self.colors['card'], padx=25, pady=20)
        progress_card.pack(fill='x', pady=(0, 15))

        self.progress_status = tk.Label(progress_card,
            text="Preparing...",
            font=('Segoe UI', 10),
            bg=self.colors['card'],
            fg=self.colors['text'])
        self.progress_status.pack(anchor='w', pady=(0, 12))

        # Progress bar
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
        self.progress_bar.pack(fill='x', pady=(0, 8))

        self.progress_text = tk.Label(progress_card,
            text=f"0 of {total_files} files",
            font=('Segoe UI', 9),
            bg=self.colors['card'],
            fg=self.colors['text_dim'])
        self.progress_text.pack(anchor='w')

        # Live stats
        stats_frame = tk.Frame(progress_card, bg=self.colors['card'])
        stats_frame.pack(fill='x', pady=(15, 0))

        self.live_converted = self.create_live_stat(stats_frame, "Converted:", "0", self.colors['success'])
        self.live_skipped = self.create_live_stat(stats_frame, "Skipped:", "0", self.colors['warning'])
        self.live_errors = self.create_live_stat(stats_frame, "Errors:", "0", self.colors['error'])

        # Current file label
        self.current_file_label = tk.Label(content,
            text="",
            font=('Consolas', 9),
            bg=self.colors['bg'],
            fg=self.colors['text_dim'])
        self.current_file_label.pack(pady=(8, 0))

    def create_live_stat(self, parent, label, value, color):
        """Create a live stat display"""
        frame = tk.Frame(parent, bg=self.colors['card'])
        frame.pack(side='left', padx=(0, 25))

        tk.Label(frame, text=label, font=('Segoe UI', 9),
            bg=self.colors['card'], fg=self.colors['text_dim']).pack(side='left')

        val_label = tk.Label(frame, text=value, font=('Segoe UI', 9, 'bold'),
            bg=self.colors['card'], fg=color)
        val_label.pack(side='left', padx=(4, 0))
        return val_label

    def show_completion_screen(self):
        """Display completion screen with results"""
        self.clear_content()

        self.current_frame = self.create_scrollable_frame()
        content = tk.Frame(self.current_frame, bg=self.colors['bg'])
        content.pack(fill='both', expand=True, padx=30, pady=20)

        # Success header
        tk.Label(content,
            text="CONVERSION COMPLETE",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['success']).pack(anchor='w', pady=(0, 15))

        # Results summary card
        summary_card = tk.Frame(content, bg=self.colors['card'], padx=20, pady=15)
        summary_card.pack(fill='x', pady=(0, 15))

        stats_frame = tk.Frame(summary_card, bg=self.colors['card'])
        stats_frame.pack(fill='x')

        self.create_result_stat(stats_frame, "Created", len(self.converted_files), self.colors['success'])
        self.create_result_stat(stats_frame, "Skipped", len(self.skipped_files), self.colors['warning'])
        self.create_result_stat(stats_frame, "Errors", len(self.error_files), self.colors['error'])

        # Created files list (showing NEW Google Doc names)
        if self.converted_files:
            self.create_section_divider(content, "CREATED GOOGLE DOCS")
            self.create_file_list(content, self.converted_files, self.colors['success'], show_gdoc=True)

        # Skipped files list
        if self.skipped_files:
            self.create_section_divider(content, "SKIPPED (already exists)")
            self.create_file_list(content, self.skipped_files, self.colors['warning'])

        # Error files list
        if self.error_files:
            self.create_section_divider(content, "FAILED")
            self.create_file_list(content, self.error_files, self.colors['error'])

        self.create_section_divider(content)

        # Action buttons row 1 - Folder and Convert More
        btn_frame1 = tk.Frame(content, bg=self.colors['bg'])
        btn_frame1.pack(fill='x', pady=(10, 8))

        if self.last_folder_path:
            BeveledButton(btn_frame1, "OPEN FOLDER",
                         command=self.open_folder, width=160, height=42).pack(side='left', padx=(0, 10))

        BeveledButton(btn_frame1, "CONVERT MORE",
                     command=self.show_welcome_screen, width=160, height=42).pack(side='left', padx=(0, 10))

        BeveledButton(btn_frame1, "EXIT", command=self.root.quit,
                     width=100, height=42, style='dark').pack(side='right')

        # Action buttons row 2 - Parse options (only if files were converted)
        if self.converted_files:
            btn_frame2 = tk.Frame(content, bg=self.colors['bg'])
            btn_frame2.pack(fill='x', pady=(0, 10))

            BeveledButton(btn_frame2, "PARSE TO KB",
                         command=self.parse_files, width=180, height=42, style='success').pack(side='left', padx=(0, 10))
            BeveledButton(btn_frame2, "PARSE & INGEST",
                         command=self.parse_and_ingest, width=180, height=42, style='success').pack(side='left')

    def create_result_stat(self, parent, label, value, color):
        """Create a result statistic display"""
        frame = tk.Frame(parent, bg=self.colors['card'])
        frame.pack(side='left', padx=(0, 35))

        tk.Label(frame, text=str(value), font=('Segoe UI', 20, 'bold'),
            bg=self.colors['card'], fg=color).pack()
        tk.Label(frame, text=label, font=('Segoe UI', 9),
            bg=self.colors['card'], fg=self.colors['text_dim']).pack()

    def create_file_list(self, parent, files, color, show_gdoc=False):
        """Create a scrollable file list showing Google Doc names"""
        list_frame = tk.Frame(parent, bg=self.colors['bg_light'], padx=15, pady=10)
        list_frame.pack(fill='x', pady=(0, 10))

        for f in files:
            if show_gdoc and isinstance(f, tuple):
                # Show the Google Doc name (new file created)
                display_name = f"  {f[1]}"  # f[1] is gdoc name
            else:
                display_name = f"  {f}" if isinstance(f, str) else f"  {f[0]}"

            tk.Label(list_frame, text=display_name, font=('Consolas', 9),
                bg=self.colors['bg_light'], fg=self.colors['accent'],
                anchor='w').pack(fill='x', pady=1)

    def open_folder(self):
        """Open the folder containing converted files"""
        if self.last_folder_path and os.path.exists(self.last_folder_path):
            subprocess.run(['explorer', str(self.last_folder_path)])

    def parse_files(self):
        """Launch the parse/ingestion tool for parsing only"""
        script_path = Path(__file__).parent / 'BATCH_INGEST_TOOL.py'
        if script_path.exists():
            subprocess.Popen(['python', str(script_path), '--parse-only'])
            messagebox.showinfo("Parse", "KB Parser tool launched.\nFiles will be parsed for knowledge base.")
        else:
            messagebox.showerror("Error", "BATCH_INGEST_TOOL.py not found.")

    def parse_and_ingest(self):
        """Launch the parse and ingest tool"""
        script_path = Path(__file__).parent / 'BATCH_INGEST_TOOL.py'
        if script_path.exists():
            subprocess.Popen(['python', str(script_path)])
            messagebox.showinfo("Parse & Ingest", "KB Ingestion tool launched.\nFiles will be parsed and ingested to knowledge base.")
        else:
            messagebox.showerror("Error", "BATCH_INGEST_TOOL.py not found.")

    # ==================== FILE SELECTION ====================

    def select_single_file(self):
        """Select a single markdown file to convert"""
        self.root.withdraw()
        self.root.update()

        file = filedialog.askopenfilename(
            title="Select Markdown File",
            initialdir="G:/My Drive/00 - Trajanus USA",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")])

        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

        if file:
            if not self.service:
                messagebox.showerror("Error", "Not connected to Google Drive.\nPlease wait for connection.")
                return
            self.last_folder_path = Path(file).parent
            self.convert_files([Path(file)])

    def select_folder(self):
        """Select a folder to convert all .md files"""
        self.root.withdraw()
        self.root.update()

        folder = filedialog.askdirectory(
            title="Select Folder with Markdown Files",
            initialdir="G:/My Drive/00 - Trajanus USA")

        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

        if folder:
            md_files = list(Path(folder).glob('*.md'))
            if md_files:
                if not self.service:
                    messagebox.showerror("Error", "Not connected to Google Drive.\nPlease wait for connection.")
                    return
                self.last_folder_path = Path(folder)
                self.convert_files(md_files)
            else:
                messagebox.showinfo("No Files", f"No .md files found in:\n{folder}")

    def select_multiple_files(self):
        """Select multiple markdown files to convert"""
        self.root.withdraw()
        self.root.update()

        files = filedialog.askopenfilenames(
            title="Select Markdown Files (hold Ctrl to select multiple)",
            initialdir="G:/My Drive/00 - Trajanus USA",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")])

        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

        if files:
            if not self.service:
                messagebox.showerror("Error", "Not connected to Google Drive.\nPlease wait for connection.")
                return
            self.last_folder_path = Path(files[0]).parent
            self.convert_files([Path(f) for f in files])

    def process_initial_path(self):
        """Process path passed from command line"""
        path = Path(self.initial_path)

        if not path.exists():
            messagebox.showerror("Error", f"Path not found: {path}")
            self.show_welcome_screen()
            return

        if path.is_file():
            if path.suffix.lower() == '.md':
                self.last_folder_path = path.parent
                self.convert_files([path])
            else:
                messagebox.showerror("Error", "Not a markdown file")
                self.show_welcome_screen()
        else:
            md_files = list(path.glob('*.md'))
            if md_files:
                self.last_folder_path = path
                self.convert_files(md_files)
            else:
                messagebox.showinfo("No Files", "No .md files found")
                self.show_welcome_screen()

    # ==================== CONVERSION ====================

    def convert_files(self, md_files):
        """Convert a list of markdown files"""
        if not md_files:
            return

        # Reset results
        self.converted_files = []
        self.skipped_files = []
        self.error_files = []

        self.show_progress_screen(len(md_files))
        self.converting = True

        def do_convert():
            source_folder = md_files[0].parent

            self.root.after(0, lambda: self.progress_status.config(
                text="Finding folder in Google Drive..."))

            folder_id = self.get_drive_folder_id(source_folder)

            if not folder_id:
                self.root.after(0, lambda: messagebox.showerror("Error",
                    "Could not find folder in Google Drive.\nMake sure it's synced."))
                self.root.after(0, self.show_welcome_screen)
                return

            self.root.after(0, lambda: self.progress_status.config(
                text="Converting files..."))

            total = len(md_files)

            for i, md_file in enumerate(sorted(md_files)):
                percent = ((i + 1) / total) * 100
                self.root.after(0, lambda p=percent: self.progress_bar.configure(value=p))
                self.root.after(0, lambda i=i, t=total: self.progress_text.config(
                    text=f"{i + 1} of {t} files"))
                self.root.after(0, lambda f=md_file.name: self.current_file_label.config(
                    text=f"Processing: {f}"))

                # Check if already converted
                gdoc_path = str(md_file)[:-3] + '.gdoc'
                url_path = str(md_file)[:-3] + '.url'

                if os.path.exists(gdoc_path) or os.path.exists(url_path):
                    self.skipped_files.append(md_file.name)
                    self.root.after(0, lambda: self.live_skipped.config(
                        text=str(len(self.skipped_files))))
                    continue

                result = self.convert_md_to_gdoc(md_file, folder_id)

                if result:
                    # Store tuple of (md_name, gdoc_name)
                    gdoc_name = result.get('name', md_file.stem)
                    self.converted_files.append((md_file.name, gdoc_name))
                    self.root.after(0, lambda: self.live_converted.config(
                        text=str(len(self.converted_files))))
                else:
                    self.error_files.append(md_file.name)
                    self.root.after(0, lambda: self.live_errors.config(
                        text=str(len(self.error_files))))

            self.converting = False
            self.root.after(0, self.show_completion_screen)

        threading.Thread(target=do_convert, daemon=True).start()

    def convert_md_to_gdoc(self, md_file, folder_id):
        """Upload and convert a single markdown file"""
        file_metadata = {
            'name': md_file.stem,
            'mimeType': 'application/vnd.google-apps.document',
            'parents': [folder_id]
        }

        media = MediaFileUpload(str(md_file), mimetype='text/markdown', resumable=True)

        try:
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name'
            ).execute()
            return file
        except Exception:
            return None

    # ==================== GOOGLE DRIVE ====================

    def connect_drive(self):
        """Connect to Google Drive"""
        def do_connect():
            try:
                creds = self.get_credentials()
                if creds:
                    self.service = build('drive', 'v3', credentials=creds)
                    self.root.after(0, lambda: self.connection_status.config(
                        text="Connected", fg=self.colors['success']))
                else:
                    self.root.after(0, lambda: self.connection_status.config(
                        text="Not Connected", fg=self.colors['error']))
            except Exception as e:
                self.root.after(0, lambda: self.connection_status.config(
                    text="Connection Failed", fg=self.colors['error']))

        threading.Thread(target=do_connect, daemon=True).start()

    def get_credentials(self):
        """Load Google Drive credentials"""
        creds_path = Path('G:/My Drive/00 - Trajanus USA/00-Command-Center/001 Credentials')
        token_path = creds_path / 'token.pickle'

        if not token_path.exists():
            return None

        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open(token_path, 'wb') as token:
                    pickle.dump(creds, token)

        return creds

    def get_drive_folder_id(self, local_folder_path):
        """Get Google Drive folder ID for a local path"""
        path_str = str(local_folder_path).replace('\\', '/')

        if 'My Drive/' in path_str:
            relative_path = path_str.split('My Drive/')[1]
        else:
            return None

        folder_names = [f for f in relative_path.split('/') if f]
        if not folder_names:
            return 'root'

        current_id = 'root'
        for folder_name in folder_names:
            escaped_name = folder_name.replace("'", "\\'")
            query = f"name='{escaped_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false and '{current_id}' in parents"

            try:
                results = self.service.files().list(q=query, fields='files(id, name)').execute()
                files = results.get('files', [])
                if not files:
                    return None
                current_id = files[0]['id']
            except Exception:
                return None

        return current_id

    def run(self):
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        self.root.mainloop()


def main():
    initial_path = None
    if len(sys.argv) > 1:
        initial_path = sys.argv[1]

    app = TrajanusConverterGUI(initial_path)
    app.run()


if __name__ == '__main__':
    main()
