"""
Model untuk tabel users di database.
Menyimpan informasi user yang bisa login ke admin panel.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class User(Base):
    """
    Model untuk tabel users di database.
    Digunakan untuk autentikasi dan otorisasi admin panel.
    """
    __tablename__ = "users"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # User Credentials
    username = Column(String(50), unique=True, index=True)  # Username untuk login
    email = Column(String(100), unique=True, index=True)  # Email user
    password_hash = Column(String(255))  # Password yang sudah di-hash
    
    # User Info
    full_name = Column(String(100))  # Nama lengkap user
    is_active = Column(Boolean, default=True)  # Status aktif/nonaktif
    is_verified = Column(Boolean, default=False)  # Apakah email sudah diverifikasi
    
    # Foreign Key ke tabel roles
    role_id = Column(Integer, ForeignKey("roles.id"))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)  # Kapan user dibuat
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Kapan terakhir diupdate
    last_login = Column(DateTime)  # Kapan terakhir login
    
    
    # Relationships
    # Relasi ke Role (many-to-one: banyak users, 1 role)
    role = relationship("Role", back_populates="users")
    
    # Relasi ke ActivityLog (one-to-many: 1 user, banyak logs)
    activity_logs = relationship("ActivityLog", back_populates="user", cascade="all, delete-orphan")
    
    # Relasi ke Notification (one-to-many: 1 user, banyak notifications)
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")

