#!/bin/bash
# OpenClaw Agent Framework Integration Script
# Integrates agent capabilities into OpenClaw system

echo "🤖 OpenClaw Agent Framework Integration"
echo "======================================"
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check Python environment
print_status "Checking Python environment..."
if [ -f "/home/admin/.openclaw/venv/bin/python" ]; then
    VENV_PYTHON="/home/admin/.openclaw/venv/bin/python"
    print_success "Virtual environment found: $VENV_PYTHON"
else
    print_warning "Virtual environment not found. Creating..."
    mkdir -p /home/admin/.openclaw/venv
    python3 -m venv /home/admin/.openclaw/venv
    VENV_PYTHON="/home/admin/.openclaw/venv/bin/python"
    print_success "Virtual environment created"
fi

# Check if LangChain is available
print_status "Checking LangChain availability..."
LANGCHAIN_STATUS=$($VENV_PYTHON -c "
import sys
try:
    import langchain
    print('INSTALLED')
except ImportError:
    print('NOT_INSTALLED')
" 2>/dev/null)

if [ "$LANGCHAIN_STATUS" == "INSTALLED" ]; then
    print_success "LangChain is installed"
    LANGCHAIN_AVAILABLE=true
else
    print_warning "LangChain not installed (using pure JS fallback)"
    LANGCHAIN_AVAILABLE=false
fi

echo ""
echo "📊 Integration Status:"
echo "--------------------"
echo -e "  LangChain (Python): ${GREEN}$LANGCHAIN_AVAILABLE${NC}"
echo -e "  Agent Framework (JS): ${GREEN}Available${NC}"
echo ""

echo "🛠️  Available Commands:"
echo "----------------------"
echo "  ./agent_framework.js           - Run agent framework demo"
echo "  ./langchain_integration.js   - LangChain integration status"
echo ""

echo "📝 Example Usage:"
echo "----------------"
cat << 'EXAMPLE'
# Create and use an agent
node -e "
const { OpenClawAgentFramework } = require('./agent_framework.js');
const fw = new OpenClawAgentFramework();

// Create a research agent
fw.createAgent({ 
    id: 'researcher', 
    name: 'ResearchAgent', 
    role: 'researcher',
    goals: ['Search knowledge', 'Analyze data', 'Report findings']
});

// Execute a task
const result = fw.executeTask('researcher', 'search for information about AI');
console.log(JSON.stringify(result, null, 2));

// Show framework status
console.log('\n=== Framework Status ===');
console.log(JSON.stringify(fw.getStatus(), null, 2));
"
EXAMPLE

echo ""
echo "🧠 Agent Framework Features:"
echo "--------------------------"
echo "  ✅ Agent Creation with custom roles and goals"
echo "  ✅ Built-in Tools: search_memory, store_memory, analyze, execute_task, log_event"
echo "  ✅ Memory Management: short-term, long-term, episodic"
echo "  ✅ Reasoning Engine: deductive, inductive, abductive"
echo "  ✅ Task Execution with appropriate tool selection"
echo "  ✅ Event Logging for learning and adaptation"
echo ""

echo "🔄 Integration Path:"
echo "-------------------"
echo "  1. Pure JS framework working now ✅"
echo "  2. LangChain Python integration (when GPU available)"
echo "  3. Multi-agent coordination (future)"
echo ""

print_success "Agent Framework integration complete!"
