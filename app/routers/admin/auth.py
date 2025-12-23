"""
Admin Authentication Router
Handles admin login, logout, and profile management.
"""

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models import User
import bcrypt
from datetime import datetime

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Create router
router = APIRouter(tags=["admin-auth"])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash using bcrypt directly"""
    try:
        # Convert to bytes
        password_bytes = plain_password.encode('utf-8')
        hash_bytes = hashed_password.encode('utf-8')
        # Verify
        return bcrypt.checkpw(password_bytes, hash_bytes)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt directly"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def get_current_user(request: Request, db: Session) -> User:
    """
    Get current logged-in user from session.
    Returns a mock user if no session (for development).
    """
    # Try to get user_id from session
    user_id = request.session.get("user_id") if hasattr(request, "session") else None
    
    if user_id:
        # Get user from database
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return user
    
    # Return mock user for development (if no session)
    mock_user = User(
        id=0,
        username="admin",
        email="admin@comparely.com",
        full_name="Administrator",
        is_active=True
    )
    return mock_user


@router.get("/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    """Display login page"""
    # Check if already logged in
    if hasattr(request, "session") and request.session.get("user_id"):
        return RedirectResponse(url="/admin/dashboard", status_code=303)
    
    return templates.TemplateResponse(
        "admin/login.html",
        {"request": request}
    )


@router.post("/login")
async def admin_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle login form submission with proper authentication"""
    
    # Find user by username
    user = db.query(User).filter(User.username == username).first()
    
    # Check if user exists
    if not user:
        return RedirectResponse(
            url="/admin/login?error=Invalid username or password",
            status_code=303
        )
    
    # Check if user is active
    if not user.is_active:
        return RedirectResponse(
            url="/admin/login?error=Account is disabled",
            status_code=303
        )
    
    # Verify password
    if not verify_password(password, user.password_hash):
        return RedirectResponse(
            url="/admin/login?error=Invalid username or password",
            status_code=303
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Set session (if SessionMiddleware is enabled)
    if hasattr(request, "session"):
        request.session["user_id"] = user.id
        request.session["username"] = user.username
        request.session["full_name"] = user.full_name or user.username
    
    # Redirect to dashboard
    return RedirectResponse(url="/admin/dashboard", status_code=303)


@router.get("/logout")
async def admin_logout(request: Request):
    """Logout admin and clear session"""
    # Clear session if available
    if hasattr(request, "session"):
        request.session.clear()
    
    return RedirectResponse(url="/admin/login", status_code=303)


@router.get("/profile", response_class=HTMLResponse)
async def admin_profile(request: Request, db: Session = Depends(get_db)):
    """Halaman profile admin"""
    current_user = get_current_user(request, db)
    
    return templates.TemplateResponse(
        "admin/profile.html",
        {
            "request": request,
            "current_user": current_user
        }
    )


@router.post("/profile/change-password")
async def admin_change_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle change password"""
    current_user = get_current_user(request, db)
    
    # Validate new password
    if new_password != confirm_password:
        return RedirectResponse(
            url="/admin/profile?error=New passwords do not match",
            status_code=303
        )
    
    # Verify current password
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user or not verify_password(current_password, user.password_hash):
        return RedirectResponse(
            url="/admin/profile?error=Current password is incorrect",
            status_code=303
        )
    
    # Update password
    user.password_hash = get_password_hash(new_password)
    db.commit()
    
    return RedirectResponse(
        url="/admin/profile?message=Password changed successfully",
        status_code=303
    )
