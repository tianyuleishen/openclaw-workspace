/**
 * Cognitive Reasoning Example
 * 
 * Demonstrates Think First methodology before task execution
 */

const { ThinkLoop } = require('./think_loop');

/**
 * Example 1: Clear request - should execute directly
 */
async function example1_clearRequest() {
    console.log('\n' + '='.repeat(60));
    console.log('Example 1: Clear Request');
    console.log('='.repeat(60) + '\n');

    const context = {
        message: '检查服务器8080端口是否运行',
        history: ['用户之前问过服务器问题'],
        memory: {}
    };

    const thinker = new ThinkLoop();
    const result = await thinker.think(context);

    console.log('\n📊 Result:');
    console.log(`   Confidence: ${(result.confidence * 100).toFixed(0)}%`);
    console.log(`   Should Execute: ${result.confirmed ? 'YES' : 'NO'}`);
    console.log(`   Ambiguities: ${result.ambiguities.length}`);

    return result;
}

/**
 * Example 2: Ambiguous request - needs clarification
 */
async function example2_ambiguousRequest() {
    console.log('\n' + '='.repeat(60));
    console.log('Example 2: Ambiguous Request');
    console.log('='.repeat(60) + '\n');

    const context = {
        message: '检查服务器',
        history: [],
        memory: {}
    };

    const thinker = new ThinkLoop();
    const result = await thinker.think(context);

    console.log('\n📊 Result:');
    console.log(`   Confidence: ${(result.confidence * 100).toFixed(0)}%`);
    console.log(`   Should Execute: ${result.confirmed ? 'YES' : 'NO'}`);
    console.log(`   Ambiguities: ${result.ambiguities.length}`);

    if (result.clarificationNeeded) {
        console.log('\n💬 Clarification Questions:');
        result.questions.forEach((q, i) => {
            console.log(`   ${i+1}. ${q.question}`);
            console.log(`      Options: ${q.options.join(' | ')}`);
        });
    }

    return result;
}

/**
 * Example 3: Complex request with implicit needs
 */
async function example3_complexRequest() {
    console.log('\n' + '='.repeat(60));
    console.log('Example 3: Complex Request with Implicit Needs');
    console.log('='.repeat(60) + '\n');

    const context = {
        message: '生成一个视频，要快又要便宜，质量好一点',
        history: [],
        memory: {}
    };

    const thinker = new ThinkLoop();
    const result = await thinker.think(context);

    console.log('\n📊 Result:');
    console.log(`   Intent: ${result.intent.type}`);
    console.log(`   Implicit Needs:`, result.intent.implicitNeeds);
    console.log(`   Confidence: ${(result.confidence * 100).toFixed(0)}%`);

    return result;
}

// Run examples
async function runAll() {
    console.log('\n' + '🧠'.repeat(25));
    console.log('🧠 COGNITIVE REASONING EXAMPLES');
    console.log('🧠'.repeat(25) + '\n');

    await example1_clearRequest();
    await example2_ambiguousRequest();
    await example3_complexRequest();

    console.log('\n' + '🧠'.repeat(25));
    console.log('🧠 EXAMPLES COMPLETE');
    console.log('🧠'.repeat(25) + '\n');
}

runAll().catch(console.error);
