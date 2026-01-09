"""
Admin routers package.
Contains all admin panel routes organized by functionality.
"""

from fastapi import APIRouter

# Create main admin router
router = APIRouter(prefix="/admin", tags=["admin"])

# Import and include sub-routers
from . import (activity_logs, analytics, auth, bulk_operations, categories,
               dashboard, devices, notifications, settings, tools, users)

# Include all sub-routers
router.include_router(auth.router)
router.include_router(dashboard.router)
router.include_router(devices.router)
router.include_router(users.router)
router.include_router(categories.router)
router.include_router(analytics.router)
router.include_router(tools.router)
router.include_router(settings.router)
router.include_router(activity_logs.router)
router.include_router(bulk_operations.router)
router.include_router(notifications.router)
