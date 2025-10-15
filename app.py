from flask import Flask, jsonify, request
from flask_cors import CORS
import hashlib
import secrets
import string
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Admin şifresi (gerçek uygulamada environment variable kullanın)
ADMIN_PASSWORD = "admin123"  # Bu şifreyi değiştirin!

# Serial key veritabanı (gerçek uygulamada gerçek veritabanı kullanın)
serial_keys_db = []

# Serial key formatı: XXXX-XXXX-XXXX-XXXX (16 karakter)
def generate_serial_key():
    """Rastgele serial key oluşturur"""
    characters = string.ascii_uppercase + string.digits
    # 4 grup, her grupta 4 karakter
    groups = []
    for _ in range(4):
        group = ''.join(secrets.choice(characters) for _ in range(4))
        groups.append(group)
    return '-'.join(groups)

def hash_password(password):
    """Şifreyi hash'ler"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Şifre doğrulaması yapar"""
    return hash_password(password) == hashed

def is_valid_serial_format(serial_key):
    """Serial key formatını kontrol eder"""
    if not serial_key or len(serial_key) != 19:
        return False
    parts = serial_key.split('-')
    if len(parts) != 4:
        return False
    for part in parts:
        if len(part) != 4:
            return False
        if not part.isalnum():
            return False
    return True

# Ana sayfa
@app.route('/', methods=['GET'])
def home():
    """Ana sayfa"""
    return jsonify({
        "success": True,
        "message": "Serial Key Management API",
        "version": "1.0.0",
        "endpoints": {
            "add_serial": "POST /api/add-serial",
            "check_serial": "GET /api/check-serial/<serial_key>",
            "list_serials": "GET /api/list-serials",
            "admin_info": "GET /api/admin-info"
        }
    })

# Admin şifre ile serial key ekleme
@app.route('/api/add-serial', methods=['POST'])
def add_serial_key():
    """Şifre ile korumalı serial key ekleme"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "message": "JSON verisi gerekli"
            }), 400
        
        # Şifre kontrolü
        password = data.get('password')
        if not password:
            return jsonify({
                "success": False,
                "message": "Admin şifresi gerekli"
            }), 400
        
        if not verify_password(password, hash_password(ADMIN_PASSWORD)):
            return jsonify({
                "success": False,
                "message": "Geçersiz admin şifresi"
            }), 401
        
        # Serial key oluşturma veya kullanıcı tarafından verilme
        if 'serial_key' in data and data['serial_key']:
            # Kullanıcı kendi serial key'ini veriyor
            serial_key = data['serial_key'].upper().strip()
            if not is_valid_serial_format(serial_key):
                return jsonify({
                    "success": False,
                    "message": "Geçersiz serial key formatı. Format: XXXX-XXXX-XXXX-XXXX"
                }), 400
        else:
            # Otomatik serial key oluştur
            serial_key = generate_serial_key()
        
        # Serial key'in zaten var olup olmadığını kontrol et
        existing_key = next((key for key in serial_keys_db if key['serial_key'] == serial_key), None)
        if existing_key:
            return jsonify({
                "success": False,
                "message": "Bu serial key zaten mevcut"
            }), 400
        
        # Serial key bilgileri
        key_info = {
            "serial_key": serial_key,
            "created_at": datetime.now().isoformat(),
            "is_active": True,
            "description": data.get('description', ''),
            "expiry_date": data.get('expiry_date'),  # Opsiyonel
            "max_uses": data.get('max_uses', 1),  # Varsayılan 1 kullanım
            "current_uses": 0
        }
        
        # Expiry date varsa kontrol et
        if key_info['expiry_date']:
            try:
                expiry = datetime.fromisoformat(key_info['expiry_date'].replace('Z', '+00:00'))
                if expiry <= datetime.now():
                    return jsonify({
                        "success": False,
                        "message": "Son kullanma tarihi geçmiş olamaz"
                    }), 400
            except ValueError:
                return jsonify({
                    "success": False,
                    "message": "Geçersiz tarih formatı. ISO format kullanın: YYYY-MM-DDTHH:MM:SS"
                }), 400
        
        # Serial key'i veritabanına ekle
        serial_keys_db.append(key_info)
        
        return jsonify({
            "success": True,
            "message": "Serial key başarıyla eklendi",
            "data": {
                "serial_key": serial_key,
                "created_at": key_info['created_at'],
                "description": key_info['description'],
                "expiry_date": key_info['expiry_date'],
                "max_uses": key_info['max_uses']
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Sunucu hatası: {str(e)}"
        }), 500

# Serial key sorgulama
@app.route('/api/check-serial/<serial_key>', methods=['GET'])
def check_serial_key(serial_key):
    """Serial key sorgulama"""
    try:
        if not serial_key:
            return jsonify({
                "success": False,
                "message": "Serial key gerekli"
            }), 400
        
        # Serial key formatını kontrol et
        formatted_key = serial_key.upper().strip()
        if not is_valid_serial_format(formatted_key):
            return jsonify({
                "success": False,
                "message": "Geçersiz serial key formatı"
            }), 400
        
        # Serial key'i veritabanında ara
        key_info = next((key for key in serial_keys_db if key['serial_key'] == formatted_key), None)
        
        if not key_info:
            return jsonify({
                "success": False,
                "message": "Serial key bulunamadı",
                "is_valid": False
            }), 404
        
        # Serial key aktif mi kontrol et
        if not key_info['is_active']:
            return jsonify({
                "success": False,
                "message": "Serial key deaktif",
                "is_valid": False
            }), 400
        
        # Son kullanma tarihi kontrolü
        if key_info['expiry_date']:
            try:
                expiry = datetime.fromisoformat(key_info['expiry_date'].replace('Z', '+00:00'))
                if expiry <= datetime.now():
                    return jsonify({
                        "success": False,
                        "message": "Serial key süresi dolmuş",
                        "is_valid": False
                    }), 400
            except ValueError:
                pass  # Tarih formatı hatası varsa görmezden gel
        
        # Kullanım limiti kontrolü
        if key_info['current_uses'] >= key_info['max_uses']:
            return jsonify({
                "success": False,
                "message": "Serial key kullanım limiti dolmuş",
                "is_valid": False
            }), 400
        
        # Başarılı sorgulama - kullanım sayısını artır
        key_info['current_uses'] += 1
        
        return jsonify({
            "success": True,
            "message": "Serial key geçerli",
            "is_valid": True,
            "data": {
                "serial_key": formatted_key,
                "created_at": key_info['created_at'],
                "description": key_info['description'],
                "expiry_date": key_info['expiry_date'],
                "max_uses": key_info['max_uses'],
                "current_uses": key_info['current_uses'],
                "remaining_uses": key_info['max_uses'] - key_info['current_uses']
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Sunucu hatası: {str(e)}"
        }), 500

# Admin şifre ile serial key listesi
@app.route('/api/list-serials', methods=['POST'])
def list_serial_keys():
    """Admin şifre ile serial key listesi"""
    try:
        data = request.get_json()
        
        if not data or not data.get('password'):
            return jsonify({
                "success": False,
                "message": "Admin şifresi gerekli"
            }), 400
        
        if not verify_password(data['password'], hash_password(ADMIN_PASSWORD)):
            return jsonify({
                "success": False,
                "message": "Geçersiz admin şifresi"
            }), 401
        
        # Serial key'leri listele (şifreleri gizle)
        safe_keys = []
        for key in serial_keys_db:
            safe_key = {
                "serial_key": key['serial_key'],
                "created_at": key['created_at'],
                "description": key['description'],
                "is_active": key['is_active'],
                "expiry_date": key['expiry_date'],
                "max_uses": key['max_uses'],
                "current_uses": key['current_uses'],
                "remaining_uses": key['max_uses'] - key['current_uses']
            }
            safe_keys.append(safe_key)
        
        return jsonify({
            "success": True,
            "message": f"{len(safe_keys)} serial key bulundu",
            "data": safe_keys,
            "count": len(safe_keys)
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Sunucu hatası: {str(e)}"
        }), 500

# Admin bilgileri
@app.route('/api/admin-info', methods=['GET'])
def admin_info():
    """Admin bilgileri ve API kullanımı"""
    return jsonify({
        "success": True,
        "message": "Serial Key Management API",
        "admin_instructions": {
            "add_serial": {
                "method": "POST",
                "endpoint": "/api/add-serial",
                "required_fields": ["password"],
                "optional_fields": ["serial_key", "description", "expiry_date", "max_uses"],
                "example": {
                    "password": "admin123",
                    "description": "Premium kullanıcı için",
                    "expiry_date": "2024-12-31T23:59:59",
                    "max_uses": 5
                }
            },
            "check_serial": {
                "method": "GET",
                "endpoint": "/api/check-serial/<serial_key>",
                "example": "/api/check-serial/ABCD-1234-EFGH-5678"
            },
            "list_serials": {
                "method": "POST",
                "endpoint": "/api/list-serials",
                "body": {"password": "admin123"}
            }
        },
        "serial_format": "XXXX-XXXX-XXXX-XXXX (16 karakter, büyük harf ve rakam)",
        "current_serial_count": len(serial_keys_db)
    })

# Serial key deaktif etme (admin)
@app.route('/api/deactivate-serial/<serial_key>', methods=['POST'])
def deactivate_serial_key(serial_key):
    """Admin şifre ile serial key deaktif etme"""
    try:
        data = request.get_json()
        
        if not data or not data.get('password'):
            return jsonify({
                "success": False,
                "message": "Admin şifresi gerekli"
            }), 400
        
        if not verify_password(data['password'], hash_password(ADMIN_PASSWORD)):
            return jsonify({
                "success": False,
                "message": "Geçersiz admin şifresi"
            }), 401
        
        formatted_key = serial_key.upper().strip()
        key_info = next((key for key in serial_keys_db if key['serial_key'] == formatted_key), None)
        
        if not key_info:
            return jsonify({
                "success": False,
                "message": "Serial key bulunamadı"
            }), 404
        
        key_info['is_active'] = False
        
        return jsonify({
            "success": True,
            "message": "Serial key deaktif edildi",
            "data": {
                "serial_key": formatted_key,
                "is_active": False
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Sunucu hatası: {str(e)}"
        }), 500

# Health check
@app.route('/health', methods=['GET'])
def health_check():
    """Sağlık kontrolü"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "serial_keys_count": len(serial_keys_db)
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "message": "Endpoint bulunamadı"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "message": "Sunucu hatası"
    }), 500

if __name__ == '__main__':
    print("🔑 Serial Key Management API başlatılıyor...")
    print(f"🔐 Admin şifresi: {ADMIN_PASSWORD}")
    print("📝 Bu şifreyi güvenli bir yerde saklayın!")
    print("🌐 API: http://localhost:5000")
    print("📖 Dokümantasyon: http://localhost:5000/api/admin-info")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
