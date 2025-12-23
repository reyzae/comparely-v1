# 📦 DEPLOYMENT PACKAGE - COMPARELY VPS

## 🎯 Informasi VPS

```
IP Address : 160.187.210.125
Username   : root
Password   : [PASSWORD_VPS]
```

---

## 📁 File-File Deployment yang Sudah Dibuat

Saya sudah membuatkan beberapa file untuk memudahkan deployment:

### 1. **QUICK_DEPLOY.md** ⭐ (RECOMMENDED)
   - Panduan lengkap deployment dengan 3 metode berbeda
   - Langkah-langkah detail dari awal sampai akhir
   - Termasuk konfigurasi Nginx dan Systemd

### 2. **COPY_PASTE_COMMANDS.txt** ⭐ (PALING MUDAH)
   - Command siap copy-paste ke SSH terminal
   - Tidak perlu download file, langsung copy-paste
   - Otomatis backup project lama

### 3. **quick_deploy.sh**
   - Bash script otomatis untuk deployment
   - Bisa dijalankan langsung di VPS
   - Include backup otomatis

### 4. **vps_commands.sh**
   - Script setup environment di VPS
   - Install dependencies dan setup Python

### 5. **deploy_to_vps.ps1**
   - PowerShell script untuk Windows
   - Generate helper scripts

### 6. **auto_deploy_ssh.ps1**
   - Script deployment otomatis via SSH
   - Dengan instruksi lengkap

### 7. **connect_vps.ps1**
   - Quick connect ke VPS via SSH

### 8. **DEPLOYMENT_VPS.md**
   - Dokumentasi lengkap deployment (sudah ada sebelumnya)
   - Panduan detail setup production

---

## 🚀 CARA DEPLOY (Pilih Salah Satu)

### ✅ METODE 1: Copy-Paste Commands (PALING CEPAT)

**Langkah:**

1. **Buka file:** `COPY_PASTE_COMMANDS.txt`

2. **Connect ke VPS:**
   ```bash
   ssh root@160.187.210.125
   # Password: [PASSWORD_VPS]
   ```

3. **Copy semua command** dari file `COPY_PASTE_COMMANDS.txt` (mulai dari `BACKUP_DATE=...` sampai `echo "Deployment completed..."`)

4. **Paste ke terminal SSH** dan tekan Enter

5. **Tunggu sampai selesai** (sekitar 5-10 menit)

6. **Ikuti "NEXT STEPS"** yang muncul di terminal

---

### ✅ METODE 2: Menggunakan Script (OTOMATIS)

**Langkah:**

1. **Connect ke VPS:**
   ```bash
   ssh root@160.187.210.125
   ```

2. **Download dan jalankan script:**
   ```bash
   curl -o quick_deploy.sh https://raw.githubusercontent.com/reyzae/comparely/main/quick_deploy.sh
   bash quick_deploy.sh
   ```

3. **Tunggu sampai selesai**

---

### ✅ METODE 3: Menggunakan WinSCP (VISUAL)

**Langkah:**

1. **Download WinSCP:** https://winscp.net/eng/download.php

2. **Connect ke VPS:**
   - Protocol: SFTP
   - Host: `160.187.210.125`
   - Port: `22`
   - Username: `root`
   - Password: `[PASSWORD_VPS]`

3. **Backup folder lama** (jika ada):
   - Rename `/root/comparely` → `/root/comparely_old_backup`

4. **Upload project:**
   - Drag & drop folder `comparely` ke `/root/`

5. **Open Terminal** (Ctrl+T) dan jalankan:
   ```bash
   cd /root/comparely
   bash vps_commands.sh
   ```

---

## 🔧 Setelah Deployment

### 1. Edit .env File

```bash
cd /root/comparely
nano .env
```

**Update setting ini:**
```env
SECRET_KEY=your-secret-key-here  # Generate dengan command di bawah
DATABASE_URL=mysql://user:pass@localhost/comparely_db  # Jika pakai MySQL
AI_API_KEY=your-xai-api-key  # Jika pakai AI
DEBUG=False
```

**Generate SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. Initialize Database

```bash
cd /root/comparely
source .venv/bin/activate
python scripts/utils/init_db.py
```

### 3. Create Admin User

```bash
python scripts/utils/create_admin_simple.py
```

### 4. Test Aplikasi

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Buka browser: `http://160.187.210.125:8000`

Jika berhasil, tekan `Ctrl+C` untuk stop.

### 5. Setup Production (Systemd + Nginx)

Ikuti panduan di file **QUICK_DEPLOY.md** atau **DEPLOYMENT_VPS.md** bagian:
- Setup Systemd Service
- Setup Nginx
- Setup Firewall

---

## 📦 Backup Information

### Lokasi Backup

Semua backup otomatis disimpan di: `/root/backups/`

Format nama: `comparely_backup_YYYYMMDD_HHMMSS.tar.gz`

### Cara Melihat Backup

```bash
ls -lh /root/backups/
```

### Cara Restore Backup

```bash
cd /root
tar -xzf backups/comparely_backup_YYYYMMDD_HHMMSS.tar.gz
systemctl restart comparely
```

### Lokasi Project Lama

Project lama dipindahkan ke: `/root/comparely_old_YYYYMMDD_HHMMSS/`

---

## 🐛 Troubleshooting

### Jika deployment gagal:

1. **Check koneksi internet VPS:**
   ```bash
   ping -c 4 google.com
   ```

2. **Check apakah Git terinstall:**
   ```bash
   git --version
   ```

3. **Check apakah Python terinstall:**
   ```bash
   python3 --version
   ```

4. **Manual clone jika gagal:**
   ```bash
   cd /root
   git clone https://github.com/reyzae/comparely.git
   ```

### Jika aplikasi tidak jalan:

1. **Check logs:**
   ```bash
   tail -f /var/log/comparely/error.log
   journalctl -u comparely -f
   ```

2. **Check service status:**
   ```bash
   systemctl status comparely
   systemctl status nginx
   ```

3. **Restart services:**
   ```bash
   systemctl restart comparely
   systemctl restart nginx
   ```

---

## 📞 Quick Commands Reference

### Connect to VPS
```bash
ssh root@160.187.210.125
```

### Check Status
```bash
systemctl status comparely
systemctl status nginx
```

### View Logs
```bash
tail -f /var/log/comparely/error.log
journalctl -u comparely -f
```

### Restart Services
```bash
systemctl restart comparely
systemctl restart nginx
```

### Update Application
```bash
cd /root/comparely
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
systemctl restart comparely
```

### Check Resources
```bash
df -h          # Disk space
free -h        # Memory
htop           # Processes
```

---

## 📚 Dokumentasi Lengkap

Untuk panduan lebih detail, lihat:

1. **QUICK_DEPLOY.md** - Panduan cepat deployment
2. **DEPLOYMENT_VPS.md** - Panduan lengkap production setup
3. **COPY_PASTE_COMMANDS.txt** - Command siap pakai
4. **TROUBLESHOOTING.md** - Panduan troubleshooting

---

## ✅ Checklist Deployment

- [ ] Connect ke VPS berhasil
- [ ] Backup project lama (jika ada)
- [ ] Clone/upload project baru
- [ ] Install dependencies
- [ ] Setup virtual environment
- [ ] Install Python packages
- [ ] Edit .env file
- [ ] Generate SECRET_KEY
- [ ] Initialize database
- [ ] Create admin user
- [ ] Test aplikasi (port 8000)
- [ ] Setup systemd service
- [ ] Setup Nginx
- [ ] Setup firewall
- [ ] Test aplikasi via domain/IP
- [ ] Verify admin panel

---

## 🎉 Setelah Deployment Berhasil

Aplikasi COMPARELY akan bisa diakses di:

- **Homepage:** `http://160.187.210.125`
- **Admin Panel:** `http://160.187.210.125/admin/login`

**Selamat! Deployment berhasil! 🚀**

---

## 💡 Tips

1. **Selalu backup** sebelum update
2. **Monitor logs** secara berkala
3. **Update aplikasi** secara rutin
4. **Setup SSL** untuk keamanan (opsional)
5. **Setup monitoring** untuk production (opsional)

---

**Dibuat oleh:** Antigravity AI Assistant
**Tanggal:** 2025-12-22
**Untuk:** Reyza - COMPARELY Project
