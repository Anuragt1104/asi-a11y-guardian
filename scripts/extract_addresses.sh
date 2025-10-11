#!/usr/bin/env bash
# Extract agent addresses from logs
set -euo pipefail

PROJECT_ROOT="/Users/anuragtiwari/asi-a11y-guardian"
LOGS_DIR="$PROJECT_ROOT/logs"

echo "📋 Extracting Agent Addresses from Logs..."
echo ""

if [ ! -d "$LOGS_DIR" ]; then
    echo "❌ Logs directory not found. Start agents first with: ./scripts/run_all_agents.sh"
    exit 1
fi

echo "Copy these values to your .env file:"
echo "-----------------------------------"
echo ""

# Extract addresses
ORCH_ADDR=$(grep -h "Agent address:" "$LOGS_DIR/orchestrator.log" 2>/dev/null | tail -1 | awk '{print $NF}' || echo "NOT_FOUND")
FETCHER_ADDR=$(grep -h "Agent address:" "$LOGS_DIR/fetcher.log" 2>/dev/null | tail -1 | awk '{print $NF}' || echo "NOT_FOUND")
ANALYZER_ADDR=$(grep -h "Agent address:" "$LOGS_DIR/analyzer.log" 2>/dev/null | tail -1 | awk '{print $NF}' || echo "NOT_FOUND")
METTA_ADDR=$(grep -h "Agent address:" "$LOGS_DIR/metta.log" 2>/dev/null | tail -1 | awk '{print $NF}' || echo "NOT_FOUND")
RESOURCE_ADDR=$(grep -h "Agent address:" "$LOGS_DIR/resource.log" 2>/dev/null | tail -1 | awk '{print $NF}' || echo "NOT_FOUND")
GATEWAY_ADDR=$(grep -h "Agent address:" "$LOGS_DIR/gateway.log" 2>/dev/null | tail -1 | awk '{print $NF}' || echo "NOT_FOUND")

echo "# Agent Addresses"
echo "ORCHESTRATOR_ADDR=$ORCH_ADDR"
echo "ORCH_FETCHER_ADDR=$FETCHER_ADDR"
echo "ORCH_ANALYZER_ADDR=$ANALYZER_ADDR"
echo "ORCH_METTA_ADDR=$METTA_ADDR"
echo "ORCH_RESOURCES_ADDR=$RESOURCE_ADDR"
echo ""
echo "# Gateway address (for testing)"
echo "GATEWAY_ADDR=$GATEWAY_ADDR"
echo ""
echo "-----------------------------------"
echo ""

if [[ "$ORCH_ADDR" == "NOT_FOUND" ]]; then
    echo "⚠️  Some addresses not found. Make sure agents are running:"
    echo "   ./scripts/run_all_agents.sh"
    echo ""
    echo "   Wait a few seconds, then try again."
else
    echo "✅ All addresses extracted!"
    echo ""
    echo "Next steps:"
    echo "  1. Copy the addresses above to your .env file"
    echo "  2. Restart orchestrator and gateway:"
    echo "     ./scripts/restart_main_agents.sh"
fi

