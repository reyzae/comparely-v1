# ========================================
# Auto Deploy ke VPS via SSH
# ========================================
# Script otomatis untuk backup dan deploy
# ========================================

$VpsIp = "160.187.210.125"
$VpsUser = "root"
$VpsPassword = "[PASSWORD_VPS]"
$BackupDate = Get-Date -Format "yyyyMMdd_HHmmss"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  COMPARELY Auto Deploy to VPS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "VPS IP      : $VpsIp" -ForegroundColor White
Write-Host "Username    : $VpsUser" -ForegroundColor White
Write-Host "Backup Date : $BackupDate" -ForegroundColor White
Write-Host ""

# Commands yang akan dijalankan di VPS
$vpsCommands = @"
echo '========================================'
echo '  Step 1: Creating Backup Directory'
echo '========================================'
mkdir -p /root/backups

echo ''
echo '========================================'
echo '  Step 2: Backup Existing Project'
echo '========================================'
if [ -d '/root/comparely' ]; then
    echo 'Existing project found. Creating backup...'
    tar -czf /root/backups/comparely_backup_$BackupDate.tar.gz -C /root comparely 2>/dev/null
    if [ -f '/root/backups/comparely_backup_$BackupDate.tar.gz' ]; then
        echo 'Backup created: /root/backups/comparely_backup_$BackupDate.tar.gz'
        du -h /root/backups/comparely_backup_$BackupDate.tar.gz
    fi
    
    echo 'Moving old project...'
    mv /root/comparely /root/comparely_old_$BackupDate
    echo 'Old project moved to: /root/comparely_old_$BackupDate'
else
    echo 'No existing project found. Skipping backup.'
fi

echo ''
echo '========================================'
echo '  Step 3: Update System'
echo '========================================'
apt update -y

echo ''
echo '========================================'
echo '  Step 4: Install Dependencies'
echo '========================================'
apt install -y python3 python3-pip python3-venv nginx git curl

echo ''
echo '========================================'
echo '  Step 5: Clone Project from GitHub'
echo '========================================'
cd /root
git clone https://github.com/reyzae/comparely.git

if [ ! -d '/root/comparely' ]; then
    echo 'ERROR: Failed to clone project!'
    exit 1
fi

echo ''
echo '========================================'
echo '  Step 6: Setup Virtual Environment'
echo '========================================'
cd /root/comparely
python3 -m venv .venv
source .venv/bin/activate

echo ''
echo '========================================'
echo '  Step 7: Install Python Dependencies'
echo '========================================'
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

echo ''
echo '========================================'
echo '  Step 8: Setup Environment File'
echo '========================================'
if [ ! -f '.env' ]; then
    cp .env.example .env
    echo '.env file created from .env.example'
fi

echo ''
echo '========================================'
echo '  Deployment Summary'
echo '========================================'
echo ''
echo 'Backup Location:'
if [ -f '/root/backups/comparely_backup_$BackupDate.tar.gz' ]; then
    ls -lh /root/backups/comparely_backup_$BackupDate.tar.gz
fi
echo ''
echo 'Old Project Location:'
if [ -d '/root/comparely_old_$BackupDate' ]; then
    echo '/root/comparely_old_$BackupDate'
fi
echo ''
echo 'New Project Location:'
echo '/root/comparely'
echo ''
echo '========================================'
echo '  Next Steps'
echo '========================================'
echo '1. Edit .env file:'
echo '   nano /root/comparely/.env'
echo ''
echo '2. Initialize database:'
echo '   cd /root/comparely'
echo '   source .venv/bin/activate'
echo '   python scripts/utils/init_db.py'
echo ''
echo '3. Create admin user:'
echo '   python scripts/utils/create_admin_simple.py'
echo ''
echo '4. Setup systemd service (see DEPLOYMENT_VPS.md)'
echo '5. Setup Nginx (see DEPLOYMENT_VPS.md)'
echo ''
echo 'Deployment completed at: $(date)'
echo '========================================'
"@

# Simpan commands ke file temporary
$tempScript = Join-Path $env:TEMP "vps_deploy_$BackupDate.sh"
$vpsCommands | Out-File -FilePath $tempScript -Encoding UTF8

Write-Host "========================================" -ForegroundColor Green
Write-Host "  Deployment Options" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "OPTION 1: Manual SSH (Recommended)" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Connect to VPS:" -ForegroundColor White
Write-Host "   ssh $VpsUser@$VpsIp" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Copy and paste these commands:" -ForegroundColor White
Write-Host ""
Write-Host $vpsCommands -ForegroundColor DarkGray
Write-Host ""

Write-Host "OPTION 2: Using PuTTY" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Open PuTTY" -ForegroundColor White
Write-Host "2. Host: $VpsIp" -ForegroundColor White
Write-Host "3. Port: 22" -ForegroundColor White
Write-Host "4. Click 'Open'" -ForegroundColor White
Write-Host "5. Login with:" -ForegroundColor White
Write-Host "   Username: $VpsUser" -ForegroundColor Gray
Write-Host "   Password: $VpsPassword" -ForegroundColor Gray
Write-Host "6. Run the commands above" -ForegroundColor White
Write-Host ""

Write-Host "OPTION 3: Using WinSCP + PuTTY" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Download WinSCP: https://winscp.net" -ForegroundColor White
Write-Host "2. Connect to VPS and upload project folder" -ForegroundColor White
Write-Host "3. Open PuTTY from WinSCP (Ctrl+P)" -ForegroundColor White
Write-Host "4. Run: bash /root/comparely/vps_commands.sh" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Quick Reference" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "VPS Credentials:" -ForegroundColor White
Write-Host "  IP      : $VpsIp" -ForegroundColor Gray
Write-Host "  User    : $VpsUser" -ForegroundColor Gray
Write-Host "  Password: $VpsPassword" -ForegroundColor Gray
Write-Host ""
Write-Host "Backup Info:" -ForegroundColor White
Write-Host "  Location: /root/backups/" -ForegroundColor Gray
Write-Host "  Filename: comparely_backup_$BackupDate.tar.gz" -ForegroundColor Gray
Write-Host ""
Write-Host "Project Paths:" -ForegroundColor White
Write-Host "  New     : /root/comparely" -ForegroundColor Gray
Write-Host "  Old     : /root/comparely_old_$BackupDate" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "  Files Ready!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Generated files:" -ForegroundColor White
Write-Host "  vps_commands.sh      - VPS setup script" -ForegroundColor Gray
Write-Host "  connect_vps.ps1      - Quick SSH connect" -ForegroundColor Gray
Write-Host "  auto_deploy_ssh.ps1  - This script" -ForegroundColor Gray
Write-Host ""
Write-Host "Documentation:" -ForegroundColor White
Write-Host "  DEPLOYMENT_VPS.md    - Complete deployment guide" -ForegroundColor Gray
Write-Host ""
