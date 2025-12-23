"""
Admin Devices Router
Handles device management (list, create, edit, delete, export).
"""

from typing import Optional, List
from math import ceil
from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, Body
from fastapi.responses import HTMLResponse, RedirectResponse, Response, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_
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
router = APIRouter(tags=["admin-devices"])


@router.get("/devices", response_class=HTMLResponse)
async def admin_devices(
    request: Request,
    page: int = 1,
    search: Optional[str] = None,
    category_id: Optional[str] = None,
    brand: Optional[str] = None,
    year: Optional[str] = None,
    sort: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    """Halaman devices management dengan filter dan pagination"""
    ITEMS_PER_PAGE = 20
    
    # Build query with eager loading
    query = db.query(Phone).options(joinedload(Phone.category))
    
    # Filters
    if category_id and category_id.strip():
        try:
            cat_id = int(category_id)
            query = query.filter(Phone.category_id == cat_id)
        except (ValueError, TypeError):
            pass
    
    if brand and brand.strip():
        query = query.filter(Phone.brand.ilike(f"%{brand}%"))
    
    if year and year.strip():
        try:
            year_int = int(year)
            query = query.filter(Phone.release_year == year_int)
        except (ValueError, TypeError):
            pass
    
    # Search
    if search and search.strip():
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Phone.name.ilike(search_term),
                Phone.brand.ilike(search_term)
            )
        )
    
    # Sorting
    valid_sorts = ["id", "name", "brand", "price", "release_year"]
    if sort in valid_sorts:
        order_column = getattr(Phone, sort)
        if order == "desc":
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())
    
    # Pagination
    total_items = query.count()
    total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    offset = (page - 1) * ITEMS_PER_PAGE
    devices = query.offset(offset).limit(ITEMS_PER_PAGE).all()
    
    # Get categories for filter
    categories = db.query(Category).all()
    
    # Get unique brands and years
    brands = db.query(Phone.brand).distinct().order_by(Phone.brand).all()
    brands = [b[0] for b in brands if b[0]]
    
    years = db.query(Phone.release_year).distinct().order_by(Phone.release_year.desc()).all()
    years = [y[0] for y in years if y[0]]
    
    # Get current user and RBAC context
    current_user = get_current_user(request, db)
    rbac_context = add_rbac_to_context(current_user)
    
    return templates.TemplateResponse(
        "admin/devices_list.html",
        {
            "request": request,
            "current_user": current_user,
            **rbac_context,  # Add RBAC permissions
            "devices": devices,
            "categories": categories,
            "brands": brands,
            "years": years,
            "page": page,
            "total_pages": total_pages,
            "total_items": total_items,
            "search": search,
            "category_id": category_id,
            "brand": brand,
            "year": year,
            "sort": sort,
            "order": order
        }
    )


@router.get("/devices/new", response_class=HTMLResponse)
async def admin_device_new(request: Request, db: Session = Depends(get_db)):
    """Form untuk create device baru"""
    categories = db.query(Category).all()
    return templates.TemplateResponse(
        "admin/device_form.html",
        {
            "request": request,
            "current_user": get_current_user(request, db),
            "device": None,
            "categories": categories
        }
    )


@router.get("/devices/{device_id}/edit", response_class=HTMLResponse)
async def admin_device_edit(
    request: Request,
    device_id: int,
    db: Session = Depends(get_db)
):
    """Form untuk edit device"""
    device = db.query(Phone).filter(Phone.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    categories = db.query(Category).all()
    return templates.TemplateResponse(
        "admin/device_form.html",
        {
            "request": request,
            "current_user": get_current_user(request, db),
            "device": device,
            "categories": categories
        }
    )


@router.get("/devices/export")
async def admin_devices_export(db: Session = Depends(get_db)):
    """Export devices to CSV"""
    devices = db.query(Phone).all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'ID', 'Name', 'Brand', 'Category', 'CPU', 'GPU', 'RAM', 'Storage',
        'Camera', 'Battery', 'Screen', 'Release Year', 'Price', 'Image URL', 'Description'
    ])
    
    # Write data
    for device in devices:
        category_name = device.category.name if device.category else 'N/A'
        writer.writerow([
            device.id, device.name, device.brand, category_name,
            device.cpu or '', device.gpu or '', device.ram or '',
            device.storage or '', device.camera or '', device.battery or '',
            device.screen or '', device.release_year or '', device.price or '',
            device.image_url or '', device.description or ''
        ])
    
    # Prepare response
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=devices_export.csv"}
    )


# ============================================
# POST Routes (Form Submissions)
# ============================================

@router.post("/devices/new")
async def admin_device_create(
    request: Request,
    name: str = Form(...),
    brand: str = Form(...),
    category_id: int = Form(...),
    cpu: str = Form(None),
    gpu: str = Form(None),
    ram: str = Form(None),
    storage: str = Form(None),
    camera: str = Form(None),
    battery: str = Form(None),
    screen: str = Form(None),
    release_year: int = Form(None),
    price: float = Form(None),
    image_url: str = Form(None),
    description: str = Form(None),
    db: Session = Depends(get_db)
):
    """Create new device"""
    try:
        device = Phone(
            name=name, brand=brand, category_id=category_id,
            cpu=cpu, gpu=gpu, ram=ram, storage=storage,
            camera=camera, battery=battery, screen=screen,
            release_year=release_year, price=price,
            image_url=image_url, description=description
        )
        db.add(device)
        db.commit()
        return RedirectResponse(
            url="/admin/devices?message=Device created successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error creating device: {e}")
        return RedirectResponse(
            url=f"/admin/devices?error={str(e)}",
            status_code=303
        )


@router.post("/devices/{device_id}/edit")
async def admin_device_update(
    request: Request,
    device_id: int,
    name: str = Form(...),
    brand: str = Form(...),
    category_id: int = Form(...),
    cpu: str = Form(None),
    gpu: str = Form(None),
    ram: str = Form(None),
    storage: str = Form(None),
    camera: str = Form(None),
    battery: str = Form(None),
    screen: str = Form(None),
    release_year: int = Form(None),
    price: float = Form(None),
    image_url: str = Form(None),
    description: str = Form(None),
    db: Session = Depends(get_db)
):
    """Update device"""
    try:
        device = db.query(Phone).filter(Phone.id == device_id).first()
        if not device:
            return RedirectResponse(
                url="/admin/devices?error=Device not found",
                status_code=303
            )
        
        device.name = name
        device.brand = brand
        device.category_id = category_id
        device.cpu = cpu
        device.gpu = gpu
        device.ram = ram
        device.storage = storage
        device.camera = camera
        device.battery = battery
        device.screen = screen
        device.release_year = release_year
        device.price = price
        device.image_url = image_url
        device.description = description
        
        db.commit()
        return RedirectResponse(
            url="/admin/devices?message=Device updated successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error updating device: {e}")
        return RedirectResponse(
            url=f"/admin/devices?error={str(e)}",
            status_code=303
        )


@router.post("/devices/{device_id}/delete")
async def admin_device_delete(device_id: int, db: Session = Depends(get_db)):
    """Delete device"""
    try:
        device = db.query(Phone).filter(Phone.id == device_id).first()
        if not device:
            return RedirectResponse(
                url="/admin/devices?error=Device not found",
                status_code=303
            )
        
        db.delete(device)
        db.commit()
        return RedirectResponse(
            url="/admin/devices?message=Device deleted successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error deleting device: {e}")
        return RedirectResponse(
            url=f"/admin/devices?error={str(e)}",
            status_code=303
        )


@router.post("/devices/bulk-delete")
async def admin_devices_bulk_delete(
    request: Request,
    device_ids: str = Form(...),
    db: Session = Depends(get_db)
):
    """Bulk delete devices"""
    try:
        ids = [int(id.strip()) for id in device_ids.split(',') if id.strip()]
        deleted_count = db.query(Phone).filter(
            Phone.id.in_(ids)
        ).delete(synchronize_session=False)
        db.commit()
        
        logger.info(f"Bulk deleted {deleted_count} devices")
        return RedirectResponse(
            url=f"/admin/devices?message=Deleted {deleted_count} devices successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error bulk deleting devices: {e}")
        return RedirectResponse(
            url="/admin/devices?error=Failed to delete devices",
            status_code=303
        )


@router.post("/devices/import")
async def import_devices_json(
    request: Request,
    data: dict = Body(...),
    db: Session = Depends(get_db)
):
    """Import devices from JSON (from CSV upload in tools page)"""
    try:
        devices_data = data.get("devices", [])
        if not devices_data:
            return JSONResponse(
                status_code=400,
                content={"detail": "No devices data provided"}
            )
        
        imported_count = 0
        errors = []
        
        for idx, device_data in enumerate(devices_data):
            try:
                # Create device from data
                device = Phone(
                    name=device_data.get('name'),
                    brand=device_data.get('brand'),
                    category_id=int(device_data.get('category_id', 1)),
                    cpu=device_data.get('cpu'),
                    gpu=device_data.get('gpu'),
                    ram=device_data.get('ram'),
                    storage=device_data.get('storage'),
                    camera=device_data.get('camera'),
                    battery=device_data.get('battery'),
                    screen=device_data.get('screen'),
                    release_year=int(device_data.get('release_year')) if device_data.get('release_year') else None,
                    price=float(device_data.get('price')) if device_data.get('price') else None,
                    image_url=device_data.get('image_url'),
                    description=device_data.get('description')
                )
                db.add(device)
                imported_count += 1
            except Exception as e:
                errors.append(f"Row {idx + 1}: {str(e)}")
                logger.error(f"Error importing device at row {idx + 1}: {e}")
        
        db.commit()
        logger.info(f"Imported {imported_count} devices via JSON")
        
        return JSONResponse(
            status_code=200,
            content={
                "imported": imported_count,
                "errors": errors,
                "message": f"Successfully imported {imported_count} devices"
            }
        )
    except Exception as e:
        logger.exception(f"Error importing devices: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Import failed: {str(e)}"}
        )
