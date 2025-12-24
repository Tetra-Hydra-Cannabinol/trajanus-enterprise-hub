#!/usr/bin/env python3
"""
MIGRATE TKB TO 13-KNOWLEDGE-BASE
Moves all documents from TKB-Trajanus-Knowledge-Base to the correct 13-Knowledge-Base location
with proper hierarchical structure.

Author: Claude Code
Date: 2025-12-18
"""

import pickle
import json
from pathlib import Path
from datetime import datetime
from googleapiclient.discovery import build
from collections import defaultdict

# ============================================================================
# CONFIGURATION
# ============================================================================

CREDENTIALS_PATH = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/Credentials/token.pickle")
OUTPUT_DIR = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/outputs")
LOG_DIR = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/logs")

# CORRECT destination folder
KB_FOLDER_ID = "1E7kK8ZIZ9-9xZ4HtvbuVbY_iX3DKmEYM"  # 13-Knowledge-Base

# OLD TKB folder IDs (source)
OLD_TKB = {
    "AI-Development": "1VVeotAPnechdDPfLnDTiOZqKA5ZEQDRM",
    "Software-Tools": "1xMWr71AGbZOfnOjAy8IoVOt75Kf_KMAx",
    "Technical-Guides": "1guwUKpc4vUnsuZ0pibalGV0jzBnYZO1n",
    "QCM-Quality": "1ehvTr0P1xQzpKmqOVyiIE-FHR8B66Zpv"
}

# ============================================================================
# HIERARCHICAL TAXONOMY FOR 13-Knowledge-Base
# ============================================================================

TAXONOMY = {
    "10-AI-Development": {
        "keywords": ["claude", "ai", "machine learning", "chatgpt", "automation", "llm", "agent", "anthropic", "openai", "embedding", "vector", "neural", "gpt", "mcp", "langchain", "rag"],
        "subcategories": {
            "Agents": {
                "keywords": ["agent", "subagent", "multi-agent", "agentic", "harness"],
                "subcategories": {
                    "Claude-Agent-SDK": {"keywords": ["agent sdk", "claude sdk", "anthropic sdk"]},
                    "Multi-Agent-Systems": {"keywords": ["multi-agent", "subagent", "collaboration", "orchestrat"]},
                    "Agent-Patterns": {"keywords": ["harness", "context window", "state management", "context engineer"]}
                }
            },
            "RAG-Systems": {
                "keywords": ["rag", "retrieval augmented", "chunking", "rerank", "hybrid search"],
                "subcategories": {
                    "Chunking-Strategies": {"keywords": ["chunk", "chunking", "split", "semantic chunk"]},
                    "Retrieval-Optimization": {"keywords": ["rerank", "hybrid search", "retrieval", "bm25"]},
                    "RAG-Monitoring": {"keywords": ["rag monitor", "rag eval", "rag metric", "rag accuracy"]}
                }
            },
            "Vector-Databases": {
                "keywords": ["pgvector", "vector similarity", "hnsw", "ivfflat", "vector index", "vector search", "pinecone", "chroma"],
                "subcategories": {
                    "Pgvector": {"keywords": ["pgvector", "pg vector", "postgresql vector"]},
                    "Embeddings": {"keywords": ["embedding", "text-embedding", "openai embed", "embed model"]}
                }
            },
            "MCP-Protocol": {
                "keywords": ["mcp", "model context protocol"],
                "subcategories": {
                    "MCP-Servers": {"keywords": ["mcp server", "build mcp", "building mcp", "stdio", "sse server"]},
                    "MCP-Integration": {"keywords": ["mcp integration", "mcp sse", "mcp debug", "mcp vs code"]},
                    "MCP-Best-Practices": {"keywords": ["mcp best practice", "mcp schema", "mcp production"]}
                }
            },
            "Claude-Specific": {
                "keywords": ["claude", "anthropic", "claude code", "opus", "sonnet", "haiku"],
                "subcategories": {
                    "Claude-Updates": {"keywords": ["claude update", "new feature", "release", "announcement"]},
                    "Claude-API": {"keywords": ["api", "claude api", "anthropic api", "sdk"]},
                    "Claude-Code-Tool": {"keywords": ["claude code", "cli", "terminal", "command line"]}
                }
            },
            "Playwright-Testing": {
                "keywords": ["playwright"],
                "subcategories": {
                    "Screenshots": {"keywords": ["screenshot", "snapshot", "visual"]},
                    "Testing-Guides": {"keywords": ["test", "testing", "automation test"]}
                }
            },
            "Supabase-AI": {
                "keywords": ["supabase", "supavisor", "rls", "row level security"],
                "subcategories": {
                    "Connection-Management": {"keywords": ["connection", "pooling", "supavisor"]},
                    "Row-Level-Security": {"keywords": ["rls", "row level", "security policies"]}
                }
            },
            "Google-Cloud-APIs": {
                "keywords": ["google drive", "cloud storage", "google api", "resumable upload"],
                "subcategories": {
                    "Drive-Storage": {"keywords": ["drive api", "upload", "storage", "google drive"]}
                }
            },
            "Uncategorized": {"keywords": [], "subcategories": {}}
        }
    },
    "11-Software-Tools": {
        "keywords": ["electron", "javascript", "typescript", "node", "npm", "python", "library", "tool", "framework", "api"],
        "subcategories": {
            "Electron": {
                "keywords": ["electron", "desktop app", "chromium", "ipc"],
                "subcategories": {
                    "IPC-Communication": {"keywords": ["ipc", "ipcmain", "ipcrenderer", "preload"]},
                    "Python-Integration": {"keywords": ["python electron", "spawn", "child process"]},
                    "Security-Architecture": {"keywords": ["sandbox", "context isolation", "security"]}
                }
            },
            "Google-APIs": {
                "keywords": ["google", "drive api", "docs api", "sheets api"],
                "subcategories": {
                    "Drive-API": {"keywords": ["drive", "file", "folder", "upload"]},
                    "Docs-API": {"keywords": ["docs", "document", "google doc"]}
                }
            },
            "Python-Development": {
                "keywords": ["python", "pip", "virtualenv", "async"],
                "subcategories": {
                    "Subprocess": {"keywords": ["subprocess", "popen", "spawn", "shell"]},
                    "Security": {"keywords": ["security", "sanitize", "escape", "injection"]}
                }
            },
            "JavaScript-Libraries": {
                "keywords": ["javascript", "typescript", "npm", "node"],
                "subcategories": {
                    "File-Management": {"keywords": ["file", "fs", "path", "glob"]},
                    "Frameworks": {"keywords": ["react", "vue", "express", "next"]}
                }
            },
            "Supabase-Tools": {"keywords": ["supabase client", "supabase js"], "subcategories": {}},
            "Uncategorized": {"keywords": [], "subcategories": {}}
        }
    },
    "12-Technical-Guides": {
        "keywords": ["guide", "tutorial", "how to", "setup", "install", "configure", "documentation"],
        "subcategories": {
            "Setup-Installation": {"keywords": ["setup", "install", "getting started"], "subcategories": {}},
            "Configuration": {"keywords": ["config", "settings", "environment"], "subcategories": {}},
            "Node-Documentation": {"keywords": ["node", "npm", "package"], "subcategories": {}},
            "Python-Guides": {"keywords": ["python", "pip", "virtualenv"], "subcategories": {}},
            "Documentation-Standards": {"keywords": ["documentation", "standard", "template"], "subcategories": {}},
            "Uncategorized": {"keywords": [], "subcategories": {}}
        }
    },
    "13-QCM-Quality": {
        "keywords": ["qcm", "quality", "inspection", "submittal", "testing", "compliance"],
        "subcategories": {
            "Submittal-Review": {"keywords": ["submittal", "review"], "subcategories": {}},
            "Inspection-Procedures": {"keywords": ["inspection", "procedure"], "subcategories": {}},
            "Testing-Requirements": {"keywords": ["test", "requirement"], "subcategories": {}},
            "Documentation": {"keywords": ["documentation", "standard"], "subcategories": {}},
            "Uncategorized": {"keywords": [], "subcategories": {}}
        }
    }
}

# ============================================================================
# GOOGLE DRIVE SERVICE
# ============================================================================

def get_service():
    with open(CREDENTIALS_PATH, "rb") as token:
        creds = pickle.load(token)
    return build("drive", "v3", credentials=creds)

# ============================================================================
# PHASE 1: ANALYZE DOCUMENTS
# ============================================================================

def get_all_documents(service):
    """Get all documents from old TKB folders recursively."""
    documents = []

    def scan_folder(folder_id, path=""):
        query = f"'{folder_id}' in parents and trashed = false"
        results = service.files().list(
            q=query,
            pageSize=200,
            fields="files(id, name, mimeType)"
        ).execute()

        for item in results.get('files', []):
            if item['mimeType'] == 'application/vnd.google-apps.document':
                documents.append({
                    "id": item['id'],
                    "name": item['name'],
                    "source_path": path,
                    "source_folder_id": folder_id
                })
            elif item['mimeType'] == 'application/vnd.google-apps.folder':
                new_path = f"{path}/{item['name']}" if path else item['name']
                scan_folder(item['id'], new_path)

    for category, folder_id in OLD_TKB.items():
        print(f"  Scanning {category}...")
        scan_folder(folder_id, category)

    return documents

def categorize_document(name, source_path):
    """Determine the best hierarchical path for a document."""
    text = f"{name} {source_path}".lower()

    best_main = "10-AI-Development"
    best_sub = "Uncategorized"
    best_subsub = None
    best_score = 0

    for main_cat, main_data in TAXONOMY.items():
        main_keywords = main_data.get("keywords", [])
        main_score = sum(2 for kw in main_keywords if kw.lower() in text)

        for sub_cat, sub_data in main_data.get("subcategories", {}).items():
            sub_keywords = sub_data.get("keywords", [])
            sub_score = main_score + sum(3 for kw in sub_keywords if kw.lower() in text)

            # Check sub-subcategories
            for subsub_cat, subsub_data in sub_data.get("subcategories", {}).items():
                subsub_keywords = subsub_data.get("keywords", [])
                subsub_score = sub_score + sum(5 for kw in subsub_keywords if kw.lower() in text)

                if subsub_score > best_score:
                    best_score = subsub_score
                    best_main = main_cat
                    best_sub = sub_cat
                    best_subsub = subsub_cat

            # Maybe just sub-category is best
            if sub_score > best_score and sub_cat != "Uncategorized":
                best_score = sub_score
                best_main = main_cat
                best_sub = sub_cat
                best_subsub = None

    if best_subsub:
        return f"{best_main}/{best_sub}/{best_subsub}"
    else:
        return f"{best_main}/{best_sub}"

# ============================================================================
# PHASE 2: CREATE FOLDERS
# ============================================================================

def create_folder(service, name, parent_id):
    """Create a folder in Google Drive."""
    metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    folder = service.files().create(body=metadata, fields='id').execute()
    return folder.get('id')

def create_all_folders(service):
    """Create all hierarchical folders in 13-Knowledge-Base."""
    folder_mapping = {}

    print("\nCreating folder structure in 13-Knowledge-Base...")

    for main_cat, main_data in TAXONOMY.items():
        # Create main category folder
        print(f"  Creating {main_cat}/")
        main_id = create_folder(service, main_cat, KB_FOLDER_ID)
        folder_mapping[main_cat] = {"id": main_id, "subcategories": {}}

        for sub_cat, sub_data in main_data.get("subcategories", {}).items():
            # Create subcategory folder
            print(f"    Creating {main_cat}/{sub_cat}/")
            sub_id = create_folder(service, sub_cat, main_id)
            folder_mapping[main_cat]["subcategories"][sub_cat] = {"id": sub_id, "subcategories": {}}

            for subsub_cat, subsub_data in sub_data.get("subcategories", {}).items():
                # Create sub-subcategory folder
                print(f"      Creating {main_cat}/{sub_cat}/{subsub_cat}/")
                subsub_id = create_folder(service, subsub_cat, sub_id)
                folder_mapping[main_cat]["subcategories"][sub_cat]["subcategories"][subsub_cat] = subsub_id

    return folder_mapping

def get_folder_id_from_path(folder_mapping, path):
    """Get folder ID from hierarchical path like '10-AI-Development/RAG-Systems/Chunking-Strategies'."""
    parts = path.split("/")

    if len(parts) >= 1:
        main = parts[0]
        if main not in folder_mapping:
            return folder_mapping["10-AI-Development"]["subcategories"]["Uncategorized"]["id"]

        if len(parts) == 1:
            return folder_mapping[main]["id"]

        sub = parts[1]
        if sub not in folder_mapping[main]["subcategories"]:
            return folder_mapping[main]["subcategories"].get("Uncategorized", {}).get("id", folder_mapping[main]["id"])

        if len(parts) == 2:
            return folder_mapping[main]["subcategories"][sub]["id"]

        subsub = parts[2]
        subsub_cats = folder_mapping[main]["subcategories"][sub].get("subcategories", {})
        if subsub in subsub_cats:
            return subsub_cats[subsub]
        else:
            return folder_mapping[main]["subcategories"][sub]["id"]

    return folder_mapping["10-AI-Development"]["subcategories"]["Uncategorized"]["id"]

# ============================================================================
# PHASE 3: MIGRATE DOCUMENTS
# ============================================================================

def move_document(service, file_id, old_parent_id, new_parent_id):
    """Move a document from one folder to another."""
    service.files().update(
        fileId=file_id,
        addParents=new_parent_id,
        removeParents=old_parent_id,
        fields='id, parents'
    ).execute()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"migrate_13kb_{timestamp}.log"

    print("=" * 70)
    print("MIGRATE TKB TO 13-KNOWLEDGE-BASE")
    print("=" * 70)

    service = get_service()

    # Phase 1: Get all documents
    print("\n[PHASE 1] Scanning documents in old TKB...")
    documents = get_all_documents(service)
    print(f"  Found {len(documents)} documents")

    # Phase 2: Analyze and categorize
    print("\n[PHASE 2] Analyzing documents...")
    analysis = []
    category_counts = defaultdict(int)

    for doc in documents:
        target_path = categorize_document(doc['name'], doc['source_path'])
        doc['target_path'] = target_path
        analysis.append(doc)
        category_counts[target_path] += 1

    print("\n  Target distribution:")
    for path, count in sorted(category_counts.items()):
        try:
            print(f"    {path}: {count} docs")
        except UnicodeEncodeError:
            print(f"    {path.encode('ascii', 'replace').decode()}: {count} docs")

    # Save analysis
    analysis_file = OUTPUT_DIR / "document_analysis_13kb.json"
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    print(f"\n  Analysis saved to: {analysis_file}")

    # Phase 3: Create folders
    print("\n[PHASE 3] Creating folders in 13-Knowledge-Base...")
    folder_mapping = create_all_folders(service)

    # Save folder mapping
    mapping_file = OUTPUT_DIR / "folder_mapping_13kb.json"
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(folder_mapping, f, indent=2)
    print(f"  Folder mapping saved to: {mapping_file}")

    # Phase 4: Migrate documents
    print(f"\n[PHASE 4] Migrating {len(documents)} documents...")

    migrated = 0
    errors = []
    log_entries = []

    for i, doc in enumerate(analysis):
        try:
            target_folder_id = get_folder_id_from_path(folder_mapping, doc['target_path'])
            move_document(service, doc['id'], doc['source_folder_id'], target_folder_id)

            log_entry = f"MOVED: {doc['name']}\n  FROM: {doc['source_path']}\n  TO: {doc['target_path']}"
            log_entries.append(log_entry)
            migrated += 1

            if (i + 1) % 20 == 0:
                print(f"    Progress: {i + 1}/{len(documents)} ({migrated} migrated)")

        except Exception as e:
            error_msg = f"ERROR: {doc['name']} - {str(e)}"
            errors.append(error_msg)
            log_entries.append(error_msg)

    # Save migration log
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"Migration Log - {timestamp}\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total documents: {len(documents)}\n")
        f.write(f"Successfully migrated: {migrated}\n")
        f.write(f"Errors: {len(errors)}\n\n")
        f.write("=" * 70 + "\n\n")
        for entry in log_entries:
            f.write(entry + "\n\n")

    # Phase 5: Generate report
    print("\n[PHASE 5] Generating reports...")

    # Generate tree structure
    tree_lines = ["13-Knowledge-Base/"]
    for main_cat, main_data in folder_mapping.items():
        tree_lines.append(f"├── {main_cat}/")
        subs = list(main_data.get("subcategories", {}).items())
        for i, (sub_cat, sub_data) in enumerate(subs):
            is_last_sub = (i == len(subs) - 1)
            prefix = "│   └──" if is_last_sub else "│   ├──"
            count = category_counts.get(f"{main_cat}/{sub_cat}", 0)
            tree_lines.append(f"{prefix} {sub_cat}/ ({count} docs)")

            subsubs = list(sub_data.get("subcategories", {}).items())
            for j, (subsub_cat, subsub_id) in enumerate(subsubs):
                is_last_subsub = (j == len(subsubs) - 1)
                sub_prefix = "│       └──" if is_last_subsub else "│       ├──"
                if is_last_sub:
                    sub_prefix = "        └──" if is_last_subsub else "        ├──"
                subcount = category_counts.get(f"{main_cat}/{sub_cat}/{subsub_cat}", 0)
                tree_lines.append(f"{sub_prefix} {subsub_cat}/ ({subcount} docs)")

    tree_file = OUTPUT_DIR / "folder_structure_13kb.txt"
    with open(tree_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(tree_lines))

    # Print summary
    print("\n" + "=" * 70)
    print("MIGRATION COMPLETE")
    print("=" * 70)
    print(f"Documents migrated: {migrated}")
    print(f"Errors: {len(errors)}")
    print(f"\nNew location: My Drive > 00 - Trajanus USA > 13-Knowledge-Base")
    print(f"\nFiles created:")
    print(f"  - {analysis_file}")
    print(f"  - {mapping_file}")
    print(f"  - {tree_file}")
    print(f"  - {log_file}")

    if errors:
        print("\nErrors encountered:")
        for err in errors[:5]:
            print(f"  {err}")
        if len(errors) > 5:
            print(f"  ... and {len(errors) - 5} more")

    return migrated, errors

if __name__ == "__main__":
    main()
