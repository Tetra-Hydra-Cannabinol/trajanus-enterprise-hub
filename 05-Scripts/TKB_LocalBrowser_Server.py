#!/usr/bin/env python3
"""
TKB Local Browser Server
========================
A simple HTTP server that provides API endpoints for browsing local Google Drive folders.

Usage:
    python TKB_LocalBrowser_Server.py

Then open: http://localhost:8080

This server reads directly from your locally-synced Google Drive folders,
so no Google API credentials are needed.
"""

import os
import json
import mimetypes
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
from datetime import datetime
import html

# Configuration
PORT = 8080
HOST = 'localhost'

# Root folders to browse
ROOTS = {
    'trajanus': r'G:\My Drive\00 - Trajanus USA',
    'archive': r'G:\My Drive\Archive'
}

class TKBRequestHandler(SimpleHTTPRequestHandler):
    """Custom request handler for TKB Browser."""

    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path

        # API endpoints
        if path == '/api/folders':
            self.handle_list_folders()
        elif path == '/api/files':
            self.handle_list_files()
        elif path == '/api/read':
            self.handle_read_file()
        elif path == '/api/roots':
            self.handle_get_roots()
        elif path == '/' or path == '/index.html':
            self.serve_browser_html()
        else:
            # Serve static files
            super().do_GET()

    def handle_get_roots(self):
        """Return available root folders."""
        roots = []
        for key, path in ROOTS.items():
            if os.path.exists(path):
                roots.append({
                    'id': key,
                    'name': os.path.basename(path),
                    'path': path,
                    'exists': True
                })
            else:
                roots.append({
                    'id': key,
                    'name': os.path.basename(path),
                    'path': path,
                    'exists': False
                })

        self.send_json(roots)

    def handle_list_folders(self):
        """List folders in a directory."""
        params = parse_qs(urlparse(self.path).query)
        folder_path = params.get('path', [''])[0]
        folder_path = unquote(folder_path)

        if not folder_path:
            self.send_error(400, 'Missing path parameter')
            return

        # Security check - only allow paths under our roots
        if not self.is_safe_path(folder_path):
            self.send_error(403, 'Access denied')
            return

        if not os.path.exists(folder_path):
            self.send_error(404, 'Folder not found')
            return

        try:
            items = []
            for name in sorted(os.listdir(folder_path)):
                item_path = os.path.join(folder_path, name)
                if os.path.isdir(item_path):
                    # Count subfolders
                    try:
                        subfolder_count = sum(1 for x in os.listdir(item_path) if os.path.isdir(os.path.join(item_path, x)))
                    except:
                        subfolder_count = 0

                    items.append({
                        'name': name,
                        'path': item_path,
                        'type': 'folder',
                        'subfolderCount': subfolder_count
                    })

            self.send_json(items)

        except Exception as e:
            self.send_error(500, str(e))

    def handle_list_files(self):
        """List files in a directory."""
        params = parse_qs(urlparse(self.path).query)
        folder_path = params.get('path', [''])[0]
        folder_path = unquote(folder_path)

        if not folder_path:
            self.send_error(400, 'Missing path parameter')
            return

        if not self.is_safe_path(folder_path):
            self.send_error(403, 'Access denied')
            return

        if not os.path.exists(folder_path):
            self.send_error(404, 'Folder not found')
            return

        try:
            files = []
            folders = []

            for name in sorted(os.listdir(folder_path)):
                item_path = os.path.join(folder_path, name)
                stat = os.stat(item_path)
                modified = datetime.fromtimestamp(stat.st_mtime).isoformat()

                if os.path.isdir(item_path):
                    folders.append({
                        'name': name,
                        'path': item_path,
                        'type': 'folder',
                        'modified': modified
                    })
                else:
                    # Get file extension and mime type
                    ext = os.path.splitext(name)[1].lower()
                    mime_type, _ = mimetypes.guess_type(name)

                    files.append({
                        'name': name,
                        'path': item_path,
                        'type': 'file',
                        'extension': ext,
                        'mimeType': mime_type or 'application/octet-stream',
                        'size': stat.st_size,
                        'modified': modified
                    })

            self.send_json({
                'folders': folders,
                'files': files,
                'path': folder_path,
                'name': os.path.basename(folder_path)
            })

        except Exception as e:
            self.send_error(500, str(e))

    def handle_read_file(self):
        """Read a file's contents."""
        params = parse_qs(urlparse(self.path).query)
        file_path = params.get('path', [''])[0]
        file_path = unquote(file_path)

        if not file_path:
            self.send_error(400, 'Missing path parameter')
            return

        if not self.is_safe_path(file_path):
            self.send_error(403, 'Access denied')
            return

        if not os.path.exists(file_path):
            self.send_error(404, 'File not found')
            return

        if not os.path.isfile(file_path):
            self.send_error(400, 'Not a file')
            return

        try:
            ext = os.path.splitext(file_path)[1].lower()

            # Handle Google Docs shortcut files (.gdoc, .gsheet, .gslides)
            if ext in ['.gdoc', '.gsheet', '.gslides', '.gform']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    gdoc_data = json.load(f)

                # Return the Google Doc URL for opening
                self.send_json({
                    'type': 'google_doc',
                    'url': gdoc_data.get('url', ''),
                    'docId': gdoc_data.get('doc_id', ''),
                    'name': os.path.basename(file_path)
                })
                return

            # Handle text/code files
            text_extensions = ['.txt', '.md', '.py', '.js', '.html', '.htm', '.css',
                            '.json', '.xml', '.yaml', '.yml', '.ps1', '.sh', '.bat',
                            '.sql', '.ts', '.jsx', '.tsx', '.csv', '.log', '.ini',
                            '.cfg', '.conf', '.env', '.gitignore', '.dockerfile']

            if ext in text_extensions:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()

                self.send_json({
                    'type': 'text',
                    'content': content,
                    'name': os.path.basename(file_path),
                    'extension': ext
                })
                return

            # Handle images
            image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.bmp', '.ico']
            if ext in image_extensions:
                self.send_json({
                    'type': 'image',
                    'url': f'/file?path={file_path}',
                    'name': os.path.basename(file_path)
                })
                return

            # Handle PDFs
            if ext == '.pdf':
                self.send_json({
                    'type': 'pdf',
                    'url': f'/file?path={file_path}',
                    'name': os.path.basename(file_path)
                })
                return

            # Unknown file type - return metadata only
            self.send_json({
                'type': 'binary',
                'name': os.path.basename(file_path),
                'size': os.path.getsize(file_path),
                'message': 'This file type cannot be displayed. Download or open externally.'
            })

        except Exception as e:
            self.send_error(500, str(e))

    def is_safe_path(self, path):
        """Check if path is under allowed roots."""
        abs_path = os.path.abspath(path)
        for root in ROOTS.values():
            if os.path.exists(root):
                root_abs = os.path.abspath(root)
                if abs_path.startswith(root_abs):
                    return True
        return False

    def send_json(self, data):
        """Send JSON response."""
        response = json.dumps(data, indent=2)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def serve_browser_html(self):
        """Serve the browser HTML."""
        html_content = self.get_browser_html()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    def get_browser_html(self):
        """Generate the browser HTML."""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TKB Browser - Local File Navigation</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .browser-container {
            max-width: 1600px;
            margin: 0 auto;
        }

        .browser-header {
            background: white;
            border-radius: 12px;
            padding: 20px 30px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 2px solid #9B7E52;
        }

        .browser-header h1 {
            color: #9B7E52;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 15px;
        }

        .button-group {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }

        .drive-btn {
            padding: 12px 24px;
            border: 2px solid #9B7E52;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            background: white;
            color: #9B7E52;
        }

        .drive-btn:hover {
            background: rgba(155, 126, 82, 0.1);
            transform: translateY(-2px);
        }

        .drive-btn.active {
            background: #9B7E52;
            color: white;
        }

        .drive-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .status-text {
            font-size: 0.9rem;
            color: #28a745;
            font-weight: 600;
            margin-left: auto;
        }

        .browser-layout {
            display: flex;
            gap: 20px;
            height: calc(100vh - 180px);
        }

        .tree-pane {
            width: 400px;
            min-width: 300px;
            background: white;
            border: 2px solid #9B7E52;
            border-radius: 12px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .tree-header {
            background: #9B7E52;
            color: white;
            padding: 15px 20px;
            font-weight: 600;
        }

        .tree-content {
            flex: 1;
            overflow-y: auto;
            padding: 15px;
        }

        .file-pane {
            flex: 1;
            background: white;
            border: 2px solid #9B7E52;
            border-radius: 12px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .file-header {
            background: #9B7E52;
            color: white;
            padding: 15px 20px;
            font-weight: 600;
            display: flex;
            justify-content: space-between;
        }

        .file-content {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
        }

        /* Tree View */
        .folder-item {
            display: flex;
            align-items: center;
            padding: 8px 10px;
            cursor: pointer;
            border-radius: 6px;
            transition: all 0.15s;
            user-select: none;
        }

        .folder-item:hover {
            background: rgba(155, 126, 82, 0.1);
        }

        .folder-item.selected {
            background: rgba(155, 126, 82, 0.2);
        }

        .expand-icon {
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: #9B7E52;
            font-size: 1.1rem;
            border-radius: 4px;
        }

        .expand-icon:hover {
            background: rgba(155, 126, 82, 0.3);
        }

        .expand-icon.empty {
            visibility: hidden;
        }

        .folder-icon {
            font-size: 1.2rem;
            margin: 0 8px;
        }

        .folder-name {
            flex: 1;
            font-size: 0.95rem;
            color: #333;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .folder-children {
            margin-left: 24px;
            border-left: 2px solid rgba(155, 126, 82, 0.2);
            padding-left: 8px;
        }

        .folder-children.collapsed {
            display: none;
        }

        /* File List */
        .file-item {
            display: flex;
            align-items: center;
            padding: 15px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            margin-bottom: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .file-item:hover {
            background: rgba(155, 126, 82, 0.08);
            border-color: #9B7E52;
            transform: translateX(5px);
        }

        .file-icon {
            font-size: 2rem;
            margin-right: 15px;
        }

        .file-info {
            flex: 1;
        }

        .file-name {
            font-weight: 600;
            color: #9B7E52;
            margin-bottom: 4px;
        }

        .file-meta {
            font-size: 0.85rem;
            color: #666;
        }

        .file-arrow {
            font-size: 1.5rem;
            color: #9B7E52;
        }

        /* Loading */
        .loading-state {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 200px;
            color: #666;
        }

        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid rgba(155, 126, 82, 0.2);
            border-top-color: #9B7E52;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 15px;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .empty-state {
            text-align: center;
            padding: 40px;
            color: #999;
        }

        .empty-state-icon {
            font-size: 4rem;
            margin-bottom: 15px;
            opacity: 0.5;
        }

        .error-message {
            background: #fff3cd;
            border: 1px solid #ffc107;
            color: #856404;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }

        .breadcrumb {
            font-size: 0.9rem;
            color: rgba(255,255,255,0.8);
        }
    </style>
</head>
<body>
    <div class="browser-container">
        <div class="browser-header">
            <h1>TKB Browser - Local File Navigation</h1>
            <div class="button-group">
                <button id="trajanusBtn" class="drive-btn" onclick="loadRoot('trajanus')">
                    Trajanus USA
                </button>
                <button id="archiveBtn" class="drive-btn" onclick="loadRoot('archive')">
                    Google Drive Archive
                </button>
                <span class="status-text">Connected to local files</span>
            </div>
        </div>

        <div class="browser-layout">
            <div class="tree-pane">
                <div class="tree-header" id="treeHeader">FOLDER TREE</div>
                <div class="tree-content" id="treeContent">
                    <div class="empty-state">
                        <div class="empty-state-icon">📁</div>
                        <p>Select a drive to browse</p>
                    </div>
                </div>
            </div>

            <div class="file-pane">
                <div class="file-header">
                    <span id="fileHeaderTitle">FILE LIST</span>
                    <span id="fileHeaderCount" class="breadcrumb"></span>
                </div>
                <div class="file-content" id="fileContent">
                    <div class="empty-state">
                        <div class="empty-state-icon">📄</div>
                        <p>Select a folder to view files</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentRoot = null;
        let selectedPath = null;

        // Load available roots on page load
        async function init() {
            try {
                const response = await fetch('/api/roots');
                const roots = await response.json();

                roots.forEach(root => {
                    const btn = document.getElementById(root.id + 'Btn');
                    if (btn) {
                        btn.disabled = !root.exists;
                        if (!root.exists) {
                            btn.title = 'Folder not found: ' + root.path;
                        }
                    }
                });
            } catch (error) {
                console.error('Error loading roots:', error);
            }
        }

        async function loadRoot(rootId) {
            currentRoot = rootId;

            // Update button states
            document.querySelectorAll('.drive-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(rootId + 'Btn').classList.add('active');

            // Get root info
            const response = await fetch('/api/roots');
            const roots = await response.json();
            const root = roots.find(r => r.id === rootId);

            if (!root || !root.exists) {
                alert('Folder not found');
                return;
            }

            document.getElementById('treeHeader').textContent = root.name.toUpperCase();

            // Load folder tree
            await loadFolderTree(root.path, root.name);
        }

        async function loadFolderTree(rootPath, rootName) {
            const treeContent = document.getElementById('treeContent');
            treeContent.innerHTML = '<div class="loading-state"><div class="spinner"></div><p>Loading...</p></div>';

            try {
                const response = await fetch('/api/folders?path=' + encodeURIComponent(rootPath));
                const folders = await response.json();

                const rootFolderId = pathToId(rootPath);
                let html = `
                    <div class="folder-item selected" data-path="${escapeHtml(rootPath)}" data-folder-id="${rootFolderId}" onclick="selectFolder('${escapePath(rootPath)}', '${escapePath(rootName)}', event)">
                        <span class="expand-icon" onclick="toggleFolderById('${rootFolderId}', '${escapePath(rootPath)}', event)">−</span>
                        <span class="folder-icon">📁</span>
                        <span class="folder-name">${escapeHtml(rootName)}</span>
                    </div>
                    <div class="folder-children" id="${rootFolderId}-children">
                `;

                for (const folder of folders) {
                    html += renderFolderItem(folder);
                }

                html += '</div>';
                treeContent.innerHTML = html;

                // Select root folder
                await selectFolder(rootPath, rootName);

            } catch (error) {
                treeContent.innerHTML = '<div class="error-message">Failed to load folders: ' + error.message + '</div>';
            }
        }

        function renderFolderItem(folder) {
            const hasSubfolders = folder.subfolderCount > 0;
            const expandClass = hasSubfolders ? '' : 'empty';
            const folderId = pathToId(folder.path);

            return `
                <div class="folder-item" data-path="${escapeHtml(folder.path)}" data-folder-id="${folderId}" onclick="selectFolder('${escapePath(folder.path)}', '${escapePath(folder.name)}', event)">
                    <span class="expand-icon ${expandClass}" onclick="toggleFolderById('${folderId}', '${escapePath(folder.path)}', event)">+</span>
                    <span class="folder-icon">📂</span>
                    <span class="folder-name">${escapeHtml(folder.name)}</span>
                </div>
                <div class="folder-children collapsed" id="${folderId}-children"></div>
            `;
        }

        async function toggleFolderById(folderId, path, event) {
            event.stopPropagation();

            const childrenDiv = document.getElementById(folderId + '-children');
            if (!childrenDiv) return;

            const folderItem = document.querySelector(`[data-folder-id="${folderId}"]`);
            const icon = folderItem ? folderItem.querySelector('.expand-icon') : null;

            const isCollapsed = childrenDiv.classList.contains('collapsed');

            if (isCollapsed) {
                if (icon) icon.textContent = '−';
                childrenDiv.classList.remove('collapsed');

                // Load children if empty
                if (childrenDiv.innerHTML === '') {
                    childrenDiv.innerHTML = '<div style="padding: 10px; color: #999;">Loading...</div>';

                    try {
                        const response = await fetch('/api/folders?path=' + encodeURIComponent(path));
                        const folders = await response.json();

                        if (folders.length === 0) {
                            childrenDiv.innerHTML = '';
                            if (icon) icon.classList.add('empty');
                        } else {
                            let html = '';
                            for (const folder of folders) {
                                html += renderFolderItem(folder);
                            }
                            childrenDiv.innerHTML = html;
                        }
                    } catch (error) {
                        childrenDiv.innerHTML = '<div class="error-message">Error loading</div>';
                    }
                }
            } else {
                if (icon) icon.textContent = '+';
                childrenDiv.classList.add('collapsed');
            }
        }

        async function selectFolder(path, name, event) {
            if (event) event.stopPropagation();

            // Update selection
            document.querySelectorAll('.folder-item').forEach(item => item.classList.remove('selected'));
            const folderId = pathToId(path);
            const folderItem = document.querySelector(`[data-folder-id="${folderId}"]`);
            if (folderItem) folderItem.classList.add('selected');

            selectedPath = path;
            await displayFiles(path, name);
        }

        async function displayFiles(path, name) {
            const fileContent = document.getElementById('fileContent');
            document.getElementById('fileHeaderTitle').textContent = name;
            document.getElementById('fileHeaderCount').textContent = 'Loading...';

            fileContent.innerHTML = '<div class="loading-state"><div class="spinner"></div><p>Loading files...</p></div>';

            try {
                const response = await fetch('/api/files?path=' + encodeURIComponent(path));
                const data = await response.json();

                const fileCount = data.files.length;
                const folderCount = data.folders.length;
                document.getElementById('fileHeaderCount').textContent = `${fileCount} file${fileCount !== 1 ? 's' : ''}, ${folderCount} folder${folderCount !== 1 ? 's' : ''}`;

                if (data.files.length === 0) {
                    fileContent.innerHTML = `
                        <div class="empty-state">
                            <div class="empty-state-icon">📭</div>
                            <p>No files in this folder</p>
                            <p style="font-size: 0.9rem; color: #999; margin-top: 10px;">
                                ${folderCount} subfolder${folderCount !== 1 ? 's' : ''} available
                            </p>
                        </div>
                    `;
                    return;
                }

                let html = '';
                for (const file of data.files) {
                    const icon = getFileIcon(file.extension, file.mimeType);
                    const date = new Date(file.modified).toLocaleDateString('en-US', {
                        year: 'numeric', month: 'short', day: 'numeric'
                    });
                    const fileType = getFileType(file.extension);
                    const size = formatSize(file.size);

                    html += `
                        <div class="file-item" onclick="openFile('${escapePath(file.path)}', '${escapePath(file.name)}')">
                            <span class="file-icon">${icon}</span>
                            <div class="file-info">
                                <div class="file-name">${escapeHtml(file.name)}</div>
                                <div class="file-meta">${fileType} • ${size} • ${date}</div>
                            </div>
                            <span class="file-arrow">→</span>
                        </div>
                    `;
                }

                fileContent.innerHTML = html;

            } catch (error) {
                fileContent.innerHTML = '<div class="error-message">Failed to load files: ' + error.message + '</div>';
            }
        }

        async function openFile(path, name) {
            try {
                const response = await fetch('/api/read?path=' + encodeURIComponent(path));
                const data = await response.json();

                if (data.type === 'google_doc') {
                    // Open Google Doc in new tab
                    window.open(data.url, '_blank');
                    return;
                }

                if (data.type === 'text') {
                    displayTextFile(name, data.content, data.extension);
                    return;
                }

                if (data.type === 'image') {
                    displayImageFile(name, '/api/read?path=' + encodeURIComponent(path) + '&raw=1');
                    return;
                }

                if (data.type === 'binary') {
                    alert(data.message || 'Cannot display this file type.');
                    return;
                }

            } catch (error) {
                alert('Error opening file: ' + error.message);
            }
        }

        function displayTextFile(name, content, ext) {
            const isCode = ['.py', '.js', '.html', '.css', '.json', '.ps1', '.sh', '.sql', '.ts', '.jsx', '.tsx'].includes(ext);

            const html = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>${escapeHtml(name)} - TKB Viewer</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border: 2px solid #9B7E52;
        }
        .header {
            border-bottom: 3px solid #9B7E52;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        h1 {
            color: #9B7E52;
            font-size: 1.8rem;
            word-break: break-word;
        }
        .badge {
            background: #9B7E52;
            color: white;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 0.85rem;
            display: inline-block;
            margin-top: 10px;
        }
        pre {
            background: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.95rem;
            line-height: 1.5;
        }
        .content {
            white-space: pre-wrap;
            font-size: 1.05rem;
        }
        .close-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #9B7E52;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
        }
        .close-btn:hover { background: #7d6542; }
    </style>
</head>
<body>
    <button class="close-btn" onclick="window.close()">✕ Close</button>
    <div class="container">
        <div class="header">
            <h1>${escapeHtml(name)}</h1>
            <span class="badge">${ext.toUpperCase().replace('.', '')} File</span>
        </div>
        ${isCode ? '<pre><code>' + escapeHtml(content) + '</code></pre>' : '<div class="content">' + escapeHtml(content) + '</div>'}
    </div>
</body>
</html>
            `;

            const win = window.open('', '_blank');
            win.document.write(html);
            win.document.close();
        }

        function getFileIcon(ext, mimeType) {
            const icons = {
                '.gdoc': '📄', '.gsheet': '📊', '.gslides': '📽️',
                '.py': '🐍', '.js': '📜', '.ts': '📜',
                '.html': '🌐', '.htm': '🌐', '.css': '🎨',
                '.json': '📋', '.xml': '📋', '.yaml': '📋', '.yml': '📋',
                '.ps1': '⚡', '.sh': '⚡', '.bat': '⚡',
                '.md': '📝', '.txt': '📄',
                '.pdf': '📕',
                '.png': '🖼️', '.jpg': '🖼️', '.jpeg': '🖼️', '.gif': '🖼️', '.webp': '🖼️', '.svg': '🖼️',
                '.mp4': '🎬', '.mov': '🎬', '.avi': '🎬',
                '.mp3': '🎵', '.wav': '🎵',
                '.zip': '📦', '.rar': '📦', '.7z': '📦'
            };
            return icons[ext] || '📄';
        }

        function getFileType(ext) {
            const types = {
                '.gdoc': 'Google Doc', '.gsheet': 'Google Sheet', '.gslides': 'Google Slides',
                '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
                '.html': 'HTML', '.htm': 'HTML', '.css': 'CSS',
                '.json': 'JSON', '.md': 'Markdown', '.txt': 'Text',
                '.pdf': 'PDF', '.ps1': 'PowerShell'
            };
            return types[ext] || ext.toUpperCase().replace('.', '');
        }

        function formatSize(bytes) {
            if (bytes < 1024) return bytes + ' B';
            if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
            return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
        }

        function escapeHtml(text) {
            if (!text) return '';
            return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
        }

        function escapePath(path) {
            // Escape for use in JavaScript strings and HTML attributes
            if (!path) return '';
            return path.replace(/\\\\/g, '\\\\\\\\').replace(/'/g, "\\\\'").replace(/"/g, '\\\\"');
        }

        function pathToId(path) {
            // Convert path to safe ID
            return 'folder-' + btoa(path).replace(/[+/=]/g, '_');
        }

        // Initialize
        init();
    </script>
</body>
</html>'''

def main():
    """Start the server."""
    print("")
    print("=" * 60)
    print("  TKB Local Browser Server")
    print("=" * 60)
    print(f"  Server running at: http://{HOST}:{PORT}")
    print("")
    print("  Browsing folders:")

    for key, path in ROOTS.items():
        exists = "[OK]" if os.path.exists(path) else "[--]"
        print(f"    {exists} {key}: {path}")

    print("")
    print("  Press Ctrl+C to stop the server")
    print("=" * 60)
    print("")

    server = HTTPServer((HOST, PORT), TKBRequestHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.shutdown()

if __name__ == '__main__':
    main()
