#!/usr/bin/env python3
"""
RESEARCH DOCUMENT PARSER v3.0 (13-Knowledge-Base)
Parses research documents, categorizes them hierarchically, converts to Google Docs,
and moves to appropriate 13-Knowledge-Base subcategories.

Author: Claude Code
Date: 2025-12-18
"""

import os
import pickle
import re
from pathlib import Path
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

# ============================================================================
# CONFIGURATION
# ============================================================================

RESEARCH_FOLDER = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/agents/Research")
CREDENTIALS_PATH = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/Credentials/token.pickle")
LOG_FOLDER = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/logs")

# Base folder: 13-Knowledge-Base
KB_FOLDER_ID = "1E7kK8ZIZ9-9xZ4HtvbuVbY_iX3DKmEYM"

# ============================================================================
# HIERARCHICAL FOLDER STRUCTURE (13-Knowledge-Base)
# ============================================================================

FOLDER_HIERARCHY = {
    "10-AI-Development": {
        "id": "1aCbSlrRoP6kV_3su3VQ1TYyq-l8mMe4J",
        "keywords": ["claude", "ai", "machine learning", "chatgpt", "automation", "llm", "agent", "anthropic", "openai", "embedding", "vector", "neural", "gpt", "mcp", "langchain", "rag"],
        "subcategories": {
            "Agents": {
                "id": "1kgLBJb9qiYgSwvsHJMPbk28ilcD_kI9l",
                "keywords": ["agent", "subagent", "multi-agent", "agentic", "harness"],
                "subcategories": {
                    "Claude-Agent-SDK": {"id": "1b1JCfWvqyFLkDKlKiW3WdQU6wJypq9Kv", "keywords": ["agent sdk", "claude sdk", "anthropic sdk"]},
                    "Multi-Agent-Systems": {"id": "1f1cFMw-jZU8PDfZNchOzmx8RjHk7XUR3", "keywords": ["multi-agent", "subagent", "collaboration", "orchestrat"]},
                    "Agent-Patterns": {"id": "1qZ4tdNnFgRtkOZrGc0uk4Pl8rGzJQicQ", "keywords": ["harness", "context window", "state management", "context engineer"]}
                }
            },
            "RAG-Systems": {
                "id": "1eKOozE3dVn1H8DoCN-A1RJKK8n97cdIv",
                "keywords": ["rag", "retrieval augmented", "chunking", "rerank", "hybrid search"],
                "subcategories": {
                    "Chunking-Strategies": {"id": "1g8cWhnfjtY7bX56K1--kkIhJQoHJ6jhS", "keywords": ["chunk", "chunking", "split", "semantic chunk"]},
                    "Retrieval-Optimization": {"id": "1T4sEzwkx6WC_jNEx5YayhX10GUoWn3wP", "keywords": ["rerank", "hybrid search", "retrieval", "bm25"]},
                    "RAG-Monitoring": {"id": "1PAv3Dy2d90rWOGR97q2WYFb55Y3h1qv5", "keywords": ["rag monitor", "rag eval", "rag metric", "rag accuracy"]}
                }
            },
            "Vector-Databases": {
                "id": "1TuwZ-058WeiMxF56G6T2UtZRJ-9nNoVc",
                "keywords": ["pgvector", "vector similarity", "hnsw", "ivfflat", "vector index", "vector search", "pinecone", "chroma"],
                "subcategories": {
                    "Pgvector": {"id": "1s1h_rMK9Ia5efWcHzzx8T3cNMPjGT6D5", "keywords": ["pgvector", "pg vector", "postgresql vector"]},
                    "Embeddings": {"id": "1fip5OsfBj5pDVH31VjgYvcNsl11h0gJL", "keywords": ["embedding", "text-embedding", "openai embed", "embed model"]}
                }
            },
            "MCP-Protocol": {
                "id": "1GVDi6QpZJBrvmnbVtbV7iFHGd51aHkSe",
                "keywords": ["mcp", "model context protocol"],
                "subcategories": {
                    "MCP-Servers": {"id": "1TQbvGaKtnIQTAra9l0vfetFWBv3iIKcy", "keywords": ["mcp server", "build mcp", "building mcp", "stdio", "sse server"]},
                    "MCP-Integration": {"id": "16En7jTTiS51Po5DNCeLhlVmAYQ0ZnGhH", "keywords": ["mcp integration", "mcp sse", "mcp debug", "mcp vs code"]},
                    "MCP-Best-Practices": {"id": "1JuFDyC8f7iYT3AIIzEN6v9qbJGSI9I9P", "keywords": ["mcp best practice", "mcp schema", "mcp production"]}
                }
            },
            "Claude-Specific": {
                "id": "1j1SQiBYaGzPlpleXZ3_95MrSCQv-SjAf",
                "keywords": ["claude", "anthropic", "claude code", "opus", "sonnet", "haiku"],
                "subcategories": {
                    "Claude-Updates": {"id": "1GyPA31gYZpocOla3Gr6jBzt91ooBtm3V", "keywords": ["claude update", "new feature", "release", "announcement"]},
                    "Claude-API": {"id": "1LaER9a9IVAS3dZAEcbYV3IXfVMPrxklx", "keywords": ["api", "claude api", "anthropic api", "sdk"]},
                    "Claude-Code-Tool": {"id": "1uVpyxFxr1BSjaldDog1uPKoB3z_paEWM", "keywords": ["claude code", "cli", "terminal", "command line"]}
                }
            },
            "Playwright-Testing": {
                "id": "1vvEFjJjRf3vPV-VpYYc2oLD32tHpoE78",
                "keywords": ["playwright"],
                "subcategories": {
                    "Screenshots": {"id": "1324J_fckom2Ws3OvytHAYKzQfz_jfcaE", "keywords": ["screenshot", "snapshot", "visual"]},
                    "Testing-Guides": {"id": "1G17R_pVwiy-psk42Q4v8ydCrKsBtXsvR", "keywords": ["test", "testing", "automation test"]}
                }
            },
            "Supabase-AI": {
                "id": "13IPEjT-5VEcNL5vM9e51Q3qOKGl1tbhB",
                "keywords": ["supabase", "supavisor", "rls", "row level security"],
                "subcategories": {
                    "Connection-Management": {"id": "1sdK6qrsv9kpB0YVLEgxz8j4C8I1zCxw1", "keywords": ["connection", "pooling", "supavisor"]},
                    "Row-Level-Security": {"id": "1Z6_Q7l4U4OdLsIqVsIV5y4gTWoP6cMRx", "keywords": ["rls", "row level", "security policies"]}
                }
            },
            "Google-Cloud-APIs": {
                "id": "1eoZtTVg3RJvNY026TnipL_tSaZtdKaa-",
                "keywords": ["google drive", "cloud storage", "google api", "resumable upload"],
                "subcategories": {
                    "Drive-Storage": {"id": "1jXSUywgnzMeS9-cQvE9B2m_8rzO4SytH", "keywords": ["drive api", "upload", "storage", "google drive"]}
                }
            },
            "Uncategorized": {"id": "19cxLHAf-lkjLujcb7HpaMEK1fawnWG0D", "keywords": [], "subcategories": {}}
        }
    },
    "11-Software-Tools": {
        "id": "1Us9tVnbsJSpXgEzZ3y68W_hkgIowWAn2",
        "keywords": ["electron", "javascript", "typescript", "node", "npm", "python", "library", "tool", "framework", "api"],
        "subcategories": {
            "Electron": {
                "id": "1H7Lfjneqv478z8mUBIkKq6gH6G5mfQ3M",
                "keywords": ["electron", "desktop app", "chromium", "ipc"],
                "subcategories": {
                    "IPC-Communication": {"id": "1PPdpRBOeMZjGPe-jeU8YDus1vcFjmv8L", "keywords": ["ipc", "ipcmain", "ipcrenderer", "preload"]},
                    "Python-Integration": {"id": "1XliY7ZYkvT2BK9znqRAlB21krOXrdwA1", "keywords": ["python electron", "spawn", "child process"]},
                    "Security-Architecture": {"id": "1jogfH2eGR_ysW0F5tFHwUeWQRJEWQMMx", "keywords": ["sandbox", "context isolation", "security"]}
                }
            },
            "Google-APIs": {
                "id": "18YsmQVwKIKpJJ--81e9wdjQQpnt7iDrG",
                "keywords": ["google", "drive api", "docs api", "sheets api"],
                "subcategories": {
                    "Drive-API": {"id": "1x33bUq2gZPblGSNuA_KAj_Mj9wNVjODH", "keywords": ["drive", "file", "folder", "upload"]},
                    "Docs-API": {"id": "1nRnNL-E00GcHcXNYxrOSm2hEV6lBhQJJ", "keywords": ["docs", "document", "google doc"]}
                }
            },
            "Python-Development": {
                "id": "1E5-NdqbSMCv1Clk31s_9EW-zPVQRLpDk",
                "keywords": ["python", "pip", "virtualenv", "async"],
                "subcategories": {
                    "Subprocess": {"id": "1LY0l0sWYmkQyTfegL6kkPFIDH_qCMcyV", "keywords": ["subprocess", "popen", "spawn", "shell"]},
                    "Security": {"id": "1_isNjE_2XyeTDfyhWEHwedHALanVTsh_", "keywords": ["security", "sanitize", "escape", "injection"]}
                }
            },
            "JavaScript-Libraries": {
                "id": "1kta2Yp_WzpzFdiP95TxxHOlC16QCNzRm",
                "keywords": ["javascript", "typescript", "npm", "node"],
                "subcategories": {
                    "File-Management": {"id": "1OAThF0V98lqoCWj1WNSaZN81JgIerk8Y", "keywords": ["file", "fs", "path", "glob"]},
                    "Frameworks": {"id": "1qYvZ99wVJH0uItQKUvUiFzovVHDDxF3X", "keywords": ["react", "vue", "express", "next"]}
                }
            },
            "Supabase-Tools": {"id": "1sD2WUO3bWoQwPfko6kC2IlX19uR_Neo5", "keywords": ["supabase client", "supabase js"], "subcategories": {}},
            "Uncategorized": {"id": "1Q27Byx5VfD62XDCIabnkxL-iBHXIfuN9", "keywords": [], "subcategories": {}}
        }
    },
    "12-Technical-Guides": {
        "id": "1KXvtF8m0fJree--dmnavM_xRS6Yg1YhN",
        "keywords": ["guide", "tutorial", "how to", "setup", "install", "configure", "documentation"],
        "subcategories": {
            "Setup-Installation": {"id": "1ZEbD_z0WU6cdiOg4XKmQsEPl7mRrNNFE", "keywords": ["setup", "install", "getting started"], "subcategories": {}},
            "Configuration": {"id": "11JkOX-MX51GukGqRpdkxzAzJeMtZ31Eo", "keywords": ["config", "settings", "environment"], "subcategories": {}},
            "Node-Documentation": {"id": "1asWuTBmhwq0pdcldn6ruUscwOG7appL8", "keywords": ["node", "npm", "package"], "subcategories": {}},
            "Python-Guides": {"id": "1Rtz9Q_vR7F5oVY1SbjEahBA4hY8f2ubf", "keywords": ["python", "pip", "virtualenv"], "subcategories": {}},
            "Documentation-Standards": {"id": "18zYKAKpC17WtqjC6WxtH1ro9DVFdPQDB", "keywords": ["documentation", "standard", "template"], "subcategories": {}},
            "Uncategorized": {"id": "1UKfI1NXxKdBluxP9XgDsBrgC9EsZaE0B", "keywords": [], "subcategories": {}}
        }
    },
    "13-QCM-Quality": {
        "id": "1R-Xq2G6OHmtRxpX_bcKC736VyV7GNN7r",
        "keywords": ["qcm", "quality", "inspection", "submittal", "testing", "compliance"],
        "subcategories": {
            "Submittal-Review": {"id": "1NMEJktULSq4YMbjQTID0NxUZfF4w8AK8", "keywords": ["submittal", "review"], "subcategories": {}},
            "Inspection-Procedures": {"id": "1bDkF-3LDdQgKn8Fpu7Afi3DMZKn6Fn9C", "keywords": ["inspection", "procedure"], "subcategories": {}},
            "Testing-Requirements": {"id": "1-otfwkHhq8kjgVAQfEEpV97SgYgeBwSx", "keywords": ["test", "requirement"], "subcategories": {}},
            "Documentation": {"id": "1xjM8HsbA4ItEwWw2vZ7RpxcjkoV1MD_w", "keywords": ["documentation", "standard"], "subcategories": {}},
            "Uncategorized": {"id": "1Uy9tJ0jurUOnKC5C7ZHp_oYcM_dprzQ0", "keywords": [], "subcategories": {}}
        }
    }
}

# ============================================================================
# GOOGLE DRIVE SERVICE
# ============================================================================

def get_service():
    """Get authenticated Google Drive service."""
    with open(CREDENTIALS_PATH, 'rb') as token:
        creds = pickle.load(token)
    return build('drive', 'v3', credentials=creds)

# ============================================================================
# CATEGORIZATION
# ============================================================================

def categorize_hierarchical(text):
    """
    Determine the best hierarchical path for a document.
    Returns: (folder_id, path_string)
    """
    text_lower = text.lower()
    best_score = 0
    best_path = "10-AI-Development/Uncategorized"
    best_folder_id = FOLDER_HIERARCHY["10-AI-Development"]["subcategories"]["Uncategorized"]["id"]

    for main_cat, main_data in FOLDER_HIERARCHY.items():
        main_keywords = main_data.get("keywords", [])
        main_score = sum(2 for kw in main_keywords if kw.lower() in text_lower)

        for sub_cat, sub_data in main_data.get("subcategories", {}).items():
            sub_keywords = sub_data.get("keywords", [])
            sub_score = main_score + sum(3 for kw in sub_keywords if kw.lower() in text_lower)

            # Check sub-subcategories
            for subsub_cat, subsub_data in sub_data.get("subcategories", {}).items():
                subsub_keywords = subsub_data.get("keywords", [])
                subsub_score = sub_score + sum(5 for kw in subsub_keywords if kw.lower() in text_lower)

                if subsub_score > best_score:
                    best_score = subsub_score
                    best_path = f"{main_cat}/{sub_cat}/{subsub_cat}"
                    best_folder_id = subsub_data["id"]

            # Maybe just sub-category is best
            if sub_score > best_score and sub_cat != "Uncategorized":
                best_score = sub_score
                best_path = f"{main_cat}/{sub_cat}"
                best_folder_id = sub_data["id"]

    return best_folder_id, best_path

# ============================================================================
# DOCUMENT PROCESSING
# ============================================================================

def convert_md_to_gdoc(service, md_file, folder_id):
    """Convert markdown file to Google Doc and place in specified folder."""
    # Read markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Create filename from markdown file
    filename = md_file.stem

    # Check for existing document with same name
    query = f"name = '{filename}' and '{folder_id}' in parents and mimeType = 'application/vnd.google-apps.document' and trashed = false"
    results = service.files().list(q=query, fields='files(id, name)').execute()
    if results.get('files'):
        return None, "DUPLICATE"

    # Create Google Doc
    file_metadata = {
        'name': filename,
        'mimeType': 'application/vnd.google-apps.document',
        'parents': [folder_id]
    }

    # Upload the markdown as text
    media = MediaFileUpload(str(md_file), mimetype='text/plain', resumable=True)
    doc = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return doc.get('id'), "CREATED"

# ============================================================================
# MAIN
# ============================================================================

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOG_FOLDER / f"parser_{timestamp}.log"

    print("=" * 60)
    print("RESEARCH DOCUMENT PARSER v3.0 (13-Knowledge-Base)")
    print("=" * 60)

    service = get_service()

    # Get all markdown files
    md_files = list(RESEARCH_FOLDER.glob("*.md"))
    print(f"\nFound {len(md_files)} markdown files in Research folder")

    if not md_files:
        print("No files to process.")
        return

    log_entries = []
    created = 0
    duplicates = 0
    errors = 0

    for i, md_file in enumerate(md_files):
        try:
            # Read content for categorization
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Categorize
            text = f"{md_file.stem} {content[:2000]}"
            folder_id, path = categorize_hierarchical(text)

            # Convert and upload
            doc_id, status = convert_md_to_gdoc(service, md_file, folder_id)

            if status == "CREATED":
                created += 1
                log_entries.append(f"CREATED: {md_file.stem} -> {path}")
            elif status == "DUPLICATE":
                duplicates += 1
                log_entries.append(f"DUPLICATE: {md_file.stem}")

            if (i + 1) % 10 == 0:
                print(f"  Progress: {i + 1}/{len(md_files)}")

        except Exception as e:
            errors += 1
            log_entries.append(f"ERROR: {md_file.stem} - {str(e)}")

    # Save log
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"Parser Log - {timestamp}\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Files processed: {len(md_files)}\n")
        f.write(f"Created: {created}\n")
        f.write(f"Duplicates: {duplicates}\n")
        f.write(f"Errors: {errors}\n\n")
        for entry in log_entries:
            f.write(entry + "\n")

    print("\n" + "=" * 60)
    print("PARSING COMPLETE")
    print("=" * 60)
    print(f"Created: {created}")
    print(f"Duplicates skipped: {duplicates}")
    print(f"Errors: {errors}")
    print(f"\nLog saved to: {log_file}")

if __name__ == "__main__":
    main()
