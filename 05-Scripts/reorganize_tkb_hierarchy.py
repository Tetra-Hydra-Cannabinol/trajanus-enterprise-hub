#!/usr/bin/env python3
"""
TKB HIERARCHICAL REORGANIZATION v1.0
Reorganizes flat TKB folders into hierarchical subcategories.

Author: Claude Code
Date: 2025-12-18
"""

import pickle
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# ============================================================================
# CONFIGURATION
# ============================================================================

CREDENTIALS_PATH = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/Credentials/token.pickle")
OUTPUT_FOLDER = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/outputs")
LOG_FOLDER = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/logs")

# TKB Base Folder ID
TKB_BASE_FOLDER_ID = "1CRB5Abd4bBb7Y0wp7BKuhgmuDH0WwH8P"

# Current Category Folder IDs
CATEGORY_FOLDERS = {
    "AI-Development": "1VVeotAPnechdDPfLnDTiOZqKA5ZEQDRM",
    "Software-Tools": "1xMWr71AGbZOfnOjAy8IoVOt75Kf_KMAx",
    "Technical-Guides": "1guwUKpc4vUnsuZ0pibalGV0jzBnYZO1n",
    "QCM-Quality": "1ehvTr0P1xQzpKmqOVyiIE-FHR8B66Zpv",
    "Building-Codes": "1h-sOv04VI6p0KxtFJlY_jL_5kDDct_kw",
    "Session-Summaries": "1BF_a2sVEojNIZ6p38xjRx8xSrsvgB8zb",
    "Construction-Management": "1zT6_-lU1sG6h78FuVq8dqZ0JANWUG9kl",
    "Business-Strategy": "1PI_OK7M70LxDdeG2J18nyGVaTmmqdZQx",
    "General-Reference": "1XiFqVP7c2l9JxE-CSi_4Nc09hrInaEWn",
}

# ============================================================================
# HIERARCHICAL TAXONOMY (Based on document analysis)
# ============================================================================

TAXONOMY = {
    "AI-Development": {
        "Vector-Databases": {
            "keywords": ["pgvector", "vector similarity", "hnsw", "ivfflat", "vector index", "vector search", "alloydb"],
            "subcategories": {
                "Pgvector": ["pgvector", "pg vector"],
                "Embeddings": ["embedding", "text-embedding", "openai embed"]
            }
        },
        "RAG-Systems": {
            "keywords": ["rag", "retrieval augmented", "chunking", "rerank", "hybrid search"],
            "subcategories": {
                "Chunking-Strategies": ["chunk", "chunking"],
                "Retrieval-Optimization": ["rerank", "hybrid search", "retrieval"],
                "RAG-Monitoring": ["rag monitor", "rag eval", "rag metric", "rag accuracy"]
            }
        },
        "MCP-Protocol": {
            "keywords": ["mcp", "model context protocol"],
            "subcategories": {
                "MCP-Servers": ["mcp server", "build mcp", "building mcp"],
                "MCP-Integration": ["mcp integration", "mcp sse", "mcp debug", "mcp vs code"],
                "MCP-Best-Practices": ["mcp best practice", "mcp schema", "mcp production", "mcp optimize"]
            }
        },
        "Agents": {
            "keywords": ["agent", "subagent", "multi-agent", "agentic"],
            "subcategories": {
                "Claude-Agent-SDK": ["agent sdk", "claude sdk", "anthropic sdk", "claude docs"],
                "Multi-Agent-Systems": ["multi-agent", "subagent", "collaboration"],
                "Agent-Patterns": ["harness", "context window", "state management", "context engineer"]
            }
        },
        "Playwright-Testing": {
            "keywords": ["playwright"],
            "subcategories": {
                "Screenshots": ["screenshot", "snapshot"],
                "Testing-Guides": ["playwright test", "playwright form", "playwright best practice", "playwright guide"]
            }
        },
        "Google-Cloud-APIs": {
            "keywords": ["google drive", "cloud storage", "google api", "resumable upload"],
            "subcategories": {
                "Drive-Storage": ["drive api", "upload", "storage"]
            }
        },
        "Supabase": {
            "keywords": ["supabase", "supavisor", "rls", "row level security"],
            "subcategories": {
                "Connection-Management": ["connection", "pooling", "supavisor"],
                "Row-Level-Security": ["rls", "row level", "security policies"]
            }
        }
    },
    "Software-Tools": {
        "Electron": {
            "keywords": ["electron"],
            "subcategories": {
                "IPC-Communication": ["ipc", "preload", "inter-process"],
                "Python-Integration": ["electron python", "python electron"],
                "Security-Architecture": ["electron security", "penetration", "electron architecture"]
            }
        },
        "Google-APIs": {
            "keywords": ["google docs api", "drive api", "google api quota", "batch request"],
            "subcategories": {
                "Drive-API": ["drive api", "drive quota", "drive limit", "drive batch"],
                "Docs-API": ["docs api", "google docs api"]
            }
        },
        "Python-Development": {
            "keywords": ["subprocess", "python security", "command injection"],
            "subcategories": {
                "Subprocess": ["subprocess"],
                "Security": ["injection", "secure python", "pep 787"]
            }
        },
        "JavaScript-Libraries": {
            "keywords": ["javascript library", "js framework", "file browser js"],
            "subcategories": {
                "File-Management": ["file browser", "file manager"],
                "Frameworks": ["framework", "library"]
            }
        },
        "Supabase-Tools": {
            "keywords": ["supabase connection", "supabase scaling", "fastapi supabase"],
            "subcategories": {}
        }
    },
    "Technical-Guides": {
        "MCP-Setup": {
            "keywords": ["mcp setup", "mcp install", "mcp server guide"],
            "subcategories": {}
        },
        "Node-Documentation": {
            "keywords": ["node.js", "child process", "node error"],
            "subcategories": {}
        },
        "Documentation-Standards": {
            "keywords": ["documentation best", "style guide", "technical spec"],
            "subcategories": {}
        },
        "Playwright-Setup": {
            "keywords": ["playwright setup", "playwright install"],
            "subcategories": {}
        },
        "Python-Guides": {
            "keywords": ["python guide", "python subprocess"],
            "subcategories": {}
        }
    },
    "QCM-Quality": {
        "Documentation": {
            "keywords": ["specification", "technical spec"],
            "subcategories": {}
        }
    }
}

# ============================================================================
# LOGGING
# ============================================================================

class Logger:
    def __init__(self):
        self.log_file = None

    def start(self, name):
        LOG_FOLDER.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = LOG_FOLDER / f'{name}_{timestamp}.log'

    def log(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = f"{timestamp} | {message}"
        try:
            print(entry)
        except UnicodeEncodeError:
            print(entry.encode('ascii', 'replace').decode('ascii'))
        if self.log_file:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(entry + '\n')

logger = Logger()

# ============================================================================
# GOOGLE DRIVE FUNCTIONS
# ============================================================================

def get_credentials():
    """Load and refresh Google Drive credentials"""
    with open(CREDENTIALS_PATH, 'rb') as token:
        creds = pickle.load(token)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(CREDENTIALS_PATH, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def get_drive_service():
    """Build Google Drive service"""
    creds = get_credentials()
    return build('drive', 'v3', credentials=creds)

def get_all_documents(service):
    """Get all documents from TKB folders"""
    all_docs = []
    for category, folder_id in CATEGORY_FOLDERS.items():
        query = f"'{folder_id}' in parents and trashed=false"
        results = service.files().list(
            q=query,
            fields='files(id, name, mimeType)',
            pageSize=500
        ).execute()
        files = results.get('files', [])
        for f in files:
            all_docs.append({
                'id': f['id'],
                'name': f['name'],
                'current_category': category,
                'current_folder_id': folder_id
            })
    return all_docs

def create_folder(service, name, parent_id):
    """Create a folder in Google Drive"""
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    folder = service.files().create(body=file_metadata, fields='id, name').execute()
    return folder.get('id')

def move_file(service, file_id, new_parent_id, current_parent_id):
    """Move a file to a new folder"""
    service.files().update(
        fileId=file_id,
        addParents=new_parent_id,
        removeParents=current_parent_id,
        fields='id, parents'
    ).execute()

# ============================================================================
# CATEGORIZATION LOGIC
# ============================================================================

def determine_subcategory(doc_name, current_category):
    """
    Determine the subcategory for a document based on keywords.
    Returns: (subcategory, sub_subcategory) or (None, None)
    """
    name_lower = doc_name.lower()

    if current_category not in TAXONOMY:
        return None, None

    category_taxonomy = TAXONOMY[current_category]

    # Check each subcategory
    best_match = None
    best_sub_match = None
    best_score = 0

    for subcat_name, subcat_config in category_taxonomy.items():
        keywords = subcat_config.get('keywords', [])
        subcategories = subcat_config.get('subcategories', {})

        # Check main subcategory keywords
        score = 0
        for kw in keywords:
            if kw.lower() in name_lower:
                score += 1

        if score > best_score:
            best_score = score
            best_match = subcat_name
            best_sub_match = None

            # Check sub-subcategories
            for sub_name, sub_keywords in subcategories.items():
                for kw in sub_keywords:
                    if kw.lower() in name_lower:
                        best_sub_match = sub_name
                        break

    return best_match, best_sub_match

def analyze_documents(documents):
    """Analyze all documents and determine their subcategories"""
    analysis = []

    for doc in documents:
        subcat, sub_subcat = determine_subcategory(doc['name'], doc['current_category'])

        # Build target path
        if subcat:
            if sub_subcat:
                target_path = f"{doc['current_category']}/{subcat}/{sub_subcat}"
            else:
                target_path = f"{doc['current_category']}/{subcat}"
        else:
            target_path = f"{doc['current_category']}/Uncategorized"

        analysis.append({
            'id': doc['id'],
            'name': doc['name'],
            'current_category': doc['current_category'],
            'current_folder_id': doc['current_folder_id'],
            'subcategory': subcat,
            'sub_subcategory': sub_subcat,
            'target_path': target_path
        })

    return analysis

# ============================================================================
# MAIN FUNCTIONS
# ============================================================================

def create_folder_structure(service):
    """Create all subcategory folders based on taxonomy"""
    folder_mapping = {}

    logger.log("=" * 70)
    logger.log("CREATING FOLDER STRUCTURE")
    logger.log("=" * 70)

    for main_cat, subcats in TAXONOMY.items():
        if main_cat not in CATEGORY_FOLDERS:
            continue

        parent_id = CATEGORY_FOLDERS[main_cat]
        folder_mapping[main_cat] = {'id': parent_id, 'subcategories': {}}

        for subcat_name, subcat_config in subcats.items():
            # Check if folder exists
            query = f"name='{subcat_name}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = service.files().list(q=query, fields='files(id)').execute()
            existing = results.get('files', [])

            if existing:
                subcat_id = existing[0]['id']
                logger.log(f"  [EXISTS] {main_cat}/{subcat_name}")
            else:
                subcat_id = create_folder(service, subcat_name, parent_id)
                logger.log(f"  [CREATED] {main_cat}/{subcat_name}")

            folder_mapping[main_cat]['subcategories'][subcat_name] = {
                'id': subcat_id,
                'subcategories': {}
            }

            # Create sub-subcategories
            sub_subcats = subcat_config.get('subcategories', {})
            for sub_name in sub_subcats.keys():
                query = f"name='{sub_name}' and '{subcat_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
                results = service.files().list(q=query, fields='files(id)').execute()
                existing = results.get('files', [])

                if existing:
                    sub_id = existing[0]['id']
                    logger.log(f"    [EXISTS] {main_cat}/{subcat_name}/{sub_name}")
                else:
                    sub_id = create_folder(service, sub_name, subcat_id)
                    logger.log(f"    [CREATED] {main_cat}/{subcat_name}/{sub_name}")

                folder_mapping[main_cat]['subcategories'][subcat_name]['subcategories'][sub_name] = sub_id

    # Create Uncategorized folders for each main category
    for main_cat, parent_id in CATEGORY_FOLDERS.items():
        if main_cat in folder_mapping and 'Uncategorized' not in folder_mapping[main_cat]['subcategories']:
            query = f"name='Uncategorized' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = service.files().list(q=query, fields='files(id)').execute()
            existing = results.get('files', [])

            if existing:
                uncat_id = existing[0]['id']
            else:
                uncat_id = create_folder(service, 'Uncategorized', parent_id)
                logger.log(f"  [CREATED] {main_cat}/Uncategorized")

            if main_cat not in folder_mapping:
                folder_mapping[main_cat] = {'id': parent_id, 'subcategories': {}}
            folder_mapping[main_cat]['subcategories']['Uncategorized'] = {'id': uncat_id, 'subcategories': {}}

    return folder_mapping

def get_target_folder_id(folder_mapping, target_path):
    """Get the folder ID for a target path like 'AI-Development/MCP-Protocol/MCP-Servers'"""
    parts = target_path.split('/')

    if len(parts) < 2:
        return None

    main_cat = parts[0]
    subcat = parts[1]
    sub_subcat = parts[2] if len(parts) > 2 else None

    if main_cat not in folder_mapping:
        return None

    if subcat not in folder_mapping[main_cat]['subcategories']:
        # Try Uncategorized
        if 'Uncategorized' in folder_mapping[main_cat]['subcategories']:
            return folder_mapping[main_cat]['subcategories']['Uncategorized']['id']
        return None

    subcat_data = folder_mapping[main_cat]['subcategories'][subcat]

    if sub_subcat and sub_subcat in subcat_data.get('subcategories', {}):
        return subcat_data['subcategories'][sub_subcat]

    return subcat_data['id']

def migrate_documents(service, analysis, folder_mapping):
    """Move documents to their new subcategory folders"""
    logger.log("")
    logger.log("=" * 70)
    logger.log("MIGRATING DOCUMENTS")
    logger.log("=" * 70)

    stats = {'moved': 0, 'skipped': 0, 'errors': 0}

    for idx, doc in enumerate(analysis, 1):
        target_folder_id = get_target_folder_id(folder_mapping, doc['target_path'])

        if not target_folder_id:
            logger.log(f"[{idx}] SKIP: No target folder for {doc['name'][:50]}...")
            stats['skipped'] += 1
            continue

        # Skip if already in correct folder
        if target_folder_id == doc['current_folder_id']:
            stats['skipped'] += 1
            continue

        try:
            move_file(service, doc['id'], target_folder_id, doc['current_folder_id'])
            logger.log(f"[{idx}] MOVED: {doc['name'][:50]}... -> {doc['target_path']}")
            stats['moved'] += 1
        except Exception as e:
            logger.log(f"[{idx}] ERROR: {doc['name'][:50]}... - {str(e)}")
            stats['errors'] += 1

    return stats

def generate_tree_visualization(folder_mapping, service):
    """Generate a visual tree of the folder structure with document counts"""
    lines = []
    lines.append("TKB-Trajanus-Knowledge-Base/")

    for main_cat in sorted(folder_mapping.keys()):
        cat_data = folder_mapping[main_cat]

        # Count docs in main category
        query = f"'{cat_data['id']}' in parents and mimeType!='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(q=query, fields='files(id)').execute()
        main_count = len(results.get('files', []))

        lines.append(f"├── {main_cat}/ ({main_count} docs at root)")

        subcats = cat_data.get('subcategories', {})
        for i, (subcat_name, subcat_data) in enumerate(sorted(subcats.items())):
            is_last_subcat = (i == len(subcats) - 1)
            prefix = "└──" if is_last_subcat else "├──"

            # Count docs
            query = f"'{subcat_data['id']}' in parents and mimeType!='application/vnd.google-apps.folder' and trashed=false"
            results = service.files().list(q=query, fields='files(id)').execute()
            subcat_count = len(results.get('files', []))

            lines.append(f"│   {prefix} {subcat_name}/ ({subcat_count} docs)")

            # Sub-subcategories
            sub_subcats = subcat_data.get('subcategories', {})
            for j, (sub_name, sub_id) in enumerate(sorted(sub_subcats.items())):
                is_last_sub = (j == len(sub_subcats) - 1)
                sub_prefix = "└──" if is_last_sub else "├──"
                indent = "    " if is_last_subcat else "│   "

                # Count docs
                query = f"'{sub_id}' in parents and trashed=false"
                results = service.files().list(q=query, fields='files(id)').execute()
                sub_count = len(results.get('files', []))

                lines.append(f"│   {indent}{sub_prefix} {sub_name}/ ({sub_count} docs)")

    return "\n".join(lines)

def main():
    """Main reorganization workflow"""
    logger.start('tkb_reorganize')

    logger.log("=" * 70)
    logger.log("TKB HIERARCHICAL REORGANIZATION v1.0")
    logger.log("=" * 70)
    logger.log(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Connect to Drive
    logger.log("\n[AUTH] Connecting to Google Drive...")
    service = get_drive_service()
    logger.log("[AUTH] Connected")

    # Get all documents
    logger.log("\n[SCAN] Getting all documents...")
    documents = get_all_documents(service)
    logger.log(f"[SCAN] Found {len(documents)} documents")

    # Analyze documents
    logger.log("\n[ANALYZE] Analyzing document categories...")
    analysis = analyze_documents(documents)

    # Count target paths
    path_counts = defaultdict(int)
    for doc in analysis:
        path_counts[doc['target_path']] += 1

    logger.log("\n[ANALYSIS] Target distribution:")
    for path, count in sorted(path_counts.items(), key=lambda x: -x[1]):
        logger.log(f"  {path}: {count} docs")

    # Save analysis
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FOLDER / 'document_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    logger.log(f"\n[SAVE] Analysis saved to {OUTPUT_FOLDER / 'document_analysis.json'}")

    # Create folder structure
    logger.log("\n[FOLDERS] Creating folder structure...")
    folder_mapping = create_folder_structure(service)

    # Save folder mapping
    with open(OUTPUT_FOLDER / 'folder_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(folder_mapping, f, indent=2, ensure_ascii=False)
    logger.log(f"[SAVE] Folder mapping saved to {OUTPUT_FOLDER / 'folder_mapping.json'}")

    # Migrate documents
    logger.log("\n[MIGRATE] Starting document migration...")
    stats = migrate_documents(service, analysis, folder_mapping)

    # Generate tree visualization
    logger.log("\n[TREE] Generating folder tree...")
    tree = generate_tree_visualization(folder_mapping, service)

    with open(OUTPUT_FOLDER / 'folder_structure_tree.txt', 'w', encoding='utf-8') as f:
        f.write(tree)

    # Summary
    logger.log("\n" + "=" * 70)
    logger.log("REORGANIZATION COMPLETE")
    logger.log("=" * 70)
    logger.log(f"Documents analyzed: {len(documents)}")
    logger.log(f"Documents moved: {stats['moved']}")
    logger.log(f"Documents skipped: {stats['skipped']}")
    logger.log(f"Errors: {stats['errors']}")
    logger.log("")
    logger.log("FOLDER STRUCTURE:")
    for line in tree.split('\n')[:30]:
        logger.log(line)
    if len(tree.split('\n')) > 30:
        logger.log("... (truncated)")
    logger.log("")
    logger.log(f"Full tree saved to: {OUTPUT_FOLDER / 'folder_structure_tree.txt'}")
    logger.log(f"Log file: {logger.log_file}")
    logger.log("=" * 70)

if __name__ == '__main__':
    main()
