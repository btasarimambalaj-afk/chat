# 🚀 GitHub'a Yükleme Rehberi

## Repository: https://github.com/btasarimambalaj-afk/deneme

## Adım 1: Git Başlat

```bash
cd c:\Users\ASUS\Desktop\asama
git init
git branch -M main
```

## Adım 2: .gitignore Kontrol

`.gitignore` dosyası zaten hazır:
- .env (gizli kalacak)
- database.db
- __pycache__/
- *.pyc
- static/uploads/* (sadece .gitkeep kalacak)

## Adım 3: Dosyaları Ekle

```bash
git add .
git status
```

## Adım 4: Commit

```bash
git commit -m "Initial commit: Musteri Destek Sistemi v1.0"
```

## Adım 5: Remote Ekle

```bash
git remote add origin https://github.com/btasarimambalaj-afk/deneme.git
```

## Adım 6: Push

```bash
git push -u origin main
```

Eğer repo'da dosya varsa:
```bash
git push -u origin main --force
```

---

## 📋 Yüklenecek Dosyalar (33 adet)

### Backend (15)
- modules/ (10 dosya)
- routes/ (5 dosya)

### Frontend (6)
- static/css/ (2)
- static/js/ (2)
- templates/ (2)

### Config (5)
- app.py
- config.py
- requirements.txt
- Procfile
- runtime.txt

### Docs (7)
- README.md
- PROJE_PLANI.md
- DEPLOYMENT.md
- QUICKSTART.md
- FINAL_CHECKLIST.md
- TEST_RESULTS.md
- RUN_TESTS.md

### Test (3)
- test_app.py
- test_simple.py
- test_integration.py

### Other (2)
- .gitignore
- .env.example

---

## ⚠️ Önemli Notlar

1. **.env dosyası yüklenmeyecek** (gitignore'da)
2. **database.db yüklenmeyecek** (gitignore'da)
3. **uploads/ klasörü boş olacak** (sadece .gitkeep)

---

## 🔐 Sonraki Adım: Railway Deployment

GitHub'a yüklendikten sonra:

1. Railway.app'e git
2. New Project → Deploy from GitHub
3. Repository seç: btasarimambalaj-afk/deneme
4. Environment Variables ekle:
   ```
   TELEGRAM_BOT_TOKEN=8033290671:AAHHqhVnDdbIiou4FsO0ACdq7-EdsgW0of8
   TELEGRAM_ADMIN_CHAT_ID=5874850928
   SECRET_KEY=<random-32-char>
   FLASK_ENV=production
   ```
5. Deploy!

---

## ✅ Hazır!

Komutları sırayla çalıştır:

```bash
cd c:\Users\ASUS\Desktop\asama
git init
git branch -M main
git add .
git commit -m "Initial commit: Musteri Destek Sistemi v1.0"
git remote add origin https://github.com/btasarimambalaj-afk/deneme.git
git push -u origin main --force
```
