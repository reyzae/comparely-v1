"""
Konfigurasi aplikasi COMPARELY.
File ini menyimpan semua konfigurasi penting seperti API keys.

PENTING: Jangan commit file ini ke Git jika berisi API key asli!
"""

import os
from dotenv import load_dotenv

# Load environment variables dari file .env (jika ada)
load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+mysqlconnector://root:@localhost/comparely"
)

# AI Configuration
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_API_URL = "https://api.x.ai/v1/chat/completions"
AI_MODEL = "grok-4-latest"

# AI Settings
AI_TEMPERATURE = 0.7  # Kreativitas AI (0.0 = strict, 1.0 = creative)
AI_MAX_TOKENS = 500  # Maksimal panjang response

# Use Case Options
USE_CASES = [
    "gaming",
    "fotografi",
    "kerja",
    "kuliah",
    "multimedia"
]
