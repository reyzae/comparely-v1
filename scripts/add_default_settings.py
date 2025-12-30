"""
Script untuk menambahkan default app settings ke database
"""

import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import text
from app.database import engine, SessionLocal
from datetime import datetime

def add_default_settings():
    """Menambahkan default app settings ke database"""
    
    db = SessionLocal()
    
    try:
        print("="*60)
        print("  Menambahkan Default App Settings")
        print("="*60)
        
        # Settings yang akan ditambahkan
        settings = [
            ('site_name', 'COMPARELY', 'Nama aplikasi'),
            ('site_description', 'Platform Perbandingan Perangkat Terlengkap', 'Deskripsi aplikasi'),
            ('maintenance_mode', 'false', 'Mode maintenance - set true untuk maintenance'),
            ('max_comparison', '5', 'Maksimal jumlah device untuk compare sekaligus'),
            ('items_per_page', '20', 'Jumlah item per halaman untuk pagination'),
            ('enable_ai', 'true', 'Aktifkan fitur AI recommendation'),
            ('enable_notifications', 'true', 'Aktifkan sistem notifikasi'),
            ('session_timeout', '3600', 'Session timeout dalam detik (default: 1 jam)'),
            ('max_upload_size', '5242880', 'Maksimal ukuran upload dalam bytes (default: 5MB)'),
            ('default_currency', 'IDR', 'Mata uang default untuk harga'),
        ]
        
        # Hapus data lama jika ada
        print("\n🗑️  Menghapus settings lama (jika ada)...")
        keys = [s[0] for s in settings]
        placeholders = ','.join([f"'{k}'" for k in keys])
        db.execute(text(f"DELETE FROM app_settings WHERE `key` IN ({placeholders})"))
        db.commit()
        
        # Insert settings baru
        print("\n➕ Menambahkan settings baru...")
        now = datetime.now()
        
        for key, value, description in settings:
            sql = text("""
                INSERT INTO app_settings (`key`, `value`, `description`, created_at, updated_at)
                VALUES (:key, :value, :description, :created_at, :updated_at)
            """)
            
            db.execute(sql, {
                'key': key,
                'value': value,
                'description': description,
                'created_at': now,
                'updated_at': now
            })
            print(f"   ✅ {key}: {value}")
        
        db.commit()
        
        # Tampilkan hasil
        print("\n📊 Settings yang berhasil ditambahkan:")
        result = db.execute(text("SELECT `key`, `value`, `description` FROM app_settings ORDER BY `key`"))
        
        for row in result:
            print(f"   • {row[0]}: {row[1]}")
            print(f"     └─ {row[2]}")
        
        print("\n✅ Berhasil menambahkan default app settings!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_default_settings()
