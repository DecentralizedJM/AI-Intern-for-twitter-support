"""
FastAPI webhook endpoint for n8n integration
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from twitter_handler import handler
import uvicorn

app = FastAPI(title="Twitter Support Bot API")


class TwitterMessage(BaseModel):
    username: str
    message: str
    is_dm: bool = False
    tweet_url: Optional[str] = None


class WebhookResponse(BaseModel):
    success: bool
    intent: str
    response: str
    ticket_number: Optional[str] = None
    escalated: bool = False


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "service": "Twitter Support Bot"}


@app.post("/webhook/twitter", response_model=WebhookResponse)
async def process_twitter_message(data: TwitterMessage):
    """
    Main webhook endpoint for n8n to send Twitter messages
    
    This endpoint receives Twitter mentions or DMs from n8n,
    processes them, and returns the bot's response.
    """
    try:
        result = handler.process_message(
            username=data.username,
            message=data.message,
            is_dm=data.is_dm,
            tweet_url=data.tweet_url
        )
        
        return WebhookResponse(
            success=True,
            intent=result["intent"],
            response=result["response"],
            ticket_number=result.get("ticket_number"),
            escalated=result["escalated"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/webhook/test")
async def test_webhook():
    """Test endpoint for n8n webhook validation"""
    return {"message": "Webhook is working!"}


if __name__ == "__main__":
    print("🚀 Starting Twitter Support Bot API...")
    print("📍 Webhook URL: http://localhost:8000/webhook/twitter")
    print("🧪 Test URL: http://localhost:8000/webhook/test")
    uvicorn.run(app, host="0.0.0.0", port=8000)
