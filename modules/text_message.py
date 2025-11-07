"""
Text Message - Metin Mesaj Modülü
"""

from modules.database import save_message, get_messages

def send_text_message(user_id, sender_type, text):
    """Metin mesajı kaydet"""
    return save_message(user_id, sender_type, 'text', text)

def get_user_text_messages(user_id):
    """Kullanıcının metin mesajlarını getir"""
    all_messages = get_messages(user_id)
    return [msg for msg in all_messages if msg['message_type'] == 'text']
