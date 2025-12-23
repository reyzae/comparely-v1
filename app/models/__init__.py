"""
Models package - Database models (SQLAlchemy ORM)

File ini mengumpulkan semua model dari file terpisah agar mudah di-import.
Contoh: from app.models import Phone, Category, User, Role
"""

from ..database import Base
from .category import Category
from .phone import Phone
from .user import User
from .role import Role
from .activity_log import ActivityLog
from .notification import Notification
from .settings import AppSettings

# List semua model yang bisa di-import
__all__ = ["Base", "Category", "Phone", "User", "Role", "ActivityLog", "Notification", "AppSettings"]

