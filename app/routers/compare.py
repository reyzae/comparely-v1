from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..core.deps import get_db  # Import get_db dari core.deps (centralized)
from ..services import comparison_service, ai as ai_service
from .. import schemas

router = APIRouter(
    prefix="/compare",
    tags=["compare"]
)

@router.get("/")
def compare_devices(id1: int, id2: int, db: Session = Depends(get_db)):
    """
    Endpoint untuk membandingkan 2 device.
    
    Query Parameters:
        id1: ID device pertama
        id2: ID device kedua
    
    Returns:
        Dictionary berisi device_1, device_2, dan highlights
    """
    try:
        # Panggil service layer untuk business logic
        result = comparison_service.compare_two_devices(db, id1, id2)
        return result
    except ValueError as e:
        # Jika device tidak ditemukan
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/ai")
def compare_devices_with_ai(
    id1: int = Query(..., description="ID device pertama"),
    id2: int = Query(..., description="ID device kedua"),
    db: Session = Depends(get_db)
):
    """
    Endpoint untuk membandingkan 2 device dengan analisis AI dari Grok AI.
    
    **Fitur Baru dengan AI:**
    - Perbandingan detail (sama seperti /compare/)
    - **Analisis mendalam dari Grok AI**
    - Rekomendasi personal berdasarkan use case
    
    Query Parameters:
        id1: ID device pertama
        id2: ID device kedua
    
    Returns:
        Dictionary berisi:
        - device_1: Data device pertama
        - device_2: Data device kedua
        - highlights: Highlight perbandingan
        - ai_analysis: Analisis lengkap dari Grok AI
    """
    try:
        # 1. Dapatkan perbandingan dasar (rule-based)
        result = comparison_service.compare_two_devices(db, id1, id2)
        
        # 2. Dapatkan analisis AI dari Grok AI
        ai_analysis = ai_service.get_comparison_analysis(
            result["device_1"],
            result["device_2"]
        )
        
        # 3. Tambahkan AI analysis ke result
        result["ai_analysis"] = ai_analysis
        
        return result
        
    except ValueError as e:
        # Jika device tidak ditemukan
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Error lainnya
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
