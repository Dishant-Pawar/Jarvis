import subprocess
import os
import shutil
from utils.logger import get_logger
from utils.helpers import format_response

logger = get_logger()

# App registry mapping common spoken names to executable commands
APP_COMMANDS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "command prompt": "cmd.exe",
    "cmd": "cmd.exe",
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
    "control panel": "control.exe",
    "windows settings": "start ms-settings:",
    "settings": "start ms-settings:",
    "camera": "start microsoft.windows.camera:",
    "google chrome": "chrome.exe",
    "chrome": "chrome.exe",
    "visual studio code": "code",
    "vs code": "code"
}

def launch_app(app_name: str) -> dict:
    app_name_clean = app_name.lower().strip()
    
    # Check if app is in registry
    matched_command = None
    for name, cmd in APP_COMMANDS.items():
        if name in app_name_clean:
            matched_command = cmd
            app_name = name
            break

    if not matched_command:
        # Fallback search in path for exact match
        executable = f"{app_name_clean}.exe"
        if shutil.which(executable) or shutil.which(app_name_clean):
            matched_command = app_name_clean
        else:
            logger.warning(f"Application command not found for: {app_name}")
            return format_response(False, f"I couldn't find the application '{app_name}' installed on your system.")

    try:
        logger.info(f"Launching system application command: {matched_command}")
        
        # Handle special protocol launchers or standard subprocess spawns
        if matched_command.startswith("start "):
            # Protocol link (Settings, Camera)
            os.system(matched_command)
        else:
            # Standalone Executable (Notepad, Calculator, VS Code)
            # Use shell=True for tools like VS Code ('code') which might be path batch scripts
            subprocess.Popen(matched_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        return format_response(True, f"Successfully launched {app_name}.", {"app": app_name})
    except Exception as e:
        logger.error(f"Failed to launch system app '{app_name}': {e}")
        return format_response(False, f"Error launching application: {str(e)}")
