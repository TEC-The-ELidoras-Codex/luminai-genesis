#!/bin/bash
# Test LuminAI Genesis Ollama integration
#
# Usage: ./scripts/test_ollama_chat.sh [session_id] [message]

SESSION_ID="${1:-test-session-$(date +%s)}"
MESSAGE="${2:-I'm feeling stressed and need grounding.}"

echo "Testing /api/chat endpoint..."
echo "Session: $SESSION_ID"
echo "Message: $MESSAGE"
echo ""

curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d @- <<EOF | jq .
{
  "session_id": "$SESSION_ID",
  "message": "$MESSAGE",
  "model": "llama3.2"
}
EOF

echo ""
echo "To retrieve session history:"
echo "curl http://localhost:8000/api/chat/sessions/$SESSION_ID | jq ."
