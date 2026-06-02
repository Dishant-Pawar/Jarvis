import os
import re
import threading
import time
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configuration and Settings Manager
from config.settings_manager import SettingsManager

# AI clients
from ai.memory_manager import MemoryManager
from ai.assistant_router import AssistantRouter

# Voice processing
from voice.text_to_speech import TextToSpeech
from voice.speech_to_text import SpeechToText
from voice.continuous_listener import ContinuousListener

# Command modules
from commands.system_apps import launch_app
from commands.pc_control import (
    change_volume, toggle_mute, change_brightness,
    take_screenshot, toggle_wifi, toggle_bluetooth,
    lock_pc, shutdown_pc, restart_pc, sleep_pc
)
from commands.file_manager import (
    create_file, delete_file, create_folder, delete_folder,
    rename_item, search_files, open_file, open_downloads,
    copy_file, move_file, paste_file, get_recent_files, organize_folder,
    open_folder, get_downloads_path
)
from commands.reminders import add_reminder, delete_reminder, list_reminders
from commands.alarms import add_alarm, delete_alarm, list_alarms
from commands.weather import get_weather
from commands.news import get_news
from commands.pdf_reader import read_pdf, summarize_pdf
from commands.email_sender import send_email

from utils.logger import get_logger
from utils.helpers import format_response

logger = get_logger()

# Initialize managers
settings = SettingsManager()
memory = MemoryManager()
ai_router = AssistantRouter(settings, memory)

# Initialize TTS
voice_config = settings.get_setting("voice_settings", {})
tts = TextToSpeech(
    rate=voice_config.get("rate", 180),
    volume=voice_config.get("volume", 1.0),
    voice_id=voice_config.get("voice_id", None)
)

# Initialize STT
stt = SpeechToText()

app = FastAPI(title="Jarvis AI Assistant Backend")

# Enable CORS for React frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# State for background email conversation steps
email_conversation = {
    "active": False,
    "recipient": "",
    "subject": "",
    "step": 0  # 1: Subject, 2: Message body
}

# Request schemas
class CommandRequest(BaseModel):
    command: str

class SettingsUpdateRequest(BaseModel):
    openrouter_api_key: str = None
    grok_api_key: str = None
    gemini_api_key: str = None
    default_provider: str = None
    voice_rate: int = None
    voice_volume: float = None
    voice_id: str = None
    stt_lang: str = None
    tts_lang: str = None
    smtp_server: str = None
    smtp_port: int = None
    smtp_email: str = None
    smtp_password: str = None


# ========================================================
# CENTRAL COMMAND ROUTER LOGIC
# ========================================================
def route_command(command_text: str) -> dict:
    global email_conversation
    cmd = command_text.strip().lower()
    
    if not cmd:
        return format_response(False, "Empty command received.")

    logger.info(f"Routing command: '{command_text}'")

    # ----------------------------------------------------
    # 0. Active Conversation Steps (Email)
    # ----------------------------------------------------
    if email_conversation["active"]:
        if email_conversation["step"] == 1:
            email_conversation["subject"] = command_text
            email_conversation["step"] = 2
            response_msg = "What is the message?"
            tts.speak(response_msg)
            return format_response(True, response_msg, {"email_step": "body"})
        elif email_conversation["step"] == 2:
            body = command_text
            recipient = email_conversation["recipient"]
            subject = email_conversation["subject"]
            
            # Reset conversation state
            email_conversation["active"] = False
            email_conversation["recipient"] = ""
            email_conversation["subject"] = ""
            email_conversation["step"] = 0
            
            # Send the email
            res = send_email(settings, recipient, subject, body)
            if res["success"]:
                tts.speak(res["message"])
            return res

    # ----------------------------------------------------
    # 1. System App Commands
    # ----------------------------------------------------
    app_patterns = [
        r"(?:open|launch|start)\s+(notepad|calculator|cmd|command prompt|file explorer|explorer|control panel|settings|camera|google chrome|chrome|visual studio code|vs code)",
        r"(notepad|calculator|cmd|command prompt|file explorer|explorer|control panel|settings|camera|google chrome|chrome|visual studio code|vs code)"
    ]
    for pattern in app_patterns:
        match = re.search(pattern, cmd)
        if match:
            app_name = match.group(1)
            res = launch_app(app_name)
            if res["success"]:
                tts.speak(res["message"])
            return res

    # ----------------------------------------------------
    # 2. PC Control Commands
    # ----------------------------------------------------
    if "volume up" in cmd or "increase volume" in cmd:
        res = change_volume("up")
        tts.speak(res["message"])
        return res
    if "volume down" in cmd or "decrease volume" in cmd:
        res = change_volume("down")
        tts.speak(res["message"])
        return res
    if "mute audio" in cmd or "mute" in cmd:
        res = toggle_mute(True)
        tts.speak(res["message"])
        return res
    if "unmute audio" in cmd or "unmute" in cmd:
        res = toggle_mute(False)
        tts.speak(res["message"])
        return res
    if "brightness increase" in cmd or "increase brightness" in cmd:
        res = change_brightness("up")
        tts.speak(res["message"])
        return res
    if "brightness decrease" in cmd or "decrease brightness" in cmd:
        res = change_brightness("down")
        tts.speak(res["message"])
        return res
    if "take screenshot" in cmd or "capture screen" in cmd or "screenshot" in cmd:
        res = take_screenshot()
        tts.speak(res["message"])
        return res
    if "turn on wifi" in cmd or "wifi on" in cmd:
        res = toggle_wifi(True)
        tts.speak(res["message"])
        return res
    if "turn off wifi" in cmd or "wifi off" in cmd:
        res = toggle_wifi(False)
        tts.speak(res["message"])
        return res
    if "turn on bluetooth" in cmd or "bluetooth on" in cmd:
        res = toggle_bluetooth(True)
        tts.speak(res["message"])
        return res
    if "turn off bluetooth" in cmd or "bluetooth off" in cmd:
        res = toggle_bluetooth(False)
        tts.speak(res["message"])
        return res
    if "lock pc" in cmd or "lock computer" in cmd:
        res = lock_pc()
        return res
    if "shutdown pc" in cmd or "shutdown computer" in cmd or "shutdown" in cmd:
        res = shutdown_pc()
        tts.speak(res["message"])
        return res
    if "restart pc" in cmd or "restart computer" in cmd or "restart" in cmd:
        res = restart_pc()
        tts.speak(res["message"])
        return res
    if "sleep pc" in cmd or "sleep mode" in cmd or "sleep computer" in cmd:
        res = sleep_pc()
        return res

    # ----------------------------------------------------
    # 3. File Management Commands
    # ----------------------------------------------------
    # Open Downloads
    if "open downloads folder" in cmd or "open downloads" in cmd:
        res = open_downloads()
        tts.speak(res["message"])
        return res
        
    # Open Folder
    match = re.search(r"open folder\s+(.+)", cmd)
    if match:
        folder = match.group(1)
        res = open_folder(folder)
        tts.speak(res["message"])
        return res

    # Create File
    match = re.search(r"create file\s+([a-zA-Z0-9_\-\.]+)", cmd)
    if match:
        filename = match.group(1)
        res = create_file(filename)
        tts.speak(res["message"])
        return res

    # Delete File
    match = re.search(r"delete file\s+([a-zA-Z0-9_\-\.]+)", cmd)
    if match:
        filename = match.group(1)
        res = delete_file(filename)
        tts.speak(res["message"])
        return res

    # Create Folder
    match = re.search(r"create folder\s+(.+)", cmd)
    if match:
        folder = match.group(1)
        res = create_folder(folder)
        tts.speak(res["message"])
        return res

    # Delete Folder
    match = re.search(r"delete folder\s+(.+)", cmd)
    if match:
        folder = match.group(1)
        res = delete_folder(folder)
        tts.speak(res["message"])
        return res

    # Rename File/Folder
    match = re.search(r"rename\s+(.+?)\s+to\s+(.+)", cmd)
    if match:
        old_path = match.group(1)
        new_name = match.group(2)
        res = rename_item(old_path, new_name)
        tts.speak(res["message"])
        return res

    # Copy File
    match = re.search(r"copy file\s+(.+)", cmd)
    if match:
        filename = match.group(1)
        res = copy_file(filename)
        tts.speak(res["message"])
        return res

    # Move File (Cut)
    match = re.search(r"move file\s+(.+)", cmd)
    if match:
        filename = match.group(1)
        res = move_file(filename)
        tts.speak(res["message"])
        return res

    # Paste File
    match = re.search(r"paste file\s+in\s+(.+)", cmd)
    if match:
        folder = match.group(1)
        res = paste_file(folder)
        tts.speak(res["message"])
        return res
    if "paste file" in cmd:
        # Paste in current working directory as default
        res = paste_file(os.getcwd())
        tts.speak(res["message"])
        return res

    # Search Documents / Files
    match = re.search(r"(?:search documents|search files|search)\s+(.+)", cmd)
    if match:
        query = match.group(1)
        res = search_files(query)
        tts.speak(res["message"])
        return res

    # Open Recent Files
    if "open recent files" in cmd or "open recents" in cmd:
        res = get_recent_files()
        tts.speak(res["message"])
        return res

    # Open Specific Files
    match = re.search(r"open file\s+(.+)", cmd)
    if match:
        filename = match.group(1)
        res = open_file(filename)
        tts.speak(res["message"])
        return res

    # Organize Files Automatically
    match = re.search(r"organize folder\s+(.+)", cmd)
    if match:
        folder = match.group(1)
        res = organize_folder(folder)
        tts.speak(res["message"])
        return res
    if "organize downloads" in cmd:
        res = organize_folder(get_downloads_path())
        tts.speak(res["message"])
        return res

    # ----------------------------------------------------
    # 4. Reminders Module
    # ----------------------------------------------------
    # Add Reminder
    match = re.search(r"remind me\s+(.+?)\s+at\s+(.+)", cmd)
    if match:
        title = match.group(1)
        time_val = match.group(2)
        res = add_reminder(title, time_val)
        tts.speak(res["message"])
        return res

    # Delete Reminder
    match = re.search(r"delete reminder\s+(\d+)", cmd)
    if match:
        rem_id = int(match.group(1))
        res = delete_reminder(rem_id)
        tts.speak(res["message"])
        return res

    # View Reminders
    if "show reminders" in cmd or "view reminders" in cmd or "list reminders" in cmd:
        res = list_reminders()
        # Read reminders list as speech
        if res["success"] and res["data"].get("reminders"):
            items = [f"{r['title']} at {r['time_str']}" for r in res["data"]["reminders"]]
            tts.speak("Active reminders are: " + ", ".join(items))
        else:
            tts.speak("No active reminders set.")
        return res

    # ----------------------------------------------------
    # 5. Alarms Module
    # ----------------------------------------------------
    # Set Alarm
    match = re.search(r"set alarm for\s+(.+)", cmd)
    if match:
        time_val = match.group(1)
        res = add_alarm(time_val)
        tts.speak(res["message"])
        return res

    # Delete Alarm
    match = re.search(r"delete alarm\s+(\d+)", cmd)
    if match:
        al_id = int(match.group(1))
        res = delete_alarm(al_id)
        tts.speak(res["message"])
        return res

    # List Alarms
    if "list alarms" in cmd or "show alarms" in cmd:
        res = list_alarms()
        if res["success"] and res["data"].get("alarms"):
            items = [r['time_str'] for r in res["data"]["alarms"]]
            tts.speak("Active alarms set for: " + ", ".join(items))
        else:
            tts.speak("No active alarms set.")
        return res

    # ----------------------------------------------------
    # 6. Weather Commands
    # ----------------------------------------------------
    match = re.search(r"weather in\s+(.+)", cmd)
    if match:
        city = match.group(1)
        res = get_weather(city)
        tts.speak(res["message"])
        return res
    if "today's weather" in cmd or "weather" in cmd:
        res = get_weather()
        tts.speak(res["message"])
        return res

    # ----------------------------------------------------
    # 7. News Commands
    # ----------------------------------------------------
    if "technology news" in cmd or "tech news" in cmd:
        res = get_news("technology")
        tts.speak(res["message"])
        return res
    if "latest news" in cmd or "news" in cmd:
        res = get_news()
        tts.speak(res["message"])
        return res

    # ----------------------------------------------------
    # 8. Email Setup Initiation
    # ----------------------------------------------------
    match = re.search(r"send email to\s+(.+)", cmd)
    if match:
        recipient = match.group(1).strip()
        email_conversation["active"] = True
        email_conversation["recipient"] = recipient
        email_conversation["step"] = 1
        
        response_msg = "What is the subject?"
        tts.speak(response_msg)
        return format_response(True, response_msg, {"email_step": "subject"})

    # ----------------------------------------------------
    # 9. PDF Reader Commands
    # ----------------------------------------------------
    match = re.search(r"summarize pdf\s+(.+)", cmd)
    if match:
        pdf_file = match.group(1).strip()
        res = summarize_pdf(pdf_file, ai_router)
        if res["success"]:
            tts.speak("Summary generated successfully.")
        return res
    match = re.search(r"read(?: this)? pdf\s+(.+)", cmd)
    if match:
        pdf_file = match.group(1).strip()
        res = read_pdf(pdf_file)
        if res["success"]:
            tts.speak("PDF extraction complete.")
        return res

    # ----------------------------------------------------
    # 10. AI Chat Assistant (Fallback Handler)
    # ----------------------------------------------------
    # If no command categories matched, route directly to LLM chat assistant
    logger.info("Command did not match system rules. Routing to LLM...")
    response_text = ai_router.query_assistant(command_text)
    tts.speak(response_text)
    return format_response(True, response_text, {"ai_response": response_text})


# ========================================================
# HTTP ENDPOINTS
# ========================================================

@app.post("/api/command")
async def execute_command(req: CommandRequest):
    try:
        response_data = route_command(req.command)
        return response_data
    except Exception as e:
        logger.error(f"Error handling command API request: {e}")
        return format_response(False, f"Internal Error: {str(e)}")

@app.get("/api/settings")
async def get_settings():
    settings.load_config()
    return format_response(True, "Settings retrieved.", settings.config)

@app.post("/api/settings")
async def update_settings(req: SettingsUpdateRequest):
    try:
        settings.load_config()
        if req.openrouter_api_key is not None:
            settings.set_setting("openrouter_api_key", req.openrouter_api_key)
        if req.grok_api_key is not None:
            settings.set_setting("grok_api_key", req.grok_api_key)
        if req.gemini_api_key is not None:
            settings.set_setting("gemini_api_key", req.gemini_api_key)
        if req.default_provider is not None:
            settings.set_setting("default_provider", req.default_provider)
            
        # Re-apply voice configurations
        global tts
        voice_settings = settings.get_setting("voice_settings", {})
        if req.voice_rate is not None:
            voice_settings["rate"] = req.voice_rate
        if req.voice_volume is not None:
            voice_settings["volume"] = req.voice_volume
        if req.voice_id is not None:
            voice_settings["voice_id"] = req.voice_id
        settings.set_setting("voice_settings", voice_settings)
        
        # Apply language preferences
        lang_settings = settings.get_setting("language_settings", {})
        if req.stt_lang is not None:
            lang_settings["stt_lang"] = req.stt_lang
        if req.tts_lang is not None:
            lang_settings["tts_lang"] = req.tts_lang
        settings.set_setting("language_settings", lang_settings)

        # Apply SMTP details
        if req.smtp_server is not None:
            settings.set_setting("smtp_server", req.smtp_server)
        if req.smtp_port is not None:
            settings.set_setting("smtp_port", req.smtp_port)
        if req.smtp_email is not None:
            settings.set_setting("smtp_email", req.smtp_email)
        if req.smtp_password is not None:
            settings.set_setting("smtp_password", req.smtp_password)

        # Refresh local TTS instance
        tts = TextToSpeech(
            rate=voice_settings.get("rate", 180),
            volume=voice_settings.get("volume", 1.0),
            voice_id=voice_settings.get("voice_id", None)
        )
        
        return format_response(True, "Configurations updated successfully.")
    except Exception as e:
        logger.error(f"Failed to update settings: {e}")
        return format_response(False, f"Update config failed: {str(e)}")

@app.get("/api/voices")
async def list_voices():
    voices = tts.get_available_voices()
    return format_response(True, "Available voices retrieved.", {"voices": voices})

@app.post("/api/voice/listen")
async def listen_mic():
    """
    HTTP route to actively listen for a single speech input command.
    """
    settings.load_config()
    lang = settings.get_setting("language_settings", {}).get("stt_lang", "en-US")
    
    transcription = stt.listen_and_transcribe(timeout=4, phrase_time_limit=5, language=lang)
    if transcription:
        return format_response(True, "Speech transcribed.", {"text": transcription})
    return format_response(False, "Could not hear or transcribe any voice input.")

# Continuous Wake-word listener instance
background_listener = None

@app.post("/api/voice/wakeword/toggle")
async def toggle_wakeword_listener(enable: bool):
    global background_listener
    
    def on_wakeword_command(cmd_text):
        # Trigger route command asynchronously
        logger.info(f"Wake word callback triggered command execution: {cmd_text}")
        route_command(cmd_text)

    try:
        if enable:
            if not background_listener:
                background_listener = ContinuousListener(on_wakeword_command, settings)
            background_listener.start()
            return format_response(True, "Continuous wake word listener activated.")
        else:
            if background_listener:
                background_listener.stop()
                background_listener = None
            return format_response(True, "Continuous wake word listener deactivated.")
    except Exception as e:
        logger.error(f"Error toggling wake word: {e}")
        return format_response(False, f"Failed to toggle listener: {str(e)}")


# ========================================================
# BACKGROUND CRON WORKER FOR ALARMS & REMINDERS
# ========================================================
def run_scheduler_poller():
    """
    Runs in a daemon thread checking SQLite database for active reminders and alarms.
    Runs check loop every 15 seconds.
    """
    logger.info("Alarm and Reminder background cron scheduler active.")
    while True:
        try:
            # Check Alarms
            import sqlite3
            conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis.db"))
            cursor = conn.cursor()
            
            current_time = time.strftime("%H:%M") # HH:MM
            current_time_alt = time.strftime("%I:%M %p") # 12-hour format, e.g. "10:00 AM"
            
            # Check active alarms
            cursor.execute("SELECT id, time_str FROM alarms WHERE status='ACTIVE'")
            alarms = cursor.fetchall()
            for al_id, time_str in alarms:
                cleaned_al = time_str.strip().lower()
                if cleaned_al == current_time.lower() or cleaned_al == current_time_alt.lower() or cleaned_al == current_time.lstrip("0") or cleaned_al == current_time_alt.lower().lstrip("0"):
                    # Trigger Alarm!
                    logger.info(f"ALARM TRIGGERED: {time_str}")
                    tts.speak("Attention! Your alarm is ringing. Wake up!")
                    # Disable alarm so it doesn't trigger repeatedly
                    cursor.execute("UPDATE alarms SET status='INACTIVE' WHERE id=?", (al_id,))
            
            # Check active reminders
            cursor.execute("SELECT id, title, time_str FROM reminders WHERE status='ACTIVE'")
            reminders = cursor.fetchall()
            for rem_id, title, time_str in reminders:
                # We can match date/time or just standard time indicators
                cleaned_rem = time_str.strip().lower()
                # Simple time matches
                if current_time in cleaned_rem or current_time_alt.lower() in cleaned_rem:
                    logger.info(f"REMINDER TRIGGERED: {title}")
                    tts.speak(f"Attention! You have a reminder: {title}.")
                    cursor.execute("UPDATE reminders SET status='INACTIVE' WHERE id=?", (rem_id,))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error in scheduler background poller: {e}")
            
        time.sleep(15)

# Start Daemon Scheduler thread on import/launch
scheduler_thread = threading.Thread(target=run_scheduler_poller, daemon=True)
scheduler_thread.start()


# ========================================================
# ENTRY POINT
# ========================================================
if __name__ == "__main__":
    logger.info("Initializing Jarvis Windows AI Voice Assistant Backend...")
    # Port 8000 is used by default for local integration
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
