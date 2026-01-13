/**
 * KB Browser JavaScript - Self-Contained Version
 * Trajanus Command Center
 *
 * Created: January 13, 2026
 * Updated: January 13, 2026 - Made self-contained, added tree view
 *
 * Direct Supabase access - no external dependencies required
 */

// ==================== CONFIGURATION ====================

const KB_CONFIG = {
    url: 'https://iaxtwrswinygwwwdkvok.supabase.co',
    key: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlheHR3cnN3aW55Z3d3d2Rrdm9rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjUyOTc4NjAsImV4cCI6MjA4MDg3Mzg2MH0.JGSdki3TtDiRS7OQrpBDuyN4nxPW1Qc9ImMunnjHFoE',
    debug: true
};

// ==================== STATE ====================

const KBBrowser = {
    sources: [],
    results: [],
    selectedResult: null,
    isLoading: false,
    viewMode: 'tree' // 'tree' or 'search'
};

// ==================== DOM ELEMENTS ====================

const elements = {
    searchInput: () => document.getElementById('search-input'),
    searchBtn: () => document.getElementById('search-btn'),
    sourceFilter: () => document.getElementById('source-filter'),
    sourceStats: () => document.getElementById('source-stats'),
    resultsList: () => document.getElementById('results-list'),
    resultsCount: () => document.getElementById('results-count'),
    detailPanel: () => document.getElementById('detail-panel'),
    detailTitle: () => document.getElementById('detail-title'),
    detailMeta: () => document.getElementById('detail-meta'),
    detailContent: () => document.getElementById('detail-content'),
    closeDetail: () => document.getElementById('close-detail'),
    loadingOverlay: () => document.getElementById('loading-overlay'),
    statSources: () => document.getElementById('stat-sources'),
    statChunks: () => document.getElementById('stat-chunks')
};

// ==================== SUPABASE API ====================

/**
 * Direct Supabase RPC call - no external library needed
 */
async function supabaseRPC(functionName, params = {}) {
    const url = `${KB_CONFIG.url}/rest/v1/rpc/${functionName}`;

    if (KB_CONFIG.debug) {
        console.log('[KB] RPC:', functionName, params);
    }

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'apikey': KB_CONFIG.key,
                'Authorization': `Bearer ${KB_CONFIG.key}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Supabase error ${response.status}: ${errorText}`);
        }

        const data = await response.json();
        if (KB_CONFIG.debug) {
            console.log('[KB] Response:', Array.isArray(data) ? `${data.length} records` : 'object');
        }
        return { data, error: null };

    } catch (error) {
        console.error('[KB] RPC Error:', error.message);
        return { data: null, error: error.message };
    }
}

// ==================== LOADING STATE ====================

function showLoading(message = 'Loading...') {
    const overlay = elements.loadingOverlay();
    if (overlay) {
        const text = overlay.querySelector('.loading-text');
        if (text) text.textContent = message;
        overlay.classList.add('visible');
    }
    KBBrowser.isLoading = true;
}

function hideLoading() {
    const overlay = elements.loadingOverlay();
    if (overlay) {
        overlay.classList.remove('visible');
    }
    KBBrowser.isLoading = false;
}

// ==================== SOURCES ====================

/**
 * Load all knowledge sources and display as tree
 */
async function loadSources() {
    console.log('[KB Browser] Loading sources...');
    showLoading('Loading Knowledge Base...');

    try {
        const result = await supabaseRPC('list_knowledge_sources', {
            filter_source: null
        });

        hideLoading();

        if (result.error || !result.data) {
            console.error('[KB Browser] Failed to load sources:', result.error);
            elements.sourceStats().innerHTML = '<span class="stat-item" style="color: #f87171;">Failed to load sources</span>';
            showError('Failed to load sources: ' + (result.error || 'Unknown error'));
            return;
        }

        KBBrowser.sources = result.data;
        console.log('[KB Browser] Loaded', KBBrowser.sources.length, 'sources');

        // Populate dropdown
        populateSourceDropdown();

        // Update stats
        const totalChunks = KBBrowser.sources.reduce((sum, s) => sum + (s.chunk_count || 0), 0);
        elements.statSources().textContent = KBBrowser.sources.length.toLocaleString();
        elements.statChunks().textContent = totalChunks.toLocaleString();
        elements.sourceStats().innerHTML = `<span class="stat-item">${KBBrowser.sources.length} sources loaded</span>`;

        // Display tree view
        renderSourceTree();

    } catch (error) {
        hideLoading();
        console.error('[KB Browser] Error loading sources:', error);
        showError('Error: ' + error.message);
    }
}

/**
 * Populate the source filter dropdown
 */
function populateSourceDropdown() {
    const select = elements.sourceFilter();
    select.innerHTML = '<option value="">All Sources</option>';

    // Sort by chunk count descending
    const sortedSources = [...KBBrowser.sources].sort((a, b) => b.chunk_count - a.chunk_count);

    sortedSources.forEach(source => {
        const option = document.createElement('option');
        option.value = source.source;
        option.textContent = `${source.source} (${source.chunk_count.toLocaleString()})`;
        select.appendChild(option);
    });
}

// ==================== TREE VIEW ====================

/**
 * Get icon for source type
 */
function getSourceIcon(sourceName) {
    const name = sourceName.toLowerCase();
    if (name.includes('youtube')) return '🎬';
    if (name.includes('traffic')) return '🚧';
    if (name.includes('langchain') || name.includes('tutorial')) return '📚';
    if (name.includes('claude') || name.includes('ai')) return '🤖';
    if (name.includes('session') || name.includes('history')) return '📝';
    if (name.includes('protocol')) return '📋';
    if (name.includes('office') || name.includes('ms-')) return '📊';
    if (name.includes('research')) return '🔬';
    return '📁';
}

/**
 * Get category for source
 */
function getSourceCategory(sourceName) {
    const name = sourceName.toLowerCase();
    if (name.includes('youtube') || name.includes('video')) return 'Videos';
    if (name.includes('traffic') || name.includes('construction')) return 'Project Documents';
    if (name.includes('langchain') || name.includes('tutorial') || name.includes('guide')) return 'Tutorials';
    if (name.includes('claude') || name.includes('ai') || name.includes('agent')) return 'AI & Agents';
    if (name.includes('session') || name.includes('history') || name.includes('eos')) return 'Session History';
    if (name.includes('protocol') || name.includes('procedure')) return 'Protocols';
    return 'Other';
}

/**
 * Render sources as a categorized tree
 */
function renderSourceTree() {
    const container = elements.resultsList();
    const countEl = elements.resultsCount();

    // Group sources by category
    const categories = {};
    KBBrowser.sources.forEach(source => {
        const category = getSourceCategory(source.source);
        if (!categories[category]) {
            categories[category] = [];
        }
        categories[category].push(source);
    });

    // Sort categories by total chunks
    const sortedCategories = Object.entries(categories).sort((a, b) => {
        const aTotal = a[1].reduce((sum, s) => sum + s.chunk_count, 0);
        const bTotal = b[1].reduce((sum, s) => sum + s.chunk_count, 0);
        return bTotal - aTotal;
    });

    const totalChunks = KBBrowser.sources.reduce((sum, s) => sum + s.chunk_count, 0);
    countEl.textContent = `${KBBrowser.sources.length} sources • ${totalChunks.toLocaleString()} chunks`;

    let html = '<div class="source-tree">';

    sortedCategories.forEach(([category, sources]) => {
        const categoryTotal = sources.reduce((sum, s) => sum + s.chunk_count, 0);

        html += `
            <div class="tree-category">
                <div class="category-header" onclick="toggleCategory(this)">
                    <span class="category-toggle">▼</span>
                    <span class="category-name">${escapeHtml(category)}</span>
                    <span class="category-count">${sources.length} sources • ${categoryTotal.toLocaleString()} chunks</span>
                </div>
                <div class="category-items">
        `;

        // Sort sources within category by chunk count
        sources.sort((a, b) => b.chunk_count - a.chunk_count);

        sources.forEach(source => {
            const icon = getSourceIcon(source.source);
            html += `
                <div class="tree-item" onclick="selectSource('${escapeHtml(source.source)}')" data-source="${escapeHtml(source.source)}">
                    <span class="item-icon">${icon}</span>
                    <span class="item-name">${escapeHtml(source.source)}</span>
                    <span class="item-stats">
                        <span class="item-chunks">${source.chunk_count.toLocaleString()} chunks</span>
                        <span class="item-urls">${source.url_count} docs</span>
                    </span>
                </div>
            `;
        });

        html += `
                </div>
            </div>
        `;
    });

    html += '</div>';

    container.innerHTML = html;
    KBBrowser.viewMode = 'tree';
}

/**
 * Toggle category expansion
 */
function toggleCategory(header) {
    const category = header.parentElement;
    const toggle = header.querySelector('.category-toggle');
    const items = category.querySelector('.category-items');

    if (items.style.display === 'none') {
        items.style.display = 'block';
        toggle.textContent = '▼';
    } else {
        items.style.display = 'none';
        toggle.textContent = '▶';
    }
}

/**
 * Select a source from the tree and search it
 */
function selectSource(sourceName) {
    // Update dropdown
    elements.sourceFilter().value = sourceName;

    // Update stats
    const source = KBBrowser.sources.find(s => s.source === sourceName);
    if (source) {
        elements.sourceStats().innerHTML = `
            <span class="stat-item">${source.chunk_count.toLocaleString()} chunks</span>
            <span class="stat-item">${source.url_count} documents</span>
        `;
    }

    // Highlight selected item
    document.querySelectorAll('.tree-item').forEach(item => {
        item.classList.toggle('selected', item.dataset.source === sourceName);
    });

    // Show source details in detail panel
    showSourceDetail(source);
}

/**
 * Show source details in the detail panel
 */
function showSourceDetail(source) {
    if (!source) return;

    elements.detailTitle().textContent = source.source;
    elements.detailMeta().innerHTML = `
        <span class="meta-item"><strong>Chunks:</strong> ${source.chunk_count.toLocaleString()}</span>
        <span class="meta-item"><strong>Documents:</strong> ${source.url_count}</span>
        <span class="meta-item"><strong>Last Updated:</strong> ${new Date(source.latest_update).toLocaleDateString()}</span>
    `;

    elements.detailContent().innerHTML = `
        <div class="source-detail-content">
            <p>This source contains <strong>${source.chunk_count.toLocaleString()}</strong> searchable chunks from <strong>${source.url_count}</strong> documents.</p>
            <p style="margin-top: 16px;">Use the search box to find specific content within this source, or click "Search" to browse all documents.</p>
            <button class="btn-primary" onclick="searchSourceContent('${escapeHtml(source.source)}')" style="margin-top: 16px;">
                Browse All Content
            </button>
        </div>
    `;
}

/**
 * Search content from a specific source
 */
async function searchSourceContent(sourceName) {
    elements.sourceFilter().value = sourceName;
    elements.searchInput().value = '';
    await searchKB();
}

// ==================== SEARCH ====================

/**
 * Get the selected search type
 */
function getSearchType() {
    const selected = document.querySelector('input[name="search-type"]:checked');
    return selected ? selected.value : 'text';
}

/**
 * Perform search
 */
async function searchKB() {
    const query = elements.searchInput().value.trim();
    const source = elements.sourceFilter().value || null;
    const searchType = getSearchType();

    // If no query but source selected, browse that source
    if (!query && source) {
        return browseSource(source);
    }

    if (!query) {
        alert('Please enter a search term or select a source to browse');
        return;
    }

    console.log('[KB Browser] Searching:', { query, source, searchType });
    showLoading('Searching...');

    try {
        let result;

        if (searchType === 'semantic') {
            // Note: Semantic search requires embedding - show message
            alert('Semantic search requires OpenAI API key. Using text search instead.');
            result = await supabaseRPC('search_by_text', {
                search_query: query,
                filter_source: source || 'Session History',
                match_count: 20
            });
        } else {
            // Text search - use source filter for performance
            const effectiveSource = source || 'Session History';
            result = await supabaseRPC('search_by_text', {
                search_query: query,
                filter_source: effectiveSource,
                match_count: 20
            });

            if (!source) {
                console.warn('[KB Browser] No source filter selected, using Session History');
            }
        }

        hideLoading();

        if (result.error) {
            console.error('[KB Browser] Search failed:', result.error);
            showError('Search failed: ' + result.error);
            return;
        }

        KBBrowser.results = result.data || [];
        console.log('[KB Browser] Found', KBBrowser.results.length, 'results');

        renderSearchResults();

    } catch (error) {
        hideLoading();
        console.error('[KB Browser] Search error:', error);
        showError('Search error: ' + error.message);
    }
}

/**
 * Browse all content from a source
 */
async function browseSource(sourceName) {
    console.log('[KB Browser] Browsing source:', sourceName);
    showLoading('Loading documents...');

    try {
        // Get sample content from the source
        const result = await supabaseRPC('search_by_text', {
            search_query: 'the',  // Common word to get results
            filter_source: sourceName,
            match_count: 20
        });

        hideLoading();

        if (result.error) {
            showError('Failed to load: ' + result.error);
            return;
        }

        KBBrowser.results = result.data || [];
        renderSearchResults();

    } catch (error) {
        hideLoading();
        showError('Error: ' + error.message);
    }
}

/**
 * Show error message in results
 */
function showError(message) {
    elements.resultsList().innerHTML = `
        <div class="empty-state">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#f87171" stroke-width="1">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 8v4M12 16h.01"/>
            </svg>
            <p style="color: #f87171;">${escapeHtml(message)}</p>
            <button class="btn-secondary" onclick="loadSources()" style="margin-top: 16px;">
                Reload Sources
            </button>
        </div>
    `;
    elements.resultsCount().textContent = 'Error';
}

// ==================== RENDER RESULTS ====================

/**
 * Render search results
 */
function renderSearchResults() {
    const container = elements.resultsList();
    const countEl = elements.resultsCount();

    if (KBBrowser.results.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                    <circle cx="11" cy="11" r="8"/>
                    <path d="M21 21l-4.35-4.35"/>
                </svg>
                <p>No results found. Try different keywords or source filter.</p>
                <button class="btn-secondary" onclick="renderSourceTree()" style="margin-top: 16px;">
                    Back to Sources
                </button>
            </div>
        `;
        countEl.textContent = '0 results';
        return;
    }

    countEl.textContent = `${KBBrowser.results.length} results`;
    KBBrowser.viewMode = 'search';

    let html = `
        <div class="results-actions">
            <button class="btn-secondary" onclick="renderSourceTree()">← Back to Sources</button>
        </div>
    `;

    html += KBBrowser.results.map((result, index) => {
        const title = result.title || 'Untitled';
        const source = result.metadata?.source || 'Unknown';
        const score = result.similarity
            ? (result.similarity * 100).toFixed(1) + '% match'
            : result.rank
            ? 'Rank: ' + result.rank.toFixed(4)
            : '';
        const snippet = result.summary || result.content?.substring(0, 200) || '';

        return `
            <div class="result-card" data-index="${index}" onclick="viewDocument(${index})">
                <div class="result-title">${escapeHtml(title)}</div>
                <div class="result-meta">
                    <span class="result-source">${escapeHtml(source)}</span>
                    ${score ? `<span class="result-score">${score}</span>` : ''}
                </div>
                <div class="result-snippet">${escapeHtml(snippet)}</div>
            </div>
        `;
    }).join('');

    container.innerHTML = html;
}

// ==================== VIEW DOCUMENT ====================

/**
 * Display selected document in detail panel
 */
function viewDocument(index) {
    const result = KBBrowser.results[index];
    if (!result) return;

    KBBrowser.selectedResult = result;

    // Update active state
    document.querySelectorAll('.result-card').forEach((card, i) => {
        card.classList.toggle('active', i === index);
    });

    // Update detail panel
    elements.detailTitle().textContent = result.title || 'Untitled';

    const source = result.metadata?.source || 'Unknown';
    const url = result.url || '';
    const chunk = result.chunk_number || 1;

    elements.detailMeta().innerHTML = `
        <span class="meta-item"><strong>Source:</strong> ${escapeHtml(source)}</span>
        <span class="meta-item"><strong>Chunk:</strong> ${chunk}</span>
        ${url ? `<span class="meta-item"><strong>URL:</strong> ${escapeHtml(url.substring(0, 50))}...</span>` : ''}
    `;

    // Format content
    const content = result.content || result.summary || 'No content available';
    elements.detailContent().innerHTML = `<div class="content-text">${escapeHtml(content)}</div>`;

    console.log('[KB Browser] Viewing document:', result.title);
}

/**
 * Close the detail panel
 */
function closeDetail() {
    KBBrowser.selectedResult = null;

    document.querySelectorAll('.result-card').forEach(card => {
        card.classList.remove('active');
    });

    elements.detailTitle().textContent = 'Select a Document';
    elements.detailMeta().innerHTML = '<span class="meta-item">No document selected</span>';
    elements.detailContent().innerHTML = '<p class="placeholder-text">Click on a source or search result to view details here.</p>';
}

// ==================== UTILITIES ====================

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ==================== EVENT HANDLERS ====================

function initEventHandlers() {
    // Search button click
    elements.searchBtn().addEventListener('click', searchKB);

    // Enter key in search input
    elements.searchInput().addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchKB();
        }
    });

    // Source filter change
    elements.sourceFilter().addEventListener('change', () => {
        const selected = elements.sourceFilter().value;
        if (selected) {
            const source = KBBrowser.sources.find(s => s.source === selected);
            if (source) {
                elements.sourceStats().innerHTML = `
                    <span class="stat-item">${source.chunk_count.toLocaleString()} chunks</span>
                    <span class="stat-item">${source.url_count} docs</span>
                `;
                showSourceDetail(source);
            }
        } else {
            const total = KBBrowser.sources.reduce((sum, s) => sum + (s.chunk_count || 0), 0);
            elements.sourceStats().innerHTML = `<span class="stat-item">${KBBrowser.sources.length} sources, ${total.toLocaleString()} total</span>`;
        }
    });

    // Close detail button
    elements.closeDetail().addEventListener('click', closeDetail);
}

// ==================== INITIALIZATION ====================

async function initKBBrowser() {
    console.log('[KB Browser] Initializing (self-contained mode)...');
    console.log('[KB Browser] Supabase URL:', KB_CONFIG.url);

    initEventHandlers();

    // Load sources immediately on page load
    await loadSources();

    console.log('[KB Browser] Ready');
}

// Run on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initKBBrowser);
} else {
    initKBBrowser();
}

// Make functions globally available
window.searchKB = searchKB;
window.viewDocument = viewDocument;
window.closeDetail = closeDetail;
window.loadSources = loadSources;
window.toggleCategory = toggleCategory;
window.selectSource = selectSource;
window.searchSourceContent = searchSourceContent;
window.renderSourceTree = renderSourceTree;
