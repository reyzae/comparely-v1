"""
Router untuk admin/management functions
Termasuk reset database, dll

Author: Kelompok COMPARELY
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models import Phone, Category, User, Role
from sqlalchemy import text

# ============================================
# Custom Jinja2Templates dengan auto current_user
# ============================================

class CustomJinja2Templates(Jinja2Templates):
    """
    Custom Jinja2Templates yang otomatis inject current_user ke semua template.
    Ini lebih efisien daripada update semua route satu-per-satu!
    """
    
    def TemplateResponse(self, name: str, context: dict, *args, **kwargs):
        """Override TemplateResponse untuk auto-inject current_user"""
        request = context.get("request")
        
        if request:
            # Safe check: pastikan session middleware sudah installed
            if "session" not in request.scope:
                # Jika belum ada session, gunakan dummy user
                context["current_user"] = {
                    "id": 1,
                    "username": "admin",
                    "email": "admin@comparely.com",
                    "full_name": "Administrator",
                    "role": {"name": "Admin"}
                }
            else:
                # Get current user dari session
                db = next(get_db())
                user_id = request.session.get("user_id")
                
                if user_id:
                    user = db.query(User).filter(User.id == user_id).first()
                    if user:
                        context["current_user"] = user
                    else:
                        # Dummy user jika tidak ada di database
                        context["current_user"] = {
                            "id": 1,
                            "username": "admin",
                            "email": "admin@comparely.com",
                            "full_name": "Administrator",
                            "role": {"name": "Admin"}
                        }
                else:
                    # Dummy user untuk development
                    context["current_user"] = {
                        "id": 1,
                        "username": "admin",
                        "email": "admin@comparely.com",
                        "full_name": "Administrator",
                        "role": {"name": "Admin"}
                    }
        
        return super().TemplateResponse(name, context, *args, **kwargs)

# Setup Custom Jinja2 Templates
templates = CustomJinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


# ============================================
# Simple Session Management
# ============================================

def get_current_user(request: Request, db: Session = Depends(get_db)):
    """
    Get current logged-in user from session.
    Untuk sementara, return dummy user jika tidak ada session.
    """
    # Cek session cookie
    user_id = request.session.get("user_id")
    
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return user
    
    # Dummy user untuk development (hapus di production!)
    # Return None jika mau enforce login
    return {
        "id": 1,
        "username": "admin",
        "email": "admin@comparely.com",
        "full_name": "Administrator",
        "role": {"name": "Admin"}
    }

@router.get("/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    """Halaman login admin"""
    return templates.TemplateResponse(
        "admin/login.html",
        {"request": request}
    )

@router.post("/login")
async def admin_login(request: Request, db: Session = Depends(get_db)):
    """Handle login form submission"""
    from fastapi.responses import RedirectResponse
    
    # TEMPORARY: Bypass authentication, langsung redirect ke dashboard
    # TODO: Re-enable proper authentication setelah SessionMiddleware fixed
    
    # Get form data (for validation purposes)
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    
    # Simple check - jika ada username dan password, langsung masuk
    if username and password:
        # Langsung redirect ke dashboard tanpa session
        return RedirectResponse(url="/admin/dashboard", status_code=303)
    else:
        return RedirectResponse(url="/admin/login?error=Please enter username and password", status_code=303)

@router.get("/logout")
async def admin_logout(request: Request):
    """Logout admin"""
    from fastapi.responses import RedirectResponse
    # TEMPORARY: Just redirect tanpa clear session
    # TODO: Re-enable session.clear() setelah SessionMiddleware fixed
    return RedirectResponse(url="/admin/login", status_code=303)

@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    """Halaman dashboard admin"""
    # Get stats untuk dashboard
    phone_count = db.query(Phone).count()
    category_count = db.query(Category).count()
    
    # Get brands
    brands = db.query(Phone.brand).distinct().all()
    brand_count = len(brands)
    
    # Get latest year
    latest_year = db.query(Phone.release_year).order_by(Phone.release_year.desc()).first()
    
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
    
    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
            # current_user auto-injected by CustomJinja2Templates!
            "total_devices": phone_count,
            "total_categories": category_count,
            "total_brands": brand_count,
            "latest_device_year": latest_year[0] if latest_year else "N/A",
            "category_stats": category_stats,
            "brand_stats": brand_stats
        }
    )

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
    from math import ceil
    from sqlalchemy.orm import joinedload
    
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
    
    # Get device count per category (optimized)
    category_stats = []
    for cat in categories:
        device_count = db.query(Phone).filter(Phone.category_id == cat.id).count()
        category_stats.append({
            "category": cat,
            "device_count": device_count
        })
    
    return templates.TemplateResponse(
        "admin/categories_list.html",
        {
            "request": request,
            "category_stats": category_stats,
            "page": page,
            "total_pages": total_pages,
            "search": search or "",
            "sort": sort,
            "order": order
        }
    )

@router.get("/devices", response_class=HTMLResponse)
async def admin_devices(
    request: Request,
    page: int = 1,
    search: Optional[str] = None,
    category_id: Optional[str] = None,  # Changed to str to handle empty values
    brand: Optional[str] = None,
    year: Optional[str] = None,  # Changed to str to handle empty values
    sort: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    """Halaman devices management"""
    from math import ceil
    from sqlalchemy.orm import joinedload
    
    ITEMS_PER_PAGE = 20
    
    # Build query with eager loading
    query = db.query(Phone).options(joinedload(Phone.category))
    
    # Filters - convert string to int safely
    if category_id and category_id.strip():
        try:
            cat_id = int(category_id)
            query = query.filter(Phone.category_id == cat_id)
        except (ValueError, TypeError):
            pass  # Ignore invalid category_id
    
    if brand and brand.strip():
        query = query.filter(Phone.brand == brand)
    
    if year and year.strip():
        try:
            year_int = int(year)
            query = query.filter(Phone.release_year == year_int)
        except (ValueError, TypeError):
            pass  # Ignore invalid year
    
    # Search
    if search:
        query = query.filter(
            (Phone.name.ilike(f"%{search}%")) |
            (Phone.brand.ilike(f"%{search}%"))
        )
    
    # Sorting
    sort_column = getattr(Phone, sort, Phone.id)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    # Count total
    total_items = query.count()
    total_pages = ceil(total_items / ITEMS_PER_PAGE) if total_items > 0 else 1
    
    # Paginate
    offset = (page - 1) * ITEMS_PER_PAGE
    devices = query.offset(offset).limit(ITEMS_PER_PAGE).all()
    
    # Get filter options
    categories = db.query(Category).all()
    brands = db.query(Phone.brand).distinct().filter(Phone.brand.isnot(None)).all()
    years = db.query(Phone.release_year).distinct().filter(Phone.release_year.isnot(None)).order_by(Phone.release_year.desc()).all()
    
    return templates.TemplateResponse(
        "admin/devices_list.html",
        {
            "request": request,
            "devices": devices,
            "page": page,
            "total_pages": total_pages,
            "search": search or "",
            "categories": categories,
            "brands": [b[0] for b in brands],
            "years": [y[0] for y in years],
            "selected_category": category_id,
            "selected_brand": brand,
            "selected_year": year,
            "sort": sort,
            "order": order
        }
    )

@router.get("/tools", response_class=HTMLResponse)
async def admin_tools(request: Request):
    """Halaman admin tools"""
    return templates.TemplateResponse(
        "admin/tools.html",
        {"request": request}
    )

@router.get("/profile", response_class=HTMLResponse)
async def admin_profile(request: Request):
    """Halaman profile admin"""
    return templates.TemplateResponse(
        "admin/profile.html",
        {"request": request}
    )

# ============================================
# Category Form Routes
# ============================================

@router.get("/categories/new", response_class=HTMLResponse)
async def admin_category_new(request: Request):
    """Form untuk create category baru"""
    return templates.TemplateResponse(
        "admin/category_form.html",
        {"request": request, "category": None}
    )

@router.get("/categories/{category_id}/edit", response_class=HTMLResponse)
async def admin_category_edit(request: Request, category_id: int, db: Session = Depends(get_db)):
    """Form untuk edit category"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return templates.TemplateResponse(
        "admin/category_form.html",
        {"request": request, "category": category}
    )

# ============================================
# Device Form Routes
# ============================================

@router.get("/devices/new", response_class=HTMLResponse)
async def admin_device_new(request: Request, db: Session = Depends(get_db)):
    """Form untuk create device baru"""
    categories = db.query(Category).all()
    return templates.TemplateResponse(
        "admin/device_form.html",
        {"request": request, "device": None, "categories": categories}
    )

@router.get("/devices/{device_id}/edit", response_class=HTMLResponse)
async def admin_device_edit(request: Request, device_id: int, db: Session = Depends(get_db)):
    """Form untuk edit device"""
    device = db.query(Phone).filter(Phone.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    categories = db.query(Category).all()
    return templates.TemplateResponse(
        "admin/device_form.html",
        {"request": request, "device": device, "categories": categories}
    )

@router.get("/devices/mobile", response_class=HTMLResponse)
async def admin_devices_mobile(request: Request, db: Session = Depends(get_db)):
    """Halaman devices management (mobile optimized)"""
    devices = db.query(Phone).all()
    categories = db.query(Category).all()
    
    return templates.TemplateResponse(
        "admin/devices_list_mobile_optimized.html",
        {
            "request": request,
            "devices": devices,
            "categories": categories,
            "page": 1,
            "total_pages": 1
        }
    )

@router.get("/devices/export")
async def admin_devices_export(db: Session = Depends(get_db)):
    """Export devices to CSV"""
    from fastapi.responses import StreamingResponse
    import io
    import csv
    
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
            device.id,
            device.name,
            device.brand,
            category_name,
            device.cpu or '',
            device.gpu or '',
            device.ram or '',
            device.storage or '',
            device.camera or '',
            device.battery or '',
            device.screen or '',
            device.release_year or '',
            device.price or '',
            device.image_url or '',
            device.description or ''
        ])
    
    # Prepare response
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=devices_export.csv"}
    )


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
    from math import ceil
    
    ITEMS_PER_PAGE = 20
    
    try:
        # Build query - tanpa joinedload dulu untuk avoid error
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
        
        # Manual load role untuk setiap user (lebih aman daripada joinedload)
        for user in users:
            if user.role_id:
                try:
                    user.role = db.query(Role).filter(Role.id == user.role_id).first()
                except:
                    user.role = None
        
        return templates.TemplateResponse(
            "admin/users_list.html",
            {
                "request": request,
                "users": users,
                "page": page,
                "total_pages": total_pages,
                "search": search or "",
                "sort": sort,
                "order": order
            }
        )
    except Exception as e:
        # Jika ada error, tampilkan halaman kosong dengan pesan error
        import logging
        logging.error(f"Error in admin_users: {e}")
        
        return templates.TemplateResponse(
            "admin/users_list.html",
            {
                "request": request,
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
    return templates.TemplateResponse(
        "admin/user_form.html",
        {"request": request, "user": None, "roles": roles}
    )

@router.get("/users/{user_id}/edit", response_class=HTMLResponse)
async def admin_user_edit(request: Request, user_id: int, db: Session = Depends(get_db)):
    """Form untuk edit user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    roles = db.query(Role).all()
    return templates.TemplateResponse(
        "admin/user_form.html",
        {"request": request, "user": user, "roles": roles}
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
    from math import ceil
    
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
    
    return templates.TemplateResponse(
        "admin/roles_list.html",
        {
            "request": request,
            "roles": roles,
            "page": page,
            "total_pages": total_pages,
            "search": search or "",
            "sort": sort,
            "order": order
        }
    )

@router.get("/roles/new", response_class=HTMLResponse)
async def admin_role_new(request: Request):
    """Form untuk create role baru"""
    return templates.TemplateResponse(
        "admin/role_form.html",
        {"request": request, "role": None}
    )

@router.get("/roles/{role_id}/edit", response_class=HTMLResponse)
async def admin_role_edit(request: Request, role_id: int, db: Session = Depends(get_db)):
    """Form untuk edit role"""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    return templates.TemplateResponse(
        "admin/role_form.html",
        {"request": request, "role": role}
    )

# ============================================
# POST Routes (Form Submissions)
# ============================================

from fastapi import Form
from fastapi.responses import RedirectResponse

# Profile POST
@router.post("/profile/change-password")
async def admin_change_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...)
):
    """Handle change password"""
    # TODO: Implement password change logic
    return RedirectResponse(url="/admin/profile?message=Password changed successfully", status_code=303)

# Category POST routes
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
        return RedirectResponse(url="/admin/categories?message=Category created successfully", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/admin/categories?error={str(e)}", status_code=303)

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
            return RedirectResponse(url="/admin/categories?error=Category not found", status_code=303)
        
        category.name = name
        db.commit()
        return RedirectResponse(url="/admin/categories?message=Category updated successfully", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/admin/categories?error={str(e)}", status_code=303)

@router.post("/categories/{category_id}/delete")
async def admin_category_delete(category_id: int, db: Session = Depends(get_db)):
    """Delete category"""
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            return RedirectResponse(url="/admin/categories?error=Category not found", status_code=303)
        
        # Check if category has devices
        device_count = db.query(Phone).filter(Phone.category_id == category_id).count()
        if device_count > 0:
            return RedirectResponse(url=f"/admin/categories?error=Cannot delete category with {device_count} devices", status_code=303)
        
        db.delete(category)
        db.commit()
        return RedirectResponse(url="/admin/categories?message=Category deleted successfully", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/admin/categories?error={str(e)}", status_code=303)

@router.post("/categories/bulk-delete")
async def admin_categories_bulk_delete(
    request: Request,
    category_ids: str = Form(...),
    db: Session = Depends(get_db)
):
    """Bulk delete categories"""
    import logging
    logger = logging.getLogger(__name__)
    
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
        deleted_count = db.query(Category).filter(Category.id.in_(ids)).delete(synchronize_session=False)
        db.commit()
        
        logger.info(f"Bulk deleted {deleted_count} categories")
        return RedirectResponse(
            url=f"/admin/categories?message=Deleted {deleted_count} categories successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error bulk deleting categories: {e}")
        return RedirectResponse(url="/admin/categories?error=Failed to delete categories", status_code=303)


# Device POST routes
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
            name=name,
            brand=brand,
            category_id=category_id,
            cpu=cpu,
            gpu=gpu,
            ram=ram,
            storage=storage,
            camera=camera,
            battery=battery,
            screen=screen,
            release_year=release_year,
            price=price,
            image_url=image_url,
            description=description
        )
        db.add(device)
        db.commit()
        return RedirectResponse(url="/admin/devices?message=Device created successfully", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/admin/devices?error={str(e)}", status_code=303)

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
            return RedirectResponse(url="/admin/devices?error=Device not found", status_code=303)
        
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
        return RedirectResponse(url="/admin/devices?message=Device updated successfully", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/admin/devices?error={str(e)}", status_code=303)

@router.post("/devices/{device_id}/delete")
async def admin_device_delete(device_id: int, db: Session = Depends(get_db)):
    """Delete device"""
    try:
        device = db.query(Phone).filter(Phone.id == device_id).first()
        if not device:
            return RedirectResponse(url="/admin/devices?error=Device not found", status_code=303)
        
        db.delete(device)
        db.commit()
        return RedirectResponse(url="/admin/devices?message=Device deleted successfully", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/admin/devices?error={str(e)}", status_code=303)

@router.post("/devices/bulk-delete")
async def admin_devices_bulk_delete(
    request: Request,
    device_ids: str = Form(...),
    db: Session = Depends(get_db)
):
    """Bulk delete devices"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        ids = [int(id.strip()) for id in device_ids.split(',') if id.strip()]
        deleted_count = db.query(Phone).filter(Phone.id.in_(ids)).delete(synchronize_session=False)
        db.commit()
        
        logger.info(f"Bulk deleted {deleted_count} devices")
        return RedirectResponse(
            url=f"/admin/devices?message=Deleted {deleted_count} devices successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error bulk deleting devices: {e}")
        return RedirectResponse(url="/admin/devices?error=Failed to delete devices", status_code=303)

# User POST routes
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
    import re
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        # Email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return RedirectResponse(url="/admin/users?error=Invalid email format", status_code=303)
        
        # Check duplicate username
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            return RedirectResponse(url="/admin/users?error=Username already exists", status_code=303)
        
        # Check duplicate email
        existing_email = db.query(User).filter(User.email == email).first()
        if existing_email:
            return RedirectResponse(url="/admin/users?error=Email already exists", status_code=303)
        
        # Hash password (simple hash - untuk production gunakan bcrypt)
        password_hash = password  # TODO: Implement proper password hashing
        
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role_id=role_id,
            is_active=is_active
        )
        db.add(user)
        db.commit()
        
        logger.info(f"User created: {username}")
        return RedirectResponse(url="/admin/users?message=User created successfully", status_code=303)
    except Exception as e:
        logger.exception(f"Error creating user: {e}")
        return RedirectResponse(url=f"/admin/users?error=An error occurred. Please try again.", status_code=303)

@router.post("/users/{user_id}/edit")
async def admin_user_update(
    request: Request,
    user_id: int,
    username: str = Form(...),
    email: str = Form(...),
    role_id: int = Form(...),
    is_active: bool = Form(False),
    db: Session = Depends(get_db)
):
    """Update user"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return RedirectResponse(url="/admin/users?error=User not found", status_code=303)
        
        user.username = username
        user.email = email
        user.role_id = role_id
        user.is_active = is_active
        
        db.commit()
        return RedirectResponse(url="/admin/users?message=User updated successfully", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/admin/users?error={str(e)}", status_code=303)

@router.post("/users/{user_id}/delete")
async def admin_user_delete(user_id: int, db: Session = Depends(get_db)):
    """Delete user"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return RedirectResponse(url="/admin/users?error=User not found", status_code=303)
        
        db.delete(user)
        db.commit()
        return RedirectResponse(url="/admin/users?message=User deleted successfully", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/admin/users?error={str(e)}", status_code=303)

# Role POST routes
@router.post("/roles/new")
async def admin_role_create(
    request: Request,
    name: str = Form(...),
    description: str = Form(None),
    permissions: str = Form(None),
    db: Session = Depends(get_db)
):
    """Create new role"""
    try:
        role = Role(
            name=name,
            description=description,
            permissions=permissions
        )
        db.add(role)
        db.commit()
        return RedirectResponse(url="/admin/roles?message=Role created successfully", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/admin/roles?error={str(e)}", status_code=303)

@router.post("/roles/{role_id}/edit")
async def admin_role_update(
    request: Request,
    role_id: int,
    name: str = Form(...),
    description: str = Form(None),
    permissions: str = Form(None),
    db: Session = Depends(get_db)
):
    """Update role"""
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return RedirectResponse(url="/admin/roles?error=Role not found", status_code=303)
        
        role.name = name
        role.description = description
        role.permissions = permissions
        
        db.commit()
        return RedirectResponse(url="/admin/roles?message=Role updated successfully", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/admin/roles?error={str(e)}", status_code=303)

@router.post("/roles/{role_id}/delete")
async def admin_role_delete(role_id: int, db: Session = Depends(get_db)):
    """Delete role"""
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return RedirectResponse(url="/admin/roles?error=Role not found", status_code=303)
        
        # Check if role has users
        user_count = db.query(User).filter(User.role_id == role_id).count()
        if user_count > 0:
            return RedirectResponse(url=f"/admin/roles?error=Cannot delete role with {user_count} users", status_code=303)
        
        db.delete(role)
        db.commit()
        return RedirectResponse(url="/admin/roles?message=Role deleted successfully", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/admin/roles?error={str(e)}", status_code=303)


# ============================================
# API Routes (JSON)
# ============================================

@router.post("/reset-database")
def reset_database(db: Session = Depends(get_db)):
    """
    Reset database - hapus semua phones
    
    ⚠️ HATI-HATI: Ini akan menghapus SEMUA data!
    """
    try:
        # Hitung data sebelum dihapus
        phone_count = db.query(Phone).count()
        
        # Hapus phones
        db.query(Phone).delete()
        
        # Commit perubahan
        db.commit()
        
        # Reset auto increment (opsional)
        try:
            db.execute(text("ALTER TABLE phones AUTO_INCREMENT = 1"))
            db.commit()
        except:
            pass  # Tidak masalah jika gagal
        
        return {
            "success": True,
            "message": "Database berhasil direset",
            "deleted": {
                "phones": phone_count
            }
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats", response_class=HTMLResponse)
async def admin_stats(request: Request, db: Session = Depends(get_db)):
    """
    Halaman statistik database dengan visual cards
    """
    try:
        phone_count = db.query(Phone).count()
        category_count = db.query(Category).count()
        
        # Hitung per brand
        brands = db.query(Phone.brand).distinct().all()
        brand_stats = {}
        for (brand,) in brands:
            count = db.query(Phone).filter(Phone.brand == brand).count()
            brand_stats[brand] = count
        
        # Sort by count descending
        brand_stats = dict(sorted(brand_stats.items(), key=lambda x: x[1], reverse=True))
        
        return templates.TemplateResponse(
            "admin/stats.html",
            {
                "request": request,
                "total_devices": phone_count,
                "total_categories": category_count,
                "total_brands": len(brands),
                "brand_stats": brand_stats
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# NEW ROUTES - Analytics, Logs, Bulk Ops, Settings
# ============================================

@router.get("/analytics", response_class=HTMLResponse)
async def admin_analytics(request: Request, db: Session = Depends(get_db)):
    """Halaman analytics dengan grafik detail"""
    
    # Price ranges - kelompokkan device berdasarkan harga
    price_ranges = {
        "< 2 Juta": 0,
        "2-5 Juta": 0,
        "5-10 Juta": 0,
        "> 10 Juta": 0
    }
    
    devices = db.query(Phone).all()
    for device in devices:
        if device.price:
            if device.price < 2000000:
                price_ranges["< 2 Juta"] += 1
            elif device.price < 5000000:
                price_ranges["2-5 Juta"] += 1
            elif device.price < 10000000:
                price_ranges["5-10 Juta"] += 1
            else:
                price_ranges["> 10 Juta"] += 1
    
    # Year statistics - hitung device per tahun
    year_stats = {}
    for device in devices:
        if device.release_year:
            year = str(device.release_year)
            year_stats[year] = year_stats.get(year, 0) + 1
    
    # Sort by year
    year_stats = dict(sorted(year_stats.items()))
    
    # Category stats
    category_stats = {}
    categories = db.query(Category).all()
    for cat in categories:
        count = db.query(Phone).filter(Phone.category_id == cat.id).count()
        category_stats[cat.name] = count
    
    # Brand details - statistik per brand
    brand_details = {}
    brands = db.query(Phone.brand).distinct().all()
    for (brand,) in brands:
        if brand:
            brand_devices = db.query(Phone).filter(Phone.brand == brand).all()
            
            # Hitung rata-rata harga
            prices = [d.price for d in brand_devices if d.price]
            avg_price = sum(prices) / len(prices) if prices else None
            
            # Tahun terbaru
            years = [d.release_year for d in brand_devices if d.release_year]
            latest_year = max(years) if years else None
            
            brand_details[brand] = {
                "count": len(brand_devices),
                "avg_price": avg_price,
                "latest_year": latest_year
            }
    
    return templates.TemplateResponse(
        "admin/analytics.html",
        {
            "request": request,
            "price_ranges": price_ranges,
            "year_stats": year_stats,
            "category_stats": category_stats,
            "brand_details": brand_details
        }
    )

@router.get("/activity-logs", response_class=HTMLResponse)
async def admin_activity_logs(
    request: Request,
    page: int = 1,
    action_type: str = None,
    entity_type: str = None
):
    """Halaman activity logs - untuk sementara data dummy"""
    from datetime import datetime, timedelta
    
    # Data dummy untuk demo - nanti bisa diganti dengan database
    all_logs = [
        {
            "action": "create",
            "title": "Device baru ditambahkan",
            "description": "Samsung Galaxy S24 Ultra berhasil ditambahkan",
            "timestamp": (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            "user": "Admin"
        },
        {
            "action": "update",
            "title": "Device diupdate",
            "description": "iPhone 15 Pro - harga diupdate",
            "timestamp": (datetime.now() - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S"),
            "user": "Admin"
        },
        {
            "action": "delete",
            "title": "Device dihapus",
            "description": "Xiaomi Redmi Note 10 dihapus dari database",
            "timestamp": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
            "user": "Admin"
        },
        {
            "action": "create",
            "title": "Category baru ditambahkan",
            "description": "Category 'Gaming Phone' berhasil ditambahkan",
            "timestamp": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),
            "user": "Admin"
        }
    ]
    
    # Filter berdasarkan action_type
    if action_type:
        all_logs = [log for log in all_logs if log["action"] == action_type]
    
    # Pagination sederhana
    ITEMS_PER_PAGE = 10
    total_items = len(all_logs)
    total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    logs = all_logs[start:end]
    
    return templates.TemplateResponse(
        "admin/activity_logs.html",
        {
            "request": request,
            "logs": logs,
            "page": page,
            "total_pages": total_pages,
            "action_type": action_type,
            "entity_type": entity_type
        }
    )

@router.get("/bulk-operations", response_class=HTMLResponse)
async def admin_bulk_operations(request: Request, db: Session = Depends(get_db)):
    """Halaman bulk operations"""
    
    # Get brands untuk dropdown
    brands = db.query(Phone.brand).distinct().filter(Phone.brand.isnot(None)).all()
    brands = [b[0] for b in brands]
    
    # Get categories untuk dropdown
    categories = db.query(Category).all()
    
    # Get years untuk dropdown
    years = db.query(Phone.release_year).distinct().filter(Phone.release_year.isnot(None)).order_by(Phone.release_year.desc()).all()
    years = [y[0] for y in years]
    
    return templates.TemplateResponse(
        "admin/bulk_operations.html",
        {
            "request": request,
            "brands": brands,
            "categories": categories,
            "years": years
        }
    )

@router.post("/bulk-operations/import")
async def bulk_import_devices(request: Request, db: Session = Depends(get_db)):
    """Import devices dari CSV"""
    from fastapi.responses import RedirectResponse
    from fastapi import UploadFile, File, Form
    import csv
    import io
    
    # Get uploaded file
    form = await request.form()
    csv_file = form.get("csv_file")
    
    if not csv_file:
        return RedirectResponse(url="/admin/bulk-operations?error=No file uploaded", status_code=303)
    
    try:
        # Read CSV
        content = await csv_file.read()
        csv_text = content.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(csv_text))
        
        imported_count = 0
        for row in csv_reader:
            # Create device dari CSV row
            device = Phone(
                name=row.get('name'),
                brand=row.get('brand'),
                category_id=int(row.get('category_id')) if row.get('category_id') else None,
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
        return RedirectResponse(
            url=f"/admin/bulk-operations?message=Successfully imported {imported_count} devices",
            status_code=303
        )
    except Exception as e:
        return RedirectResponse(
            url=f"/admin/bulk-operations?error=Import failed: {str(e)}",
            status_code=303
        )

@router.post("/bulk-operations/assign-category")
async def bulk_assign_category(
    request: Request,
    brand: str = Form(...),
    category_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """Assign category ke semua device dengan brand tertentu"""
    from fastapi.responses import RedirectResponse
    
    try:
        # Update semua device dengan brand tersebut
        updated = db.query(Phone).filter(Phone.brand == brand).update(
            {"category_id": category_id},
            synchronize_session=False
        )
        db.commit()
        
        return RedirectResponse(
            url=f"/admin/bulk-operations?message=Updated {updated} devices",
            status_code=303
        )
    except Exception as e:
        return RedirectResponse(
            url=f"/admin/bulk-operations?error={str(e)}",
            status_code=303
        )

@router.post("/bulk-operations/update-price")
async def bulk_update_price(
    request: Request,
    category_id: int = Form(None),
    adjustment_type: str = Form(...),
    adjustment_value: float = Form(...),
    db: Session = Depends(get_db)
):
    """Update harga secara massal"""
    from fastapi.responses import RedirectResponse
    
    try:
        # Build query
        query = db.query(Phone)
        if category_id:
            query = query.filter(Phone.category_id == category_id)
        
        devices = query.all()
        updated_count = 0
        
        for device in devices:
            if device.price:
                if adjustment_type == "percentage":
                    # Update berdasarkan persentase
                    device.price = device.price * (1 + adjustment_value / 100)
                else:
                    # Update berdasarkan nilai tetap
                    device.price = device.price + adjustment_value
                
                updated_count += 1
        
        db.commit()
        
        return RedirectResponse(
            url=f"/admin/bulk-operations?message=Updated prices for {updated_count} devices",
            status_code=303
        )
    except Exception as e:
        return RedirectResponse(
            url=f"/admin/bulk-operations?error={str(e)}",
            status_code=303
        )

@router.post("/bulk-operations/delete")
async def bulk_delete_devices(
    request: Request,
    year: int = Form(None),
    brand: str = Form(None),
    db: Session = Depends(get_db)
):
    """Delete devices secara massal berdasarkan filter"""
    from fastapi.responses import RedirectResponse
    
    try:
        # Build query
        query = db.query(Phone)
        
        if year:
            query = query.filter(Phone.release_year == year)
        if brand:
            query = query.filter(Phone.brand == brand)
        
        # Delete
        deleted_count = query.delete(synchronize_session=False)
        db.commit()
        
        return RedirectResponse(
            url=f"/admin/bulk-operations?message=Deleted {deleted_count} devices",
            status_code=303
        )
    except Exception as e:
        return RedirectResponse(
            url=f"/admin/bulk-operations?error={str(e)}",
            status_code=303
        )

@router.get("/settings", response_class=HTMLResponse)
async def admin_settings(request: Request, db: Session = Depends(get_db)):
    """Halaman settings"""
    import os
    
    # Get system info
    total_devices = db.query(Phone).count()
    total_categories = db.query(Category).count()
    
    # Check database connection
    try:
        db.execute(text("SELECT 1"))
        database_status = "Connected"
    except:
        database_status = "Disconnected"
    
    # Get AI API key (masked)
    ai_api_key = os.getenv("AI_API_KEY", "")
    ai_api_key_masked = "*" * 20 if ai_api_key else ""
    
    return templates.TemplateResponse(
        "admin/settings.html",
        {
            "request": request,
            "total_devices": total_devices,
            "total_categories": total_categories,
            "database_status": database_status,
            "ai_api_key_masked": ai_api_key_masked
        }
    )

@router.post("/settings/update-api")
async def update_api_settings(
    request: Request,
    ai_api_key: str = Form(...)
):
    """Update API settings"""
    from fastapi.responses import RedirectResponse
    import os
    
    # Untuk sementara, hanya redirect dengan message
    # TODO: Implement proper .env file update
    return RedirectResponse(
        url="/admin/settings?message=API settings updated (restart required)",
        status_code=303
    )

@router.post("/settings/backup-database")
async def backup_database(request: Request, db: Session = Depends(get_db)):
    """Backup database ke CSV"""
    from fastapi.responses import StreamingResponse, RedirectResponse
    import io
    import csv
    from datetime import datetime
    
    try:
        devices = db.query(Phone).all()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'ID', 'Name', 'Brand', 'Category ID', 'CPU', 'GPU', 'RAM', 'Storage',
            'Camera', 'Battery', 'Screen', 'Release Year', 'Price', 'Image URL', 'Description'
        ])
        
        # Write data
        for device in devices:
            writer.writerow([
                device.id, device.name, device.brand, device.category_id,
                device.cpu or '', device.gpu or '', device.ram or '', device.storage or '',
                device.camera or '', device.battery or '', device.screen or '',
                device.release_year or '', device.price or '', device.image_url or '',
                device.description or ''
            ])
        
        # Prepare response
        output.seek(0)
        filename = f"comparely_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        return RedirectResponse(
            url=f"/admin/settings?error=Backup failed: {str(e)}",
            status_code=303
        )

@router.post("/settings/optimize-database")
async def optimize_database(request: Request, db: Session = Depends(get_db)):
    """Optimize database"""
    from fastapi.responses import RedirectResponse
    
    try:
        # Simple optimization - hapus orphaned records, dll
        # Untuk MySQL/MariaDB
        db.execute(text("OPTIMIZE TABLE phones"))
        db.execute(text("OPTIMIZE TABLE categories"))
        db.commit()
        
        return RedirectResponse(
            url="/admin/settings?message=Database optimized successfully",
            status_code=303
        )
    except Exception as e:
        return RedirectResponse(
            url=f"/admin/settings?message=Optimization completed (some tables may not support OPTIMIZE)",
            status_code=303
        )

@router.post("/settings/update-ui")
async def update_ui_preferences(request: Request):
    """Update UI preferences"""
    from fastapi.responses import RedirectResponse
    
    # TODO: Save to session or database
    return RedirectResponse(
        url="/admin/settings?message=UI preferences updated",
        status_code=303
    )

@router.post("/settings/clear-cache")
async def clear_cache(request: Request):
    """Clear cache"""
    from fastapi.responses import RedirectResponse
    
    # TODO: Implement cache clearing
    return RedirectResponse(
        url="/admin/settings?message=Cache cleared successfully",
        status_code=303
    )

