# ✅ n8n Setup Checklist

Use this checklist to set up and test the n8n workflow.

---

## 📦 Installation

### 1. Install n8n
```bash
npm install -g n8n
```
- [ ] Installed successfully
- [ ] Verified with `n8n --version`

---

## 🚀 Startup

### 2. Start Services

**Terminal 1: Start n8n**
```bash
n8n start
```
- [ ] n8n running
- [ ] Accessible at http://localhost:5678
- [ ] No errors in terminal

**Terminal 2: Start Python Backend**
```bash
cd "/Users/jm/API Bot"
source .venv/bin/activate
python webhook_server.py
```
- [ ] Backend running
- [ ] Shows "Uvicorn running on http://0.0.0.0:8000"
- [ ] No errors in terminal

---

## 📥 Import Workflow

### 3. Import the Workflow File

1. Open browser → http://localhost:5678
   - [ ] n8n UI loaded

2. Click "Add workflow" (top left)
   - [ ] New workflow created

3. Click 3-dot menu (⋮) → "Import from File"
   - [ ] Import dialog opened

4. Select file: `/Users/jm/API Bot/n8n_workflow.json`
   - [ ] File imported successfully

5. Check nodes are visible:
   - [ ] Webhook (Manual Trigger)
   - [ ] Call Python Backend
   - [ ] Success?
   - [ ] Format Response
   - [ ] Handle Error

---

## 🧪 Test Workflow

### 4. Execute Workflow

1. Click "Execute Workflow" button
   - [ ] Workflow is in execution mode
   - [ ] Waiting for webhook trigger

2. Get webhook URL
   - [ ] Click on "Webhook (Manual Trigger)" node
   - [ ] Copy the Test URL
   - [ ] Should be: `http://localhost:5678/webhook-test/twitter-message`

---

### 5. Send Test Request

**Option A: Use Terminal**
```bash
curl -X POST http://localhost:5678/webhook-test/twitter-message \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "message": "My withdrawal is stuck!",
    "is_dm": false
  }'
```
- [ ] Command executed
- [ ] Got JSON response

**Option B: Use Test Script**
```bash
cd "/Users/jm/API Bot"
./test_n8n.sh
```
- [ ] All 4 scenarios tested
- [ ] All returned responses

---

## ✅ Verify Results

### 6. Check n8n Execution

In n8n UI:
- [ ] Workflow executed successfully (green checkmarks)
- [ ] Click "Webhook" node - see input data
- [ ] Click "Call Python Backend" - see response from backend
- [ ] Click "Success?" - routed to TRUE path
- [ ] Click "Format Response" - see final formatted output

### 7. Check Python Backend

In Python terminal:
- [ ] See log: "Processing Tweet from @test_user"
- [ ] See intent classification
- [ ] See response generated
- [ ] No errors

### 8. Check Database

```bash
cd "/Users/jm/API Bot"
sqlite3 data/conversations.db "SELECT username, intent, response FROM conversations ORDER BY created_at DESC LIMIT 5;"
```
- [ ] Database shows test conversations
- [ ] Correct intents detected
- [ ] Responses stored

---

## 🎯 Test All Scenarios

### 9. Run Complete Test Suite

Run each scenario and verify:

**Scenario 1: New Complaint**
```bash
curl -X POST http://localhost:5678/webhook-test/twitter-message \
  -H "Content-Type: application/json" \
  -d '{"username":"angry_user","message":"My withdrawal is stuck!","is_dm":false}'
```
- [ ] Intent: `new_complaint`
- [ ] Response: "Please email help@mudrex.com..."

**Scenario 2: Has Ticket**
```bash
curl -X POST http://localhost:5678/webhook-test/twitter-message \
  -H "Content-Type: application/json" \
  -d '{"username":"patient_user","message":"I raised ticket already","is_dm":false}'
```
- [ ] Intent: `has_ticket`
- [ ] Response: "Please DM the ticket number..."

**Scenario 3: DM with Ticket (ESCALATION)**
```bash
curl -X POST http://localhost:5678/webhook-test/twitter-message \
  -H "Content-Type: application/json" \
  -d '{"username":"patient_user","message":"#12345","is_dm":true}'
```
- [ ] Intent: `dm_ticket_shared`
- [ ] Response: "Escalated ticket #12345..."
- [ ] Python log: "[MOCK SLACK] Would send escalation"
- [ ] `escalated: true` in response

**Scenario 4: Credentials Shared**
```bash
curl -X POST http://localhost:5678/webhook-test/twitter-message \
  -H "Content-Type: application/json" \
  -d '{"username":"naive_user","message":"user@gmail.com","is_dm":false}'
```
- [ ] Intent: `credentials_shared`
- [ ] Response: "⚠️ Please don't share..."

---

## 🎉 Success Criteria

All checkboxes above should be checked. You should have:

- [ ] n8n running and accessible
- [ ] Python backend responding
- [ ] Workflow imported and executing
- [ ] All 4+ test scenarios working
- [ ] Responses showing in n8n
- [ ] Logs showing in Python terminal
- [ ] Data stored in database
- [ ] Escalation mock working

---

## 📊 View Execution History

### 10. Check Past Executions

In n8n:
1. Click "Executions" in left sidebar
   - [ ] See list of all test runs

2. Click any execution
   - [ ] See complete data flow
   - [ ] See input/output of each node
   - [ ] See timing information

3. Filter by status
   - [ ] All should be "Success" (green)

---

## 🔧 Troubleshooting

If something doesn't work:

**Webhook not triggering:**
- [ ] Workflow in "Execute" mode (not just saved)
- [ ] Using Test URL (not Production URL)
- [ ] Webhook node is active

**Backend connection failed:**
- [ ] Python backend is running (check terminal)
- [ ] URL is correct: `http://localhost:8000/webhook/twitter`
- [ ] No firewall blocking localhost

**Wrong responses:**
- [ ] Check Python logs for intent classification
- [ ] Verify input JSON format is correct
- [ ] Check `.env` file if using Gemini

---

## 🚀 Ready for Production

Once all tests pass:

### 11. Switch to Production URL

In n8n:
1. Click "Webhook" node
2. Switch from "Test URL" to "Production URL"
   - [ ] Production webhook URL copied

3. Save workflow
   - [ ] Workflow saved

4. Activate workflow
   - [ ] Toggle "Active" switch (top right)
   - [ ] Workflow status: ACTIVE

Now the workflow will run automatically when triggered!

---

## 📝 Next Steps

After successful testing:

- [ ] Add Gemini API key to `.env` for better classification
- [ ] Set up Slack webhook for real escalations
- [ ] When you get Twitter API, add Twitter trigger node
- [ ] Deploy to production (Railway, Heroku, etc.)

---

## 💡 Quick Commands Reference

```bash
# Start n8n
n8n start

# Start backend
cd "/Users/jm/API Bot" && source .venv/bin/activate && python webhook_server.py

# Run test script
./test_n8n.sh

# Check database
sqlite3 data/conversations.db "SELECT * FROM conversations;"

# Stop n8n
Ctrl+C in n8n terminal

# Stop backend
Ctrl+C in Python terminal
```

---

**All set? Start with Step 1 and work your way down! 🎯**
