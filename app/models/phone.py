from sqlalchemy import Column, Integer, String, ForeignKey, Text, DECIMAL
from sqlalchemy.orm import relationship
from ..database import Base

class Phone(Base):
    """
    Model untuk tabel phones di database.
    Menyimpan informasi lengkap handphone yang akan dibandingkan.
    """
    __tablename__ = "phones"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Informasi Dasar
    name = Column(String(255), index=True)  # Nama handphone, misal: "Samsung Galaxy S24"
    brand = Column(String(100), index=True)  # Merek, misal: "Samsung"
    
    # Foreign Key ke tabel categories
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    # Spesifikasi Handphone
    cpu = Column(String(255))       # Processor, misal: "Snapdragon 8 Gen 3"
    gpu = Column(String(255))       # Graphics, misal: "Adreno 750"
    ram = Column(String(100))       # Memory, misal: "8GB"
    storage = Column(String(100))   # Penyimpanan, misal: "256GB"
    camera = Column(String(255))    # Kamera, misal: "50MP + 12MP + 10MP"
    battery = Column(String(100))   # Baterai, misal: "5000 mAh"
    screen = Column(String(255))    # Layar, misal: "6.2 inch AMOLED"
    
    # Informasi Tambahan
    release_year = Column(Integer)          # Tahun rilis, misal: 2024
    price = Column(DECIMAL(15, 2))          # Harga dalam Rupiah
    image_url = Column(String(500))         # URL gambar produk
    description = Column(Text)              # Deskripsi lengkap
    source_data = Column(String(500))       # URL sumber data (GSMArena, dll)
    
    # Relationships
    # Relasi ke Category (many-to-one: banyak phone, 1 category)
    category = relationship("Category", back_populates="phones")
