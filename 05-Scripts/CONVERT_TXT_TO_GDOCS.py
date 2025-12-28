#!/usr/bin/env python3
"""
TRAJANUS TXT TO GOOGLE DOCS CONVERTER
Convert text files to Google Docs format
Standard Tool UI Template
"""

import os
import sys
import pickle
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class TrajanusTxtConverterGUI:
    def __init__(self, initial_path=None):
        self.root = tk.Tk()
        self.root.title("Trajanus - TXT to GDocs Converter")
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
        self.service = None
        self.converting = False
        self.initial_path = initial_path

        # Results storage
        self.converted_files = []
        self.skipped_files = []
        self.error_files = []

        # Current frame reference
        self.current_frame = None

        self.setup_header()
        self.connect_drive()

        if self.initial_path:
            self.root.after(500, lambda: self.process_initial_path())
        else:
            self.show_welcome_screen()

    def setup_header(self):
        """Create persistent header"""
        self.header = tk.Frame(self.root, bg=self.colors['accent'], height=60)
        self.header.pack(fill='x')
        self.header.pack_propagate(False)

        title = tk.Label(self.header,
            text="TRAJANUS TXT CONVERTER",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['accent'],
            fg='#1a1a1a')
        title.pack(pady=15)

        # Connection status bar
        self.status_bar = tk.Frame(self.root, bg=self.colors['border'], height=30)
        self.status_bar.pack(fill='x')
        self.status_bar.pack_propagate(False)

        self.connection_label = tk.Label(self.status_bar,
            text="Connecting to Google Drive...",
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
            text="Welcome to the TXT Converter",
            font=('Segoe UI', 16),
            bg=self.colors['bg'],
            fg=self.colors['text'])
        welcome.pack(pady=(0, 20))

        # Info card
        info_frame = tk.Frame(self.current_frame, bg=self.colors['card'], padx=25, pady=20)
        info_frame.pack(fill='x', pady=(0, 25))

        info_text = """This tool converts plain text (.txt) files to Google Docs format.

HOW IT WORKS:
  1. Select single file, multiple files, or entire folder
  2. Files are uploaded to your Google Drive
  3. Converted to native Google Docs format
  4. Original .txt files remain unchanged

NOTE: Files already converted will be skipped to prevent duplicates.
      The tool checks for existing .gdoc files before converting."""

        tk.Label(info_frame,
            text=info_text,
            font=('Segoe UI', 11),
            bg=self.colors['card'],
            fg=self.colors['text_dim'],
            justify='left').pack(anchor='w')

        # Mode selection title
        tk.Label(self.current_frame,
            text="SELECT CONVERSION MODE",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text_dim']).pack(pady=(10, 15))

        # Mode buttons container
        btn_container = tk.Frame(self.current_frame, bg=self.colors['bg'])
        btn_container.pack(fill='x')

        # Create mode cards
        self.create_mode_card(btn_container,
            "SINGLE FILE",
            "Select one .txt file to convert",
            "Best for quick single conversions",
            self.select_single_file,
            side='left')

        self.create_mode_card(btn_container,
            "BATCH FOLDER",
            "Convert all .txt files in a folder",
            "Converts entire directory at once",
            self.select_folder,
            side='left')

        self.create_mode_card(btn_container,
            "MULTI-SELECT",
            "Pick multiple specific files",
            "Choose exactly which files to convert",
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
        """Display conversion progress screen"""
        self.clear_content()

        self.current_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.current_frame.pack(fill='both', expand=True, padx=40, pady=30)

        tk.Label(self.current_frame,
            text="Converting Files...",
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

        self.live_converted = self.create_live_stat(stats_frame, "Converted:", "0", self.colors['success'])
        self.live_skipped = self.create_live_stat(stats_frame, "Skipped:", "0", self.colors['warning'])
        self.live_errors = self.create_live_stat(stats_frame, "Errors:", "0", self.colors['error'])

        self.current_file_label = tk.Label(self.current_frame,
            text="",
            font=('Consolas', 9),
            bg=self.colors['bg'],
            fg=self.colors['text_dim'])
        self.current_file_label.pack(pady=(10, 0))

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

    def show_completion_screen(self):
        """Display completion screen with results"""
        self.clear_content()

        self.current_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.current_frame.pack(fill='both', expand=True, padx=40, pady=30)

        header_frame = tk.Frame(self.current_frame, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, 20))

        tk.Label(header_frame,
            text="CONVERSION COMPLETE",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['success']).pack(side='left')

        summary_card = tk.Frame(self.current_frame, bg=self.colors['card'], padx=25, pady=20)
        summary_card.pack(fill='x', pady=(0, 20))

        stats_frame = tk.Frame(summary_card, bg=self.colors['card'])
        stats_frame.pack(fill='x')

        self.create_result_stat(stats_frame, "Converted", len(self.converted_files), self.colors['success'])
        self.create_result_stat(stats_frame, "Skipped", len(self.skipped_files), self.colors['warning'])
        self.create_result_stat(stats_frame, "Errors", len(self.error_files), self.colors['error'])

        if self.converted_files:
            self.create_file_list("CONVERTED FILES", self.converted_files, self.colors['success'])

        if self.skipped_files:
            self.create_file_list("SKIPPED FILES (already converted)", self.skipped_files, self.colors['warning'])

        if self.error_files:
            self.create_file_list("FAILED FILES", self.error_files, self.colors['error'])

        btn_frame = tk.Frame(self.current_frame, bg=self.colors['bg'])
        btn_frame.pack(fill='x', pady=(20, 0))

        convert_more_btn = tk.Button(btn_frame,
            text="Convert More Files",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['accent'],
            fg='#1a1a1a',
            activebackground=self.colors['hover'],
            activeforeground='#1a1a1a',
            padx=25, pady=10,
            cursor='hand2',
            relief='flat',
            command=self.show_welcome_screen)
        convert_more_btn.pack(side='left')

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
        """Select a single text file to convert"""
        if not self.service:
            messagebox.showerror("Error", "Not connected to Google Drive.\nPlease wait for connection.")
            return

        self.root.attributes('-topmost', False)
        self.root.update()

        file = filedialog.askopenfilename(
            title="Select Text File",
            initialdir="G:/My Drive/00 - Trajanus USA",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            parent=self.root)

        self.root.lift()
        self.root.focus_force()

        if file:
            self.convert_files([Path(file)])

    def select_folder(self):
        """Select a folder to convert all .txt files"""
        if not self.service:
            messagebox.showerror("Error", "Not connected to Google Drive.\nPlease wait for connection.")
            return

        self.root.attributes('-topmost', False)
        self.root.update()

        folder = filedialog.askdirectory(
            title="Select Folder with Text Files",
            initialdir="G:/My Drive/00 - Trajanus USA",
            parent=self.root)

        self.root.lift()
        self.root.focus_force()

        if folder:
            txt_files = list(Path(folder).glob('*.txt'))
            if txt_files:
                self.convert_files(txt_files)
            else:
                messagebox.showinfo("No Files", f"No .txt files found in:\n{folder}")

    def select_multiple_files(self):
        """Select multiple text files to convert"""
        if not self.service:
            messagebox.showerror("Error", "Not connected to Google Drive.\nPlease wait for connection.")
            return

        self.root.attributes('-topmost', False)
        self.root.update()

        files = filedialog.askopenfilenames(
            title="Select Text Files (hold Ctrl to select multiple)",
            initialdir="G:/My Drive/00 - Trajanus USA",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
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
            if path.suffix.lower() == '.txt':
                self.convert_files([path])
            else:
                messagebox.showerror("Error", "Not a text file")
                self.show_welcome_screen()
        else:
            txt_files = list(path.glob('*.txt'))
            if txt_files:
                self.convert_files(txt_files)
            else:
                messagebox.showinfo("No Files", "No .txt files found")
                self.show_welcome_screen()

    # ==================== CONVERSION ====================

    def convert_files(self, txt_files):
        """Convert a list of text files"""
        if not txt_files:
            return

        self.converted_files = []
        self.skipped_files = []
        self.error_files = []

        self.show_progress_screen(len(txt_files))
        self.converting = True

        def do_convert():
            source_folder = txt_files[0].parent

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

            total = len(txt_files)

            for i, txt_file in enumerate(sorted(txt_files)):
                percent = ((i + 1) / total) * 100
                self.root.after(0, lambda p=percent: self.progress_bar.configure(value=p))
                self.root.after(0, lambda i=i, t=total: self.progress_text.config(
                    text=f"{i + 1} of {t} files"))
                self.root.after(0, lambda f=txt_file.name: self.current_file_label.config(
                    text=f"Processing: {f}"))

                gdoc_path = str(txt_file)[:-4] + '.gdoc'
                url_path = str(txt_file)[:-4] + '.url'

                if os.path.exists(gdoc_path) or os.path.exists(url_path):
                    self.skipped_files.append(txt_file.name)
                    self.root.after(0, lambda: self.live_skipped.config(
                        text=str(len(self.skipped_files))))
                    continue

                result = self.convert_txt_to_gdoc(txt_file, folder_id)

                if result:
                    self.converted_files.append(txt_file.name)
                    self.root.after(0, lambda: self.live_converted.config(
                        text=str(len(self.converted_files))))
                else:
                    self.error_files.append(txt_file.name)
                    self.root.after(0, lambda: self.live_errors.config(
                        text=str(len(self.error_files))))

            self.converting = False
            self.root.after(0, self.show_completion_screen)

        threading.Thread(target=do_convert, daemon=True).start()

    def convert_txt_to_gdoc(self, txt_file, folder_id):
        """Upload and convert a single text file"""
        file_metadata = {
            'name': txt_file.stem,
            'mimeType': 'application/vnd.google-apps.document',
            'parents': [folder_id]
        }

        media = MediaFileUpload(str(txt_file), mimetype='text/plain', resumable=True)

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

    app = TrajanusTxtConverterGUI(initial_path)
    app.run()


if __name__ == '__main__':
    main()
