"""
Telegram Bot - Mesaj Gönderme Modülü
- Yeni kullanıcı bildirimi
- Yeni mesaj bildirimi
- Medya desteği (metin/ses/görüntü)
- Retry mekanizması
"""

import os
import requests
import threading
import time
from datetime import datetime

class TelegramBot:
    def __init__(self, token, admin_chat_id):
        self.token = token
        self.admin_chat_id = admin_chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"
        
    def send_message(self, text, parse_mode='HTML'):
        """Telegram'a metin mesajı gönder"""
        url = f"{self.base_url}/sendMessage"
        data = {
            'chat_id': self.admin_chat_id,
            'text': text,
            'parse_mode': parse_mode
        }
        return self._send_with_retry(url, data)
    
    def send_photo(self, photo_path, caption=''):
        """Telegram'a fotoğraf gönder"""
        url = f"{self.base_url}/sendPhoto"
        
        with open(photo_path, 'rb') as photo:
            files = {'photo': photo}
            data = {
                'chat_id': self.admin_chat_id,
                'caption': caption,
                'parse_mode': 'HTML'
            }
            return self._send_with_retry(url, data, files)
    
    def send_voice(self, voice_path, caption=''):
        """Telegram'a ses dosyası gönder"""
        url = f"{self.base_url}/sendVoice"
        
        with open(voice_path, 'rb') as voice:
            files = {'voice': voice}
            data = {
                'chat_id': self.admin_chat_id,
                'caption': caption,
                'parse_mode': 'HTML'
            }
            return self._send_with_retry(url, data, files)
    
    def _send_with_retry(self, url, data, files=None, max_retries=3):
        """Retry mekanizması ile gönder"""
        for attempt in range(max_retries):
            try:
                if files:
                    response = requests.post(url, data=data, files=files, timeout=10)
                else:
                    response = requests.post(url, json=data, timeout=10)
                
                if response.status_code == 200:
                    return {'success': True, 'data': response.json()}
                else:
                    print(f"Telegram API error: {response.text}")
                    
            except Exception as e:
                print(f"Telegram send error (attempt {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(1)
        
        return {'success': False, 'error': 'Max retries exceeded'}
    
    def notify_new_user(self, user_id, name):
        """Yeni kullanıcı bildirimi"""
        text = f"""
🆕 <b>Yeni Kullanıcı</b>

👤 İsim: {name or 'Anonim'}
🆔 ID: {user_id}
🕐 Zaman: {datetime.now().strftime('%H:%M:%S')}

💬 Kullanıcı mesaj bekliyoruz...
        """
        threading.Thread(target=self.send_message, args=(text,)).start()
    
    def notify_new_message(self, user_id, name, message_type, content):
        """Yeni mesaj bildirimi"""
        type_emoji = {
            'text': '💬',
            'voice': '🎤',
            'image': '📷'
        }
        
        text = f"""
{type_emoji.get(message_type, '💬')} <b>Yeni Mesaj</b>

👤 {name or 'Anonim'} (ID: {user_id})
🕐 {datetime.now().strftime('%H:%M:%S')}
        """
        
        if message_type == 'text':
            text += f"\n\n💬 Mesaj:\n{content[:200]}"
            threading.Thread(target=self.send_message, args=(text,)).start()
        elif message_type == 'voice':
            threading.Thread(target=self.send_voice, args=(content, text)).start()
        elif message_type == 'image':
            threading.Thread(target=self.send_photo, args=(content, text)).start()
    
    def send_admin_reply(self, user_id, name, message_type, content):
        """Admin yanıtını Telegram'a bildir"""
        type_emoji = {
            'text': '💬',
            'voice': '🎤',
            'image': '📷'
        }
        
        text = f"""
✅ <b>Yanıt Gönderildi</b>

👤 Alıcı: {name or 'Anonim'} (ID: {user_id})
{type_emoji.get(message_type, '💬')} Tip: {message_type.upper()}
🕐 {datetime.now().strftime('%H:%M:%S')}
        """
        
        threading.Thread(target=self.send_message, args=(text,)).start()
