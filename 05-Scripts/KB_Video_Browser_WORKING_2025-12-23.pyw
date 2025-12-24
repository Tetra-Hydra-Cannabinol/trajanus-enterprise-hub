"""
TRAJANUS KNOWLEDGE BASE - VIDEO BROWSER
Search knowledge base and browse YouTube tutorials with thumbnails.
Transcripts are for Claude's knowledge, videos are for your reference.
"""

import os
import sys
import re
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import threading
import webbrowser
from io import BytesIO
import urllib.request

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

# Thumbnail cache
thumbnail_cache = {}


def extract_video_id(title: str) -> str:
    """Extract YouTube video ID from title format: DATE_LEVEL_VIDEOID_Title"""
    match = re.search(r'\d{4}-\d{2}-\d{2}_[A-Z]+_([a-zA-Z0-9_-]{11})_', title)
    if match:
        return match.group(1)
    return None


def extract_video_info(title: str) -> dict:
    """Extract clean video info from title"""
    # Pattern: 2025-12-19_ADVANCED_wt5-Mcimw78_Word_Advanced_Tutorial
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


def get_thumbnail_url(video_id: str, quality: str = 'mqdefault') -> str:
    """Get YouTube thumbnail URL"""
    # mqdefault = 320x180, hqdefault = 480x360, maxresdefault = 1280x720
    return f"https://img.youtube.com/vi/{video_id}/{quality}.jpg"


class VideoCard(tk.Frame):
    """A card displaying a video with thumbnail"""

    def __init__(self, parent, video_info: dict, similarity: float, source: str, **kwargs):
        super().__init__(parent, bg='#16213e', **kwargs)

        self.video_id = video_info.get('video_id')
        self.video_url = f"https://www.youtube.com/watch?v={self.video_id}" if self.video_id else None

        # Main container
        self.configure(padx=10, pady=10)

        # Left side - Thumbnail
        thumb_frame = tk.Frame(self, bg='#16213e', width=180, height=101)
        thumb_frame.pack(side=tk.LEFT, padx=(0, 15))
        thumb_frame.pack_propagate(False)

        # Thumbnail placeholder
        self.thumb_label = tk.Label(
            thumb_frame,
            text="Loading...",
            bg='#0f0f23',
            fg='#666',
            font=('Segoe UI', 9)
        )
        self.thumb_label.pack(fill=tk.BOTH, expand=True)

        if self.video_id and HAS_PIL:
            self.load_thumbnail()
        elif self.video_id:
            self.thumb_label.config(text="[Thumbnail]", cursor='hand2')
            self.thumb_label.bind('<Button-1>', lambda e: self.open_video())

        # Right side - Info
        info_frame = tk.Frame(self, bg='#16213e')
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Title
        title_text = video_info.get('title', 'Unknown Video')[:70]
        title_label = tk.Label(
            info_frame,
            text=title_text,
            font=('Segoe UI', 12, 'bold'),
            bg='#16213e',
            fg='#00d4ff',
            anchor='w',
            cursor='hand2'
        )
        title_label.pack(fill=tk.X, pady=(0, 5))
        title_label.bind('<Button-1>', lambda e: self.open_video())
        title_label.bind('<Enter>', lambda e: title_label.config(fg='#66e0ff'))
        title_label.bind('<Leave>', lambda e: title_label.config(fg='#00d4ff'))

        # Metadata row
        meta_frame = tk.Frame(info_frame, bg='#16213e')
        meta_frame.pack(fill=tk.X, pady=(0, 8))

        # Level badge
        level = video_info.get('level', '')
        level_colors = {
            'BEGINNER': '#2d6a4f',
            'INTERMEDIATE': '#b5838d',
            'ADVANCED': '#9d4edd',
            'COMPREHENSIVE': '#0077b6'
        }
        if level:
            level_label = tk.Label(
                meta_frame,
                text=f" {level} ",
                font=('Segoe UI', 8, 'bold'),
                bg=level_colors.get(level, '#4a4e69'),
                fg='white'
            )
            level_label.pack(side=tk.LEFT, padx=(0, 10))

        # Date
        date = video_info.get('date', '')
        if date:
            date_label = tk.Label(
                meta_frame,
                text=date,
                font=('Segoe UI', 9),
                bg='#16213e',
                fg='#888'
            )
            date_label.pack(side=tk.LEFT, padx=(0, 10))

        # Similarity
        sim_label = tk.Label(
            meta_frame,
            text=f"{similarity:.0f}% match",
            font=('Segoe UI', 9, 'bold'),
            bg='#16213e',
            fg='#00ff88'
        )
        sim_label.pack(side=tk.LEFT, padx=(0, 10))

        # Source
        source_label = tk.Label(
            meta_frame,
            text=source,
            font=('Segoe UI', 9),
            bg='#16213e',
            fg='#666'
        )
        source_label.pack(side=tk.LEFT)

        # Watch button
        btn_frame = tk.Frame(info_frame, bg='#16213e')
        btn_frame.pack(fill=tk.X)

        if self.video_id:
            watch_btn = tk.Button(
                btn_frame,
                text="Watch on YouTube",
                command=self.open_video,
                font=('Segoe UI', 10, 'bold'),
                bg='#c9184a',
                fg='white',
                activebackground='#ff4d6d',
                relief=tk.FLAT,
                padx=20,
                pady=6,
                cursor='hand2'
            )
            watch_btn.pack(side=tk.LEFT)

    def load_thumbnail(self):
        """Load thumbnail in background"""
        def fetch():
            try:
                if self.video_id in thumbnail_cache:
                    img = thumbnail_cache[self.video_id]
                else:
                    url = get_thumbnail_url(self.video_id, 'mqdefault')
                    with urllib.request.urlopen(url, timeout=5) as response:
                        data = response.read()
                    img = Image.open(BytesIO(data))
                    img = img.resize((180, 101), Image.Resampling.LANCZOS)
                    thumbnail_cache[self.video_id] = img

                # Update UI in main thread
                self.after(0, lambda: self.set_thumbnail(img))
            except Exception as e:
                self.after(0, lambda: self.thumb_label.config(text="[No Thumb]"))

        thread = threading.Thread(target=fetch, daemon=True)
        thread.start()

    def set_thumbnail(self, img):
        """Set thumbnail image"""
        try:
            photo = ImageTk.PhotoImage(img)
            self.thumb_label.config(image=photo, text='', cursor='hand2')
            self.thumb_label.image = photo  # Keep reference
            self.thumb_label.bind('<Button-1>', lambda e: self.open_video())
        except:
            self.thumb_label.config(text="[Thumb Error]")

    def open_video(self):
        """Open video in browser"""
        if self.video_url:
            webbrowser.open(self.video_url)


class KBSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trajanus Knowledge Base - Video Browser")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a2e')

        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#1a1a2e')
        style.configure('TLabel', background='#1a1a2e', foreground='#eef', font=('Segoe UI', 11))
        style.configure('Header.TLabel', font=('Segoe UI', 20, 'bold'), foreground='#00d4ff')

        # Main frame
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header = ttk.Label(main_frame, text="Trajanus Video Browser", style='Header.TLabel')
        header.pack(pady=(0, 5))

        subheader = ttk.Label(main_frame, text="Search knowledge base • Watch tutorial videos",
                             font=('Segoe UI', 10), foreground='#888')
        subheader.pack(pady=(0, 20))

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
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=12, padx=(0, 10))
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
            pady=12,
            cursor='hand2'
        )
        self.search_btn.pack(side=tk.RIGHT)

        # Status label
        self.status_var = tk.StringVar(value="Enter a topic to find relevant video tutorials")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.pack(pady=(0, 10))

        # Results container with scrollbar
        results_container = ttk.Frame(main_frame)
        results_container.pack(fill=tk.BOTH, expand=True)

        # Canvas and scrollbar
        self.canvas = tk.Canvas(results_container, bg='#0f0f23', highlightthickness=0)
        scrollbar = ttk.Scrollbar(results_container, orient=tk.VERTICAL, command=self.canvas.yview)

        self.results_frame = tk.Frame(self.canvas, bg='#0f0f23')
        self.results_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        self.canvas_window = self.canvas.create_window((0, 0), window=self.results_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Footer
        if not HAS_PIL:
            footer_text = "Install Pillow for thumbnails: pip install Pillow"
        else:
            footer_text = "Click video title or thumbnail to watch on YouTube"
        footer = ttk.Label(main_frame, text=footer_text, font=('Segoe UI', 9), foreground='#666')
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

            # Search with higher count to get enough unique videos
            result = supabase.rpc(
                'match_knowledge_base',
                {
                    'query_embedding': query_embedding,
                    'match_threshold': 0.25,
                    'match_count': 50  # Get more to deduplicate
                }
            ).execute()

            self.root.after(0, lambda: self.display_results(query, result.data))

        except Exception as e:
            self.root.after(0, lambda: self.display_error(str(e)))

    def display_results(self, query, docs):
        self.search_btn.config(state=tk.NORMAL, text="Search")

        if not docs:
            self.status_var.set("No results found")
            no_results = tk.Label(
                self.results_frame,
                text="No matching videos found.\n\nTry different search terms.",
                font=('Segoe UI', 12),
                bg='#0f0f23',
                fg='#888'
            )
            no_results.pack(pady=50)
            return

        # Deduplicate by video ID - keep highest similarity for each video
        videos_seen = {}
        for doc in docs:
            title = doc.get('title', '')
            video_info = extract_video_info(title)

            if video_info and video_info.get('video_id'):
                vid = video_info['video_id']
                similarity = doc.get('similarity', 0) * 100
                source = doc.get('metadata', {}).get('source', 'Unknown')

                if vid not in videos_seen or similarity > videos_seen[vid]['similarity']:
                    videos_seen[vid] = {
                        'video_info': video_info,
                        'similarity': similarity,
                        'source': source
                    }

        unique_videos = list(videos_seen.values())
        unique_videos.sort(key=lambda x: x['similarity'], reverse=True)

        # Limit to top 15 videos
        unique_videos = unique_videos[:15]

        self.status_var.set(f"Found {len(unique_videos)} videos for: {query}")

        for video_data in unique_videos:
            card = VideoCard(
                self.results_frame,
                video_data['video_info'],
                video_data['similarity'],
                video_data['source']
            )
            card.pack(fill=tk.X, padx=5, pady=5)

        self.canvas.yview_moveto(0)

    def display_error(self, error):
        self.search_btn.config(state=tk.NORMAL, text="Search")
        self.status_var.set("Error occurred")
        error_label = tk.Label(
            self.results_frame,
            text=f"Error: {error}",
            font=('Segoe UI', 11),
            bg='#0f0f23',
            fg='#ff6b6b'
        )
        error_label.pack(pady=50)


def main():
    root = tk.Tk()
    app = KBSearchApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
