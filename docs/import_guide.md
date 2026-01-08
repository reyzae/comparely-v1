# Cara Import Data dari Google Sheets

## Langkah-Langkah

### 1. Export dari Google Sheets
1. Buka Google Sheets yang berisi data HP
2. Klik **File** → **Download** → **Comma Separated Values (.csv)**
3. Rename file jadi `devices.csv`
4. Pindahin file ke folder `data/` di project ini

### 2. Jalanin Script Import
```bash
# Aktifin virtual environment dulu
.\.venv\Scripts\Activate.ps1

# Jalanin script import
python import_csv.py
```

### 3. Verifikasi Data
Setelah import selesai, cek di Swagger UI:
```
http://127.0.0.1:8000/docs
```
Buka endpoint `GET /devices/` buat liat semua data yang udah masuk.

---

## Format CSV yang Bener

File CSV harus punya header (baris pertama) dengan kolom berikut:

```
name,brand,category_id,cpu,gpu,ram,storage,camera,battery,screen,release_year,price,image_url,description
```

**Note**: `description` bisa juga pake nama field `source_data` (keduanya didukung).

**Kolom Wajib:**
- `name`: Nama HP
- `brand`: Merek
- `category_id`: 1 (Smartphone) atau 2 (Laptop)
- `price`: Harga (angka aja, tanpa titik/koma)

**Kolom Opsional:**
- Semua kolom lain boleh kosong, bakal diisi "N/A" otomatis

---

## Tips Penting

### Format Harga
```
BENER: 12999000
SALAH: 12.999.000
SALAH: Rp 12.999.000
```

### Category ID
```
1 = Smartphone
2 = Laptop
```
Pastiin kategori udah dibuat dulu di database!

### Encoding File
Pastiin file CSV disimpen dengan encoding **UTF-8** biar karakter Indonesia gak error.

---

## Troubleshooting

### Error: "File not found"
- Pastiin file `devices.csv` ada di folder `data/`
- Atau jalanin dengan path custom: `python import_csv.py path/to/file.csv`

### Error: "Foreign key constraint"
- Pastiin kategori dengan ID tersebut udah ada
- Bikin kategori dulu lewat `POST /categories/`

### Error: "Invalid price format"
- Hapus semua titik, koma, atau karakter non-angka dari kolom price
- Contoh: `12999000` bukan `12.999.000`

---

## Contoh Data

Liat file `data/devices_sample.csv` buat contoh format yang bener.
