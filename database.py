"""
Database handler for tracking conversations
"""
import sqlite3
import json
from datetime import datetime
from typing import Optional, Dict, List
import config


class ConversationDB:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or config.DATABASE_PATH
        self._init_db()
    
    def _init_db(self):
        """Initialize database with required tables"""
        # Ensure data directory exists
        import os
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                message TEXT NOT NULL,
                intent TEXT NOT NULL,
                response TEXT NOT NULL,
                is_dm BOOLEAN NOT NULL,
                ticket_number TEXT,
                escalated BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create user state table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_state (
                username TEXT PRIMARY KEY,
                last_intent TEXT,
                ticket_number TEXT,
                last_interaction TIMESTAMP,
                escalation_count INTEGER DEFAULT 0
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_conversation(
        self,
        username: str,
        message: str,
        intent: str,
        response: str,
        is_dm: bool = False,
        ticket_number: str = None,
        escalated: bool = False
    ):
        """Save a conversation to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO conversations 
            (username, message, intent, response, is_dm, ticket_number, escalated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, message, intent, response, is_dm, ticket_number, escalated))
        
        conn.commit()
        conn.close()
    
    def update_user_state(
        self,
        username: str,
        intent: str,
        ticket_number: str = None
    ):
        """Update user's conversation state"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO user_state 
            (username, last_intent, ticket_number, last_interaction)
            VALUES (?, ?, ?, ?)
        """, (username, intent, ticket_number, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_user_state(self, username: str) -> Optional[Dict]:
        """Get user's current state"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT last_intent, ticket_number, last_interaction, escalation_count
            FROM user_state
            WHERE username = ?
        """, (username,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "last_intent": row[0],
                "ticket_number": row[1],
                "last_interaction": row[2],
                "escalation_count": row[3]
            }
        return None
    
    def increment_escalation(self, username: str):
        """Increment escalation count for user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE user_state
            SET escalation_count = escalation_count + 1
            WHERE username = ?
        """, (username,))
        
        conn.commit()
        conn.close()
    
    def get_conversation_history(self, username: str, limit: int = 10) -> List[Dict]:
        """Get recent conversation history for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT message, intent, response, is_dm, ticket_number, created_at
            FROM conversations
            WHERE username = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (username, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "message": row[0],
                "intent": row[1],
                "response": row[2],
                "is_dm": bool(row[3]),
                "ticket_number": row[4],
                "created_at": row[5]
            }
            for row in rows
        ]


# Global instance
db = ConversationDB()
