"""
Pytest configuration file
"""
import os
import sys

import pytest

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Set up test environment variables before importing app
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"
os.environ["ENVIRONMENT"] = "testing"
os.environ["DEBUG"] = "True"


@pytest.fixture(scope="session")
def test_app():
    """Create test application instance"""
    from app.main import app

    return app


@pytest.fixture(scope="session")
def test_client(test_app):
    """Create test client"""
    from fastapi.testclient import TestClient

    with TestClient(test_app) as client:
        yield client

