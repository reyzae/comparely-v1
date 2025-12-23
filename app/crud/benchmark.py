from sqlalchemy.orm import Session
from .. import models, schemas

# ==================== CREATE OPERATIONS ====================

def create_benchmark(
    db: Session, 
    benchmark: schemas.BenchmarkCreate, 
    device_id: int
) -> models.Benchmark:
    """
    Membuat benchmark baru untuk sebuah device.
    
    Args:
        db: Database session
        benchmark: Data benchmark (cpu_score, gpu_score)
        device_id: ID device yang mau ditambahkan benchmark
    
    Returns:
        Benchmark object yang baru dibuat
    """
    # Buat Benchmark model dengan data dari schema + device_id
    db_benchmark = models.Benchmark(
        **benchmark.dict(), 
        device_id=device_id
    )
    
    db.add(db_benchmark)
    db.commit()
    db.refresh(db_benchmark)
    
    return db_benchmark


# ==================== READ OPERATIONS ====================

def get_benchmark_by_device(db: Session, device_id: int):
    """
    Mengambil benchmark berdasarkan device ID.
    
    Args:
        db: Database session
        device_id: ID device
    
    Returns:
        Benchmark object jika ada, None jika tidak ada
    """
    return db.query(models.Benchmark).filter(
        models.Benchmark.device_id == device_id
    ).first()
