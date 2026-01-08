# Dokumentasi API - Fitur AI

## Perbandingan Cerdas pake AI

### **GET /compare/ai**

Bandingin 2 HP dengan analisis mendalam dari Grok AI.

**Parameter Query:**
- `id1` (wajib): ID HP pertama
- `id2` (wajib): ID HP kedua

**Response:**
```json
{
  "device_1": { /* spesifikasi HP */ },
  "device_2": { /* spesifikasi HP */ },
  "highlights": [
    "xiaomi redmi 4x lebih murah Rp 11,000,000",
    "iphone 15 128gb lebih baru (Rilis 2023)"
  ],
  "ai_analysis": "**Performa:** iPhone 15 dengan CPU A16 Bionic..."
}
```

**Contoh:**
```bash
curl -X GET "http://localhost:8000/compare/ai?id1=10&id2=11"
```

---

## Rekomendasi pake AI

### **GET /recommendation/ai**

Dapetin rekomendasi HP cerdas dengan analisis dari Grok AI.

**Parameter Query:**
- `max_price` (opsional): Budget maksimal
- `category_id` (opsional): Filter berdasarkan kategori
- `min_release_year` (opsional): Tahun rilis minimal
- `use_case` (opsional): Use case (gaming, fotografi, kerja, kuliah, multimedia)
- `limit` (opsional, default=5): Jumlah hasil maksimal

**Response:**
```json
{
  "devices": [
    { /* spesifikasi HP 1 */ },
    { /* spesifikasi HP 2 */ },
    { /* spesifikasi HP 3 */ }
  ],
  "ai_recommendation": "**Top 3 Rekomendasi:**\n\n1. iPhone 15 128GB - Layar Super Retina XDR..."
}
```

**Contoh:**
```bash
curl -X GET "http://localhost:8000/recommendation/ai?max_price=12000000&use_case=multimedia&limit=3"
```

---

## Use Case yang Tersedia

- `gaming` - Gaming & performa tinggi
- `fotografi` - Fotografi & videografi
- `kerja` - Produktivitas & kerja
- `kuliah` - Kuliah & pembelajaran
- `multimedia` - Multimedia & entertainment

---

## Konfigurasi AI

**AI Provider**: Grok AI (xAI)
**Model**: grok-4-latest
**Bahasa Response**: Bahasa Indonesia
**Rata-rata Response Time**: 2-3 detik

---

## Error Handling

Kalau AI service gagal, endpoint bakal return fallback message:
```json
{
  "ai_analysis": "Maaf, analisis AI sedang gak tersedia. Error: ..."
}
```

Fitur comparison/recommendation rule-based tetap jalan normal.
