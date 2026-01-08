# Panduan Authentication - COMPARELY

Semua password user udah direset dengan pattern: `[username]123`

---

## Login Credentials

| Username | Password | Role | Email |
|----------|----------|------|-------|
| admin | admin123 | Super Admin | admin@comparely.com |
| tegar | tegar123 | Admin | tegar@wiracenter.com |
| rachmat | rachmat123 | Admin | rachmat@wiracenter.com |
| user1 | user1123 | Viewer | user1@wiracenter.com |
| khair | khair123 | Admin | khair@wiracenter.com |
| rofik | rofik123 | Admin | rofik@wiracenter.com |

---

## Fitur Ganti Password

### Cara Pakai:

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

### Fitur Change Password:
- ✅ Verify password lama (keamanan)
- ✅ Validasi password baru harus match
- ✅ Hash pake bcrypt
- ✅ Update database
- ✅ Pesan success/error
- ✅ Tersedia di `/admin/profile`

---

## Testing Login

### Test 1: Login pake Admin
```
URL: http://localhost:8000/admin/login
Username: admin
Password: admin123
```

### Test 2: Login pake User Lain
```
URL: http://localhost:8000/admin/login
Username: tegar
Password: tegar123
```

### Test 3: Ganti Password
```
1. Login sebagai admin
2. Buka: http://localhost:8000/admin/profile
3. Ganti password dari admin123 ke password baru
4. Logout
5. Login lagi pake password baru
```

---

## Sistem Authentication

### Fitur:
- ✅ Autentikasi user beneran (bcrypt hash)
- ✅ Session management (SessionMiddleware)
- ✅ Login/Logout
- ✅ Ganti password
- ✅ Verifikasi password
- ✅ Data per-user
- ✅ Support multi-user
- ✅ Tampilan berdasarkan role

### Keamanan:
- ✅ Password hashing pake Bcrypt
- ✅ Enkripsi session (SECRET_KEY)
- ✅ Verifikasi password lama
- ✅ Konfirmasi password
- ✅ Cek user aktif
- ✅ Tracking last login

---

## Akses Admin Panel

### Routes:
- `/admin/login` - Halaman login
- `/admin/logout` - Logout
- `/admin/profile` - Profile user & ganti password
- `/admin/dashboard` - Dashboard (setelah login)

### Bagian Halaman Profile:
1. **Info Profile**:
   - Avatar (huruf pertama username)
   - Username
   - Email
   - Role
   - Last login

2. **Ganti Password**:
   - Input password lama
   - Input password baru
   - Input konfirmasi password
   - Tombol update

3. **Session**:
   - Tombol logout

---

## Langkah Selanjutnya

1. ✅ **Test Login**: Login pake semua user buat verify
2. ✅ **Test Ganti Password**: Ubah password dan test login lagi
3. ✅ **Production**: Ganti SECRET_KEY di .env buat production
4. ⏭️ **Opsional**: Implement fitur "Forgot Password"
5. ⏭️ **Opsional**: Implement "Force Password Change" di first login

---

## Catatan Penting

1. **Password Default**: Semua user punya password default `[username]123`
2. **Keamanan**: Instruksikan user buat **ganti password** setelah first login
3. **SECRET_KEY**: Jangan commit SECRET_KEY ke Git
4. **Production**: Pake HTTPS buat secure cookies
5. **Backup**: Backup database sebelum production

---

## Troubleshooting

### Login gagal?
- Cek: Username dan password bener
- Cek: User is_active = True
- Cek: Password hash di database bener (mulai dengan $2)
- Cek: SessionMiddleware aktif

### Ganti password gagal?
- Cek: Password lama bener
- Cek: Password baru dan konfirmasi password match
- Cek: User udah login (session valid)

### Session gak persist?
- Cek: SECRET_KEY ada di .env
- Cek: SessionMiddleware di main.py
- Cek: Browser cookies enabled

---

**SISTEM AUTHENTICATION SIAP!** 🎉
