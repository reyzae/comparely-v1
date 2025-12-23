# 📱 MATERI PRESENTASI COMPARELY
## Aplikasi Perbandingan Perangkat Teknologi

---

## 📋 DAFTAR ISI

1. [Pendahuluan](#1-pendahuluan)
2. [Arsitektur Sistem](#2-arsitektur-sistem)
3. [Teknologi yang Digunakan](#3-teknologi-yang-digunakan)
4. [Struktur Database](#4-struktur-database)
5. [Fitur-Fitur Utama](#5-fitur-fitur-utama)
6. [Penjelasan Source Code](#6-penjelasan-source-code)
7. [Alur Kerja Aplikasi](#7-alur-kerja-aplikasi)
8. [Integrasi AI](#8-integrasi-ai)
9. [Cara Menjalankan](#9-cara-menjalankan)
10. [Demo dan Screenshot](#10-demo-dan-screenshot)

---

## 1. PENDAHULUAN

### 1.1 Latar Belakang
COMPARELY adalah aplikasi web yang dirancang untuk membantu pengguna dalam membandingkan perangkat teknologi (smartphone dan laptop) secara objektif dan mendalam. Aplikasi ini menggabungkan analisis berbasis aturan (rule-based) dengan kecerdasan buatan (AI) untuk memberikan rekomendasi yang akurat.

### 1.2 Tujuan Proyek
- Memudahkan pengguna dalam membandingkan spesifikasi perangkat
- Memberikan rekomendasi perangkat berdasarkan budget dan kebutuhan
- Memanfaatkan AI untuk analisis yang lebih mendalam
- Menyediakan interface yang user-friendly dan responsif

### 1.3 Tim Pengembang
- **Ketua**: Reyza Wirakusuma [17250107]
- **Anggota**:
  - Rachmat Muhaimin Rustam [17250381]
  - Tegar Apdiansyah [17250651]
  - Abdul Khair [17250610]
  - Rofik Rokhmattullah [17250705]

---

## 2. ARSITEKTUR SISTEM

### 2.1 Pola Arsitektur
COMPARELY menggunakan arsitektur **Layered Architecture** dengan pemisahan yang jelas:

```
┌─────────────────────────────────────┐
│         PRESENTATION LAYER          │
│    (Templates HTML + CSS + JS)      │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│          ROUTER LAYER               │
│   (FastAPI Routers - Endpoints)     │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│         SERVICE LAYER               │
│  (Business Logic & AI Integration)  │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│           CRUD LAYER                │
│    (Database Operations)            │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│          MODEL LAYER                │
│    (SQLAlchemy Models)              │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│         DATABASE LAYER              │
│          (MySQL)                    │
└─────────────────────────────────────┘
```

### 2.2 Komponen Utama

#### A. Frontend (Presentation Layer)
- **Lokasi**: `app/templates/` dan `app/static/`
- **Teknologi**: HTML5, CSS3, Vanilla JavaScript, Jinja2
- **File Utama**:
  - `index.html` - Homepage
  - `devices.html` - Daftar perangkat
  - `compare.html` - Halaman perbandingan
  - `device_detail.html` - Detail perangkat
  - `base.html` - Template dasar

#### B. Backend (API Layer)
- **Lokasi**: `app/main.py` dan `app/routers/`
- **Teknologi**: FastAPI, Uvicorn
- **Routers**:
  - `frontend.py` - Routing halaman web
  - `devices.py` - API perangkat
  - `compare.py` - API perbandingan
  - `recommendation.py` - API rekomendasi
  - `categories.py` - API kategori

#### C. Business Logic (Service Layer)
- **Lokasi**: `app/services/`
- **Services**:
  - `comparison_service.py` - Logika perbandingan
  - `recommendation_service.py` - Logika rekomendasi
  - `grok_service.py` - Integrasi AI

#### D. Data Access (CRUD Layer)
- **Lokasi**: `app/crud/`
- **CRUD Operations**:
  - `device.py` - CRUD perangkat
  - `category.py` - CRUD kategori
  - `benchmark.py` - CRUD benchmark

#### E. Database Models
- **Lokasi**: `app/models/`
- **Models**:
  - `device.py` - Model Device
  - `category.py` - Model Category
  - `benchmark.py` - Model Benchmark

---

## 3. TEKNOLOGI YANG DIGUNAKAN

### 3.1 Backend Technologies

#### FastAPI
- **Versi**: Latest
- **Alasan Pemilihan**:
  - Performance tinggi (setara dengan NodeJS dan Go)
  - Auto-generated documentation (Swagger UI)
  - Type hints dan validasi otomatis
  - Async support untuk operasi I/O

#### SQLAlchemy
- **Fungsi**: ORM (Object-Relational Mapping)
- **Keuntungan**:
  - Abstraksi database yang powerful
  - Query yang type-safe
  - Relationship management otomatis
  - Migration support

#### Pydantic
- **Fungsi**: Data validation dan serialization
- **Keuntungan**:
  - Validasi data otomatis
  - Type checking
  - JSON serialization/deserialization
  - Error handling yang jelas

#### MySQL
- **Fungsi**: Relational Database
- **Alasan Pemilihan**:
  - Reliable dan mature
  - Support untuk complex queries
  - ACID compliance
  - Scalable untuk production

### 3.2 Frontend Technologies

#### Jinja2
- **Fungsi**: Template Engine
- **Fitur yang Digunakan**:
  - Template inheritance (`{% extends %}`)
  - Variable rendering (`{{ variable }}`)
  - Control structures (`{% for %}`, `{% if %}`)
  - Filters dan functions

#### Vanilla CSS
- **Pendekatan**: Custom Design System
- **Fitur**:
  - CSS Variables untuk theming
  - Flexbox dan Grid layout
  - Responsive design dengan media queries
  - Gradient backgrounds
  - Smooth animations

### 3.3 External Services

#### AI API (xAI)
- **Model**: grok-4-1-fast-reasoning
- **Fungsi**:
  - Analisis perbandingan mendalam
  - Rekomendasi personal
  - Natural language processing

---

## 4. STRUKTUR DATABASE

### 4.1 Entity Relationship Diagram

```
┌─────────────────────┐
│     categories      │
├─────────────────────┤
│ id (PK)            │
│ name               │
│ description        │
└─────────────────────┘
          │
          │ 1:N
          ↓
┌─────────────────────┐
│      devices        │
├─────────────────────┤
│ id (PK)            │
│ name               │
│ brand              │
│ category_id (FK)   │
│ cpu                │
│ gpu                │
│ ram                │
│ storage            │
│ camera             │
│ battery            │
│ screen             │
│ release_year       │
│ price              │
│ image_url          │
│ description        │
└─────────────────────┘
          │
          │ 1:1
          ↓
┌─────────────────────┐
│     benchmarks      │
├─────────────────────┤
│ id (PK)            │
│ device_id (FK)     │
│ cpu_score          │
│ gpu_score          │
│ battery_score      │
│ camera_score       │
└─────────────────────┘
```

### 4.2 Penjelasan Tabel

#### Tabel: categories
```sql
CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT
);
```
- **Fungsi**: Menyimpan kategori perangkat (Smartphone, Laptop, dll)
- **Relasi**: One-to-Many dengan devices

#### Tabel: devices
```sql
CREATE TABLE devices (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(100) NOT NULL,
    category_id INT,
    cpu VARCHAR(255),
    gpu VARCHAR(255),
    ram VARCHAR(100),
    storage VARCHAR(100),
    camera VARCHAR(255),
    battery VARCHAR(100),
    screen VARCHAR(255),
    release_year INT,
    price DECIMAL(15,2),
    image_url VARCHAR(500),
    description TEXT,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```
- **Fungsi**: Menyimpan data lengkap perangkat
- **Field Penting**:
  - `name`: Nama perangkat (contoh: "iPhone 15 Pro")
  - `brand`: Merek (contoh: "Apple")
  - `category_id`: Referensi ke kategori
  - `price`: Harga dalam Rupiah (DECIMAL untuk presisi)
  - Spesifikasi: cpu, gpu, ram, storage, camera, battery, screen

#### Tabel: benchmarks
```sql
CREATE TABLE benchmarks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    device_id INT UNIQUE,
    cpu_score INT,
    gpu_score INT,
    battery_score INT,
    camera_score INT,
    FOREIGN KEY (device_id) REFERENCES devices(id)
);
```
- **Fungsi**: Menyimpan skor benchmark perangkat
- **Relasi**: One-to-One dengan devices

---

## 5. FITUR-FITUR UTAMA

### 5.1 Pencarian Perangkat
**Endpoint**: `GET /devices/search?query={keyword}`

**Cara Kerja**:
1. User memasukkan keyword di search bar
2. Backend melakukan query ke database dengan LIKE pattern
3. Mencari di field `name` dan `brand`
4. Mengembalikan list perangkat yang cocok

**Contoh Query SQL**:
```sql
SELECT * FROM devices 
WHERE name LIKE '%iPhone%' 
   OR brand LIKE '%Apple%';
```

### 5.2 Perbandingan Perangkat (Rule-Based)
**Endpoint**: `POST /compare/`

**Input**:
```json
{
  "device_id_1": 1,
  "device_id_2": 2
}
```

**Proses**:
1. Ambil data kedua device dari database
2. Bandingkan spesifikasi:
   - Harga (lebih murah = keunggulan)
   - Tahun rilis (lebih baru = keunggulan)
3. Generate highlights

**Output**:
```json
{
  "device_1": {...},
  "device_2": {...},
  "highlights": [
    "iPhone 15 Pro lebih murah Rp 2,000,000",
    "Samsung Galaxy S24 lebih baru (Rilis 2024)"
  ]
}
```

### 5.3 Perbandingan dengan AI
**Endpoint**: `POST /compare/ai`

**Proses**:
1. Jalankan perbandingan rule-based terlebih dahulu
2. Kirim data ke AI API dengan prompt terstruktur
3. AI menganalisis:
   - Performa (CPU, GPU, RAM)
   - Kualitas kamera
   - Daya tahan baterai
   - Value for money
4. AI memberikan rekomendasi personal

**Contoh Prompt ke AI**:
```
Bandingkan 2 perangkat berikut:

Device 1: iPhone 15 Pro
- CPU: A17 Pro
- RAM: 8GB
- Harga: Rp 12,000,000

Device 2: Samsung Galaxy S24
- CPU: Snapdragon 8 Gen 3
- RAM: 8GB
- Harga: Rp 11,000,000

Berikan analisis dalam format JSON...
```

### 5.4 Rekomendasi Perangkat (Rule-Based)
**Endpoint**: `GET /recommendation/`

**Parameter**:
- `max_price`: Budget maksimal
- `category_id`: Kategori (1=Smartphone, 2=Laptop)
- `min_release_year`: Tahun rilis minimal
- `limit`: Jumlah hasil (default: 5)

**Algoritma**:
1. Filter berdasarkan parameter
2. Sort berdasarkan:
   - Tahun rilis (DESC) - prioritas perangkat terbaru
   - Harga (ASC) - prioritas harga murah
3. Limit hasil

**Contoh Query**:
```sql
SELECT * FROM devices
WHERE price <= 10000000
  AND category_id = 1
  AND release_year >= 2023
ORDER BY release_year DESC, price ASC
LIMIT 5;
```

### 5.5 Rekomendasi dengan AI
**Endpoint**: `POST /recommendation/ai`

**Input**:
```json
{
  "max_price": 10000000,
  "category_id": 1,
  "use_case": "gaming dan fotografi"
}
```

**Proses**:
1. Ambil top 3 devices dari rekomendasi rule-based
2. Kirim ke AI dengan use case user
3. AI melakukan ranking berdasarkan use case
4. AI memberikan penjelasan untuk setiap rekomendasi

### 5.6 Import Data CSV
**Script**: `import_csv.py`

**Format CSV**:
```csv
name,brand,category_id,cpu,gpu,ram,storage,camera,battery,screen,release_year,price,image_url,source_data
iPhone 15 Pro,Apple,1,A17 Pro,Apple GPU,8GB,256GB,48MP,3274 mAh,6.1" OLED,2023,12000000,https://...,GSMArena
```

**Fitur**:
- Validasi field wajib
- Konversi tipe data otomatis
- Handle missing values
- Skip duplicate entries
- Summary report

---

## 6. PENJELASAN SOURCE CODE

### 6.1 File: `app/main.py`
**Fungsi**: Entry point aplikasi FastAPI

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import devices, compare, categories, recommendation, frontend
from .database import engine
from .models import Base

# Load environment variables
load_dotenv()

# Membuat tabel database otomatis
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="COMPARELY",
    description="Aplikasi Perbandingan Perangkat",
    version="1.0.0"
)
```

**Penjelasan**:
- `Base.metadata.create_all()`: Membuat semua tabel di database secara otomatis berdasarkan models
- `FastAPI()`: Inisialisasi aplikasi dengan metadata untuk dokumentasi
- `app.mount("/static", ...)`: Mount folder static untuk CSS/JS/Images

**Startup Event**:
```python
@app.on_event("startup")
async def startup_event():
    # Validasi AI_API_KEY
    ai_api_key = os.getenv("AI_API_KEY", "")
    if not ai_api_key:
        print("⚠️  WARNING: AI_API_KEY tidak ditemukan!")
```
- Mengecek konfigurasi saat aplikasi start
- Memberikan warning jika API key tidak ada

### 6.2 File: `app/database.py`
**Fungsi**: Konfigurasi koneksi database

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .core.config import DATABASE_URL

# Create engine untuk koneksi ke database
engine = create_engine(DATABASE_URL)

# SessionLocal: factory untuk membuat database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class untuk semua models
Base = declarative_base()
```

**Penjelasan**:
- `create_engine()`: Membuat koneksi pool ke MySQL
- `SessionLocal`: Factory untuk membuat session database
- `Base`: Base class yang akan di-inherit oleh semua models

### 6.3 File: `app/models/device.py`
**Fungsi**: Model SQLAlchemy untuk tabel devices

```python
class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    brand = Column(String(100), index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    # Spesifikasi
    cpu = Column(String(255))
    gpu = Column(String(255))
    ram = Column(String(100))
    storage = Column(String(100))
    camera = Column(String(255))
    battery = Column(String(100))
    screen = Column(String(255))
    
    # Info tambahan
    release_year = Column(Integer)
    price = Column(DECIMAL(15, 2))
    image_url = Column(String(500))
    description = Column(Text)
    
    # Relationships
    category = relationship("Category", back_populates="devices")
    benchmark = relationship("Benchmark", back_populates="device", uselist=False)
```

**Penjelasan**:
- `__tablename__`: Nama tabel di database
- `Column()`: Definisi kolom dengan tipe data
- `ForeignKey()`: Relasi ke tabel lain
- `relationship()`: ORM relationship untuk join otomatis
- `index=True`: Membuat index untuk query lebih cepat

### 6.4 File: `app/crud/device.py`
**Fungsi**: CRUD operations untuk Device

```python
def get_device(db: Session, device_id: int):
    """Ambil 1 device berdasarkan ID"""
    return db.query(models.Device).filter(models.Device.id == device_id).first()

def get_devices(db: Session, skip: int = 0, limit: int = 100):
    """Ambil list devices dengan pagination"""
    return db.query(models.Device).offset(skip).limit(limit).all()

def search_devices(db: Session, query: str):
    """Cari devices berdasarkan nama atau brand"""
    search_pattern = f"%{query}%"
    return db.query(models.Device).filter(
        (models.Device.name.like(search_pattern)) |
        (models.Device.brand.like(search_pattern))
    ).all()
```

**Penjelasan**:
- `db.query()`: Membuat query SQLAlchemy
- `.filter()`: WHERE clause
- `.first()`: Ambil 1 hasil
- `.all()`: Ambil semua hasil
- `like()`: Pattern matching untuk search

### 6.5 File: `app/services/comparison_service.py`
**Fungsi**: Business logic untuk perbandingan

```python
def compare_two_devices(db: Session, device_id_1: int, device_id_2: int):
    # Ambil data kedua device
    device1 = device_crud.get_device(db, device_id_1)
    device2 = device_crud.get_device(db, device_id_2)
    
    # Validasi
    if not device1 or not device2:
        raise ValueError("Device tidak ditemukan")
    
    # Generate highlights
    highlights = generate_highlights(device1, device2)
    
    return {
        "device_1": device1,
        "device_2": device2,
        "highlights": highlights
    }

def generate_highlights(device1, device2):
    highlights = []
    
    # Bandingkan harga
    if device1.price < device2.price:
        price_diff = device2.price - device1.price
        highlights.append(f"{device1.name} lebih murah Rp {price_diff:,.0f}")
    
    # Bandingkan tahun rilis
    if device1.release_year > device2.release_year:
        highlights.append(f"{device1.name} lebih baru (Rilis {device1.release_year})")
    
    return highlights
```

**Penjelasan**:
- Separation of concerns: CRUD di layer terpisah
- Business logic di service layer
- Error handling dengan exception
- Return format yang konsisten

### 6.6 File: `app/services/grok_service.py`
**Fungsi**: Integrasi dengan AI API

```python
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_API_URL = "https://api.x.ai/v1/chat/completions"
AI_MODEL = "grok-4-1-fast-reasoning"

def call_ai_api(messages: List[Dict], temperature: float = 0.7):
    """Helper function untuk call AI API"""
    
    if not AI_API_KEY:
        return "AI API key tidak tersedia"
    
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": AI_MODEL,
        "messages": messages,
        "temperature": temperature
    }
    
    response = requests.post(AI_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"AI API Error: {response.status_code}")
```

**Penjelasan**:
- Environment variable untuk API key (security)
- HTTP request ke AI API
- Error handling untuk API failures
- Temperature control untuk kreativitas AI

**Fungsi AI Comparison**:
```python
def get_comparison_analysis(device1, device2):
    """Analisis perbandingan dengan AI"""
    
    prompt = f"""
    Bandingkan 2 perangkat berikut dan berikan analisis dalam format JSON:
    
    Device 1: {device1.name}
    - CPU: {device1.cpu}
    - GPU: {device1.gpu}
    - RAM: {device1.ram}
    - Kamera: {device1.camera}
    - Baterai: {device1.battery}
    - Harga: Rp {device1.price:,.0f}
    
    Device 2: {device2.name}
    - CPU: {device2.cpu}
    - GPU: {device2.gpu}
    - RAM: {device2.ram}
    - Kamera: {device2.camera}
    - Baterai: {device2.battery}
    - Harga: Rp {device2.price:,.0f}
    
    Format JSON:
    {{
      "performa": "analisis performa...",
      "kamera": "analisis kamera...",
      "baterai": "analisis baterai...",
      "value_for_money": "analisis harga...",
      "rekomendasi": "device mana yang lebih baik dan untuk siapa"
    }}
    """
    
    messages = [
        {"role": "system", "content": "Kamu adalah ahli teknologi yang membantu perbandingan perangkat."},
        {"role": "user", "content": prompt}
    ]
    
    return call_ai_api(messages)
```

### 6.7 File: `app/routers/frontend.py`
**Fungsi**: Routing untuk halaman web

```python
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request, db: Session = Depends(get_db)):
    """Homepage COMPARELY"""
    
    # Ambil 2 device terbaru untuk example comparison
    latest_devices = db.query(models.Device)\
        .order_by(models.Device.release_year.desc())\
        .limit(2)\
        .all()
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "devices": latest_devices
    })
```

**Penjelasan**:
- `@router.get("/")`: Decorator untuk routing
- `response_class=HTMLResponse`: Return HTML
- `Depends(get_db)`: Dependency injection untuk database session
- `templates.TemplateResponse()`: Render Jinja2 template

**Halaman Perbandingan**:
```python
@router.get("/compare-page", response_class=HTMLResponse)
async def compare_page(
    request: Request,
    id1: int,
    id2: int,
    db: Session = Depends(get_db)
):
    """Halaman perbandingan 2 device"""
    
    # Ambil data devices
    device1 = device_crud.get_device(db, id1)
    device2 = device_crud.get_device(db, id2)
    
    if not device1 or not device2:
        return RedirectResponse(url="/devices")
    
    # Generate comparison
    comparison = comparison_service.compare_two_devices(db, id1, id2)
    
    return templates.TemplateResponse("compare.html", {
        "request": request,
        "device1": device1,
        "device2": device2,
        "highlights": comparison["highlights"]
    })
```

### 6.8 File: `app/routers/compare.py`
**Fungsi**: API endpoints untuk perbandingan

```python
@router.post("/", response_model=schemas.ComparisonResponse)
def compare_devices(
    comparison: schemas.ComparisonRequest,
    db: Session = Depends(get_db)
):
    """API endpoint untuk perbandingan rule-based"""
    
    try:
        result = comparison_service.compare_two_devices(
            db,
            comparison.device_id_1,
            comparison.device_id_2
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/ai", response_model=schemas.AIComparisonResponse)
def compare_devices_ai(
    comparison: schemas.ComparisonRequest,
    db: Session = Depends(get_db)
):
    """API endpoint untuk perbandingan dengan AI"""
    
    # Jalankan comparison biasa dulu
    base_comparison = comparison_service.compare_two_devices(
        db,
        comparison.device_id_1,
        comparison.device_id_2
    )
    
    # Dapatkan AI analysis
    try:
        ai_analysis = grok_service.get_comparison_analysis(
            base_comparison["device_1"],
            base_comparison["device_2"]
        )
    except Exception as e:
        ai_analysis = "AI analysis tidak tersedia"
    
    return {
        **base_comparison,
        "ai_analysis": ai_analysis
    }
```

**Penjelasan**:
- `response_model`: Pydantic schema untuk validasi output
- `Depends(get_db)`: Dependency injection
- Try-except untuk error handling
- Fallback jika AI tidak tersedia

---

## 7. ALUR KERJA APLIKASI

### 7.1 Flow: User Mencari Perangkat

```
1. User buka homepage (/)
   ↓
2. User ketik keyword di search bar (contoh: "iPhone")
   ↓
3. Form submit ke /search?query=iPhone
   ↓
4. Router frontend.py → search_devices()
   ↓
5. Call device_crud.search_devices(db, "iPhone")
   ↓
6. Query database:
   SELECT * FROM devices 
   WHERE name LIKE '%iPhone%' OR brand LIKE '%iPhone%'
   ↓
7. Return hasil ke template search_results.html
   ↓
8. User melihat list perangkat yang cocok
```

### 7.2 Flow: User Membandingkan 2 Perangkat

```
1. User pilih 2 device di halaman /devices
   ↓
2. Klik tombol "Compare"
   ↓
3. Redirect ke /compare-page?id1=1&id2=2
   ↓
4. Router frontend.py → compare_page()
   ↓
5. Call comparison_service.compare_two_devices(db, 1, 2)
   ↓
6. Service layer:
   - Ambil device1 dari database
   - Ambil device2 dari database
   - Generate highlights (bandingkan harga, tahun rilis)
   ↓
7. Return data ke template compare.html
   ↓
8. User melihat perbandingan:
   - Spesifikasi side-by-side
   - Highlights keunggulan masing-masing
   - Tombol "Get AI Analysis"
```

### 7.3 Flow: User Request AI Analysis

```
1. User klik "Get AI Analysis" di halaman compare
   ↓
2. JavaScript fetch ke /compare/ai
   ↓
3. Router compare.py → compare_devices_ai()
   ↓
4. Jalankan comparison biasa (rule-based)
   ↓
5. Call grok_service.get_comparison_analysis()
   ↓
6. Grok Service:
   - Prepare prompt dengan spesifikasi lengkap
   - Call AI API (POST https://api.x.ai/v1/chat/completions)
   - Parse JSON response
   ↓
7. AI mengembalikan analisis:
   {
     "performa": "iPhone 15 Pro unggul dengan A17 Pro...",
     "kamera": "Kedua device setara di 48MP...",
     "baterai": "Samsung lebih besar 4000 mAh vs 3274 mAh...",
     "value_for_money": "Samsung lebih worth it...",
     "rekomendasi": "Pilih iPhone untuk ekosistem Apple..."
   }
   ↓
8. Return ke frontend
   ↓
9. JavaScript render AI analysis di halaman
```

### 7.4 Flow: User Minta Rekomendasi

```
1. User akses halaman recommendation
   ↓
2. User input:
   - Budget: Rp 10,000,000
   - Kategori: Smartphone
   - Use case: "gaming dan fotografi"
   ↓
3. Submit form ke /recommendation/ai
   ↓
4. Router recommendation.py → get_ai_recommendation()
   ↓
5. Call recommendation_service.get_recommendations()
   - Filter: price <= 10,000,000
   - Filter: category_id = 1
   - Sort: release_year DESC, price ASC
   - Limit: 3
   ↓
6. Dapat top 3 devices dari database
   ↓
7. Call grok_service.get_ai_recommendation()
   - Kirim list devices + use case ke AI
   - AI ranking berdasarkan use case
   ↓
8. AI response:
   {
     "top_1": {
       "device": "Samsung Galaxy S24",
       "reason": "Snapdragon 8 Gen 3 terbaik untuk gaming..."
     },
     "top_2": {...},
     "top_3": {...},
     "summary": "Untuk gaming dan fotografi, prioritaskan GPU..."
   }
   ↓
9. Return ke frontend
   ↓
10. User melihat ranking dengan penjelasan AI
```

### 7.5 Flow: Import Data CSV

```
1. Admin jalankan: python import_csv.py data/devices.csv
   ↓
2. Script baca CSV dengan pandas
   ↓
3. Untuk setiap row:
   a. Validasi field wajib (name, brand, category_id, price)
   b. Konversi tipe data (price → Decimal, release_year → int)
   c. Handle missing values (default "N/A")
   ↓
4. Cek apakah category_id exists
   - Jika tidak: create category baru
   ↓
5. Cek duplicate (nama + brand sama)
   - Jika duplicate: skip row
   ↓
6. Insert device ke database
   ↓
7. Commit transaction
   ↓
8. Print summary:
   ✅ Total processed: 50
   ✅ Success: 48
   ⚠️  Skipped (duplicate): 2
```

---

## 8. INTEGRASI AI

### 8.1 Mengapa Menggunakan AI?

**Keterbatasan Rule-Based**:
- Hanya bisa bandingkan angka (harga, tahun rilis)
- Tidak bisa analisis konteks (use case user)
- Tidak bisa pertimbangan subjektif (value for money)

**Keunggulan AI**:
- Analisis mendalam berdasarkan spesifikasi
- Pertimbangan use case user
- Rekomendasi personal
- Natural language explanation

### 8.2 AI Model yang Digunakan

**Model**: `grok-4-1-fast-reasoning`
- Provider: xAI (X.AI)
- Kecepatan: Fast inference
- Kemampuan: Reasoning dan analysis

### 8.3 Prompt Engineering

**Prinsip Prompt yang Baik**:
1. **Clear Instructions**: Jelaskan apa yang diinginkan
2. **Structured Output**: Minta format JSON untuk parsing mudah
3. **Context**: Berikan semua informasi yang relevan
4. **Examples**: Berikan contoh output yang diharapkan

**Contoh Prompt Comparison**:
```
System: Kamu adalah ahli teknologi yang membantu perbandingan perangkat.

User: Bandingkan 2 perangkat berikut dan berikan analisis dalam format JSON.

Device 1: iPhone 15 Pro
- CPU: A17 Pro (3nm, 6-core)
- GPU: Apple GPU 6-core
- RAM: 8GB
- Storage: 256GB
- Kamera: 48MP Main + 12MP Ultra Wide + 12MP Telephoto
- Baterai: 3274 mAh
- Layar: 6.1" OLED 120Hz
- Harga: Rp 12,000,000

Device 2: Samsung Galaxy S24
- CPU: Snapdragon 8 Gen 3 (4nm, 8-core)
- GPU: Adreno 750
- RAM: 8GB
- Storage: 256GB
- Kamera: 50MP Main + 12MP Ultra Wide + 10MP Telephoto
- Baterai: 4000 mAh
- Layar: 6.2" AMOLED 120Hz
- Harga: Rp 11,000,000

Berikan analisis dalam format JSON berikut:
{
  "performa": "Analisis CPU, GPU, RAM untuk gaming, multitasking, dll",
  "kamera": "Analisis kualitas foto, video, fitur kamera",
  "baterai": "Analisis daya tahan baterai",
  "value_for_money": "Analisis harga vs fitur yang didapat",
  "rekomendasi": "Device mana yang lebih baik dan untuk siapa"
}

Gunakan bahasa Indonesia yang mudah dipahami.
```

### 8.4 Error Handling untuk AI

**Skenario Error**:
1. API key tidak valid
2. Network timeout
3. AI API down
4. Rate limit exceeded
5. Invalid JSON response

**Strategi Handling**:
```python
def get_comparison_analysis(device1, device2):
    try:
        # Call AI API
        response = call_ai_api(messages)
        
        # Parse JSON
        analysis = json.loads(response)
        
        return analysis
        
    except requests.exceptions.Timeout:
        return "AI sedang sibuk, coba lagi nanti"
        
    except requests.exceptions.RequestException as e:
        return f"Koneksi ke AI gagal: {str(e)}"
        
    except json.JSONDecodeError:
        return "AI response tidak valid"
        
    except Exception as e:
        return f"Error: {str(e)}"
```

**Fallback Strategy**:
- Jika AI gagal, tetap tampilkan comparison rule-based
- User tetap dapat informasi dasar
- Aplikasi tidak crash

---

## 9. CARA MENJALANKAN

### 9.1 Prerequisites

**Software yang Dibutuhkan**:
1. Python 3.11 atau lebih baru
2. MySQL 8.0 atau lebih baru
3. Git (untuk clone repository)
4. Text editor (VS Code recommended)

### 9.2 Langkah-Langkah Setup

#### Step 1: Clone Repository
```bash
git clone https://github.com/reyzae/comparely.git
cd comparely
```

#### Step 2: Buat Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

**Mengapa Virtual Environment?**
- Isolasi dependencies
- Tidak conflict dengan project lain
- Reproducible environment

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies yang Terinstall**:
- fastapi
- uvicorn[standard]
- sqlalchemy
- mysql-connector-python
- pydantic
- pydantic-settings
- python-dotenv
- requests
- jinja2

#### Step 4: Setup Database
```bash
# Buat database MySQL
mysql -u root -p
```

```sql
CREATE DATABASE comparely;
EXIT;
```

#### Step 5: Konfigurasi Environment
```bash
# Copy .env.example ke .env
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Edit `.env`:
```env
DATABASE_URL=mysql+mysqlconnector://root:password@localhost/comparely
AI_API_KEY=your_ai_api_key_here
```

**Cara Mendapatkan AI API Key**:
1. Buka https://console.x.ai/
2. Sign up / Login
3. Buat API key baru
4. Copy dan paste ke .env

#### Step 6: Inisialisasi Database
```bash
python init_db.py
```

**Apa yang Terjadi**:
- Membuat semua tabel (devices, categories, benchmarks)
- Membuat kategori default (Smartphone, Laptop)

#### Step 7: Import Sample Data (Optional)
```bash
python import_csv.py data/devices.csv
```

#### Step 8: Jalankan Server
```bash
uvicorn app.main:app --reload
```

**Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.

============================================================
🚀 COMPARELY - Aplikasi Perbandingan Perangkat
============================================================
✅ AI_API_KEY terdeteksi - Fitur AI aktif
✅ DATABASE_URL terdeteksi
============================================================
```

#### Step 9: Akses Aplikasi

**Web Interface**:
- Homepage: http://localhost:8000
- Devices: http://localhost:8000/devices
- Features: http://localhost:8000/features
- About: http://localhost:8000/about

**API Documentation**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 9.3 Testing

#### Manual Testing
1. Buka http://localhost:8000
2. Coba search perangkat
3. Pilih 2 device untuk compare
4. Klik "Get AI Analysis"
5. Coba recommendation dengan use case

#### API Testing dengan Swagger
1. Buka http://localhost:8000/docs
2. Expand endpoint yang ingin ditest
3. Klik "Try it out"
4. Input parameter
5. Klik "Execute"
6. Lihat response

---

## 10. DEMO DAN SCREENSHOT

### 10.1 Homepage
**Fitur**:
- Hero section dengan gradient background
- Search bar untuk quick search
- Example comparison dari 2 device terbaru
- Call-to-action buttons

**Teknologi**:
- Jinja2 template: `index.html`
- CSS: Gradient cyan-teal, glassmorphism effect
- JavaScript: Search form handling

### 10.2 Halaman Devices
**Fitur**:
- Grid layout untuk semua devices
- Filter berdasarkan kategori dan harga
- Checkbox untuk select 2 devices
- Tombol "Compare Selected"

**Teknologi**:
- CSS Grid untuk responsive layout
- JavaScript untuk checkbox logic
- Query parameters untuk filtering

### 10.3 Halaman Comparison
**Fitur**:
- Side-by-side comparison
- Spesifikasi lengkap kedua device
- Highlights keunggulan
- Tombol "Get AI Analysis"
- Modal untuk AI analysis

**Teknologi**:
- Flexbox untuk 2-column layout
- Fetch API untuk AJAX request
- Modal dengan CSS animation

### 10.4 Halaman Detail Device
**Fitur**:
- Hero image perangkat
- Spesifikasi lengkap dalam card
- Harga dan tahun rilis
- Tombol "Compare with..."

### 10.5 API Documentation (Swagger)
**Fitur**:
- Interactive API testing
- Request/response examples
- Schema definitions
- Authentication info

---

## 📊 KESIMPULAN

### Pencapaian Project
✅ Implementasi full-stack web application dengan FastAPI
✅ Database relational dengan MySQL dan SQLAlchemy ORM
✅ Integrasi AI untuk analisis mendalam
✅ RESTful API dengan dokumentasi otomatis
✅ Responsive web design dengan custom CSS
✅ CSV import utility untuk data management
✅ Error handling dan validation yang robust
✅ Separation of concerns dengan layered architecture

### Teknologi yang Dipelajari
- **Backend**: FastAPI, SQLAlchemy, Pydantic, Uvicorn
- **Frontend**: Jinja2, HTML5, CSS3, JavaScript
- **Database**: MySQL, relational design, ORM
- **AI Integration**: API integration, prompt engineering
- **DevOps**: Virtual environment, environment variables, Git

### Tantangan yang Dihadapi
1. **AI Integration**: Handling API errors dan fallback strategy
2. **Database Design**: Normalization dan relationship management
3. **Frontend-Backend Communication**: AJAX dan template rendering
4. **Data Validation**: Pydantic schemas dan error messages

### Pengembangan Selanjutnya
- [ ] User authentication dan authorization
- [ ] Wishlist dan comparison history
- [ ] Review dan rating dari user
- [ ] Price tracking dan alerts
- [ ] Mobile app dengan React Native
- [ ] Deployment ke cloud (AWS/GCP)

---

**Terima Kasih!**

Tim COMPARELY
Dasar Pemrograman - 2025
