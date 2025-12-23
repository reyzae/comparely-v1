from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Benchmark(Base):
    """
    Model untuk tabel benchmarks di database.
    Menyimpan skor benchmark (performa) dari setiap perangkat.
    """
    __tablename__ = "benchmarks"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Key ke tabel devices
    device_id = Column(Integer, ForeignKey("devices.id"))
    
    # Skor Benchmark
    cpu_score = Column(Integer)  # Skor performa CPU, misal: 15000
    gpu_score = Column(Integer)  # Skor performa GPU, misal: 12000

    # Relationship: 1 benchmark untuk 1 device
    device = relationship("Device", back_populates="benchmark")
