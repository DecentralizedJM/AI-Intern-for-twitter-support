# Twitter Support Bot - Quick Start Guide

## ✅ MVP is Ready!

Your Twitter support bot is built and tested. Here's what you have:

## Current Status

### ✅ Completed
- ✅ Python backend with Gemini AI integration
- ✅ Intent classification (6 scenarios)
- ✅ Response generation with variations
- ✅ Slack escalation system
- ✅ Conversation tracking (SQLite)
- ✅ Mock testing interface (no Twitter API needed)
- ✅ FastAPI webhook for n8n
- ✅ n8n workflow template

### 🔜 Pending (Need API Access)
- Twitter API credentials
- Gemini API key (optional - has fallback)
- Slack webhook URL

## How to Test Right Now

### 1. Run Automated Demo
```bash
cd "/Users/jm/API Bot"
source .venv/bin/activate
python demo_auto.py
```

### 2. Interactive Testing
```bash
python test_bot.py
```
Then choose options to:
- Simulate tweets
- Simulate DMs
- View conversation history
- Test predefined scenarios

### 3. Start API Server (for n8n)
```bash
python webhook_server.py
```
Server runs at: http://localhost:8000

Test webhook:
```bash
curl -X POST http://localhost:8000/webhook/twitter \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "message": "I need help with withdrawal",
    "is_dm": false
  }'
```

## Next Steps to Go Live

### Step 1: Get Twitter API Access
1. Go to https://developer.twitter.com/
2. Apply for "Elevated" access (needed for DMs)
3. Create a new app
4. Generate API keys

**Cost:** Free for basic, $100/month for Elevated

### Step 2: Get Gemini API Key (Optional)
1. Go to https://makersuite.google.com/app/apikey
2. Create API key
3. Add to `.env` file

**Note:** Bot has fallback keyword matching, but Gemini is better

### Step 3: Set Up Slack
1. Go to https://api.slack.com/apps
2. Create app → "Incoming Webhooks"
3. Add to channel (e.g., #twitter-escalations)
4. Copy webhook URL to `.env`

### Step 4: Install n8n
```bash
npm install -g n8n
n8n start
```
Access at: http://localhost:5678

Import workflow: `n8n_workflow.json`

### Step 5: Connect Everything
1. Update `.env` with all credentials
2. Start webhook server: `python webhook_server.py`
3. In n8n, configure Twitter trigger
4. Point n8n HTTP node to `http://localhost:8000/webhook/twitter`
5. Test with a tweet!

## Project Structure

```
API Bot/
├── config.py              # Response templates & settings
├── gemini_handler.py      # AI classification & responses
├── twitter_handler.py     # Main logic
├── slack_handler.py       # Escalation notifications
├── database.py            # Conversation tracking
├── webhook_server.py      # FastAPI endpoint
├── test_bot.py           # Interactive tester
├── demo_auto.py          # Automated demo
├── n8n_workflow.json     # n8n template
└── data/
    └── conversations.db   # SQLite database
```

## How It Works

```
Twitter Mention/DM
        ↓
     n8n Workflow
        ↓
  Python Backend (webhook_server.py)
        ↓
  Intent Classifier (gemini_handler.py)
        ↓
  ┌───────────────┐
  │ Route by      │
  │ Intent        │
  └───────────────┘
        ↓
  ┌─────────────────────┬──────────────┬─────────────┐
  ↓                     ↓              ↓             ↓
New Complaint    Has Ticket    DM Ticket    Follow-up
  ↓                     ↓              ↓             ↓
"Email            "DM me       Escalate    "Being
help@..."         ticket #"    to Slack     reviewed"
```

## Bot Behavior Summary

| Scenario | User Action | Bot Response | Escalation |
|----------|-------------|--------------|------------|
| New complaint | Tweets complaint | "Please email help@mudrex.com" | No |
| Has ticket | Mentions ticket | "Please DM the ticket number" | No |
| DM ticket | DMs #12345 | "Escalated!" | ✅ Yes → Slack |
| Follow-up | Asks for update | "Being reviewed, you'll hear soon" | No |
| Credentials | Shares email/pwd | ⚠️ Security warning | No |
| General Q | Asks how-to | "Check FAQ or email help@..." | No |

## Response Examples

All responses have 3-4 variations to sound human!

**Complaint:**
- "We understand your concern. Please email help@mudrex.com..."
- "We hear you. Kindly write to help@mudrex.com..."
- "We appreciate you reaching out. Please contact help@..."

**Has Ticket:**
- "Thanks for raising the issue! Please DM me the ticket number..."
- "Got it! Please DM the ticket number and I'll escalate..."

**Escalation Confirmed:**
- "Thank you! I've escalated ticket #12345 to our team..."
- "Noted! Ticket #12345 has been escalated..."

## Ticket Format

Expected: `#12345` (# followed by 5 digits)

Regex: `#(\d{5})`

## Testing Checklist

- [x] New complaint → Email redirect
- [x] Has ticket → Ask for DM
- [x] DM with ticket → Slack escalation
- [x] Follow-up → De-escalate
- [x] Credentials → Security warning
- [x] General question → FAQ link
- [x] Response variations work
- [x] Database tracking works
- [x] Webhook server works
- [ ] Twitter API integration (pending API)
- [ ] n8n workflow (pending setup)
- [ ] Slack notifications (pending webhook)

## Troubleshooting

**Packages not found?**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**Database errors?**
```bash
rm -rf data/
python demo_auto.py  # Recreates DB
```

**Test Slack webhook:**
```bash
curl -X POST YOUR_SLACK_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{"text": "Test from Twitter bot!"}'
```

## Cost Breakdown

| Service | Cost |
|---------|------|
| Twitter API (Elevated) | $100/month |
| Gemini API | Free tier (1500 req/day) |
| Slack | Free |
| n8n (self-hosted) | Free |
| **Total** | ~**$100/month** |

## Support & Documentation

- **Test bot:** `python test_bot.py`
- **Auto demo:** `python demo_auto.py`
- **Start server:** `python webhook_server.py`
- **View DB:** `sqlite3 data/conversations.db`

## What Makes This Bot Special

✅ **No hallucinations** - Uses templates, not free-form generation  
✅ **Human-like** - Multiple response variations  
✅ **Safe** - Never gives financial advice  
✅ **Smart routing** - Auto-escalates urgent issues  
✅ **Trackable** - All conversations logged  
✅ **Testable** - Works without Twitter API  

---

**Ready to go live?** Just add Twitter API credentials and deploy! 🚀
