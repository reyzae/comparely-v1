"""
Activity Log Model - Track semua perubahan data di sistem

Author: Kelompok COMPARELY
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class ActivityLog(Base):
    """
    Model untuk menyimpan log aktivitas admin.
    Setiap kali ada perubahan data (create, update, delete), akan tercatat di sini.
    """
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # User yang melakukan aksi
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user_name = Column(String(100), nullable=False)  # Backup jika user dihapus
    
    # Detail aktivitas
    action = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, LOGIN, LOGOUT
    entity_type = Column(String(50), nullable=False)  # Phone, Category, User, etc.
    entity_id = Column(Integer, nullable=True)  # ID dari entity yang diubah
    entity_name = Column(String(200), nullable=True)  # Nama entity untuk referensi
    
    # Perubahan data (JSON format)
    old_values = Column(Text, nullable=True)  # Data sebelum perubahan
    new_values = Column(Text, nullable=True)  # Data setelah perubahan
    
    # Metadata
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)  # Deskripsi human-readable
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="activity_logs")

    def __repr__(self):
        return f"<ActivityLog(id={self.id}, user={self.user_name}, action={self.action}, entity={self.entity_type})>"
