# Panduan RBAC (Role-Based Access Control)

Sistem RBAC udah diimplementasikan buat ngatur akses berdasarkan role user.

---

## Hirarki Role

### 1. Super Admin
- Akses penuh ke semua fitur
- Bisa manage users & roles
- Create, Read, Update, Delete (CRUD) semua resource
- Akses ke Settings & Tools

### 2. Admin
- Akses penuh ke devices & categories
- Bisa CRUD operations
- Liat analytics
- Akses terbatas ke user management
- Gak bisa akses system settings

### 3. Viewer
- Akses read-only
- Bisa liat devices, categories, analytics
- Gak bisa create, edit, atau delete
- Gak bisa akses user management
- Gak bisa akses settings

---

## Implementasi

### 1. RBAC Middleware (`app/core/rbac.py`)

**Fungsi-fungsi:**
```python
# Decorators
@require_role(["Admin", "Super Admin"])  # Proteksi route

# Cek permission
can_create(user)  # Cek permission create
can_update(user)  # Cek permission update
can_delete(user)  # Cek permission delete
has_permission(user, "permission_name")  # Custom permission
```

**Cara Pake di Routes:**
```python
from app.core.rbac import require_role

@router.post("/devices/new")
@require_role(["Admin", "Super Admin"])
async def create_device(...):
    # Cuma Admin & Super Admin yang bisa akses
    ...
```

---

### 2. Template Context (`app/core/rbac_context.py`)

**Fungsi buat Templates:**
```python
add_rbac_to_context(current_user)  # Tambahin ke template context
```

**Return:**
- `can_create` - Boolean
- `can_edit` - Boolean
- `can_delete` - Boolean
- `is_admin` - Boolean
- `is_viewer` - Boolean
- `user_role` - String (nama role)

**Cara Pake di Templates:**
```html
{% if can_create %}
    <a href="/admin/devices/new" class="btn btn-success">
        <i class="fas fa-plus"></i> Tambah Device Baru
    </a>
{% endif %}

{% if can_edit %}
    <button class="btn btn-edit">Edit</button>
{% endif %}

{% if can_delete %}
    <button class="btn btn-delete">Hapus</button>
{% endif %}
```

---

## Cara Pakai

### Langkah 1: Update Router buat Include RBAC Context

```python
from app.core.rbac_context import add_rbac_to_context

@router.get("/devices")
async def admin_devices(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    
    # Tambahin RBAC context
    rbac_context = add_rbac_to_context(current_user)
    
    return templates.TemplateResponse(
        "admin/devices_list.html",
        {
            "request": request,
            "current_user": current_user,
            **rbac_context,  # Tambahin RBAC permissions
            "devices": devices,
            # ... context lainnya
        }
    )
```

### Langkah 2: Proteksi Routes pake Decorator

```python
from app.core.rbac import require_role

# Cuma Admin & Super Admin
@router.post("/devices/new")
@require_role(["Admin", "Super Admin"])
async def create_device(...):
    ...

# Cuma Super Admin
@router.post("/users/delete")
@require_role(["Super Admin"])
async def delete_user(...):
    ...
```

### Langkah 3: Sembunyiin Elemen UI di Templates

```html
<!-- Tampilkan tombol "Tambah Baru" cuma buat Admin/Super Admin -->
{% if can_create %}
<a href="/admin/devices/new" class="btn btn-success">
    <i class="fas fa-plus"></i> Tambah Device Baru
</a>
{% endif %}

<!-- Tampilkan tombol Edit/Hapus cuma buat Admin/Super Admin -->
{% if can_edit %}
<a href="/admin/devices/{{ device.id }}/edit" class="btn btn-edit btn-sm">
    <i class="fas fa-edit"></i> Edit
</a>
{% endif %}

{% if can_delete %}
<form method="POST" action="/admin/devices/{{ device.id }}/delete" style="display: inline;">
    <button type="submit" class="btn btn-delete btn-sm">
        <i class="fas fa-trash"></i> Hapus
    </button>
</form>
{% endif %}

<!-- Tampilkan pesan khusus role -->
{% if is_viewer %}
<div class="alert alert-info">
    <i class="fas fa-info-circle"></i>
    Kamu punya akses read-only. Hubungi admin kalau mau request edit permissions.
</div>
{% endif %}
```

---

## Checklist Implementasi

### File RBAC Core Udah Dibuat:
- [x] `app/core/rbac.py` - Middleware & decorators
- [x] `app/core/rbac_context.py` - Template helpers

### TODO: Update Routers (Perlu Manual):

Buat setiap admin router, tambahin RBAC context:

**Contoh buat `devices.py`**:
```python
from app.core.rbac_context import add_rbac_to_context

# Di setiap GET route:
rbac_context = add_rbac_to_context(current_user)
return templates.TemplateResponse(
    "template.html",
    {
        "request": request,
        "current_user": current_user,
        **rbac_context,  # TAMBAHIN INI
        # ... context lainnya
    }
)
```

**Routers yang Perlu Di-update**:
- [ ] `dashboard.py`
- [ ] `devices.py`
- [ ] `categories.py`
- [ ] `users.py`
- [ ] `analytics.py`
- [ ] `tools.py`
- [ ] `settings.py`
- [ ] `bulk_operations.py`

### TODO: Update Templates (Perlu Manual):

Buat setiap template, wrap tombol action pake cek permission:

**Contoh**:
```html
<!-- Sebelum -->
<a href="/admin/devices/new" class="btn btn-success">Tambah Baru</a>

<!-- Sesudah -->
{% if can_create %}
<a href="/admin/devices/new" class="btn btn-success">Tambah Baru</a>
{% endif %}
```

**Templates yang Perlu Di-update**:
- [ ] `devices_list.html`
- [ ] `categories_list.html`
- [ ] `users_list.html`
- [ ] `dashboard.html`
- [ ] dll.

---

## Testing

### Test 1: Login sebagai Admin
```
Username: admin
Password: admin123
Expected: Akses penuh, bisa create/edit/delete
```

### Test 2: Login sebagai Viewer
```
Username: user1
Password: user1123
Expected: Read-only, gak ada tombol create/edit/delete
```

### Test 3: Akses URL Langsung
```
Coba akses: POST /admin/devices/new sebagai Viewer
Expected: Error 403 Forbidden
```

---

## Quick Start

### Opsi 1: Auto-Update Semua Routers (Recommended)

Jalanin script ini buat auto-add RBAC context ke semua routers:

```bash
python update_routers_rbac.py
```

### Opsi 2: Update Manual (Step by Step)

1. Update satu router dulu
2. Test setiap router
3. Update template yang sesuai
4. Test UI permissions

---

## Tabel Permission

| Fitur | Super Admin | Admin | Viewer |
|-------|-------------|-------|--------|
| Liat Devices | Ya | Ya | Ya |
| Buat Device | Ya | Ya | Tidak |
| Edit Device | Ya | Ya | Tidak |
| Hapus Device | Ya | Ya | Tidak |
| Liat Users | Ya | Terbatas | Tidak |
| Manage Users | Ya | Tidak | Tidak |
| Liat Analytics | Ya | Ya | Ya |
| System Settings | Ya | Tidak | Tidak |
| Bulk Operations | Ya | Ya | Tidak |

---

## Catatan Penting

1. **RBAC udah diimplementasikan tapi BELUM DITERAPKAN ke semua routes**
2. **Perlu update manual** buat setiap router & template
3. **Test dengan teliti** setelah implementasi
4. **Role Viewer** = Akses read-only
5. **Role Admin** = Akses CRUD penuh (kecuali user management)
6. **Super Admin** = Akses penuh ke semuanya

---

## Langkah Selanjutnya

1. **RBAC Core**: Udah diimplementasikan
2. **Update Routers**: Tambahin RBAC context ke semua routers
3. **Update Templates**: Sembunyiin tombol berdasarkan permissions
4. **Test**: Login sebagai role yang berbeda dan verify akses
5. **Production**: Deploy dengan role assignment yang proper

---

**SISTEM RBAC SIAP DIIMPLEMENTASIKAN!**

Pake fungsi helper dan decorators buat ngamanin admin panel kamu.
