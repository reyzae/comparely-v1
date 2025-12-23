"""
Notification Model - Sistem notifikasi untuk admin

Author: Kelompok COMPARELY
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Notification(Base):
    """
    Model untuk menyimpan notifikasi admin.
    Notifikasi bisa berupa: data baru, error, warning, info, dll.
    """
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    
    # Target user (jika null = untuk semua admin)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Detail notifikasi
    type = Column(String(50), nullable=False)  # success, info, warning, error
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    
    # Link/Action
    action_url = Column(String(500), nullable=True)  # URL untuk redirect
    action_label = Column(String(100), nullable=True)  # Label button action
    
    # Status
    is_read = Column(Boolean, default=False, nullable=False)
    read_at = Column(DateTime, nullable=True)
    
    # Metadata
    icon = Column(String(50), nullable=True)  # Font Awesome icon class
    priority = Column(Integer, default=0)  # 0=normal, 1=high, 2=urgent
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)  # Auto-delete setelah tanggal ini
    
    # Relationship
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, type={self.type}, title={self.title})>"
