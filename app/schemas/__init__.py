"""
Schemas package - Pydantic schemas untuk validasi dan serialisasi data

File ini mengumpulkan semua schema dari file terpisah.
Contoh: from app.schemas import Phone, Category, PhoneCreate
"""

from .category import Category, CategoryBase, CategoryCreate
from .phone import Phone, PhoneBase, PhoneCreate

# List semua schema yang bisa di-import
__all__ = [
    # Category schemas
    "Category",
    "CategoryCreate",
    "CategoryBase",
    # Phone schemas
    "Phone",
    "PhoneCreate",
    "PhoneBase",
]
