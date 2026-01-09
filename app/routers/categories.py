from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from ..core.deps import get_db  # Import get_db dari core.deps (centralized)
from ..crud import category as category_crud

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return category_crud.create_category(db=db, category=category)


@router.get("/", response_model=List[schemas.Category])
def read_categories(db: Session = Depends(get_db)):
    return category_crud.get_categories(db)
