# 🚀 Twikit Integration Guide

## What's New

Your AI Twitter Intern now has **real Twitter API integration** using Twikit! No more mock data - this bot can now:

✅ **Monitor** real Twitter mentions and DMs  
✅ **Reply** automatically with AI-generated responses  
✅ **Escalate** tickets to Slack when users share ticket numbers  
✅ **Authenticate** securely with session persistence  
✅ **Run 24/7** with continuous monitoring  

---

## 🆕 New Files Added

### 1. `twitter_client.py`
Twikit wrapper that handles:
- Authentication with Twitter
- Fetching mentions
- Fetching DMs
- Posting replies
- Sending DMs
- Session persistence (cookies)

### 2. `twitter_monitor.py`
Continuous monitoring script that:
- Polls Twitter every 60 seconds (configurable)
- Processes new mentions and DMs
- Sends AI-generated responses
- Tracks processed messages to avoid duplicates

### 3. Updated Files
- `requirements.txt` - Added `twikit>=2.3.3`
- `.env.example` - Added Twitter credentials

---

## 📦 Installation

### 1. Navigate to project directory
```bash
cd AI-Intern-for-twitter-support
```

### 2. Activate virtual environment
```bash
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

### 3. Install new dependencies
```bash
pip install -r requirements.txt
```

This will install twikit and all its dependencies.

---

## 🔑 Configuration

### 1. Update your `.env` file

Add your Twitter credentials:

```bash
# Twitter Credentials (for Twikit)
TWITTER_USERNAME=your_twitter_username
TWITTER_EMAIL=your_email@example.com
TWITTER_PASSWORD=your_password

# Twitter Monitoring
TWITTER_POLL_INTERVAL=60  # Check every 60 seconds

# Existing configs
GEMINI_API_KEY=your_gemini_api_key
SLACK_WEBHOOK_URL=your_slack_webhook
```

### 2. Create data directory
```bash
mkdir -p data
```

This stores:
- `twitter_cookies.json` - Session cookies (auto-generated)
- `conversations.db` - Conversation history

---

## 🧪 Testing

### Test 1: Twitter Connection
```bash
python twitter_client.py
```

Expected output:
```
🧪 Testing Twitter Connection...
🔑 Logging in to Twitter...
✅ Successfully authenticated as @YourUsername

📱 Fetching mentions...
@user1: Hey @YourBot I need help with...
@user2: Thanks for the support!

💬 Fetching DMs...
@user3: I have ticket #12345

✅ Twitter connection test complete!
```

### Test 2: Process a Single Message (Mock)
```bash
python test_bot.py
```

This tests the AI response logic without Twitter.

### Test 3: Full Integration Demo
```bash
python demo_auto.py
```

Tests the complete flow with mock Twitter data.

---

## 🚀 Running the Bot

### Start Monitoring
```bash
python twitter_monitor.py
```

Expected output:
```
============================================================
🤖 AI Twitter Intern - Starting Monitor
============================================================

🔑 Loading saved session...
✅ Authenticated as @YourBot

⏰ Polling every 60 seconds
Press Ctrl+C to stop

============================================================
🔄 Poll #1 - 2025-11-27 14:30:00
============================================================

📬 Checking mentions... [14:30:00]
✅ Processed 2 new mentions

💬 Checking DMs... [14:30:01]
✅ Processed 1 new DMs

⏸️  Sleeping for 60 seconds...
```

### Stop Monitoring
Press `Ctrl+C` to stop gracefully.

---

## 🔄 How It Works

### Flow Diagram

```
Twitter Mention/DM
       ↓
twitter_monitor.py (polls every 60s)
       ↓
twitter_client.py (fetch via Twikit)
       ↓
twitter_handler.py (existing logic)
       ↓
gemini_handler.py (AI classification)
       ↓
Response Generated
       ↓
twitter_client.py (send reply)
       ↓
Slack Notification (if ticket escalated)
```

### Example Scenario

**User tweets:** `@YourBot My withdrawal is stuck!`

1. **Monitor detects** the mention (60s poll)
2. **AI classifies** intent as "new_complaint"
3. **Response generated:** "We understand your concern. Please email help@mudrex.com..."
4. **Bot replies** on Twitter
5. **Saved to database**

**User DMs:** `#12345`

1. **Monitor detects** the DM
2. **AI extracts** ticket number
3. **Escalates to Slack** with details
4. **DM response:** "Thank you! I've escalated ticket #12345..."
5. **Saved to database**

---

## ⚙️ Configuration Options

Edit `.env` to customize:

```bash
# How often to check Twitter (seconds)
TWITTER_POLL_INTERVAL=60

# Where to save cookies (for faster re-authentication)
TWITTER_COOKIES_FILE=./data/twitter_cookies.json

# Enable/disable features
TESTING_MODE=false  # Set to false for production
```

---

## 🔐 Security Best Practices

### 1. **Never commit credentials**
```bash
# .env is already in .gitignore
# Double-check it's there:
cat .gitignore | grep .env
```

### 2. **Use a dedicated Twitter account**
- Don't use your personal account
- Create a support account (@YourCompanySupport)
- Enable 2FA (optional, but recommended)

### 3. **Secure the cookies file**
```bash
# Set proper permissions
chmod 600 data/twitter_cookies.json
```

### 4. **Monitor rate limits**
Twikit handles rate limits automatically, but be aware:
- Twitter has rate limits on API calls
- The bot will pause if limits are hit
- Check logs for `⚠️ Rate limit hit` messages

---

## 🐛 Troubleshooting

### Issue: "Authentication failed"

**Solution:**
1. Check credentials in `.env`
2. Try deleting `data/twitter_cookies.json` and re-authenticating
3. Check if Twitter account is locked/suspended

### Issue: "No new mentions found"

**Possible causes:**
1. No one has mentioned your bot yet
2. Bot username in `.env` doesn't match Twitter account
3. Rate limit hit (check logs)

**Test manually:**
```python
# Test authentication
python twitter_client.py
```

### Issue: "Import twikit could not be resolved"

**Solution:**
```bash
pip install twikit
# or
pip install -r requirements.txt
```

### Issue: Rate limits

**Symptoms:**
```
⚠️ Rate limit hit. Reset at: 1732723800
```

**Solution:**
- Wait for the reset time
- Increase `TWITTER_POLL_INTERVAL` (e.g., from 60 to 120 seconds)
- Twikit automatically handles retries

---

## 📊 Monitoring & Logs

### View real-time activity
```bash
python twitter_monitor.py
```

### Check database
```bash
sqlite3 data/conversations.db "SELECT * FROM conversations ORDER BY timestamp DESC LIMIT 10;"
```

### Monitor Slack escalations
Check your Slack channel (e.g., `#twitter-escalations`) for urgent ticket notifications.

---

## 🎯 Next Steps

### 1. **Deploy to Production**
   - Set up a server (EC2, DigitalOcean, etc.)
   - Run monitor as a background service
   - Set up logging to file
   - Monitor uptime

### 2. **Enhance Features**
   - Add sentiment analysis
   - Multi-language support
   - Custom auto-responses per user
   - Analytics dashboard

### 3. **Scale**
   - Multiple Twitter accounts
   - Load balancing
   - Database backup
   - Webhook integration (instead of polling)

---

## 🚨 Production Checklist

Before going live:

- [ ] Test on a staging Twitter account
- [ ] Verify all credentials in `.env`
- [ ] Test Slack escalations
- [ ] Set `TESTING_MODE=false`
- [ ] Monitor for 24 hours
- [ ] Set up error alerting
- [ ] Document response times
- [ ] Train team on escalation flow

---

## 💡 Tips

1. **Start slow**: Set `TWITTER_POLL_INTERVAL=120` (2 minutes) initially
2. **Monitor closely**: Watch the first 100 interactions carefully
3. **Adjust responses**: Update `config.py` templates based on feedback
4. **Rate limits**: Twitter has generous free limits, but don't abuse
5. **Be human**: The AI should sound helpful, not robotic

---

## 📚 Architecture Overview

### Before (Mock Data)
```
webhook_server.py → twitter_handler.py → gemini_handler.py
                         ↓
                    Mock responses
```

### After (Real Twitter)
```
twitter_monitor.py ────┐
   ↓                   │
twitter_client.py      │
   ↓                   ↓
twitter_handler.py ────┤
   ↓                   │
gemini_handler.py      │
   ↓                   │
slack_handler.py       │
   ↓                   ↓
Real Twitter Replies + Slack Escalations
```

---

## 🎓 Key Concepts

### Twikit
- **No API key needed** - Free Twitter automation
- **Async/await** - Handles concurrent requests
- **Session persistence** - Cookies saved between runs
- **Rate limit handling** - Automatic backoff

### Polling vs Streaming
- **Polling** (current): Check Twitter every 60s
- **Streaming** (future): Real-time updates (advanced)

### Why Twikit?
- ✅ Free (no Twitter API costs)
- ✅ Full functionality
- ✅ Active development
- ✅ Python-friendly
- ⚠️ Against Twitter ToS (use carefully)

---

## 📞 Support

- **GitHub Issues**: Report bugs
- **Docs**: Check `README.md` and `DEPLOYMENT_SUMMARY.md`
- **Author**: @DecentralizedJM

---

## 🎉 You're Ready!

Your AI Twitter Intern is now powered by real Twitter API integration. Start monitoring and let the bot handle customer support automatically!

```bash
# Start the bot
python twitter_monitor.py
```

Happy automating! 🚀
