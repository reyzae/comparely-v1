"""
Basic Tests untuk COMPARELY
Smoke tests untuk memastikan aplikasi berjalan dengan baik.
"""

import pytest
from app.main import app
from fastapi.testclient import TestClient

# Test client
client = TestClient(app)


class TestBasicEndpoints:
    """Test basic endpoints untuk memastikan aplikasi berjalan"""
    
    def test_homepage(self):
        """Test homepage dapat diakses"""
        response = client.get("/")
        assert response.status_code == 200
        assert "COMPARELY" in response.text or "Comparely" in response.text
    
    def test_devices_page(self):
        """Test halaman devices dapat diakses"""
        response = client.get("/devices")
        assert response.status_code == 200
    
    def test_features_page(self):
        """Test halaman features dapat diakses"""
        response = client.get("/features")
        assert response.status_code == 200
    
    def test_about_page(self):
        """Test halaman about dapat diakses"""
        response = client.get("/about")
        assert response.status_code == 200
    
    def test_api_docs(self):
        """Test API documentation dapat diakses"""
        response = client.get("/docs")
        assert response.status_code == 200


class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_get_devices_api(self):
        """Test GET /devices/ API endpoint"""
        response = client.get("/devices/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_categories_api(self):
        """Test GET /categories/ API endpoint"""
        response = client.get("/categories/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_search_devices(self):
        """Test search functionality"""
        response = client.get("/search?query=samsung")
        assert response.status_code == 200


class TestModels:
    """Test database models dapat di-import"""
    
    def test_import_models(self):
        """Test semua models dapat di-import"""
        from app.models import Device, Category, Benchmark
        assert Device is not None
        assert Category is not None
        assert Benchmark is not None
    
    def test_import_schemas(self):
        """Test semua schemas dapat di-import"""
        from app.schemas import DeviceCreate, CategoryCreate
        assert DeviceCreate is not None
        assert CategoryCreate is not None


class TestServices:
    """Test services dapat di-import"""
    
    def test_import_comparison_service(self):
        """Test comparison service dapat di-import"""
        from app.services import comparison_service
        assert comparison_service is not None
    
    def test_import_ai_service(self):
        """Test ai service dapat di-import"""
        from app.services import grok_service as ai_service
        assert ai_service is not None
    
    def test_import_recommendation_service(self):
        """Test recommendation service dapat di-import"""
        from app.services import recommendation_service
        assert recommendation_service is not None


class TestCSVImport:
    """Test CSV import script"""
    
    def test_import_csv_syntax(self):
        """Test import_csv.py syntax valid"""
        import py_compile
        import os
        
        # Path ke import_csv.py
        csv_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "import_csv.py")
        
        # Compile untuk check syntax
        try:
            py_compile.compile(csv_file, doraise=True)
            assert True
        except py_compile.PyCompileError:
            assert False, "import_csv.py has syntax errors"


# Jika dijalankan langsung
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
