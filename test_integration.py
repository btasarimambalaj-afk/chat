# -*- coding: utf-8 -*-
"""
Integration Test - Mesaj ve Telegram Gonderme Testi
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_user_registration():
    """Test 1: Kullanici kaydi"""
    print("\n=== TEST 1: Kullanici Kaydi ===")
    
    data = {
        "user_id": "test_user_123",
        "name": "Test Kullanici"
    }
    
    response = requests.post(f"{BASE_URL}/api/users", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 200

def test_send_text_message():
    """Test 2: Metin mesaj gonderme"""
    print("\n=== TEST 2: Metin Mesaj Gonderme ===")
    
    data = {
        "user_id": "test_user_123",
        "sender_type": "customer",
        "message_type": "text",
        "content": "Merhaba, bu bir test mesajidir!"
    }
    
    response = requests.post(f"{BASE_URL}/api/messages", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 200

def test_get_messages():
    """Test 3: Mesajlari getirme"""
    print("\n=== TEST 3: Mesajlari Getirme ===")
    
    response = requests.get(f"{BASE_URL}/api/users/test_user_123/messages")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Mesaj sayisi: {len(data.get('messages', []))}")
        return True
    
    return False

def test_admin_otp_request():
    """Test 4: Admin OTP isteme"""
    print("\n=== TEST 4: Admin OTP Isteme ===")
    
    session = requests.Session()
    response = session.post(f"{BASE_URL}/api/admin/request-otp")
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data}")
        
        if 'otp' in data:
            print(f"\nOTP Kodu: {data['otp']}")
            print("Bu kod Telegram'a gonderilmeli!")
            return True, data['otp'], session
    
    return False, None, None

def test_admin_otp_verify(otp, session):
    """Test 5: Admin OTP dogrulama"""
    print("\n=== TEST 5: Admin OTP Dogrulama ===")
    
    data = {"otp": otp}
    response = session.post(f"{BASE_URL}/api/admin/verify-otp", json=data)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 200

def test_admin_users_list(session):
    """Test 6: Admin kullanici listesi"""
    print("\n=== TEST 6: Admin Kullanici Listesi ===")
    
    response = session.get(f"{BASE_URL}/api/admin/users")
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        users = data.get('users', [])
        print(f"Kullanici sayisi: {len(users)}")
        
        for user in users:
            print(f"- {user['name']} (ID: {user['id']}, Mesaj: {user['message_count']})")
        
        return True
    
    return False

def test_admin_stats(session):
    """Test 7: Admin istatistikler"""
    print("\n=== TEST 7: Admin Istatistikler ===")
    
    response = session.get(f"{BASE_URL}/api/admin/stats")
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        stats = data.get('stats', {})
        print(f"Toplam mesaj: {stats.get('total_messages', 0)}")
        print(f"Toplam kullanici: {stats.get('total_users', 0)}")
        print(f"Aktif baglanti: {stats.get('active_connections', 0)}")
        
        return True
    
    return False

def test_telegram_bot():
    """Test 8: Telegram bot testi"""
    print("\n=== TEST 8: Telegram Bot Testi ===")
    
    try:
        from modules.telegram_bot import TelegramBot
        from config import Config
        
        if not Config.TELEGRAM_BOT_TOKEN or not Config.TELEGRAM_ADMIN_CHAT_ID:
            print("UYARI: Telegram credentials bulunamadi!")
            print("Telegram testleri atlanacak.")
            return False
        
        bot = TelegramBot(Config.TELEGRAM_BOT_TOKEN, Config.TELEGRAM_ADMIN_CHAT_ID)
        
        # Test mesaji gonder
        result = bot.send_message("TEST: Sistem calisma testi\n\nBu bir test mesajidir.")
        
        if result['success']:
            print("Telegram mesaji basariyla gonderildi!")
            return True
        else:
            print(f"Telegram mesaji gonderilemedi: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"Telegram test hatasi: {e}")
        return False

def run_all_tests():
    """Tum testleri calistir"""
    print("=" * 60)
    print("INTEGRATION TEST - Mesaj & Telegram")
    print("=" * 60)
    print("\nONEMLI: Flask uygulamasi calisiyor olmali!")
    print("Baska bir terminalde: python app.py")
    print("\nDevam etmek icin Enter'a basin...")
    input()
    
    results = []
    
    # Test 1-3: Temel mesajlasma
    results.append(("Kullanici Kaydi", test_user_registration()))
    time.sleep(0.5)
    
    results.append(("Metin Mesaj Gonderme", test_send_text_message()))
    time.sleep(0.5)
    
    results.append(("Mesajlari Getirme", test_get_messages()))
    time.sleep(0.5)
    
    # Test 4-7: Admin islemleri
    success, otp, session = test_admin_otp_request()
    results.append(("Admin OTP Isteme", success))
    
    if success and otp:
        time.sleep(0.5)
        results.append(("Admin OTP Dogrulama", test_admin_otp_verify(otp, session)))
        time.sleep(0.5)
        results.append(("Admin Kullanici Listesi", test_admin_users_list(session)))
        time.sleep(0.5)
        results.append(("Admin Istatistikler", test_admin_stats(session)))
    else:
        results.append(("Admin OTP Dogrulama", False))
        results.append(("Admin Kullanici Listesi", False))
        results.append(("Admin Istatistikler", False))
    
    # Test 8: Telegram
    time.sleep(0.5)
    results.append(("Telegram Bot", test_telegram_bot()))
    
    # Sonuclar
    print("\n" + "=" * 60)
    print("TEST SONUCLARI")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "OK" if result else "XX"
        print(f"{symbol} {name}: {status}")
        
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Toplam: {len(results)} | Basarili: {passed} | Basarisiz: {failed}")
    print("=" * 60)
    
    if failed == 0:
        print("\nTum testler basarili!")
    else:
        print(f"\n{failed} test basarisiz!")
    
    return failed == 0

if __name__ == '__main__':
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest iptal edildi.")
        exit(1)
    except Exception as e:
        print(f"\n\nTest hatasi: {e}")
        exit(1)
