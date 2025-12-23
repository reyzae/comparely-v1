#!/bin/bash
# ========================================
# COMPARELY - Quick Deploy Script
# ========================================
# Copy dan paste script ini ke SSH terminal VPS Anda
# ========================================

BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
PROJECT_PATH="/root/comparely"
BACKUP_PATH="/root/backups"
GITHUB_REPO="https://github.com/reyzae/comparely.git"

echo ""
echo "========================================"
echo "  COMPARELY VPS Deployment"
echo "========================================"
echo "Backup Date: $BACKUP_DATE"
echo ""

# Step 1: Create backup directory
echo "[1/9] Creating backup directory..."
mkdir -p $BACKUP_PATH

# Step 2: Backup existing project
echo "[2/9] Backing up existing project..."
if [ -d "$PROJECT_PATH" ]; then
    echo "Existing project found. Creating backup..."
    tar -czf $BACKUP_PATH/comparely_backup_$BACKUP_DATE.tar.gz -C /root comparely 2>/dev/null
    
    if [ -f "$BACKUP_PATH/comparely_backup_$BACKUP_DATE.tar.gz" ]; then
        echo "✓ Backup created successfully!"
        echo "  Location: $BACKUP_PATH/comparely_backup_$BACKUP_DATE.tar.gz"
        echo "  Size: $(du -h $BACKUP_PATH/comparely_backup_$BACKUP_DATE.tar.gz | cut -f1)"
    else
        echo "⚠ Backup failed, but continuing..."
    fi
    
    echo "Moving old project..."
    mv $PROJECT_PATH ${PROJECT_PATH}_old_$BACKUP_DATE
    echo "✓ Old project moved to: ${PROJECT_PATH}_old_$BACKUP_DATE"
else
    echo "No existing project found. Fresh installation."
fi

# Step 3: Update system
echo ""
echo "[3/9] Updating system packages..."
apt update -y > /dev/null 2>&1
echo "✓ System updated"

# Step 4: Install dependencies
echo ""
echo "[4/9] Installing dependencies..."
apt install -y python3 python3-pip python3-venv nginx git curl > /dev/null 2>&1
echo "✓ Dependencies installed"

# Step 5: Clone project
echo ""
echo "[5/9] Cloning project from GitHub..."
cd /root
git clone $GITHUB_REPO 2>&1 | grep -E "(Cloning|done)"

if [ ! -d "$PROJECT_PATH" ]; then
    echo "✗ ERROR: Failed to clone project!"
    echo "Please check your internet connection and GitHub repository."
    exit 1
fi
echo "✓ Project cloned successfully"

# Step 6: Setup virtual environment
echo ""
echo "[6/9] Setting up Python virtual environment..."
cd $PROJECT_PATH
python3 -m venv .venv
source .venv/bin/activate
echo "✓ Virtual environment created"

# Step 7: Install Python dependencies
echo ""
echo "[7/9] Installing Python packages..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
pip install gunicorn > /dev/null 2>&1
echo "✓ Python packages installed"

# Step 8: Setup environment file
echo ""
echo "[8/9] Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ .env file created from template"
else
    echo "✓ .env file already exists"
fi

# Step 9: Initialize database (optional, commented out)
echo ""
echo "[9/9] Database initialization..."
echo "⚠ Skipping database init (run manually after .env configuration)"

# Summary
echo ""
echo "========================================"
echo "  Deployment Summary"
echo "========================================"
echo ""

if [ -f "$BACKUP_PATH/comparely_backup_$BACKUP_DATE.tar.gz" ]; then
    echo "📦 Backup:"
    echo "   Location: $BACKUP_PATH/comparely_backup_$BACKUP_DATE.tar.gz"
    echo "   Size: $(du -h $BACKUP_PATH/comparely_backup_$BACKUP_DATE.tar.gz | cut -f1)"
    echo ""
fi

if [ -d "${PROJECT_PATH}_old_$BACKUP_DATE" ]; then
    echo "📁 Old Project:"
    echo "   Location: ${PROJECT_PATH}_old_$BACKUP_DATE"
    echo ""
fi

echo "📂 New Project:"
echo "   Location: $PROJECT_PATH"
echo "   Python: $(python3 --version)"
echo ""

echo "========================================"
echo "  Next Steps"
echo "========================================"
echo ""
echo "1️⃣  Configure Environment:"
echo "   nano $PROJECT_PATH/.env"
echo ""
echo "   Important settings to update:"
echo "   - DATABASE_URL (if using MySQL)"
echo "   - SECRET_KEY (generate new one!)"
echo "   - AI_API_KEY (if using AI features)"
echo ""
echo "2️⃣  Generate Secret Key:"
echo "   python3 -c 'import secrets; print(secrets.token_urlsafe(32))'"
echo ""
echo "3️⃣  Initialize Database:"
echo "   cd $PROJECT_PATH"
echo "   source .venv/bin/activate"
echo "   python scripts/utils/init_db.py"
echo ""
echo "4️⃣  Create Admin User:"
echo "   python scripts/utils/create_admin_simple.py"
echo ""
echo "5️⃣  Test Application:"
echo "   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"
echo "   # Press Ctrl+C to stop after testing"
echo ""
echo "6️⃣  Setup Systemd Service:"
echo "   See: $PROJECT_PATH/DEPLOYMENT_VPS.md (Step 3)"
echo ""
echo "7️⃣  Setup Nginx:"
echo "   See: $PROJECT_PATH/DEPLOYMENT_VPS.md (Step 4)"
echo ""
echo "8️⃣  Setup SSL (Optional):"
echo "   See: $PROJECT_PATH/DEPLOYMENT_VPS.md (Step 5)"
echo ""
echo "========================================"
echo "  Useful Commands"
echo "========================================"
echo ""
echo "View all backups:"
echo "  ls -lh $BACKUP_PATH/"
echo ""
echo "Restore from backup:"
echo "  tar -xzf $BACKUP_PATH/comparely_backup_YYYYMMDD_HHMMSS.tar.gz -C /root"
echo ""
echo "Check disk space:"
echo "  df -h"
echo ""
echo "Check memory:"
echo "  free -h"
echo ""
echo "========================================"
echo "  Deployment completed at: $(date)"
echo "========================================"
echo ""
