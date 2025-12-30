# 🔄 CI/CD Setup Guide untuk COMPARELY

Panduan lengkap untuk menggunakan CI/CD pipeline yang sudah dikonfigurasi untuk project COMPARELY.

---

## 📋 Overview

Pipeline CI/CD ini mencakup:
- ✅ **Continuous Integration (CI)**: Automated testing, code quality, dan security checks
- 🚀 **Continuous Deployment (CD)**: Automated deployment ke VPS
- 🔒 **Security Scanning**: Vulnerability dan dependency checks
- 📊 **Code Quality**: Formatting, linting, dan complexity analysis

---

## 🔐 Setup GitHub Secrets

Sebelum deployment dapat berjalan, Anda perlu mengkonfigurasi GitHub Secrets:

### 1. Buka Repository Settings
- Pergi ke repository GitHub: https://github.com/reyzae/comparely-v1
- Click **Settings** → **Secrets and variables** → **Actions**

### 2. Tambahkan Secrets Berikut

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `VPS_HOST` | IP address atau hostname VPS | `103.123.45.67` atau `comparely.example.com` |
| `VPS_USERNAME` | Username untuk SSH ke VPS | `comparely` |
| `VPS_SSH_KEY` | Private SSH key untuk akses VPS | Isi dari file `~/.ssh/id_rsa` |
| `VPS_DB_PASSWORD` | Password database production | `your_secure_password` |
| `SECRET_KEY` | Application secret key | Generate dengan: `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `AI_API_KEY` | xAI API key (optional) | `xai-...` |

### 3. Generate SSH Key (Jika Belum Ada)

```bash
# Di komputer lokal
ssh-keygen -t rsa -b 4096 -C "github-actions@comparely"

# Copy public key ke VPS
ssh-copy-id -i ~/.ssh/id_rsa.pub username@vps-host

# Copy private key untuk GitHub Secret
cat ~/.ssh/id_rsa
# Copy seluruh output ke VPS_SSH_KEY secret
```

---

## 🔄 Workflows

### 1. **CI Workflow** (`ci.yml`)

**Trigger:** Push atau Pull Request ke `main`, `master`, atau `develop`

**Apa yang dilakukan:**
- ✅ Run tests dengan pytest
- ✅ Code quality checks (black, isort, flake8)
- ✅ Security scanning (bandit, safety)
- ✅ Upload coverage reports
- ✅ Validate database models

**Status Badge:**
```markdown
![CI Status](https://github.com/reyzae/comparely-v1/workflows/CI%20-%20COMPARELY/badge.svg)
```

### 2. **CD Deployment** (`cd-deploy.yml`)

**Trigger:** 
- Push ke `main` atau `master` (automatic)
- Manual trigger via GitHub Actions UI

**Apa yang dilakukan:**
- 📦 Backup database
- 📥 Pull latest code
- 📦 Install dependencies
- 🔄 Restart service
- 🏥 Health check
- 🔙 Rollback jika gagal

**Manual Deployment:**
1. Buka GitHub Actions tab
2. Pilih workflow "CD - Deploy to VPS"
3. Click "Run workflow"
4. Pilih environment (production/staging)
5. Click "Run workflow" button

### 3. **Security Scan** (`security-scan.yml`)

**Trigger:**
- Scheduled (setiap Senin jam 00:00 UTC)
- Push ke `main` atau `master`
- Manual trigger

**Apa yang dilakukan:**
- 🔍 Scan vulnerabilities dengan Bandit
- 🔍 Check dependency vulnerabilities (Safety, pip-audit)
- 🔍 Secret detection dengan TruffleHog
- 📊 Upload security reports

### 4. **Code Quality** (`code-quality.yml`)

**Trigger:** Pull Request ke `main`, `master`, atau `develop`

**Apa yang dilakukan:**
- 🎨 Code formatting check (Black)
- 📦 Import sorting (isort)
- 🔍 Linting (flake8, pylint)
- 📝 Type checking (mypy)
- 📊 Complexity analysis (radon)

---

## 🎯 Cara Menggunakan

### Push Code Baru

```bash
# Di komputer lokal
git add .
git commit -m "Add new feature"
git push origin main
```

**Apa yang terjadi:**
1. ✅ CI workflow otomatis running (test, quality checks)
2. ✅ Security scan running (jika push ke main)
3. 🚀 CD workflow otomatis deploy ke VPS (jika push ke main)
4. 📧 Notifikasi email dari GitHub (jika diaktifkan)

### Buat Pull Request

```bash
git checkout -b feature/new-feature
# Make changes
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

**Apa yang terjadi:**
1. ✅ CI workflow running
2. ✅ Code Quality workflow running
3. 📊 Results posted as PR comment
4. ⚠️  PR tidak bisa merge jika checks failed (opsional)

---

## 📊 Monitoring

### Melihat Status Workflows

1. Buka repository di GitHub
2. Go to **Actions** tab
3. Lihat list workflows dan status mereka

### Melihat Logs

1. Click pada workflow run
2. Click pada job yang ingin dilihat
3. Expand steps untuk melihat detailed logs

### Download Artifacts

Beberapa workflows menghasilkan artifacts (coverage reports, security reports):

1. Go to workflow run
2. Scroll ke bawah ke **Artifacts** section
3. Download files

---

## 🐛 Troubleshooting

### Deployment Gagal

**Check:**
1. GitHub Secrets sudah dikonfigurasi dengan benar?
2. SSH key valid dan bisa akses VPS?
3. VPS service running?
4. Check deployment logs di GitHub Actions

**Manual Fix:**
```bash
# SSH ke VPS
ssh username@vps-host

# Check service status
sudo systemctl status comparely

# Check logs
sudo journalctl -u comparely -n 100

# Manual restart
sudo systemctl restart comparely
```

### Tests Gagal

**Local Testing:**
```bash
# Jalankan tests lokal
pytest tests/ -v

# Run specific test
pytest tests/test_basic.py -v

# Run with coverage
pytest --cov=app tests/
```

### Security Scan Menemukan Vulnerabilities

1. Check security report di Artifacts
2. Update vulnerable dependencies:
   ```bash
   pip install --upgrade package-name
   pip freeze > requirements.txt
   ```
3. Commit dan push update

---

## 🔄 Rollback

### Manual Rollback

```bash
# SSH ke VPS
ssh username@vps-host
cd /home/comparely/comparely

# Lihat available backups
ls -lt /home/comparely/backups/

# Restore backup
cp /home/comparely/backups/comparely_YYYYMMDD_HHMMSS.db comparely.db

# Restart service
sudo systemctl restart comparely
```

### Git Rollback

```bash
# Di komputer lokal
git log --oneline  # Find commit to rollback to

git revert <commit-hash>
# atau
git reset --hard <commit-hash>
git push origin main --force  # Hati-hati dengan force push!
```

---

## 📝 Best Practices

### Before Pushing

```bash
# Format code
black app/ tests/ scripts/

# Sort imports
isort app/ tests/ scripts/

# Run tests locally
pytest tests/

# Check code quality
flake8 app/ tests/ scripts/
```

### Branch Strategy

```
main/master     → Production (auto-deploy)
develop         → Development (CI only)
feature/*       → Features (CI + Code Quality)
hotfix/*        → Hotfixes (CI + Fast-track to main)
```

### Commit Messages

```
feat: Add new comparison feature
fix: Fix database connection issue
docs: Update deployment guide
test: Add tests for user authentication
refactor: Improve recommendation algorithm
```

---

## 🔧 Maintenance

### Update Dependencies

```bash
# Check for updates
pip list --outdated

# Update dependencies
pip install --upgrade package-name
pip freeze > requirements.txt

# Test locally
pytest tests/

# Commit and push
git add requirements.txt
git commit -m "chore: Update dependencies"
git push
```

### Review Security Reports

- Check GitHub Security tab regularly
- Enable Dependabot alerts
- Review weekly security scan results

---

## 📞 Support

**Issues:**
- GitHub Issues: https://github.com/reyzae/comparely-v1/issues
- Check workflow logs di GitHub Actions
- Review documentation di `/docs`

**Quick Commands:**
```bash
# Check CI status
git push && open https://github.com/reyzae/comparely-v1/actions

# Manual deploy
# Go to: Actions → CD - Deploy to VPS → Run workflow

# Check VPS
ssh username@vps-host "sudo systemctl status comparely"
```

---

## ✅ Checklist Setup

- [ ] GitHub Secrets dikonfigurasi
- [ ] SSH key setup untuk VPS
- [ ] VPS sudah ada systemd service `comparely`
- [ ] Test push code → CI running
- [ ] Test manual deployment → CD running
- [ ] Review security scan results
- [ ] Setup branch protection rules (optional)
- [ ] Enable email notifications (optional)

---

**🎉 CI/CD Pipeline siap digunakan! Every push akan otomatis di-test dan di-deploy!**
