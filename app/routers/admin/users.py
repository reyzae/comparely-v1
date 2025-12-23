"""
Admin Users Router
Handles user and role management (list, create, edit, delete).
"""

from math import ceil
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models import User, Role
from .auth import get_current_user
from app.core.rbac_context import add_rbac_to_context

import logging
import re

# Setup templates
templates = Jinja2Templates(directory="app/templates")
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(tags=["admin-users"])


# ============================================
# User Management Routes
# ============================================

@router.get("/users", response_class=HTMLResponse)
async def admin_users(
    request: Request,
    page: int = 1,
    search: str = None,
    sort: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    """Halaman users management"""
    ITEMS_PER_PAGE = 20
    
    try:
        # Build query
        query = db.query(User)
        
        # Search
        if search:
            query = query.filter(
                (User.username.ilike(f"%{search}%")) |
                (User.email.ilike(f"%{search}%"))
            )
        
        # Sorting
        sort_column = getattr(User, sort, User.id)
        if order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        # Count total
        total_items = query.count()
        total_pages = ceil(total_items / ITEMS_PER_PAGE) if total_items > 0 else 1
        
        # Paginate
        offset = (page - 1) * ITEMS_PER_PAGE
        users = query.offset(offset).limit(ITEMS_PER_PAGE).all()
        
        # Manual load role untuk setiap user
        for user in users:
            if user.role_id:
                try:
                    user.role = db.query(Role).filter(Role.id == user.role_id).first()
                except:
                    user.role = None
        
        current_user = get_current_user(request, db)
        rbac_context = add_rbac_to_context(current_user)

        return templates.TemplateResponse(
            "admin/users_list.html",
            {
                "request": request,
                "current_user": current_user,
                **rbac_context,  # Add RBAC permissions
                "users": users,
                "page": page,
                "total_pages": total_pages,
                "search": search or "",
                "sort": sort,
                "order": order
            }
        )
    except Exception as e:
        logger.exception(f"Error in admin_users: {e}")
        current_user = get_current_user(request, db)
        rbac_context = add_rbac_to_context(current_user)

        return templates.TemplateResponse(
            "admin/users_list.html",
            {
                "request": request,
                "current_user": current_user,
                **rbac_context,  # Add RBAC permissions
                "users": [],
                "page": 1,
                "total_pages": 1,
                "search": "",
                "sort": "id",
                "order": "asc"
            }
        )


@router.get("/users/new", response_class=HTMLResponse)
async def admin_user_new(request: Request, db: Session = Depends(get_db)):
    """Form untuk create user baru"""
    roles = db.query(Role).all()
    current_user = get_current_user(request, db)
    rbac_context = add_rbac_to_context(current_user)

    return templates.TemplateResponse(
        "admin/user_form.html",
        {
            "request": request,
            "current_user": current_user,
            **rbac_context,  # Add RBAC permissions
            "user": None,
            "roles": roles
        }
    )


@router.get("/users/{user_id}/edit", response_class=HTMLResponse)
async def admin_user_edit(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Form untuk edit user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    roles = db.query(Role).all()
    current_user = get_current_user(request, db)
    rbac_context = add_rbac_to_context(current_user)

    return templates.TemplateResponse(
        "admin/user_form.html",
        {
            "request": request,
            "current_user": current_user,
            **rbac_context,  # Add RBAC permissions
            "user": user,
            "roles": roles
        }
    )


# ============================================
# Role Management Routes
# ============================================

@router.get("/roles", response_class=HTMLResponse)
async def admin_roles(
    request: Request,
    page: int = 1,
    search: str = None,
    sort: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    """Halaman roles management"""
    ITEMS_PER_PAGE = 20
    
    # Build query
    query = db.query(Role)
    
    # Search
    if search:
        query = query.filter(Role.name.ilike(f"%{search}%"))
    
    # Sorting
    sort_column = getattr(Role, sort, Role.id)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    # Count total
    total_items = query.count()
    total_pages = ceil(total_items / ITEMS_PER_PAGE) if total_items > 0 else 1
    
    # Paginate
    offset = (page - 1) * ITEMS_PER_PAGE
    roles = query.offset(offset).limit(ITEMS_PER_PAGE).all()
    
    current_user = get_current_user(request, db)
    rbac_context = add_rbac_to_context(current_user)

    return templates.TemplateResponse(
        "admin/roles_list.html",
        {
            "request": request,
            "current_user": current_user,
            **rbac_context,  # Add RBAC permissions
            "roles": roles,
            "page": page,
            "total_pages": total_pages,
            "search": search or "",
            "sort": sort,
            "order": order
        }
    )


@router.get("/roles/new", response_class=HTMLResponse)
async def admin_role_new(request: Request, db: Session = Depends(get_db)):
    """Form untuk create role baru"""
    current_user = get_current_user(request, db)
    rbac_context = add_rbac_to_context(current_user)

    return templates.TemplateResponse(
        "admin/role_form.html",
        {
            "request": request,
            "current_user": current_user,
            **rbac_context,  # Add RBAC permissions
            "role": None
        }
    )


@router.get("/roles/{role_id}/edit", response_class=HTMLResponse)
async def admin_role_edit(
    request: Request,
    role_id: int,
    db: Session = Depends(get_db)
):
    """Form untuk edit role"""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    current_user = get_current_user(request, db)
    rbac_context = add_rbac_to_context(current_user)

    return templates.TemplateResponse(
        "admin/role_form.html",
        {
            "request": request,
            "current_user": current_user,
            **rbac_context,  # Add RBAC permissions
            "role": role
        }
    )


# ============================================
# POST Routes (Form Submissions)
# ============================================

@router.post("/users/new")
async def admin_user_create(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role_id: int = Form(...),
    is_active: bool = Form(False),
    db: Session = Depends(get_db)
):
    """Create new user"""
    try:
        # Email validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return RedirectResponse(
                url="/admin/users?error=Invalid email format",
                status_code=303
            )
        
        # Check if username or email already exists
        existing_user = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            return RedirectResponse(
                url="/admin/users?error=Username or email already exists",
                status_code=303
            )
        
        # Create user (password should be hashed in production!)
        user = User(
            username=username,
            email=email,
            password_hash=password,  # TODO: Hash password!
            role_id=role_id,
            is_active=is_active
        )
        db.add(user)
        db.commit()
        
        logger.info(f"Created new user: {username}")
        return RedirectResponse(
            url="/admin/users?message=User created successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error creating user: {e}")
        return RedirectResponse(
            url=f"/admin/users?error={str(e)}",
            status_code=303
        )


@router.post("/users/{user_id}/edit")
async def admin_user_update(
    request: Request,
    user_id: int,
    username: str = Form(...),
    email: str = Form(...),
    role_id: int = Form(...),
    is_active: bool = Form(False),
    password: str = Form(None),
    db: Session = Depends(get_db)
):
    """Update user"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return RedirectResponse(
                url="/admin/users?error=User not found",
                status_code=303
            )
        
        user.username = username
        user.email = email
        user.role_id = role_id
        user.is_active = is_active
        
        # Update password if provided
        if password and password.strip():
            user.password_hash = password  # TODO: Hash password!
        
        db.commit()
        return RedirectResponse(
            url="/admin/users?message=User updated successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error updating user: {e}")
        return RedirectResponse(
            url=f"/admin/users?error={str(e)}",
            status_code=303
        )


@router.post("/users/{user_id}/delete")
async def admin_user_delete(user_id: int, db: Session = Depends(get_db)):
    """Delete user"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return RedirectResponse(
                url="/admin/users?error=User not found",
                status_code=303
            )
        
        db.delete(user)
        db.commit()
        return RedirectResponse(
            url="/admin/users?message=User deleted successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error deleting user: {e}")
        return RedirectResponse(
            url=f"/admin/users?error={str(e)}",
            status_code=303
        )


@router.post("/roles/new")
async def admin_role_create(
    request: Request,
    name: str = Form(...),
    description: str = Form(None),
    db: Session = Depends(get_db)
):
    """Create new role"""
    try:
        role = Role(name=name, description=description)
        db.add(role)
        db.commit()
        return RedirectResponse(
            url="/admin/roles?message=Role created successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error creating role: {e}")
        return RedirectResponse(
            url=f"/admin/roles?error={str(e)}",
            status_code=303
        )


@router.post("/roles/{role_id}/edit")
async def admin_role_update(
    request: Request,
    role_id: int,
    name: str = Form(...),
    description: str = Form(None),
    db: Session = Depends(get_db)
):
    """Update role"""
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return RedirectResponse(
                url="/admin/roles?error=Role not found",
                status_code=303
            )
        
        role.name = name
        role.description = description
        db.commit()
        return RedirectResponse(
            url="/admin/roles?message=Role updated successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error updating role: {e}")
        return RedirectResponse(
            url=f"/admin/roles?error={str(e)}",
            status_code=303
        )


@router.post("/roles/{role_id}/delete")
async def admin_role_delete(role_id: int, db: Session = Depends(get_db)):
    """Delete role"""
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return RedirectResponse(
                url="/admin/roles?error=Role not found",
                status_code=303
            )
        
        # Check if role has users
        user_count = db.query(User).filter(User.role_id == role_id).count()
        if user_count > 0:
            return RedirectResponse(
                url=f"/admin/roles?error=Cannot delete role with {user_count} users",
                status_code=303
            )
        
        db.delete(role)
        db.commit()
        return RedirectResponse(
            url="/admin/roles?message=Role deleted successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error deleting role: {e}")
        return RedirectResponse(
            url=f"/admin/roles?error={str(e)}",
            status_code=303
        )
