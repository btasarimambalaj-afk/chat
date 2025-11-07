# Müşteri Destek Sistemi - Proje Planı

## 📋 Proje Özeti
Gerçek zamanlı müşteri destek sistemi - 320px mobil destekli, modüler yapı, Telegram entegrasyonlu

**🌐 Production URL:** https://adminsohbet.up.railway.app/  
**🤖 Telegram Bot:** @Sohbet_Admin_Bot  
**👤 Admin:** @mzengin (ID: 5874850928)

---

## 🎯 Temel Özellikler

### Müşteri Tarafı (index.html)
- ✅ Direkt mesajlaşma (ticket sistemi yok)
- ✅ Metin mesaj gönderme
- ✅ Sesli mesaj gönderme
- ✅ Resim/görüntü gönderme
- ✅ **Real-time mesaj alma (SSE)** - Sayfa yenileme yok
- ✅ Kullanıcı ID (localStorage)

### Admin Tarafı (admin.html)
- ✅ Tüm kullanıcıları görüntüleme
- ✅ **Real-time mesaj alma (SSE)** - Anlık bildirim
- ✅ Kullanıcılara yanıt verme (metin/ses/resim)
- ✅ **Kullanıcı silme** - Tüm mesajlar + dosyalar silinir
- ✅ **OTP ile güvenli giriş** (5 dk geçerli, 10 saat session)

### Telegram Entegrasyonu 🔥
- ✅ **Yeni kullanıcı bildirimi** - Anında haberdar ol
- ✅ **Yeni mesaj bildirimi** - Her mesajda bildirim
- ✅ **Telegram'dan direkt cevap** - Reply ile yanıt ver
- ✅ **Medya desteği** - Metin/Ses/Görüntü gönder

---

## 🏗️ Teknoloji Yığını

### Frontend
- **HTML5** - Yapı
- **CSS3** - Stil (320px mobil öncelikli)
- **JavaScript (Vanilla)** - İnteraktivite
- **SSE (Server-Sent Events)** - Real-time mesajlaşma

### Backend
- **Python 3.x**
- **Flask** - Web framework
- **SQLite** - Veritabanı (basit, dosya tabanlı)
- **Threading** - Asenkron işlemler

### Güvenlik
- **Flask-WTF** - CSRF koruması
- **Rate Limiting** - Spam önleme (in-memory)
- **OTP** - Tek kullanımlık şifre (5 dk geçerli)
- **Session** - 10 saatlik admin oturumu

### Telegram
- **python-telegram-bot** - Bot API
- **Webhook** - Telegram'dan mesaj alma
- **Retry Mekanizması** - 3 deneme + fallback

### Deployment
- **Railway** - Hosting platform
- **Gunicorn** - WSGI server
- **SQLite** - Persistent storage

### Kütüphaneler
```bash
Flask==3.0.0
flask-wtf==1.2.1
pillow==10.1.0
python-telegram-bot==20.7
requests==2.31.0
gunicorn==21.2.0
python-dotenv==1.0.0
```

---

## 📁 Dosya Yapısı

```
/project
  │
  ├── Procfile                  # 🔥 Railway config
  ├── runtime.txt               # 🔥 Python version
  ├── .gitignore                # 🔥 Git ignore
  ├── .env.example              # 🔥 Environment template
  ├── app.py                    # Ana Flask uygulaması
  ├── config.py                 # Konfigürasyon ayarları
  ├── database.db               # SQLite veritabanı (otomatik oluşur)
  ├── requirements.txt          # Python bağımlılıkları
  ├── PROJE_PLANI.md           # Bu dosya
  ├── .env                      # Environment variables (GİZLİ)
  │
  ├── modules/                  # Modüler yapı - Her özellik ayrı
  │   ├── __init__.py
  │   ├── database.py           # Veritabanı işlemleri
  │   ├── text_message.py       # Metin mesaj modülü
  │   ├── voice_message.py      # Sesli mesaj modülü
  │   ├── image_upload.py       # Görüntü yükleme modülü
  │   ├── telegram_bot.py       # 🔥 Telegram bot işlemleri
  │   ├── telegram_webhook.py   # 🔥 Telegram webhook handler
  │   ├── otp_manager.py        # 🔥 OTP oluşturma/doğrulama
  │   └── security.py           # 🔥 Rate limit, CSRF, validasyon
  │
  ├── routes/                   # 🔥 API Routes - Organize yapı
  │   ├── __init__.py
  │   ├── chat.py               # Mesajlaşma API (SSE dahil)
  │   ├── admin.py              # Admin API (OTP, stats)
  │   └── files.py              # Dosya upload API
  │
  ├── static/                   # Statik dosyalar
  │   ├── css/
  │   │   └── style.css         # Ana stil dosyası (320px mobil)
  │   ├── js/
  │   │   ├── text.js           # Metin gönderme
  │   │   ├── voice.js          # Ses kayıt
  │   │   ├── image.js          # Görüntü yükleme
  │   │   └── sse.js            # 🔥 Real-time mesaj dinleme
  │   └── uploads/              # Yüklenen dosyalar
  │       ├── images/
  │       └── voices/
  │
  └── templates/                # HTML şablonları
      ├── index.html            # Müşteri sayfası
      └── admin.html            # Admin paneli
```

---

## 🔧 Modüler Yapı Avantajları

### Neden Modüler?
1. **Bağımsız Çalışma** - Bir modül bozulursa diğerleri çalışmaya devam eder
2. **Kolay Bakım** - Sorun olan modülü bul, düzelt
3. **Ölçeklenebilir** - Yeni özellik eklemek kolay
4. **Test Edilebilir** - Her modül ayrı test edilir
5. **Temiz Kod** - Her şey organize ve anlaşılır

### Modül Görevleri

#### database.py
- Veritabanı bağlantısı
- Tablo oluşturma (users, messages)
- CRUD işlemleri
- Kullanıcı silme (cascade)

#### text_message.py
- Metin mesajları veritabanına kaydet
- Metin mesajları getir

#### voice_message.py
- Ses dosyasını kaydet
- Format dönüşümü (webm → mp3) - opsiyonel
- Ses dosyasını getir

#### image_upload.py
- Resim yükle ve kaydet
- Resim boyutlandır/optimize et (Pillow)
- Resim getir

#### telegram_bot.py 🔥
- Telegram'a mesaj gönder (metin/ses/görüntü)
- Asenkron gönderim (threading)
- Retry mekanizması (3 deneme)
- Fallback (dosyaya kaydet)

#### telegram_webhook.py 🔥
- Telegram'dan gelen mesajları yakala
- Reply mesajlarını parse et
- User ID'yi bul
- Database'e admin mesajı olarak kaydet

#### otp_manager.py 🔥
- 6 haneli OTP oluştur (kriptografik güvenli)
- OTP doğrula (5 dk geçerli, 3 deneme)
- Session yönetimi (10 saat)

#### security.py 🔥
- Rate limiting (20 istek/dakika)
- CSRF token kontrolü
- Input validasyonu
- Hassas veri gizleme (loglarda)

---

## 📊 Veritabanı Yapısı

### users (Kullanıcılar)
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,              -- Unique user ID (localStorage'dan)
    name TEXT NOT NULL,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### messages (Mesajlar)
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,            -- users.id ile ilişkili
    sender_type TEXT NOT NULL,        -- customer/admin
    message_type TEXT NOT NULL,       -- text/voice/image
    content TEXT NOT NULL,            -- Metin veya dosya yolu
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### ⚠️ Önemli: Ticket Sistemi Yok!
- Kullanıcı bazlı mesajlaşma
- Her kullanıcının unique ID'si var (localStorage)
- Admin kullanıcıyı silince tüm mesajlar + dosyalar silinir

### otp_codes (OTP Kayıtları) - In-Memory
```python
# Veritabanında değil, bellekte tutulur
otp_codes = {
    'session_id': {
        'code': '123456',
        'expires': datetime + 5 minutes,
        'attempts': 0,
        'created_at': datetime
    }
}
```

### admin_sessions (Admin Oturumları) - In-Memory
```python
admin_sessions = {
    'session_id': {
        'authenticated': True,
        'timestamp': datetime,
        'expires': datetime + 10 hours
    }
}
```

---

## 🎨 Tasarım Prensipleri

- **Mobile First** - 320px'den başla
- **Minimal** - Sadece gerekli özellikler
- **Hızlı** - Hafif ve optimize
- **Kullanıcı Dostu** - Basit ve anlaşılır

---

## 🎨 Frontend Tasarım Referansı

### UI/UX Özellikleri (Referans Alınan)

#### 1. Renk Paleti
```css
/* Ana gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Müşteri mesaj balonu */
background: linear-gradient(135deg, #667eea, #764ba2);

/* Admin mesaj balonu */
background: white;
border: 1px solid #e5e7eb;
```

#### 2. Header Bileşenleri
- ✅ **Company Avatar** - Headset icon, gradient background
- ✅ **Company Name** - "Canlı Destek"
- ✅ **Online Status** - Yeşil nokta + pulse animasyon
- ✅ **Yanıt Süresi** - "~2 dk" bilgisi
- ❌ **Telefon Butonu** - Şimdilik kullanılmayacak

#### 3. Welcome Banner
```html
<div class="welcome-banner">
    <div class="welcome-icon">👋</div>
    <div class="welcome-title">Hoş Geldiniz!</div>
    <div class="welcome-text">Size nasıl yardımcı olabiliriz?</div>
</div>
```

#### 4. Mesaj Bileşenleri
- ✅ **Avatar Sistemi** - İlk harf gösterimi (müşteri), icon (admin)
- ✅ **Mesaj Baloncukları** - Sağ (müşteri), Sol (admin)
- ✅ **Zaman Damgası** - Her mesajın altında
- ✅ **Medya Önizleme** - Resim/Ses gösterimi
- ✅ **Animasyonlar** - slideIn, pulse, wave

#### 5. Input Area
- ✅ **Resim Butonu** - 📷 emoji
- ✅ **Ses Butonu** - 🎤 emoji (kayıt sırasında ⏹️)
- ✅ **Textarea** - Auto-resize (max 100px)
- ✅ **Gönder Butonu** - Gradient, disabled state

#### 6. Modal Sistemi
**İsim Alma Modal:**
```javascript
// İlk girişte göster
- İsim input (2-40 karakter)
- localStorage'da sakla
- İsteğe bağlı (boş bırakılabilir)
```

#### 7. Toast Bildirimleri
```javascript
showToast('Mesaj gönderildi', 'success'); // Yeşil
showToast('Hata oluştu', 'error');        // Kırmızı
```

#### 8. Animasyonlar
```css
@keyframes slideIn {     /* Mesaj gelişi */
@keyframes pulse {       /* Online status */
@keyframes wave {        /* Welcome icon */
@keyframes modalSlideIn { /* Modal açılış */
```

---

## 🔄 Frontend-Backend Entegrasyonu

### Değiştirilecek Kısımlar

#### 1. Mesaj Gönderme
**❌ Eski (Referans):**
```javascript
messages.push({...});  // LocalStorage'da array
renderMessages();
```

**✅ Yeni (Bizim Yapı):**
```javascript
// Backend'e POST
fetch(`/api/users/${userId}/messages`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({
        text: messageText,
        type: 'text'
    })
});
```

#### 2. Kullanıcı Silme (Admin)
```javascript
// Admin kullanıcıyı siler
fetch(`/api/admin/users/${userId}`, {
    method: 'DELETE',
    headers: {'X-Admin-Token': adminToken}
})
.then(() => {
    // 1. Database'den silinir (users + messages)
    // 2. Dosyalar silinir (images/ + voices/)
    // 3. SSE ile müşteriye bildirim
    // 4. Admin panelden kaldırılır
});
```

#### 3. Kullanıcı ID Yönetimi
```javascript
// localStorage'da sakla
let userId = localStorage.getItem('userId');

if (!userId) {
    // Yeni kullanıcı - unique ID oluştur
    userId = generateUserId(); // 12 karakter
    localStorage.setItem('userId', userId);
    
    // Backend'e kullanıcı oluştur
    fetch('/api/users', {
        method: 'POST',
        body: JSON.stringify({
            id: userId,
            name: customerName,
            email: customerEmail
        })
    });
}

// SSE bağlantısını başlat
startSSE(userIdketId}/messages`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({
        text: messageText,
        type: 'text'
    })
});
```

#### 2. Mesaj Alma (Real-time)
**❌ Eski (Referans):**
```javascript
// Sadece kendi mesajları göster
```

**✅ Yeni (Bizim Yapı):**
```javascript
// SSE ile admin mesajlarını dinle
const eventSource = new EventSource(`/api/tickets/${ticketId}/stream`);

eventSource.onmessage = (event) => {
    const message = JSON.parse(event.data);
    addMessageToUI(message);
};
```

#### 3. Resim Upload
**❌ Eski (Referans):**
```javascript
// Base64 olarak sakla
reader.readAsDataURL(file);
messages.push({ image: e.target.result });
```

**✅ Yeni (Bizim Yapı):**
```javascript
// FormData ile backend'e gönder
const formData = new FormData();
formData.append('file', file);
formData.append('ticket_id', ticketId);
formData.append('type', 'image');

fetch('/api/files/upload', {
    method: 'POST',
    body: formData
});
```

#### 4. Ses Kaydı
**❌ Eski (Referans):**
```javascript
// Blob URL olarak sakla
const audioUrl = URL.createObjectURL(audioBlob);
messages.push({ audio: audioUrl });
```

**✅ Yeni (Bizim Yapı):**
```javascript
// FormData ile backend'e gönder
const formData = new FormData();
formData.append('file', audioBlob, 'voice.webm');
formData.append('ticket_id', ticketId);
formData.append('type', 'voice');

fetch('/api/files/upload', {
    method: 'POST',
    body: formData
});
```

#### 5. Ticket Oluşturma
**✅ Yeni (Bizim Yapı):**
```javascript
// Sayfa yüklendiğinde
window.onload = async () => {
    // URL'den ticket_id al veya yeni oluştur
    const urlParams = new URLSearchParams(window.location.search);
    let ticketId = urlParams.get('ticket');
    
    if (!ticketId) {
        // Yeni ticket oluştur
        const response = await fetch('/api/tickets', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                customer_name: customerName,
                customer_email: customerEmail
            })
        });
        const data = await response.json();
        ticketId = data.ticket_id;
        
        // URL'i güncelle
        window.history.pushState({}, '', `?ticket=${ticketId}`);
    }
    
    // SSE bağlantısını başlat
    startSSE(ticketId);
};
```

---

## 📱 Index.html Yapısı

### HTML Bileşenleri
```html
<div class="container">
    <!-- Header -->
    <div class="header">
        <div class="company-avatar">🎧</div>
        <div class="company-info">
            <div class="company-name">Canlı Destek</div>
            <div class="company-status">
                <span class="status-dot"></span>
                Çevrimiçi - Yanıt süresi ~2 dk
            </div>
        </div>
    </div>
    
    <!-- Welcome Banner -->
    <div class="welcome-banner">
        <div class="welcome-icon">👋</div>
        <div class="welcome-title">Hoş Geldiniz!</div>
        <div class="welcome-text">Size nasıl yardımcı olabiliriz?</div>
    </div>
    
    <!-- Messages -->
    <div class="messages-container" id="messagesContainer"></div>
    
    <!-- Input Area -->
    <div class="input-area">
        <button id="imageBtn" class="media-btn">📷</button>
        <button id="audioBtn" class="media-btn">🎤</button>
        <textarea id="messageInput" class="message-input"></textarea>
        <button id="sendBtn" class="send-btn">Gönder</button>
    </div>
</div>

<!-- Name Modal -->
<div id="nameModal" class="modal">
    <div class="modal-card">
        <h3>👋 Selam! Hoş geldin</h3>
        <input id="nameInput" type="text" placeholder="Adınız...">
        <input id="emailInput" type="email" placeholder="Email (opsiyonel)">
        <button id="startBtn">Başla</button>
    </div>
</div>
```

### JavaScript Modülleri
```javascript
// Global değişkenler
let ticketId = null;
let customerName = 'Müşteri';
let customerEmail = null;
let eventSource = null;
let csrfToken = null;

// Ana fonksiyonlar
- init()                  // Sayfa yüklendiğinde
- createTicket()          // Yeni ticket oluştur
- startSSE()              // Real-time bağlantı
- sendMessage()           // Metin gönder
- uploadImage()           // Resim yükle
- recordAudio()           // Ses kaydet
- addMessageToUI()        // Mesajı ekrana bas
- showToast()             // Bildirim göster
```

---

## 🔄 Mesaj Akışı

### 1️⃣ Müşteri → Admin (Yeni Mesaj)
```
Müşteri mesaj yazar (index.html)
    ↓
POST /api/users/{user_id}/messages
    ↓
Database'e kaydet (sender=customer)
    ↓
Telegram'a bildirim gönder (threading)
    ↓
SSE ile admin panele push
    ↓
Admin anında görür ✅
```

### 2️⃣ Admin → Müşteri (Admin Panelden)
```
Admin cevap yazar (admin.html)
    ↓
POST /api/users/{user_id}/messages
    ↓
Database'e kaydet (sender=admin)
    ↓
SSE ile müşteri sayfasına push
    ↓
Müşteri anında görür ✅
```

### 3️⃣ Admin → Müşteri (Telegram'dan) 🔥
```
Telegram'da bildirim gelir
    ↓
Admin mesaja REPLY yapar
    ↓
Webhook: POST /api/telegram/webhook
    ↓
Reply'den user_id parse et
    ↓
Database'e kaydet (sender=admin)
    ↓
SSE ile müşteri sayfasına push
    ↓
Müşteri anında görür ✅
```

### 4️⃣ Admin Kullanıcıyı Siler 🗑️
```
Admin "Sil" butonuna basar
    ↓
Onay ister ("Emin misiniz?")
    ↓
DELETE /api/admin/users/{user_id}
    ↓
Backend:
  1. Kullanıcıya ait dosyaları bul
  2. Dosyaları diskten sil (images/, voices/)
  3. messages tablosundan sil (CASCADE)
  4. users tablosundan sil
  5. SSE ile müşteriye bildir
    ↓
Müşteri (Index):
  - "Sohbet sonlandırıldı" mesajı
  - Mesajlar temizlenir
  - localStorage temizlenir
  - Yeni sohbet başlatabilir
    ↓
Admin Panel:
  - Kullanıcı listeden kaldırılır
  - İstatistikler güncellenir
```

---

## 🔐 Admin Giriş Akışı

```
Admin paneli aç
    ↓
"Şifre İste" butonuna bas
    ↓
POST /api/admin/request-otp
    ↓
OTP oluştur (6 haneli, 5 dk geçerli)
    ↓
Telegram'a gönder (threading)
    ↓
Admin Telegram'dan kodu okur
    ↓
Kodu girer
    ↓
POST /api/admin/verify-otp
    ↓
OTP doğrula (3 deneme hakkı)
    ↓
Session oluştur (10 saat geçerli)
    ↓
Admin panele giriş ✅
```

---

## 🔒 Güvenlik Katmanları

### 1. Rate Limiting
```python
# In-memory rate limit
- 20 istek/dakika
- 2 istek/saniye
- IP bazlı takip
```

### 2. CSRF Koruması
```python
# Flask-WTF
- Her form'da token
- POST isteklerinde zorunlu
```

### 3. OTP Güvenliği
```python
- Kriptografik rastgele (secrets modülü)
- 5 dakika geçerli
- 3 yanlış deneme hakkı
- Session 10 saat
```

### 4. Input Validasyonu
```python
- Email format kontrolü
- Dosya boyutu limiti (5MB resim, 10MB ses)
- Dosya tipi kontrolü
- XSS önleme
```

### 5. Telegram Güvenliği
```python
- Bot token .env'de
- Webhook secret key
- Retry + fallback mekanizması
```

---

## 📝 Sonraki Adımlar

### Aşama 1: Temel Yapı ✅
- [x] Proje planı oluştur
- [ ] Dosya yapısını kur
- [ ] .env dosyası oluştur
- [ ] requirements.txt oluştur

### Aşama 2: Backend Core
- [ ] config.py - Ayarlar
- [ ] modules/database.py - DB işlemleri
- [ ] modules/security.py - Güvenlik
- [ ] app.py - Ana Flask app

### Aşama 3: Telegram Entegrasyonu
- [ ] modules/telegram_bot.py - Bot işlemleri
- [ ] modules/telegram_webhook.py - Webhook
- [ ] modules/otp_manager.py - OTP sistemi
- [ ] Telegram bot oluştur (BotFather)
- [ ] Webhook kur

### Aşama 4: API Routes
- [ ] routes/chat.py - Mesajlaşma + SSE
- [ ] routes/admin.py - Admin işlemleri
- [ ] routes/files.py - Dosya upload

### Aşama 5: Medya Modülleri
- [ ] modules/text_message.py
- [ ] modules/voice_message.py
- [ ] modules/image_upload.py

### Aşama 6: Frontend (Index.html)
- [ ] templates/index.html - Referans tasarımı adapte et
- [ ] static/css/style.css - Gradient tema, animasyonlar
- [ ] static/js/app.js - Ana JavaScript
  - [ ] Ticket oluşturma
  - [ ] SSE bağlantısı
  - [ ] Mesaj gönderme (text/image/voice)
  - [ ] Toast bildirimleri
  - [ ] Modal sistemi

### Aşama 7: Frontend (Admin.html)
- [ ] templates/admin.html - Admin paneli
- [ ] static/js/admin.js - Admin JavaScript
  - [ ] OTP giriş
  - [ ] Ticket listesi
  - [ ] SSE bağlantısı
  - [ ] Cevap gönderme

### Aşama 8: Test & Deploy
- [ ] Local test
- [ ] Telegram test
- [ ] Webhook test
- [ ] Hata düzelt
- [ ] Deploy (Railway/Heroku)ad

### Aşama 5: Medya Modülleri
- [ ] modules/text_message.py
- [ ] modules/voice_message.py
- [ ] modules/image_upload.py

### Aşama 6: Frontend
- [ ] templates/index.html - Müşteri sayfası
- [ ] templates/admin.html - Admin paneli
- [ ] static/css/style.css - Mobil responsive
- [ ] static/js/sse.js - Real-time
- [ ] static/js/text.js - Metin gönderme
- [ ] static/js/voice.js - Ses kayıt
- [ ] static/js/image.js - Görüntü upload

### Aşama 7: Test & Deploy
- [ ] Local test
- [ ] Telegram test
- [ ] Webhook test
- [ ] Hata düzelt
- [ ] Deploy (Railway/Heroku)

---

## 💡 Önemli Notlar

### Teknoloji Kararları
- ✅ **SQLite** kullanılacak (PostgreSQL değil) - Basit ve yeterli
- ✅ **Threading** kullanılacak (Celery değil) - Daha basit kurulum
- ✅ **In-memory rate limit** (Redis değil) - Gereksiz bağımlılık yok
- ✅ **Flask session** (JWT değil) - Basit ve güvenli
- ❌ **E2E encryption yok** - HTTPS yeterli

### Medya İşleme
- Ses kaydı: Tarayıcı MediaRecorder API (webm/ogg formatı)
- Resim: Pillow ile resize/optimize (max 5MB)
- Ses: pydub ile format dönüşümü (opsiyonel)

### Telegram
- Bot token ve chat ID .env dosyasında
- Webhook Railway/Heroku deploy sonrası kurulacak
- Local test için polling kullanılabilir

### Güvenlik
- Admin tek kişi (sen)
- OTP ile giriş (5 dk geçerli)
- Session 10 saat
- Rate limiting aktif
- CSRF koruması aktif

### Performans
- SSE ile real-time mesajlaşma
- Threading ile asenkron Telegram gönderimi
- Otomatik temizlik (eski OTP'ler, sessionlar)

### Frontend Referans
- **Tasarım:** Modern gradient tema (mor-mavi)
- **Animasyonlar:** slideIn, pulse, wave
- **Responsive:** 320px mobil destekli
- **UX:** Toast bildirimleri, modal sistemi
- **Medya:** Resim önizleme, ses oynatıcı

---

## 🎯 Proje Hedefleri

✅ **Basit** - Gereksiz karmaşıklık yok  
✅ **Hızlı** - Real-time mesajlaşma  
✅ **Güvenli** - OTP + Rate limit + CSRF  
✅ **Mobil** - 320px responsive  
✅ **Pratik** - Telegram'dan cevap verebilme  
✅ **Modern** - Gradient tema, animasyonlar  

---

## 📚 API Endpoints (Özet)

### Kullanıcı İşlemleri
```
POST   /api/users                # Yeni kullanıcı oluştur
GET    /api/users/{id}           # Kullanıcı detayı
GET    /api/users/{id}/stream    # SSE stream
DELETE /api/admin/users/{id}     # Kullanıcı sil (admin)
```

### Mesaj İşlemleri
```
POST   /api/users/{id}/messages  # Mesaj gönder
GET    /api/users/{id}/messages  # Mesajları getir
```

### Dosya İşlemleri
```
POST   /api/files/upload          # Resim/Ses yükle
GET    /api/files/{filename}      # Dosya indir
```

### Admin İşlemleri
```
POST   /api/admin/request-otp     # OTP iste
POST   /api/admin/verify-otp      # OTP doğrula
GET    /api/admin/users           # Tüm kullanıcılar
DELETE /api/admin/users/{id}      # Kullanıcı sil
GET    /api/admin/stats           # İstatistikler
```

### Telegram Webhook
```
POST   /api/telegram/webhook      # Telegram mesajları
POST   /api/telegram/set-webhook  # Webhook kur
```

---

---

## 🚀 Railway Deployment

### Gerekli Dosyalar

#### Procfile
```
web: gunicorn app:app
```

#### runtime.txt
```
python-3.11.0
```

#### .gitignore
```
.env
database.db
__pycache__/
*.pyc
*.pyo
*.log
static/uploads/*
!static/uploads/.gitkeep
```

#### .env.example
```bash
# Telegram
TELEGRAM_BOT_TOKEN=8033290671:AAHHqhVnDdbIiou4FsO0ACdq7-EdsgW0of8
TELEGRAM_ADMIN_CHAT_ID=5874850928

# Flask
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
PORT=5000

# Admin
ADMIN_OTP_VALIDITY_MINUTES=5
ADMIN_SESSION_HOURS=10

# File Upload
MAX_IMAGE_SIZE_MB=5
MAX_VOICE_SIZE_MB=10
```

### Railway Environment Variables
```
TELEGRAM_BOT_TOKEN=8033290671:AAHHqhVnDdbIiou4FsO0ACdq7-EdsgW0of8
TELEGRAM_ADMIN_CHAT_ID=5874850928
SECRET_KEY=<generate-random-key>
FLASK_ENV=production
```

### Webhook Kurulumu
Deploy sonrası:
```bash
curl -X POST https://adminsohbet.up.railway.app/api/telegram/set-webhook
```

### Deploy Adımları
1. GitHub'a push
2. Railway'de proje oluştur
3. GitHub repo bağla
4. Environment variables ekle
5. Deploy
6. Webhook kur

---

---

## 🗑️ Kullanıcı Silme Sistemi

### Özellikler:
1. ✅ **Cascade Delete** - Kullanıcı silinince tüm mesajlar silinir
2. ✅ **Dosya Temizliği** - İlgili resim/ses dosyaları silinir
3. ✅ **Real-time Bildirim** - Müşteri anında haberdar olur
4. ✅ **Toplu Silme** - Seçili kullanıcıları toplu sil
5. ✅ **Onay Mekanizması** - Yanlışlıkla silmeyi önler

### Backend (routes/admin.py):
```python
@admin_bp.route('/users/<user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    # 1. Dosyaları sil
    messages = get_user_messages(user_id)
    for msg in messages:
        if msg['message_type'] in ['image', 'voice']:
            if os.path.exists(msg['content']):
                os.remove(msg['content'])
    
    # 2. Database'den sil (CASCADE ile mesajlar da silinir)
    db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    
    # 3. SSE ile bildir
    notify_user_deleted(user_id)
    
    return {'success': True}
```

---

**Son Güncelleme:** 2025-01-22  
**Versiyon:** 2.4 (Ticket sistemi kaldırıldı, kullanıcı bazlı yapı)  
**Production:** https://adminsohbet.up.railway.app/


## 🛡️ Admin.html Tasarım Referansı

### Admin UI/UX Özellikleri

#### 1. Admin Header
- **Admin Avatar** - 🛡️ emoji, gradient background
- **Admin Info** - "Admin Panel", "Sohbet Yönetimi"
- **Çıkış Butonu** - 🚪 emoji, kırmızı renk

#### 2. İstatistik Kartları (Stats Grid)
```html
<!-- 3 Kolon Grid -->
<div class="stats-grid">
    <!-- Toplam Mesaj -->
    <div class="stat-card">
        <div class="stat-icon blue">💬</div>
        <div class="stat-value">0</div>
        <div class="stat-label">Mesaj</div>
    </div>
    
    <!-- Aktif Kullanıcılar -->
    <div class="stat-card">
        <div class="stat-icon green">👥</div>
        <div class="stat-value">0</div>
        <div class="stat-label">Aktif</div>
    </div>
    
    <!-- Okunmamış -->
    <div class="stat-card">
        <div class="stat-icon purple">🕒</div>
        <div class="stat-value">0</div>
        <div class="stat-label">Okunmamış</div>
    </div>
</div>
```

#### 3. Arama ve Filtreleme
- **Arama Kutusu** - 🔎 emoji, real-time arama
- **Filtre Butonu** - ⚙️ emoji, "Tüm Kullanıcılar" / "Sadece Aktif"

#### 4. Toplu İşlemler (Action Bar)
- **Tümünü Seç** - ☑️ emoji, toggle seçim
- **Sil Butonu** - 🗑️ emoji, kırmızı, disabled state

#### 5. Ticket Kartları (User Cards)
```html
<div class="user-card unread">
    <input type="checkbox" class="user-checkbox">
    
    <div class="user-avatar-wrapper">
        <div class="user-avatar">A</div>
        <div class="online-badge"></div>
    </div>
    
    <div class="user-info">
        <div class="user-name">Ahmet</div>
        <div class="unread-badge">3</div>
        <div class="user-message">Son mesaj...</div>
    </div>
    
    <div class="user-meta">
        <div class="user-time">5dk</div>
        <div class="user-status online">Aktif</div>
    </div>
</div>
```

#### 6. Chat View
- **Back Button** - ⬅️ emoji, mor gradient
- **Chat Header** - Avatar + İsim + Status
- **Messages Container** - Scrollable
- **Input Area** - Index ile aynı

#### 7. OTP Login Modal
```html
<div class="login-modal">
    <div class="login-card">
        <h2>🔐 Admin Girişi</h2>
        <input type="password" placeholder="OTP Kodu">
        <button class="login-btn">Giriş Yap</button>
        <button class="otp-btn">📱 OTP Gönder</button>
    </div>
</div>
```

---

## 🔄 Admin Frontend-Backend Entegrasyonu

### 1. OTP Giriş
```javascript
// OTP İste
fetch('/api/admin/request-otp', {
    method: 'POST'
}).then(res => res.json())
  .then(data => showToast('OTP Telegram\'a gönderildi', 'success'));

// OTP Doğrula
fetch('/api/admin/verify-otp', {
    method: 'POST',
    body: JSON.stringify({ otp: otpCode })
}).then(res => res.json())
  .then(data => {
      localStorage.setItem('adminToken', data.token);
      initAdmin();
  });
```

### 2. Ticket Listesi
```javascript
// Ticketları yükle
fetch('/api/admin/tickets', {
    headers: {'X-Admin-Token': adminToken}
}).then(res => res.json())
  .then(tickets => renderTicketList(tickets));

// Her ticket için SSE
tickets.forEach(ticket => {
    const es = new EventSource(`/api/tickets/${ticket.id}/stream`);
    es.onmessage = (e) => updateTicketUI(ticket.id, JSON.parse(e.data));
});
```

### 3. Admin Mesaj Gönderme
```javascript
// Metin
fetch(`/api/tickets/${ticketId}/messages`, {
    method: 'POST',
    headers: {'X-Admin-Token': adminToken},
    body: JSON.stringify({ text, sender: 'admin', type: 'text' })
});

// Resim/Ses
const formData = new FormData();
formData.append('file', file);
formData.append('ticket_id', ticketId);
formData.append('sender', 'admin');

fetch('/api/files/upload', {
    method: 'POST',
    headers: {'X-Admin-Token': adminToken},
    body: formData
});
```

### 4. İstatistikler
```javascript
fetch('/api/admin/stats', {
    headers: {'X-Admin-Token': adminToken}
}).then(res => res.json())
  .then(stats => {
      document.getElementById('totalMessages').textContent = stats.total_messages;
      document.getElementById('onlineUsers').textContent = stats.online_users;
      document.getElementById('unreadCount').textContent = stats.unread_count;
  });
```

### 5. Ticket Silme
```javascript
Promise.all(
    selectedTickets.map(id => 
        fetch(`/api/admin/tickets/${id}`, {
            method: 'DELETE',
            headers: {'X-Admin-Token': adminToken}
        })
    )
).then(() => {
    showToast('Seçili ticketlar silindi', 'success');
    loadTickets();
});
```

---

## 🎨 Ortak Tasarım Özellikleri

### Renk Paleti (Index + Admin)
```css
/* Primary Gradient */
--gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Stat Colors */
--blue: #2563eb;
--blue-light: #dbeafe;
--green: #059669;
--green-light: #d1fae5;
--purple: #9333ea;
--purple-light: #e9d5ff;

/* Neutral */
--gray-50: #f9fafb;
--gray-200: #e5e7eb;
--gray-300: #d1d5db;
--gray-400: #9ca3af;
--gray-500: #6b7280;
--gray-700: #374151;
--gray-800: #1f2937;
```

### Avatar Renk Sistemi
```javascript
const avatarColors = [
    '#667eea', '#f093fb', '#4facfe', '#43e97b',
    '#fa709a', '#ff6b6b', '#4ecdc4', '#45b7d1'
];

function getAvatarColor(id) {
    const hash = id.split('').reduce((a, b) => {
        a = ((a << 5) - a) + b.charCodeAt(0);
        return a & a;
    }, 0);
    return avatarColors[Math.abs(hash) % avatarColors.length];}
```

### Time Ago Formatter
```javascript
function getTimeAgo(date) {
    const diff = new Date() - date;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'Şimdi';
    if (minutes < 60) return minutes + 'dk';
    if (hours < 24) return hours + 'sa';
    return days + 'g';
}
```

---

## 📱 Admin.html Yapısı

### Ana Bileşenler

#### 1. List View (Ticket Listesi)
- Header (Avatar, İstatistikler)
- Arama ve Filtreleme
- Toplu İşlem Butonları
- Ticket Kartları (Scrollable)

#### 2. Chat View (Mesajlaşma)
- Chat Header (Geri, Avatar, İsim, Status)
- Messages Container (Scrollable)
- Input Area (Metin/Resim/Ses)

#### 3. Login Modal
- OTP İsteme
- OTP Doğrulama
- Session Yönetimi

### JavaScript Modülleri
```javascript
// Global değişkenler
let adminToken = null;
let tickets = [];
let currentTicket = null;
let selectedTickets = new Set();
let filterOnline = false;
let searchTerm = '';

// Ana fonksiyonlar
- checkAdminAuth()        // Token kontrolü
- showLoginModal()        // OTP modal
- sendOTP()               // OTP iste
- attemptLogin()          // OTP doğrula
- initAdmin()             // Admin başlat
- loadTickets()           // Ticketları yükle
- renderTicketList()      // Liste render
- openChat()              // Chat aç
- sendMessage()           // Mesaj gönder
- updateStats()           // İstatistik güncelle
- selectAll()             // Tümünü seç
- deleteSelected()        // Seçilenleri sil
- logout()                // Çıkış
```

---

## 🎯 Kullanılacak Özellikler

### ✅ ALINACAKLAR (Admin)
1. **OTP Login** - Telegram ile giriş
2. **İstatistik Kartları** - 3 kolon grid
3. **Arama** - Real-time filtreleme
4. **Filtre** - Aktif/Tüm kullanıcılar
5. **Toplu İşlem** - Checkbox + Sil
6. **Avatar Renk** - Hash bazlı
7. **Online Badge** - Yeşil nokta
8. **Unread Badge** - Okunmamış sayısı
9. **Time Ago** - "5dk", "2sa", "3g"
10. **Toast** - Success/Error
11. **Responsive** - 320px mobil
12. **Empty State** - "Kullanıcı bulunamadı"

### ❌ DEĞİŞTİRİLECEKLER
1. **Socket.io → SSE** - Real-time
2. **In-memory → Database** - Ticket saklama
3. **Telefon Butonu** - Kaldırılacak

---

**Versiyon:** 2.2 (Admin referans + Ortak tasarım eklendi)
