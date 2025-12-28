#!/usr/bin/env python3
"""
TRAJANUS QUERY KB TOOL
Search and browse the knowledge base
Standard Tool UI Template
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


class TrajanusQueryKBGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Trajanus - Query KB Tool")
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
        self.searching = False
        self.sources_list = []

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
            text="TRAJANUS QUERY KB",
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
            text="Welcome to the Query KB Tool",
            font=('Segoe UI', 16),
            bg=self.colors['bg'],
            fg=self.colors['text'])
        welcome.pack(pady=(0, 20))

        # Info card
        info_frame = tk.Frame(self.current_frame, bg=self.colors['card'], padx=25, pady=20)
        info_frame.pack(fill='x', pady=(0, 25))

        info_text = """This tool searches the Trajanus Knowledge Base.

HOW IT WORKS:
  1. Enter a natural language query
  2. Query is converted to embedding vector
  3. Semantic similarity search finds matches
  4. Results ranked by relevance score

FEATURES: Semantic search, browse by source, view recent sessions
TIP: Use natural language - "How do we handle QCM reviews?" """

        tk.Label(info_frame,
            text=info_text,
            font=('Segoe UI', 11),
            bg=self.colors['card'],
            fg=self.colors['text_dim'],
            justify='left').pack(anchor='w')

        # Mode selection title
        tk.Label(self.current_frame,
            text="SELECT QUERY MODE",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text_dim']).pack(pady=(10, 15))

        # Mode buttons container
        btn_container = tk.Frame(self.current_frame, bg=self.colors['bg'])
        btn_container.pack(fill='x')

        # Create mode cards
        self.create_mode_card(btn_container,
            "SEMANTIC SEARCH",
            "Natural language query",
            "AI-powered similarity search",
            self.show_search_screen,
            side='left')

        self.create_mode_card(btn_container,
            "BROWSE SOURCES",
            "View by category",
            "Explore documents by source",
            self.show_sources_screen,
            side='left')

        self.create_mode_card(btn_container,
            "RECENT SESSIONS",
            "View latest entries",
            "See most recent additions",
            self.show_recent_screen,
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
