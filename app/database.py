from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .core.config import DATABASE_URL

# Database URL diambil dari config.py
# Format: mysql+mysqlconnector://user:password@host/db_name
SQLALCHEMY_DATABASE_URL = DATABASE_URL

# Create engine untuk koneksi ke database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal: factory untuk membuat database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class untuk semua models
Base = declarative_base()
