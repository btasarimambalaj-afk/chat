"""
OTP Manager - Tek Kullanımlık Şifre Yönetimi
- 6 haneli OTP oluştur (kriptografik güvenli)
- OTP doğrula (5 dk geçerli, 3 deneme)
- Session yönetimi (10 saat)
"""

import secrets
import string
from datetime import datetime, timedelta

class OTPManager:
    def __init__(self):
        # In-memory storage
        self.otp_codes = {}
        self.admin_sessions = {}
        
        # Ayarlar
        self.OTP_LENGTH = 6
        self.OTP_EXPIRY_MINUTES = 5
        self.MAX_ATTEMPTS = 3
        self.SESSION_HOURS = 10
    
    def generate_otp(self, session_id):
        """Kriptografik güvenli OTP oluştur"""
        # 6 haneli sayısal kod
        code = ''.join(secrets.choice(string.digits) for _ in range(self.OTP_LENGTH))
        
        # Kaydet
        self.otp_codes[session_id] = {
            'code': code,
            'expires': datetime.now() + timedelta(minutes=self.OTP_EXPIRY_MINUTES),
            'attempts': 0,
            'created_at': datetime.now()
        }
        
        # Eski OTP'leri temizle
        self._cleanup_expired_otps()
        
        return code
    
    def verify_otp(self, session_id, code):
        """OTP'yi doğrula"""
        otp_data = self.otp_codes.get(session_id)
        
        if not otp_data:
            return {'success': False, 'error': 'OTP bulunamadı'}
        
        # Süre kontrolü
        if datetime.now() > otp_data['expires']:
            del self.otp_codes[session_id]
            return {'success': False, 'error': 'OTP süresi doldu'}
        
        # Deneme sayısı kontrolü
        if otp_data['attempts'] >= self.MAX_ATTEMPTS:
            del self.otp_codes[session_id]
            return {'success': False, 'error': 'Çok fazla hatalı deneme'}
        
        # Kod kontrolü
        if otp_data['code'] == code:
            # Başarılı - OTP'yi sil ve session oluştur
            del self.otp_codes[session_id]
            self._create_session(session_id)
            return {'success': True}
        else:
            # Hatalı - deneme sayısını artır
            otp_data['attempts'] += 1
            remaining = self.MAX_ATTEMPTS - otp_data['attempts']
            return {
                'success': False, 
                'error': f'Hatalı kod. Kalan deneme: {remaining}'
            }
    
    def _create_session(self, session_id):
        """Admin session oluştur"""
        self.admin_sessions[session_id] = {
            'authenticated': True,
            'timestamp': datetime.now(),
            'expires': datetime.now() + timedelta(hours=self.SESSION_HOURS)
        }
    
    def is_authenticated(self, session_id):
        """Session kontrolü"""
        session = self.admin_sessions.get(session_id)
        
        if not session:
            return False
        
        # Süre kontrolü
        if datetime.now() > session['expires']:
            del self.admin_sessions[session_id]
            return False
        
        return True
    
    def logout(self, session_id):
        """Session'ı sonlandır"""
        if session_id in self.admin_sessions:
            del self.admin_sessions[session_id]
    
    def _cleanup_expired_otps(self):
        """Süresi dolmuş OTP'leri temizle"""
        now = datetime.now()
        expired = [sid for sid, data in self.otp_codes.items() if now > data['expires']]
        for sid in expired:
            del self.otp_codes[sid]
    
    def get_stats(self):
        """İstatistikler"""
        return {
            'active_otps': len(self.otp_codes),
            'active_sessions': len(self.admin_sessions)
        }
