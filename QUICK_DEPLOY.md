# 🚀 Panduan Cepat Deploy ke VPS

**VPS Information:**
- IP Address: `160.187.210.125`
- Username: `root`
- Password: `[PASSWORD_VPS]`

---

## 📋 Pilih Metode Deployment

### ✅ METODE 1: Quick Deploy (PALING MUDAH)

**Langkah-langkah:**

1. **Connect ke VPS via SSH:**
   ```bash
   ssh root@160.187.210.125
   # Password: [PASSWORD_VPS]
   ```

2. **Download dan jalankan script deployment:**
   ```bash
   curl -o quick_deploy.sh https://raw.githubusercontent.com/reyzae/comparely/main/quick_deploy.sh
   bash quick_deploy.sh
   ```

   **ATAU copy-paste langsung script ini:**
   ```bash
   wget https://raw.githubusercontent.com/reyzae/comparely/main/quick_deploy.sh
   bash quick_deploy.sh
   ```

3. **Selesai!** Script akan otomatis:
   - ✅ Backup project lama (jika ada)
   - ✅ Install dependencies
   - ✅ Clone project dari GitHub
   - ✅ Setup virtual environment
   - ✅ Install Python packages

---

### ✅ METODE 2: Manual Step-by-Step

**1. Connect ke VPS:**
```bash
ssh root@160.187.210.125
# Password: [PASSWORD_VPS]
```

**2. Backup project lama (jika ada):**
```bash
cd /root
if [ -d "comparely" ]; then
    mkdir -p backups
    tar -czf backups/comparely_backup_$(date +%Y%m%d_%H%M%S).tar.gz comparely
    mv comparely comparely_old_$(date +%Y%m%d_%H%M%S)
fi
```

**3. Update system:**
```bash
apt update
apt upgrade -y
```

**4. Install dependencies:**
```bash
apt install -y python3 python3-pip python3-venv nginx git
```

**5. Clone project:**
```bash
cd /root
git clone https://github.com/reyzae/comparely.git
cd comparely
```

**6. Setup virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**7. Install Python packages:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

**8. Setup .env:**
```bash
cp .env.example .env
nano .env
```

---

### ✅ METODE 3: Menggunakan WinSCP (Windows)

**1. Download WinSCP:**
- Link: https://winscp.net/eng/download.php

**2. Connect ke VPS:**
- Protocol: `SFTP`
- Host: `160.187.210.125`
- Port: `22`
- Username: `root`
- Password: `[PASSWORD_VPS]`

**3. Backup folder lama:**
- Jika ada folder `/root/comparely`, rename menjadi `/root/comparely_old_backup`

**4. Upload project:**
- Drag & drop folder `comparely` ke `/root/`

**5. Open Terminal (Ctrl+T) dan jalankan:**
```bash
cd /root/comparely
bash vps_commands.sh
```

---

## 🔧 Konfigurasi Setelah Deploy

### 1. Edit .env File

```bash
cd /root/comparely
nano .env
```

**Setting penting:**
```env
# Database (gunakan MySQL untuk production)
DATABASE_URL=mysql://user:password@localhost/comparely_db

# Secret Key (WAJIB GANTI!)
SECRET_KEY=your-secret-key-here

# AI API (opsional)
AI_API_KEY=your-xai-api-key

# Application
APP_NAME=COMPARELY
DEBUG=False
```

**Generate SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. Setup Database

**Jika pakai MySQL:**
```bash
# Login ke MySQL
mysql -u root -p

# Buat database
CREATE DATABASE comparely_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'comparely_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON comparely_db.* TO 'comparely_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**Initialize database:**
```bash
cd /root/comparely
source .venv/bin/activate
python scripts/utils/init_db.py
```

### 3. Buat Admin User

```bash
python scripts/utils/create_admin_simple.py
```

### 4. Test Aplikasi

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Buka browser: `http://160.187.210.125:8000`

Jika berhasil, tekan `Ctrl+C` untuk stop.

---

## 🔥 Setup Production (Systemd + Nginx)

### 1. Buat Systemd Service

```bash
sudo nano /etc/systemd/system/comparely.service
```

**Isi file:**
```ini
[Unit]
Description=COMPARELY FastAPI Application
After=network.target

[Service]
Type=notify
User=root
Group=root
WorkingDirectory=/root/comparely
Environment="PATH=/root/comparely/.venv/bin"
ExecStart=/root/comparely/.venv/bin/gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile /var/log/comparely/access.log \
    --error-logfile /var/log/comparely/error.log
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

**Buat log directory:**
```bash
mkdir -p /var/log/comparely
```

**Enable dan start service:**
```bash
systemctl daemon-reload
systemctl enable comparely
systemctl start comparely
systemctl status comparely
```

### 2. Setup Nginx

```bash
sudo nano /etc/nginx/sites-available/comparely
```

**Isi file:**
```nginx
server {
    listen 80;
    server_name 160.187.210.125;

    client_max_body_size 50M;

    access_log /var/log/nginx/comparely_access.log;
    error_log /var/log/nginx/comparely_error.log;

    location /static {
        alias /root/comparely/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

**Enable site:**
```bash
ln -s /etc/nginx/sites-available/comparely /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### 3. Setup Firewall

```bash
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
ufw status
```

---

## ✅ Verifikasi

### Check Services

```bash
# Check Gunicorn
systemctl status comparely

# Check Nginx
systemctl status nginx

# Check logs
tail -f /var/log/comparely/error.log
tail -f /var/log/nginx/comparely_error.log
```

### Test Aplikasi

Buka browser:
- **Homepage:** `http://160.187.210.125`
- **Admin Panel:** `http://160.187.210.125/admin/login`

---

## 🔄 Update Aplikasi di Kemudian Hari

```bash
cd /root/comparely
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
systemctl restart comparely
```

---

## 📦 Restore dari Backup

### List semua backup:
```bash
ls -lh /root/backups/
```

### Restore backup:
```bash
cd /root
tar -xzf backups/comparely_backup_YYYYMMDD_HHMMSS.tar.gz
systemctl restart comparely
```

---

## 🐛 Troubleshooting

### Service tidak start:
```bash
journalctl -u comparely -n 50
systemctl status comparely
```

### Nginx error:
```bash
nginx -t
tail -f /var/log/nginx/error.log
```

### Permission issues:
```bash
chown -R root:root /root/comparely
chmod +x /root/comparely
```

### Database connection error:
```bash
systemctl status mysql
mysql -u comparely_user -p comparely_db
```

---

## 📞 Quick Reference

### VPS Credentials
```
IP      : 160.187.210.125
User    : root
Password: [PASSWORD_VPS]
```

### Important Paths
```
Project     : /root/comparely
Backups     : /root/backups/
Logs        : /var/log/comparely/
Nginx Logs  : /var/log/nginx/
```

### Useful Commands
```bash
# Restart service
systemctl restart comparely

# View logs
journalctl -u comparely -f

# Check disk space
df -h

# Check memory
free -h

# Check processes
htop
```

---

## 📚 Dokumentasi Lengkap

Lihat file `DEPLOYMENT_VPS.md` untuk panduan lengkap dan detail.

---

**Deployment berhasil! 🎉**

Aplikasi COMPARELY sekarang live di: `http://160.187.210.125`
