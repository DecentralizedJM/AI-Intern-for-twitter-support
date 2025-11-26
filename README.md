# 🤖 AI Intern for Twitter Support

> **⚠️ Work In Progress (WIP)** - Currently in development and testing phase

An intelligent AI-powered support assistant that handles Twitter customer support with empathy, routing, and smart escalation - acting like a helpful intern who knows when to escalate to humans.

Built to solve real-world support challenges for **Mudrex** (@MudrexHelp), but designed as a reusable framework for any customer support team.

---

## 🎯 What This Does

This AI intern doesn't pretend to solve problems it can't handle. Instead, it:

✅ **Responds with genuine empathy** to customer complaints  
✅ **Routes everything to proper channels** (help@mudrex.com)  
✅ **Asks users to DM ticket numbers** for priority handling  
✅ **Auto-escalates to Slack** when tickets are shared  
✅ **De-escalates impatient users** politely  
✅ **Warns about security** when credentials are shared publicly  
✅ **Never hallucinates** - only says what it's programmed to say  

**Think of it as a smart intern who:**
- Is always polite and empathetic
- Knows their limitations
- Routes urgent issues to the right people
- Never makes promises they can't keep

---

## 🏗️ Architecture

\`\`\`
Twitter Mentions/DMs
        ↓
    n8n Workflow
        ↓
Python Backend (FastAPI)
        ↓
   ┌────┴────┐
   ↓         ↓
Gemini AI   SQLite
(Optional)  (Tracking)
   ↓
Response + Escalation
   ↓
Slack Notification (if urgent)
\`\`\`

---

## ✨ Features

### 🧠 Smart Intent Detection
- New complaints → "Email help@..."
- Existing tickets → "DM me the ticket number"
- Ticket shared → Auto-escalate to Slack
- Follow-ups → "Being reviewed..."
- Credentials shared → Security warning
- Questions → FAQ link

### 💬 Human-Like Responses
- 3-4 variations per response type
- Never sounds robotic
- Always empathetic

### 🚨 Auto-Escalation
- Instant Slack notifications
- Includes user info + ticket details
- Confirms escalation to user

---

## 🚀 Quick Start

\`\`\`bash
# Clone the repository
git clone https://github.com/DecentralizedJM/AI-Intern-for-twitter-support.git
cd twitter-support-ai-intern

# Set up Python environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Test without Twitter API
python demo_auto.py
\`\`\`

---

## 🧪 Testing

Test everything locally without Twitter API:

\`\`\`bash
# Automated demo
python demo_auto.py

# Interactive testing
python test_bot.py

# Start API server
python webhook_server.py
\`\`\`

---

## 📊 Example Conversations

**New Complaint:**
\`\`\`
User: "My withdrawal is stuck for 3 days!"
Bot:  "We understand the urgency. Please write to help@mudrex.com"
\`\`\`

**Escalation Flow:**
\`\`\`
User: "I raised a ticket but no response"
Bot:  "Thanks! Please DM me the ticket number"

User DM: "#12345"
Bot DM:  "Escalated! Our team will prioritize this"
[Slack notification sent]
\`\`\`

---

## 🗂️ Project Structure

\`\`\`
twitter-support-ai-intern/
├── config.py              # Response templates
├── gemini_handler.py      # AI classification
├── twitter_handler.py     # Main processor
├── slack_handler.py       # Escalations
├── database.py            # Tracking
├── webhook_server.py      # API endpoint
├── test_bot.py           # Interactive test
├── demo_auto.py          # Automated demo
├── n8n_workflow.json     # n8n template
└── docs/                 # Documentation
\`\`\`

---

## 📈 Roadmap

### ✅ Completed (MVP)
- [x] Intent classification
- [x] Response generation
- [x] Slack escalation
- [x] Conversation tracking
- [x] Mock testing
- [x] n8n workflow
- [x] API endpoint

### 🚧 In Progress
- [ ] Twitter API integration
- [ ] Live Slack testing
- [ ] Production deployment

### 🔮 Planned
- [ ] Multi-language support
- [ ] Sentiment analysis
- [ ] Analytics dashboard

---

## 🤝 Use Case: Mudrex Support

**Built to solve:**
- High volume Twitter support queries
- Manual escalation process
- Delayed off-hours responses

**Solution:**
- AI triage 24/7
- Auto-escalation
- Consistent responses

---

## 💰 Cost Estimate

| Service | Cost |
|---------|------|
| Twitter API | $100/mo |
| Gemini (optional) | Free |
| Slack | Free |
| n8n | Free |
| **Total** | ~**$100/mo** |

---

## 📝 License

**Copyright © 2025 @DecentralizedJM (DecentralizedJM)**

**All Rights Reserved.**

This project is proprietary software created by @DecentralizedJM.

**Permitted:**
✅ Personal use and modification  
✅ Use for your own company/projects  
✅ Learning and educational purposes  

**Not Permitted:**
❌ Commercial redistribution  
❌ Selling as a product/service  
❌ Creating competing products  
❌ Use without attribution  

**Attribution Required:** If used publicly, credit must be given to @DecentralizedJM (DecentralizedJM).

For commercial licensing or questions, please contact via GitHub.

See [LICENSE](LICENSE) file for complete terms.

---

## 🙏 Acknowledgments

- **Created for:** Mudrex customer support challenges
- **Powered by:** Google Gemini AI
- **Orchestration:** n8n workflow automation
- **Philosophy:** Honest, empathetic AI that knows its limits

---

## 📞 Contact

- **Author:** @DecentralizedJM ([@DecentralizedJM](https://github.com/DecentralizedJM))
- **Repository:** [AI-Intern-for-twitter-support](https://github.com/DecentralizedJM/AI-Intern-for-twitter-support)
- **Issues:** [Report Here](https://github.com/DecentralizedJM/AI-Intern-for-twitter-support/issues)

---

## 🌟 Why This Matters

Unlike typical AI chatbots that hallucinate and overpromise:

✅ **Honest** - Admits what it can't do  
✅ **Empathetic** - Understands user frustration  
✅ **Smart** - Knows when to escalate  
✅ **Safe** - Template-based, no hallucinations  

**Not replacing humans** - helping them work better.

---

**⚠️ Current Status:** Active development, not yet in production

**Next Milestone:** Twitter API integration and live testing

---

Made with ❤️ by [@DecentralizedJM](https://github.com/DecentralizedJM)
