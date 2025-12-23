"""
CRUD operations untuk Notifications

Author: Kelompok COMPARELY
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.notification import Notification


def create_notification(
    db: Session,
    type: str,
    title: str,
    message: str,
    user_id: Optional[int] = None,
    action_url: Optional[str] = None,
    action_label: Optional[str] = None,
    icon: Optional[str] = None,
    priority: int = 0,
    expires_at: Optional[datetime] = None
) -> Notification:
    """
    Buat notifikasi baru.
    
    Args:
        db: Database session
        type: Tipe notifikasi (success, info, warning, error)
        title: Judul notifikasi
        message: Isi pesan
        user_id: Target user (None = semua admin)
        action_url: URL untuk redirect
        action_label: Label button action
        icon: Font Awesome icon class
        priority: 0=normal, 1=high, 2=urgent
        expires_at: Tanggal kadaluarsa
    
    Returns:
        Notification object yang baru dibuat
    """
    notification = Notification(
        user_id=user_id,
        type=type,
        title=title,
        message=message,
        action_url=action_url,
        action_label=action_label,
        icon=icon,
        priority=priority,
        expires_at=expires_at
    )
    
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def get_notifications(
    db: Session,
    user_id: Optional[int] = None,
    is_read: Optional[bool] = None,
    type: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
) -> List[Notification]:
    """
    Ambil daftar notifikasi dengan filter.
    
    Args:
        db: Database session
        user_id: Filter by user ID (None = semua)
        is_read: Filter by read status
        type: Filter by notification type
        skip: Offset untuk pagination
        limit: Jumlah maksimal hasil
    
    Returns:
        List of Notification objects
    """
    query = db.query(Notification)
    
    # Filter by user (include user-specific + global notifications)
    if user_id is not None:
        query = query.filter(
            (Notification.user_id == user_id) | (Notification.user_id == None)
        )
    
    if is_read is not None:
        query = query.filter(Notification.is_read == is_read)
    
    if type:
        query = query.filter(Notification.type == type)
    
    # Filter expired notifications
    query = query.filter(
        (Notification.expires_at == None) | (Notification.expires_at > datetime.utcnow())
    )
    
    # Order by priority (urgent first) then newest
    query = query.order_by(
        Notification.priority.desc(),
        Notification.created_at.desc()
    )
    
    return query.offset(skip).limit(limit).all()


def get_notification_by_id(db: Session, notification_id: int) -> Optional[Notification]:
    """
    Ambil notifikasi berdasarkan ID.
    
    Args:
        db: Database session
        notification_id: ID notifikasi yang dicari
    
    Returns:
        Notification object atau None jika tidak ditemukan
    """
    return db.query(Notification).filter(Notification.id == notification_id).first()


def mark_as_read(db: Session, notification_id: int) -> Optional[Notification]:
    """
    Tandai notifikasi sebagai sudah dibaca.
    
    Args:
        db: Database session
        notification_id: ID notifikasi
    
    Returns:
        Notification object yang sudah diupdate atau None
    """
    notification = get_notification_by_id(db, notification_id)
    if notification:
        notification.is_read = True
        notification.read_at = datetime.utcnow()
        db.commit()
        db.refresh(notification)
    return notification


def mark_all_as_read(db: Session, user_id: Optional[int] = None) -> int:
    """
    Tandai semua notifikasi sebagai sudah dibaca.
    
    Args:
        db: Database session
        user_id: User ID (None = semua)
    
    Returns:
        Jumlah notifikasi yang diupdate
    """
    query = db.query(Notification).filter(Notification.is_read == False)
    
    if user_id is not None:
        query = query.filter(
            (Notification.user_id == user_id) | (Notification.user_id == None)
        )
    
    count = query.update({
        "is_read": True,
        "read_at": datetime.utcnow()
    })
    db.commit()
    return count


def count_unread_notifications(db: Session, user_id: Optional[int] = None) -> int:
    """
    Hitung jumlah notifikasi yang belum dibaca.
    
    Args:
        db: Database session
        user_id: User ID (None = semua)
    
    Returns:
        Jumlah notifikasi unread
    """
    query = db.query(Notification).filter(Notification.is_read == False)
    
    if user_id is not None:
        query = query.filter(
            (Notification.user_id == user_id) | (Notification.user_id == None)
        )
    
    # Filter expired notifications
    query = query.filter(
        (Notification.expires_at == None) | (Notification.expires_at > datetime.utcnow())
    )
    
    return query.count()


def delete_notification(db: Session, notification_id: int) -> bool:
    """
    Hapus notifikasi.
    
    Args:
        db: Database session
        notification_id: ID notifikasi yang akan dihapus
    
    Returns:
        True jika berhasil, False jika tidak ditemukan
    """
    notification = get_notification_by_id(db, notification_id)
    if notification:
        db.delete(notification)
        db.commit()
        return True
    return False


def delete_expired_notifications(db: Session) -> int:
    """
    Hapus notifikasi yang sudah kadaluarsa.
    Berguna untuk maintenance database.
    
    Args:
        db: Database session
    
    Returns:
        Jumlah notifikasi yang dihapus
    """
    deleted = db.query(Notification).filter(
        Notification.expires_at < datetime.utcnow()
    ).delete()
    db.commit()
    return deleted
