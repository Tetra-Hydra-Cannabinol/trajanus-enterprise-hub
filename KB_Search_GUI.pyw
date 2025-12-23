"""
TRAJANUS KNOWLEDGE BASE SEARCH GUI
Double-click to launch a search interface for the knowledge base.
Features: Clickable results to open transcripts or watch YouTube videos.
"""

import os
import sys
import re
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from pathlib import Path
import threading
import webbrowser
import subprocess

# Load environment
def load_env():
    env_path = Path(r'G:\My Drive\00 - Trajanus USA\00-Command-Center\.env')
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env()

from openai import OpenAI
from supabase import create_client

# Initialize clients
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_ANON_KEY')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
openai_client = OpenAI(api_key=OPENAI_KEY)

# Base paths for transcripts
GDRIVE_BASE = Path(r'G:\My Drive\00 - Trajanus USA')
TRANSCRIPT_PATHS = [
    GDRIVE_BASE / '00-Command-Center' / '13-Knowledge-Base' / 'Transcripts',
    GDRIVE_BASE / '01-Morning-Sessions' / 'Research',
    GDRIVE_BASE / '00-Command-Center' / 'knowledge_Archive' / 'Transcripts',
]


def extract_video_id(title: str) -> str:
    """Extract YouTube video ID from title format: DATE_LEVEL_VIDEOID_Title"""
    # Pattern: 2025-12-19_ADVANCED_wt5-Mcimw78_Word_Advanced...
    match = re.search(r'\d{4}-\d{2}-\d{2}_[A-Z]+_([a-zA-Z0-9_-]{11})_', title)
    if match:
        return match.group(1)
    return None


def find_transcript_file(filename: str, url: str = None) -> Path:
    """Find the transcript file on disk"""
    # Try to extract path from URL
    if url and url.startswith('file:///'):
        rel_path = url[8:].replace('/', '\\')
        full_path = GDRIVE_BASE / rel_path
        if full_path.exists():
            return full_path

    # Search in known transcript locations
    for base_path in TRANSCRIPT_PATHS:
        if base_path.exists():
            # Direct match
            direct = base_path / filename
            if direct.exists():
                return direct

            # Search subdirectories
            for f in base_path.rglob(filename):
                return f

    return None


class KBSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trajanus Knowledge Base Search")
        self.root.geometry("1000x800")
        self.root.configure(bg='#1a1a2e')
        self.results_data = []  # Store search results

        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#1a1a2e')
        style.configure('TLabel', background='#1a1a2e', foreground='#eef', font=('Segoe UI', 11))
        style.configure('TButton', font=('Segoe UI', 10), padding=5)
        style.configure('Header.TLabel', font=('Segoe UI', 18, 'bold'), foreground='#00d4ff')
        style.configure('Action.TButton', font=('Segoe UI', 9, 'bold'))

        # Main frame
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header = ttk.Label(main_frame, text="Trajanus Knowledge Base", style='Header.TLabel')
        header.pack(pady=(0, 20))

        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 15))

        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 14),
            bg='#16213e',
            fg='#fff',
            insertbackground='#fff',
            relief=tk.FLAT,
            width=50
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=(0, 10))
        self.search_entry.bind('<Return>', lambda e: self.search())
        self.search_entry.focus()

        # Search button
        self.search_btn = tk.Button(
            search_frame,
            text="Search",
            command=self.search,
            font=('Segoe UI', 12, 'bold'),
            bg='#0f4c75',
            fg='white',
            activebackground='#3282b8',
            activeforeground='white',
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor='hand2'
        )
        self.search_btn.pack(side=tk.RIGHT)

        # Status label
        self.status_var = tk.StringVar(value="Enter a search query and click Search")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.pack(pady=(0, 10))

        # Results container with scrollbar
        results_container = ttk.Frame(main_frame)
        results_container.pack(fill=tk.BOTH, expand=True)

        # Canvas and scrollbar for results
        self.canvas = tk.Canvas(results_container, bg='#0f0f23', highlightthickness=0)
        scrollbar = ttk.Scrollbar(results_container, orient=tk.VERTICAL, command=self.canvas.yview)

        self.results_frame = ttk.Frame(self.canvas)
        self.results_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        self.canvas_window = self.canvas.create_window((0, 0), window=self.results_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Bind canvas resize to adjust results frame width
        self.canvas.bind('<Configure>', self._on_canvas_configure)

        # Mouse wheel scrolling
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Footer
        footer = ttk.Label(main_frame, text="Click result titles to open transcript | Click 'Watch' to open YouTube video",
                          font=('Segoe UI', 9), foreground='#888')
        footer.pack(pady=(10, 0))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), 'units')

    def search(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("Empty Query", "Please enter a search query")
            return

        self.search_btn.config(state=tk.DISABLED, text="Searching...")
        self.status_var.set(f"Searching for: {query}...")

        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Run search in background thread
        thread = threading.Thread(target=self.do_search, args=(query,))
        thread.start()

    def do_search(self, query):
        try:
            # Generate embedding
            response = openai_client.embeddings.create(
                input=query,
                model="text-embedding-3-small"
            )
            query_embedding = response.data[0].embedding

            # Search database
            result = supabase.rpc(
                'match_knowledge_base',
                {
                    'query_embedding': query_embedding,
                    'match_threshold': 0.3,
                    'match_count': 15
                }
            ).execute()

            # Update UI in main thread
            self.root.after(0, lambda: self.display_results(query, result.data))

        except Exception as e:
            self.root.after(0, lambda: self.display_error(str(e)))

    def display_results(self, query, docs):
        self.search_btn.config(state=tk.NORMAL, text="Search")
        self.results_data = docs

        if not docs:
            self.status_var.set("No results found")
            no_results = ttk.Label(self.results_frame, text="No matching documents found.\n\nTry different search terms.",
                                  font=('Segoe UI', 12))
            no_results.pack(pady=50)
            return

        self.status_var.set(f"Found {len(docs)} results for: {query}")

        for i, doc in enumerate(docs):
            self.create_result_card(i, doc)

        # Scroll to top
        self.canvas.yview_moveto(0)

    def create_result_card(self, index: int, doc: dict):
        """Create a clickable result card"""
        similarity = doc.get('similarity', 0) * 100
        title = doc.get('title', 'Unknown')
        source = doc.get('metadata', {}).get('source', 'Unknown')
        filename = doc.get('metadata', {}).get('filename', '')
        url = doc.get('url', '')
        content = doc.get('content', '')[:400]

        # Extract video ID for YouTube link
        video_id = extract_video_id(title)

        # Find transcript file
        transcript_path = find_transcript_file(filename, url) if filename else None

        # Card frame
        card = tk.Frame(self.results_frame, bg='#16213e', padx=15, pady=12)
        card.pack(fill=tk.X, padx=10, pady=8)

        # Header row with title and similarity
        header_frame = tk.Frame(card, bg='#16213e')
        header_frame.pack(fill=tk.X)

        # Result number and similarity
        info_label = tk.Label(
            header_frame,
            text=f"#{index+1}  |  {similarity:.1f}% match  |  {source}",
            font=('Segoe UI', 9),
            bg='#16213e',
            fg='#00ff88'
        )
        info_label.pack(side=tk.LEFT)

        # Title (clickable if transcript exists)
        # Clean title for display (remove part number)
        display_title = re.sub(r' \(Part \d+\)$', '', title)
        display_title = re.sub(r'^\d{4}-\d{2}-\d{2}_[A-Z]+_[a-zA-Z0-9_-]+_', '', display_title)
        display_title = display_title.replace('_', ' ')[:80]

        title_label = tk.Label(
            card,
            text=display_title or title[:80],
            font=('Segoe UI', 12, 'bold'),
            bg='#16213e',
            fg='#00d4ff',
            cursor='hand2' if transcript_path else 'arrow',
            anchor='w'
        )
        title_label.pack(fill=tk.X, pady=(5, 5))

        if transcript_path:
            title_label.bind('<Button-1>', lambda e, p=transcript_path: self.open_transcript(p))
            title_label.bind('<Enter>', lambda e: title_label.config(fg='#66e0ff'))
            title_label.bind('<Leave>', lambda e: title_label.config(fg='#00d4ff'))

        # Content preview
        content_label = tk.Label(
            card,
            text=content + "..." if len(doc.get('content', '')) > 400 else content,
            font=('Consolas', 10),
            bg='#16213e',
            fg='#aaaaaa',
            justify=tk.LEFT,
            anchor='w',
            wraplength=900
        )
        content_label.pack(fill=tk.X, pady=(0, 10))

        # Action buttons frame
        btn_frame = tk.Frame(card, bg='#16213e')
        btn_frame.pack(fill=tk.X)

        # Open Transcript button
        if transcript_path:
            open_btn = tk.Button(
                btn_frame,
                text="Open Transcript",
                command=lambda p=transcript_path: self.open_transcript(p),
                font=('Segoe UI', 9, 'bold'),
                bg='#2d6a4f',
                fg='white',
                activebackground='#40916c',
                relief=tk.FLAT,
                padx=15,
                pady=5,
                cursor='hand2'
            )
            open_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Watch Video button (if YouTube video)
        if video_id:
            watch_btn = tk.Button(
                btn_frame,
                text="Watch on YouTube",
                command=lambda vid=video_id: self.open_youtube(vid),
                font=('Segoe UI', 9, 'bold'),
                bg='#c9184a',
                fg='white',
                activebackground='#ff4d6d',
                relief=tk.FLAT,
                padx=15,
                pady=5,
                cursor='hand2'
            )
            watch_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Copy content button
        copy_btn = tk.Button(
            btn_frame,
            text="Copy Content",
            command=lambda c=doc.get('content', ''): self.copy_to_clipboard(c),
            font=('Segoe UI', 9),
            bg='#4a4e69',
            fg='white',
            activebackground='#6b6f8a',
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        copy_btn.pack(side=tk.LEFT)

        # File path indicator
        if transcript_path:
            path_label = tk.Label(
                btn_frame,
                text=f"  {transcript_path.name}",
                font=('Segoe UI', 8),
                bg='#16213e',
                fg='#666666'
            )
            path_label.pack(side=tk.RIGHT)

    def open_transcript(self, filepath: Path):
        """Open transcript file in default application"""
        try:
            if filepath.exists():
                os.startfile(str(filepath))
            else:
                messagebox.showerror("File Not Found", f"Could not find:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")

    def open_youtube(self, video_id: str):
        """Open YouTube video in browser"""
        url = f"https://www.youtube.com/watch?v={video_id}"
        webbrowser.open(url)

    def copy_to_clipboard(self, content: str):
        """Copy content to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.status_var.set("Content copied to clipboard!")

    def display_error(self, error):
        self.search_btn.config(state=tk.NORMAL, text="Search")
        self.status_var.set("Error occurred")
        error_label = ttk.Label(self.results_frame, text=f"Error: {error}", foreground='#ff6b6b')
        error_label.pack(pady=50)


def main():
    root = tk.Tk()
    app = KBSearchApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
