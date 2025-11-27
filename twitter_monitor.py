"""
Twitter Monitor - Continuously monitors mentions and DMs
Integrates with existing twitter_handler.py for processing
"""
import asyncio
from datetime import datetime
from typing import Set
import os
from twitter_client import twitter_client
from twitter_handler import TwitterHandler
from database import db


class TwitterMonitor:
    def __init__(self, poll_interval: int = 60):
        """
        Initialize Twitter Monitor
        
        Args:
            poll_interval: Seconds between each poll (default: 60)
        """
        self.poll_interval = poll_interval
        self.handler = TwitterHandler()
        self.processed_ids: Set[str] = set()
        self.running = False
        
        # Load previously processed IDs from database
        self._load_processed_ids()
    
    def _load_processed_ids(self):
        """Load previously processed tweet/DM IDs to avoid duplicates"""
        # Get recent processed IDs from database
        recent = db.get_recent_conversations(limit=100)
        for conv in recent:
            if 'tweet_id' in conv:
                self.processed_ids.add(conv['tweet_id'])
    
    async def process_mentions(self):
        """Fetch and process new mentions"""
        print(f"\n📬 Checking mentions... [{datetime.now().strftime('%H:%M:%S')}]")
        
        mentions = await twitter_client.get_mentions(count=20)
        new_mentions = 0
        
        for mention in mentions:
            # Skip if already processed
            if mention['id'] in self.processed_ids:
                continue
            
            # Process the mention
            result = self.handler.process_message(
                username=mention['username'],
                message=mention['text'],
                is_dm=False,
                tweet_url=mention['tweet_url']
            )
            
            # Send reply
            if result.get('response'):
                success = await twitter_client.reply_to_tweet(
                    tweet_id=mention['id'],
                    text=result['response']
                )
                
                if success:
                    print(f"✅ Replied to @{mention['username']}")
                    self.processed_ids.add(mention['id'])
                    new_mentions += 1
                else:
                    print(f"❌ Failed to reply to @{mention['username']}")
        
        if new_mentions > 0:
            print(f"✅ Processed {new_mentions} new mentions")
        else:
            print("📭 No new mentions")
    
    async def process_dms(self):
        """Fetch and process new DMs"""
        print(f"\n💬 Checking DMs... [{datetime.now().strftime('%H:%M:%S')}]")
        
        dms = await twitter_client.get_dms(count=20)
        new_dms = 0
        
        for dm in dms:
            # Skip if already processed
            if dm['id'] in self.processed_ids:
                continue
            
            # Process the DM
            result = self.handler.process_message(
                username=dm['username'],
                message=dm['text'],
                is_dm=True,
                tweet_url=None
            )
            
            # Send DM reply
            if result.get('response'):
                success = await twitter_client.send_dm(
                    user_id=dm['user_id'],
                    text=result['response']
                )
                
                if success:
                    print(f"✅ Replied to DM from @{dm['username']}")
                    self.processed_ids.add(dm['id'])
                    new_dms += 1
                else:
                    print(f"❌ Failed to reply to DM from @{dm['username']}")
        
        if new_dms > 0:
            print(f"✅ Processed {new_dms} new DMs")
        else:
            print("📭 No new DMs")
    
    async def monitor_loop(self):
        """Main monitoring loop"""
        print("\n" + "="*60)
        print("🤖 AI Twitter Intern - Starting Monitor")
        print("="*60)
        
        # Authenticate
        if not await twitter_client.authenticate():
            print("❌ Authentication failed. Exiting.")
            return
        
        print(f"\n⏰ Polling every {self.poll_interval} seconds")
        print("Press Ctrl+C to stop\n")
        
        self.running = True
        iteration = 0
        
        try:
            while self.running:
                iteration += 1
                print(f"\n{'='*60}")
                print(f"🔄 Poll #{iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'='*60}")
                
                # Process mentions and DMs
                await self.process_mentions()
                await self.process_dms()
                
                # Wait before next poll
                print(f"\n⏸️  Sleeping for {self.poll_interval} seconds...")
                await asyncio.sleep(self.poll_interval)
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Shutting down gracefully...")
            self.running = False
        except Exception as e:
            print(f"\n❌ Error in monitor loop: {e}")
            raise
    
    def start(self):
        """Start the monitor"""
        asyncio.run(self.monitor_loop())


def main():
    """Main entry point"""
    # Get poll interval from env or default to 60 seconds
    poll_interval = int(os.getenv("TWITTER_POLL_INTERVAL", "60"))
    
    monitor = TwitterMonitor(poll_interval=poll_interval)
    monitor.start()


if __name__ == "__main__":
    main()
