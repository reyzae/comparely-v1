"""
Admin Activity Logs Router
Handles activity logging and monitoring.
"""

from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.deps import get_db
from .auth import get_current_user
from app.core.rbac_context import add_rbac_to_context

from datetime import datetime, timedelta
from math import ceil
from typing import Optional

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Create router
router = APIRouter(tags=["admin-activity-logs"])


@router.get("/activity-logs", response_class=HTMLResponse)
async def admin_activity_logs(
    request: Request,
    page: int = 1,
    action_type: Optional[str] = Query(None),
    entity_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Halaman activity logs with filters"""
    
    ITEMS_PER_PAGE = 20
    
    # Placeholder activity logs data
    # In production, fetch from activity_logs table
    all_logs = []
    
    # Generate sample logs with proper structure
    actions = [
        {"type": "create", "title": "Created Device", "description": "Added new device to database"},
        {"type": "update", "title": "Updated Device", "description": "Modified device information"},
        {"type": "delete", "title": "Deleted Device", "description": "Removed device from database"},
        {"type": "create", "title": "Created Category", "description": "Added new category"},
        {"type": "update", "title": "Updated Category", "description": "Modified category details"},
        {"type": "create", "title": "Created User", "description": "Added new admin user"},
    ]
    
    for i in range(1, 51):
        action = actions[i % len(actions)]
        log = {
            "id": i,
            "user": "Administrator",
            "action": action["type"],
            "title": action["title"],
            "description": f"{action['description']} (ID: {i})",
            "entity_type": "device" if "Device" in action["title"] else "category" if "Category" in action["title"] else "user",
            "timestamp": (datetime.now() - timedelta(hours=i)).strftime("%Y-%m-%d %H:%M:%S"),
            "ip_address": "127.0.0.1",
            "status": "success"
        }
        all_logs.append(log)
    
    # Apply filters
    filtered_logs = all_logs
    
    if action_type:
        filtered_logs = [log for log in filtered_logs if log["action"] == action_type]
    
    if entity_type:
        filtered_logs = [log for log in filtered_logs if log["entity_type"] == entity_type]
    
    # Pagination
    total_items = len(filtered_logs)
    total_pages = ceil(total_items / ITEMS_PER_PAGE) if total_items > 0 else 1
    offset = (page - 1) * ITEMS_PER_PAGE
    logs = filtered_logs[offset:offset + ITEMS_PER_PAGE]
    
    current_user = get_current_user(request, db)
    rbac_context = add_rbac_to_context(current_user)

    return templates.TemplateResponse(
        "admin/activity_logs.html",
        {
            "request": request,
            "current_user": current_user,
            **rbac_context,  # Add RBAC permissions
            "logs": logs,
            "page": page,
            "total_pages": total_pages,
            "action_type": action_type,
            "entity_type": entity_type
        }
    )
