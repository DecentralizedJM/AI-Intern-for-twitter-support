# 📥 n8n Workflow Import Guide

## Quick Import (2 Minutes)

### Step 1: Install n8n
```bash
# Install n8n globally
npm install -g n8n

# Start n8n
n8n start
```

n8n will open at: **http://localhost:5678**

---

### Step 2: Import the Workflow

1. **Open n8n Dashboard** → http://localhost:5678

2. **Click "Add Workflow"** (+ button in top right)

3. **Click the 3-dot menu** (⋯) in top right

4. **Select "Import from File"**

5. **Choose file:** `n8n_workflow.json`

6. **Click "Import"**

✅ **Done!** Your workflow is now loaded.

---

## 🎯 What You'll See

The imported workflow has **5 nodes**:

```
┌─────────────────────┐
│ Webhook Trigger     │ ← Receives Twitter messages
│ (Manual Test Mode)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Call Python Backend │ ← POST to localhost:8000
│ (HTTP Request)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Check Success       │ ← IF node (success = true?)
│ (IF Node)           │
└──────┬──────────────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
┌──────┐ ┌─────────┐
│ Yes  │ │ No      │
│ Path │ │ Path    │
└──┬───┘ └───┬─────┘
   │         │
   ▼         ▼
┌──────┐ ┌─────────┐
│Format│ │ Handle  │
│Good  │ │ Error   │
│Reply │ │         │
└──────┘ └─────────┘
```

---

## 🧪 Test the Workflow

### Step 1: Make Sure Python Server is Running
```bash
cd /path/to/AI-Intern-for-twitter-support
source .venv/bin/activate
python webhook_server.py
```

Should show:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

### Step 2: Test in n8n

1. **Click "Test workflow"** (play button)

2. **Click "Listen for test event"** on the Webhook node

3. **Use the webhook URL shown** or click "Execute Node"

4. **Send test data:**
```json
{
  "username": "test_user",
  "message": "My withdrawal is stuck!",
  "is_dm": false
}
```

5. **Watch the flow execute** through all nodes

6. **Check the output** - you should see:
   - Intent classification
   - Generated response
   - Escalation status

---

## 📊 Sample Test Cases

### Test 1: New Complaint
```json
{
  "username": "angry_user",
  "message": "My withdrawal has been stuck for 3 days!",
  "is_dm": false
}
```
**Expected:** Routes to help@mudrex.com

---

### Test 2: User Has Ticket
```json
{
  "username": "patient_user",
  "message": "I raised a ticket but haven't heard back",
  "is_dm": false
}
```
**Expected:** Asks for DM with ticket number

---

### Test 3: Ticket Shared in DM
```json
{
  "username": "patient_user",
  "message": "Here's my ticket #12345",
  "is_dm": true
}
```
**Expected:** Escalates to Slack, confirms to user

---

### Test 4: Credentials Warning
```json
{
  "username": "risky_user",
  "message": "My password is xyz123 please help",
  "is_dm": false
}
```
**Expected:** Security warning

---

## 🔧 Customize the Workflow

After import, you can:

1. **Change Python Backend URL**
   - Click "Call Python Backend" node
   - Update URL if hosting elsewhere

2. **Add Twitter Trigger** (when you get API)
   - Delete Webhook node
   - Add Twitter trigger node
   - Connect to "Call Python Backend"

3. **Add Response Actions**
   - Add Twitter reply node after "Format Good Reply"
   - Connect to your Twitter account

4. **Add Error Notifications**
   - Add Email/Slack node after "Handle Error"
   - Get notified when bot fails

---

## 📁 Workflow File Location

```
./n8n_workflow.json
```

---

## 🎬 Video Walkthrough

### Visual Flow:
1. Import JSON file ✅
2. See nodes appear automatically ✅
3. Click "Test workflow" ✅
4. Send test message ✅
5. Watch execution path ✅
6. See response generated ✅

---

## ⚡ Quick Commands

```bash
# Start n8n
n8n start

# Start Python backend
cd /path/to/AI-Intern-for-twitter-support
source .venv/bin/activate
python webhook_server.py

# Test with curl (alternative)
curl -X POST http://localhost:5678/webhook-test/twitter-support-bot \
  -H "Content-Type: application/json" \
  -d '{"username":"test","message":"help!","is_dm":false}'
```

---

## 🆘 Troubleshooting

### "Cannot connect to localhost:8000"
- Start Python server first: `python webhook_server.py`

### "Webhook not responding"
- Click "Listen for test event"
- Make sure n8n is running on port 5678

### "Import failed"
- Make sure file is `n8n_workflow.json` (not .txt or .json.json)
- Try copying content and using "Import from URL/Text" instead

---

## 🚀 Next Steps

After testing in n8n:

1. ✅ Verify all 6 scenarios work
2. ✅ Check Python logs for errors
3. ✅ Test Slack escalation (mock mode)
4. 🔲 Get Twitter API credentials
5. 🔲 Replace webhook with Twitter trigger
6. 🔲 Deploy to production!

---

**File Ready:** `n8n_workflow.json` (3.5 KB)

**Status:** ✅ Ready to import and test!

