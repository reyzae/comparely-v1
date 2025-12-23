# ========================================
# COMPARELY - VPS Deployment Script
# ========================================
# Script untuk backup dan deploy ke VPS
# Author: Reyza
# Date: 2025-12-22
# ========================================

param(
    [string]$VpsIp = "160.187.210.125",
    [string]$VpsUser = "root",
    [string]$VpsPassword = "[PASSWORD_VPS]",
    [string]$ProjectPath = "/root/comparely",
    [string]$BackupPath = "/root/backups"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  COMPARELY VPS Deployment Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check project files
Write-Host "[1/4] Checking project files..." -ForegroundColor Green

$requiredFiles = @(
    "app",
    "requirements.txt",
    ".env.example",
    "README.md"
)

foreach ($file in $requiredFiles) {
    $filePath = Join-Path $PSScriptRoot $file
    if (Test-Path $filePath) {
        Write-Host "  [OK] $file found" -ForegroundColor Green
    }
    else {
        Write-Host "  [X] $file NOT found" -ForegroundColor Red
    }
}
Write-Host ""

# Step 2: Generate backup date
Write-Host "[2/4] Preparing deployment..." -ForegroundColor Green
$backupDate = Get-Date -Format "yyyyMMdd_HHmmss"
Write-Host "Backup timestamp: $backupDate" -ForegroundColor White
Write-Host ""

# Step 3: Generate VPS commands
Write-Host "[3/4] Generating VPS setup script..." -ForegroundColor Green

$vpsScriptContent = @"
#!/bin/bash
# ========================================
# VPS Deployment Commands
# Run this script on your VPS
# ========================================

BACKUP_DATE="$backupDate"
PROJECT_PATH="/root/comparely"
BACKUP_PATH="/root/backups"

echo "========================================="
echo "  COMPARELY VPS Setup"
echo "========================================="
echo ""

# Create backup directory
echo "[1/8] Creating backup directory..."
mkdir -p `$BACKUP_PATH

# Backup existing project
echo "[2/8] Backing up existing project..."
if [ -d "`$PROJECT_PATH" ]; then
    echo "Existing project found. Creating backup..."
    tar -czf `$BACKUP_PATH/comparely_backup_`$BACKUP_DATE.tar.gz -C /root comparely
    echo "Backup saved to: `$BACKUP_PATH/comparely_backup_`$BACKUP_DATE.tar.gz"
    
    # Move old project
    mv `$PROJECT_PATH `$PROJECT_PATH`_old_`$BACKUP_DATE
    echo "Old project moved to: `$PROJECT_PATH`_old_`$BACKUP_DATE"
else
    echo "No existing project found. Skipping backup."
fi

# Update system
echo "[3/8] Updating system..."
apt update
apt upgrade -y

# Install dependencies
echo "[4/8] Installing dependencies..."
apt install -y python3 python3-pip python3-venv nginx git

# Clone project (if using Git)
echo "[5/8] Cloning project..."
cd /root
# Uncomment if you want to clone from GitHub:
# git clone https://github.com/reyzae/comparely.git

# If project already uploaded, skip to next step
if [ ! -d "`$PROJECT_PATH" ]; then
    echo "ERROR: Project not found at `$PROJECT_PATH"
    echo "Please upload the project first or clone from Git."
    exit 1
fi

# Setup virtual environment
echo "[6/8] Setting up virtual environment..."
cd `$PROJECT_PATH
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
echo "[7/8] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Setup .env
echo "[8/8] Setting up environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "IMPORTANT: Edit .env file with your configuration!"
    echo "Run: nano .env"
fi

echo ""
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file: nano .env"
echo "2. Initialize database: python scripts/utils/init_db.py"
echo "3. Create admin user: python scripts/utils/create_admin_simple.py"
echo "4. Setup systemd service (see DEPLOYMENT_VPS.md)"
echo "5. Setup Nginx (see DEPLOYMENT_VPS.md)"
echo ""
echo "Backup location: `$BACKUP_PATH/comparely_backup_`$BACKUP_DATE.tar.gz"
echo ""
"@

$sshCommandsFile = Join-Path $PSScriptRoot "vps_commands.sh"
$vpsScriptContent | Out-File -FilePath $sshCommandsFile -Encoding UTF8
Write-Host "  [OK] Generated: vps_commands.sh" -ForegroundColor Green

# Step 4: Generate quick connect script
$connectScriptContent = @"
# Quick VPS Connect Script
Write-Host "Connecting to VPS..." -ForegroundColor Green
Write-Host "IP: $VpsIp" -ForegroundColor White
Write-Host "User: $VpsUser" -ForegroundColor White
Write-Host ""

ssh $VpsUser@$VpsIp
"@

$quickConnectFile = Join-Path $PSScriptRoot "connect_vps.ps1"
$connectScriptContent | Out-File -FilePath $quickConnectFile -Encoding UTF8
Write-Host "  [OK] Generated: connect_vps.ps1" -ForegroundColor Green

Write-Host ""
Write-Host "[4/4] Deployment Instructions" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "VPS Details:" -ForegroundColor Yellow
Write-Host "  IP Address : $VpsIp" -ForegroundColor White
Write-Host "  Username   : $VpsUser" -ForegroundColor White
Write-Host "  Password   : $VpsPassword" -ForegroundColor White
Write-Host "  Project    : $ProjectPath" -ForegroundColor White
Write-Host ""

Write-Host "OPTION 1: Deploy via Git (RECOMMENDED)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Push project ke GitHub (jika belum):" -ForegroundColor White
Write-Host "   git add ." -ForegroundColor Gray
Write-Host "   git commit -m 'Ready for deployment'" -ForegroundColor Gray
Write-Host "   git push origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Connect ke VPS:" -ForegroundColor White
Write-Host "   ssh $VpsUser@$VpsIp" -ForegroundColor Gray
Write-Host "   Password: $VpsPassword" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Jalankan commands berikut di VPS:" -ForegroundColor White
Write-Host ""
Write-Host "   # Backup existing project (if any)" -ForegroundColor DarkGray
Write-Host "   cd /root" -ForegroundColor Gray
Write-Host "   if [ -d 'comparely' ]; then" -ForegroundColor Gray
Write-Host "       tar -czf /root/backups/comparely_backup_$backupDate.tar.gz comparely" -ForegroundColor Gray
Write-Host "       mv comparely comparely_old_$backupDate" -ForegroundColor Gray
Write-Host "   fi" -ForegroundColor Gray
Write-Host ""
Write-Host "   # Clone new version" -ForegroundColor DarkGray
Write-Host "   git clone https://github.com/reyzae/comparely.git" -ForegroundColor Gray
Write-Host "   cd comparely" -ForegroundColor Gray
Write-Host ""
Write-Host "   # Setup environment" -ForegroundColor DarkGray
Write-Host "   python3 -m venv .venv" -ForegroundColor Gray
Write-Host "   source .venv/bin/activate" -ForegroundColor Gray
Write-Host "   pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "   pip install gunicorn" -ForegroundColor Gray
Write-Host ""
Write-Host "   # Configure .env" -ForegroundColor DarkGray
Write-Host "   cp .env.example .env" -ForegroundColor Gray
Write-Host "   nano .env" -ForegroundColor Gray
Write-Host ""

Write-Host "OPTION 2: Deploy via WinSCP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Download WinSCP: https://winscp.net/eng/download.php" -ForegroundColor White
Write-Host ""
Write-Host "2. Connect to VPS:" -ForegroundColor White
Write-Host "   Host    : $VpsIp" -ForegroundColor Gray
Write-Host "   User    : $VpsUser" -ForegroundColor Gray
Write-Host "   Password: $VpsPassword" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Backup existing /root/comparely (if exists)" -ForegroundColor White
Write-Host "   - Rename to: comparely_old_$backupDate" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Upload project folder to /root/comparely" -ForegroundColor White
Write-Host ""
Write-Host "5. Open PuTTY/SSH and run: bash /root/comparely/vps_commands.sh" -ForegroundColor White
Write-Host ""

Write-Host "OPTION 3: Quick SSH Commands" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Copy file vps_commands.sh ke VPS, lalu jalankan:" -ForegroundColor White
Write-Host "   bash vps_commands.sh" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Files Generated" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  vps_commands.sh  - Setup script untuk VPS" -ForegroundColor White
Write-Host "  connect_vps.ps1  - Quick connect ke VPS" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Need Help?" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Lihat panduan lengkap di: DEPLOYMENT_VPS.md" -ForegroundColor White
Write-Host ""
