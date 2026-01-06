# 📱 COMPARELY - Device Comparison Platform

![CI Status](https://github.com/reyzae/comparely-v1/workflows/CI%20-%20COMPARELY/badge.svg)

A modern web application for comparing and recommending technology devices (smartphones & laptops) built with **Python FastAPI** and **AI-powered recommendations**.

---

## ✨ Key Features

### 🌐 Public Features
- **Modern Web Interface**: Responsive design with consistent UI
- **Device Search**: Search devices by name, brand, or specifications
- **Side-by-Side Comparison**: Compare 2 devices in detail
- **🤖 AI-Powered Comparison**: Smart analysis using xAI Grok
- **Smart Recommendations**: Get recommendations based on budget and needs
- **🧠 AI Recommendations**: Personalized suggestions based on your use case
- **Filter & Sort**: Filter by category, brand, year, and price
- **Responsive Design**: Optimized for desktop, tablet, and mobile

### 🔐 Admin Panel
- **Dashboard Analytics**: Complete statistics with charts and visualizations
- **Device Management**: Full CRUD operations with bulk actions
- **Category Management**: Manage device categories
- **User Management**: Manage users and roles
- **Role-Based Access Control (RBAC)**: Super Admin, Admin, and Viewer roles
- **Activity Logs**: Track all admin activities
- **CSV Import/Export**: Bulk data operations
- **Tools & Utilities**: Database optimization and cache management

---

## 🛠️ Tech Stack

**Backend**
- Python 3.11+ & FastAPI
- SQLAlchemy ORM
- SQLite/MySQL Database
- xAI Grok for AI features
- bcrypt for security

**Frontend**
- Jinja2 Templates
- Vanilla CSS
- Responsive Design

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/reyzae/comparely-v1.git
cd comparely-v1
```

### 2. Setup Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
```bash
# Copy example file
cp .env.example .env

# Edit .env and configure:
# - DATABASE_URL (SQLite by default)
# - AI_API_KEY (optional, for AI features)
# - SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
```

### 5. Initialize Database
```bash
python scripts/utils/init_db.py
```

### 6. Create Admin User
```bash
python scripts/utils/create_admin_simple.py
# Follow prompts to create admin user
# Default: admin / admin123
```

### 7. Run Application
```bash
uvicorn app.main:app --reload

# Available at:
# - Public: http://localhost:8000
# - Admin: http://localhost:8000/admin/login
```

---

## 📚 Documentation

For detailed documentation, see the `/docs` folder:
- Authentication Guide
- RBAC Implementation
- API Documentation
- Deployment Guide

---

## 🔒 Security Features

- Bcrypt password hashing
- Session management with encrypted cookies
- Role-based access control
- SQL injection prevention (SQLAlchemy)
- XSS protection (Jinja2 auto-escaping)

**⚠️ Important**: Change default admin password after first login!

---

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 📞 Support

For issues, questions, or suggestions:
- **GitHub Issues**: [Create an issue](https://github.com/reyzae/comparely-v1/issues)
- **Documentation**: Check the `/docs` folder

---

**Built with ❤️ using Python & FastAPI**
