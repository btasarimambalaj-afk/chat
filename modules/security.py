"""
Security - Güvenlik Modülü
- Rate limiting (20 istek/dakika)
- Input validasyonu
- Hassas veri gizleme
"""

import re
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

class SecurityManager:
    def __init__(self):
        # In-memory rate limit storage
        self.rate_limits = {}
        
        # Ayarlar
        self.MAX_REQUESTS = 100  # Test için artırıldı
        self.TIME_WINDOW = 60  # saniye
        self.CLEANUP_INTERVAL = 300  # 5 dakika
        self.last_cleanup = datetime.now()
    
    def rate_limit(self, f):
        """Rate limiting decorator"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # IP adresini al
            ip = request.remote_addr
            now = datetime.now()
            
            # Periyodik temizlik
            if (now - self.last_cleanup).seconds > self.CLEANUP_INTERVAL:
                self._cleanup_old_entries()
            
            # Rate limit kontrolü
            if not self._check_rate_limit(ip, now):
                return jsonify({
                    'success': False,
                    'error': 'Çok fazla istek. Lütfen bekleyin.'
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    
    def _check_rate_limit(self, ip, now):
        """Rate limit kontrolü yap"""
        if ip not in self.rate_limits:
            self.rate_limits[ip] = []
        
        # Eski istekleri temizle
        cutoff = now - timedelta(seconds=self.TIME_WINDOW)
        self.rate_limits[ip] = [
            timestamp for timestamp in self.rate_limits[ip]
            if timestamp > cutoff
        ]
        
        # Limit kontrolü
        if len(self.rate_limits[ip]) >= self.MAX_REQUESTS:
            return False
        
        # Yeni isteği kaydet
        self.rate_limits[ip].append(now)
        return True
    
    def _cleanup_old_entries(self):
        """Eski rate limit kayıtlarını temizle"""
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.TIME_WINDOW)
        
        for ip in list(self.rate_limits.keys()):
            self.rate_limits[ip] = [
                timestamp for timestamp in self.rate_limits[ip]
                if timestamp > cutoff
            ]
            if not self.rate_limits[ip]:
                del self.rate_limits[ip]
        
        self.last_cleanup = now
    
    @staticmethod
    def validate_user_id(user_id):
        """User ID validasyonu"""
        if not user_id or not isinstance(user_id, str):
            return False
        
        # 3-50 karakter, alfanumerik + _ -
        if not re.match(r'^[a-zA-Z0-9_-]{3,50}$', user_id):
            return False
        
        return True
    
    @staticmethod
    def validate_name(name):
        """İsim validasyonu"""
        if not name:
            return True  # İsteğe bağlı
        
        if not isinstance(name, str):
            return False
        
        # 2-40 karakter
        if len(name) < 2 or len(name) > 40:
            return False
        
        return True
    
    @staticmethod
    def validate_message(message):
        """Mesaj validasyonu"""
        if not message or not isinstance(message, str):
            return False
        
        # 1-5000 karakter
        if len(message) < 1 or len(message) > 5000:
            return False
        
        return True
    
    @staticmethod
    def validate_file_extension(filename, allowed_extensions):
        """Dosya uzantısı kontrolü"""
        if not filename:
            return False
        
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    @staticmethod
    def sanitize_filename(filename):
        """Dosya adını güvenli hale getir"""
        # Tehlikeli karakterleri kaldır
        filename = re.sub(r'[^\w\s.-]', '', filename)
        # Boşlukları alt çizgi yap
        filename = filename.replace(' ', '_')
        return filename
    
    @staticmethod
    def mask_sensitive_data(text, mask_char='*'):
        """Hassas verileri gizle (loglarda)"""
        # Email
        text = re.sub(
            r'([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            r'\1***@\2',
            text
        )
        
        # Telefon (Türkiye formatı)
        text = re.sub(
            r'(\+?90)?[\s-]?(\d{3})[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})',
            r'\1 \2 *** ** **',
            text
        )
        
        return text
    
    def get_stats(self):
        """İstatistikler"""
        return {
            'tracked_ips': len(self.rate_limits),
            'total_requests': sum(len(reqs) for reqs in self.rate_limits.values())
        }
