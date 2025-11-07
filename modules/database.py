import sqlite3
import logging
from datetime import datetime
from config import Config

logger = logging.getLogger(__name__)

def get_db():
    """Database bağlantısı"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')  # CASCADE DELETE için gerekli
    return conn

def init_db():
    """Veritabanı tablolarını oluştur"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Messages tablosu (CASCADE DELETE)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            sender_type TEXT NOT NULL,
            message_type TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized")

def create_user(user_id, name, email=None):
    """Yeni kullanıcı oluştur"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO users (id, name, email) 
            VALUES (?, ?, ?)
        ''', (user_id, name, email))
        conn.commit()
        logger.info(f"User created: {user_id}")
        return True
    except sqlite3.IntegrityError:
        logger.warning(f"User already exists: {user_id}")
        return False
    finally:
        conn.close()

def get_user(user_id):
    """Kullanıcı bilgisi"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def get_all_users():
    """Tüm kullanıcılar"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users ORDER BY last_seen DESC')
    users = cursor.fetchall()
    conn.close()
    return [dict(user) for user in users]

def update_last_seen(user_id):
    """Son görülme zamanını güncelle"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET last_seen = CURRENT_TIMESTAMP 
        WHERE id = ?
    ''', (user_id,))
    conn.commit()
    conn.close()

def delete_user(user_id):
    """Kullanıcıyı sil (CASCADE ile mesajlar da silinir)"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    logger.info(f"User deleted: {user_id}")

def save_message(user_id, sender_type, message_type, content):
    """Mesaj kaydet"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (user_id, sender_type, message_type, content)
        VALUES (?, ?, ?, ?)
    ''', (user_id, sender_type, message_type, content))
    conn.commit()
    message_id = cursor.lastrowid
    conn.close()
    logger.info(f"Message saved: {message_id}")
    return message_id

def get_messages(user_id):
    """Kullanıcının tüm mesajları"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM messages 
        WHERE user_id = ? 
        ORDER BY created_at ASC
    ''', (user_id,))
    messages = cursor.fetchall()
    conn.close()
    return [dict(msg) for msg in messages]

def get_stats():
    """İstatistikler"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Toplam mesaj sayısı
    cursor.execute('SELECT COUNT(*) as count FROM messages')
    total_messages = cursor.fetchone()['count']
    
    # Toplam kullanıcı sayısı
    cursor.execute('SELECT COUNT(*) as count FROM users')
    total_users = cursor.fetchone()['count']
    
    conn.close()
    
    return {
        'total_messages': total_messages,
        'total_users': total_users
    }
