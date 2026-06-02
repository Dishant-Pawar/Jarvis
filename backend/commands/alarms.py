import sqlite3
import os
from utils.logger import get_logger
from utils.helpers import format_response

logger = get_logger()

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BACKEND_DIR, "jarvis.db")

def get_connection():
    return sqlite3.connect(DB_FILE)

def add_alarm(time_str: str) -> dict:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO alarms (time_str, status) VALUES (?, 'ACTIVE')", 
            (time_str,)
        )
        conn.commit()
        alarm_id = cursor.lastrowid
        conn.close()
        logger.info(f"Alarm set for: {time_str}")
        return format_response(True, f"Alarm successfully set for {time_str}", {"id": alarm_id})
    except Exception as e:
        logger.error(f"Error adding alarm: {e}")
        return format_response(False, f"Failed to set alarm: {str(e)}")

def delete_alarm(alarm_id: int) -> dict:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alarms WHERE id = ?", (alarm_id,))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        if rows_affected > 0:
            return format_response(True, f"Alarm #{alarm_id} deleted successfully.")
        return format_response(False, f"Alarm #{alarm_id} not found.")
    except Exception as e:
        logger.error(f"Error deleting alarm: {e}")
        return format_response(False, f"Failed to delete alarm: {str(e)}")

def list_alarms() -> dict:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, time_str, status FROM alarms WHERE status = 'ACTIVE'")
        rows = cursor.fetchall()
        conn.close()
        
        alarms_list = []
        for a_id, time_str, status in rows:
            alarms_list.append({
                "id": a_id,
                "time_str": time_str,
                "status": status
            })
            
        return format_response(True, f"Found {len(alarms_list)} active alarms.", {"alarms": alarms_list})
    except Exception as e:
        logger.error(f"Error listing alarms: {e}")
        return format_response(False, f"Failed to get alarms: {str(e)}")
