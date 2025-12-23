"""
Admin Bulk Operations Router
Handles bulk operations on devices and categories.
"""

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models import Phone, Category
from .auth import get_current_user
from app.core.rbac_context import add_rbac_to_context

import logging

# Setup templates
templates = Jinja2Templates(directory="app/templates")
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(tags=["admin-bulk-operations"])


@router.get("/bulk-operations", response_class=HTMLResponse)
async def admin_bulk_operations(request: Request, db: Session = Depends(get_db)):
    """Halaman bulk operations"""
    
    categories = db.query(Category).all()
    
    current_user = get_current_user(request, db)
    rbac_context = add_rbac_to_context(current_user)

    return templates.TemplateResponse(
        "admin/bulk_operations.html",
        {
            "request": request,
            "current_user": current_user,
            **rbac_context,  # Add RBAC permissions
            "categories": categories
        }
    )


@router.post("/bulk-operations/update-category")
async def bulk_update_category(
    request: Request,
    device_ids: str = Form(...),
    new_category_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """Bulk update device category"""
    try:
        ids = [int(id.strip()) for id in device_ids.split(',') if id.strip()]
        
        updated_count = db.query(Phone).filter(
            Phone.id.in_(ids)
        ).update(
            {"category_id": new_category_id},
            synchronize_session=False
        )
        db.commit()
        
        logger.info(f"Bulk updated category for {updated_count} devices")
        
        return RedirectResponse(
            url=f"/admin/bulk-operations?message=Updated {updated_count} devices successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error in bulk update: {e}")
        return RedirectResponse(
            url="/admin/bulk-operations?error=Failed to update devices",
            status_code=303
        )


@router.post("/bulk-operations/update-price")
async def bulk_update_price(
    request: Request,
    device_ids: str = Form(...),
    price_adjustment: float = Form(...),
    adjustment_type: str = Form("percentage"),
    db: Session = Depends(get_db)
):
    """Bulk update device prices"""
    try:
        ids = [int(id.strip()) for id in device_ids.split(',') if id.strip()]
        devices = db.query(Phone).filter(Phone.id.in_(ids)).all()
        
        updated_count = 0
        for device in devices:
            if device.price:
                if adjustment_type == "percentage":
                    device.price = device.price * (1 + price_adjustment / 100)
                else:
                    device.price = device.price + price_adjustment
                updated_count += 1
        
        db.commit()
        logger.info(f"Bulk updated prices for {updated_count} devices")
        
        return RedirectResponse(
            url=f"/admin/bulk-operations?message=Updated prices for {updated_count} devices",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error in bulk price update: {e}")
        return RedirectResponse(
            url="/admin/bulk-operations?error=Failed to update prices",
            status_code=303
        )
