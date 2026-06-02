import os
import time
import subprocess
import pyautogui
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from utils.logger import get_logger
from utils.helpers import format_response

logger = get_logger()

def get_volume_interface():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(interface, POINTER(IAudioEndpointVolume))
    except Exception as e:
        logger.error(f"Failed to access audio device endpoints: {e}")
        return None

def change_volume(direction: str) -> dict:
    volume = get_volume_interface()
    if not volume:
        return format_response(False, "Could not access system audio speakers.")

    try:
        current_volume = volume.GetMasterVolumeLevelScalar()
        if direction.lower() == "up":
            new_volume = min(1.0, current_volume + 0.1)
            msg = f"Volume increased to {int(new_volume * 100)}%."
        else:
            new_volume = max(0.0, current_volume - 0.1)
            msg = f"Volume decreased to {int(new_volume * 100)}%."
            
        volume.SetMasterVolumeLevelScalar(new_volume, None)
        return format_response(True, msg, {"volume": int(new_volume * 100)})
    except Exception as e:
        logger.error(f"Error adjusting volume: {e}")
        return format_response(False, f"Error adjusting volume: {str(e)}")

def toggle_mute(mute_state: bool) -> dict:
    volume = get_volume_interface()
    if not volume:
        return format_response(False, "Could not access system audio speakers.")

    try:
        volume.SetMute(1 if mute_state else 0, None)
        status = "muted" if mute_state else "unmuted"
        return format_response(True, f"Audio successfully {status}.", {"muted": mute_state})
    except Exception as e:
        logger.error(f"Error setting mute status: {e}")
        return format_response(False, f"Error setting mute: {str(e)}")

def change_brightness(direction: str) -> dict:
    try:
        brightness_list = sbc.get_brightness()
        if not brightness_list:
            return format_response(False, "No brightness-adjustable monitors detected.")
        current_brightness = brightness_list[0]
        if direction.lower() == "up":
            new_brightness = min(100, current_brightness + 10)
            msg = f"Brightness increased to {new_brightness}%."
        else:
            new_brightness = max(0, current_brightness - 10)
            msg = f"Brightness decreased to {new_brightness}%."
            
        sbc.set_brightness(new_brightness)
        return format_response(True, msg, {"brightness": new_brightness})
    except Exception as e:
        logger.error(f"Error adjusting brightness: {e}")
        return format_response(False, f"Error adjusting screen brightness: {str(e)}")

def take_screenshot() -> dict:
    try:
        # Create screenshots folder in project dir
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ss_dir = os.path.join(project_dir, "screenshots")
        os.makedirs(ss_dir, exist_ok=True)
        
        filename = f"screenshot_{int(time.time())}.png"
        filepath = os.path.join(ss_dir, filename)
        
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        
        logger.info(f"Screenshot saved to: {filepath}")
        return format_response(True, "Screenshot captured successfully.", {"filepath": filepath})
    except Exception as e:
        logger.error(f"Failed to capture screenshot: {e}")
        return format_response(False, f"Failed to take screenshot: {str(e)}")

def toggle_wifi(enable: bool) -> dict:
    try:
        status = "enabled" if enable else "disabled"
        admin_action = "enabled" if enable else "disabled"
        
        # Netsh command on Windows to enable/disable Wi-Fi interface
        cmd = f'netsh interface set interface name="Wi-Fi" admin={admin_action}'
        # Execute cmd (requires admin permissions)
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            return format_response(True, f"Wi-Fi interface has been {status}.")
        else:
            # Fallback to Powershell command
            ps_cmd = f"powershell -Command \"Start-Process netsh -ArgumentList 'interface set interface \\\"Wi-Fi\\\" admin={admin_action}' -Verb RunAs\""
            subprocess.Popen(ps_cmd, shell=True)
            return format_response(True, f"Requested administrator privilege to turn Wi-Fi {status}.")
    except Exception as e:
        logger.error(f"Failed to toggle Wi-Fi: {e}")
        return format_response(False, f"Failed to toggle Wi-Fi: {str(e)}")

def toggle_bluetooth(enable: bool) -> dict:
    try:
        status = "on" if enable else "off"
        # Toggling bluetooth on Windows usually requires device controller scripts
        # We trigger a powershell command that loads radio manager classes
        action = "Enable-NetAdapter" if enable else "Disable-NetAdapter"
        ps_cmd = f'powershell -Command "Start-Process powershell -ArgumentList \'-Command Get-Service -Name bthserv | Set-Service -Status { "Running" if enable else "Stopped" }\' -Verb RunAs"'
        subprocess.Popen(ps_cmd, shell=True)
        return format_response(True, f"Requested administrator privilege to toggle Bluetooth {status}.", {"bluetooth": status})
    except Exception as e:
        logger.error(f"Failed to toggle Bluetooth: {e}")
        return format_response(False, f"Failed to toggle Bluetooth: {str(e)}")

def lock_pc() -> dict:
    try:
        logger.info("Locking Windows workstation...")
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return format_response(True, "Station locked successfully.")
    except Exception as e:
        logger.error(f"Failed to lock workstation: {e}")
        return format_response(False, f"Failed to lock PC: {str(e)}")

def shutdown_pc() -> dict:
    try:
        logger.info("Triggering system shutdown...")
        os.system("shutdown /s /t 1")
        return format_response(True, "System is shutting down.")
    except Exception as e:
        logger.error(f"Shutdown trigger failed: {e}")
        return format_response(False, f"Failed to shutdown PC: {str(e)}")

def restart_pc() -> dict:
    try:
        logger.info("Triggering system restart...")
        os.system("shutdown /r /t 1")
        return format_response(True, "System is restarting.")
    except Exception as e:
        logger.error(f"Restart trigger failed: {e}")
        return format_response(False, f"Failed to restart PC: {str(e)}")

def sleep_pc() -> dict:
    try:
        logger.info("Triggering sleep mode...")
        # Uses powrprof dll to trigger sleep/suspend
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return format_response(True, "System entering sleep mode.")
    except Exception as e:
        logger.error(f"Sleep trigger failed: {e}")
        return format_response(False, f"Failed to enter sleep mode: {str(e)}")
