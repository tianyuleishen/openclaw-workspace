#!/usr/bin/env node
/**
 * OpenClaw Agent Framework
 * Pure JavaScript agent implementation (no LangChain dependency)
 * Provides agent capabilities when LangChain is not available
 */

class OpenClawAgentFramework {
  constructor(options = {}) {
    this.name = options.name || 'OpenClawAgent';
    this.version = '1.0.0';
    this.agents = new Map();
    this.tools = new Map();
    this.memory = {
      shortTerm: new Map(),
      longTerm: new Map(),
      episodic: []
    };
    this.taskQueue = [];
    this.executionLog = [];
    
    // Setup built-in tools
    this._setupBuiltInTools();
    
    console.log(`🤖 OpenClaw Agent Framework v${this.version} initialized`);
  }
  
  _setupBuiltInTools() {
    // Built-in tools available to all agents
    this.registerTool({
      name: 'search_memory',
      description: 'Search agent memory for information',
      handler: (query, context) => {
        const results = [];
        // Search short-term memory
        for (const [key, value] of this.memory.shortTerm.entries()) {
          if (key.includes(query) || String(value).includes(query)) {
            results.push({ source: 'short-term', key, value });
          }
        }
        // Search long-term memory
        for (const [key, value] of this.memory.longTerm.entries()) {
          if (key.includes(query) || String(value).includes(query)) {
            results.push({ source: 'long-term', key, value });
          }
        }
        return { query, results, count: results.length };
      }
    });
    
    this.registerTool({
      name: 'store_memory',
      description: 'Store information in memory',
      handler: (data, context) => {
        const key = data.key || `memory_${Date.now()}`;
        const type = data.type || 'short-term';
        if (type === 'long-term') {
          this.memory.longTerm.set(key, data.value);
        } else {
          this.memory.shortTerm.set(key, { value: data.value, timestamp: Date.now() });
        }
        return { stored: true, key, type };
      }
    });
    
    this.registerTool({
      name: 'analyze',
      description: 'Analyze data and return insights',
      handler: (data, context) => {
        const analysis = {
          length: String(data).length,
          type: typeof data,
          timestamp: new Date().toISOString()
        };
        return analysis;
      }
    });
    
    this.registerTool({
      name: 'execute_task',
      description: 'Execute a defined task',
      handler: (task, context) => {
        return { executed: task, timestamp: new Date().toISOString() };
      }
    });
    
    this.registerTool({
      name: 'log_event',
      description: 'Log an event to episodic memory',
      handler: (event, context) => {
        const episode = {
          event,
          context,
          timestamp: new Date().toISOString()
        };
        this.memory.episodic.push(episode);
        return { logged: true, episodeCount: this.memory.episodic.length };
      }
    });
  }
  
  registerTool(tool) {
    this.tools.set(tool.name, tool);
    console.log(`   📦 Registered tool: ${tool.name}`);
  }
  
  createAgent(config) {
    const agentId = config.id || `agent_${Date.now()}`;
    
    const agent = {
      id: agentId,
      name: config.name || agentId,
      role: config.role || 'general',
      goals: config.goals || [],
      tools: config.tools || [],
      state: {
        status: 'idle',
        lastTask: null,
        completedTasks: 0,
        memory: {
          shortTerm: new Map(),
          longTerm: new Map(),
          episodic: []
        }
      },
      createdAt: new Date().toISOString()
    };
    
    // Add default tools if none specified
    if (agent.tools.length === 0) {
      agent.tools = ['search_memory', 'store_memory', 'analyze', 'execute_task', 'log_event'];
    }
    
    this.agents.set(agentId, agent);
    
    console.log(`✅ Created agent: ${agent.name} (${agentId})`);
    
    return {
      success: true,
      agentId,
      agent: {
        id: agent.id,
        name: agent.name,
        role: agent.role,
        tools: agent.tools,
        createdAt: agent.createdAt
      }
    };
  }
  
  async executeTask(agentId, task, context = {}) {
    const agent = this.agents.get(agentId);
    
    if (!agent) {
      return { success: false, error: `Agent ${agentId} not found` };
    }
    
    // Update agent status
    agent.state.status = 'executing';
    agent.state.lastTask = task;
    
    const result = {
      agentId,
      task,
      context,
      timestamp: new Date().toISOString(),
      status: 'completed',
      toolsUsed: [],
      result: null
    };
    
    // Find and execute appropriate tool
    let bestTool = null;
    
    for (const toolName of agent.tools) {
      const tool = this.tools.get(toolName);
      if (tool && (task.toLowerCase().includes(tool.name.replace('_', ' ')) ||
                   task.toLowerCase().includes(tool.name.replace('_', '')))) {
        bestTool = tool;
        break;
      }
    }
    
    // Use 'execute_task' as fallback
    if (!bestTool) {
      bestTool = this.tools.get('execute_task');
    }
    
    if (bestTool) {
      try {
        result.result = await bestTool.handler(task, context);
        result.toolsUsed.push(bestTool.name);
      } catch (error) {
        result.status = 'error';
        result.error = error.message;
      }
    }
    
    // Update agent state
    agent.state.status = 'idle';
    agent.state.completedTasks++;
    
    // Log execution
    this.executionLog.push(result);
    
    return result;
  }
  
  getAgentMemory(agentId) {
    const agent = this.agents.get(agentId);
    return agent ? agent.state.memory : null;
  }
  
  storeAgentMemory(agentId, key, value, type = 'short-term') {
    const agent = this.agents.get(agentId);
    if (!agent) return { success: false, error: 'Agent not found' };
    
    if (type === 'long-term') {
      agent.state.memory.longTerm.set(key, value);
    } else {
      agent.state.memory.shortTerm.set(key, { value, timestamp: Date.now() });
    }
    
    return { success: true, key, type };
  }
  
  getStatus() {
    return {
      framework: {
        name: this.name,
        version: this.version,
        toolsCount: this.tools.size,
        agentsCount: this.agents.size
      },
      agents: Array.from(this.agents.entries()).map(([id, agent]) => ({
        id: agent.id,
        name: agent.name,
        role: agent.role,
        status: agent.state.status,
        completedTasks: agent.state.completedTasks,
        tools: agent.tools,
        createdAt: agent.createdAt
      })),
      tools: Array.from(this.tools.keys()),
      memory: {
        shortTermItems: this.memory.shortTerm.size,
        longTermItems: this.memory.longTerm.size,
        episodicCount: this.memory.episodic.length
      },
      executionLogCount: this.executionLog.length
    };
  }
  
  // Reasoning capabilities
  reasoning = {
    // Deductive reasoning
    deduct: (premise, rules) => {
      const conclusions = [];
      for (const rule of rules) {
        if (premise.includes(rule.condition)) {
          conclusions.push(rule.conclusion);
        }
      }
      return { type: 'deductive', premise, conclusions };
    },
    
    // Inductive reasoning  
    induce: (observations) => {
      const patterns = [];
      // Simple pattern detection
      if (observations.length > 1) {
        patterns.push(`Observed ${observations.length} similar events`);
      }
      return { type: 'inductive', observations, patterns };
    },
    
    // Abductive reasoning (best explanation)
    abduct: (observation, hypotheses) => {
      let best = { hypothesis: null, score: 0 };
      for (const h of hypotheses) {
        // Simple scoring
        const score = h.explanation?.length || 0;
        if (score > best.score) {
          best = { hypothesis: h, score };
        }
      }
      return { type: 'abductive', observation, bestExplanation: best.hypothesis };
    }
  };
}

// Export
module.exports = { OpenClawAgentFramework };

// CLI
if (require.main === module) {
  const framework = new OpenClawAgentFramework();
  
  console.log('\n🤖 OpenClaw Agent Framework - Demo\n');
  
  // Create a test agent
  console.log('1. Creating test agent...');
  const createResult = framework.createAgent({
    id: 'test_agent',
    name: 'TestAgent',
    role: 'researcher',
    goals: ['Analyze data', 'Search memory', 'Execute tasks']
  });
  console.log(JSON.stringify(createResult, null, 2));
  
  // Execute a task
  console.log('\n2. Executing task...');
  const execResult = framework.executeTask('test_agent', 'search for information about AI agents');
  console.log(JSON.stringify(execResult, null, 2));
  
  // Show status
  console.log('\n3. Framework Status:');
  console.log(JSON.stringify(framework.getStatus(), null, 2));
  
  // Test reasoning
  console.log('\n4. Reasoning Demo:');
  console.log(JSON.stringify(framework.reasoning.deduct('AI is smart', [
    { condition: 'AI', conclusion: 'AI can learn' },
    { condition: 'smart', conclusion: 'AI is intelligent' }
  ]), null, 2));
  
  console.log('\n✅ Agent Framework demo complete!');
}
