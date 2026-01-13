/**
 * Main JavaScript Entry Point
 * Trajanus Command Center
 *
 * Created: January 13, 2026
 * Project: Trajanus Command Center (Tauri 2.0)
 *
 * This file initializes the Knowledge Base client and provides
 * global access to Supabase RPC functions.
 *
 * Usage in HTML:
 *   <script src="supabase-client.js"></script>
 *   <script src="main.js"></script>
 *
 *   // Then in your code:
 *   const results = await window.KB.searchByText('query', 'Session History');
 */

// ==================== CONFIGURATION ====================

// Supabase credentials - same as used in team_feedback
const KB_CONFIG = {
    url: 'https://iaxtwrswinygwwwdkvok.supabase.co',
    // Using the same anon key as team_feedback
    key: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlheHR3cnN3aW55Z3d3d2Rrdm9rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjUyOTc4NjAsImV4cCI6MjA4MDg3Mzg2MH0.JGSdki3TtDiRS7OQrpBDuyN4nxPW1Qc9ImMunnjHFoE',
    // OpenAI key - set this for semantic search (optional)
    openaiKey: null,
    // Enable debug logging
    debug: true
};

// ==================== INITIALIZATION ====================

/**
 * Initialize the Knowledge Base client
 * Called automatically when script loads
 */
function initKnowledgeBase() {
    console.log('[Main] Initializing Knowledge Base client...');

    // Check if KnowledgeBaseClient is available
    if (typeof KnowledgeBaseClient === 'undefined') {
        console.error('[Main] KnowledgeBaseClient not found. Make sure supabase-client.js is loaded first.');
        return null;
    }

    // Create and configure client
    const kb = new KnowledgeBaseClient({
        url: KB_CONFIG.url,
        debug: KB_CONFIG.debug
    });

    // Set API keys
    kb.setKeys(KB_CONFIG.key, KB_CONFIG.openaiKey);

    console.log('[Main] Knowledge Base client ready');
    return kb;
}

// ==================== GLOBAL API ====================

/**
 * Global Knowledge Base instance
 * Access via window.KB
 */
window.KB = null;

/**
 * IPC-style handlers for use by frontend components
 * These mirror the pattern that would be used with Tauri invoke()
 */
window.KBHandlers = {
    /**
     * Search knowledge base using semantic vector search
     * @param {Object} params - { query, threshold?, count? }
     */
    async searchKnowledgeBase(params) {
        if (!window.KB) {
            return { success: false, error: 'Knowledge base not initialized' };
        }

        try {
            const result = await window.KB.searchKnowledgeBase(
                params.query,
                params.threshold || 0.4,
                params.count || 10
            );

            return {
                success: !result.error,
                data: result.data,
                error: result.error
            };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    /**
     * Search by text (full-text search)
     * IMPORTANT: Use filterSource for better performance!
     * @param {Object} params - { query, source?, count? }
     */
    async searchByText(params) {
        if (!window.KB) {
            return { success: false, error: 'Knowledge base not initialized' };
        }

        try {
            const result = await window.KB.searchByText(
                params.query,
                params.source || null,
                params.count || 10
            );

            return {
                success: !result.error,
                data: result.data,
                error: result.error
            };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    /**
     * List all knowledge sources
     * @param {Object} params - { source? }
     */
    async listKnowledgeSources(params = {}) {
        if (!window.KB) {
            return { success: false, error: 'Knowledge base not initialized' };
        }

        try {
            const result = await window.KB.listKnowledgeSources(params.source || null);

            return {
                success: !result.error,
                data: result.data,
                error: result.error
            };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    /**
     * Get all content for a specific URL
     * @param {Object} params - { url }
     */
    async getUrlContent(params) {
        if (!window.KB) {
            return { success: false, error: 'Knowledge base not initialized' };
        }

        if (!params.url) {
            return { success: false, error: 'URL parameter required' };
        }

        try {
            const result = await window.KB.getUrlContent(params.url);

            return {
                success: !result.error,
                data: result.data,
                error: result.error
            };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    /**
     * Quick search - tries text first, falls back to semantic
     * @param {Object} params - { query, source? }
     */
    async quickSearch(params) {
        if (!window.KB) {
            return { success: false, error: 'Knowledge base not initialized' };
        }

        try {
            const result = await window.KB.quickSearch(
                params.query,
                params.source || null
            );

            return {
                success: !result.error,
                data: result.data,
                method: result.method,
                error: result.error
            };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    /**
     * Get knowledge base statistics
     */
    async getStatistics() {
        if (!window.KB) {
            return { success: false, error: 'Knowledge base not initialized' };
        }

        try {
            const stats = await window.KB.getStatistics();
            return { success: true, data: stats };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
};

// ==================== CONVENIENCE FUNCTIONS ====================

/**
 * Quick access functions for common operations
 * These can be called directly: searchKB('my query')
 */

async function searchKB(query, source = null) {
    return window.KBHandlers.searchByText({ query, source });
}

async function searchKBSemantic(query, threshold = 0.4) {
    return window.KBHandlers.searchKnowledgeBase({ query, threshold });
}

async function listKBSources() {
    return window.KBHandlers.listKnowledgeSources();
}

async function getKBStats() {
    return window.KBHandlers.getStatistics();
}

// ==================== TAURI INTEGRATION ====================

/**
 * Check if running in Tauri environment
 */
function isTauri() {
    return window.__TAURI__ && window.__TAURI__.core;
}

/**
 * Register Tauri event listeners (if in Tauri environment)
 */
function registerTauriHandlers() {
    if (!isTauri()) {
        console.log('[Main] Not running in Tauri environment');
        return;
    }

    console.log('[Main] Tauri environment detected, handlers available via window.KBHandlers');

    // Future: Could register custom Tauri commands here
    // window.__TAURI__.core.invoke('register_kb_handlers');
}

// ==================== STARTUP ====================

/**
 * Initialize everything when DOM is ready
 */
function onReady() {
    console.log('[Main] DOM ready, starting initialization...');

    // Initialize KB client
    window.KB = initKnowledgeBase();

    if (window.KB) {
        // Register Tauri handlers if applicable
        registerTauriHandlers();

        // Log statistics on startup (debug mode)
        if (KB_CONFIG.debug) {
            window.KB.getStatistics().then(stats => {
                console.log('[Main] Knowledge Base Stats:', stats);
            });
        }

        console.log('[Main] Initialization complete');
        console.log('[Main] Usage: window.KBHandlers.searchByText({ query: "your query", source: "Session History" })');
    }
}

// Run on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', onReady);
} else {
    onReady();
}

// ==================== EXPORTS ====================

// Make convenience functions available globally
if (typeof window !== 'undefined') {
    window.searchKB = searchKB;
    window.searchKBSemantic = searchKBSemantic;
    window.listKBSources = listKBSources;
    window.getKBStats = getKBStats;
}
