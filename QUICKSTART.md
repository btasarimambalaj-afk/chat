# 🚀 QUICK START GUIDE

## 5 Dakikada Başla!

### 1️⃣ Kurulum (2 dakika)

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Test et
python test_app.py
```

### 2️⃣ Konfigürasyon (1 dakika)

`.env` dosyasını düzenle:
```bash
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_ADMIN_CHAT_ID=your-chat-id
SECRET_KEY=your-secret-key
FLASK_ENV=development
```

### 3️⃣ Çalıştır (1 dakika)

```bash
python app.py
```

Tarayıcıda aç:
- **Müşteri:** http://localhost:5000
- **Admin:** http://localhost:5000/admin

### 4️⃣ Test Et (1 dakika)

**Müşteri Tarafı:**
1. İsim gir
2. Mesaj yaz
3. Gönder

**Admin Tarafı:**
1. OTP iste (Telegram'a gelecek)
2. OTP gir
3. Giriş yap

---

## 🌐 Production Deployment

### Railway (Önerilen)

```bash
# 1. GitHub'a push
git init
git add .
git commit -m "Initial commit"
git push origin main

# 2. Railway.app'e git
# - New Project
# - Deploy from GitHub
# - Repository seç

# 3. Environment Variables ekle
TELEGRAM_BOT_TOKEN=...
TELEGRAM_ADMIN_CHAT_ID=...
SECRET_KEY=...
FLASK_ENV=production

# 4. Deploy!
# Otomatik deploy olacak

# 5. Webhook kur
curl -X POST https://your-app.up.railway.app/api/telegram/set-webhook
```

---

## 🔑 Telegram Bot Kurulumu

### 1. Bot Oluştur
```
1. @BotFather'a git
2. /newbot komutunu gönder
3. Bot adı ver
4. Bot username ver
5. Token'ı kopyala
```

### 2. Chat ID Bul
```
1. Bot'a mesaj gönder
2. https://api.telegram.org/bot<TOKEN>/getUpdates
3. "chat":{"id": BURASI} kopyala
```

### 3. .env'e Ekle
```bash
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_ADMIN_CHAT_ID=123456789
```

---

## 📱 Kullanım

### Müşteri
1. Siteyi aç
2. İsim gir (isteğe bağlı)
3. Mesaj yaz / Resim gönder / Ses kaydet
4. Admin yanıtını bekle (real-time)

### Admin
1. /admin'e git
2. OTP iste
3. Telegram'dan OTP'yi al
4. Giriş yap
5. Kullanıcıları gör
6. Chat aç
7. Yanıt ver

---

## 🐛 Sorun Giderme

### Port Hatası
```bash
# Farklı port kullan
PORT=8000 python app.py
```

### Database Hatası
```bash
# Database'i sıfırla
rm database.db
python app.py
```

### Telegram Hatası
```bash
# Webhook'u kontrol et
curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo

# Webhook'u sil
curl https://api.telegram.org/bot<TOKEN>/deleteWebhook

# Yeniden kur
curl -X POST https://your-app.up.railway.app/api/telegram/set-webhook
```

### Upload Hatası
```bash
# Klasörleri oluştur
mkdir -p static/uploads/images
mkdir -p static/uploads/voices
```

---

## 📞 Destek

- **Dokümantasyon:** README.md
- **Deployment:** DEPLOYMENT.md
- **Checklist:** FINAL_CHECKLIST.md
- **Proje Planı:** PROJE_PLANI.md

---

**Hazır! Artık kullanabilirsin! 🎉**
