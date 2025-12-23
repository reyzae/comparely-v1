# Panduan Penggunaan Scraper & Database Management

## 🚀 Enhanced Scraper

Script `scrape_gsmarena.py` sudah dilengkapi dengan fitur:

### Fitur Utama:
1. **✅ Filter Data N/A** - Hanya simpan data lengkap (camera, battery, RAM, storage)
2. **✅ Pencegahan Duplicate** - Cek nama & brand sebelum simpan
3. **✅ Auto-Retry** - 3x percobaan jika koneksi gagal
4. **✅ Progress Detail** - Lihat status setiap device (SAVED/SKIP/DUPLICATE)
5. **✅ Statistik Lengkap** - Total scraped, complete, skipped

### Cara Menggunakan:

```bash
# Jalankan scraper
python scrape_gsmarena.py

# Output akan di: data/scraped_phones.csv
```

### Output Example:
```
📊 STATISTIK:
   Total scraped      : 150~
   ✅ Complete & saved : 45
   ⏭️  Skipped (N/A)    : 95
   ⏭️  Skipped (Dup)    : 10
```

---

## 🗑️ Database Reset

### Opsi 1: Via Script (Recommended)

```bash
python reset_database.py
```

**Fitur:**
- Konfirmasi safety (ketik 'RESET')
- Tampilkan jumlah data yang akan dihapus
- Reset auto increment ID
- Aman dan terkontrol

### Opsi 2: Via API Endpoint

```bash
# Reset database via API
curl -X POST http://localhost:8000/admin/reset-database

# Cek statistik database
curl http://localhost:8000/admin/stats
```

**Response:**
```json
{
  "success": true,
  "message": "Database berhasil direset",
  "deleted": {
    "devices": 80,
    "benchmarks": 0
  }
}
```

---

## 📋 Workflow Lengkap

### 1. Reset Database (jika perlu)
```bash
python reset_database.py
# Ketik: RESET
```

### 2. Scrape Data Baru
```bash
python scrape_gsmarena.py
# Tunggu sampai selesai (5-15 menit)
```

### 3. Import ke Database
```bash
python import_csv.py data/scraped_phones.csv
```

### 4. Verifikasi
```bash
# Jalankan web app
uvicorn app.main:app --reload

# Buka browser: http://localhost:8000
```

---

## 🎯 Tips & Best Practices

### Untuk Demo/Presentasi:
1. **Scrape 1x saja** - Gunakan data yang sudah di-scrape
2. **Fokus ke kualitas** - 40-50 devices lengkap lebih baik dari 100 dengan N/A
3. **Backup data** - Copy CSV sebelum import ulang

### Troubleshooting:

**Q: Scraper dapat banyak SKIP?**
- Normal! Banyak model di GSMArena belum punya data lengkap
- Model upcoming/rumor memang datanya tidak complete
- Target: 40-50 complete dari 150 scraped sudah bagus

**Q: Duplicate terdeteksi?**
- Bagus! Berarti filter bekerja
- Duplicate bisa terjadi jika scrape ulang tanpa reset DB

**Q: Import gagal?**
- Pastikan database MySQL running
- Cek .env file (DATABASE_URL)
- Reset database dulu jika ada konflik

---

## 🔧 Konfigurasi Scraper

Edit `scrape_gsmarena.py` jika perlu:

```python
# Jumlah model per brand
MODELS_TO_SCRAPE = 30  # Default: 30

# Retry attempts
MAX_RETRIES = 3  # Default: 3

# Brands
BRANDS = {
    "Samsung": "samsung-phones-9",
    "Xiaomi": "xiaomi-phones-80",
    # Tambah brand lain di sini
}
```

---

## 📊 Database Stats API

Cek statistik database:

```bash
curl http://localhost:8000/admin/stats
```

Response:
```json
{
  "total_devices": 45,
  "total_benchmarks": 0,
  "brands": {
    "Samsung": 10,
    "Xiaomi": 12,
    "Oppo": 8,
    "Vivo": 9,
    "Infinix": 6
  }
}
```

---

**Happy Scraping! 🚀**
