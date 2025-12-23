"""
Admin Notifications Router
Handles notification display, filtering, and management.
"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.crud import notification as crud_notification
from .auth import get_current_user
from app.core.rbac_context import add_rbac_to_context

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Create router
router = APIRouter(prefix="/notifications", tags=["admin-notifications"])


@router.get("/", response_class=HTMLResponse)
async def notifications_page(
    request: Request,
    filter: str = None,
    db: Session = Depends(get_db)
):
    """Display notifications page with filtering"""
    current_user = get_current_user(request, db)
    rbac_context = add_rbac_to_context(current_user)
    
    # Determine filter type
    filter_type = None
    is_read_filter = None
    
    if filter == 'unread':
        is_read_filter = False
    elif filter in ['success', 'warning', 'error', 'info']:
        filter_type = filter
    
    # Get notifications
    notifications = crud_notification.get_notifications(
        db,
        user_id=current_user.id,
        type=filter_type,
        is_read=is_read_filter,
        limit=50
    )
    
    # Get counts
    total_count = len(crud_notification.get_notifications(db, user_id=current_user.id, limit=1000))
    unread_count = crud_notification.count_unread_notifications(db, current_user.id)
    
    # Check if there are more notifications
    has_more = len(notifications) >= 50
    
    return templates.TemplateResponse(
        "admin/notifications.html",
        {
            "request": request,
            "current_user": current_user,
            **rbac_context,
            "notifications": notifications,
            "total_count": total_count,
            "unread_count": unread_count,
            "filter": filter,
            "has_more": has_more
        }
    )


@router.post("/api/notifications/{notification_id}/read")
async def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db)
):
    """Mark a single notification as read"""
    notification = crud_notification.mark_as_read(db, notification_id)
    if notification:
        return {"success": True, "message": "Notification marked as read"}
    return {"success": False, "error": "Notification not found"}


@router.post("/api/notifications/mark-all-read")
async def mark_all_notifications_read(
    request: Request,
    db: Session = Depends(get_db)
):
    """Mark all notifications as read for current user"""
    current_user = get_current_user(request, db)
    count = crud_notification.mark_all_as_read(db, current_user.id)
    return {"success": True, "count": count, "message": f"{count} notifications marked as read"}


@router.delete("/api/notifications/{notification_id}")
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):
    """Delete a notification"""
    success = crud_notification.delete_notification(db, notification_id)
    if success:
        return {"success": True, "message": "Notification deleted"}
    return {"success": False, "error": "Notification not found"}


@router.get("/api/notifications")
async def get_notifications_api(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    filter: str = None,
    db: Session = Depends(get_db)
):
    """API endpoint for paginated notifications (for AJAX load more)"""
    current_user = get_current_user(request, db)
    
    # Determine filter
    filter_type = None
    is_read_filter = None
    
    if filter == 'unread':
        is_read_filter = False
    elif filter in ['success', 'warning', 'error', 'info']:
        filter_type = filter
    
    # Get notifications
    notifications = crud_notification.get_notifications(
        db,
        user_id=current_user.id,
        type=filter_type,
        is_read=is_read_filter,
        skip=skip,
        limit=limit
    )
    
    # Convert to dict for JSON response
    notifications_data = [
        {
            "id": n.id,
            "type": n.type,
            "title": n.title,
            "message": n.message,
            "is_read": n.is_read,
            "created_at": n.created_at.isoformat(),
            "action_url": n.action_url,
            "action_label": n.action_label,
            "icon": n.icon,
            "priority": n.priority
        }
        for n in notifications
    ]
    
    return {
        "success": True,
        "notifications": notifications_data,
        "count": len(notifications_data),
        "has_more": len(notifications_data) >= limit
    }
