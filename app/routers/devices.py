from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.deps import get_db  # Import get_db dari core.deps (centralized)
from ..crud import device as device_crud
from .. import schemas

# Membuat router (kelompok URL) untuk devices
router = APIRouter(
    prefix="/devices",
    tags=["devices"]
)



# API: Tambah Phone Baru
@router.post("/", response_model=schemas.Phone)
def create_device(phone: schemas.PhoneCreate, db: Session = Depends(get_db)):
    return device_crud.create_device(db=db, phone=phone)

# API: Ambil Semua Phone (bisa cari nama)
@router.get("/", response_model=List[schemas.Phone])
def read_devices(skip: int = 0, limit: int = 100, search: str = None, db: Session = Depends(get_db)):
    phones = device_crud.get_devices(db, skip=skip, limit=limit, search=search)
    return phones

# API: Autocomplete Search (untuk suggestions)
@router.get("/autocomplete")
def autocomplete_devices(query: str, db: Session = Depends(get_db)):
    """
    Endpoint untuk autocomplete search.
    
    Cara kerja:
    - User ketik di search bar (minimal 2 karakter)
    - Frontend kirim request ke endpoint ini
    - Return list phone yang namanya match dengan query
    - Frontend tampilkan sebagai dropdown suggestions
    
    Contoh:
    - Query: "galaxy" → Return: Galaxy S24, Galaxy S23, dll
    - Query: "iphone" → Return: iPhone 14, iPhone 13, dll
    """
    
    # Cari phone yang namanya mengandung query (case insensitive)
    # Limit 5 hasil agar tidak terlalu banyak
    phones = device_crud.get_devices(db, search=query, limit=5)
    
    # Return hanya data yang diperlukan (id dan name)
    # Biar response lebih ringan
    return [
        {"id": phone.id, "name": phone.name, "brand": phone.brand}
        for phone in phones
    ]


# API: Ambil Detail Phone per ID
@router.get("/{device_id}", response_model=schemas.Phone)
def read_device(device_id: int, db: Session = Depends(get_db)):
    db_phone = device_crud.get_device(db, phone_id=device_id)
    if db_phone is None:
        raise HTTPException(status_code=404, detail="Phone not found")
    return db_phone
