# Scripts Directory

Utility scripts untuk maintenance dan development COMPARELY.

## 📁 Structure

```
scripts/
├── utils/              # Utility scripts
│   ├── create_admin_simple.py      # Create admin user
│   ├── reset_all_passwords.py      # Reset user passwords
│   ├── create_sample_users.py      # Create sample users
│   ├── update_routers_rbac.py      # Update routers with RBAC
│   ├── reset_database.py           # Reset database
│   └── init_db.py                  # Initialize database
├── import_csv.py       # Import devices from CSV
└── scrape_gsmarena.py  # Scrape data from GSMArena
```

## 🔧 Utility Scripts

### **create_admin_simple.py**
Create or reset admin user password.

```bash
python scripts/utils/create_admin_simple.py
```

### **reset_all_passwords.py**
Reset all user passwords to `[username]123` pattern.

```bash
python scripts/utils/reset_all_passwords.py
```

### **create_sample_users.py**
Create sample users for testing.

```bash
python scripts/utils/create_sample_users.py
```

### **reset_database.py**
Reset database to initial state.

```bash
python scripts/utils/reset_database.py
```

### **init_db.py**
Initialize database tables.

```bash
python scripts/utils/init_db.py
```

## 📊 Data Scripts

### **import_csv.py**
Import device data from CSV file.

```bash
python scripts/import_csv.py
```

### **scrape_gsmarena.py**
Scrape device data from GSMArena.

```bash
python scripts/scrape_gsmarena.py
```

## ⚠️ Important Notes

- Run scripts from project root directory
- Backup database before running reset scripts
- Scripts require active virtual environment
- Some scripts are interactive and require user input

## 🚀 Quick Start

### First Time Setup:
```bash
# 1. Initialize database
python scripts/utils/init_db.py

# 2. Create admin user
python scripts/utils/create_admin_simple.py

# 3. Import sample data (optional)
python scripts/import_csv.py
```

### Password Management:
```bash
# Reset all passwords
python scripts/utils/reset_all_passwords.py

# Create new admin
python scripts/utils/create_admin_simple.py
```

### Development:
```bash
# Create sample users for testing
python scripts/utils/create_sample_users.py

# Update routers with RBAC
python scripts/utils/update_routers_rbac.py
```
