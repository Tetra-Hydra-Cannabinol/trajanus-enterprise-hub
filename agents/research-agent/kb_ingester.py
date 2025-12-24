"""
Knowledge Base Ingester Module
Extracts text from documents, chunks, embeds, and stores in Supabase
"""

import os
from datetime import datetime
from PyPDF2 import PdfReader
from docx import Document
from openai import OpenAI
from supabase import create_client
import config


def extract_text_pdf(filepath: str) -> str:
    """Extract text from PDF file"""
    try:
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF {filepath}: {e}")
        return ""


def extract_text_docx(filepath: str) -> str:
    """Extract text from DOCX file"""
    try:
        doc = Document(filepath)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        print(f"Error reading DOCX {filepath}: {e}")
        return ""


def extract_text(filepath: str) -> str:
    """Extract text from PDF or DOCX"""
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        return extract_text_pdf(filepath)
    elif ext in [".docx", ".doc"]:
        return extract_text_docx(filepath)
    else:
        print(f"Unsupported file type: {ext}")
        return ""


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> list:
    """
    Split text into chunks of approximately chunk_size tokens.
    Uses simple word-based splitting (rough approximation).

    Args:
        text: Full text to chunk
        chunk_size: Target chunk size in tokens (~4 chars per token)
        overlap: Overlap between chunks in tokens

    Returns:
        List of text chunks
    """
    if not text:
        return []

    # Rough approximation: 1 token ~ 4 characters
    char_chunk_size = chunk_size * 4
    char_overlap = overlap * 4

    chunks = []
    start = 0

    while start < len(text):
        end = start + char_chunk_size

        # Try to break at sentence or paragraph boundary
        if end < len(text):
            # Look for paragraph break
            para_break = text.rfind("\n\n", start, end)
            if para_break > start + char_chunk_size // 2:
                end = para_break

            # Or sentence break
            elif (sentence_break := text.rfind(". ", start, end)) > start + char_chunk_size // 2:
                end = sentence_break + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - char_overlap

    return chunks


def generate_embedding(text: str, client: OpenAI) -> list:
    """Generate embedding using OpenAI text-embedding-3-small"""
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Embedding error: {e}")
        return None


def ingest_to_kb(file_paths: list) -> dict:
    """
    Ingest documents into Supabase knowledge base.

    Args:
        file_paths: List of file paths to process

    Returns:
        Dict with: files_processed, chunks_created, errors
    """
    stats = {
        "files_processed": 0,
        "chunks_created": 0,
        "errors": []
    }

    # Check config
    if not config.OPENAI_API_KEY:
        stats["errors"].append("OPENAI_API_KEY not set")
        return stats

    if not config.SUPABASE_URL or not config.SUPABASE_KEY:
        stats["errors"].append("SUPABASE_URL or SUPABASE_KEY not set")
        return stats

    # Initialize clients
    try:
        openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
        supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    except Exception as e:
        stats["errors"].append(f"Failed to initialize clients: {e}")
        return stats

    for filepath in file_paths:
        print(f"\nProcessing: {os.path.basename(filepath)}")

        # Extract text
        text = extract_text(filepath)
        if not text:
            stats["errors"].append(f"No text extracted from {filepath}")
            continue

        # Chunk text
        chunks = chunk_text(text)
        print(f"  Created {len(chunks)} chunks")

        # Process each chunk
        for i, chunk in enumerate(chunks):
            # Generate embedding
            embedding = generate_embedding(chunk, openai_client)
            if not embedding:
                stats["errors"].append(f"Embedding failed for chunk {i} of {filepath}")
                continue

            # Prepare record
            record = {
                "source": os.path.basename(filepath),
                "source_path": filepath,
                "content": chunk,
                "chunk_index": i,
                "embedding": embedding,
                "metadata": {
                    "ingested_at": datetime.now().isoformat(),
                    "chunk_count": len(chunks)
                }
            }

            # Insert into Supabase
            try:
                supabase.table("trajanus_kb").insert(record).execute()
                stats["chunks_created"] += 1
            except Exception as e:
                stats["errors"].append(f"DB insert error: {e}")

        stats["files_processed"] += 1

    return stats


if __name__ == "__main__":
    print("=" * 60)
    print("Knowledge Base Ingester Test")
    print("=" * 60)

    # Check configuration
    missing = config.validate_config()
    if missing:
        print(f"\nMissing config: {missing}")
        print("The ingester is ready but needs these environment variables.")
    else:
        print("\nAll configuration present.")
        print("To ingest files, call: ingest_to_kb(['path/to/file.pdf'])")

    # Test text chunking
    print("\nTesting chunker with sample text...")
    sample = "This is a test. " * 500
    chunks = chunk_text(sample, chunk_size=100)
    print(f"Sample text ({len(sample)} chars) -> {len(chunks)} chunks")
