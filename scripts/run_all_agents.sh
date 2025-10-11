#!/usr/bin/env bash
# Run all A11y Guardian agents in the background for local testing
set -euo pipefail

PROJECT_ROOT="/Users/anuragtiwari/asi-a11y-guardian"
VENV_ACTIVATE="$PROJECT_ROOT/.venv/bin/activate"

echo "🚀 Starting A11y Guardian Agents..."

# Activate virtual environment
source "$VENV_ACTIVATE"

# Create logs directory if it doesn't exist
mkdir -p "$PROJECT_ROOT/logs"

# Function to start an agent
start_agent() {
    local agent_name=$1
    local module_path=$2
    local log_file="$PROJECT_ROOT/logs/${agent_name}.log"
    
    echo "  Starting $agent_name..."
    nohup python -m "$module_path" > "$log_file" 2>&1 &
    echo $! > "$PROJECT_ROOT/logs/${agent_name}.pid"
    echo "    ✓ $agent_name started (PID: $(cat $PROJECT_ROOT/logs/${agent_name}.pid))"
}

# Start all agents
start_agent "fetcher" "src.fetcher_agent.agent"
start_agent "analyzer" "src.analyzer_agent.agent"
start_agent "metta" "src.metta_agent.agent"
start_agent "resource" "src.resource_agent.agent"
start_agent "orchestrator" "src.orchestrator_agent.agent"
start_agent "gateway" "src.gateway_agent.agent"

echo ""
echo "✅ All agents started!"
echo ""
echo "📝 Next steps:"
echo "  1. Wait ~5 seconds for agents to initialize"
echo "  2. Check logs in ./logs/ directory"
echo "  3. Extract agent addresses from logs: grep 'Agent address' logs/*.log"
echo "  4. Update .env with agent addresses"
echo "  5. Restart orchestrator and gateway: ./scripts/restart_main_agents.sh"
echo ""
echo "To stop all agents: ./scripts/stop_all_agents.sh"
echo "To view logs: tail -f logs/*.log"

