# COMPARELY - Platform Perbandingan Perangkat

![CI Status](https://github.com/reyzae/comparely-v1/workflows/CI%20-%20COMPARELY/badge.svg)

Web app buat bandingin dan cari rekomendasi gadget (smartphone & laptop). Dibangun pakai Python FastAPI dengan fitur rekomendasi AI.

---

## Fitur Utama

### Untuk Pengguna
- **Tampilan Modern**: Interface yang clean dan responsif
- **Cari Perangkat**: Cari gadget berdasarkan nama, brand, atau spesifikasi
- **Bandingkan Langsung**: Bandingin 2 perangkat secara detail side-by-side
- **Analisis AI**: Perbandingan otomatis pakai xAI Grok yang kasih insight mendalam
- **Rekomendasi Pintar**: Cari gadget sesuai budget dan kebutuhan kamu
- **Saran Personal AI**: Rekomendasi yang disesuaikan dengan cara pakai kamu
- **Filter Lengkap**: Filter berdasarkan kategori, brand, tahun rilis, dan range harga
- **Responsif**: Lancar dibuka di desktop, tablet, maupun HP

### Panel Admin
- **Dashboard Analytics**: Lihat statistik lengkap dengan grafik dan visualisasi
- **Kelola Device**: Tambah, edit, hapus perangkat dengan mudah, termasuk bulk actions
- **Kelola Kategori**: Atur kategori perangkat
- **Kelola User**: Manajemen user dan role
- **Role-Based Access**: Ada 3 role - Super Admin, Admin, dan Viewer
- **Activity Logs**: Tracking semua aktivitas yang dilakukan admin
- **Import/Export CSV**: Upload atau download data dalam jumlah banyak
- **Tools Tambahan**: Optimasi database dan manajemen cache

---

## Teknologi yang Dipakai

**Backend**
- Python 3.11+ & FastAPI
- SQLAlchemy ORM
- Database SQLite/MySQL
- xAI Grok untuk fitur AI
- bcrypt untuk enkripsi password

**Frontend**
- Jinja2 Templates
- Vanilla CSS
- Responsive Design

---

## Cara Install

### 1. Clone Repository
```bash
git clone https://github.com/reyzae/comparely-v1.git
cd comparely-v1
```

### 2. Bikin Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
```bash
# Copy file example
cp .env.example .env

# Edit file .env, atur:
# - DATABASE_URL (default pakai SQLite)
# - AI_API_KEY (opsional, kalau mau pakai fitur AI)
# - SECRET_KEY (generate pakai: python -c "import secrets; print(secrets.token_urlsafe(32))")
```

### 5. Inisialisasi Database
```bash
python scripts/utils/init_db.py
```

### 6. Buat Akun Admin
```bash
python scripts/utils/create_admin_simple.py
# Ikuti instruksi untuk bikin akun admin
# Default: username admin / password admin123
```

### 7. Jalankan Aplikasi
```bash
uvicorn app.main:app --reload

# Buka di browser:
# - Halaman Publik: http://localhost:8000
# - Login Admin: http://localhost:8000/admin/login
```

---

## Dokumentasi

Dokumentasi lengkap ada di folder `/docs`:
- Panduan Autentikasi
- Implementasi RBAC
- Dokumentasi API
- Panduan Deployment

---

## Keamanan

- Password di-hash pakai bcrypt
- Session management dengan encrypted cookies
- Role-based access control
- Proteksi SQL injection (SQLAlchemy)
- Proteksi XSS (Jinja2 auto-escaping)

**Penting**: Jangan lupa ganti password admin default setelah login pertama kali!

---

## Testing

```bash
# Jalankan tests
pytest

# Jalankan dengan coverage report
pytest --cov=app tests/
```

---

## Lisensi

Project ini menggunakan MIT License.

---

## Butuh Bantuan?

Kalau ada masalah, pertanyaan, atau saran:
- **GitHub Issues**: [Buat issue baru](https://github.com/reyzae/comparely-v1/issues)
- **Dokumentasi**: Cek folder `/docs`
