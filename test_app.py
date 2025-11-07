# -*- coding: utf-8 -*-
"""
Basit Test Script - Uygulamanin calisip calismadigini kontrol et
"""

import sys
import os

def test_imports():
    """Tum modullerin import edilip edilmedigini test et"""
    print("Testing imports...")
    
    try:
        from flask import Flask
        print("OK Flask")
        
        from config import Config
        print("OK Config")
        
        from modules.database import init_db
        print("OK Database")
        
        from modules.telegram_bot import TelegramBot
        print("OK Telegram Bot")
        
        from routes.chat import chat_bp
        print("OK Chat Routes")
        
        from routes.admin import admin_bp
        print("OK Admin Routes")
        
        from routes.files import files_bp
        print("OK Files Routes")
        
        from routes.telegram import telegram_bp
        print("OK Telegram Routes")
        
        print("\nAll imports successful!")
        return True
        
    except Exception as e:
        print(f"\nImport error: {e}")
        return False

def test_config():
    """Config dosyasini test et"""
    print("\nTesting config...")
    
    try:
        from config import Config
        
        assert hasattr(Config, 'SECRET_KEY'), "SECRET_KEY missing"
        assert hasattr(Config, 'DATABASE_PATH'), "DATABASE_PATH missing"
        assert hasattr(Config, 'IMAGE_UPLOAD_FOLDER'), "IMAGE_UPLOAD_FOLDER missing"
        assert hasattr(Config, 'VOICE_UPLOAD_FOLDER'), "VOICE_UPLOAD_FOLDER missing"
        
        print("OK Config")
        return True
        
    except Exception as e:
        print(f"Config error: {e}")
        return False

def test_folders():
    """Gerekli klasorlerin varligini test et"""
    print("\nTesting folders...")
    
    folders = [
        'modules',
        'routes',
        'static',
        'static/css',
        'static/js',
        'static/uploads',
        'static/uploads/images',
        'static/uploads/voices',
        'templates'
    ]
    
    all_ok = True
    for folder in folders:
        if os.path.exists(folder):
            print(f"OK {folder}")
        else:
            print(f"FAIL {folder} - NOT FOUND")
            all_ok = False
    
    return all_ok

def test_files():
    """Gerekli dosyalarin varligini test et"""
    print("\nTesting files...")
    
    files = [
        'app.py',
        'config.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        '.env.example',
        'templates/index.html',
        'templates/admin.html',
        'static/css/style.css',
        'static/css/admin.css',
        'static/js/app.js',
        'static/js/admin.js'
    ]
    
    all_ok = True
    for file in files:
        if os.path.exists(file):
            print(f"OK {file}")
        else:
            print(f"FAIL {file} - NOT FOUND")
            all_ok = False
    
    return all_ok

if __name__ == '__main__':
    print("=" * 50)
    print("MUSTERI DESTEK SISTEMI - TEST")
    print("=" * 50)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Config", test_config()))
    results.append(("Folders", test_folders()))
    results.append(("Files", test_files()))
    
    print("\n" + "=" * 50)
    print("TEST SONUCLARI")
    print("=" * 50)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(r[1] for r in results)
    
    if all_passed:
        print("\nTum testler basarili! Uygulama calistir ilabilir.")
        print("\nCalistirmak icin:")
        print("  python app.py")
        sys.exit(0)
    else:
        print("\nBazi testler basarisiz! Lutfen hatalari duzeltin.")
        sys.exit(1)
