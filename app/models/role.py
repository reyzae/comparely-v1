"""
Model untuk tabel roles di database.
Menyimpan informasi tentang role/peran user (Admin, Editor, Viewer, dll).
"""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from ..database import Base


class Role(Base):
    """
    Model untuk tabel roles di database.
    Digunakan untuk mengatur hak akses user.
    """
    __tablename__ = "roles"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Role Info
    name = Column(String(50), unique=True, index=True)  # Nama role, misal: "Admin", "Editor"
    description = Column(Text)  # Deskripsi role
    permissions = Column(Text)  # Permissions dalam format JSON atau comma-separated
    
    
    # Relationships
    # Relasi ke User (one-to-many: 1 role, banyak users)
    users = relationship("User", back_populates="role")

