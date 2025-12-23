from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models
from ..crud import device as device_crud

def get_recommendations(
    db: Session,
    max_price: Optional[float] = None,
    category_id: Optional[int] = None,
    min_release_year: Optional[int] = None,
    limit: int = 5
) -> List[models.Phone]:
    """
    Memberikan rekomendasi phone berdasarkan kriteria yang diberikan.
    
    Logika sederhana untuk mahasiswa:
    1. Filter berdasarkan kriteria (harga, kategori, tahun)
    2. Sort berdasarkan tahun rilis (terbaru) dan harga (termurah)
    3. Return top N phones
    
    Args:
        db: Database session
        max_price: Harga maksimal yang diinginkan
        category_id: ID kategori (1=Smartphone, 2=Laptop, dll)
        min_release_year: Tahun rilis minimal
        limit: Berapa banyak rekomendasi yang dikembalikan
    
    Returns:
        List of Phone objects
    """
    # Mulai dengan query semua devices
    query = db.query(models.Phone)
    
    # Filter berdasarkan harga maksimal
    if max_price is not None:
        query = query.filter(models.Phone.price <= max_price)
    
    # Filter berdasarkan kategori
    if category_id is not None:
        query = query.filter(models.Phone.category_id == category_id)
    
    # Filter berdasarkan tahun rilis minimal
    if min_release_year is not None:
        query = query.filter(models.Phone.release_year >= min_release_year)
    
    # Sort: Prioritas tahun terbaru, lalu harga termurah
    query = query.order_by(
        models.Phone.release_year.desc(),  # Tahun terbaru dulu
        models.Phone.price.asc()            # Harga termurah dulu
    )
    
    # Ambil top N phones
    return query.limit(limit).all()


def calculate_device_score(device: models.Phone) -> float:
    """
    Menghitung skor phone berdasarkan beberapa faktor.
    Skor lebih tinggi = lebih direkomendasikan.
    
    Faktor yang dipertimbangkan:
    - Tahun rilis (lebih baru = lebih baik)
    - Harga (lebih murah = lebih baik, dengan normalisasi)
    
    Args:
        device: Phone object
    
    Returns:
        Skor phone (float)
    """
    score = 0.0
    
    # Faktor 1: Tahun Rilis (bobot 60%)
    # Asumsi: tahun 2020-2025 adalah range yang relevan
    if device.release_year:
        # Normalisasi: 2020 = 0, 2025 = 5
        year_score = max(0, device.release_year - 2020) * 12  # Max 60 poin
        score += year_score
    
    # Faktor 2: Harga (bobot 40%)
    # Semakin murah semakin baik (inverse)
    if device.price:
        # Normalisasi harga: 1jt = 40 poin, 20jt = 0 poin
        price_float = float(device.price)
        price_score = max(0, 40 - (price_float / 500000))  # Max 40 poin
        score += price_score
    
    return score
