from typing import Generator
from sqlalchemy.orm import Session
from ..database import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function untuk mendapatkan database session.
    
    Fungsi ini digunakan di semua router dengan FastAPI Depends().
    Session akan otomatis di-close setelah request selesai.
    
    Yield:
        Session: SQLAlchemy database session
    
    Contoh penggunaan di router:
        @router.get("/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        # Yield session ke router
        yield db
    finally:
        # Pastikan session selalu di-close, bahkan jika ada error
        db.close()
