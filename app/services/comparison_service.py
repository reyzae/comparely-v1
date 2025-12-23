from sqlalchemy.orm import Session
from typing import Dict, List, Any
from .. import models
from ..crud import device as device_crud

def compare_two_devices(db: Session, device_id_1: int, device_id_2: int) -> Dict[str, Any]:
    """
    Membandingkan 2 device dan menghasilkan highlights keunggulan masing-masing.
    
    Args:
        db: Database session
        device_id_1: ID device pertama
        device_id_2: ID device kedua
    
    Returns:
        Dictionary berisi:
        - device_1: Data device pertama
        - device_2: Data device kedua
        - highlights: List keunggulan masing-masing device
    
    Raises:
        ValueError: Jika salah satu atau kedua device tidak ditemukan
    """
    # Ambil data kedua device dari database
    device1 = device_crud.get_device(db, device_id_1)
    device2 = device_crud.get_device(db, device_id_2)
    
    # Validasi: pastikan kedua device ada
    if not device1 or not device2:
        raise ValueError("Salah satu atau kedua perangkat tidak ditemukan")
    
    # Generate highlights (keunggulan masing-masing)
    highlights = generate_highlights(device1, device2)
    
    # FastAPI akan otomatis convert SQLAlchemy model ke JSON
    # menggunakan Pydantic schema yang sudah di-set di router
    return {
        "device_1": device1,
        "device_2": device2,
        "highlights": highlights
    }


def generate_highlights(device1: models.Phone, device2: models.Phone) -> List[str]:
    """
    Generate list highlights yang membandingkan keunggulan 2 device.
    
    Logic sederhana untuk mahasiswa:
    - Bandingkan harga (lebih murah = keunggulan)
    - Bandingkan tahun rilis (lebih baru = keunggulan)
    
    Args:
        device1: Device pertama
        device2: Device kedua
    
    Returns:
        List of string highlights
    """
    highlights = []
    
    # 1. Bandingkan Harga
    if device1.price and device2.price:
        price_diff = abs(device1.price - device2.price)
        
        if device1.price < device2.price:
            highlights.append(
                f"{device1.name} lebih murah Rp {price_diff:,.0f}"
            )
        elif device2.price < device1.price:
            highlights.append(
                f"{device2.name} lebih murah Rp {price_diff:,.0f}"
            )
        # Jika sama, tidak ada highlight
    
    # 2. Bandingkan Tahun Rilis
    if device1.release_year and device2.release_year:
        if device1.release_year > device2.release_year:
            highlights.append(
                f"{device1.name} lebih baru (Rilis {device1.release_year})"
            )
        elif device2.release_year > device1.release_year:
            highlights.append(
                f"{device2.name} lebih baru (Rilis {device2.release_year})"
            )
    
    # TODO: Bisa ditambahkan comparison lain seperti:
    # - RAM (perlu parsing string "8GB" -> integer)
    # - Storage (perlu parsing string "256GB" -> integer)
    # - Benchmark scores (jika ada)
    
    return highlights


def calculate_price_difference(device1: models.Phone, device2: models.Phone) -> float:
    """
    Menghitung selisih harga antara 2 device.
    
    Args:
        device1: Device pertama
        device2: Device kedua
    
    Returns:
        Selisih harga (absolute value)
    """
    if not device1.price or not device2.price:
        return 0.0
    
    return abs(float(device1.price) - float(device2.price))
