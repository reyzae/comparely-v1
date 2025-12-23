"""
Admin Categories Router
Handles category management (list, create, edit, delete).
"""

from math import ceil
from fastapi import APIRouter, Depends, Request, Form, HTTPException
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
router = APIRouter(tags=["admin-categories"])


@router.get("/categories", response_class=HTMLResponse)
async def admin_categories(
    request: Request,
    page: int = 1,
    search: str = None,
    sort: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    """Halaman categories management"""
    ITEMS_PER_PAGE = 20
    
    # Build query
    query = db.query(Category)
    
    # Search
    if search:
        query = query.filter(Category.name.ilike(f"%{search}%"))
    
    # Sorting
    sort_column = getattr(Category, sort, Category.id)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    # Count total
    total_items = query.count()
    total_pages = ceil(total_items / ITEMS_PER_PAGE) if total_items > 0 else 1
    
    # Paginate
    offset = (page - 1) * ITEMS_PER_PAGE
    categories = query.offset(offset).limit(ITEMS_PER_PAGE).all()
    
    # Get device count per category
    category_stats = []
    for cat in categories:
        device_count = db.query(Phone).filter(Phone.category_id == cat.id).count()
        category_stats.append({
            "category": cat,
            "device_count": device_count
        })
    
    current_user = get_current_user(request, db)
    rbac_context = add_rbac_to_context(current_user)

    return templates.TemplateResponse(
        "admin/categories_list.html",
        {
            "request": request,
            "current_user": current_user,
            **rbac_context,  # Add RBAC permissions
            "category_stats": category_stats,
            "page": page,
            "total_pages": total_pages,
            "search": search or "",
            "sort": sort,
            "order": order
        }
    )


@router.get("/categories/new", response_class=HTMLResponse)
async def admin_category_new(request: Request, db: Session = Depends(get_db)):
    """Form untuk create category baru"""
    current_user = get_current_user(request, db)
    rbac_context = add_rbac_to_context(current_user)

    return templates.TemplateResponse(
        "admin/category_form.html",
        {
            "request": request,
            "current_user": current_user,
            **rbac_context,  # Add RBAC permissions
            "category": None
        }
    )


@router.get("/categories/{category_id}/edit", response_class=HTMLResponse)
async def admin_category_edit(
    request: Request,
    category_id: int,
    db: Session = Depends(get_db)
):
    """Form untuk edit category"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    current_user = get_current_user(request, db)
    rbac_context = add_rbac_to_context(current_user)

    return templates.TemplateResponse(
        "admin/category_form.html",
        {
            "request": request,
            "current_user": current_user,
            **rbac_context,  # Add RBAC permissions
            "category": category
        }
    )


# ============================================
# POST Routes (Form Submissions)
# ============================================

@router.post("/categories/new")
async def admin_category_create(
    request: Request,
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    """Create new category"""
    try:
        category = Category(name=name)
        db.add(category)
        db.commit()
        return RedirectResponse(
            url="/admin/categories?message=Category created successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error creating category: {e}")
        return RedirectResponse(
            url=f"/admin/categories?error={str(e)}",
            status_code=303
        )


@router.post("/categories/{category_id}/edit")
async def admin_category_update(
    request: Request,
    category_id: int,
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    """Update category"""
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            return RedirectResponse(
                url="/admin/categories?error=Category not found",
                status_code=303
            )
        
        category.name = name
        db.commit()
        return RedirectResponse(
            url="/admin/categories?message=Category updated successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error updating category: {e}")
        return RedirectResponse(
            url=f"/admin/categories?error={str(e)}",
            status_code=303
        )


@router.post("/categories/{category_id}/delete")
async def admin_category_delete(category_id: int, db: Session = Depends(get_db)):
    """Delete category"""
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            return RedirectResponse(
                url="/admin/categories?error=Category not found",
                status_code=303
            )
        
        # Check if category has devices
        device_count = db.query(Phone).filter(Phone.category_id == category_id).count()
        if device_count > 0:
            return RedirectResponse(
                url=f"/admin/categories?error=Cannot delete category with {device_count} devices",
                status_code=303
            )
        
        db.delete(category)
        db.commit()
        return RedirectResponse(
            url="/admin/categories?message=Category deleted successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error deleting category: {e}")
        return RedirectResponse(
            url=f"/admin/categories?error={str(e)}",
            status_code=303
        )


@router.post("/categories/bulk-delete")
async def admin_categories_bulk_delete(
    request: Request,
    category_ids: str = Form(...),
    db: Session = Depends(get_db)
):
    """Bulk delete categories"""
    try:
        # Parse IDs
        ids = [int(id.strip()) for id in category_ids.split(',') if id.strip()]
        
        # Check if any category has devices
        for cat_id in ids:
            device_count = db.query(Phone).filter(Phone.category_id == cat_id).count()
            if device_count > 0:
                category = db.query(Category).filter(Category.id == cat_id).first()
                cat_name = category.name if category else f"ID {cat_id}"
                return RedirectResponse(
                    url=f"/admin/categories?error=Cannot delete category '{cat_name}' with {device_count} devices",
                    status_code=303
                )
        
        # Delete categories
        deleted_count = db.query(Category).filter(
            Category.id.in_(ids)
        ).delete(synchronize_session=False)
        db.commit()
        
        logger.info(f"Bulk deleted {deleted_count} categories")
        return RedirectResponse(
            url=f"/admin/categories?message=Deleted {deleted_count} categories successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error bulk deleting categories: {e}")
        return RedirectResponse(
            url="/admin/categories?error=Failed to delete categories",
            status_code=303
        )
