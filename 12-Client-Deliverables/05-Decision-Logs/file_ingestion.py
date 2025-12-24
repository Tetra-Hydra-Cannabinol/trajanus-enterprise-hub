"""
TRAJANUS FILE INGESTION SYSTEM
Upload existing documents from Trajanus folders into knowledge base
"""

import os
import sys
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client, Client
from datetime import datetime
import json
import time

# Document processing libraries
try:
    from docx import Document
    import PyPDF2
except ImportError:
    print("Installing required libraries...")
    os.system("pip install python-docx PyPDF2 --break-system-packages")
    from docx import Document
    import PyPDF2

# ANSI colors
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

# Load environment
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Initialize clients
supabase: Client = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_SERVICE_KEY')
)

openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def print_header():
    """Print header"""
    print(f"\n{Colors.CYAN}{'='*70}")
    print(f"{'TRAJANUS FILE INGESTION SYSTEM':^70}")
    print(f"{'Upload Your Documents to Knowledge Base':^70}")
    print(f"{'='*70}{Colors.END}\n")

def print_progress(step: str, status: str = "working", detail: str = ""):
    """Print formatted progress"""
    symbols = {
        "working": "⏳",
        "success": "✅",
        "error": "❌",
        "info": "ℹ️"
    }
    colors = {
        "working": Colors.YELLOW,
        "success": Colors.GREEN,
        "error": Colors.RED,
        "info": Colors.CYAN
    }
    
    symbol = symbols.get(status, "ℹ️")
    color = colors.get(status, Colors.CYAN)
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    print(f"{color}[{timestamp}] {symbol} {step}{Colors.END}")
    if detail:
        print(f"    └─ {detail}")

def read_docx(filepath: Path) -> str:
    """Read Word document"""
    try:
        doc = Document(filepath)
        text = '\n'.join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print_progress(f"Error reading DOCX: {filepath.name}", "error", str(e))
        return ""

def read_pdf(filepath: Path) -> str:
    """Read PDF document"""
    try:
        text = ""
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print_progress(f"Error reading PDF: {filepath.name}", "error", str(e))
        return ""

def read_text_file(filepath: Path) -> str:
    """Read plain text or markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print_progress(f"Error reading text file: {filepath.name}", "error", str(e))
        return ""

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        
        if end < text_length:
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

def process_file(filepath: Path, source_category: str):
    """Process a single file"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'─'*70}")
    print(f"Processing: {filepath.name}")
    print(f"{'─'*70}{Colors.END}\n")
    
    # Read file based on extension
    ext = filepath.suffix.lower()
    
    if ext == '.docx':
        print_progress("Reading Word document", "working")
        content = read_docx(filepath)
    elif ext == '.pdf':
        print_progress("Reading PDF", "working")
        content = read_pdf(filepath)
    elif ext in ['.txt', '.md', '.gdoc']:
        print_progress("Reading text file", "working")
        content = read_text_file(filepath)
    else:
        print_progress(f"Unsupported file type: {ext}", "error")
        return
    
    if not content or len(content) < 50:
        print_progress("File empty or too short", "error")
        return
    
    print_progress(f"Read {len(content)} characters", "success")
    
    # Chunk the content
    print_progress("Chunking document", "working")
    chunks = chunk_text(content)
    print_progress(f"Created {len(chunks)} chunks", "success")
    
    # Process each chunk
    for i, chunk in enumerate(chunks, 1):
        print(f"\n  {Colors.YELLOW}Chunk {i}/{len(chunks)}{Colors.END}")
        
        # Generate embedding
        print_progress(f"  Generating embedding", "working")
        try:
            response = openai_client.embeddings.create(
                input=chunk,
                model="text-embedding-3-small"
            )
            embedding = response.data[0].embedding
            print_progress(f"  Embedding created ({len(embedding)} dims)", "success")
        except Exception as e:
            print_progress(f"  Embedding failed", "error", str(e))
            continue
        
        # Generate summary
        summary = ' '.join(chunk.split()[:20]) + '...'
        
        # Store in database
        print_progress(f"  Storing in database", "working")
        try:
            # Use relative path from Trajanus root
            relative_path = str(filepath).replace("G:\\My Drive\\00 - Trajanus USA\\", "")
            
            data = {
                "url": f"file:///{relative_path}",
                "chunk_number": i,
                "title": f"{filepath.stem} (Part {i})",
                "summary": summary,
                "content": chunk,
                "metadata": {
                    "source": source_category,
                    "filename": filepath.name,
                    "file_type": ext,
                    "total_chunks": len(chunks),
                    "processed_at": datetime.now().isoformat()
                },
                "embedding": embedding
            }
            
            result = supabase.table('knowledge_base').insert(data).execute()
            doc_id = result.data[0]['id']
            print_progress(f"  Stored successfully (ID: {doc_id})", "success")
            
            time.sleep(0.3)  # Rate limiting
            
        except Exception as e:
            print_progress(f"  Database insert failed", "error", str(e))
            continue
    
    print(f"\n{Colors.GREEN}✅ File processing complete!{Colors.END}\n")

def scan_folder(folder_path: Path, pattern: str = "*") -> List[Path]:
    """Scan folder for files matching pattern"""
    files = []
    supported_extensions = ['.docx', '.pdf', '.txt', '.md', '.gdoc']
    
    for ext in supported_extensions:
        files.extend(folder_path.glob(f"**/{pattern}{ext}"))
    
    return sorted(files)

def show_stats():
    """Show current KB stats"""
    try:
        result = supabase.table('knowledge_base').select('id,url,metadata').execute()
        data = result.data
        
        unique_urls = len(set(d['url'] for d in data))
        total_chunks = len(data)
        sources = set(d['metadata'].get('source', 'Unknown') for d in data if d.get('metadata'))
        
        print(f"\n{Colors.CYAN}{'='*70}")
        print(f"{'CURRENT KNOWLEDGE BASE STATS':^70}")
        print(f"{'='*70}{Colors.END}")
        print(f"  📚 Total Documents: {unique_urls}")
        print(f"  📄 Total Chunks: {total_chunks}")
        print(f"  🗂️  Knowledge Sources: {len(sources)}")
        print(f"{Colors.CYAN}{'='*70}{Colors.END}\n")
        
        return total_chunks
    except Exception as e:
        print_progress("Failed to get stats", "error", str(e))
        return 0

def main():
    """Main file ingestion interface"""
    print_header()
    
    initial_count = show_stats()
    
    base_path = Path("G:/My Drive/00 - Trajanus USA")
    
    print(f"{Colors.BOLD}What would you like to upload?{Colors.END}\n")
    print("1. EOS Files (08-EOS-Files)")
    print("2. Today's EOS Docs (Session-Summaries)")
    print("3. Code Repository (05-Code-Repository)")
    print("4. Protocols (06-Protocols-Preferences)")
    print("5. All Master Documents")
    print("6. Specific folder (manual path)")
    print("7. Single file")
    print("8. Exit\n")
    
    choice = input(f"{Colors.YELLOW}Enter choice (1-8): {Colors.END}")
    
    files_to_process = []
    source_category = "Unknown"
    
    if choice == "1":
        folder = base_path / "08-EOS-Files"
        files_to_process = scan_folder(folder)
        source_category = "Session Documentation"
        
    elif choice == "2":
        folder = Path("G:/My Drive/00 - Trajanus USA/Session-Summaries")
        files_to_process = scan_folder(folder)
        source_category = "Session Documentation"
        
    elif choice == "3":
        folder = base_path / "05-Code-Repository"
        files_to_process = scan_folder(folder)
        source_category = "Code Repository"
        
    elif choice == "4":
        folder = base_path / "06-Protocols-Preferences"
        files_to_process = scan_folder(folder)
        source_category = "Protocols"
        
    elif choice == "5":
        # Scan multiple folders
        folders = [
            ("03-Project-History", "Session History"),
            ("04-Technical-Decisions", "Technical Decisions"),
            ("05-Code-Repository", "Code Repository"),
            ("06-Protocols-Preferences", "Protocols"),
        ]
        
        all_files = []
        for folder_name, category in folders:
            folder = base_path / folder_name
            if folder.exists():
                files = scan_folder(folder)
                all_files.extend([(f, category) for f in files])
        
        # Process all with their categories
        print(f"\n{Colors.CYAN}Found {len(all_files)} files to process{Colors.END}\n")
        
        if len(all_files) > 20:
            confirm = input(f"{Colors.YELLOW}Process {len(all_files)} files? This may take a while. (y/n): {Colors.END}")
            if confirm.lower() != 'y':
                return
        
        for filepath, category in all_files:
            process_file(filepath, category)
        
        # Show final stats
        final_count = show_stats()
        added = final_count - initial_count
        print(f"{Colors.GREEN}{Colors.BOLD}📊 Added {added} new chunks!{Colors.END}\n")
        return
        
    elif choice == "6":
        folder_path = input(f"{Colors.YELLOW}Enter folder path: {Colors.END}")
        folder = Path(folder_path)
        if not folder.exists():
            print_progress("Folder not found", "error")
            return
        files_to_process = scan_folder(folder)
        source_category = input(f"{Colors.YELLOW}Source category: {Colors.END}")
        
    elif choice == "7":
        file_path = input(f"{Colors.YELLOW}Enter file path: {Colors.END}")
        filepath = Path(file_path)
        if not filepath.exists():
            print_progress("File not found", "error")
            return
        files_to_process = [filepath]
        source_category = input(f"{Colors.YELLOW}Source category: {Colors.END}")
        
    elif choice == "8":
        print(f"\n{Colors.GREEN}Exiting ingestion system.{Colors.END}\n")
        return
    
    # Process files
    if not files_to_process:
        print_progress("No files found", "error")
        return
    
    print(f"\n{Colors.CYAN}Found {len(files_to_process)} files to process{Colors.END}\n")
    
    if len(files_to_process) > 20:
        confirm = input(f"{Colors.YELLOW}Process {len(files_to_process)} files? This may take a while. (y/n): {Colors.END}")
        if confirm.lower() != 'y':
            return
    
    for filepath in files_to_process:
        process_file(filepath, source_category)
    
    # Show final stats
    final_count = show_stats()
    added = final_count - initial_count
    
    print(f"{Colors.GREEN}{Colors.BOLD}📊 Added {added} new chunks to knowledge base!{Colors.END}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Ingestion interrupted. Exiting...{Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.END}\n")
