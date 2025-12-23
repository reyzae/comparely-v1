# Dokumentasi API - Fitur AI

## 🤖 Perbandingan Cerdas dengan AI

### **GET /compare/ai**

Bandingkan 2 perangkat dengan analisis mendalam dari Grok AI.

**Parameter Query:**
- `id1` (wajib): ID perangkat pertama
- `id2` (wajib): ID perangkat kedua

**Response:**
```json
{
  "device_1": { /* spesifikasi perangkat */ },
  "device_2": { /* spesifikasi perangkat */ },
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

## 🧠 Rekomendasi dengan AI

### **GET /recommendation/ai**

Dapatkan rekomendasi perangkat cerdas dengan analisis dari Grok AI.

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
    { /* spesifikasi perangkat 1 */ },
    { /* spesifikasi perangkat 2 */ },
    { /* spesifikasi perangkat 3 */ }
  ],
  "ai_recommendation": "**Top 3 Rekomendasi:**\n\n1. iPhone 15 128GB - Layar Super Retina XDR..."
}
```

**Contoh:**
```bash
curl -X GET "http://localhost:8000/recommendation/ai?max_price=12000000&use_case=multimedia&limit=3"
```

---

## 📝 Use Case yang Tersedia

- `gaming` - Gaming & performa tinggi
- `fotografi` - Fotografi & videografi
- `kerja` - Produktivitas & kerja
- `kuliah` - Kuliah & pembelajaran
- `multimedia` - Multimedia & entertainment

---

## ⚙️ Konfigurasi AI

**AI Provider**: Grok AI (xAI)
**Model**: grok-4-latest
**Bahasa Response**: Bahasa Indonesia
**Rata-rata Response Time**: 2-3 detik

---

## 🔧 Error Handling

Jika AI service gagal, endpoint akan mengembalikan fallback message:
```json
{
  "ai_analysis": "Maaf, analisis AI sedang tidak tersedia. Error: ..."
}
```

Fitur comparison/recommendation rule-based tetap berfungsi normal.

