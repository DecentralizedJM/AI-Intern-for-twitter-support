# n8n Setup - Step by Step Guide

## 🎯 What We'll Do

Set up n8n locally to test the Twitter Support Bot workflow **without needing Twitter API** (using manual webhook testing).

## 📋 Prerequisites

- ✅ Python backend installed (you already have this)
- ✅ n8n (we'll install now)
- ✅ Node.js installed on your Mac

---

## Step 1: Install n8n

Open a terminal and run:

```bash
# Install n8n globally
npm install -g n8n
```

**Expected output:**
```
added 500+ packages in 30s
```

**Verify installation:**
```bash
n8n --version
```

Should show something like: `1.x.x`

---

## Step 2: Start n8n

In a new terminal window:

```bash
n8n start
```

**Expected output:**
```
Editor is now accessible via:
http://localhost:5678/
```

**Important:** Keep this terminal running! Don't close it.

---

## Step 3: Start Python Backend

In another terminal window:

```bash
cd "/Users/jm/API Bot"
source .venv/bin/activate
python webhook_server.py
```

**Expected output:**
```
🚀 Starting Twitter Support Bot API...
📍 Webhook URL: http://localhost:8000/webhook/twitter
🧪 Test URL: http://localhost:8000/webhook/test
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Important:** Keep this terminal running too!

---

## Step 4: Open n8n in Browser

1. Open your browser
2. Go to: **http://localhost:5678**
3. You'll see the n8n welcome screen

If this is your first time:
- It may ask you to create an account (local only)
- Or just click "Get Started"

---

## Step 5: Import the Workflow

1. In n8n, click **"Add workflow"** (top left)

2. Click the **3 dots menu** (⋮) in the top right

3. Select **"Import from File"**

4. Navigate to and select:
   ```
   /Users/jm/API Bot/n8n_workflow.json
   ```

5. Click **"Import"**

6. The workflow will load with these nodes:
   - 📥 Webhook (Manual Trigger)
   - 🔗 Call Python Backend
   - ❓ Success?
   - ✅ Format Response
   - ❌ Handle Error

---

## Step 6: Test the Workflow

### 6.1 Activate the Workflow

1. Click **"Execute Workflow"** button (top right)
2. This starts listening for webhook calls

### 6.2 Get the Webhook URL

1. Click on the **"Webhook (Manual Trigger)"** node
2. Copy the **"Test URL"** 
3. It should look like:
   ```
   http://localhost:5678/webhook-test/twitter-message
   ```

### 6.3 Send a Test Request

Open a **new terminal** and run:

```bash
curl -X POST http://localhost:5678/webhook-test/twitter-message \
  -H "Content-Type: application/json" \
  -d '{
    "username": "angry_user",
    "message": "My withdrawal is stuck for 3 days!",
    "is_dm": false
  }'
```

### 6.4 Check the Results

**In n8n:**
- You'll see the workflow execute
- Click on each node to see the data flow
- Final output should show the bot's response

**In Python terminal:**
- You'll see the processing log:
```
============================================================
Processing Tweet from @angry_user
Message: My withdrawal is stuck for 3 days!
============================================================
📊 Intent: new_complaint
💬 Response: We understand your concern...
```

---

## Step 7: Test Different Scenarios

Try these different test cases:

### Scenario 1: User has ticket
```bash
curl -X POST http://localhost:5678/webhook-test/twitter-message \
  -H "Content-Type: application/json" \
  -d '{
    "username": "patient_user",
    "message": "I raised ticket but no response",
    "is_dm": false
  }'
```

### Scenario 2: DM with ticket (ESCALATION!)
```bash
curl -X POST http://localhost:5678/webhook-test/twitter-message \
  -H "Content-Type: application/json" \
  -d '{
    "username": "patient_user",
    "message": "My ticket number is #12345",
    "is_dm": true
  }'
```

**Check Python terminal** - you should see:
```
[MOCK SLACK] Would send escalation for ticket #12345
```

### Scenario 3: Credentials shared
```bash
curl -X POST http://localhost:5678/webhook-test/twitter-message \
  -H "Content-Type: application/json" \
  -d '{
    "username": "naive_user",
    "message": "My email is user@gmail.com please help",
    "is_dm": false
  }'
```

---

## Step 8: View Execution History

1. In n8n, click **"Executions"** tab (left sidebar)
2. See all your test runs
3. Click any execution to see:
   - Input data
   - Output from each node
   - Errors (if any)

---

## 🎯 What You Should See

### Successful Flow:

```
Webhook receives data
    ↓
Calls Python Backend (localhost:8000)
    ↓
Backend returns:
{
  "success": true,
  "intent": "new_complaint",
  "response": "We understand your concern...",
  "escalated": false
}
    ↓
Success? → TRUE
    ↓
Format Response
    ↓
Shows final message
```

---

## 🔍 Troubleshooting

### Issue: "Connection refused" to localhost:8000

**Solution:** Start the Python backend:
```bash
cd "/Users/jm/API Bot"
source .venv/bin/activate
python webhook_server.py
```

### Issue: n8n won't start

**Solution:** Check if port 5678 is in use:
```bash
lsof -i :5678
# If something is using it:
kill -9 <PID>
# Then restart n8n
n8n start
```

### Issue: Webhook not triggering

**Solution:** 
1. Make sure workflow is in "Execute" mode (not just saved)
2. Use the Test URL, not Production URL
3. Check the webhook node is listening

### Issue: Python backend errors

**Solution:**
```bash
# Check if virtual env is activated
which python
# Should show: /Users/jm/API Bot/.venv/bin/python

# If not:
source .venv/bin/activate
```

---

## 📊 Verify Everything Works

Run this complete test:

```bash
# Test 1: Backend is running
curl http://localhost:8000/

# Test 2: n8n webhook receives data
curl -X POST http://localhost:5678/webhook-test/twitter-message \
  -H "Content-Type: application/json" \
  -d '{"username":"test","message":"help","is_dm":false}'

# Test 3: Check database
cd "/Users/jm/API Bot"
sqlite3 data/conversations.db "SELECT username, intent, response FROM conversations ORDER BY created_at DESC LIMIT 3;"
```

---

## 🎉 Success Checklist

- [ ] n8n running on localhost:5678
- [ ] Python backend running on localhost:8000
- [ ] Workflow imported successfully
- [ ] Test webhook trigger works
- [ ] See bot response in n8n output
- [ ] Python logs show intent classification
- [ ] Database stores conversations
- [ ] Escalation test shows Slack notification (mock)

---

## 🚀 Next Steps

Once this works:

1. **Production URL:** 
   - Click "Webhook" node
   - Switch from "Test URL" to "Production URL"
   - This will give you a permanent webhook

2. **Twitter Integration (when you get API):**
   - Add Twitter trigger node instead of webhook
   - Connect to @MudrexHelp
   - Add Twitter reply nodes

3. **Slack Integration:**
   - Add Slack webhook URL to `.env`
   - Test real Slack notifications

---

## 📝 Quick Reference

**Start n8n:**
```bash
n8n start
```

**Start Backend:**
```bash
cd "/Users/jm/API Bot"
source .venv/bin/activate
python webhook_server.py
```

**Test Webhook:**
```bash
curl -X POST http://localhost:5678/webhook-test/twitter-message \
  -H "Content-Type: application/json" \
  -d '{"username":"test","message":"help","is_dm":false}'
```

**View Logs:**
```bash
# Python logs - in terminal running webhook_server.py
# n8n logs - in terminal running n8n
# Database - sqlite3 data/conversations.db
```

---

## 🎓 Understanding the Workflow

**Node 1: Webhook**
- Listens for HTTP POST requests
- Accepts JSON with username, message, is_dm

**Node 2: Call Python Backend**
- Sends data to localhost:8000/webhook/twitter
- Gets back intent and response

**Node 3: Success?**
- Checks if backend returned success: true
- Routes to either success or error handler

**Node 4: Format Response**
- Prepares final output
- Shows bot's response

**Node 5: Handle Error**
- Catches any failures
- Logs error info

---

## 💡 Pro Tips

1. **Keep terminals organized:**
   - Terminal 1: n8n
   - Terminal 2: Python backend
   - Terminal 3: Testing (curl commands)

2. **Use n8n's built-in testing:**
   - Click "Execute Workflow" 
   - Manually input test data
   - No need for curl

3. **Check the flow:**
   - Click each node after execution
   - See the data transform step-by-step
   - Debug easier

4. **Database inspection:**
   ```bash
   sqlite3 data/conversations.db
   .tables
   SELECT * FROM conversations;
   .quit
   ```

---

**Ready to test? Follow the steps above and you'll have n8n working in 10 minutes!** 🚀
