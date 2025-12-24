#!/usr/bin/env python3
"""
ORGANIZE USER'S GUIDES FOLDER
Converts files to Google Docs, analyzes content, creates categories, and organizes.

Author: Claude Code
Date: 2025-12-18
"""

import pickle
import json
import time
from pathlib import Path
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from collections import defaultdict
import io

# ============================================================================
# CONFIGURATION
# ============================================================================

CREDENTIALS_PATH = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/Credentials/token.pickle")
OUTPUT_DIR = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/outputs")
LOG_DIR = Path("G:/My Drive/00 - Trajanus USA/00-Command-Center/logs")

# User's Guides folder
USERS_GUIDES_FOLDER_ID = "1zBHvLXZYSByV2R0gHtpYBBuF5DnmU8K8"

# ============================================================================
# GOOGLE DRIVE SERVICE
# ============================================================================

def get_service():
    with open(CREDENTIALS_PATH, "rb") as token:
        creds = pickle.load(token)
    return build("drive", "v3", credentials=creds)

# ============================================================================
# PHASE 1: RECONNAISSANCE
# ============================================================================

def list_all_files(service):
    """List all files in User's Guides folder."""
    print("\n[PHASE 1] RECONNAISSANCE")
    print("=" * 60)

    query = f"'{USERS_GUIDES_FOLDER_ID}' in parents and trashed = false"
    results = service.files().list(
        q=query,
        fields="files(id, name, mimeType, webViewLink)",
        pageSize=200
    ).execute()

    files = results.get('files', [])

    # Separate folders from files
    folders = [f for f in files if f['mimeType'] == 'application/vnd.google-apps.folder']
    documents = [f for f in files if f['mimeType'] != 'application/vnd.google-apps.folder']

    print(f"\nFound {len(documents)} files and {len(folders)} existing folders")

    # Categorize by type
    needs_conversion = []
    already_gdocs = []
    other_files = []

    for file in documents:
        name = file['name']
        mime = file['mimeType']

        if mime == 'application/vnd.google-apps.document':
            already_gdocs.append(file)
        elif name.endswith('.md') or mime == 'text/markdown':
            needs_conversion.append(file)
        elif name.endswith(('.docx', '.doc')) or 'word' in mime.lower():
            needs_conversion.append(file)
        elif name.endswith('.txt') or mime == 'text/plain':
            needs_conversion.append(file)
        else:
            other_files.append(file)

    print(f"\nFile breakdown:")
    print(f"  - Already Google Docs: {len(already_gdocs)}")
    print(f"  - Need conversion (md/docx/txt): {len(needs_conversion)}")
    print(f"  - Other files: {len(other_files)}")

    print(f"\nFiles needing conversion:")
    for f in needs_conversion:
        try:
            print(f"  - {f['name']} ({f['mimeType']})")
        except:
            print(f"  - {f['name'].encode('ascii', 'replace').decode()}")

    return {
        'all_files': documents,
        'folders': folders,
        'needs_conversion': needs_conversion,
        'already_gdocs': already_gdocs,
        'other_files': other_files
    }

# ============================================================================
# PHASE 2: FILE CONVERSION
# ============================================================================

def convert_file_to_gdoc(service, file):
    """Convert a file to Google Doc format."""
    file_id = file['id']
    file_name = file['name']
    mime_type = file['mimeType']

    # Clean up name (remove extension)
    clean_name = file_name
    for ext in ['.md', '.docx', '.doc', '.txt']:
        if clean_name.lower().endswith(ext):
            clean_name = clean_name[:-len(ext)]

    try:
        if file_name.endswith(('.docx', '.doc')) or 'word' in mime_type.lower():
            # Word docs can be copied with conversion
            doc_metadata = {
                'name': clean_name,
                'mimeType': 'application/vnd.google-apps.document',
                'parents': [USERS_GUIDES_FOLDER_ID]
            }
            doc = service.files().copy(
                fileId=file_id,
                body=doc_metadata
            ).execute()
            return doc, "converted"

        elif file_name.endswith('.md') or file_name.endswith('.txt') or mime_type == 'text/plain':
            # Download content first
            content = service.files().get_media(fileId=file_id).execute()

            # Create Google Doc with content
            doc_metadata = {
                'name': clean_name,
                'mimeType': 'application/vnd.google-apps.document',
                'parents': [USERS_GUIDES_FOLDER_ID]
            }

            media = MediaIoBaseUpload(
                io.BytesIO(content),
                mimetype='text/plain',
                resumable=True
            )

            doc = service.files().create(
                body=doc_metadata,
                media_body=media,
                fields='id, name'
            ).execute()
            return doc, "converted"

    except Exception as e:
        print(f"  ERROR converting {file_name}: {e}")
        return None, str(e)

    return None, "unsupported"

def convert_all_files(service, files_to_convert):
    """Convert all files that need conversion."""
    print("\n[PHASE 2] FILE CONVERSION")
    print("=" * 60)

    if not files_to_convert:
        print("No files need conversion.")
        return []

    converted = []
    errors = []

    for i, file in enumerate(files_to_convert):
        print(f"\n  Converting ({i+1}/{len(files_to_convert)}): {file['name']}")
        doc, status = convert_file_to_gdoc(service, file)

        if doc:
            print(f"    [OK] Created: {doc['name']}")
            converted.append({
                'original': file,
                'converted': doc,
                'status': status
            })
        else:
            print(f"    [ERROR] Failed: {status}")
            errors.append({
                'original': file,
                'error': status
            })

    print(f"\nConversion complete:")
    print(f"  - Converted: {len(converted)}")
    print(f"  - Errors: {len(errors)}")

    return converted

# ============================================================================
# PHASE 3: CONTENT ANALYSIS
# ============================================================================

def get_doc_content(service, file_id):
    """Get text content from a Google Doc."""
    try:
        content = service.files().export(
            fileId=file_id,
            mimeType='text/plain'
        ).execute()
        return content.decode('utf-8')[:2000]  # First 2000 chars
    except:
        return ""

def analyze_files(service):
    """Analyze all Google Docs and categorize them."""
    print("\n[PHASE 3] CONTENT ANALYSIS")
    print("=" * 60)

    # Get all Google Docs in folder
    query = f"'{USERS_GUIDES_FOLDER_ID}' in parents and mimeType = 'application/vnd.google-apps.document' and trashed = false"
    results = service.files().list(
        q=query,
        fields="files(id, name)",
        pageSize=200
    ).execute()

    docs = results.get('files', [])
    print(f"\nAnalyzing {len(docs)} Google Docs...")

    # Keyword mapping for categories
    category_keywords = {
        'Integration-Guides': ['procore', 'p6', 'primavera', 'rms', 'integration', 'sync', 'import', 'export'],
        'System-Architecture': ['architecture', 'system', 'design', 'structure', 'component', 'module'],
        'Knowledge-Base-RAG': ['rag', 'knowledge', 'supabase', 'vector', 'embedding', 'retrieval', 'chunk'],
        'MCP-API-Documentation': ['mcp', 'api', 'server', 'protocol', 'endpoint', 'request', 'response'],
        'Session-Protocols': ['session', 'protocol', 'workflow', 'process', 'procedure', 'handoff'],
        'Developer-Documentation': ['developer', 'code', 'technical', 'implementation', 'function', 'class'],
        'Traffic-Studies': ['traffic', 'study', 'count', 'volume', 'intersection', 'turning'],
        'User-Instructions': ['user', 'guide', 'instruction', 'how to', 'tutorial', 'step']
    }

    file_analysis = []
    category_counts = defaultdict(int)

    for i, doc in enumerate(docs):
        if (i + 1) % 10 == 0:
            print(f"  Progress: {i+1}/{len(docs)}")

        content = get_doc_content(service, doc['id'])
        text = (doc['name'] + ' ' + content).lower()

        # Score each category
        scores = {}
        for category, keywords in category_keywords.items():
            score = sum(3 if kw in text else 0 for kw in keywords)
            # Bonus for keyword in title
            score += sum(5 if kw in doc['name'].lower() else 0 for kw in keywords)
            scores[category] = score

        # Get best category
        best_category = max(scores, key=scores.get)
        best_score = scores[best_category]

        # If no strong match, use General
        if best_score < 3:
            best_category = 'General-Documentation'

        category_counts[best_category] += 1

        file_analysis.append({
            'id': doc['id'],
            'name': doc['name'],
            'category': best_category,
            'score': best_score
        })

    print(f"\nCategory distribution:")
    for cat, count in sorted(category_counts.items()):
        print(f"  - {cat}: {count} files")

    return file_analysis, category_counts

# ============================================================================
# PHASE 4: CREATE FOLDERS
# ============================================================================

def create_category_folders(service, categories):
    """Create subfolders for each category."""
    print("\n[PHASE 4] CREATE FOLDER STRUCTURE")
    print("=" * 60)

    created_folders = {}

    for category in categories:
        # Check if folder already exists
        query = f"'{USERS_GUIDES_FOLDER_ID}' in parents and name = '{category}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        existing = results.get('files', [])

        if existing:
            print(f"  [EXISTS] Folder exists: {category}")
            created_folders[category] = existing[0]['id']
        else:
            folder_metadata = {
                'name': category,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [USERS_GUIDES_FOLDER_ID]
            }

            folder = service.files().create(
                body=folder_metadata,
                fields='id, name'
            ).execute()

            created_folders[category] = folder['id']
            print(f"  [OK] Created: {category}")

    print(f"\n{len(created_folders)} category folders ready")
    return created_folders

# ============================================================================
# PHASE 5: MOVE FILES
# ============================================================================

def move_files_to_categories(service, file_analysis, folder_mapping):
    """Move each file to its assigned category folder."""
    print("\n[PHASE 5] MOVE FILES TO CATEGORIES")
    print("=" * 60)

    move_log = []
    success_count = 0
    error_count = 0

    for i, item in enumerate(file_analysis):
        file_id = item['id']
        file_name = item['name']
        category = item['category']

        if category not in folder_mapping:
            print(f"  [WARN] No folder for category: {category}")
            continue

        target_folder_id = folder_mapping[category]

        try:
            # Get current parents
            file = service.files().get(fileId=file_id, fields='parents').execute()
            current_parents = ','.join(file.get('parents', []))

            # Move file
            service.files().update(
                fileId=file_id,
                addParents=target_folder_id,
                removeParents=current_parents,
                fields='id'
            ).execute()

            success_count += 1
            move_log.append({
                'file': file_name,
                'category': category,
                'status': 'success'
            })

            if (i + 1) % 10 == 0:
                print(f"  Progress: {i+1}/{len(file_analysis)} ({success_count} moved)")

        except Exception as e:
            error_count += 1
            move_log.append({
                'file': file_name,
                'category': category,
                'status': 'error',
                'error': str(e)
            })
            print(f"  [ERROR] Error moving {file_name}: {e}")

    print(f"\nMove complete:")
    print(f"  - Successful: {success_count}")
    print(f"  - Errors: {error_count}")

    return move_log

# ============================================================================
# PHASE 6: REPORTS
# ============================================================================

def generate_reports(service, file_analysis, folder_mapping, move_log, conversion_info):
    """Generate organization reports."""
    print("\n[PHASE 6] GENERATE REPORTS")
    print("=" * 60)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Build folder tree
    tree_lines = ["User's Guides/", ""]

    for category in sorted(folder_mapping.keys()):
        folder_id = folder_mapping[category]

        # Get files in this folder
        query = f"'{folder_id}' in parents and trashed = false"
        results = service.files().list(
            q=query,
            fields="files(name)",
            orderBy="name"
        ).execute()

        files_in_folder = results.get('files', [])
        tree_lines.append(f"├── {category}/ ({len(files_in_folder)} files)")

        for j, f in enumerate(files_in_folder):
            is_last = (j == len(files_in_folder) - 1)
            prefix = "│   └──" if is_last else "│   ├──"
            tree_lines.append(f"{prefix} {f['name']}")

    # Save tree
    tree_path = OUTPUT_DIR / "User_Guides_Folder_Tree.txt"
    with open(tree_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(tree_lines))
    print(f"  [OK] Folder tree: {tree_path}")

    # Build JSON report
    report = {
        'date': datetime.now().isoformat(),
        'base_folder': "User's Guides",
        'base_folder_id': USERS_GUIDES_FOLDER_ID,
        'total_files': len(file_analysis),
        'conversions': len(conversion_info) if conversion_info else 0,
        'folders_created': list(folder_mapping.keys()),
        'category_distribution': {},
        'move_log': move_log
    }

    for item in file_analysis:
        cat = item['category']
        report['category_distribution'][cat] = report['category_distribution'].get(cat, 0) + 1

    report_path = OUTPUT_DIR / "User_Guides_Organization_Report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print(f"  [OK] JSON report: {report_path}")

    # Build summary
    summary = f"""# User's Guides Organization Summary

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Base Folder:** User's Guides
**Total Files Processed:** {len(file_analysis)}
**Files Converted:** {len(conversion_info) if conversion_info else 0}
**Categories Created:** {len(folder_mapping)}

## Category Distribution

"""

    for cat in sorted(report['category_distribution'].keys()):
        count = report['category_distribution'][cat]
        summary += f"- **{cat}**: {count} files\n"

    summary += f"""
## Folder Structure

```
{"chr(10)".join(tree_lines)}
```

## Location

**Google Drive Path:** `G:/My Drive/00 - Trajanus USA/09-Active-Projects/User's Guides/`

Each subfolder contains related documentation for easy navigation.
"""

    summary_path = OUTPUT_DIR / "User_Guides_Organization_Summary.md"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"  [OK] Summary: {summary_path}")

    # Print tree
    print("\n" + "=" * 60)
    print("FINAL FOLDER STRUCTURE")
    print("=" * 60)
    for line in tree_lines:
        try:
            print(line)
        except:
            print(line.encode('ascii', 'replace').decode())

    return tree_lines

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 70)
    print("ORGANIZE USER'S GUIDES FOLDER")
    print("=" * 70)

    service = get_service()

    # Phase 1: List files
    inventory = list_all_files(service)

    # Phase 2: Convert files
    converted = convert_all_files(service, inventory['needs_conversion'])

    # Phase 3: Analyze content
    file_analysis, category_counts = analyze_files(service)

    # Get unique categories
    categories = list(set(item['category'] for item in file_analysis))

    # Phase 4: Create folders
    folder_mapping = create_category_folders(service, categories)

    # Phase 5: Move files
    move_log = move_files_to_categories(service, file_analysis, folder_mapping)

    # Phase 6: Generate reports
    generate_reports(service, file_analysis, folder_mapping, move_log, converted)

    print("\n" + "=" * 70)
    print("ORGANIZATION COMPLETE")
    print("=" * 70)
    print(f"\nUser's Guides folder is now organized!")
    print(f"Location: G:/My Drive/00 - Trajanus USA/09-Active-Projects/User's Guides/")

if __name__ == "__main__":
    main()
