"""
Auto-update all admin routers to include RBAC context.
This script adds RBAC context to all template responses.
"""

import re
import os

ROUTERS_DIR = "app/routers/admin"

# Routers to update
ROUTERS = [
    "dashboard.py",
    "categories.py",
    "users.py",
    "analytics.py",
    "tools.py",
    "settings.py",
    "activity_logs.py",
    "bulk_operations.py"
]

def update_router(filepath):
    """Update a router file to include RBAC context"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already updated
    if 'from app.core.rbac_context import add_rbac_to_context' in content:
        print(f"✓ {os.path.basename(filepath)} - Already updated")
        return False
    
    # Add import
    import_line = "from app.core.rbac_context import add_rbac_to_context\n"
    
    # Find where to insert import (after other imports)
    if 'from .auth import get_current_user' in content:
        content = content.replace(
            'from .auth import get_current_user',
            'from .auth import get_current_user\n' + import_line
        )
    else:
        # Insert after first import block
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('from app.') or line.startswith('from .'):
                lines.insert(i+1, import_line.strip())
                break
        content = '\n'.join(lines)
    
    # Find and update templates.TemplateResponse calls
    # Pattern: templates.TemplateResponse(\n    "template.html",\n    {\n        "request": request,\n        "current_user": get_current_user(request, db),
    
    # Replace get_current_user inline calls with variable
    pattern = r'("current_user":\s*)get_current_user\(request,\s*db\)'
    
    def replace_func(match):
        return match.group(1) + 'current_user'
    
    content = re.sub(pattern, replace_func, content)
    
    # Add current_user variable and rbac_context before TemplateResponse
    # Find all TemplateResponse blocks
    pattern = r'(return templates\.TemplateResponse\(\s*"[^"]+",\s*\{)'
    
    def add_rbac_context(match):
        # Check if there's already current_user assignment before this
        return match.group(1)
    
    # Add current_user and rbac_context assignment before each TemplateResponse
    # This is complex, so we'll do it manually for now
    
    # Simple approach: Add these lines before each TemplateResponse if not present
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a TemplateResponse line
        if 'return templates.TemplateResponse(' in line:
            # Check if current_user is already assigned in previous lines
            has_current_user = False
            has_rbac = False
            
            for j in range(max(0, i-10), i):
                if 'current_user = get_current_user' in lines[j]:
                    has_current_user = True
                if 'rbac_context = add_rbac_to_context' in lines[j]:
                    has_rbac = True
            
            # Add assignments if not present
            if not has_current_user:
                indent = len(line) - len(line.lstrip())
                new_lines.append(' ' * indent + 'current_user = get_current_user(request, db)')
            
            if not has_rbac:
                indent = len(line) - len(line.lstrip())
                new_lines.append(' ' * indent + 'rbac_context = add_rbac_to_context(current_user)')
                new_lines.append('')  # Empty line
            
            # Add the TemplateResponse line
            new_lines.append(line)
            
            # Check next lines for the context dict
            i += 1
            while i < len(lines):
                new_lines.append(lines[i])
                # Look for "current_user": line in context
                if '"current_user":' in lines[i] and 'current_user' in lines[i]:
                    # Add **rbac_context after current_user line
                    indent = len(lines[i]) - len(lines[i].lstrip())
                    new_lines.append(' ' * indent + '**rbac_context,  # Add RBAC permissions')
                if lines[i].strip() == '}' or lines[i].strip() == '},':
                    break
                i += 1
        else:
            new_lines.append(line)
        
        i += 1
    
    content = '\n'.join(new_lines)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ {os.path.basename(filepath)} - Updated")
    return True

def main():
    print("=" * 70)
    print("AUTO-UPDATE ROUTERS WITH RBAC CONTEXT")
    print("=" * 70)
    
    updated_count = 0
    
    for router in ROUTERS:
        filepath = os.path.join(ROUTERS_DIR, router)
        if os.path.exists(filepath):
            if update_router(filepath):
                updated_count += 1
        else:
            print(f"✗ {router} - File not found")
    
    print("\n" + "=" * 70)
    print(f"DONE! Updated {updated_count} routers")
    print("=" * 70)
    print("\nNext: Update templates to use RBAC variables")
    print("  - can_create, can_edit, can_delete")
    print("  - is_admin, is_viewer")

if __name__ == "__main__":
    main()
