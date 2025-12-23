from sqlalchemy import Column, Integer, String, ForeignKey, Text, DECIMAL
from sqlalchemy.orm import relationship
from ..database import Base

class Device(Base):
    """
    Model untuk tabel devices di database.
    Menyimpan informasi lengkap perangkat yang akan dibandingkan.
    """
    __tablename__ = "devices"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Informasi Dasar
    name = Column(String(255), index=True)  # Nama perangkat, misal: "iPhone 15 Pro"
    brand = Column(String(100), index=True)  # Merek, misal: "Apple"
    
    # Foreign Key ke tabel categories
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    # Spesifikasi Perangkat
    cpu = Column(String(255))       # Processor, misal: "A17 Pro"
    gpu = Column(String(255))       # Graphics, misal: "Apple GPU 6-core"
    ram = Column(String(100))       # Memory, misal: "8GB"
    storage = Column(String(100))   # Penyimpanan, misal: "256GB"
    camera = Column(String(255))    # Kamera, misal: "48MP + 12MP"
    battery = Column(String(100))   # Baterai, misal: "3274 mAh"
    screen = Column(String(255))    # Layar, misal: "6.1 inch OLED"
    
    # Informasi Tambahan
    release_year = Column(Integer)          # Tahun rilis, misal: 2023
    price = Column(DECIMAL(15, 2))          # Harga dalam Rupiah
    image_url = Column(String(500))         # URL gambar produk
    description = Column(Text)              # Deskripsi lengkap
    
    # Relationships
    # Relasi ke Category (many-to-one: banyak device, 1 category)
    category = relationship("Category", back_populates="devices")
    
    # Relasi ke Benchmark (one-to-one: 1 device, 1 benchmark)
    benchmark = relationship("Benchmark", back_populates="device", uselist=False)
