# n8n Setup Guide for Twitter Support Bot

## Overview

This guide shows how to connect Twitter → n8n → Python Backend → Slack for automated support.

## Architecture

```
Twitter API
    ↓ (webhook/polling)
n8n Workflow
    ↓ (HTTP POST)
Python Backend (localhost:8000)
    ↓ (classification + response)
n8n receives response
    ↓ (conditional)
├─ If DM → Send DM
└─ If Tweet → Reply to Tweet
```

## Prerequisites

- n8n installed (self-hosted)
- Python backend running (`python webhook_server.py`)
- Twitter API credentials (Elevated access)

## Installation

### 1. Install n8n

```bash
# Install globally
npm install -g n8n

# Or use npx (no install needed)
npx n8n

# Access n8n UI
open http://localhost:5678
```

### 2. Create Twitter App

1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create new app
3. Go to "Keys and tokens"
4. Generate:
   - API Key
   - API Secret
   - Access Token
   - Access Token Secret
5. Save these for n8n

### 3. Import Workflow

#### Option A: Import JSON
1. In n8n, click "Import from File"
2. Select `n8n_workflow.json`
3. Workflow loads with all nodes

#### Option B: Build Manually

**Node 1: Twitter Trigger**
- Type: Twitter
- Operation: Listen to mentions
- Credentials: Add Twitter OAuth
- Additional Options:
  - Include DMs: Yes
  - Filter: @MudrexHelp

**Node 2: HTTP Request**
- Method: POST
- URL: `http://localhost:8000/webhook/twitter`
- Body:
```json
{
  "username": "={{ $json.user.screen_name }}",
  "message": "={{ $json.text || $json.message_create.message_data.text }}",
  "is_dm": "={{ $json.message_create ? true : false }}",
  "tweet_url": "={{ $json.entities ? 'https://twitter.com/' + $json.user.screen_name + '/status/' + $json.id_str : '' }}"
}
```

**Node 3: IF (Route based on is_dm)**
- Condition: `{{ $json.is_dm }} === true`
- True → Send DM node
- False → Reply to Tweet node

**Node 4a: Send Twitter Reply**
- Type: Twitter
- Operation: Tweet
- Text: `{{ $json.response }}`
- Additional Fields:
  - In reply to: `{{ $node["Twitter Trigger"].json.id_str }}`

**Node 4b: Send Twitter DM**
- Type: Twitter
- Operation: Send DM
- Text: `{{ $json.response }}`
- Recipient: `{{ $node["Twitter Trigger"].json.user.id_str }}`

## Workflow Configuration

### Complete n8n Workflow

```json
{
  "nodes": [
    {
      "name": "Twitter Trigger",
      "type": "n8n-nodes-base.twitterTrigger",
      "parameters": {
        "event": "mentions",
        "additionalFields": {
          "includeDMs": true
        }
      }
    },
    {
      "name": "Call Python Backend",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://localhost:8000/webhook/twitter",
        "method": "POST",
        "bodyParameters": {
          "username": "={{ $json.user.screen_name }}",
          "message": "={{ $json.text }}",
          "is_dm": "={{ !!$json.direct_message }}",
          "tweet_url": "={{ 'https://twitter.com/' + $json.user.screen_name + '/status/' + $json.id_str }}"
        }
      }
    },
    {
      "name": "Is DM?",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "boolean": [
            {
              "value1": "={{ $json.is_dm }}",
              "operation": "equal",
              "value2": true
            }
          ]
        }
      }
    },
    {
      "name": "Reply to Tweet",
      "type": "n8n-nodes-base.twitter",
      "parameters": {
        "operation": "tweet",
        "text": "={{ $json.response }}",
        "additionalFields": {
          "inReplyToStatusId": "={{ $node['Twitter Trigger'].json.id_str }}"
        }
      }
    },
    {
      "name": "Send DM",
      "type": "n8n-nodes-base.twitter",
      "parameters": {
        "operation": "directMessage",
        "text": "={{ $json.response }}",
        "recipient": "={{ $node['Twitter Trigger'].json.user.id_str }}"
      }
    }
  ],
  "connections": {
    "Twitter Trigger": {
      "main": [[{"node": "Call Python Backend"}]]
    },
    "Call Python Backend": {
      "main": [[{"node": "Is DM?"}]]
    },
    "Is DM?": {
      "main": [
        [{"node": "Send DM"}],
        [{"node": "Reply to Tweet"}]
      ]
    }
  }
}
```

## Testing

### 1. Start Python Backend

```bash
cd "/Users/jm/API Bot"
source .venv/bin/activate
python webhook_server.py
```

Server should show:
```
🚀 Starting Twitter Support Bot API...
📍 Webhook URL: http://localhost:8000/webhook/twitter
🧪 Test URL: http://localhost:8000/webhook/test
```

### 2. Test Webhook Manually

```bash
curl -X POST http://localhost:8000/webhook/twitter \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "message": "My withdrawal is stuck!",
    "is_dm": false
  }'
```

Expected response:
```json
{
  "success": true,
  "intent": "new_complaint",
  "response": "We understand your concern. Please email help@mudrex.com...",
  "ticket_number": null,
  "escalated": false
}
```

### 3. Test in n8n

1. Click "Execute Workflow" in n8n
2. Manually trigger with test data
3. Check each node's output
4. Verify response reaches Twitter

### 4. Test Live

1. Tweet at @MudrexHelp
2. Check n8n execution log
3. Verify bot replies
4. Test DM flow with ticket number

## Monitoring

### n8n Execution History
- View all executions in n8n UI
- See success/failure rates
- Debug failed executions

### Python Logs
- Check terminal running `webhook_server.py`
- All intents and responses logged

### Database
```bash
sqlite3 data/conversations.db
SELECT * FROM conversations ORDER BY created_at DESC LIMIT 10;
```

## Error Handling

### Common Issues

**1. Twitter API Rate Limits**
- Elevated: 100 tweets/15min
- Solution: Add rate limiting in n8n

**2. Webhook timeout**
- If Python backend slow
- Solution: Increase n8n timeout to 30s

**3. DM permissions**
- User must follow @MudrexHelp first
- Solution: Handle error gracefully

### Add Error Handling Node

After "Call Python Backend", add "IF Error" node:

```javascript
// Check if backend returned error
{{ $json.success === false }}
```

If error, send fallback response:
```
"We're experiencing technical difficulties. Please email help@mudrex.com directly."
```

## Advanced Features

### 1. Add Delay to Seem Human

After "Call Python Backend":
- Add "Wait" node
- Random delay: 2-5 seconds
- Makes responses feel less bot-like

### 2. Rate Limiting

Before replying:
- Add "Rate Limit" node
- Max 30 responses per hour
- Prevents spam issues

### 3. Logging to External DB

Add "MySQL" or "Postgres" node to log:
- All interactions
- Response times
- Escalation stats

### 4. Sentiment Analysis

Before escalation, add:
- "HTTP Request" to sentiment API
- Flag highly negative tweets
- Priority escalation to Slack

## Production Deployment

### Option 1: Keep n8n + Python Local
- Run on always-on machine
- Use ngrok for public webhook
- **Pros:** Free, simple
- **Cons:** Not scalable

### Option 2: Cloud Deployment

**n8n:**
- n8n Cloud ($20/month)
- Or self-host on DigitalOcean ($12/month)

**Python Backend:**
- Railway.app (Free tier)
- Heroku ($7/month)
- DigitalOcean App Platform ($5/month)

**Update webhook URL:**
```
https://your-app.railway.app/webhook/twitter
```

### Option 3: Fully Serverless
- AWS Lambda for Python backend
- n8n Cloud
- Trigger via API Gateway

## Security Checklist

- [ ] Twitter API keys in environment variables
- [ ] Webhook endpoint uses HTTPS in production
- [ ] Rate limiting enabled
- [ ] Error handling for all scenarios
- [ ] Logging without exposing user data
- [ ] Slack webhook URL not hardcoded

## Maintenance

### Daily
- Check n8n execution log
- Review escalated tickets in Slack
- Monitor response rate

### Weekly
- Review conversation database
- Check for new edge cases
- Update response templates if needed

### Monthly
- Analyze metrics (response time, escalation rate)
- Tune intent classification
- Update FAQ links

## Metrics to Track

1. **Response Rate:** % of mentions responded to
2. **Escalation Rate:** % of DMs that escalate
3. **Response Time:** Avg seconds to reply
4. **Intent Accuracy:** Manual review of classifications
5. **User Satisfaction:** Track sentiment in follow-ups

## Support Commands

```bash
# View n8n workflows
n8n list:workflow

# Export workflow
n8n export:workflow --id=1 --output=backup.json

# Check n8n version
n8n --version

# View Python logs
tail -f webhook_server.log
```

## Next Steps

1. ✅ Import workflow to n8n
2. ✅ Add Twitter credentials
3. ✅ Test webhook connection
4. ✅ Send test tweet
5. ✅ Verify bot replies
6. ✅ Test DM escalation
7. ✅ Monitor for 24 hours
8. ✅ Go fully live!

---

**Questions?** Check the main README.md or test locally first!
