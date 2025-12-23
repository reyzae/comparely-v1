from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas

# ==================== READ OPERATIONS ====================

def get_categories(db: Session) -> List[models.Category]:
    """
    Mengambil semua kategori dari database.
    
    Args:
        db: Database session
    
    Returns:
        List of Category objects
    """
    return db.query(models.Category).all()


def get_category(db: Session, category_id: int):
    """
    Mengambil 1 kategori berdasarkan ID.
    
    Args:
        db: Database session
        category_id: ID kategori yang dicari
    
    Returns:
        Category object jika ditemukan, None jika tidak ada
    """
    return db.query(models.Category).filter(models.Category.id == category_id).first()


# ==================== CREATE OPERATIONS ====================

def create_category(db: Session, category: schemas.CategoryCreate) -> models.Category:
    """
    Membuat kategori baru di database.
    
    Args:
        db: Database session
        category: Data kategori dari request
    
    Returns:
        Category object yang baru dibuat
    """
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
