"""
Telegram Webhook - Telegram'dan Mesaj Alma
- Reply mesajlarını yakala
- User ID'yi parse et
- Database'e admin mesajı olarak kaydet
"""

import re
import os
import requests
from modules.database import save_message
from config import Config

class TelegramWebhook:
    def __init__(self, telegram_token):
        self.token = telegram_token
        self.base_url = f"https://api.telegram.org/bot{telegram_token}"
    
    def process_update(self, update_data):
        """Telegram'dan gelen update'i işle"""
        try:
            message = update_data.get('message', {})
            
            # Reply mesajı mı kontrol et
            reply_to = message.get('reply_to_message')
            if not reply_to:
                return {'success': False, 'error': 'Not a reply message'}
            
            # User ID'yi bul (reply edilen mesajın caption'ından)
            user_id = self._extract_user_id(reply_to)
            if not user_id:
                return {'success': False, 'error': 'User ID not found'}
            
            # Mesaj tipini belirle ve kaydet
            if message.get('text'):
                return self._handle_text(user_id, message['text'])
            elif message.get('voice'):
                return self._handle_voice(user_id, message['voice'])
            elif message.get('photo'):
                return self._handle_photo(user_id, message['photo'])
            else:
                return {'success': False, 'error': 'Unsupported message type'}
                
        except Exception as e:
            print(f"Webhook process error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _extract_user_id(self, reply_message):
        """Reply edilen mesajdan user ID'yi çıkar"""
        caption = reply_message.get('caption', '')
        text = reply_message.get('text', '')
        content = caption or text
        
        # "ID: user_123" formatını ara
        match = re.search(r'ID:\s*([a-zA-Z0-9_-]+)', content)
        if match:
            return match.group(1)
        return None
    
    def _handle_text(self, user_id, text):
        """Metin mesajını kaydet"""
        try:
            save_message(user_id, 'admin', 'text', text)
            return {'success': True, 'type': 'text'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _handle_voice(self, user_id, voice_data):
        """Ses mesajını indir ve kaydet"""
        try:
            file_id = voice_data['file_id']
            file_path = self._download_file(file_id, 'voice')
            
            if file_path:
                save_message(user_id, 'admin', 'voice', file_path)
                return {'success': True, 'type': 'voice'}
            else:
                return {'success': False, 'error': 'File download failed'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _handle_photo(self, user_id, photo_data):
        """Fotoğrafı indir ve kaydet"""
        try:
            file_id = photo_data[-1]['file_id']
            file_path = self._download_file(file_id, 'image')
            
            if file_path:
                save_message(user_id, 'admin', 'image', file_path)
                return {'success': True, 'type': 'image'}
            else:
                return {'success': False, 'error': 'File download failed'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _download_file(self, file_id, file_type):
        """Telegram'dan dosya indir"""
        try:
            # File path al
            url = f"{self.base_url}/getFile?file_id={file_id}"
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                return None
            
            file_path = response.json()['result']['file_path']
            file_url = f"https://api.telegram.org/file/bot{self.token}/{file_path}"
            
            # Dosyayı indir
            file_response = requests.get(file_url, timeout=30)
            if file_response.status_code != 200:
                return None
            
            # Kaydet
            folder = Config.VOICE_UPLOAD_FOLDER if file_type == 'voice' else Config.IMAGE_UPLOAD_FOLDER
            filename = f"telegram_{file_id}.{file_path.split('.')[-1]}"
            local_path = os.path.join(folder, filename)
            
            with open(local_path, 'wb') as f:
                f.write(file_response.content)
            
            return local_path
        except Exception as e:
            print(f"File download error: {e}")
            return None
