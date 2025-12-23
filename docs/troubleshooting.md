# 🔧 Troubleshooting & Bug Fixes - COMPARELY Project

Dokumen ini mencatat semua masalah yang ditemukan selama development dan solusinya.

---

## 📋 Daftar Isi
1. [Foreign Key Constraint Error](#1-foreign-key-constraint-error)
2. [Pydantic v1 vs v2 Incompatibility](#2-pydantic-v1-vs-v2-incompatibility)
3. [Compare Endpoint Serialization Error](#3-compare-endpoint-serialization-error)
4. [Uvicorn Command Not Found](#4-uvicorn-command-not-found)
5. [Validation Error 422](#5-validation-error-422-unprocessable-content)

---

## 1. Foreign Key Constraint Error

### ❌ **Error Message:**
```
sqlalchemy.exc.IntegrityError: (mysql.connector.errors.IntegrityError) 1452 (23000): 
Cannot add or update a child row: a foreign key constraint fails 
(`comparely`.`devices`, CONSTRAINT `devices_ibfk_1` FOREIGN KEY (`category_id`) 
REFERENCES `categories` (`id`))
```

### 🔍 **Penyebab:**
User mencoba menambahkan device dengan `category_id` yang tidak ada di tabel `categories`.

### ✅ **Solusi:**
1. Buat kategori terlebih dahulu menggunakan endpoint `POST /categories/`
2. Catat ID kategori yang dibuat (misal: `id: 1`)
3. Gunakan ID tersebut saat membuat device baru

**Contoh:**
```json
// 1. Buat kategori dulu
POST /categories/
{
  "name": "Smartphone"
}

// Response: {"id": 1, "name": "smartphone"}

// 2. Baru buat device dengan category_id yang valid
POST /devices/
{
  "category_id": 1,  // ← Gunakan ID dari kategori yang sudah dibuat
  ...
}
```

### 📝 **File Terkait:**
- `app/routers/categories.py`
- `app/models.py` (relasi foreign key)

---

## 2. Pydantic v1 vs v2 Incompatibility

### ❌ **Error Message:**
```
UserWarning: Valid config keys have changed in V2:
* 'orm_mode' has been renamed to 'from_attributes'
```

### 🔍 **Penyebab:**
Kode menggunakan sintaks Pydantic v1 (`orm_mode = True`), tapi library yang terinstall adalah Pydantic v2.

### ✅ **Solusi:**
Update semua Pydantic schema untuk menggunakan sintaks v2.

**Perubahan di `app/schemas/device.py`:**
```python
# ❌ SEBELUM (Pydantic v1)
class Device(DeviceBase):
    id: int
    
    class Config:
        orm_mode = True

# ✅ SESUDAH (Pydantic v2)
class Device(DeviceBase):
    id: int
    
    class Config:
        from_attributes = True
```

### 📝 **File yang Diperbaiki:**
- `app/schemas/device.py`
- `app/schemas/category.py`
- `app/schemas/benchmark.py`

---

## 3. Compare Endpoint Serialization Error

### ❌ **Error Message:**
```
500 Internal Server Error
```

### 🔍 **Penyebab:**
Ada 2 masalah:
1. Router menggunakan `response_model=dict` yang terlalu strict
2. Service layer mencoba manual serialization dengan `.from_orm()` (Pydantic v1 syntax)

### ✅ **Solusi:**

**1. Hapus `response_model=dict` di router:**

File: `app/routers/compare.py`
```python
# ❌ SEBELUM
@router.get("/", response_model=dict)
def compare_devices(id1: int, id2: int, db: Session = Depends(get_db)):
    ...

# ✅ SESUDAH
@router.get("/")
def compare_devices(id1: int, id2: int, db: Session = Depends(get_db)):
    ...
```

**2. Return SQLAlchemy models langsung di service:**

File: `app/services/comparison_service.py`
```python
# ❌ SEBELUM (Manual serialization)
from ..schemas.device import Device as DeviceSchema

return {
    "device_1": DeviceSchema.from_orm(device1).dict(),
    "device_2": DeviceSchema.from_orm(device2).dict(),
    "highlights": highlights
}

# ✅ SESUDAH (Biarkan FastAPI yang handle)
return {
    "device_1": device1,
    "device_2": device2,
    "highlights": highlights
}
```

### 📝 **File yang Diperbaiki:**
- `app/routers/compare.py`
- `app/services/comparison_service.py`

---

## 4. Uvicorn Command Not Found

### ❌ **Error Message:**
```powershell
uvicorn : The term 'uvicorn' is not recognized as the name of a cmdlet, 
function, script file, or operable program.
```

### 🔍 **Penyebab:**
Virtual environment (`.venv`) belum diaktifkan di terminal PowerShell.

### ✅ **Solusi:**
Aktifkan virtual environment terlebih dahulu:

```powershell
# Aktifkan .venv
.\.venv\Scripts\Activate.ps1

# Setelah berhasil, akan muncul (.venv) di awal prompt
(.venv) PS E:\SOURCE CODE REYZA\comparely>

# Baru jalankan uvicorn
uvicorn app.main:app --reload
```

### 💡 **Tips:**
Jika muncul error "running scripts is disabled", jalankan:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 5. Validation Error 422 (Unprocessable Content)

### ❌ **Error Message:**
```
422 Unprocessable Content
```

### 🔍 **Penyebab:**
Data yang dikirim tidak sesuai dengan schema yang didefinisikan. Kemungkinan:
- Ada field wajib yang kosong
- Tipe data salah (misal: string untuk field integer)
- Format data tidak sesuai (misal: `price` pakai koma sebagai pemisah ribuan)

### ✅ **Solusi:**
1. Cek schema di Swagger UI (klik "Schema" tab)
2. Pastikan semua field wajib terisi
3. Pastikan tipe data sesuai

**Contoh Kesalahan Umum:**

```json
// ❌ SALAH
{
  "category_id": 0,        // ← ID 0 tidak valid
  "price": "1.000.000",    // ← Format salah (pakai titik)
  "release_year": "2023"   // ← Seharusnya integer, bukan string
}

// ✅ BENAR
{
  "category_id": 1,
  "price": 1000000,        // atau "1000000.00"
  "release_year": 2023
}
```

---

## 📌 Best Practices untuk Menghindari Error

### 1. **Selalu Buat Kategori Dulu**
Sebelum input device, pastikan kategori sudah ada:
```bash
GET /categories/  # Cek kategori yang tersedia
```

### 2. **Gunakan Swagger UI untuk Testing**
- Akses: `http://127.0.0.1:8000/docs`
- Swagger otomatis validasi format JSON
- Ada contoh schema yang bisa di-copy

### 3. **Cek Error di Terminal**
Jika ada error 500, selalu cek terminal yang menjalankan uvicorn untuk melihat traceback lengkap.

### 4. **Aktifkan Virtual Environment**
Setiap kali buka terminal baru, jangan lupa:
```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. **Gunakan Auto-reload**
Jalankan uvicorn dengan flag `--reload` agar perubahan kode otomatis ter-apply:
```powershell
uvicorn app.main:app --reload
```

---

## 🔍 Cara Debug Error Baru

Jika menemukan error baru, ikuti langkah ini:

1. **Catat Error Message** (screenshot atau copy-paste)
2. **Cek Terminal** (lihat traceback lengkap)
3. **Identifikasi File & Line Number** (dari traceback)
4. **Cek Dokumentasi** (Swagger UI, FastAPI docs, SQLAlchemy docs)
5. **Test dengan Data Minimal** (coba dengan data paling sederhana dulu)
6. **Tambahkan ke Dokumen Ini** (agar tidak terulang)

---

## 📚 Referensi

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic v2 Migration Guide](https://docs.pydantic.dev/latest/migration/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [MySQL Connector Python](https://dev.mysql.com/doc/connector-python/en/)

---

**Terakhir diupdate:** 3 Desember 2025  
**Versi:** 1.0
