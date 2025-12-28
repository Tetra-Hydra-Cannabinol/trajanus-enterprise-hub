#!/usr/bin/env python3
"""
TRAJANUS BATCH INGEST TOOL
Ingest files into the knowledge base with embeddings
Standard Tool UI Template
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


class TrajanusBatchIngestGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Trajanus - Batch Ingest Tool")
        self.root.geometry("624x520")
        self.root.resizable(True, True)
        self.root.minsize(480, 400)

        # Standard colors (all tools use same palette)
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

        self.setup_header()
        self.connect_services()
        self.show_welcome_screen()

    def setup_header(self):
        """Create persistent header"""
        self.header = tk.Frame(self.root, bg=self.colors['accent'], height=60)
        self.header.pack(fill='x')
        self.header.pack_propagate(False)

        title = tk.Label(self.header,
            text="TRAJANUS BATCH INGEST",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['accent'],
            fg='#1a1a1a')
        title.pack(pady=15)

        # Connection status bar
        self.status_bar = tk.Frame(self.root, bg=self.colors['border'], height=30)
        self.status_bar.pack(fill='x')
        self.status_bar.pack_propagate(False)

        self.connection_label = tk.Label(self.status_bar,
            text="Connecting to services...",
            font=('Segoe UI', 9),
            bg=self.colors['border'],
            fg=self.colors['text_dim'])
        self.connection_label.pack(side='left', padx=15, pady=5)

        self.connection_status = tk.Label(self.status_bar,
            text="",
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['border'],
            fg=self.colors['warning'])
        self.connection_status.pack(side='right', padx=15, pady=5)

    def clear_content(self):
        """Clear current content frame"""
        if self.current_frame:
            self.current_frame.destroy()

    def show_welcome_screen(self):
        """Display welcome/mode selection screen"""
        self.clear_content()

        self.current_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.current_frame.pack(fill='both', expand=True, padx=40, pady=30)

        # Welcome text
        welcome = tk.Label(self.current_frame,
            text="Welcome to the Batch Ingest Tool",
            font=('Segoe UI', 16),
            bg=self.colors['bg'],
            fg=self.colors['text'])
        welcome.pack(pady=(0, 20))

        # Info card
        info_frame = tk.Frame(self.current_frame, bg=self.colors['card'], padx=25, pady=20)
        info_frame.pack(fill='x', pady=(0, 25))

        info_text = """This tool ingests files into the Trajanus Knowledge Base.

HOW IT WORKS:
  1. Select text files (.txt, .md, .json, etc.)
  2. Choose a source category for organization
  3. Files are chunked and embedded using OpenAI
  4. Stored in Supabase for semantic search

SUPPORTED: .txt, .md, .json, .py, .js, .html, .css, .yaml, .xml
NOTE: Large files are automatically chunked for optimal retrieval."""

        tk.Label(info_frame,
            text=info_text,
            font=('Segoe UI', 11),
            bg=self.colors['card'],
            fg=self.colors['text_dim'],
            justify='left').pack(anchor='w')

        # Category selection
        cat_frame = tk.Frame(self.current_frame, bg=self.colors['bg'])
        cat_frame.pack(fill='x', pady=(0, 15))

        tk.Label(cat_frame,
            text="SOURCE CATEGORY:",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text_dim']).pack(side='left')

        categories = ["General", "Documentation", "Transcripts", "Research", "Code", "Meeting Notes", "Procedures"]
        cat_dropdown = ttk.Combobox(cat_frame, textvariable=self.source_category,
            values=categories, state='readonly', width=20)
        cat_dropdown.pack(side='left', padx=(15, 0))

        # Mode selection title
        tk.Label(self.current_frame,
            text="SELECT INGEST MODE",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text_dim']).pack(pady=(10, 15))

        # Mode buttons container
        btn_container = tk.Frame(self.current_frame, bg=self.colors['bg'])
        btn_container.pack(fill='x')

        # Create mode cards
        self.create_mode_card(btn_container,
            "SINGLE FILE",
            "Select one file to ingest",
            "Best for quick single additions",
            self.select_single_file,
            side='left')

        self.create_mode_card(btn_container,
            "BATCH FOLDER",
            "Ingest all files in a folder",
            "Process entire directory at once",
            self.select_folder,
            side='left')

        self.create_mode_card(btn_container,
            "MULTI-SELECT",
            "Pick multiple specific files",
            "Choose exactly which files to ingest",
            self.select_multiple_files,
            side='left')

        # Exit button at bottom
        exit_frame = tk.Frame(self.current_frame, bg=self.colors['bg'])
        exit_frame.pack(fill='x', pady=(30, 0))

        exit_btn = tk.Button(exit_frame,
            text="Exit",
            font=('Segoe UI', 10),
            bg=self.colors['border'],
            fg=self.colors['text'],
            activebackground='#444444',
            activeforeground=self.colors['text'],
            padx=30, pady=8,
            cursor='hand2',
            relief='flat',
            command=self.root.quit)
        exit_btn.pack(side='right')

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
