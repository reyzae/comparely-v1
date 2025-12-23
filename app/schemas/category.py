from pydantic import BaseModel
from typing import Optional

# ==================== BASE SCHEMAS ====================

class CategoryBase(BaseModel):
    """
    Schema dasar untuk Category.
    Berisi field yang dipakai untuk create dan read.
    """
    name: str  # Nama kategori, misal: "Smartphone"


# ==================== CREATE SCHEMAS ====================

class CategoryCreate(CategoryBase):
    """
    Schema untuk membuat Category baru.
    Inherit semua field dari CategoryBase.
    
    Digunakan di endpoint POST /categories/
    """
    pass


# ==================== RESPONSE SCHEMAS ====================

class Category(CategoryBase):
    """
    Schema untuk response Category dari database.
    Menambahkan field id yang auto-generate.
    
    Digunakan untuk return data ke client.
    """
    id: int
    
    class Config:
        # Agar bisa convert dari SQLAlchemy model ke Pydantic
        from_attributes = True
