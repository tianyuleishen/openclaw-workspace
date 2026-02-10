// Cognitive Architecture Demo
// Demonstrates the use of memory system, reasoning engine, and coordination system

const MemorySystem = require('../memory_system');
const ReasoningEngine = require('../reasoning_engine');
const CoordinationSystem = require('../coordination_system');

// Basic Agent class for demo purposes
class DemoAgent {
  constructor(id, name, capabilities = []) {
    this.id = id;
    this.name = name;
    this.capabilities = capabilities;
    this.status = 'idle';
  }

  async executeTask(task) {
    console.log(`Agent ${this.name} executing task: ${task.description}`);
    
    // Simulate task execution based on type
    switch(task.type) {
      case 'research':
        await this.simulateWork(2000);
        return {
          success: true,
          data: `Research completed on ${task.topic}`,
          findings: ['Finding 1', 'Finding 2', 'Finding 3']
        };
      case 'analysis':
        await this.simulateWork(1500);
        return {
          success: true,
          analysis: `Analysis of ${task.subject}`,
          results: { metric1: 0.85, metric2: 0.92 }
        };
      case 'calculation':
        await this.simulateWork(1000);
        return {
          success: true,
          result: task.a + task.b
        };
      default:
        await this.simulateWork(1000);
        return {
          success: true,
          message: `Task completed: ${task.description}`
        };
    }
  }

  receiveMessage(from, message) {
    console.log(`Agent ${this.name} received message from ${from}:`, message.type || message.content?.type);
    return { received: true, agentId: this.id };
  }

  async simulateWork(duration) {
    return new Promise(resolve => setTimeout(resolve, duration));
  }
}

async function runDemo() {
  console.log('🧠 Starting Cognitive Architecture Demo...\n');

  // Initialize cognitive components
  const memorySystem = new MemorySystem({
    shortTermTTL: 30000, // 30 seconds
    maxEpisodicSize: 100
  });
  
  const reasoningEngine = new ReasoningEngine(memorySystem);
  
  const coordinationSystem = new CoordinationSystem({
    taskTimeout: 60000, // 1 minute
    maxMessageHistory: 50
  });

  console.log('✅ Cognitive components initialized\n');

  // 1. DEMONSTRATE MEMORY SYSTEM
  console.log('💾 Testing Memory System...\n');
  
  // Store information in different memory types
  memorySystem.storeShortTerm('current_weather', { city: 'Shanghai', temp: 22, condition: 'sunny' }, 60000);
  memorySystem.storeLongTerm('population_fact', { shanghai: 29000000, beijing: 21000000 }, 'demographics');
  memorySystem.storeEpisode('user_interaction', { userId: 'user123', action: 'query', result: 'success' });
  memorySystem.storeSemantic('AI_agent', 'An artificial intelligence designed to perform tasks autonomously', ['cognitive_architecture', 'machine_learning']);
  memorySystem.storeProcedure('data_analysis', [
    'collect_data', 'clean_data', 'analyze_patterns', 'generate_insights'
  ]);

  // Retrieve information
  const weather = memorySystem.retrieve('current_weather');
  console.log('Short-term memory retrieval:', weather);
  
  const population = memorySystem.retrieve('population_fact');
  console.log('Long-term memory retrieval:', population);
  
  const relatedConcepts = memorySystem.findRelated('AI_agent');
  console.log('Related concepts:', relatedConcepts);
  
  // Search memory
  const searchResults = memorySystem.search('AI');
  console.log('Memory search results:', searchResults.length, 'items found\n');

  // 2. DEMONSTRATE REASONING ENGINE
  console.log('🧩 Testing Reasoning Engine...\n');
  
  // Add facts
  reasoningEngine.addFact('agent', 'has_capability', 'research');
  reasoningEngine.addFact('agent', 'has_capability', 'analysis');
  reasoningEngine.addFact('system', 'is_healthy', true);
  
  // Add rules
  reasoningEngine.addRule(
    { subject: 'system', predicate: 'is_healthy', object: true },
    { action: 'continue_operation', priority: 'high' },
    10
  );
  
  reasoningEngine.addRule(
    { subject: 'agent', predicate: 'has_capability', object: 'research' },
    { action: 'assign_research_task', priority: 'medium' },
    5
  );

  // Perform deduction
  const deductions = reasoningEngine.deduct();
  console.log('Deductions:', deductions);

  // Perform induction
  const observations = [
    { condition: 'high_load', action: 'scale_up' },
    { condition: 'high_load', action: 'scale_up' },
    { condition: 'high_load', action: 'scale_up' }
  ];
  const hypotheses = reasoningEngine.induct(observations);
  console.log('Inductive hypotheses:', hypotheses);

  // Problem solving
  const initialState = { battery: 20, tasks: 5, energy: 30 };
  const goalState = { battery: '>50', tasks: 0 };
  const operators = [
    {
      name: 'charge_battery',
      description: 'Charge the battery',
      preconditions: [{ attribute: 'battery', value: 100, comparison: 'less_than' }],
      effects: [{ attribute: 'battery', value: 100, operation: 'set' }]
    },
    {
      name: 'complete_task',
      description: 'Complete one task',
      preconditions: [{ attribute: 'tasks', value: 0, comparison: 'greater_than' }],
      effects: [
        { attribute: 'tasks', value: 1, operation: 'add' }, // subtract 1 (negative value)
        { attribute: 'energy', value: 5, operation: 'add' } // subtract 5 energy
      ]
    }
  ];

  const problemSolution = reasoningEngine.solveProblem(initialState, goalState, operators);
  console.log('Problem solution:', problemSolution.success ? 'Found!' : 'Not found');
  if (problemSolution.solution) {
    console.log('Solution path:', problemSolution.solution);
  }
  console.log('');

  // 3. DEMONSTRATE COORDINATION SYSTEM
  console.log('🤝 Testing Coordination System...\n');
  
  // Create demo agents
  const researchAgent = new DemoAgent('ra-001', 'ResearchAgent', ['research', 'analysis']);
  const calcAgent = new DemoAgent('ca-001', 'CalculatorAgent', ['calculation', 'math']);
  const generalAgent = new DemoAgent('ga-001', 'GeneralAgent', ['general', 'coordination']);

  // Register agents
  await coordinationSystem.registerAgent(researchAgent);
  await coordinationSystem.registerAgent(calcAgent);
  await coordinationSystem.registerAgent(generalAgent);

  // Assign tasks
  const researchTask = {
    id: 'task-001',
    description: 'Research AI trends',
    type: 'research',
    topic: 'cognitive_architecture',
    requiredCapabilities: ['research']
  };

  const calcTask = {
    id: 'task-002',
    description: 'Calculate sum',
    type: 'calculation',
    a: 15,
    b: 25,
    requiredCapabilities: ['calculation']
  };

  console.log('Assigning research task...');
  const researchAssignment = await coordinationSystem.assignTask(researchTask);
  console.log('Research task assignment:', researchAssignment);

  console.log('\nAssigning calculation task...');
  const calcAssignment = await coordinationSystem.assignTask(calcTask);
  console.log('Calculation task assignment:', calcAssignment);

  // Wait a bit for tasks to complete
  await new Promise(resolve => setTimeout(resolve, 4000));

  // Check system status
  const status = coordinationSystem.getStatus();
  console.log('\n📊 System Status:');
  console.log(`- Total Agents: ${status.totalAgents}`);
  console.log(`- Pending Tasks: ${status.pendingTasks}`);
  console.log(`- Active Tasks: ${status.activeTasks}`);
  console.log(`- Active Agreements: ${status.activeAgreements}`);

  console.log('\n🎯 Cognitive Architecture Demo Completed Successfully!');
  console.log('\nSummary of Capabilities Demonstrated:');
  console.log('• Memory System: Short-term, long-term, episodic, semantic, and procedural memory');
  console.log('• Reasoning Engine: Deduction, induction, abduction, and problem solving');
  console.log('• Coordination System: Agent registration, task assignment, and communication');
}

// Run the demo if this file is executed directly
if (require.main === module) {
  runDemo().catch(console.error);
}

module.exports = {
  MemorySystem,
  ReasoningEngine, 
  CoordinationSystem,
  DemoAgent,
  runDemo
};