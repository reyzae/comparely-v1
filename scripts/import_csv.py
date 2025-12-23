"""
Script untuk import data devices dari CSV ke database MySQL.

Cara Pakai:
1. Export Google Sheets ke CSV dengan nama 'devices.csv'
2. Simpan file CSV di folder 'data/'
3. Jalankan: python import_csv.py

Format CSV yang diharapkan:
name,brand,category_id,cpu,gpu,ram,storage,camera,battery,screen,release_year,price,image_url,source_data
"""

import csv
import sys
from decimal import Decimal
from app.database import SessionLocal
from app.models import Device

def import_devices_from_csv(csv_file_path: str):
    """
    Import devices dari file CSV ke database.
    
    Args:
        csv_file_path: Path ke file CSV
    """
    db = SessionLocal()
    success_count = 0
    error_count = 0
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            # Baca CSV dengan DictReader (otomatis pakai header sebagai key)
            csv_reader = csv.DictReader(file)
            
            print(f"📂 Membaca file: {csv_file_path}")
            print("=" * 60)
            
            for row_num, row in enumerate(csv_reader, start=2):  # Start=2 karena row 1 adalah header
                try:
                    # Validasi: Pastikan field wajib tidak kosong
                    required_fields = ['name', 'brand', 'category_id', 'price']
                    for field in required_fields:
                        if not row.get(field) or row[field].strip() == '':
                            raise ValueError(f"Field '{field}' tidak boleh kosong")
                    
                    # Buat object Device baru
                    device = Device(
                        name=row['name'].strip(),
                        brand=row['brand'].strip(),
                        category_id=int(row['category_id']),
                        cpu=row.get('cpu', '').strip() or 'N/A',
                        gpu=row.get('gpu', '').strip() or 'N/A',
                        ram=row.get('ram', '').strip() or 'N/A',
                        storage=row.get('storage', '').strip() or 'N/A',
                        camera=row.get('camera', '').strip() or 'N/A',
                        battery=row.get('battery', '').strip() or 'N/A',
                        screen=row.get('screen', '').strip() or 'N/A',
                        release_year=int(row.get('release_year', 2023)),
                        price=Decimal(row['price'].replace(',', '').replace('.', '')),  # Hapus koma/titik pemisah ribuan
                        image_url=row.get('image_url', '').strip() or None,
                        description=row.get('source_data', '').strip() or None  # Gunakan source_data sebagai description
                    )
                    
                    # Tambahkan ke database
                    db.add(device)
                    db.commit()
                    
                    success_count += 1
                    print(f"✅ Baris {row_num}: {device.name} - Berhasil")
                    
                except ValueError as e:
                    error_count += 1
                    print(f"❌ Baris {row_num}: Error - {str(e)}")
                    db.rollback()
                    
                except Exception as e:
                    error_count += 1
                    print(f"❌ Baris {row_num}: Error tidak terduga - {str(e)}")
                    db.rollback()
            
            print("=" * 60)
            print(f"\n📊 HASIL IMPORT:")
            print(f"   ✅ Berhasil: {success_count} devices")
            print(f"   ❌ Gagal: {error_count} devices")
            print(f"   📝 Total: {success_count + error_count} baris diproses")
            
    except FileNotFoundError:
        print(f"❌ ERROR: File '{csv_file_path}' tidak ditemukan!")
        print(f"   Pastikan file CSV ada di folder yang benar.")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        sys.exit(1)
        
    finally:
        db.close()


if __name__ == "__main__":
    # Default path ke file CSV
    csv_path = "data/devices.csv"
    
    # Bisa juga terima argument dari command line
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    
    print("🚀 COMPARELY - CSV Import Script")
    print("=" * 60)
    
    import_devices_from_csv(csv_path)
    
    print("\n✨ Import selesai!")
