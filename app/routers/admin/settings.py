"""
Admin Settings Router
Handles application settings and configuration.
"""

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.deps import get_db
from app.models import Phone, Category, AppSettings
from .auth import get_current_user
from app.core.rbac_context import add_rbac_to_context

import logging
import os
import shutil
from datetime import datetime
from pathlib import Path

# Setup templates
templates = Jinja2Templates(directory="app/templates")
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(tags=["admin-settings"])

# Helper functions
def get_setting(db: Session, key: str, default: str = "") -> str:
    """Get setting value from database"""
    setting = db.query(AppSettings).filter(AppSettings.key == key).first()
    return setting.value if setting else default


def set_setting(db: Session, key: str, value: str, description: str = None):
    """Set setting value in database"""
    setting = db.query(AppSettings).filter(AppSettings.key == key).first()
    if setting:
        setting.value = value
        if description:
            setting.description = description
    else:
        setting = AppSettings(key=key, value=value, description=description)
        db.add(setting)
    db.commit()


def get_database_size(db: Session) -> str:
    """Get database size in MB"""
    try:
        result = db.execute(text("""
            SELECT 
                ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as size_mb
            FROM information_schema.TABLES 
            WHERE table_schema = DATABASE()
        """)).first()
        return f"{result[0] if result and result[0] else 0} MB"
    except Exception as e:
        logger.error(f"Error getting database size: {e}")
        return "N/A"


@router.get("/settings", response_class=HTMLResponse)
async def admin_settings(request: Request, db: Session = Depends(get_db)):
    """Halaman settings"""
    
    # Get database stats
    total_devices = db.query(Phone).count()
    total_categories = db.query(Category).count()
    database_size = get_database_size(db)
    
    # Get settings from database
    ai_api_key = get_setting(db, "ai_api_key", "")
    items_per_page = get_setting(db, "items_per_page", "20")
    date_format = get_setting(db, "date_format", "YYYY-MM-DD")
    last_backup = get_setting(db, "last_backup_date", "Never")
    
    current_user = get_current_user(request, db)
    rbac_context = add_rbac_to_context(current_user)

    return templates.TemplateResponse(
        "admin/settings.html",
        {
            "request": request,
            "current_user": current_user,
            **rbac_context,
            "database_status": "Connected",
            "total_devices": total_devices,
            "total_categories": total_categories,
            "database_size": database_size,
            "ai_api_key_masked": "••••••••••••" if ai_api_key else "",
            "items_per_page": items_per_page,
            "date_format": date_format,
            "last_backup": last_backup
        }
    )


@router.post("/settings/update-api")
async def update_api_settings(
    request: Request,
    ai_api_key: str = Form(...),
    db: Session = Depends(get_db)
):
    """Update API settings"""
    try:
        # Save API key to database
        set_setting(db, "ai_api_key", ai_api_key, "AI API Key for recommendations")
        
        # Also update .env file if needed
        env_path = Path(".env")
        if env_path.exists():
            with open(env_path, "r") as f:
                lines = f.readlines()
            
            # Update or add AI_API_KEY
            found = False
            for i, line in enumerate(lines):
                if line.startswith("AI_API_KEY="):
                    lines[i] = f"AI_API_KEY={ai_api_key}\n"
                    found = True
                    break
            
            if not found:
                lines.append(f"\nAI_API_KEY={ai_api_key}\n")
            
            with open(env_path, "w") as f:
                f.writelines(lines)
        
        logger.info("API settings updated")
        
        return RedirectResponse(
            url="/admin/settings?message=API settings updated successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error updating API settings: {e}")
        return RedirectResponse(
            url="/admin/settings?error=Failed to update API settings",
            status_code=303
        )


@router.post("/settings/backup-database")
async def backup_database(request: Request, db: Session = Depends(get_db)):
    """Backup database to SQL file"""
    try:
        # Create backups directory if not exists
        backup_dir = Path("backups")
        backup_dir.mkdir(exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"comparely_backup_{timestamp}.sql"
        
        # Get database connection info
        db_url = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:@localhost/comparely")
        
        # Parse database URL
        # Format: mysql+mysqlconnector://user:password@host/database
        parts = db_url.replace("mysql+mysqlconnector://", "").split("@")
        user_pass = parts[0].split(":")
        host_db = parts[1].split("/")
        
        user = user_pass[0]
        password = user_pass[1] if len(user_pass) > 1 else ""
        host = host_db[0]
        database = host_db[1]
        
        # Create mysqldump command
        cmd = f'mysqldump -u {user}'
        if password:
            cmd += f' -p{password}'
        cmd += f' -h {host} {database} > "{backup_file}"'
        
        # Execute backup
        os.system(cmd)
        
        # Save last backup date
        set_setting(db, "last_backup_date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        logger.info(f"Database backup created: {backup_file}")
        
        return RedirectResponse(
            url=f"/admin/settings?message=Database backup created successfully: {backup_file.name}",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error backing up database: {e}")
        return RedirectResponse(
            url="/admin/settings?error=Failed to backup database",
            status_code=303
        )


@router.post("/settings/optimize-database")
async def optimize_database(request: Request, db: Session = Depends(get_db)):
    """Optimize database tables"""
    try:
        # Get all tables
        tables = ["phones", "categories", "users", "roles", "activity_logs", "notifications", "app_settings"]
        
        optimized_count = 0
        for table in tables:
            try:
                db.execute(text(f"OPTIMIZE TABLE {table}"))
                optimized_count += 1
            except Exception as e:
                logger.warning(f"Could not optimize table {table}: {e}")
        
        db.commit()
        logger.info(f"Database optimization completed: {optimized_count} tables optimized")
        
        return RedirectResponse(
            url=f"/admin/settings?message=Database optimized successfully ({optimized_count} tables)",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error optimizing database: {e}")
        return RedirectResponse(
            url="/admin/settings?error=Failed to optimize database",
            status_code=303
        )


@router.post("/admin/reset-database")
async def reset_database(request: Request, db: Session = Depends(get_db)):
    """Reset database (delete all devices)"""
    try:
        # Delete all devices
        deleted_count = db.query(Phone).delete()
        db.commit()
        
        logger.warning(f"Database reset: {deleted_count} devices deleted")
        
        return RedirectResponse(
            url=f"/admin/settings?message=Database reset successfully ({deleted_count} devices deleted)",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error resetting database: {e}")
        return RedirectResponse(
            url="/admin/settings?error=Failed to reset database",
            status_code=303
        )


@router.post("/settings/clear-cache")
async def clear_cache(request: Request, db: Session = Depends(get_db)):
    """Clear application cache"""
    try:
        # Clear any cache directories or temp files
        cache_cleared = False
        
        # Example: Clear __pycache__ directories
        for root, dirs, files in os.walk("app"):
            if "__pycache__" in dirs:
                pycache_dir = os.path.join(root, "__pycache__")
                shutil.rmtree(pycache_dir)
                cache_cleared = True
        
        logger.info("Cache cleared")
        
        message = "Cache cleared successfully" if cache_cleared else "No cache to clear"
        return RedirectResponse(
            url=f"/admin/settings?message={message}",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error clearing cache: {e}")
        return RedirectResponse(
            url="/admin/settings?error=Failed to clear cache",
            status_code=303
        )


@router.post("/settings/update-ui")
async def update_ui_preferences(
    request: Request,
    items_per_page: int = Form(20),
    date_format: str = Form("YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    """Update UI preferences"""
    try:
        # Save preferences to database
        set_setting(db, "items_per_page", str(items_per_page), "Number of items per page")
        set_setting(db, "date_format", date_format, "Date format for display")
        
        logger.info(f"UI preferences updated: {items_per_page} items per page, {date_format} date format")
        
        return RedirectResponse(
            url="/admin/settings?message=UI preferences updated successfully",
            status_code=303
        )
    except Exception as e:
        logger.exception(f"Error updating UI preferences: {e}")
        return RedirectResponse(
            url="/admin/settings?error=Failed to update UI preferences",
            status_code=303
        )
