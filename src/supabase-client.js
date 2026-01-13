/**
 * Supabase Knowledge Base Client
 * Provides access to RAG functions for the Trajanus Command Center
 *
 * Created: January 13, 2026
 * Project: Trajanus Command Center (Tauri 2.0)
 *
 * Usage:
 *   const kb = new KnowledgeBaseClient();
 *   const results = await kb.searchByText('construction management', 'Session History');
 */

class KnowledgeBaseClient {
    constructor(config = {}) {
        // Default to the Trajanus production database
        this.supabaseUrl = config.url || 'https://iaxtwrswinygwwwdkvok.supabase.co';
        this.supabaseKey = config.key || null;
        this.openaiKey = config.openaiKey || null;

        // Debug mode for console logging
        this.debug = config.debug || false;

        this.log('KnowledgeBaseClient initialized');
    }

    /**
     * Internal logging helper
     */
    log(...args) {
        if (this.debug) {
            console.log('[KB]', ...args);
        }
    }

    /**
     * Internal error logging
     */
    logError(...args) {
        console.error('[KB ERROR]', ...args);
    }

    /**
     * Set API keys (call this after loading from .env or config)
     */
    setKeys(supabaseKey, openaiKey = null) {
        this.supabaseKey = supabaseKey;
        this.openaiKey = openaiKey;
        this.log('API keys configured');
    }

    /**
     * Check if the client is properly configured
     */
    isConfigured() {
        return this.supabaseKey !== null;
    }

    /**
     * Make authenticated request to Supabase REST API
     */
    async request(endpoint, options = {}) {
        if (!this.isConfigured()) {
            throw new Error('KnowledgeBaseClient not configured. Call setKeys() first.');
        }

        const url = `${this.supabaseUrl}${endpoint}`;
        const headers = {
            'apikey': this.supabaseKey,
            'Authorization': `Bearer ${this.supabaseKey}`,
            'Content-Type': 'application/json',
            ...options.headers
        };

        this.log(`Request: ${options.method || 'GET'} ${endpoint}`);

        try {
            const response = await fetch(url, {
                ...options,
                headers
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Supabase error ${response.status}: ${errorText}`);
            }

            const data = await response.json();
            this.log(`Response: ${Array.isArray(data) ? data.length + ' records' : 'object'}`);
            return { data, error: null };

        } catch (error) {
            this.logError(error.message);
            return { data: null, error: error.message };
        }
    }

    /**
     * Call an RPC function
     */
    async rpc(functionName, params = {}) {
        return this.request(`/rest/v1/rpc/${functionName}`, {
            method: 'POST',
            body: JSON.stringify(params)
        });
    }

    // ==================== RPC FUNCTION WRAPPERS ====================

    /**
     * List all knowledge sources with statistics
     * @param {string|null} filterSource - Optional source filter
     * @returns {Promise<{data: Array, error: string|null}>}
     */
    async listKnowledgeSources(filterSource = null) {
        this.log('listKnowledgeSources', { filterSource });
        return this.rpc('list_knowledge_sources', {
            filter_source: filterSource
        });
    }

    /**
     * Full-text search across knowledge base
     * IMPORTANT: Always use filterSource to avoid timeouts on large datasets!
     *
     * @param {string} searchQuery - The search terms
     * @param {string|null} filterSource - Source filter (RECOMMENDED for performance)
     * @param {number} matchCount - Maximum results (default: 10)
     * @returns {Promise<{data: Array, error: string|null}>}
     */
    async searchByText(searchQuery, filterSource = null, matchCount = 10) {
        this.log('searchByText', { searchQuery, filterSource, matchCount });

        // Performance warning
        if (!filterSource) {
            console.warn('[KB] searchByText without filterSource may timeout on large datasets. Consider using a source filter.');
        }

        return this.rpc('search_by_text', {
            search_query: searchQuery,
            filter_source: filterSource,
            match_count: matchCount
        });
    }

    /**
     * Get all chunks for a specific URL
     * @param {string} targetUrl - The URL to retrieve
     * @returns {Promise<{data: Array, error: string|null}>}
     */
    async getUrlContent(targetUrl) {
        this.log('getUrlContent', { targetUrl });
        return this.rpc('get_url_content', {
            target_url: targetUrl
        });
    }

    /**
     * Semantic vector search using embeddings
     * Requires OpenAI API key for embedding generation
     *
     * @param {string} query - Natural language query
     * @param {number} matchThreshold - Similarity threshold (0.3-0.5 recommended)
     * @param {number} matchCount - Maximum results (default: 10)
     * @returns {Promise<{data: Array, error: string|null}>}
     */
    async searchKnowledgeBase(query, matchThreshold = 0.4, matchCount = 10) {
        this.log('searchKnowledgeBase', { query, matchThreshold, matchCount });

        // First, generate embedding
        const embedding = await this.generateEmbedding(query);
        if (!embedding) {
            return { data: null, error: 'Failed to generate embedding' };
        }

        // Then search
        return this.rpc('match_knowledge_base', {
            query_embedding: embedding,
            match_threshold: matchThreshold,
            match_count: matchCount
        });
    }

    /**
     * Generate embedding using OpenAI API
     * @param {string} text - Text to embed
     * @returns {Promise<number[]|null>} - 1536-dimension embedding or null
     */
    async generateEmbedding(text) {
        if (!this.openaiKey) {
            this.logError('OpenAI API key not configured. Cannot generate embeddings.');
            return null;
        }

        this.log('Generating embedding for:', text.substring(0, 50) + '...');

        try {
            const response = await fetch('https://api.openai.com/v1/embeddings', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.openaiKey}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    model: 'text-embedding-3-small',
                    input: text
                })
            });

            if (!response.ok) {
                throw new Error(`OpenAI API error: ${response.status}`);
            }

            const result = await response.json();
            this.log('Embedding generated:', result.data[0].embedding.length, 'dimensions');
            return result.data[0].embedding;

        } catch (error) {
            this.logError('Embedding generation failed:', error.message);
            return null;
        }
    }

    // ==================== CONVENIENCE METHODS ====================

    /**
     * Quick search - tries text search first, falls back to semantic
     * @param {string} query - Search query
     * @param {string|null} source - Optional source filter
     * @returns {Promise<{data: Array, error: string|null, method: string}>}
     */
    async quickSearch(query, source = null) {
        // Try text search first (faster)
        const textResult = await this.searchByText(query, source, 10);

        if (textResult.data && textResult.data.length > 0) {
            return { ...textResult, method: 'text' };
        }

        // Fall back to semantic search if no results and OpenAI key available
        if (this.openaiKey) {
            const semanticResult = await this.searchKnowledgeBase(query, 0.3, 10);
            return { ...semanticResult, method: 'semantic' };
        }

        return { data: [], error: null, method: 'none' };
    }

    /**
     * Get statistics about the knowledge base
     * @returns {Promise<{sources: number, totalChunks: number, topSources: Array}>}
     */
    async getStatistics() {
        const result = await this.listKnowledgeSources();

        if (result.error || !result.data) {
            return { sources: 0, totalChunks: 0, topSources: [] };
        }

        const totalChunks = result.data.reduce((sum, s) => sum + (s.chunk_count || 0), 0);

        return {
            sources: result.data.length,
            totalChunks,
            topSources: result.data.slice(0, 5)
        };
    }
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { KnowledgeBaseClient };
}

// Also make available globally for browser usage
if (typeof window !== 'undefined') {
    window.KnowledgeBaseClient = KnowledgeBaseClient;
}
