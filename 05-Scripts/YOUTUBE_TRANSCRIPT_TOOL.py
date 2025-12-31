#!/usr/bin/env python3
"""
TRAJANUS YOUTUBE TRANSCRIPT TOOL
Crawl YouTube, extract transcripts, and ingest to knowledge base
Standard 3-section black/gold UI
"""

import os
import sys
import io
import threading
import subprocess
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add agents directory to path
SCRIPT_DIR = Path(__file__).parent
AGENTS_DIR = SCRIPT_DIR.parent / "agents" / "research-agent"
sys.path.insert(0, str(AGENTS_DIR))


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


class TrajanusYouTubeTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Trajanus - YouTube Transcript Tool")
        self.root.geometry("650x550")
        self.root.resizable(True, True)
        self.root.minsize(600, 500)

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
        self.processing = False
        self.video_url = tk.StringVar()
        self.search_query = tk.StringVar(value="Claude AI tutorial")

        # Current frame reference
        self.current_frame = None
        self.scroll_canvas = None

        self.setup_header()
        self.show_welcome_screen()

    def setup_header(self):
        """Create compact header"""
        self.header = tk.Frame(self.root, bg=self.colors['accent'], height=35)
        self.header.pack(fill='x')
        self.header.pack_propagate(False)

        title = tk.Label(self.header,
            text="TRAJANUS YOUTUBE TRANSCRIPT TOOL",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['accent'],
            fg='#0a0a0a')
        title.pack(pady=7)

        # Status bar
        self.status_bar = tk.Frame(self.root, bg=self.colors['border'], height=24)
        self.status_bar.pack(fill='x')
        self.status_bar.pack_propagate(False)

        self.status_label = tk.Label(self.status_bar,
            text="Ready",
            font=('Segoe UI', 8),
            bg=self.colors['border'],
            fg=self.colors['text_dim'])
        self.status_label.pack(side='left', padx=10, pady=3)

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
            text="Crawl YouTube for videos, extract transcripts, and ingest to knowledge base.\nSupports single video URLs, batch processing, and automated scanning.",
            font=('Segoe UI', 9),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            justify='left').pack(anchor='w', pady=(4, 8))

        # Gold divider line
        tk.Frame(self.current_frame, bg=self.colors['divider'], height=2).pack(fill='x', pady=(0, 12))

        # ═══════════════════════════════════════════════════════════════
        # SECTION 2: OPERATION DESCRIPTIONS
        # ═══════════════════════════════════════════════════════════════
        tk.Label(self.current_frame,
            text="OPERATIONS",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['accent']).pack(anchor='w')

        # Operation explanations
        op_info = tk.Frame(self.current_frame, bg=self.colors['bg'])
        op_info.pack(fill='x', pady=(6, 8))

        tk.Label(op_info,
            text="SCAN YOUTUBE",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']).pack(anchor='w')
        tk.Label(op_info,
            text="Search YouTube for videos matching configured queries (Claude AI, Anthropic, etc.). Generates a research briefing with discovered videos.",
            font=('Segoe UI', 8),
            bg=self.colors['bg'],
            fg=self.colors['text_dim'],
            wraplength=560,
            justify='left').pack(anchor='w', pady=(0, 6))

        tk.Label(op_info,
            text="EXTRACT TRANSCRIPT",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']).pack(anchor='w')
        tk.Label(op_info,
            text="Extract transcript from a YouTube video URL using browser automation. Saves as formatted markdown with metadata.",
            font=('Segoe UI', 8),
            bg=self.colors['bg'],
            fg=self.colors['text_dim'],
            wraplength=560,
            justify='left').pack(anchor='w', pady=(0, 6))

        tk.Label(op_info,
            text="INGEST TO KB",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']).pack(anchor='w')
        tk.Label(op_info,
            text="Ingest extracted transcripts into the Trajanus Knowledge Base. Files are chunked, embedded, and stored for semantic search.",
            font=('Segoe UI', 8),
            bg=self.colors['bg'],
            fg=self.colors['text_dim'],
            wraplength=560,
            justify='left').pack(anchor='w', pady=(0, 6))

        tk.Label(op_info,
            text="FULL PIPELINE",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']).pack(anchor='w')
        tk.Label(op_info,
            text="Run complete workflow: Scan YouTube -> Extract transcripts from results -> Ingest all to KB. Automated end-to-end processing.",
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

        # URL input row
        url_row = tk.Frame(self.current_frame, bg=self.colors['bg'])
        url_row.pack(fill='x', pady=(0, 10))

        tk.Label(url_row,
            text="VIDEO URL:",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']).pack(side='left')

        self.url_entry = tk.Entry(url_row, textvariable=self.video_url, width=50,
            font=('Segoe UI', 9), bg=self.colors['bg_light'], fg=self.colors['text'],
            insertbackground=self.colors['text'])
        self.url_entry.pack(side='left', padx=(10, 0), fill='x', expand=True)

        # Button row 1
        btn_row1 = tk.Frame(self.current_frame, bg=self.colors['bg'])
        btn_row1.pack(fill='x', pady=(0, 8))

        BeveledButton(btn_row1, "SCAN YOUTUBE",
                     command=self.scan_youtube, width=140, height=36, palette=self.colors).pack(side='left', padx=(0, 10))
        BeveledButton(btn_row1, "EXTRACT TRANSCRIPT",
                     command=self.extract_transcript, width=160, height=36, palette=self.colors).pack(side='left', padx=(0, 10))
        BeveledButton(btn_row1, "INGEST TO KB",
                     command=self.ingest_to_kb, width=130, height=36, palette=self.colors).pack(side='left')

        # Button row 2
        btn_row2 = tk.Frame(self.current_frame, bg=self.colors['bg'])
        btn_row2.pack(fill='x', pady=(0, 8))

        BeveledButton(btn_row2, "FULL PIPELINE",
                     command=self.run_full_pipeline, width=140, height=36, palette=self.colors).pack(side='left', padx=(0, 10))
        BeveledButton(btn_row2, "BATCH EXTRACT",
                     command=self.batch_extract, width=140, height=36, palette=self.colors).pack(side='left')

        # Exit button row
        exit_row = tk.Frame(self.current_frame, bg=self.colors['bg'])
        exit_row.pack(fill='x', pady=(8, 0))
        BeveledButton(exit_row, "EXIT", command=self.root.quit,
                     width=80, height=30, style='dark', palette=self.colors).pack(side='right')

    def update_status(self, message):
        """Update status bar"""
        self.status_label.config(text=message)
        self.root.update()

    def scan_youtube(self):
        """Scan YouTube for videos"""
        if self.processing:
            return
        self.processing = True
        self.update_status("Scanning YouTube...")

        def do_scan():
            try:
                # Import and run youtube scanner
                import youtube_scanner
                videos = youtube_scanner.scan_youtube()

                # Generate briefing
                import research_agent
                briefing_path = research_agent.generate_briefing(videos)

                self.root.after(0, lambda: self.update_status(f"Scan complete: {len(videos)} videos found"))
                self.root.after(0, lambda: messagebox.showinfo("Scan Complete",
                    f"Found {len(videos)} videos\nBriefing saved to:\n{briefing_path}"))
            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"Error: {str(e)}"))
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            finally:
                self.processing = False

        threading.Thread(target=do_scan, daemon=True).start()

    def extract_transcript(self):
        """Extract transcript from URL"""
        url = self.video_url.get().strip()
        if not url:
            messagebox.showwarning("No URL", "Please enter a YouTube video URL")
            return

        if self.processing:
            return
        self.processing = True
        self.update_status("Extracting transcript...")

        def do_extract():
            try:
                # Run the extract script
                script_path = SCRIPT_DIR / "extract_youtube_transcript.py"
                result = subprocess.run(
                    [sys.executable, str(script_path), url],
                    capture_output=True, text=True, cwd=str(SCRIPT_DIR)
                )

                if result.returncode == 0:
                    self.root.after(0, lambda: self.update_status("Transcript extracted successfully"))
                    self.root.after(0, lambda: messagebox.showinfo("Success", "Transcript extracted successfully"))
                else:
                    raise Exception(result.stderr or "Unknown error")
            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"Error: {str(e)}"))
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            finally:
                self.processing = False

        threading.Thread(target=do_extract, daemon=True).start()

    def ingest_to_kb(self):
        """Ingest files to knowledge base"""
        folder = filedialog.askdirectory(title="Select folder with transcripts to ingest")
        if not folder:
            return

        if self.processing:
            return
        self.processing = True
        self.update_status("Ingesting to KB...")

        def do_ingest():
            try:
                import kb_ingester
                results = kb_ingester.ingest_folder(folder)

                self.root.after(0, lambda: self.update_status(f"Ingested {results.get('count', 0)} files"))
                self.root.after(0, lambda: messagebox.showinfo("Ingest Complete",
                    f"Ingested {results.get('count', 0)} files to knowledge base"))
            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"Error: {str(e)}"))
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            finally:
                self.processing = False

        threading.Thread(target=do_ingest, daemon=True).start()

    def batch_extract(self):
        """Batch extract transcripts from file list"""
        file_path = filedialog.askopenfilename(
            title="Select file with YouTube URLs (one per line)",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not file_path:
            return

        if self.processing:
            return
        self.processing = True
        self.update_status("Running batch extraction...")

        def do_batch():
            try:
                script_path = SCRIPT_DIR / "batch_extract_transcripts.py"
                result = subprocess.run(
                    [sys.executable, str(script_path), file_path],
                    capture_output=True, text=True, cwd=str(SCRIPT_DIR)
                )

                if result.returncode == 0:
                    self.root.after(0, lambda: self.update_status("Batch extraction complete"))
                    self.root.after(0, lambda: messagebox.showinfo("Success", "Batch extraction complete"))
                else:
                    raise Exception(result.stderr or "Unknown error")
            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"Error: {str(e)}"))
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            finally:
                self.processing = False

        threading.Thread(target=do_batch, daemon=True).start()

    def run_full_pipeline(self):
        """Run complete pipeline: scan -> extract -> ingest"""
        if self.processing:
            return
        self.processing = True
        self.update_status("Running full pipeline...")

        def do_pipeline():
            try:
                import research_agent
                research_agent.run_research()

                self.root.after(0, lambda: self.update_status("Pipeline complete"))
                self.root.after(0, lambda: messagebox.showinfo("Pipeline Complete",
                    "Full research pipeline completed successfully"))
            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"Error: {str(e)}"))
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            finally:
                self.processing = False

        threading.Thread(target=do_pipeline, daemon=True).start()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TrajanusYouTubeTool()
    app.run()
