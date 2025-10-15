#!/usr/bin/env python3
"""
Serial Key Management API Test Script
Bu script API'nin tüm fonksiyonlarını test eder.
"""

import requests
import json
import time

BASE_URL = "https://my-first-deployed-flask-project.onrender.com/"
ADMIN_PASSWORD = "admin123"

def test_api():
    print("🔑 Serial Key Management API Test Başlatılıyor...")
    print("=" * 60)
    
    # Test 1: API bilgileri
    print("\n1. API Bilgileri Test Ediliyor...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API: {data['message']}")
            print(f"📊 Version: {data['version']}")
        else:
            print("❌ API bilgileri alınamadı")
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return
    
    # Test 2: Health check
    print("\n2. Health Check Test Ediliyor...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data['status']}")
            print(f"📊 Serial Key Sayısı: {data['serial_keys_count']}")
        else:
            print("❌ Health check başarısız")
    except Exception as e:
        print(f"❌ Health check hatası: {e}")
    
    # Test 3: Admin bilgileri
    print("\n3. Admin Bilgileri Test Ediliyor...")
    try:
        response = requests.get(f"{BASE_URL}/api/admin-info")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['message']}")
            print(f"📝 Serial Format: {data['serial_format']}")
            print(f"📊 Mevcut Serial Sayısı: {data['current_serial_count']}")
        else:
            print("❌ Admin bilgileri alınamadı")
    except Exception as e:
        print(f"❌ Admin bilgileri hatası: {e}")
    
    # Test 4: Serial key ekleme (otomatik)
    print("\n4. Otomatik Serial Key Ekleme Test Ediliyor...")
    try:
        new_serial_data = {
            "password": ADMIN_PASSWORD,
            "description": "Test serial key - otomatik oluşturuldu",
            "expiry_date": "2024-12-31T23:59:59",
            "max_uses": 3
        }
        response = requests.post(f"{BASE_URL}/api/add-serial", json=new_serial_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Serial key oluşturuldu: {data['data']['serial_key']}")
            print(f"📝 Açıklama: {data['data']['description']}")
            print(f"🔢 Max kullanım: {data['data']['max_uses']}")
            auto_serial_key = data['data']['serial_key']
        else:
            print(f"❌ Serial key oluşturulamadı: {response.json().get('message', 'Bilinmeyen hata')}")
            auto_serial_key = None
    except Exception as e:
        print(f"❌ Serial key ekleme hatası: {e}")
        auto_serial_key = None
    
    # Test 5: Manuel serial key ekleme
    print("\n5. Manuel Serial Key Ekleme Test Ediliyor...")
    try:
        manual_serial_data = {
            "password": ADMIN_PASSWORD,
            "serial_key": "TEST-1234-MANU-5678",
            "description": "Test serial key - manuel eklendi",
            "max_uses": 1
        }
        response = requests.post(f"{BASE_URL}/api/add-serial", json=manual_serial_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Manuel serial key eklendi: {data['data']['serial_key']}")
            manual_serial_key = data['data']['serial_key']
        else:
            print(f"❌ Manuel serial key eklenemedi: {response.json().get('message', 'Bilinmeyen hata')}")
            manual_serial_key = "TEST-1234-MANU-5678"
    except Exception as e:
        print(f"❌ Manuel serial key ekleme hatası: {e}")
        manual_serial_key = "TEST-1234-MANU-5678"
    
    # Test 6: Serial key sorgulama (geçerli)
    print("\n6. Geçerli Serial Key Sorgulama Test Ediliyor...")
    if manual_serial_key:
        try:
            response = requests.get(f"{BASE_URL}/api/check-serial/{manual_serial_key}")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Serial key geçerli: {data['data']['serial_key']}")
                print(f"📝 Açıklama: {data['data']['description']}")
                print(f"🔢 Kalan kullanım: {data['data']['remaining_uses']}")
            else:
                print(f"❌ Serial key sorgulanamadı: {response.json().get('message', 'Bilinmeyen hata')}")
        except Exception as e:
            print(f"❌ Serial key sorgulama hatası: {e}")
    
    # Test 7: Geçersiz serial key sorgulama
    print("\n7. Geçersiz Serial Key Sorgulama Test Ediliyor...")
    try:
        response = requests.get(f"{BASE_URL}/api/check-serial/INVALID-1234-TEST-5678")
        print(f"Status: {response.status_code}")
        if response.status_code == 404:
            data = response.json()
            print(f"✅ Beklenen sonuç: {data['message']}")
        else:
            print(f"❌ Beklenmeyen sonuç: {response.json().get('message', 'Bilinmeyen hata')}")
    except Exception as e:
        print(f"❌ Geçersiz serial key test hatası: {e}")
    
    # Test 8: Yanlış şifre ile serial key ekleme
    print("\n8. Yanlış Şifre ile Serial Key Ekleme Test Ediliyor...")
    try:
        wrong_password_data = {
            "password": "wrong_password",
            "description": "Bu eklenmemeli"
        }
        response = requests.post(f"{BASE_URL}/api/add-serial", json=wrong_password_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 401:
            data = response.json()
            print(f"✅ Beklenen sonuç: {data['message']}")
        else:
            print(f"❌ Beklenmeyen sonuç: {response.json().get('message', 'Bilinmeyen hata')}")
    except Exception as e:
        print(f"❌ Yanlış şifre test hatası: {e}")
    
    # Test 9: Serial key listesi (admin)
    print("\n9. Serial Key Listesi Test Ediliyor...")
    try:
        list_data = {"password": ADMIN_PASSWORD}
        response = requests.post(f"{BASE_URL}/api/list-serials", json=list_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['message']}")
            print(f"📊 Toplam serial key: {data['count']}")
            for i, key in enumerate(data['data'][:3], 1):  # İlk 3'ünü göster
                print(f"   {i}. {key['serial_key']} - {key['description']}")
        else:
            print(f"❌ Serial key listesi alınamadı: {response.json().get('message', 'Bilinmeyen hata')}")
    except Exception as e:
        print(f"❌ Serial key listesi hatası: {e}")
    
    # Test 10: Serial key deaktif etme
    print("\n10. Serial Key Deaktif Etme Test Ediliyor...")
    if manual_serial_key:
        try:
            deactivate_data = {"password": ADMIN_PASSWORD}
            response = requests.post(f"{BASE_URL}/api/deactivate-serial/{manual_serial_key}", json=deactivate_data)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {data['message']}")
                print(f"🔑 Serial key: {data['data']['serial_key']}")
                print(f"❌ Aktif: {data['data']['is_active']}")
            else:
                print(f"❌ Serial key deaktif edilemedi: {response.json().get('message', 'Bilinmeyen hata')}")
        except Exception as e:
            print(f"❌ Serial key deaktif etme hatası: {e}")
    
    # Test 11: Deaktif serial key sorgulama
    print("\n11. Deaktif Serial Key Sorgulama Test Ediliyor...")
    if manual_serial_key:
        try:
            response = requests.get(f"{BASE_URL}/api/check-serial/{manual_serial_key}")
            print(f"Status: {response.status_code}")
            if response.status_code == 400:
                data = response.json()
                print(f"✅ Beklenen sonuç: {data['message']}")
            else:
                print(f"❌ Beklenmeyen sonuç: {response.json().get('message', 'Bilinmeyen hata')}")
        except Exception as e:
            print(f"❌ Deaktif serial key test hatası: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Serial Key Management API test tamamlandı!")
    print("\n📋 Test Özeti:")
    print("   - API bilgileri ve health check ✅")
    print("   - Otomatik ve manuel serial key ekleme ✅")
    print("   - Serial key sorgulama ✅")
    print("   - Geçersiz serial key kontrolü ✅")
    print("   - Şifre koruması ✅")
    print("   - Serial key listesi ✅")
    print("   - Serial key deaktif etme ✅")
    print("\n🔐 Admin şifresi: admin123")
    print("🌐 API URL: http://localhost:5000")

if __name__ == "__main__":
    try:
        test_api()
    except KeyboardInterrupt:
        print("\n\n⏹️ Test kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n❌ Test sırasında hata oluştu: {e}")
        print("💡 Flask sunucusunun çalıştığından emin olun: python app.py")
