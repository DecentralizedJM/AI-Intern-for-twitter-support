"""
Slack Integration for Ticket Escalations
"""
import requests
import json
from datetime import datetime
import config


def send_escalation(ticket_number: str, username: str, tweet_url: str = None, original_message: str = None):
    """
    Send escalation notification to Slack
    
    Args:
        ticket_number: The ticket number being escalated
        username: Twitter username
        tweet_url: URL to the original tweet
        original_message: The user's original complaint
    
    Returns:
        bool: Success status
    """
    if not config.SLACK_WEBHOOK_URL or config.SLACK_WEBHOOK_URL == "your_slack_webhook_url_here":
        print(f"\n[MOCK SLACK] Would send escalation for ticket #{ticket_number}")
        print(f"User: @{username}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if original_message:
            print(f"Message: {original_message}")
        return True
    
    try:
        # Build Slack message blocks
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🚨 Twitter Ticket Escalation"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*User:* @{username}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Ticket:* #{ticket_number}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Platform:* Twitter DM"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    }
                ]
            }
        ]
        
        # Add original message if available
        if original_message:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Original Message:*\n{original_message}"
                }
            })
        
        # Add tweet link if available
        if tweet_url:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<{tweet_url}|View Tweet>"
                }
            })
        
        # Add action button
        blocks.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "View Ticket"
                    },
                    "url": f"https://support.mudrex.com/ticket/{ticket_number}",
                    "style": "primary"
                }
            ]
        })
        
        payload = {
            "channel": config.SLACK_CHANNEL,
            "blocks": blocks
        }
        
        response = requests.post(
            config.SLACK_WEBHOOK_URL,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print(f"✅ Escalation sent to Slack for ticket #{ticket_number}")
            return True
        else:
            print(f"❌ Failed to send to Slack: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending Slack notification: {e}")
        return False


def send_test_message():
    """
    Send a test message to verify Slack integration
    """
    payload = {
        "channel": config.SLACK_CHANNEL,
        "text": "✅ Twitter Support Bot - Slack integration test successful!",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "✅ *Twitter Support Bot Connected*\nSlack escalation notifications are working correctly."
                }
            }
        ]
    }
    
    try:
        response = requests.post(
            config.SLACK_WEBHOOK_URL,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Test failed: {e}")
        return False
