from pydantic import BaseModel

# ==================== BASE SCHEMAS ====================

class BenchmarkBase(BaseModel):
    """
    Schema dasar untuk Benchmark.
    Berisi skor performa CPU dan GPU.
    """
    cpu_score: int  # Skor CPU, misal: 15000
    gpu_score: int  # Skor GPU, misal: 12000


# ==================== CREATE SCHEMAS ====================

class BenchmarkCreate(BenchmarkBase):
    """
    Schema untuk membuat Benchmark baru.
    
    Digunakan di endpoint POST untuk menambah benchmark.
    """
    pass


# ==================== RESPONSE SCHEMAS ====================

class Benchmark(BenchmarkBase):
    """
    Schema untuk response Benchmark dari database.
    Menambahkan id dan device_id.
    """
    id: int
    device_id: int
    
    class Config:
        # Agar bisa convert dari SQLAlchemy model ke Pydantic
        from_attributes = True
