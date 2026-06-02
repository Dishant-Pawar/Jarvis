import sqlite3
import os
from utils.logger import get_logger

logger = get_logger()

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BACKEND_DIR, "jarvis.db")

class MemoryManager:
    def __init__(self):
        self.conn = None
        self.init_db()

    def get_connection(self):
        # Local connection per thread
        return sqlite3.connect(DB_FILE)

    def init_db(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversation_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create tables for reminders and alarms as well
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    time_str TEXT NOT NULL,
                    status TEXT DEFAULT 'ACTIVE'
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alarms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time_str TEXT NOT NULL,
                    status TEXT DEFAULT 'ACTIVE'
                )
            """)
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to initialize SQLite database: {e}")

    def save_message(self, role: str, content: str):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO conversation_memory (role, content) VALUES (?, ?)", 
                (role, content)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to save message to memory: {e}")

    def get_history(self, limit: int = 15) -> list:
        history = []
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT role, content FROM conversation_memory ORDER BY id DESC LIMIT ?", 
                (limit,)
            )
            rows = cursor.fetchall()
            conn.close()
            
            # Convert to user-role dict and reverse to chronological order
            for role, content in reversed(rows):
                history.append({
                    "role": role,
                    "content": content
                })
        except Exception as e:
            logger.error(f"Failed to retrieve conversation history: {e}")
        return history

    def clear_history(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM conversation_memory")
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Failed to clear conversation history: {e}")
            return False
