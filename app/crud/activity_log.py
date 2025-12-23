"""
CRUD operations untuk Activity Logs

Author: Kelompok COMPARELY
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.models.activity_log import ActivityLog
import json


def create_activity_log(
    db: Session,
    user_id: Optional[int],
    user_name: str,
    action: str,
    entity_type: str,
    entity_id: Optional[int] = None,
    entity_name: Optional[str] = None,
    old_values: Optional[dict] = None,
    new_values: Optional[dict] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    description: Optional[str] = None
) -> ActivityLog:
    """
    Buat log aktivitas baru.
    
    Args:
        db: Database session
        user_id: ID user yang melakukan aksi
        user_name: Nama user (backup)
        action: Jenis aksi (CREATE, UPDATE, DELETE, LOGIN, LOGOUT)
        entity_type: Tipe entity (Phone, Category, User, dll)
        entity_id: ID entity yang diubah
        entity_name: Nama entity
        old_values: Data sebelum perubahan (dict)
        new_values: Data setelah perubahan (dict)
        ip_address: IP address user
        user_agent: Browser user agent
        description: Deskripsi human-readable
    
    Returns:
        ActivityLog object yang baru dibuat
    """
    log = ActivityLog(
        user_id=user_id,
        user_name=user_name,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        entity_name=entity_name,
        old_values=json.dumps(old_values) if old_values else None,
        new_values=json.dumps(new_values) if new_values else None,
        ip_address=ip_address,
        user_agent=user_agent,
        description=description
    )
    
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_activity_logs(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    user_id: Optional[int] = None,
    action: Optional[str] = None,
    entity_type: Optional[str] = None,
    days: Optional[int] = None
) -> List[ActivityLog]:
    """
    Ambil daftar activity logs dengan filter.
    
    Args:
        db: Database session
        skip: Offset untuk pagination
        limit: Jumlah maksimal hasil
        user_id: Filter by user ID
        action: Filter by action type
        entity_type: Filter by entity type
        days: Filter logs dari X hari terakhir
    
    Returns:
        List of ActivityLog objects
    """
    query = db.query(ActivityLog)
    
    # Apply filters
    if user_id:
        query = query.filter(ActivityLog.user_id == user_id)
    
    if action:
        query = query.filter(ActivityLog.action == action)
    
    if entity_type:
        query = query.filter(ActivityLog.entity_type == entity_type)
    
    if days:
        date_from = datetime.utcnow() - timedelta(days=days)
        query = query.filter(ActivityLog.created_at >= date_from)
    
    # Order by newest first
    query = query.order_by(ActivityLog.created_at.desc())
    
    return query.offset(skip).limit(limit).all()


def get_activity_log_by_id(db: Session, log_id: int) -> Optional[ActivityLog]:
    """
    Ambil activity log berdasarkan ID.
    
    Args:
        db: Database session
        log_id: ID log yang dicari
    
    Returns:
        ActivityLog object atau None jika tidak ditemukan
    """
    return db.query(ActivityLog).filter(ActivityLog.id == log_id).first()


def count_activity_logs(
    db: Session,
    user_id: Optional[int] = None,
    action: Optional[str] = None,
    entity_type: Optional[str] = None,
    days: Optional[int] = None
) -> int:
    """
    Hitung jumlah activity logs dengan filter.
    
    Args:
        db: Database session
        user_id: Filter by user ID
        action: Filter by action type
        entity_type: Filter by entity type
        days: Filter logs dari X hari terakhir
    
    Returns:
        Jumlah logs
    """
    query = db.query(ActivityLog)
    
    if user_id:
        query = query.filter(ActivityLog.user_id == user_id)
    
    if action:
        query = query.filter(ActivityLog.action == action)
    
    if entity_type:
        query = query.filter(ActivityLog.entity_type == entity_type)
    
    if days:
        date_from = datetime.utcnow() - timedelta(days=days)
        query = query.filter(ActivityLog.created_at >= date_from)
    
    return query.count()


def delete_old_logs(db: Session, days: int = 90) -> int:
    """
    Hapus logs yang lebih tua dari X hari.
    Berguna untuk maintenance database.
    
    Args:
        db: Database session
        days: Hapus logs lebih tua dari X hari
    
    Returns:
        Jumlah logs yang dihapus
    """
    date_threshold = datetime.utcnow() - timedelta(days=days)
    deleted = db.query(ActivityLog).filter(ActivityLog.created_at < date_threshold).delete()
    db.commit()
    return deleted
