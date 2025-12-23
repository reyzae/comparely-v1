# 🚀 Panduan Deployment COMPARELY ke VPS

Panduan lengkap untuk deploy aplikasi COMPARELY ke VPS (Ubuntu/Debian).

---

## 📋 Prasyarat

### VPS Requirements
- **OS**: Ubuntu 20.04+ atau Debian 11+
- **RAM**: Minimal 1GB (Rekomendasi 2GB+)
- **Storage**: Minimal 10GB
- **CPU**: 1 Core (Rekomendasi 2+ cores)
- **Domain**: (Opsional) untuk HTTPS

### Yang Perlu Disiapkan
- ✅ Akses SSH ke VPS
- ✅ Domain name (opsional, bisa pakai IP)
- ✅ File `.env` dengan konfigurasi production
- ✅ Database MySQL (atau gunakan SQLite)

---

## 🔧 Step 1: Persiapan VPS

### 1.1 Login ke VPS
```bash
ssh root@your-vps-ip
# atau
ssh username@your-vps-ip
```

### 1.2 Update System
```bash
sudo apt update
sudo apt upgrade -y
```

### 1.3 Install Dependencies
```bash
# Install Python 3.11+
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install Nginx
sudo apt install nginx -y

# Install Git
sudo apt install git -y

# Install MySQL (opsional, jika tidak pakai SQLite)
sudo apt install mysql-server -y
```

### 1.4 Buat User untuk Aplikasi (Recommended)
```bash
sudo adduser comparely
sudo usermod -aG sudo comparely
su - comparely
```

---

## 📦 Step 2: Clone & Setup Aplikasi

### 2.1 Clone Repository
```bash
cd /home/comparely
git clone https://github.com/reyzae/comparely.git
cd comparely
```

### 2.2 Setup Virtual Environment
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 2.3 Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn  # Production server
```

### 2.4 Setup Environment Variables
```bash
# Copy example
cp .env.example .env

# Edit .env
nano .env
```

**Konfigurasi `.env` untuk Production**:
```env
# Database (gunakan MySQL untuk production)
DATABASE_URL=mysql://username:password@localhost/comparely_db

# AI API (opsional)
AI_API_KEY=your-xai-api-key-here

# Session Secret (WAJIB GANTI!)
SECRET_KEY=GENERATE_NEW_SECURE_KEY_HERE

# Application
APP_NAME=COMPARELY
DEBUG=False
```

**Generate SECRET_KEY**:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2.5 Setup Database

**Jika pakai MySQL**:
```bash
# Login ke MySQL
sudo mysql

# Buat database dan user
CREATE DATABASE comparely_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'comparely_user'@'localhost' IDENTIFIED BY 'strong_password_here';
GRANT ALL PRIVILEGES ON comparely_db.* TO 'comparely_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**Inisialisasi Database**:
```bash
python scripts/utils/init_db.py
```

### 2.6 Buat Admin User
```bash
python scripts/utils/create_admin_simple.py
```

### 2.7 Import Data (Opsional)
```bash
python scripts/import_csv.py
```

---

## 🔥 Step 3: Setup Gunicorn (Production Server)

### 3.1 Test Gunicorn
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Jika berhasil, tekan `Ctrl+C` untuk stop.

### 3.2 Buat Systemd Service
```bash
sudo nano /etc/systemd/system/comparely.service
```

**Isi file** (sesuaikan path):
```ini
[Unit]
Description=COMPARELY FastAPI Application
After=network.target

[Service]
Type=notify
User=comparely
Group=comparely
WorkingDirectory=/home/comparely/comparely
Environment="PATH=/home/comparely/comparely/.venv/bin"
ExecStart=/home/comparely/comparely/.venv/bin/gunicorn app.main:app \
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

### 3.3 Buat Log Directory
```bash
sudo mkdir -p /var/log/comparely
sudo chown comparely:comparely /var/log/comparely
```

### 3.4 Enable & Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable comparely
sudo systemctl start comparely
sudo systemctl status comparely
```

**Perintah Berguna**:
```bash
# Check status
sudo systemctl status comparely

# Restart
sudo systemctl restart comparely

# Stop
sudo systemctl stop comparely

# View logs
sudo journalctl -u comparely -f
```

---

## 🌐 Step 4: Setup Nginx (Reverse Proxy)

### 4.1 Buat Nginx Config
```bash
sudo nano /etc/nginx/sites-available/comparely
```

**Isi file**:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;  # Ganti dengan domain Anda
    # Atau gunakan IP: server_name 123.456.789.0;

    client_max_body_size 50M;

    # Logs
    access_log /var/log/nginx/comparely_access.log;
    error_log /var/log/nginx/comparely_error.log;

    # Static files
    location /static {
        alias /home/comparely/comparely/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

### 4.2 Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/comparely /etc/nginx/sites-enabled/
sudo nginx -t  # Test konfigurasi
sudo systemctl restart nginx
```

---

## 🔒 Step 5: Setup SSL/HTTPS (Recommended)

### 5.1 Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 5.2 Dapatkan SSL Certificate
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

Ikuti prompt, pilih:
- Email untuk notifikasi
- Agree to terms
- Redirect HTTP to HTTPS: **Yes**

### 5.3 Auto-Renewal
```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot akan auto-renew via cron
```

---

## 🔥 Step 6: Setup Firewall

```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP & HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
sudo ufw status
```

---

## ✅ Step 7: Verifikasi Deployment

### 7.1 Check Services
```bash
# Check Gunicorn
sudo systemctl status comparely

# Check Nginx
sudo systemctl status nginx

# Check logs
sudo tail -f /var/log/comparely/error.log
sudo tail -f /var/log/nginx/comparely_error.log
```

### 7.2 Test Aplikasi
```bash
# Test dari server
curl http://localhost:8000

# Test dari browser
# http://your-domain.com
# atau
# http://your-vps-ip
```

### 7.3 Test Admin Panel
```
http://your-domain.com/admin/login
Username: admin
Password: (yang Anda set)
```

---

## 🔄 Update Aplikasi

Untuk update aplikasi di kemudian hari:

```bash
cd /home/comparely/comparely
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart comparely
```

---

## 📊 Monitoring & Maintenance

### Check Disk Space
```bash
df -h
```

### Check Memory
```bash
free -h
```

### Check Processes
```bash
htop
# atau
top
```

### Database Backup
```bash
# MySQL
mysqldump -u comparely_user -p comparely_db > backup_$(date +%Y%m%d).sql

# SQLite
cp comparely.db backup_$(date +%Y%m%d).db
```

### Log Rotation
Nginx dan systemd sudah auto-rotate logs. Untuk custom logs:

```bash
sudo nano /etc/logrotate.d/comparely
```

```
/var/log/comparely/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 comparely comparely
    sharedscripts
    postrotate
        systemctl reload comparely > /dev/null
    endscript
}
```

---

## 🐛 Troubleshooting

### Service Tidak Start
```bash
# Check logs
sudo journalctl -u comparely -n 50

# Check permissions
ls -la /home/comparely/comparely

# Check .env file
cat /home/comparely/comparely/.env
```

### Nginx Error
```bash
# Check config
sudo nginx -t

# Check logs
sudo tail -f /var/log/nginx/error.log
```

### Database Connection Error
```bash
# Check MySQL
sudo systemctl status mysql

# Test connection
mysql -u comparely_user -p comparely_db
```

### Permission Issues
```bash
# Fix ownership
sudo chown -R comparely:comparely /home/comparely/comparely

# Fix permissions
chmod +x /home/comparely/comparely
```

---

## 📝 Checklist Deployment

- [ ] VPS sudah siap (Ubuntu/Debian)
- [ ] Dependencies terinstall (Python, Nginx, MySQL)
- [ ] Repository di-clone
- [ ] Virtual environment dibuat
- [ ] Dependencies Python terinstall
- [ ] File `.env` dikonfigurasi (SECRET_KEY diganti!)
- [ ] Database dibuat dan diinisialisasi
- [ ] Admin user dibuat
- [ ] Gunicorn service berjalan
- [ ] Nginx dikonfigurasi
- [ ] SSL/HTTPS aktif (jika pakai domain)
- [ ] Firewall dikonfigurasi
- [ ] Aplikasi dapat diakses dari browser
- [ ] Admin panel berfungsi
- [ ] Backup strategy disetup

---

## 🎯 Performance Tips

1. **Gunicorn Workers**: `workers = (2 x CPU cores) + 1`
2. **Database**: Gunakan MySQL untuk production
3. **Caching**: Implementasi Redis (opsional)
4. **CDN**: Gunakan CDN untuk static files (opsional)
5. **Monitoring**: Setup monitoring (Grafana, Prometheus)

---

## 🆘 Support

Jika ada masalah:
1. Check logs: `sudo journalctl -u comparely -f`
2. Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
3. Restart services: `sudo systemctl restart comparely nginx`
4. Buat issue di GitHub

---

**Deployment berhasil! Aplikasi COMPARELY sekarang live di VPS! 🎉**
