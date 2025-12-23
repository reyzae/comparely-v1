"""
Admin routers package.
Contains all admin panel routes organized by functionality.
"""

from fastapi import APIRouter

# Create main admin router
router = APIRouter(prefix="/admin", tags=["admin"])

# Import and include sub-routers
from . import auth
from . import dashboard
from . import devices
from . import users
from . import categories
from . import analytics
from . import tools
from . import settings
from . import activity_logs
from . import bulk_operations
from . import notifications

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
