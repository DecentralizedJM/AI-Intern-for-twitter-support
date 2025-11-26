"""
Twitter message handler with mock data for testing
"""
from typing import Dict, Optional
import gemini_handler
import slack_handler
from database import db


class TwitterHandler:
    def __init__(self):
        self.mock_mode = True  # Will be True until Twitter API is connected
    
    def process_message(
        self,
        username: str,
        message: str,
        is_dm: bool = False,
        tweet_url: str = None
    ) -> Dict:
        """
        Process a Twitter message (mention or DM) and generate response
        
        Args:
            username: Twitter username (without @)
            message: The message content
            is_dm: Whether this is a DM
            tweet_url: URL to the tweet
        
        Returns:
            Dict with response and metadata
        """
        print(f"\n{'='*60}")
        print(f"Processing {'DM' if is_dm else 'Tweet'} from @{username}")
        print(f"Message: {message}")
        print(f"{'='*60}")
        
        # Get user's previous state
        user_state = db.get_user_state(username)
        
        # Classify intent
        intent = gemini_handler.classify_intent(message, is_dm)
        print(f"📊 Intent: {intent}")
        
        # Extract ticket number if present
        ticket_number = gemini_handler.extract_ticket_number(message)
        
        # Handle special cases
        response = None
        escalated = False
        
        # Case 1: User shared credentials publicly
        if intent == "credentials_shared" and not is_dm:
            response = gemini_handler.generate_response("credentials_warning")
        
        # Case 2: DM with ticket number
        elif intent == "dm_ticket_shared" and is_dm and ticket_number:
            # Escalate to Slack
            original_complaint = self._get_original_complaint(username)
            slack_handler.send_escalation(
                ticket_number=ticket_number,
                username=username,
                tweet_url=tweet_url,
                original_message=original_complaint
            )
            response = gemini_handler.generate_response(
                "dm_ticket_received",
                ticket_number=ticket_number
            )
            escalated = True
            db.increment_escalation(username)
        
        # Case 3: User mentions having a ticket
        elif intent == "has_ticket":
            response = gemini_handler.generate_response("has_ticket")
        
        # Case 4: Follow-up/stalking
        elif intent == "follow_up":
            response = gemini_handler.generate_response("follow_up")
        
        # Case 5: General question
        elif intent == "general_question":
            response = gemini_handler.generate_response("general_question")
        
        # Case 6: DM without ticket number
        elif is_dm and intent != "dm_ticket_shared":
            response = gemini_handler.generate_response("dm_no_ticket")
        
        # Default: New complaint
        else:
            response = gemini_handler.generate_response("new_complaint")
        
        # Save to database
        db.save_conversation(
            username=username,
            message=message,
            intent=intent,
            response=response,
            is_dm=is_dm,
            ticket_number=ticket_number,
            escalated=escalated
        )
        
        # Update user state
        db.update_user_state(
            username=username,
            intent=intent,
            ticket_number=ticket_number
        )
        
        print(f"\n💬 Response: {response}")
        
        return {
            "username": username,
            "intent": intent,
            "response": response,
            "ticket_number": ticket_number,
            "escalated": escalated,
            "is_dm": is_dm
        }
    
    def _get_original_complaint(self, username: str) -> Optional[str]:
        """Get the original complaint message from user's history"""
        history = db.get_conversation_history(username, limit=5)
        for conv in history:
            if conv["intent"] in ["new_complaint", "has_ticket"]:
                return conv["message"]
        return None


# Global instance
handler = TwitterHandler()
