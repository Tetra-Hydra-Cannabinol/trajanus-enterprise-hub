/**
 * Google Drive Browser for Trajanus Command Center
 * Implements UniversalBrowser interface for local/Google Drive files
 * Created: 2025-12-15
 */

// =============================================================================
// GDRIVE BROWSER CLASS
// =============================================================================

class GDriveBrowser {
    constructor(options = {}) {
        this.type = 'gdrive';
        this.overlayId = 'gdriveBrowserOverlay';
        this.currentPath = options.rootPath || 'G:\\My Drive\\00 - Trajanus USA';
        this.rootPath = options.rootPath || 'G:\\My Drive\\00 - Trajanus USA';
        this.pathHistory = [];
        this.selectedItems = [];
        this.allItems = [];
        this.filteredItems = [];
        this.itemsPerPage = 50;
        this.currentPage = 1;
        this.onSelect = options.onSelect || null;
        this.multiSelect = options.multiSelect !== false;
        this.fileFilter = options.fileFilter || null; // e.g., ['docx', 'pdf']
    }

    // =========================================================================
    // OPEN/CLOSE
    // =========================================================================

    async open() {
        // Check if already open
        if (document.getElementById(this.overlayId)) {
            console.log('[GDriveBrowser] Already open');
            return;
        }

        // Check electronAPI availability
        if (!window.electronAPI || !window.electronAPI.listDirectory) {
            alert('File system API not available. Please restart the app.');
            return;
        }

        this.render();
        await this.loadFolder(this.currentPath);

        if (typeof log === 'function') {
            log('Opened Google Drive Browser', 'success', 'devtools');
        }
    }

    close() {
        const overlay = document.getElementById(this.overlayId);
        if (overlay) {
            overlay.remove();
        }
        this.selectedItems = [];
        this.pathHistory = [];

        if (typeof log === 'function') {
            log('Closed Google Drive Browser', 'info', 'devtools');
        }
    }

    // =========================================================================
    // RENDER
    // =========================================================================

    render() {
        const overlay = document.createElement('div');
        overlay.id = this.overlayId;
        overlay.className = 'universal-browser-overlay';

        overlay.innerHTML = `
            <div class="universal-browser gdrive-browser">
                <!-- Header -->
                <div class="browser-header">
                    <div class="browser-header-left">
                        <span class="browser-icon">📂</span>
                        <div class="browser-title-group">
                            <h2 class="browser-title">GOOGLE DRIVE BROWSER</h2>
                            <div class="browser-subtitle">Browse files and folders</div>
                        </div>
                    </div>
                    <button class="browser-close-btn" onclick="gdriveBrowser.close()">×</button>
                </div>

                <!-- Toolbar -->
                <div class="browser-toolbar">
                    <input type="text"
                           class="browser-search-box"
                           id="gdriveSearchBox"
                           placeholder="Filter by filename..."
                           onkeyup="gdriveBrowser.filterItems()">
                    <select class="browser-filter-select" id="gdriveFilterSelect" onchange="gdriveBrowser.filterItems()">
                        <option value="">All Files</option>
                        <option value="folder">Folders Only</option>
                        <option value="docx">Word Documents</option>
                        <option value="pdf">PDF Files</option>
                        <option value="xlsx">Excel Files</option>
                        <option value="html">HTML Files</option>
                        <option value="md">Markdown Files</option>
                        <option value="json">JSON Files</option>
                    </select>
                </div>

                <!-- Breadcrumb -->
                <div class="browser-breadcrumb">
                    <div class="breadcrumb-path" id="gdriveBreadcrumb">
                        <span class="breadcrumb-item" onclick="gdriveBrowser.goHome()">🏠 Home</span>
                    </div>
                    <button class="browser-refresh-btn" onclick="gdriveBrowser.refresh()">↻ Refresh</button>
                </div>

                <!-- Content -->
                <div class="browser-content" id="gdriveBrowserContent">
                    <div class="browser-loading">
                        <div class="browser-loading-icon">📂</div>
                        <div class="browser-loading-text">Loading files...</div>
                    </div>
                </div>

                <!-- Footer -->
                <div class="browser-footer">
                    <div class="browser-footer-left">
                        <span class="browser-item-count" id="gdriveItemCount">0 items</span>
                        <span class="browser-selected-count" id="gdriveSelectedCount"></span>
                    </div>
                    <div class="browser-footer-right">
                        <button class="browser-btn browser-btn-secondary" onclick="gdriveBrowser.close()">Cancel</button>
                        <button class="browser-btn browser-btn-primary" id="gdriveAddBtn" onclick="gdriveBrowser.confirmSelection()" disabled>Add to Project</button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(overlay);

        // Close on overlay click
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                this.close();
            }
        });
    }

    // =========================================================================
    // DATA LOADING
    // =========================================================================

    async loadFolder(folderPath) {
        const content = document.getElementById('gdriveBrowserContent');

        content.innerHTML = `
            <div class="browser-loading">
                <div class="browser-loading-icon">📂</div>
                <div class="browser-loading-text">Loading files...</div>
            </div>
        `;

        try {
            const result = await window.electronAPI.listDirectory(folderPath);

            if (!result.success) {
                throw new Error(result.error || 'Failed to load folder');
            }

            this.currentPath = folderPath;
            this.allItems = (result.files || []).map(file => ({
                id: file.path,
                name: file.name,
                type: file.isDirectory ? 'folder' : 'file',
                path: file.path,
                size: file.size,
                date: file.modified,
                extension: file.isDirectory ? '' : this.getExtension(file.name)
            }));

            this.filteredItems = [...this.allItems];
            this.currentPage = 1;
            this.renderItems();
            this.updateBreadcrumb();
            this.updateCounts();

        } catch (error) {
            content.innerHTML = `
                <div class="browser-empty">
                    <div class="browser-empty-icon">❌</div>
                    <div class="browser-empty-text">Failed to load folder</div>
                    <div class="browser-empty-hint">${error.message}</div>
                </div>
            `;
        }
    }

    // =========================================================================
    // RENDERING
    // =========================================================================

    renderItems() {
        const content = document.getElementById('gdriveBrowserContent');
        const items = this.filteredItems;

        if (items.length === 0) {
            content.innerHTML = `
                <div class="browser-empty">
                    <div class="browser-empty-icon">📭</div>
                    <div class="browser-empty-text">No files found</div>
                    <div class="browser-empty-hint">This folder is empty or no files match your filter</div>
                </div>
            `;
            return;
        }

        // Paginate
        const start = 0;
        const end = this.currentPage * this.itemsPerPage;
        const displayItems = items.slice(start, end);
        const hasMore = items.length > end;

        let html = '<ul class="browser-items">';

        displayItems.forEach(item => {
            const isSelected = this.selectedItems.some(s => s.id === item.id);
            const date = item.date ? new Date(item.date).toLocaleDateString() : '';
            const icon = item.type === 'folder' ? '📁' : this.getFileIcon(item.extension);
            const size = item.type === 'file' ? this.formatSize(item.size) : '';

            html += `
                <li class="browser-item ${isSelected ? 'selected' : ''}"
                    onclick="gdriveBrowser.handleItemClick('${this.escapeAttr(item.id)}', '${item.type}')"
                    ondblclick="gdriveBrowser.handleItemDblClick('${this.escapeAttr(item.id)}', '${item.type}')">
                    ${this.multiSelect && item.type === 'file' ? `<input type="checkbox" class="browser-item-checkbox" ${isSelected ? 'checked' : ''} onclick="event.stopPropagation()">` : ''}
                    <span class="browser-item-icon ${item.type}">${icon}</span>
                    <div class="browser-item-info">
                        <div class="browser-item-name">${this.escapeHtml(item.name)}</div>
                        <div class="browser-item-meta">${size}</div>
                    </div>
                    <span class="browser-item-date">${date}</span>
                    <span class="browser-item-arrow">→</span>
                </li>
            `;
        });

        html += '</ul>';

        // Add pagination
        if (hasMore) {
            html += `
                <div class="browser-pagination">
                    <span class="browser-pagination-info">Showing ${displayItems.length} of ${items.length} items</span>
                    <button class="browser-load-more-btn" onclick="gdriveBrowser.loadMore()">Load More</button>
                </div>
            `;
        }

        content.innerHTML = html;
    }

    // =========================================================================
    // INTERACTIONS
    // =========================================================================

    handleItemClick(itemId, itemType) {
        if (itemType === 'folder') {
            // Don't select folders, navigate instead
            return;
        }

        const item = this.filteredItems.find(i => i.id === itemId);
        if (!item) return;

        const existingIndex = this.selectedItems.findIndex(s => s.id === itemId);

        if (existingIndex >= 0) {
            this.selectedItems.splice(existingIndex, 1);
        } else {
            if (this.multiSelect) {
                this.selectedItems.push(item);
            } else {
                this.selectedItems = [item];
            }
        }

        this.renderItems();
        this.updateCounts();
    }

    handleItemDblClick(itemId, itemType) {
        if (itemType === 'folder') {
            this.navigateTo(itemId);
        } else {
            // Open file with default application
            this.openFile(itemId);
        }
    }

    async openFile(filePath) {
        try {
            const result = await window.electronAPI.openFile(filePath);
            if (!result.success) {
                throw new Error(result.error || 'Failed to open file');
            }
            if (typeof log === 'function') {
                log(`Opened file: ${filePath}`, 'success', 'devtools');
            }
        } catch (error) {
            alert('Failed to open file: ' + error.message);
        }
    }

    // =========================================================================
    // NAVIGATION
    // =========================================================================

    navigateTo(folderPath) {
        this.pathHistory.push(this.currentPath);
        this.loadFolder(folderPath);
    }

    goBack() {
        if (this.pathHistory.length > 0) {
            const prevPath = this.pathHistory.pop();
            this.loadFolder(prevPath);
        }
    }

    goHome() {
        this.pathHistory = [];
        document.getElementById('gdriveSearchBox').value = '';
        document.getElementById('gdriveFilterSelect').value = '';
        this.loadFolder(this.rootPath);
    }

    goToPath(path) {
        // Build path history up to this point
        const parts = this.getPathParts(path);
        this.pathHistory = parts.slice(0, -1).map((_, i) =>
            parts.slice(0, i + 1).join('\\')
        );
        this.loadFolder(path);
    }

    refresh() {
        this.loadFolder(this.currentPath);
    }

    loadMore() {
        this.currentPage++;
        this.renderItems();
    }

    // =========================================================================
    // FILTERING
    // =========================================================================

    filterItems() {
        const searchTerm = document.getElementById('gdriveSearchBox').value.toLowerCase();
        const typeFilter = document.getElementById('gdriveFilterSelect').value;

        this.filteredItems = this.allItems.filter(item => {
            // Search filter
            if (searchTerm && !item.name.toLowerCase().includes(searchTerm)) {
                return false;
            }

            // Type filter
            if (typeFilter) {
                if (typeFilter === 'folder') {
                    return item.type === 'folder';
                } else {
                    return item.extension === typeFilter;
                }
            }

            return true;
        });

        this.currentPage = 1;
        this.renderItems();
        this.updateCounts();
    }

    // =========================================================================
    // SELECTION
    // =========================================================================

    confirmSelection() {
        if (this.selectedItems.length === 0) return;

        if (this.onSelect) {
            this.onSelect(this.selectedItems);
        }

        if (typeof log === 'function') {
            log(`Selected ${this.selectedItems.length} files from Google Drive`, 'success', 'devtools');
        }

        this.close();
    }

    getSelection() {
        return this.selectedItems;
    }

    // =========================================================================
    // BREADCRUMB
    // =========================================================================

    updateBreadcrumb() {
        const container = document.getElementById('gdriveBreadcrumb');
        if (!container) return;

        const parts = this.getPathParts(this.currentPath);
        let html = `<span class="breadcrumb-item" onclick="gdriveBrowser.goHome()">🏠 Home</span>`;

        let buildPath = '';
        parts.forEach((part, index) => {
            buildPath += (index === 0 ? '' : '\\') + part;
            const fullPath = buildPath;

            html += `<span class="breadcrumb-separator">></span>`;

            if (index === parts.length - 1) {
                html += `<span class="breadcrumb-current">${this.escapeHtml(this.getDisplayName(part))}</span>`;
            } else {
                html += `<span class="breadcrumb-item" onclick="gdriveBrowser.goToPath('${this.escapeAttr(fullPath)}')">${this.escapeHtml(this.getDisplayName(part))}</span>`;
            }
        });

        container.innerHTML = html;
    }

    getPathParts(path) {
        // Handle Google Drive paths
        return path.split('\\').filter(p => p && p !== 'G:');
    }

    getDisplayName(part) {
        // Clean up path part names
        if (part === 'My Drive') return 'My Drive';
        if (part.startsWith('00 - ')) return part.substring(5);
        return part;
    }

    // =========================================================================
    // UTILITIES
    // =========================================================================

    updateCounts() {
        const countEl = document.getElementById('gdriveItemCount');
        const selectedEl = document.getElementById('gdriveSelectedCount');
        const addBtn = document.getElementById('gdriveAddBtn');

        if (countEl) {
            countEl.textContent = `${this.filteredItems.length} items`;
        }

        if (selectedEl) {
            selectedEl.textContent = this.selectedItems.length > 0
                ? `Selected: ${this.selectedItems.length}`
                : '';
        }

        if (addBtn) {
            addBtn.disabled = this.selectedItems.length === 0;
        }
    }

    getExtension(filename) {
        const parts = filename.split('.');
        return parts.length > 1 ? parts.pop().toLowerCase() : '';
    }

    getFileIcon(ext) {
        const icons = {
            'docx': '📝',
            'doc': '📝',
            'pdf': '📕',
            'xlsx': '📊',
            'xls': '📊',
            'pptx': '📊',
            'html': '🌐',
            'htm': '🌐',
            'md': '📋',
            'txt': '📄',
            'json': '📋',
            'js': '📜',
            'py': '🐍',
            'css': '🎨',
            'png': '🖼️',
            'jpg': '🖼️',
            'jpeg': '🖼️',
            'gif': '🖼️',
            'mp4': '🎬',
            'mp3': '🎵',
            'zip': '📦',
            'rar': '📦'
        };
        return icons[ext] || '📄';
    }

    formatSize(bytes) {
        if (!bytes) return '';
        const units = ['B', 'KB', 'MB', 'GB'];
        let size = bytes;
        let unitIndex = 0;
        while (size >= 1024 && unitIndex < units.length - 1) {
            size /= 1024;
            unitIndex++;
        }
        return `${size.toFixed(1)} ${units[unitIndex]}`;
    }

    escapeHtml(text) {
        if (!text) return '';
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    escapeAttr(text) {
        if (!text) return '';
        return text
            .replace(/\\/g, '\\\\')
            .replace(/'/g, "\\'");
    }
}

// =============================================================================
// GLOBAL INSTANCE
// =============================================================================

let gdriveBrowser = null;

function openGDriveBrowser(options = {}) {
    gdriveBrowser = new GDriveBrowser(options);
    gdriveBrowser.open();
    return gdriveBrowser;
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { GDriveBrowser, openGDriveBrowser };
}
