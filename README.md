# 📱 COMPARELY - Platform Perbandingan Perangkat

![CI Status](https://github.com/reyzae/comparely-v1/workflows/CI%20-%20COMPARELY/badge.svg)

Aplikasi web modern untuk membandingkan dan memberikan rekomendasi perangkat teknologi (smartphone & laptop) yang dibangun dengan **Python FastAPI** dan **rekomendasi berbasis AI**.

---

## ✨ Fitur Utama

### 🌐 Fitur Publik
- **Interface Web Modern**: Desain responsif dengan UI yang konsisten
- **Pencarian Perangkat**: Cari perangkat berdasarkan nama, brand, atau spesifikasi
- **Perbandingan Side-by-Side**: Bandingkan 2 perangkat secara detail
- **🤖 Perbandingan AI**: Analisis cerdas menggunakan xAI Grok
- **Rekomendasi Cerdas**: Dapatkan rekomendasi berdasarkan budget dan kebutuhan
- **🧠 Rekomendasi AI**: Saran personal berdasarkan use case Anda
- **Filter & Sort**: Filter berdasarkan kategori, brand, tahun, dan harga
- **Desain Responsif**: Optimal untuk desktop, tablet, dan mobile

### 🔐 Panel Admin
- **Dashboard Analytics**: Statistik lengkap dengan charts dan visualisasi
- **Manajemen Device**: Operasi CRUD lengkap dengan bulk actions
- **Manajemen Kategori**: Kelola kategori perangkat
- **Manajemen User**: Kelola users dan roles
- **Role-Based Access Control (RBAC)**: Role Super Admin, Admin, dan Viewer
- **Activity Logs**: Tracking semua aktivitas admin
- **CSV Import/Export**: Operasi data massal
- **Tools & Utilities**: Optimasi database dan manajemen cache

---

## 🛠️ Teknologi

**Backend**
- Python 3.11+ & FastAPI
- SQLAlchemy ORM
- Database SQLite/MySQL
- xAI Grok untuk fitur AI
- bcrypt untuk keamanan

**Frontend**
- Jinja2 Templates
- Vanilla CSS
- Responsive Design

---

## 🚀 Panduan Cepat

### 1. Clone Repository
```bash
git clone https://github.com/reyzae/comparely-v1.git
cd comparely-v1
```

### 2. Setup Virtual Environment
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

# Edit .env dan konfigurasi:
# - DATABASE_URL (SQLite secara default)
# - AI_API_KEY (opsional, untuk fitur AI)
# - SECRET_KEY (generate dengan: python -c "import secrets; print(secrets.token_urlsafe(32))")
```

### 5. Inisialisasi Database
```bash
python scripts/utils/init_db.py
```

### 6. Buat User Admin
```bash
python scripts/utils/create_admin_simple.py
# Ikuti prompt untuk membuat user admin
# Default: admin / admin123
```

### 7. Jalankan Aplikasi
```bash
uvicorn app.main:app --reload

# Aplikasi tersedia di:
# - Publik: http://localhost:8000
# - Admin: http://localhost:8000/admin/login
```

---

## 📚 Dokumentasi

Untuk dokumentasi lengkap, lihat folder `/docs`:
- Panduan Autentikasi
- Implementasi RBAC
- Dokumentasi API
- Panduan Deployment

---

## 🔒 Fitur Keamanan

- Bcrypt password hashing
- Manajemen session dengan encrypted cookies
- Role-based access control
- Pencegahan SQL injection (SQLAlchemy)
- Proteksi XSS (Jinja2 auto-escaping)

**⚠️ Penting**: Ganti password admin default setelah login pertama kali!

---

## 🧪 Testing

```bash
# Jalankan tests
pytest

# Jalankan dengan coverage
pytest --cov=app tests/
```
---

## 📄 Lisensi

Project ini dilisensikan di bawah MIT License.

---

## 📞 Dukungan

Untuk masalah, pertanyaan, atau saran:
- **GitHub Issues**: [Buat issue](https://github.com/reyzae/comparely-v1/issues)
- **Dokumentasi**: Cek folder `/docs`
