#!/usr/bin/env bash
# Restart orchestrator and gateway agents (useful after updating .env)
set -euo pipefail

PROJECT_ROOT="/Users/anuragtiwari/asi-a11y-guardian"
VENV_ACTIVATE="$PROJECT_ROOT/.venv/bin/activate"

echo "🔄 Restarting Main Agents (Orchestrator & Gateway)..."

# Activate virtual environment
source "$VENV_ACTIVATE"

# Create logs directory if it doesn't exist
mkdir -p "$PROJECT_ROOT/logs"

# Function to stop an agent
stop_agent() {
    local agent_name=$1
    local pid_file="$PROJECT_ROOT/logs/${agent_name}.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p "$pid" > /dev/null 2>&1; then
            echo "  Stopping $agent_name..."
            kill "$pid" 2>/dev/null || true
            rm "$pid_file"
        fi
    fi
}

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

# Stop main agents
stop_agent "orchestrator"
stop_agent "gateway"

# Small delay to ensure clean shutdown
sleep 1

# Start main agents
start_agent "orchestrator" "src.orchestrator_agent.agent"
start_agent "gateway" "src.gateway_agent.agent"

echo ""
echo "✅ Main agents restarted!"
echo "  View logs: tail -f logs/orchestrator.log logs/gateway.log"

