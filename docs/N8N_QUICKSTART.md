# 🚀 n8n Quick Start - 5 Minutes

Get n8n working with the Twitter Support Bot in 5 minutes!

---

## Step 1: Install n8n (1 minute)

```bash
npm install -g n8n
```

Wait for installation to complete.

---

## Step 2: Start Everything (1 minute)

**Open Terminal 1:**
```bash
n8n start
```
Keep this running. You should see:
```
Editor is now accessible via:
http://localhost:5678/
```

**Open Terminal 2:**
```bash
cd "/Users/jm/API Bot"
source .venv/bin/activate
python webhook_server.py
```
Keep this running. You should see:
```
🚀 Starting Twitter Support Bot API...
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Step 3: Import Workflow (1 minute)

1. Open browser → **http://localhost:5678**
2. Click **"Add workflow"**
3. Click **⋮ menu** → **"Import from File"**
4. Select: `/Users/jm/API Bot/n8n_workflow.json`
5. Click **"Import"**

Done! You should see 5 nodes connected.

---

## Step 4: Test It! (2 minutes)

**In n8n:**
1. Click **"Execute Workflow"** button (top right)
2. Workflow starts listening

**Open Terminal 3:**
```bash
curl -X POST http://localhost:5678/webhook-test/twitter-message \
  -H "Content-Type: application/json" \
  -d '{
    "username": "angry_user",
    "message": "My withdrawal is stuck!",
    "is_dm": false
  }'
```

**Check Results:**
- n8n shows green checkmarks ✓
- Terminal 2 shows: "Processing Tweet from @angry_user"
- You get a JSON response with the bot's reply

---

## ✅ Success!

You should see output like:
```json
{
  "success": true,
  "intent": "new_complaint",
  "response": "We understand your concern. Please email help@mudrex.com...",
  "escalated": false
}
```

---

## 🎯 Quick Tests

Run these to see different scenarios:

**Test DM with ticket (escalation):**
```bash
curl -X POST http://localhost:5678/webhook-test/twitter-message \
  -H "Content-Type: application/json" \
  -d '{"username":"user","message":"#12345","is_dm":true}'
```

**Test credentials warning:**
```bash
curl -X POST http://localhost:5678/webhook-test/twitter-message \
  -H "Content-Type: application/json" \
  -d '{"username":"user","message":"user@gmail.com","is_dm":false}'
```

**Or run all tests at once:**
```bash
cd "/Users/jm/API Bot"
./test_n8n.sh
```

---

## 🔍 What to Check

### In n8n UI:
- Click each node to see data flow
- Green checkmarks = success
- Click "Executions" tab to see history

### In Python Terminal:
- See intent classification logs
- See responses generated
- See "[MOCK SLACK]" for escalations

### In Database:
```bash
sqlite3 data/conversations.db "SELECT username, intent FROM conversations LIMIT 5;"
```

---

## ❌ Troubleshooting

**"Connection refused" error?**
- Make sure both terminals are still running
- Check Python backend: `curl http://localhost:8000/`
- Check n8n: `curl http://localhost:5678/`

**Workflow not executing?**
- Click "Execute Workflow" button first
- Use the **Test URL**, not Production URL
- Make sure webhook node is active

**Wrong responses?**
- Check Python terminal for errors
- Verify JSON format in curl command
- Try the test script: `./test_n8n.sh`

---

## 📚 More Info

- **Detailed Guide:** See `N8N_STEP_BY_STEP.md`
- **Checklist:** See `N8N_CHECKLIST.md`
- **Full Docs:** See `README.md`

---

## 🎉 What's Next?

Once this works:

1. Get Gemini API key for better classification
2. Set up Slack webhook for real escalations
3. When you get Twitter API, add Twitter trigger
4. Deploy to production

---

**That's it! You now have n8n working with the Twitter Support Bot!** 🚀
