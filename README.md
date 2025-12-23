<<<<<<< HEAD
# 📱 COMPARELY - Aplikasi Perbandingan Perangkat Teknologi

![CI Status](https://github.com/reyzae/comparely/workflows/CI%20-%20COMPARELY/badge.svg)

Aplikasi web modern untuk membandingkan dan memberikan rekomendasi perangkat teknologi (smartphone & laptop) berbasis **Python FastAPI** dengan **Panel Admin** lengkap dan **Role-Based Access Control (RBAC)**.

---

## ✨ Fitur Utama

### 🌐 **Fitur Publik**
1. **Interface Web Modern**: Antarmuka responsif dengan design system yang konsisten
2. **Pencarian Perangkat**: Cari perangkat berdasarkan nama, brand, atau spesifikasi
3. **Perbandingan Detail**: Bandingkan 2 perangkat secara side-by-side
4. **🤖 Perbandingan AI**: Analisis perbandingan menggunakan xAI Grok
5. **Rekomendasi Cerdas**: Rekomendasi berdasarkan budget dan kebutuhan
6. **🧠 Rekomendasi AI**: Rekomendasi personal dari AI berdasarkan use case
7. **Filter & Sort**: Filter berdasarkan kategori, brand, tahun, dan harga
8. **Desain Responsif**: Optimal di desktop, tablet, dan mobile

### 🔐 **Fitur Panel Admin**
1. **Dashboard Analytics**: Statistik lengkap dengan charts dan visualisasi
2. **Manajemen Device**: Operasi CRUD untuk devices dengan bulk operations
3. **Manajemen Kategori**: Kelola kategori perangkat
4. **Manajemen User**: Kelola users dan roles
5. **Role-Based Access Control (RBAC)**: 
   - Super Admin: Akses penuh
   - Admin: Operasi CRUD
   - Viewer: Akses read-only
6. **Activity Logs**: Tracking semua aktivitas admin
7. **Bulk Operations**: Update multiple devices sekaligus
8. **CSV Import/Export**: Import data dari CSV, export ke CSV
9. **Tools & Utilities**: Optimasi database, pembersihan cache
10. **Manajemen Settings**: Konfigurasi aplikasi dan API

### 🔒 **Autentikasi & Keamanan**
- ✅ Password hashing yang aman (bcrypt)
- ✅ Manajemen session
- ✅ Permission berbasis role
- ✅ Protected admin routes
- ✅ Fitur ganti password
- ✅ User activity tracking

---

## 🛠️ Teknologi

### Backend
- **Python 3.11+**
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - ORM untuk database
- **Pydantic V2** - Validasi data
- **Uvicorn** - ASGI server
- **SQLite/MySQL** - Database (dapat dikonfigurasi)
- **xAI Grok** - Analisis & rekomendasi AI
- **bcrypt** - Password hashing
- **Passlib** - Password utilities

### Frontend
- **Jinja2** - Template engine
- **Vanilla CSS** - Custom design system
- **Font Awesome** - Icons
- **Google Fonts (Inter)** - Typography
- **Responsive Design** - Mobile-first approach

---

## 📁 Struktur Project

```
comparely/
├── app/
│   ├── core/              # Modul inti
│   │   ├── config.py      # Konfigurasi
│   │   ├── deps.py        # Dependencies
│   │   ├── rbac.py        # RBAC middleware
│   │   └── rbac_context.py # RBAC template helpers
│   ├── crud/              # Operasi CRUD
│   ├── models/            # SQLAlchemy models
│   │   ├── phone.py       # Model device
│   │   ├── category.py    # Model kategori
│   │   ├── user.py        # Model user
│   │   ├── role.py        # Model role
│   │   └── activity_log.py # Model activity log
│   ├── routers/           # API routes
│   │   ├── admin/         # Routes panel admin
│   │   │   ├── auth.py    # Autentikasi
│   │   │   ├── dashboard.py
│   │   │   ├── devices.py
│   │   │   ├── categories.py
│   │   │   ├── users.py
│   │   │   ├── analytics.py
│   │   │   ├── tools.py
│   │   │   ├── settings.py
│   │   │   ├── activity_logs.py
│   │   │   └── bulk_operations.py
│   │   ├── frontend.py    # Routes publik
│   │   ├── devices.py     # Device API
│   │   ├── compare.py     # Comparison API
│   │   ├── recommendation.py # Recommendation API
│   │   └── categories.py  # Category API
│   ├── services/          # Business logic
│   │   ├── comparison_service.py
│   │   ├── recommendation_service.py
│   │   └── ai_service.py  # Integrasi xAI Grok
│   ├── static/            # File statis
│   │   ├── css/          # Stylesheets
│   │   ├── js/           # JavaScript
│   │   └── images/       # Gambar & icons
│   ├── templates/         # Template Jinja2
│   │   ├── admin/        # Template panel admin
│   │   └── public/       # Template publik
│   ├── utils/            # Utilities
│   ├── database.py       # Koneksi database
│   └── main.py           # Entry point aplikasi
├── scripts/              # Utility scripts
│   ├── utils/           # Admin & DB utilities
│   │   ├── create_admin_simple.py
│   │   ├── reset_all_passwords.py
│   │   ├── create_sample_users.py
│   │   ├── reset_database.py
│   │   └── init_db.py
│   ├── import_csv.py    # Import CSV
│   ├── scrape_gsmarena.py # Scraping data
│   └── README.md        # Dokumentasi scripts
├── docs/                # Dokumentasi
│   ├── AUTHENTICATION.md    # Panduan sistem auth
│   ├── RBAC_GUIDE.md       # Implementasi RBAC
│   ├── RBAC_STATUS.md      # Status & contoh RBAC
│   ├── SECRET_KEY_SETUP.md # Setup keamanan
│   └── FINAL_SUMMARY.md    # Ringkasan lengkap
├── data/                # File data
├── tests/               # File testing
├── .env.example         # Template environment
├── .gitignore          # Aturan Git ignore
├── requirements.txt    # Dependencies Python
├── DEPLOYMENT_GUIDE.md # Panduan deployment
└── README.md           # File ini
```

---

## 🚀 Panduan Cepat

### 1. Clone Repository
```bash
git clone https://github.com/reyzae/comparely.git
cd comparely
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

### 7. Import Data Sample (Opsional)
```bash
python scripts/import_csv.py
```

### 8. Jalankan Aplikasi
```bash
uvicorn app.main:app --reload

# Aplikasi akan tersedia di:
# - Publik: http://localhost:8000
# - Admin: http://localhost:8000/admin/login
```

---

## 🔐 Kredensial Login Default

Setelah menjalankan `create_admin_simple.py`:

| Username | Password | Role | Level Akses |
|----------|----------|------|-------------|
| admin | admin123 | Super Admin | Akses penuh |

**⚠️ PENTING**: Ganti password default setelah login pertama kali!

---

## 📚 Dokumentasi

### Dokumentasi Inti
- **[AUTHENTICATION.md](docs/AUTHENTICATION.md)** - Panduan sistem autentikasi
- **[RBAC_GUIDE.md](docs/RBAC_GUIDE.md)** - Implementasi Role-Based Access Control
- **[RBAC_STATUS.md](docs/RBAC_STATUS.md)** - Status dan contoh RBAC
- **[SECRET_KEY_SETUP.md](docs/SECRET_KEY_SETUP.md)** - Konfigurasi keamanan
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Panduan deployment

### Dokumentasi Scripts
- **[scripts/README.md](scripts/README.md)** - Panduan utility scripts

---

## 🎯 Checklist Fitur

### ✅ Sudah Diimplementasikan
- [x] Backend FastAPI
- [x] SQLAlchemy ORM dengan dukungan SQLite/MySQL
- [x] Operasi CRUD Device
- [x] Manajemen kategori
- [x] Service perbandingan (rule-based + AI)
- [x] Engine rekomendasi (rule-based + AI)
- [x] Integrasi xAI Grok
- [x] Import/Export CSV
- [x] **Panel Admin Lengkap**
- [x] **Autentikasi User (bcrypt)**
- [x] **Role-Based Access Control (RBAC)**
- [x] **Manajemen Session**
- [x] **Activity Logging**
- [x] **Dashboard Analytics**
- [x] **Bulk Operations**
- [x] **Desain Responsif**
- [x] **UI/UX Modern**

### 🔄 Dalam Pengembangan
- [ ] Notifikasi email
- [ ] Filter lanjutan
- [ ] API rate limiting
- [ ] Caching layer

### 📋 Direncanakan
- [ ] Mobile app (React Native)
- [ ] Analytics lanjutan
- [ ] Dukungan multi-bahasa
- [ ] Dark mode

---

## 🔒 Fitur Keamanan

1. **Keamanan Password**
   - Bcrypt hashing (cost factor 12)
   - Validasi kekuatan password
   - Reset password yang aman

2. **Keamanan Session**
   - Session cookies terenkripsi
   - SECRET_KEY yang dapat dikonfigurasi
   - Session timeout

3. **Kontrol Akses**
   - Permission berbasis role
   - Proteksi route
   - Penyembunyian elemen UI berdasarkan role

4. **Proteksi Data**
   - Pencegahan SQL injection (SQLAlchemy)
   - Proteksi XSS (Jinja2 auto-escaping)
   - Proteksi CSRF (direkomendasikan untuk produksi)

---

## 🎨 Fitur Panel Admin

### Dashboard
- Statistik total devices, kategori, users
- Feed aktivitas terbaru
- Quick actions
- Charts dan visualisasi

### Manajemen Device
- List semua devices dengan pagination
- Search dan filter (kategori, brand, tahun)
- Create, edit, delete devices
- Bulk operations (update kategori, penyesuaian harga)
- Import/export CSV

### Manajemen User
- Kelola users dan roles
- Assign permissions
- Lihat aktivitas user
- Aktivasi/deaktivasi users

### Analytics
- Statistik device per kategori
- Charts distribusi harga
- Analisis brand
- Tren per tahun

### Tools
- Utility import CSV
- Optimasi database
- Manajemen cache
- Pengecekan kesehatan sistem

---

## 🌐 API Endpoints

### API Publik
- `GET /` - Homepage
- `GET /devices` - Daftar device
- `GET /devices/{id}` - Detail device
- `GET /search` - Pencarian devices
- `GET /compare` - Bandingkan devices
- `GET /api/compare` - API perbandingan (rule-based)
- `GET /api/compare/ai` - Perbandingan AI
- `GET /api/recommendation` - API rekomendasi
- `GET /api/recommendation/ai` - Rekomendasi AI

### API Admin
- `GET /admin/login` - Halaman login
- `POST /admin/login` - Handler login
- `GET /admin/logout` - Logout
- `GET /admin/dashboard` - Dashboard
- `GET /admin/devices` - Manajemen device
- `GET /admin/users` - Manajemen user
- `GET /admin/analytics` - Analytics
- ... dan lainnya

Lihat dokumentasi API lengkap di komentar kode.

---

## 🧪 Testing

```bash
# Jalankan tests
pytest

# Jalankan dengan coverage
pytest --cov=app tests/

# Jalankan test spesifik
pytest tests/test_basic.py
```

---

## 📦 Deployment

Lihat **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** untuk panduan deployment lengkap.

### Quick Deploy (Production)

1. **Set environment variables**:
```bash
export DATABASE_URL="mysql://user:pass@host/dbname"
export SECRET_KEY="your-secure-random-key"
export AI_API_KEY="your-xai-api-key"
```

2. **Jalankan dengan Gunicorn**:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

3. **Atau gunakan Docker** (jika Dockerfile tersedia):
```bash
docker build -t comparely .
docker run -p 8000:8000 comparely
```

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:

1. Fork repository
2. Buat feature branch (`git checkout -b feature/FiturKeren`)
3. Commit perubahan (`git commit -m 'Tambah fitur keren'`)
4. Push ke branch (`git push origin feature/FiturKeren`)
5. Buat Pull Request

---

## 📄 Lisensi

Project ini dilisensikan di bawah MIT License - lihat file LICENSE untuk detail.

---

## 👥 Tim

- **Developer**: Reyza
- **Project**: COMPARELY - Platform Perbandingan Perangkat
- **Institusi**: [Institusi Anda]
- **Tahun**: 2024-2025

---

## 📞 Dukungan

Untuk masalah, pertanyaan, atau saran:
- **GitHub Issues**: [Buat issue](https://github.com/reyzae/comparely/issues)
- **Email**: [Email Anda]
- **Dokumentasi**: Cek folder `/docs`

---

## 🙏 Acknowledgments

- **FastAPI** - Modern web framework
- **SQLAlchemy** - Database ORM
- **xAI Grok** - Integrasi AI
- **Font Awesome** - Icons
- **Google Fonts** - Typography

---

## 📊 Statistik Project

- **Baris Kode**: 15,000+
- **File**: 100+
- **Fitur**: 30+
- **Halaman Dokumentasi**: 10+
- **Test Coverage**: Berkembang

---

**Dibuat dengan ❤️ menggunakan Python & FastAPI**
=======
# comparely-v1
Comparely v1.0
>>>>>>> 61dd9ce4acd5a5039962e2b4ccb3cd799b6b1069
