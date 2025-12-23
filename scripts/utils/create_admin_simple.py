"""
Create admin user with direct bcrypt (no passlib)
"""

from app.database import SessionLocal
from app.models import User, Role
import bcrypt
from datetime import datetime

def create_admin_simple():
    db = SessionLocal()
    
    try:
        # Check/create admin role
        admin_role = db.query(Role).filter(Role.name == "Admin").first()
        if not admin_role:
            admin_role = Role(
                name="Admin",
                description="Full access",
                permissions="all"
            )
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)
        
        # Check if admin exists
        admin = db.query(User).filter(User.username == "admin").first()
        
        if admin:
            print(f"Admin exists: {admin.username}")
            choice = input("Reset password? (y/n): ")
            if choice.lower() != 'y':
                return
        else:
            admin = User(
                username="admin",
                email="admin@comparely.com",
                full_name="Administrator",
                role_id=admin_role.id,
                is_active=True,
                is_verified=True
            )
        
        # Set password
        password = "admin123"
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        admin.password_hash = hashed.decode('utf-8')
        
        if admin.id is None:
            db.add(admin)
        
        db.commit()
        
        print("\n✅ Admin user ready!")
        print(f"Username: admin")
        print(f"Password: {password}")
        print(f"Hash: {admin.password_hash[:50]}...")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_simple()
