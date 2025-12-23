"""
Role-Based Access Control (RBAC) Middleware
Provides decorators and utilities for permission checking.
"""

from fastapi import HTTPException, Request, Depends
from sqlalchemy.orm import Session
from functools import wraps
from typing import List, Optional
from app.core.deps import get_db
from app.models import User, Role


def get_current_user_with_role(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    """
    Get current user with role information from session.
    Returns None if not logged in.
    """
    user_id = request.session.get("user_id") if hasattr(request, "session") else None
    
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            # Load role relationship
            if user.role_id:
                user.role = db.query(Role).filter(Role.id == user.role_id).first()
            return user
    
    return None


def require_role(allowed_roles: List[str]):
    """
    Decorator to require specific roles for a route.
    
    Usage:
        @router.get("/admin/users")
        @require_role(["Admin", "Super Admin"])
        async def admin_users(...):
            ...
    
    Args:
        allowed_roles: List of role names that are allowed to access this route
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get request and db from kwargs
            request = kwargs.get('request')
            db = kwargs.get('db')
            
            if not request or not db:
                raise HTTPException(status_code=500, detail="Internal server error")
            
            # Get current user
            user = get_current_user_with_role(request, db)
            
            if not user:
                raise HTTPException(status_code=401, detail="Not authenticated")
            
            # Check if user has role
            if not user.role:
                raise HTTPException(status_code=403, detail="No role assigned")
            
            # Check if user's role is in allowed roles
            if user.role.name not in allowed_roles:
                raise HTTPException(
                    status_code=403,
                    detail=f"Access denied. Required role: {', '.join(allowed_roles)}"
                )
            
            # Call original function
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


def has_permission(user: User, permission: str) -> bool:
    """
    Check if user has a specific permission.
    
    Args:
        user: User object
        permission: Permission string (e.g., "create_device", "delete_user")
    
    Returns:
        True if user has permission, False otherwise
    """
    if not user or not user.role:
        return False
    
    # Super Admin has all permissions
    if user.role.name == "Super Admin":
        return True
    
    # Check role permissions
    if not user.role.permissions:
        return False
    
    # If permissions is "all", grant all permissions
    if user.role.permissions == "all":
        return True
    
    # Check if permission is in role's permissions
    # Assuming permissions is stored as JSON string like: ["read", "create", "update"]
    try:
        import json
        permissions_list = json.loads(user.role.permissions) if isinstance(user.role.permissions, str) else user.role.permissions
        return permission in permissions_list
    except:
        return False


def can_create(user: User) -> bool:
    """Check if user can create resources"""
    return has_permission(user, "create") or user.role.name in ["Admin", "Super Admin"]


def can_update(user: User) -> bool:
    """Check if user can update resources"""
    return has_permission(user, "update") or user.role.name in ["Admin", "Super Admin"]


def can_delete(user: User) -> bool:
    """Check if user can delete resources"""
    return has_permission(user, "delete") or user.role.name in ["Admin", "Super Admin"]


def can_read(user: User) -> bool:
    """Check if user can read resources"""
    return has_permission(user, "read") or user.role is not None
