#!/usr/bin/env bash
# Stop all A11y Guardian agents
set -euo pipefail

PROJECT_ROOT="/Users/anuragtiwari/asi-a11y-guardian"

echo "🛑 Stopping A11y Guardian Agents..."

# Function to stop an agent
stop_agent() {
    local agent_name=$1
    local pid_file="$PROJECT_ROOT/logs/${agent_name}.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p "$pid" > /dev/null 2>&1; then
            echo "  Stopping $agent_name (PID: $pid)..."
            kill "$pid" 2>/dev/null || true
            rm "$pid_file"
            echo "    ✓ $agent_name stopped"
        else
            echo "  ⚠️  $agent_name (PID: $pid) not running"
            rm "$pid_file"
        fi
    else
        echo "  ⚠️  $agent_name PID file not found"
    fi
}

# Stop all agents
stop_agent "gateway"
stop_agent "orchestrator"
stop_agent "resource"
stop_agent "metta"
stop_agent "analyzer"
stop_agent "fetcher"

echo ""
echo "✅ All agents stopped!"

