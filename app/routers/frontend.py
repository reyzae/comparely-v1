from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from ..core.deps import get_db
from ..crud import device as device_crud

# Setup Jinja2 Templates
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["frontend"])


@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request, db: Session = Depends(get_db)):
    """
    Homepage COMPARELY - Menampilkan halaman utama dengan:
    - Hero section dengan search bar
    - Example comparison dari 2 device terbaru
    - Quick verdict
    
    Penjelasan:
    - Request: Object dari FastAPI yang berisi info tentang HTTP request
    - db: Database session untuk query data
    - templates.TemplateResponse: Render HTML template dengan data
    """
    
    # Ambil 2 device terbaru untuk example comparison
    devices = device_crud.get_devices(db, skip=0, limit=2)
    
    # Siapkan data untuk template
    comparison_data = {
        "title": "Belum ada data",
        "device1": {
            "name": "Device 1",
            "score": "N/A",
            "battery": "N/A",
            "weight": "N/A",
            "camera": "N/A",
            "price": "N/A"
        },
        "device2": {
            "name": "Device 2",
            "score": "N/A",
            "battery": "N/A",
            "weight": "N/A",
            "camera": "N/A",
            "price": "N/A"
        },
        "verdict": "Import data CSV untuk melihat perbandingan."
    }
    
    # Jika ada data device, gunakan untuk comparison
    if len(devices) >= 2:
        device1 = devices[0]
        device2 = devices[1]
        
        comparison_data = {
            "title": f"{device1.name} vs {device2.name}",
            "device1": {
                "name": device1.name,
                "score": "8.9",  # Bisa dihitung dari benchmark jika ada
                "battery": device1.battery or "N/A",
                "weight": getattr(device1, 'weight', 'N/A'),
                "camera": device1.camera or "N/A",
                "price": f"Rp {device1.price:,.0f}" if device1.price else "N/A"
            },
            "device2": {
                "name": device2.name,
                "score": "8.6",
                "battery": device2.battery or "N/A",
                "weight": getattr(device2, 'weight', 'N/A'),
                "camera": device2.camera or "N/A",
                "price": f"Rp {device2.price:,.0f}" if device2.price else "N/A"
            },
            "verdict": f"{device1.name} unggul di kamera dan nilai, sementara {device2.name} menang di ekosistem & stabilitas."
        }
    
    # Render template dengan data
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "comparison": comparison_data
        }
    )


@router.get("/device/{device_id}", response_class=HTMLResponse)
async def device_detail_page(
    request: Request,
    device_id: int,
    db: Session = Depends(get_db)
):
    """
    Halaman detail 1 device.
    
    Cara kerja:
    - User klik tombol "Detail" di halaman devices
    - URL jadi: /device/12
    - Kita ambil data device dari database berdasarkan ID
    - Tampilkan semua spesifikasi lengkap
    """
    
    # Ambil data device dari database berdasarkan ID
    device = device_crud.get_device(db, device_id)
    
    # Kalau device tidak ada, redirect ke halaman devices
    if not device:
        return RedirectResponse(url="/devices")
    
    # Render template device_detail.html dengan data device
    return templates.TemplateResponse(
        "device_detail.html",
        {
            "request": request,
            "device": device
        }
    )


@router.get("/devices", response_class=HTMLResponse)
async def devices_page(
    request: Request,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    ram: Optional[str] = None,
    storage: Optional[str] = None,
    max_price: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Halaman daftar semua device dengan advanced filters.
    
    Cara kerja:
    - Tampilkan semua device dalam bentuk grid atau list
    - User bisa filter berdasarkan kategori, brand, RAM, storage, dan harga
    - User bisa pilih 2 device untuk dibandingkan
    
    Filters:
    - category: 1 (Smartphone) atau 2 (Laptop)
    - brand: Brand name (Samsung, Apple, dll)
    - ram: RAM size (4GB, 8GB, dll)
    - storage: Storage size (128GB, 256GB, dll)
    - max_price: Harga maksimal (contoh: 5000000)
    """
    
    # Get unique brands for filter dropdown
    brands = device_crud.get_unique_brands(db)
    
    # Convert parameters
    category_id = int(category) if category else None
    max_price_float = None
    if max_price and max_price.strip():
        try:
            max_price_float = float(max_price)
        except ValueError:
            pass
    
    # Get filtered devices using new function
    devices = device_crud.get_devices_filtered(
        db=db,
        category_id=category_id,
        brand=brand if brand else None,
        ram=ram if ram else None,
        storage=storage if storage else None,
        max_price=max_price_float,
        limit=100
    )
    
    # Render template devices.html dengan data
    return templates.TemplateResponse(
        "devices.html",
        {
            "request": request,
            "devices": devices,
            "brands": brands,  # Pass brands list for dropdown
            "category": category,
            "brand": brand,
            "ram": ram,
            "storage": storage,
            "max_price": max_price
        }
    )


@router.get("/search", response_class=HTMLResponse)
async def search_devices(
    request: Request,
    query: str,
    db: Session = Depends(get_db)
):
    """
    Search devices berdasarkan query dari user.
    
    Penjelasan:
    - Query parameter 'query' diambil dari form search di homepage
    - Mencari device berdasarkan nama atau brand
    - Tampilkan hasil di halaman search_results.html
    """
    
    # Cari devices berdasarkan query (nama atau brand)
    devices = device_crud.get_devices(db, search=query, limit=50)
    
    # Render template search_results.html dengan hasil pencarian
    return templates.TemplateResponse(
        "search_results.html",
        {
            "request": request,
            "query": query,
            "devices": devices,
            "total_results": len(devices)
        }
    )


@router.get("/compare-page", response_class=HTMLResponse)
async def compare_page(
    request: Request,
    id1: int,
    id2: int,
    db: Session = Depends(get_db)
):
    """
    Halaman perbandingan 2 device.
    
    Cara kerja:
    - User klik tombol "Select" di 2 device
    - URL jadi: /compare-page?id1=1&id2=2
    - Kita ambil data kedua device dari database
    - Tampilkan di halaman compare.html
    """
    
    # Ambil data device pertama dari database
    device1 = device_crud.get_device(db, id1)
    # Ambil data device kedua dari database
    device2 = device_crud.get_device(db, id2)
    
    # Kalau salah satu device tidak ada, redirect ke homepage
    if not device1 or not device2:
        return RedirectResponse(url="/")
    
    # Buat highlights (perbandingan sederhana)
    # Ini logika sederhana untuk mahasiswa, bukan pakai AI dulu
    highlights = []
    
    # Bandingkan harga
    if device1.price and device2.price:
        price_diff = abs(device1.price - device2.price)
        if device1.price < device2.price:
            highlights.append({
                "category": "<i class='fa-solid fa-tag'></i> Harga",
                "winner": f"{device1.name} lebih murah Rp {price_diff:,.0f}"
            })
        elif device2.price < device1.price:
            highlights.append({
                "category": "<i class='fa-solid fa-tag'></i> Harga",
                "winner": f"{device2.name} lebih murah Rp {price_diff:,.0f}"
            })
    
    # Bandingkan tahun rilis
    if device1.release_year and device2.release_year:
        if device1.release_year > device2.release_year:
            highlights.append({
                "category": "<i class='fa-solid fa-calendar'></i> Tahun Rilis",
                "winner": f"{device1.name} lebih baru ({device1.release_year})"
            })
        elif device2.release_year > device1.release_year:
            highlights.append({
                "category": "<i class='fa-solid fa-calendar'></i> Tahun Rilis",
                "winner": f"{device2.name} lebih baru ({device2.release_year})"
            })
    
    # Bandingkan RAM (extract angka dari string seperti "8GB")
    if device1.ram and device2.ram:
        try:
            ram1 = int(''.join(filter(str.isdigit, device1.ram)))
            ram2 = int(''.join(filter(str.isdigit, device2.ram)))
            if ram1 > ram2:
                highlights.append({
                    "category": "<i class='fa-solid fa-memory'></i> RAM",
                    "winner": f"{device1.name} lebih besar ({device1.ram} vs {device2.ram})"
                })
            elif ram2 > ram1:
                highlights.append({
                    "category": "<i class='fa-solid fa-memory'></i> RAM",
                    "winner": f"{device2.name} lebih besar ({device2.ram} vs {device1.ram})"
                })
        except:
            pass  # Skip jika format RAM tidak standar
    
    # Bandingkan Storage (extract angka dari string seperti "256GB")
    if device1.storage and device2.storage:
        try:
            storage1 = int(''.join(filter(str.isdigit, device1.storage)))
            storage2 = int(''.join(filter(str.isdigit, device2.storage)))
            if storage1 > storage2:
                highlights.append({
                    "category": "<i class='fa-solid fa-hard-drive'></i> Storage",
                    "winner": f"{device1.name} lebih besar ({device1.storage} vs {device2.storage})"
                })
            elif storage2 > storage1:
                highlights.append({
                    "category": "<i class='fa-solid fa-hard-drive'></i> Storage",
                    "winner": f"{device2.name} lebih besar ({device2.storage} vs {device1.storage})"
                })
        except:
            pass
    
    # Bandingkan Kamera (extract angka MP dari string seperti "48MP + 12MP")
    if device1.camera and device2.camera:
        try:
            # Ambil angka pertama (main camera)
            cam1 = int(''.join(filter(str.isdigit, device1.camera.split('+')[0])))
            cam2 = int(''.join(filter(str.isdigit, device2.camera.split('+')[0])))
            if cam1 > cam2:
                highlights.append({
                    "category": "<i class='fa-solid fa-camera'></i> Kamera",
                    "winner": f"{device1.name} lebih tinggi ({cam1}MP vs {cam2}MP)"
                })
            elif cam2 > cam1:
                highlights.append({
                    "category": "<i class='fa-solid fa-camera'></i> Kamera",
                    "winner": f"{device2.name} lebih tinggi ({cam2}MP vs {cam1}MP)"
                })
        except:
            pass
    
    # Bandingkan Baterai (extract angka mAh dari string seperti "5000 mAh")
    if device1.battery and device2.battery:
        try:
            bat1 = int(''.join(filter(str.isdigit, device1.battery)))
            bat2 = int(''.join(filter(str.isdigit, device2.battery)))
            if bat1 > bat2:
                highlights.append({
                    "category": "<i class='fa-solid fa-battery-three-quarters'></i> Baterai",
                    "winner": f"{device1.name} lebih besar ({bat1} mAh vs {bat2} mAh)"
                })
            elif bat2 > bat1:
                highlights.append({
                    "category": "<i class='fa-solid fa-battery-three-quarters'></i> Baterai",
                    "winner": f"{device2.name} lebih besar ({bat2} mAh vs {bat1} mAh)"
                })
        except:
            pass
    
    # Bandingkan Screen (extract angka inch dari string seperti "6.7\"")
    if device1.screen and device2.screen:
        try:
            screen1 = float(''.join(c for c in device1.screen.split('"')[0] if c.isdigit() or c == '.'))
            screen2 = float(''.join(c for c in device2.screen.split('"')[0] if c.isdigit() or c == '.'))
            if screen1 > screen2:
                highlights.append({
                    "category": "<i class='fa-solid fa-display'></i> Layar",
                    "winner": f"{device1.name} lebih besar ({screen1}\" vs {screen2}\")"
                })
            elif screen2 > screen1:
                highlights.append({
                    "category": "<i class='fa-solid fa-display'></i> Layar",
                    "winner": f"{device2.name} lebih besar ({screen2}\" vs {screen1}\")"
                })
        except:
            pass
    
    # Render template compare.html dengan data yang sudah disiapkan
    return templates.TemplateResponse(
        "compare.html",
        {
            "request": request,
            "device1": device1,
            "device2": device2,
            "highlights": highlights
        }
    )

@router.get("/features", response_class=HTMLResponse)
async def features_page(request: Request):
    """
    Halaman Features - Menampilkan fitur-fitur unggulan COMPARELY
    
    Penjelasan:
    - Halaman statis yang menjelaskan fitur-fitur aplikasi
    - Tidak perlu database query
    - Hanya render template features.html
    """
    return templates.TemplateResponse(
        "features.html",
        {"request": request}
    )


@router.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """
    Halaman About - Menampilkan informasi tentang COMPARELY
    
    Penjelasan:
    - Halaman statis yang menjelaskan tentang aplikasi
    - Berisi misi, visi, dan informasi tim
    - Tidak perlu database query
    - Hanya render template about.html
    """
    return templates.TemplateResponse(
        "about.html",
        {"request": request}
    )


@router.get("/privacy", response_class=HTMLResponse)
async def privacy_page(request: Request):
    """
    Halaman Privacy Policy - Menampilkan kebijakan privasi COMPARELY
    
    Penjelasan:
    - Halaman statis yang menjelaskan kebijakan privasi
    - Tidak perlu database query
    - Hanya render template privacy.html
    """
    return templates.TemplateResponse(
        "privacy.html",
        {"request": request}
    )


@router.get("/terms", response_class=HTMLResponse)
async def terms_page(request: Request):
    """
    Halaman Terms of Service - Menampilkan syarat dan ketentuan COMPARELY
    
    Penjelasan:
    - Halaman statis yang menjelaskan syarat dan ketentuan
    - Tidak perlu database query
    - Hanya render template terms.html
    """
    return templates.TemplateResponse(
        "terms.html",
        {"request": request}
    )


@router.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    """
    Halaman Contact - Menampilkan informasi kontak COMPARELY
    
    Penjelasan:
    - Halaman statis yang menampilkan informasi kontak tim
    - Tidak perlu database query
    - Hanya render template contact.html
    """
    return templates.TemplateResponse(
        "contact.html",
        {"request": request}
    )

