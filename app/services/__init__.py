"""
Services package - Business logic layer

Service layer berisi business logic yang lebih kompleks.
Perbedaan dengan CRUD:
- CRUD: Operasi database sederhana (get, create, update, delete)
- Service: Logic bisnis yang mungkin:
  * Pakai beberapa CRUD operations
  * Ada validasi kompleks
  * Ada kalkulasi/transformasi data
  * Ada external API calls

Contoh:
- comparison_service: Logic untuk membandingkan 2 device
- device_service: Logic kompleks untuk device (jika diperlukan)

Import:
    from app.services import comparison_service
    
    result = comparison_service.compare_two_devices(db, id1, id2)
"""

from . import comparison_service

__all__ = ["comparison_service"]
