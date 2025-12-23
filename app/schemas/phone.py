from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

# Import schema Category untuk nested response
from .category import Category

# ==================== BASE SCHEMAS ====================

class PhoneBase(BaseModel):
    """
    Schema dasar untuk Phone.
    Berisi semua field yang diperlukan untuk create phone.
    """
    name: str                    # Nama handphone
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
    source_data: Optional[str] = None    # URL sumber data (opsional)


# ==================== CREATE SCHEMAS ====================

class PhoneCreate(PhoneBase):
    """
    Schema untuk membuat Phone baru.
    Inherit semua field dari PhoneBase.
    
    Digunakan di endpoint POST /phones/
    """
    pass


# ==================== RESPONSE SCHEMAS ====================

class Phone(PhoneBase):
    """
    Schema untuk response Phone dari database.
    Menambahkan id dan relasi ke category.
    
    Digunakan untuk return data ke client.
    """
    id: int
    
    # Nested objects (opsional, bisa null)
    category: Optional[Category] = None
    
    class Config:
        # Agar bisa convert dari SQLAlchemy model ke Pydantic
        from_attributes = True
