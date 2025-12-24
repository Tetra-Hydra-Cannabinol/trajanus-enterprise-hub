/**
 * KB Service Module
 * Provides Supabase knowledge base integration for Trajanus Command Center
 *
 * Created: 2025-12-14
 * Task: TASK-010
 */

const { createClient } = require('@supabase/supabase-js');
const path = require('path');
const fs = require('fs');

// Load .env manually (no dotenv package needed - Google Drive npm issue)
function loadEnv() {
    const envPath = path.join(__dirname, '..', '.env');
    const env = {};
    try {
        const content = fs.readFileSync(envPath, 'utf8');
        for (const line of content.split('\n')) {
            const trimmed = line.trim();
            if (trimmed && !trimmed.startsWith('#')) {
                const eqIndex = trimmed.indexOf('=');
                if (eqIndex > 0) {
                    const key = trimmed.substring(0, eqIndex).trim();
                    const value = trimmed.substring(eqIndex + 1).trim();
                    env[key] = value;
                }
            }
        }
    } catch (error) {
        console.error('[KB Service] Could not load .env:', error.message);
    }
    return env;
}

const envVars = loadEnv();

// Initialize Supabase client
const supabaseUrl = envVars.SUPABASE_URL || process.env.SUPABASE_URL;
const supabaseKey = envVars.SUPABASE_ANON_KEY || process.env.SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
    console.error('[KB Service] Missing Supabase credentials in .env');
    console.error('[KB Service] Expected .env at:', path.join(__dirname, '..', '.env'));
}

const supabase = createClient(supabaseUrl || '', supabaseKey || '');

/**
 * Search knowledge base using text search
 * @param {string} query - Search query
 * @param {Object} options - Search options
 * @param {number} options.limit - Max results (default 20)
 * @param {string} options.source - Filter by source
 * @returns {Promise<Array>} Search results
 */
async function search(query, options = {}) {
    const limit = options.limit || 20;

    try {
        // Use RPC function if available, fallback to direct query
        let result;

        if (options.useRpc !== false) {
            // Try RPC function first
            result = await supabase.rpc('search_by_text', {
                search_query: query
            });

            if (result.error) {
                throw result.error;
            }

            let data = result.data || [];

            // Apply source filter if specified
            if (options.source) {
                data = data.filter(row =>
                    row.metadata?.source === options.source
                );
            }

            return data.slice(0, limit);
        }

        // Direct query fallback
        let queryBuilder = supabase
            .from('knowledge_base')
            .select('id, url, chunk_number, title, summary, content, metadata, created_at')
            .or(`title.ilike.%${query}%,summary.ilike.%${query}%,content.ilike.%${query}%`)
            .limit(limit);

        if (options.source) {
            queryBuilder = queryBuilder.eq('metadata->>source', options.source);
        }

        result = await queryBuilder;

        if (result.error) {
            throw result.error;
        }

        return result.data || [];

    } catch (error) {
        console.error('[KB Service] Search error:', error.message);
        throw error;
    }
}

/**
 * List all knowledge sources (unique documents)
 * @returns {Promise<Array>} List of sources with metadata
 */
async function listSources() {
    try {
        // Try RPC function first
        const rpcResult = await supabase.rpc('list_knowledge_sources');

        if (!rpcResult.error && rpcResult.data) {
            return rpcResult.data;
        }

        // Fallback: Get distinct URLs with first chunk info
        const result = await supabase
            .from('knowledge_base')
            .select('url, title, summary, metadata, created_at')
            .eq('chunk_number', 0)
            .order('created_at', { ascending: false });

        if (result.error) {
            throw result.error;
        }

        return result.data || [];

    } catch (error) {
        console.error('[KB Service] listSources error:', error.message);
        throw error;
    }
}

/**
 * Get all chunks for a specific URL/document
 * @param {string} url - Document URL
 * @returns {Promise<Array>} All chunks for the document
 */
async function getByUrl(url) {
    try {
        // Try RPC function first
        const rpcResult = await supabase.rpc('get_url_content', {
            target_url: url
        });

        if (!rpcResult.error && rpcResult.data) {
            return rpcResult.data;
        }

        // Fallback: Direct query
        const result = await supabase
            .from('knowledge_base')
            .select('id, url, chunk_number, title, summary, content, metadata, created_at')
            .eq('url', url)
            .order('chunk_number', { ascending: true });

        if (result.error) {
            throw result.error;
        }

        return result.data || [];

    } catch (error) {
        console.error('[KB Service] getByUrl error:', error.message);
        throw error;
    }
}

/**
 * Browse documents by source category
 * @param {string} source - Source category (e.g., 'Session History', 'Core Protocols')
 * @param {number} limit - Max results (default 50)
 * @returns {Promise<Array>} Documents matching source
 */
async function browseBySource(source, limit = 50) {
    try {
        const result = await supabase
            .from('knowledge_base')
            .select('url, title, summary, metadata, created_at')
            .eq('chunk_number', 0)
            .eq('metadata->>source', source)
            .order('created_at', { ascending: false })
            .limit(limit);

        if (result.error) {
            throw result.error;
        }

        return result.data || [];

    } catch (error) {
        console.error('[KB Service] browseBySource error:', error.message);
        throw error;
    }
}

/**
 * Get recent documents
 * @param {number} limit - Max results (default 20)
 * @returns {Promise<Array>} Recent documents
 */
async function getRecent(limit = 20) {
    try {
        const result = await supabase
            .from('knowledge_base')
            .select('url, title, summary, metadata, created_at')
            .eq('chunk_number', 0)
            .order('created_at', { ascending: false })
            .limit(limit);

        if (result.error) {
            throw result.error;
        }

        return result.data || [];

    } catch (error) {
        console.error('[KB Service] getRecent error:', error.message);
        throw error;
    }
}

/**
 * Get available source categories
 * @returns {Promise<Array>} List of source categories with counts
 */
async function getSourceCategories() {
    try {
        const result = await supabase
            .from('knowledge_base')
            .select('metadata');

        if (result.error) {
            throw result.error;
        }

        // Count by source
        const sourceCounts = {};
        for (const row of result.data || []) {
            const source = row.metadata?.source || 'Unknown';
            sourceCounts[source] = (sourceCounts[source] || 0) + 1;
        }

        // Convert to array and sort
        return Object.entries(sourceCounts)
            .map(([source, count]) => ({ source, count }))
            .sort((a, b) => b.count - a.count);

    } catch (error) {
        console.error('[KB Service] getSourceCategories error:', error.message);
        throw error;
    }
}

/**
 * Test connection to Supabase
 * @returns {Promise<Object>} Connection status
 */
async function testConnection() {
    try {
        const result = await supabase
            .from('knowledge_base')
            .select('id')
            .limit(1);

        if (result.error) {
            return { connected: false, error: result.error.message };
        }

        return { connected: true, rows: result.data.length };

    } catch (error) {
        return { connected: false, error: error.message };
    }
}

module.exports = {
    search,
    listSources,
    getByUrl,
    browseBySource,
    getRecent,
    getSourceCategories,
    testConnection,
    supabase // Export client for advanced usage
};
