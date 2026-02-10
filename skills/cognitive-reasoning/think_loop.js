/**
 * Cognitive Reasoning Framework - Think First Loop
 * 
 * Implements "Think Before Act" methodology for deep reasoning
 * and intent understanding before task execution.
 */

const fs = require('fs');
const path = require('path');

class ThinkLoop {
    constructor() {
        this.threshold = 0.7;  // Confidence threshold for auto-execution
        this.historyDir = path.join(process.env.HOME || '/home', '.openclaw/workspace/memory');
    }

    /**
     * Main thinking loop - called before any major task
     * @param {Object} context - Current context
     * @returns {Object} Analysis result with clarity score
     */
    async think(context) {
        console.log('\n' + '🧠'.repeat(20));
        console.log('🧠 THINK LOOP ACTIVATED');
        console.log('🧠'.repeat(20) + '\n');

        const analysis = {
            timestamp: new Date().toISOString(),
            originalRequest: context.message || context.task,
            intent: null,
            ambiguities: [],
            confidence: 0,
            steps: [],
            clarificationNeeded: false,
            questions: [],
            confirmed: false
        };

        // Step 1: Intent Classification
        analysis.steps.push('Step 1: Classifying intent...');
        analysis.intent = await this.classifyIntent(context);
        console.log(`🎯 Intent: ${analysis.intent.type} (${(analysis.intent.confidence * 100).toFixed(0)}%)`);

        // Step 2: Ambiguity Detection
        analysis.steps.push('Step 2: Detecting ambiguities...');
        analysis.ambiguities = await this.detectAmbiguities(context, analysis.intent);
        console.log(`🔍 Ambiguities found: ${analysis.ambiguities.length}`);

        // Step 3: Confidence Calculation
        analysis.steps.push('Step 3: Calculating confidence...');
        analysis.confidence = this.calculateConfidence(analysis.intent, analysis.ambiguities);
        console.log(`📊 Overall Confidence: ${(analysis.confidence * 100).toFixed(0)}%`);

        // Step 4: Decision
        if (analysis.confidence >= this.threshold) {
            analysis.steps.push('Step 4: High confidence - ready to execute');
            analysis.confirmed = true;
            console.log('✅ High confidence - proceeding with execution\n');
        } else {
            analysis.steps.push('Step 4: Low confidence - clarification needed');
            analysis.clarificationNeeded = true;
            analysis.questions = await this.generateClarificationQuestions(
                analysis.intent, 
                analysis.ambiguities
            );
            console.log('⚠️ Low confidence - clarification needed\n');
        }

        // Step 5: Log reasoning
        analysis.steps.push('Step 5: Logging reasoning process');
        await this.logReasoning(analysis);

        console.log('🧠'.repeat(20) + '\n');

        return analysis;
    }

    /**
     * Classify the user's intent
     */
    async classifyIntent(context) {
        const message = (context.message || '').toLowerCase();
        
        // Intent patterns
        const patterns = [
            { type: 'EXECUTE_TASK', keywords: ['执行', '生成', 'create', 'make', '生成', '做'], confidence: 0.9 },
            { type: 'CHECK_STATUS', keywords: ['检查', '查看', 'check', 'status', '看'], confidence: 0.85 },
            { type: 'SEARCH_INFO', keywords: ['搜索', '查找', 'search', 'find', '找'], confidence: 0.8 },
            { type: 'LEARNING', keywords: ['学习', '了解', 'learn', 'study', '看看'], confidence: 0.75 },
            { type: 'CONFIG', keywords: ['配置', '设置', 'config', 'setup', '设置'], confidence: 0.85 },
            { type: 'CONVERSATION', keywords: ['聊天', 'talk', '对话'], confidence: 0.7 }
        ];

        // Default to EXECUTE_TASK if no match
        let bestMatch = { type: 'EXECUTE_TASK', confidence: 0.5 };

        for (const pattern of patterns) {
            const matchCount = pattern.keywords.filter(k => message.includes(k)).length;
            if (matchCount > 0) {
                const confidence = Math.min(0.95, 0.5 + (matchCount * 0.15));
                if (confidence > bestMatch.confidence) {
                    bestMatch = { type: pattern.type, confidence };
                }
            }
        }

        // Detect implicit needs
        const implicitNeeds = [];
        if (message.includes('快速') || message.includes('快')) {
            implicitNeeds.push({ need: 'speed', weight: 0.8 });
        }
        if (message.includes('便宜') || message.includes('省')) {
            implicitNeeds.push({ need: 'cost_efficiency', weight: 0.9 });
        }
        if (message.includes('质量') || message.includes('好')) {
            implicitNeeds.push({ need: 'quality', weight: 0.8 });
        }

        return {
            ...bestMatch,
            implicitNeeds,
            entities: this.extractEntities(message),
            sentiment: this.analyzeSentiment(message)
        };
    }

    /**
     * Detect ambiguities in the request
     */
    async detectAmbiguities(context, intent) {
        const ambiguities = [];
        const message = (context.message || '').toLowerCase();

        // Common ambiguity patterns
        const ambiguityPatterns = [
            {
                pattern: /^(检查|查看|check)/,
                question: 'What specific aspect should I check?',
                options: ['Health/Status', 'Logs', 'Performance', 'All'],
                weight: 0.9
            },
            {
                pattern: /^(生成|create|make)/,
                question: 'What format/output do you need?',
                options: ['File', 'Link', 'Display only'],
                weight: 0.8
            },
            {
                pattern: /^(搜索|search)/,
                question: 'Where should I search?',
                options: ['Web', 'Local files', 'Memory', 'All'],
                weight: 0.85
            },
            {
                pattern: /(图片|image|photo)/,
                question: 'What style/size for the image?',
                options: ['Cartoon', 'Realistic', 'Specific dimensions'],
                weight: 0.7
            },
            {
                pattern: /(视频|video)/,
                question: 'Duration and resolution?',
                options: ['5s/720P', '10s/720P', '15s/1080P'],
                weight: 0.8
            }
        ];

        for (const ap of ambiguityPatterns) {
            if (ap.pattern.test(message)) {
                ambiguities.push({
                    type: 'INCOMPLETE_SPEC',
                    question: ap.question,
                    options: ap.options,
                    weight: ap.weight
                });
            }
        }

        // Check for missing context
        if (!context.history && !context.memory) {
            ambiguities.push({
                type: 'NO_CONTEXT',
                question: 'Should I check memory/history first?',
                options: ['Yes, check memory', 'No, just execute', 'Summarize first'],
                weight: 0.6
            });
        }

        return ambiguities;
    }

    /**
     * Calculate overall confidence score
     */
    calculateConfidence(intent, ambiguities) {
        let score = intent.confidence;

        // Penalize for ambiguities
        for (const amb of ambiguities) {
            score -= (amb.weight * 0.15);
        }

        return Math.max(0, Math.min(1, score));
    }

    /**
     * Generate clarification questions
     */
    async generateClarificationQuestions(intent, ambiguities) {
        const questions = [];

        for (const amb of ambiguities) {
            questions.push({
                question: amb.question,
                options: amb.options,
                type: amb.type
            });
        }

        // Add intent-specific questions
        if (intent.implicitNeeds.length > 0) {
            questions.push({
                question: 'Any priority? (Speed vs Quality vs Cost)',
                options: intent.implicitNeeds.map(n => n.need),
                type: 'PRIORITY'
            });
        }

        return questions;
    }

    /**
     * Extract entities from message
     */
    extractEntities(message) {
        const entities = {
            files: [],
            commands: [],
            parameters: []
        };

        // Simple entity extraction
        const filePattern = /\/(?:tmp|home|workspace)\/[\w\-./]+/g;
        const files = message.match(filePattern);
        if (files) entities.files = files;

        return entities;
    }

    /**
     * Analyze sentiment
     */
    analyzeSentiment(message) {
        const positive = ['好', '棒', '优秀', 'great', 'good', 'excellent'];
        const negative = ['错', '坏', '慢', 'error', 'bad', 'slow', 'fail'];
        
        let score = 0;
        positive.forEach(w => { if (message.includes(w)) score += 0.2; });
        negative.forEach(w => { if (message.includes(w)) score -= 0.2; });

        return {
            score: Math.max(-1, Math.min(1, score)),
            label: score > 0.2 ? 'positive' : score < -0.2 ? 'negative' : 'neutral'
        };
    }

    /**
     * Log reasoning process
     */
    async logReasoning(analysis) {
        const logPath = path.join(this.historyDir, `reasoning_${Date.now()}.json`);
        
        try {
            fs.writeFileSync(logPath, JSON.stringify(analysis, null, 2));
            console.log(`📝 Reasoning logged: ${logPath}`);
        } catch (e) {
            console.log(`⚠️ Failed to log reasoning: ${e.message}`);
        }
    }

    /**
     * Confirm understanding with user
     */
    formatClarification(analysis) {
        let response = `**理解确认**\n\n`;
        response += `我理解你想：${analysis.intent.type}\n`;
        response += `\n但有几个不明确的地方：\n`;
        
        analysis.questions.forEach((q, i) => {
            response += `\n${i+1}. ${q.question}\n`;
            response += `   选项：${q.options.join(' | ')}\n`;
        });

        response += `\n请回复选项编号或详细说明。`;

        return response;
    }
}

module.exports = { ThinkLoop };
