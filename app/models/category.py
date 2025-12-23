from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base

class Category(Base):
    """
    Model untuk tabel categories di database.
    Menyimpan kategori perangkat seperti Smartphone, Laptop, dll.
    """
    __tablename__ = "categories"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Nama kategori (unik, tidak boleh duplikat)
    name = Column(String(100), unique=True, index=True)

    # Relationship: 1 category bisa punya banyak phones
    phones = relationship("Phone", back_populates="category")

