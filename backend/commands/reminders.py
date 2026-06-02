import sqlite3
import os
from utils.logger import get_logger
from utils.helpers import format_response

logger = get_logger()

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BACKEND_DIR, "jarvis.db")

def get_connection():
    return sqlite3.connect(DB_FILE)

def add_reminder(title: str, time_str: str) -> dict:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reminders (title, time_str, status) VALUES (?, ?, 'ACTIVE')", 
            (title, time_str)
        )
        conn.commit()
        reminder_id = cursor.lastrowid
        conn.close()
        logger.info(f"Reminder added: {title} at {time_str}")
        return format_response(True, f"Reminder set for {time_str}: '{title}'", {"id": reminder_id})
    except Exception as e:
        logger.error(f"Error adding reminder: {e}")
        return format_response(False, f"Failed to set reminder: {str(e)}")

def delete_reminder(reminder_id: int) -> dict:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        if rows_affected > 0:
            return format_response(True, f"Reminder #{reminder_id} deleted successfully.")
        return format_response(False, f"Reminder #{reminder_id} not found.")
    except Exception as e:
        logger.error(f"Error deleting reminder: {e}")
        return format_response(False, f"Failed to delete reminder: {str(e)}")

def list_reminders() -> dict:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, time_str, status FROM reminders WHERE status = 'ACTIVE'")
        rows = cursor.fetchall()
        conn.close()
        
        reminders_list = []
        for r_id, title, time_str, status in rows:
            reminders_list.append({
                "id": r_id,
                "title": title,
                "time_str": time_str,
                "status": status
            })
            
        return format_response(True, f"Found {len(reminders_list)} active reminders.", {"reminders": reminders_list})
    except Exception as e:
        logger.error(f"Error listing reminders: {e}")
        return format_response(False, f"Failed to get reminders: {str(e)}")
