/**
 * KB Browser JavaScript
 * Trajanus Command Center
 *
 * Created: January 13, 2026
 * Provides search and document viewing functionality for the Knowledge Base.
 */

// ==================== STATE ====================

const KBBrowser = {
    sources: [],
    results: [],
    selectedResult: null,
    isLoading: false
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

// ==================== LOADING STATE ====================

function showLoading(message = 'Searching...') {
    const overlay = elements.loadingOverlay();
    const text = overlay.querySelector('.loading-text');
    if (text) text.textContent = message;
    overlay.classList.add('visible');
    KBBrowser.isLoading = true;
}

function hideLoading() {
    elements.loadingOverlay().classList.remove('visible');
    KBBrowser.isLoading = false;
}

// ==================== SOURCES ====================

/**
 * Load all knowledge sources and populate the filter dropdown
 */
async function loadSources() {
    console.log('[KB Browser] Loading sources...');

    try {
        const result = await window.KBHandlers.listKnowledgeSources({});

        if (!result.success || !result.data) {
            console.error('[KB Browser] Failed to load sources:', result.error);
            elements.sourceStats().innerHTML = '<span class="stat-item">Failed to load sources</span>';
            return;
        }

        KBBrowser.sources = result.data;
        console.log('[KB Browser] Loaded', KBBrowser.sources.length, 'sources');

        // Populate dropdown
        const select = elements.sourceFilter();
        select.innerHTML = '<option value="">All Sources</option>';

        KBBrowser.sources.forEach(source => {
            const option = document.createElement('option');
            option.value = source.source;
            option.textContent = `${source.source} (${source.chunk_count.toLocaleString()})`;
            select.appendChild(option);
        });

        // Update stats
        const totalChunks = KBBrowser.sources.reduce((sum, s) => sum + (s.chunk_count || 0), 0);
        elements.statSources().textContent = KBBrowser.sources.length.toLocaleString();
        elements.statChunks().textContent = totalChunks.toLocaleString();
        elements.sourceStats().innerHTML = `<span class="stat-item">${KBBrowser.sources.length} sources loaded</span>`;

    } catch (error) {
        console.error('[KB Browser] Error loading sources:', error);
        elements.sourceStats().innerHTML = '<span class="stat-item">Error loading sources</span>';
    }
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
 * Perform search using selected method
 */
async function searchKB() {
    const query = elements.searchInput().value.trim();
    if (!query) {
        alert('Please enter a search term');
        return;
    }

    const source = elements.sourceFilter().value || null;
    const searchType = getSearchType();

    console.log('[KB Browser] Searching:', { query, source, searchType });
    showLoading('Searching...');

    try {
        let result;

        if (searchType === 'semantic') {
            result = await window.KBHandlers.searchKnowledgeBase({
                query: query,
                threshold: 0.3,
                count: 20
            });
        } else {
            // Text search - always use source filter for performance
            const effectiveSource = source || 'Session History'; // Default to smaller dataset
            result = await window.KBHandlers.searchByText({
                query: query,
                source: effectiveSource,
                count: 20
            });

            // Show warning if no source selected
            if (!source) {
                console.warn('[KB Browser] No source filter selected, defaulting to Session History');
            }
        }

        hideLoading();

        if (!result.success) {
            console.error('[KB Browser] Search failed:', result.error);
            showError('Search failed: ' + result.error);
            return;
        }

        KBBrowser.results = result.data || [];
        console.log('[KB Browser] Found', KBBrowser.results.length, 'results');

        renderResults();

    } catch (error) {
        hideLoading();
        console.error('[KB Browser] Search error:', error);
        showError('Search error: ' + error.message);
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
            <p style="color: #f87171;">${message}</p>
        </div>
    `;
    elements.resultsCount().textContent = 'Error';
}

// ==================== RENDER RESULTS ====================

/**
 * Render search results in the list
 */
function renderResults() {
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
            </div>
        `;
        countEl.textContent = '0 results';
        return;
    }

    countEl.textContent = `${KBBrowser.results.length} results`;

    container.innerHTML = KBBrowser.results.map((result, index) => {
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
    elements.detailContent().innerHTML = '<p class="placeholder-text">Click on a search result to view its full content here.</p>';
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

    // Source filter change - update stats
    elements.sourceFilter().addEventListener('change', () => {
        const selected = elements.sourceFilter().value;
        if (selected) {
            const source = KBBrowser.sources.find(s => s.source === selected);
            if (source) {
                elements.sourceStats().innerHTML = `
                    <span class="stat-item">${source.chunk_count.toLocaleString()} chunks</span>
                    <span class="stat-item">${source.url_count} URLs</span>
                `;
            }
        } else {
            const total = KBBrowser.sources.reduce((sum, s) => sum + (s.chunk_count || 0), 0);
            elements.sourceStats().innerHTML = `<span class="stat-item">${KBBrowser.sources.length} sources, ${total.toLocaleString()} total chunks</span>`;
        }
    });

    // Close detail button
    elements.closeDetail().addEventListener('click', closeDetail);
}

// ==================== INITIALIZATION ====================

async function initKBBrowser() {
    console.log('[KB Browser] Initializing...');

    // Wait for KB client to be ready
    if (!window.KB) {
        console.error('[KB Browser] KB client not initialized. Make sure supabase-client.js and main.js are loaded.');
        elements.sourceStats().innerHTML = '<span class="stat-item" style="color: #f87171;">KB client not loaded</span>';
        return;
    }

    initEventHandlers();
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
