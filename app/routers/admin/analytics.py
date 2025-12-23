"""
Admin Analytics Router
Handles analytics and reporting features.
"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.core.deps import get_db
from app.models import Phone, Category, User
from .auth import get_current_user
from app.core.rbac_context import add_rbac_to_context

from datetime import datetime, timedelta

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Create router
router = APIRouter(tags=["admin-analytics"])


@router.get("/analytics", response_class=HTMLResponse)
async def admin_analytics(request: Request, db: Session = Depends(get_db)):
    """Halaman analytics dengan charts dan reports"""
    
    # Get device statistics by year
    devices_by_year = db.query(
        Phone.release_year,
        func.count(Phone.id).label('count')
    ).group_by(Phone.release_year).order_by(Phone.release_year.desc()).limit(5).all()
    
    # Get devices by category
    devices_by_category = db.query(
        Category.name,
        func.count(Phone.id).label('count')
    ).join(Phone).group_by(Category.name).all()
    
    # Get devices by brand (top 10) with details
    brand_stats = db.query(
        Phone.brand,
        func.count(Phone.id).label('count')
    ).group_by(Phone.brand).order_by(func.count(Phone.id).desc()).limit(10).all()
    
    # Create brand details dictionary
    brand_details = {}
    for brand, count in brand_stats:
        brand_details[brand] = {
            'count': count,
            'avg_price': db.query(func.avg(Phone.price)).filter(
                Phone.brand == brand,
                Phone.price.isnot(None)
            ).scalar() or 0
        }
    
    # Get price statistics
    price_stats = db.query(
        func.avg(Phone.price).label('avg_price'),
        func.min(Phone.price).label('min_price'),
        func.max(Phone.price).label('max_price')
    ).filter(Phone.price.isnot(None)).first()
    
    # Total counts
    total_devices = db.query(Phone).count()
    total_categories = db.query(Category).count()
    total_brands = db.query(Phone.brand).distinct().count()
    
    # Prepare data for charts
    year_stats = {str(year): count for year, count in devices_by_year}
    category_stats = {name: count for name, count in devices_by_category}
    
    # Price ranges for chart
    price_ranges = {
        "< 5 juta": db.query(Phone).filter(Phone.price < 5000000).count(),
        "5-10 juta": db.query(Phone).filter(Phone.price.between(5000000, 10000000)).count(),
        "10-15 juta": db.query(Phone).filter(Phone.price.between(10000000, 15000000)).count(),
        "15-20 juta": db.query(Phone).filter(Phone.price.between(15000000, 20000000)).count(),
        "> 20 juta": db.query(Phone).filter(Phone.price > 20000000).count()
    }
    
    current_user = get_current_user(request, db)
    rbac_context = add_rbac_to_context(current_user)

    return templates.TemplateResponse(
        "admin/analytics.html",
        {
            "request": request,
            "current_user": current_user,
            **rbac_context,  # Add RBAC permissions
            "total_devices": total_devices,
            "total_categories": total_categories,
            "total_brands": total_brands,
            "devices_by_year": devices_by_year,
            "devices_by_category": devices_by_category,
            "devices_by_brand": brand_stats,
            "brand_details": brand_details,
            "price_stats": price_stats,
            "year_stats": year_stats,
            "category_stats": category_stats,
            "price_ranges": price_ranges
        }
    )
