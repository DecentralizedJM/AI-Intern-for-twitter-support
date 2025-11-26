"""
Gemini AI Integration for Intent Classification and Response Generation
"""
import google.generativeai as genai
import random
import config

# Configure Gemini
if config.GEMINI_API_KEY:
    genai.configure(api_key=config.GEMINI_API_KEY)

# Intent classification prompt
INTENT_CLASSIFICATION_PROMPT = """
You are analyzing a Twitter message sent to @MudrexHelp (a crypto trading platform support handle).

Classify the intent into ONE of these categories:
1. new_complaint - User is complaining for the first time (hasn't mentioned raising a ticket)
2. has_ticket - User mentions they have already raised/created a support ticket
3. dm_ticket_shared - User is sharing a ticket number in DM (format: #12345)
4. follow_up - User is following up, asking for updates, or being impatient
5. credentials_shared - User shared email, password, or sensitive info publicly
6. general_question - User asking general questions about Mudrex features/products

Message: "{message}"
Is DM: {is_dm}

Response format: Just return the category name, nothing else.
"""

# Response generation prompt
RESPONSE_GENERATION_PROMPT = """
You are a helpful but limited support assistant for @MudrexHelp on Twitter.

Your role:
- Be empathetic and human-like
- Keep responses short (1-2 sentences max)
- You can ONLY direct users to help@mudrex.com or ask for ticket numbers
- You cannot answer technical questions
- Vary your phrasing to sound natural

Intent: {intent}
User message: "{message}"
Ticket number (if any): {ticket_number}

Generate a response that sounds human and empathetic. Don't use phrases like "I'm here to help" or "As an AI".
"""


def classify_intent(message: str, is_dm: bool = False) -> str:
    """
    Classify the intent of a Twitter message using Gemini
    
    Args:
        message: The tweet/DM content
        is_dm: Whether this is a direct message
    
    Returns:
        Intent category as string
    """
    if not config.GEMINI_API_KEY:
        # Fallback to basic keyword matching for testing
        return _fallback_classify(message, is_dm)
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = INTENT_CLASSIFICATION_PROMPT.format(
            message=message,
            is_dm=is_dm
        )
        response = model.generate_content(prompt)
        intent = response.text.strip().lower()
        
        # Validate intent
        valid_intents = [
            "new_complaint", "has_ticket", "dm_ticket_shared",
            "follow_up", "credentials_shared", "general_question"
        ]
        
        if intent in valid_intents:
            return intent
        else:
            return "new_complaint"  # Default fallback
            
    except Exception as e:
        print(f"Error in Gemini classification: {e}")
        return _fallback_classify(message, is_dm)


def generate_response(intent: str, message: str = "", ticket_number: str = None) -> str:
    """
    Generate a response based on intent
    
    Args:
        intent: The classified intent
        message: Original user message
        ticket_number: Extracted ticket number if any
    
    Returns:
        Response text
    """
    # Use templates for consistent, tested responses
    if intent in config.RESPONSE_TEMPLATES:
        template = random.choice(config.RESPONSE_TEMPLATES[intent])
        
        # Replace ticket number if present
        if ticket_number and "{ticket_number}" in template:
            return template.format(ticket_number=ticket_number)
        
        return template
    
    # Fallback
    return random.choice(config.RESPONSE_TEMPLATES["new_complaint"])


def _fallback_classify(message: str, is_dm: bool) -> str:
    """
    Simple keyword-based classification when Gemini is not available
    """
    message_lower = message.lower()
    
    # Check for credentials
    if any(word in message_lower for word in ["password", "login", "credentials", "@gmail", "@yahoo"]):
        return "credentials_shared"
    
    # Check for ticket mention
    import re
    if re.search(config.TICKET_PATTERN, message):
        if is_dm:
            return "dm_ticket_shared"
        else:
            return "has_ticket"
    
    if any(word in message_lower for word in ["ticket", "raised", "created", "submitted"]):
        return "has_ticket"
    
    # Check for follow-up
    if any(word in message_lower for word in ["update", "status", "still waiting", "when", "how long"]):
        return "follow_up"
    
    # Check for questions
    if any(word in message_lower for word in ["how to", "what is", "can i", "does mudrex"]):
        return "general_question"
    
    # Default to new complaint
    return "new_complaint"


def extract_ticket_number(message: str) -> str:
    """
    Extract ticket number from message
    
    Args:
        message: The message text
    
    Returns:
        Ticket number without # or None
    """
    import re
    match = re.search(config.TICKET_PATTERN, message)
    if match:
        return match.group(1)  # Returns just the digits
    return None
