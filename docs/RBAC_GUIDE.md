# 🔐 ROLE-BASED ACCESS CONTROL (RBAC) - IMPLEMENTATION GUIDE

## ✅ RBAC System Implemented!

Role-Based Access Control telah diimplementasikan untuk membatasi akses berdasarkan role user.

---

## 📊 ROLE HIERARCHY

### **1. Super Admin**
- ✅ Full access ke semua fitur
- ✅ Manage users & roles
- ✅ Create, Read, Update, Delete (CRUD) semua resources
- ✅ Access ke Settings & Tools

### **2. Admin**
- ✅ Full access ke devices & categories
- ✅ CRUD operations
- ✅ View analytics
- ⚠️ Limited access ke user management
- ❌ Cannot access system settings

### **3. Viewer**
- ✅ Read-only access
- ✅ View devices, categories, analytics
- ❌ Cannot create, edit, or delete
- ❌ Cannot access user management
- ❌ Cannot access settings

---

## 🛠️ IMPLEMENTATION

### **1. RBAC Middleware** (`app/core/rbac.py`)

**Functions**:
```python
# Decorators
@require_role(["Admin", "Super Admin"])  # Route protection

# Permission checks
can_create(user)  # Check create permission
can_update(user)  # Check update permission
can_delete(user)  # Check delete permission
has_permission(user, "permission_name")  # Custom permission
```

**Usage in Routes**:
```python
from app.core.rbac import require_role

@router.post("/devices/new")
@require_role(["Admin", "Super Admin"])
async def create_device(...):
    # Only Admin & Super Admin can access
    ...
```

---

### **2. Template Context** (`app/core/rbac_context.py`)

**Functions for Templates**:
```python
add_rbac_to_context(current_user)  # Add to template context
```

**Returns**:
- `can_create` - Boolean
- `can_edit` - Boolean
- `can_delete` - Boolean
- `is_admin` - Boolean
- `is_viewer` - Boolean
- `user_role` - String (role name)

**Usage in Templates**:
```html
{% if can_create %}
    <a href="/admin/devices/new" class="btn btn-success">
        <i class="fas fa-plus"></i> Add New Device
    </a>
{% endif %}

{% if can_edit %}
    <button class="btn btn-edit">Edit</button>
{% endif %}

{% if can_delete %}
    <button class="btn btn-delete">Delete</button>
{% endif %}
```

---

## 🎯 HOW TO USE

### **Step 1: Update Router to Include RBAC Context**

```python
from app.core.rbac_context import add_rbac_to_context

@router.get("/devices")
async def admin_devices(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    
    # Add RBAC context
    rbac_context = add_rbac_to_context(current_user)
    
    return templates.TemplateResponse(
        "admin/devices_list.html",
        {
            "request": request,
            "current_user": current_user,
            **rbac_context,  # Add RBAC permissions
            "devices": devices,
            # ... other context
        }
    )
```

### **Step 2: Protect Routes with Decorator**

```python
from app.core.rbac import require_role

# Only Admin & Super Admin
@router.post("/devices/new")
@require_role(["Admin", "Super Admin"])
async def create_device(...):
    ...

# Only Super Admin
@router.post("/users/delete")
@require_role(["Super Admin"])
async def delete_user(...):
    ...
```

### **Step 3: Hide UI Elements in Templates**

```html
<!-- Show "Add New" button only for Admin/Super Admin -->
{% if can_create %}
<a href="/admin/devices/new" class="btn btn-success">
    <i class="fas fa-plus"></i> Add New Device
</a>
{% endif %}

<!-- Show Edit/Delete buttons only for Admin/Super Admin -->
{% if can_edit %}
<a href="/admin/devices/{{ device.id }}/edit" class="btn btn-edit btn-sm">
    <i class="fas fa-edit"></i> Edit
</a>
{% endif %}

{% if can_delete %}
<form method="POST" action="/admin/devices/{{ device.id }}/delete" style="display: inline;">
    <button type="submit" class="btn btn-delete btn-sm">
        <i class="fas fa-trash"></i> Delete
    </button>
</form>
{% endif %}

<!-- Show role-specific message -->
{% if is_viewer %}
<div class="alert alert-info">
    <i class="fas fa-info-circle"></i>
    You have read-only access. Contact admin to request edit permissions.
</div>
{% endif %}
```

---

## 📝 IMPLEMENTATION CHECKLIST

### **✅ Core RBAC Files Created**:
- [x] `app/core/rbac.py` - Middleware & decorators
- [x] `app/core/rbac_context.py` - Template helpers

### **⏭️ TODO: Update Routers** (Manual Implementation Needed):

For each admin router, add RBAC context:

**Example for `devices.py`**:
```python
from app.core.rbac_context import add_rbac_to_context

# In each GET route:
rbac_context = add_rbac_to_context(current_user)
return templates.TemplateResponse(
    "template.html",
    {
        "request": request,
        "current_user": current_user,
        **rbac_context,  # ADD THIS
        # ... other context
    }
)
```

**Routers to Update**:
- [ ] `dashboard.py`
- [ ] `devices.py`
- [ ] `categories.py`
- [ ] `users.py`
- [ ] `analytics.py`
- [ ] `tools.py`
- [ ] `settings.py`
- [ ] `bulk_operations.py`

### **⏭️ TODO: Update Templates** (Manual Implementation Needed):

For each template, wrap action buttons with permission checks:

**Example**:
```html
<!-- Before -->
<a href="/admin/devices/new" class="btn btn-success">Add New</a>

<!-- After -->
{% if can_create %}
<a href="/admin/devices/new" class="btn btn-success">Add New</a>
{% endif %}
```

**Templates to Update**:
- [ ] `devices_list.html`
- [ ] `categories_list.html`
- [ ] `users_list.html`
- [ ] `dashboard.html`
- [ ] etc.

---

## 🧪 TESTING

### **Test 1: Login as Admin**
```
Username: admin
Password: admin123
Expected: Full access, can create/edit/delete
```

### **Test 2: Login as Viewer**
```
Username: user1
Password: user1123
Expected: Read-only, no create/edit/delete buttons
```

### **Test 3: Direct URL Access**
```
Try accessing: POST /admin/devices/new as Viewer
Expected: 403 Forbidden error
```

---

## 🚀 QUICK START

### **Option 1: Auto-Update All Routers** (Recommended)

Run this script to auto-add RBAC context to all routers:

```bash
python update_routers_rbac.py
```

### **Option 2: Manual Update** (Step by Step)

1. Update one router at a time
2. Test each router
3. Update corresponding template
4. Test UI permissions

---

## 📚 PERMISSION MATRIX

| Feature | Super Admin | Admin | Viewer |
|---------|-------------|-------|--------|
| View Devices | ✅ | ✅ | ✅ |
| Create Device | ✅ | ✅ | ❌ |
| Edit Device | ✅ | ✅ | ❌ |
| Delete Device | ✅ | ✅ | ❌ |
| View Users | ✅ | ⚠️ | ❌ |
| Manage Users | ✅ | ❌ | ❌ |
| View Analytics | ✅ | ✅ | ✅ |
| System Settings | ✅ | ❌ | ❌ |
| Bulk Operations | ✅ | ✅ | ❌ |

---

## ⚠️ IMPORTANT NOTES

1. **RBAC is implemented but NOT YET APPLIED to all routes**
2. **Manual update needed** for each router & template
3. **Test thoroughly** after implementing
4. **Viewer role** = Read-only access
5. **Admin role** = Full CRUD access (except user management)
6. **Super Admin** = Full access to everything

---

## 🛠️ NEXT STEPS

1. ✅ **RBAC Core**: Implemented
2. ⏭️ **Update Routers**: Add RBAC context to all routers
3. ⏭️ **Update Templates**: Hide buttons based on permissions
4. ⏭️ **Test**: Login as different roles and verify access
5. ⏭️ **Production**: Deploy with proper role assignments

---

**RBAC SYSTEM READY FOR IMPLEMENTATION!** 🎉

Use the helper functions and decorators to secure your admin panel.
