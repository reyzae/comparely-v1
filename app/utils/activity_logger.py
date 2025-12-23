"""
Activity Logger Utility - Helper untuk auto-logging aktivitas

Author: Kelompok COMPARELY
"""

from sqlalchemy.orm import Session
from fastapi import Request
from typing import Optional, Dict, Any
from app.crud import activity_log as activity_log_crud
import json


def log_activity(
    db: Session,
    request: Request,
    action: str,
    entity_type: str,
    entity_id: Optional[int] = None,
    entity_name: Optional[str] = None,
    old_values: Optional[Dict[str, Any]] = None,
    new_values: Optional[Dict[str, Any]] = None,
    description: Optional[str] = None
):
    """
    Helper function untuk log aktivitas dengan mudah.
    
    Args:
        db: Database session
        request: FastAPI Request object
        action: Jenis aksi (CREATE, UPDATE, DELETE, LOGIN, LOGOUT)
        entity_type: Tipe entity (Phone, Category, User, dll)
        entity_id: ID entity yang diubah
        entity_name: Nama entity
        old_values: Data sebelum perubahan
        new_values: Data setelah perubahan
        description: Deskripsi human-readable
    
    Example:
        log_activity(
            db=db,
            request=request,
            action="CREATE",
            entity_type="Phone",
            entity_id=phone.id,
            entity_name=phone.name,
            description=f"Created new phone: {phone.name}"
        )
    """
    # Get user info from session
    user_id = request.session.get("user_id")
    user_name = request.session.get("user_name", "System")
    
    # Get request metadata
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    
    # Create log
    activity_log_crud.create_activity_log(
        db=db,
        user_id=user_id,
        user_name=user_name,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        entity_name=entity_name,
        old_values=old_values,
        new_values=new_values,
        ip_address=ip_address,
        user_agent=user_agent,
        description=description
    )


def log_create(
    db: Session,
    request: Request,
    entity_type: str,
    entity_id: int,
    entity_name: str,
    data: Optional[Dict[str, Any]] = None
):
    """
    Shortcut untuk log CREATE action.
    
    Example:
        log_create(db, request, "Phone", phone.id, phone.name, {"brand": "Apple"})
    """
    description = f"Created new {entity_type}: {entity_name}"
    log_activity(
        db=db,
        request=request,
        action="CREATE",
        entity_type=entity_type,
        entity_id=entity_id,
        entity_name=entity_name,
        new_values=data,
        description=description
    )


def log_update(
    db: Session,
    request: Request,
    entity_type: str,
    entity_id: int,
    entity_name: str,
    old_data: Optional[Dict[str, Any]] = None,
    new_data: Optional[Dict[str, Any]] = None
):
    """
    Shortcut untuk log UPDATE action.
    
    Example:
        log_update(db, request, "Phone", phone.id, phone.name, 
                  old_data={"price": 10000}, new_data={"price": 12000})
    """
    description = f"Updated {entity_type}: {entity_name}"
    log_activity(
        db=db,
        request=request,
        action="UPDATE",
        entity_type=entity_type,
        entity_id=entity_id,
        entity_name=entity_name,
        old_values=old_data,
        new_values=new_data,
        description=description
    )


def log_delete(
    db: Session,
    request: Request,
    entity_type: str,
    entity_id: int,
    entity_name: str,
    data: Optional[Dict[str, Any]] = None
):
    """
    Shortcut untuk log DELETE action.
    
    Example:
        log_delete(db, request, "Phone", phone.id, phone.name)
    """
    description = f"Deleted {entity_type}: {entity_name}"
    log_activity(
        db=db,
        request=request,
        action="DELETE",
        entity_type=entity_type,
        entity_id=entity_id,
        entity_name=entity_name,
        old_values=data,
        description=description
    )


def log_login(db: Session, request: Request, user_name: str):
    """
    Shortcut untuk log LOGIN action.
    
    Example:
        log_login(db, request, "admin@example.com")
    """
    log_activity(
        db=db,
        request=request,
        action="LOGIN",
        entity_type="User",
        entity_name=user_name,
        description=f"User {user_name} logged in"
    )


def log_logout(db: Session, request: Request, user_name: str):
    """
    Shortcut untuk log LOGOUT action.
    
    Example:
        log_logout(db, request, "admin@example.com")
    """
    log_activity(
        db=db,
        request=request,
        action="LOGOUT",
        entity_type="User",
        entity_name=user_name,
        description=f"User {user_name} logged out"
    )


def get_model_changes(old_obj: Any, new_data: Dict[str, Any]) -> tuple:
    """
    Helper untuk detect perubahan antara object lama dan data baru.
    
    Args:
        old_obj: SQLAlchemy model object
        new_data: Dictionary dengan data baru
    
    Returns:
        Tuple (old_values, new_values) yang berisi hanya field yang berubah
    
    Example:
        old_vals, new_vals = get_model_changes(phone, form_data)
        log_update(db, request, "Phone", phone.id, phone.name, old_vals, new_vals)
    """
    old_values = {}
    new_values = {}
    
    for key, new_value in new_data.items():
        if hasattr(old_obj, key):
            old_value = getattr(old_obj, key)
            # Only log if value changed
            if old_value != new_value:
                old_values[key] = str(old_value) if old_value is not None else None
                new_values[key] = str(new_value) if new_value is not None else None
    
    return old_values, new_values
