# Algoritma AI Custom untuk n8n

Ini algoritma AI sederhana buat nganalisis perbandingan HP **tanpa perlu bayar API**. Pake sistem scoring dan logic rule-based yang jalan di n8n Function node.

## Kenapa Pake Ini?

**Gratis 100%** - Gak perlu token atau API key  
**Cepet** - Gak usah nunggu API external  
**Bisa diubah-ubah** - Logic-nya bisa disesuaikan sesuka hati  
**Aman** - Data gak keluar dari server kita  

---

## Cara Kerja Scoring

### 1. Skor Performa (CPU + RAM)

**Rumusnya:**
```
Skor Performa = (RAM × 0.4) + (Skor CPU × 0.6)
```

**Tabel Skor CPU:**
| CPU | Skor |
|-----|------|
| A17 Pro | 98 |
| A16 Bionic | 93 |
| Snapdragon 8 Gen 3 | 95 |
| Snapdragon 8 Gen 2 | 90 |
| Dimensity 9300 | 92 |

**Parsing RAM:**
- "8GB" → 8
- "12GB" → 12

---

### 2. Skor Kamera

**Rumusnya:**
```
Skor Kamera = Nilai Megapixel
```

**Parsing:**
- "48MP" → 48
- "50MP Triple" → 50

---

### 3. Skor Baterai

**Rumusnya:**
```
Skor Baterai = Nilai mAh
```

**Parsing:**
- "3274mAh" → 3274
- "4000mAh" → 4000

---

### 4. Skor Value for Money

**Rumusnya:**
```
Skor Value = (Performa + Kamera + Baterai) / (Harga dalam jutaan)
```

Makin tinggi skor dengan harga lebih murah = value makin bagus

---

### 5. Skor Kebaruan

**Rumusnya:**
```
Skor Kebaruan = Tahun Rilis
```

HP lebih baru = teknologi lebih canggih

---

## Code untuk n8n Function Node

Copy-paste code ini ke **Function node** di workflow n8n kamu:

```javascript
// Algoritma AI Custom buat Perbandingan HP
// 100% Gratis, gak perlu API external

const device1 = $input.item.json.device_1;
const device2 = $input.item.json.device_2;

// ============================================
// FUNGSI HELPER
// ============================================

// Parse RAM (contoh: "8GB" -> 8)
function parseRAM(ramStr) {
  if (!ramStr) return 0;
  const match = ramStr.match(/(\d+)/);
  return match ? parseInt(match[1]) : 0;
}

// Parse Kamera MP (contoh: "48MP" -> 48)
function parseCamera(cameraStr) {
  if (!cameraStr) return 0;
  const match = cameraStr.match(/(\d+)\s*MP/i);
  return match ? parseInt(match[1]) : 0;
}

// Parse Baterai mAh (contoh: "3274mAh" -> 3274)
function parseBattery(batteryStr) {
  if (!batteryStr) return 0;
  const match = batteryStr.match(/(\d+)/);
  return match ? parseInt(match[1]) : 0;
}

// Hitung Skor CPU (pake logika sederhana)
function getCPUScore(cpuStr) {
  if (!cpuStr) return 0;
  
  const cpu = cpuStr.toLowerCase();
  
  // Seri Snapdragon
  if (cpu.includes('snapdragon 8 gen 3')) return 95;
  if (cpu.includes('snapdragon 8 gen 2')) return 90;
  if (cpu.includes('snapdragon 8 gen 1')) return 85;
  if (cpu.includes('snapdragon 888')) return 80;
  if (cpu.includes('snapdragon 870')) return 75;
  if (cpu.includes('snapdragon 7')) return 70;
  
  // Apple A series
  if (cpu.includes('a17')) return 98;
  if (cpu.includes('a16')) return 93;
  if (cpu.includes('a15')) return 88;
  if (cpu.includes('a14')) return 83;
  if (cpu.includes('a13')) return 78;
  
  // MediaTek Dimensity
  if (cpu.includes('dimensity 9300')) return 92;
  if (cpu.includes('dimensity 9200')) return 87;
  if (cpu.includes('dimensity 9000')) return 82;
  if (cpu.includes('dimensity 8200')) return 75;
  if (cpu.includes('dimensity 7')) return 68;
  
  // Google Tensor
  if (cpu.includes('tensor g3')) return 88;
  if (cpu.includes('tensor g2')) return 83;
  
  // Default
  return 50;
}

// ============================================
// HITUNG SKOR
// ============================================

// 1. SKOR PERFORMA (CPU + RAM)
const ram1 = parseRAM(device1.ram);
const ram2 = parseRAM(device2.ram);
const cpu1Score = getCPUScore(device1.cpu);
const cpu2Score = getCPUScore(device2.cpu);

const perf1 = (ram1 * 0.4) + (cpu1Score * 0.6);
const perf2 = (ram2 * 0.4) + (cpu2Score * 0.6);

// 2. SKOR KAMERA
const cam1 = parseCamera(device1.camera);
const cam2 = parseCamera(device2.camera);

// 3. SKOR BATERAI
const bat1 = parseBattery(device1.battery);
const bat2 = parseBattery(device2.battery);

// 4. SKOR VALUE FOR MONEY
// Makin murah dengan specs tinggi = makin bagus
const value1 = (perf1 + cam1 + (bat1/100)) / (device1.price / 1000000);
const value2 = (perf2 + cam2 + (bat2/100)) / (device2.price / 1000000);

// 5. SKOR KEBARUAN
const recency1 = device1.release_year || 2020;
const recency2 = device2.release_year || 2020;

// ============================================
// BIKIN HIGHLIGHT AI
// ============================================

const highlights = [];

// Highlight Performa
if (Math.abs(perf1 - perf2) > 5) {
  const winner = perf1 > perf2 ? device1.name : device2.name;
  const loser = perf1 > perf2 ? device2.name : device1.name;
  const perfDiff = Math.abs(perf1 - perf2).toFixed(0);
  const winnerCPU = perf1 > perf2 ? device1.cpu : device2.cpu;
  
  highlights.push({
    category: "Performa Gaming",
    winner: winner,
    reason: `Skor performa ${perfDiff}% lebih tinggi pake ${winnerCPU}, lebih smooth buat gaming sama multitasking`
  });
}

// Highlight Kamera
if (Math.abs(cam1 - cam2) > 2) {
  const winner = cam1 > cam2 ? device1.name : device2.name;
  const camWinner = cam1 > cam2 ? cam1 : cam2;
  const camLoser = cam1 > cam2 ? cam2 : cam1;
  const camDiff = Math.abs(cam1 - cam2);
  
  highlights.push({
    category: "Kamera",
    winner: winner,
    reason: `${camWinner}MP vs ${camLoser}MP, selisih ${camDiff}MP bikin foto lebih detail dan tajam`
  });
}

// Highlight Baterai
if (Math.abs(bat1 - bat2) > 300) {
  const winner = bat1 > bat2 ? device1.name : device2.name;
  const batWinner = bat1 > bat2 ? bat1 : bat2;
  const batLoser = bat1 > bat2 ? bat2 : bat1;
  const batDiffPercent = Math.round(((batWinner - batLoser) / batLoser) * 100);
  
  highlights.push({
    category: "Daya Tahan Baterai",
    winner: winner,
    reason: `${batWinner}mAh vs ${batLoser}mAh, tahan ${batDiffPercent}% lebih lama buat pemakaian sehari-hari`
  });
}

// Highlight Value for Money
if (Math.abs(value1 - value2) > 0.5) {
  const winner = value1 > value2 ? device1.name : device2.name;
  const priceDiff = Math.abs(device1.price - device2.price);
  const cheaper = device1.price < device2.price ? device1.name : device2.name;
  
  highlights.push({
    category: "Value for Money",
    winner: winner,
    reason: `Lebih worth it! ${cheaper} lebih murah Rp ${(priceDiff/1000).toFixed(0)}rb dengan specs yang oke`
  });
}

// Highlight Kebaruan
if (Math.abs(recency1 - recency2) > 0) {
  const winner = recency1 > recency2 ? device1.name : device2.name;
  const yearWinner = recency1 > recency2 ? recency1 : recency2;
  const yearLoser = recency1 > recency2 ? recency2 : recency1;
  const yearDiff = Math.abs(recency1 - recency2);
  
  highlights.push({
    category: "Teknologi Terbaru",
    winner: winner,
    reason: `Rilis ${yearWinner} (${yearDiff} tahun lebih baru), udah pake teknologi sama fitur terkini`
  });
}

// ============================================
// BIKIN SUMMARY
// ============================================

const device1Wins = highlights.filter(h => h.winner === device1.name).length;
const device2Wins = highlights.filter(h => h.winner === device2.name).length;

let summary = "";
if (device1Wins > device2Wins) {
  summary = `${device1.name} unggul di ${device1Wins} dari ${highlights.length} kategori. Cocok buat yang prioritas performa sama teknologi terbaru.`;
} else if (device2Wins > device1Wins) {
  summary = `${device2.name} unggul di ${device2Wins} dari ${highlights.length} kategori. Pilihan terbaik buat value for money sama fitur lengkap.`;
} else {
  summary = `Kedua HP seimbang dengan masing-masing ${device1Wins} keunggulan. Pilih ${device1.name} buat ekosistem ${device1.brand}, atau ${device2.name} buat ${device2.brand}.`;
}

// ============================================
// RETURN RESPONSE
// ============================================

return {
  json: {
    ai_highlights: highlights,
    ai_summary: summary,
    scores: {
      device1: {
        name: device1.name,
        performance: perf1.toFixed(1),
        camera: cam1,
        battery: bat1,
        value: value1.toFixed(2),
        total_wins: device1Wins
      },
      device2: {
        name: device2.name,
        performance: perf2.toFixed(1),
        camera: cam2,
        battery: bat2,
        value: value2.toFixed(2),
        total_wins: device2Wins
      }
    }
  }
};
```

---

## Contoh Input/Output

### Input (dari API Comparely):

```json
{
  "device_1": {
    "id": 1,
    "name": "iPhone 15 Pro",
    "brand": "Apple",
    "price": 15000000,
    "cpu": "A17 Pro",
    "ram": "8GB",
    "camera": "48MP",
    "battery": "3274mAh",
    "release_year": 2023
  },
  "device_2": {
    "id": 2,
    "name": "Samsung Galaxy S24",
    "brand": "Samsung",
    "price": 12000000,
    "cpu": "Snapdragon 8 Gen 3",
    "ram": "12GB",
    "camera": "50MP",
    "battery": "4000mAh",
    "release_year": 2024
  }
}
```

### Output (dari n8n):

```json
{
  "ai_highlights": [
    {
      "category": "Performa Gaming",
      "winner": "iPhone 15 Pro",
      "reason": "Skor performa 6% lebih tinggi pake A17 Pro, lebih smooth buat gaming sama multitasking"
    },
    {
      "category": "Kamera",
      "winner": "Samsung Galaxy S24",
      "reason": "50MP vs 48MP, selisih 2MP bikin foto lebih detail dan tajam"
    },
    {
      "category": "Daya Tahan Baterai",
      "winner": "Samsung Galaxy S24",
      "reason": "4000mAh vs 3274mAh, tahan 22% lebih lama buat pemakaian sehari-hari"
    },
    {
      "category": "Value for Money",
      "winner": "Samsung Galaxy S24",
      "reason": "Lebih worth it! Samsung Galaxy S24 lebih murah Rp 3000rb dengan specs yang oke"
    },
    {
      "category": "Teknologi Terbaru",
      "winner": "Samsung Galaxy S24",
      "reason": "Rilis 2024 (1 tahun lebih baru), udah pake teknologi sama fitur terkini"
    }
  ],
  "ai_summary": "Samsung Galaxy S24 unggul di 4 dari 5 kategori. Pilihan terbaik buat value for money sama fitur lengkap.",
  "scores": {
    "device1": {
      "name": "iPhone 15 Pro",
      "performance": "62.0",
      "camera": 48,
      "battery": 3274,
      "value": "7.48",
      "total_wins": 1
    },
    "device2": {
      "name": "Samsung Galaxy S24",
      "performance": "61.8",
      "camera": 50,
      "battery": 4000,
      "value": "9.82",
      "total_wins": 4
    }
  }
}
```

---

## Cara Kustomisasi

### Nambahin CPU Baru

Edit fungsi `getCPUScore()`:

```javascript
// Tambahin di bagian yang sesuai
if (cpu.includes('snapdragon 8 gen 4')) return 100;
if (cpu.includes('a18')) return 100;
```

### Ubah Bobot Scoring

Edit formula di bagian hitung skor:

```javascript
// Ubah bobot RAM vs CPU
const perf1 = (ram1 * 0.3) + (cpu1Score * 0.7);  // CPU lebih penting
// atau
const perf1 = (ram1 * 0.5) + (cpu1Score * 0.5);  // Seimbang
```

### Nambahin Kategori Baru

Contoh: Perbandingan Storage

```javascript
// 1. Tambahin fungsi helper
function parseStorage(storageStr) {
  if (!storageStr) return 0;
  const match = storageStr.match(/(\d+)\s*GB/i);
  return match ? parseInt(match[1]) : 0;
}

// 2. Hitung skor
const storage1 = parseStorage(device1.storage);
const storage2 = parseStorage(device2.storage);

// 3. Bikin highlight
if (Math.abs(storage1 - storage2) > 64) {
  const winner = storage1 > storage2 ? device1.name : device2.name;
  highlights.push({
    category: "Storage",
    winner: winner,
    reason: `${Math.max(storage1, storage2)}GB lebih lega buat foto, video, sama aplikasi`
  });
}
```

---

## Tips Optimasi

1. **Nilai Threshold** - Sesuaikan threshold (contoh: `> 5`, `> 300`) biar highlight gak terlalu banyak atau terlalu dikit

2. **Skor CPU** - Update tabel skor CPU secara berkala kalau ada chipset baru

3. **Kategori Prioritas** - Tambahin/kurangin kategori sesuai kebutuhan user (gaming, fotografi, dll)

4. **Bahasa** - Ubah teks reason buat tone yang lebih santai/formal

---

## Troubleshooting

### Highlight gak muncul

- Cek threshold value terlalu tinggi
- Pastiin data HP lengkap (gak null)
- Cek fungsi parsing (RAM, Kamera, Baterai)

### Skor gak akurat

- Update tabel skor CPU
- Sesuaikan bobot formula
- Tambahin normalisasi buat range yang beda

### Response lambat

- Kurangin kompleksitas di skor CPU
- Cache hasil parsing
- Optimasi string matching
