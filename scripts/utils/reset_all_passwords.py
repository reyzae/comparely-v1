"""
Bulk Password Reset Tool
Reset password untuk semua user atau user tertentu dengan bcrypt hash yang benar.
"""

from app.database import SessionLocal
from app.models import User
import bcrypt

def hash_password(password: str) -> str:
    """Hash password dengan bcrypt"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def reset_all_users():
    """Reset password semua user ke default password"""
    db = SessionLocal()
    
    try:
        # Get all users
        users = db.query(User).all()
        
        if not users:
            print("❌ No users found in database!")
            return
        
        print("=" * 70)
        print(f"FOUND {len(users)} USERS")
        print("=" * 70)
        
        for user in users:
            print(f"\n{user.id}. {user.username} ({user.email}) - Role ID: {user.role_id}")
        
        print("\n" + "=" * 70)
        print("RESET OPTIONS")
        print("=" * 70)
        print("1. Reset ALL users to default password (username123)")
        print("2. Reset specific user")
        print("3. Cancel")
        
        choice = input("\nChoose option (1/2/3): ").strip()
        
        if choice == "1":
            # Reset all users
            default_password_template = "{username}123"  # admin -> admin123, tegar -> tegar123
            
            confirm = input(f"\n⚠️  Reset ALL {len(users)} users to password: [username]123? (y/n): ")
            if confirm.lower() != 'y':
                print("Cancelled.")
                return
            
            updated_count = 0
            for user in users:
                password = default_password_template.format(username=user.username)
                hashed = hash_password(password)
                user.password_hash = hashed
                updated_count += 1
                print(f"✓ {user.username} -> password: {password}")
            
            db.commit()
            
            print("\n" + "=" * 70)
            print(f"✅ {updated_count} users updated successfully!")
            print("=" * 70)
            print("\nLOGIN CREDENTIALS:")
            for user in users:
                print(f"  - {user.username} / {user.username}123")
            print("=" * 70)
            
        elif choice == "2":
            # Reset specific user
            username = input("\nEnter username: ").strip()
            user = db.query(User).filter(User.username == username).first()
            
            if not user:
                print(f"❌ User '{username}' not found!")
                return
            
            print(f"\nUser found: {user.username} ({user.email})")
            new_password = input("Enter new password: ").strip()
            
            if not new_password:
                print("❌ Password cannot be empty!")
                return
            
            hashed = hash_password(new_password)
            user.password_hash = hashed
            db.commit()
            
            print("\n✅ Password updated!")
            print(f"Username: {user.username}")
            print(f"Password: {new_password}")
            
        else:
            print("Cancelled.")
            return
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


def quick_reset_admin():
    """Quick reset untuk admin user saja"""
    db = SessionLocal()
    
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        
        if not admin:
            print("❌ Admin user not found!")
            return
        
        password = "admin123"
        hashed = hash_password(password)
        admin.password_hash = hashed
        db.commit()
        
        print("✅ Admin password reset!")
        print(f"Username: admin")
        print(f"Password: {password}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick-admin":
        quick_reset_admin()
    else:
        reset_all_users()
