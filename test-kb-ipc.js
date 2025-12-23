/**
 * KB IPC Integration Test Script
 * Tests the kb-service module directly from Node.js
 *
 * Run with: node test-kb-ipc.js
 *
 * Created: 2025-12-14
 * Task: TASK-010
 */

const kbService = require('./services/kb-service');

async function runTests() {
    console.log('=======================================');
    console.log('KB SERVICE INTEGRATION TESTS');
    console.log('=======================================\n');

    let passed = 0;
    let failed = 0;

    // Test 1: Connection
    console.log('TEST 1: Connection');
    console.log('-'.repeat(40));
    try {
        const status = await kbService.testConnection();
        if (status.connected) {
            console.log('  PASS: Connected to Supabase');
            passed++;
        } else {
            console.log('  FAIL: Connection failed -', status.error);
            failed++;
        }
    } catch (error) {
        console.log('  FAIL: Exception -', error.message);
        failed++;
    }

    // Test 2: Search
    console.log('\nTEST 2: Search("QCM")');
    console.log('-'.repeat(40));
    try {
        const results = await kbService.search('QCM', { limit: 5 });
        if (Array.isArray(results) && results.length > 0) {
            console.log(`  PASS: Found ${results.length} results`);
            console.log(`  First result: "${results[0].title || 'No title'}"`);
            passed++;
        } else if (Array.isArray(results)) {
            console.log('  PASS: Query returned (0 results)');
            passed++;
        } else {
            console.log('  FAIL: Invalid response type');
            failed++;
        }
    } catch (error) {
        console.log('  FAIL: Exception -', error.message);
        failed++;
    }

    // Test 3: List Sources
    console.log('\nTEST 3: List Sources');
    console.log('-'.repeat(40));
    try {
        const sources = await kbService.listSources();
        if (Array.isArray(sources)) {
            console.log(`  PASS: Found ${sources.length} sources`);
            if (sources.length > 0) {
                console.log(`  First source: "${sources[0].title || sources[0].url}"`);
            }
            passed++;
        } else {
            console.log('  FAIL: Invalid response type');
            failed++;
        }
    } catch (error) {
        console.log('  FAIL: Exception -', error.message);
        failed++;
    }

    // Test 4: Get Categories
    console.log('\nTEST 4: Get Categories');
    console.log('-'.repeat(40));
    try {
        const categories = await kbService.getSourceCategories();
        if (Array.isArray(categories)) {
            console.log(`  PASS: Found ${categories.length} categories`);
            for (const cat of categories.slice(0, 3)) {
                console.log(`    - ${cat.source}: ${cat.count} rows`);
            }
            passed++;
        } else {
            console.log('  FAIL: Invalid response type');
            failed++;
        }
    } catch (error) {
        console.log('  FAIL: Exception -', error.message);
        failed++;
    }

    // Test 5: Get Recent
    console.log('\nTEST 5: Get Recent Documents');
    console.log('-'.repeat(40));
    try {
        const recent = await kbService.getRecent(3);
        if (Array.isArray(recent)) {
            console.log(`  PASS: Got ${recent.length} recent documents`);
            for (const doc of recent) {
                console.log(`    - ${doc.title || doc.url}`);
            }
            passed++;
        } else {
            console.log('  FAIL: Invalid response type');
            failed++;
        }
    } catch (error) {
        console.log('  FAIL: Exception -', error.message);
        failed++;
    }

    // Test 6: Get By URL (if we have sources)
    console.log('\nTEST 6: Get Document By URL');
    console.log('-'.repeat(40));
    try {
        const sources = await kbService.listSources();
        if (sources.length > 0) {
            const testUrl = sources[0].url;
            const chunks = await kbService.getByUrl(testUrl);
            if (Array.isArray(chunks)) {
                console.log(`  PASS: Got ${chunks.length} chunks for document`);
                passed++;
            } else {
                console.log('  FAIL: Invalid response type');
                failed++;
            }
        } else {
            console.log('  SKIP: No sources available');
        }
    } catch (error) {
        console.log('  FAIL: Exception -', error.message);
        failed++;
    }

    // Summary
    console.log('\n=======================================');
    console.log('SUMMARY');
    console.log('=======================================');
    console.log(`  PASSED: ${passed}`);
    console.log(`  FAILED: ${failed}`);
    console.log(`  TOTAL:  ${passed + failed}`);
    console.log('=======================================\n');

    if (failed === 0) {
        console.log('All tests passed! KB integration is working.');
    } else {
        console.log('Some tests failed. Check errors above.');
    }

    process.exit(failed > 0 ? 1 : 0);
}

runTests().catch(error => {
    console.error('Test suite failed:', error);
    process.exit(1);
});
