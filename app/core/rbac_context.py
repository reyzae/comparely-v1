"""
Template context processors for RBAC
Add permission checking functions to all templates
"""

from app.models import User


def add_rbac_to_context(current_user: User) -> dict:
    """
    Add RBAC helper functions to template context.
    
    Usage in template:
        {% if can_create %}
            <button>Add New</button>
        {% endif %}
    """
    
    def has_role(role_name: str) -> bool:
        """Check if user has specific role"""
        if not current_user or not current_user.role:
            return False
        return current_user.role.name == role_name
    
    def has_any_role(role_names: list) -> bool:
        """Check if user has any of the specified roles"""
        if not current_user or not current_user.role:
            return False
        return current_user.role.name in role_names
    
    def can_create() -> bool:
        """Check if user can create resources"""
        if not current_user or not current_user.role:
            return False
        return current_user.role.name in ["Admin", "Super Admin"]
    
    def can_edit() -> bool:
        """Check if user can edit resources"""
        if not current_user or not current_user.role:
            return False
        return current_user.role.name in ["Admin", "Super Admin"]
    
    def can_delete() -> bool:
        """Check if user can delete resources"""
        if not current_user or not current_user.role:
            return False
        return current_user.role.name in ["Admin", "Super Admin"]
    
    def is_admin() -> bool:
        """Check if user is admin"""
        if not current_user or not current_user.role:
            return False
        return current_user.role.name in ["Admin", "Super Admin"]
    
    def is_viewer() -> bool:
        """Check if user is viewer (read-only)"""
        if not current_user or not current_user.role:
            return False
        return current_user.role.name == "Viewer"
    
    return {
        "has_role": has_role,
        "has_any_role": has_any_role,
        "can_create": can_create(),
        "can_edit": can_edit(),
        "can_delete": can_delete(),
        "is_admin": is_admin(),
        "is_viewer": is_viewer(),
        "user_role": current_user.role.name if current_user and current_user.role else "Guest"
    }
