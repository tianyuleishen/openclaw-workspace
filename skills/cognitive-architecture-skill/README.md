# Cognitive Architecture Skill for OpenClaw

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![AI](https://img.shields.io/badge/AI-Cognitive_Architecture-green)](https://github.com/topics/cognitive-architecture)

Advanced cognitive architecture components for OpenClaw agents including memory systems, reasoning engines, and task coordination capabilities.

## 🚀 Overview

The Cognitive Architecture Skill enhances OpenClaw agents with sophisticated cognitive capabilities:

- **Memory Systems**: Five-tier memory management (short-term, long-term, episodic, semantic, procedural)
- **Reasoning Engine**: Deductive, inductive, and abductive reasoning with problem-solving capabilities
- **Coordination System**: Multi-agent task management and communication

## ✨ Features

### Memory Management
- **Short-term Memory**: Volatile storage with configurable TTL
- **Long-term Memory**: Persistent categorized storage
- **Episodic Memory**: Sequential event tracking
- **Semantic Memory**: Concept and relationship storage
- **Procedural Memory**: Process and procedure storage

### Reasoning Capabilities
- **Deductive Reasoning**: Derive specific conclusions from general rules
- **Inductive Reasoning**: Identify patterns from specific observations
- **Abductive Reasoning**: Find best explanations for observations
- **Problem Solving**: Means-end analysis and state transition planning

### Coordination Features
- **Agent Management**: Registration, discovery, and lifecycle
- **Task Assignment**: Intelligent allocation based on capabilities
- **Communication**: Message passing and broadcasting
- **Contract Management**: Agreement and contract handling

## 📦 Installation

### Prerequisites
- OpenClaw v2.0+
- Node.js 18+

### Install via ClawHub (Recommended)
```bash
# Navigate to your OpenClaw workspace
cd ~/.openclaw/workspace

# Install the skill via ClawHub
clawhub install cognitive-architecture
```

### Manual Installation
```bash
# Navigate to your OpenClaw workspace skills directory
cd ~/.openclaw/workspace/skills

# Clone the repository
git clone https://github.com/tianyuleishen/cognitive-architecture-skill.git cognitive-architecture

# Or create the directory structure manually
mkdir -p cognitive-architecture
cd cognitive-architecture
```

Then copy the following files:
- `SKILL.md` - Skill definition and metadata
- `memory_system.js` - Memory management implementation
- `reasoning_engine.js` - Reasoning engine implementation
- `coordination_system.js` - Coordination system implementation
- `examples/demo.js` - Example usage demonstration

## ⚙️ Configuration

The skill requires no special configuration to run. However, you can customize the following options by modifying the JavaScript instantiation:

```javascript
// Customize memory system
const memorySystem = new MemorySystem({
  shortTermTTL: 300000,     // 5 minutes default
  maxEpisodicSize: 1000,    // 1000 episodes maximum
});

// Customize coordination system
const coordinationSystem = new CoordinationSystem({
  taskTimeout: 300000,      // 5 minutes default
  maxMessageHistory: 1000,  // 1000 messages maximum
});
```

## 🛠️ Usage

### Basic Usage
```javascript
const MemorySystem = require('./skills/cognitive-architecture/memory_system');
const ReasoningEngine = require('./skills/cognitive-architecture/reasoning_engine');
const CoordinationSystem = require('./skills/cognitive-architecture/coordination_system');

// Initialize cognitive components
const memory = new MemorySystem();
const reasoning = new ReasoningEngine(memory);
const coordination = new CoordinationSystem();

// Use the components as needed
```

### Memory System Usage
```javascript
// Store information
memory.storeShortTerm('current_weather', { city: 'Shanghai', temp: 22, condition: 'sunny' });
memory.storeLongTerm('population_fact', { shanghai: 29000000, beijing: 21000000 }, 'demographics');

// Retrieve information
const weather = memory.retrieve('current_weather');
const population = memory.retrieve('population_fact');

// Search memory
const results = memory.search('AI');
```

### Reasoning Engine Usage
```javascript
// Add facts and rules
reasoning.addFact('agent', 'has_capability', 'research', 0.9);
reasoning.addRule(
  { subject: 'agent', predicate: 'has_capability', object: 'research' },
  { action: 'assign_research_task', priority: 'medium' },
  5
);

// Perform reasoning
const deductions = reasoning.deduct();
const hypotheses = reasoning.induct(observations);
const solution = reasoning.solveProblem(initialState, goalState, operators);
```

### Coordination System Usage
```javascript
// Register an agent
await coordination.registerAgent(agent);

// Assign a task
const assignment = await coordination.assignTask(task);

// Send messages between agents
const result = coordination.sendMessage(fromAgentId, toAgentId, message);
```

## 🧪 Examples

See the `examples/` directory for complete usage examples:

```bash
node skills/cognitive-architecture/examples/demo.js
```

## 🧠 Architecture

The cognitive architecture follows a modular design:

```
┌─────────────────────────────────────────┐
│           Cognitive Architecture        │
├─────────────────┬───────────────────────┤
│   Memory System │   Reasoning Engine    │
│                 │                       │
│ • Short-term    │ • Deductive Reasoning │
│ • Long-term     │ • Inductive Reasoning │
│ • Episodic      │ • Abductive Reasoning │
│ • Semantic      │ • Problem Solving     │
│ • Procedural    │                       │
├─────────────────┼───────────────────────┤
│    Coordination System                   │
│                                         │
│ • Agent Management                      │
│ • Task Assignment                       │
│ • Communication                         │
│ • Contract Management                   │
└─────────────────────────────────────────┘
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🔄 Upgrades and Migration

The cognitive architecture skill includes a comprehensive migration system to ensure memory documents and data are preserved during upgrades.

### Safe Upgrades
- Automatic backup before any upgrade
- Memory preservation during version updates
- Safe rollback capabilities
- Version compatibility management

### Upgrade Commands
```bash
# Check for updates
node migration/upgrade.js check

# Perform a dry run
node migration/upgrade.js dry-run

# Upgrade to latest version
node migration/upgrade.js upgrade

# Upgrade to specific version
node migration/upgrade.js upgrade v1.2.0
```

For more details, see the [Migration System Documentation](migration/README.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- [GitHub Issues](https://github.com/tianyuleishen/cognitive-architecture-skill/issues)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Community Discord](https://discord.gg/clawd)

## 🙏 Acknowledgments

- Built for the OpenClaw ecosystem
- Inspired by cognitive architecture research
- Thanks to the OpenClaw community for feedback and support

---

⭐ If you find this skill useful, please give it a star!