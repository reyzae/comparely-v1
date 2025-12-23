"""
Service untuk integrasi dengan AI.
Menyediakan analisis perbandingan dan rekomendasi device menggunakan AI.
"""

import requests
import json
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from .. import models

# Load environment variables
load_dotenv()

# AI Configuration - Load dari environment variable
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_API_URL = "https://api.x.ai/v1/chat/completions"
AI_MODEL = "grok-4-1-fast-reasoning"  # Model AI yang digunakan



def call_ai_api(messages: List[Dict], temperature: float = 0.7) -> str:
    """
    Helper function untuk call AI API.
    
    Args:
        messages: List of message dicts dengan role & content
        temperature: Kreativitas AI (0.0 = strict, 1.0 = creative)
    
    Returns:
        Response text dari AI
    """
    # Validasi API key
    if not AI_API_KEY or AI_API_KEY == "":
        return """⚠️ **AI tidak tersedia**

Untuk menggunakan fitur AI, silakan:
1. Dapatkan API key
2. Tambahkan ke file `.env`:
   ```
   AI_API_KEY=your-api-key-here
   ```
3. Restart aplikasi

Sementara itu, Anda masih bisa melihat perbandingan manual di atas."""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AI_API_KEY}"
    }
    
    payload = {
        "messages": messages,
        "model": AI_MODEL,
        "stream": False,
        "temperature": temperature
    }
    
    try:
        response = requests.post(AI_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return data['choices'][0]['message']['content']
        
    except requests.exceptions.Timeout:
        return """⏱️ **Request timeout**

Koneksi ke AI terlalu lama. Silakan:
- Cek koneksi internet Anda
- Coba lagi dalam beberapa saat"""
        
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            return """🔑 **API Key tidak valid**

Silakan cek:
1. API key di file `.env` sudah benar
2. API key masih aktif
3. Format: `AI_API_KEY=...`"""
        elif response.status_code == 429:
            return """⚠️ **Quota API habis**

Anda sudah mencapai limit penggunaan API.
Silakan tunggu beberapa saat."""
        else:
            return f"""❌ **Error HTTP {response.status_code}**

Terjadi kesalahan saat menghubungi AI.
Detail: {str(e)}"""
            
    except requests.exceptions.ConnectionError:
        return """🌐 **Tidak ada koneksi internet**

Silakan cek koneksi internet Anda dan coba lagi."""
        
    except requests.exceptions.RequestException as e:
        return f"""❌ **Error koneksi**

Gagal menghubungi AI.
Detail: {str(e)}"""
        
    except (KeyError, IndexError) as e:
        return f"""❌ **Error parsing response**

Format response dari AI tidak sesuai.
Detail: {str(e)}"""


def get_comparison_analysis(device1: models.Phone, device2: models.Phone) -> str:
    """
    Mendapatkan analisis perbandingan 2 device dari AI.
    
    Args:
        device1: Device pertama
        device2: Device kedua
    
    Returns:
        String berisi analisis AI dalam bahasa Indonesia
    """
    try:
        # Buat prompt dengan format JSON strict
        user_prompt = f"""Bandingkan 2 smartphone berikut. Output HARUS dalam format JSON yang valid.

Device 1: {device1.name} ({device1.brand}) - Rp {device1.price:,.0f} - {device1.release_year}
CPU: {device1.cpu}, RAM: {device1.ram}, Kamera: {device1.camera}, Baterai: {device1.battery}

Device 2: {device2.name} ({device2.brand}) - Rp {device2.price:,.0f} - {device2.release_year}
CPU: {device2.cpu}, RAM: {device2.ram}, Kamera: {device2.camera}, Baterai: {device2.battery}

Kamu wajib memberikan output dalam format JSON berikut:

{{
  "performa": "Perbandingan CPU dan RAM dalam 1-2 kalimat",
  "kamera": "Perbandingan kamera dalam 1 kalimat",
  "baterai": "Perbandingan baterai dalam 1 kalimat",
  "value_for_money": "Analisis harga vs fitur dalam 1-2 kalimat",
  "rekomendasi": "Pilih device 1 jika... Pilih device 2 jika..."
}}

Jangan gunakan format lain. Hanya kirim JSON yang valid. Jawab dalam bahasa Indonesia."""

        messages = [
            {
                "role": "system",
                "content": "Kamu adalah asisten ahli teknologi yang membantu user memilih smartphone. Selalu jawab dalam format JSON yang valid."
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
        
        # Call AI API
        response_text = call_ai_api(messages, temperature=0.7)
        
        # Parse JSON response
        try:
            # Clean response (hapus markdown jika ada)
            clean_text = response_text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text.replace("```json", "").replace("```", "").strip()
            
            # Parse JSON
            analysis = json.loads(clean_text)
            
            # Format ke text yang readable
            formatted = f"""
**Performa:** {analysis.get('performa', 'N/A')}

**Kamera:** {analysis.get('kamera', 'N/A')}

**Baterai:** {analysis.get('baterai', 'N/A')}

**Value for Money:** {analysis.get('value_for_money', 'N/A')}

**Rekomendasi:** {analysis.get('rekomendasi', 'N/A')}
"""
            return formatted.strip()
            
        except json.JSONDecodeError:
            # Kalau gagal parse JSON, return as is
            return response_text
        
    except Exception as e:
        return f"Maaf, analisis AI sedang tidak tersedia. Error: {str(e)}"


def get_ai_recommendation(
    devices: List[models.Phone],
    use_case: Optional[str] = None,
    max_price: Optional[float] = None
) -> Dict[str, any]:
    """
    Mendapatkan rekomendasi device dari Grok AI berdasarkan use case.
    
    Args:
        devices: List device yang sudah di-filter
        use_case: Use case user (gaming, fotografi, kerja, dll)
        max_price: Budget maksimal user
    
    Returns:
        Dictionary berisi ranking devices + penjelasan AI
    """
    try:
        # Buat daftar device untuk prompt
        device_list = ""
        for i, device in enumerate(devices[:3], 1):
            device_list += f"{i}. {device.name} - Rp {device.price:,.0f} ({device.release_year})\n"
        
        # Buat prompt
        use_case_text = f"untuk {use_case}" if use_case else ""
        budget_text = f"budget max Rp {max_price:,.0f}" if max_price else ""
        
        user_prompt = f"""Rekomendasi smartphone {use_case_text} {budget_text}:

{device_list}

Kamu wajib memberikan output dalam format JSON berikut:

{{
  "top_1": "Nama device dan alasan singkat",
  "top_2": "Nama device dan alasan singkat",
  "top_3": "Nama device dan alasan singkat",
  "summary": "Kesimpulan singkat 1-2 kalimat"
}}

Jangan gunakan format lain. Hanya kirim JSON yang valid. Jawab dalam bahasa Indonesia."""

        messages = [
            {
                "role": "system",
                "content": "Kamu adalah asisten ahli teknologi yang membantu user memilih smartphone. Selalu jawab dalam format JSON yang valid."
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
        
        # Call AI API
        response_text = call_ai_api(messages, temperature=0.7)
        
        # Parse JSON response
        try:
            clean_text = response_text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text.replace("```json", "").replace("```", "").strip()
            
            recommendation = json.loads(clean_text)
            
            # Format ke text
            formatted = f"""
**Top 3 Rekomendasi:**

1. {recommendation.get('top_1', 'N/A')}
2. {recommendation.get('top_2', 'N/A')}
3. {recommendation.get('top_3', 'N/A')}

**Kesimpulan:** {recommendation.get('summary', 'N/A')}
"""
            
            return {
                "devices": devices[:3],
                "ai_recommendation": formatted.strip()
            }
            
        except json.JSONDecodeError:
            return {
                "devices": devices[:3],
                "ai_recommendation": response_text
            }
        
    except Exception as e:
        return {
            "devices": devices[:3],
            "ai_recommendation": f"Maaf, rekomendasi AI sedang tidak tersedia. Error: {str(e)}"
        }


def test_ai_connection() -> bool:
    """
    Test koneksi ke AI API.
    
    Returns:
        True jika berhasil, False jika gagal
    """
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello World' and nothing else."}
        ]
        response = call_ai_api(messages, temperature=0)
        return "hello" in response.lower()
    except Exception as e:
        print(f"Error testing AI connection: {str(e)}")
        return False
