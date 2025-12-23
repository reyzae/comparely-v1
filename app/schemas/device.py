from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

# Import schema Category untuk nested response
from .category import Category

# ==================== BASE SCHEMAS ====================

class DeviceBase(BaseModel):
    """
    Schema dasar untuk Device.
    Berisi semua field yang diperlukan untuk create device.
    """
    name: str                    # Nama perangkat
    brand: str                   # Merek
    category_id: int             # ID kategori (foreign key)
    
    # Spesifikasi
    cpu: str                     # Processor
    gpu: str                     # Graphics
    ram: str                     # Memory
    storage: str                 # Penyimpanan
    camera: str                  # Kamera
    battery: str                 # Baterai
    screen: str                  # Layar
    
    # Info tambahan
    release_year: int            # Tahun rilis
    price: Decimal               # Harga
    image_url: Optional[str] = None      # URL gambar (opsional)
    description: Optional[str] = None    # Deskripsi (opsional)


# ==================== CREATE SCHEMAS ====================

class DeviceCreate(DeviceBase):
    """
    Schema untuk membuat Device baru.
    Inherit semua field dari DeviceBase.
    
    Digunakan di endpoint POST /devices/
    """
    pass


# ==================== RESPONSE SCHEMAS ====================

class Device(DeviceBase):
    """
    Schema untuk response Device dari database.
    Menambahkan id dan relasi ke category & benchmark.
    
    Digunakan untuk return data ke client.
    """
    id: int
    
    # Nested objects (opsional, bisa null)
    category: Optional[Category] = None
    # benchmark: Optional[Benchmark] = None  # Uncomment jika perlu
    
    class Config:
        # Agar bisa convert dari SQLAlchemy model ke Pydantic
        from_attributes = True
