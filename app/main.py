from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from .routers import devices, compare, categories, recommendation, frontend, admin
from .database import engine
from .models import Base  # Import Base dari models package baru
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Membuat tabel database otomatis
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="COMPARELY",
    description="Aplikasi Perbandingan Perangkat",
    version="1.0.0"
)

# Add SessionMiddleware for user authentication
# Secret key untuk encrypt session cookies
SECRET_KEY = os.getenv("SECRET_KEY", "comparely-secret-key-change-in-production-please")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


@app.on_event("startup")
async def startup_event():
    """
    Event yang dijalankan saat aplikasi startup.
    Melakukan validasi konfigurasi dan menampilkan warning jika ada yang kurang.
    """
    print("\n" + "="*60)
    print("🚀 COMPARELY - Aplikasi Perbandingan Perangkat")
    print("="*60)
    
    # Check AI_API_KEY
    ai_api_key = os.getenv("AI_API_KEY", "")
    if not ai_api_key or ai_api_key == "":
        print("\n⚠️  WARNING: AI_API_KEY tidak ditemukan!")
        print("   Fitur AI tidak akan tersedia.")
        print("   Untuk mengaktifkan:")
        print("   1. Dapatkan API key")
        print("   2. Tambahkan ke file .env: AI_API_KEY=...")
        print("   3. Restart aplikasi\n")
    else:
        print("✅ AI_API_KEY terdeteksi - Fitur AI aktif")
    
    # Check DATABASE_URL
    db_url = os.getenv("DATABASE_URL", "")
    if db_url:
        print("✅ DATABASE_URL terdeteksi")
    else:
        print("⚠️  WARNING: DATABASE_URL tidak ditemukan di .env")
    
    print("="*60 + "\n")

# Favicon route
from fastapi.responses import FileResponse

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon"""
    return FileResponse("app/static/images/favicon.ico")

# Folder untuk file CSS/Gambar
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Menambahkan router (halaman/fitur)
# Frontend router harus di-include PERTAMA agar route "/" bisa handle HTML
app.include_router(frontend.router)
app.include_router(admin.router)  # Admin panel routes
app.include_router(devices.router)
app.include_router(compare.router)
app.include_router(categories.router)
app.include_router(recommendation.router)
