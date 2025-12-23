#!/bin/bash

# COMPARELY - Quick VPS Deployment Script
# Run this script on your VPS after cloning the repository

set -e  # Exit on error

echo "======================================"
echo "COMPARELY - VPS Deployment Script"
echo "======================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root or with sudo${NC}"
    exit 1
fi

echo -e "${GREEN}Step 1: Update system${NC}"
apt update && apt upgrade -y

echo -e "${GREEN}Step 2: Install dependencies${NC}"
apt install -y python3.11 python3.11-venv python3-pip nginx git mysql-server

echo -e "${GREEN}Step 3: Create application user${NC}"
if ! id "comparely" &>/dev/null; then
    adduser --disabled-password --gecos "" comparely
    echo "User 'comparely' created"
else
    echo "User 'comparely' already exists"
fi

echo -e "${GREEN}Step 4: Setup application directory${NC}"
APP_DIR="/home/comparely/comparely"

if [ ! -d "$APP_DIR" ]; then
    echo "Please clone the repository first:"
    echo "  cd /home/comparely"
    echo "  git clone https://github.com/reyzae/comparely.git"
    exit 1
fi

cd $APP_DIR

echo -e "${GREEN}Step 5: Setup virtual environment${NC}"
sudo -u comparely python3.11 -m venv .venv
sudo -u comparely .venv/bin/pip install --upgrade pip
sudo -u comparely .venv/bin/pip install -r requirements.txt
sudo -u comparely .venv/bin/pip install gunicorn

echo -e "${GREEN}Step 6: Setup environment file${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}Please edit .env file and configure:${NC}"
    echo "  - DATABASE_URL"
    echo "  - SECRET_KEY (generate with: python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
    echo "  - AI_API_KEY (optional)"
    echo ""
    read -p "Press Enter after editing .env file..."
fi

echo -e "${GREEN}Step 7: Setup MySQL database${NC}"
read -p "Do you want to setup MySQL database? (y/n): " setup_mysql
if [ "$setup_mysql" = "y" ]; then
    read -p "Enter database name [comparely_db]: " db_name
    db_name=${db_name:-comparely_db}
    
    read -p "Enter database user [comparely_user]: " db_user
    db_user=${db_user:-comparely_user}
    
    read -sp "Enter database password: " db_pass
    echo ""
    
    mysql -e "CREATE DATABASE IF NOT EXISTS $db_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    mysql -e "CREATE USER IF NOT EXISTS '$db_user'@'localhost' IDENTIFIED BY '$db_pass';"
    mysql -e "GRANT ALL PRIVILEGES ON $db_name.* TO '$db_user'@'localhost';"
    mysql -e "FLUSH PRIVILEGES;"
    
    echo "Database created successfully!"
    echo "Update your .env file with:"
    echo "DATABASE_URL=mysql://$db_user:$db_pass@localhost/$db_name"
fi

echo -e "${GREEN}Step 8: Initialize database${NC}"
sudo -u comparely .venv/bin/python scripts/utils/init_db.py

echo -e "${GREEN}Step 9: Create admin user${NC}"
sudo -u comparely .venv/bin/python scripts/utils/create_admin_simple.py

echo -e "${GREEN}Step 10: Setup systemd service${NC}"
cat > /etc/systemd/system/comparely.service << EOF
[Unit]
Description=COMPARELY FastAPI Application
After=network.target

[Service]
Type=notify
User=comparely
Group=comparely
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/.venv/bin"
ExecStart=$APP_DIR/.venv/bin/gunicorn app.main:app \\
    --workers 4 \\
    --worker-class uvicorn.workers.UvicornWorker \\
    --bind 0.0.0.0:8000 \\
    --access-logfile /var/log/comparely/access.log \\
    --error-logfile /var/log/comparely/error.log
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

mkdir -p /var/log/comparely
chown comparely:comparely /var/log/comparely

systemctl daemon-reload
systemctl enable comparely
systemctl start comparely

echo -e "${GREEN}Step 11: Setup Nginx${NC}"
read -p "Enter your domain name (or IP address): " domain_name

cat > /etc/nginx/sites-available/comparely << EOF
server {
    listen 80;
    server_name $domain_name;

    client_max_body_size 50M;

    access_log /var/log/nginx/comparely_access.log;
    error_log /var/log/nginx/comparely_error.log;

    location /static {
        alias $APP_DIR/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF

ln -sf /etc/nginx/sites-available/comparely /etc/nginx/sites-enabled/
nginx -t && systemctl restart nginx

echo -e "${GREEN}Step 12: Setup firewall${NC}"
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
echo "y" | ufw enable

echo -e "${GREEN}Step 13: Setup SSL (optional)${NC}"
read -p "Do you want to setup SSL with Let's Encrypt? (y/n): " setup_ssl
if [ "$setup_ssl" = "y" ]; then
    apt install -y certbot python3-certbot-nginx
    certbot --nginx -d $domain_name
fi

echo ""
echo "======================================"
echo -e "${GREEN}Deployment Complete!${NC}"
echo "======================================"
echo ""
echo "Application is running at:"
echo "  http://$domain_name"
echo "  http://$domain_name/admin/login"
echo ""
echo "Useful commands:"
echo "  sudo systemctl status comparely    # Check status"
echo "  sudo systemctl restart comparely   # Restart app"
echo "  sudo journalctl -u comparely -f    # View logs"
echo ""
echo "Next steps:"
echo "  1. Test the application in browser"
echo "  2. Login to admin panel"
echo "  3. Import sample data (optional)"
echo "  4. Setup monitoring (optional)"
echo ""
