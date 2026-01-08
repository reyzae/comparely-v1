# Cara Integrasi n8n buat Fitur Highlight

Ini dokumentasi lengkap buat setup dan konfigurasi integrasi n8n dengan Comparely. n8n dipake buat proses highlight perbandingan HP pake **algoritma AI custom** yang gratis (gak perlu bayar API).

---

## Yang Perlu Disiapkan

1. **n8n self-hosted** udah jalan di `n8n.wiracenter.com`
2. **Backend Comparely** udah terinstall dan running
3. Akses ke dashboard n8n buat bikin workflow

---

## Setup Workflow n8n

### Langkah 1: Login ke n8n

Buka browser dan akses: `https://n8n.wiracenter.com`

### Langkah 2: Bikin Workflow Baru

1. Klik **"New Workflow"** di dashboard
2. Kasih nama: `Comparely - Device Comparison AI`

### Langkah 3: Tambahin Webhook Node

1. Klik **"+"** buat add node
2. Pilih **"Webhook"**
3. Konfigurasi:
   - **HTTP Method**: `POST`
   - **Path**: `comparison-highlight`
   - **Response Mode**: `When Last Node Finishes`
   - **Response Data**: `First Entry JSON`

4. **Save** node

### Langkah 4: Tambahin Function Node

1. Klik **"+"** setelah Webhook node
2. Pilih **"Code"** → **"Run Once for All Items"**
3. **Copy-paste** kode JavaScript dari file `N8N_CUSTOM_AI_ALGORITHM.md`
4. **Save** node

### Langkah 5: Hubungkan Node

1. Drag dari Webhook node ke Function node
2. Pastiin ada garis yang nyambungin keduanya

### Langkah 6: Aktifkan Workflow

1. Klik toggle **"Inactive"** → **"Active"** di kanan atas
2. Workflow sekarang udah live!

### Langkah 7: Copy URL Webhook

1. Klik pada Webhook node
2. Copy **Production URL** (contoh: `https://n8n.wiracenter.com/webhook/comparison-highlight`)
3. Simpen URL ini buat konfigurasi backend

---

## Konfigurasi Backend Comparely

### Langkah 1: Update File .env

Bikin atau edit file `.env` di root folder Comparely:

```bash
# Konfigurasi Integrasi n8n
N8N_WEBHOOK_URL=https://n8n.wiracenter.com/webhook/comparison-highlight
N8N_ENABLED=true
N8N_TIMEOUT=10
```

**Penjelasan:**
- `N8N_WEBHOOK_URL`: URL webhook dari n8n (dari Langkah 7 di atas)
- `N8N_ENABLED`: Set `true` buat enable n8n, `false` buat disable
- `N8N_TIMEOUT`: Timeout dalam detik (default: 10)

### Langkah 2: Restart Aplikasi

```bash
# Stop aplikasi (Ctrl+C kalau lagi running)
# Start ulang
uvicorn app.main:app --reload
```

---

## Testing Integrasi

### Test 1: Perbandingan Dasar

1. Buka browser: `http://localhost:8000/compare?id1=1&id2=2`
2. Cek response JSON

**Response yang Diharapkan:**

```json
{
  "device_1": { ... },
  "device_2": { ... },
  "highlights": [
    {
      "category": "🎮 Performa Gaming",
      "winner": "iPhone 15 Pro",
      "reason": "Skor performa 6% lebih tinggi pake A17 Pro"
    },
    ...
  ],
  "ai_summary": "Samsung Galaxy S24 unggul di 4 dari 5 kategori.",
  "scores": {
    "device1": { ... },
    "device2": { ... }
  },
  "source": "n8n_ai"
}
```

**Yang Perlu Dicek:**
- `highlights` berisi array of objects (bukan string)
- `ai_summary` ada dan gak kosong
- `scores` berisi skor performance/camera/battery
- `source` = `"n8n_ai"` (bukan `"rule_based"`)

### Test 2: Mekanisme Fallback

1. Set `N8N_ENABLED=false` di `.env`
2. Restart aplikasi
3. Test comparison lagi

**Yang Diharapkan:**
- Response tetap berhasil (gak error)
- `highlights` berisi string sederhana
- `source` = `"rule_based"`

### Test 3: Error Handling

1. Set `N8N_WEBHOOK_URL=https://invalid-url.com/webhook`
2. Set `N8N_ENABLED=true`
3. Restart dan test

**Yang Diharapkan:**
- Response tetap berhasil (fallback ke rule-based)
- Cek logs buat error message
- User gak liat error

---

## Monitoring & Debugging

### Cek Log Eksekusi n8n

1. Login ke dashboard n8n
2. Klik **"Executions"** di sidebar
3. Liat list eksekusi dari workflow
4. Klik eksekusi buat detail

**Yang Perlu Dicek:**
- Status: Success (hijau)
- Input data: device_1, device_2 ada
- Output data: ai_highlights, ai_summary ada

### Cek Log Backend

```bash
# Liat logs aplikasi
# Cari log dari n8n_service
```

**Pesan Log:**
- `INFO: Sending comparison to n8n: iPhone 15 Pro vs Samsung Galaxy S24`
- `INFO: Successfully received response from n8n`
- `ERROR: n8n request timeout after 10 seconds` (kalau timeout)
- `INFO: Using rule-based highlights (n8n not available)` (kalau fallback)

---

## Troubleshooting

### Masalah: `source` selalu `"rule_based"`

**Kemungkinan Penyebab:**
1. `N8N_ENABLED=false` di `.env`
2. `N8N_WEBHOOK_URL` salah atau kosong
3. Workflow n8n gak aktif
4. Server n8n down

**Solusi:**
1. Cek file `.env`
2. Verify URL webhook di dashboard n8n
3. Pastiin workflow toggle = "Active"
4. Test URL n8n di browser/Postman

---

### Masalah: Response lambat (> 10 detik)

**Kemungkinan Penyebab:**
1. Proses n8n terlalu lama
2. Network latency tinggi
3. Kode Function node gak optimal

**Solusi:**
1. Naikin `N8N_TIMEOUT` di `.env` (contoh: `15`)
2. Optimasi kode JavaScript di Function node
3. Cek koneksi network

---

### Masalah: `highlights` kosong atau format salah

**Kemungkinan Penyebab:**
1. Kode Function node error
2. Input data gak lengkap
3. Parsing error di JavaScript

**Solusi:**
1. Cek log eksekusi n8n buat error
2. Verify input data di n8n
3. Test kode Function node secara manual
4. Cek `N8N_CUSTOM_AI_ALGORITHM.md` buat kode yang bener

---

### Masalah: Workflow n8n error

**Kemungkinan Penyebab:**
1. Syntax error JavaScript
2. Field yang hilang di input
3. Konfigurasi node salah

**Solusi:**
1. Cek error message di eksekusi n8n
2. Validasi kode JavaScript
3. Re-check konfigurasi webhook
4. Test pake sample data di n8n

---

## Konfigurasi Advanced

### Custom Timeout per Request

Edit `app/services/n8n_service.py`:

```python
# Line ~70
response = requests.post(
    config.N8N_WEBHOOK_URL,
    json=payload,
    timeout=15,  # Custom timeout (override config)
    headers={"Content-Type": "application/json"}
)
```

### Tambahin Authentication

Kalau webhook n8n perlu authentication:

1. **Di n8n**: Enable authentication di Webhook node
2. **Di backend**: Update `n8n_service.py`:

```python
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_TOKEN_HERE"
}
```

### Disable n8n Sementara

Tanpa restart aplikasi:

```python
# Set environment variable
import os
os.environ["N8N_ENABLED"] = "false"
```

Atau edit `.env` dan restart.

---

## Tips Performa

1. **Cache Results**: Implement caching buat comparison yang sama
2. **Async Processing**: Call n8n udah non-blocking
3. **Batch Processing**: Buat multiple comparisons, pertimbangin batch API
4. **Monitoring**: Setup monitoring buat n8n uptime

---

## Pertimbangan Keamanan

1. **HTTPS Only**: Pastiin n8n pake HTTPS
2. **Webhook Secret**: Tambahin secret token buat validasi request
3. **Rate Limiting**: Implement rate limiting di n8n
4. **Input Validation**: Validasi data sebelum kirim ke n8n

---

## Langkah Selanjutnya

1. Setup workflow n8n
2. Konfigurasi backend
3. Test integrasi
4. Kustomisasi algoritma AI (liat `N8N_CUSTOM_AI_ALGORITHM.md`)
5. Monitor performa
6. Deploy ke production

---

## Bantuan

Kalau ada masalah atau pertanyaan:
- Cek dokumentasi: `N8N_CUSTOM_AI_ALGORITHM.md`
- Review implementation plan: `implementation_plan.md`
- Cek backend logs
- Review log eksekusi n8n
