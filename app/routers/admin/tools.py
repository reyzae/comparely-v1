"""
Admin Tools Router
Handles admin tools and utilities.
"""

from fastapi import APIRouter, Depends, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models import Phone, Category
from .auth import get_current_user
from app.core.rbac_context import add_rbac_to_context

import csv
import io
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


@router.post("/tools/import-csv")
async def import_devices_csv(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Import devices from CSV file"""
    try:
        # Read CSV file
        contents = await file.read()
        csv_data = contents.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(csv_data))
        
        imported_count = 0
        for row in csv_reader:
            # Create device from CSV row
            device = Phone(
                name=row.get('name'),
                brand=row.get('brand'),
                category_id=int(row.get('category_id', 1)),
                cpu=row.get('cpu'),
                gpu=row.get('gpu'),
                ram=row.get('ram'),
                storage=row.get('storage'),
                camera=row.get('camera'),
                battery=row.get('battery'),
                screen=row.get('screen'),
                release_year=int(row.get('release_year')) if row.get('release_year') else None,
                price=float(row.get('price')) if row.get('price') else None,
                image_url=row.get('image_url'),
                description=row.get('description')
            )
            db.add(device)
            imported_count += 1
        
        db.commit()
        logger.info(f"Imported {imported_count} devices from CSV")
        
        return RedirectResponse(
            url=f"/admin/tools?message=Successfully imported {imported_count} devices",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error importing CSV: {e}")
        return RedirectResponse(
            url=f"/admin/tools?error=Failed to import CSV: {str(e)}",
            status_code=303
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
