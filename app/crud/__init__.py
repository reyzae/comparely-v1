"""
CRUD operations package.
Berisi fungsi-fungsi untuk Create, Read, Update, Delete database.
"""

# Import hanya modules yang essential dan sudah working
from . import category
from . import device

# Export semua agar bisa di-import
__all__ = [
    "category",
    "device"
]
