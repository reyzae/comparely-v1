"""
Admin Dashboard Router
Handles dashboard display with statistics and charts.
"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models import Phone, Category
from .auth import get_current_user
from app.core.rbac_context import add_rbac_to_context
  # Import get_current_user

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Create router
router = APIRouter(tags=["admin-dashboard"])


@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    """Halaman dashboard admin dengan statistik"""
    # Get stats untuk dashboard
    phone_count = db.query(Phone).count()
    category_count = db.query(Category).count()
    
    # Get brands
    brands = db.query(Phone.brand).distinct().all()
    brand_count = len(brands)
    
    # Get latest year
    latest_year = db.query(Phone.release_year).order_by(
        Phone.release_year.desc()
    ).first()
    
    # Category stats untuk pie chart
    category_stats = {}
    categories = db.query(Category).all()
    for cat in categories:
        count = db.query(Phone).filter(Phone.category_id == cat.id).count()
        category_stats[cat.name] = count
    
    # Brand stats untuk bar chart
    brand_stats = {}
    for (brand,) in brands:
        count = db.query(Phone).filter(Phone.brand == brand).count()
        brand_stats[brand] = count
    
    current_user = get_current_user(request, db)
    rbac_context = add_rbac_to_context(current_user)

    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
            "current_user": current_user,  # Add current_user
            **rbac_context,  # Add RBAC permissions
            "total_devices": phone_count,
            "total_categories": category_count,
            "total_brands": brand_count,
            "latest_device_year": latest_year[0] if latest_year else "N/A",
            "category_stats": category_stats,
            "brand_stats": brand_stats
        }
    )
