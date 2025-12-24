#!/usr/bin/env python3
"""
deep_dive_recall.py
Trajanus USA - Command Center Script

Deep search through session journals, living documents, and code repositories
to find information from past sessions.

Author: Trajanus USA / Claude AI
Created: 2025-12-05
"""

import os
import sys
import re
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# Configuration
TRAJANUS_ROOT = r'G:\My Drive\00 - Trajanus USA'
SEARCH_FOLDERS = [
    ('Session Journals', os.path.join(TRAJANUS_ROOT, '07-Session-Journals')),
    ('Living Documents', os.path.join(TRAJANUS_ROOT, '03-Living-Documents')),
    ('EOS Files', os.path.join(TRAJANUS_ROOT, '08-EOS-Files')),
    ('Core Protocols', os.path.join(TRAJANUS_ROOT, '01-Core-Protocols')),
    ('Command Center', os.path.join(TRAJANUS_ROOT, '00-Command-Center')),
]

SEARCHABLE_EXTENSIONS = ['.md', '.txt', '.html', '.py', '.ps1', '.json']

class DeepDiveRecall:
    def __init__(self, root):
        self.root = root
        self.root.title("Deep Dive Recall - Trajanus Command Center")
        self.root.geometry("900x700")
        self.root.configure(bg='#3d2a1f')
        
        self.setup_ui()
        self.results = []
    
    def setup_ui(self):
        """Setup the user interface."""
        # Title
        title_frame = tk.Frame(self.root, bg='#3d2a1f')
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title = tk.Label(title_frame, text="🔍 Deep Dive Recall", 
                        font=('Segoe UI', 18, 'bold'),
                        bg='#3d2a1f', fg='#e8922a')
        title.pack(side=tk.LEFT)
        
        subtitle = tk.Label(title_frame, text="Search session history and documents",
                           font=('Segoe UI', 10),
                           bg='#3d2a1f', fg='#FFF8F0')
        subtitle.pack(side=tk.LEFT, padx=20)
        
        # Search frame
        search_frame = tk.Frame(self.root, bg='#3d2a1f')
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                     font=('Segoe UI', 12),
                                     bg='#1f1410', fg='#FFF8F0',
                                     insertbackground='#e8922a',
                                     width=50)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind('<Return>', lambda e: self.perform_search())
        
        search_btn = tk.Button(search_frame, text="Search", 
                              command=self.perform_search,
                              font=('Segoe UI', 10, 'bold'),
                              bg='#e8922a', fg='#1f1410',
                              padx=20, pady=5)
        search_btn.pack(side=tk.LEFT, padx=10)
        
        # Options frame
        options_frame = tk.Frame(self.root, bg='#3d2a1f')
        options_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.case_sensitive = tk.BooleanVar(value=False)
        case_check = tk.Checkbutton(options_frame, text="Case Sensitive",
                                    variable=self.case_sensitive,
                                    bg='#3d2a1f', fg='#FFF8F0',
                                    selectcolor='#1f1410',
                                    activebackground='#3d2a1f')
        case_check.pack(side=tk.LEFT)
        
        self.search_dates = tk.BooleanVar(value=False)
        date_check = tk.Checkbutton(options_frame, text="Search by Date (YYYY-MM-DD)",
                                    variable=self.search_dates,
                                    bg='#3d2a1f', fg='#FFF8F0',
                                    selectcolor='#1f1410',
                                    activebackground='#3d2a1f')
        date_check.pack(side=tk.LEFT, padx=20)
        
        # Folder selection
        folder_frame = tk.LabelFrame(self.root, text="Search In:", 
                                     bg='#3d2a1f', fg='#e8922a',
                                     font=('Segoe UI', 10))
        folder_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.folder_vars = {}
        for name, path in SEARCH_FOLDERS:
            var = tk.BooleanVar(value=True)
            self.folder_vars[path] = var
            cb = tk.Checkbutton(folder_frame, text=name, variable=var,
                               bg='#3d2a1f', fg='#FFF8F0',
                               selectcolor='#1f1410',
                               activebackground='#3d2a1f')
            cb.pack(side=tk.LEFT, padx=10)
        
        # Results frame
        results_frame = tk.Frame(self.root, bg='#3d2a1f')
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.results_text = scrolledtext.ScrolledText(results_frame,
                                                       font=('Consolas', 10),
                                                       bg='#1f1410', fg='#FFF8F0',
                                                       insertbackground='#e8922a',
                                                       wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var,
                             font=('Segoe UI', 9),
                             bg='#1f1410', fg='#a89890',
                             anchor=tk.W, padx=10)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def search_file(self, filepath, query, case_sensitive=False):
        """Search a single file for the query."""
        matches = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                search_line = line if case_sensitive else line.lower()
                search_query = query if case_sensitive else query.lower()
                
                if search_query in search_line:
                    # Get context (2 lines before and after)
                    start = max(0, i - 3)
                    end = min(len(lines), i + 2)
                    context = ''.join(lines[start:end])
                    
                    matches.append({
                        'line_num': i,
                        'line': line.strip(),
                        'context': context.strip()
                    })
        
        except Exception as e:
            pass  # Skip files that can't be read
        
        return matches
    
    def perform_search(self):
        """Perform the search across all selected folders."""
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search term")
            return
        
        self.results_text.delete(1.0, tk.END)
        self.results = []
        total_matches = 0
        files_searched = 0
        
        self.status_var.set(f"Searching for: {query}...")
        self.root.update()
        
        case_sensitive = self.case_sensitive.get()
        
        for folder_path, var in self.folder_vars.items():
            if not var.get():
                continue
                
            if not os.path.exists(folder_path):
                continue
            
            for root, dirs, files in os.walk(folder_path):
                # Skip certain directories
                dirs[:] = [d for d in dirs if d.lower() not in ['archive', '.git', 'node_modules', 'credentials']]
                
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext not in SEARCHABLE_EXTENSIONS:
                        continue
                    
                    filepath = os.path.join(root, file)
                    files_searched += 1
                    
                    matches = self.search_file(filepath, query, case_sensitive)
                    
                    if matches:
                        total_matches += len(matches)
                        self.results.append({
                            'file': file,
                            'path': filepath,
                            'matches': matches
                        })
        
        # Display results
        self.display_results(query, files_searched, total_matches)
    
    def display_results(self, query, files_searched, total_matches):
        """Display search results."""
        self.results_text.delete(1.0, tk.END)
        
        header = f"""
{'='*60}
DEEP DIVE RECALL RESULTS
{'='*60}
Query: "{query}"
Files Searched: {files_searched}
Total Matches: {total_matches}
Files with Matches: {len(self.results)}
{'='*60}

"""
        self.results_text.insert(tk.END, header)
        
        if not self.results:
            self.results_text.insert(tk.END, "No matches found.\n")
        else:
            for result in self.results:
                file_header = f"\n📄 {result['file']}\n"
                file_header += f"   Path: {result['path']}\n"
                file_header += f"   Matches: {len(result['matches'])}\n"
                file_header += "-" * 40 + "\n"
                
                self.results_text.insert(tk.END, file_header)
                
                for match in result['matches'][:5]:  # Limit to first 5 matches per file
                    match_text = f"\n   Line {match['line_num']}:\n"
                    match_text += f"   {match['line'][:100]}...\n" if len(match['line']) > 100 else f"   {match['line']}\n"
                    self.results_text.insert(tk.END, match_text)
                
                if len(result['matches']) > 5:
                    self.results_text.insert(tk.END, f"\n   ... and {len(result['matches']) - 5} more matches\n")
        
        self.status_var.set(f"Found {total_matches} matches in {len(self.results)} files")

def main():
    """Main function."""
    root = tk.Tk()
    app = DeepDiveRecall(root)
    root.mainloop()

if __name__ == "__main__":
    main()
