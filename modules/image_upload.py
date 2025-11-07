"""
Image Upload - Görüntü Yükleme Modülü
"""

import os
import time
from PIL import Image
from werkzeug.utils import secure_filename
from modules.database import save_message
from config import Config

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_SIZE = (1920, 1920)

def save_image_file(file, user_id):
    """Resim dosyasını kaydet ve optimize et"""
    if not file or file.filename == '':
        return None
    
    filename = secure_filename(file.filename)
    if not filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
        return None
    
    # Unique filename
    timestamp = str(int(time.time() * 1000))
    filename = f"{user_id}_{timestamp}.{filename.split('.')[-1]}"
    filepath = os.path.join(Config.IMAGE_UPLOAD_FOLDER, filename)
    
    # Resmi kaydet ve optimize et
    try:
        img = Image.open(file)
        img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
        img.save(filepath, optimize=True, quality=85)
        return filepath
    except Exception as e:
        print(f"Image save error: {e}")
        return None

def send_image_message(user_id, sender_type, file):
    """Görüntü mesajı kaydet"""
    filepath = save_image_file(file, user_id)
    if filepath:
        return save_message(user_id, sender_type, 'image', filepath)
    return None
