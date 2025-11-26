#!/bin/bash
# Quick test script for n8n + Python backend integration

echo "======================================"
echo "Twitter Support Bot - n8n Test Script"
echo "======================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python backend is running
echo -n "Checking Python backend... "
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Running${NC}"
else
    echo -e "${RED}✗ Not running${NC}"
    echo "Start it with: cd '/Users/jm/API Bot' && source .venv/bin/activate && python webhook_server.py"
    exit 1
fi

# Check if n8n is running
echo -n "Checking n8n... "
if curl -s http://localhost:5678/ > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Running${NC}"
else
    echo -e "${RED}✗ Not running${NC}"
    echo "Start it with: n8n start"
    exit 1
fi

echo ""
echo "======================================"
echo "Running Test Scenarios"
echo "======================================"
echo ""

# Test 1: New Complaint
echo -e "${YELLOW}Test 1: New Complaint${NC}"
curl -X POST http://localhost:5678/webhook-test/twitter-message \
  -H "Content-Type: application/json" \
  -d '{
    "username": "angry_user",
    "message": "My withdrawal is stuck for 3 days!",
    "is_dm": false
  }' 2>/dev/null
echo ""
echo ""
sleep 2

# Test 2: Has Ticket
echo -e "${YELLOW}Test 2: User Has Ticket${NC}"
curl -X POST http://localhost:5678/webhook-test/twitter-message \
  -H "Content-Type: application/json" \
  -d '{
    "username": "patient_user",
    "message": "I raised a ticket but no response",
    "is_dm": false
  }' 2>/dev/null
echo ""
echo ""
sleep 2

# Test 3: DM with Ticket (Escalation)
echo -e "${YELLOW}Test 3: DM with Ticket Number (ESCALATION!)${NC}"
curl -X POST http://localhost:5678/webhook-test/twitter-message \
  -H "Content-Type: application/json" \
  -d '{
    "username": "patient_user",
    "message": "My ticket number is #12345",
    "is_dm": true
  }' 2>/dev/null
echo ""
echo ""
sleep 2

# Test 4: Credentials Shared
echo -e "${YELLOW}Test 4: Credentials Shared (Security Warning)${NC}"
curl -X POST http://localhost:5678/webhook-test/twitter-message \
  -H "Content-Type: application/json" \
  -d '{
    "username": "naive_user",
    "message": "My email is user@gmail.com please help",
    "is_dm": false
  }' 2>/dev/null
echo ""
echo ""

echo "======================================"
echo -e "${GREEN}All tests completed!${NC}"
echo "======================================"
echo ""
echo "Check:"
echo "  - n8n executions tab for results"
echo "  - Python backend logs for intent classification"
echo "  - Database: sqlite3 data/conversations.db"
echo ""
