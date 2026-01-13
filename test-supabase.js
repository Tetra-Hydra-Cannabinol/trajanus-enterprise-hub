/**
 * Supabase RPC Function Test Suite
 * Tests all 4 RPC functions before integration into main app
 *
 * Created: January 13, 2026
 * Project: Trajanus Command Center
 */

const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');

// Load environment variables from .env file
function loadEnv() {
    const envPath = 'G:\\My Drive\\00 - Trajanus USA\\00-Command-Center\\05-Scripts\\.env';

    if (!fs.existsSync(envPath)) {
        console.error('❌ ERROR: .env file not found at:', envPath);
        process.exit(1);
    }

    const envContent = fs.readFileSync(envPath, 'utf8');
    const lines = envContent.split('\n');

    lines.forEach(line => {
        const trimmed = line.trim();
        if (trimmed && !trimmed.startsWith('#')) {
            const [key, ...valueParts] = trimmed.split('=');
            if (key && valueParts.length > 0) {
                process.env[key.trim()] = valueParts.join('=').trim();
            }
        }
    });

    return {
        supabaseUrl: process.env.SUPABASE_URL,
        supabaseKey: process.env.SUPABASE_KEY,
        openaiKey: process.env.OPENAI_API_KEY
    };
}

// Test results storage
const results = {
    timestamp: new Date().toISOString(),
    tests: [],
    summary: { passed: 0, failed: 0 }
};

// Helper to log test results
function logTest(name, passed, data, error = null) {
    const status = passed ? '✅ PASS' : '❌ FAIL';
    console.log(`\n${status}: ${name}`);

    if (error) {
        console.log(`   Error: ${error}`);
    }

    if (passed && data) {
        console.log(`   Records returned: ${Array.isArray(data) ? data.length : 1}`);
    }

    results.tests.push({
        name,
        passed,
        recordCount: Array.isArray(data) ? data.length : (data ? 1 : 0),
        error: error ? String(error) : null,
        sampleData: data ? (Array.isArray(data) ? data.slice(0, 2) : data) : null
    });

    if (passed) results.summary.passed++;
    else results.summary.failed++;
}

// Generate embedding using OpenAI API
async function generateEmbedding(text, apiKey) {
    const response = await fetch('https://api.openai.com/v1/embeddings', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            model: 'text-embedding-3-small',
            input: text
        })
    });

    if (!response.ok) {
        throw new Error(`OpenAI API error: ${response.status} ${response.statusText}`);
    }

    const result = await response.json();
    return result.data[0].embedding;
}

// Main test runner
async function runTests() {
    console.log('═══════════════════════════════════════════════════════════');
    console.log('  SUPABASE RPC FUNCTION TEST SUITE');
    console.log('  Trajanus Command Center');
    console.log('  ' + new Date().toLocaleString());
    console.log('═══════════════════════════════════════════════════════════');

    // Load credentials
    console.log('\n📋 Loading credentials...');
    const { supabaseUrl, supabaseKey, openaiKey } = loadEnv();

    if (!supabaseUrl || !supabaseKey) {
        console.error('❌ Missing SUPABASE_URL or SUPABASE_KEY');
        process.exit(1);
    }

    console.log(`   Supabase URL: ${supabaseUrl}`);
    console.log(`   API Key: ${supabaseKey.substring(0, 20)}...`);

    // Create Supabase client
    const supabase = createClient(supabaseUrl, supabaseKey);
    console.log('   ✅ Supabase client created');

    // ═══════════════════════════════════════════════════════════
    // TEST 1: list_knowledge_sources
    // ═══════════════════════════════════════════════════════════
    console.log('\n───────────────────────────────────────────────────────────');
    console.log('TEST 1: list_knowledge_sources(NULL)');
    console.log('───────────────────────────────────────────────────────────');

    try {
        const { data, error } = await supabase.rpc('list_knowledge_sources', {
            filter_source: null
        });

        if (error) throw error;

        logTest('list_knowledge_sources', true, data);

        if (data && data.length > 0) {
            console.log('\n   Top 5 Sources:');
            data.slice(0, 5).forEach((src, i) => {
                console.log(`   ${i + 1}. ${src.source}: ${src.chunk_count} chunks, ${src.url_count} URLs`);
            });
        }
    } catch (err) {
        logTest('list_knowledge_sources', false, null, err.message);
    }

    // ═══════════════════════════════════════════════════════════
    // TEST 2: search_by_text
    // ═══════════════════════════════════════════════════════════
    console.log('\n───────────────────────────────────────────────────────────');
    console.log('TEST 2: search_by_text("RAG", filter: Session History)');
    console.log('───────────────────────────────────────────────────────────');

    try {
        // Use a specific source filter to avoid timeout on full table scan
        const { data, error } = await supabase.rpc('search_by_text', {
            search_query: 'RAG',
            filter_source: 'Session History',  // Filter to smaller dataset
            match_count: 5
        });

        if (error) throw error;

        logTest('search_by_text', true, data);

        if (data && data.length > 0) {
            console.log('\n   Sample Results:');
            data.slice(0, 3).forEach((item, i) => {
                console.log(`   ${i + 1}. [Rank: ${item.rank?.toFixed(4) || 'N/A'}] ${item.title?.substring(0, 60) || 'No title'}...`);
            });
        }
    } catch (err) {
        logTest('search_by_text', false, null, err.message);
    }

    // ═══════════════════════════════════════════════════════════
    // TEST 3: get_url_content
    // ═══════════════════════════════════════════════════════════
    console.log('\n───────────────────────────────────────────────────────────');
    console.log('TEST 3: get_url_content (using known test URL)');
    console.log('───────────────────────────────────────────────────────────');

    try {
        // First, get a valid URL from the database
        const { data: urlData } = await supabase
            .from('knowledge_base')
            .select('url')
            .limit(1)
            .single();

        const testUrl = urlData?.url || 'https://test.local/manual-insert';
        console.log(`   Testing with URL: ${testUrl.substring(0, 60)}...`);

        const { data, error } = await supabase.rpc('get_url_content', {
            target_url: testUrl
        });

        if (error) throw error;

        logTest('get_url_content', true, data);

        if (data && data.length > 0) {
            console.log(`\n   Chunks for URL: ${data.length}`);
            console.log(`   First chunk title: ${data[0].title?.substring(0, 50) || 'No title'}...`);
        }
    } catch (err) {
        logTest('get_url_content', false, null, err.message);
    }

    // ═══════════════════════════════════════════════════════════
    // TEST 4: match_knowledge_base (Semantic Search)
    // ═══════════════════════════════════════════════════════════
    console.log('\n───────────────────────────────────────────────────────────');
    console.log('TEST 4: match_knowledge_base (semantic vector search)');
    console.log('───────────────────────────────────────────────────────────');

    if (!openaiKey) {
        console.log('   ⚠️  OPENAI_API_KEY not found - skipping embedding generation');
        logTest('match_knowledge_base', false, null, 'Missing OPENAI_API_KEY');
    } else {
        try {
            console.log('   Generating embedding for: "RAG system database setup"');
            const embedding = await generateEmbedding('RAG system database setup', openaiKey);
            console.log(`   ✅ Embedding generated (${embedding.length} dimensions)`);

            const { data, error } = await supabase.rpc('match_knowledge_base', {
                query_embedding: embedding,
                match_threshold: 0.3,  // Lower threshold to catch more results
                match_count: 5
            });

            if (error) throw error;

            logTest('match_knowledge_base', true, data);

            if (data && data.length > 0) {
                console.log('\n   Semantic Search Results:');
                data.slice(0, 3).forEach((item, i) => {
                    console.log(`   ${i + 1}. [Similarity: ${item.similarity?.toFixed(4) || 'N/A'}] ${item.title?.substring(0, 50) || 'No title'}...`);
                });
            }
        } catch (err) {
            logTest('match_knowledge_base', false, null, err.message);
        }
    }

    // ═══════════════════════════════════════════════════════════
    // SUMMARY
    // ═══════════════════════════════════════════════════════════
    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('  TEST SUMMARY');
    console.log('═══════════════════════════════════════════════════════════');
    console.log(`  Passed: ${results.summary.passed}`);
    console.log(`  Failed: ${results.summary.failed}`);
    console.log(`  Total:  ${results.tests.length}`);
    console.log('═══════════════════════════════════════════════════════════');

    // Write results to JSON for documentation
    const outputPath = path.join(__dirname, 'test-supabase-results.json');
    fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
    console.log(`\n📄 Full results saved to: ${outputPath}`);

    // Return exit code based on results
    process.exit(results.summary.failed > 0 ? 1 : 0);
}

// Run the tests
runTests().catch(err => {
    console.error('\n💥 FATAL ERROR:', err);
    process.exit(1);
});
