"""
Cleanup script - Remove temporary and unused files
"""

import os
import shutil

# Files to remove (temporary/development scripts)
FILES_TO_REMOVE = [
    "check_roles.py",
    "cleanup_csv.py",
    "create_admin.py",  # Keep create_admin_simple.py instead
    "debug_admin.py",
    "fix_password.py",
    "generate_hash.py",
    "reset_admin_password.py",
    "update_password_manual.py",
    "recreate_user_tables.py",
    "rescrape_complete.py",
    "test_scraper.py",
]

# Directories to remove
DIRS_TO_REMOVE = [
    "__pycache__",
]

# Files to keep (important)
IMPORTANT_FILES = [
    "create_admin_simple.py",  # For creating admin users
    "reset_all_passwords.py",  # For password management
    "import_csv.py",  # For importing data
    "scrape_gsmarena.py",  # For scraping data
    "reset_database.py",  # For database reset
    "init_db.py",  # For database initialization
    "update_routers_rbac.py",  # For RBAC updates
    "create_sample_users.py",  # For creating sample users
]

def cleanup():
    """Remove temporary files and organize structure"""
    
    print("=" * 70)
    print("CLEANUP - REMOVING TEMPORARY FILES")
    print("=" * 70)
    
    removed_count = 0
    
    # Remove files
    for filename in FILES_TO_REMOVE:
        filepath = filename
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"✓ Removed: {filename}")
                removed_count += 1
            except Exception as e:
                print(f"✗ Error removing {filename}: {e}")
        else:
            print(f"  Skip: {filename} (not found)")
    
    # Remove directories
    for dirname in DIRS_TO_REMOVE:
        dirpath = dirname
        if os.path.exists(dirpath) and os.path.isdir(dirpath):
            try:
                shutil.rmtree(dirpath)
                print(f"✓ Removed directory: {dirname}")
                removed_count += 1
            except Exception as e:
                print(f"✗ Error removing {dirname}: {e}")
    
    print("\n" + "=" * 70)
    print(f"CLEANUP COMPLETE - {removed_count} items removed")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print("IMPORTANT FILES KEPT:")
    print("=" * 70)
    for filename in IMPORTANT_FILES:
        if os.path.exists(filename):
            print(f"  ✓ {filename}")
    
    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("1. Review remaining files")
    print("2. Commit changes: git add -A && git commit -m 'chore: cleanup temporary files'")
    print("3. Push to GitHub: git push origin main")

if __name__ == "__main__":
    cleanup()
