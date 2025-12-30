#!/bin/bash

# COMPARELY Deployment Script
# This script automates the deployment process on the VPS

set -e  # Exit on error

echo "========================================="
echo "🚀 COMPARELY Deployment Script"
echo "========================================="

# Configuration
APP_DIR="/home/comparely/comparely"
BACKUP_DIR="/home/comparely/backups"
VENV_DIR="$APP_DIR/.venv"
LOG_DIR="/var/log/comparely"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}ℹ️  $1${NC}"
}

log_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Create backup directory if not exists
mkdir -p "$BACKUP_DIR"

# Navigate to app directory
cd "$APP_DIR"

# Step 1: Backup database
log_info "Backing up database..."
if [ -f "comparely.db" ]; then
    BACKUP_FILE="$BACKUP_DIR/comparely_$(date +%Y%m%d_%H%M%S).db"
    cp comparely.db "$BACKUP_FILE"
    log_info "Database backed up to: $BACKUP_FILE"
    
    # Keep only last 10 backups
    ls -t "$BACKUP_DIR"/comparely_*.db | tail -n +11 | xargs -r rm
    log_info "Old backups cleaned (kept last 10)"
else
    log_warn "No database file found to backup"
fi

# Step 2: Pull latest code
log_info "Pulling latest code from repository..."
git fetch origin
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
log_info "Current branch: $CURRENT_BRANCH"
git reset --hard origin/"$CURRENT_BRANCH"
log_info "Code updated successfully"

# Step 3: Activate virtual environment
log_info "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Step 4: Update dependencies
log_info "Updating dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
log_info "Dependencies updated"

# Step 5: Run database migrations (if applicable)
# Uncomment if using Alembic or other migration tool
# log_info "Running database migrations..."
# alembic upgrade head

# Step 6: Collect static files (if applicable)
# Uncomment if needed
# log_info "Collecting static files..."
# python scripts/collect_static.py

# Step 7: Run tests (optional)
if [ "$RUN_TESTS" = "true" ]; then
    log_info "Running tests..."
    pytest tests/ -v
fi

# Step 8: Restart application
log_info "Restarting application service..."
sudo systemctl restart comparely

# Wait for service to start
sleep 5

# Step 9: Verify deployment
log_info "Verifying deployment..."
if sudo systemctl is-active --quiet comparely; then
    log_info "✅ Service is running"
else
    log_error "❌ Service failed to start"
    log_error "Checking logs..."
    sudo journalctl -u comparely -n 50 --no-pager
    exit 1
fi

# Step 10: Health check
log_info "Running health check..."
if curl -f http://localhost:8000/ &> /dev/null; then
    log_info "✅ Application is responding"
else
    log_warn "⚠️  Application is not responding on port 8000"
fi

# Step 11: Log deployment
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) - Deployment completed successfully" >> "$LOG_DIR/deployments.log"

echo ""
echo "========================================="
echo "✅ Deployment completed successfully!"
echo "========================================="
echo "Deployed branch: $CURRENT_BRANCH"
echo "Deployed at: $(date)"
echo "========================================="

exit 0
