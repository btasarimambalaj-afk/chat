# 🚀 Deployment Guide

## Local Development

### 1. Kurulum
```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Test et
python test_app.py

# Çalıştır
python app.py
```

Tarayıcıda aç: http://localhost:5000

### 2. Environment Variables
`.env` dosyasını düzenle:
```bash
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_ADMIN_CHAT_ID=your-chat-id
SECRET_KEY=your-secret-key
FLASK_ENV=development
```

---

## Railway Deployment

### 1. GitHub'a Push
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/username/repo.git
git push -u origin main
```

### 2. Railway Setup
1. https://railway.app/ → Login
2. **New Project** → **Deploy from GitHub**
3. Repository seç
4. **Add Variables** (Environment):
   ```
   TELEGRAM_BOT_TOKEN=8033290671:AAHHqhVnDdbIiou4FsO0ACdq7-EdsgW0of8
   TELEGRAM_ADMIN_CHAT_ID=5874850928
   SECRET_KEY=<generate-random-32-char-string>
   FLASK_ENV=production
   PORT=5000
   ```

### 3. Deploy
- Railway otomatik deploy eder
- Build logs'u kontrol et
- Deploy tamamlandığında URL alırsın

### 4. Webhook Kurulumu
Deploy sonrası webhook'u kur:
```bash
curl -X POST https://your-app.up.railway.app/api/telegram/set-webhook
```

Veya tarayıcıda aç:
```
https://your-app.up.railway.app/api/telegram/set-webhook
```

---

## Heroku Deployment (Alternatif)

### 1. Heroku CLI Kur
```bash
# macOS
brew install heroku/brew/heroku

# Windows
# https://devcenter.heroku.com/articles/heroku-cli
```

### 2. Login & Create
```bash
heroku login
heroku create your-app-name
```

### 3. Environment Variables
```bash
heroku config:set TELEGRAM_BOT_TOKEN=your-token
heroku config:set TELEGRAM_ADMIN_CHAT_ID=your-chat-id
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production
```

### 4. Deploy
```bash
git push heroku main
```

### 5. Webhook
```bash
curl -X POST https://your-app-name.herokuapp.com/api/telegram/set-webhook
```

---

## Vercel Deployment (Alternatif)

### 1. vercel.json Oluştur
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### 2. Deploy
```bash
npm i -g vercel
vercel
```

### 3. Environment Variables
Vercel Dashboard → Settings → Environment Variables

---

## Docker Deployment (Gelişmiş)

### 1. Dockerfile Oluştur
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

### 2. Build & Run
```bash
docker build -t customer-support .
docker run -p 5000:5000 --env-file .env customer-support
```

---

## Troubleshooting

### Database Hatası
```bash
# Database'i sıfırla
rm database.db
python app.py
```

### Port Hatası
```bash
# Farklı port kullan
PORT=8000 python app.py
```

### Telegram Webhook Hatası
```bash
# Webhook'u kontrol et
curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo

# Webhook'u sil
curl https://api.telegram.org/bot<TOKEN>/deleteWebhook

# Yeniden kur
curl -X POST https://your-app.up.railway.app/api/telegram/set-webhook
```

### Upload Klasörü Hatası
```bash
# Klasörleri oluştur
mkdir -p static/uploads/images
mkdir -p static/uploads/voices
```

---

## Production Checklist

- [ ] `.env` dosyası `.gitignore`'da
- [ ] `SECRET_KEY` güçlü ve unique
- [ ] `FLASK_ENV=production`
- [ ] Telegram credentials doğru
- [ ] Database backup stratejisi
- [ ] HTTPS aktif
- [ ] Webhook kuruldu
- [ ] Error logging aktif
- [ ] Rate limiting test edildi

---

## Monitoring

### Logs
```bash
# Railway
railway logs

# Heroku
heroku logs --tail

# Local
tail -f app.log
```

### Health Check
```bash
curl https://your-app.up.railway.app/
```

---

## Backup

### Database
```bash
# Backup
cp database.db database.backup.db

# Restore
cp database.backup.db database.db
```

### Uploads
```bash
# Backup
tar -czf uploads.tar.gz static/uploads/

# Restore
tar -xzf uploads.tar.gz
```
