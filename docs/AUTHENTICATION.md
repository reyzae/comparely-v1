# 🔐 AUTHENTICATION GUIDE - COMPARELY

## ✅ Password Reset Complete!

Semua user password sudah direset dengan pattern: `[username]123`

---

## 👥 LOGIN CREDENTIALS

| Username | Password | Role | Email |
|----------|----------|------|-------|
| admin | admin123 | Super Admin | admin@comparely.com |
| tegar | tegar123 | Admin | tegar@wiracenter.com |
| rachmat | rachmat123 | Admin | rachmat@wiracenter.com |
| user1 | user1123 | Viewer | user1@wiracenter.com |
| khair | khair123 | Admin | khair@wiracenter.com |
| rofik | rofik123 | Admin | rofik@wiracenter.com |

---

## 🔑 CHANGE PASSWORD FEATURE

### **Cara Menggunakan**:

1. **Login** ke admin panel
2. **Klik avatar** di kanan atas
3. **Pilih "My Profile"** atau langsung ke: http://localhost:8000/admin/profile
4. **Scroll ke "Change Password"** section
5. **Isi form**:
   - Current Password: (password lama, contoh: `admin123`)
   - New Password: (password baru)
   - Confirm New Password: (ulangi password baru)
6. **Klik "Update Password"**
7. **Done!** Password berhasil diubah

### **Fitur Change Password**:
- ✅ Verify current password (security)
- ✅ Validate new password match
- ✅ Hash dengan bcrypt
- ✅ Update database
- ✅ Success/error message
- ✅ Available di `/admin/profile`

---

## 🚀 TESTING LOGIN

### **Test 1: Login dengan Admin**
```
URL: http://localhost:8000/admin/login
Username: admin
Password: admin123
```

### **Test 2: Login dengan User Lain**
```
URL: http://localhost:8000/admin/login
Username: tegar
Password: tegar123
```

### **Test 3: Change Password**
```
1. Login sebagai admin
2. Buka: http://localhost:8000/admin/profile
3. Change password dari admin123 ke password baru
4. Logout
5. Login lagi dengan password baru
```

---

## 🔧 AUTHENTICATION SYSTEM

### **Features**:
- ✅ Real user authentication (bcrypt hash)
- ✅ Session management (SessionMiddleware)
- ✅ Login/Logout
- ✅ Change password
- ✅ Password verification
- ✅ User-specific data
- ✅ Multi-user support
- ✅ Role-based display

### **Security**:
- ✅ Bcrypt password hashing
- ✅ Session encryption (SECRET_KEY)
- ✅ Current password verification
- ✅ Password confirmation
- ✅ Active user check
- ✅ Last login tracking

---

## 📝 ADMIN PANEL ACCESS

### **Routes**:
- `/admin/login` - Login page
- `/admin/logout` - Logout
- `/admin/profile` - User profile & change password
- `/admin/dashboard` - Dashboard (after login)

### **Profile Page Sections**:
1. **Profile Info**:
   - Avatar (first letter of username)
   - Username
   - Email
   - Role
   - Last login

2. **Change Password**:
   - Current password input
   - New password input
   - Confirm password input
   - Update button

3. **Session**:
   - Logout button

---

## 🎯 NEXT STEPS

1. ✅ **Test Login**: Login dengan semua user untuk verify
2. ✅ **Test Change Password**: Ubah password dan test login lagi
3. ✅ **Production**: Ganti SECRET_KEY di .env untuk production
4. ⏭️ **Optional**: Implement "Forgot Password" feature
5. ⏭️ **Optional**: Implement "Force Password Change" on first login

---

## ⚠️ IMPORTANT NOTES

1. **Default Passwords**: Semua user punya password default `[username]123`
2. **Security**: Instruksikan user untuk **change password** setelah first login
3. **SECRET_KEY**: Jangan commit SECRET_KEY ke Git
4. **Production**: Use HTTPS untuk secure cookies
5. **Backup**: Backup database sebelum production

---

## 🛠️ TROUBLESHOOTING

### **Login gagal?**
- Check: Username dan password benar
- Check: User is_active = True
- Check: Password hash di database benar (starts with $2)
- Check: SessionMiddleware aktif

### **Change password gagal?**
- Check: Current password benar
- Check: New password dan confirm password match
- Check: User logged in (session valid)

### **Session tidak persist?**
- Check: SECRET_KEY ada di .env
- Check: SessionMiddleware di main.py
- Check: Browser cookies enabled

---

**AUTHENTICATION SYSTEM READY!** 🎉
