# 📥 Cara Import Data dari Google Sheets

## 📋 Langkah-Langkah

### 1. Export dari Google Sheets
1. Buka Google Sheets yang berisi data devices
2. Klik **File** → **Download** → **Comma Separated Values (.csv)**
3. Rename file menjadi `devices.csv`
4. Pindahkan file ke folder `data/` di project ini

### 2. Jalankan Script Import
```bash
# Aktifkan virtual environment dulu
.\.venv\Scripts\Activate.ps1

# Jalankan script import
python import_csv.py
```

### 3. Verifikasi Data
Setelah import selesai, cek di Swagger UI:
```
http://127.0.0.1:8000/docs
```
Buka endpoint `GET /devices/` untuk melihat semua data yang sudah masuk.

---

## 📝 Format CSV yang Benar

File CSV harus punya header (baris pertama) dengan kolom berikut:

```
name,brand,category_id,cpu,gpu,ram,storage,camera,battery,screen,release_year,price,image_url,source_data
```

**Kolom Wajib:**
- `name`: Nama device
- `brand`: Merek
- `category_id`: 1 (Smartphone) atau 2 (Laptop)
- `price`: Harga (angka saja, tanpa titik/koma)

**Kolom Opsional:**
- Semua kolom lain boleh kosong, akan diisi "N/A" otomatis

---

## ⚠️ Tips Penting

### Format Harga
```
✅ BENAR: 12999000
❌ SALAH: 12.999.000
❌ SALAH: Rp 12.999.000
```

### Category ID
```
1 = Smartphone
2 = Laptop
```
Pastikan kategori sudah dibuat dulu di database!

### Encoding File
Pastikan file CSV disimpan dengan encoding **UTF-8** agar karakter Indonesia tidak error.

---

## 🔍 Troubleshooting

### Error: "File not found"
- Pastikan file `devices.csv` ada di folder `data/`
- Atau jalankan dengan path custom: `python import_csv.py path/to/file.csv`

### Error: "Foreign key constraint"
- Pastikan kategori dengan ID tersebut sudah ada
- Buat kategori dulu lewat `POST /categories/`

### Error: "Invalid price format"
- Hapus semua titik, koma, atau karakter non-angka dari kolom price
- Contoh: `12999000` bukan `12.999.000`

---

## 📊 Contoh Data

Lihat file `data/devices_sample.csv` untuk contoh format yang benar.
