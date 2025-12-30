"""
Admin Tools Router
Handles admin tools and utilities.
"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.deps import get_db
from .auth import get_current_user
from app.core.rbac_context import add_rbac_to_context

import logging

# Setup templates
templates = Jinja2Templates(directory="app/templates")
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(tags=["admin-tools"])


@router.get("/tools", response_class=HTMLResponse)
async def admin_tools(request: Request, db: Session = Depends(get_db)):
    """Halaman admin tools"""
    current_user = get_current_user(request, db)
    rbac_context = add_rbac_to_context(current_user)

    return templates.TemplateResponse(
        "admin/tools.html",
        {
            "request": request,
            "current_user": current_user,
            **rbac_context,  # Add RBAC permissions
        }
    )





@router.post("/tools/clear-cache")
async def clear_cache(request: Request, db: Session = Depends(get_db)):
    """Clear application cache"""
    try:
        # Placeholder for cache clearing logic
        logger.info("Cache cleared")
        return RedirectResponse(
            url="/admin/tools?message=Cache cleared successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error clearing cache: {e}")
        return RedirectResponse(
            url=f"/admin/tools?error=Failed to clear cache",
            status_code=303
        )
