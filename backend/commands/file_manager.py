import os
import shutil
import glob
import time
from utils.logger import get_logger
from utils.helpers import format_response

logger = get_logger()

# Global clipboard variables for copy/move/paste actions
CLIPBOARD_FILE = None
CLIPBOARD_ACTION = None  # "COPY" or "MOVE"

def get_downloads_path() -> str:
    # Cross-platform downloads directory
    return os.path.join(os.path.expanduser("~"), "Downloads")

def open_downloads() -> dict:
    downloads = get_downloads_path()
    if os.path.exists(downloads):
        os.startfile(downloads)
        return format_response(True, "Opened Downloads folder.", {"path": downloads})
    return format_response(False, "Downloads folder not found.")

def open_folder(folder_path: str) -> dict:
    expanded_path = os.path.expanduser(folder_path)
    if os.path.exists(expanded_path):
        os.startfile(expanded_path)
        return format_response(True, f"Opened folder: {expanded_path}", {"path": expanded_path})
    return format_response(False, f"Folder '{folder_path}' does not exist.")

def create_file(file_path: str, content: str = "") -> dict:
    full_path = os.path.abspath(os.path.expanduser(file_path))
    try:
        # Create parent directories if missing
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return format_response(True, f"Created file: {os.path.basename(full_path)}.", {"path": full_path})
    except Exception as e:
        logger.error(f"Error creating file: {e}")
        return format_response(False, f"Failed to create file: {str(e)}")

def delete_file(file_path: str) -> dict:
    full_path = os.path.abspath(os.path.expanduser(file_path))
    try:
        if os.path.exists(full_path):
            os.remove(full_path)
            return format_response(True, f"Deleted file: {os.path.basename(full_path)}.")
        return format_response(False, "File does not exist.")
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        return format_response(False, f"Failed to delete file: {str(e)}")

def create_folder(folder_path: str) -> dict:
    full_path = os.path.abspath(os.path.expanduser(folder_path))
    try:
        os.makedirs(full_path, exist_ok=True)
        return format_response(True, f"Created folder: {os.path.basename(full_path)}.", {"path": full_path})
    except Exception as e:
        logger.error(f"Error creating folder: {e}")
        return format_response(False, f"Failed to create folder: {str(e)}")

def delete_folder(folder_path: str) -> dict:
    full_path = os.path.abspath(os.path.expanduser(folder_path))
    try:
        if os.path.exists(full_path):
            shutil.rmtree(full_path)
            return format_response(True, f"Deleted folder: {os.path.basename(full_path)}.")
        return format_response(False, "Folder does not exist.")
    except Exception as e:
        logger.error(f"Error deleting folder: {e}")
        return format_response(False, f"Failed to delete folder: {str(e)}")

def rename_item(old_path: str, new_name: str) -> dict:
    old_full = os.path.abspath(os.path.expanduser(old_path))
    if not os.path.exists(old_full):
        return format_response(False, "Source file or folder does not exist.")
        
    parent_dir = os.path.dirname(old_full)
    new_full = os.path.join(parent_dir, new_name)
    
    try:
        os.rename(old_full, new_full)
        return format_response(True, f"Successfully renamed to {new_name}.", {"path": new_full})
    except Exception as e:
        logger.error(f"Error renaming item: {e}")
        return format_response(False, f"Failed to rename: {str(e)}")

def search_files(query: str, search_dir: str = "~") -> dict:
    root_dir = os.path.expanduser(search_dir)
    results = []
    try:
        # Search depth limited for quick results
        for root, dirs, files in os.walk(root_dir):
            # Filter out hidden directories and large system/app folders
            dirs[:] = [d for d in dirs if not d.startswith('.') and d.lower() not in ['appdata', 'local settings', 'application data', 'searches', 'links', 'documents and settings', 'programdata', 'microsoft']]
            # Limit depth of search to prevent freezing
            if root.count(os.sep) - root_dir.count(os.sep) > 3:
                del dirs[:]  # skip deep dirs
                continue
                
            for file in files:
                if query.lower() in file.lower():
                    results.append(os.path.join(root, file))
                    if len(results) >= 15:  # limit results
                        break
            if len(results) >= 15:
                break
                
        return format_response(True, f"Found {len(results)} matches for '{query}'.", {"matches": results})
    except Exception as e:
        logger.error(f"Error searching files: {e}")
        return format_response(False, f"Search failed: {str(e)}")

def open_file(file_path: str) -> dict:
    full_path = os.path.abspath(os.path.expanduser(file_path))
    if os.path.exists(full_path):
        try:
            os.startfile(full_path)
            return format_response(True, f"Opening file: {os.path.basename(full_path)}.")
        except Exception as e:
            return format_response(False, f"Could not open file: {str(e)}")
    return format_response(False, f"File '{file_path}' does not exist.")

def copy_file(file_path: str) -> dict:
    global CLIPBOARD_FILE, CLIPBOARD_ACTION
    full_path = os.path.abspath(os.path.expanduser(file_path))
    if os.path.exists(full_path) and os.path.isfile(full_path):
        CLIPBOARD_FILE = full_path
        CLIPBOARD_ACTION = "COPY"
        return format_response(True, f"Copied {os.path.basename(full_path)} to clipboard.")
    return format_response(False, "File does not exist.")

def move_file(file_path: str) -> dict:
    global CLIPBOARD_FILE, CLIPBOARD_ACTION
    full_path = os.path.abspath(os.path.expanduser(file_path))
    if os.path.exists(full_path) and os.path.isfile(full_path):
        CLIPBOARD_FILE = full_path
        CLIPBOARD_ACTION = "MOVE"
        return format_response(True, f"Cut {os.path.basename(full_path)} to clipboard.")
    return format_response(False, "File does not exist.")

def paste_file(destination_dir: str) -> dict:
    global CLIPBOARD_FILE, CLIPBOARD_ACTION
    if not CLIPBOARD_FILE or not os.path.exists(CLIPBOARD_FILE):
        return format_response(False, "Clipboard is empty or source file no longer exists.")
        
    dest_path = os.path.join(os.path.abspath(os.path.expanduser(destination_dir)), os.path.basename(CLIPBOARD_FILE))
    try:
        if CLIPBOARD_ACTION == "COPY":
            shutil.copy2(CLIPBOARD_FILE, dest_path)
            return format_response(True, f"Pasted copy of {os.path.basename(CLIPBOARD_FILE)}.")
        elif CLIPBOARD_ACTION == "MOVE":
            shutil.move(CLIPBOARD_FILE, dest_path)
            old_file = CLIPBOARD_FILE
            CLIPBOARD_FILE = None  # Clear clipboard after move
            CLIPBOARD_ACTION = None
            return format_response(True, f"Moved {os.path.basename(old_file)} here.")
    except Exception as e:
        logger.error(f"Paste failed: {e}")
        return format_response(False, f"Paste failed: {str(e)}")

def get_recent_files(directory: str = "~", limit: int = 10) -> dict:
    target_dir = os.path.expanduser(directory)
    file_list = []
    try:
        for root, dirs, files in os.walk(target_dir):
            # Filter out hidden directories and large system/app folders
            dirs[:] = [d for d in dirs if not d.startswith('.') and d.lower() not in ['appdata', 'local settings', 'application data', 'searches', 'links', 'documents and settings', 'programdata', 'microsoft']]
            if root.count(os.sep) - target_dir.count(os.sep) > 2:
                del dirs[:]
                continue
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    mtime = os.path.getmtime(filepath)
                    file_list.append((filepath, mtime))
                except Exception:
                    continue
        
        # Sort by modification time desc
        file_list.sort(key=lambda x: x[1], reverse=True)
        recent = [x[0] for x in file_list[:limit]]
        return format_response(True, "Fetched recent files.", {"recent": recent})
    except Exception as e:
        logger.error(f"Error fetching recent files: {e}")
        return format_response(False, f"Failed to get recent files: {str(e)}")

def organize_folder(folder_path: str) -> dict:
    target_dir = os.path.abspath(os.path.expanduser(folder_path))
    if not os.path.exists(target_dir):
        return format_response(False, f"Directory '{folder_path}' does not exist.")

    # Extension category mappings
    categories = {
        "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".csv", ".pptx", ".md"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
        "Audio": [".mp3", ".wav", ".aac", ".flac", ".m4a"],
        "Video": [".mp4", ".mkv", ".avi", ".mov", ".flv"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Programs": [".exe", ".msi", ".bat", ".cmd"]
    }

    moved_count = 0
    try:
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            if os.path.isfile(item_path):
                ext = os.path.splitext(item)[1].lower()
                
                # Determine category
                matched_category = "Others"
                for cat, extensions in categories.items():
                    if ext in extensions:
                        matched_category = cat
                        break
                
                # Move to category subfolder
                cat_dir = os.path.join(target_dir, matched_category)
                os.makedirs(cat_dir, exist_ok=True)
                shutil.move(item_path, os.path.join(cat_dir, item))
                moved_count += 1
                
        return format_response(True, f"Organized {moved_count} files into categorized folders.")
    except Exception as e:
        logger.error(f"Error organizing folder: {e}")
        return format_response(False, f"Organization failed: {str(e)}")
