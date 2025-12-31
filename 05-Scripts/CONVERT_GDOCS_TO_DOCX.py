#!/usr/bin/env python3
"""
TRAJANUS GDOCS-DOCX CONVERTER
Export Google Docs (.gdoc files) to Word (.docx) format
Enhanced with 3D buttons and scrollable interface
"""

import os
import sys
import json
import pickle
import threading
import subprocess
import re
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import io

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


class BeveledButton(tk.Canvas):
    """3D Beveled button with machine indicator light effect"""

    def __init__(self, parent, text, command=None, width=180, height=40,
                 bg_color='#d4a574', fg_color='#1a1a1a', style='gold', **kwargs):
        super().__init__(parent, width=width, height=height,
                        bg=parent.cget('bg'), highlightthickness=0, **kwargs)

        self.command = command
        self.text = text
        self.width = width
        self.height = height
        self.style = style
        self.pressed = False

        self.schemes = {
            'gold': {
                'face': '#d4a574',
                'light': '#f0c896',
                'dark': '#8a6b4a',
                'text': '#1a1a1a',
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

        self.colors = self.schemes.get(style, self.schemes['gold'])
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


class TrajanusGdocConverterGUI:
    def __init__(self, initial_path=None):
        self.root = tk.Tk()
        self.root.title("Trajanus - GDocs-DOCX Converter")
        self.root.geometry("750x650")
        self.root.resizable(True, True)
        self.root.minsize(650, 550)

        # Navy/Gold palette for comparison
        self.colors = {
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
        }

        self.root.configure(bg=self.colors['bg'])

        # State
        self.service = None
        self.converting = False
        self.initial_path = initial_path

        # Results storage
        self.converted_files = []
        self.converted_paths = []
        self.skipped_files = []
        self.error_files = []
        self.output_folder = None

        # Current frame reference
        self.current_frame = None
        self.scroll_canvas = None

        self.setup_header()
        self.connect_drive()

        if self.initial_path:
            self.root.after(500, lambda: self.process_initial_path())
        else:
            self.show_welcome_screen()

    def setup_header(self):
        """Create compact header (matches other tools)"""
        self.header = tk.Frame(self.root, bg=self.colors['accent'], height=35)
        self.header.pack(fill='x')
        self.header.pack_propagate(False)

        title = tk.Label(self.header,
            text="TRAJANUS GDOCS-DOCX CONVERTER",
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
        """Display welcome/mode selection screen"""
        self.clear_content()

        self.current_frame = self.create_scrollable_frame()
        content = tk.Frame(self.current_frame, bg=self.colors['bg'])
        content.pack(fill='both', expand=True, padx=30, pady=20)

        # Tool description card
        desc_card = tk.Frame(content, bg=self.colors['card'], padx=20, pady=15)
        desc_card.pack(fill='x', pady=(0, 15))

        tk.Label(desc_card,
            text="TOOL DESCRIPTION",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['accent']).pack(anchor='w')

        tk.Label(desc_card,
            text="Exports Google Docs (.gdoc files) to Word (.docx) format.\nReads document ID from .gdoc file and downloads from Google Drive.",
            font=('Segoe UI', 10),
            bg=self.colors['card'],
            fg=self.colors['text'],
            justify='left').pack(anchor='w', pady=(5, 0))

        self.create_section_divider(content, "HOW TO USE")

        # Instructions
        instructions_card = tk.Frame(content, bg=self.colors['bg_light'], padx=20, pady=15)
        instructions_card.pack(fill='x', pady=(0, 15))

        instructions = [
            "1. Select .gdoc files (Google Doc shortcuts)",
            "2. Tool reads the document ID from each file",
            "3. Exports from Google Drive as .docx",
            "4. Saves to same folder as the .gdoc file",
            "",
            "NOTE: Requires Google Drive Desktop sync."
        ]

        for inst in instructions:
            color = self.colors['accent'] if inst.startswith('NOTE') else self.colors['text']
            tk.Label(instructions_card,
                text=inst,
                font=('Segoe UI', 10),
                bg=self.colors['bg_light'],
                fg=color,
                justify='left').pack(anchor='w', pady=1)

        self.create_section_divider(content, "SELECT EXPORT MODE")

        # Mode buttons container - use BeveledButtons
        btn_container = tk.Frame(content, bg=self.colors['bg'])
        btn_container.pack(fill='x', pady=(10, 0))

        BeveledButton(btn_container, "SINGLE FILE",
                     command=self.select_single_file, width=200, height=45).pack(side='left', padx=(0, 10))
        BeveledButton(btn_container, "BATCH FOLDER",
                     command=self.select_folder, width=200, height=45).pack(side='left', padx=(0, 10))
        BeveledButton(btn_container, "MULTI-SELECT",
                     command=self.select_multiple_files, width=200, height=45).pack(side='left')

        self.create_section_divider(content)

        # Exit button at bottom
        exit_frame = tk.Frame(content, bg=self.colors['bg'])
        exit_frame.pack(fill='x', pady=(10, 0))

        BeveledButton(exit_frame, "EXIT", command=self.root.quit,
                     width=120, height=38, style='dark').pack(side='right')

    def create_mode_card(self, parent, title, subtitle, description, command, side='left'):
        """Create a mode selection card - entire card is clickable"""
        card = tk.Frame(parent, bg=self.colors['card'], padx=15, pady=15, cursor='hand2')
        card.pack(side=side, padx=(0, 10), fill='both', expand=True)

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
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['accent'],
            cursor='hand2')
        title_label.pack(anchor='w')
        title_label.bind('<Button-1>', lambda e: command())

        subtitle_label = tk.Label(card,
            text=subtitle,
            font=('Segoe UI', 9),
            bg=self.colors['card'],
            fg=self.colors['text'],
            cursor='hand2')
        subtitle_label.pack(anchor='w', pady=(3, 0))
        subtitle_label.bind('<Button-1>', lambda e: command())

        desc_label = tk.Label(card,
            text=description,
            font=('Segoe UI', 8),
            bg=self.colors['card'],
            fg=self.colors['text_dim'],
            cursor='hand2')
        desc_label.pack(anchor='w', pady=(2, 10))
        desc_label.bind('<Button-1>', lambda e: command())

        btn = tk.Button(card,
            text=title,
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['accent'],
            fg='#1a1a1a',
            activebackground=self.colors['hover'],
            activeforeground='#1a1a1a',
            padx=15, pady=6,
            cursor='hand2',
            relief='flat',
            command=command)
        btn.pack(fill='x')

    def show_progress_screen(self, total_files):
        """Display conversion progress screen"""
        self.clear_content()

        self.current_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.current_frame.pack(fill='both', expand=True, padx=30, pady=20)

        tk.Label(self.current_frame,
            text="Exporting Files...",
            font=('Segoe UI', 14),
            bg=self.colors['bg'],
            fg=self.colors['text']).pack(pady=(0, 15))

        progress_card = tk.Frame(self.current_frame, bg=self.colors['card'], padx=25, pady=20)
        progress_card.pack(fill='x', pady=(0, 15))

        self.progress_status = tk.Label(progress_card,
            text="Preparing...",
            font=('Segoe UI', 10),
            bg=self.colors['card'],
            fg=self.colors['text'])
        self.progress_status.pack(anchor='w', pady=(0, 10))

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
            length=400,
            mode='determinate')
        self.progress_bar.pack(fill='x', pady=(0, 8))

        self.progress_text = tk.Label(progress_card,
            text=f"0 of {total_files} files",
            font=('Segoe UI', 9),
            bg=self.colors['card'],
            fg=self.colors['text_dim'])
        self.progress_text.pack(anchor='w')

        stats_frame = tk.Frame(progress_card, bg=self.colors['card'])
        stats_frame.pack(fill='x', pady=(15, 0))

        self.live_converted = self.create_live_stat(stats_frame, "Exported:", "0", self.colors['success'])
        self.live_skipped = self.create_live_stat(stats_frame, "Skipped:", "0", self.colors['warning'])
        self.live_errors = self.create_live_stat(stats_frame, "Errors:", "0", self.colors['error'])

        self.current_file_label = tk.Label(self.current_frame,
            text="",
            font=('Consolas', 8),
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
        val_label.pack(side='left', padx=(5, 0))
        return val_label

    def show_completion_screen(self):
        """Display completion screen with results"""
        self.clear_content()

        self.current_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.current_frame.pack(fill='both', expand=True, padx=30, pady=20)

        header_frame = tk.Frame(self.current_frame, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, 15))

        tk.Label(header_frame,
            text="EXPORT COMPLETE",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['success']).pack(side='left')

        summary_card = tk.Frame(self.current_frame, bg=self.colors['card'], padx=20, pady=15)
        summary_card.pack(fill='x', pady=(0, 15))

        stats_frame = tk.Frame(summary_card, bg=self.colors['card'])
        stats_frame.pack(fill='x')

        self.create_result_stat(stats_frame, "Exported", len(self.converted_files), self.colors['success'])
        self.create_result_stat(stats_frame, "Skipped", len(self.skipped_files), self.colors['warning'])
        self.create_result_stat(stats_frame, "Errors", len(self.error_files), self.colors['error'])

        if self.converted_files:
            self.create_file_list("EXPORTED FILES", self.converted_files, self.converted_paths, self.colors['success'])

        if self.skipped_files:
            self.create_file_list("SKIPPED FILES (already exist)", self.skipped_files, [], self.colors['warning'])

        if self.error_files:
            self.create_file_list("FAILED FILES", self.error_files, [], self.colors['error'])

        btn_frame = tk.Frame(self.current_frame, bg=self.colors['bg'])
        btn_frame.pack(fill='x', pady=(15, 0))

        # Action buttons
        if self.converted_paths:
            open_folder_btn = tk.Button(btn_frame,
                text="Open Folder",
                font=('Segoe UI', 10),
                bg=self.colors['card'],
                fg=self.colors['accent'],
                activebackground=self.colors['sidebar'],
                activeforeground=self.colors['accent'],
                padx=15, pady=6,
                cursor='hand2',
                relief='flat',
                command=self.open_output_folder)
            open_folder_btn.pack(side='left', padx=(0, 10))

            if len(self.converted_paths) == 1:
                view_btn = tk.Button(btn_frame,
                    text="View File",
                    font=('Segoe UI', 10),
                    bg=self.colors['card'],
                    fg=self.colors['accent'],
                    activebackground=self.colors['sidebar'],
                    activeforeground=self.colors['accent'],
                    padx=15, pady=6,
                    cursor='hand2',
                    relief='flat',
                    command=lambda: self.open_file(self.converted_paths[0]))
                view_btn.pack(side='left', padx=(0, 10))

        convert_more_btn = tk.Button(btn_frame,
            text="Export More",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['accent'],
            fg='#1a1a1a',
            activebackground=self.colors['hover'],
            activeforeground='#1a1a1a',
            padx=20, pady=6,
            cursor='hand2',
            relief='flat',
            command=self.show_welcome_screen)
        convert_more_btn.pack(side='left')

        exit_btn = tk.Button(btn_frame,
            text="Exit",
            font=('Segoe UI', 10),
            bg=self.colors['border'],
            fg=self.colors['text'],
            activebackground='#444444',
            activeforeground=self.colors['text'],
            padx=25, pady=6,
            cursor='hand2',
            relief='flat',
            command=self.root.quit)
        exit_btn.pack(side='right')

    def create_result_stat(self, parent, label, value, color):
        """Create a result statistic display"""
        frame = tk.Frame(parent, bg=self.colors['card'])
        frame.pack(side='left', padx=(0, 30))

        tk.Label(frame, text=str(value), font=('Segoe UI', 20, 'bold'),
            bg=self.colors['card'], fg=color).pack()
        tk.Label(frame, text=label, font=('Segoe UI', 9),
            bg=self.colors['card'], fg=self.colors['text_dim']).pack()

    def create_file_list(self, title, files, paths, color):
        """Create a file list with clickable items"""
        list_frame = tk.Frame(self.current_frame, bg=self.colors['sidebar'])
        list_frame.pack(fill='x', pady=(0, 10))

        header = tk.Frame(list_frame, bg=self.colors['border'])
        header.pack(fill='x')
        tk.Label(header, text=title, font=('Segoe UI', 8, 'bold'),
            bg=self.colors['border'], fg=color,
            padx=10, pady=3).pack(anchor='w')

        display_files = files[:4]
        display_paths = paths[:4] if paths else []

        for i, f in enumerate(display_files):
            file_path = display_paths[i] if i < len(display_paths) else None

            if file_path:
                # Clickable file
                file_label = tk.Label(list_frame, text=f"  {f}", font=('Consolas', 8),
                    bg=self.colors['sidebar'], fg=self.colors['accent'],
                    anchor='w', cursor='hand2')
                file_label.pack(fill='x', padx=8, pady=1)
                file_label.bind('<Button-1>', lambda e, p=file_path: self.open_file(p))
                file_label.bind('<Enter>', lambda e, l=file_label: l.config(fg=self.colors['hover']))
                file_label.bind('<Leave>', lambda e, l=file_label: l.config(fg=self.colors['accent']))
            else:
                tk.Label(list_frame, text=f"  {f}", font=('Consolas', 8),
                    bg=self.colors['sidebar'], fg=self.colors['accent'],
                    anchor='w').pack(fill='x', padx=8, pady=1)

        if len(files) > 4:
            tk.Label(list_frame, text=f"  ... and {len(files) - 4} more",
                font=('Consolas', 8, 'italic'),
                bg=self.colors['sidebar'], fg=self.colors['accent'],
                anchor='w').pack(fill='x', padx=8, pady=1)

    def open_file(self, filepath):
        """Open a file with default application"""
        try:
            os.startfile(filepath)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

    def open_output_folder(self):
        """Open the output folder in Explorer"""
        if self.converted_paths:
            folder = Path(self.converted_paths[0]).parent
            try:
                subprocess.run(['explorer', str(folder)])
            except Exception as e:
                messagebox.showerror("Error", f"Could not open folder: {e}")

    # ==================== FILE SELECTION ====================

    def select_single_file(self):
        """Select a single .gdoc file"""
        if not self.service:
            messagebox.showerror("Error", "Not connected to Google Drive.\nPlease wait for connection.")
            return

        self.root.attributes('-topmost', False)
        self.root.update()

        file = filedialog.askopenfilename(
            title="Select Google Doc File",
            initialdir="G:/My Drive/00 - Trajanus USA",
            filetypes=[("Google Doc files", "*.gdoc"), ("All files", "*.*")],
            parent=self.root)

        self.root.lift()
        self.root.focus_force()

        if file:
            self.convert_files([Path(file)])

    def select_folder(self):
        """Select a folder to export all .gdoc files"""
        if not self.service:
            messagebox.showerror("Error", "Not connected to Google Drive.\nPlease wait for connection.")
            return

        self.root.attributes('-topmost', False)
        self.root.update()

        folder = filedialog.askdirectory(
            title="Select Folder with Google Docs",
            initialdir="G:/My Drive/00 - Trajanus USA",
            parent=self.root)

        self.root.lift()
        self.root.focus_force()

        if folder:
            gdoc_files = list(Path(folder).glob('*.gdoc'))
            if gdoc_files:
                self.convert_files(gdoc_files)
            else:
                messagebox.showinfo("No Files", f"No .gdoc files found in:\n{folder}")

    def select_multiple_files(self):
        """Select multiple .gdoc files"""
        if not self.service:
            messagebox.showerror("Error", "Not connected to Google Drive.\nPlease wait for connection.")
            return

        self.root.attributes('-topmost', False)
        self.root.update()

        files = filedialog.askopenfilenames(
            title="Select Google Doc Files (Ctrl+Click for multiple)",
            initialdir="G:/My Drive/00 - Trajanus USA",
            filetypes=[("Google Doc files", "*.gdoc"), ("All files", "*.*")],
            parent=self.root)

        self.root.lift()
        self.root.focus_force()

        if files:
            self.convert_files([Path(f) for f in files])

    def process_initial_path(self):
        """Process path passed from command line"""
        path = Path(self.initial_path)

        if not path.exists():
            messagebox.showerror("Error", f"Path not found: {path}")
            self.show_welcome_screen()
            return

        if path.is_file():
            if path.suffix.lower() == '.gdoc':
                self.convert_files([path])
            else:
                messagebox.showerror("Error", "Not a .gdoc file")
                self.show_welcome_screen()
        else:
            gdoc_files = list(path.glob('*.gdoc'))
            if gdoc_files:
                self.convert_files(gdoc_files)
            else:
                messagebox.showinfo("No Files", "No .gdoc files found")
                self.show_welcome_screen()

    # ==================== CONVERSION ====================

    def extract_file_id(self, gdoc_path):
        """Extract Google Drive file ID from .gdoc file"""
        try:
            with open(gdoc_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Try JSON format first
            try:
                data = json.loads(content)
                if 'doc_id' in data:
                    return data['doc_id']
                if 'url' in data:
                    # Extract ID from URL
                    match = re.search(r'/d/([a-zA-Z0-9_-]+)', data['url'])
                    if match:
                        return match.group(1)
            except json.JSONDecodeError:
                pass

            # Try URL format
            match = re.search(r'/d/([a-zA-Z0-9_-]+)', content)
            if match:
                return match.group(1)

            return None

        except Exception:
            return None

    def convert_files(self, gdoc_files):
        """Convert a list of .gdoc files to .docx"""
        if not gdoc_files:
            return

        self.converted_files = []
        self.converted_paths = []
        self.skipped_files = []
        self.error_files = []
        self.output_folder = gdoc_files[0].parent

        self.show_progress_screen(len(gdoc_files))
        self.converting = True

        def do_convert():
            self.root.after(0, lambda: self.progress_status.config(
                text="Exporting files..."))

            total = len(gdoc_files)

            for i, gdoc_file in enumerate(sorted(gdoc_files)):
                percent = ((i + 1) / total) * 100
                self.root.after(0, lambda p=percent: self.progress_bar.configure(value=p))
                self.root.after(0, lambda i=i, t=total: self.progress_text.config(
                    text=f"{i + 1} of {t} files"))
                self.root.after(0, lambda f=gdoc_file.name: self.current_file_label.config(
                    text=f"Processing: {f}"))

                # Check if .docx already exists
                docx_path = gdoc_file.with_suffix('.docx')
                if docx_path.exists():
                    self.skipped_files.append(gdoc_file.stem)
                    self.root.after(0, lambda: self.live_skipped.config(
                        text=str(len(self.skipped_files))))
                    continue

                # Extract file ID from .gdoc
                file_id = self.extract_file_id(gdoc_file)
                if not file_id:
                    self.error_files.append(gdoc_file.stem + " (bad .gdoc)")
                    self.root.after(0, lambda: self.live_errors.config(
                        text=str(len(self.error_files))))
                    continue

                # Export to docx
                result = self.export_gdoc_to_docx(file_id, gdoc_file.stem, gdoc_file.parent)

                if result:
                    self.converted_files.append(result.name)
                    self.converted_paths.append(str(result))
                    self.root.after(0, lambda: self.live_converted.config(
                        text=str(len(self.converted_files))))
                else:
                    self.error_files.append(gdoc_file.stem)
                    self.root.after(0, lambda: self.live_errors.config(
                        text=str(len(self.error_files))))

            self.converting = False
            self.root.after(0, self.show_completion_screen)

        threading.Thread(target=do_convert, daemon=True).start()

    def export_gdoc_to_docx(self, file_id, file_name, output_folder):
        """Export a Google Doc to .docx format"""
        output_path = output_folder / f"{file_name}.docx"

        try:
            request = self.service.files().export_media(
                fileId=file_id,
                mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )

            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False

            while not done:
                status, done = downloader.next_chunk()

            with open(output_path, 'wb') as f:
                f.write(fh.getvalue())

            return output_path

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

    def run(self):
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

    app = TrajanusGdocConverterGUI(initial_path)
    app.run()


if __name__ == '__main__':
    main()
