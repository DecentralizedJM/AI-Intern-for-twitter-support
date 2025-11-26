# 📦 n8n Workflow - Complete Package

## 🎁 What You Have

I've created everything you need to get n8n working with your Twitter Support Bot:

---

## 📁 Files Created

### 1. **n8n_workflow.json** ⭐
The actual n8n workflow file - ready to import!

**What it contains:**
- Webhook trigger (manual testing)
- HTTP request to Python backend
- Success/error routing
- Response formatting

**How to use:**
Import this file directly into n8n (see guides below)

---

### 2. **N8N_QUICKSTART.md** 🚀
**5-minute setup guide** - fastest way to get started

**Contains:**
- 4 simple steps
- Copy-paste commands
- Quick tests
- Troubleshooting

**Start here if:** You want to test immediately

---

### 3. **N8N_STEP_BY_STEP.md** 📖
**Detailed walkthrough** with explanations

**Contains:**
- Complete installation process
- Detailed testing scenarios
- Understanding each node
- Production deployment tips

**Start here if:** You want to understand everything

---

### 4. **N8N_CHECKLIST.md** ✅
**Interactive checklist** - tick boxes as you go

**Contains:**
- Step-by-step checklist
- All test scenarios
- Verification points
- Troubleshooting section

**Start here if:** You like structured workflows

---

### 5. **test_n8n.sh** 🧪
**Automated test script** - tests all scenarios

**What it does:**
- Checks if services are running
- Runs 4 test scenarios
- Shows results in terminal

**How to use:**
```bash
cd "/Users/jm/API Bot"
./test_n8n.sh
```

---

## 🎯 Quick Start (Choose Your Path)

### Path A: Fastest (5 minutes)
```bash
# 1. Install n8n
npm install -g n8n

# 2. Start n8n (Terminal 1)
n8n start

# 3. Start backend (Terminal 2)
cd "/Users/jm/API Bot"
source .venv/bin/activate
python webhook_server.py

# 4. Import workflow
# - Open http://localhost:5678
# - Import n8n_workflow.json

# 5. Test
curl -X POST http://localhost:5678/webhook-test/twitter-message \
  -H "Content-Type: application/json" \
  -d '{"username":"test","message":"help","is_dm":false}'
```

Follow: **N8N_QUICKSTART.md**

---

### Path B: Thorough (15 minutes)
1. Read **N8N_STEP_BY_STEP.md**
2. Follow each step carefully
3. Understand what each part does
4. Test all scenarios

---

### Path C: Checklist (10 minutes)
1. Open **N8N_CHECKLIST.md**
2. Check off each item as you complete it
3. Verify everything works
4. All boxes should be checked at the end

---

## 🔧 What the Workflow Does

```
User message comes in
      ↓
Webhook receives it
      ↓
Sends to Python backend (localhost:8000)
      ↓
Backend classifies intent & generates response
      ↓
Returns JSON with response
      ↓
n8n formats and displays it
```

**Key Features:**
- ✅ Works without Twitter API (uses manual webhook)
- ✅ Tests all bot scenarios
- ✅ Shows intent classification
- ✅ Displays bot responses
- ✅ Logs to database

---

## 📊 Workflow Nodes Explained

### 1. Webhook (Manual Trigger)
- Receives HTTP POST requests
- Accepts: `{username, message, is_dm}`
- Provides Test URL for testing

### 2. Call Python Backend
- Sends data to `localhost:8000/webhook/twitter`
- Gets back intent and response
- Timeout: 30 seconds

### 3. Success?
- Checks if `success: true`
- Routes to Format Response or Handle Error

### 4. Format Response
- Structures final output
- Shows bot's reply

### 5. Handle Error
- Catches failures
- Logs error information

---

## 🧪 Testing Scenarios

All these work with the test script or manual curl:

| Scenario | Expected Intent | Expected Response |
|----------|----------------|-------------------|
| "Withdrawal stuck" | new_complaint | "Email help@mudrex.com" |
| "I raised ticket" | has_ticket | "DM the ticket number" |
| DM: "#12345" | dm_ticket_shared | "Escalated!" + Slack |
| "Still waiting" | follow_up | "Being reviewed..." |
| "user@gmail.com" | credentials_shared | "⚠️ Don't share..." |

---

## ✅ Success Indicators

You'll know it's working when:

**In n8n:**
- ✅ All nodes show green checkmarks
- ✅ Each node displays data when clicked
- ✅ Final output shows bot response

**In Python terminal:**
- ✅ See "Processing Tweet from @username"
- ✅ See intent classification
- ✅ See response generated

**In test output:**
- ✅ JSON response with `success: true`
- ✅ Correct intent detected
- ✅ Appropriate response text

---

## 🚨 Common Issues & Fixes

### "Cannot connect to localhost:8000"
**Fix:** Start Python backend
```bash
cd "/Users/jm/API Bot"
source .venv/bin/activate
python webhook_server.py
```

### "Webhook not found"
**Fix:** 
1. Click "Execute Workflow" in n8n
2. Use Test URL, not Production URL
3. Make sure workflow is saved

### "n8n won't start"
**Fix:** Check if port 5678 is in use
```bash
lsof -i :5678
# Kill the process if needed
kill -9 <PID>
n8n start
```

---

## 📈 Next Steps

### Immediate (Today)
- [ ] Install n8n
- [ ] Import workflow
- [ ] Run test scenarios
- [ ] Verify all works

### Short-term (This Week)
- [ ] Get Gemini API key (optional)
- [ ] Set up Slack webhook
- [ ] Test real Slack notifications

### Medium-term (When you get Twitter API)
- [ ] Add Twitter trigger node
- [ ] Replace webhook with Twitter listener
- [ ] Add Twitter reply nodes
- [ ] Go live!

---

## 📚 Documentation Map

```
Quick Start
    ↓
N8N_QUICKSTART.md ← Start here for 5-min setup
    ↓
Need more details?
    ↓
N8N_STEP_BY_STEP.md ← Complete guide
    ↓
Want checklist?
    ↓
N8N_CHECKLIST.md ← Tick boxes as you go
    ↓
Need architecture?
    ↓
ARCHITECTURE.md ← Visual diagrams
    ↓
Full project info?
    ↓
README.md ← Complete overview
```

---

## 💡 Pro Tips

1. **Keep terminals organized**
   - Terminal 1: n8n
   - Terminal 2: Python backend
   - Terminal 3: Testing

2. **Use n8n's execution viewer**
   - Click "Executions" tab
   - See all past runs
   - Debug issues easily

3. **Test incrementally**
   - Start with one scenario
   - Verify it works
   - Then test others

4. **Check logs**
   - Python terminal shows intent classification
   - n8n shows data flow
   - Database stores history

---

## 🎉 You're Ready!

Everything you need is in these files:

1. **n8n_workflow.json** - Import this
2. **N8N_QUICKSTART.md** - Follow this
3. **test_n8n.sh** - Run this

**Time to get started:** 5 minutes  
**Difficulty:** Easy  
**Requirements:** n8n, Python backend (already have)

---

**Pick a guide above and let's get n8n working! 🚀**
