"""
COMPARELY - Enhanced GSMArena Scraper
Fitur lengkap untuk scraping handphone dengan kualitas data terjamin

Fitur:
✅ Pencegahan duplicate data
✅ Filter data N/A (hanya ambil data lengkap)
✅ Progress tracking detail
✅ Auto-retry untuk koneksi gagal
✅ Export ke CSV dengan validasi

Author: Kelompok COMPARELY
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from fake_useragent import UserAgent
import os

# ==================== KONFIGURASI ====================

BASE_URL = "https://www.gsmarena.com"
OUTPUT_FILE = "data/scraped_phones.csv"

# Brand yang mau di-scrape
BRANDS = {
    "Samsung": "samsung-phones-9",
    "Xiaomi": "xiaomi-phones-80",
    "Oppo": "oppo-phones-82",
    "Vivo": "vivo-phones-98",
    "Infinix": "infinix-phones-119"
}

# Berapa banyak model per brand (akan scrape lebih banyak untuk kompensasi yang di-skip)
MODELS_TO_SCRAPE = 30  # Scrape 30, harapan dapat 20 yang complete
MAX_RETRIES = 3  # Retry jika koneksi gagal

# ==================== FUNGSI HELPER ====================

def get_random_user_agent():
    """Generate random user agent untuk menghindari deteksi bot"""
    ua = UserAgent()
    return ua.random

def is_data_complete(phone_data):
    """
    Validasi apakah data handphone lengkap
    
    Field wajib: camera, battery, ram, storage
    Nama tidak boleh Unknown
    """
    required_fields = ['camera', 'battery', 'ram', 'storage']
    
    # Cek setiap field wajib
    for field in required_fields:
        value = phone_data.get(field, 'N/A')
        if not value or value == 'N/A' or value == 'Unknown':
            return False
    
    # Pastikan nama bukan Unknown
    if phone_data.get('name') == 'Unknown':
        return False
    
    return True

def is_duplicate(phone_data, existing_phones):
    """
    Cek apakah handphone sudah ada di list (duplicate)
    
    Kriteria duplicate: nama sama DAN brand sama
    """
    for existing in existing_phones:
        if (existing['name'] == phone_data['name'] and 
            existing['brand'] == phone_data['brand']):
            return True
    return False

# ==================== FUNGSI SCRAPING ====================

def scrape_phone_list(brand_name, brand_url):
    """
    Ambil daftar URL handphone dari halaman brand
    
    Returns:
        List of phone URLs
    """
    print(f"\n🔍 Mengambil daftar {brand_name}...")
    
    url = f"{BASE_URL}/{brand_url}.php"
    headers = {'User-Agent': get_random_user_agent()}
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            phone_links = []
            
            # Cari div.general-menu yang berisi list handphone
            general_menu = soup.find('div', class_='general-menu')
            if general_menu:
                links = general_menu.find_all('a')
                for link in links:
                    if 'href' in link.attrs and '.php' in link['href']:
                        phone_url = BASE_URL + "/" + link['href']
                        phone_links.append(phone_url)
                        
                        if len(phone_links) >= MODELS_TO_SCRAPE:
                            break
            
            print(f"   ✅ Berhasil dapat {len(phone_links)} model {brand_name}")
            return phone_links[:MODELS_TO_SCRAPE]
            
        except Exception as e:
            print(f"   ⚠️ Attempt {attempt + 1}/{MAX_RETRIES} gagal: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2)
            else:
                print(f"   ❌ Gagal mengambil daftar {brand_name}")
                return []

def scrape_phone_details(phone_url, brand_name):
    """
    Scrape detail spesifikasi dari halaman produk
    
    Returns:
        Dictionary berisi data spesifikasi atau None jika gagal
    """
    headers = {'User-Agent': get_random_user_agent()}
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(phone_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Ambil nama - coba beberapa selector
            name = "Unknown"
            name_tag = soup.find('h1', class_='specs-phone-name-title')
            if name_tag:
                name = name_tag.text.strip()
            else:
                # Fallback: ambil dari title
                title_tag = soup.find('title')
                if title_tag:
                    title_text = title_tag.text.strip()
                    if ' - ' in title_text:
                        name = title_text.split(' - ')[0].strip()
            
            # Ambil gambar
            img_tag = soup.find('div', class_='specs-photo-main')
            if img_tag:
                img_tag = img_tag.find('img')
            image_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else ""
            
            # Inisialisasi data
            phone_data = {
                'name': name,
                'brand': brand_name,
                'category_id': 1,
                'cpu': 'N/A',
                'gpu': 'N/A',
                'ram': 'N/A',
                'storage': 'N/A',
                'camera': 'N/A',
                'battery': 'N/A',
                'screen': 'N/A',
                'release_year': 2024,
                'price': 0,
                'image_url': image_url,
                'source_data': phone_url
            }
            
            # Scrape spesifikasi dari tabel
            spec_tables = soup.find_all('table', attrs={'cellspacing': '0'})
            
            for table in spec_tables:
                rows = table.find_all('tr')
                
                for row in rows:
                    header = row.find('td', class_='ttl')
                    value = row.find('td', class_='nfo')
                    
                    if header and value:
                        field_name = header.text.strip().lower()
                        field_value = value.text.strip()
                        
                        # CPU/Chipset
                        if 'chipset' in field_name:
                            phone_data['cpu'] = field_value
                        
                        # GPU
                        elif 'gpu' in field_name:
                            phone_data['gpu'] = field_value
                        
                        # RAM & Storage
                        elif 'internal' in field_name:
                            if 'GB' in field_value:
                                parts = field_value.split()
                                storage_parts = []
                                ram_parts = []
                                
                                for i, part in enumerate(parts):
                                    if 'GB' in part:
                                        if i + 1 < len(parts) and 'RAM' in parts[i + 1].upper():
                                            if i > 0 and parts[i-1].replace('.', '').isdigit():
                                                ram_parts.append(parts[i-1] + part)
                                        else:
                                            if i > 0 and parts[i-1].replace('.', '').isdigit():
                                                storage_parts.append(parts[i-1] + part)
                                            elif part[0].isdigit():
                                                storage_parts.append(part)
                                
                                if storage_parts:
                                    phone_data['storage'] = storage_parts[0]
                                if ram_parts:
                                    phone_data['ram'] = ram_parts[0]
                        
                        # Camera
                        elif 'camera' in field_name and phone_data['camera'] == 'N/A':
                            if 'single' not in field_name.lower() and 'selfie' not in field_name.lower():
                                phone_data['camera'] = field_value
                        
                        # Battery
                        elif 'battery' in field_name and phone_data['battery'] == 'N/A':
                            if 'mAh' in field_value or 'Wh' in field_value:
                                phone_data['battery'] = field_value
                        
                        # Screen
                        elif 'size' in field_name and phone_data['screen'] == 'N/A':
                            phone_data['screen'] = field_value
                        
                        # Release Year
                        elif 'announced' in field_name:
                            try:
                                year_str = field_value.split(',')[0].strip()
                                if year_str.isdigit() and len(year_str) == 4:
                                    phone_data['release_year'] = int(year_str)
                            except:
                                pass
            
            return phone_data
            
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(1)
            else:
                return None

# ==================== FUNGSI UTAMA ====================

def main():
    """Fungsi utama untuk menjalankan scraper"""
    
    print("=" * 80)
    print("🚀 COMPARELY - Enhanced GSMArena Scraper")
    print("=" * 80)
    print("Fitur:")
    print("  ✅ Filter data N/A (hanya ambil data lengkap)")
    print("  ✅ Pencegahan duplicate")
    print("  ✅ Auto-retry koneksi gagal")
    print("=" * 80)
    print(f"Target: {MODELS_TO_SCRAPE} model per brand")
    print(f"Brands: {', '.join(BRANDS.keys())}")
    print("=" * 80)
    
    all_phones = []
    stats = {
        'total_scraped': 0,
        'complete': 0,
        'skipped_incomplete': 0,
        'skipped_duplicate': 0
    }
    
    # Loop untuk setiap brand
    for brand_name, brand_url in BRANDS.items():
        print(f"\n📱 Memproses brand: {brand_name}")
        
        # Ambil daftar handphone
        phone_urls = scrape_phone_list(brand_name, brand_url)
        
        if not phone_urls:
            print(f"   ⚠️ Tidak ada URL ditemukan untuk {brand_name}")
            continue
        
        brand_complete = 0
        
        # Scrape detail setiap handphone
        for idx, phone_url in enumerate(phone_urls, 1):
            print(f"   [{idx}/{len(phone_urls)}] {phone_url.split('/')[-1]}")
            
            phone_data = scrape_phone_details(phone_url, brand_name)
            stats['total_scraped'] += 1
            
            if not phone_data:
                print(f"      ❌ Gagal scraping")
                continue
            
            # Validasi: cek duplicate
            if is_duplicate(phone_data, all_phones):
                stats['skipped_duplicate'] += 1
                print(f"      ⏭️  DUPLICATE: {phone_data['name']}")
                continue
            
            # Validasi: cek data lengkap
            if not is_data_complete(phone_data):
                stats['skipped_incomplete'] += 1
                missing = [f for f in ['camera', 'battery', 'ram', 'storage'] 
                          if phone_data.get(f) == 'N/A']
                print(f"      ⏭️  INCOMPLETE: {phone_data['name']} (Missing: {', '.join(missing)})")
                continue
            
            # Data valid! Simpan
            all_phones.append(phone_data)
            brand_complete += 1
            stats['complete'] += 1
            print(f"      ✅ SAVED: {phone_data['name']}")
            
            # Delay anti rate-limit
            delay = random.uniform(1, 3)
            time.sleep(delay)
        
        print(f"\n   📊 {brand_name}: {brand_complete} complete dari {len(phone_urls)} scraped")
    
    # Save ke CSV
    if all_phones:
        # Buat folder data jika belum ada
        os.makedirs('data', exist_ok=True)
        
        fieldnames = [
            'name', 'brand', 'category_id', 'cpu', 'gpu', 'ram', 
            'storage', 'camera', 'battery', 'screen', 'release_year', 
            'price', 'image_url', 'source_data'
        ]
        
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_phones)
        
        print("\n" + "=" * 80)
        print("✨ SCRAPING SELESAI!")
        print("=" * 80)
        print(f"📊 STATISTIK:")
        print(f"   Total scraped      : {stats['total_scraped']}")
        print(f"   ✅ Complete & saved : {stats['complete']}")
        print(f"   ⏭️  Skipped (N/A)    : {stats['skipped_incomplete']}")
        print(f"   ⏭️  Skipped (Dup)    : {stats['skipped_duplicate']}")
        print(f"\n📁 File tersimpan: {OUTPUT_FILE}")
        print("=" * 80)
        print("\n💡 Langkah selanjutnya:")
        print("   1. Cek file CSV: notepad data/scraped_phones.csv")
        print("   2. Import ke DB: python import_csv.py data/scraped_phones.csv")
        print("=" * 80)
    else:
        print("\n❌ Tidak ada data yang berhasil di-scrape!")

if __name__ == "__main__":
    main()
