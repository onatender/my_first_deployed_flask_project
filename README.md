# Serial Key Management API

Flask tabanlı serial key yönetim sistemi. Admin şifresi ile korumalı serial key ekleme ve sorgulama özelliklerine sahiptir.

## Özellikler

- 🔐 **Admin Şifre Koruması**: Serial key ekleme işlemleri şifre ile korunur
- 🔑 **Serial Key Oluşturma**: Otomatik veya manuel serial key oluşturma
- 🔍 **Serial Key Sorgulama**: Serial key geçerliliği kontrolü
- ⏰ **Son Kullanma Tarihi**: Serial key'ler için son kullanma tarihi
- 🔢 **Kullanım Limiti**: Serial key'ler için maksimum kullanım sayısı
- 📊 **Admin Paneli**: Tüm serial key'leri listeleme ve yönetim

## Kurulum

1. Projeyi indirin
2. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

## Çalıştırma

```bash
python app.py
```

API `http://localhost:5000` adresinde çalışacaktır.

## API Endpoints

### Ana Sayfa
- **GET** `/` - API bilgileri ve endpoint listesi

### Serial Key Ekleme (Admin)
- **POST** `/api/add-serial`
- **Gerekli**: `password` (admin şifresi)
- **Opsiyonel**: `serial_key`, `description`, `expiry_date`, `max_uses`

### Serial Key Sorgulama
- **GET** `/api/check-serial/<serial_key>`
- Serial key geçerliliğini kontrol eder

### Serial Key Listesi (Admin)
- **POST** `/api/list-serials`
- **Body**: `{"password": "admin123"}`
- Tüm serial key'leri listeler

### Serial Key Deaktif Etme (Admin)
- **POST** `/api/deactivate-serial/<serial_key>`
- Serial key'i deaktif eder

### Admin Bilgileri
- **GET** `/api/admin-info`
- API kullanım bilgileri

### Sağlık Kontrolü
- **GET** `/health`
- API durumu

## Serial Key Formatı

Serial key'ler şu formatta olmalıdır:
- **Format**: `XXXX-XXXX-XXXX-XXXX`
- **Uzunluk**: 19 karakter (4 grup, her grupta 4 karakter)
- **Karakterler**: Büyük harf ve rakam (A-Z, 0-9)

**Örnek**: `ABCD-1234-EFGH-5678`

## Kullanım Örnekleri

### 1. Serial Key Ekleme

**Otomatik Serial Key Oluşturma:**
```bash
curl -X POST http://localhost:5000/api/add-serial \
  -H "Content-Type: application/json" \
  -d '{
    "password": "admin123",
    "description": "Premium kullanıcı için",
    "expiry_date": "2024-12-31T23:59:59",
    "max_uses": 5
  }'
```

**Manuel Serial Key Ekleme:**
```bash
curl -X POST http://localhost:5000/api/add-serial \
  -H "Content-Type: application/json" \
  -d '{
    "password": "admin123",
    "serial_key": "ABCD-1234-EFGH-5678",
    "description": "Özel serial key",
    "max_uses": 1
  }'
```

### 2. Serial Key Sorgulama

```bash
curl http://localhost:5000/api/check-serial/ABCD-1234-EFGH-5678
```

**Başarılı Yanıt:**
```json
{
  "success": true,
  "message": "Serial key geçerli",
  "is_valid": true,
  "data": {
    "serial_key": "ABCD-1234-EFGH-5678",
    "created_at": "2024-01-20T10:30:00",
    "description": "Premium kullanıcı için",
    "expiry_date": "2024-12-31T23:59:59",
    "max_uses": 5,
    "current_uses": 1,
    "remaining_uses": 4
  }
}
```

### 3. Serial Key Listesi (Admin)

```bash
curl -X POST http://localhost:5000/api/list-serials \
  -H "Content-Type: application/json" \
  -d '{"password": "admin123"}'
```

### 4. Serial Key Deaktif Etme (Admin)

```bash
curl -X POST http://localhost:5000/api/deactivate-serial/ABCD-1234-EFGH-5678 \
  -H "Content-Type: application/json" \
  -d '{"password": "admin123"}'
```

## Python Örnekleri

```python
import requests

BASE_URL = "http://localhost:5000"

# Serial key ekleme
def add_serial_key(password, description="", expiry_date=None, max_uses=1):
    data = {
        "password": password,
        "description": description,
        "max_uses": max_uses
    }
    if expiry_date:
        data["expiry_date"] = expiry_date
    
    response = requests.post(f"{BASE_URL}/api/add-serial", json=data)
    return response.json()

# Serial key sorgulama
def check_serial_key(serial_key):
    response = requests.get(f"{BASE_URL}/api/check-serial/{serial_key}")
    return response.json()

# Serial key listesi
def list_serial_keys(password):
    response = requests.post(f"{BASE_URL}/api/list-serials", json={"password": password})
    return response.json()

# Örnek kullanım
if __name__ == "__main__":
    # Serial key ekle
    result = add_serial_key(
        password="admin123",
        description="Test serial key",
        expiry_date="2024-12-31T23:59:59",
        max_uses=3
    )
    print("Serial key eklendi:", result)
    
    # Serial key sorgula
    if result.get("success"):
        serial_key = result["data"]["serial_key"]
        check_result = check_serial_key(serial_key)
        print("Serial key kontrolü:", check_result)
```

## Güvenlik Notları

⚠️ **Önemli Güvenlik Uyarıları:**

1. **Admin Şifresi**: Varsayılan şifre `admin123`'tür. **Mutlaka değiştirin!**
2. **Production**: Gerçek uygulamada environment variable kullanın
3. **HTTPS**: Production'da HTTPS kullanın
4. **Veritabanı**: Gerçek uygulamada gerçek veritabanı kullanın
5. **Rate Limiting**: API'ye rate limiting ekleyin

## Admin Şifresi Değiştirme

`app.py` dosyasında `ADMIN_PASSWORD` değişkenini değiştirin:

```python
ADMIN_PASSWORD = "yeni_güvenli_şifreniz"
```

## Hata Kodları

- **200**: Başarılı
- **201**: Oluşturuldu
- **400**: Geçersiz istek
- **401**: Yetkisiz erişim
- **404**: Bulunamadı
- **500**: Sunucu hatası

## Geliştirme

Debug modu aktif olarak çalışır. Production için:

1. `debug=False` yapın
2. Gunicorn gibi production WSGI server kullanın
3. Environment variable'ları ayarlayın

## Lisans

Bu proje MIT lisansı altında açık kaynak kodludur.
