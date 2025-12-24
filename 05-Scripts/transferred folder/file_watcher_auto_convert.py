#!/usr/bin/env python3
"""
TRAJANUS FILE WATCHER - Automatic Conversion
Monitors folders for new .md, .docx, .xlsx, .pptx files
Automatically converts to Google Docs format when detected
Run in background during work sessions
"""

import os
import time
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
WATCH_ROOT = r"G:\My Drive\00 - Trajanus USA"
COMMAND_CENTER = r"G:\My Drive\00 - Trajanus USA\00-Command-Center"

# Files to convert
CONVERTIBLE_EXTENSIONS = {'.md', '.docx', '.xlsx', '.pptx'}

# Ignore these folders
IGNORE_FOLDERS = {'Credentials', 'node_modules', '.git', '__pycache__'}

class ConversionHandler(FileSystemEventHandler):
    """Handles file system events and triggers conversions"""
    
    def __init__(self):
        self.pending_conversions = set()
        self.last_conversion = {}
        
    def on_created(self, event):
        """Called when a file is created"""
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        
        # Check if file should be converted
        if file_path.suffix.lower() in CONVERTIBLE_EXTENSIONS:
            # Ignore if in excluded folder
            if any(folder in file_path.parts for folder in IGNORE_FOLDERS):
                return
            
            # Add to pending conversions
            self.pending_conversions.add(file_path)
            print(f"📝 New file detected: {file_path.name}")
    
    def on_modified(self, event):
        """Called when a file is modified"""
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        
        # Check if file should be converted
        if file_path.suffix.lower() in CONVERTIBLE_EXTENSIONS:
            # Ignore if in excluded folder
            if any(folder in file_path.parts for folder in IGNORE_FOLDERS):
                return
            
            # Check if enough time has passed since last conversion
            now = time.time()
            last_time = self.last_conversion.get(str(file_path), 0)
            
            # Wait 30 seconds after last modification before converting
            if now - last_time > 30:
                self.pending_conversions.add(file_path)
                print(f"✏️  File modified: {file_path.name}")
    
    def on_moved(self, event):
        """Called when a file is moved (like browser downloads)"""
        if event.is_directory:
            return
            
        dest_path = Path(event.dest_path)
        
        # Check if destination file should be converted
        if dest_path.suffix.lower() in CONVERTIBLE_EXTENSIONS:
            # Ignore if in excluded folder
            if any(folder in dest_path.parts for folder in IGNORE_FOLDERS):
                return
            
            # Add to pending conversions
            self.pending_conversions.add(dest_path)
            print(f"📥 File moved/downloaded: {dest_path.name}")
    
    def process_conversions(self):
        """Process all pending conversions"""
        if not self.pending_conversions:
            return
        
        print(f"\n🔄 Processing {len(self.pending_conversions)} file(s)...")
        
        for file_path in list(self.pending_conversions):
            try:
                # Wait for file to be fully written
                time.sleep(2)
                
                if not file_path.exists():
                    print(f"⚠️  File no longer exists: {file_path.name}")
                    self.pending_conversions.remove(file_path)
                    continue
                
                # Determine conversion script
                suffix = file_path.suffix.lower()
                
                if suffix == '.md':
                    script = 'convert_single_md.py'
                    args = [str(file_path)]
                elif suffix == '.docx':
                    script = 'convert_to_google_docs.py'
                    args = [str(file_path)]
                elif suffix in {'.xlsx', '.pptx'}:
                    script = 'convert_office_to_google.py'
                    args = [str(file_path)]
                else:
                    self.pending_conversions.remove(file_path)
                    continue
                
                # Run conversion
                print(f"Converting: {file_path.name}")
                
                result = subprocess.run(
                    ['python', script] + args,
                    cwd=COMMAND_CENTER,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print(f"✅ Converted: {file_path.name}")
                    self.last_conversion[str(file_path)] = time.time()
                else:
                    print(f"❌ Failed: {file_path.name}")
                    print(f"   Error: {result.stderr[:100]}")
                
                self.pending_conversions.remove(file_path)
                
            except Exception as e:
                print(f"❌ Error converting {file_path.name}: {e}")
                self.pending_conversions.remove(file_path)
        
        print("✅ Conversion batch complete\n")


def main():
    """Main file watcher loop"""
    print("=" * 60)
    print("TRAJANUS AUTOMATIC FILE CONVERSION WATCHER")
    print("=" * 60)
    print(f"Monitoring: {WATCH_ROOT}")
    print(f"Converting: .md, .docx, .xlsx, .pptx → Google Docs format")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    # Create event handler and observer
    event_handler = ConversionHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_ROOT, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(10)  # Check every 10 seconds
            event_handler.process_conversions()
            
    except KeyboardInterrupt:
        print("\n\n⏹  Stopping file watcher...")
        observer.stop()
    
    observer.join()
    print("File watcher stopped.")


if __name__ == '__main__':
    # Check if watchdog is installed
    try:
        import watchdog
    except ImportError:
        print("ERROR: watchdog library not installed")
        print("Install with: pip install watchdog")
        exit(1)
    
    main()
