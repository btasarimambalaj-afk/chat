# 🎧 Müşteri Destek Sistemi

Gerçek zamanlı müşteri destek sistemi - 320px mobil destekli, modüler yapı, Telegram entegrasyonlu

## 🌐 Production

**URL:** https://adminsohbet.up.railway.app/  
**Telegram Bot:** @Sohbet_Admin_Bot  
**Admin:** @mzengin (ID: 5874850928)

## ✨ Özellikler

### Müşteri Tarafı
- ✅ Direkt mesajlaşma (ticket sistemi yok)
- ✅ Metin/Ses/Resim gönderme
- ✅ Real-time mesaj alma (SSE)
- ✅ Kullanıcı ID (localStorage)

### Admin Tarafı
- ✅ Tüm kullanıcıları görüntüleme
- ✅ Real-time mesaj alma (SSE)
- ✅ Kullanıcılara yanıt verme
- ✅ Kullanıcı silme (cascade)
- ✅ OTP ile güvenli giriş

### Telegram Entegrasyonu
- ✅ Yeni kullanıcı bildirimi
- ✅ Yeni mesaj bildirimi
- ✅ Telegram'dan direkt cevap
- ✅ Medya desteği

## 🚀 Kurulum

### 1. Gereksinimler
```bash
Python 3.11+
```

### 2. Bağımlılıkları Yükle
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
`.env` dosyası oluştur:
```bash
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_ADMIN_CHAT_ID=your-chat-id
SECRET_KEY=your-secret-key
FLASK_ENV=development
```

### 4. Çalıştır
```bash
python app.py
```

Tarayıcıda aç: http://localhost:5000

## 📁 Proje Yapısı

```
/project
├── app.py                 # Ana uygulama
├── config.py              # Konfigürasyon
├── modules/               # Backend modüller
│   ├── database.py
│   ├── telegram_bot.py
│   ├── otp_manager.py
│   └── ...
├── routes/                # API endpoints
│   ├── chat.py
│   ├── admin.py
│   └── ...
├── static/                # Frontend
│   ├── css/
│   ├── js/
│   └── uploads/
└── templates/             # HTML
    ├── index.html
    └── admin.html
```

## 🔧 Teknolojiler

**Backend:**
- Flask 3.0
- SQLite
- SSE (Server-Sent Events)
- python-telegram-bot

**Frontend:**
- Vanilla JavaScript
- CSS3 (320px mobil öncelikli)
- HTML5

## 📝 API Endpoints

### Chat
- `POST /api/users` - Kullanıcı kaydı
- `POST /api/messages` - Mesaj gönder
- `GET /api/messages/<user_id>` - Mesajları getir
- `GET /api/stream/<user_id>` - SSE stream

### Admin
- `POST /api/admin/request-otp` - OTP iste
- `POST /api/admin/verify-otp` - OTP doğrula
- `GET /api/admin/users` - Kullanıcı listesi
- `DELETE /api/admin/users/<user_id>` - Kullanıcı sil

### Files
- `POST /api/files/upload/image` - Resim yükle
- `POST /api/files/upload/voice` - Ses yükle

## 🚀 Railway Deployment

### 1. GitHub'a Push
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Railway'de Deploy
1. Railway.app'e git
2. New Project → Deploy from GitHub
3. Repository seç
4. Environment variables ekle:
   - TELEGRAM_BOT_TOKEN
   - TELEGRAM_ADMIN_CHAT_ID
   - SECRET_KEY
   - FLASK_ENV=production

### 3. Webhook Kur
```bash
curl -X POST https://your-app.up.railway.app/api/telegram/set-webhook
```

## 📄 Lisans

MIT License

## 👨‍💻 Geliştirici

Proje Planı: PROJE_PLANI.md
