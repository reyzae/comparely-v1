# 🔧 Troubleshooting

Panduan mengatasi masalah umum yang mungkin terjadi saat menggunakan COMPARELY.

---

## Database Connection Error

**Problem**: `Can't connect to MySQL server` atau `Access denied for user`

**Solutions**:

1. Pastikan MySQL service sudah running:

   ```bash
   # Windows
   net start MySQL80
   
   # Linux/Mac
   sudo systemctl start mysql
   ```

2. Cek credentials di `.env`:

   ```env
   DATABASE_URL=mysql+mysqlconnector://root:YOUR_PASSWORD@localhost/comparely
   ```

3. Pastikan database `comparely` sudah dibuat:

   ```bash
   mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS comparely;"
   ```

---

## Import CSV Failed

**Problem**: `Validation error` saat import CSV

**Solutions**:

1. Cek format CSV sesuai dengan template di `data/devices.csv`

2. Pastikan header CSV benar:

   ```
   name,brand,category_id,cpu,gpu,ram,storage,camera,battery,price,screen,release_year,source,image_url
   ```

3. Pastikan field wajib tidak kosong: `name`, `brand`, `category_id`, `price`

4. Cek tipe data:
   - `price`: harus angka (integer/decimal)
   - `category_id`: harus 1 (smartphone) atau 2 (laptop)
   - `release_year`: harus angka tahun (contoh: 2024)

---

## AI Error

**Problem**: Analisis AI gagal dimuat atau menampilkan pesan error

**Solutions**:

1. **Pastikan `AI_API_KEY` sudah diset di `.env`**:

   ```env
   AI_API_KEY=xai-your-actual-api-key-here
   ```
   
   **Cara mendapatkan API key**:
   - Kunjungi https://console.x.ai/
   - Login atau buat akun
   - Buat API key baru
   - Copy dan paste ke file `.env`

2. **Cek koneksi internet**

   Pastikan komputer Anda terhubung ke internet untuk mengakses AI API.

3. **Verifikasi API key masih valid**
   
   - Login ke [console.x.ai](https://console.x.ai/)
   - Cek status API key
   - Jika expired, buat key baru

4. **Cek quota API**
   
   - AI memiliki limit penggunaan
   - Cek usage di console.x.ai
   - Upgrade plan jika sudah habis

5. **Restart aplikasi setelah menambahkan API key**

   ```bash
   # Stop server (Ctrl+C)
   # Lalu jalankan lagi
   uvicorn app.main:app --reload
   ```

6. **Pesan error spesifik**:

   - **"AI tidak tersedia"**: API key belum diset
   - **"API Key tidak valid"**: API key salah atau expired
   - **"Quota API habis"**: Limit penggunaan tercapai
   - **"Request timeout"**: Koneksi lambat atau bermasalah
   - **"Tidak ada koneksi internet"**: Cek koneksi internet

**Note**: Aplikasi tetap berfungsi tanpa AI. Fitur perbandingan manual tetap tersedia di halaman compare.

---

## Module Not Found Error

**Problem**: `ModuleNotFoundError: No module named 'xxx'`

**Solutions**:

1. Pastikan virtual environment sudah aktif:

   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

2. Install ulang dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Server Won't Start

**Problem**: `Address already in use` atau port 8000 sudah dipakai

**Solutions**:

1. Gunakan port lain:

   ```bash
   uvicorn app.main:app --reload --port 8001
   ```

2. Atau kill process yang menggunakan port 8000:

   ```bash
   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   
   # Linux/Mac
   lsof -ti:8000 | xargs kill -9
   ```

---

## CI/CD Badge Not Showing

**Problem**: Badge CI Status tidak muncul di README

**Solutions**:

1. Pastikan file `.github/workflows/ci.yml` sudah ada di repository

2. Push ke GitHub:

   ```bash
   git add .
   git commit -m "Add CI workflow"
   git push origin main
   ```

3. Tunggu workflow pertama kali running (bisa dilihat di tab Actions di GitHub)

4. Badge akan otomatis muncul setelah workflow pertama selesai

---

**Jika masalah masih berlanjut**, silakan buka issue di [GitHub Repository](https://github.com/reyzae/comparely/issues).
