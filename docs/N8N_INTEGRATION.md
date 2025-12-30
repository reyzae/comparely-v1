# Integrasi n8n untuk Fitur Highlight

## Overview

Dokumentasi lengkap untuk setup dan konfigurasi integrasi n8n dengan Comparely. n8n digunakan untuk memproses highlight perbandingan device dengan **custom AI algorithm** yang gratis (tidak perlu API berbayar).

---

## Prerequisites

1. **n8n self-hosted** sudah running di `n8n.wiracenter.com`
2. **Comparely backend** sudah terinstall dan berjalan
3. Akses ke n8n dashboard untuk membuat workflow

---

## Setup n8n Workflow

### Step 1: Login ke n8n

Buka browser dan akses: `https://n8n.wiracenter.com`

### Step 2: Create New Workflow

1. Click **"New Workflow"** di dashboard
2. Beri nama: `Comparely - Device Comparison AI`

### Step 3: Add Webhook Node

1. Click **"+"** untuk add node
2. Pilih **"Webhook"**
3. Konfigurasi:
   - **HTTP Method**: `POST`
   - **Path**: `comparison-highlight`
   - **Response Mode**: `When Last Node Finishes`
   - **Response Data**: `First Entry JSON`

4. **Save** node

### Step 4: Add Function Node

1. Click **"+"** setelah Webhook node
2. Pilih **"Code"** → **"Run Once for All Items"**
3. **Copy-paste** JavaScript code dari file `N8N_CUSTOM_AI_ALGORITHM.md`
4. **Save** node

### Step 5: Connect Nodes

1. Drag dari Webhook node ke Function node
2. Pastikan ada garis connecting keduanya

### Step 6: Activate Workflow

1. Click toggle **"Inactive"** → **"Active"** di kanan atas
2. Workflow sekarang live!

### Step 7: Copy Webhook URL

1. Click pada Webhook node
2. Copy **Production URL** (contoh: `https://n8n.wiracenter.com/webhook/comparison-highlight`)
3. Save URL ini untuk konfigurasi backend

---

## Konfigurasi Backend Comparely

### Step 1: Update .env File

Buat atau edit file `.env` di root folder Comparely:

```bash
# n8n Integration Configuration
N8N_WEBHOOK_URL=https://n8n.wiracenter.com/webhook/comparison-highlight
N8N_ENABLED=true
N8N_TIMEOUT=10
```

**Penjelasan:**
- `N8N_WEBHOOK_URL`: URL webhook dari n8n (dari Step 7 di atas)
- `N8N_ENABLED`: Set `true` untuk enable n8n, `false` untuk disable
- `N8N_TIMEOUT`: Timeout dalam detik (default: 10)

### Step 2: Restart Aplikasi

```bash
# Stop aplikasi (Ctrl+C jika running)
# Start ulang
uvicorn app.main:app --reload
```

---

## Testing Integration

### Test 1: Basic Comparison

1. Buka browser: `http://localhost:8000/compare?id1=1&id2=2`
2. Periksa response JSON

**Expected Response:**

```json
{
  "device_1": { ... },
  "device_2": { ... },
  "highlights": [
    {
      "category": "🎮 Gaming Performance",
      "winner": "iPhone 15 Pro",
      "reason": "Score performa 6% lebih tinggi dengan A17 Pro"
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

**Check:**
- ✅ `highlights` berisi array of objects (bukan string)
- ✅ `ai_summary` ada dan tidak kosong
- ✅ `scores` berisi performance/camera/battery scores
- ✅ `source` = `"n8n_ai"` (bukan `"rule_based"`)

### Test 2: Fallback Mechanism

1. Set `N8N_ENABLED=false` di `.env`
2. Restart aplikasi
3. Test comparison lagi

**Expected:**
- ✅ Response tetap berhasil (tidak error)
- ✅ `highlights` berisi simple strings
- ✅ `source` = `"rule_based"`

### Test 3: Error Handling

1. Set `N8N_WEBHOOK_URL=https://invalid-url.com/webhook`
2. Set `N8N_ENABLED=true`
3. Restart dan test

**Expected:**
- ✅ Response tetap berhasil (fallback ke rule-based)
- ✅ Check logs untuk error message
- ✅ User tidak melihat error

---

## Monitoring & Debugging

### Check n8n Execution Logs

1. Login ke n8n dashboard
2. Click **"Executions"** di sidebar
3. Lihat list executions dari workflow
4. Click execution untuk detail

**What to check:**
- ✅ Status: Success (hijau)
- ✅ Input data: device_1, device_2 ada
- ✅ Output data: ai_highlights, ai_summary ada

### Check Backend Logs

```bash
# Lihat logs aplikasi
# Cari log dari n8n_service
```

**Log messages:**
- `INFO: Sending comparison to n8n: iPhone 15 Pro vs Samsung Galaxy S24`
- `INFO: Successfully received response from n8n`
- `ERROR: n8n request timeout after 10 seconds` (jika timeout)
- `INFO: Using rule-based highlights (n8n not available)` (jika fallback)

---

## Troubleshooting

### Problem: `source` selalu `"rule_based"`

**Possible causes:**
1. `N8N_ENABLED=false` di `.env`
2. `N8N_WEBHOOK_URL` salah atau kosong
3. n8n workflow tidak active
4. n8n server down

**Solution:**
1. Check `.env` file
2. Verify webhook URL di n8n dashboard
3. Pastikan workflow toggle = "Active"
4. Test n8n URL di browser/Postman

---

### Problem: Response lambat (> 10 detik)

**Possible causes:**
1. n8n processing terlalu lama
2. Network latency tinggi
3. Function node code tidak optimal

**Solution:**
1. Increase `N8N_TIMEOUT` di `.env` (contoh: `15`)
2. Optimize JavaScript code di Function node
3. Check network connection

---

### Problem: `highlights` kosong atau format salah

**Possible causes:**
1. Function node code error
2. Input data tidak lengkap
3. Parsing error di JavaScript

**Solution:**
1. Check n8n execution logs untuk error
2. Verify input data di n8n
3. Test Function node code secara manual
4. Check `N8N_CUSTOM_AI_ALGORITHM.md` untuk code yang benar

---

### Problem: n8n workflow error

**Possible causes:**
1. JavaScript syntax error
2. Missing fields di input
3. Node configuration salah

**Solution:**
1. Check error message di n8n execution
2. Validate JavaScript code
3. Re-check webhook configuration
4. Test dengan sample data di n8n

---

## Advanced Configuration

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

### Add Authentication

Jika n8n webhook perlu authentication:

1. **Di n8n**: Enable authentication di Webhook node
2. **Di backend**: Update `n8n_service.py`:

```python
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_TOKEN_HERE"
}
```

### Disable n8n Temporarily

Tanpa restart aplikasi:

```python
# Set environment variable
import os
os.environ["N8N_ENABLED"] = "false"
```

Atau edit `.env` dan restart.

---

## Performance Tips

1. **Cache Results**: Implement caching untuk comparison yang sama
2. **Async Processing**: n8n call sudah non-blocking
3. **Batch Processing**: Untuk multiple comparisons, consider batch API
4. **Monitoring**: Setup monitoring untuk n8n uptime

---

## Security Considerations

1. **HTTPS Only**: Pastikan n8n menggunakan HTTPS
2. **Webhook Secret**: Add secret token untuk validate requests
3. **Rate Limiting**: Implement rate limiting di n8n
4. **Input Validation**: Validate data sebelum send ke n8n

---

## Next Steps

1. ✅ Setup n8n workflow
2. ✅ Configure backend
3. ✅ Test integration
4. 📝 Customize AI algorithm (lihat `N8N_CUSTOM_AI_ALGORITHM.md`)
5. 📊 Monitor performance
6. 🚀 Deploy to production

---

## Support

Untuk masalah atau pertanyaan:
- Check dokumentasi: `N8N_CUSTOM_AI_ALGORITHM.md`
- Review implementation plan: `implementation_plan.md`
- Check backend logs
- Review n8n execution logs
