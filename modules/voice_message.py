"""
Voice Message - Sesli Mesaj Modülü
"""

import os
import time
from werkzeug.utils import secure_filename
from modules.database import save_message
from config import Config

ALLOWED_EXTENSIONS = {'webm', 'ogg', 'mp3', 'wav'}

def save_voice_file(file, user_id):
    """Ses dosyasını kaydet"""
    if not file or file.filename == '':
        return None
    
    filename = secure_filename(file.filename)
    if not filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
        return None
    
    # Unique filename
    timestamp = str(int(time.time() * 1000))
    filename = f"{user_id}_{timestamp}.{filename.split('.')[-1]}"
    filepath = os.path.join(Config.VOICE_UPLOAD_FOLDER, filename)
    
    file.save(filepath)
    return filepath

def send_voice_message(user_id, sender_type, file):
    """Sesli mesaj kaydet"""
    filepath = save_voice_file(file, user_id)
    if filepath:
        return save_message(user_id, sender_type, 'voice', filepath)
    return None
