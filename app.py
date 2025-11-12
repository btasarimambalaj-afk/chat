"""
Müşteri Destek Sistemi - Basitleştirilmiş Versiyon
"""

import os
import logging
from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
from datetime import datetime
import sqlite3
import json
import queue

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
CORS(app)

# Database
DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
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

# SSE Manager
sse_queues = {}

def create_sse_queue(user_id):
    if user_id not in sse_queues:
        sse_queues[user_id] = queue.Queue(maxsize=100)
    return sse_queues[user_id]

def notify_sse(user_id, data):
    if user_id in sse_queues:
        try:
            sse_queues[user_id].put(data, block=False)
        except queue.Full:
            pass

# Routes
@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'Server is running'}, 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

# API - Register User
@app.route('/api/users', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        name = data.get('name', 'Anonim')
        
        if not user_id:
            return jsonify({'success': False, 'error': 'User ID gerekli'}), 400
        
        conn = get_db()
        try:
            conn.execute('INSERT INTO users (id, name) VALUES (?, ?)', (user_id, name))
            conn.commit()
            logger.info(f"User created: {user_id}")
        except sqlite3.IntegrityError:
            logger.info(f"User already exists: {user_id}")
        finally:
            conn.close()
        
        return jsonify({'success': True, 'user_id': user_id})
    except Exception as e:
        logger.error(f"Register error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# API - Send Message
@app.route('/api/messages', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        sender_type = data.get('sender_type', 'customer')
        message_type = data.get('message_type', 'text')
        content = data.get('content')
        
        if not user_id or not content:
            return jsonify({'success': False, 'error': 'Eksik veri'}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Kullanıcı var mı?
        cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'error': 'Kullanıcı bulunamadı'}), 404
        
        # Mesajı kaydet
        cursor.execute('''
            INSERT INTO messages (user_id, sender_type, message_type, content)
            VALUES (?, ?, ?, ?)
        ''', (user_id, sender_type, message_type, content))
        
        message_id = cursor.lastrowid
        
        # Last seen güncelle
        cursor.execute('UPDATE users SET last_seen = CURRENT_TIMESTAMP WHERE id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        
        # SSE bildirimi
        notify_sse(user_id, {
            'id': message_id,
            'user_id': user_id,
            'sender_type': sender_type,
            'message_type': message_type,
            'content': content,
            'created_at': datetime.now().isoformat()
        })
        
        logger.info(f"Message saved: {message_id}")
        return jsonify({'success': True, 'message_id': message_id})
        
    except Exception as e:
        logger.error(f"Send message error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# API - Get Messages
@app.route('/api/messages/<user_id>', methods=['GET'])
def get_messages(user_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM messages 
            WHERE user_id = ? 
            ORDER BY created_at ASC
        ''', (user_id,))
        messages = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({'success': True, 'messages': messages})
    except Exception as e:
        logger.error(f"Get messages error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# API - SSE Stream
@app.route('/api/stream/<user_id>')
def stream_messages(user_id):
    q = create_sse_queue(user_id)
    
    def event_stream():
        while True:
            try:
                message = q.get(timeout=30)
                yield f"data: {json.dumps(message)}\n\n"
            except queue.Empty:
                yield f"data: {json.dumps({'type': 'ping'})}\n\n"
    
    return Response(event_stream(), mimetype='text/event-stream')

# API - Admin Users
@app.route('/api/admin/users', methods=['GET'])
def get_users():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users ORDER BY last_seen DESC')
        users = [dict(row) for row in cursor.fetchall()]
        
        # Her kullanıcı için mesaj sayısı
        for user in users:
            cursor.execute('SELECT COUNT(*) as count FROM messages WHERE user_id = ?', (user['id'],))
            user['message_count'] = cursor.fetchone()['count']
        
        conn.close()
        return jsonify({'success': True, 'users': users})
    except Exception as e:
        logger.error(f"Get users error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# API - Admin Delete User
@app.route('/api/admin/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        # SSE bildirimi gönder
        notify_sse(user_id, {
            'type': 'user_deleted',
            'message': 'Oturumunuz sonlandırıldı'
        })
        
        conn = get_db()
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        # SSE queue temizle
        if user_id in sse_queues:
            del sse_queues[user_id]
        
        logger.info(f"User deleted: {user_id}")
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Delete user error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# API - Admin OTP (Basitleştirilmiş)
@app.route('/api/admin/request-otp', methods=['POST'])
def request_otp():
    import secrets
    otp = ''.join(secrets.choice('0123456789') for _ in range(6))
    logger.info(f"OTP Generated: {otp}")
    return jsonify({'success': True, 'otp': otp, 'token': 'admin-token'})

@app.route('/api/admin/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    otp = data.get('otp')
    # Basit doğrulama - production'da düzelt
    if otp and len(otp) == 6:
        return jsonify({'success': True, 'token': 'admin-token'})
    return jsonify({'success': False, 'error': 'Geçersiz OTP'}), 400

# Error Handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

# Initialize
init_db()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
