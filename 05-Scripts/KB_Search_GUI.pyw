"""
TRAJANUS KNOWLEDGE BASE - UNIFIED BROWSER
Combines: Video Search + File Upload + Local Folder Browse
"""

import os
import sys
import re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import threading
import webbrowser
from io import BytesIO
import urllib.request
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

# Try to import PIL for thumbnails
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# Initialize clients
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_ANON_KEY')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
openai_client = OpenAI(api_key=OPENAI_KEY)

# Paths
GDRIVE_BASE = Path(r'G:\My Drive\00 - Trajanus USA')
SCRIPTS_PATH = GDRIVE_BASE / '00-Command-Center' / '05-Scripts'

# Thumbnail cache
thumbnail_cache = {}

# Color scheme (matching TKB)
COLORS = {
    'bg_dark': '#1a1a2e',
    'bg_panel': '#16213e',
    'bg_input': '#0f0f23',
    'gold': '#9B7E52',
    'gold_dark': '#7B6142',
    'gold_light': '#c4a574',
    'text': '#ffffff',
    'text_dim': '#888888',
    'green': '#00ff88',
    'red': '#c9184a',
    'blue': '#00d4ff'
}


def extract_video_info(title: str) -> dict:
    """Extract clean video info from title"""
    match = re.match(r'(\d{4}-\d{2}-\d{2})_([A-Z]+)_([a-zA-Z0-9_-]{11})_(.+?)(?:\s*\(Part \d+\))?$', title)
    if match:
        date, level, video_id, name = match.groups()
        clean_name = name.replace('_', ' ').strip()
        return {
            'date': date,
            'level': level,
            'video_id': video_id,
            'title': clean_name
        }
    return None


def get_thumbnail_url(video_id: str) -> str:
    return f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"


class VideoCard(tk.Frame):
    """A card displaying a video with thumbnail"""
    def __init__(self, parent, video_info: dict, similarity: float, source: str, **kwargs):
        super().__init__(parent, bg=COLORS['bg_panel'], **kwargs)
        self.video_id = video_info.get('video_id')
        self.video_url = f"https://www.youtube.com/watch?v={self.video_id}" if self.video_id else None
        self.configure(padx=10, pady=10)

        # Thumbnail
        thumb_frame = tk.Frame(self, bg=COLORS['bg_panel'], width=160, height=90)
        thumb_frame.pack(side=tk.LEFT, padx=(0, 15))
        thumb_frame.pack_propagate(False)

        self.thumb_label = tk.Label(thumb_frame, text="...", bg=COLORS['bg_input'], fg=COLORS['text_dim'])
        self.thumb_label.pack(fill=tk.BOTH, expand=True)

        if self.video_id and HAS_PIL:
            self.load_thumbnail()

        # Info
        info_frame = tk.Frame(self, bg=COLORS['bg_panel'])
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Title
        title_text = video_info.get('title', 'Unknown')[:65]
        title_label = tk.Label(info_frame, text=title_text, font=('Segoe UI', 11, 'bold'),
                              bg=COLORS['bg_panel'], fg=COLORS['blue'], anchor='w', cursor='hand2')
        title_label.pack(fill=tk.X)
        title_label.bind('<Button-1>', lambda e: self.open_video())

        # Meta
        meta_frame = tk.Frame(info_frame, bg=COLORS['bg_panel'])
        meta_frame.pack(fill=tk.X, pady=5)

        level = video_info.get('level', '')
        level_colors = {'BEGINNER': '#2d6a4f', 'INTERMEDIATE': '#b5838d', 'ADVANCED': '#9d4edd', 'COMPREHENSIVE': '#0077b6'}
        if level:
            tk.Label(meta_frame, text=f" {level} ", font=('Segoe UI', 8, 'bold'),
                    bg=level_colors.get(level, COLORS['gold']), fg='white').pack(side=tk.LEFT, padx=(0, 8))

        tk.Label(meta_frame, text=f"{similarity:.0f}% match", font=('Segoe UI', 9, 'bold'),
                bg=COLORS['bg_panel'], fg=COLORS['green']).pack(side=tk.LEFT, padx=(0, 8))
        tk.Label(meta_frame, text=source, font=('Segoe UI', 9),
                bg=COLORS['bg_panel'], fg=COLORS['text_dim']).pack(side=tk.LEFT)

        # Watch button
        tk.Button(info_frame, text="Watch on YouTube", command=self.open_video,
                 font=('Segoe UI', 9, 'bold'), bg=COLORS['red'], fg='white',
                 relief=tk.FLAT, padx=15, pady=4, cursor='hand2').pack(anchor='w', pady=(5, 0))

    def load_thumbnail(self):
        def fetch():
            try:
                if self.video_id in thumbnail_cache:
                    img = thumbnail_cache[self.video_id]
                else:
                    url = get_thumbnail_url(self.video_id)
                    with urllib.request.urlopen(url, timeout=5) as response:
                        data = response.read()
                    img = Image.open(BytesIO(data))
                    img = img.resize((160, 90), Image.Resampling.LANCZOS)
                    thumbnail_cache[self.video_id] = img
                self.after(0, lambda: self.set_thumbnail(img))
            except:
                pass
        threading.Thread(target=fetch, daemon=True).start()

    def set_thumbnail(self, img):
        try:
            photo = ImageTk.PhotoImage(img)
            self.thumb_label.config(image=photo, text='', cursor='hand2')
            self.thumb_label.image = photo
            self.thumb_label.bind('<Button-1>', lambda e: self.open_video())
        except:
            pass

    def open_video(self):
        if self.video_url:
            webbrowser.open(self.video_url)


class TrajanusBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("Trajanus Knowledge Base")
        self.root.geometry("1000x750")
        self.root.configure(bg=COLORS['bg_dark'])

        self.selected_files = []

        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=COLORS['bg_dark'])
        style.configure('TLabel', background=COLORS['bg_dark'], foreground=COLORS['text'])
        style.configure('TNotebook', background=COLORS['bg_dark'])
        style.configure('TNotebook.Tab', background=COLORS['gold_dark'], foreground='white',
                       padding=[15, 8], font=('Segoe UI', 10, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', COLORS['gold'])])

        # Header
        header = tk.Frame(root, bg=COLORS['gold'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="Trajanus Knowledge Base", font=('Segoe UI', 18, 'bold'),
                bg=COLORS['gold'], fg='white').pack(side=tk.LEFT, padx=20, pady=15)

        # Get KB stats
        self.kb_count = self.get_kb_count()
        tk.Label(header, text=f"{self.kb_count:,} chunks", font=('Segoe UI', 10),
                bg=COLORS['gold'], fg='#eeeeee').pack(side=tk.RIGHT, padx=20)

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1: Video Search
        self.video_tab = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(self.video_tab, text="  Video Search  ")
        self.setup_video_tab()

        # Tab 2: Upload Files
        self.upload_tab = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(self.upload_tab, text="  Upload & Ingest  ")
        self.setup_upload_tab()

        # Tab 3: Browse Folders
        self.browse_tab = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(self.browse_tab, text="  Browse Folders  ")
        self.setup_browse_tab()

    def get_kb_count(self):
        try:
            result = supabase.table('knowledge_base').select('id', count='exact').execute()
            return result.count or 0
        except:
            return 0

    # ==================== VIDEO SEARCH TAB ====================
    def setup_video_tab(self):
        # Search frame
        search_frame = tk.Frame(self.video_tab, bg=COLORS['bg_dark'])
        search_frame.pack(fill=tk.X, padx=20, pady=15)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                    font=('Segoe UI', 13), bg=COLORS['bg_input'],
                                    fg=COLORS['text'], insertbackground='white',
                                    relief=tk.FLAT)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=(0, 10))
        self.search_entry.bind('<Return>', lambda e: self.search_videos())
        self.search_entry.insert(0, "Search for tutorials...")
        self.search_entry.bind('<FocusIn>', lambda e: self.search_entry.delete(0, tk.END) if self.search_entry.get() == "Search for tutorials..." else None)

        self.search_btn = tk.Button(search_frame, text="Search", command=self.search_videos,
                                   font=('Segoe UI', 11, 'bold'), bg=COLORS['gold'],
                                   fg='white', relief=tk.FLAT, padx=25, pady=10, cursor='hand2')
        self.search_btn.pack(side=tk.RIGHT)

        # Status
        self.video_status = tk.StringVar(value="Enter a topic to find video tutorials")
        tk.Label(self.video_tab, textvariable=self.video_status,
                font=('Segoe UI', 10), bg=COLORS['bg_dark'], fg=COLORS['text_dim']).pack()

        # Results
        results_container = tk.Frame(self.video_tab, bg=COLORS['bg_dark'])
        results_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.video_canvas = tk.Canvas(results_container, bg=COLORS['bg_input'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(results_container, orient=tk.VERTICAL, command=self.video_canvas.yview)

        self.video_results = tk.Frame(self.video_canvas, bg=COLORS['bg_input'])
        self.video_results.bind('<Configure>', lambda e: self.video_canvas.configure(scrollregion=self.video_canvas.bbox('all')))

        self.video_canvas_window = self.video_canvas.create_window((0, 0), window=self.video_results, anchor='nw')
        self.video_canvas.configure(yscrollcommand=scrollbar.set)
        self.video_canvas.bind('<Configure>', lambda e: self.video_canvas.itemconfig(self.video_canvas_window, width=e.width))
        self.video_canvas.bind_all('<MouseWheel>', lambda e: self.video_canvas.yview_scroll(int(-1*(e.delta/120)), 'units'))

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.video_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def search_videos(self):
        query = self.search_var.get().strip()
        if not query or query == "Search for tutorials...":
            return

        self.search_btn.config(state=tk.DISABLED, text="...")
        self.video_status.set(f"Searching: {query}")
        for w in self.video_results.winfo_children():
            w.destroy()

        threading.Thread(target=self.do_video_search, args=(query,)).start()

    def do_video_search(self, query):
        try:
            response = openai_client.embeddings.create(input=query, model="text-embedding-3-small")
            query_embedding = response.data[0].embedding

            result = supabase.rpc('match_knowledge_base', {
                'query_embedding': query_embedding,
                'match_threshold': 0.25,
                'match_count': 50
            }).execute()

            self.root.after(0, lambda: self.display_video_results(query, result.data))
        except Exception as e:
            self.root.after(0, lambda: self.video_status.set(f"Error: {e}"))
            self.root.after(0, lambda: self.search_btn.config(state=tk.NORMAL, text="Search"))

    def display_video_results(self, query, docs):
        self.search_btn.config(state=tk.NORMAL, text="Search")

        videos_seen = {}
        for doc in docs:
            video_info = extract_video_info(doc.get('title', ''))
            if video_info and video_info.get('video_id'):
                vid = video_info['video_id']
                similarity = doc.get('similarity', 0) * 100
                source = doc.get('metadata', {}).get('source', 'Unknown')
                if vid not in videos_seen or similarity > videos_seen[vid]['similarity']:
                    videos_seen[vid] = {'video_info': video_info, 'similarity': similarity, 'source': source}

        unique_videos = sorted(videos_seen.values(), key=lambda x: x['similarity'], reverse=True)[:15]
        self.video_status.set(f"Found {len(unique_videos)} videos for: {query}")

        for video_data in unique_videos:
            card = VideoCard(self.video_results, video_data['video_info'],
                           video_data['similarity'], video_data['source'])
            card.pack(fill=tk.X, padx=5, pady=5)

        self.video_canvas.yview_moveto(0)

    # ==================== UPLOAD TAB ====================
    def setup_upload_tab(self):
        main = tk.Frame(self.upload_tab, bg=COLORS['bg_dark'])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Drop zone
        self.drop_zone = tk.Frame(main, bg=COLORS['bg_input'], highlightbackground=COLORS['gold'],
                                 highlightthickness=3, height=150)
        self.drop_zone.pack(fill=tk.X, pady=(0, 20))
        self.drop_zone.pack_propagate(False)

        drop_content = tk.Frame(self.drop_zone, bg=COLORS['bg_input'])
        drop_content.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(drop_content, text="+", font=('Segoe UI', 36), bg=COLORS['bg_input'],
                fg=COLORS['gold']).pack()
        tk.Label(drop_content, text="Click to Select Files for Ingestion", font=('Segoe UI', 12),
                bg=COLORS['bg_input'], fg=COLORS['text']).pack()
        tk.Label(drop_content, text="Supports: .txt, .md, .docx, .pdf", font=('Segoe UI', 9),
                bg=COLORS['bg_input'], fg=COLORS['text_dim']).pack()

        self.drop_zone.bind('<Button-1>', lambda e: self.select_files())
        for child in self.drop_zone.winfo_children():
            child.bind('<Button-1>', lambda e: self.select_files())
            for grandchild in child.winfo_children():
                grandchild.bind('<Button-1>', lambda e: self.select_files())

        # Selected files list
        files_frame = tk.Frame(main, bg=COLORS['bg_panel'], padx=15, pady=15)
        files_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(files_frame, text="Selected Files:", font=('Segoe UI', 11, 'bold'),
                bg=COLORS['bg_panel'], fg=COLORS['gold']).pack(anchor='w')

        self.files_list = tk.Frame(files_frame, bg=COLORS['bg_panel'])
        self.files_list.pack(fill=tk.X, pady=10)
        self.files_label = tk.Label(self.files_list, text="No files selected",
                                   font=('Segoe UI', 10), bg=COLORS['bg_panel'], fg=COLORS['text_dim'])
        self.files_label.pack(anchor='w')

        # Category selector
        cat_frame = tk.Frame(main, bg=COLORS['bg_dark'])
        cat_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(cat_frame, text="Category:", font=('Segoe UI', 11, 'bold'),
                bg=COLORS['bg_dark'], fg=COLORS['text']).pack(side=tk.LEFT)

        self.category_var = tk.StringVar(value="YouTube Tutorials")
        categories = ["YouTube Tutorials", "Session History", "Core Protocols",
                     "Research", "Technical Docs", "LangChain Tutorials"]
        self.category_menu = ttk.Combobox(cat_frame, textvariable=self.category_var,
                                         values=categories, state='readonly', width=30)
        self.category_menu.pack(side=tk.LEFT, padx=10)

        # Ingest button
        self.ingest_btn = tk.Button(main, text="Ingest Selected Files to Knowledge Base",
                                   command=self.ingest_files, font=('Segoe UI', 12, 'bold'),
                                   bg=COLORS['gold'], fg='white', relief=tk.FLAT,
                                   pady=12, cursor='hand2', state=tk.DISABLED)
        self.ingest_btn.pack(fill=tk.X)

        # Progress
        self.ingest_status = tk.StringVar(value="")
        tk.Label(main, textvariable=self.ingest_status, font=('Segoe UI', 10),
                bg=COLORS['bg_dark'], fg=COLORS['green']).pack(pady=10)

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select Files to Ingest",
            filetypes=[("Text files", "*.txt"), ("Markdown", "*.md"),
                      ("All supported", "*.txt *.md *.docx *.pdf")]
        )
        if files:
            self.selected_files = list(files)
            self.update_files_list()

    def update_files_list(self):
        for w in self.files_list.winfo_children():
            w.destroy()

        if not self.selected_files:
            tk.Label(self.files_list, text="No files selected",
                    font=('Segoe UI', 10), bg=COLORS['bg_panel'], fg=COLORS['text_dim']).pack(anchor='w')
            self.ingest_btn.config(state=tk.DISABLED)
            return

        for f in self.selected_files:
            fname = Path(f).name
            size = os.path.getsize(f)
            size_str = f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/(1024*1024):.1f} MB"

            row = tk.Frame(self.files_list, bg=COLORS['bg_panel'])
            row.pack(fill=tk.X, pady=2)
            tk.Label(row, text=f"  {fname}", font=('Segoe UI', 10),
                    bg=COLORS['bg_panel'], fg=COLORS['text']).pack(side=tk.LEFT)
            tk.Label(row, text=size_str, font=('Segoe UI', 9),
                    bg=COLORS['bg_panel'], fg=COLORS['text_dim']).pack(side=tk.LEFT, padx=10)

        self.ingest_btn.config(state=tk.NORMAL)

    def ingest_files(self):
        if not self.selected_files:
            return

        category = self.category_var.get()
        self.ingest_btn.config(state=tk.DISABLED, text="Ingesting...")
        self.ingest_status.set("Starting ingestion...")

        threading.Thread(target=self.do_ingest, args=(self.selected_files.copy(), category)).start()

    def do_ingest(self, files, category):
        try:
            total_chunks = 0
            for i, filepath in enumerate(files, 1):
                self.root.after(0, lambda i=i, f=Path(filepath).name: self.ingest_status.set(f"Processing {i}/{len(files)}: {f}"))

                # Read file
                with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()

                # Chunk
                chunks = []
                chunk_size, overlap = 1000, 200
                start = 0
                while start < len(content):
                    chunk = content[start:start+chunk_size]
                    if chunk.strip():
                        chunks.append(chunk)
                    start += chunk_size - overlap

                # Ingest chunks
                for j, chunk in enumerate(chunks, 1):
                    response = openai_client.embeddings.create(input=chunk, model="text-embedding-3-small")
                    embedding = response.data[0].embedding

                    data = {
                        'url': f'file:///{filepath}',
                        'chunk_number': j,
                        'title': f"{Path(filepath).stem} (Part {j})",
                        'summary': ' '.join(chunk.split()[:20]) + '...',
                        'content': chunk,
                        'metadata': {'source': category, 'filename': Path(filepath).name},
                        'embedding': embedding
                    }
                    supabase.table('knowledge_base').insert(data).execute()
                    total_chunks += 1

            self.root.after(0, lambda: self.ingest_complete(total_chunks))
        except Exception as e:
            self.root.after(0, lambda: self.ingest_status.set(f"Error: {e}"))
            self.root.after(0, lambda: self.ingest_btn.config(state=tk.NORMAL, text="Ingest Selected Files to Knowledge Base"))

    def ingest_complete(self, total_chunks):
        self.ingest_status.set(f"Success! Added {total_chunks} chunks to knowledge base")
        self.ingest_btn.config(state=tk.NORMAL, text="Ingest Selected Files to Knowledge Base")
        self.selected_files = []
        self.update_files_list()
        self.kb_count = self.get_kb_count()

    # ==================== BROWSE TAB ====================
    def setup_browse_tab(self):
        main = tk.Frame(self.browse_tab, bg=COLORS['bg_dark'])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Folder buttons
        btn_frame = tk.Frame(main, bg=COLORS['bg_dark'])
        btn_frame.pack(fill=tk.X, pady=(0, 15))

        folders = [
            ("Trajanus USA", GDRIVE_BASE),
            ("Scripts", SCRIPTS_PATH),
            ("Knowledge Base", GDRIVE_BASE / '00-Command-Center' / '13-Knowledge-Base'),
            ("Transcripts", GDRIVE_BASE / '00-Command-Center' / 'knowledge_Archive' / 'Transcripts'),
        ]

        for name, path in folders:
            btn = tk.Button(btn_frame, text=name, command=lambda p=path: self.browse_folder(p),
                           font=('Segoe UI', 10, 'bold'), bg=COLORS['gold_dark'],
                           fg='white', relief=tk.FLAT, padx=15, pady=8, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=(0, 10))

        # Current path
        self.current_path = tk.StringVar(value="Select a folder to browse")
        tk.Label(main, textvariable=self.current_path, font=('Segoe UI', 10),
                bg=COLORS['bg_dark'], fg=COLORS['gold']).pack(anchor='w', pady=(0, 10))

        # File list
        list_frame = tk.Frame(main, bg=COLORS['bg_panel'])
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.folder_canvas = tk.Canvas(list_frame, bg=COLORS['bg_panel'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.folder_canvas.yview)

        self.folder_content = tk.Frame(self.folder_canvas, bg=COLORS['bg_panel'])
        self.folder_content.bind('<Configure>', lambda e: self.folder_canvas.configure(scrollregion=self.folder_canvas.bbox('all')))

        self.folder_canvas_window = self.folder_canvas.create_window((0, 0), window=self.folder_content, anchor='nw')
        self.folder_canvas.configure(yscrollcommand=scrollbar.set)
        self.folder_canvas.bind('<Configure>', lambda e: self.folder_canvas.itemconfig(self.folder_canvas_window, width=e.width))

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.folder_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def browse_folder(self, path):
        if not path.exists():
            messagebox.showerror("Error", f"Folder not found:\n{path}")
            return

        self.current_path.set(str(path))

        for w in self.folder_content.winfo_children():
            w.destroy()

        # Back button if not root
        if path != GDRIVE_BASE:
            back_btn = tk.Button(self.folder_content, text=".. (Go Up)",
                               command=lambda: self.browse_folder(path.parent),
                               font=('Segoe UI', 10), bg=COLORS['bg_input'],
                               fg=COLORS['gold'], relief=tk.FLAT, anchor='w', padx=10, pady=8)
            back_btn.pack(fill=tk.X, pady=2)

        # List folders first
        try:
            items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        except PermissionError:
            tk.Label(self.folder_content, text="Permission denied",
                    bg=COLORS['bg_panel'], fg=COLORS['red']).pack()
            return

        for item in items[:100]:  # Limit to 100 items
            if item.name.startswith('.') or item.name.startswith('~'):
                continue

            is_dir = item.is_dir()
            icon = "" if is_dir else ""
            color = COLORS['gold'] if is_dir else COLORS['text']

            btn = tk.Button(self.folder_content, text=f"{icon} {item.name}",
                          command=lambda p=item: self.item_clicked(p),
                          font=('Segoe UI', 10), bg=COLORS['bg_panel'],
                          fg=color, relief=tk.FLAT, anchor='w', padx=10, pady=6,
                          cursor='hand2')
            btn.pack(fill=tk.X, pady=1)

    def item_clicked(self, path):
        if path.is_dir():
            self.browse_folder(path)
        else:
            # Open file
            try:
                os.startfile(str(path))
            except:
                webbrowser.open(str(path))


def main():
    root = tk.Tk()
    app = TrajanusBrowser(root)
    root.mainloop()


if __name__ == "__main__":
    main()
