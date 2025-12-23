"""
Script sederhana untuk membuat sample users dan roles
Jalankan dengan: python create_sample_users.py
"""

from app.database import SessionLocal
from app.models import User, Role

def create_sample_data():
    """Buat sample users dan roles untuk testing"""
    db = SessionLocal()
    
    try:
        # Cek apakah sudah ada roles
        existing_roles = db.query(Role).count()
        if existing_roles == 0:
            print("Membuat sample roles...")
            
            # Buat roles
            admin_role = Role(
                name="Admin",
                description="Administrator dengan akses penuh",
                permissions="all"
            )
            editor_role = Role(
                name="Editor",
                description="Dapat edit devices dan categories",
                permissions="edit_devices,edit_categories"
            )
            viewer_role = Role(
                name="Viewer",
                description="Hanya bisa melihat data",
                permissions="view_only"
            )
            
            db.add(admin_role)
            db.add(editor_role)
            db.add(viewer_role)
            db.commit()
            
            print("✅ 3 roles berhasil dibuat")
        else:
            print(f"Roles sudah ada ({existing_roles} roles)")
        
        # Cek apakah sudah ada users
        existing_users = db.query(User).count()
        if existing_users == 0:
            print("Membuat sample users...")
            
            # Get admin role
            admin_role = db.query(Role).filter(Role.name == "Admin").first()
            editor_role = db.query(Role).filter(Role.name == "Editor").first()
            
            # Buat users
            admin_user = User(
                username="admin",
                email="admin@comparely.com",
                hashed_password="admin123",  # Dalam production, gunakan bcrypt!
                full_name="Administrator",
                is_active=True,
                is_superuser=True,
                role_id=admin_role.id if admin_role else None
            )
            
            editor_user = User(
                username="editor",
                email="editor@comparely.com",
                hashed_password="editor123",
                full_name="Editor User",
                is_active=True,
                is_superuser=False,
                role_id=editor_role.id if editor_role else None
            )
            
            db.add(admin_user)
            db.add(editor_user)
            db.commit()
            
            print("✅ 2 users berhasil dibuat")
        else:
            print(f"Users sudah ada ({existing_users} users)")
        
        # Tampilkan summary
        print("\n" + "="*50)
        print("SUMMARY")
        print("="*50)
        print(f"Total Roles: {db.query(Role).count()}")
        print(f"Total Users: {db.query(User).count()}")
        print("\nSample login credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
