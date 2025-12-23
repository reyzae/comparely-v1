"""
Script untuk RESET database devices
Menghapus semua data devices dari database

⚠️ HATI-HATI: Script ini akan menghapus SEMUA data devices!

Cara pakai: python reset_database.py
"""

from app.database import SessionLocal
from app.models import Device, Benchmark
from sqlalchemy import text

def reset_database():
    """
    Hapus semua data dari tabel devices dan benchmarks
    """
    print("=" * 70)
    print("⚠️  DATABASE RESET - COMPARELY")
    print("=" * 70)
    print("Script ini akan menghapus SEMUA data devices dan benchmarks!")
    print("=" * 70)
    
    # Konfirmasi dari user
    confirm = input("\nKetik 'RESET' untuk konfirmasi (atau Enter untuk batal): ")
    
    if confirm != 'RESET':
        print("\n❌ Reset dibatalkan!")
        return
    
    db = SessionLocal()
    
    try:
        # Hitung jumlah data sebelum dihapus
        device_count = db.query(Device).count()
        benchmark_count = db.query(Benchmark).count()
        
        print(f"\n📊 Data yang akan dihapus:")
        print(f"   Devices: {device_count}")
        print(f"   Benchmarks: {benchmark_count}")
        
        # Hapus benchmarks dulu (karena ada foreign key ke devices)
        print("\n🗑️  Menghapus benchmarks...")
        db.query(Benchmark).delete()
        db.commit()
        print("   ✅ Benchmarks dihapus")
        
        # Hapus devices
        print("🗑️  Menghapus devices...")
        db.query(Device).delete()
        db.commit()
        print("   ✅ Devices dihapus")
        
        # Reset auto increment (opsional, agar ID mulai dari 1 lagi)
        print("\n🔄 Reset auto increment...")
        try:
            db.execute(text("ALTER TABLE devices AUTO_INCREMENT = 1"))
            db.execute(text("ALTER TABLE benchmarks AUTO_INCREMENT = 1"))
            db.commit()
            print("   ✅ Auto increment direset")
        except Exception as e:
            print(f"   ⚠️  Auto increment reset gagal (tidak masalah): {str(e)}")
        
        print("\n" + "=" * 70)
        print("✅ DATABASE BERHASIL DIRESET!")
        print("=" * 70)
        print(f"Dihapus: {device_count} devices, {benchmark_count} benchmarks")
        print("\n💡 Database sekarang kosong dan siap untuk import data baru")
        print("   Jalankan: python import_csv.py data/scraped_phones.csv")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        db.rollback()
    finally:
        db.close()

def quick_reset():
    """
    Reset cepat tanpa konfirmasi (untuk automation)
    HANYA gunakan jika Anda yakin!
    """
    db = SessionLocal()
    try:
        db.query(Benchmark).delete()
        db.query(Device).delete()
        db.commit()
        print("✅ Database direset (quick mode)")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_database()
