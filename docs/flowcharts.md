# COMPARELY - Flowcharts & Diagrams

Dokumentasi visual untuk sistem COMPARELY menggunakan Mermaid diagrams.

---

## 📊 1. Arsitektur Sistem

```mermaid
graph TB
    subgraph "Frontend (Future)"
        UI[User Interface]
    end
    
    subgraph "Backend - FastAPI"
        API[API Gateway<br/>FastAPI Router]
        
        subgraph "Services Layer"
            CS[Comparison Service]
            RS[Recommendation Service]
            GS[Grok AI Service]
        end
        
        subgraph "CRUD Layer"
            DC[Device CRUD]
            CC[Category CRUD]
        end
        
        subgraph "Models"
            DM[Device Model]
            CM[Category Model]
        end
    end
    
    subgraph "External Services"
        DB[(MySQL Database)]
        GROK[Grok AI API<br/>xAI]
    end
    
    UI -->|HTTP Request| API
    API --> CS
    API --> RS
    API --> DC
    API --> CC
    
    CS --> DC
    CS --> GS
    RS --> DC
    RS --> GS
    
    DC --> DM
    CC --> CM
    
    DM --> DB
    CM --> DB
    
    GS -->|API Call| GROK
    
    style UI fill:#4FC3F7,stroke:#0277BD,stroke-width:3px,color:#000
    style API fill:#FFD54F,stroke:#F57C00,stroke-width:3px,color:#000
    style CS fill:#81C784,stroke:#2E7D32,stroke-width:2px,color:#000
    style RS fill:#81C784,stroke:#2E7D32,stroke-width:2px,color:#000
    style GS fill:#BA68C8,stroke:#6A1B9A,stroke-width:3px,color:#fff
    style DC fill:#FFB74D,stroke:#E65100,stroke-width:2px,color:#000
    style CC fill:#FFB74D,stroke:#E65100,stroke-width:2px,color:#000
    style DM fill:#A5D6A7,stroke:#388E3C,stroke-width:2px,color:#000
    style CM fill:#A5D6A7,stroke:#388E3C,stroke-width:2px,color:#000
    style DB fill:#66BB6A,stroke:#1B5E20,stroke-width:3px,color:#fff
    style GROK fill:#AB47BC,stroke:#4A148C,stroke-width:3px,color:#fff
```

---

## 🔍 2. Flow Pencarian Perangkat

```mermaid
flowchart TD
    Start([User Akses /devices/search]) --> Input[Input: query parameter]
    Input --> Validate{Query valid?}
    
    Validate -->|Tidak| Error400[Return 400<br/>Bad Request]
    Validate -->|Ya| SearchDB[Search di Database<br/>LIKE %query%]
    
    SearchDB --> CheckResult{Ada hasil?}
    
    CheckResult -->|Tidak| Empty[Return empty list<br/>200 OK]
    CheckResult -->|Ya| Format[Format response<br/>dengan Pydantic]
    
    Format --> Return[Return list devices<br/>200 OK]
    
    Error400 --> End([End])
    Empty --> End
    Return --> End
    
    style Start fill:#42A5F5,stroke:#1565C0,stroke-width:3px,color:#fff
    style End fill:#42A5F5,stroke:#1565C0,stroke-width:3px,color:#fff
    style Validate fill:#FFA726,stroke:#E65100,stroke-width:3px,color:#000
    style CheckResult fill:#FFA726,stroke:#E65100,stroke-width:3px,color:#000
    style SearchDB fill:#FFD54F,stroke:#F57C00,stroke-width:2px,color:#000
    style Format fill:#BA68C8,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style Error400 fill:#EF5350,stroke:#C62828,stroke-width:2px,color:#fff
    style Empty fill:#66BB6A,stroke:#2E7D32,stroke-width:2px,color:#fff
    style Return fill:#66BB6A,stroke:#2E7D32,stroke-width:2px,color:#fff
```

---

## ⚖️ 3. Flow Perbandingan Perangkat

```mermaid
flowchart TD
    Start([User Akses /compare/]) --> Input[Input: id1, id2]
    Input --> Validate{ID valid?}
    
    Validate -->|Tidak| Error422[Return 422<br/>Validation Error]
    Validate -->|Ya| GetDevices[Get Device 1 & 2<br/>dari Database]
    
    GetDevices --> CheckExist{Kedua device<br/>ditemukan?}
    
    CheckExist -->|Tidak| Error404[Return 404<br/>Device Not Found]
    CheckExist -->|Ya| Compare[Generate Highlights:<br/>- Perbedaan harga<br/>- Device lebih baru]
    
    Compare --> Format[Format Response:<br/>- device_1<br/>- device_2<br/>- highlights]
    
    Format --> Return[Return comparison<br/>200 OK]
    
    Error422 --> End([End])
    Error404 --> End
    Return --> End
    
    style Start fill:#42A5F5,stroke:#1565C0,stroke-width:3px,color:#fff
    style End fill:#42A5F5,stroke:#1565C0,stroke-width:3px,color:#fff
    style Validate fill:#FFA726,stroke:#E65100,stroke-width:3px,color:#000
    style CheckExist fill:#FFA726,stroke:#E65100,stroke-width:3px,color:#000
    style GetDevices fill:#FFD54F,stroke:#F57C00,stroke-width:2px,color:#000
    style Compare fill:#FFD54F,stroke:#F57C00,stroke-width:2px,color:#000
    style Format fill:#BA68C8,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style Error422 fill:#EF5350,stroke:#C62828,stroke-width:2px,color:#fff
    style Error404 fill:#EF5350,stroke:#C62828,stroke-width:2px,color:#fff
    style Return fill:#66BB6A,stroke:#2E7D32,stroke-width:2px,color:#fff
```

---

## 🤖 4. Flow Perbandingan dengan AI

```mermaid
flowchart TD
    Start([User Akses /compare/ai]) --> Input[Input: id1, id2]
    Input --> BaseCompare[Jalankan Comparison<br/>Rule-Based]
    
    BaseCompare --> GetResult{Comparison<br/>berhasil?}
    
    GetResult -->|Tidak| Error[Return Error]
    GetResult -->|Ya| PreparePrompt[Prepare AI Prompt:<br/>- Device specs<br/>- JSON format strict]
    
    PreparePrompt --> CallGrok[Call Grok AI API<br/>POST /chat/completions]
    
    CallGrok --> CheckAI{AI Response<br/>berhasil?}
    
    CheckAI -->|Tidak| Fallback[AI Analysis =<br/>'Maaf, AI tidak tersedia']
    CheckAI -->|Ya| ParseJSON[Parse JSON Response:<br/>- performa<br/>- kamera<br/>- baterai<br/>- value_for_money<br/>- rekomendasi]
    
    ParseJSON --> FormatAI[Format AI Analysis<br/>ke readable text]
    
    Fallback --> Combine[Combine:<br/>Base Comparison +<br/>AI Analysis]
    FormatAI --> Combine
    
    Combine --> Return[Return Full Response<br/>200 OK]
    
    Error --> End([End])
    Return --> End
    
    style Start fill:#42A5F5,stroke:#1565C0,stroke-width:3px,color:#fff
    style End fill:#42A5F5,stroke:#1565C0,stroke-width:3px,color:#fff
    style GetResult fill:#FFA726,stroke:#E65100,stroke-width:3px,color:#000
    style CheckAI fill:#FFA726,stroke:#E65100,stroke-width:3px,color:#000
    style BaseCompare fill:#FFD54F,stroke:#F57C00,stroke-width:2px,color:#000
    style PreparePrompt fill:#FFD54F,stroke:#F57C00,stroke-width:2px,color:#000
    style CallGrok fill:#AB47BC,stroke:#4A148C,stroke-width:3px,color:#fff
    style ParseJSON fill:#BA68C8,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style FormatAI fill:#BA68C8,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style Combine fill:#81C784,stroke:#2E7D32,stroke-width:2px,color:#000
    style Fallback fill:#FFB74D,stroke:#E65100,stroke-width:2px,color:#000
    style Error fill:#EF5350,stroke:#C62828,stroke-width:2px,color:#fff
    style Return fill:#66BB6A,stroke:#2E7D32,stroke-width:2px,color:#fff
```

---

## 🎯 5. Flow Rekomendasi Perangkat

```mermaid
flowchart TD
    Start([User Akses /recommendation/]) --> Input[Input Parameters:<br/>- max_price<br/>- category_id<br/>- min_release_year<br/>- limit]
    
    Input --> BuildQuery[Build SQL Query<br/>dengan Filters]
    
    BuildQuery --> ApplyFilters{Apply Filters}
    
    ApplyFilters --> FilterPrice[Filter: price <= max_price]
    FilterPrice --> FilterCategory[Filter: category_id]
    FilterCategory --> FilterYear[Filter: release_year >= min]
    
    FilterYear --> Sort[Sort By:<br/>1. release_year DESC<br/>2. price ASC]
    
    Sort --> Limit[Apply Limit<br/>default: 5]
    
    Limit --> CheckResult{Ada hasil?}
    
    CheckResult -->|Tidak| Empty[Return empty list<br/>200 OK]
    CheckResult -->|Ya| Format[Format dengan<br/>Pydantic Schema]
    
    Format --> Return[Return list devices<br/>200 OK]
    
    Empty --> End([End])
    Return --> End
    
    style Start fill:#42A5F5,stroke:#1565C0,stroke-width:3px,color:#fff
    style End fill:#42A5F5,stroke:#1565C0,stroke-width:3px,color:#fff
    style ApplyFilters fill:#FFA726,stroke:#E65100,stroke-width:3px,color:#000
    style CheckResult fill:#FFA726,stroke:#E65100,stroke-width:3px,color:#000
    style BuildQuery fill:#FFD54F,stroke:#F57C00,stroke-width:2px,color:#000
    style FilterPrice fill:#81C784,stroke:#2E7D32,stroke-width:2px,color:#000
    style FilterCategory fill:#81C784,stroke:#2E7D32,stroke-width:2px,color:#000
    style FilterYear fill:#81C784,stroke:#2E7D32,stroke-width:2px,color:#000
    style Sort fill:#BA68C8,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style Limit fill:#FFB74D,stroke:#E65100,stroke-width:2px,color:#000
    style Format fill:#BA68C8,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style Empty fill:#66BB6A,stroke:#2E7D32,stroke-width:2px,color:#fff
    style Return fill:#66BB6A,stroke:#2E7D32,stroke-width:2px,color:#fff
```

---

## 🧠 6. Flow Rekomendasi dengan AI

```mermaid
flowchart TD
    Start([User Akses /recommendation/ai]) --> Input[Input Parameters:<br/>+ use_case]
    
    Input --> BaseRec[Jalankan Recommendation<br/>Rule-Based<br/>Top 3 devices]
    
    BaseRec --> CheckDevices{Ada devices?}
    
    CheckDevices -->|Tidak| Empty[Return empty +<br/>AI: 'Tidak ada device']
    CheckDevices -->|Ya| PreparePrompt[Prepare AI Prompt:<br/>- Device list<br/>- Use case<br/>- Budget<br/>- JSON format]
    
    PreparePrompt --> CallGrok[Call Grok AI API<br/>Model: grok-4-latest]
    
    CallGrok --> CheckAI{AI Response<br/>OK?}
    
    CheckAI -->|Tidak| Fallback[AI Recommendation =<br/>'Maaf, AI tidak tersedia']
    CheckAI -->|Ya| ParseJSON[Parse JSON:<br/>- top_1<br/>- top_2<br/>- top_3<br/>- summary]
    
    ParseJSON --> FormatAI[Format AI<br/>Recommendation]
    
    Fallback --> Combine[Combine:<br/>Devices List +<br/>AI Recommendation]
    FormatAI --> Combine
    
    Combine --> Return[Return Full Response<br/>200 OK]
    
    Empty --> End([End])
    Return --> End
    
    style Start fill:#42A5F5,stroke:#1565C0,stroke-width:3px,color:#fff
    style End fill:#42A5F5,stroke:#1565C0,stroke-width:3px,color:#fff
    style CheckDevices fill:#FFA726,stroke:#E65100,stroke-width:3px,color:#000
    style CheckAI fill:#FFA726,stroke:#E65100,stroke-width:3px,color:#000
    style BaseRec fill:#FFD54F,stroke:#F57C00,stroke-width:2px,color:#000
    style PreparePrompt fill:#FFD54F,stroke:#F57C00,stroke-width:2px,color:#000
    style CallGrok fill:#AB47BC,stroke:#4A148C,stroke-width:3px,color:#fff
    style ParseJSON fill:#BA68C8,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style FormatAI fill:#BA68C8,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style Combine fill:#81C784,stroke:#2E7D32,stroke-width:2px,color:#000
    style Fallback fill:#FFB74D,stroke:#E65100,stroke-width:2px,color:#000
    style Empty fill:#EF5350,stroke:#C62828,stroke-width:2px,color:#fff
    style Return fill:#66BB6A,stroke:#2E7D32,stroke-width:2px,color:#fff
```

---

## 📥 7. Flow Import Data CSV

```mermaid
flowchart TD
    Start([Run import_csv.py]) --> Input[Input: CSV file path]
    
    Input --> CheckFile{File exists?}
    
    CheckFile -->|Tidak| ErrorFile[Error: File not found]
    CheckFile -->|Ya| ReadCSV[Read CSV dengan pandas]
    
    ReadCSV --> Validate[Validate setiap row:<br/>- Required fields<br/>- Data types<br/>- Price > 0]
    
    Validate --> CheckValid{Semua valid?}
    
    CheckValid -->|Tidak| ShowErrors[Print validation errors<br/>Skip invalid rows]
    CheckValid -->|Ya| ProcessRows[Process each row]
    
    ShowErrors --> ProcessRows
    
    ProcessRows --> CheckCategory{Category exists?}
    
    CheckCategory -->|Tidak| CreateCategory[Create new category]
    CheckCategory -->|Ya| InsertDevice[Insert device to DB]
    
    CreateCategory --> InsertDevice
    
    InsertDevice --> CheckDuplicate{Duplicate?}
    
    CheckDuplicate -->|Ya| Skip[Skip row<br/>Log warning]
    CheckDuplicate -->|Tidak| Commit[Commit to DB]
    
    Skip --> NextRow{More rows?}
    Commit --> NextRow
    
    NextRow -->|Ya| ProcessRows
    NextRow -->|Tidak| Summary[Print Summary:<br/>- Total processed<br/>- Success count<br/>- Error count]
    
    Summary --> End([End])
    ErrorFile --> End
    
    style Start fill:#42A5F5,stroke:#1565C0,stroke-width:3px,color:#fff
    style End fill:#42A5F5,stroke:#1565C0,stroke-width:3px,color:#fff
    style CheckFile fill:#FFA726,stroke:#E65100,stroke-width:3px,color:#000
    style CheckValid fill:#FFA726,stroke:#E65100,stroke-width:3px,color:#000
    style CheckCategory fill:#FFA726,stroke:#E65100,stroke-width:3px,color:#000
    style CheckDuplicate fill:#FFA726,stroke:#E65100,stroke-width:3px,color:#000
    style NextRow fill:#FFA726,stroke:#E65100,stroke-width:3px,color:#000
    style ReadCSV fill:#FFD54F,stroke:#F57C00,stroke-width:2px,color:#000
    style Validate fill:#FFD54F,stroke:#F57C00,stroke-width:2px,color:#000
    style ProcessRows fill:#81C784,stroke:#2E7D32,stroke-width:2px,color:#000
    style CreateCategory fill:#81C784,stroke:#2E7D32,stroke-width:2px,color:#000
    style InsertDevice fill:#81C784,stroke:#2E7D32,stroke-width:2px,color:#000
    style Commit fill:#66BB6A,stroke:#1B5E20,stroke-width:3px,color:#fff
    style Summary fill:#BA68C8,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style ErrorFile fill:#EF5350,stroke:#C62828,stroke-width:2px,color:#fff
    style ShowErrors fill:#FFB74D,stroke:#E65100,stroke-width:2px,color:#000
    style Skip fill:#FFB74D,stroke:#E65100,stroke-width:2px,color:#000
```

---

## 🔄 8. Activity Diagram - User Journey

```mermaid
stateDiagram-v2
    [*] --> HomePage: User Akses Website
    
    HomePage --> Search: Input keyword
    HomePage --> Browse: Lihat kategori
    
    Search --> SearchResults: Submit search
    Browse --> CategoryView: Pilih kategori
    
    SearchResults --> DeviceDetail: Klik device
    CategoryView --> DeviceDetail: Klik device
    
    DeviceDetail --> SelectCompare: Pilih "Compare"
    DeviceDetail --> ViewSpec: Lihat spesifikasi
    
    SelectCompare --> ChooseDevice2: Pilih device kedua
    
    ChooseDevice2 --> ComparisonView: Submit
    
    ComparisonView --> ViewRuleBased: Lihat comparison biasa
    ComparisonView --> ViewAI: Lihat AI analysis
    
    ViewRuleBased --> Decision: Buat keputusan
    ViewAI --> Decision: Buat keputusan
    
    Decision --> [*]: Selesai
    
    note right of ViewAI
        AI memberikan analisis:
        - Performa
        - Kamera
        - Baterai
        - Value for Money
        - Rekomendasi personal
    end note
```

---

## 📝 Catatan Diagram

### Konvensi Warna:
- 🔵 **Biru** (`#42A5F5`): Start/End points
- � **Orange** (`#FFA726`): Decision points (diamond shapes)
- �🟡 **Kuning** (`#FFD54F`): Processing/Logic
- 🟣 **Ungu** (`#BA68C8`, `#AB47BC`): AI/External services & formatting
- 🟢 **Hijau** (`#81C784`, `#66BB6A`): Success states & database operations
- 🔴 **Merah** (`#EF5350`): Error states
- 🟤 **Orange Muda** (`#FFB74D`): Warning/Skip states

### Cara Menggunakan:
1. Copy kode Mermaid ke Markdown viewer yang support Mermaid
2. Atau gunakan online editor: https://mermaid.live/
3. Untuk proposal, screenshot diagram dan masukkan ke dokumen
4. Diagram akan otomatis render dengan warna yang cerah dan jelas

---

**Dibuat**: 3 Desember 2025
**Untuk**: Proposal & Dokumentasi Proyek COMPARELY
