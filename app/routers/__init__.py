"""
Routers package - API endpoints dan halaman

Package ini berisi semua router untuk aplikasi COMPARELY:
- admin: Admin panel routes
- categories: API endpoints untuk categories
- compare: API endpoints untuk comparison
- devices: API endpoints untuk devices
- frontend: Routes untuk halaman HTML
- recommendation: API endpoints untuk recommendations
"""

from . import admin, categories, compare, devices, frontend, recommendation

__all__ = ["admin", "categories", "compare", "devices", "frontend", "recommendation"]
