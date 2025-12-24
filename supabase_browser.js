/**
 * Supabase Browser for Trajanus Command Center
 * Implements UniversalBrowser interface for Supabase knowledge base
 * Created: 2025-12-15
 */

// =============================================================================
// SUPABASE BROWSER CLASS
// =============================================================================

class SupabaseBrowser {
    constructor(options = {}) {
        this.type = 'supabase';
        this.overlayId = 'supabaseBrowserOverlay';
        this.currentCategory = '';
        this.selectedItems = [];
        this.allItems = [];
        this.filteredItems = [];
        this.itemsPerPage = 50;
        this.currentPage = 1;
        this.onSelect = options.onSelect || null;
        this.multiSelect = options.multiSelect !== false;
    }

    // =========================================================================
    // OPEN/CLOSE
    // =========================================================================

    async open() {
        // Check if already open
        if (document.getElementById(this.overlayId)) {
            console.log('[SupabaseBrowser] Already open');
            return;
        }

        // Check KB API availability
        if (!window.kb) {
            alert('Knowledge Base API not available. Please restart the app.');
            return;
        }

        this.render();
        await this.loadItems();
        await this.loadCategories();

        if (typeof log === 'function') {
            log('Opened Supabase Browser', 'success', 'devtools');
        }
    }

    close() {
        const overlay = document.getElementById(this.overlayId);
        if (overlay) {
            overlay.remove();
        }
        this.selectedItems = [];

        if (typeof log === 'function') {
            log('Closed Supabase Browser', 'info', 'devtools');
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
            <div class="universal-browser supabase-browser">
                <!-- Header -->
                <div class="browser-header">
                    <div class="browser-header-left">
                        <span class="browser-icon">🗄️</span>
                        <div class="browser-title-group">
                            <h2 class="browser-title">SUPABASE KNOWLEDGE BASE</h2>
                            <div class="browser-subtitle">Browse documents in Supabase database</div>
                        </div>
                    </div>
                    <button class="browser-close-btn" onclick="supabaseBrowser.close()">×</button>
                </div>

                <!-- Toolbar -->
                <div class="browser-toolbar">
                    <input type="text"
                           class="browser-search-box"
                           id="supabaseSearchBox"
                           placeholder="Search documents by title, content, or keywords..."
                           onkeypress="if(event.key==='Enter') supabaseBrowser.search()">
                    <select class="browser-filter-select" id="supabaseFilterSelect" onchange="supabaseBrowser.filterByCategory()">
                        <option value="">All Categories</option>
                    </select>
                </div>

                <!-- Breadcrumb -->
                <div class="browser-breadcrumb">
                    <div class="breadcrumb-path">
                        <span class="breadcrumb-item" onclick="supabaseBrowser.goHome()">🏠 Home</span>
                        <span class="breadcrumb-separator">></span>
                        <span class="breadcrumb-current" id="supabaseBreadcrumb">All Documents</span>
                    </div>
                    <button class="browser-refresh-btn" onclick="supabaseBrowser.refresh()">↻ Refresh</button>
                </div>

                <!-- Content -->
                <div class="browser-content" id="supabaseBrowserContent">
                    <div class="browser-loading">
                        <div class="browser-loading-icon">📚</div>
                        <div class="browser-loading-text">Loading documents...</div>
                    </div>
                </div>

                <!-- Footer -->
                <div class="browser-footer">
                    <div class="browser-footer-left">
                        <span class="browser-item-count" id="supabaseItemCount">0 items</span>
                        <span class="browser-selected-count" id="supabaseSelectedCount"></span>
                    </div>
                    <div class="browser-footer-right">
                        <button class="browser-btn browser-btn-secondary" onclick="supabaseBrowser.close()">Cancel</button>
                        <button class="browser-btn browser-btn-primary" id="supabaseAddBtn" onclick="supabaseBrowser.confirmSelection()" disabled>Add to Project</button>
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

    async loadItems() {
        const content = document.getElementById('supabaseBrowserContent');

        try {
            const result = await window.kb.listSources();

            if (!result.success) {
                throw new Error(result.error || 'Failed to load documents');
            }

            this.allItems = (result.data || []).map(item => ({
                id: item.url,
                name: item.title || item.url || 'Untitled',
                type: 'file',
                category: item.metadata?.source || 'Unknown',
                date: item.created_at,
                summary: item.summary || '',
                url: item.url,
                metadata: item.metadata
            }));

            this.filteredItems = [...this.allItems];
            this.renderItems();
            this.updateCounts();

        } catch (error) {
            content.innerHTML = `
                <div class="browser-empty">
                    <div class="browser-empty-icon">❌</div>
                    <div class="browser-empty-text">Failed to load documents</div>
                    <div class="browser-empty-hint">${error.message}</div>
                </div>
            `;
        }
    }

    async loadCategories() {
        try {
            const result = await window.kb.getCategories();

            if (result.success && result.data) {
                const select = document.getElementById('supabaseFilterSelect');
                result.data.forEach(cat => {
                    const option = document.createElement('option');
                    option.value = cat.source;
                    option.textContent = `${cat.source} (${cat.count})`;
                    select.appendChild(option);
                });
            }
        } catch (error) {
            console.error('[SupabaseBrowser] Error loading categories:', error);
        }
    }

    // =========================================================================
    // RENDERING
    // =========================================================================

    renderItems() {
        const content = document.getElementById('supabaseBrowserContent');
        const items = this.filteredItems;

        if (items.length === 0) {
            content.innerHTML = `
                <div class="browser-empty">
                    <div class="browser-empty-icon">📭</div>
                    <div class="browser-empty-text">No documents found</div>
                    <div class="browser-empty-hint">Try a different search term or category</div>
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
            const icon = item.type === 'folder' ? '📁' : '📄';

            html += `
                <li class="browser-item ${isSelected ? 'selected' : ''}"
                    onclick="supabaseBrowser.toggleItem('${item.id}')"
                    ondblclick="supabaseBrowser.viewItem('${encodeURIComponent(item.url)}')">
                    ${this.multiSelect ? `<input type="checkbox" class="browser-item-checkbox" ${isSelected ? 'checked' : ''} onclick="event.stopPropagation()">` : ''}
                    <span class="browser-item-icon ${item.type}">${icon}</span>
                    <div class="browser-item-info">
                        <div class="browser-item-name">${this.escapeHtml(item.name)}</div>
                        <div class="browser-item-meta">${item.category}</div>
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
                    <button class="browser-load-more-btn" onclick="supabaseBrowser.loadMore()">Load More</button>
                </div>
            `;
        }

        content.innerHTML = html;
    }

    // =========================================================================
    // INTERACTIONS
    // =========================================================================

    toggleItem(itemId) {
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

    async viewItem(encodedUrl) {
        const url = decodeURIComponent(encodedUrl);

        try {
            const result = await window.kb.getByUrl(url);

            if (!result.success) {
                throw new Error(result.error || 'Failed to load document');
            }

            const chunks = result.data || [];
            if (chunks.length === 0) {
                throw new Error('Document has no content');
            }

            const title = chunks[0]?.title || url;
            const content = chunks.map(c => c.content).join('\n\n---\n\n');

            // Show in a viewer
            this.showDocumentViewer(title, content, chunks.length);

        } catch (error) {
            alert('Failed to load document: ' + error.message);
        }
    }

    showDocumentViewer(title, content, chunkCount) {
        const viewer = document.createElement('div');
        viewer.id = 'supabaseDocViewer';
        viewer.className = 'universal-browser-overlay';
        viewer.style.zIndex = '10001';

        viewer.innerHTML = `
            <div style="background: #1a1a1a; border: 2px solid #9B7E52; border-radius: 8px; width: 90%; max-width: 900px; height: 85%; display: flex; flex-direction: column; box-shadow: 0 10px 40px rgba(0,0,0,0.5);">
                <div style="background: linear-gradient(180deg, #9B7E52 0%, #7B6142 100%); padding: 20px; border-radius: 6px 6px 0 0; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <h2 style="margin: 0; color: #fff; font-size: 1.3rem; font-weight: 600;">${this.escapeHtml(title)}</h2>
                        <div style="color: rgba(255,255,255,0.8); font-size: 0.85rem; margin-top: 5px;">${chunkCount} chunk(s)</div>
                    </div>
                    <button onclick="document.getElementById('supabaseDocViewer').remove()" style="background: rgba(255,255,255,0.2); border: none; color: #fff; font-size: 1.8rem; width: 40px; height: 40px; border-radius: 4px; cursor: pointer; line-height: 1;">×</button>
                </div>
                <div style="flex: 1; overflow-y: auto; padding: 25px;">
                    <pre style="white-space: pre-wrap; word-wrap: break-word; color: #ddd; font-family: inherit; font-size: 0.95rem; line-height: 1.6; margin: 0;">${this.escapeHtml(content)}</pre>
                </div>
                <div style="padding: 15px 20px; background: rgba(0,0,0,0.3); border-top: 1px solid rgba(155,126,82,0.3); display: flex; justify-content: flex-end; gap: 10px; border-radius: 0 0 6px 6px;">
                    <button class="browser-btn browser-btn-secondary" onclick="document.getElementById('supabaseDocViewer').remove()">Close</button>
                </div>
            </div>
        `;

        document.body.appendChild(viewer);

        viewer.addEventListener('click', (e) => {
            if (e.target === viewer) {
                viewer.remove();
            }
        });
    }

    // =========================================================================
    // SEARCH & FILTER
    // =========================================================================

    async search() {
        const query = document.getElementById('supabaseSearchBox').value.trim();
        const category = document.getElementById('supabaseFilterSelect').value;
        const content = document.getElementById('supabaseBrowserContent');

        if (!query && !category) {
            this.filteredItems = [...this.allItems];
            this.renderItems();
            this.updateCounts();
            this.updateBreadcrumb('All Documents');
            return;
        }

        content.innerHTML = `
            <div class="browser-loading">
                <div class="browser-loading-icon">🔍</div>
                <div class="browser-loading-text">Searching...</div>
            </div>
        `;

        try {
            let result;

            if (query) {
                result = await window.kb.search(query, {
                    limit: 100,
                    source: category || undefined
                });
            } else if (category) {
                result = await window.kb.browseBySource(category, 100);
            }

            if (!result.success) {
                throw new Error(result.error || 'Search failed');
            }

            this.filteredItems = (result.data || []).map(item => ({
                id: item.url,
                name: item.title || item.url || 'Untitled',
                type: 'file',
                category: item.metadata?.source || 'Unknown',
                date: item.created_at,
                summary: item.summary || '',
                url: item.url,
                metadata: item.metadata
            }));

            this.currentPage = 1;
            this.renderItems();
            this.updateCounts();
            this.updateBreadcrumb(query ? `Search: "${query}"` : category);

        } catch (error) {
            content.innerHTML = `
                <div class="browser-empty">
                    <div class="browser-empty-icon">❌</div>
                    <div class="browser-empty-text">Search failed</div>
                    <div class="browser-empty-hint">${error.message}</div>
                </div>
            `;
        }
    }

    filterByCategory() {
        this.search();
    }

    // =========================================================================
    // NAVIGATION
    // =========================================================================

    goHome() {
        document.getElementById('supabaseSearchBox').value = '';
        document.getElementById('supabaseFilterSelect').value = '';
        this.filteredItems = [...this.allItems];
        this.currentPage = 1;
        this.renderItems();
        this.updateCounts();
        this.updateBreadcrumb('All Documents');
    }

    refresh() {
        this.loadItems();
    }

    loadMore() {
        this.currentPage++;
        this.renderItems();
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
            log(`Selected ${this.selectedItems.length} items from Supabase`, 'success', 'devtools');
        }

        this.close();
    }

    getSelection() {
        return this.selectedItems;
    }

    // =========================================================================
    // UTILITIES
    // =========================================================================

    updateCounts() {
        const countEl = document.getElementById('supabaseItemCount');
        const selectedEl = document.getElementById('supabaseSelectedCount');
        const addBtn = document.getElementById('supabaseAddBtn');

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

    updateBreadcrumb(text) {
        const el = document.getElementById('supabaseBreadcrumb');
        if (el) {
            el.textContent = text;
        }
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
}

// =============================================================================
// GLOBAL INSTANCE
// =============================================================================

let supabaseBrowser = null;

function openSupabaseBrowser(options = {}) {
    supabaseBrowser = new SupabaseBrowser(options);
    supabaseBrowser.open();
    return supabaseBrowser;
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SupabaseBrowser, openSupabaseBrowser };
}
