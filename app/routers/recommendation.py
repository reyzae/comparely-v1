from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.deps import get_db
from ..services import recommendation_service, ai as ai_service
from ..schemas.device import Device
from ..core.config import USE_CASES

router = APIRouter(
    prefix="/recommendation",
    tags=["recommendation"]
)

@router.get("/", response_model=List[Device])
def get_device_recommendations(
    max_price: Optional[float] = Query(None, description="Harga maksimal (Rp)"),
    category_id: Optional[int] = Query(None, description="ID Kategori (1=Smartphone, 2=Laptop)"),
    min_release_year: Optional[int] = Query(None, description="Tahun rilis minimal (misal: 2020)"),
    limit: int = Query(5, description="Jumlah rekomendasi maksimal", ge=1, le=20),
    db: Session = Depends(get_db)
):
    """
    Endpoint untuk mendapatkan rekomendasi device.
    
    **Cara Pakai:**
    - Tanpa parameter: Menampilkan 5 device terbaru
    - Dengan `max_price`: Filter device dengan harga <= max_price
    - Dengan `category_id`: Filter berdasarkan kategori (1=Smartphone, 2=Laptop)
    - Dengan `min_release_year`: Filter device yang rilis >= tahun tertentu
    
    **Contoh:**
    - `/recommendation/?max_price=5000000` → Device dengan harga max 5 juta
    - `/recommendation/?category_id=1&max_price=10000000` → Smartphone max 10 juta
    - `/recommendation/?min_release_year=2022&limit=10` → 10 device terbaru (2022+)
    
    **Hasil:**
    Device akan di-sort berdasarkan:
    1. Tahun rilis (terbaru dulu)
    2. Harga (termurah dulu)
    """
    recommendations = recommendation_service.get_recommendations(
        db=db,
        max_price=max_price,
        category_id=category_id,
        min_release_year=min_release_year,
        limit=limit
    )
    
    return recommendations


@router.get("/ai")
def get_ai_recommendations(
    max_price: Optional[float] = Query(None, description="Harga maksimal (Rp)"),
    category_id: Optional[int] = Query(None, description="ID Kategori (1=Smartphone, 2=Laptop)"),
    min_release_year: Optional[int] = Query(None, description="Tahun rilis minimal"),
    use_case: Optional[str] = Query(None, description=f"Use case: {', '.join(USE_CASES)}"),
    limit: int = Query(5, description="Jumlah rekomendasi maksimal", ge=1, le=10),
    db: Session = Depends(get_db)
):
    """
    Endpoint untuk mendapatkan rekomendasi device dengan analisis AI dari Grok AI.
    
    **Fitur Baru dengan AI:**
    - Filter device berdasarkan kriteria (sama seperti /recommendation/)
    - **Ranking & analisis dari Grok AI**
    - Penjelasan kenapa device cocok untuk use case tertentu
    
    **Use Case yang Tersedia:**
    - `gaming`: Untuk bermain game
    - `fotografi`: Untuk fotografi/konten creator
    - `kerja`: Untuk produktivitas/kerja
    - `kuliah`: Untuk pelajar/mahasiswa
    - `multimedia`: Untuk hiburan/multimedia
    
    **Contoh:**
    - `/recommendation/ai?max_price=5000000&use_case=gaming`
    - `/recommendation/ai?category_id=1&use_case=fotografi&limit=3`
    
    Returns:
        Dictionary berisi:
        - devices: List device yang direkomendasikan
        - ai_recommendation: Analisis & ranking dari Grok AI
    """
    # 1. Filter device berdasarkan kriteria (rule-based)
    devices = recommendation_service.get_recommendations(
        db=db,
        max_price=max_price,
        category_id=category_id,
        min_release_year=min_release_year,
        limit=limit
    )
    
    # 2. Jika tidak ada device yang match, return empty
    if not devices:
        return {
            "devices": [],
            "ai_recommendation": "Maaf, tidak ada device yang sesuai dengan kriteria Anda."
        }
    
    # 3. Dapatkan rekomendasi AI dari Grok AI
    result = ai_service.get_ai_recommendation(
        devices=devices,
        use_case=use_case,
        max_price=max_price
    )
    
    return result
