"""
Twitter API Client using Twikit
Handles authentication, monitoring mentions, DMs, and posting responses
"""
import asyncio
import os
import json
from typing import List, Dict, Optional
from datetime import datetime
from twikit import Client
from twikit.errors import TwitterException, TooManyRequests
import config


class TwitterClient:
    def __init__(self):
        self.client = Client('en-US')
        self.authenticated = False
        self.user_id = None
        self.username = None
        
        # Credentials from env
        self.twitter_username = os.getenv("TWITTER_USERNAME")
        self.twitter_email = os.getenv("TWITTER_EMAIL")
        self.twitter_password = os.getenv("TWITTER_PASSWORD")
        
        # Cookies file path
        self.cookies_file = os.getenv("TWITTER_COOKIES_FILE", "./data/twitter_cookies.json")
    
    async def authenticate(self) -> bool:
        """
        Authenticate with Twitter using credentials or saved cookies
        
        Returns:
            bool: True if authentication successful
        """
        try:
            # Try loading saved cookies first
            if os.path.exists(self.cookies_file):
                print("🔑 Loading saved session...")
                self.client.load_cookies(self.cookies_file)
                
                # Verify session is still valid
                try:
                    user = await self.client.user()
                    self.user_id = user.id
                    self.username = user.screen_name
                    self.authenticated = True
                    print(f"✅ Authenticated as @{self.username}")
                    return True
                except:
                    print("⚠️ Saved session expired, re-authenticating...")
            
            # Fresh login
            if not all([self.twitter_username, self.twitter_email, self.twitter_password]):
                print("❌ Twitter credentials not found in .env")
                return False
            
            print("🔑 Logging in to Twitter...")
            await self.client.login(
                auth_info_1=self.twitter_username,
                auth_info_2=self.twitter_email,
                password=self.twitter_password
            )
            
            # Save cookies
            os.makedirs(os.path.dirname(self.cookies_file), exist_ok=True)
            self.client.save_cookies(self.cookies_file)
            
            # Get user info
            user = await self.client.user()
            self.user_id = user.id
            self.username = user.screen_name
            self.authenticated = True
            
            print(f"✅ Successfully authenticated as @{self.username}")
            return True
            
        except TwitterException as e:
            print(f"❌ Twitter authentication failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error during authentication: {e}")
            return False
    
    async def get_mentions(self, count: int = 20) -> List[Dict]:
        """
        Get recent mentions of the authenticated account
        
        Args:
            count: Number of mentions to retrieve
            
        Returns:
            List of mention dictionaries
        """
        if not self.authenticated:
            print("❌ Not authenticated. Call authenticate() first.")
            return []
        
        try:
            # Search for mentions
            tweets = await self.client.search_tweet(
                f"@{self.username}",
                product='Latest',
                count=count
            )
            
            mentions = []
            for tweet in tweets:
                # Skip our own tweets
                if tweet.user.screen_name == self.username:
                    continue
                
                mention = {
                    'id': tweet.id,
                    'username': tweet.user.screen_name,
                    'user_id': tweet.user.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'tweet_url': f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}",
                    'is_reply': tweet.in_reply_to is not None,
                    'in_reply_to_id': tweet.in_reply_to
                }
                mentions.append(mention)
            
            print(f"📬 Retrieved {len(mentions)} mentions")
            return mentions
            
        except TooManyRequests as e:
            print(f"⚠️ Rate limit hit. Reset at: {e.rate_limit_reset}")
            return []
        except TwitterException as e:
            print(f"❌ Error fetching mentions: {e}")
            return []
    
    async def get_dms(self, count: int = 20) -> List[Dict]:
        """
        Get recent direct messages
        
        Args:
            count: Number of DM conversations to check
            
        Returns:
            List of DM dictionaries
        """
        if not self.authenticated:
            print("❌ Not authenticated. Call authenticate() first.")
            return []
        
        try:
            # Get DM conversations
            conversations = await self.client.get_dm_conversations()
            
            dms = []
            for conversation in conversations[:count]:
                # Get messages from this conversation
                messages = await conversation.get_messages()
                
                if messages:
                    latest_message = messages[0]
                    
                    # Skip if we sent it
                    if latest_message.sender_id == self.user_id:
                        continue
                    
                    dm = {
                        'id': latest_message.id,
                        'conversation_id': conversation.id,
                        'username': latest_message.sender.screen_name,
                        'user_id': latest_message.sender_id,
                        'text': latest_message.text,
                        'created_at': latest_message.created_at,
                        'is_dm': True
                    }
                    dms.append(dm)
            
            print(f"💬 Retrieved {len(dms)} new DMs")
            return dms
            
        except TooManyRequests as e:
            print(f"⚠️ Rate limit hit. Reset at: {e.rate_limit_reset}")
            return []
        except TwitterException as e:
            print(f"❌ Error fetching DMs: {e}")
            return []
    
    async def reply_to_tweet(self, tweet_id: str, text: str) -> bool:
        """
        Reply to a tweet
        
        Args:
            tweet_id: ID of the tweet to reply to
            text: Reply text
            
        Returns:
            bool: True if successful
        """
        if not self.authenticated:
            print("❌ Not authenticated. Call authenticate() first.")
            return False
        
        try:
            tweet = await self.client.create_tweet(
                text=text,
                reply_to=tweet_id
            )
            print(f"✅ Replied to tweet {tweet_id}")
            return True
            
        except TwitterException as e:
            print(f"❌ Error replying to tweet: {e}")
            return False
    
    async def send_dm(self, user_id: str, text: str) -> bool:
        """
        Send a direct message to a user
        
        Args:
            user_id: Twitter user ID
            text: Message text
            
        Returns:
            bool: True if successful
        """
        if not self.authenticated:
            print("❌ Not authenticated. Call authenticate() first.")
            return False
        
        try:
            await self.client.send_dm(user_id, text)
            print(f"✅ Sent DM to user {user_id}")
            return True
            
        except TwitterException as e:
            print(f"❌ Error sending DM: {e}")
            return False
    
    async def post_tweet(self, text: str) -> bool:
        """
        Post a new tweet
        
        Args:
            text: Tweet text
            
        Returns:
            bool: True if successful
        """
        if not self.authenticated:
            print("❌ Not authenticated. Call authenticate() first.")
            return False
        
        try:
            tweet = await self.client.create_tweet(text=text)
            print(f"✅ Posted tweet: {text[:50]}...")
            return True
            
        except TwitterException as e:
            print(f"❌ Error posting tweet: {e}")
            return False


# Singleton instance
twitter_client = TwitterClient()


async def test_connection():
    """Test Twitter connection"""
    print("\n🧪 Testing Twitter Connection...")
    
    if await twitter_client.authenticate():
        print("\n📱 Fetching mentions...")
        mentions = await twitter_client.get_mentions(count=5)
        
        for mention in mentions:
            print(f"\n@{mention['username']}: {mention['text'][:100]}")
        
        print("\n💬 Fetching DMs...")
        dms = await twitter_client.get_dms(count=5)
        
        for dm in dms:
            print(f"\n@{dm['username']}: {dm['text'][:100]}")
        
        print("\n✅ Twitter connection test complete!")
    else:
        print("\n❌ Twitter connection test failed!")


if __name__ == "__main__":
    asyncio.run(test_connection())
