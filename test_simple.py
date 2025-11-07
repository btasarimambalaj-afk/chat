# -*- coding: utf-8 -*-
"""
Simple Test - Telegram Mesaj Gonderme Testi
"""

def test_telegram_message():
    """Telegram mesaj gonderme testi"""
    print("=" * 60)
    print("TELEGRAM MESAJ GONDERME TESTI")
    print("=" * 60)
    
    try:
        from modules.telegram_bot import TelegramBot
        from config import Config
        
        print("\n1. Config kontrol ediliyor...")
        
        if not Config.TELEGRAM_BOT_TOKEN:
            print("HATA: TELEGRAM_BOT_TOKEN bulunamadi!")
            print("Lutfen .env dosyasini kontrol edin.")
            return False
        
        if not Config.TELEGRAM_ADMIN_CHAT_ID:
            print("HATA: TELEGRAM_ADMIN_CHAT_ID bulunamadi!")
            print("Lutfen .env dosyasini kontrol edin.")
            return False
        
        print(f"OK Token: {Config.TELEGRAM_BOT_TOKEN[:20]}...")
        print(f"OK Chat ID: {Config.TELEGRAM_ADMIN_CHAT_ID}")
        
        print("\n2. Telegram bot olusturuluyor...")
        bot = TelegramBot(Config.TELEGRAM_BOT_TOKEN, Config.TELEGRAM_ADMIN_CHAT_ID)
        print("OK Bot olusturuldu")
        
        print("\n3. Test mesaji gonderiliyor...")
        result = bot.send_message(
            "<b>TEST MESAJI</b>\n\n"
            "Bu bir test mesajidir.\n"
            "Sistem calisma testi yapiliyor.\n\n"
            "Eger bu mesaji goruyorsaniz, Telegram entegrasyonu calisiyor!"
        )
        
        if result['success']:
            print("OK Mesaj basariyla gonderildi!")
            print("\nTelegram'i kontrol edin!")
            return True
        else:
            print(f"HATA: Mesaj gonderilemedi")
            print(f"Hata: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"\nHATA: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_telegram_notifications():
    """Telegram bildirim testleri"""
    print("\n" + "=" * 60)
    print("TELEGRAM BILDIRIM TESTLERI")
    print("=" * 60)
    
    try:
        from modules.telegram_bot import TelegramBot
        from config import Config
        
        bot = TelegramBot(Config.TELEGRAM_BOT_TOKEN, Config.TELEGRAM_ADMIN_CHAT_ID)
        
        # Test 1: Yeni kullanici bildirimi
        print("\n1. Yeni kullanici bildirimi...")
        bot.notify_new_user("test_user_123", "Test Kullanici")
        print("OK Bildirim gonderildi")
        
        import time
        time.sleep(2)
        
        # Test 2: Yeni mesaj bildirimi
        print("\n2. Yeni mesaj bildirimi...")
        bot.notify_new_message(
            "test_user_123",
            "Test Kullanici",
            "text",
            "Merhaba, bu bir test mesajidir!"
        )
        print("OK Bildirim gonderildi")
        
        time.sleep(2)
        
        # Test 3: Admin yanit bildirimi
        print("\n3. Admin yanit bildirimi...")
        bot.send_admin_reply(
            "test_user_123",
            "Test Kullanici",
            "text",
            "Test yaniti"
        )
        print("OK Bildirim gonderildi")
        
        print("\nTelegram'i kontrol edin! 3 bildirim gelmeli.")
        return True
        
    except Exception as e:
        print(f"\nHATA: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_otp_send():
    """OTP gonderme testi"""
    print("\n" + "=" * 60)
    print("OTP GONDERME TESTI")
    print("=" * 60)
    
    try:
        from modules.telegram_bot import TelegramBot
        from modules.otp_manager import OTPManager
        from config import Config
        
        bot = TelegramBot(Config.TELEGRAM_BOT_TOKEN, Config.TELEGRAM_ADMIN_CHAT_ID)
        otp_manager = OTPManager()
        
        print("\n1. OTP olusturuluyor...")
        otp_code = otp_manager.generate_otp("test_session")
        print(f"OK OTP: {otp_code}")
        
        print("\n2. OTP Telegram'a gonderiliyor...")
        result = bot.send_message(
            f"<b>Admin OTP</b>\n\n"
            f"Kod: <code>{otp_code}</code>\n\n"
            f"5 dakika gecerli"
        )
        
        if result['success']:
            print("OK OTP gonderildi!")
            print("\nTelegram'i kontrol edin!")
            return True
        else:
            print(f"HATA: OTP gonderilemedi")
            return False
            
    except Exception as e:
        print(f"\nHATA: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("\n")
    
    results = []
    
    # Test 1: Basit mesaj
    results.append(("Telegram Mesaj", test_telegram_message()))
    
    input("\nDevam etmek icin Enter'a basin...")
    
    # Test 2: Bildirimler
    results.append(("Telegram Bildirimler", test_telegram_notifications()))
    
    input("\nDevam etmek icin Enter'a basin...")
    
    # Test 3: OTP
    results.append(("OTP Gonderme", test_otp_send()))
    
    # Sonuclar
    print("\n" + "=" * 60)
    print("TEST SONUCLARI")
    print("=" * 60)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(r[1] for r in results)
    
    if all_passed:
        print("\nTum testler basarili!")
    else:
        print("\nBazi testler basarisiz!")
