import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#twitter-escalations")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/twitter-escalation")

# Database
DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/conversations.db")

# Testing
TESTING_MODE = os.getenv("TESTING_MODE", "true").lower() == "true"

# Response Templates
RESPONSE_TEMPLATES = {
    "new_complaint": [
        "We understand your concern. Please email help@mudrex.com and our support team will assist you promptly.",
        "We hear you. Kindly write to help@mudrex.com – our team will look into this right away.",
        "We appreciate you reaching out. Please contact help@mudrex.com so our support team can help resolve this.",
        "We understand the urgency. Please write to help@mudrex.com, our support team will assist you.",
    ],
    "has_ticket": [
        "Thanks for raising the issue! Please DM me the ticket number so I can speed up the resolution.",
        "Got it! Please DM the ticket number and I'll escalate this for you.",
        "Thank you for creating a ticket. Please send me the ticket number via DM so I can prioritize this.",
    ],
    "dm_ticket_received": [
        "Thank you! I've escalated ticket #{ticket_number} to our team. They'll prioritize this.",
        "Noted! Ticket #{ticket_number} has been escalated. Our team will review this urgently.",
        "Got it! I've flagged ticket #{ticket_number} for immediate attention.",
    ],
    "follow_up": [
        "We're reviewing your ticket and you'll hear from us soon. Thanks for your patience!",
        "Your ticket is being reviewed. Our team will get back to you shortly.",
        "We're on it! You should receive an update soon. Appreciate your patience.",
        "The team is looking into this. You'll hear back shortly!",
    ],
    "credentials_warning": [
        "⚠️ Please don't share personal details or credentials publicly on X for security reasons. Our team will never ask for passwords here.",
        "⚠️ For your security, please don't post sensitive information like emails or passwords on X. DM us or email help@mudrex.com instead.",
    ],
    "general_question": [
        "Please check our FAQ at https://mudrex.com/faq or write to help@mudrex.com for detailed assistance.",
        "For detailed information, please visit https://mudrex.com/faq or email help@mudrex.com.",
    ],
    "dm_no_ticket": [
        "I can help escalate your issue. Please share your ticket number (format: #12345).",
        "I'd be happy to escalate this. Could you share your ticket number?",
    ]
}

# Ticket number pattern
TICKET_PATTERN = r'#(\d{5})'
